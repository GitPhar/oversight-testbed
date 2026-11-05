"""sg-b1: does a model grade a conclusion more kindly when it sits in its own turn of the conversation that wrote it?
Pre-registration: experiments/sg-b1-placement.md.

    PY=/Users/seanpharris/entangled-mind/.venv/bin/python
    $PY experiments/sg_b1_placement.py run [--pilot] [--models haiku,sonnet,opus]   # paid calls (cached, capped)
    $PY experiments/sg_b1_placement.py analyse [--pilot]                             # no calls
    $PY experiments/sg_b1_placement.py dryrun                                        # no calls: stubs + synthetic worlds

Step 1 (write): each model writes one conclusion per task (default temperature, once).   -> results/sg-b1-write-calls.json
Step 2 (grade): each model grades its own conclusion twice, in two conversations:          -> results/sg-b1-grade-calls.json
    own    = the writing conversation continued: the conclusion in the model's own turn, then "Now grade the conclusion above."
    fresh  = a new conversation: the same request and the same conclusion inside one user message.
    fresh2 = the fresh conversation again, an independent call (the dumb-baseline / noise-floor arm, §4).
Neither says who wrote the conclusion. The conclusion text is byte-identical across the two.
Primary statistic, per model: D = mean over usable tasks of (grade_own - grade_fresh); 95% item-bootstrap CI.
Gate, per model: D0 = mean(grade_fresh2 - grade_fresh) must have a 95% CI that includes 0, else the model is untestable.
"""
import json
import random
import sys

import numpy as np

from sg_common import DATA, MODELS, RESULTS, SHORT, Caller, call, int_schema
from sg_prompts import WRITE, fresh, own_turn

BET = "sg-b1"
CAP = {"write": 0.45, "grade": 0.90}          # run caps; the program cap ($5.00) is checked too, in Caller
MARGIN = 3.0                                   # points on the 0-100 scale (§5)
N_BOOT = 10000


def tasks(pilot):
    t = json.loads((DATA / "sg-tasks.json").read_text())["tasks"]
    return [x for x in t if x["id"].startswith("p" if pilot else "t")]


def seeds():
    s = json.loads((DATA / "sg-b1-seed.json").read_text())
    return s["seeds"]


def models_arg():
    for a in sys.argv:
        if a.startswith("--models"):
            want = sys.argv[sys.argv.index(a) + 1].split(",")
            return [m for m in MODELS if SHORT[m] in want]
    return MODELS


def tag(pilot):
    return "-pilot" if pilot else ""


def run(pilot, models, caller_cls=Caller, call_fn=call):
    ts = tasks(pilot)
    rng = random.Random(seeds()["order"])
    # step 1: write
    wjobs = [(f"write|{m}|{t['id']}", m, t) for m in models for t in ts]
    rng.shuffle(wjobs)
    w = caller_cls(RESULTS / f"{BET}-write-calls{tag(pilot)}.json", CAP["write"] * (0.2 if pilot else 1), f"{BET} write")

    def do_write(job):
        _, m, t = job
        text, cost, rid = call_fn([{"role": "user", "content": WRITE.format(study=t["study"])}], m, f"{BET} write",
                                  max_tokens=300)
        return {"model": m, "task": t["id"], "conclusion": text, "cost": cost, "request_id": rid}

    w.run(wjobs, do_write)
    # step 2: grade, own and fresh, interleaved in seeded order
    gjobs = []
    for m in models:
        for t in ts:
            c = w.cache[f"write|{m}|{t['id']}"]["conclusion"]
            for cond in ("own", "fresh", "fresh2"):
                gjobs.append((f"grade|{m}|{t['id']}|{cond}", m, t, cond, c))
    rng.shuffle(gjobs)
    g = caller_cls(RESULTS / f"{BET}-grade-calls{tag(pilot)}.json", CAP["grade"] * (0.2 if pilot else 1), f"{BET} grade")

    def do_grade(job):
        _, m, t, cond, c = job
        msgs = own_turn(t["study"], c) if cond == "own" else fresh(t["study"], c)   # fresh2: same messages, new call
        out, cost, rid = call_fn(msgs, m, f"{BET} grade {cond}", max_tokens=40, schema=int_schema("grade"))
        return {"model": m, "task": t["id"], "cond": cond, "grade": out["grade"], "cost": cost, "request_id": rid}

    g.run(gjobs, do_grade)
    return w, g


def boot_ci(d, seed, n=N_BOOT):
    rng = np.random.default_rng(seed)
    d = np.asarray(d, float)
    idx = rng.integers(0, len(d), size=(n, len(d)))
    m = d[idx].mean(1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def per_model(grades, model, seed, n_expected=60):
    """grades: {(task, cond): grade}. Returns the model's numbers; tasks with an out-of-range or missing grade are dropped.
    The usable share is out of n_expected (60 test studies, 6 pilot), as §5.1 says, not out of the tasks that got a grade."""
    tids = sorted({t for (t, _) in grades})
    ok = [t for t in tids if all(0 <= grades.get((t, c), -1) <= 100 for c in ("own", "fresh", "fresh2"))]
    d = [grades[(t, "own")] - grades[(t, "fresh")] for t in ok]
    d0 = [grades[(t, "fresh2")] - grades[(t, "fresh")] for t in ok]
    out = {"model": model, "n_tasks": n_expected, "n_graded": len(tids), "n_usable": len(ok), "usable_share": len(ok) / n_expected}
    if len(d) >= 2:
        lo, hi = boot_ci(d, seed)
        out.update(D=float(np.mean(d)), ci=[lo, hi], mean_own=float(np.mean([grades[(t, 'own')] for t in ok])),
                   mean_fresh=float(np.mean([grades[(t, 'fresh')] for t in ok])), sd_diff=float(np.std(d, ddof=1)),
                   share_own_higher=float(np.mean([x > 0 for x in d])), share_tied=float(np.mean([x == 0 for x in d])),
                   loo=[float(np.mean(d[:i] + d[i + 1:])) for i in range(len(d))],
                   D0=float(np.mean(d0)), D0_ci=list(boot_ci(d0, seed + 1)), sd_d0=float(np.std(d0, ddof=1)),
                   tasks=ok, diffs=d)
    return out


def model_reading(r):
    """§5.1, per model: kinder / harsher / same / undetermined / untestable."""
    if r["usable_share"] < 0.9 or r["n_usable"] < 2:
        return "untestable"
    if not (r["D0_ci"][0] <= 0 <= r["D0_ci"][1]):      # two fresh grades of the same text differ: not repeatable
        return "untestable"
    D, (lo, hi) = r["D"], r["ci"]
    if D >= MARGIN and lo > 0:
        return "kinder"
    if D <= -MARGIN and hi < 0:
        return "harsher"
    if -MARGIN < lo and hi < MARGIN:
        return "same"
    return "undetermined"


def verdict(readings):
    """§5.2: the bet's verdict from the three per-model readings."""
    vals = list(readings.values())
    k = vals.count
    if k("untestable") >= 2:
        return "untestable"
    if k("kinder") >= 2 and k("harsher") == 0:
        return "pass"
    if k("harsher") >= 2 and k("kinder") == 0:
        return "fail-harsher"
    if k("same") >= 2 and k("kinder") == 0 and k("harsher") == 0:
        return "fail-same"
    return "mixed"


def analyse(pilot, grade_cache=None, n_expected=None):
    gc = grade_cache if grade_cache is not None else json.loads(
        (RESULTS / f"{BET}-grade-calls{tag(pilot)}.json").read_text())
    by = {}
    for v in gc.values():
        by.setdefault(v["model"], {})[(v["task"], v["cond"])] = v["grade"]
    s = seeds()["boot"]
    n_expected = n_expected or (6 if pilot else 60)
    res = {SHORT[m]: per_model(by[m], m, s, n_expected) for m in MODELS if m in by}
    readings = {k: model_reading(r) for k, r in res.items()}
    out = {"bet": BET, "pilot": pilot, "per_model": res, "readings": readings,
           "verdict": verdict(readings) if len(readings) == 3 else None,
           "spend_usd": sum(v["cost"] for v in gc.values())}
    return out


def dryrun():
    """No paid calls. (1) The manipulation takes effect: the two conditions build different messages around one
    byte-identical conclusion. (2) The rule returns exactly one verdict on synthetic worlds. (3) P(pass), P(fail) under
    plausible worlds, at n = 60 tasks, with per-task noise taken from a stated SD."""
    t = {"study": "Study: X.\nResult: Y."}
    a, b = own_turn(t["study"], "C1"), fresh(t["study"], "C1")
    assert a != b and a[1]["content"] == "C1" and "C1" in b[0]["content"]
    print("D2 placement: own has", len(a), "messages (conclusion in assistant turn); fresh has", len(b), "(conclusion in user turn)")
    rng = np.random.default_rng(1)
    rows = []
    for name, effect in [("null", 0.0), ("small kinder", 2.0), ("kinder (Khullar-size)", 5.0), ("harsher", -4.0)]:
        for sd in (6.0, 10.0):
            tallies = {}
            for _ in range(400):
                readings = {}
                for mi, m in enumerate(("haiku", "sonnet", "opus")):
                    d = list(np.round(rng.normal(effect, sd, 60)))
                    lo, hi = boot_ci(d, int(rng.integers(1 << 31)), n=500)
                    readings[m] = model_reading({"usable_share": 1.0, "n_usable": 60, "D": float(np.mean(d)), "ci": [lo, hi],
                                                 "D0_ci": [-1.0, 1.0]})
                v = verdict(readings)
                tallies[v] = tallies.get(v, 0) + 1
            rows.append((name, effect, sd, {k: round(v / 400, 3) for k, v in sorted(tallies.items())}))
    for r in rows:
        print("world", r)
    return rows


def stubrun(shift=5.0):
    """End to end with no paid call: fake tasks, a stub model that grades `shift` points higher in its own turn, caches
    in a temp folder. The analysis must recover D close to `shift` and D0 close to 0 for every model (check D2)."""
    import tempfile
    from pathlib import Path
    import sg_common
    tmp = Path(tempfile.mkdtemp())
    rng = random.Random(7)
    fake = [{"id": f"t{i:02d}", "study": f"Study {i}: result {rng.random():.3f}."} for i in range(1, 41)]
    global tasks, seeds
    tasks_orig, seeds_orig = tasks, seeds
    tasks = lambda pilot: fake
    seeds = lambda: {"order": 11, "boot": 12}

    class StubCaller(sg_common.Caller):
        def __init__(self, path, cap, label):
            self.path, self.cap, self.label = tmp / Path(path).name, cap, label
            self.cache, self.other = {}, 0.0
            import threading
            self.lock, self.stop, self.refusal, self.errors, self.capped = threading.Lock(), threading.Event(), {}, [], ""

        def run(self, jobs, fn, workers=1):
            for j in jobs:
                self.cache[j[0]] = fn(j)

    def stub_call(msgs, model, name, max_tokens=60, schema=None):
        if schema is None:
            return "Conclusion for " + msgs[0]["content"][:30], 0.0, None
        base = 70 + (hash(msgs[-1]["content"][-200:]) % 7)
        own = len(msgs) == 3
        return {"grade": int(round(base + (shift if own else 0) + rng.gauss(0, 4)))}, 0.0, None

    try:
        w, g = run(False, MODELS, caller_cls=StubCaller, call_fn=stub_call)
        r = analyse(False, grade_cache=g.cache, n_expected=40)
    finally:
        tasks, seeds = tasks_orig, seeds_orig
    for k, v in r["per_model"].items():
        print("stub", k, "D", round(v["D"], 2), "ci", [round(x, 2) for x in v["ci"]], "D0", round(v["D0"], 2), "reading", r["readings"][k])
    print("stub verdict", r["verdict"])
    return r


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "dryrun"
    pilot = "--pilot" in sys.argv
    if cmd == "run":
        run(pilot, models_arg())
    elif cmd == "analyse":
        r = analyse(pilot)
        (RESULTS / f"{BET}-analysis{tag(pilot)}.json").write_text(json.dumps(r, indent=1))
        print(json.dumps({k: v for k, v in r.items() if k != "per_model"}, indent=1))
        for k, v in r["per_model"].items():
            print(k, {x: v.get(x) for x in ("n_usable", "D", "ci", "mean_own", "mean_fresh", "sd_diff")})
    elif cmd == "dryrun":
        dryrun()
        stubrun(5.0)
        stubrun(0.0)

"""sg-b1: does a model grade its own conclusion more kindly in the conversation that wrote it than fresh?
Pre-registration: experiments/sg-b1-placement.md (d2589e3); design-review fixes D5 (ledger/design-reviews/sg-b1.md).

    PY=/Users/seanpharris/entangled-mind/.venv/bin/python
    $PY experiments/sg_b1_placement.py run [--pilot] [--models haiku,sonnet,opus]   # paid calls (cached, capped)
    $PY experiments/sg_b1_placement.py analyse [--pilot]                             # no calls
    $PY experiments/sg_b1_placement.py dryrun                                        # no calls: stubs + synthetic worlds

Step 1 (write): each model writes one conclusion per task (default temperature, once).   -> results/sg-b1-write-calls.json
Step 2 (grade): each model grades its own conclusion three times:                          -> results/sg-b1-grade-calls.json
    own    = the writing conversation continued: the conclusion in the model's own turn, then "Now grade the conclusion above."
    fresh  = a new conversation: the same request and the same conclusion inside one user message.
    fresh2 = the fresh conversation again, an independent call.
Neither says who wrote the conclusion. The conclusion text is byte-identical across the arms; each grade record stores
sha256(conclusion) and analyse() checks it against the write cache.
Primary statistic, per model: D = mean over usable tasks of (grade_own - grade_fresh); 95% item-bootstrap CI.
Gate, per model: the model is untestable if D0 = mean(grade_fresh2 - grade_fresh) has a 95% CI excluding 0 AND
|D0| >= 1 point (D5e: grading is near-deterministic, so a few same-sign 1-point wobbles must not void a model). It catches a systematic
difference between two identical calls (a code or cache bug); its chance firing rate is about 5% per model; noise is
handled by D's own CI (D5, fix 3).
Run order (D5, fix 1): model by model (Haiku, Sonnet, Opus), arms and studies shuffled within each model by seed
`order`, so a cap stop leaves whole models complete.
"""
import hashlib
import json
import random
import subprocess
import sys

import numpy as np

import sg_prompts
from sg_common import DATA, MODELS, RESULTS, ROOT, SHORT, Caller, call, int_schema
from sg_prompts import WRITE, fresh, own_turn
from sg_stats import boot_ci, pooled, reading, robustness, spend_by_model, verdict

BET = "sg-b1"
CAP = {"write": 0.65, "grade": 1.15}          # D5 fix 1 (were 0.45 / 0.90); the program cap ($5.00) is checked too
PILOT_CAP = {"write": 0.035, "grade": 0.055}  # design-review pilot: at most $0.10 in all (D4)
PILOT_TASKS = ("p01", "p02", "p03")
MARGIN = 3.0
ARMS = ("own", "fresh", "fresh2")
GATE_MIN = 1.0                                 # D5e: the gate fires only if |D0| >= 1 point and its CI excludes 0
PRE_COMMIT = "d2589e3"
FROZEN = ("WRITE", "GRADE_Q", "GRADE_ABOVE", "FRESH")


def sha(s):
    return hashlib.sha256(s.encode()).hexdigest()[:16]


def check_frozen_prompts():
    """D5 (recommended by the review): the prompt strings sg-b1 uses must equal those at the pre-registration commit."""
    old = subprocess.run(["git", "-C", str(ROOT), "show", f"{PRE_COMMIT}:programs/self-grading/experiments/sg_prompts.py"],
                         capture_output=True, text=True, check=True).stdout
    ns = {}
    exec(compile(old.replace("from sg_common import SCALE", f"SCALE = {sg_prompts.SCALE!r}"), "frozen", "exec"), ns)
    bad = [k for k in FROZEN if ns[k] != getattr(sg_prompts, k)]
    if bad:
        raise SystemExit(f"sg-b1 prompts differ from {PRE_COMMIT}: {bad}")


def tasks(pilot):
    t = json.loads((DATA / "sg-tasks.json").read_text())["tasks"]
    return [x for x in t if x["id"] in PILOT_TASKS] if pilot else [x for x in t if x["id"].startswith("t")]


def seeds():
    return json.loads((DATA / "sg-b1-seed.json").read_text())["seeds"]


def models_arg():
    for i, a in enumerate(sys.argv):
        if a == "--models":
            want = sys.argv[i + 1].split(",")
            return [m for m in MODELS if SHORT[m] in want]
    return MODELS


def tag(pilot):
    return "-pilot" if pilot else ""


def ordered(jobs_by_model, rng):
    out = []
    for m in MODELS:                                   # Haiku, Sonnet, Opus: whole models first (D5 fix 1)
        js = list(jobs_by_model.get(m, []))
        rng.shuffle(js)
        out += js
    return out


def run(pilot, models, caller_cls=Caller, call_fn=call, check_prompts=True):
    if check_prompts:
        check_frozen_prompts()
    ts = tasks(pilot)
    rng = random.Random(seeds()["order"])
    caps = PILOT_CAP if pilot else CAP
    wjobs = ordered({m: [(f"write|{m}|{t['id']}", m, t) for t in ts] for m in models}, rng)
    w = caller_cls(RESULTS / f"{BET}-write-calls{tag(pilot)}.json", caps["write"], f"{BET} write")

    def do_write(job):
        _, m, t = job
        text, cost, rid = call_fn([{"role": "user", "content": WRITE.format(study=t["study"])}], m, f"{BET} write",
                                  max_tokens=300)
        return {"model": m, "task": t["id"], "conclusion": text, "cost": cost, "request_id": rid}

    w.run(wjobs, do_write, workers=4)
    gj = {}
    for m in models:
        for t in ts:
            c = w.cache[f"write|{m}|{t['id']}"]["conclusion"]
            for arm in ARMS:
                gj.setdefault(m, []).append((f"grade|{m}|{t['id']}|{arm}", m, t, arm, c))
    g = caller_cls(RESULTS / f"{BET}-grade-calls{tag(pilot)}.json", caps["grade"], f"{BET} grade")

    def do_grade(job):
        _, m, t, arm, c = job
        msgs = own_turn(t["study"], c) if arm == "own" else fresh(t["study"], c)   # fresh2: same messages, new call
        out, cost, rid = call_fn(msgs, m, f"{BET} grade {arm}", max_tokens=40, schema=int_schema("grade"))
        return {"model": m, "task": t["id"], "cond": arm, "grade": out["grade"], "conclusion_sha": sha(c),
                "cost": cost, "request_id": rid}

    g.run(ordered(gj, rng), do_grade, workers=4)
    return w, g


def per_model(grades, model, seed, n_expected, designs):
    ok = sorted(t for t in {t for (t, _) in grades} if all(0 <= grades.get((t, a), -1) <= 100 for a in ARMS))
    out = {"model": model, "n_tasks": n_expected, "n_usable": len(ok), "usable_share": len(ok) / n_expected}
    if len(ok) < 2:
        out["reading"] = "untestable"
        return out
    d = [grades[(t, "own")] - grades[(t, "fresh")] for t in ok]
    d0 = [grades[(t, "fresh2")] - grades[(t, "fresh")] for t in ok]
    ci, d0ci = boot_ci(d, seed), boot_ci(d0, seed + 1)
    gate_ok = (d0ci[0] <= 0 <= d0ci[1]) or abs(float(np.mean(d0))) < GATE_MIN   # D5e: a shift under 1 point is not a fault
    out.update(D=float(np.mean(d)), ci=list(ci), D0=float(np.mean(d0)), D0_ci=list(d0ci), gate_ok=gate_ok,
               mean={a: float(np.mean([grades[(t, a)] for t in ok])) for a in ARMS},
               sd_diff=float(np.std(d, ddof=1)), share_own_higher=float(np.mean([x > 0 for x in d])),
               share_tied=float(np.mean([x == 0 for x in d])), tasks=ok, diffs=d)
    out["reading"] = reading(out["D"], ci, MARGIN, "kinder", "harsher", out["usable_share"] >= 0.9, gate_ok)
    out["robustness"] = robustness(d, [designs[t] for t in ok], seed, MARGIN, "kinder", "harsher", gate_ok)
    return out


def analyse(pilot, grade_cache=None, write_cache=None, n_expected=None, task_list=None):
    gc = grade_cache if grade_cache is not None else json.loads((RESULTS / f"{BET}-grade-calls{tag(pilot)}.json").read_text())
    wc = write_cache if write_cache is not None else json.loads((RESULTS / f"{BET}-write-calls{tag(pilot)}.json").read_text())
    ts = task_list if task_list is not None else tasks(pilot)
    designs = {t["id"]: t.get("design", "?") for t in ts}
    n_expected = n_expected or len(ts)
    mism = [k for k, v in gc.items() if "conclusion_sha" in v and
            sha(wc[f"write|{v['model']}|{v['task']}"]["conclusion"]) != v["conclusion_sha"]]
    if mism:
        raise SystemExit(f"{len(mism)} grade records do not match the write cache's conclusions, e.g. {mism[:3]}")
    by = {m: {} for m in MODELS}                                  # D5 fix 2: every model gets a reading
    for v in gc.values():
        by[v["model"]][(v["task"], v["cond"])] = v["grade"]
    s = seeds()["boot"]
    res = {SHORT[m]: per_model(by[m], m, s, n_expected, designs) for m in MODELS}
    readings = {k: r["reading"] for k, r in res.items()}
    pool = pooled({k: dict(zip(r["tasks"], r["diffs"])) for k, r in res.items() if "diffs" in r}, s + 2)
    return {"bet": BET, "pilot": pilot, "per_model": res, "readings": readings, "verdict": verdict(readings, "kinder", "harsher"),
            "pooled_D": pool, "spend_usd": sum(v["cost"] for v in list(gc.values()) + list(wc.values())),
            "spend_by_model": {"write": spend_by_model(wc), "grade": spend_by_model(gc)}}


def dryrun():
    """No paid calls. D2: the arms' messages; D3: the gate fires on a shifted fresh2; D1: a missing model reads
    untestable; D11: P(verdict) by world, with the gate live."""
    a, b = own_turn("Study: X.", "C1"), fresh("Study: X.", "C1")
    assert a != b and a[1]["content"] == "C1" and "C1" in b[0]["content"]
    print("D2 placement: own has", len(a), "messages (conclusion in assistant turn); fresh has", len(b), "(in user turn)")
    check_frozen_prompts()
    print("D10 sg-b1's prompt strings equal those at", PRE_COMMIT)
    rng = np.random.default_rng(1)

    def world(eff, sd, n=60, shift2=0.0, missing=None):
        res = {}
        for m in ("haiku", "sonnet", "opus"):
            if m == missing:
                res[m] = "untestable"
                continue
            d = np.round(rng.normal(eff, sd, n))
            d0 = np.round(rng.normal(shift2, sd * 0.7, n))
            ci, c0 = boot_ci(d, int(rng.integers(1 << 31)), 500), boot_ci(d0, int(rng.integers(1 << 31)), 500)
            res[m] = reading(float(d.mean()), ci, MARGIN, "kinder", "harsher", True,
                             (c0[0] <= 0 <= c0[1]) or abs(float(d0.mean())) < GATE_MIN)
        return verdict(res, "kinder", "harsher"), res

    fired = sum(world(0, 3, shift2=3.0)[1]["haiku"] == "untestable" for _ in range(200)) / 200
    print(f"D3 gate: fresh2 shifted +3 (SD 3) -> haiku untestable in {fired:.2f} of 200 draws")
    nd = 0
    for _ in range(400):                                    # near-deterministic grader: 5 of 60 calls differ by +1
        d0 = np.array([1.0] * 5 + [0.0] * 55)
        c0 = boot_ci(d0, int(rng.integers(1 << 31)), 2000)
        nd += not ((c0[0] <= 0 <= c0[1]) or abs(d0.mean()) < GATE_MIN)
    print(f"D3 gate: near-deterministic grader with five same-sign 1-point wobbles -> fires in {nd / 400:.2f} (must be 0)")
    v, r = world(5, 3, missing="opus")
    print("D1 Opus missing, others +5:", r, "->", v)
    for name, eff in [("null", 0.0), ("+3", 3.0), ("+5", 5.0), ("-4", -4.0)]:
        for sd in (3.0, 6.0, 10.0):
            tal = {}
            for _ in range(300):
                vv, _ = world(eff, sd)
                tal[vv] = tal.get(vv, 0) + 1
            print("world", name, "sd", sd, {k: round(x / 300, 3) for k, x in sorted(tal.items())})


def stubrun(shift=5.0):
    """End to end with no paid call: 40 fake tasks, a stub model grading `shift` points higher in its own turn."""
    import tempfile
    import threading
    from pathlib import Path
    tmp = Path(tempfile.mkdtemp())
    rr = random.Random(7)
    fake = [{"id": f"t{i:02d}", "design": ["randomised", "self-selected", "before-after"][i % 3],
             "study": f"Study {i}: result {rr.random():.3f}."} for i in range(1, 41)]
    global tasks, seeds
    tasks_orig, seeds_orig = tasks, seeds
    tasks = lambda pilot: fake
    seeds = lambda: {"order": 11, "boot": 12}

    class StubCaller(Caller):
        def __init__(self, path, cap, label):
            self.path, self.cap, self.label, self.cache, self.other = tmp / Path(path).name, cap, label, {}, 0.0
            self.lock, self.stop, self.refusal, self.errors, self.capped = threading.Lock(), threading.Event(), {}, [], ""

        def run(self, jobs, fn, workers=1):
            for j in jobs:
                self.cache[j[0]] = fn(j)

    def stub_call(msgs, model, name, max_tokens=60, schema=None):
        if schema is None:
            return "Conclusion for " + msgs[0]["content"][:30], 0.0, None
        return {"grade": int(round(85 + (shift if len(msgs) == 3 else 0) + rr.gauss(0, 3)))}, 0.0, None

    try:
        w, g = run(False, MODELS, caller_cls=StubCaller, call_fn=stub_call, check_prompts=False)
        r = analyse(False, grade_cache=g.cache, write_cache=w.cache)
    finally:
        tasks, seeds = tasks_orig, seeds_orig
    for k, v in r["per_model"].items():
        print("stub", k, "D", round(v["D"], 2), "ci", [round(x, 2) for x in v["ci"]], "D0", round(v["D0"], 2),
              v["reading"], "fragile", v["robustness"]["fragile"],
              "by design", {d: round(x["mean"], 1) for d, x in v["robustness"]["by_design"].items()})
    print("stub verdict", r["verdict"], "pooled", round(r["pooled_D"]["mean"], 2))
    order = [k.split("|")[1] for k in g.cache]
    print("stub run order is model by model:", order == sorted(order, key=lambda m: MODELS.index(m)))
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
            print(k, {x: v.get(x) for x in ("n_usable", "D", "ci", "D0", "D0_ci", "mean", "sd_diff", "reading")})
    elif cmd == "dryrun":
        dryrun()
        stubrun(5.0)
        stubrun(0.0)

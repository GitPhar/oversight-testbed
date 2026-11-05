"""sg-b3: does grading in the conversation that wrote it blunt a model's penalty for an overclaim planted in its own
conclusion? Pre-registration: experiments/sg-b3-flaw.md.

    PY=/Users/seanpharris/entangled-mind/.venv/bin/python
    $PY experiments/sg_b3_flaw.py run [--pilot]        # paid calls (cached, capped); needs sg-b1's write archive
    $PY experiments/sg_b3_flaw.py analyse [--pilot]    # no calls
    $PY experiments/sg_b3_flaw.py dryrun               # no calls

Reads each model's own conclusions from results/sg-b1-write-calls.json (sg-b1's write step only, none of its grades).
Four cells per study and model, all graded with sg-b1's prompts:
    own-clean    the writing conversation continued; the model's conclusion in its own turn       (sg_prompts.own_turn)
    own-flawed   the same, with one overclaim sentence appended to the conclusion in its own turn
    fresh-clean  a new conversation; request and conclusion in one user message                     (sg_prompts.fresh)
    fresh-flawed the same, with the overclaim appended
The overclaim (sg_prompts.OVERCLAIM): "This proves that the intervention (<intervention>) causes a large improvement in <outcome> for all
<population>." It is unsupported by every study here (small samples; "proves", "large", "for all").
Per model: P_fresh = mean(clean - flawed | fresh), P_own = mean(clean - flawed | own); G = P_fresh - P_own (per study,
then averaged); 95% study-bootstrap CI. G > 0: the flaw costs less in the model's own turn (blunted).
Gate (the manipulation takes effect, P4): P_fresh >= 10 points with CI lower > 0, else the model is untestable.
Reading and verdict: experiments/sg_stats.py (margin 5 points, two of three models). Run order: model by model.
"""
import hashlib
import json
import random
import re
import subprocess
import sys

import numpy as np

import sg_common
import sg_prompts
from sg_common import DATA, MODELS, RESULTS, ROOT, SHORT, Caller, call, int_schema
from sg_items import DOMAINS
from sg_prompts import OVERCLAIM, fresh, own_turn
from sg_stats import boot_ci, pooled, reading, robustness, spend_by_model, verdict

BET = "sg-b3"
CAP = 1.40                    # from sg-b1's pilot cost per grade call (Haiku $0.00008, Sonnet $0.0016, Opus $0.0031)
PILOT_CAP = 0.09
PILOT_TASKS = ("p01", "p02", "p03")
MARGIN = 5.0
GATE = 10.0
CELLS = ("own-clean", "own-flawed", "fresh-clean", "fresh-flawed")


def tasks(pilot):
    t = json.loads((DATA / "sg-tasks.json").read_text())["tasks"]
    return [x for x in t if x["id"] in PILOT_TASKS] if pilot else [x for x in t if x["id"].startswith("t")]


def seeds():
    return json.loads((DATA / "sg-b3-seed.json").read_text())["seeds"]


FLOOR = 5.0                   # D9a: below a mean fresh-flawed grade of 5, sharpening cannot be measured


def check_frozen_prompts():
    """D9e (review fix 5): WRITE, GRADE_Q, GRADE_ABOVE, FRESH, OVERCLAIM (sg_prompts) and SCALE (sg_common) must equal
    their text at this bet's pre-registration commit e29f25c."""
    show = lambda f: subprocess.run(["git", "-C", str(ROOT), "show", f"e29f25c:programs/self-grading/experiments/{f}"],
                                    capture_output=True, text=True, check=True).stdout
    scale = re.search(r'^SCALE = (".*")$', show("sg_common.py"), re.M).group(1)
    ns = {}
    exec(compile(show("sg_prompts.py").replace("from sg_common import SCALE", f"SCALE = {scale}"), "frozen", "exec"), ns)
    bad = [k for k in ("WRITE", "GRADE_Q", "GRADE_ABOVE", "FRESH", "OVERCLAIM") if ns[k] != getattr(sg_prompts, k)]
    bad += ["SCALE"] if ns["SCALE"] != sg_common.SCALE else []
    if bad:
        raise SystemExit(f"sg-b3 prompts differ from e29f25c: {bad}")


def n_sentences(text):
    return len([x for x in re.split(r"(?<=[.!?])\s+", text.strip()) if x])


def sha(x):
    return hashlib.sha256(x.encode()).hexdigest()[:16]


def conclusions(pilot):
    f = RESULTS / f"sg-b1-write-calls{'-pilot' if pilot else ''}.json"
    return {(v["model"], v["task"]): v["conclusion"] for v in json.loads(f.read_text()).values()}


def overclaim(task):
    interv, pop, out = DOMAINS[task["domain"]][:3]
    return OVERCLAIM.format(interv=interv, outcome=out, population=pop)


def flawed(conclusion, task):
    return conclusion.rstrip() + " " + overclaim(task)


def messages(cell, task, conclusion):
    c = flawed(conclusion, task) if cell.endswith("flawed") else conclusion
    return own_turn(task["study"], c) if cell.startswith("own") else fresh(task["study"], c)


def run(pilot, models=MODELS, caller_cls=Caller, call_fn=call, concl=None, check=True):
    ts = tasks(pilot)
    cs = concl if concl is not None else conclusions(pilot)
    if check:
        check_frozen_prompts()
        missing = [(m, t["id"]) for m in models for t in ts if (m, t["id"]) not in cs]
        if missing:
            raise SystemExit(f"sg-b3: {len(missing)} conclusions missing from sg-b1's write cache, e.g. {missing[:3]}")
    rng = random.Random(seeds()["order"])
    jobs = []
    for m in MODELS:                       # model by model (Haiku, Sonnet, Opus), shuffled within: a cap stop leaves whole models
        if m not in models:
            continue
        js = [(f"grade|{m}|{t['id']}|{c}", m, t, c, cs[(m, t["id"])]) for t in ts for c in CELLS if (m, t["id"]) in cs]
        rng.shuffle(js)
        jobs += js
    g = caller_cls(RESULTS / f"{BET}-grade-calls{'-pilot' if pilot else ''}.json", PILOT_CAP if pilot else CAP, f"{BET} grade")

    def do(job):
        _, m, t, c, concl_ = job
        out, cost, rid = call_fn(messages(c, t, concl_), m, f"{BET} grade {c}", max_tokens=40, schema=int_schema("grade"))
        return {"model": m, "task": t["id"], "cond": c, "grade": out["grade"], "conclusion_sha": sha(concl_), "cost": cost,
                "request_id": rid}

    g.run(jobs, do, workers=4)
    return g


def per_model(grades, model, seed, n_expected, designs, info=None):
    """info: {task: {"ci_excludes_0": bool, "over3": bool}} for the D9c secondaries."""
    info = info or {}
    ok = sorted(t for t in {t for (t, _) in grades} if all(0 <= grades.get((t, c), -1) <= 100 for c in CELLS))
    out = {"model": model, "n_tasks": n_expected, "n_usable": len(ok), "usable_share": len(ok) / n_expected}
    if len(ok) < 2:
        out["reading"] = "untestable"
        return out
    g = lambda t, c: grades[(t, c)]
    pf = [g(t, "fresh-clean") - g(t, "fresh-flawed") for t in ok]
    po = [g(t, "own-clean") - g(t, "own-flawed") for t in ok]
    G = [a - b for a, b in zip(pf, po)]
    fD = [g(t, "own-flawed") - g(t, "fresh-flawed") for t in ok]
    cD = [g(t, "own-clean") - g(t, "fresh-clean") for t in ok]
    ci, pfci = boot_ci(G, seed), boot_ci(pf, seed + 1)
    fdci = boot_ci(fD, seed + 4)
    fdci_s = boot_ci(fD, seed + 5)
    gate_ok = float(np.mean(pf)) >= GATE and pfci[0] > 0          # the planted flaw must be penalised fresh (P4, P6)
    mean_fresh_flawed = float(np.mean([g(t, "fresh-flawed") for t in ok]))
    floor = mean_fresh_flawed < FLOOR
    out.update(G=float(np.mean(G)), ci=list(ci), P_fresh=float(np.mean(pf)), P_fresh_ci=list(pfci), gate_ok=gate_ok,
               P_own=float(np.mean(po)), P_own_ci=list(boot_ci(po, seed + 2)),
               mean={c: float(np.mean([g(t, c) for t in ok])) for c in CELLS},
               clean_D=float(np.mean(cD)), clean_D_ci=list(boot_ci(cD, seed + 6)),
               flawed_D=float(np.mean(fD)), flawed_D_ci=list(fdci), flawed_D_ci_sharp=list(fdci_s),
               at_floor=floor, sd_G=float(np.std(G, ddof=1)), tasks=ok, diffs=G)
    r = reading(out["G"], ci, MARGIN, "blunted", "sharpened", out["usable_share"] >= 0.9, gate_ok)
    if r == "blunted" and not fdci[0] > 0:            # D9b: the flawed text itself must score higher in the own turn
        r = "undetermined"
    if r == "sharpened" and (floor or not fdci_s[1] < 0):   # D9a: sharpening needs flawed_D below 0, and no floor
        r = "undetermined"
    out["reading"] = r
    out["note"] = "not blunted (sharpening not measurable at the floor)" if (floor and r == "same") else None
    out["robustness"] = robustness(G, [designs[t] for t in ok], seed, MARGIN, "blunted", "sharpened", gate_ok)
    sec = {}
    for key in ("ci_excludes_0", "over3"):
        for val in (True, False):
            v = [x for t, x in zip(ok, G) if info.get(t, {}).get(key) is val]
            sec[f"G_{key}_{val}"] = {"n": len(v), "mean": float(np.mean(v)) if v else None}
    out["secondaries"] = sec
    return out


def analyse(pilot, grade_cache=None, n_expected=None, concl=None, task_list=None):
    gc = grade_cache if grade_cache is not None else json.loads(
        (RESULTS / f"{BET}-grade-calls{'-pilot' if pilot else ''}.json").read_text())
    ts = task_list if task_list is not None else tasks(pilot)
    designs = {t["id"]: t.get("design", "?") for t in ts}
    n_expected = n_expected or len(ts)
    cs = concl if concl is not None else conclusions(pilot)
    mism = [k for k, v in gc.items() if sha(cs[(v["model"], v["task"])]) != v["conclusion_sha"]]
    if mism:
        raise SystemExit(f"{len(mism)} grade records do not match sg-b1's conclusions, e.g. {mism[:3]}")
    by = {m: {} for m in MODELS}                       # every model gets a reading; no data = untestable
    for v in gc.values():
        by[v["model"]][(v["task"], v["cond"])] = v["grade"]
    s = seeds()["boot"]
    tinfo = {t["id"]: t for t in ts}
    info = {m: {tid: {"ci_excludes_0": tinfo[tid].get("ci_excludes_0"),
                      "over3": n_sentences(flawed(cs[(m, tid)], tinfo[tid])) > 3}
                for tid in tinfo if (m, tid) in cs} for m in MODELS}
    res = {SHORT[m]: per_model(by[m], m, s, n_expected, designs, info.get(m)) for m in MODELS}
    readings = {k: r["reading"] for k, r in res.items()}
    pool = pooled({k: dict(zip(r["tasks"], r["diffs"])) for k, r in res.items() if "diffs" in r}, s + 3)
    return {"bet": BET, "pilot": pilot, "per_model": res, "readings": readings,
            "verdict": verdict(readings, "blunted", "sharpened"), "pooled_G": pool,
            "spend_usd": sum(v["cost"] for v in gc.values()), "spend_by_model": spend_by_model(gc)}


def bounded_worlds(reps=60, n=60):
    """D9a, D9b: grades bounded at the pilot's floor (fresh-flawed about 3, clean about 92), noise on the logit scale.
    Worlds: null; blunting (own-flawed +1.5 logit); own-turn harshness only (every own-turn grade -1 logit, no
    flaw-specific effect; must not pass); sharpening (own-flawed -1 logit; unmeasurable at the floor)."""
    rng = np.random.default_rng(4)
    L = lambda p: np.log(p / (1 - p))
    S = lambda x: 100 / (1 + np.exp(-x))
    base = {"clean": L(0.92), "flawed": L(0.03)}
    worlds = {"null": {}, "blunting +1.5 logit": {"own-flawed": 1.5}, "harshness only -1 logit": {"own-clean": -1.0, "own-flawed": -1.0},
              "sharpening -1 logit": {"own-flawed": -1.0}}
    for name, sh in worlds.items():
        tal = {}
        for _ in range(reps):
            rd = {}
            for mi, m in enumerate(("haiku", "sonnet", "opus")):
                grades = {}
                for i in range(n):
                    item = rng.normal(0, 0.4)
                    for c in CELLS:
                        x = base[c.split("-")[1]] + item + sh.get(c, 0.0) + rng.normal(0, 0.35)
                        grades[(f"t{i:02d}", c)] = int(np.clip(np.round(S(x)), 0, 100))
                rd[m] = per_model(grades, m, 100 + mi, n, {f"t{i:02d}": "x" for i in range(n)})["reading"]
            v = verdict(rd, "blunted", "sharpened")
            tal[v] = tal.get(v, 0) + 1
        print("bounded world", name, {k: round(x / reps, 3) for k, x in sorted(tal.items())})


def dryrun():
    """No paid calls. D2: for one real study, the four cells' messages; the flawed text differs from the clean only by
    the appended sentence. D3: a grader that ignores the flaw is made untestable by the gate. D11: P(verdict) by world."""
    t = json.loads((DATA / "sg-tasks.json").read_text())["tasks"][0] if (DATA / "sg-tasks.json").exists() else \
        {"id": "x", "domain": 0, "study": "Study: X."}
    c = "The data show a small difference whose interval includes zero."
    for cell in CELLS:
        m = messages(cell, t, c)
        print("D2", cell, len(m), "messages; last 90 chars:", repr(m[-1]["content"][-90:]) if cell.startswith("fresh")
              else repr(m[1]["content"][-90:]))
    assert flawed(c, t).startswith(c) and flawed(c, t) != c
    blind = per_model({(f"t{i:02d}", c): 90 for i in range(60) for c in CELLS}, "stub", 1, 60, {f"t{i:02d}": "x" for i in range(60)})
    assert blind["reading"] == "untestable" and not blind["gate_ok"]
    print("D3 a flaw-blind grader -> untestable (gate fires)")
    check_frozen_prompts()
    print("D10 sg-b3's prompt strings equal those at e29f25c")
    bounded_worlds()
    rng = np.random.default_rng(3)
    print("unbounded worlds (as first committed; the bounded table above replaces the -8 row at the floor):")
    for name, eff in [("null", 0.0), ("blunted +8", 8.0), ("blunted +4", 4.0), ("sharpened -8", -8.0)]:
        for sd in (4.0, 8.0, 14.0):
            tal = {}
            for _ in range(400):
                rd = {}
                for m in ("haiku", "sonnet", "opus"):
                    d = list(np.round(rng.normal(eff, sd, 60)))
                    lo, hi = boot_ci(d, int(rng.integers(1 << 31)), n=500)
                    rd[m] = reading(float(np.mean(d)), [lo, hi], MARGIN, "blunted", "sharpened")
                v = verdict(rd, "blunted", "sharpened")
                tal[v] = tal.get(v, 0) + 1
            print("world", name, "sd", sd, {k: round(v / 400, 3) for k, v in sorted(tal.items())})


def stubrun(blunt=8.0):
    """End to end with no paid call: 40 fake tasks; a stub that docks 20 points for the overclaim fresh and
    20 - `blunt` in its own turn."""
    import tempfile
    import threading
    from pathlib import Path
    tmp = Path(tempfile.mkdtemp())
    rr = random.Random(9)
    fake = [{"id": f"t{i:02d}", "domain": i % 20, "design": ["randomised", "self-selected", "before-after"][i % 3],
             "study": f"Study {i}."} for i in range(1, 41)]
    cs = {(m, t["id"]): f"Conclusion {m} {t['id']}." for m in MODELS for t in fake}
    global tasks, seeds
    to, so = tasks, seeds
    tasks, seeds = (lambda pilot: fake), (lambda: {"order": 31, "boot": 32})

    class StubCaller(Caller):
        def __init__(self, path, cap, label):
            self.path, self.cap, self.label, self.cache, self.other = tmp / Path(path).name, cap, label, {}, 0.0
            self.lock, self.stop, self.refusal, self.errors, self.capped = threading.Lock(), threading.Event(), {}, [], ""

        def run(self, jobs, fn, workers=1):
            for j in jobs:
                self.cache[j[0]] = fn(j)

    def stub_call(msgs, model, name, max_tokens=60, schema=None):
        text = json.dumps(msgs)
        own = len(msgs) == 3
        pen = (20 - (blunt if own else 0)) if "This proves that" in text else 0
        return {"grade": int(round(90 - pen + rr.gauss(0, 2)))}, 0.0, None

    try:
        g = run(False, MODELS, caller_cls=StubCaller, call_fn=stub_call, concl=cs, check=False)
        r = analyse(False, grade_cache=g.cache, concl=cs)
    finally:
        tasks, seeds = to, so
    for k, v in r["per_model"].items():
        print("stub", k, "G", round(v["G"], 2), [round(x, 2) for x in v["ci"]], "P_fresh", round(v["P_fresh"], 1),
              "P_own", round(v["P_own"], 1), v["reading"], "fragile", v["robustness"]["fragile"])
    order = [k.split("|")[1] for k in g.cache]
    print("stub verdict", r["verdict"], "| model-by-model order:", order == sorted(order, key=lambda m: MODELS.index(m)))
    return r


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "dryrun"
    pilot = "--pilot" in sys.argv
    if cmd == "run":
        run(pilot)
    elif cmd == "analyse":
        r = analyse(pilot)
        (RESULTS / f"{BET}-analysis{'-pilot' if pilot else ''}.json").write_text(json.dumps(r, indent=1))
        print(json.dumps({k: v for k, v in r.items() if k != "per_model"}, indent=1))
        for k, v in r["per_model"].items():
            print(k, {x: v.get(x) for x in ("n_usable", "G", "ci", "P_fresh", "P_own", "clean_D", "flawed_D", "mean", "reading")})
    else:
        dryrun()
        stubrun(8.0)
        stubrun(0.0)

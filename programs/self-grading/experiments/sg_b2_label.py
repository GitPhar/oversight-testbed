"""sg-b2: does telling a model "this conclusion was written by you" (text unchanged) earn a kinder grade than
"written by another AI model"? Pre-registration: experiments/sg-b2-label.md.

    PY=/Users/seanpharris/entangled-mind/.venv/bin/python
    $PY experiments/sg_b2_label.py run [--pilot]        # paid calls (cached, capped); needs sg-b1's write archive
    $PY experiments/sg_b2_label.py analyse [--pilot]    # no calls
    $PY experiments/sg_b2_label.py dryrun               # no calls

Reads each model's own conclusions from results/sg-b1-write-calls.json (sg-b1's write step; nothing of sg-b1's grades).
Each model grades its own conclusion three times, fresh, in one user message, differing only by one sentence:
    self  = "This conclusion was written by you, in an earlier conversation."
    other = "This conclusion was written by another AI model, in an earlier conversation."
    none  = no sentence (reported; the self-inflation / other-deflation split, secondary)
Primary, per model: L = mean over usable studies of (grade_self - grade_other); 95% study-bootstrap CI.
Reading and verdict: experiments/sg_stats.py, the same rule as sg-b1 (margin 3 points, two of three models), with L.
Run order: model by model (Haiku, Sonnet, Opus), arms and studies shuffled within each model by seed `order`.
Noise-floor gate, free: the "none" arm's prompt is byte-identical to sg-b1's "fresh" prompt (sg_prompts.labelled(...,
"none") == sg_prompts.fresh(...)). D0 = mean(grade_none [sg-b2] - grade_fresh [sg-b1]); if its 95% CI excludes 0 and
|D0| >= 1 point, two identical calls disagree systematically and the model is untestable.
"""
import hashlib
import json
import random
import subprocess
import sys

import numpy as np

import sg_prompts
from sg_common import DATA, MODELS, RESULTS, ROOT, SHORT, Caller, call, int_schema
from sg_prompts import labelled
from sg_stats import boot_ci, pooled, reading, robustness, spend_by_model, verdict

BET = "sg-b2"
CAP = 1.10                    # from sg-b1's pilot cost per grade call (Haiku $0.00008, Sonnet $0.0016, Opus $0.0031)
PILOT_CAP = 0.09
GATE_MIN = 1.0                # the noise-floor gate fires only if |D0| >= 1 point and its CI excludes 0 (as sg-b1 D5e)
PILOT_TASKS = ("p01", "p02", "p03")
MARGIN = 3.0
ARMS = ("self", "other", "none")


def tasks(pilot):
    t = json.loads((DATA / "sg-tasks.json").read_text())["tasks"]
    return [x for x in t if x["id"] in PILOT_TASKS] if pilot else [x for x in t if x["id"].startswith("t")]


def seeds():
    return json.loads((DATA / "sg-b2-seed.json").read_text())["seeds"]


def frozen(commit, names):
    old = subprocess.run(["git", "-C", str(ROOT), "show", f"{commit}:programs/self-grading/experiments/sg_prompts.py"],
                         capture_output=True, text=True, check=True).stdout
    ns = {}
    exec(compile(old.replace("from sg_common import SCALE", f"SCALE = {sg_prompts.SCALE!r}"), "frozen", "exec"), ns)
    return [k for k in names if ns[k] != getattr(sg_prompts, k)]


def preflight(ts, cs, models):
    """Review fix D8a (ledger/design-reviews/sg-b2.md, flaw 2): the prompts are the frozen ones (WRITE, GRADE_Q, FRESH
    as at sg-b1's d2589e3; LABELS as at this bet's ffa8033), each arm carries exactly its sentence, and every model has
    a conclusion for all 60 studies. Otherwise the run does not start."""
    bad = frozen("d2589e3", ("WRITE", "GRADE_Q", "FRESH")) + frozen("ffa8033", ("LABELS",))
    if bad:
        raise SystemExit(f"sg-b2 prompts differ from the frozen ones: {bad}")
    missing = [(m, x["id"]) for m in models for x in ts if (m, x["id"]) not in cs]
    if missing:
        raise SystemExit(f"sg-b2: {len(missing)} conclusions missing from sg-b1's write cache, e.g. {missing[:3]}")
    from sg_prompts import fresh
    sentences = [v for v in sg_prompts.LABELS.values() if v]
    bad = []
    for m in models:                                   # D8c: every (model, study), not one
        for x in ts:
            c = cs[(m, x["id"])]
            none = labelled(x["study"], c, "none")
            if none != fresh(x["study"], c):
                bad.append((m, x["id"], "none != sg-b1 fresh"))
            nb = none[0]["content"]
            for a in ("self", "other"):
                body = labelled(x["study"], c, a)[0]["content"]
                lab = sg_prompts.LABELS[a]
                counts = [body.count(sv) for sv in sentences]
                if body.count(lab) != 1 or sum(counts) != 1 or body.replace(lab + " ", "", 1) != nb:
                    bad.append((m, x["id"], a))
            if any(nb.count(sv) for sv in sentences):
                bad.append((m, x["id"], "label sentence in none"))
    if bad:
        raise SystemExit(f"sg-b2 preflight: {len(bad)} arm(s) malformed, e.g. {bad[:3]}")


def sha(x):
    return hashlib.sha256(x.encode()).hexdigest()[:16]


def conclusions(pilot):
    f = RESULTS / f"sg-b1-write-calls{'-pilot' if pilot else ''}.json"
    return {(v["model"], v["task"]): v["conclusion"] for v in json.loads(f.read_text()).values()}


def run(pilot, models=MODELS, caller_cls=Caller, call_fn=call, concl=None, check=True):
    ts = tasks(pilot)
    cs = concl if concl is not None else conclusions(pilot)
    if check:
        preflight(ts, cs, models)
    rng = random.Random(seeds()["order"])
    jobs = []
    for m in MODELS:                       # model by model (Haiku, Sonnet, Opus), shuffled within: a cap stop leaves whole models
        if m not in models:
            continue
        js = [(f"grade|{m}|{t['id']}|{a}", m, t, a, cs[(m, t["id"])]) for t in ts for a in ARMS if (m, t["id"]) in cs]
        rng.shuffle(js)
        jobs += js
    g = caller_cls(RESULTS / f"{BET}-grade-calls{'-pilot' if pilot else ''}.json", PILOT_CAP if pilot else CAP, f"{BET} grade")

    def do(job):
        _, m, t, a, c = job
        out, cost, rid = call_fn(labelled(t["study"], c, a), m, f"{BET} grade {a}", max_tokens=40, schema=int_schema("grade"))
        return {"model": m, "task": t["id"], "cond": a, "grade": out["grade"], "conclusion_sha": sha(c), "cost": cost,
                "request_id": rid}

    g.run(jobs, do, workers=4)
    return g


def per_model(grades, model, seed, n_expected, b1_fresh, designs):
    b1_fresh = b1_fresh or {}
    ok = sorted(t for t in {t for (t, _) in grades}
                if all(0 <= grades.get((t, a), -1) <= 100 for a in ARMS) and 0 <= b1_fresh.get(t, -1) <= 100)
    out = {"model": model, "n_tasks": n_expected, "n_usable": len(ok), "usable_share": len(ok) / n_expected}
    if len(ok) < 2:
        out["reading"] = "untestable"
        return out
    L = [grades[(t, "self")] - grades[(t, "other")] for t in ok]
    S = [grades[(t, "self")] - grades[(t, "none")] for t in ok]
    O = [grades[(t, "other")] - grades[(t, "none")] for t in ok]
    d0 = [grades[(t, "none")] - b1_fresh[t] for t in ok]
    ci, d0ci = boot_ci(L, seed), boot_ci(d0, seed + 3)
    gate_ok = (d0ci[0] <= 0 <= d0ci[1]) or abs(float(np.mean(d0))) < GATE_MIN
    out.update(L=float(np.mean(L)), ci=list(ci), D0=float(np.mean(d0)), D0_ci=list(d0ci), gate_ok=gate_ok,
               self_minus_none=float(np.mean(S)), self_minus_none_ci=list(boot_ci(S, seed + 1)),
               other_minus_none=float(np.mean(O)), other_minus_none_ci=list(boot_ci(O, seed + 2)),
               mean={a: float(np.mean([grades[(t, a)] for t in ok])) for a in ARMS},
               sd_diff=float(np.std(L, ddof=1)), share_self_higher=float(np.mean([x > 0 for x in L])),
               share_tied=float(np.mean([x == 0 for x in L])), tasks=ok, diffs=L)
    out["reading"] = reading(out["L"], ci, MARGIN, "kinder", "harsher", out["usable_share"] >= 0.9, gate_ok)
    out["robustness"] = robustness(L, [designs[t] for t in ok], seed, MARGIN, "kinder", "harsher", gate_ok)
    return out


def b1_fresh_grades(pilot):
    f = RESULTS / f"sg-b1-grade-calls{'-pilot' if pilot else ''}.json"
    out = {}
    for v in json.loads(f.read_text()).values():
        if v["cond"] == "fresh":
            out.setdefault(v["model"], {})[v["task"]] = v["grade"]
    return out


def analyse(pilot, grade_cache=None, n_expected=None, b1=None, concl=None, task_list=None):
    gc = grade_cache if grade_cache is not None else json.loads(
        (RESULTS / f"{BET}-grade-calls{'-pilot' if pilot else ''}.json").read_text())
    ts = task_list if task_list is not None else tasks(pilot)
    designs = {t["id"]: t.get("design", "?") for t in ts}
    n_expected = n_expected or len(ts)
    b1 = b1 if b1 is not None else b1_fresh_grades(pilot)
    cs = concl if concl is not None else conclusions(pilot)
    mism = [k for k, v in gc.items() if sha(cs[(v["model"], v["task"])]) != v["conclusion_sha"]]
    if mism:
        raise SystemExit(f"{len(mism)} grade records do not match sg-b1's conclusions, e.g. {mism[:3]}")
    by = {m: {} for m in MODELS}                       # every model gets a reading; no data = untestable
    for v in gc.values():
        by[v["model"]][(v["task"], v["cond"])] = v["grade"]
    s = seeds()["boot"]
    res = {SHORT[m]: per_model(by[m], m, s, n_expected, b1.get(m), designs) for m in MODELS}
    readings = {k: r["reading"] for k, r in res.items()}
    pool = pooled({k: dict(zip(r["tasks"], r["diffs"])) for k, r in res.items() if "diffs" in r}, s + 4)
    return {"bet": BET, "pilot": pilot, "per_model": res, "readings": readings,
            "verdict": verdict(readings, "kinder", "harsher"), "pooled_L": pool,
            "spend_usd": sum(v["cost"] for v in gc.values()), "spend_by_model": spend_by_model(gc)}


def dryrun():
    """No paid calls. D2: the three arms differ by exactly one sentence around a byte-identical conclusion.
    D11: P(verdict) under synthetic worlds at n = 60."""
    a, b, c = (labelled("Study: X.", "C1", x)[0]["content"] for x in ARMS)
    assert "written by you" in a and "another AI model" in b and "written by" not in c
    assert a.replace("This conclusion was written by you, in an earlier conversation. ", "") == c
    assert b.replace("This conclusion was written by another AI model, in an earlier conversation. ", "") == c
    from sg_prompts import fresh
    assert labelled("Study: X.", "C1", "none") == fresh("Study: X.", "C1")
    print("D2 the none arm is byte-identical to sg-b1's fresh arm (the free noise-floor gate)")
    gate = {"usable_share": 1.0, "n_usable": 60, "L": 5.0, "ci": [3.0, 7.0], "D0_ci": [1.0, 4.0]}
    assert reading(gate["L"], gate["ci"], MARGIN, "kinder", "harsher", True,
                   (gate["D0_ci"][0] <= 0 <= gate["D0_ci"][1]) or 2.5 < GATE_MIN) == "untestable"
    print("D3 a model whose identical calls disagree (D0 CI excludes 0) -> untestable")
    print("D2 labels: self and other differ from none by exactly one sentence; conclusion identical")
    print("D10 frozen prompts:", "ok" if not (frozen("d2589e3", ("WRITE", "GRADE_Q", "FRESH")) + frozen("ffa8033", ("LABELS",))) else "DIFFER")
    if (RESULTS / "sg-b1-write-calls.json").exists():
        preflight(tasks(False), conclusions(False), MODELS)
        print("D10 preflight on the real write cache: all 60 conclusions per model present; arms carry their sentences")
    rng = np.random.default_rng(2)
    for name, eff in [("null", 0.0), ("Popov-size, Sonnet only harsher", None), ("Chae-size kinder (+6)", 6.0), ("Khullar-size (+2)", 2.0)]:
        for sd in (3.0, 6.0, 10.0):
            tal = {}
            for _ in range(400):
                rd = {}
                for m in ("haiku", "sonnet", "opus"):
                    e = eff if eff is not None else (-3.0 if m == "sonnet" else 0.0)
                    d = list(np.round(rng.normal(e, sd, 60)))
                    lo, hi = boot_ci(d, int(rng.integers(1 << 31)), n=500)
                    rd[m] = reading(float(np.mean(d)), [lo, hi], MARGIN, "kinder", "harsher")
                v = verdict(rd, "kinder", "harsher")
                tal[v] = tal.get(v, 0) + 1
            print("world", name, "sd", sd, {k: round(v / 400, 3) for k, v in sorted(tal.items())})


def stubrun(shift=5.0):
    """End to end with no paid call: 40 fake tasks and conclusions, a stub model grading `shift` points higher under
    the "you" label; sg-b1's fresh grades faked at the same level as "none"."""
    import tempfile
    import threading
    from pathlib import Path
    tmp = Path(tempfile.mkdtemp())
    rr = random.Random(5)
    fake = [{"id": f"t{i:02d}", "design": ["randomised", "self-selected", "before-after"][i % 3],
             "study": f"Study {i}."} for i in range(1, 41)]
    cs = {(m, t["id"]): f"Conclusion {m} {t['id']}" for m in MODELS for t in fake}
    b1 = {m: {t["id"]: 88 for t in fake} for m in MODELS}
    global tasks, seeds
    to, so = tasks, seeds
    tasks, seeds = (lambda pilot: fake), (lambda: {"order": 21, "boot": 22})

    class StubCaller(Caller):
        def __init__(self, path, cap, label):
            self.path, self.cap, self.label, self.cache, self.other = tmp / Path(path).name, cap, label, {}, 0.0
            self.lock, self.stop, self.refusal, self.errors, self.capped = threading.Lock(), threading.Event(), {}, [], ""

        def run(self, jobs, fn, workers=1):
            for j in jobs:
                self.cache[j[0]] = fn(j)

    def stub_call(msgs, model, name, max_tokens=60, schema=None):
        body = msgs[0]["content"]
        return {"grade": int(round(88 + (shift if "written by you" in body else 0) + rr.gauss(0, 2)))}, 0.0, None

    try:
        g = run(False, MODELS, caller_cls=StubCaller, call_fn=stub_call, concl=cs, check=False)
        r = analyse(False, grade_cache=g.cache, b1=b1, concl=cs)
    finally:
        tasks, seeds = to, so
    for k, v in r["per_model"].items():
        print("stub", k, "L", round(v["L"], 2), [round(x, 2) for x in v["ci"]], "self-none", round(v["self_minus_none"], 2),
              "D0", round(v["D0"], 2), v["reading"], "fragile", v["robustness"]["fragile"])
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
            print(k, {x: v.get(x) for x in ("n_usable", "L", "ci", "D0", "self_minus_none", "other_minus_none", "mean", "reading")})
    else:
        dryrun()
        stubrun(5.0)
        stubrun(0.0)

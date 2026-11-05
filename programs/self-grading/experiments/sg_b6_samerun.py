"""sg-b6 (direction sg-d13): does sg-b4's turn-role reading hold when the own-turn and quoted-copy grades come from one
run instead of two? Pre-registration: experiments/sg-b6-samerun.md.

    PY=/Users/seanpharris/entangled-mind/.venv/bin/python
    $PY experiments/sg_b6_samerun.py run       # paid calls (cached, capped)
    $PY experiments/sg_b6_samerun.py analyse   # no calls
    $PY experiments/sg_b6_samerun.py dryrun    # no calls

Four cells per study, all graded in this one run (nothing archived enters a statistic):
    own-clean, own-flawed        sg-b3's own-turn cells (sg_prompts.own_turn; the overclaim appended, sg_b3_flaw.flawed)
    quoted-clean, quoted-flawed  sg-b4's quoted copy (sg_prompts.quoted, frozen at 65f6f93)
Haiku: all 60 studies, every cell twice. Sonnet and Opus: sg-b4's 30 studies, every cell once.
Per study (cell grade = mean over its repeats): q = quoted-clean - quoted-flawed; o = own-clean - own-flawed; T = q - o;
F = own-flawed - quoted-flawed.
Reading (sg_samerun.read): turn role if T >= H (Haiku 6.3, Opus 3.0) with 20-domain cluster CI lower > 0 and F's
cluster CI lower > 0; layout if T's CI upper < H; undetermined otherwise; untestable if the gate (mean q >= 10, CI lower
> 0) fails or under 90% of studies are usable.
Verdict (scored on Haiku, the map's and the card's event): pass if Haiku reads turn role; fail if layout; mixed if
undetermined; untestable if untestable. Opus's reading (bar 3.0) and Sonnet's T are reported, not scored.
"""
import json
import sys

import numpy as np

import sg_samerun as S
from sg_b3_flaw import conclusions, flawed
from sg_common import MODELS, RESULTS, SHORT, Caller, call
from sg_followups import cluster_boot_ci, test_tasks
from sg_prompts import fresh, own_turn, quoted
from sg_stats import boot_ci

BET = "sg-b6"
CAP = 0.80                 # estimate $0.64 at sg-b3/sg-b4's cost per call (Haiku $0.000075, Sonnet $0.0016, Opus $0.0034)
GATE = 10.0
H = {"haiku": 6.3, "opus": 3.0}          # half of each model's sg-b3 G (12.58, 5.97), as sg-b4 and the card
CELLS = ("own-clean", "own-flawed", "quoted-clean", "quoted-flawed")
FRESH_CELLS = ("fresh-clean", "fresh-flawed")   # D23 (review sg-b6, recommended): Haiku only, secondary, never in a reading
REPS = {"claude-haiku-5-5": 2, "claude-sonnet-5-5": 1, "claude-opus-5-5": 1}
ORDER = ("claude-haiku-5-5", "claude-opus-5-5", "claude-sonnet-5-5")   # the scored model first, the unscored last
LABELS = ("turn role", "layout")
FROZEN = {"WRITE": "d4d62ab7d46098edabdab5497f78fb015b3df0866d48d943c966f9b220e8f87b",
          "FRESH": "f83e57e3dc6f7866957fab998d0ef0a3041216cf4e2ab4101565bf7ba49cf6b6",
          "GRADE_ABOVE": "81dee144f1e7a5151f11654312208a21dc8dccb2c1837e6e409dbda2b805876f",
          "QUOTED": "e4bb72034ba5440856f5dd5ec5bfa17e99064d5e45dedac005625d22370367e5",
          "OVERCLAIM": "80f6f0de786c3795f6e5bc97e1c35c8856b788863ee904df3283e3db04f5b872"}


def plan(ts=None):
    ids = sorted(t["id"] for t in (ts if ts is not None else test_tasks()))
    half = S.sg_b4_half()
    return {m: ((ids, CELLS + FRESH_CELLS, REPS[m]) if m == "claude-haiku-5-5" else (half, CELLS, REPS[m])) for m in MODELS}


def messages(cell, task, conclusion):
    c = flawed(conclusion, task) if cell.endswith("flawed") else conclusion
    if cell.startswith("fresh"):
        return fresh(task["study"], c)
    return quoted(task["study"], c) if cell.startswith("quoted") else own_turn(task["study"], c)


def check_frozen():
    from sg_b3_flaw import check_frozen_prompts
    from sg_b4_quoted import check_frozen as b4
    check_frozen_prompts()      # sg-b3's strings as at e29f25c
    b4()                        # QUOTED as at 65f6f93
    S.check_hashes(FROZEN)


def run(caller_cls=Caller, call_fn=call, check=True, seed=None):
    if check:
        check_frozen()
    return S.run(BET, plan(), ORDER, messages, CAP, (seed or S.seeds(BET))["order"], caller_cls, call_fn)


def per_model(cache, model, ids, dom, seed, robust=True):
    k = SHORT[model]
    reps = REPS[model]
    g = S.cell_grades(cache, model)
    ok = S.usable(g, ids, CELLS, reps)
    out = {"model": model, "n_tasks": len(ids), "n_usable": len(ok), "usable_share": len(ok) / len(ids), "reps": reps}
    if len(ok) < 2:
        out["reading"] = "untestable"
        return out
    cl = [dom[t] for t in ok]
    mc = lambda t, c: S.mean_cell(g, t, c)
    q = [mc(t, "quoted-clean") - mc(t, "quoted-flawed") for t in ok]
    o = [mc(t, "own-clean") - mc(t, "own-flawed") for t in ok]
    T = [a - b for a, b in zip(q, o)]
    F = [mc(t, "own-flawed") - mc(t, "quoted-flawed") for t in ok]
    C = [mc(t, "quoted-clean") - mc(t, "own-clean") for t in ok]
    qci = cluster_boot_ci(q, cl, seed + 2)
    gate_ok = S.ge(float(np.mean(q)), GATE) and S.gt(qci[0], 0)
    out.update(T=float(np.mean(T)), T_ci=list(cluster_boot_ci(T, cl, seed)), T_ci_study=list(boot_ci(T, seed)),
               F=float(np.mean(F)), F_ci=list(cluster_boot_ci(F, cl, seed + 1)), q=float(np.mean(q)), q_ci=list(qci),
               o=float(np.mean(o)), o_ci=list(cluster_boot_ci(o, cl, seed + 3)), gate_ok=gate_ok,
               clean_shift=float(np.mean(C)), clean_shift_ci=list(cluster_boot_ci(C, cl, seed + 4)),
               mean={c: float(np.mean([mc(t, c) for t in ok])) for c in CELLS}, sd_T=float(np.std(T, ddof=1)),
               tasks=ok, diffs=T)
    bar = H.get(k)
    if bar is None:
        out["reading"] = "reported only" if (out["usable_share"] >= S.USABLE and gate_ok) else "untestable"
    else:
        out["reading"] = S.read(T, F, cl, bar, seed, gate_ok, out["usable_share"], LABELS)
        out["reading_study_bootstrap"] = _study_read(T, F, bar, seed, gate_ok, out["usable_share"])
        if robust:
            out["robustness"] = S.robustness(T, F, cl, ok, bar, seed, gate_ok, out["usable_share"], LABELS,
                                             out["reading"])
    fr = [t for t in ok if all(len(g.get((t, c), [])) == reps for c in FRESH_CELLS)]
    if fr:                              # D23: same-run blunting G_today = fresh penalty - own penalty (secondary)
        Gt = [(mc(t, "fresh-clean") - mc(t, "fresh-flawed")) - (mc(t, "own-clean") - mc(t, "own-flawed")) for t in fr]
        Tf = [T[ok.index(t)] for t in fr]
        out["G_today"] = {"n": len(fr), "mean": float(np.mean(Gt)), "ci": list(cluster_boot_ci(Gt, [dom[t] for t in fr], seed + 5)),
                          "T_share": float(np.mean(Tf)) / float(np.mean(Gt)) if abs(float(np.mean(Gt))) > 1e-9 else None}
    if reps == 2:                       # secondaries on the two repeats (reported, never promoted)
        r = lambda t, c, i: g[(t, c)][i]
        Tr = [[(r(t, "quoted-clean", i) - r(t, "quoted-flawed", i)) - (r(t, "own-clean", i) - r(t, "own-flawed", i))
               for t in ok] for i in (0, 1)]
        d = [g[(t, c)][1] - g[(t, c)][0] for t in ok for c in CELLS]
        out["repeats"] = {"T_r1": float(np.mean(Tr[0])), "T_r2": float(np.mean(Tr[1])),
                          "identical_share": float(np.mean([x == 0 for x in d])),
                          "sd_r2_minus_r1": float(np.std(d, ddof=1))}
    return out


def _study_read(T, F, bar, seed, gate_ok, share):
    if share < S.USABLE or not gate_ok:
        return "untestable"
    ci, fci = boot_ci(T, seed), boot_ci(F, seed + 1)
    if S.ge(float(np.mean(T)), bar) and S.gt(ci[0], 0) and S.gt(fci[0], 0):
        return LABELS[0]
    if S.lt(ci[1], bar):
        return LABELS[1]
    return "undetermined"


def cross_run(res, seed):
    """Secondaries against the archives (reported only): today's own-turn penalty minus sg-b3's on the same studies,
    and today's quoted penalty minus sg-b4's; sg-b4's T on the same studies."""
    b3, b4 = S.archive("sg-b3"), S.archive("sg-b4")
    dom = {t["id"]: t["domain"] for t in test_tasks()}
    out = {}
    for m in MODELS:
        r = res[SHORT[m]]
        if "tasks" not in r:
            continue
        ok = r["tasks"]
        cl = [dom[t] for t in ok]
        own_b3 = [b3[(m, t, "own-clean")] - b3[(m, t, "own-flawed")] for t in ok]
        q_b4 = [b4[(m, t, "quoted-clean")] - b4[(m, t, "quoted-flawed")] for t in ok]
        T_b4 = [a - b for a, b in zip(q_b4, own_b3)]
        o_now = r["_o"]
        q_now = [T + o for T, o in zip(r["diffs"], o_now)]
        do = [a - b for a, b in zip(o_now, own_b3)]
        dq = [a - b for a, b in zip(q_now, q_b4)]
        out[SHORT[m]] = {"T_sg_b4_same_studies": float(np.mean(T_b4)),
                         "own_penalty_now_minus_sg_b3": float(np.mean(do)),
                         "own_penalty_now_minus_sg_b3_ci": list(cluster_boot_ci(do, cl, seed + 6)),
                         "quoted_penalty_now_minus_sg_b4": float(np.mean(dq)),
                         "quoted_penalty_now_minus_sg_b4_ci": list(cluster_boot_ci(dq, cl, seed + 7))}
    return out


def verdict(readings):
    return {"turn role": "pass", "layout": "fail", "undetermined": "mixed"}.get(readings["haiku"], "untestable")


def analyse(pilot=False, cache=None, s=None, robust=True):
    """pilot: accepted for reproduce.py's calling convention (analyse(pilot)); these bets have no pilot (D24)."""
    if pilot:
        raise SystemExit("no pilot for this bet")
    cache = cache if cache is not None else json.loads((RESULTS / f"{BET}-grade-calls.json").read_text())
    S.verify(cache, messages)
    s = s or S.seeds(BET)
    ts = test_tasks()
    dom = {t["id"]: t["domain"] for t in ts}
    pl = plan(ts)
    res = {}
    for m in MODELS:
        r = per_model(cache, m, pl[m][0], dom, s["boot"], robust)
        if "tasks" in r:
            g = S.cell_grades(cache, m)
            r["_o"] = [S.mean_cell(g, t, "own-clean") - S.mean_cell(g, t, "own-flawed") for t in r["tasks"]]
        res[SHORT[m]] = r
    xr = cross_run(res, s["boot"])
    for r in res.values():
        r.pop("_o", None)
    readings = {k: r["reading"] for k, r in res.items()}
    return {"bet": BET, "study_sets": {SHORT[m]: pl[m][0] for m in MODELS}, "per_model": res, "readings": readings,
            "verdict": verdict(readings), "cross_run": xr, **S.spend(cache)}


# ---------------------------------------------------------------- dry run (no calls) ---------------------------------
def truths(world):
    """Per (model, study, cell) true grades for a dry-run world, from sg-b3's own-turn and sg-b4's quoted cells (P15):
    'as sg-b4'       own = sg-b3's own cells, quoted = sg-b4's quoted cells (sg-b4's result, cross-run noise included)
    'drift'          as sg-b4, but today's own-turn penalty is 4.3 points smaller on Haiku (sg-b4's measured drift)
    'layout'         quoted = own (no role effect)
    'at the bar'     quoted-clean = own-clean, quoted-flawed = own-flawed - H (T exactly the bar)
    'regression'     quoted-flawed = own-flawed - 3.8, quoted-clean = own-clean (sg-b4's T minus 3 points)
    'kinder-clean'   quoted-clean = own-clean + 8, quoted-flawed = own-flawed (the F guard must reject it)"""
    b3, b4 = S.archive("sg-b3"), S.archive("sg-b4")
    pl = plan()
    tr = {}
    for m, (ids, _, _) in pl.items():
        bar = H.get(SHORT[m], 1.0)
        for t in ids:
            oc, of = b3[(m, t, "own-clean")], b3[(m, t, "own-flawed")]
            if world == "drift" and m == "claude-haiku-5-5":
                of += 4.3
            qc, qf = b4[(m, t, "quoted-clean")], b4[(m, t, "quoted-flawed")]
            if world == "layout":
                qc, qf = oc, of
            elif world == "at the bar":     # D23: true T exactly the bar after clipping at 0
                qc, qf = oc, of - bar
                if qf < 0:
                    qc, qf = oc - qf, 0.0
            elif world == "regression":
                qc, qf = oc, of - 3.8
            elif world == "kinder-clean":
                qc, qf = oc + 8, of
            tr.update({(m, t, "own-clean"): oc, (m, t, "own-flawed"): of, (m, t, "quoted-clean"): qc,
                       (m, t, "quoted-flawed"): qf, (m, t, "fresh-clean"): b3[(m, t, "fresh-clean")],
                       (m, t, "fresh-flawed"): b3[(m, t, "fresh-flawed")]})
    return tr


def simulate(world, reps=200, seed=5):
    rng = np.random.default_rng(seed)
    tr, pl = truths(world), plan()
    dom = {t["id"]: t["domain"] for t in test_tasks()}
    tal, opus = {}, {}
    for _ in range(reps):
        c = S.synth_cache(pl, tr, rng)
        sd = int(rng.integers(1 << 30))
        rh = per_model(c, "claude-haiku-5-5", pl["claude-haiku-5-5"][0], dom, sd, robust=False)
        ro = per_model(c, "claude-opus-5-5", pl["claude-opus-5-5"][0], dom, sd, robust=False)
        v = verdict({"haiku": rh["reading"]})
        tal[v] = tal.get(v, 0) + 1
        opus[ro["reading"]] = opus.get(ro["reading"], 0) + 1
    return {k: round(x / reps, 3) for k, x in sorted(tal.items())}, {k: round(x / reps, 3) for k, x in sorted(opus.items())}


def dryrun():
    check_frozen()
    S.check_noise()
    print("P15 per-cell noise (D23):", S.REPEAT_SD)
    for w in ("at the bar",):
        tr, pl = truths(w), plan()
        print("true T in", repr(w), {SHORT[m]: round(float(np.mean([(tr[(m, t, "quoted-clean")] - tr[(m, t, "quoted-flawed")])
              - (tr[(m, t, "own-clean")] - tr[(m, t, "own-flawed")]) for t in pl[m][0]])), 3) for m in MODELS})
    print("D10 frozen strings: sg-b3's at e29f25c, QUOTED at 65f6f93, hashes of WRITE, GRADE_ABOVE, QUOTED, OVERCLAIM")
    t = test_tasks()[0]
    c = "The data show a small difference whose interval includes zero."
    for cell in CELLS:
        ms = messages(cell, t, c)
        print("D2", cell, len(ms), "message(s); last 120 chars:", repr(ms[-1]["content"][-120:]))
    pl = plan()
    print("plan:", {SHORT[m]: (len(v[0]), v[2]) for m, v in pl.items()}, "calls",
          sum(len(v[0]) * len(v[1]) * v[2] for v in pl.values()))
    dom = {x["id"]: x["domain"] for x in test_tasks()}
    ids = pl["claude-haiku-5-5"][0]
    blind = {f"grade|claude-haiku-5-5|{t}|{c}|r{k}": {"model": "claude-haiku-5-5", "task": t, "cond": c, "rep": k,
             "grade": 90, "cost": 0} for t in ids for c in CELLS for k in (1, 2)}
    r = per_model(blind, "claude-haiku-5-5", ids, dom, 1, robust=False)
    assert r["reading"] == "untestable" and not r["gate_ok"]
    print("D3 a flaw-blind grader -> untestable (gate fires)")
    exact = {}
    for i, t in enumerate(ids):
        for k in (1, 2):
            for cc, gr in (("own-clean", 90), ("own-flawed", 20), ("quoted-clean", 90),
                           ("quoted-flawed", 20 - (6 if i % 10 else 9))):        # T = 6.3 exactly
                exact[f"grade|claude-haiku-5-5|{t}|{cc}|r{k}"] = {"model": "claude-haiku-5-5", "task": t, "cond": cc,
                                                                  "rep": k, "grade": gr, "cost": 0}
    r = per_model(exact, "claude-haiku-5-5", ids, dom, 1, robust=False)
    print("P13 Haiku T exactly", round(r["T"], 12), "(bar 6.3) ->", r["reading"])
    assert r["reading"] == "turn role"
    for w in ("as sg-b4", "drift", "layout", "at the bar", "regression", "kinder-clean"):
        v, o = simulate(w)
        print("world", repr(w), "verdict (Haiku)", v, "| Opus reading (reported)", o)


def stubrun():
    """End to end with no paid call: the stub grades every cell from the 'as sg-b4' world."""
    import tempfile
    import threading
    from pathlib import Path
    tmp = Path(tempfile.mkdtemp())
    tr = truths("as sg-b4")
    tid = {t["study"]: t["id"] for t in test_tasks()}

    class StubCaller(Caller):
        def __init__(self, path, cap, label):
            self.path, self.cap, self.label, self.cache, self.other = tmp / Path(path).name, cap, label, {}, 0.0
            self.lock, self.stop, self.refusal, self.errors, self.capped = threading.Lock(), threading.Event(), {}, [], ""

        def run(self, jobs, fn, workers=1):
            for j in jobs:
                self.cache[j[0]] = fn(j)

    def stub_call(msgs, model, name, max_tokens=60, schema=None):
        t = next(v for k, v in tid.items() if k in msgs[0]["content"])
        body = msgs[-1]["content"] if len(msgs) == 1 else msgs[1]["content"]
        arm = ("fresh" if msgs[0]["content"].startswith("Here is a request") else "quoted") if len(msgs) == 1 else "own"
        cell = arm + ("-flawed" if "This proves that" in body else "-clean")
        return {"grade": int(tr[(model, t, cell)])}, 0.0, None

    seed = {"order": 13, "boot": 12}
    g = run(caller_cls=StubCaller, call_fn=stub_call, seed=seed)
    r = analyse(cache=g.cache, s=seed)
    print("stub calls by model", r["calls_by_model"], "| model by model:",
          [k.split("|")[1] for k in g.cache] == sorted([k.split("|")[1] for k in g.cache], key=ORDER.index))
    for k, v in r["per_model"].items():
        print("stub", k, "T", round(v["T"], 2), [round(x, 2) for x in v["T_ci"]], "F", round(v["F"], 2), v["reading"])
    print("stub verdict", r["verdict"], "| cross-run", {k: round(v["T_sg_b4_same_studies"], 2) for k, v in r["cross_run"].items()})


def tables(r):
    """The write-up's tables, regenerated from the analysis (results/sg-b6-samerun.md; reproduce.py compares them)."""
    from sg_followups import cix, fx, sx, table
    P = r["per_model"]
    rows = []
    for k in ("haiku", "opus", "sonnet"):
        v = P[k]
        rows.append([k.capitalize(), v["n_usable"], v["reps"], sx(v.get("T")), cix(v.get("T_ci")),
                     cix(v.get("T_ci_study")), sx(v.get("F")), cix(v.get("F_ci")), fx(v.get("q")), fx(v.get("o")),
                     (f"**{v['reading']}**" if k == "haiku" else v["reading"])])
    t1 = table(["model", "studies", "repeats", "T", "95% CI (20 domains)", "95% CI (studies)", "F", "F 95% CI (domains)",
                "penalty, quoted copy", "penalty, own turn", "reading"], rows)
    X = r["cross_run"]
    sec = [["sg-b4's T on the same studies (cross-run)"] + [sx(X[k]["T_sg_b4_same_studies"]) for k in ("haiku", "opus", "sonnet")],
           ["own-turn penalty, this run − sg-b3's"] + [sx(X[k]["own_penalty_now_minus_sg_b3"]) for k in ("haiku", "opus", "sonnet")],
           ["  95% CI (domains)"] + [cix(X[k]["own_penalty_now_minus_sg_b3_ci"]) for k in ("haiku", "opus", "sonnet")],
           ["quoted penalty, this run − sg-b4's"] + [sx(X[k]["quoted_penalty_now_minus_sg_b4"]) for k in ("haiku", "opus", "sonnet")],
           ["clean text, quoted − own (points)"] + [sx(P[k].get("clean_shift")) for k in ("haiku", "opus", "sonnet")],
           ["same-run blunting G (fresh − own; Haiku only)"] + [sx((P[k].get("G_today") or {}).get("mean")) for k in ("haiku", "opus", "sonnet")],
           ["  95% CI (domains)"] + [cix((P[k].get("G_today") or {}).get("ci")) for k in ("haiku", "opus", "sonnet")],
           ["T as a share of the same-run G"] + [fx((P[k].get("G_today") or {}).get("T_share"), 2) for k in ("haiku", "opus", "sonnet")]]
    for lab, f in (("reading on the study bootstrap", lambda v: v.get("reading_study_bootstrap", "—")),
                   ("fragile, one study dropped", lambda v: ("yes" if v["robustness"]["fragile_study"] else "no") if "robustness" in v else "—"),
                   ("fragile, one domain dropped", lambda v: ("yes" if v["robustness"]["fragile_domain"] else "no") if "robustness" in v else "—"),
                   ("ties (T = 0)", lambda v: v["robustness"]["n_ties"] if "robustness" in v else "—"),
                   ("median T", lambda v: sx(v["robustness"]["median"]) if "robustness" in v else "—"),
                   ("10% trimmed mean T", lambda v: sx(v["robustness"]["trimmed_mean_10"]) if "robustness" in v else "—")):
        sec.append([lab] + [f(P[k]) for k in ("haiku", "opus", "sonnet")])
    t2 = table(["", "Haiku", "Opus", "Sonnet"], sec)
    rp = P["haiku"].get("repeats", {})
    t3 = table(["Haiku's two repeats", "value"],
               [["T, first repeat only", sx(rp.get("T_r1"))], ["T, second repeat only", sx(rp.get("T_r2"))],
                ["share of grades identical across repeats", fx(rp.get("identical_share"), 2)],
                ["SD of (second − first), points", fx(rp.get("sd_r2_minus_r1"), 2)]])
    sp = r["spend_by_model"]
    t4 = table(["", "Haiku", "Opus", "Sonnet", "total"],
               [["test run", f"${sp['haiku']:.3f}", f"${sp['opus']:.3f}", f"${sp['sonnet']:.3f}", f"**${r['spend_usd']:.3f}**"]])
    return [t1, t2, t3, t4]


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "dryrun"
    if cmd == "run":
        run()
    elif cmd == "analyse":
        r = analyse()
        (RESULTS / f"{BET}-analysis.json").write_text(json.dumps(r, indent=1))
        print(json.dumps({k: v for k, v in r.items() if k not in ("per_model", "study_sets")}, indent=1))
        for k, v in r["per_model"].items():
            print(k, {x: v.get(x) for x in ("n_usable", "T", "T_ci", "F", "F_ci", "q", "reading")})
    else:
        dryrun()
        stubrun()

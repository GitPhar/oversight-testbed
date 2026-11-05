"""sg-b7 (direction sg-d14): does the closing line "Now grade the conclusion above." carry part of what sg-b4 left
between its quoted copy and sg-b3's fresh frame? Pre-registration: experiments/sg-b7-leadin.md.

    PY=/Users/seanpharris/entangled-mind/.venv/bin/python
    $PY experiments/sg_b7_leadin.py run       # paid calls (cached, capped)
    $PY experiments/sg_b7_leadin.py analyse   # no calls
    $PY experiments/sg_b7_leadin.py dryrun    # no calls

Four cells per study, all graded in this one run (nothing archived enters a statistic):
    quoted-clean, quoted-flawed  sg-b4's quoted copy, closing line "Now grade the conclusion above." (sg_prompts.quoted)
    plain-clean, plain-flawed    the same quoted copy with only that line swapped for the fresh frame's "Grade the
                                 conclusion." (sg_prompts.quoted_plain); header sentence and User/Assistant blocks kept
Haiku: all 60 studies; Sonnet and Opus: sg-b4's 30 studies; every cell once.
Per study: p = plain-clean - plain-flawed; q = quoted-clean - quoted-flawed; S = p - q; F = quoted-flawed - plain-flawed.
Reading (sg_samerun.read): lead-in carries part if S >= B (half the model's sg-b4 L: Haiku 2.9, Opus 0.75) with
20-domain cluster CI lower > 0 and F's cluster CI lower > 0; not the lead-in if S's CI upper < B; undetermined
otherwise; untestable if the gate (mean q >= 10, CI lower > 0) fails or under 90% of studies are usable.
Verdict: untestable if Haiku or Opus is untestable; pass if both read lead-in carries part; fail if both read not the
lead-in; mixed otherwise. Sonnet's S is reported, not scored.
"""
import json
import sys

import numpy as np

import sg_samerun as S
from sg_b3_flaw import flawed
from sg_common import MODELS, RESULTS, SHORT, Caller, call
from sg_followups import cluster_boot_ci, test_tasks
from sg_prompts import quoted, quoted_plain
from sg_stats import boot_ci

BET = "sg-b7"
CAP = 0.75                 # estimate $0.59 at sg-b4's cost per call (Haiku $0.000075, Sonnet $0.0016, Opus $0.0032)
GATE = 10.0
B = {"haiku": 2.9, "opus": 0.75}         # half of each model's sg-b4 L (5.77, 1.50), as on the map and the card
SG_B4_L = {"haiku": 5.766666666666667, "opus": 1.5, "sonnet": 0.16666666666666666}   # results/sg-b4-analysis.json
CELLS = ("quoted-clean", "quoted-flawed", "plain-clean", "plain-flawed")
ORDER = ("claude-haiku-5-5", "claude-opus-5-5", "claude-sonnet-5-5")
LABELS = ("lead-in carries part", "not the lead-in")
FROZEN = {"WRITE": "d4d62ab7d46098edabdab5497f78fb015b3df0866d48d943c966f9b220e8f87b",
          "GRADE_ABOVE": "81dee144f1e7a5151f11654312208a21dc8dccb2c1837e6e409dbda2b805876f",
          "QUOTED": "e4bb72034ba5440856f5dd5ec5bfa17e99064d5e45dedac005625d22370367e5",
          "QUOTED_PLAIN": "3f55d0c17d8399e170c3019670888f55223537119324a8ab0a53d6953cfab387",
          "OVERCLAIM": "80f6f0de786c3795f6e5bc97e1c35c8856b788863ee904df3283e3db04f5b872"}


def plan(ts=None):
    ids = sorted(t["id"] for t in (ts if ts is not None else test_tasks()))
    half = S.sg_b4_half()
    return {m: (ids if m == "claude-haiku-5-5" else half, CELLS, 1) for m in MODELS}


def messages(cell, task, conclusion):
    c = flawed(conclusion, task) if cell.endswith("flawed") else conclusion
    return quoted_plain(task["study"], c) if cell.startswith("plain") else quoted(task["study"], c)


def check_frozen():
    import sg_prompts
    from sg_b3_flaw import check_frozen_prompts
    from sg_b4_quoted import check_frozen as b4
    check_frozen_prompts()
    b4()
    S.check_hashes(FROZEN)
    a, b = quoted("S", "C")[0]["content"], quoted_plain("S", "C")[0]["content"]
    if a.replace(sg_prompts.GRADE_ABOVE, sg_prompts.PLAIN_LEAD) != b or a == b:
        raise SystemExit("the plain cell must differ from the quoted cell in the closing line only")


def run(caller_cls=Caller, call_fn=call, check=True, seed=None):
    if check:
        check_frozen()
    return S.run(BET, plan(), ORDER, messages, CAP, (seed or S.seeds(BET))["order"], caller_cls, call_fn)


def per_model(cache, model, ids, dom, seed, robust=True):
    k = SHORT[model]
    g = S.cell_grades(cache, model)
    ok = S.usable(g, ids, CELLS, 1)
    out = {"model": model, "n_tasks": len(ids), "n_usable": len(ok), "usable_share": len(ok) / len(ids)}
    if len(ok) < 2:
        out["reading"] = "untestable"
        return out
    cl = [dom[t] for t in ok]
    mc = lambda t, c: S.mean_cell(g, t, c)
    p = [mc(t, "plain-clean") - mc(t, "plain-flawed") for t in ok]
    q = [mc(t, "quoted-clean") - mc(t, "quoted-flawed") for t in ok]
    Sv = [a - b for a, b in zip(p, q)]
    F = [mc(t, "quoted-flawed") - mc(t, "plain-flawed") for t in ok]
    C = [mc(t, "plain-clean") - mc(t, "quoted-clean") for t in ok]
    qci = cluster_boot_ci(q, cl, seed + 2)
    gate_ok = S.ge(float(np.mean(q)), GATE) and S.gt(qci[0], 0)
    out.update(S=float(np.mean(Sv)), S_ci=list(cluster_boot_ci(Sv, cl, seed)), S_ci_study=list(boot_ci(Sv, seed)),
               F=float(np.mean(F)), F_ci=list(cluster_boot_ci(F, cl, seed + 1)), q=float(np.mean(q)), q_ci=list(qci),
               p=float(np.mean(p)), gate_ok=gate_ok, share_of_sg_b4_L=float(np.mean(Sv)) / SG_B4_L[k],
               clean_shift=float(np.mean(C)), clean_shift_ci=list(cluster_boot_ci(C, cl, seed + 4)),
               mean={c: float(np.mean([mc(t, c) for t in ok])) for c in CELLS}, sd_S=float(np.std(Sv, ddof=1)),
               tasks=ok, diffs=Sv, _q=q)
    bar = B.get(k)
    if bar is None:
        out["reading"] = "reported only" if (out["usable_share"] >= S.USABLE and gate_ok) else "untestable"
        return out
    out["reading"] = S.read(Sv, F, cl, bar, seed, gate_ok, out["usable_share"], LABELS)
    ci, fci = boot_ci(Sv, seed), boot_ci(F, seed + 1)
    out["reading_study_bootstrap"] = ("untestable" if not (out["usable_share"] >= S.USABLE and gate_ok) else
                                      LABELS[0] if (S.ge(out["S"], bar) and S.gt(ci[0], 0) and S.gt(fci[0], 0)) else
                                      LABELS[1] if S.lt(ci[1], bar) else "undetermined")
    if robust:
        out["robustness"] = S.robustness(Sv, F, cl, ok, bar, seed, gate_ok, out["usable_share"], LABELS, out["reading"])
    return out


def verdict(readings):
    h, o = readings["haiku"], readings["opus"]
    if "untestable" in (h, o):
        return "untestable"
    if h == o == LABELS[0]:
        return "pass"
    if h == o == LABELS[1]:
        return "fail"
    return "mixed"


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
    b4 = S.archive("sg-b4")
    res, xr = {}, {}
    for m in MODELS:
        r = per_model(cache, m, pl[m][0], dom, s["boot"], robust)
        if "tasks" in r:      # secondary: today's quoted penalty minus sg-b4's on the same studies (cross-run)
            d = [a - (b4[(m, t, "quoted-clean")] - b4[(m, t, "quoted-flawed")]) for t, a in zip(r["tasks"], r["_q"])]
            xr[SHORT[m]] = {"quoted_penalty_now_minus_sg_b4": float(np.mean(d)),
                            "ci": list(cluster_boot_ci(d, [dom[t] for t in r["tasks"]], s["boot"] + 6))}
        r.pop("_q", None)
        res[SHORT[m]] = r
    readings = {k: r["reading"] for k, r in res.items()}
    return {"bet": BET, "study_sets": {SHORT[m]: pl[m][0] for m in MODELS}, "per_model": res, "readings": readings,
            "verdict": verdict(readings), "cross_run": xr, **S.spend(cache)}


# ---------------------------------------------------------------- dry run (no calls) ---------------------------------
def truths(world):
    """True grades per (model, study, cell), from sg-b4's quoted cells and sg-b3's fresh cells (P15):
    'none'        plain = quoted (the lead-in carries nothing)
    'all of L'    plain = sg-b3's fresh cells (the lead-in carries the whole remainder)
    'at the bar'  plain-clean = quoted-clean, plain-flawed = quoted-flawed - B (S exactly the bar)
    'clean-only'  plain-clean = quoted-clean + 4, plain-flawed = quoted-flawed (the F guard must reject it)
    'item'        plain = fresh on the 14 studies whose interval excludes 0, quoted elsewhere (P16)"""
    b3, b4 = S.archive("sg-b3"), S.archive("sg-b4")
    excl = {t["id"] for t in test_tasks() if t["ci_excludes_0"]}
    tr = {}
    for m, (ids, _, _) in plan().items():
        bar = B.get(SHORT[m], 0.1)
        for t in ids:
            qc, qf = b4[(m, t, "quoted-clean")], b4[(m, t, "quoted-flawed")]
            pc, pf = qc, qf
            if world == "all of L" or (world == "item" and t in excl):
                pc, pf = b3[(m, t, "fresh-clean")], b3[(m, t, "fresh-flawed")]
            elif world == "at the bar":     # D23: true S exactly the bar after clipping at 0
                pf = qf - bar
                if pf < 0:
                    pc, pf = qc - pf, 0.0
            elif world == "clean-only":
                pc = qc + 4
            tr.update({(m, t, "quoted-clean"): qc, (m, t, "quoted-flawed"): qf, (m, t, "plain-clean"): pc,
                       (m, t, "plain-flawed"): pf})
    return tr


def simulate(world, reps=200, seed=5):
    rng = np.random.default_rng(seed)
    tr, pl = truths(world), plan()
    dom = {t["id"]: t["domain"] for t in test_tasks()}
    tal, rd = {}, {"haiku": {}, "opus": {}}
    for _ in range(reps):
        c = S.synth_cache(pl, tr, rng)
        sd = int(rng.integers(1 << 30))
        rr = {SHORT[m]: per_model(c, m, pl[m][0], dom, sd, robust=False)["reading"]
              for m in ("claude-haiku-5-5", "claude-opus-5-5")}
        v = verdict(rr)
        tal[v] = tal.get(v, 0) + 1
        for k in rd:
            rd[k][rr[k]] = rd[k].get(rr[k], 0) + 1
    return {k: round(x / reps, 3) for k, x in sorted(tal.items())}, rd


def dryrun():
    check_frozen()
    S.check_noise()
    print("P15 per-cell noise (D23):", S.REPEAT_SD)
    print("D10 frozen strings: sg-b3's at e29f25c, QUOTED at 65f6f93, hashes incl. QUOTED_PLAIN; plain differs from quoted "
          "in the closing line only")
    t = test_tasks()[0]
    c = "The data show a small difference whose interval includes zero."
    for cell in CELLS:
        ms = messages(cell, t, c)
        print("D2", cell, len(ms), "message(s); last 175 chars:", repr(ms[-1]["content"][-175:]))
    pl = plan()
    print("plan:", {SHORT[m]: len(v[0]) for m, v in pl.items()}, "calls", sum(len(v[0]) * len(v[1]) for v in pl.values()))
    dom = {x["id"]: x["domain"] for x in test_tasks()}
    ids = pl["claude-haiku-5-5"][0]
    mk = lambda f: {f"grade|claude-haiku-5-5|{t}|{cc}|r1": {"model": "claude-haiku-5-5", "task": t, "cond": cc, "rep": 1,
                    "grade": f(i, cc), "cost": 0} for i, t in enumerate(ids) for cc in CELLS}
    r = per_model(mk(lambda i, cc: 90), "claude-haiku-5-5", ids, dom, 1, robust=False)
    assert r["reading"] == "untestable" and not r["gate_ok"]
    print("D3 a flaw-blind grader -> untestable (gate fires)")
    ex = {"quoted-clean": 90, "quoted-flawed": 20, "plain-clean": 90}
    r = per_model(mk(lambda i, cc: ex.get(cc, 20 - (3 if i % 10 else 2))), "claude-haiku-5-5", ids, dom, 1, robust=False)
    print("P13 Haiku S exactly", round(r["S"], 12), "(bar 2.9) ->", r["reading"])
    assert r["reading"] == LABELS[0]
    for w in ("none", "all of L", "at the bar", "clean-only", "item"):
        v, rd = simulate(w)
        print("world", repr(w), "verdict", v, "| readings", rd)


def stubrun():
    """End to end with no paid call: the stub grades every cell from the 'all of L' world."""
    import tempfile
    import threading
    from pathlib import Path
    import sg_prompts
    tmp = Path(tempfile.mkdtemp())
    tr = truths("all of L")
    tid = {t["study"]: t["id"] for t in test_tasks()}

    class StubCaller(Caller):
        def __init__(self, path, cap, label):
            self.path, self.cap, self.label, self.cache, self.other = tmp / Path(path).name, cap, label, {}, 0.0
            self.lock, self.stop, self.refusal, self.errors, self.capped = threading.Lock(), threading.Event(), {}, [], ""

        def run(self, jobs, fn, workers=1):
            for j in jobs:
                self.cache[j[0]] = fn(j)

    def stub_call(msgs, model, name, max_tokens=60, schema=None):
        body = msgs[0]["content"]
        t = next(v for k, v in tid.items() if k in body)
        cell = ("plain" if body.endswith(sg_prompts.PLAIN_LEAD) else "quoted") + ("-flawed" if "This proves that" in body else "-clean")
        return {"grade": int(tr[(model, t, cell)])}, 0.0, None

    seed = {"order": 13, "boot": 12}
    g = run(caller_cls=StubCaller, call_fn=stub_call, seed=seed)
    r = analyse(cache=g.cache, s=seed)
    print("stub calls by model", r["calls_by_model"])
    for k, v in r["per_model"].items():
        print("stub", k, "S", round(v["S"], 2), [round(x, 2) for x in v["S_ci"]], "F", round(v["F"], 2), v["reading"])
    print("stub verdict", r["verdict"], "| cross-run quoted", {k: round(v["quoted_penalty_now_minus_sg_b4"], 2) for k, v in r["cross_run"].items()})


def tables(r):
    """The write-up's tables, regenerated from the analysis (results/sg-b7-leadin.md; reproduce.py compares them)."""
    from sg_followups import cix, fx, sx, table
    P = r["per_model"]
    ks = ("haiku", "opus", "sonnet")
    rows = []
    for k in ks:
        v = P[k]
        rows.append([k.capitalize(), v["n_usable"], sx(v.get("S")), cix(v.get("S_ci")), cix(v.get("S_ci_study")),
                     sx(v.get("F")), cix(v.get("F_ci")), fx(v.get("p")), fx(v.get("q")), sx(SG_B4_L[k]),
                     f"**{v['reading']}**" if k != "sonnet" else v["reading"]])
    t1 = table(["model", "studies", "S", "95% CI (20 domains)", "95% CI (studies)", "F", "F 95% CI (domains)",
                "penalty, 'Grade the conclusion.'", "penalty, 'Now grade the conclusion above.'", "sg-b4's L", "reading"], rows)
    rb = lambda v, f: f(v["robustness"]) if "robustness" in v else "—"
    sec = [["S as a share of sg-b4's L"] + [fx(P[k].get("share_of_sg_b4_L"), 2) for k in ks],
           ["clean text, plain − quoted (points)"] + [sx(P[k].get("clean_shift")) for k in ks],
           ["quoted penalty, this run − sg-b4's"] + [sx(r["cross_run"][k]["quoted_penalty_now_minus_sg_b4"]) for k in ks],
           ["reading on the study bootstrap"] + [P[k].get("reading_study_bootstrap", "—") for k in ks],
           ["fragile, one study dropped"] + [rb(P[k], lambda x: "yes" if x["fragile_study"] else "no") for k in ks],
           ["fragile, one domain dropped"] + [rb(P[k], lambda x: "yes" if x["fragile_domain"] else "no") for k in ks],
           ["ties (S = 0)"] + [rb(P[k], lambda x: x["n_ties"]) for k in ks],
           ["median S"] + [rb(P[k], lambda x: sx(x["median"])) for k in ks]]
    t2 = table(["", "Haiku", "Opus", "Sonnet"], sec)
    sp = r["spend_by_model"]
    t3 = table(["", "Haiku", "Opus", "Sonnet", "total"],
               [["test run", f"${sp['haiku']:.3f}", f"${sp['opus']:.3f}", f"${sp['sonnet']:.3f}", f"**${r['spend_usd']:.3f}**"]])
    return [t1, t2, t3]


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "dryrun"
    if cmd == "run":
        run()
    elif cmd == "analyse":
        r = analyse()
        (RESULTS / f"{BET}-analysis.json").write_text(json.dumps(r, indent=1))
        print(json.dumps({k: v for k, v in r.items() if k not in ("per_model", "study_sets")}, indent=1))
        for k, v in r["per_model"].items():
            print(k, {x: v.get(x) for x in ("n_usable", "S", "S_ci", "F", "F_ci", "q", "reading")})
    else:
        dryrun()
        stubrun()

"""sg-b8 (direction sg-d15): does prepending "Wait" to the own-turn grading request take away the blunting sg-b3 found?
Tsui 2025's correction marker, moved into the user's grading request, on a graded penalty. Pre-registration:
experiments/sg-b8-wait.md.

    PY=/Users/seanpharris/entangled-mind/.venv/bin/python
    $PY experiments/sg_b8_wait.py run       # paid calls (cached, capped)
    $PY experiments/sg_b8_wait.py analyse   # no calls
    $PY experiments/sg_b8_wait.py dryrun    # no calls

Six cells per study, all graded in this one run (sg-b3's design plus two cells; nothing archived enters a statistic):
    own-clean, own-flawed      sg-b3's own-turn conversation, closing request "Now grade the conclusion above. ..."
    wait-clean, wait-flawed    the same conversation, closing request "Wait. Now grade the conclusion above. ..."
                               (sg_prompts.own_turn_wait: WAIT_ABOVE = "Wait. " + GRADE_ABOVE)
    fresh-clean, fresh-flawed  sg-b3's fresh frame (sg_prompts.fresh)
Haiku and Sonnet: all 60 studies; Opus: 30 of 60, stratified by domain, drawn by the beacon seed "items".
Per study: o = own-clean - own-flawed; w = wait-clean - wait-flawed; f = fresh-clean - fresh-flawed;
W = w - o (how much "Wait" adds to the penalty in the own turn); G0 = f - o (sg-b3's blunting, this run);
Fw = own-flawed - wait-flawed (the flawed text graded lower with "Wait": the guard).
Gate: mean f >= 10 with cluster CI lower > 0 (the flaw is docked fresh) AND G0's cluster CI lower > 0 (the blunting is
there in this run to be taken away); else untestable.
Reading (sg_samerun.read): Wait shrinks it if W >= H (half the model's sg-b3 G: Haiku 6.3, Opus 3.0) with 20-domain
cluster CI lower > 0 and Fw's cluster CI lower > 0; Wait does not if W's CI upper < H; undetermined otherwise.
Verdict: untestable if Haiku or Opus is untestable; pass if both read Wait shrinks it; fail if both read Wait does not;
mixed otherwise. Sonnet's W is reported, not scored.
"""
import json
import sys

import numpy as np

import sg_samerun as S
from sg_b3_flaw import flawed
from sg_common import MODELS, RESULTS, SHORT, Caller, call
from sg_followups import cluster_boot_ci, stratified_half, test_tasks
from sg_prompts import fresh, own_turn, own_turn_wait
from sg_stats import boot_ci

BET = "sg-b8"
CAP = 1.40                 # estimate $1.24 at sg-b3's cost per call (Haiku $0.000075, Sonnet $0.0016, Opus $0.0035)
GATE = 10.0
H = {"haiku": 6.3, "opus": 3.0}          # half of each model's sg-b3 G (12.58, 5.97), as on the card
CELLS = ("own-clean", "own-flawed", "wait-clean", "wait-flawed", "fresh-clean", "fresh-flawed")
ORDER = ("claude-haiku-5-5", "claude-opus-5-5", "claude-sonnet-5-5")
LABELS = ("Wait shrinks it", "Wait does not")
FROZEN = {"WRITE": "d4d62ab7d46098edabdab5497f78fb015b3df0866d48d943c966f9b220e8f87b",
          "GRADE_ABOVE": "81dee144f1e7a5151f11654312208a21dc8dccb2c1837e6e409dbda2b805876f",
          "FRESH": "f83e57e3dc6f7866957fab998d0ef0a3041216cf4e2ab4101565bf7ba49cf6b6",
          "OVERCLAIM": "80f6f0de786c3795f6e5bc97e1c35c8856b788863ee904df3283e3db04f5b872",
          "WAIT_ABOVE": "99edc002bf1eb47f0a0a8926abbdbc1c399913ceeeb15679047caa261d7ff577"}


def plan(s=None, ts=None):
    ts = ts if ts is not None else test_tasks()
    ids = sorted(t["id"] for t in ts)
    half = stratified_half(ts, (s or S.seeds(BET))["items"])
    return {m: (half if m == "claude-opus-5-5" else ids, CELLS, 1) for m in MODELS}


def messages(cell, task, conclusion):
    c = flawed(conclusion, task) if cell.endswith("flawed") else conclusion
    if cell.startswith("wait"):
        return own_turn_wait(task["study"], c)
    if cell.startswith("fresh"):
        return fresh(task["study"], c)
    return own_turn(task["study"], c)


def check_frozen():
    import sg_prompts
    from sg_b3_flaw import check_frozen_prompts
    check_frozen_prompts()
    S.check_hashes(FROZEN)
    a, b = own_turn("S", "C"), own_turn_wait("S", "C")
    if a[:2] != b[:2] or b[2]["content"] != "Wait. " + a[2]["content"]:
        raise SystemExit("the wait cell must differ from the own-turn cell only by 'Wait. ' at the start of the last message")


def run(caller_cls=Caller, call_fn=call, check=True, seed=None):
    if check:
        check_frozen()
    s = seed or S.seeds(BET)
    return S.run(BET, plan(s), ORDER, messages, CAP, s["order"], caller_cls, call_fn)


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
    pen = lambda t, a: mc(t, f"{a}-clean") - mc(t, f"{a}-flawed")
    o, w, f = ([pen(t, a) for t in ok] for a in ("own", "wait", "fresh"))
    W = [a - b for a, b in zip(w, o)]
    G0 = [a - b for a, b in zip(f, o)]
    Gw = [a - b for a, b in zip(f, w)]
    Fw = [mc(t, "own-flawed") - mc(t, "wait-flawed") for t in ok]
    C = [mc(t, "wait-clean") - mc(t, "own-clean") for t in ok]
    fci, g0ci = cluster_boot_ci(f, cl, seed + 2), cluster_boot_ci(G0, cl, seed + 3)
    gate_flaw = S.ge(float(np.mean(f)), GATE) and S.gt(fci[0], 0)
    gate_blunt = S.gt(g0ci[0], 0)
    gate_ok = gate_flaw and gate_blunt
    out.update(W=float(np.mean(W)), W_ci=list(cluster_boot_ci(W, cl, seed)), W_ci_study=list(boot_ci(W, seed)),
               Fw=float(np.mean(Fw)), Fw_ci=list(cluster_boot_ci(Fw, cl, seed + 1)),
               G0=float(np.mean(G0)), G0_ci=list(g0ci), G_wait=float(np.mean(Gw)), G_wait_ci=list(cluster_boot_ci(Gw, cl, seed + 5)),
               P_own=float(np.mean(o)), P_wait=float(np.mean(w)), P_fresh=float(np.mean(f)), P_fresh_ci=list(fci),
               gate_flaw=gate_flaw, gate_blunting=gate_blunt, gate_ok=gate_ok,
               share_of_G0=(float(np.mean(W)) / float(np.mean(G0))) if abs(float(np.mean(G0))) > 1e-9 else None,
               clean_shift=float(np.mean(C)), clean_shift_ci=list(cluster_boot_ci(C, cl, seed + 4)),
               mean={c: float(np.mean([mc(t, c) for t in ok])) for c in CELLS}, sd_W=float(np.std(W, ddof=1)),
               tasks=ok, diffs=W)
    bar = H.get(k)
    if bar is None:
        out["reading"] = "reported only" if (out["usable_share"] >= S.USABLE and gate_flaw) else "untestable"
        return out
    out["reading"] = S.read(W, Fw, cl, bar, seed, gate_ok, out["usable_share"], LABELS)
    ci, gci = boot_ci(W, seed), boot_ci(Fw, seed + 1)
    out["reading_study_bootstrap"] = ("untestable" if not (out["usable_share"] >= S.USABLE and gate_ok) else
                                      LABELS[0] if (S.ge(out["W"], bar) and S.gt(ci[0], 0) and S.gt(gci[0], 0)) else
                                      LABELS[1] if S.lt(ci[1], bar) else "undetermined")
    if robust:
        out["robustness"] = S.robustness(W, Fw, cl, ok, bar, seed, gate_ok, out["usable_share"], LABELS, out["reading"])
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
    pl = plan(s, ts)
    b3 = S.archive("sg-b3")
    res, xr = {}, {}
    for m in MODELS:
        r = per_model(cache, m, pl[m][0], dom, s["boot"], robust)
        res[SHORT[m]] = r
        if "tasks" in r:      # secondary: sg-b3's archived G on the same studies (cross-run)
            xr[SHORT[m]] = {"G_sg_b3_same_studies": float(np.mean(
                [(b3[(m, t, "fresh-clean")] - b3[(m, t, "fresh-flawed")]) - (b3[(m, t, "own-clean")] - b3[(m, t, "own-flawed")])
                 for t in r["tasks"]]))}
    readings = {k: r["reading"] for k, r in res.items()}
    return {"bet": BET, "study_sets": {SHORT[m]: pl[m][0] for m in MODELS}, "per_model": res, "readings": readings,
            "verdict": verdict(readings), "cross_run": xr, **S.spend(cache)}


# ---------------------------------------------------------------- dry run (no calls) ---------------------------------
def truths(world, s):
    """True grades from sg-b3's archived own and fresh cells (P15):
    'nothing'     wait = own ("Wait" changes nothing)
    'all'         wait = fresh ("Wait" takes away all of the blunting)
    'at the bar'  wait-clean = own-clean, wait-flawed = own-flawed - H (W exactly the bar)
    'harsh'       wait = own - 8 on both cells (stricter overall, no flaw-specific change: W = 0)
    'clean-only'  wait-clean = own-clean + 6, wait-flawed = own-flawed (the guard must reject it)
    'item'        wait = fresh on the 14 studies whose interval excludes 0, own elsewhere (P16)"""
    b3 = S.archive("sg-b3")
    excl = {t["id"] for t in test_tasks() if t["ci_excludes_0"]}
    tr = {}
    for m, (ids, _, _) in plan(s).items():
        bar = H.get(SHORT[m], 0.7)
        for t in ids:
            oc, of, fc, ff = (b3[(m, t, c)] for c in ("own-clean", "own-flawed", "fresh-clean", "fresh-flawed"))
            wc, wf = oc, of
            if world == "all" or (world == "item" and t in excl):
                wc, wf = fc, ff
            elif world == "at the bar":     # true W exactly the bar after clipping at 0
                wf = of - bar
                if wf < 0:
                    wc, wf = oc - wf, 0.0
            elif world == "harsh":
                wc, wf = oc - 8, of - 8
            elif world == "clean-only":
                wc = oc + 6
            tr.update({(m, t, "own-clean"): oc, (m, t, "own-flawed"): of, (m, t, "wait-clean"): wc, (m, t, "wait-flawed"): wf,
                       (m, t, "fresh-clean"): fc, (m, t, "fresh-flawed"): ff})
    return tr


def simulate(world, reps=200, seed=5):
    rng = np.random.default_rng(seed)
    s = {"items": 11, "order": 13, "boot": 12}
    pl = plan(s)
    tr = truths(world, s)
    dom = {t["id"]: t["domain"] for t in test_tasks()}
    tal, rd = {}, {"haiku": {}, "opus": {}}
    for _ in range(reps):
        c = S.synth_cache(pl, tr, rng)
        sd = int(rng.integers(1 << 30))
        rr = {SHORT[m]: per_model(c, m, pl[m][0], dom, sd, robust=False)["reading"] for m in ("claude-haiku-5-5", "claude-opus-5-5")}
        v = verdict(rr)
        tal[v] = tal.get(v, 0) + 1
        for k in rd:
            rd[k][rr[k]] = rd[k].get(rr[k], 0) + 1
    return {k: round(x / reps, 3) for k, x in sorted(tal.items())}, rd


def dryrun():
    check_frozen()
    S.check_noise()
    print("P15 per-cell noise (D23):", S.REPEAT_SD)
    print("D10 frozen strings: sg-b3's at e29f25c; hashes incl. WAIT_ABOVE; the wait cell differs from own only by 'Wait. '")
    t = test_tasks()[0]
    c = "The data show a small difference whose interval includes zero."
    for cell in CELLS:
        ms = messages(cell, t, c)
        print("D2", cell, len(ms), "message(s); last message starts:", repr(ms[-1]["content"][:60]))
    pl = plan({"items": 11, "order": 13, "boot": 12})
    print("plan (dummy seed 11):", {SHORT[m]: len(v[0]) for m, v in pl.items()}, "calls", sum(len(v[0]) * len(v[1]) for v in pl.values()))
    dom = {x["id"]: x["domain"] for x in test_tasks()}
    ids = pl["claude-haiku-5-5"][0]
    mk = lambda f: {f"grade|claude-haiku-5-5|{t}|{cc}|r1": {"model": "claude-haiku-5-5", "task": t, "cond": cc, "rep": 1,
                    "grade": f(i, cc), "cost": 0} for i, t in enumerate(ids) for cc in CELLS}
    r = per_model(mk(lambda i, cc: 90), "claude-haiku-5-5", ids, dom, 1, robust=False)
    assert r["reading"] == "untestable" and not r["gate_ok"]
    print("D3 a flaw-blind grader -> untestable (gate fires)")
    r = per_model(mk(lambda i, cc: 20 if cc.endswith("flawed") else 90), "claude-haiku-5-5", ids, dom, 1, robust=False)
    assert r["reading"] == "untestable" and not r["gate_blunting"]
    print("D3 no blunting in this run (own = fresh) -> untestable (blunting gate fires)")
    ex = {"own-clean": 90, "own-flawed": 30, "wait-clean": 90, "fresh-clean": 90, "fresh-flawed": 10}
    r = per_model(mk(lambda i, cc: ex.get(cc, 30 - (6 if i % 10 else 9))), "claude-haiku-5-5", ids, dom, 1, robust=False)
    print("P13 Haiku W exactly", round(r["W"], 12), "(bar 6.3) ->", r["reading"])
    assert r["reading"] == LABELS[0]
    for w in ("nothing", "all", "at the bar", "harsh", "clean-only", "item"):
        v, rd = simulate(w)
        print("world", repr(w), "verdict", v, "| readings", rd)


def stubrun():
    """End to end with no paid call: the stub grades every cell from the 'all' world."""
    import tempfile
    import threading
    from pathlib import Path
    tmp = Path(tempfile.mkdtemp())
    seed = {"items": 11, "order": 13, "boot": 12}
    tr = truths("all", seed)
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
        if len(msgs) == 1:
            arm, body = "fresh", msgs[0]["content"]
        else:
            arm, body = ("wait" if msgs[2]["content"].startswith("Wait. ") else "own"), msgs[1]["content"]
        cell = arm + ("-flawed" if "This proves that" in body else "-clean")
        return {"grade": int(tr[(model, t, cell)])}, 0.0, None

    g = run(caller_cls=StubCaller, call_fn=stub_call, seed=seed)
    r = analyse(cache=g.cache, s=seed)
    print("stub calls by model", r["calls_by_model"])
    for k, v in r["per_model"].items():
        print("stub", k, "W", round(v["W"], 2), [round(x, 2) for x in v["W_ci"]], "G0", round(v["G0"], 2), "Fw",
              round(v["Fw"], 2), v["reading"])
    print("stub verdict", r["verdict"])


def tables(r):
    """The write-up's tables, regenerated from the analysis (results/sg-b8-wait.md; reproduce.py compares them)."""
    from sg_followups import cix, fx, sx, table
    P = r["per_model"]
    ks = ("haiku", "opus", "sonnet")
    rows = []
    for k in ks:
        v = P[k]
        rows.append([k.capitalize(), v["n_usable"], sx(v.get("W")), cix(v.get("W_ci")), cix(v.get("W_ci_study")),
                     sx(v.get("Fw")), cix(v.get("Fw_ci")), fx(v.get("P_own")), fx(v.get("P_wait")), fx(v.get("P_fresh")),
                     sx(v.get("G0")), cix(v.get("G0_ci")), f"**{v['reading']}**" if k != "sonnet" else v["reading"]])
    t1 = table(["model", "studies", "W", "95% CI (20 domains)", "95% CI (studies)", "Fw", "Fw 95% CI (domains)",
                "penalty, own turn", "penalty, own turn with 'Wait'", "penalty, fresh", "G0 = fresh − own",
                "G0 95% CI (domains)", "reading"], rows)
    rb = lambda v, f: f(v["robustness"]) if "robustness" in v else "—"
    sec = [["blunting left with 'Wait' (fresh − wait)"] + [sx(P[k].get("G_wait")) for k in ks],
           ["W as a share of G0"] + [fx(P[k].get("share_of_G0"), 2) for k in ks],
           ["sg-b3's G on the same studies (cross-run)"] + [sx(r["cross_run"][k]["G_sg_b3_same_studies"]) for k in ks],
           ["clean text, wait − own (points)"] + [sx(P[k].get("clean_shift")) for k in ks],
           ["reading on the study bootstrap"] + [P[k].get("reading_study_bootstrap", "—") for k in ks],
           ["fragile, one study dropped"] + [rb(P[k], lambda x: "yes" if x["fragile_study"] else "no") for k in ks],
           ["fragile, one domain dropped"] + [rb(P[k], lambda x: "yes" if x["fragile_domain"] else "no") for k in ks],
           ["ties (W = 0)"] + [rb(P[k], lambda x: x["n_ties"]) for k in ks],
           ["median W"] + [rb(P[k], lambda x: sx(x["median"])) for k in ks]]
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
            print(k, {x: v.get(x) for x in ("n_usable", "W", "W_ci", "Fw", "Fw_ci", "G0", "G0_ci", "reading")})
    else:
        dryrun()
        stubrun()

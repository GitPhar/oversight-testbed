"""P3-16: does 3 November's result come back when the circuit runs alone in its own job? (experiments/p3-16-lone-job.md)

    PY=entangled-mind/.venv/bin/python
    $PY experiments/p3_16_lone.py --check       # structure only, FakeFez: no network, no QPU
    $PY experiments/p3_16_lone.py --predict     # live calibration -> predictions, circuits, job order (commit before --submit)
    $PY experiments/p3_16_lone.py --submit      # every gate in code -> three jobs back to back via run_hardware
    $PY experiments/p3_16_lone.py --analyse     # from the saved raw counts

Three jobs on the original nine qubits (program 1's gate list; clbit order 117,125,124,123,144,136,143,141,142),
1,000 shots per circuit, in a seeded order:
  A  the barrier circuit, alone in its own job (3 November exactly)
  B  the no-barrier circuit, alone in its own job
  C  both circuits as two PUBs in one job (their order inside C seeded): the P3-15 condition
"""

from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from qiskit import qpy
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import ALAPScheduleAnalysis, ASAPScheduleAnalysis, PadDelay

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p3sim  # noqa: E402
from p3_15_repeat import base_isa, with_barrier, check_isa, meas_times_us, ORIG, _p, _diff, _class  # noqa: E402

ROOT = p3sim.ROOT
ENGINE = ROOT.parents[1]
SHOTS = 1000
SIM_SHOTS = 100_000
EST_JOB_CAP_S = 4.0
EST_TOTAL_CAP_S = 10.0          # the budget stated in the pre-registration (approval: the engine's budget_ruling, D29)
RESERVE_LINE_S = 300.0
BACK_TO_BACK_MIN = 60.0         # report "not back to back" if the three jobs' executions span more than this
DESIGN_REVIEW = ENGINE / "ledger" / "design-reviews" / "ng-p3-16.md"
SPEND = ENGINE / "ledger" / "spend.jsonl"
D = ROOT / "data"
SEED = D / "p3-16-seed.json"
PRED = D / "p3-16-predictions.json"
QPY = D / "p3-16-circuits.qpy"
raw_path = lambda j: D / f"p3-16-job{j}-raw.json"
OUT = ROOT / "results" / "p3-16-lone-job.json"
CODE = ["programs/nature-graded/experiments/p3_16_lone.py", "programs/nature-graded/experiments/p3_15_repeat.py",
        "programs/nature-graded/experiments/p3sim.py", "programs/entangled-mind/src"]
P315_BB = 0.29650000000000004      # P3-15's barrier 1,000-shot PUB, runs 1 and 2 pooled (0.311, 0.282; results/p3-15-repeat.json)
HIGH, BIG, ZMIN, EQUIV, CONTROL_TOL = 0.40, 0.10, 3.0, 0.05, 0.05


def build(seed_order: int):
    """Jobs in submission order: [(job, [(arm, circuit, shots), ...]), ...]."""
    isa = base_isa()
    bar = with_barrier(isa)
    rng = np.random.default_rng(seed_order)
    c_pubs = [("CB", bar, SHOTS), ("CN", isa, SHOTS)]
    c_pubs = [c_pubs[i] for i in rng.permutation(2)]
    jobs = {"A": [("A", bar, SHOTS)], "B": [("B", isa, SHOTS)], "C": c_pubs}
    order = [["A", "B", "C"][i] for i in rng.permutation(3)]
    return [(j, jobs[j]) for j in order]


def est_s(n_shots: int) -> float:
    return 0.28e-3 * n_shots + 2.0


def check():
    t = p3sim.fake_fez().target
    jobs = build(12345)
    for j, pubs in jobs:
        for _, c, _ in pubs:
            check_isa(c, t)
    bar = jobs[[j for j, _ in jobs].index("A")][1][0][1]
    isa = jobs[[j for j, _ in jobs].index("B")][1][0][1]
    print("barrier arm: same gates plus one barrier:", [i for i in bar.data if i.operation.name != "barrier"] == list(isa.data))
    for j, pubs in jobs:
        print("job", j, [(a, s) for a, _, s in pubs], "est QPU s", round(est_s(sum(s for *_, s in pubs)), 2))
    print("total est QPU s", round(sum(est_s(sum(s for *_, s in p)) for _, p in jobs), 2))


def git(*a):
    return subprocess.check_output(["git", "-C", str(ENGINE), *a], text=True).strip()


def cz_pairs():
    isa = base_isa()
    return sorted({tuple(isa.find_bit(q).index for q in i.qubits) for i in isa.data if i.operation.num_qubits == 2})


def calibration(be):
    """IBM's values with their measurement dates (audit ng-p3-15, B9), from a refreshed properties read; also the
    target's values (what the simulator uses) and every CZ pair the circuit uses (design review ng-p3-16, O1)."""
    t, props = be.target, be.properties(refresh=True)
    qs = []
    for q in ORIG:
        qp = props.qubit_property(q)
        qs.append({"qubit": q, "T1_us": qp["T1"][0] * 1e6, "T2_us": qp["T2"][0] * 1e6,
                   "readout_error": qp["readout_error"][0] if "readout_error" in qp else None,
                   "T1_date": str(qp["T1"][1]), "T2_date": str(qp["T2"][1]),
                   "readout_date": str(qp["readout_error"][1]) if "readout_error" in qp else None,
                   "target_T1_us": t.qubit_properties[q].t1 * 1e6, "target_T2_us": t.qubit_properties[q].t2 * 1e6,
                   "target_readout_error": t["measure"][(q,)].error})
    cz = []
    for a, b in cz_pairs():
        try:
            gp = props.gate_property("cz", [a, b])
            cz.append({"pair": [a, b], "error": gp["gate_error"][0], "date": str(gp["gate_error"][1]),
                       "target_error": t["cz"][(a, b)].error})
        except Exception as e:
            cz.append({"pair": [a, b], "error": None, "note": repr(e)})
    return {"read_at": dt.datetime.now(dt.timezone.utc).isoformat(), "last_update_date": str(props.last_update_date),
            "qubits": qs, "cz": cz}


def predict():
    p3sim.load_ibm_token()
    from entangled_mind import backends
    if not SEED.exists():
        raise SystemExit("no seed file: the seed commit must land first")
    sd = json.loads(SEED.read_text())
    be = backends.backend()
    t = be.target
    jobs = build(sd["seed32_order"])
    for _, pubs in jobs:
        for _, c, _ in pubs:
            check_isa(c, t)
    isa = base_isa(); bar = with_barrier(isa)
    web = p3sim.stage1_web()
    sim = p3sim.simulator(be, method="density_matrix")
    pred = {}
    for name, c, asap in (("barrier_ALAP", bar, False), ("nobarrier_ALAP", isa, False),
                          ("barrier_ASAP", bar, True), ("nobarrier_ASAP", isa, True)):
        sc = PassManager([(ASAPScheduleAnalysis if asap else ALAPScheduleAnalysis)(target=t), PadDelay(target=t)]).run(c)
        act = set(p3sim.active_qubits(c))
        keep = sc.copy_empty_like()
        for inst in sc.data:
            if inst.operation.name == "delay" and sc.find_bit(inst.qubits[0]).index not in act:
                continue
            keep.append(inst)
        cnt = sim.run(keep, shots=SIM_SHOTS, seed_simulator=sd["seed32_sim"]).result().get_counts()
        p = p3sim.p_yes(cnt, web)
        pred[name] = {"p_yes": p, "se": math.sqrt(p * (1 - p) / SIM_SHOTS), "marginals_p1": p3sim.marginals_p1(cnt, 9),
                      "measure_times_us": meas_times_us(c, t, asap)}
    circs = [c for _, pubs in jobs for _, c, _ in pubs]
    buf = io.BytesIO(); qpy.dump(circs, buf); QPY.write_bytes(buf.getvalue())
    labels = [{"job": j, "arm": a, "shots": s} for j, pubs in jobs for a, _, s in pubs]
    out = {"made_at_head": git("rev-parse", "--short", "HEAD"), "backend": be.name, "predictions": pred,
           "calibration": calibration(be), "job_order": [j for j, _ in jobs], "labels": labels,
           "estimate_qpu_s": {j: est_s(sum(s for *_, s in pubs)) for j, pubs in jobs},
           "qpy_sha256": hashlib.sha256(QPY.read_bytes()).hexdigest()}
    out["estimate_total_qpu_s"] = sum(out["estimate_qpu_s"].values())
    PRED.write_text(json.dumps(out, indent=1))
    print(json.dumps({"job_order": out["job_order"], "labels": labels, "estimate": out["estimate_qpu_s"],
                      "predictions": {n: round(v["p_yes"], 4) for n, v in pred.items()}}, indent=1))


def design_review_go() -> bool:
    if not DESIGN_REVIEW.exists():
        return False
    head = DESIGN_REVIEW.read_text().split("---")[1]
    v = [l.split(":", 1)[1].strip() for l in head.splitlines() if l.startswith("verdict:")]
    c = [l.split(":", 1)[1].strip() for l in head.splitlines() if l.startswith("confirmed_at:")]
    return bool(v) and (v[0] == "go" or (v[0] == "fix-first" and c and c[0] not in ("", "null")))


def approved_qpu_s() -> float | None:
    """D29, operators/hardware.md 'Who approves': the engine records its approval as a budget_ruling row in
    ledger/spend.jsonl citing st-16. Returns the approved QPU seconds for ng-p3-16 (the latest such row), or None."""
    if not SPEND.exists():
        return None
    got = None
    for line in SPEND.read_text().splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        if (r.get("kind") == "budget_ruling" and r.get("bet") == "ng-p3-16" and r.get("resource") == "qpu_s"
                and "st-16" in str(r.get("under", "")) and isinstance(r.get("approved_qpu_s"), (int, float))):
            got = float(r["approved_qpu_s"])
    return got


def already_logged(j: str) -> bool:
    from entangled_mind import backends
    led = json.loads(backends.USAGE_JSON.read_text()) if backends.USAGE_JSON.exists() else []
    return any(str(e.get("purpose", "")).startswith(f"Program 3 P3-16 job {j}") for e in led)


def submit():
    p3sim.load_ibm_token()
    from entangled_mind import backends
    jobs_done = [j for j in "ABC" if raw_path(j).exists() or already_logged(j)]
    if jobs_done:
        raise SystemExit(f"jobs {jobs_done} already ran (raw file or QPU ledger entry); nothing is resubmitted")
    if not design_review_go():
        raise SystemExit("no design-review go (or confirmed fix-first) at " + str(DESIGN_REVIEW))
    approved = approved_qpu_s()
    if approved is None:
        raise SystemExit("no budget_ruling row for ng-p3-16 (resource qpu_s, under st-16, approved_qpu_s) in ledger/spend.jsonl")
    if subprocess.run(["git", "-C", str(ENGINE), "ls-files", "--error-unmatch", str(SPEND)], capture_output=True).returncode \
            or git("status", "--porcelain", "--", str(SPEND)):
        raise SystemExit("ledger/spend.jsonl (the budget ruling) must be committed, unchanged, before submission (design review O2)")
    chk = subprocess.run(["python3", str(ENGINE / "ledger" / "check_prereg.py"), "ng-p3-16", str(ENGINE),
                          "programs/nature-graded/experiments/p3-16-lone-job.md", "--before-run"], capture_output=True, text=True)
    if chk.returncode != 0:
        raise SystemExit("check_prereg.py --before-run failed:\n" + chk.stdout + chk.stderr)
    dirty = git("status", "--porcelain", "--", *CODE)               # commit before submitting, always
    if dirty:
        raise SystemExit("uncommitted changes in code this run executes:\n" + dirty)
    for p in (PRED, QPY):
        if subprocess.run(["git", "-C", str(ENGINE), "ls-files", "--error-unmatch", str(p)], capture_output=True).returncode \
                or git("status", "--porcelain", "--", str(p)):
            raise SystemExit(f"{p.name} must be committed, unchanged, before submission")
    pred = json.loads(PRED.read_text())
    if hashlib.sha256(QPY.read_bytes()).hexdigest() != pred["qpy_sha256"]:
        raise SystemExit("circuit hash mismatch")
    est = pred["estimate_qpu_s"]
    if max(est.values()) > EST_JOB_CAP_S or pred["estimate_total_qpu_s"] > EST_TOTAL_CAP_S:
        raise SystemExit(f"estimate {est} above the per-job {EST_JOB_CAP_S} s or total {EST_TOTAL_CAP_S} s cap")
    if pred["estimate_total_qpu_s"] > approved:
        raise SystemExit(f"planned total {pred['estimate_total_qpu_s']:.2f} s above the approved {approved} s (D29)")
    used = max(backends.cumulative_qpu_seconds(), float(backends.service_usage()["usage_consumed_seconds"] or 0))
    if used + 1.5 * pred["estimate_total_qpu_s"] > RESERVE_LINE_S:
        raise SystemExit(f"reserve rule: {used} + 1.5 x {pred['estimate_total_qpu_s']:.1f} > {RESERVE_LINE_S}")
    circs = qpy.load(io.BytesIO(QPY.read_bytes()))
    k, billed = 0, 0.0
    for n, j in enumerate(pred["job_order"]):
        labs = [l for l in pred["labels"] if l["job"] == j]
        rest = sum(est[x] for x in pred["job_order"][n:])
        if billed + rest > approved:     # D29: never past the approved seconds, counting what earlier jobs billed
            msg = f"billed {billed} s + remaining estimate {rest:.2f} s > approved {approved} s; job {j} and later not submitted"
            for x in pred["job_order"][n:]:                             # F2 (D32): the stop is recorded, and is untestable
                raw_path(x).write_text(json.dumps({"job": x, "not_submitted": msg}, indent=1))
            raise SystemExit(msg)
        try:
            cal = calibration(backends.backend())                       # O1 (D35): IBM's values at each submission
        except Exception as e:
            cal = {"error": repr(e)}
        pubs = [(circs[k + i], None, l["shots"]) for i, l in enumerate(labs)]
        k += len(labs)
        t0 = dt.datetime.now(dt.timezone.utc).isoformat()
        try:
            counts, usage = backends.run_hardware(pubs, purpose=f"Program 3 P3-16 job {j}: {' + '.join(l['arm'] for l in labs)} "
                                                                f"({len(pubs)} pub{'s' if len(pubs) > 1 else ''}, {sum(l['shots'] for l in labs)} shots)",
                                                  shots=SHOTS)
        except Exception as e:      # recorded, never resubmitted; the remaining jobs are not submitted (section 5.3)
            raw_path(j).write_text(json.dumps({"job": j, "submitted_at": t0, "job_error": repr(e), "calibration": cal}, indent=1))
            raise SystemExit(f"job {j} failed: {e!r}; remaining jobs not submitted")
        billed += float(usage["quantum_seconds"] or 0)
        rec = {"job": j, "arms": [l["arm"] for l in labs], "submitted_at": t0, "usage": usage, "counts": counts, "calibration": cal}
        raw_path(j).write_text(json.dumps(rec, indent=1))           # saved at once, before anything else
        try:
            jb = backends.service().job(usage["job_id"])
            rec["timestamps"] = jb.metrics().get("timestamps", {})
            res = jb.result()
            spans = res.metadata.get("execution", {}).get("execution_spans")
            rec["execution_spans"] = [{"start": str(sp.start), "stop": str(sp.stop), "pubs": sorted(int(i) for i in sp.pub_idxs)}
                                      for sp in (spans or [])]
            rec["bitstrings"] = [pub.data.meas.get_bitstrings() for pub in res]
        except Exception as e:
            rec["enrich_error"] = repr(e)
        raw_path(j).write_text(json.dumps(rec, indent=1))
        print("done job", j, usage["job_id"], usage["quantum_seconds"], rec.get("timestamps"), flush=True)


def untestable(pred) -> str | None:
    for j in "ABC":
        if not raw_path(j).exists():
            return f"job {j} did not run"
        raw = json.loads(raw_path(j).read_text())
        if "job_error" in raw:
            return f"job {j} error: {raw['job_error']}"
        if "not_submitted" in raw:
            return f"job {j} not submitted: {raw['not_submitted']}"
        labs = [l for l in pred["labels"] if l["job"] == j]
        got = [sum(c.values()) for c in raw["counts"]]
        if len(got) != len(labs) or any(g != l["shots"] for g, l in zip(got, labs)):
            return f"job {j} returned shots {got} for {[l['shots'] for l in labs]}"
    return None


def _ts(raw, key):
    v = raw.get("timestamps", {}).get(key)
    return dt.datetime.fromisoformat(v.replace("Z", "+00:00")) if v else None


def _diff9(x, y):
    """F6 (D38): p3_15_repeat._diff with the difference rounded to 9 decimals before z, the CI, within_equiv and big,
    so a difference of exactly 100 shots in 1,000 (0.500 - 0.400 = 0.09999999999999998 in floating point) meets >= 0.10."""
    d = round(x["p_yes"] - y["p_yes"], 9); se = math.sqrt(x["se"] ** 2 + y["se"] ** 2)
    return {"diff": d, "se": se, "z": d / se if se else 0.0, "ci90": [d - 1.645 * se, d + 1.645 * se],
            "within_equiv": (d - 1.645 * se > -EQUIV) and (d + 1.645 * se < EQUIV),
            "big": d >= BIG and (d / se if se else 0) >= ZMIN}


def c_shared_span(spans) -> bool:
    """F-O3-r1 (D36): True if any one execution span of job C holds both of its PUBs (0 and 1)."""
    return any({0, 1} <= set(sp.get("pubs", [])) for sp in spans)


def evaluate(arms, job_order, c_spans=None, spread_min=None):
    """The scored rule and the section 5 reading (amended D31-D34), from the four arms' P(yes) and SE."""
    arms = {a: {**v, "p_yes": round(v["p_yes"], 9)} for a, v in arms.items()}   # F6 (D38): no floating-point error at 0.40
    A, B, CB, CN = arms["A"], arms["B"], arms["CB"], arms["CN"]
    prim, rep = _diff9(A, CB), _diff9(B, CN)
    comps = {"A_minus_CB (primary: alone vs shared, barrier)": prim,
             "B_minus_CN (in-evening replicate: alone vs shared, no barrier)": rep,
             "A_minus_B (barrier effect, alone)": _diff9(A, B),
             "CB_minus_CN (barrier effect, shared)": _diff9(CB, CN)}
    passed = A["p_yes"] >= HIGH and prim["diff"] >= BIG and prim["z"] >= ZMIN
    pa, pb, pcb, pcn = A["p_yes"], B["p_yes"], CB["p_yes"], CN["p_yes"]
    d, z = prim["diff"], prim["z"]
    within = prim["within_equiv"]                       # F2 (D32): the 90% CI of A - CB lies inside (-0.05, +0.05)
    when = "earlier" if job_order.index("C") < job_order.index("A") else "later"
    f = lambda x: f"{x:+.3f}"
    S, keys = [], []
    if passed:
        keys.append("pass")
        S.append("Run alone in its own job, the 3 November circuit again said 'yes' at least 40% of the time, clearly more than "
                 f"the same circuit sharing a job with one other circuit, in a separate job seconds to minutes {when}. The 3 November surprise came "
                 "at least partly from the circuit running alone in its job, not only from that afternoon.")
        if rep["big"] and pb >= HIGH:                   # F4 (D34), conditioned on B's level too (F4-r1, D36)
            keys.append("pass: replicate agrees")
            S.append("Both lone jobs (with and without the barrier) came back, and both were clearly above their shared-job twins.")
        elif rep["big"]:
            keys.append("pass: replicate clear, B below 0.40")
            S.append(f"Without the barrier, the lone job was also clearly above its shared-job twin (B − CN = {f(rep['diff'])}), "
                     f"but below 40% (B = {pb:.3f}).")
        elif pb >= HIGH:
            keys.append("pass: B high, replicate not clear")
            S.append(f"Without the barrier, the lone job also said 'yes' at least 40% of the time (B = {pb:.3f}), but was not "
                     f"clearly above its shared-job twin (B − CN = {f(rep['diff'])}).")
        else:
            keys.append("pass: rests on one job")       # F4-r2 (D37): scoped to the two lone jobs
            S.append(f"Of the two lone jobs, only the barrier job came back (B = {pb:.3f}, B − CN = {f(rep['diff'])}). The pass "
                     "rests on one job, so a passing state of the chip during that job is not ruled out.")
        if pcb >= HIGH or pcn >= HIGH:                  # D37 (recommended by the second confirmation)
            keys.append("pass: shared also came back")
            who = ("The shared job" if pcb >= HIGH and pcn >= HIGH else
                   "The barrier circuit in the shared job" if pcb >= HIGH else "The no-barrier circuit in the shared job")
            S.append(f"{who} also came back (CB = {pcb:.3f}, CN = {pcn:.3f}).")
    elif pa < HIGH:
        if within:
            keys.append("fail: within")
            S.append("Running the 3 November circuit (with its barrier) alone in its own job did not bring back 3 November's result, and for the barrier circuit, "
                     "running alone or sharing a job made no difference larger than 0.05. This evening, running the barrier circuit "
                     "alone in its own job did not raise its rate by more than 0.05 (assuming IBM's servers handled a one-circuit job "
                     "the same way on 3 November).")
        elif d >= BIG and z >= ZMIN:
            keys.append("fail: alone raised, below 0.40")
            S.append(f"Run alone, the barrier circuit said 'yes' clearly more often than sharing a job (Δ = {f(d)}), but not the 40% of "
                     "3 November. Running alone raised the rate without bringing back 3 November's result.")
        elif d > 0:
            keys.append("fail: smaller positive")
            S.append("Running the 3 November circuit (with its barrier) alone in its own job did not bring back 3 November's result. Running alone may make a "
                     f"smaller difference (Δ = {f(d)}), which this test cannot pin down.")
        else:
            clear = d <= -BIG and z <= -ZMIN
            keys.append("fail: alone lower" + (", clear" if clear else ""))
            S.append("Running the 3 November circuit (with its barrier) alone in its own job did not bring back 3 November's result. Run alone, it said "
                     f"'yes' less often than sharing a job (Δ = {f(d)})" + (", a clear difference." if clear else ", a difference this test cannot pin down."))
        if pb < HIGH and pcb < HIGH and pcn < HIGH:      # F1 (D31): only when no arm came back
            keys.append("add: none brought back")
            S.append("Of the things the 4 November runs and this one varied (the barrier, the shot grouping, running alone), none "
                     "brought back 3 November's result. The chip on that afternoon remains the main candidate among them, not a "
                     "demonstrated cause.")
        if pb >= HIGH:
            keys.append("add: B came back")
            S.append(f"Run alone without the barrier, the circuit said 'yes' at least 40% of the time (B = {pb:.3f}), but with the "
                     "barrier it did not. One lone job came back and the other did not.")
        if pcb >= HIGH or pcn >= HIGH:                  # F1-r2 (D36): name which shared-job circuit came back
            keys.append("add: shared came back")
            who = ("The shared job" if pcb >= HIGH and pcn >= HIGH else
                   "The barrier circuit in the shared job" if pcb >= HIGH else "The no-barrier circuit in the shared job")
            S.append(f"{who} came back (CB = {pcb:.3f}, CN = {pcn:.3f}) while the lone barrier job did not.")
    else:                                               # A >= 0.40, not a pass
        if pcb >= HIGH:
            if within:
                keys.append("fail: both high, within")
                S.append("The chip again said 'yes' about 40% of the time or more, alone or sharing a job. A large part of "
                         "3 November's result came back, and running alone was not what caused it.")
            elif d > 0:
                keys.append("fail: both high, alone adds")
                S.append("The chip again said 'yes' about 40% of the time or more, alone or sharing a job. A large part of "
                         "3 November's result came back alone or sharing a job; running alone may add a smaller amount "
                         f"(Δ = {f(d)}), which this test cannot pin down.")
            else:
                keys.append("fail: both high, alone lower")
                S.append("The chip again said 'yes' about 40% of the time or more, alone or sharing a job. A large part of "
                         f"3 November's result came back alone or sharing a job; running alone did not add to it (Δ = {f(d)}).")
        else:
            keys.append("fail: A high, CB not clearly lower")
            S.append("Run alone, the circuit again said 'yes' at least 40% of the time, but the shared-job version was not clearly "
                     f"lower (Δ = {f(d)}, below the 0.10 bar or z < 3). Running alone may contribute, but this test cannot show that "
                     "it caused 3 November's result.")
    ab = comps["A_minus_B (barrier effect, alone)"]
    if ab["big"]:
        keys.append("barrier alone: raised"); S.append(f"Run alone, the barrier raised the 'yes' rate by {ab['diff']:.3f}.")
    elif ab["diff"] <= -BIG and ab["z"] <= -ZMIN:      # F1-r1 (D36): a clear negative is not "a smaller difference"
        keys.append("barrier alone: lowered"); S.append(f"Run alone, the barrier lowered the 'yes' rate by {-ab['diff']:.3f}.")
    elif ab["within_equiv"]:
        keys.append("barrier alone: within"); S.append("Run alone, the barrier made no difference larger than 0.05.")
    else:
        keys.append("barrier alone: smaller"); S.append(f"Run alone, the barrier may make a smaller difference ({f(ab['diff'])}), "
                                                        "which this test cannot pin down.")
    ctrl = abs(pcb - P315_BB) <= CONTROL_TOL
    if not ctrl:
        keys.append("add: control moved")
        S.append(f"The chip itself had moved since P3-15: the shared-job barrier circuit now gives {pcb:.3f}.")
    if spread_min is not None and spread_min > BACK_TO_BACK_MIN:
        keys.append("add: not back to back"); S.append(f"The three jobs ran over {spread_min:.0f} minutes, not back to back.")
    if c_spans and not c_shared_span(c_spans):          # O3 (D35); F-O3-r1 (D36): no one span holds both PUBs
        keys.append("add: C separate spans"); S.append("The two shared-job circuits ran in separate spans.")
    return {"verdict": "pass" if passed else "fail", "comparisons": comps, "classes": {k: _class(v) for k, v in comps.items()},
            "control_CB_vs_p3_15": {"CB": pcb, "p3_15_BB_pooled": P315_BB, "within_0.05": ctrl},
            "sentence_keys": keys, "sentences": S}


def analyse():
    pred = json.loads(PRED.read_text())
    out = {"bet": "ng-p3-16", "job_order": pred["job_order"]}
    why = untestable(pred)
    if why:
        out |= {"verdict": "untestable", "why": why}
        OUT.write_text(json.dumps(out, indent=1)); print(out); return
    web = p3sim.stage1_web()
    raws = {j: json.loads(raw_path(j).read_text()) for j in "ABC"}
    arms = {}
    for j, raw in raws.items():
        for a, c in zip(raw["arms"], raw["counts"]):
            arms[a] = _p(c, web)
    starts = [_ts(r, "running") for r in raws.values()]
    ends = [_ts(r, "finished") for r in raws.values()]
    spread_min = (max(ends) - min(starts)).total_seconds() / 60 if all(starts) and all(ends) else None
    ev = evaluate(arms, pred["job_order"], raws["C"].get("execution_spans") or None, spread_min)
    out |= {"arms": arms, **ev,
            "C_same_span": c_shared_span(raws["C"]["execution_spans"]) if raws["C"].get("execution_spans") else None,
            "execution_spans": {j: r.get("execution_spans") for j, r in raws.items()},
            "timestamps": {j: r.get("timestamps") for j, r in raws.items()},
            "spread_minutes": spread_min, "back_to_back": (spread_min is not None and spread_min <= BACK_TO_BACK_MIN),
            "qpu_s": {j: r["usage"]["quantum_seconds"] for j, r in raws.items()},
            "predictions": {n: v["p_yes"] for n, v in pred["predictions"].items()},
            "calibration_predict": pred["calibration"], "calibration_submit": {j: r.get("calibration") for j, r in raws.items()}}
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("verdict", "classes", "control_CB_vs_p3_15", "C_same_span", "spread_minutes", "qpu_s")}, indent=1))
    print({a: (round(v["p_yes"], 3), round(v["se"], 3)) for a, v in arms.items()})
    print("\n".join(out["sentences"]))


def worlds(n=200):
    """F1 (D31) dry run: the reviewer's eleven worlds, binomial draws of the four arms, through evaluate()."""
    W = {"W0 nothing": (.30, .30, .30, .30), "W1 alone causes it": (.50, .50, .30, .30), "W2 lone barrier job only": (.50, .30, .30, .30),
         "W3 half return": (.40, .40, .30, .30), "W4 back everywhere": (.50, .50, .50, .50), "W5 big alone effect, A < 0.40": (.38, .38, .26, .26),
         "W6 lone no-barrier only": (.30, .50, .30, .30), "W7 shared comes back": (.30, .30, .48, .48), "W8 small alone effect": (.35, .35, .30, .30),
         "W9 alone adds 0.08": (.48, .48, .40, .40), "W10 alone lowers": (.24, .24, .30, .30)}
    order = json.loads(PRED.read_text())["job_order"] if PRED.exists() else ["C", "B", "A"]
    rng = np.random.default_rng(20261105)
    res = {}
    for name, ps in W.items():
        tally = {}
        for _ in range(n):
            arms = {}
            for a, p in zip(("A", "B", "CB", "CN"), ps):
                ph = rng.binomial(SHOTS, p) / SHOTS
                arms[a] = {"p_yes": ph, "se": math.sqrt(max(ph * (1 - ph), 1e-12) / SHOTS)}
            ev = evaluate(arms, order)
            k = (ev["verdict"],) + tuple(ev["sentence_keys"])     # F1-r1 (D36): barrier-alone keys are no longer dropped
            tally[k] = tally.get(k, 0) + 1
        res[name] = {" | ".join(k): v / n for k, v in sorted(tally.items(), key=lambda kv: -kv[1])}
        print(f"\n{name} {ps}")
        for k, v in res[name].items():
            print(f"   {v:6.3f}  {k}")
    return res


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    elif "--predict" in sys.argv:
        predict()
    elif "--submit" in sys.argv:
        submit()
    elif "--analyse" in sys.argv:
        analyse()
    elif "--worlds" in sys.argv:
        r = worlds()
        (D / "p3-16-worlds.json").write_text(json.dumps(r, indent=1))
    else:
        print(__doc__)

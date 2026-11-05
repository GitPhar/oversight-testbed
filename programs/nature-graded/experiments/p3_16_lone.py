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


def calibration(be):
    """Live target values plus IBM's measurement date for each value (audit ng-p3-15, B9: last_update_date alone is not enough)."""
    t, props = be.target, be.properties(refresh=True)
    qs = []
    for q in ORIG:
        qp = props.qubit_property(q)
        qs.append({"qubit": q, "T1_us": t.qubit_properties[q].t1 * 1e6, "T2_us": t.qubit_properties[q].t2 * 1e6,
                   "readout_error": t["measure"][(q,)].error,
                   "T1_date": str(qp["T1"][1]), "T2_date": str(qp["T2"][1]),
                   "readout_date": str(qp.get("readout_error", (None, None))[1])})
    return {"read_at": dt.datetime.now(dt.timezone.utc).isoformat(), "last_update_date": str(props.last_update_date), "qubits": qs}


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
            raise SystemExit(f"billed {billed} s + remaining estimate {rest:.2f} s > approved {approved} s; job {j} and later not submitted")
        pubs = [(circs[k + i], None, l["shots"]) for i, l in enumerate(labs)]
        k += len(labs)
        t0 = dt.datetime.now(dt.timezone.utc).isoformat()
        try:
            counts, usage = backends.run_hardware(pubs, purpose=f"Program 3 P3-16 job {j}: {' + '.join(l['arm'] for l in labs)} "
                                                                f"({len(pubs)} pub{'s' if len(pubs) > 1 else ''}, {sum(l['shots'] for l in labs)} shots)",
                                                  shots=SHOTS)
        except Exception as e:      # recorded, never resubmitted; the remaining jobs are not submitted (section 5.3)
            raw_path(j).write_text(json.dumps({"job": j, "submitted_at": t0, "job_error": repr(e)}, indent=1))
            raise SystemExit(f"job {j} failed: {e!r}; remaining jobs not submitted")
        billed += float(usage["quantum_seconds"] or 0)
        rec = {"job": j, "arms": [l["arm"] for l in labs], "submitted_at": t0, "usage": usage, "counts": counts}
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
        labs = [l for l in pred["labels"] if l["job"] == j]
        got = [sum(c.values()) for c in raw["counts"]]
        if len(got) != len(labs) or any(g != l["shots"] for g, l in zip(got, labs)):
            return f"job {j} returned shots {got} for {[l['shots'] for l in labs]}"
    return None


def _ts(raw, key):
    v = raw.get("timestamps", {}).get(key)
    return dt.datetime.fromisoformat(v.replace("Z", "+00:00")) if v else None


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
    A, B, CB, CN = arms["A"], arms["B"], arms["CB"], arms["CN"]
    prim = _diff(A, CB)
    passed = A["p_yes"] >= HIGH and prim["diff"] >= BIG and prim["z"] >= ZMIN
    comps = {"A_minus_CB (primary: alone vs shared, barrier)": prim,
             "B_minus_CN (alone vs shared, no barrier)": _diff(B, CN),
             "A_minus_B (barrier effect, alone)": _diff(A, B),
             "CB_minus_CN (barrier effect, shared)": _diff(CB, CN)}
    starts = [_ts(r, "running") for r in raws.values()]
    ends = [_ts(r, "finished") for r in raws.values()]
    spread_min = (max(ends) - min(starts)).total_seconds() / 60 if all(starts) and all(ends) else None
    out |= {"arms": arms, "comparisons": comps, "classes": {k: _class(v) for k, v in comps.items()},
            "verdict": "pass" if passed else "fail",
            "control_CB_vs_p3_15": {"CB": CB["p_yes"], "p3_15_BB_pooled": P315_BB,
                                    "within_0.05": abs(CB["p_yes"] - P315_BB) <= CONTROL_TOL},
            "C_same_span": (len(raws["C"].get("execution_spans") or []) == 1) if raws["C"].get("execution_spans") else None,
            "execution_spans": {j: r.get("execution_spans") for j, r in raws.items()},
            "timestamps": {j: r.get("timestamps") for j, r in raws.items()},
            "spread_minutes": spread_min, "back_to_back": (spread_min is not None and spread_min <= BACK_TO_BACK_MIN),
            "qpu_s": {j: r["usage"]["quantum_seconds"] for j, r in raws.items()},
            "predictions": {n: v["p_yes"] for n, v in pred["predictions"].items()},
            "calibration": pred["calibration"]}
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("verdict", "classes", "control_CB_vs_p3_15", "C_same_span", "spread_minutes", "qpu_s")}, indent=1))
    print({a: (round(v["p_yes"], 3), round(v["se"], 3)) for a, v in arms.items()})


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    elif "--predict" in sys.argv:
        predict()
    elif "--submit" in sys.argv:
        submit()
    elif "--analyse" in sys.argv:
        analyse()
    else:
        print(__doc__)

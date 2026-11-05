"""P3-15: what made 3 November different? Barrier x shot grouping, twice, >= 3 h apart (experiments/p3-15-repeat.md).

    PY=entangled-mind/.venv/bin/python
    $PY experiments/p3_15_repeat.py --check            # structure only, FakeFez: no network, no QPU
    $PY experiments/p3_15_repeat.py --predict 1|2      # live calibration -> predictions, circuits (before that run)
    $PY experiments/p3_15_repeat.py --submit 1|2       # committed predictions + a design-review go -> ONE job via run_hardware
    $PY experiments/p3_15_repeat.py --analyse          # from the saved raw counts

Per run, on the original nine qubits (program 1's gate list; clbit order 117,125,124,123,144,136,143,141,142):
  BB  barrier restored, one PUB of 1,000 shots          NB  no barrier, one PUB of 1,000 shots
  BI  barrier, 10 PUBs x 100 shots, interleaved         NI  no barrier, 10 x 100, interleaved (4 November's set-up)
  R0, R1  readout calibration, 5 x 100 each, interleaved
The job's units [BB block, NB block, interleaved section] are put in a seeded order; the interleaved section's
30 pieces are in a seeded order. 5,000 shots per run.
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
from qiskit import QuantumCircuit, qpy
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import ALAPScheduleAnalysis, ASAPScheduleAnalysis

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p3sim  # noqa: E402

ROOT = p3sim.ROOT
JOB0 = "dbl423dgg49c73dk0db0"
ORIG = [117, 125, 124, 123, 144, 136, 143, 141, 142]
BLOCK, PIECE, N_PIECES, N_CAL = 1000, 100, 10, 5
SIM_SHOTS = 100_000
EST_CAP_S = 5.0                # per run
RESERVE_LINE_S = 300.0
MIN_GAP_H = 3.0
DESIGN_REVIEW = Path("/Users/seanpharris/oversight-testbed/ledger/design-reviews/ng-p3-15.md")
D = ROOT / "data"
pred_path = lambda k: D / f"p3-15-run{k}-predictions.json"
qpy_path = lambda k: D / f"p3-15-run{k}-circuits.qpy"
raw_path = lambda k: D / f"p3-15-run{k}-raw.json"
OUT = ROOT / "results" / "p3-15-repeat.json"


def base_isa() -> QuantumCircuit:
    return p3sim.load_isa(p3sim.HW / f"{JOB0}-0.json")


def with_barrier(isa: QuantumCircuit) -> QuantumCircuit:
    """Program 1's circuit as built by measure_all(): one barrier across the nine qubits just before the measurements."""
    act = p3sim.active_qubits(isa)
    out = isa.copy_empty_like()
    placed = False
    for inst in isa.data:
        if inst.operation.name == "measure" and not placed:
            out.barrier(act)
            placed = True
        out.append(inst)
    assert placed
    return out


def readout_cal(isa: QuantumCircuit, ones: bool) -> QuantumCircuit:
    qc = isa.copy_empty_like()
    for q in ORIG:
        if ones:
            qc.x(q)
    for k, q in enumerate(ORIG):
        qc.measure(q, k)
    return qc


def meas_times_us(c: QuantumCircuit, target, asap: bool) -> list[float]:
    pm = PassManager([(ASAPScheduleAnalysis if asap else ALAPScheduleAnalysis)(target=target)])
    pm.run(c)
    ts = pm.property_set["node_start_time"]
    return sorted(round(v * target.dt * 1e6, 3) for n, v in ts.items() if n.op.name == "measure")


def build(seed_order: int):
    """Returns pubs [(circuit, None, shots)] and their labels, in job order."""
    isa = base_isa()
    bar = with_barrier(isa)
    r0, r1 = readout_cal(isa, False), readout_cal(isa, True)
    rng = np.random.default_rng(seed_order)
    pieces = [("BI", bar)] * N_PIECES + [("NI", isa)] * N_PIECES + [("R0", r0)] * N_CAL + [("R1", r1)] * N_CAL
    perm = rng.permutation(len(pieces))
    inter = [(pieces[k][0], pieces[k][1], PIECE) for k in perm]
    units = [[("BB", bar, BLOCK)], [("NB", isa, BLOCK)], inter]
    uorder = rng.permutation(3)
    seq = [p for u in uorder for p in units[u]]
    labels = [{"arm": a, "shots": s, "position": j} for j, (a, _, s) in enumerate(seq)]
    return [(c, None, s) for (_, c, s) in seq], labels, [int(u) for u in uorder]


def check_isa(c, target):
    for inst in c.data:
        if inst.operation.name == "barrier":
            continue
        qs = tuple(c.find_bit(q).index for q in inst.qubits)
        assert target.instruction_supported(inst.operation.name, qs), f"not ISA: {inst.operation.name} {qs}"


def check():
    be = p3sim.fake_fez()
    t = be.target
    isa = base_isa()
    bar = with_barrier(isa)
    for c in (isa, bar, readout_cal(isa, False), readout_cal(isa, True)):
        check_isa(c, t)
    diff = [(i.operation.name) for i in bar.data if i.operation.name == "barrier"]
    print("barrier arm adds", len(diff), "barrier on", len(bar.data[[i.operation.name for i in bar.data].index('barrier')].qubits), "qubits;",
          "gate lists otherwise identical:", [i for i in bar.data if i.operation.name != "barrier"] == list(isa.data))
    for name, c in (("no barrier", isa), ("barrier", bar)):
        print(f"{name:10s} ALAP measure times (us):", meas_times_us(c, t, False))
        print(f"{name:10s} ASAP measure times (us):", meas_times_us(c, t, True))
    pubs, labels, uorder = build(12345)
    shots = sum(s for _, _, s in pubs)
    print("pubs", len(pubs), "shots", shots, "est QPU s", round(0.28e-3 * shots + 2, 2), "unit order", uorder)
    from collections import Counter
    print("shots per arm", dict(Counter({a: 0 for a in ()}) | {a: sum(l["shots"] for l in labels if l["arm"] == a) for a in ("BB", "NB", "BI", "NI", "R0", "R1")}))


# --- predict / submit / analyse ---------------------------------------------------------------

def seeds():
    return json.loads((D / "p3-15-seed.json").read_text())


def git(*a):
    return subprocess.check_output(["git", "-C", str(ROOT), *a], text=True).strip()


def predict(k: int):
    from entangled_mind import backends
    sd = seeds()
    be = backends.backend()
    t = be.target
    isa, bar = base_isa(), with_barrier(base_isa())
    pubs, labels, uorder = build(sd[f"seed32_order{k}"])
    for c, _, _ in pubs:
        check_isa(c, t)
    web = p3sim.stage1_web()
    sim = p3sim.simulator(be, method="density_matrix")
    pred = {}
    for name, c, asap in (("barrier_ALAP", bar, False), ("nobarrier_ALAP", isa, False), ("nobarrier_ASAP", isa, True)):
        pm = PassManager([(ASAPScheduleAnalysis if asap else ALAPScheduleAnalysis)(target=t),
                          __import__("qiskit.transpiler.passes", fromlist=["PadDelay"]).PadDelay(target=t)])
        sc = pm.run(c)
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
    buf = io.BytesIO()
    qpy.dump([c for c, _, _ in pubs], buf)
    qpy_path(k).write_bytes(buf.getvalue())
    props = be.properties()
    cal = {"read_at": dt.datetime.now(dt.timezone.utc).isoformat(), "last_update_date": str(props.last_update_date),
           "qubits": [{"qubit": q, "T1_us": t.qubit_properties[q].t1 * 1e6, "T2_us": t.qubit_properties[q].t2 * 1e6,
                       "readout_error": t["measure"][(q,)].error} for q in ORIG]}
    shots = sum(s for _, _, s in pubs)
    out = {"run": k, "made_at_head": git("rev-parse", "--short", "HEAD"), "backend": be.name, "predictions": pred,
           "calibration": cal, "labels": labels, "unit_order": uorder, "shots": [s for _, _, s in pubs],
           "total_shots": shots, "estimate_qpu_s": 0.28e-3 * shots + 2.0,
           "qpy_sha256": hashlib.sha256(qpy_path(k).read_bytes()).hexdigest()}
    pred_path(k).write_text(json.dumps(out, indent=1))
    print(json.dumps({"predictions": {n: round(v["p_yes"], 4) for n, v in pred.items()}, "estimate": out["estimate_qpu_s"],
                      "unit_order": uorder, "calibration_last_update": cal["last_update_date"]}, indent=1))


def design_review_go() -> bool:
    if not DESIGN_REVIEW.exists():
        return False
    head = DESIGN_REVIEW.read_text().split("---")[1]
    v = [l.split(":", 1)[1].strip() for l in head.splitlines() if l.startswith("verdict:")]
    c = [l.split(":", 1)[1].strip() for l in head.splitlines() if l.startswith("confirmed_at:")]
    return bool(v) and (v[0] == "go" or (v[0] == "fix-first" and c and c[0] not in ("", "null")))


def submit(k: int):
    from entangled_mind import backends
    if raw_path(k).exists():
        raise SystemExit(f"run {k} already ran; nothing is resubmitted")
    if not design_review_go():
        raise SystemExit("no design-review go (or confirmed fix-first) at " + str(DESIGN_REVIEW))
    for p in (pred_path(k), qpy_path(k)):
        if subprocess.run(["git", "-C", str(ROOT), "ls-files", "--error-unmatch", str(p)], capture_output=True).returncode \
                or git("status", "--porcelain", "--", str(p)):
            raise SystemExit(f"{p.name} must be committed, unchanged, before submission")
    pred = json.loads(pred_path(k).read_text())
    if hashlib.sha256(qpy_path(k).read_bytes()).hexdigest() != pred["qpy_sha256"]:
        raise SystemExit("circuit hash mismatch")
    if k == 2:
        r1 = json.loads(raw_path(1).read_text())
        t1 = dt.datetime.fromisoformat(r1["finished_utc"])
        gap = (dt.datetime.now(dt.timezone.utc) - t1).total_seconds() / 3600
        if gap < MIN_GAP_H:
            raise SystemExit(f"only {gap:.2f} h since run 1 finished; the rule is >= {MIN_GAP_H} h")
    est = pred["estimate_qpu_s"]
    used = max(backends.cumulative_qpu_seconds(), float(backends.service_usage()["usage_consumed_seconds"] or 0))
    if est > EST_CAP_S:
        raise SystemExit(f"estimate {est:.1f} s > cap {EST_CAP_S} s")
    if used + 1.5 * est > RESERVE_LINE_S:
        raise SystemExit(f"reserve rule: {used} + 1.5 x {est:.1f} > {RESERVE_LINE_S}")
    circs = qpy.load(io.BytesIO(qpy_path(k).read_bytes()))
    pubs = [(c, None, s) for c, s in zip(circs, pred["shots"])]
    t0 = dt.datetime.now(dt.timezone.utc).isoformat()
    counts, usage = backends.run_hardware(pubs, purpose=f"Program 3 P3-15 run {k}: barrier x grouping repeat ({len(pubs)} pubs, 5,000 shots)",
                                          shots=PIECE)
    job = backends.service().job(usage["job_id"])
    ts = job.metrics().get("timestamps", {})
    raw_path(k).write_text(json.dumps({"run": k, "submitted_at": t0, "usage": usage, "timestamps": ts,
                                       "finished_utc": dt.datetime.fromisoformat(ts["finished"].replace("Z", "+00:00")).isoformat(),
                                       "counts": counts}, indent=1))
    print("done run", k, usage["job_id"], usage["quantum_seconds"], ts)


def analyse():
    web = p3sim.stage1_web()
    out = {"runs": {}}
    for k in (1, 2):
        if not raw_path(k).exists():
            continue
        pred = json.loads(pred_path(k).read_text())
        raw = json.loads(raw_path(k).read_text())
        arms = {}
        for lab, c in zip(pred["labels"], raw["counts"]):
            a = arms.setdefault(lab["arm"], {})
            for b, n in c.items():
                a[b] = a.get(b, 0) + n
        res = {}
        for a, c in arms.items():
            n = sum(c.values())
            p = p3sim.p_yes(c, web)
            res[a] = {"p_yes": p, "se": math.sqrt(p * (1 - p) / n), "shots": n, "marginals_p1": p3sim.marginals_p1(c, 9)}
        def diff(x, y):
            d = res[x]["p_yes"] - res[y]["p_yes"]
            se = math.sqrt(res[x]["se"] ** 2 + res[y]["se"] ** 2)
            return {"diff": d, "se": se, "z": d / se, "ci90": [d - 1.645 * se, d + 1.645 * se]}
        def pooled(xs):
            c = {}
            for x in xs:
                for b, n in arms[x].items():
                    c[b] = c.get(b, 0) + n
            n = sum(c.values()); p = p3sim.p_yes(c, web)
            return {"p_yes": p, "se": math.sqrt(p * (1 - p) / n), "shots": n}
        res["B_pooled"], res["N_pooled"] = pooled(["BB", "BI"]), pooled(["NB", "NI"])
        res["block_pooled"], res["inter_pooled"] = pooled(["BB", "NB"]), pooled(["BI", "NI"])
        cmp = {"BB_minus_NB": diff("BB", "NB"), "barrier_pooled": diff("B_pooled", "N_pooled"),
               "grouping_pooled": diff("block_pooled", "inter_pooled")}
        r0, r1 = res["R0"]["marginals_p1"], res["R1"]["marginals_p1"]
        out["runs"][str(k)] = {"job": raw["usage"]["job_id"], "qpu_s": raw["usage"]["quantum_seconds"],
                               "timestamps": raw["timestamps"], "arms": res, "comparisons": cmp,
                               "predictions": {n: v["p_yes"] for n, v in pred["predictions"].items()},
                               "readout": {"p1_given_0": r0, "p0_given_1": [1 - x for x in r1]}}
    r = out["runs"].get("1")
    if r:
        bb, c = r["arms"]["BB"]["p_yes"], r["comparisons"]["BB_minus_NB"]
        out["primary"] = {"BB": bb, "BB_minus_NB": c["diff"], "z": c["z"],
                          "verdict": "pass" if (bb >= 0.40 and c["diff"] >= 0.10 and c["z"] >= 3) else "fail"}
        out["control_NI_vs_nov4"] = {"NI": r["arms"]["NI"]["p_yes"], "nov4": 0.24600000000000016,
                                     "within_0.05": abs(r["arms"]["NI"]["p_yes"] - 0.24600000000000016) <= 0.05}
        e = lambda d: (d["ci90"][0] > -0.05 and d["ci90"][1] < 0.05)
        out["equivalence_run1"] = {"barrier_no_effect_gt_0.05": e(r["comparisons"]["barrier_pooled"]),
                                   "grouping_no_effect_gt_0.05": e(r["comparisons"]["grouping_pooled"])}
    if "1" in out["runs"] and "2" in out["runs"]:
        drift = {}
        for a in ("BB", "NB", "BI", "NI", "B_pooled", "N_pooled"):
            x, y = out["runs"]["2"]["arms"][a], out["runs"]["1"]["arms"][a]
            d = x["p_yes"] - y["p_yes"]; se = math.sqrt(x["se"] ** 2 + y["se"] ** 2)
            drift[a] = {"diff": d, "se": se, "z": d / se, "ci90": [d - 1.645 * se, d + 1.645 * se]}
        out["drift_run2_minus_run1"] = drift
        out["drift_stable_within_0.05"] = all(-0.05 < drift[a]["ci90"][0] and drift[a]["ci90"][1] < 0.05
                                              for a in ("B_pooled", "N_pooled"))
        if "primary" in out:
            r2 = out["runs"]["2"]
            out["run2_agrees_with_run1_label"] = (
                ("pass" if (r2["arms"]["BB"]["p_yes"] >= 0.40 and r2["comparisons"]["BB_minus_NB"]["diff"] >= 0.10
                            and r2["comparisons"]["BB_minus_NB"]["z"] >= 3) else "fail") == out["primary"]["verdict"])
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "runs"}, indent=1))
    for k, r in out["runs"].items():
        print("run", k, {a: (round(v["p_yes"], 4), round(v["se"], 4)) for a, v in r["arms"].items()})


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "--check":
        check()
    elif cmd == "--predict":
        predict(int(sys.argv[2]))
    elif cmd == "--submit":
        submit(int(sys.argv[2]))
    elif cmd == "--analyse":
        analyse()

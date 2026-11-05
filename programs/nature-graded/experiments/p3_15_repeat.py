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
    for name, c, asap in (("barrier_ALAP", bar, False), ("nobarrier_ALAP", isa, False),
                           ("barrier_ASAP", bar, True), ("nobarrier_ASAP", isa, True)):     # F3 (D13): four predictions
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
    out["predicted_barrier_effect"] = {"if_ALAP": pred["barrier_ALAP"]["p_yes"] - pred["nobarrier_ALAP"]["p_yes"],
                                       "if_ASAP": pred["barrier_ASAP"]["p_yes"] - pred["nobarrier_ASAP"]["p_yes"]}
    pred_path(k).write_text(json.dumps(out, indent=1))
    print(json.dumps({"predicted_barrier_effect": out["predicted_barrier_effect"], "predictions": {n: round(v["p_yes"], 4) for n, v in pred.items()}, "estimate": out["estimate_qpu_s"],
                      "unit_order": uorder, "calibration_last_update": cal["last_update_date"]}, indent=1))


def design_review_go() -> bool:
    if not DESIGN_REVIEW.exists():
        return False
    head = DESIGN_REVIEW.read_text().split("---")[1]
    v = [l.split(":", 1)[1].strip() for l in head.splitlines() if l.startswith("verdict:")]
    c = [l.split(":", 1)[1].strip() for l in head.splitlines() if l.startswith("confirmed_at:")]
    return bool(v) and (v[0] == "go" or (v[0] == "fix-first" and c and c[0] not in ("", "null")))


def already_logged(k: int) -> bool:
    """F5 (D15): the project QPU ledger already has this run (e.g. the process died after the job but before saving)."""
    from entangled_mind import backends
    led = json.loads(backends.USAGE_JSON.read_text()) if backends.USAGE_JSON.exists() else []
    return any(str(e.get("purpose", "")).startswith(f"Program 3 P3-15 run {k}") for e in led)


def f6_ruled() -> bool:
    """D16: Sean's budget ruling for ng-p3-15 must be recorded in a DEVIATIONS row containing 'F6 ruling:'."""
    dev = (ROOT / "DEVIATIONS.md").read_text()
    return any("F6 ruling:" in line and "ng-p3-15" in line for line in dev.splitlines() if line.startswith("|"))


def submit(k: int):
    from entangled_mind import backends
    if raw_path(k).exists() or already_logged(k):
        raise SystemExit(f"run {k} already ran (raw file or QPU ledger entry); nothing is resubmitted")
    if not design_review_go():
        raise SystemExit("no design-review go (or confirmed fix-first) at " + str(DESIGN_REVIEW))
    if not f6_ruled():
        raise SystemExit("no 'F6 ruling:' row for ng-p3-15 in DEVIATIONS.md (Sean's budget ruling, D16)")
    chk = subprocess.run(["python3", str(ROOT.parents[1] / "ledger" / "check_prereg.py"), "ng-p3-15",
                          str(ROOT.parents[1]), "programs/nature-graded/experiments/p3-15-repeat.md", "--before-run"],
                         capture_output=True, text=True)
    if chk.returncode != 0:
        raise SystemExit("check_prereg.py --before-run failed:\n" + chk.stdout + chk.stderr)
    for p in (pred_path(k), qpy_path(k)):
        if subprocess.run(["git", "-C", str(ROOT), "ls-files", "--error-unmatch", str(p)], capture_output=True).returncode \
                or git("status", "--porcelain", "--", str(p)):
            raise SystemExit(f"{p.name} must be committed, unchanged, before submission")
    pred = json.loads(pred_path(k).read_text())
    if hashlib.sha256(qpy_path(k).read_bytes()).hexdigest() != pred["qpy_sha256"]:
        raise SystemExit("circuit hash mismatch")
    if k == 2:
        r1 = json.loads(raw_path(1).read_text())
        t1 = dt.datetime.fromisoformat(r1["finished_utc"]) if "finished_utc" in r1 else \
            dt.datetime.strptime(r1["usage"]["when"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=dt.timezone.utc)
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
    try:
        before = {j.job_id() for j in backends.service().jobs(limit=5)}
    except Exception:
        before = None
    try:
        counts, usage = backends.run_hardware(pubs, purpose=f"Program 3 P3-15 run {k}: barrier x grouping repeat ({len(pubs)} pubs, 5,000 shots)",
                                              shots=PIECE)
    except Exception as e:  # job error: recorded, never resubmitted (section 5.3)
        new_job = None
        try:   # D16: record whether a job id existed (refused before submission, or failed after it)
            after = [j for j in backends.service().jobs(limit=5) if before is not None and j.job_id() not in before]
            new_job = after[0].job_id() if after else None
        except Exception:
            pass
        raw_path(k).write_text(json.dumps({"run": k, "submitted_at": t0, "job_error": repr(e),
                                           "job_id_existed": new_job is not None, "job_id": new_job}, indent=1))
        raise
    rec = {"run": k, "submitted_at": t0, "usage": usage, "counts": counts}
    raw_path(k).write_text(json.dumps(rec, indent=1))            # F5 (D15): saved at once, before anything else
    try:                                                          # enrich; never deletes what is saved
        job = backends.service().job(usage["job_id"])
        ts = job.metrics().get("timestamps", {})
        rec["timestamps"] = ts
        rec["finished_utc"] = dt.datetime.fromisoformat(ts["finished"].replace("Z", "+00:00")).isoformat()
        res = job.result()
        spans = res.metadata.get("execution", {}).get("execution_spans")
        rec["execution_spans"] = [{"start": str(sp.start), "stop": str(sp.stop), "pubs": sorted(int(i) for i in sp.pub_idxs)}
                                  for sp in (spans or [])]
        rec["bitstrings"] = [pub.data.meas.get_bitstrings() for pub in res]          # F4 (D14): per-shot order
        raw_path(k).write_text(json.dumps(rec, indent=1))
    except Exception as e:
        rec["enrich_error"] = repr(e)
        raw_path(k).write_text(json.dumps(rec, indent=1))
    print("done run", k, usage["job_id"], usage["quantum_seconds"], rec.get("timestamps"))


NOV4_NI = 0.24600000000000016          # 4 November arm A P(yes) (results/p3-2-3-job.json)
EQUIV, BIG, ZMIN, HIGH = 0.05, 0.10, 3.0, 0.40
TOTAL_SHOTS = 5000


def _p(c, web):
    n = sum(c.values()); p = p3sim.p_yes(c, web)
    return {"p_yes": p, "se": math.sqrt(max(p * (1 - p), 1e-12) / n), "shots": n,
            "marginals_p1": p3sim.marginals_p1(c, 9), **_uniformity(c)}


def _uniformity(c):
    """O2: Shannon entropy (bits) of the 9-bit distribution and total-variation distance from uniform."""
    n = sum(c.values())
    probs = np.array([v / n for v in c.values()])
    ent = float(-(probs * np.log2(probs)).sum())
    tvd = 0.5 * (float(np.abs(probs - 1 / 512).sum()) + (512 - len(probs)) / 512)
    return {"entropy_bits": ent, "tvd_from_uniform": tvd}


def _merge(cs):
    out = {}
    for c in cs:
        for b, n in c.items():
            out[b] = out.get(b, 0) + n
    return out


def _diff(x, y):
    d = x["p_yes"] - y["p_yes"]; se = math.sqrt(x["se"] ** 2 + y["se"] ** 2)
    return {"diff": d, "se": se, "z": d / se if se else 0.0, "ci90": [d - 1.645 * se, d + 1.645 * se],
            "within_equiv": (d - 1.645 * se > -EQUIV) and (d + 1.645 * se < EQUIV),
            "big": d >= BIG and (d / se if se else 0) >= ZMIN}


def _class(d):
    return "big" if d["big"] else ("within" if d["within_equiv"] else "between")


def run_untestable(pred, raw):
    """F2 (D12): section 5.3 in code."""
    if "job_error" in raw:
        return f"job error: {raw['job_error']}"
    got = [sum(c.values()) for c in raw["counts"]]
    if len(got) != len(pred["labels"]):
        return f"{len(got)} PUB results for {len(pred['labels'])} PUBs"
    if sum(got) < 0.9 * TOTAL_SHOTS:
        return f"{sum(got)} shots returned, below 90% of {TOTAL_SHOTS}"
    bad = [(l["arm"], l["shots"], g) for l, g in zip(pred["labels"], got) if g != l["shots"]]
    if bad:
        return f"PUB shot counts differ from their labels: {bad[:4]}"
    return None


def contiguous_block(raw, labels, arm):
    """F4 (D14): an arm's single PUB counts as a contiguous block only if no execution span holding it holds another PUB."""
    spans = raw.get("execution_spans")
    if not spans:
        return None
    idx = [i for i, l in enumerate(labels) if l["arm"] == arm]
    return all(set(sp["pubs"]) <= set(idx) for sp in spans if set(sp["pubs"]) & set(idx))


def analyse_run(k, web):
    pred = json.loads(pred_path(k).read_text())
    raw = json.loads(raw_path(k).read_text())
    why = run_untestable(pred, raw)
    if why:
        return {"untestable": why}
    by_arm, pieces = {}, {}
    for lab, c in zip(pred["labels"], raw["counts"]):
        by_arm.setdefault(lab["arm"], []).append(c)
    res = {a: _p(_merge(cs), web) for a, cs in by_arm.items()}
    res["B_pooled"], res["N_pooled"] = _p(_merge(by_arm["BB"] + by_arm["BI"]), web), _p(_merge(by_arm["NB"] + by_arm["NI"]), web)
    res["block_pooled"], res["inter_pooled"] = _p(_merge(by_arm["BB"] + by_arm["NB"]), web), _p(_merge(by_arm["BI"] + by_arm["NI"]), web)
    cmp = {"BB_minus_NB": _diff(res["BB"], res["NB"]), "barrier_pooled": _diff(res["B_pooled"], res["N_pooled"]),
           "grouping_pooled": _diff(res["block_pooled"], res["inter_pooled"])}
    # O3: leave-one-piece-out over the 10 BI and 10 NI pieces for the pooled secondaries
    lopo = {"barrier_pooled": [], "grouping_pooled": []}
    for arm in ("BI", "NI"):
        for j in range(len(by_arm[arm])):
            keep = {a: list(cs) for a, cs in by_arm.items()}
            keep[arm] = keep[arm][:j] + keep[arm][j + 1:]
            bp, np_ = _p(_merge(keep["BB"] + keep["BI"]), web), _p(_merge(keep["NB"] + keep["NI"]), web)
            bl, it = _p(_merge(keep["BB"] + keep["NB"]), web), _p(_merge(keep["BI"] + keep["NI"]), web)
            lopo["barrier_pooled"].append(_class(_diff(bp, np_)))
            lopo["grouping_pooled"].append(_class(_diff(bl, it)))
    lopo_stable = {k2: len(set(v)) == 1 and v[0] == _class(cmp[k2]) for k2, v in lopo.items()}
    r0, r1 = res["R0"]["marginals_p1"], res["R1"]["marginals_p1"]
    return {"job": raw["usage"]["job_id"], "qpu_s": raw["usage"]["quantum_seconds"], "timestamps": raw.get("timestamps"),
            "arms": res, "comparisons": cmp, "classes": {k2: _class(v) for k2, v in cmp.items()},
            "lopo_classes": lopo, "lopo_stable": lopo_stable,
            "BB_contiguous_block": contiguous_block(raw, pred["labels"], "BB"),
            "NB_contiguous_block": contiguous_block(raw, pred["labels"], "NB"),
            "predictions": {n: v["p_yes"] for n, v in pred["predictions"].items()},
            "predicted_barrier_effect": pred.get("predicted_barrier_effect"),
            "readout": {"p1_given_0": r0, "p0_given_1": [1 - x for x in r1]}}


def primary_label(r):
    bb, c = r["arms"]["BB"]["p_yes"], r["comparisons"]["BB_minus_NB"]
    return "pass" if (bb >= HIGH and c["diff"] >= BIG and c["z"] >= ZMIN) else "fail"


def analyse():
    web = p3sim.stage1_web()
    out = {"runs": {}}
    for k in (1, 2):
        if raw_path(k).exists():
            out["runs"][str(k)] = analyse_run(k, web)
    r = out["runs"].get("1")
    if r is None:
        out["verdict"] = "not run"
    elif "untestable" in r:
        out["verdict"] = "untestable"; out["untestable_reason"] = r["untestable"]
    else:
        out["verdict"] = primary_label(r)
        a = r["arms"]
        out["flags"] = {   # which section 5 sentences apply (F1, D11)
            "BB_high": a["BB"]["p_yes"] >= HIGH, "NB_high": a["NB"]["p_yes"] >= HIGH,
            "all_arms_high": all(a[x]["p_yes"] >= HIGH for x in ("BB", "NB", "BI", "NI")),
            "barrier_class": r["classes"]["barrier_pooled"], "grouping_class": r["classes"]["grouping_pooled"],
            "control_NI_within_0.05_of_nov4": abs(a["NI"]["p_yes"] - NOV4_NI) <= EQUIV,
            "BB_contiguous_block": r["BB_contiguous_block"]}
        out["control_NI_vs_nov4"] = {"NI": a["NI"]["p_yes"], "nov4": NOV4_NI}
    r2 = out["runs"].get("2")
    if r and r2 and "untestable" not in r and "untestable" not in r2:
        drift = {x: _diff(r2["arms"][x], r["arms"][x]) for x in ("BB", "NB", "BI", "NI", "B_pooled", "N_pooled")}
        out["drift_run2_minus_run1"] = drift
        out["drift_stable_within_0.05"] = drift["B_pooled"]["within_equiv"] and drift["N_pooled"]["within_equiv"]
        out["run2_label"] = primary_label(r2)
        out["unstable_across_runs"] = out["run2_label"] != out["verdict"]
    elif r2 is not None and "untestable" in r2:
        out["run2_untestable"] = r2["untestable"]
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "runs"}, indent=1, default=str))
    for k, rr in out["runs"].items():
        if "arms" in rr:
            print("run", k, {a: (round(v["p_yes"], 4), round(v["se"], 4)) for a, v in rr["arms"].items()})
    return out


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

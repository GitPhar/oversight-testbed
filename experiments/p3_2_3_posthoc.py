"""Post-hoc records for the P3-2 / P3-3 job (not pre-registered; audit round 2 asks, DEVIATIONS.md D6).

    PY=entangled-mind/.venv/bin/python
    $PY experiments/p3_2_3_posthoc.py exec-calibration [out.json]   # data/p3-2-3-exec-calibration.json
    $PY experiments/p3_2_3_posthoc.py mirror-sim [out.json]         # data/p3-2-3-mirror-posthoc-sim.json
    $PY experiments/p3_2_3_posthoc.py arm-sims [out.json]           # data/p3-2-3-arm-sims-posthoc.json

`exec-calibration` and `mirror-sim` are the code first run inline on 2026-11-04 ~15:54 (uncommitted then), committed
here unchanged in substance; re-running reproduces the committed files when IBM's calibration is unchanged.
`arm-sims` simulates the submitted B, B2, C, D (and A, L1, L2 for reference) circuits with the same model as the
pre-registered predictions: NoiseModel.from_backend(live ibm_fez), ALAP-scheduled with the live durations. It refuses
unless that model reproduces the committed S (0.26894, seed `order`, 100,000 shots) exactly, i.e. the live calibration
still equals the prediction-time one. It does not use p3sim.overwrite_calibration (held; D5).
"""

import datetime as dt
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p3sim  # noqa: E402
import p3_2_3_job as J  # noqa: E402
from qiskit import qpy  # noqa: E402


def exec_calibration():
    from entangled_mind import backends
    o = json.loads(J.OUT.read_text())
    pred = json.loads(J.PRED.read_text())
    job = backends.service().job(o["job"])
    ts = job.metrics().get("timestamps", {})
    when = dt.datetime.fromisoformat((ts.get("running") or ts["created"]).replace("Z", "+00:00"))
    props = backends.backend().properties(datetime=when)
    rec = {"job": o["job"], "execution_start_utc": when.isoformat(), "properties_last_update": str(props.last_update_date),
           "qubits": [], "cz_pairs": []}
    for q in sorted({x["qubit"] for x in pred["calibration"]["qubits"]}):
        def g(n):
            try:
                return float(props.qubit_property(q, n)[0])
            except Exception:
                return None
        rec["qubits"].append({"qubit": q,
                              "T1_us": g("T1") * 1e6 if g("T1") and g("T1") < 1 else g("T1"),
                              "T2_us": g("T2") * 1e6 if g("T2") and g("T2") < 1 else g("T2"),
                              "readout_error": g("readout_error"),
                              "prob_meas1_prep0": g("prob_meas1_prep0"), "prob_meas0_prep1": g("prob_meas0_prep1")})
    for p in pred["calibration"]["cz_pairs"]:
        try:
            e = float(props.gate_error("cz", p["pair"]))
        except Exception:
            e = None
        rec["cz_pairs"].append({"pair": p["pair"], "cz_error": e})
    return rec


def _model():
    from entangled_mind import backends
    be = backends.backend()
    return be, p3sim.simulator(be, method="density_matrix")


def _check_reproduces_S(be, sim):
    pred = json.loads(J.PRED.read_text())
    isa = p3sim.load_isa(p3sim.HW / f"{J.JOB0}-0.json")
    cnt = sim.run(p3sim.schedule(isa, be), shots=J.SIM_SHOTS, seed_simulator=pred["seeds32"]["order"]).result().get_counts()
    s = p3sim.p_yes(cnt, p3sim.stage1_web())
    if abs(s - pred["predictions"]["A_orig"]["p_yes"]) > 1e-12:
        raise SystemExit(f"live model no longer reproduces S ({s} vs {pred['predictions']['A_orig']['p_yes']}): calibration changed")
    return s


def mirror_sim():
    be, sim = _model()
    pred = json.loads(J.PRED.read_text())
    circ = qpy.load(io.BytesIO(J.QPY.read_bytes()))
    ok = tot = 0
    marg = [0.0] * 9
    for c, m in zip(circ, pred["meta"]):
        if m["group"] != "M":
            continue
        cnt = sim.run(p3sim.schedule(c, be), shots=1000, seed_simulator=7).result().get_counts()
        cnt = {J.flip(b, m["mask"]): v for b, v in cnt.items()}
        ok += cnt.get("0" * 9, 0)
        tot += 1000
        for k, x in enumerate(p3sim.marginals_p1(cnt, 9)):
            marg[k] += x / 20
    return {"note": "post hoc, not pre-registered: corrected simulator (live target at analysis time, ALAP) on the 20 "
                    "submitted mirror circuits, 1,000 shots each, seed 7", "success": ok / tot, "per_qubit_error": marg}


def arm_sims():
    be, sim = _model()
    s = _check_reproduces_S(be, sim)
    pred = json.loads(J.PRED.read_text())
    circ = qpy.load(io.BytesIO(J.QPY.read_bytes()))
    web = p3sim.stage1_web()
    out = {"note": "post hoc, not pre-registered (D6): the pre-registered prediction model (from_backend(live ibm_fez), "
                   "ALAP with live durations), checked to reproduce S exactly; 5,000 shots per submitted instance, "
                   "seed `order`; masks flipped back as in the analysis", "S_reproduced": s, "arms": {}}
    for g in ("A", "B", "B2", "C", "D", "L1", "L2"):
        pooled = {}
        for c, m in zip(circ, pred["meta"]):
            if m["group"] != g:
                continue
            circ_s = c if any(i.operation.name == "delay" for i in c.data) else p3sim.schedule(c, be)
            cnt = sim.run(circ_s, shots=5000, seed_simulator=pred["seeds32"]["order"]).result().get_counts()
            if m["mask"] is not None:
                cnt = {J.flip(b, m["mask"]): v for b, v in cnt.items()}
            for b, v in cnt.items():
                pooled[b] = pooled.get(b, 0) + v
        out["arms"][g] = {"p_yes": p3sim.p_yes(pooled, web), "marginals_p1": p3sim.marginals_p1(pooled, 9),
                          "shots": sum(pooled.values())}
        print(g, round(out["arms"][g]["p_yes"], 4), flush=True)
    return out


if __name__ == "__main__":
    what = sys.argv[1]
    default = {"exec-calibration": "p3-2-3-exec-calibration.json", "mirror-sim": "p3-2-3-mirror-posthoc-sim.json",
               "arm-sims": "p3-2-3-arm-sims-posthoc.json"}[what]
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else p3sim.ROOT / "data" / default
    rec = {"exec-calibration": exec_calibration, "mirror-sim": mirror_sim, "arm-sims": arm_sims}[what]()
    out.write_text(json.dumps(rec, indent=1))
    print("wrote", out)

"""P3-1: does a correctly scheduled noise model close the Stage 1 gap? (experiments/p3-1-scheduled-sim.md)

    entangled-mind/.venv/bin/python experiments/p3_1_scheduled.py

Refuses to run until data/p3-1-seed.json (the seed commit) exists. Laptop only: no network, no QPU.
Writes results/p3-1-scheduled-sim.json; the markdown is written by hand from it, plain English first.
"""

import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p3sim  # noqa: E402

SEED_FILE = p3sim.ROOT / "data" / "p3-1-seed.json"
OUT = p3sim.ROOT / "results" / "p3-1-scheduled-sim.json"
JOB = "dbl423dgg49c73dk0db0"
SHOTS = 100_000
SHOTS_EXPLORATORY = 20_000
PASS_AT = 0.40
CONTROL_TARGET, CONTROL_TOL = 0.251, 0.03   # archived Stage 1 noisy-sim P(yes), +- tolerance


def main() -> None:
    if not SEED_FILE.exists():
        raise SystemExit("no seed file: the seed commit must land before any simulation")
    seed = json.loads(SEED_FILE.read_text())["seed32_sim"]

    isa = p3sim.load_isa(p3sim.HW / f"{JOB}-0.json")
    web = p3sim.stage1_web()
    base = p3sim.fake_fez()
    be = p3sim.overwrite_calibration(base, p3sim.snapshot(JOB))
    sched = p3sim.schedule(isa, be)

    def run(circ, backend, shots, **kw):
        sim = p3sim.simulator(backend, method="density_matrix", **kw)
        c = sim.run(circ, shots=shots, seed_simulator=seed).result().get_counts()
        p = p3sim.p_yes(c, web)
        return {"p_yes": p, "se": math.sqrt(p * (1 - p) / shots), "shots": shots,
                "marginals_p1": p3sim.marginals_p1(c, 9), "counts": c}

    out = {"bet": "ng-p3-1", "seed32_sim": seed, "job": JOB,
           "circuit_duration_s": {"unscheduled_estimate": p3sim.duration_s(isa, be),
                                  "scheduled": p3sim.duration_s(sched, be)},
           "n_delays": sum(1 for i in sched.data if i.operation.name == "delay")}

    # 1. control: the same model, unscheduled (must reproduce the archived 0.251 within 0.03)
    out["control_unscheduled"] = run(isa, be, SHOTS)
    # 2. primary: scheduled
    out["scheduled"] = run(sched, be, SHOTS)
    # 3. exploratory, not scored
    out["exploratory"] = {
        "E2_scheduled_zz_0.1rad_per_cz": run(sched, be, SHOTS_EXPLORATORY, zz_phase=0.1),
        "E3_scheduled_errors_x3": run(p3sim.schedule(isa, p3sim.overwrite_calibration(base, p3sim.snapshot(JOB), scale=3.0)),
                                      p3sim.overwrite_calibration(base, p3sim.snapshot(JOB), scale=3.0), SHOTS_EXPLORATORY),
        "E1_temperature": "not run: FakeFez carries no qubit frequencies, which Aer's temperature option needs (stated in the pre-registration)",
    }
    stage1 = json.loads((p3sim.EM / "results" / "stage1-run-1.json").read_text())["arms"]
    out["archived"] = {k: {"p_yes": v["readout"]["p_yes"], "marginals_p1": p3sim.marginals_p1(v["counts"], 9)}
                       for k, v in stage1.items()}

    c = out["control_unscheduled"]["p_yes"]
    s = out["scheduled"]["p_yes"]
    control_ok = abs(c - CONTROL_TARGET) <= CONTROL_TOL
    out["verdict"] = ("untestable" if not control_ok else ("pass" if s >= PASS_AT else "fail"))
    out["rule"] = {"pass_at": PASS_AT, "control_target": CONTROL_TARGET, "control_tol": CONTROL_TOL,
                   "control_ok": control_ok}
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k not in ("exploratory", "archived")} |
                     {"control": c, "scheduled": s}, default=lambda o: "...", indent=1)[:3000])


if __name__ == "__main__":
    main()

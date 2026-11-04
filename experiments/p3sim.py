"""Shared simulator machinery for program 3 (nature-graded).

The "P3-1 model": FakeFez (qiskit-ibm-runtime 0.51.0, offline snapshot) as the device
description, with T1, T2, readout error, sx/x error and CZ error on the qubits a job used
overwritten from a job-time calibration snapshot, turned into an Aer noise model by
`NoiseModel.from_backend` (depolarising + thermal relaxation per gate, symmetric readout,
relaxation on explicit `Delay`s). "Scheduled" means the ISA circuit is ALAP-scheduled with
the target's durations and idle windows padded with `Delay`s, so waiting qubits decay.

No network and no keys are needed for anything in this module except `live_backend()`.
"""

from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

import numpy as np
from qiskit import ClassicalRegister, QuantumCircuit
from qiskit.transpiler import InstructionProperties, PassManager, QubitProperties
from qiskit.transpiler.passes import ALAPScheduleAnalysis, PadDelay
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel

ROOT = Path(__file__).resolve().parents[1]
EM = Path("/Users/seanpharris/entangled-mind")
sys.path.insert(0, str(EM / "src"))
HW = EM / "window" / "data" / "hardware"
CALIB = EM / "results" / "ibm-calibration.json"


# --- archived circuits -----------------------------------------------------

def load_isa(path: Path, n_qubits: int = 156) -> QuantumCircuit:
    """Rebuild an as-run ISA circuit, gate for gate, from an entangled-mind hardware archive."""
    rec = json.loads(Path(path).read_text())
    gates = rec["gates"]
    n_clbits = 1 + max(c for g in gates if g["gate"] == "measure" for c in g["clbits"])
    qc = QuantumCircuit(n_qubits)
    qc.add_register(ClassicalRegister(n_clbits, "meas"))
    for g in gates:
        name, qs, ps = g["gate"], g["qubits"], g.get("params", [])
        if name == "measure":
            qc.measure(qs[0], g["clbits"][0])
        elif name == "barrier":
            qc.barrier(qs)
        else:
            getattr(qc, name)(*ps, *qs)
    return qc


def active_qubits(qc: QuantumCircuit) -> list[int]:
    return sorted({qc.find_bit(q).index for inst in qc.data for q in inst.qubits
                   if inst.operation.name not in ("barrier", "delay")})


# --- device description ----------------------------------------------------

def fake_fez():
    from qiskit_ibm_runtime.fake_provider import FakeFez
    return FakeFez()


def overwrite_calibration(backend, snapshot: dict, scale: float = 1.0):
    """Return a deep copy of `backend` whose target carries the snapshot's numbers on the snapshot's
    qubits and CZ pairs (both directions). `scale` multiplies every error rate and divides T1, T2
    (exploratory only)."""
    be = copy.deepcopy(backend)
    t = be.target
    for q in snapshot["qubits"]:
        i = q["qubit"]
        t.qubit_properties[i] = QubitProperties(t1=q["T1_us"] * 1e-6 / scale, t2=q["T2_us"] * 1e-6 / scale,
                                                frequency=t.qubit_properties[i].frequency)
        for gate in ("sx", "x"):
            old = t[gate][(i,)]
            t.update_instruction_properties(gate, (i,), InstructionProperties(old.duration, q["sx_error"] * scale))
        old = t["measure"][(i,)]
        t.update_instruction_properties("measure", (i,), InstructionProperties(old.duration, min(0.5, q["readout_error"] * scale)))
    for p in snapshot["cz_pairs"]:
        for pair in (tuple(p["pair"]), tuple(p["pair"][::-1])):
            if pair in t["cz"]:
                old = t["cz"][pair]
                t.update_instruction_properties("cz", pair, InstructionProperties(old.duration, p["cz_error"] * scale))
    return be


def snapshot(job_id: str) -> dict:
    return json.loads(CALIB.read_text())[job_id]


def simulator(backend, method: str = "automatic", zz_phase: float = 0.0) -> AerSimulator:
    nm = NoiseModel.from_backend(backend, thermal_relaxation=True)
    if zz_phase:
        from qiskit_aer.noise import coherent_unitary_error
        from scipy.linalg import expm
        zz = np.diag([1, -1, -1, 1]).astype(complex)
        err = coherent_unitary_error(expm(-0.5j * zz_phase * zz))
        nm.add_all_qubit_quantum_error(err, ["cz"], warnings=False)
    return AerSimulator.from_backend(backend, noise_model=nm, method=method)


# --- scheduling ------------------------------------------------------------

def schedule(isa: QuantumCircuit, backend) -> QuantumCircuit:
    """ALAP-schedule with the target's durations and pad idle windows with Delays.
    Delays on qubits the circuit never uses are removed (they cannot affect the measured qubits)."""
    pm = PassManager([ALAPScheduleAnalysis(target=backend.target), PadDelay(target=backend.target)])
    out = pm.run(isa)
    act = set(active_qubits(isa))
    keep = out.copy_empty_like()
    for inst in out.data:
        if inst.operation.name == "delay" and out.find_bit(inst.qubits[0]).index not in act:
            continue
        keep.append(inst)
    return keep


def duration_s(qc: QuantumCircuit, backend) -> float:
    return float(qc.estimate_duration(backend.target, unit="s"))


# --- readout -----------------------------------------------------------------

def stage1_web():
    from entangled_mind import encoder
    pool = json.loads((EM / "results" / "pool-run-1.json").read_text())
    rec = {r["id"]: r for r in pool["records"]}["q01"]
    return encoder.build_web(rec["contentions"], rec["pairs"])


def p_yes(counts: dict, web) -> float:
    from entangled_mind import readout
    return readout.quantum_readout(counts, web)["p_yes"]


def marginals_p1(counts: dict, n: int) -> list[float]:
    """P(bit k = 1) for clbit k = 0..n-1 (Qiskit order: clbit 0 is the rightmost character)."""
    tot = sum(counts.values())
    return [sum(c for b, c in counts.items() if b[::-1][k] == "1") / tot for k in range(n)]

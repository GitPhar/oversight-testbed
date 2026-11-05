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
# Inside the engine monorepo (2026-11-04 17:35): program 1 is the sibling folder programs/entangled-mind. Its code,
# archives and QPU usage ledger (results/ibm-usage.json, which run_hardware's hard stop reads) are used from there.
EM = ROOT.parent / "entangled-mind"
sys.path.insert(0, str(EM / "src"))
# The IBM token stays in the old checkout's .env (Sean's instruction): loaded into this process only, never printed
# or copied. load_dotenv in entangled_mind.backends does not override variables already set.
# Loaded only by code paths that talk to IBM (design review ng-p3-5c recommendation), never at import.
_OLD_ENV = Path("/Users/seanpharris/entangled-mind/.env")


def load_ibm_token() -> None:
    import os
    from dotenv import dotenv_values
    if _OLD_ENV.exists():
        for _k, _v in dotenv_values(_OLD_ENV).items():
            if _k.startswith("IBM_QUANTUM_") and _v and _k not in os.environ:
                os.environ[_k] = _v
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


def overwrite_calibration(backend, snapshot: dict, scale: float = 1.0, legacy_t1t2_bug: bool = False):
    """Return a deep copy of `backend` whose target carries the snapshot's numbers on the snapshot's
    qubits and CZ pairs (both directions). `scale` multiplies every error rate and divides T1, T2
    (exploratory only).

    Fixed 2026-11-04 (nature-graded D8): in qiskit 2.6.1 `Target.qubit_properties` returns a new list on every
    access, so the original per-element assignment was discarded and FakeFez's T1/T2 stayed. The whole list is now
    assigned and the result asserted. `legacy_t1t2_bug=True` reproduces the original behaviour (T1/T2 untouched),
    only to regenerate the first P3-1 / P3-5 runs."""
    be = copy.deepcopy(backend)
    t = be.target
    qp = list(t.qubit_properties)
    for q in snapshot["qubits"]:
        i = q["qubit"]
        qp[i] = QubitProperties(t1=q["T1_us"] * 1e-6 / scale, t2=q["T2_us"] * 1e-6 / scale, frequency=qp[i].frequency)
    if not legacy_t1t2_bug:
        t.qubit_properties = qp
        for q in snapshot["qubits"]:
            got = t.qubit_properties[q["qubit"]]
            assert abs(got.t1 - q["T1_us"] * 1e-6 / scale) < 1e-12 and abs(got.t2 - q["T2_us"] * 1e-6 / scale) < 1e-12, \
                f"T1/T2 not written for qubit {q['qubit']}"
            assert abs(be.qubit_properties(q["qubit"]).t2 - q["T2_us"] * 1e-6 / scale) < 1e-12
    for q in snapshot["qubits"]:
        i = q["qubit"]
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


def simulator(backend, method: str = "automatic", zz_phase: float = 0.0, legacy_zz_bug: bool = False) -> AerSimulator:
    """Fixed 2026-11-04 (nature-graded D8): the ZZ phase was added as an all-qubit CZ error, which Aer ignores where a
    pair has its own (local) CZ error, i.e. everywhere after from_backend. It is now composed into every local CZ
    error (Aer's add_quantum_error composes with an existing error) and checked. `legacy_zz_bug=True` reproduces the
    original no-op."""
    nm = NoiseModel.from_backend(backend, thermal_relaxation=True)
    if zz_phase:
        from qiskit_aer.noise import coherent_unitary_error
        from scipy.linalg import expm
        zz = np.diag([1, -1, -1, 1]).astype(complex)
        err = coherent_unitary_error(expm(-0.5j * zz_phase * zz))
        if legacy_zz_bug:
            nm.add_all_qubit_quantum_error(err, ["cz"], warnings=False)
        else:
            local = dict(nm._local_quantum_errors.get("cz", {}))
            assert local, "no local CZ errors to compose with"
            for qubits, old in local.items():
                nm.add_quantum_error(err, ["cz"], list(qubits), warnings=False)
                assert nm._local_quantum_errors["cz"][qubits] != old, f"ZZ not composed on {qubits}"
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

"""P3-2 + P3-3: one interleaved ibm_fez job on the Stage 1 circuit (experiments/p3-2-twirl-dd.md, p3-3-layouts.md).

    PY=entangled-mind/.venv/bin/python
    $PY experiments/p3_2_3_job.py --check     # toy checks on FakeFez only: no network, no archive outcomes
    $PY experiments/p3_2_3_job.py --predict   # after both seed commits: live calibration, layouts, circuits, sim predictions
    $PY experiments/p3_2_3_job.py --submit    # after the prediction commit: cost checks, then ONE job via run_hardware
    $PY experiments/p3_2_3_job.py --analyse   # from the saved raw counts

Twirling and DD are built into the circuits (SamplerV2 options apply to a whole job, and run_hardware passes none),
so every arm can sit in one job, interleaved:
  A  as run (the archived ISA circuit, unchanged)            B  Pauli twirl of every CZ + measurement twirl
  B2 Pauli twirl of every CZ only (exploratory)              C  DD XY4 in every idle window (ALAP-scheduled)
  D  B + DD                                                  R0, R1  readout calibration, all-0 / all-1
  M  mirror P then U then U^dagger, P a random Pauli (exploratory)  L1, L2  arm A on two alternative 9-qubit layouts (P3-3)
Each arm = 20 circuit instances x 100 shots = 2,000 shots; 200 circuits, 20,000 shots in all.
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
from qiskit.circuit.library import XGate, YGate
from qiskit.transpiler import InstructionProperties, PassManager
from qiskit.transpiler.passes import (ALAPScheduleAnalysis, Optimize1qGatesDecomposition, PadDelay,
                                      PadDynamicalDecoupling)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p3sim  # noqa: E402

ROOT = p3sim.ROOT
JOB0 = "dbl423dgg49c73dk0db0"
N_INST, SHOTS_PER = 20, 100
GROUPS = ["A", "B", "B2", "C", "D", "R0", "R1", "M", "L1", "L2"]
SIM_SHOTS = 100_000
EST_CAP_S = 12.0             # refuse to submit if the cost estimate exceeds this
RESERVE_LINE_S = 300.0       # map month rule 1: cumulative + 1.5 x estimate must not pass 300 s
PRED = ROOT / "data" / "p3-2-3-predictions.json"
QPY = ROOT / "data" / "p3-2-3-circuits.qpy"
RAW = ROOT / "data" / "p3-2-3-raw.json"
OUT = ROOT / "results" / "p3-2-3-job.json"
ORIG_LAYOUT = [117, 125, 124, 123, 144, 136, 143, 141, 142]    # clbit k is measured on ORIG_LAYOUT[k]
PAULI = "IXYZ"


# --- circuit transforms ------------------------------------------------------------------------------

def apply_pauli(qc: QuantumCircuit, p: str, q: int) -> None:
    """Y = i X Z, so Y is rz(pi) then x (global phase dropped)."""
    if p in ("Z", "Y"):
        qc.rz(math.pi, q)
    if p in ("X", "Y"):
        qc.x(q)


def conj_through_cz(pa: str, pb: str) -> tuple[str, str]:
    """CZ (Pa x Pb) CZ = (Pa Z^[Pb has X]) x (Pb Z^[Pa has X]) up to phase."""
    mult = {("I", "Z"): "Z", ("X", "Z"): "Y", ("Y", "Z"): "X", ("Z", "Z"): "I"}
    hx = lambda p: p in ("X", "Y")
    return (mult[(pa, "Z")] if hx(pb) else pa), (mult[(pb, "Z")] if hx(pa) else pb)


def twirl(isa: QuantumCircuit, rng, target, measure_mask: list[int] | None) -> QuantumCircuit:
    """Pauli-twirl every CZ (random Paulis before, their CZ-conjugates after) and, if a mask is given, put an X
    before each masked measurement (the bit is flipped back in analysis). 1q runs are then re-synthesised into
    the target's basis, so the unitary of every run is kept exactly (up to global phase)."""
    out = isa.copy_empty_like()
    meas_q = {}
    for inst in isa.data:
        name = inst.operation.name
        qs = [isa.find_bit(q).index for q in inst.qubits]
        if name == "cz":
            pa, pb = PAULI[rng.integers(4)], PAULI[rng.integers(4)]
            apply_pauli(out, pa, qs[0]); apply_pauli(out, pb, qs[1])
            out.cz(qs[0], qs[1])
            ca, cb = conj_through_cz(pa, pb)
            apply_pauli(out, ca, qs[0]); apply_pauli(out, cb, qs[1])
        elif name == "measure":
            k = isa.find_bit(inst.clbits[0]).index
            if measure_mask is not None and measure_mask[k]:
                out.x(qs[0])
            meas_q[k] = qs[0]
            out.append(inst)
        else:
            out.append(inst)
    return PassManager([Optimize1qGatesDecomposition(target=target)]).run(out)


def with_y_target(target):
    """A copy of the target that also lists a Y gate with X's durations (so DD can place XY4); Y is replaced
    by rz(pi) x afterwards."""
    import copy
    t = copy.deepcopy(target)
    t.add_instruction(YGate(), {qa: InstructionProperties(t["x"][qa].duration, t["x"][qa].error) for qa in t["x"]})
    return t


def add_dd(isa: QuantumCircuit, target) -> QuantumCircuit:
    ty = with_y_target(target)
    pm = PassManager([ALAPScheduleAnalysis(target=ty),
                      PadDynamicalDecoupling(target=ty, dd_sequence=[XGate(), YGate(), XGate(), YGate()],
                                             qubits=p3sim.active_qubits(isa), pulse_alignment=ty.pulse_alignment),
                      ])
    s = pm.run(isa)
    act = set(p3sim.active_qubits(isa))
    out = s.copy_empty_like()
    for inst in s.data:
        if inst.operation.name == "delay" and s.find_bit(inst.qubits[0]).index not in act:
            continue                                     # unused qubits: no delays sent
        if inst.operation.name == "y":
            q = s.find_bit(inst.qubits[0]).index
            out.rz(math.pi, q); out.x(q)
        else:
            out.append(inst)
    return out


def remap(isa: QuantumCircuit, mapping: dict[int, int]) -> QuantumCircuit:
    """The same gate list with physical qubit p moved to mapping[p]."""
    out = isa.copy_empty_like()
    for inst in isa.data:
        qs = [out.qubits[mapping[isa.find_bit(q).index]] for q in inst.qubits]
        out.append(inst.operation, qs, inst.clbits)
    return out


def readout_cal(isa: QuantumCircuit, ones: bool) -> QuantumCircuit:
    qc = isa.copy_empty_like()
    for k, q in enumerate(ORIG_LAYOUT):
        if ones:
            qc.x(q)
    for k, q in enumerate(ORIG_LAYOUT):
        qc.measure(q, k)
    return qc


def mirror(isa: QuantumCircuit, pauli: list[str], target) -> QuantumCircuit:
    """Mirror on the original layout; ideal outcome: bit k = 1 iff P on ORIG_LAYOUT[k] has an X part."""
    body = isa.copy_empty_like()
    for inst in isa.data:
        if inst.operation.name != "measure":
            body.append(inst)
    # P first, then U, then U^dagger: ideal output P|0> (U is not Clifford, so U P U^dagger is not a basis state)
    qc = body.copy_empty_like()
    for k, q in enumerate(ORIG_LAYOUT):
        apply_pauli(qc, pauli[k], q)
    qc.barrier(ORIG_LAYOUT)
    qc.compose(body, inplace=True)
    qc.barrier(ORIG_LAYOUT)
    qc.compose(body.inverse(), inplace=True)
    qc.barrier(ORIG_LAYOUT)
    for k, q in enumerate(ORIG_LAYOUT):
        qc.measure(q, k)
    return PassManager([Optimize1qGatesDecomposition(target=target)]).run(qc)


# --- layouts (P3-3) ------------------------------------------------------------------------------------

class _G:
    """A small undirected graph keyed by physical qubit number, backed by rustworkx (ships with qiskit)."""

    def __init__(self, nodes, edges):
        import rustworkx as rx
        self.g = rx.PyGraph()
        self.idx = {q: self.g.add_node(q) for q in sorted(nodes)}
        for a, b in edges:
            if a in self.idx and b in self.idx and not self.g.has_edge(self.idx[a], self.idx[b]):
                self.g.add_edge(self.idx[a], self.idx[b], None)
        self.edges = [(self.g[a], self.g[b]) for a, b in self.g.edge_list()]


def interaction_graph(isa: QuantumCircuit) -> _G:
    edges = {tuple(sorted(isa.find_bit(q).index for q in inst.qubits)) for inst in isa.data if inst.operation.name == "cz"}
    return _G(p3sim.active_qubits(isa), edges)


def usable(target, props_ok) -> _G:
    """Device graph of qubits and CZ pairs that pass the pre-registered health screen."""
    nodes = [q for q in range(target.num_qubits) if props_ok(q)]
    edges = [(a, b) for (a, b), ip in target["cz"].items()
             if ip is not None and ip.error is not None and ip.error < 0.02]
    return _G(nodes, edges)


def choose_layouts(isa: QuantumCircuit, target, rng, exclude: set[int]):
    """All subgraph monomorphisms of the circuit's interaction graph into the healthy device graph that avoid
    `exclude`; ranked by median T2 of the 9 qubits (descending), ties by a seeded random key; L1 = best,
    L2 = best disjoint from L1."""
    import rustworkx as rx
    pat = interaction_graph(isa)

    def ok(q):
        qp = target.qubit_properties[q]
        m = target["measure"].get((q,))
        return (q not in exclude and qp is not None and qp.t1 and qp.t2 and m is not None
                and m.error is not None and m.error < 0.05)

    dev = usable(target, ok)
    cands = []
    for m in rx.vf2_mapping(dev.g, pat.g, subgraph=True, induced=False):
        inv = {pat.g[p]: dev.g[d] for d, p in m.items()}   # pattern (original physical) -> device qubit
        t2 = float(np.median([target.qubit_properties[d].t2 for d in inv.values()]))
        cands.append((t2, inv))
    keys = rng.random(len(cands))
    order = sorted(range(len(cands)), key=lambda i: (-cands[i][0], keys[i]))
    l1 = cands[order[0]][1]
    s1 = set(l1.values())
    l2 = next(cands[i][1] for i in order if not (set(cands[i][1].values()) & s1))
    return l1, l2, len(cands)


# --- build ---------------------------------------------------------------------------------------------

def build(isa, target, seeds, layouts):
    r_tw = np.random.default_rng(seeds["twirl"])
    r_mi = np.random.default_rng(seeds["mirror"])
    circ, meta = [], []
    for g in GROUPS:
        for i in range(N_INST):
            mask = None
            if g == "A":
                c = isa
            elif g in ("B", "D"):
                mask = [int(b) for b in r_tw.integers(0, 2, 9)]
                c = twirl(isa, r_tw, target, mask)
                if g == "D":
                    c = add_dd(c, target)
            elif g == "B2":
                c = twirl(isa, r_tw, target, None)
            elif g == "C":
                c = add_dd(isa, target)
            elif g in ("R0", "R1"):
                c = readout_cal(isa, g == "R1")
            elif g == "M":
                pauli = [PAULI[k] for k in r_mi.integers(0, 4, 9)]
                c = mirror(isa, pauli, target)
                mask = [int(p in ("X", "Y")) for p in pauli]     # the ideal outcome; analysis flips it to all-0
            else:
                c = remap(isa, layouts[g])
            circ.append(c)
            meta.append({"group": g, "instance": i, "mask": mask})
    perm = np.random.default_rng(seeds["order"]).permutation(len(circ))
    return [circ[k] for k in perm], [meta[k] | {"position": int(j)} for j, k in enumerate(perm)]


def check_isa(c: QuantumCircuit, target) -> None:
    for inst in c.data:
        n = inst.operation.name
        if n == "barrier":
            continue
        qs = tuple(c.find_bit(q).index for q in inst.qubits)
        assert target.instruction_supported(n, qs), f"not ISA: {n} on {qs}"


# --- checks before pre-registration (toy circuits / FakeFez only) ---------------------------------------

def check():
    from qiskit.quantum_info import Operator
    be = p3sim.fake_fez()
    t = be.target
    rng = np.random.default_rng(0)
    # twirl exactness on a small CZ circuit (on qubits 0, 1 of the device)
    toy = QuantumCircuit(156, 2)
    toy.sx(0); toy.rz(0.3, 1); toy.cz(0, 1); toy.sx(1); toy.rz(1.1, 0); toy.cz(0, 1); toy.sx(0)
    small = lambda c: Operator(c.remove_final_measurements(inplace=False)).data if c.num_qubits < 10 else None
    def two(c):
        q2 = QuantumCircuit(2)
        for inst in c.data:
            if inst.operation.name in ("measure", "barrier", "delay"):
                continue
            q2.append(inst.operation, [c.find_bit(q).index for q in inst.qubits])
        return Operator(q2)
    ref = two(toy)
    for _ in range(20):
        tw = twirl(toy, rng, t, None)
        assert two(tw).equiv(ref), "twirl changed the unitary"
        check_isa(tw, t)
    print("twirl: 20 random twirls of a 2-CZ toy circuit keep its unitary exactly; ISA ok")
    # DD keeps the unitary and is ISA
    dd = add_dd(toy, t)
    assert two(dd).equiv(ref), "DD changed the unitary"
    check_isa(dd, t)
    print("dd: XY4 padding keeps the unitary; ISA ok;", dict(dd.count_ops()))
    # mirror on the toy: U P U^dag = P up to phase
    print("mirror and remap are exercised on the real circuit in --predict (structure only)")


# --- predict (after both seed commits) -----------------------------------------------------------------

def git_head():
    return subprocess.check_output(["git", "-C", str(ROOT), "rev-parse", "--short", "HEAD"], text=True).strip()


def live_backend():
    from entangled_mind import backends
    return backends.backend()


def calib_record(be, qubits, pairs):
    t = be.target
    props = be.properties()
    rec = {"read_at": dt.datetime.now(dt.timezone.utc).isoformat(), "last_update_date": str(props.last_update_date),
           "qubits": [], "cz_pairs": []}
    for q in sorted(qubits):
        qp = t.qubit_properties[q]
        rec["qubits"].append({"qubit": q, "T1_us": qp.t1 * 1e6, "T2_us": qp.t2 * 1e6,
                              "readout_error": t["measure"][(q,)].error, "sx_error": t["sx"][(q,)].error})
    for a, b in sorted(pairs):
        ip = t["cz"].get((a, b)) or t["cz"].get((b, a))
        rec["cz_pairs"].append({"pair": [a, b], "cz_error": ip.error, "duration_s": ip.duration})
    return rec


def predict():
    seeds = {**json.loads((ROOT / "data" / "p3-2-seed.json").read_text()),
             **json.loads((ROOT / "data" / "p3-3-seed.json").read_text())}
    s2 = json.loads((ROOT / "data" / "p3-2-seed.json").read_text())
    s3 = json.loads((ROOT / "data" / "p3-3-seed.json").read_text())
    sd = {"twirl": s2["seed32_twirl"], "mirror": s2["seed32_mirror"], "order": s2["seed32_order"],
          "layout": s3["seed32_layout"]}
    be = live_backend()
    t = be.target
    isa = p3sim.load_isa(p3sim.HW / f"{JOB0}-0.json")
    l1, l2, n_cands = choose_layouts(isa, t, np.random.default_rng(sd["layout"]), exclude=set(ORIG_LAYOUT))
    layouts = {"L1": l1, "L2": l2}
    circuits, meta = build(isa, t, sd, layouts)
    for c in circuits:
        check_isa(c, t)
    # corrected-simulator predictions from the live calibration (P3-1 construction: from_backend + ALAP schedule)
    web = p3sim.stage1_web()
    sim = p3sim.simulator(be, method="density_matrix")
    pred = {}
    for name, c in (("A_orig", isa), ("L1", remap(isa, l1)), ("L2", remap(isa, l2))):
        cnt = sim.run(p3sim.schedule(c, be), shots=SIM_SHOTS, seed_simulator=sd["order"]).result().get_counts()
        p = p3sim.p_yes(cnt, web)
        pred[name] = {"p_yes": p, "se": math.sqrt(p * (1 - p) / SIM_SHOTS),
                      "marginals_p1": p3sim.marginals_p1(cnt, 9), "duration_s": p3sim.duration_s(p3sim.schedule(c, be), be)}
    buf = io.BytesIO()
    qpy.dump(circuits, buf)
    QPY.write_bytes(buf.getvalue())
    used = set(ORIG_LAYOUT) | set(l1.values()) | set(l2.values())
    pairs = set()
    for c in (isa, remap(isa, l1), remap(isa, l2)):
        pairs |= {tuple(sorted(e)) for e in interaction_graph(c).edges}
    shots = len(circuits) * SHOTS_PER
    out = {"made_at_head": git_head(), "backend": be.name, "seeds32": sd,
           "layouts": {k: {str(p): d for p, d in v.items()} for k, v in layouts.items()},
           "layout_qubits_in_clbit_order": {k: [v[p] for p in ORIG_LAYOUT] for k, v in layouts.items()},
           "n_layout_candidates": n_cands,
           "predictions": pred, "calibration": calib_record(be, used, pairs),
           "n_circuits": len(circuits), "shots_per_circuit": SHOTS_PER, "total_shots": shots,
           "estimate_qpu_s": 0.28e-3 * shots + 2.0,
           "qpy_sha256": hashlib.sha256(QPY.read_bytes()).hexdigest(), "meta": meta,
           "ops": {g: dict(circuits[[m["group"] for m in meta].index(g)].count_ops()) for g in GROUPS},
           "pulse_alignment": t.pulse_alignment, "dt": t.dt}
    PRED.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: out[k] for k in ("layout_qubits_in_clbit_order", "n_layout_candidates", "predictions",
                                          "total_shots", "estimate_qpu_s", "ops")}, indent=1))


# --- submit (after the prediction commit) --------------------------------------------------------------

def submit():
    from entangled_mind import backends
    if RAW.exists():
        raise SystemExit("raw results already exist: this bet's one job has run; nothing is resubmitted")
    st = subprocess.check_output(["git", "-C", str(ROOT), "status", "--porcelain", "--", str(PRED), str(QPY)], text=True)
    tracked = subprocess.run(["git", "-C", str(ROOT), "ls-files", "--error-unmatch", str(PRED), str(QPY)],
                             capture_output=True).returncode == 0
    if st.strip() or not tracked:
        raise SystemExit("the prediction file and circuits must be committed, unchanged, before submission")
    pred = json.loads(PRED.read_text())
    if hashlib.sha256(QPY.read_bytes()).hexdigest() != pred["qpy_sha256"]:
        raise SystemExit("circuit file hash does not match the prediction commit")
    est = pred["estimate_qpu_s"]
    used = max(backends.cumulative_qpu_seconds(), float(backends.service_usage()["usage_consumed_seconds"] or 0))
    if est > EST_CAP_S:
        raise SystemExit(f"estimate {est:.1f} s exceeds the pre-registered cap {EST_CAP_S} s")
    if used + 1.5 * est > RESERVE_LINE_S:
        raise SystemExit(f"reserve rule: {used} + 1.5 x {est:.1f} > {RESERVE_LINE_S}")
    circuits = qpy.load(io.BytesIO(QPY.read_bytes()))
    t0 = dt.datetime.now(dt.timezone.utc).isoformat()
    counts, usage = backends.run_hardware(circuits, purpose="Program 3 wave 1: P3-2 twirl/DD + P3-3 layouts (200 circuits)",
                                          shots=SHOTS_PER)
    RAW.write_text(json.dumps({"submitted_at": t0, "usage": usage, "counts": counts}, indent=1))
    print("done", usage["job_id"], usage["quantum_seconds"])


# --- analyse -------------------------------------------------------------------------------------------

def flip(bitstr: str, mask: list[int]) -> str:
    """Bit k is character -(k+1); flip where mask[k] = 1."""
    b = list(bitstr)
    for k, m in enumerate(mask):
        if m:
            b[-(k + 1)] = "1" if b[-(k + 1)] == "0" else "0"
    return "".join(b)


def analyse():
    pred = json.loads(PRED.read_text())
    raw = json.loads(RAW.read_text())
    web = p3sim.stage1_web()
    groups = {g: [] for g in GROUPS}
    for m, c in zip(pred["meta"], raw["counts"]):
        if m["mask"] is not None:
            c = {flip(b, m["mask"]): n for b, n in c.items()}
        groups[m["group"]].append(c)
    res = {}
    for g, lst in groups.items():
        pooled = {}
        for c in lst:
            for b, n in c.items():
                pooled[b] = pooled.get(b, 0) + n
        inst = [p3sim.p_yes(c, web) for c in lst]
        res[g] = {"p_yes": p3sim.p_yes(pooled, web), "se": float(np.std(inst, ddof=1) / math.sqrt(len(inst))),
                  "se_binomial": math.sqrt(max(1e-12, p3sim.p_yes(pooled, web) * (1 - p3sim.p_yes(pooled, web)) / sum(pooled.values()))),
                  "shots": sum(pooled.values()), "instances": len(lst), "marginals_p1": p3sim.marginals_p1(pooled, 9),
                  "p_all_zero": pooled.get("0" * 9, 0) / sum(pooled.values()), "pooled": pooled}
    P = pred["predictions"]
    S = P["A_orig"]["p_yes"]
    gap_a = res["A"]["p_yes"] - S
    sgn = 1 if gap_a > 0 else -1

    def toward(g):
        mv = sgn * (res["A"]["p_yes"] - res[g]["p_yes"])
        z = mv / math.sqrt(res["A"]["se"] ** 2 + res[g]["se"] ** 2)
        return {"movement_toward_sim": mv, "z": z, "diff": res[g]["p_yes"] - res["A"]["p_yes"]}

    p32 = {"S_orig": S, "gap_A": gap_a, "B": toward("B"), "B2": toward("B2"), "C": toward("C"), "D": toward("D")}
    if abs(gap_a) < 0.125:
        p32["verdict"] = "untestable"
    else:
        p32["verdict"] = "pass" if (p32["B"]["movement_toward_sim"] >= 0.125 and p32["B"]["z"] >= 3) else "fail"
    gap_orig = abs(gap_a)
    p33 = {"gap_orig": gap_orig,
           "L1": {"hw": res["L1"]["p_yes"], "sim": P["L1"]["p_yes"], "gap": abs(res["L1"]["p_yes"] - P["L1"]["p_yes"])},
           "L2": {"hw": res["L2"]["p_yes"], "sim": P["L2"]["p_yes"], "gap": abs(res["L2"]["p_yes"] - P["L2"]["p_yes"])}}
    if gap_orig < 0.10:
        p33["verdict"] = "untestable"
    else:
        p33["verdict"] = "pass" if (p33["L1"]["gap"] < 0.5 * gap_orig and p33["L2"]["gap"] < 0.5 * gap_orig) else "fail"
    # defaults for waves 2-3 (rule pre-registered in p3-2-twirl-dd.md section 5)
    bd = res["B"]["p_yes"] - res["A"]["p_yes"]
    bz = abs(bd) / math.sqrt(res["A"]["se"] ** 2 + res["B"]["se"] ** 2)
    defaults = {"twirl": bool(p32["verdict"] == "pass" or (abs(bd) >= 0.05 and bz >= 3)),
                "dd": bool(p32["C"]["movement_toward_sim"] >= 0.05 and p32["C"]["z"] >= 3)}
    # mirror success and readout matrices (secondary)
    r0, r1 = res["R0"]["marginals_p1"], res["R1"]["marginals_p1"]
    out = {"job": raw["usage"]["job_id"], "qpu_s": raw["usage"]["quantum_seconds"], "arms": res,
           "p3_2": p32, "p3_3": p33, "defaults_waves_2_3": defaults,
           "readout": {"p1_given_0": r0, "p0_given_1": [1 - x for x in r1]},
           "mirror_success": res["M"]["p_all_zero"]}
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "arms"} |
                     {"arms": {g: (round(r["p_yes"], 4), round(r["se"], 4)) for g, r in res.items()}}, indent=1))


if __name__ == "__main__":
    {"--check": check, "--predict": predict, "--submit": submit, "--analyse": analyse}[sys.argv[1]]()

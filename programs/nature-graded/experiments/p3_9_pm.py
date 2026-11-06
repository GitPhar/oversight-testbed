"""P3-9: sequential Peres-Mermin on ibm_fez under the exact Contextuality-by-Default 2.0 linear program
(experiments/p3-9-peres-mermin.md, bet ng-p3-9; scored). The chip is a referee and the object measured here, never a
computational resource: its counts decide a pre-registered bet about the device, and nothing uses them as an estimate
of anything else. Every circuit is three qubits and is simulated exactly on a laptop below.

    PY=/Users/seanpharris/entangled-mind/.venv/bin/python
    $PY experiments/p3_9_pm.py --check      # offline: LP self-tests, circuits on a fake target, the rule on synthetic tables
    $PY experiments/p3_9_pm.py --select     # free read of IBM's properties -> qubit triple by the rule, ISA circuits (qpy),
                                            # ideal + noisy-simulator prediction (data/p3-9-prepared.json); commit before --submit
    $PY experiments/p3_9_pm.py --worlds     # P(pass) under the named worlds, from the committed prediction (D11)
    $PY experiments/p3_9_pm.py --submit     # every gate in code -> one SamplerV2 job via run_hardware; raw counts saved at once
    $PY experiments/p3_9_pm.py --retrieve   # free read, only after a client error: the marker's job id -> its counts or status
    $PY experiments/p3_9_pm.py --analyse    # from the committed raw counts: CNT2 per system, bootstrap, verdict sentences

The job: 6 lines of the square (3 rows, 3 columns) x 2 orders (forward, reverse) x 2 input states (|00>, Bell) = 24
circuits x 4,000 shots = 96,000 shots, in a beacon-seeded order. Estimate 0.28 ms x 96,000 + 2 s = 28.9 s nominal;
cap 45 s in code (x1.5 contingency for dynamic circuits, 43.3 s, rounded up).
"""

from __future__ import annotations

import datetime as dt
import hashlib
import io
import itertools
import json
import multiprocessing as mp
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cbd_lp as L  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent                       # programs/nature-graded
ENGINE = ROOT.parents[1]
EM = ROOT.parent / "entangled-mind"
sys.path.insert(0, str(EM / "src"))

BET = "ng-p3-9"
PREREG = "programs/nature-graded/experiments/p3-9-peres-mermin.md"
STATES = ("00", "bell")
ORDERS = ("fwd", "rev")
SHOTS = 4000
EST_PER_SHOT_S, EST_PER_JOB_S = 0.28e-3, 2.0
EST_CAP_S = 45.0                         # the budget stated in the pre-registration; approval: a budget_ruling row
RESERVE_LINE_S = 300.0
HARD_STOP_S = 420.0
MIN_SHOT_FRAC = 0.90
B = 1000                                 # bootstrap draws per system
LB_RANK = 10                             # 99% lower bound = the 10th smallest of 1,000 draws
TOL = L.TOL                              # 1e-6: CNT2 above this is "not zero" (P13)
SIM_SHOTS = 200_000                      # per circuit, for the noisy-simulator prediction
# selection rule (frozen in the pre-registration)
MAX_RO, MAX_CZ, MIN_T_US = 0.05, 0.02, 50.0

D = ROOT / "data"
SEED_FILE = D / "p3-9-seed.json"
PREP = D / "p3-9-prepared.json"
QPY = D / "p3-9-circuits.qpy"
RAW = D / "p3-9-raw.json"
MARKER = D / "p3-9-submitting.json"      # written before run_hardware; never removed
WORLDS = D / "p3-9-worlds.json"
OUT = ROOT / "results" / "p3-9-peres-mermin.json"
DESIGN_REVIEW = ENGINE / "ledger" / "design-reviews" / "ng-p3-9.md"
SPEND = ENGINE / "ledger" / "spend.jsonl"
CODE = ["programs/nature-graded/experiments/p3_9_pm.py", "programs/nature-graded/experiments/cbd_lp.py",
        "programs/entangled-mind/src", PREREG, "ledger/check_prereg.py"]
SELECT_USES = ["programs/nature-graded/experiments/p3_9_pm.py", "programs/nature-graded/experiments/cbd_lp.py",
               "programs/entangled-mind/src"]
SUBMIT_USES = CODE + ["programs/nature-graded/data/p3-9-seed.json", "programs/nature-graded/data/p3-9-prepared.json",
                      "programs/nature-graded/data/p3-9-circuits.qpy", "ledger/design-reviews/ng-p3-9.md", "ledger/spend.jsonl"]
ANALYSE_USES = SUBMIT_USES + ["programs/nature-graded/data/p3-9-raw.json", "programs/nature-graded/data/p3-9-submitting.json"]


class NotSubmitted(Exception):
    pass


# --- circuits ------------------------------------------------------------------------------------------------------

def labels():
    """The 24 circuits in canonical order: (state, line index, order)."""
    return [{"state": s, "line": k, "line_name": L.LINE_NAMES[k], "order": o,
             "measured": list(L.LINES[k] if o == "fwd" else L.LINES[k][::-1])}
            for s in STATES for k in range(6) for o in ORDERS]


def logical(lab):
    """Three virtual qubits: 0 = data qubit '1', 1 = ancilla, 2 = data qubit '2'. One classical register 'meas' with
    three bits; bit j = the j-th observable measured. Each observable is measured by the same block in every context
    (rotate the data qubits so the Pauli is Z..Z, CNOT each involved data qubit onto the ancilla, rotate back, measure
    the ancilla mid-circuit, reset it), separated by barriers so no gate crosses from one block to the next."""
    from qiskit import ClassicalRegister, QuantumCircuit, QuantumRegister
    q = QuantumRegister(3, "q")
    c = ClassicalRegister(3, "meas")
    qc = QuantumCircuit(q, c, name=f"{lab['state']}-{lab['line_name']}-{lab['order']}")
    d = {"1": 0, "2": 2}
    if lab["state"] == "bell":       # (|00> + |11>)/sqrt2 on the data qubits through the ancilla; ancilla back to |0>
        qc.h(0); qc.cx(0, 1); qc.cx(1, 2); qc.cx(0, 1)
    qc.barrier()
    for j, obs in enumerate(lab["measured"]):
        paulis = [(obs[i], obs[i + 1]) for i in range(0, len(obs), 2)]       # e.g. "Z1X2" -> [("Z","1"),("X","2")]
        for p, w in paulis:
            if p == "X":
                qc.h(d[w])
            elif p == "Y":
                qc.sdg(d[w]); qc.h(d[w])
        for p, w in paulis:
            qc.cx(d[w], 1)
        for p, w in paulis:
            if p == "X":
                qc.h(d[w])
            elif p == "Y":
                qc.h(d[w]); qc.s(d[w])
        qc.measure(1, j)
        qc.reset(1)
        qc.barrier()
    return qc


def isa(qc, backend, layout):
    """Map the three virtual qubits onto the physical triple and translate to the target's basis, optimisation level 0
    (no gate is merged or moved; the barriers stay)."""
    from qiskit import transpile
    return transpile(qc, backend=backend, initial_layout=list(layout), optimization_level=0, seed_transpiler=9)


def check_isa(c, target, layout):
    used = set()
    for inst in c.data:
        qs = tuple(c.find_bit(x).index for x in inst.qubits)
        name = inst.operation.name
        if name == "barrier":
            continue
        assert name in target.operation_names, f"{name} not in target"
        assert target.instruction_supported(name, qs), f"{name} on {qs} not supported"
        used.update(qs)
    assert used <= set(layout), f"qubits {sorted(used - set(layout))} outside the triple"


def est_s(n_circuits=24, shots=SHOTS):
    return EST_PER_SHOT_S * n_circuits * shots + EST_PER_JOB_S


# --- qubit selection (free read) -----------------------------------------------------------------------------------

def candidates(backend, props):
    """Every triple (d1, a, d2), a coupled to both, d1 < d2. Eligible: all errors reported, ancilla readout <= 5%, both
    CZ errors <= 2%, T1 and T2 >= 50 us on all three. Score = 3 x ancilla readout error + 2.5 x (CZ(d1,a) + CZ(a,d2)):
    three mid-circuit readouts on the ancilla and about 2.5 CZs per data qubit per circuit. Lowest score wins; ties by
    (a, d1, d2)."""
    t = backend.target
    nbr = {}
    for (x, y) in t["cz"].keys():
        nbr.setdefault(x, set()).add(y); nbr.setdefault(y, set()).add(x)

    def cz(x, y):
        for pr in ((x, y), (y, x)):
            try:
                return props.gate_error("cz", list(pr))
            except Exception:  # noqa: BLE001
                continue
        return None

    rows = []
    for a in sorted(nbr):
        for d1, d2 in itertools.combinations(sorted(nbr[a]), 2):
            try:
                ro = props.readout_error(a)
                e1, e2 = cz(d1, a), cz(a, d2)
                T = [(props.qubit_property(q)["T1"][0] * 1e6, props.qubit_property(q)["T2"][0] * 1e6) for q in (d1, a, d2)]
                sx = [props.gate_error("sx", [q]) for q in (d1, a, d2)]
            except Exception:  # noqa: BLE001
                continue
            if None in (ro, e1, e2) or any(v is None for v in sx):
                continue
            ok = ro <= MAX_RO and e1 <= MAX_CZ and e2 <= MAX_CZ and all(min(x) >= MIN_T_US for x in T)
            rows.append({"triple": [d1, a, d2], "ancilla_readout": ro, "cz_d1a": e1, "cz_ad2": e2,
                         "T1T2_us": T, "sx": sx, "eligible": bool(ok), "score": 3 * ro + 2.5 * (e1 + e2)})
    el = sorted([r for r in rows if r["eligible"]], key=lambda r: (round(r["score"], 12), r["triple"][1], r["triple"][0], r["triple"][2]))
    return el, len(rows)


# --- predictions ---------------------------------------------------------------------------------------------------

def probs_from_counts(counts, n=None):
    p = np.zeros(8)
    for k, v in counts.items():
        p[int(k.replace(" ", ""), 2) & 7] += v
    return p / (p.sum() if n is None else n)


def systems_from(dist_by_label, labs):
    """dist_by_label: list of 8-vectors in the canonical label order -> {(state, order): System}."""
    out = {}
    for s in STATES:
        for o in ORDERS:
            b = [None] * 6
            for lab, p in zip(labs, dist_by_label):
                if lab["state"] == s and lab["order"] == o:
                    b[lab["line"]] = p
            out[(s, o)] = L.pm_system(b, reverse=(o == "rev"))
    return out


def summary(sysm):
    return {"chi": L.chi(sysm), "cnt2": L.cnt2(sysm), "delta0": L.delta0(sysm), "masse_cntx": L.masse_cntx(sysm),
            "means": {f"{L.LINE_NAMES[i]}:{q}": v for (i, q), v in L.means_pm1(sysm).items()}}


def ideal_dists(labs):
    from qiskit.quantum_info import DensityMatrix  # noqa: F401
    from qiskit_aer import AerSimulator
    sim = AerSimulator(method="density_matrix")
    out = []
    for lab in labs:
        qc = logical(lab)
        r = sim.run(qc, shots=SIM_SHOTS, seed_simulator=91).result().get_counts()
        out.append(probs_from_counts(r))
    return out


def noisy_dists(isas, backend):
    """qiskit-aer's AerSimulator.from_backend(the live ibm_fez backend): IBM's reported gate, readout and T1/T2 errors as
    the device model. It has no model of mid-circuit-measurement crosstalk or reset error; that is what the chip
    referees."""
    from qiskit_aer import AerSimulator
    sim = AerSimulator.from_backend(backend)
    out = []
    for c in isas:
        r = sim.run(c, shots=SIM_SHOTS, seed_simulator=92).result().get_counts()
        out.append(probs_from_counts(r))
    return out


# --- the rule --------------------------------------------------------------------------------------------------------

class FastCNT2:
    """CNT2 by the same LP as cbd_lp.cnt2, built with cbd_lp.build_fast (numpy). Checked equal in --check."""

    def __call__(self, sysm):
        from scipy.optimize import linprog
        from scipy.sparse import csc_matrix, hstack, identity, vstack
        A_fix, b_fix, A_b, p_b = L.build_fast(sysm)
        n, m = A_fix.shape[1], A_b.shape[0]
        I = identity(m, format="csc")
        res = linprog(np.concatenate([np.zeros(n), np.ones(m)]),
                      A_ub=vstack([hstack([A_b, -I]), hstack([-A_b, -I])]).tocsc(), b_ub=np.concatenate([p_b, -p_b]),
                      A_eq=hstack([A_fix, csc_matrix((A_fix.shape[0], m))]).tocsc(), b_eq=b_fix, bounds=(0, None), method="highs")
        if res.status != 0:
            raise RuntimeError(res.message)
        return max(0.0, float(res.fun))


def _rhs(sysm):
    b_fix = [1.0]
    for q in sysm.contents:
        _, masses = L.threshold_strings([sysm.marginal(i, j) for i, j in sysm.conn[q]])
        b_fix += [float(x) for x in masses]
    p_b = np.array([sysm.subset_all_ones(i, js) for i, js in L._bunch_events(sysm)])
    return None, np.array(b_fix), None, p_b


_F = None


def _boot_one(args):
    global _F
    dists, labs, seed, n = args
    rng = np.random.default_rng(seed)
    if _F is None:
        _F = FastCNT2()                  # one structure cache per worker process
    f = _F
    draws = [rng.multinomial(n, p / p.sum()) / n for p in dists]
    systems = systems_from(draws, labs)
    return {f"{s}-{o}": (f(systems[(s, o)]), L.chi(systems[(s, o)])) for s in STATES for o in ORDERS}


def bootstrap(dists, labs, seed, n=SHOTS, b=B, procs=6, pool=None):
    ss = np.random.SeedSequence(seed)
    seeds = [int(x) for x in ss.generate_state(b)]
    jobs = [(dists, labs, s, n) for s in seeds]
    if pool is not None:
        out = pool.map(_boot_one, jobs, chunksize=10)
    else:
        with mp.get_context("spawn").Pool(procs) as p_:
            out = p_.map(_boot_one, jobs, chunksize=10)
    return {k: {"cnt2": [o[k][0] for o in out], "chi": [o[k][1] for o in out]} for k in out[0]}


def lower(vals):
    return float(np.sort(vals)[LB_RANK - 1])


def classify(point, boot):
    """One system: 'contextual' if CNT2's 99% lower bound > TOL; else 'absorbed' if chi's 99% lower bound > 4 (the raw
    sum beat the classical bound but CbD's correction for the measured disturbance absorbed it); else 'below'."""
    lb = lower(boot["cnt2"])
    chi_lb = lower(boot["chi"])
    if lb > TOL:
        return "contextual", lb, chi_lb
    if chi_lb > 4 + TOL:
        return "absorbed", lb, chi_lb
    return "below", lb, chi_lb


STATE_WORDS = {"00": "the |00⟩ input", "bell": "the Bell-state input"}
ORDER_WORDS = {"fwd": "measured in the square's order", "rev": "measured in reverse order"}


def verdict(cls: dict, why_untestable: str | None = None) -> dict:
    """cls: {'00-fwd': (label, cnt2_lb, chi_lb), ...}. Returns the verdict and the pre-registered sentences."""
    if why_untestable:
        return {"verdict": "untestable", "outcome": None, "sentences": [
            f"The test could not be run as pre-registered ({why_untestable}), so it says nothing about the check or the "
            "chip; it is not scored."]}
    ok = {k: v[0] == "contextual" for k, v in cls.items()}
    sents = []
    for k, (lab, lb, chi_lb) in cls.items():
        s, o = k.split("-")
        if lab == "contextual":
            sents.append(f"For {STATE_WORDS[s]} {ORDER_WORDS[o]}, the exact CbD linear program rejects noncontextuality "
                         f"(CNT2's 99% lower bound {lb:.4f} > 0).")
            if chi_lb <= 4 + TOL:
                sents.append(f"There the Peres-Mermin sum itself did not clearly beat 4 (99% lower bound {chi_lb:.3f}): "
                             "the linear program found the contextuality in the full set of noncontextuality constraints, "
                             "not in the Peres-Mermin inequality alone.")
        elif lab == "absorbed":
            sents.append(f"For {STATE_WORDS[s]} {ORDER_WORDS[o]}, the raw Peres-Mermin sum still beat the classical bound "
                         f"of 4 (99% lower bound {chi_lb:.3f}), but the chip's measurements disturbed each other enough "
                         "that CbD could not tell the result from a noncontextual system with that disturbance "
                         f"(CNT2's 99% lower bound {lb:.4f}): noise spoiled the check here, not quantum theory.")
        else:
            sents.append(f"For {STATE_WORDS[s]} {ORDER_WORDS[o]}, the chip's measurements were too noisy for even the raw "
                         f"Peres-Mermin sum to clear the classical bound of 4 (99% lower bound {chi_lb:.3f}): noise "
                         "spoiled the check here, not quantum theory.")
    if all(ok.values()):
        head = ("Pass: for both input states, in both measurement orders, the exact CbD linear program rejects "
                "noncontextuality with CNT2's bootstrap 99% lower bound above 0. The exact CbD 2.0 linear program, "
                "which reduces to program 1's rank-2 Gamma on two-question systems (shown in --check), sees "
                "contextuality on this chip where physics says it must be. This is an instrument check on one chip, one qubit triple "
                "and one job, not a new fact about quantum theory, and it says nothing about language models.")
        v, out = "pass", 1
    else:
        passed_states = [s for s in STATES if ok[f"{s}-fwd"] and ok[f"{s}-rev"]]
        if passed_states:
            s = passed_states[0]
            head = (f"Fail by the rule: the check saw contextuality for {STATE_WORDS[s]} in both orders, but not for "
                    f"{STATE_WORDS[[x for x in STATES if x != s][0]]} in both orders.")
        elif any(ok.values()):
            head = ("Fail by the rule: the check saw contextuality in some of the four state-and-order systems but not "
                    "for both input states in both orders.")
        else:
            head = "Fail: in none of the four state-and-order systems did the check see contextuality."
        if not any(v_[0] == "below" for v_ in cls.values()) and not all(ok.values()):
            head += (" Wherever it missed, the raw sum still beat the classical bound, so what failed is the chip's "
                     "measurement quality under CbD's correction, not quantum theory.")
        elif any(v_[0] == "below" for v_ in cls.values()):
            head += (" Where the raw sum did not clear 4, the chip's sequential measurements were too noisy for this "
                     "test, which says nothing against quantum theory.")
        v, out = "fail", 0
    one_order = [s for s in STATES if ok[f"{s}-fwd"] != ok[f"{s}-rev"]]
    if one_order:
        sents.append("For " + " and ".join(STATE_WORDS[s] for s in one_order) + ", one order passed and the other did "
                     "not, so the order of the measurements mattered on this chip (by CbD 2.0 Theorem 3 the system with "
                     "order folded into context is still contextual for that input).")
    return {"verdict": v, "outcome": out, "headline": head, "sentences": sents}


# --- git gates -------------------------------------------------------------------------------------------------------

def git(*a):
    return subprocess.check_output(["git", "-C", str(ENGINE), *a], text=True).strip()


def uncommitted(paths):
    bad = []
    for p in paths:
        if subprocess.run(["git", "-C", str(ENGINE), "ls-files", "--error-unmatch", p], capture_output=True).returncode:
            bad.append(p + " (not tracked)")
            continue
        st = git("status", "--porcelain", "--", p)
        if st:
            bad.append(p + " (" + st.splitlines()[0][:2].strip() + ")")
    return bad


def load_token():
    import os
    from dotenv import dotenv_values
    env = Path("/Users/seanpharris/entangled-mind/.env")       # the token stays there; loaded into this process only
    for k, v in dotenv_values(env).items():
        if k.startswith("IBM_QUANTUM_") and v and k not in os.environ:
            os.environ[k] = v


def snapshot(be, layout, when=None):
    props = be.properties(datetime=when) if when is not None else be.properties(refresh=True)
    if props is None:
        raise NotSubmitted(f"no IBM properties returned (datetime={when})")
    d1, a, d2 = layout
    out = {"read_at": dt.datetime.now(dt.timezone.utc).isoformat(), "last_update_date": str(props.last_update_date), "qubits": []}
    for q in layout:
        qp = props.qubit_property(q)
        out["qubits"].append({"qubit": q, "T1_us": qp["T1"][0] * 1e6, "T2_us": qp["T2"][0] * 1e6,
                              "readout_error": props.readout_error(q), "sx_error": props.gate_error("sx", [q]),
                              "T1_date": str(qp["T1"][1]), "readout_date": str(props.qubit_property(q).get("readout_error", (None, None))[1])})
    out["cz"] = {}
    for x, y in ((d1, a), (a, d2)):
        for pr in ((x, y), (y, x)):
            try:
                out["cz"][f"{x}-{y}"] = props.gate_error("cz", list(pr)); break
            except Exception:  # noqa: BLE001
                continue
    return out


# --- select: the free read, the triple, the circuits, the prediction -----------------------------------------------

def select():
    bad = uncommitted(SELECT_USES)          # runs before the pre-registration: the prediction is committed in it
    if bad:
        raise SystemExit("refused: uncommitted files the preparation uses:\n  " + "\n  ".join(bad))
    if PREP.exists():
        raise SystemExit(f"{PREP.name} exists; it is never regenerated")
    load_token()
    from entangled_mind import backends
    be = backends.backend()
    props = be.properties(refresh=True)
    el, n_all = candidates(be, props)
    if not el:
        raise SystemExit("no eligible triple under the rule (the bet would be untestable; nothing written)")
    layout = el[0]["triple"]
    labs = labels()
    isas = [isa(logical(l), be, layout) for l in labs]
    for c in isas:
        check_isa(c, be.target, layout)
    buf = io.BytesIO()
    from qiskit import qpy
    qpy.dump(isas, buf)
    QPY.write_bytes(buf.getvalue())
    ideal = ideal_dists(labs)
    noisy = noisy_dists(isas, be)
    out = {"bet": BET, "made_at_head": git("rev-parse", "--short", "HEAD"), "backend": be.name,
           "made_at": dt.datetime.now(dt.timezone.utc).isoformat(), "layout": layout,
           "selection": {"eligible": len(el), "triples_considered": n_all, "top5": el[:5]},
           "snapshot": snapshot(be, layout), "labels": labs, "shots": SHOTS, "estimate_qpu_s": est_s(),
           "qpy_sha256": hashlib.sha256(QPY.read_bytes()).hexdigest(),
           "circuit_ops": [dict(c.count_ops()) for c in isas],
           "prediction": {"simulators": {"ideal": "qiskit-aer AerSimulator(method='density_matrix'), no noise, logical circuits",
                                         "noisy": "qiskit-aer AerSimulator.from_backend(live ibm_fez), ISA circuits"},
                          "sim_shots": SIM_SHOTS,
                          "ideal": {"dists": [p.tolist() for p in ideal]},
                          "noisy": {"dists": [p.tolist() for p in noisy]}}}
    for name, dists in (("ideal", ideal), ("noisy", noisy)):
        sysms = systems_from(dists, labs)
        out["prediction"][name]["systems"] = {f"{s}-{o}": summary(sysms[(s, o)]) for s in STATES for o in ORDERS}
    PREP.write_text(json.dumps(out, indent=1))
    for name in ("ideal", "noisy"):
        print(name, {k: (round(v["chi"], 3), round(v["cnt2"], 4), round(v["delta0"], 3))
                     for k, v in out["prediction"][name]["systems"].items()})
    print("layout", layout, "| estimate", round(out["estimate_qpu_s"], 2), "s | eligible triples", len(el))


# --- worlds (D11) -----------------------------------------------------------------------------------------------------

def world_dists(name, base, labs, rng=None):
    """Named worlds built from the committed noisy prediction (base, canonical order)."""
    if name == "noisy_sim":
        return base
    if name.startswith("flip"):                     # position-dependent extra flips: eps * (position + 1) on each outcome
        eps = float(name[4:])
        out = []
        for lab, p in zip(labs, base):
            q = np.zeros(8)
            fl = [eps * (j + 1) for j in range(3)]
            for s in range(8):
                for f in range(8):
                    w = np.prod([fl[j] if (f >> j) & 1 else 1 - fl[j] for j in range(3)])
                    q[s ^ f] += p[s] * w
            out.append(q)
        return out
    if name == "cheat":                              # noncontextual: context-dependent deterministic answers, chi = 6
        out = []
        for lab in labs:
            q = np.zeros(8)
            sign = L.SIGN[lab["line"]]
            bits = [0, 0, 0] if sign > 0 else [0, 0, 1]
            q[sum(b << j for j, b in enumerate(bits))] = 1.0
            out.append(q)
        return out
    raise ValueError(name)


def worlds(n_draws=20, b=100):
    prep = json.loads(PREP.read_text())
    labs = prep["labels"]
    base = [np.array(p) for p in prep["prediction"]["noisy"]["dists"]]
    res = {}
    root = 20261105
    pool = mp.get_context("spawn").Pool(6)
    for name in ("noisy_sim", "flip0.03", "flip0.04", "flip0.05", "cheat"):
        dists = world_dists(name, base, labs)
        passes, labels_seen = 0, {}
        for k in range(n_draws):
            rng = np.random.default_rng([root, k])
            obs = [rng.multinomial(SHOTS, p / p.sum()) / SHOTS for p in dists]
            pts = systems_from(obs, labs)
            bt = bootstrap(obs, labs, seed=int(rng.integers(2 ** 63)), b=b, pool=pool)
            # with b draws, the 99% lower bound is the (b/100)-th smallest
            cls = {}
            for s in STATES:
                for o in ORDERS:
                    key = f"{s}-{o}"
                    v = sorted(bt[key]["cnt2"]); c = sorted(bt[key]["chi"])
                    r = max(1, b // 100)
                    lab = "contextual" if v[r - 1] > TOL else ("absorbed" if c[r - 1] > 4 + TOL else "below")
                    cls[key] = (lab, v[r - 1], c[r - 1])
            vd = verdict(cls)
            passes += vd["outcome"] == 1
            for key, (lab, _, _) in cls.items():
                labels_seen.setdefault(key, {}).setdefault(lab, 0)
                labels_seen[key][lab] += 1
        pts0 = systems_from(dists, labs)
        res[name] = {"p_pass": passes / n_draws, "n_draws": n_draws, "boot_b": b, "labels": labels_seen,
                     "truth": {f"{s}-{o}": {"chi": L.chi(pts0[(s, o)]), "cnt2": L.cnt2(pts0[(s, o)]),
                                            "delta0": L.delta0(pts0[(s, o)])} for s in STATES for o in ORDERS}}
        print(name, "P(pass)", res[name]["p_pass"], {k: round(v["chi"], 3) for k, v in res[name]["truth"].items()},
              {k: round(v["cnt2"], 4) for k, v in res[name]["truth"].items()}, flush=True)
    pool.close(); pool.join()
    WORLDS.write_text(json.dumps(res, indent=1))


# --- submit ------------------------------------------------------------------------------------------------------------

def design_review_go():
    if not DESIGN_REVIEW.exists():
        return False
    head = DESIGN_REVIEW.read_text().split("---")[1]
    v = [l.split(":", 1)[1].strip() for l in head.splitlines() if l.startswith("verdict:")]
    c = [l.split(":", 1)[1].strip() for l in head.splitlines() if l.startswith("confirmed_at:")]
    return bool(v) and (v[0] == "go" or (v[0] == "fix-first" and c and c[0] not in ("", "null")))


def approved_qpu_s():
    got = None
    for line in SPEND.read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            if (r.get("kind") == "budget_ruling" and r.get("bet") == BET and r.get("resource") == "qpu_s"
                    and "st-16" in str(r.get("under", "")) and isinstance(r.get("approved_qpu_s"), (int, float))):
                got = float(r["approved_qpu_s"])
    return got


def already_ran():
    from entangled_mind import backends
    led = json.loads(backends.USAGE_JSON.read_text()) if backends.USAGE_JSON.exists() else []
    return RAW.exists() or MARKER.exists() or any(str(e.get("purpose", "")).startswith("Program 3 P3-9 ") for e in led)


def job_order(prep):
    seed = json.loads(SEED_FILE.read_text())["seed_order"]
    return [int(i) for i in np.random.default_rng(seed).permutation(len(prep["labels"]))]


def submit():
    load_token()
    from entangled_mind import backends
    if already_ran():
        raise SystemExit("P3-9 already ran (raw file, marker or QPU ledger entry); nothing is resubmitted")
    if not design_review_go():
        raise SystemExit("no design-review go (or confirmed fix-first) at " + str(DESIGN_REVIEW))
    bad = uncommitted(SUBMIT_USES)
    if bad:
        raise SystemExit("refused: files this run uses are not committed and unchanged:\n  " + "\n  ".join(bad))
    approved = approved_qpu_s()
    if approved is None:
        raise SystemExit("no budget_ruling row for ng-p3-9 (resource qpu_s, under st-16, approved_qpu_s) in ledger/spend.jsonl")
    chk = subprocess.run(["python3", str(ENGINE / "ledger" / "check_prereg.py"), BET, str(ENGINE), PREREG, "--before-run"],
                         capture_output=True, text=True)
    if chk.returncode != 0:
        raise SystemExit("check_prereg.py --before-run failed:\n" + chk.stdout + chk.stderr)
    prep = json.loads(PREP.read_text())
    if hashlib.sha256(QPY.read_bytes()).hexdigest() != prep["qpy_sha256"]:
        raise SystemExit("circuit hash mismatch")
    est = prep["estimate_qpu_s"]
    if est > EST_CAP_S or EST_CAP_S > approved:
        raise SystemExit(f"estimate {est:.2f} s or cap {EST_CAP_S} s above the approved {approved} s")
    from qiskit import qpy
    circs = qpy.load(io.BytesIO(QPY.read_bytes()))
    be = backends.backend()
    used = max(backends.cumulative_qpu_seconds(), float(backends.service_usage()["usage_consumed_seconds"] or 0))
    try:
        if used + 1.5 * est > RESERVE_LINE_S:
            raise NotSubmitted(f"reserve rule: {used} + 1.5 x {est:.1f} > {RESERVE_LINE_S}")
        if used + EST_CAP_S > HARD_STOP_S:
            raise NotSubmitted(f"hard stop: {used} + cap {EST_CAP_S} > {HARD_STOP_S}")
        for c in circs:
            try:
                check_isa(c, be.target, prep["layout"])
            except AssertionError as e:
                raise NotSubmitted(f"circuit not ISA on the live target at submission: {e}")
    except NotSubmitted as e:
        RAW.write_text(json.dumps({"not_submitted": str(e), "at": dt.datetime.now(dt.timezone.utc).isoformat()}, indent=1))
        raise SystemExit("not submitted (untestable, section 5.3): " + str(e))
    try:
        cal = snapshot(be, prep["layout"])
    except Exception as e:  # noqa: BLE001
        cal = {"error": repr(e)}
    order = job_order(prep)
    pubs = [circs[i] for i in order]
    t0 = dt.datetime.now(dt.timezone.utc)
    MARKER.write_text(json.dumps({"submitting_at": t0.isoformat(), "qpy_sha256": prep["qpy_sha256"], "order": order,
                                  "cumulative_before_s": used, "job_id": None}, indent=1))
    purpose = f"Program 3 P3-9 sequential Peres-Mermin: 24 pubs, {24 * SHOTS} shots"
    try:
        def on_submit(job_id, batch_id):           # F1a: the job id is on disk before the client waits for the result
            m_ = json.loads(MARKER.read_text()); m_["job_id"] = job_id; m_["batch_id"] = batch_id
            MARKER.write_text(json.dumps(m_, indent=1))
        counts, usage = backends.run_hardware(pubs, purpose=purpose, shots=SHOTS, on_submit=on_submit, expected_s=EST_CAP_S)
        rec = {"submitted_at": t0.isoformat(), "order": order, "usage": usage, "counts_in_job_order": counts,
               "calibration_at_submit": cal}
    except BaseException as e:  # noqa: BLE001  never resubmitted: the marker blocks it; look the job up by hand
        rec = {"submitted_at": t0.isoformat(), "order": order, "client_error": repr(e), "calibration_at_submit": cal,
               "job_id": json.loads(MARKER.read_text()).get("job_id"),
               "note": "client error; never resubmitted (marker file blocks it). If IBM reports the job DONE, its counts "
                       "are the data: run --retrieve (a free read)."}
        RAW.write_text(json.dumps(rec, indent=1))
        raise
    RAW.write_text(json.dumps(rec, indent=1))                    # saved at once, before anything else
    m = json.loads(MARKER.read_text()); m["job_id"] = usage.get("job_id")
    MARKER.write_text(json.dumps(m, indent=1))
    try:
        jb = backends.service().job(m["job_id"])
        rec["timestamps"] = jb.metrics().get("timestamps", {})
        when = rec["timestamps"].get("running")
        when = dt.datetime.fromisoformat(when.replace("Z", "+00:00")) if when else dt.datetime.now(dt.timezone.utc)
        rec["calibration_at_run"] = snapshot(be, prep["layout"], when=when) | {"requested_datetime": when.isoformat()}
    except Exception as e:  # noqa: BLE001
        rec["enrich_error"] = repr(e)
    RAW.write_text(json.dumps(rec, indent=1))
    print("done", m["job_id"], "QPU s", usage.get("quantum_seconds"), "cumulative before", used, flush=True)


def retrieve():
    """F1c: a free read after a client error. Needs the marker's job id and a raw file with no counts. If IBM reports
    the job DONE, its counts are fetched and written in the normal format (retrieved: true); otherwise its status is
    recorded. Never submits."""
    load_token()
    from entangled_mind import backends
    if not MARKER.exists():
        raise SystemExit("no marker: nothing was submitted")
    m = json.loads(MARKER.read_text())
    raw = json.loads(RAW.read_text()) if RAW.exists() else {}
    if "counts_in_job_order" in raw:
        raise SystemExit("the raw file already holds counts; nothing to retrieve")
    if not m.get("job_id"):                     # confirmation F1(ii): the client failed before IBM returned an id
        since = dt.datetime.fromisoformat(m["submitting_at"]) - dt.timedelta(minutes=2)
        listed = backends.service().jobs(backend_name=backends.backend().name, created_after=since, limit=50)
        ids = [j.job_id() for j in listed]
        raw |= {"job_list_read_at": dt.datetime.now(dt.timezone.utc).isoformat(), "job_list_since": since.isoformat(),
                "job_list_ids": ids}
        if not ids:
            raw |= {"ibm_status": "NOT_SUBMITTED", "order": m["order"]}
            RAW.write_text(json.dumps(raw, indent=1))
            print("no ibm_fez job created since", since.isoformat(), "-> NOT_SUBMITTED (untestable)")
            return
        if len(ids) > 1:
            RAW.write_text(json.dumps(raw, indent=1))
            raise SystemExit(f"{len(ids)} jobs on the backend since the marker: {ids}; none adopted (recorded)")
        m["job_id"] = ids[0]; m["job_id_from"] = "job list (one job since the marker)"
        MARKER.write_text(json.dumps(m, indent=1))
    jb = backends.service().job(m["job_id"])
    st = str(jb.status()).split(".")[-1].upper()
    raw |= {"job_id": m["job_id"], "order": m["order"], "ibm_status": st,
            "status_read_at": dt.datetime.now(dt.timezone.utc).isoformat()}
    if st == "DONE":
        res = jb.result()
        met = jb.metrics()
        raw |= {"counts_in_job_order": [pub.data.meas.get_counts() for pub in res], "retrieved": True,
                "usage": {"job_id": m["job_id"], "quantum_seconds": backends.qpu_seconds(met.get("usage") or {}),
                          "job_metrics_usage": met.get("usage")},
                "timestamps": met.get("timestamps", {})}
    RAW.write_text(json.dumps(raw, indent=1))
    print("job", m["job_id"], "status", st, "| counts retrieved" if st == "DONE" else "| no counts")


# --- analyse -------------------------------------------------------------------------------------------------------------

def untestable(prep, raw):
    """F1d: a client error is never by itself untestable. If IBM reports the job DONE, its counts are the data (fetched
    with --retrieve). Untestable only if: not submitted; IBM reports ERROR or CANCELLED; no counts; the wrong number
    of circuits; a circuit under 90% of its shots."""
    if "not_submitted" in raw:
        return "not submitted: " + raw["not_submitted"]
    st = raw.get("ibm_status")
    if st in ("ERROR", "CANCELLED"):
        return f"IBM reports the job {st}"
    if st == "NOT_SUBMITTED":
        return "not submitted: the client failed before IBM returned a job id, and IBM lists no job since the marker"
    if "counts_in_job_order" not in raw:      # confirmation F1(i): QUEUED, RUNNING, DONE-without-counts or unread: no call
        raise SystemExit(f"no counts and IBM's status is {st or 'not yet read'}: run --retrieve (a free read) "
                         "until the job is DONE, ERROR or CANCELLED; nothing is decided before then")
    if len(raw["counts_in_job_order"]) != len(prep["labels"]):
        return "the job returned the wrong number of circuits"
    for c in raw["counts_in_job_order"]:
        if sum(c.values()) < MIN_SHOT_FRAC * SHOTS:
            return f"a circuit returned {sum(c.values())} of {SHOTS} shots (< 90%)"
    return None


def analyse():
    bad = uncommitted(ANALYSE_USES)
    if bad:
        raise SystemExit("refused: files the analysis uses are not committed and unchanged:\n  " + "\n  ".join(bad))
    prep = json.loads(PREP.read_text())
    raw = json.loads(RAW.read_text())
    labs = prep["labels"]
    why = untestable(prep, raw)
    out = {"bet": BET, "analysed_at_head": git("rev-parse", "--short", "HEAD")}
    if why:
        out["verdict"] = verdict({}, why)
        OUT.write_text(json.dumps(out, indent=1)); print(out["verdict"]); return
    counts = [None] * len(labs)
    for pos, i in enumerate(raw["order"]):
        counts[i] = raw["counts_in_job_order"][pos]
    dists = [probs_from_counts(c) for c in counts]
    pts = systems_from(dists, labs)
    seed = json.loads(SEED_FILE.read_text())["seed_boot"]
    bt = bootstrap(dists, labs, seed=seed)
    cls, table = {}, {}
    for s in STATES:
        for o in ORDERS:
            key = f"{s}-{o}"
            lab, lb, chi_lb = classify(None, bt[key])
            cls[key] = (lab, lb, chi_lb)
            sm = summary(pts[(s, o)])
            chis = np.array(bt[key]["chi"])
            table[key] = sm | {"label": lab, "cnt2_lb99": lb, "chi_lb99": chi_lb, "chi_se": float(chis.std(ddof=1)),
                               "cnt2_boot_min": float(min(bt[key]["cnt2"])), "cnt2_boot_median": float(np.median(bt[key]["cnt2"])),
                               "n_boot_zero": int(sum(v <= TOL for v in bt[key]["cnt2"]))}
    noisy = [np.array(x) for x in prep["prediction"]["noisy"]["dists"]]
    loo = {}
    for s_ in STATES:                                    # P10: each circuit replaced by its noisy prediction, point CNT2
        for o in ORDERS:
            key = f"{s_}-{o}"
            loo[key] = {}
            for i, lab in enumerate(labs):
                if lab["state"] == s_ and lab["order"] == o:
                    d2 = list(dists); d2[i] = noisy[i]
                    loo[key][lab["line_name"]] = L.cnt2(systems_from(d2, labs)[(s_, o)])
            table[key]["loo_cnt2_min"] = min(loo[key].values())
            table[key]["loo_rests_on"] = [k for k, v in loo[key].items() if (v <= TOL) != (table[key]["cnt2"] <= TOL)]
    out |= {"counts": counts, "systems": table, "verdict": verdict(cls), "leave_one_out": loo,
            "prediction_noisy": prep["prediction"]["noisy"]["systems"], "prediction_ideal": prep["prediction"]["ideal"]["systems"],
            "bootstrap": {"B": B, "lower_bound_rank": LB_RANK, "seed": seed}, "usage": raw.get("usage"),
            "timestamps": raw.get("timestamps")}
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps(out["verdict"], indent=1))
    for k, v in table.items():
        print(k, v["label"], "chi", round(v["chi"], 3), "+/-", round(v["chi_se"], 3), "CNT2", round(v["cnt2"], 4),
              "lb", round(v["cnt2_lb99"], 4), "delta0", round(v["delta0"], 3))


# --- check (offline) -------------------------------------------------------------------------------------------------------

def check():
    """No network, no QPU. (1) the LP against KDL and the full LP; (2) the cheat and noncontextual controls; (3) the
    circuits on a fake ibm_fez target, ideal simulation = textbook values; (4) the rule on synthetic tables."""
    rng = np.random.default_rng(3)
    # (1) cyclic systems against KDL
    agree = n = 0
    for nn in (3, 4, 5):
        for _ in range(60):
            mf = rng.uniform(-1, 1, nn) * (0.1 if _ % 2 else 1); ms = rng.uniform(-1, 1, nn) * (0.1 if _ % 2 else 1)
            e = [rng.uniform(abs(a + b) - 1, 1 - abs(a - b)) for a, b in zip(mf, ms)]
            if _ % 2:
                e = [np.sign(rng.random() - 0.3) * rng.uniform(0.5, 0.8) for _ in range(nn)]
            try:
                s = L.cyclic_system(nn, e, list(mf), list(ms))
            except AssertionError:
                continue
            n += 1; agree += (L.cnt2(s) > TOL) == (L.kdl_contextual(nn, e, list(mf), list(ms)) > 0)
    assert agree == n, f"LP disagrees with KDL on {n - agree} of {n}"
    print(f"(1) LP = KDL on {n} of {n} random cyclic systems")
    # (1b) rank 2 (design review F2a): the LP = KDL at n = 2 = program 1's Gamma = |q_QQ| - OSS on the same bunches
    r2 = np.random.default_rng(42)
    n2 = a2 = c2 = 0
    for t in range(200):
        sc = 1.0 if t % 2 else 0.15
        mf, ms = r2.uniform(-1, 1, 2) * sc, r2.uniform(-1, 1, 2) * sc
        e = [r2.uniform(abs(a + b) - 1, 1 - abs(a - b)) for a, b in zip(mf, ms)]
        if t % 4 == 1:
            e = [r2.choice([-1, 1]) * r2.uniform(0.6, 0.95), r2.choice([-1, 1]) * r2.uniform(0.6, 0.95)]
        try:
            s2 = L.cyclic_system(2, e, list(mf), list(ms))
        except AssertionError:
            continue
        k2 = L.kdl_contextual(2, e, list(mf), list(ms))
        if abs(k2) < 1e-6:
            continue
        q = (s2.bunches[0][1] + s2.bunches[0][2]) - (s2.bunches[1][1] + s2.bunches[1][2])      # P(disagree) shift
        oss = abs(s2.marginal(0, 0) - s2.marginal(1, 1)) + abs(s2.marginal(0, 1) - s2.marginal(1, 0))
        gamma = abs(q) - oss                                                                   # exp4_run.py's Gamma
        cc = L.cnt2(s2) > TOL
        n2 += 1; c2 += cc; a2 += cc == (k2 > 0) == (gamma > 0)
    assert a2 == n2 and 0.25 * n2 < c2 < 0.75 * n2, (a2, n2, c2)
    print(f"(1b) rank 2: LP = KDL = program 1's Gamma (|q_QQ| - OSS) on {n2} of {n2} random systems ({c2} contextual)")
    # (2) Kirchmair; the cheat; ideal QM; FastCNT2 = cnt2; full LP = reduced on one contextual PM system
    mn, me, ks = L.completion_bounds(L.KIRCHMAIR_MEANS, L.KIRCHMAIR_PRODUCTS)
    assert mn > 0.1 and abs(L.chi(ks) - 5.463) < 1e-3 and abs(L.delta0(ks) - 0.166) < 1e-3
    print(f"(2) Kirchmair: min CNT2 over completions {mn:.4f}; chi {L.chi(ks):.3f}; delta0 {L.delta0(ks):.3f}")
    labs = labels()
    cheat = systems_from(world_dists("cheat", None, labs), labs)
    for k, sy in cheat.items():
        assert abs(L.chi(sy) - 6) < 1e-9 and L.cnt2(sy) <= TOL, k
    print("    cheat (context-dependent fixed answers): chi 6.000 and CNT2 0 in all four systems: chi alone is a dumb baseline")
    obs9 = [q for line in L.SQUARE for q in line]
    worst = 0.0
    for t in range(30):                  # D3: noncontextual systems with context- and position-dependent flips stay at 0
        w = np.zeros(512); idx = rng.choice(512, size=int(rng.integers(1, 4)), replace=False); w[idx] = rng.dirichlet(np.ones(len(idx)))
        fl = rng.uniform(0, 0.1, (6, 3)); b_ = []
        for k, ln in enumerate(L.LINES):
            p = np.zeros(8)
            for g in np.nonzero(w)[0]:
                base = [(int(g) >> obs9.index(q)) & 1 for q in ln]
                for fb in range(8):
                    pf = np.prod([fl[k][j] if (fb >> j) & 1 else 1 - fl[k][j] for j in range(3)])
                    p[sum((base[j] ^ ((fb >> j) & 1)) << j for j in range(3))] += w[g] * pf
            b_.append(p)
        worst = max(worst, L.cnt2(L.pm_system(b_)))
    assert worst <= TOL, worst
    print(f"    30 near-deterministic noncontextual models with flips up to 10% per context and position: max CNT2 {worst:.2g}")
    f = FastCNT2()
    assert abs(f(ks) - L.cnt2(ks)) < 1e-9
    A1, A2 = L.build(ks), L.build_fast(ks)
    assert abs(A1[0] - A2[0]).max() < 1e-12 and abs(A1[2] - A2[2]).max() < 1e-12 and np.allclose(A1[1], A2[1])
    print("    build_fast = build and FastCNT2 = cnt2 on the Kirchmair system")
    # (3) circuits: ideal simulation of the logical circuits gives chi 6, CNT2 0.25, delta0 0 in all four systems
    ideal = ideal_dists(labs)
    sy = systems_from(ideal, labs)
    for k, v in sy.items():
        assert abs(L.chi(v) - 6) < 0.02 and abs(L.cnt2(v) - 0.25) < 0.01 and L.delta0(v) < 0.02, (k, L.chi(v), L.cnt2(v))
    print("(3) ideal simulation of the 24 logical circuits: chi", {f"{a}-{b}": round(L.chi(v), 3) for (a, b), v in sy.items()})
    for k in (("bell", "fwd"),):
        v = sy[k]
        assert abs(L.cnt2(v, full_lp=True) - L.cnt2(v)) < 1e-6
    print("    full 2^18 LP = reduced LP on the ideal Bell forward system")
    try:
        from qiskit_ibm_runtime.fake_provider import FakeFez
        fb = FakeFez()
        c = isa(logical(labs[-1]), fb, [3, 4, 5])
        check_isa(c, fb.target, [3, 4, 5])
        print("    ISA on FakeFez triple (3, 4, 5):", dict(c.count_ops()))
    except ImportError:
        print("    (FakeFez unavailable; ISA check skipped offline)")
    # (4) the rule on synthetic tables: every combination of labels gives exactly one verdict
    for combo in itertools.product(("contextual", "absorbed", "below"), repeat=4):
        cl = {k: (lab, 0.1 if lab == "contextual" else 0.0, 5.0 if lab != "below" else 3.9)
              for k, lab in zip([f"{s}-{o}" for s in STATES for o in ORDERS], combo)}
        vd = verdict(cl)
        assert vd["verdict"] in ("pass", "fail") and (vd["verdict"] == "pass") == all(x == "contextual" for x in combo)
    print("(4) the rule returns exactly one verdict on all 81 label combinations; pass iff all four contextual")
    # (5) design review F1d: a client error alone is never untestable
    p_ = {"labels": labs}
    good = [{"000": SHOTS}] * len(labs)
    ce = {"client_error": "TimeoutError()", "order": list(range(24))}
    try:
        untestable(p_, ce); raise AssertionError("client error without a status must refuse")
    except SystemExit:
        pass
    for st_ in ("RUNNING", "QUEUED", "DONE", "INITIALIZING"):      # not finished, or DONE but counts not yet fetched
        try:
            untestable(p_, ce | {"ibm_status": st_}); raise AssertionError(f"status {st_} without counts must refuse")
        except SystemExit:
            pass
    assert untestable(p_, ce | {"ibm_status": "NOT_SUBMITTED"}).startswith("not submitted")
    assert untestable(p_, ce | {"ibm_status": "ERROR"}) == "IBM reports the job ERROR"
    assert untestable(p_, ce | {"ibm_status": "CANCELLED"}) == "IBM reports the job CANCELLED"
    assert untestable(p_, ce | {"ibm_status": "DONE", "retrieved": True, "counts_in_job_order": good}) is None
    assert untestable(p_, {"counts_in_job_order": good[:23]}) is not None
    assert untestable(p_, {"counts_in_job_order": [{"000": 3500}] * 24}) is not None
    assert untestable(p_, {"not_submitted": "reserve rule"}).startswith("not submitted")
    print("(5) untestable(): no counts refuses unless ERROR, CANCELLED or NOT_SUBMITTED (QUEUED, RUNNING, DONE without "
          "counts, unread all refuse: run --retrieve); DONE with counts is data; short counts, wrong circuit count, not "
          "submitted are untestable")
    print("check OK")


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "--check"
    {"--check": check, "--select": select, "--worlds": worlds, "--submit": submit, "--retrieve": retrieve,
     "--analyse": analyse}[arg]()

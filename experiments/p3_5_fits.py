"""P3-5: coherent or incoherent, from program 1's archived two-qubit tomography (experiments/p3-5-coherent-fits.md).

    entangled-mind/.venv/bin/python experiments/p3_5_fits.py            # the pre-registered run (needs the seed file)
    entangled-mind/.venv/bin/python experiments/p3_5_fits.py --synthetic # dry run on synthetic counts only, no archive

For each of the 3 items: a reference state rho_ref (the P3-1-corrected simulator's reduced state, from exact
simulated tomography of the 9 as-run setting circuits, readout excluded), then two 7-parameter families fitted by
maximum likelihood to the hardware counts through the archived hardware assignment matrix:
  (i)  coherent:   (U_j x U_i) exp(-i phi ZZ / 2) rho_ref (...)^dagger   (6 local Euler angles + 1 ZZ phase)
  (ii) incoherent: (1-p) (Pauli_j x Pauli_i)(rho_ref) + p I/4           (6 local Pauli probabilities + 1 depolarising)
Primary: dlogL = logL(i) - logL(ii) per item; pass if >= 10 on at least 2 of 3 items.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p3sim  # noqa: E402

SEED_FILE = p3sim.ROOT / "data" / "p3-5-seed.json"
OUT = p3sim.ROOT / "results" / "p3-5-coherent-fits.json"
JOB = "dbl6e1d8mdtc73d5gesg"
SETTINGS = [a + b for a in "XYZ" for b in "XYZ"]   # a: qubit i (clbit 0), b: qubit j (clbit 1)
N_RANDOM_STARTS = 20
PASS_DLOGL, PASS_ITEMS = 10.0, 2

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], complex)
Y = np.array([[0, -1j], [1j, 0]], complex)
Z = np.diag([1, -1]).astype(complex)
H = np.array([[1, 1], [1, -1]], complex) / np.sqrt(2)
SDG = np.diag([1, -1j])
BASIS = {"X": H, "Y": H @ SDG, "Z": I2}
ZZ = np.kron(Z, Z)
PAULIS = [I2, X, Y, Z]


# --- model ----------------------------------------------------------------------------------------

def setting_probs(rho: np.ndarray, s: str) -> np.ndarray:
    """Outcome probabilities, index 2*b_j + b_i (rho is in kron(j, i) order)."""
    V = np.kron(BASIS[s[1]], BASIS[s[0]])
    return np.clip(np.real(np.diag(V @ rho @ V.conj().T)), 0, None)


def euler(a, b, c):
    rz = lambda t: np.diag([np.exp(-0.5j * t), np.exp(0.5j * t)])
    ry = lambda t: np.array([[np.cos(t / 2), -np.sin(t / 2)], [np.sin(t / 2), np.cos(t / 2)]], complex)
    return rz(a) @ ry(b) @ rz(c)


def fam_coherent(theta, rho):
    Ui, Uj = euler(*theta[0:3]), euler(*theta[3:6])
    U = np.kron(Uj, Ui) @ expm(-0.5j * theta[6] * ZZ)
    return U @ rho @ U.conj().T


def pauli_probs(logits):
    w = np.exp(np.concatenate([[0.0], logits]))
    return w / w.sum()


def fam_incoherent(theta, rho):
    pi, pj = pauli_probs(theta[0:3]), pauli_probs(theta[3:6])
    out = np.zeros_like(rho)
    for a in range(4):
        for b in range(4):
            K = np.kron(PAULIS[b], PAULIS[a])
            out += pi[a] * pj[b] * (K @ rho @ K.conj().T)
    p = 1 / (1 + np.exp(-theta[6]))
    return (1 - p) * out + p * np.eye(4) / 4


def loglik(rho, counts, A):
    ll = 0.0
    for s in SETTINGS:
        p = np.clip(A @ setting_probs(rho, s), 1e-12, None)
        ll += float(np.dot(counts[s], np.log(p / p.sum())))
    return ll


def fit(family, rho_ref, counts, A, rng):
    if family == "coherent":
        f, x0s = fam_coherent, [np.zeros(7)] + [rng.uniform(-0.3, 0.3, 7) for _ in range(N_RANDOM_STARTS)]
    else:
        f, x0s = fam_incoherent, [np.full(7, -8.0)] + [rng.uniform(-8, -2, 7) for _ in range(N_RANDOM_STARTS)]
    best = None
    for x0 in x0s:
        r = minimize(lambda t: -loglik(f(t, rho_ref), counts, A), x0, method="L-BFGS-B")
        if best is None or r.fun < best.fun:
            best = r
    rho = f(best.x, rho_ref)
    return {"logL": -float(best.fun), "theta": best.x.tolist(), "rho": rho, "converged": bool(best.success)}


def negativity(rho):
    pt = rho.reshape(2, 2, 2, 2).transpose(0, 3, 2, 1).reshape(4, 4)   # partial transpose on one qubit
    w = np.linalg.eigvalsh((pt + pt.conj().T) / 2)
    return float(-w[w < 0].sum())


def counts_vec(c):
    return np.array([c.get(b, 0) for b in ("00", "01", "10", "11")], float)


def saturated(counts):
    tot = 0.0
    for s in SETTINGS:
        n = counts[s]
        tot += float(np.sum(n[n > 0] * np.log(n[n > 0] / n.sum())))
    return tot


# --- reference states -----------------------------------------------------------------------------

def reference_states(item_files, noisy=True):
    """Exact simulated tomography of the 9 as-run setting circuits (readout excluded) -> linear inversion."""
    from qiskit_aer import AerSimulator
    base = p3sim.fake_fez()
    # legacy_t1t2_bug=True reproduces the run as made (D8); a corrected P3-5 re-run is not pre-registered
    be = p3sim.overwrite_calibration(base, p3sim.snapshot(JOB), legacy_t1t2_bug=True)
    sim = p3sim.simulator(be, method="density_matrix") if noisy else AerSimulator(method="density_matrix")
    probs = {}
    for s, path in item_files.items():
        isa = p3sim.load_isa(path)
        meas = {isa.find_bit(i.clbits[0]).index: isa.find_bit(i.qubits[0]).index
                for i in isa.data if i.operation.name == "measure"}
        circ = p3sim.schedule(isa, be) if noisy else isa
        bare = circ.copy_empty_like()
        for inst in circ.data:
            if inst.operation.name != "measure":
                bare.append(inst)
        bare.save_probabilities([meas[0], meas[1]], label="p")
        res = sim.run(bare).result()
        probs[s] = np.asarray(res.data(0)["p"], float)
    return linear_inversion(probs), probs


def linear_inversion(probs):
    sign = np.array([1, -1])
    E = {("I", "I"): 1.0}
    for s, p in probs.items():
        for k, pk in enumerate(p):
            bi, bj = k & 1, k >> 1
            E[(s[0], s[1])] = E.get((s[0], s[1]), 0) + sign[bi] * sign[bj] * pk
            E[(s[0], "I")] = E.get((s[0], "I"), 0) + sign[bi] * pk / 3
            E[("I", s[1])] = E.get(("I", s[1]), 0) + sign[bj] * pk / 3
    P = {"I": I2, "X": X, "Y": Y, "Z": Z}
    rho = sum(E[(a, b)] * np.kron(P[b], P[a]) for a in "IXYZ" for b in "IXYZ") / 4
    w, v = np.linalg.eigh((rho + rho.conj().T) / 2)
    w = np.clip(w, 0, None)
    return (v * (w / w.sum())) @ v.conj().T


# --- runs -------------------------------------------------------------------------------------------

def analyse_item(rho_ref, counts, A, rng):
    out = {"logL_ref": loglik(rho_ref, counts, A), "logL_saturated": saturated(counts),
           "negativity_ref": negativity(rho_ref)}
    for fam in ("coherent", "incoherent"):
        r = fit(fam, rho_ref, counts, A, rng)
        out[fam] = {"logL": r["logL"], "theta": r["theta"], "converged": r["converged"],
                    "negativity": negativity(r["rho"])}
    out["dlogL"] = out["coherent"]["logL"] - out["incoherent"]["logL"]
    return out


def synthetic():
    """Dry run, no archive: a Bell-like state; data generated from each family; check each family wins on its own data."""
    rng = np.random.default_rng(0)
    psi = np.array([0.78, 0, 0, -0.63], complex); psi /= np.linalg.norm(psi)
    rho0 = np.outer(psi, psi.conj())
    A = np.array([[0.98, 0.02, 0.02, 0.0], [0.01, 0.97, 0.0, 0.02], [0.01, 0.0, 0.97, 0.02], [0.0, 0.01, 0.01, 0.96]])
    truths = {"coherent": fam_coherent(np.array([0.1, 0.2, -0.1, 0.05, -0.15, 0.1, 0.4]), rho0),
              "incoherent": fam_incoherent(np.array([-3, -4, -2.5, -3.5, -3, -2.8, -2.0]), rho0)}
    for name, rho_true in truths.items():
        counts = {s: rng.multinomial(4000, (A @ setting_probs(rho_true, s)) / (A @ setting_probs(rho_true, s)).sum()).astype(float)
                  for s in SETTINGS}
        r = analyse_item(rho0, counts, A, rng)
        print(f"truth={name}: dlogL(coh - inc) = {r['dlogL']:+.1f}; logL ref {r['logL_ref']:.1f}, "
              f"coh {r['coherent']['logL']:.1f}, inc {r['incoherent']['logL']:.1f}, sat {r['logL_saturated']:.1f}")


def main():
    if "--synthetic" in sys.argv:
        return synthetic()
    if not SEED_FILE.exists():
        raise SystemExit("no seed file: the seed commit must land before the archive is opened")
    seed = json.loads(SEED_FILE.read_text())["seed32_starts"]
    rng = np.random.default_rng(seed)
    hw = json.loads((p3sim.EM / "results" / "witness-run-1.json").read_text())
    files = {}
    for k in range(39):
        rec = json.loads((p3sim.HW / f"{JOB}-{k}.json").read_text())
        if rec.get("role") == "tomography setting":
            files.setdefault(rec["item"], {})[rec["setting"]] = p3sim.HW / f"{JOB}-{k}.json"
    out = {"bet": "ng-p3-5", "seed32_starts": seed, "items": []}
    for item in hw["items"]:
        rho_ref, ref_probs = reference_states(files[item["id"]], noisy=True)
        rho_ideal, _ = reference_states(files[item["id"]], noisy=False)
        counts = {s: counts_vec(c) for s, c in zip(SETTINGS, item["hardware_counts"][:9])}
        A = np.array(item["hardware"]["assignment_matrix"])
        r = {"id": item["id"], "physical_qubits": item["physical_qubits"],
             "negativity_hardware_archived": item["hardware"]["negativity"],
             "negativity_noisy_sim_archived": item["noisy_sim"]["negativity"],
             "primary": analyse_item(rho_ref, counts, A, rng),
             "secondary_ideal_reference": analyse_item(rho_ideal, counts, A, rng)}
        out["items"].append(r)
        print(item["id"], "dlogL", round(r["primary"]["dlogL"], 2), "ideal-ref dlogL", round(r["secondary_ideal_reference"]["dlogL"], 2))
    n_pass = sum(r["primary"]["dlogL"] >= PASS_DLOGL for r in out["items"])
    out["n_items_coherent_wins"] = n_pass
    out["verdict"] = "pass" if n_pass >= PASS_ITEMS else "fail"
    OUT.write_text(json.dumps(out, indent=1))
    print("verdict", out["verdict"], n_pass)


if __name__ == "__main__":
    main()

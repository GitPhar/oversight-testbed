"""P3-5c: the corrected P3-5 re-analysis (experiments/p3-5c-nested.md). Not scored: its archive was already analysed.

    PY=/Users/seanpharris/entangled-mind/.venv/bin/python
    $PY experiments/p3_5c_fits.py --synthetic [--fast]   # D4 dry run on synthetic data only (no archive)
    $PY experiments/p3_5c_fits.py --run                  # the pre-registered run (needs the seed file and a design-review go)

For each of the 3 archived items (program 1's witness tomography, 9 settings x 4,000 shots):
  rho_ref  the P3-1 construction with T1/T2 actually loaded (p3sim, D8 fix), ALAP-scheduled: exact simulated
           tomography of the 9 as-run setting circuits, readout excluded, then linear inversion.
  models   coh (7):  U rho U^dag, U = (U_j x U_i) exp(-i phi ZZ / 2)                 [P3-5's family (i)]
           inc (7):  (1 - p) (Pauli_j x Pauli_i)(rho) + p I/4, probabilities direct and bounded
                     (p_X, p_Y, p_Z in [0, 0.25] per qubit; p in [0, 0.5])            [P3-5's family (ii), reparametrised]
           full (14): inc applied after coh. Each nested model is full with the other's knobs at zero.
  tests    coherent given incoherent: LR_c = 2 (logL_full - logL_inc); parametric bootstrap null from the fitted inc
           state, B = 100. Incoherent given coherent: LR_i = 2 (logL_full - logL_coh); null from the fitted coh state.
           Co-primary: leave-one-setting-out cross-validated held-out log-likelihood gain of full over inc (and over coh).
  label    per item and kind: "present" iff bootstrap p < 0.01; otherwise "not detected". The CV gain is a reported
           secondary, not a gate: the synthetic dry run (D10) showed leave-one-setting-out CV penalises the 14-parameter
           model when a whole basis is held out (CV -13.8 on data with real coherent error, LR 46.5), so AND-ing it in
           would miss coherent error exactly when both kinds are present.
  spectator (secondary) the audit's $0 check: simulate the h088 and h268 as-run circuits with a 0.1 rad ZZ phase added
           only on CZ pairs NOT touching the measured pair, sample 4,000 shots per setting through the item's assignment
           matrix, and report whether LR_c exceeds the 99th percentile of that item's real-data bootstrap null (i.e.
           whether spectator steering is detected as coherent error, or absorbed as blur).
Every refit (CV folds, bootstrap samples) is warm-started from the full-data optima, plus random starts, so optimiser
shortfalls cannot pose as evidence.
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p3sim  # noqa: E402
import p3_5_fits as F  # noqa: E402  (setting_probs, fam_coherent, negativity, linear_inversion, counts_vec)

SEED_FILE = p3sim.ROOT / "data" / "p3-5c-seed.json"
OUT = p3sim.ROOT / "results" / "p3-5c-nested.json"
DESIGN_REVIEW = p3sim.ROOT.parents[1] / "ledger" / "design-reviews" / "ng-p3-5c.md"
JOB = "dbl6e1d8mdtc73d5gesg"
SETTINGS = F.SETTINGS
B = 100
ALPHA = 0.01
N_STARTS = 10
INC_BOUNDS = [(0.0, 0.25)] * 6 + [(0.0, 0.5)]
COH_BOUNDS = [(None, None)] * 7
FULL_BOUNDS = COH_BOUNDS + INC_BOUNDS
PAULIS = [F.I2, F.X, F.Y, F.Z]


def fam_inc(theta, rho):
    pi = np.array([1 - theta[0] - theta[1] - theta[2], theta[0], theta[1], theta[2]])
    pj = np.array([1 - theta[3] - theta[4] - theta[5], theta[3], theta[4], theta[5]])
    out = np.zeros_like(rho)
    for a in range(4):
        for b in range(4):
            K = np.kron(PAULIS[b], PAULIS[a])
            out += pi[a] * pj[b] * (K @ rho @ K.conj().T)
    return (1 - theta[6]) * out + theta[6] * np.eye(4) / 4


def fam_full(theta, rho):
    return fam_inc(theta[7:14], F.fam_coherent(theta[0:7], rho))


MODELS = {"coh": (F.fam_coherent, COH_BOUNDS), "inc": (fam_inc, INC_BOUNDS), "full": (fam_full, FULL_BOUNDS)}


def loglik(rho, counts, A, settings):
    ll = 0.0
    for s in settings:
        p = np.clip(A @ F.setting_probs(rho, s), 1e-12, None)
        ll += float(np.dot(counts[s], np.log(p / p.sum())))
    return ll


def best_fit(kind, x0s, rho, counts, A, settings=SETTINGS):
    f, bounds = MODELS[kind]
    g = lambda t: -loglik(f(t, rho), counts, A, settings)
    best = None
    for x0 in x0s:
        r = minimize(g, np.asarray(x0, float), method="L-BFGS-B", bounds=bounds)
        if best is None or r.fun < best.fun:
            best = r
    return best


def rand_starts(kind, rng, n):
    coh0, inc0 = np.zeros(7), np.zeros(7)
    rc = lambda: rng.uniform(-0.3, 0.3, 7)
    ri = lambda: np.concatenate([rng.uniform(0, 0.05, 6), rng.uniform(0, 0.1, 1)])
    if kind == "coh":
        return [coh0] + [rc() for _ in range(n)]
    if kind == "inc":
        return [inc0] + [ri() for _ in range(n)]
    return [np.concatenate([coh0, inc0])] + [np.concatenate([rc(), ri()]) for _ in range(n)]


def fit_all(rho, counts, A, rng, n=N_STARTS, settings=SETTINGS, warm=None):
    """warm: dict kind -> parameter vector (full-data optima) used as extra starts."""
    w = warm or {}
    fc = best_fit("coh", rand_starts("coh", rng, n) + ([w["coh"]] if "coh" in w else []), rho, counts, A, settings)
    fi = best_fit("inc", rand_starts("inc", rng, n) + ([w["inc"]] if "inc" in w else []), rho, counts, A, settings)
    x0s = rand_starts("full", rng, n) + [np.concatenate([fc.x, np.zeros(7)]), np.concatenate([np.zeros(7), fi.x])]
    if "full" in w:
        x0s.append(w["full"])
    ff = best_fit("full", x0s, rho, counts, A, settings)
    return {"coh": fc, "inc": fi, "full": ff}


def sample_counts(rho, A, rng, n=4000):
    out = {}
    for s in SETTINGS:
        p = np.clip(A @ F.setting_probs(rho, s), 0, None)
        out[s] = rng.multinomial(n, p / p.sum()).astype(float)
    return out


def bootstrap(lr_obs, null_kind, null_theta, rho_ref, A, rng, warm, b=B):
    """Parametric bootstrap of the LR for 'the other kind is present', under the fitted null model."""
    null_rho = MODELS[null_kind][0](null_theta, rho_ref)
    lrs = []
    for _ in range(b):
        c = sample_counts(null_rho, A, rng)
        fits = fit_all(rho_ref, c, A, rng, n=2, warm=warm)
        lrs.append(2 * (-fits["full"].fun - (-fits[null_kind].fun)))
    lrs = np.array(lrs)
    return float((1 + np.sum(lrs >= lr_obs)) / (b + 1)), lrs.tolist()


def loso_cv(rho, counts, A, rng, warm):
    tot = {k: 0.0 for k in MODELS}
    per = []
    for s_out in SETTINGS:
        keep = [s for s in SETTINGS if s != s_out]
        fits = fit_all(rho, counts, A, rng, n=3, settings=keep, warm=warm)
        row = {"held_out": s_out}
        for k in MODELS:
            row[k] = loglik(MODELS[k][0](fits[k].x, rho), counts, A, [s_out])
            tot[k] += row[k]
        per.append(row)
    return tot, per


def analyse_item(rho_ref, counts, A, rng, b=B):
    fits = fit_all(rho_ref, counts, A, rng)
    l = {k: -v.fun for k, v in fits.items()}
    warm = {k: v.x for k, v in fits.items()}
    lr_c, lr_i = 2 * (l["full"] - l["inc"]), 2 * (l["full"] - l["coh"])
    p_c, null_c = bootstrap(lr_c, "inc", fits["inc"].x, rho_ref, A, rng, warm, b)
    p_i, null_i = bootstrap(lr_i, "coh", fits["coh"].x, rho_ref, A, rng, warm, b)
    cv, per = loso_cv(rho_ref, counts, A, rng, warm)
    gc, gi = cv["full"] - cv["inc"], cv["full"] - cv["coh"]
    return {"logL": l, "logL_saturated": F.saturated(counts), "dlogL_7v7": l["coh"] - l["inc"],
            "LR_coherent_given_incoherent": lr_c, "LR_incoherent_given_coherent": lr_i,
            "p_coherent": p_c, "p_incoherent": p_i, "null_LR_coherent": null_c, "null_LR_incoherent": null_i,
            "cv_total": cv, "cv_gain_coherent": gc, "cv_gain_incoherent": gi, "cv_per_setting": per,
            "theta": {k: v.x.tolist() for k, v in fits.items()}, "converged": {k: bool(v.success) for k, v in fits.items()},
            "negativity": {k: F.negativity(MODELS[k][0](fits[k].x, rho_ref)) for k in MODELS} | {"ref": F.negativity(rho_ref)},
            "purity": {k: float(np.real(np.trace(np.linalg.matrix_power(MODELS[k][0](fits[k].x, rho_ref), 2)))) for k in MODELS},
            "label_coherent": "present" if p_c < ALPHA else "not detected",
            "label_incoherent": "present" if p_i < ALPHA else "not detected",
            "cv_supports": {"coherent": gc > 0, "incoherent": gi > 0}}


def synthetic(fast=False):
    """D4 matched-rivals dry run, no archive: four known truths on a mixed reference."""
    rng = np.random.default_rng(0)
    psi = np.array([0.78, 0, 0, -0.63], complex); psi /= np.linalg.norm(psi)
    rho0 = np.outer(psi, psi.conj())
    ref = fam_inc(np.array([0.01, 0.005, 0.01, 0.005, 0.01, 0.01, 0.03]), rho0)
    A = np.array([[0.98, 0.02, 0.02, 0.0], [0.01, 0.97, 0.0, 0.02], [0.01, 0.0, 0.97, 0.02], [0.0, 0.01, 0.01, 0.96]])
    inc_t = np.array([0.04, 0.01, 0.06, 0.02, 0.03, 0.05, 0.08])
    coh_t = np.array([0.08, 0.12, -0.05, 0.04, -0.10, 0.06, 0.15])
    truths = {"incoherent only": fam_inc(inc_t, ref), "coherent only": F.fam_coherent(coh_t, ref),
              "both": fam_full(np.concatenate([coh_t, inc_t]), ref), "neither": ref}
    b = 20 if fast else B
    res = {}
    for name, rho_true in truths.items():
        r = analyse_item(ref, sample_counts(rho_true, A, rng), A, rng, b=b)
        res[name] = {k: r[k] for k in ("LR_coherent_given_incoherent", "LR_incoherent_given_coherent", "p_coherent",
                                       "p_incoherent", "cv_gain_coherent", "cv_gain_incoherent", "label_coherent",
                                       "label_incoherent", "dlogL_7v7")}
        print(f"truth={name:16s} coh: {r['label_coherent']:12s} LR {r['LR_coherent_given_incoherent']:7.1f} p {r['p_coherent']:.3f} cv {r['cv_gain_coherent']:+7.1f} | "
              f"inc: {r['label_incoherent']:12s} LR {r['LR_incoherent_given_coherent']:7.1f} p {r['p_incoherent']:.3f} cv {r['cv_gain_incoherent']:+7.1f} | 7v7 {r['dlogL_7v7']:+.1f}", flush=True)
    return res


def reference_states_fixed(item_files):
    """F.reference_states, but with the D8-fixed overwrite (T1/T2 actually loaded)."""
    from qiskit_aer import AerSimulator  # noqa: F401
    base = p3sim.fake_fez()
    be = p3sim.overwrite_calibration(base, p3sim.snapshot(JOB))          # fixed: legacy_t1t2_bug=False
    snap = p3sim.snapshot(JOB)
    for q in snap["qubits"]:
        assert abs(be.target.qubit_properties[q["qubit"]].t2 - q["T2_us"] * 1e-6) < 1e-12
    sim = p3sim.simulator(be, method="density_matrix")
    probs = {}
    for s, path in item_files.items():
        isa = p3sim.load_isa(path)
        meas = {isa.find_bit(i.clbits[0]).index: isa.find_bit(i.qubits[0]).index for i in isa.data if i.operation.name == "measure"}
        circ = p3sim.schedule(isa, be)
        bare = circ.copy_empty_like()
        for inst in circ.data:
            if inst.operation.name != "measure":
                bare.append(inst)
        bare.save_probabilities([meas[0], meas[1]], label="p")
        probs[s] = np.asarray(sim.run(bare).result().data(0)["p"], float)
    return F.linear_inversion(probs), probs


def spectator_check(item_files, measured, A, rho_ref, null_c, rng):
    """Secondary: steering on spectators only. Returns LR_c, LR_i on synthetic counts and the 99th pct of null_c."""
    import numpy as _np
    from qiskit_aer.noise import coherent_unitary_error
    from scipy.linalg import expm
    base = p3sim.fake_fez()
    be = p3sim.overwrite_calibration(base, p3sim.snapshot(JOB))
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel
    nm = NoiseModel.from_backend(be, thermal_relaxation=True)
    err = coherent_unitary_error(expm(-0.5j * 0.1 * _np.diag([1, -1, -1, 1]).astype(complex)))
    n_spect = 0
    for qubits in list(nm._local_quantum_errors.get("cz", {})):
        if not (set(qubits) & set(measured)):
            nm.add_quantum_error(err, ["cz"], list(qubits), warnings=False)
            n_spect += 1
    sim = AerSimulator.from_backend(be, noise_model=nm, method="density_matrix")
    probs = {}
    for s, path in item_files.items():
        isa = p3sim.load_isa(path)
        meas = {isa.find_bit(i.clbits[0]).index: isa.find_bit(i.qubits[0]).index for i in isa.data if i.operation.name == "measure"}
        circ = p3sim.schedule(isa, be)
        bare = circ.copy_empty_like()
        for inst in circ.data:
            if inst.operation.name != "measure":
                bare.append(inst)
        bare.save_probabilities([meas[0], meas[1]], label="p")
        probs[s] = _np.asarray(sim.run(bare).result().data(0)["p"], float)
    counts = {}
    for s in SETTINGS:
        p = _np.clip(A @ probs[s], 0, None)
        counts[s] = rng.multinomial(4000, p / p.sum()).astype(float)
    fits = fit_all(rho_ref, counts, A, rng)
    l = {k: -v.fun for k, v in fits.items()}
    lr_c, lr_i = 2 * (l["full"] - l["inc"]), 2 * (l["full"] - l["coh"])
    q99 = float(_np.percentile(null_c, 99))
    return {"n_spectator_cz_pairs_with_zz": n_spect, "LR_c": lr_c, "LR_i": lr_i, "null_c_q99": q99,
            "spectator_steering_detected_as_coherent": lr_c > q99, "dlogL_7v7": l["coh"] - l["inc"]}


def design_review_go():
    if not DESIGN_REVIEW.exists():
        return False
    head = DESIGN_REVIEW.read_text().split("---")[1]
    v = [l.split(":", 1)[1].strip() for l in head.splitlines() if l.startswith("verdict:")]
    c = [l.split(":", 1)[1].strip() for l in head.splitlines() if l.startswith("confirmed_at:")]
    return bool(v) and (v[0] == "go" or (v[0] == "fix-first" and c and c[0] not in ("", "null")))


def run():
    if not SEED_FILE.exists():
        raise SystemExit("no seed file")
    if not design_review_go():
        raise SystemExit("no design-review go at " + str(DESIGN_REVIEW))
    seed = json.loads(SEED_FILE.read_text())["seed32_boot"]
    rng = np.random.default_rng(seed)
    hw = json.loads((p3sim.EM / "results" / "witness-run-1.json").read_text())
    files = {}
    for k in range(39):
        rec = json.loads((p3sim.HW / f"{JOB}-{k}.json").read_text())
        if rec.get("role") == "tomography setting":
            files.setdefault(rec["item"], {})[rec["setting"]] = p3sim.HW / f"{JOB}-{k}.json"
    out = {"bet": "ng-p3-5c", "seed32_boot": seed, "B": B, "alpha": ALPHA, "items": []}
    for item in hw["items"]:
        rho_ref, _ = reference_states_fixed(files[item["id"]])
        counts = {s: F.counts_vec(c) for s, c in zip(SETTINGS, item["hardware_counts"][:9])}
        A = np.array(item["hardware"]["assignment_matrix"])
        r = analyse_item(rho_ref, counts, A, rng)
        r |= {"id": item["id"], "physical_qubits": item["physical_qubits"]}
        if item["id"] in ("h088", "h268"):
            r["spectator_check"] = spectator_check(files[item["id"]], item["physical_qubits"], A, rho_ref,
                                                   r["null_LR_coherent"], rng)
        out["items"].append(r)
        OUT.write_text(json.dumps(out, indent=1))
        print(item["id"], "coh", r["label_coherent"], round(r["LR_coherent_given_incoherent"], 1), r["p_coherent"],
              round(r["cv_gain_coherent"], 1), "| inc", r["label_incoherent"], round(r["LR_incoherent_given_coherent"], 1),
              r["p_incoherent"], round(r["cv_gain_incoherent"], 1), flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    if "--synthetic" in sys.argv:
        res = synthetic(fast="--fast" in sys.argv)
        if not "--fast" in sys.argv:
            (p3sim.ROOT / "data" / "p3-5c-synthetic-B100.json").write_text(json.dumps(res, indent=1))
    elif "--run" in sys.argv:
        run()

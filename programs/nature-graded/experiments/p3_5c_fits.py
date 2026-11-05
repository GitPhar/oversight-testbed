"""P3-5c: the corrected P3-5 re-analysis (experiments/p3-5c-nested.md). Not scored: its archive was already analysed.

    PY=/Users/seanpharris/entangled-mind/.venv/bin/python
    $PY experiments/p3_5c_fits.py --recovery     # D19 synthetic recovery on the three real reference states (no archive counts)
    $PY experiments/p3_5c_fits.py --run          # the pre-registered run (needs the seed file, a design-review go, check_prereg)

As amended after design review ledger/design-reviews/ng-p3-5c.md (DEVIATIONS D19-D25):
  rho_ref  the P3-1 construction with T1/T2 loaded and asserted (D8 fix), ALAP-scheduled; exact simulated tomography
           of the 9 as-run setting circuits, readout excluded, then linear inversion.
  models   coh (7):    U rho U^dag, U = (U_j x U_i) exp(-i phi ZZ / 2)                          rotation-type
           inc9 (9):   amplitude damping gamma_i, gamma_j in [0, 0.2], then Pauli flips p_X,Y,Z in [0, 0.25] per
                       qubit, then uniform mixing p in [0, 0.5]                                  blur-type (D19, F1)
           full16:     inc9 applied after coh.
           secondary:  inc7 (no damping) and full14, the version frozen at 930efe8.
  tests    LR_c = 2 (logL_full16 - logL_inc9), null from the fitted inc9 state;
           LR_i = 2 (logL_full16 - logL_coh),  null from the fitted coh state.
           Parametric bootstrap, B = 100, extended to B = 1,000 whenever p <= 0.05 (D20, F2); floor 1/(B+1) reported.
  label    "present" iff p < 0.01.
  also     goodness of fit (D22), per-setting LR shares and drop-one refits (D24), spectator outcomes over 20 draws
           (D23), CV as a noisy secondary (D21), P3-5 comparison three ways (D25).
"""

import json
import multiprocessing as mp
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize
from scipy.stats import chi2

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p3sim  # noqa: E402
import p3_5_fits as F  # noqa: E402

SEED_FILE = p3sim.ROOT / "data" / "p3-5c-seed.json"
OUT = p3sim.ROOT / "results" / "p3-5c-nested.json"
RECOVERY_OUT = p3sim.ROOT / "data" / "p3-5c-recovery.json"
ENGINE = p3sim.ROOT.parents[1]
DESIGN_REVIEW = ENGINE / "ledger" / "design-reviews" / "ng-p3-5c.md"
JOB = "dbl6e1d8mdtc73d5gesg"
SETTINGS = F.SETTINGS
B0, B1, EXTEND_AT, ALPHA = 100, 1000, 0.05, 0.01
N_STARTS = 10
PAULIS = [F.I2, F.X, F.Y, F.Z]
GENERIC_A = np.array([[0.98, 0.02, 0.02, 0.0], [0.01, 0.97, 0.0, 0.02], [0.01, 0.0, 0.97, 0.02], [0.0, 0.01, 0.01, 0.96]])


# --- families ---------------------------------------------------------------------------------------

def _pauli_mix(theta, rho):
    pi = np.array([1 - theta[0] - theta[1] - theta[2], theta[0], theta[1], theta[2]])
    pj = np.array([1 - theta[3] - theta[4] - theta[5], theta[3], theta[4], theta[5]])
    out = np.zeros_like(rho)
    for a in range(4):
        for b in range(4):
            K = np.kron(PAULIS[b], PAULIS[a])
            out += pi[a] * pj[b] * (K @ rho @ K.conj().T)
    return (1 - theta[6]) * out + theta[6] * np.eye(4) / 4


def _damp(gi, gj, rho):
    k = lambda g: [np.array([[1, 0], [0, np.sqrt(1 - g)]], complex), np.array([[0, np.sqrt(g)], [0, 0]], complex)]
    out = np.zeros_like(rho)
    for Ki in k(gi):
        for Kj in k(gj):
            K = np.kron(Kj, Ki)
            out += K @ rho @ K.conj().T
    return out


def fam_inc7(theta, rho):
    return _pauli_mix(theta, rho)


def fam_inc9(theta, rho):
    return _pauli_mix(theta[2:9], _damp(theta[0], theta[1], rho))


def fam_full16(theta, rho):
    return fam_inc9(theta[7:16], F.fam_coherent(theta[0:7], rho))


def fam_full14(theta, rho):
    return fam_inc7(theta[7:14], F.fam_coherent(theta[0:7], rho))


COH_B = [(None, None)] * 7
INC7_B = [(0.0, 0.25)] * 6 + [(0.0, 0.5)]
INC9_B = [(0.0, 0.2)] * 2 + INC7_B
MODELS = {"coh": (F.fam_coherent, COH_B), "inc9": (fam_inc9, INC9_B), "full16": (fam_full16, COH_B + INC9_B),
          "inc7": (fam_inc7, INC7_B), "full14": (fam_full14, COH_B + INC7_B)}
SETS = {"primary": ("coh", "inc9", "full16"), "secondary14": ("coh", "inc7", "full14")}


# --- likelihood and fitting -------------------------------------------------------------------------

def per_setting_ll(rho, counts, A, settings=SETTINGS):
    out = {}
    for s in settings:
        p = np.clip(A @ F.setting_probs(rho, s), 1e-12, None)
        out[s] = float(np.dot(counts[s], np.log(p / p.sum())))
    return out


def loglik(rho, counts, A, settings=SETTINGS):
    return sum(per_setting_ll(rho, counts, A, settings).values())


def best_fit(kind, x0s, rho, counts, A, settings=SETTINGS):
    f, bounds = MODELS[kind]
    g = lambda t: -loglik(f(t, rho), counts, A, settings)
    best = None
    for x0 in x0s:
        r = minimize(g, np.asarray(x0, float), method="L-BFGS-B", bounds=bounds)
        if best is None or r.fun < best.fun:
            best = r
    return best


def rand_start(kind, rng):
    rc = lambda: rng.uniform(-0.3, 0.3, 7)
    rp = lambda: np.concatenate([rng.uniform(0, 0.05, 6), rng.uniform(0, 0.1, 1)])
    rd = lambda: rng.uniform(0, 0.05, 2)
    return {"coh": rc, "inc7": rp, "inc9": lambda: np.concatenate([rd(), rp()]),
            "full14": lambda: np.concatenate([rc(), rp()]), "full16": lambda: np.concatenate([rc(), rd(), rp()])}[kind]()


def zero(kind):
    return np.zeros({"coh": 7, "inc7": 7, "inc9": 9, "full14": 14, "full16": 16}[kind])


def fit_set(rho, counts, A, rng, which="primary", n=N_STARTS, settings=SETTINGS, warm=None):
    c, i, f = SETS[which]
    w = warm or {}
    fc = best_fit(c, [zero(c)] + [rand_start(c, rng) for _ in range(n)] + ([w[c]] if c in w else []), rho, counts, A, settings)
    fi = best_fit(i, [zero(i)] + [rand_start(i, rng) for _ in range(n)] + ([w[i]] if i in w else []), rho, counts, A, settings)
    x0s = [zero(f)] + [rand_start(f, rng) for _ in range(n)] + [np.concatenate([fc.x, np.zeros(len(zero(i)))]),
                                                                np.concatenate([np.zeros(7), fi.x])]
    if f in w:
        x0s.append(w[f])
    ff = best_fit(f, x0s, rho, counts, A, settings)
    return {c: fc, i: fi, f: ff}


def sample_counts(rho, A, rng, n=4000):
    out = {}
    for s in SETTINGS:
        p = np.clip(A @ F.setting_probs(rho, s), 0, None)
        out[s] = rng.multinomial(n, p / p.sum()).astype(float)
    return out


# --- parametric bootstrap (parallel, adaptive) ------------------------------------------------------

def _boot_worker(args):
    null_rho, rho_ref, A, warm, which, null_kind, seed = args
    rng = np.random.default_rng(seed)
    c = sample_counts(null_rho, A, rng)
    fits = fit_set(rho_ref, c, A, rng, which=which, n=2, warm=warm)
    f = SETS[which][2]
    return 2 * (-fits[f].fun - (-fits[null_kind].fun))


def bootstrap(lr_obs, null_kind, null_theta, rho_ref, A, ss, warm, which, pool):
    """B0 draws; extended to B1 if p <= EXTEND_AT. Seeds from SeedSequence ss (reproducible)."""
    null_rho = MODELS[null_kind][0](null_theta, rho_ref)
    seeds = ss.generate_state(B1)
    args = lambda lo, hi: [(null_rho, rho_ref, A, warm, which, null_kind, int(seeds[k])) for k in range(lo, hi)]
    lrs = list(pool.map(_boot_worker, args(0, B0)))
    p = (1 + sum(x >= lr_obs for x in lrs)) / (len(lrs) + 1)
    if p <= EXTEND_AT:
        lrs += list(pool.map(_boot_worker, args(B0, B1)))
        p = (1 + sum(x >= lr_obs for x in lrs)) / (len(lrs) + 1)
    return {"p": float(p), "B": len(lrs), "floor": 1 / (len(lrs) + 1), "q99": float(np.percentile(lrs, 99)),
            "null": [float(x) for x in lrs]}


# --- one item ---------------------------------------------------------------------------------------

def analyse_item(rho_ref, counts, A, rng, ss, pool, which="primary", extras=True):
    c, i, f = SETS[which]
    fits = fit_set(rho_ref, counts, A, rng, which=which)
    l = {k: -v.fun for k, v in fits.items()}
    warm = {k: v.x for k, v in fits.items()}
    lr_c, lr_i = 2 * (l[f] - l[i]), 2 * (l[f] - l[c])
    ssc, ssi = ss.spawn(2)
    bc = bootstrap(lr_c, i, fits[i].x, rho_ref, A, ssc, warm, which, pool)
    bi = bootstrap(lr_i, c, fits[c].x, rho_ref, A, ssi, warm, which, pool)
    out = {"model_set": which, "logL": l, "LR_rotation_given_blur": lr_c, "LR_blur_given_rotation": lr_i,
           "boot_rotation": bc, "boot_blur": bi, "theta": {k: v.x.tolist() for k, v in fits.items()},
           "converged": {k: bool(v.success) for k, v in fits.items()},
           "label_rotation": "present" if bc["p"] < ALPHA else "not detected",
           "label_blur": "present" if bi["p"] < ALPHA else "not detected"}
    if not extras:
        return out
    sat = F.saturated(counts)
    k_full = len(zero(f))
    dev = 2 * (sat - l[f]); df = 27 - k_full
    out["goodness_of_fit"] = {"deviance": dev, "df": df, "chi2_q99": float(chi2.ppf(0.99, df)),
                              "misfit": bool(dev > chi2.ppf(0.99, df))}                       # D22, F4
    # D24, F6: per-setting shares of each statistic, at the fitted optima; drop-one refit when one setting dominates
    psl = {k: per_setting_ll(MODELS[k][0](fits[k].x, rho_ref), counts, A) for k in (c, i, f)}
    share = {}
    for name, a_, b_, lr in (("rotation", f, i, lr_c), ("blur", f, c, lr_i)):
        contrib = {s: 2 * (psl[a_][s] - psl[b_][s]) for s in SETTINGS}
        top = max(contrib, key=contrib.get)
        share[name] = {"per_setting": contrib, "top_setting": top, "top_share": contrib[top] / lr if lr > 0 else None}
        present = out[f"label_{name}"] == "present"
        if present and lr > 0 and contrib[top] / lr > 0.5:
            keep = [s for s in SETTINGS if s != top]
            fd = fit_set(rho_ref, counts, A, rng, which=which, settings=keep, warm=warm)
            lr_drop = 2 * (-fd[a_].fun - (-fd[b_].fun))
            q99 = (bc if name == "rotation" else bi)["q99"]
            share[name]["drop_top_refit"] = {"dropped": top, "LR": lr_drop, "exceeds_item_null_q99": lr_drop > q99,
                                             "note": "in-sample, reported, not a gate"}
    out["setting_shares"] = share
    # D21, F3: CV as a noisy secondary
    tot = {k: 0.0 for k in (c, i, f)}
    for s_out in SETTINGS:
        keep = [s for s in SETTINGS if s != s_out]
        fk = fit_set(rho_ref, counts, A, rng, which=which, n=3, settings=keep, warm=warm)
        for k in tot:
            tot[k] += loglik(MODELS[k][0](fk[k].x, rho_ref), counts, A, [s_out])
    out["cv_gain_rotation"], out["cv_gain_blur"] = tot[f] - tot[i], tot[f] - tot[c]
    out["cv_agrees"] = {"rotation": (out["cv_gain_rotation"] > 0) == (out["label_rotation"] == "present"),
                        "blur": (out["cv_gain_blur"] > 0) == (out["label_blur"] == "present")}
    out["negativity"] = {k: F.negativity(MODELS[k][0](fits[k].x, rho_ref)) for k in (c, i, f)} | {"ref": F.negativity(rho_ref)}
    return out


# --- reference states -------------------------------------------------------------------------------

def item_files():
    files = {}
    for k in range(39):
        rec = json.loads((p3sim.HW / f"{JOB}-{k}.json").read_text())
        if rec.get("role") == "tomography setting":
            files.setdefault(rec["item"], {})[rec["setting"]] = p3sim.HW / f"{JOB}-{k}.json"
    return files


def _bare_probs(be, sim, item_files_):
    probs = {}
    for s, path in item_files_.items():
        isa = p3sim.load_isa(path)
        meas = {isa.find_bit(i.clbits[0]).index: isa.find_bit(i.qubits[0]).index for i in isa.data if i.operation.name == "measure"}
        circ = p3sim.schedule(isa, be)
        bare = circ.copy_empty_like()
        for inst in circ.data:
            if inst.operation.name != "measure":
                bare.append(inst)
        bare.save_probabilities([meas[0], meas[1]], label="p")
        probs[s] = np.asarray(sim.run(bare).result().data(0)["p"], float)
    return probs


def reference_state(item_files_, legacy=False):
    be = p3sim.overwrite_calibration(p3sim.fake_fez(), p3sim.snapshot(JOB), legacy_t1t2_bug=legacy)
    if not legacy:
        for q in p3sim.snapshot(JOB)["qubits"]:
            assert abs(be.target.qubit_properties[q["qubit"]].t2 - q["T2_us"] * 1e-6) < 1e-12
    sim = p3sim.simulator(be, method="density_matrix")
    return F.linear_inversion(_bare_probs(be, sim, item_files_))


def spectator_state(item_files_, measured, zz=0.1):
    from qiskit_aer import AerSimulator
    from qiskit_aer.noise import NoiseModel, coherent_unitary_error
    from scipy.linalg import expm
    be = p3sim.overwrite_calibration(p3sim.fake_fez(), p3sim.snapshot(JOB))
    nm = NoiseModel.from_backend(be, thermal_relaxation=True)
    err = coherent_unitary_error(expm(-0.5j * zz * np.diag([1, -1, -1, 1]).astype(complex)))
    n = 0
    for qubits in list(nm._local_quantum_errors.get("cz", {})):
        if not (set(qubits) & set(measured)):
            nm.add_quantum_error(err, ["cz"], list(qubits), warnings=False); n += 1
    sim = AerSimulator.from_backend(be, noise_model=nm, method="density_matrix")
    return F.linear_inversion(_bare_probs(be, sim, item_files_)), n


def trace_distance(a, b):
    return float(0.5 * np.abs(np.linalg.eigvalsh(a - b)).sum())


# --- D19 recovery study (synthetic counts on the real reference states; no archive counts) -----------

INC_T = np.array([0.0, 0.0, 0.04, 0.01, 0.06, 0.02, 0.03, 0.05, 0.08])
COH_T = np.array([0.08, 0.12, -0.05, 0.04, -0.10, 0.06, 0.15])


def truths(ref):
    from scipy.linalg import expm
    XX = np.kron(F.X, F.X)
    U = expm(-0.5j * 0.15 * XX)
    return {"neither": ref, "blur only": fam_inc9(INC_T, ref), "rotation only": F.fam_coherent(COH_T, ref),
            "both": fam_full16(np.concatenate([COH_T, INC_T]), ref), "XX rotation 0.15 rad": U @ ref @ U.conj().T,
            "amplitude damping 0.03": _damp(0.03, 0.03, ref)}


def recovery():
    files = item_files()
    refs = {it: reference_state(files[it]) for it in ("h221", "h088", "h268")}
    root = np.random.SeedSequence(20261104)
    out = {"note": "D19: synthetic recovery on the three real reference states (T1/T2 loaded); counts are synthetic "
                   "(4,000 shots x 9 settings, generic assignment matrix); no archive counts read. Primary model set "
                   "(coh / inc9 / full16) with the adaptive bootstrap; secondary 14-knob set without extras.",
           "cells": {}, "decay_false_flags": {}, "power": {}}
    with mp.get_context("fork").Pool(11) as pool:
        for it, ref in refs.items():
            for name, rho_t in truths(ref).items():
                ss = root.spawn(1)[0]
                rng = np.random.default_rng(ss.generate_state(1)[0])
                cnt = sample_counts(rho_t, GENERIC_A, rng)
                r = analyse_item(ref, cnt, GENERIC_A, rng, ss, pool, extras=False)
                r14 = analyse_item(ref, cnt, GENERIC_A, rng, ss.spawn(1)[0], pool, which="secondary14", extras=False)
                out["cells"][f"{it} | {name}"] = {"rotation": r["label_rotation"], "blur": r["label_blur"],
                                                  "LR_rot": r["LR_rotation_given_blur"], "p_rot": r["boot_rotation"]["p"],
                                                  "B_rot": r["boot_rotation"]["B"], "q99_rot": r["boot_rotation"]["q99"],
                                                  "LR_blur": r["LR_blur_given_rotation"], "p_blur": r["boot_blur"]["p"],
                                                  "B_blur": r["boot_blur"]["B"], "q99_blur": r["boot_blur"]["q99"],
                                                  "secondary14": {"rotation": r14["label_rotation"], "blur": r14["label_blur"],
                                                                  "p_rot": r14["boot_rotation"]["p"], "p_blur": r14["boot_blur"]["p"]}}
                print(it, f"{name:22s}", "rot", r["label_rotation"], round(r["LR_rotation_given_blur"], 1), r["boot_rotation"]["p"],
                      "| blur", r["label_blur"], round(r["LR_blur_given_rotation"], 1), r["boot_blur"]["p"],
                      "| 14-knob:", r14["label_rotation"], r14["label_blur"], flush=True)
                RECOVERY_OUT.write_text(json.dumps(out, indent=1))
            # decay false-flag rate (8 draws; LR_rot against this item's bootstrap q99 from the decay cell)
            q99 = out["cells"][f"{it} | amplitude damping 0.03"]["q99_rot"]
            flags = []
            for d in range(8):
                rng = np.random.default_rng(root.spawn(1)[0].generate_state(1)[0])
                cnt = sample_counts(_damp(0.03, 0.03, ref), GENERIC_A, rng)
                fits = fit_set(ref, cnt, GENERIC_A, rng)
                flags.append(2 * (-fits["full16"].fun + fits["inc9"].fun) > q99)
            out["decay_false_flags"][it] = {"flagged": int(sum(flags)), "of": 8, "q99_used": q99}
            # power (8 draws per level; LR against the q99 of the matching recovery cell's null)
            pw = {}
            q_rot = out["cells"][f"{it} | blur only"]["q99_rot"]          # rotation null fitted on blur-only data
            q_blur = out["cells"][f"{it} | rotation only"]["q99_blur"]    # blur null fitted on rotation-only data
            for lvl in (0.0025, 0.005, 0.01):
                hits = 0
                for d in range(8):
                    rng = np.random.default_rng(root.spawn(1)[0].generate_state(1)[0])
                    th = np.array([0, 0] + [lvl / 3] * 6 + [0.0])
                    fits = fit_set(ref, sample_counts(fam_inc9(th, ref), GENERIC_A, rng), GENERIC_A, rng)
                    hits += 2 * (-fits["full16"].fun + fits["coh"].fun) > q_blur
                pw[f"blur {lvl:.4f} per qubit"] = hits / 8
            for scale in (0.025, 0.05, 0.1):
                hits = 0
                for d in range(8):
                    rng = np.random.default_rng(root.spawn(1)[0].generate_state(1)[0])
                    th = COH_T / np.linalg.norm(COH_T) * scale
                    fits = fit_set(ref, sample_counts(F.fam_coherent(th, ref), GENERIC_A, rng), GENERIC_A, rng)
                    hits += 2 * (-fits["full16"].fun + fits["inc9"].fun) > q_rot
                pw[f"rotation norm {scale} rad"] = hits / 8
            out["power"][it] = pw
            print(it, "decay false flags", out["decay_false_flags"][it], "power", pw, flush=True)
            RECOVERY_OUT.write_text(json.dumps(out, indent=1))
    return out


# --- the run ----------------------------------------------------------------------------------------

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
    chk = subprocess.run(["python3", str(ENGINE / "ledger" / "check_prereg.py"), "ng-p3-5c", str(ENGINE),
                          "programs/nature-graded/experiments/p3-5c-nested.md", "--before-run"], capture_output=True, text=True)
    if chk.returncode != 0:
        raise SystemExit("check_prereg.py --before-run failed:\n" + chk.stdout + chk.stderr)
    seed = json.loads(SEED_FILE.read_text())["seed32_boot"]
    root = np.random.SeedSequence(seed)
    rng = np.random.default_rng(seed)
    hw = json.loads((p3sim.EM / "results" / "witness-run-1.json").read_text())
    files = item_files()
    out = {"bet": "ng-p3-5c", "seed32_boot": seed, "B0": B0, "B1": B1, "extend_at": EXTEND_AT, "alpha": ALPHA, "items": []}
    with mp.get_context("fork").Pool(11) as pool:
        for item in hw["items"]:
            ref = reference_state(files[item["id"]])
            ref_legacy = reference_state(files[item["id"]], legacy=True)
            counts = {s: F.counts_vec(c) for s, c in zip(SETTINGS, item["hardware_counts"][:9])}
            A = np.array(item["hardware"]["assignment_matrix"])
            ss_p, ss_s, ss_sp = root.spawn(3)
            r = analyse_item(ref, counts, A, rng, ss_p, pool)
            r["secondary14"] = analyse_item(ref, counts, A, rng, ss_s, pool, which="secondary14", extras=False)
            # D25, F7: the P3-5 7-v-7 comparison three ways
            p35 = lambda rr: F.fit("coherent", rr, counts, A, rng)["logL"] - F.fit("incoherent", rr, counts, A, rng)["logL"]
            r["p3_5_comparison"] = {
                "P3-5 families, legacy reference (should reproduce P3-5)": p35(ref_legacy),
                "P3-5 families, fixed reference (isolates the T1/T2 fix)": p35(ref),
                "bounded 7-knob blur family, fixed reference (isolates the reparametrisation)":
                    -best_fit("coh", [zero("coh")] + [rand_start("coh", rng) for _ in range(N_STARTS)], ref, counts, A).fun
                    + best_fit("inc7", [zero("inc7")] + [rand_start("inc7", rng) for _ in range(N_STARTS)], ref, counts, A).fun,
                "9-knob blur family (with decay), fixed reference":
                    r["logL"]["coh"] - r["logL"]["inc9"]}
            # D23, F5: spectator outcomes, 20 draws, on h088 and h268
            if item["id"] in ("h088", "h268"):
                spec, n_pairs = spectator_state(files[item["id"]], item["physical_qubits"])
                q99c, q99i = r["boot_rotation"]["q99"], r["boot_blur"]["q99"]
                outcomes = []
                for d in range(20):
                    rr = np.random.default_rng(ss_sp.spawn(1)[0].generate_state(1)[0])
                    fits = fit_set(ref, sample_counts(spec, A, rr), A, rr, warm={k: np.array(v) for k, v in r["theta"].items()})
                    lc = 2 * (-fits["full16"].fun + fits["inc9"].fun); li = 2 * (-fits["full16"].fun + fits["coh"].fun)
                    outcomes.append("detected as rotation" if lc > q99c else ("absorbed as blur" if li > q99i else "invisible"))
                r["spectator"] = {"zz_rad": 0.1, "n_spectator_cz_pairs": n_pairs, "trace_distance_to_ref": trace_distance(spec, ref),
                                  "outcomes": {o: outcomes.count(o) for o in ("detected as rotation", "absorbed as blur", "invisible")},
                                  "majority": max(set(outcomes), key=outcomes.count)}
            r |= {"id": item["id"], "physical_qubits": item["physical_qubits"]}
            out["items"].append(r)
            OUT.write_text(json.dumps(out, indent=1))
            print(item["id"], "rotation", r["label_rotation"], round(r["LR_rotation_given_blur"], 1), r["boot_rotation"]["p"],
                  "| blur", r["label_blur"], round(r["LR_blur_given_rotation"], 1), r["boot_blur"]["p"], flush=True)
    OUT.write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    if "--recovery" in sys.argv:
        recovery()
    elif "--run" in sys.argv:
        run()

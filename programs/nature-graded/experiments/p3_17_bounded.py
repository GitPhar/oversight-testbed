"""P3-17: is P3-5c's blur-type term still needed when readout error may be up to 3x each job's calibration value?
(experiments/p3-17-bounded-readout.md, bet ng-p3-17; scored.)

    PY=/Users/seanpharris/entangled-mind/.venv/bin/python
    $PY experiments/p3_17_bounded.py --check       # knob mechanics on synthetic states only (no archive counts)
    $PY experiments/p3_17_bounded.py --recovery    # pre-run worlds (D11/P12): reference states from archived circuits,
                                                   # P3-5c's published fitted parameters, the archived assignment
                                                   # matrices; synthetic counts only, no archived tomography counts
    $PY experiments/p3_17_bounded.py --run         # the pre-registered run (seed file, design-review go, check_prereg,
                                                   # every file it uses committed and unchanged)

Readout knobs. Each P3-5c model gets four knobs: per measured qubit q, e0_q (extra P(read 1 | prepared 0)) and
e1_q (extra P(read 0 | prepared 1)), applied after the archived assignment matrix A:
    A'(e) = (R_j (x) R_i) A,   R_q = [[1 - e0_q, e1_q], [e0_q, 1 - e1_q]]   (columns: prepared bit; rows: read bit)
Primary bound (the bet): r_q,b is qubit q's misread rate for prepared value b in the same job's calibration (from A:
the mean of the two calibration columns with that prepared value, 8,000 shots). The knob may move the readout
error from 0 up to 3 x r:  e in [-r, +2 r].
Secondary bounds (point fits only, reported, not tests): "knob" |e| <= 3 r (the cockpit card's wording);
"3 SE" |e| <= 3 x binomial SE of r (the remap's test text); "wide" e in [-0.02, 0.05] (audit ng-p3-5c, round 2).

Tests (models as P3-5c's primary set, D19: coh 7, inc9 9, full16 16; each +4 knobs -> cohR 11, inc9R 13, full16R 20)
    primary    LR_b = 2 (logL_full16R - logL_cohR); null: parametric bootstrap from the fitted cohR (its state and its
               knobs), each draw refitted with cohR and full16R; B = 100, extended to 1,000 if p <= 0.05;
               blur "still needed" on a pair iff p < 0.01.
    pass       still needed on all three pairs (h221, h088, h268).
"""

from __future__ import annotations

import hashlib
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
import p3_5c_fits as C  # noqa: E402

ROOT = p3sim.ROOT
ENGINE = ROOT.parents[1]
BET = "ng-p3-17"
PREREG = "programs/nature-graded/experiments/p3-17-bounded-readout.md"
SEED_FILE = ROOT / "data" / "p3-17-seed.json"
RECOVERY_OUT = ROOT / "data" / "p3-17b-recovery.json"
OUT = ROOT / "results" / "p3-17-bounded-readout.json"
DESIGN_REVIEW = ENGINE / "ledger" / "design-reviews" / "ng-p3-17.md"
P35C = ROOT / "results" / "p3-5c-nested.json"
SETTINGS = F.SETTINGS
ITEMS = ("h221", "h088", "h268")
B0, B1, EXTEND_AT, ALPHA = 100, 1000, 0.05, 0.01
N_STARTS = 10
N_CAL = 8000            # calibration shots behind each rate: 2 prepared states x 4,000 shots
K_BOUND = 3.0           # readout error allowed up to K_BOUND x the calibration value
# Every file the run executes or reads, relative to the engine root: the run refuses if any is uncommitted or changed.
USES = ["programs/nature-graded/experiments/p3_17_bounded.py", "programs/nature-graded/experiments/p3_5c_fits.py",
        "programs/nature-graded/experiments/p3_5_fits.py", "programs/nature-graded/experiments/p3sim.py",
        "programs/nature-graded/data/p3-17-seed.json", "programs/nature-graded/results/p3-5c-nested.json",
        "programs/entangled-mind/results/witness-run-1.json", "programs/entangled-mind/results/ibm-calibration.json",
        "programs/entangled-mind/window/data/hardware", PREREG, "ledger/design-reviews/ng-p3-17.md",
        "ledger/check_prereg.py", "ledger/human_odds_match.py"]


# --- readout knobs ------------------------------------------------------------------------------------

def rates(A):
    """Per-qubit misread rates from an assignment matrix A (A[m, k] = P(read m | prepared k), index 2*b_j + b_i).
    Returns [e0_i, e1_i, e0_j, e1_j], each the mean over the two prepared states with that bit value."""
    A = np.asarray(A, float)
    bi = lambda k: k & 1
    bj = lambda k: k >> 1
    def rate(bit, val):
        cols = [k for k in range(4) if bit(k) == val]
        wrong = [m for m in range(4) if bit(m) != val]
        return float(np.mean([A[wrong, k].sum() for k in cols]))
    return [rate(bi, 0), rate(bi, 1), rate(bj, 0), rate(bj, 1)]


def bounds_for(A, kind="primary"):
    r = rates(A)
    if kind == "primary":
        return [(-x, (K_BOUND - 1.0) * x) for x in r]
    if kind == "knob":
        return [(-K_BOUND * x, K_BOUND * x) for x in r]
    if kind == "3se":
        se = [np.sqrt(x * (1 - x) / N_CAL) for x in r]
        return [(-3 * s, 3 * s) for s in se]
    if kind == "wide":
        return [(-0.02, 0.05)] * 4
    raise ValueError(kind)


def readout(A, e):
    Ri = np.array([[1 - e[0], e[1]], [e[0], 1 - e[1]]])
    Rj = np.array([[1 - e[2], e[3]], [e[2], 1 - e[3]]])
    return np.kron(Rj, Ri) @ np.asarray(A, float)


# --- models with knobs -----------------------------------------------------------------------------------

BASE = {"cohR": "coh", "inc9R": "inc9", "full16R": "full16"}
NK = {"coh": 7, "inc9": 9, "full16": 16}


def state_and_A(kind, theta, rho_ref, A):
    b = BASE[kind]
    k = NK[b]
    return C.MODELS[b][0](theta[:k], rho_ref), readout(A, theta[k:k + 4])


def ll(kind, theta, rho_ref, counts, A, settings=SETTINGS):
    rho, A2 = state_and_A(kind, theta, rho_ref, A)
    return C.loglik(rho, counts, A2, settings)


def fit(kind, x0s, rho_ref, counts, A, kb, settings=SETTINGS):
    bnds = C.MODELS[BASE[kind]][1] + list(kb)
    g = lambda t: -ll(kind, t, rho_ref, counts, A, settings)
    best = None
    for x0 in x0s:
        x0 = np.clip(np.asarray(x0, float), [lo if lo is not None else -np.inf for lo, _ in bnds],
                     [hi if hi is not None else np.inf for _, hi in bnds])
        r = minimize(g, x0, method="L-BFGS-B", bounds=bnds)
        if best is None or r.fun < best.fun:
            best = r
    return best


N_RAND = 3              # random starts per model: the same for the observed fits and for every null draw (F2, D43)


def rand_knobs(kb, rng):
    return np.array([rng.uniform(lo, hi) for lo, hi in kb])


def corner(kb):
    return np.array([hi for _, hi in kb], float)


def start_list(kind, rng, kb, informed, warm=None):
    """F2 (D43): one start recipe for observed and null fits alike: zero; zero state with the knobs at the upper
    corner; N_RAND random states with random knobs inside the bounds; P3-5c's optimum for this base model with knobs
    at 0 and at the corner (`informed`, fixed constants); and the observed optimum (`warm`) when given."""
    b = BASE[kind]
    k = NK[b]
    out = [np.zeros(k + 4), np.concatenate([np.zeros(k), corner(kb)])]
    out += [np.concatenate([C.rand_start(b, rng), rand_knobs(kb, rng)]) for _ in range(N_RAND)]
    for x in informed.get(kind, []):
        x = np.asarray(x, float)
        out += [np.concatenate([x, np.zeros(4)]), np.concatenate([x, corner(kb)])]
    if warm is not None and kind in warm:
        out.append(np.asarray(warm[kind], float))
    return out


def fit_pair(rho_ref, counts, A, kb, rng, informed, warm=None, with_inc=False, settings=SETTINGS):
    """cohR and full16R (and inc9R if asked), every fit from start_list(). full16R also starts from cohR's optimum
    with zero blur (and inc9R's with zero rotation); then cohR is refitted once from full16R's optimum with the blur
    block removed (theta[:7] + theta[16:20]) and the better cohR kept (F2)."""
    fc = fit("cohR", start_list("cohR", rng, kb, informed, warm), rho_ref, counts, A, kb, settings)
    out = {}
    extra = [np.concatenate([fc.x[:7], np.zeros(9), fc.x[7:]])]
    if with_inc:
        fi = fit("inc9R", start_list("inc9R", rng, kb, informed, warm), rho_ref, counts, A, kb, settings)
        out["inc9R"] = fi
        extra.append(np.concatenate([np.zeros(7), fi.x]))
    ff = fit("full16R", start_list("full16R", rng, kb, informed, warm) + extra, rho_ref, counts, A, kb, settings)
    fc2 = fit("cohR", [np.concatenate([ff.x[:7], ff.x[16:20]])], rho_ref, counts, A, kb, settings)
    out["cohR"] = fc2 if fc2.fun < fc.fun else fc
    out["full16R"] = ff
    return out


def informed_for(p35item):
    th = p35item["theta"]
    return {"cohR": [th["coh"]], "inc9R": [th["inc9"]], "full16R": [th["full16"]]}


def lr_b_of(f):
    return float(2 * (f["cohR"].fun - f["full16R"].fun))


def sample(rho, A2, rng, n=4000):
    return C.sample_counts(rho, A2, rng, n)


# --- parametric bootstrap: two generators, the larger p (F1, D43) ----------------------------------------------------

def _boot_worker(args):
    null_rho, null_A, rho_ref, A, kb, informed, warm, seed = args
    rng = np.random.default_rng(seed)
    c = sample(null_rho, null_A, rng)
    return lr_b_of(fit_pair(rho_ref, c, A, kb, rng, informed, warm=warm))


def corner_null_theta(rho_ref, counts, A, kb, rng, informed, settings=SETTINGS):
    """F1(i): the coh state refitted with all four knobs held at their upper bound."""
    kb_fixed = [(hi, hi) for _, hi in kb]
    f = fit("cohR", start_list("cohR", rng, kb_fixed, informed), rho_ref, counts, A, kb_fixed, settings)
    return f.x


def _one_null(lr_obs, theta, rho_ref, A, kb, ss, informed, warm, pool, b0, b1):
    null_rho, null_A = state_and_A("cohR", theta, rho_ref, A)
    seeds = ss.generate_state(b1)
    args = lambda lo, hi: [(null_rho, null_A, rho_ref, A, kb, informed, warm, int(seeds[k])) for k in range(lo, hi)]
    lrs = list(pool.map(_boot_worker, args(0, b0)))
    p = (1 + sum(x >= lr_obs for x in lrs)) / (len(lrs) + 1)
    if p <= EXTEND_AT and b1 > b0:
        lrs += list(pool.map(_boot_worker, args(b0, b1)))
        p = (1 + sum(x >= lr_obs for x in lrs)) / (len(lrs) + 1)
    return {"p": float(p), "B": len(lrs), "floor": 1 / (len(lrs) + 1), "q99": float(np.percentile(lrs, 99)),
            "max": float(max(lrs)), "theta": [float(x) for x in theta], "null": [float(x) for x in lrs]}


def bootstrap(lr_obs, theta_fitted, theta_corner, rho_ref, A, kb, ss, informed, warm, pool, b0=B0, b1=B1):
    """F1(i): nulls generated at the fitted cohR point and at the corner fit; p = max of the two (same B rule each)."""
    s1, s2 = ss.spawn(2)
    a = _one_null(lr_obs, theta_fitted, rho_ref, A, kb, s1, informed, warm, pool, b0, b1)
    b = _one_null(lr_obs, theta_corner, rho_ref, A, kb, s2, informed, warm, pool, b0, b1)
    return {"p": max(a["p"], b["p"]), "B_complete": a["B"] in (b0, b1) and b["B"] in (b0, b1),
            "q99": max(a["q99"], b["q99"]), "fitted": a, "corner": b}


# --- the verdict (section 5), from the per-pair results ---------------------------------------------------------

RO = "per-qubit readout error of the modelled kind (each qubit separately, fixed over the job)"


def robustness_sentence(per_setting, lr):
    """F4 (D43): on a 'still needed' pair, name the setting(s) carrying most of LR_b."""
    if not per_setting or lr <= 0:
        return None, None
    order = sorted(per_setting, key=per_setting.get, reverse=True)
    s1, s2 = per_setting[order[0]] / lr, (per_setting[order[0]] + per_setting[order[1]]) / lr
    if s1 > 0.5:
        return f"This rests mostly on setting {order[0]}.", None
    if s2 > 0.67:
        return f"This rests mostly on settings {order[0]} and {order[1]}.", order[:2]
    return None, None


def verdict(pairs: dict) -> dict:
    """pairs: {item: {"finite", "B_complete", "p", "lr_b", "per_setting", "deviance", "misfit", "scaled_lr_b",
    "null_q99"}}. Returns the verdict and the section 5 sentences (as amended by D43)."""
    if set(pairs) != set(ITEMS) or any(not v["finite"] or not v["B_complete"] for v in pairs.values()):
        bad = [k for k in ITEMS if k not in pairs or not pairs[k]["finite"] or not pairs[k]["B_complete"]]
        return {"verdict": "untestable", "sentences": [
            f"The refit could not be completed on {', '.join(bad)}, so this test cannot say whether {RO} within three "
            "times the calibration value can stand in for the blur-type term."]}
    needed = [k for k in ITEMS if pairs[k]["p"] < ALPHA]
    not_needed = [k for k in ITEMS if k not in needed]
    S, drop2 = [], {}
    for k in ITEMS:
        v = pairs[k]
        if k in needed:
            t = (f"On pair {k}, the blur-type term is still needed even when {RO} may be up to three times its "
                 "calibration value in that job: readout knobs of this kind, that large, cannot stand in for it.")
            rs, two = robustness_sentence(v.get("per_setting"), v["lr_b"])
            if rs:
                t += " " + rs
            if two:
                drop2[k] = two
        else:
            t = (f"On pair {k}, the blur-type term is no longer needed once {RO} may be up to three times its "
                 "calibration value in that job: on this pair the archive cannot tell the blur-type term from readout "
                 "knobs of this kind.")
        if v.get("misfit") and v.get("scaled_lr_b") is not None and v["scaled_lr_b"] <= v["null_q99"]:
            t += (f" Its full model misfits these counts (deviance {v['deviance']:.1f} on 7 df); scaled for that misfit, "
                  "the blur-type term's gain is within its null, so on this pair the label rests on a null the counts reject.")
        S.append(t)
    if not not_needed:
        S.append(f"Overall: on all three archived pairs (one job, 3 November), P3-5c's blur-type term is still needed when "
                 f"{RO} may be up to three times the job's own calibration value. These are terms in a fitted model, not "
                 "identified physical mechanisms; larger readout drift, and readout errors of other kinds (correlated "
                 "between qubits, or drifting during the job), are not excluded.")
        return {"verdict": "pass", "sentences": S, "needed": needed, "not_needed": not_needed, "drop_two": drop2}
    S.append(f"Overall: on {len(not_needed)} of 3 archived pairs ({', '.join(not_needed)}), readout knobs of this kind "
             "within three times the job's calibration value can stand in for P3-5c's blur-type term, so P3-5c's finding "
             "that the 16-knob model needs a blur-type term on all three archived pairs does not stand on the archive "
             "alone. This does not show the chip was misreading; it shows the archive cannot tell the blur-type term "
             "from readout knobs of this kind on those pairs.")
    return {"verdict": "fail", "sentences": S, "needed": needed, "not_needed": not_needed, "drop_two": drop2}


# --- gates -----------------------------------------------------------------------------------------------

def git(*a):
    return subprocess.check_output(["git", "-C", str(ENGINE), *a], text=True).strip()


def uncommitted(paths):
    """Paths (relative to the engine root) that are untracked, modified, or staged-but-uncommitted."""
    bad = []
    for p in paths:
        if subprocess.run(["git", "-C", str(ENGINE), "ls-files", "--error-unmatch", p], capture_output=True).returncode:
            bad.append(p + " (not tracked)")
            continue
        st = git("status", "--porcelain", "--", p)
        if st:
            bad.append(p + " (" + st.splitlines()[0][:2].strip() + ")")
    return bad


def design_review_go():
    if not DESIGN_REVIEW.exists():
        return False
    head = DESIGN_REVIEW.read_text().split("---")[1]
    v = [l.split(":", 1)[1].strip() for l in head.splitlines() if l.startswith("verdict:")]
    c = [l.split(":", 1)[1].strip() for l in head.splitlines() if l.startswith("confirmed_at:")]
    return bool(v) and (v[0] == "go" or (v[0] == "fix-first" and c and c[0] not in ("", "null")))


def gates():
    if not SEED_FILE.exists():
        raise SystemExit("no seed file: the seed commit must land first")
    if not design_review_go():
        raise SystemExit("no design-review go (or confirmed fix-first) at " + str(DESIGN_REVIEW))
    bad = uncommitted(USES)
    if bad:
        raise SystemExit("refused: files this run uses are not committed and unchanged:\n  " + "\n  ".join(bad))
    chk = subprocess.run(["python3", str(ENGINE / "ledger" / "check_prereg.py"), BET, str(ENGINE), PREREG, "--before-run"],
                         capture_output=True, text=True)
    if chk.returncode != 0:
        raise SystemExit("check_prereg.py --before-run failed:\n" + chk.stdout + chk.stderr)
    if OUT.exists():
        raise SystemExit(f"{OUT.name} exists: the run is never repeated")


# --- inputs ------------------------------------------------------------------------------------------------

def assignment_matrices():
    """The archived per-pair assignment matrices (calibration only; no tomography counts are read here)."""
    hw = json.loads((p3sim.EM / "results" / "witness-run-1.json").read_text())
    return {it["id"]: np.array(it["hardware"]["assignment_matrix"]) for it in hw["items"]}


def tomography_counts():
    hw = json.loads((p3sim.EM / "results" / "witness-run-1.json").read_text())
    return {it["id"]: {s: F.counts_vec(c) for s, c in zip(SETTINGS, it["hardware_counts"][:9])} for it in hw["items"]}


# --- check: knob mechanics on synthetic states (D2) ------------------------------------------------------------

def versions():
    import importlib.metadata as md
    out = {"python": sys.version.split()[0]}
    for pkg in ("numpy", "scipy", "qiskit", "qiskit-aer", "qiskit-ibm-runtime"):
        try:
            out[pkg] = md.version(pkg)
        except Exception:  # noqa: BLE001
            out[pkg] = None
    return out


def check():
    rng = np.random.default_rng(1)
    psi = np.array([1, 0, 0, 1]) / np.sqrt(2)
    ref = np.outer(psi, psi).astype(complex)
    A = C.GENERIC_A
    r = rates(A)
    print("rates of GENERIC_A [e0_i, e1_i, e0_j, e1_j]:", [round(x, 4) for x in r])
    for kind in ("primary", "knob", "3se", "wide"):
        print(f"  bounds {kind:8s}", [(round(float(a), 4), round(float(b), 4)) for a, b in bounds_for(A, kind)])
    kb = bounds_for(A)
    up = corner(kb)
    A_up = readout(A, up)
    print("columns of A' sum to 1:", np.allclose(A_up.sum(0), 1), "| A' - A max", round(float(np.abs(A_up - A).max()), 4))
    print("rates of A' at the upper bound (about 3 x rates of A):", [round(x, 4) for x in rates(A_up)])
    print("rates of A' at the lower bound (about 0):", [round(x, 4) for x in rates(readout(A, [a for a, _ in kb]))])
    cnt = sample(ref, A_up, rng)
    f = fit_pair(ref, cnt, A, kb, rng, {})
    print("fitted cohR knobs on readout-only synthetic data:", [round(float(x), 4) for x in f["cohR"].x[7:]], "true", list(up))
    print("LR_b on readout-only synthetic data:", round(lr_b_of(f), 3))
    print("verdict() on synthetic tables:")
    base = {"finite": True, "B_complete": True, "lr_b": 40.0, "per_setting": {s: 40.0 / 9 for s in SETTINGS},
            "deviance": 10.0, "misfit": False, "scaled_lr_b": 40.0, "null_q99": 12.0}
    tab = lambda ps, **kw: {k: {**base, "p": p, **kw.get(k, {})} for k, p in ps.items()}
    for ps in ({"h221": .001, "h088": .001, "h268": .001}, {"h221": .2, "h088": .001, "h268": .001},
               {"h221": .01, "h088": .001, "h268": .001}, {"h221": .0099, "h088": .001, "h268": .5}):
        print("  ", ps, "->", verdict(tab(ps))["verdict"])
    print("   non-finite h221 ->", verdict(tab({"h221": .001, "h088": .001, "h268": .001}, h221={"finite": False}))["verdict"])
    one = {s: (30.0 if s == "XZ" else 10.0 / 8) for s in SETTINGS}
    two = {s: (16.0 if s in ("XZ", "XY") else 8.0 / 7) for s in SETTINGS}
    v = verdict(tab({"h221": .001, "h088": .001, "h268": .001}, h221={"per_setting": one}, h268={"per_setting": two},
                    h088={"misfit": True, "deviance": 63.3, "scaled_lr_b": 9.0}))
    for t in v["sentences"]:
        print("   ", t)
    print("   drop-two refit requested for:", v["drop_two"])


# --- recovery: pre-run worlds per pair (D3, D11 / P12; amended by F1, D43) ---------------------------------------

def _draw_worker(args):
    rho_t, A_t, ref, A, kb, informed, seed, truth = args
    rng = np.random.default_rng(seed)
    cnt = sample(rho_t, A_t, rng)
    f = fit_pair(ref, cnt, A, kb, rng, informed)
    out = {"LR_b": lr_b_of(f), "cohR_knobs": [float(x) for x in f["cohR"].x[7:]], "cohR_fun": float(f["cohR"].fun),
           "theta_cohR": [float(x) for x in f["cohR"].x], "warm": {k: [float(x) for x in v.x] for k, v in f.items()},
           "corner_theta": [float(x) for x in corner_null_theta(ref, cnt, A, kb, rng, informed)]}
    if truth is not None:                                  # F2: shortfall of the procedure against a truth-started fit
        ft = fit("cohR", [np.asarray(truth, float)], ref, cnt, A, kb)
        out["cohR_shortfall_vs_truth_start"] = float(f["cohR"].fun - ft.fun)
    return out


def recovery():
    """F1 (D43). Worlds, 4,000 shots x 9 settings, synthetic counts only (no archived tomography counts):
      W_blur     truth = P3-5c's published fitted full16 state through the archived A           (8 draws per pair)
      W_readout  truth = P3-5c's fitted coh state through A'(the primary knobs' upper corner)    (24 draws per pair)
      W_mixed    h088 as W_blur, h221 and h268 as W_readout (P(pass) from the per-pair rates)
    Each world's draws are classified with the run's two-generator rule at B = 100: 'still needed' iff LR_b exceeds
    the larger of the 99th percentiles of the null at the first draw's fitted cohR point and of the null at its
    corner fit. Also (F2) the cohR shortfall of the procedure against a fit started at the truth, on the first 16
    W_readout draws per pair."""
    p35 = {it["id"]: it for it in json.loads(P35C.read_text())["items"]}
    As = assignment_matrices()
    files = C.item_files()
    root = np.random.SeedSequence(20261105)
    out = {"note": recovery.__doc__, "root_seed": 20261105, "versions": versions(), "cells": {}}
    n_draws = {"W_blur": 8, "W_readout": 24}
    with mp.get_context("fork").Pool(11) as pool:
        for it in ITEMS:
            ref = C.reference_state(files[it])
            A = As[it]
            kb = bounds_for(A)
            th = p35[it]["theta"]
            inf = informed_for(p35[it])
            up = corner(kb)
            worlds = {"W_blur": (C.fam_full16(np.array(th["full16"]), ref), A, None),
                      "W_readout": (F.fam_coherent(np.array(th["coh"]), ref), readout(A, up),
                                    np.concatenate([np.array(th["coh"]), up]))}
            for w, (rho_t, A_t, truth) in worlds.items():
                ss = root.spawn(1)[0]
                seeds = [int(x) for x in ss.generate_state(n_draws[w])]
                draws = pool.map(_draw_worker, [(rho_t, A_t, ref, A, kb, inf, sd, truth if k < 16 else None)
                                                for k, sd in enumerate(seeds)])
                d0 = draws[0]
                bs = bootstrap(d0["LR_b"], np.array(d0["theta_cohR"]), np.array(d0["corner_theta"]), ref, A, kb,
                               ss.spawn(1)[0], inf, {k: np.array(v) for k, v in d0["warm"].items()}, pool, b0=B0, b1=B0)
                thr = bs["q99"]
                needed = sum(d["LR_b"] > thr for d in draws)
                cell = {"LR_b": [d["LR_b"] for d in draws], "q99_fitted_B100": bs["fitted"]["q99"],
                        "q99_corner_B100": bs["corner"]["q99"], "threshold": thr, "blur_still_needed": int(needed),
                        "of": len(draws), "rate": needed / len(draws), "cohR_knobs_fitted": [d["cohR_knobs"] for d in draws],
                        "knob_bounds": kb, "true_knobs": (list(up) if w == "W_readout" else [0, 0, 0, 0])}
                sh = [d["cohR_shortfall_vs_truth_start"] for d in draws if "cohR_shortfall_vs_truth_start" in d]
                if sh:
                    cell["cohR_shortfall_vs_truth_start_max"] = max(sh)
                    cell["cohR_shortfall_n"] = len(sh)
                out["cells"][f"{it} | {w}"] = cell
                print(it, w, "LR_b", [round(x, 1) for x in cell["LR_b"]], "q99 fitted/corner", round(bs["fitted"]["q99"], 1),
                      round(bs["corner"]["q99"], 1), "needed", needed, "/", len(draws),
                      ("| max cohR shortfall %.4f" % max(sh)) if sh else "", flush=True)
                RECOVERY_OUT.write_text(json.dumps(out, indent=1))
    rate = lambda it, w: out["cells"][f"{it} | {w}"]["rate"]
    out["P_still_needed_W_readout_per_pair"] = {it: rate(it, "W_readout") for it in ITEMS}
    out["P_pass_W_blur"] = float(np.prod([rate(it, "W_blur") for it in ITEMS]))
    out["P_fail_W_readout"] = 1 - float(np.prod([rate(it, "W_readout") for it in ITEMS]))
    out["P_pass_W_mixed"] = rate("h088", "W_blur") * rate("h221", "W_readout") * rate("h268", "W_readout")
    out["F1_ii_each_W_readout_rate_le_0.05"] = all(rate(it, "W_readout") <= 0.05 for it in ITEMS)
    out["F1_iii_P_pass_W_mixed_le_0.05"] = out["P_pass_W_mixed"] <= 0.05
    RECOVERY_OUT.write_text(json.dumps(out, indent=1))
    print("P(still needed | W_readout) per pair:", out["P_still_needed_W_readout_per_pair"])
    print("P(pass | W_blur) =", round(out["P_pass_W_blur"], 3), " P(fail | W_readout) =", round(out["P_fail_W_readout"], 3),
          " P(pass | W_mixed) =", round(out["P_pass_W_mixed"], 4))
    return out


# --- the run -------------------------------------------------------------------------------------------------

def run():
    gates()
    sd = json.loads(SEED_FILE.read_text())
    seed = sd["seed32_boot"]
    root = np.random.SeedSequence(seed)
    rng = np.random.default_rng(seed)
    p35 = {it["id"]: it for it in json.loads(P35C.read_text())["items"]}
    As = assignment_matrices()
    counts_all = tomography_counts()          # the archived tomography counts are opened here, after every gate
    files = C.item_files()
    out = {"bet": BET, "seed32_boot": seed, "B0": B0, "B1": B1, "extend_at": EXTEND_AT, "alpha": ALPHA,
           "k_bound": K_BOUND, "n_rand": N_RAND, "made_at_head": git("rev-parse", "--short", "HEAD"), "versions": versions(),
           "inputs_sha256": {p: hashlib.sha256((ENGINE / p).read_bytes()).hexdigest() for p in USES
                             if (ENGINE / p).is_file()}, "items": []}
    pairs = {}
    with mp.get_context("fork").Pool(11) as pool:
        for it in ITEMS:
            ref = C.reference_state(files[it])
            A, counts = As[it], counts_all[it]
            kb = bounds_for(A)
            inf = informed_for(p35[it])
            ss_p = root.spawn(1)[0]
            f = fit_pair(ref, counts, A, kb, rng, inf, with_inc=True)
            l = {k: -v.fun for k, v in f.items()}
            finite = all(np.isfinite(v) for v in l.values())
            lr_b = 2 * (l["full16R"] - l["cohR"])
            lr_r = 2 * (l["full16R"] - l["inc9R"])
            warm = {k: v.x for k, v in f.items() if k != "inc9R"}
            th_corner = corner_null_theta(ref, counts, A, kb, rng, inf)
            bs = bootstrap(lr_b, f["cohR"].x, th_corner, ref, A, kb, ss_p, inf, warm, pool) if finite else None
            sat = F.saturated(counts)
            dev = 2 * (sat - l["full16R"]); df = 27 - 20
            psl = {k: (lambda rho_, A_: C.per_setting_ll(rho_, counts, A_))(*state_and_A(k, f[k].x, ref, A)) for k in ("cohR", "full16R")}
            contrib = {s: 2 * (psl["full16R"][s] - psl["cohR"][s]) for s in SETTINGS}
            top = max(contrib, key=contrib.get)
            r = {"id": it, "rates": rates(A), "knob_bounds": kb, "logL": l, "LR_blur_given_rotation_readout": lr_b,
                 "LR_rotation_given_blur_readout_point": lr_r, "boot_blur": bs,
                 "label_blur": ("still needed" if bs and bs["p"] < ALPHA else "not needed"),
                 "theta": {k: v.x.tolist() for k, v in f.items()}, "corner_null_theta": list(map(float, th_corner)),
                 "converged": {k: bool(v.success) for k, v in f.items()},
                 "knobs_at_bound": {k: [bool(abs(x - lo) < 1e-6 or abs(x - hi) < 1e-6)
                                        for x, (lo, hi) in zip(v.x[-4:], kb)] for k, v in f.items()},
                 "goodness_of_fit": {"deviance": dev, "df": df, "chi2_q99": float(chi2.ppf(0.99, df)),
                                     "misfit": bool(dev > chi2.ppf(0.99, df)),
                                     "LR_b_scaled_by_overdispersion": lr_b / max(1.0, dev / df)},
                 "setting_shares": {"per_setting": contrib, "top_setting": top,
                                    "top_share": contrib[top] / lr_b if lr_b > 0 else None}}
            pairs[it] = {"finite": bool(finite), "B_complete": bool(bs and bs["B_complete"]), "p": bs["p"] if bs else 1.0,
                         "lr_b": float(lr_b), "per_setting": contrib, "deviance": float(dev), "misfit": r["goodness_of_fit"]["misfit"],
                         "scaled_lr_b": float(r["goodness_of_fit"]["LR_b_scaled_by_overdispersion"]),
                         "null_q99": bs["q99"] if bs else None}
            sec = {}
            for kind in ("knob", "3se", "wide"):
                kb2 = bounds_for(A, kind)
                w2 = {k: np.concatenate([v[:-4], np.clip(v[-4:], [a for a, _ in kb2], [b for _, b in kb2])]) for k, v in warm.items()}
                f2 = fit_pair(ref, counts, A, kb2, rng, inf, warm=w2)
                sec[kind] = {"bounds": kb2, "LR_b_point": lr_b_of(f2), "cohR_knobs": f2["cohR"].x[7:].tolist(),
                             "note": "point fit only; compared with the primary null's 99th percentile, not a test"}
            r["secondary_bounds"] = sec
            r["P3_5c_LR_blur_given_rotation"] = p35[it]["LR_blur_given_rotation"]
            out["items"].append(r)
            OUT.write_text(json.dumps(out, indent=1))
            print(it, "LR_b", round(lr_b, 2), "p", bs and bs["p"], "q99", bs and round(bs["q99"], 2), "label", r["label_blur"],
                  "| secondary LR_b", {k: round(v["LR_b_point"], 2) for k, v in sec.items()}, flush=True)
    v = verdict(pairs)
    for it, two in v["drop_two"].items():                  # F4: post-hoc drop-both refit, reported, not a gate
        rr = next(x for x in out["items"] if x["id"] == it)
        keep = [s for s in SETTINGS if s not in two]
        ref = C.reference_state(files[it])
        A = As[it]
        f3 = fit_pair(ref, counts_all[it], A, bounds_for(A), rng, informed_for(p35[it]), settings=keep,
                      warm={k: np.array(x) for k, x in rr["theta"].items() if k != "inc9R"})
        rr["drop_two_refit"] = {"dropped": two, "LR_b": lr_b_of(f3), "null_q99_full_data": rr["boot_blur"]["q99"],
                                "note": "in-sample, post hoc, reported, not a gate"}
    out["pairs"] = pairs
    out["verdict"] = v["verdict"]
    out["sentences"] = v["sentences"]
    OUT.write_text(json.dumps(out, indent=1))
    print("VERDICT", v["verdict"])
    for s in v["sentences"]:
        print(" ", s)


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    elif "--recovery" in sys.argv:
        recovery()
    elif "--run" in sys.argv:
        run()
    else:
        sys.exit(__doc__)

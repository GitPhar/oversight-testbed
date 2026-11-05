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
        "ledger/check_prereg.py"]


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


def starts(kind, rng, n, warm=None, extra=()):
    b = BASE[kind]
    out = [np.zeros(NK[b] + 4)] + [np.concatenate([C.rand_start(b, rng), np.zeros(4)]) for _ in range(n)]
    out += [np.asarray(x, float) for x in extra]
    if warm is not None and kind in warm:
        out.append(np.asarray(warm[kind], float))
    return out


def fit_pair(rho_ref, counts, A, kb, rng, n=N_STARTS, warm=None, with_inc=False, settings=SETTINGS, plain=None):
    """cohR and full16R (and inc9R if asked). full16R also starts from cohR's optimum with zero blur, from P3-5c's
    full16 optimum with zero knobs (`plain`), and from inc9R's optimum with zero rotation."""
    fc = fit("cohR", starts("cohR", rng, n, warm), rho_ref, counts, A, kb, settings)
    out = {"cohR": fc}
    extra = [np.concatenate([fc.x[:7], np.zeros(9), fc.x[7:]])]
    if plain is not None:
        extra.append(np.concatenate([np.asarray(plain, float), np.zeros(4)]))
    if with_inc:
        fi = fit("inc9R", starts("inc9R", rng, n, warm), rho_ref, counts, A, kb, settings)
        out["inc9R"] = fi
        extra.append(np.concatenate([np.zeros(7), fi.x]))
    out["full16R"] = fit("full16R", starts("full16R", rng, n, warm, extra), rho_ref, counts, A, kb, settings)
    return out


def sample(rho, A2, rng, n=4000):
    return C.sample_counts(rho, A2, rng, n)


# --- parametric bootstrap ----------------------------------------------------------------------------------

def _boot_worker(args):
    null_rho, null_A, rho_ref, A, kb, warm, seed = args
    rng = np.random.default_rng(seed)
    c = sample(null_rho, null_A, rng)
    f = fit_pair(rho_ref, c, A, kb, rng, n=2, warm=warm)
    return float(2 * (f["cohR"].fun - f["full16R"].fun))


def bootstrap(lr_obs, theta_coh, rho_ref, A, kb, ss, warm, pool, b0=B0, b1=B1):
    null_rho, null_A = state_and_A("cohR", theta_coh, rho_ref, A)
    seeds = ss.generate_state(b1)
    args = lambda lo, hi: [(null_rho, null_A, rho_ref, A, kb, warm, int(seeds[k])) for k in range(lo, hi)]
    lrs = list(pool.map(_boot_worker, args(0, b0)))
    p = (1 + sum(x >= lr_obs for x in lrs)) / (len(lrs) + 1)
    if p <= EXTEND_AT and b1 > b0:
        lrs += list(pool.map(_boot_worker, args(b0, b1)))
        p = (1 + sum(x >= lr_obs for x in lrs)) / (len(lrs) + 1)
    return {"p": float(p), "B": len(lrs), "floor": 1 / (len(lrs) + 1), "q99": float(np.percentile(lrs, 99)),
            "max": float(max(lrs)), "null": [float(x) for x in lrs]}


# --- the verdict (section 5), from the per-pair labels ---------------------------------------------------------

def verdict(pairs: dict) -> dict:
    """pairs: {item: {"finite": bool, "B_complete": bool, "p": float}}. Returns verdict and the section 5 sentences."""
    if set(pairs) != set(ITEMS) or any(not v["finite"] or not v["B_complete"] for v in pairs.values()):
        bad = [k for k in ITEMS if k not in pairs or not pairs[k]["finite"] or not pairs[k]["B_complete"]]
        return {"verdict": "untestable", "sentences": [
            f"The refit could not be completed on {', '.join(bad)}, so this test cannot say whether readout error "
            "within three times the calibration value can stand in for the blur-type term."]}
    needed = [k for k in ITEMS if pairs[k]["p"] < ALPHA]
    not_needed = [k for k in ITEMS if k not in needed]
    S = []
    for k in ITEMS:
        if k in needed:
            S.append(f"On pair {k}, the blur-type term is still needed even when each qubit's readout error may be "
                     "up to three times its calibration value in that job: extra readout error that large cannot "
                     "stand in for it.")
        else:
            S.append(f"On pair {k}, the blur-type term is no longer needed once each qubit's readout error may be up "
                     "to three times its calibration value in that job: readout error that large can stand in for "
                     "it, so on this pair the archive cannot tell blur from misreading.")
    if not not_needed:
        S.append("Overall: on all three archived pairs (one job, 3 November), P3-5c's blur-type term survives readout "
                 "error up to three times the job's own calibration value. These are terms in a fitted model, not "
                 "identified physical mechanisms, and readout drift larger than three times the calibration value is "
                 "not excluded.")
        return {"verdict": "pass", "sentences": S, "needed": needed, "not_needed": not_needed}
    S.append(f"Overall: on {len(not_needed)} of 3 archived pairs ({', '.join(not_needed)}), readout error within "
             "three times the job's calibration value can stand in for P3-5c's blur-type term, so P3-5c's 'blur on "
             "every pair' does not stand on the archive alone. This does not show the chip was misreading; it shows "
             "the archive cannot tell the two apart on those pairs.")
    return {"verdict": "fail", "sentences": S, "needed": needed, "not_needed": not_needed}


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

def check():
    rng = np.random.default_rng(1)
    psi = np.array([1, 0, 0, 1]) / np.sqrt(2)
    ref = np.outer(psi, psi).astype(complex)
    A = C.GENERIC_A
    r = rates(A)
    print("rates of GENERIC_A [e0_i, e1_i, e0_j, e1_j]:", [round(x, 4) for x in r])
    for kind in ("primary", "knob", "3se", "wide"):
        print(f"  bounds {kind:8s}", [(round(a, 4), round(b, 4)) for a, b in bounds_for(A, kind)])
    up = [b for _, b in bounds_for(A)]
    A_up = readout(A, up)
    print("columns of A' sum to 1:", np.allclose(A_up.sum(0), 1), "| A' - A max", round(float(np.abs(A_up - A).max()), 4))
    print("rates of A' at the upper bound (should be about 3 x rates of A):", [round(x, 4) for x in rates(A_up)])
    print("rates of A' at the lower bound (should be about 0):", [round(x, 4) for x in rates(readout(A, [a for a, _ in bounds_for(A)]))])
    cnt = sample(ref, A_up, rng)
    th0 = np.zeros(11)
    th_up = np.concatenate([np.zeros(7), up])
    print("logL cohR at zero knobs vs at the true knobs:", round(ll("cohR", th0, ref, cnt, A), 2),
          round(ll("cohR", th_up, ref, cnt, A), 2))
    f = fit_pair(ref, cnt, A, bounds_for(A), rng, n=2)
    print("fitted cohR knobs on readout-only synthetic data:", [round(x, 4) for x in f["cohR"].x[7:]], "true", [round(x, 4) for x in up])
    print("LR_b on readout-only synthetic data:", round(2 * (f["cohR"].fun - f["full16R"].fun), 3))
    print("verdict() on synthetic tables:")
    for ps in ({"h221": .001, "h088": .001, "h268": .001}, {"h221": .2, "h088": .001, "h268": .001},
               {"h221": .01, "h088": .001, "h268": .001}, {"h221": .0099, "h088": .001, "h268": .5}):
        v = verdict({k: {"finite": True, "B_complete": True, "p": p} for k, p in ps.items()})
        print("  ", ps, "->", v["verdict"])
    v = verdict({"h221": {"finite": False, "B_complete": True, "p": .001}, "h088": {"finite": True, "B_complete": True, "p": .001},
                 "h268": {"finite": True, "B_complete": True, "p": .001}})
    print("   non-finite h221 ->", v["verdict"])


# --- recovery: two pre-run worlds per pair (D3, D11 / P12) -------------------------------------------------------

def recovery():
    """W_blur: truth = P3-5c's fitted full16 state through the archived A (blur really there, readout as
    calibrated). W_readout: truth = P3-5c's fitted coh state through A'(upper bound of the primary knobs) (no blur;
    readout error at 3x the calibration value). 8 draws each, 4,000 shots x 9 settings; each draw's LR_b is classified
    against the 99th percentile of one B = 100 null fitted on that world's first draw. No archived tomography counts."""
    p35 = {it["id"]: it for it in json.loads(P35C.read_text())["items"]}
    As = assignment_matrices()
    files = C.item_files()
    root = np.random.SeedSequence(20261105)
    out = {"note": recovery.__doc__, "root_seed": 20261105, "cells": {}}
    with mp.get_context("fork").Pool(11) as pool:
        for it in ITEMS:
            ref = C.reference_state(files[it])
            A = As[it]
            kb = bounds_for(A)
            th = p35[it]["theta"]
            up = [b for _, b in kb]
            worlds = {"W_blur": (C.fam_full16(np.array(th["full16"]), ref), A),
                      "W_readout": (F.fam_coherent(np.array(th["coh"]), ref), readout(A, up))}
            for w, (rho_t, A_t) in worlds.items():
                ss = root.spawn(1)[0]
                rng = np.random.default_rng(ss.generate_state(1)[0])
                lrs, knobs = [], []
                for d in range(8):
                    cnt = sample(rho_t, A_t, rng)
                    f = fit_pair(ref, cnt, A, kb, rng, n=4, plain=th["full16"])
                    lrs.append(float(2 * (f["cohR"].fun - f["full16R"].fun)))
                    knobs.append([float(x) for x in f["cohR"].x[7:]])
                    if d == 0:
                        warm = {k: v.x for k, v in f.items()}
                        bs = bootstrap(lrs[0], f["cohR"].x, ref, A, kb, ss.spawn(1)[0], warm, pool, b0=B0, b1=B0)
                needed = sum(x > bs["q99"] for x in lrs)
                out["cells"][f"{it} | {w}"] = {"LR_b": lrs, "null_q99_B100": bs["q99"], "null_max": bs["max"],
                                               "blur_still_needed": int(needed), "of": 8,
                                               "cohR_knobs_fitted": knobs, "knob_bounds": kb, "true_knobs":
                                               (up if w == "W_readout" else [0, 0, 0, 0])}
                print(it, w, "LR_b", [round(x, 1) for x in lrs], "q99", round(bs["q99"], 1), "needed", needed, "/ 8", flush=True)
                RECOVERY_OUT.write_text(json.dumps(out, indent=1))
    pb = [out["cells"][f"{it} | W_blur"]["blur_still_needed"] / 8 for it in ITEMS]
    pr = [out["cells"][f"{it} | W_readout"]["blur_still_needed"] / 8 for it in ITEMS]
    out["P_pass_W_blur"] = float(np.prod(pb))
    out["P_pass_W_readout"] = float(np.prod(pr))
    out["P_fail_W_readout"] = 1 - out["P_pass_W_readout"]
    RECOVERY_OUT.write_text(json.dumps(out, indent=1))
    print("P(pass | W_blur) =", round(out["P_pass_W_blur"], 3), " P(fail | W_readout) =", round(out["P_fail_W_readout"], 3))
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
           "k_bound": K_BOUND, "made_at_head": git("rev-parse", "--short", "HEAD"),
           "inputs_sha256": {p: hashlib.sha256((ENGINE / p).read_bytes()).hexdigest() for p in USES
                             if (ENGINE / p).is_file()}, "items": []}
    pairs = {}
    with mp.get_context("fork").Pool(11) as pool:
        for it in ITEMS:
            ref = C.reference_state(files[it])
            A, counts = As[it], counts_all[it]
            kb = bounds_for(A)
            ss_p, ss_s = root.spawn(2)
            f = fit_pair(ref, counts, A, kb, rng, with_inc=True, plain=p35[it]["theta"]["full16"])
            l = {k: -v.fun for k, v in f.items()}
            finite = all(np.isfinite(v) for v in l.values())
            lr_b = 2 * (l["full16R"] - l["cohR"])
            lr_r = 2 * (l["full16R"] - l["inc9R"])
            warm = {k: v.x for k, v in f.items()}
            bs = bootstrap(lr_b, f["cohR"].x, ref, A, kb, ss_p, warm, pool) if finite else None
            r = {"id": it, "rates": rates(A), "knob_bounds": kb, "logL": l, "LR_blur_given_rotation_readout": lr_b,
                 "LR_rotation_given_blur_readout_point": lr_r, "boot_blur": bs,
                 "label_blur": ("still needed" if bs and bs["p"] < ALPHA else "not needed"),
                 "theta": {k: v.x.tolist() for k, v in f.items()},
                 "converged": {k: bool(v.success) for k, v in f.items()},
                 "knobs_at_bound": {k: [bool(abs(x - lo) < 1e-6 or abs(x - hi) < 1e-6)
                                        for x, (lo, hi) in zip(v.x[-4:], kb)] for k, v in f.items()}}
            pairs[it] = {"finite": bool(finite), "B_complete": bool(bs and bs["B"] in (B0, B1)), "p": bs["p"] if bs else 1.0}
            # secondaries, reported, not tests
            sat = F.saturated(counts)
            dev = 2 * (sat - l["full16R"]); df = 27 - 20
            r["goodness_of_fit"] = {"deviance": dev, "df": df, "chi2_q99": float(chi2.ppf(0.99, df)),
                                    "misfit": bool(dev > chi2.ppf(0.99, df)),
                                    "LR_b_scaled_by_overdispersion": lr_b / max(1.0, dev / df)}
            psl = {k: C.per_setting_ll(*state_and_A(k, f[k].x, ref, A), counts) for k in ("cohR", "full16R")}
            contrib = {s: 2 * (psl["full16R"][s] - psl["cohR"][s]) for s in SETTINGS}
            top = max(contrib, key=contrib.get)
            r["setting_shares"] = {"per_setting": contrib, "top_setting": top,
                                   "top_share": contrib[top] / lr_b if lr_b > 0 else None}
            sec = {}
            for kind in ("knob", "3se", "wide"):
                kb2 = bounds_for(A, kind)
                f2 = fit_pair(ref, counts, A, kb2, rng, warm={k: np.concatenate([v.x[:-4], np.clip(v.x[-4:], [a for a, _ in kb2], [b for _, b in kb2])])
                                                              for k, v in f.items() if k != "inc9R"},
                              plain=p35[it]["theta"]["full16"])
                sec[kind] = {"bounds": kb2, "LR_b_point": float(2 * (f2["cohR"].fun - f2["full16R"].fun)),
                             "cohR_knobs": f2["cohR"].x[7:].tolist(),
                             "note": "point fit only; compared with the primary null's 99th percentile, not a test"}
            r["secondary_bounds"] = sec
            r["P3_5c_LR_blur_given_rotation"] = p35[it]["LR_blur_given_rotation"]
            out["items"].append(r)
            OUT.write_text(json.dumps(out, indent=1))
            print(it, "LR_b", round(lr_b, 2), "p", bs and bs["p"], "B", bs and bs["B"], "q99", bs and round(bs["q99"], 2),
                  "label", r["label_blur"], "| secondary LR_b", {k: round(v["LR_b_point"], 2) for k, v in sec.items()}, flush=True)
    v = verdict(pairs)
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

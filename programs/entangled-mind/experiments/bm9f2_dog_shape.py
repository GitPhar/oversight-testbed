"""bm9-f2 (bet em-bm9f2): does the pull of Haiku's main rating toward the sub-rating it just gave have the human
serial-dependence shape (largest at middling gaps, smaller at large ones)? Pre-registered in experiments/bm9f2-dog-shape.md.
Archive only (em-bm9's pairs from results/exp5-conversations.json, anchor (a)); no API calls; $0.

    python experiments/bm9f2_dog_shape.py --selftest                 # synthetic data; never opens the archive
    python experiments/bm9f2_dog_shape.py --power <sigma> [--L-from-archive]   # design-review power check
    python experiments/bm9f2_dog_shape.py --seed <bootstrap seed>      # the run (seed from the beacon)

Per pair (bm_offline.bm9_pairs, unchanged): d = mean M after S - mean M asked first; L = mean S - mean M-first (the gap);
C = the claim's content push. Three models, each with intercept a and content term c*C, fitted by least squares:
  linear  f(L) = b*L                                  (k = 3 mean parameters)
  DoG     f(L) = A*L*exp(-(L/w)^2)                    (k = 4: a, c, A, w)  peak of the pull at |L| = w/sqrt(2)
  tanh    f(L) = A*w*tanh(L/w)                        (k = 4: a, c, A, w)  monotone saturation, same parameter count
w is profiled on a fixed log grid W_GRID (A, a, c by least squares at each w). AIC = n*log(RSS/n) + 2*(k+1).
Writes results/bm9f2-dog-shape.{json,md}.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))
sys.path.insert(0, str(HERE))

import numpy as np

W_GRID = np.exp(np.linspace(np.log(3.0), np.log(400.0), 400))
DAIC_LIN, DAIC_TANH, TOL, NBOOT, MIN_PAIRS = 4.0, 2.0, 1e-9, 10000, 60


def ls(X, y):
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ beta
    return beta, float(r @ r)


def fit_linear(d, L, C):
    X = np.column_stack([np.ones(len(d)), C, L])
    beta, rss = ls(X, d)
    return {"rss": rss, "k": 3, "b": float(beta[2])}


def fit_shape(d, L, C, kind):
    best = None
    for w in W_GRID:
        g = L * np.exp(-(L / w) ** 2) if kind == "dog" else w * np.tanh(L / w)
        X = np.column_stack([np.ones(len(d)), C, g])
        beta, rss = ls(X, d)
        if best is None or rss < best["rss"]:
            best = {"rss": rss, "k": 4, "A": float(beta[2]), "w": float(w)}
    return best


def aic(m, n):
    return n * np.log(max(m["rss"], 1e-300) / n) + 2 * (m["k"] + 1)


def fit_all(d, L, C):
    n = len(d)
    lin, dog, tnh = fit_linear(d, L, C), fit_shape(d, L, C, "dog"), fit_shape(d, L, C, "tanh")
    a_lin, a_dog, a_tnh = aic(lin, n), aic(dog, n), aic(tnh, n)
    peak = dog["w"] / np.sqrt(2)
    return {"n": n, "linear": lin, "dog": dog, "tanh": tnh, "dAIC_dog_vs_linear": float(a_lin - a_dog),
            "dAIC_dog_vs_tanh": float(a_tnh - a_dog), "dog_peak_abs_L": float(peak),
            "abs_L_range": [float(np.abs(L).min()), float(np.abs(L).max())],
            "dog_w_at_grid_edge": bool(dog["w"] >= W_GRID[-1] - TOL or dog["w"] <= W_GRID[0] + TOL)}


def verdict(r):
    if r["n"] < MIN_PAIRS:
        return "untestable"
    lo, hi = r["abs_L_range"]
    inside = lo + TOL < r["dog_peak_abs_L"] < hi - TOL
    if r["dAIC_dog_vs_linear"] >= DAIC_LIN - TOL and r["dAIC_dog_vs_tanh"] >= DAIC_TANH - TOL and inside and r["dog"]["A"] > 0:
        return "pass"
    return "fail"


SENTENCES = {
    "pass": "On Haiku's 80 archived sub-question and main-question pairs, the pull of the main rating toward the sub-rating just given was best described by the human serial-dependence shape: it grew with the gap up to a peak inside the observed gaps and then shrank, beating both a straight-line pull and an equally flexible pull that only levels off.",
    "fail": "On Haiku's 80 archived pairs, the pull of the main rating toward the sub-rating just given was not shown to have the human serial-dependence shape, by the pre-registered rule; a straight-line or levelling-off pull describes it as well.",
    "untestable": "Too few pairs were usable to read the rule.",
}


def analyse(d, L, C, items, seed, nboot=NBOOT):
    r = fit_all(d, L, C)
    r["verdict"] = verdict(r)
    labs = sorted(set(items))
    idx = {q: np.array([i for i, x in enumerate(items) if x == q]) for q in labs}
    rng = np.random.default_rng(seed % 2**63)
    B = []
    for _ in range(nboot):
        s = np.concatenate([idx[labs[j]] for j in rng.integers(0, len(labs), len(labs))])
        f = fit_all(d[s], L[s], C[s])
        B.append((f["dAIC_dog_vs_linear"], f["dAIC_dog_vs_tanh"], verdict(f) == "pass"))
    B = np.array(B, float)
    r["boot_dAIC_dog_vs_linear_95"] = [float(np.percentile(B[:, 0], 2.5)), float(np.percentile(B[:, 0], 97.5))]
    r["boot_dAIC_dog_vs_tanh_95"] = [float(np.percentile(B[:, 1], 2.5)), float(np.percentile(B[:, 1], 97.5))]
    r["boot_share_pass"] = float(B[:, 2].mean())
    flips = []
    for q in labs:
        keep = np.array([i for i in range(len(d)) if items[i] != q])
        if verdict(fit_all(d[keep], L[keep], C[keep])) != r["verdict"]:
            flips.append(q)
    r["loo_item_flips"] = flips
    r["sentence"] = SENTENCES[r["verdict"]]
    return r


def simulate(L, C, items, sigma, world, rng):
    a, c = -5.0, 7.7
    if world == "linear":
        f = 0.27 * L
    elif world == "tanh":
        f = 0.40 * 25 * np.tanh(L / 25)
    else:                                     # human-like DoG with peak at |L| = 20
        f = 0.9 * L * np.exp(-(L / 28.3) ** 2)
    return a + c * C + f + rng.normal(0, sigma, len(L))


def power(L, C, items, sigma, nsim=300, seed=1):
    rng = np.random.default_rng(seed)
    out = {}
    for world in ("dog", "linear", "tanh"):
        out[world] = float(np.mean([verdict(fit_all(simulate(L, C, items, sigma, world, rng), L, C)) == "pass" for _ in range(nsim)]))
    return out


def selftest():
    rng = np.random.default_rng(2)
    n = 80
    items = [f"i{i // 2}" for i in range(n)]
    L = rng.uniform(-70, 70, n)
    C = rng.uniform(-1, 1, n)
    ok = True
    for world, want in (("dog", "pass"), ("linear", "fail"), ("tanh", "fail")):
        d = simulate(L, C, items, 2.0, world, rng)
        r = analyse(d, L, C, items, 3, nboot=200)
        print(f"{world} world, sigma 2: dAIC vs linear {r['dAIC_dog_vs_linear']:+.1f}, vs tanh {r['dAIC_dog_vs_tanh']:+.1f}, "
              f"peak |L| {r['dog_peak_abs_L']:.1f} -> {r['verdict']} (want {want})")
        ok &= r["verdict"] == want
    p = power(L, C, items, 8.0, nsim=100)
    print(f"power at sigma 8 (uniform L in +/-70): P(pass) dog {p['dog']:.2f}, linear {p['linear']:.2f}, tanh {p['tanh']:.2f}")
    base = {"n": 80, "abs_L_range": [0.0, 60.0], "dog_peak_abs_L": 20.0, "dog": {"A": 1.0}, "dAIC_dog_vs_linear": 4.0, "dAIC_dog_vs_tanh": 2.0}
    assert verdict(base) == "pass"
    assert verdict({**base, "dAIC_dog_vs_linear": 3.999}) == "fail" and verdict({**base, "dAIC_dog_vs_tanh": 1.999}) == "fail"
    assert verdict({**base, "dog_peak_abs_L": 60.0}) == "fail" and verdict({**base, "dog": {"A": -1.0}}) == "fail"
    assert verdict({**base, "n": 59}) == "untestable"
    print("boundary checks ok")
    print("SELFTEST", "OK" if ok else "FAILED")
    return ok


def load():
    import exp5_run as er
    import bm_offline as bo
    split = json.loads(er.SPLIT.read_text())
    recs = {r["id"]: r for r in json.loads(er.POOL.read_text())["records"]}
    pairs = bo.bm9_pairs(json.loads(bo.CONV1.read_text()), split["candidates"], split, recs, er.R_QQ, True)
    items, rows = [], []
    for q, arr in pairs.items():
        for row in arr:
            items.append(q); rows.append(row)
    A = np.array(rows, float)
    sha = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in (bo.CONV1, er.SPLIT, er.POOL)}
    return A[:, 0], A[:, 1], A[:, 2], items, sha


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--power", type=float, help="residual SD for the power check")
    ap.add_argument("--L-from-archive", action="store_true", help="use the archive's gaps L and content C (no outcome d is read)")
    ap.add_argument("--seed", type=int)
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(0 if selftest() else 1)
    if a.power is not None:
        if a.L_from_archive:
            _, L, C, items, _ = load()
        else:
            rng = np.random.default_rng(4); L = rng.uniform(-70, 70, 80); C = rng.uniform(-1, 1, 80); items = [f"i{i // 2}" for i in range(80)]
        print(json.dumps(power(np.asarray(L), np.asarray(C), items, a.power)))
        return
    if a.seed is None:
        raise SystemExit("--seed (the beacon's bootstrap seed) is required for the run")
    d, L, C, items, sha = load()
    r = analyse(d, L, C, items, a.seed)
    r.update(seed=a.seed, archive_sha256=sha)
    from entangled_mind import config
    (config.RESULTS / "bm9f2-dog-shape.json").write_text(json.dumps(r, indent=1, default=float))
    f = lambda x: f"{x:+.2f}"
    Ls = ["# bm9-f2: does the pull toward the last rating have the human serial-dependence shape? (Haiku, archive)", "",
          "Pre-registered in `experiments/bm9f2-dog-shape.md`. Archive only (em-bm9's run-1 pairs); $0.", "",
          "## In plain English", "", "(Hand-written after the run; excluded from reproduce.py's comparison.)", "",
          "## Fits (d = a + c·C + f(L))", "",
          "| model | f(L) | RSS | key parameters |", "|---|---|---|---|",
          f"| linear | b·L | {r['linear']['rss']:.1f} | b = {r['linear']['b']:+.3f} |",
          f"| DoG | A·L·exp(−(L/w)²) | {r['dog']['rss']:.1f} | A = {r['dog']['A']:+.3f}, w = {r['dog']['w']:.1f} (peak at abs(L) = {r['dog_peak_abs_L']:.1f}) |",
          f"| tanh | A·w·tanh(L/w) | {r['tanh']['rss']:.1f} | A = {r['tanh']['A']:+.3f}, w = {r['tanh']['w']:.1f} |", "",
          f"- n = {r['n']} pairs; observed abs(L) from {r['abs_L_range'][0]:.1f} to {r['abs_L_range'][1]:.1f}; DoG w at the grid's edge: {r['dog_w_at_grid_edge']}.",
          f"- **ΔAIC, DoG vs linear: {f(r['dAIC_dog_vs_linear'])}** (needs ≥ +4); item-cluster bootstrap 95% [{f(r['boot_dAIC_dog_vs_linear_95'][0])}, {f(r['boot_dAIC_dog_vs_linear_95'][1])}].",
          f"- **ΔAIC, DoG vs tanh: {f(r['dAIC_dog_vs_tanh'])}** (needs ≥ +2); bootstrap 95% [{f(r['boot_dAIC_dog_vs_tanh_95'][0])}, {f(r['boot_dAIC_dog_vs_tanh_95'][1])}].",
          f"- Share of bootstrap resamples that pass: {r['boot_share_pass']:.3f}. Items whose removal flips the verdict: {', '.join(r['loo_item_flips']) or 'none'}.",
          "- Archive sha256: " + "; ".join(f"`{k}` {v[:16]}" for k, v in sha.items()) + ".",
          "", f"## Pre-registered reading: **{r['verdict']}**", "", r["sentence"]]
    (config.RESULTS / "bm9f2-dog-shape.md").write_text("\n".join(Ls) + "\n")
    print("\n".join(Ls))


if __name__ == "__main__":
    main()

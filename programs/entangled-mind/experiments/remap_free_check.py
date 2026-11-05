"""Free-direction check before pre-registration (2026-11-05): can g-f2's event pass at the n the archive holds?

Uses only numbers already published in results/calibration-under-format.md (n parsed and accuracy per
conversation cell, and each cell's AUROC). It never opens the archive. For each model and format it simulates
the two orders with the SAME true AUROC (the most favourable world for g-f2's equivalence event), draws a
question bootstrap of the AUROC difference, and counts how often g-f2's event (|difference| < 0.05 and the
95% interval inside +/-0.08, on every model) would be met. Fixed seed 20261105; no beacon (no data is split).

    python3 programs/entangled-mind/experiments/remap_free_check.py
"""
import numpy as np

CELLS = {  # (n, accuracy, AUROC) for forward and reversed conversation cells, from the published table
    ("haiku", "P"): ((108, 0.630, 0.578), (121, 0.678, 0.546)),
    ("haiku", "F"): ((191, 0.639, 0.569), (197, 0.690, 0.611)),
    ("sonnet", "P"): ((68, 0.941, 0.748), (80, 0.875, 0.662)),
    ("sonnet", "F"): ((112, 0.795, 0.861), (118, 0.839, 0.843)),
}


def auroc(s, y):
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    gt = (pos[:, None] > neg[None, :]).mean()
    eq = (pos[:, None] == neg[None, :]).mean()
    return gt + 0.5 * eq


def sim_cell(rng, n, acc, a):
    y = (rng.random(n) > acc).astype(int)            # 1 = error
    d = np.sqrt(2) * __import__("scipy.stats", fromlist=["norm"]).norm.ppf(a)
    s = rng.normal(0, 1, n) + d * y                  # binormal score with true AUROC a
    return s, y


def main():
    rng = np.random.default_rng(20261105)
    sims, boots = 300, 400
    ok_all = 0
    width = {k: [] for k in CELLS}
    for _ in range(sims):
        ok = True
        for k, (fw, rv) in CELLS.items():
            a = 0.5 * (fw[2] + rv[2])                # same true AUROC in both orders
            s1, y1 = sim_cell(rng, fw[0], fw[1], a)
            s2, y2 = sim_cell(rng, rv[0], rv[1], a)
            diff = auroc(s2, y2) - auroc(s1, y1)
            bd = []
            for _ in range(boots):
                i1 = rng.integers(0, fw[0], fw[0]); i2 = rng.integers(0, rv[0], rv[0])
                bd.append(auroc(s2[i2], y2[i2]) - auroc(s1[i1], y1[i1]))
            lo, hi = np.nanpercentile(bd, [2.5, 97.5])
            width[k].append(hi - lo)
            if not (abs(diff) < 0.05 and lo > -0.08 and hi < 0.08):
                ok = False
        ok_all += ok
    print(f"g-f2 event met in {ok_all}/{sims} simulated runs with no true order effect (most favourable world)")
    for k, w in width.items():
        print(f"  {k}: median 95% interval width of the order difference {np.median(w):.3f} (event needs < 0.16)")


if __name__ == "__main__":
    main()

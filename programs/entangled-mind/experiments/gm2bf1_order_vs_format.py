"""gm2b-f1 (bet em-gm2bf1): do the claims whose ratings move most with question order also move most with answer
format? Pre-registered in experiments/gm2bf1-order-vs-format.md. Archive only; no API calls; $0. Haiku.

    python experiments/gm2bf1_order_vs_format.py --selftest          # synthetic data; never opens the archive
    python experiments/gm2bf1_order_vs_format.py --seed <bootstrap>    # the run (seed from the beacon)

Reads:
- results/gm2-conversations.json (10 items) and results/gm2b-conversations.json (30 items): keys <item>|O1..O4|shown|<rep>,
  turns of kind "S" (claim id, rating 0-100). Only the "shown" condition, orders O1-O4, S turns. ("redacted" S turns are
  read for a secondary only.)
- results/gm3b-calls.json (Haiku, six formats): keys <item>|<claim>|<F1..F6>|<rep>, field value, decoded by
  gm3b_format_invariance.encode / observed_scale exactly as em-gm3b and em-gm3c did.
- experiments/split-exp5.json: the 40 items and their four chain claims.
Writes results/gm2bf1-order-vs-format.{json,md}.

Per claim (160):
- order span S = max - min over the four orders of the claim's mean S rating (10 conversations per order, shown);
- within-order SD W = the pooled within-order SD of those ratings (noise covariate);
- format spread G = SD over the six formats of the claim's percentile rank among the 160 claims, where each format's
  per-claim mean is on its observed scale (rank is invariant to each format's monotone scale);
- extremity E = |mean 0-100 rating (format F1) - 50|.
Primary: Spearman rho(S, G). Guard (P3, P8): partial Spearman of S and G controlling for E and W (Pearson partial
correlation of the ranks). Item-cluster bootstrap (40 items carrying their claims; P14).
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
from scipy.stats import rankdata

RHO_BAR, TOL, NBOOT, MIN_CLAIMS = 0.30, 1e-9, 10000, 120
ORDERS = ["O1", "O2", "O3", "O4"]
RESULTS = HERE.parent / "results"


def ranks(x):
    return rankdata(x) / len(x)


def spearman(a, b):
    return float(np.corrcoef(rankdata(a), rankdata(b))[0, 1])


def partial_spearman(a, b, covs):
    """Partial correlation of rank(a) and rank(b) given the ranks of covs (OLS residuals)."""
    Z = np.column_stack([np.ones(len(a))] + [rankdata(c) for c in covs])
    ra, rb = rankdata(a), rankdata(b)
    ea = ra - Z @ np.linalg.lstsq(Z, ra, rcond=None)[0]
    eb = rb - Z @ np.linalg.lstsq(Z, rb, rcond=None)[0]
    return float(np.corrcoef(ea, eb)[0, 1])


def order_measures(conv, claims, cond="shown"):
    """claims: list of (item, claim). Returns S (span) and W (pooled within-order SD), NaN if a cell is missing."""
    S, W = np.full(len(claims), np.nan), np.full(len(claims), np.nan)
    for i, (q, k) in enumerate(claims):
        per = []
        for o in ORDERS:
            vals = []
            for r in range(40):
                v = conv.get(f"{q}|{o}|{cond}|{r}")
                if v is None:
                    continue
                for t in v["turns"]:
                    if t["kind"] == "S" and t["claim"] == k and t.get("rating") is not None:
                        vals.append(float(t["rating"]))
            per.append(vals)
        if all(len(v) >= 2 for v in per):
            means = [np.mean(v) for v in per]
            S[i] = max(means) - min(means)
            W[i] = float(np.sqrt(np.mean([np.var(v, ddof=1) for v in per])))
    return S, W


def format_measures(fmt_means, f1_means):
    """fmt_means: (n_claims, 6) per-claim means on each format's observed scale. Returns G and E."""
    R = np.column_stack([ranks(fmt_means[:, j]) for j in range(fmt_means.shape[1])])
    G = R.std(axis=1, ddof=1)
    E = np.abs(f1_means - 50.0)
    return G, E


def stats(S, G, E, W, idx):
    return spearman(S[idx], G[idx]), partial_spearman(S[idx], G[idx], [E[idx], W[idx]])


def verdict(n, rho, rho_lo, prho_lo):
    if n < MIN_CLAIMS:
        return "untestable"
    if rho >= RHO_BAR - TOL and rho_lo > 0 + TOL and prho_lo > 0 + TOL:
        return "pass"
    return "fail"


SENTENCES = {
    "pass": "On Haiku's 160 deliberation claims, the claims whose rating moved most with question order were also the ones whose position moved most across answer formats, and this held after allowing for how extreme the claim's rating was and how noisy its ratings were.",
    "fail": "On Haiku's 160 deliberation claims, the claims that moved most with question order were not shown to be the ones that moved most across answer formats, by the pre-registered rule.",
    "untestable": "Too few claims had complete order and format data to read the rule.",
}


def analyse(S, G, E, W, items_of, seed, nboot=NBOOT):
    ok = ~(np.isnan(S) | np.isnan(G) | np.isnan(E) | np.isnan(W))
    idx_all = np.where(ok)[0]
    n = len(idx_all)
    res = {"n_claims": n}
    if n < 10:
        res.update(verdict="untestable", sentence=SENTENCES["untestable"])
        return res
    rho, prho = stats(S, G, E, W, idx_all)
    items = sorted({items_of[i] for i in idx_all})
    by_item = {it: np.array([i for i in idx_all if items_of[i] == it]) for it in items}
    rng = np.random.default_rng(seed % 2**63)
    B = np.array([stats(S, G, E, W, np.concatenate([by_item[items[j]] for j in rng.integers(0, len(items), len(items))]))
                  for _ in range(nboot)])
    lo, hi = np.percentile(B, 2.5, axis=0), np.percentile(B, 97.5, axis=0)
    v = verdict(n, rho, lo[0], lo[1])
    # leave-one-item-out (P10): does dropping one item's claims flip the label (bounds held)?
    flips = []
    for it in items:
        keep = np.array([i for i in idx_all if items_of[i] != it])
        r1, p1 = stats(S, G, E, W, keep)
        if verdict(n, r1, lo[0] + (r1 - rho), lo[1] + (p1 - prho)) != v:
            flips.append(it)
    res.update(rho=rho, rho_ci=[float(lo[0]), float(hi[0])], partial_rho=prho, partial_rho_ci=[float(lo[1]), float(hi[1])],
               n_items=len(items), rho_S_E=spearman(S[idx_all], E[idx_all]), rho_G_E=spearman(G[idx_all], E[idx_all]),
               rho_S_W=spearman(S[idx_all], W[idx_all]), rho_G_W=spearman(G[idx_all], W[idx_all]),
               loo_item_flips=flips, verdict=v, sentence=SENTENCES[v])
    return res


def selftest():
    rng = np.random.default_rng(5)
    n, ok = 160, True
    items_of = [f"i{i // 4}" for i in range(n)]
    ext = rng.uniform(0, 50, n)                                   # extremity
    W = 3 + 0.2 * (50 - ext) + rng.normal(0, 1, n)                # noisier mid-scale
    u = rng.normal(0, 1, n)                                       # a claim-level "instability" trait
    worlds = {
        "shared instability beyond extremity": (5 + 0.3 * (50 - ext) + 6 * u + rng.normal(0, 3, n), 0.10 + 0.002 * (50 - ext) + 0.06 * u + rng.normal(0, .02, n), "pass"),
        "both driven by extremity only": (5 + 0.3 * (50 - ext) + rng.normal(0, 3, n), 0.10 + 0.002 * (50 - ext) + rng.normal(0, .02, n), "fail"),
        "unrelated": (rng.normal(10, 4, n), rng.normal(0.15, .04, n), "fail"),
    }
    for name, (S, G, want) in worlds.items():
        r = analyse(S, G, ext, W, items_of, 9, nboot=1000)
        print(f"{name}: rho {r['rho']:+.2f} [{r['rho_ci'][0]:+.2f}, {r['rho_ci'][1]:+.2f}] partial {r['partial_rho']:+.2f} "
              f"[{r['partial_rho_ci'][0]:+.2f}, {r['partial_rho_ci'][1]:+.2f}] -> {r['verdict']} (want {want})")
        ok &= r["verdict"] == want
    # boundaries (P13)
    assert verdict(160, 0.30, 0.01, 0.01) == "pass" and verdict(160, 0.2999, 0.01, 0.01) == "fail"
    assert verdict(160, 0.5, 0.0, 0.01) == "fail" and verdict(160, 0.5, 0.01, 0.0) == "fail" and verdict(119, 0.9, .5, .5) == "untestable"
    # format spread is invariant to a monotone rescaling of one format
    fm = rng.normal(0, 1, (50, 6)); g1, _ = format_measures(fm, np.full(50, 50.0)); fm2 = fm.copy(); fm2[:, 2] = np.exp(fm2[:, 2])
    g2, _ = format_measures(fm2, np.full(50, 50.0)); assert np.allclose(g1, g2)
    # order span from a tiny synthetic conversation set
    conv = {f"q|{o}|shown|{r}": {"turns": [{"kind": "S", "claim": 3, "rating": 10 * j + r % 2}]} for j, o in enumerate(ORDERS) for r in range(4)}
    S, W = order_measures(conv, [("q", 3)]); assert abs(S[0] - 30) < 1e-9, S
    print("boundary and measure checks ok")
    print("SELFTEST", "OK" if ok else "FAILED")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--seed", type=int)
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(0 if selftest() else 1)
    if a.seed is None:
        raise SystemExit("--seed (the beacon's bootstrap seed) is required for the run")
    import gm3b_format_invariance as g
    import gm3c_heldout_format as h
    files = ["gm2-conversations.json", "gm2b-conversations.json", "gm3b-calls.json"]
    sha = {f: hashlib.sha256((RESULTS / f).read_bytes()).hexdigest() for f in files}
    conv = {}
    for f in files[:2]:
        conv.update(json.loads((RESULTS / f).read_text()))
    cl = g.claims()
    S, W = order_measures(conv, cl, "shown")
    Sr, _ = order_measures(conv, cl, "redacted")
    obs, nc = g.encode(json.loads((RESULTS / files[2]).read_text()))
    fm = np.column_stack([h.claim_means(h.observed_scale(f, obs[f]), obs[f]["c"], nc) for f in g.FORMATS])
    G, E = format_measures(fm, fm[:, 0])
    items_of = [q for q, _ in cl]
    r = analyse(S, G, E, W, items_of, a.seed)
    rr = analyse(Sr, G, E, W, items_of, a.seed + 1)            # secondary: order span with earlier answers hidden
    out = {"seed": a.seed, "archive_sha256": sha, "primary": r,
           "secondary_redacted": {k: rr.get(k) for k in ("n_claims", "rho", "rho_ci", "partial_rho", "partial_rho_ci")},
           "median_order_span": float(np.nanmedian(S)), "median_format_spread": float(np.nanmedian(G))}
    (RESULTS / "gm2bf1-order-vs-format.json").write_text(json.dumps(out, indent=1, default=float))
    L = ["# gm2b-f1: do claims that move with question order also move with answer format? (Haiku, archive)", "",
         "Pre-registered in `experiments/gm2bf1-order-vs-format.md`. Archive only; $0.", "",
             "## In plain English", "", "(Hand-written after the run; excluded from reproduce.py's comparison.)", "",
         "| claims | Spearman ρ(order span, format spread) [95%] | partial ρ given extremity and noise [95%] | verdict |", "|---|---|---|---|"]
    if "rho" in r:
        L.append(f"| {r['n_claims']} ({r['n_items']} items) | {r['rho']:+.3f} [{r['rho_ci'][0]:+.3f}, {r['rho_ci'][1]:+.3f}] | "
                 f"{r['partial_rho']:+.3f} [{r['partial_rho_ci'][0]:+.3f}, {r['partial_rho_ci'][1]:+.3f}] | {r['verdict']} |")
        L += ["", "Secondary (cannot change the verdict):", "",
              f"- Order span vs extremity ρ {r['rho_S_E']:+.3f}; format spread vs extremity ρ {r['rho_G_E']:+.3f}; "
              f"order span vs within-order SD ρ {r['rho_S_W']:+.3f}; format spread vs within-order SD ρ {r['rho_G_W']:+.3f}.",
              f"- With earlier answers hidden (redacted): ρ {rr.get('rho', float('nan')):+.3f}, partial {rr.get('partial_rho', float('nan')):+.3f}.",
              f"- Median order span {out['median_order_span']:.1f} points; median format spread {out['median_format_spread']:.3f} (rank units).",
              f"- Items whose removal flips the verdict: {', '.join(r['loo_item_flips']) or 'none'}.",
              "- Archive sha256: " + "; ".join(f"`{k}` {v[:16]}" for k, v in sha.items()) + "."]
    L += ["", f"## Pre-registered reading: **{r['verdict']}**", "", r["sentence"]]
    (RESULTS / "gm2bf1-order-vs-format.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()

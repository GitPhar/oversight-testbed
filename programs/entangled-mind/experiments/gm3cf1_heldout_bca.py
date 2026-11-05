"""gm3c-f1 (bet em-gm3cf1): re-test of em-gm3c's borderline label. Can Haiku's answer in one elicitation format be
recovered from its answers in the other five? Pre-registered in experiments/gm3cf1-heldout-bca.md.
Archive only (results/gm3b-calls.json, Haiku, 160 claims x 6 formats x 10 repeats); no API calls; $0.

    python experiments/gm3cf1_heldout_bca.py --selftest                       # synthetic data; never opens the archive
    python experiments/gm3cf1_heldout_bca.py --fold-seed <s> --boot-seed <s>    # the run (seeds from the beacon)

Differences from em-gm3c (experiments/gm3c_heldout_format.py, whose prediction step is reused unchanged):
- the one-credence fit runs to convergence: gm3b's block ascent, copied, stopping when the objective changes by less
  than FIT_TOL = 1e-3 log-likelihood units between rounds (gm3b capped it at 40 rounds), up to MAX_ROUNDS; fits that
  hit the cap are counted and reported;
- per-claim predictions are averaged over K_ASSIGN item-to-fold assignments drawn from the beacon seed, not one;
- the interval is BCa (bias-corrected and accelerated; acceleration from the leave-one-item-out jackknife) from
  NBOOT item-cluster resamples;
- a link-free predictor (least squares from the other five formats' even-repeat claim means, same folds) is the
  dumb baseline, and must also recover under 0.5 for a pass.
Writes results/gm3cf1-heldout-bca.{json,md}.
"""
import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))      # this checkout's entangled_mind, never the old folder's
sys.path.insert(0, str(HERE))

import numpy as np
from scipy.stats import norm

from entangled_mind import config                  # noqa: E402

assert Path(config.RESULTS).resolve() == (HERE.parent / "results").resolve(), f"config.RESULTS points at {config.RESULTS}"

import gm3b_format_invariance as g                  # noqa: E402
import gm3c_heldout_format as h                     # noqa: E402

K_ASSIGN, N_FOLDS, MAX_ROUNDS, NBOOT = 10, 5, 2000, 10000
FIT_TOL = 1e-3
BAR, TOL = 0.50, 1e-9
MAX_UNCONVERGED_SHARE = 0.10                        # more fits at the cap than this -> untestable


def fit_tol(obs, n_claims, mask_fn, counter):
    """gm3b's block coordinate ascent for the one-credence model (g.fit with single=True), copied unchanged except the
    stop rule: |change in objective| < FIT_TOL (log-likelihood units, summed over ~4,800 observations) or MAX_ROUNDS.
    Counts fits that stop at the cap."""
    tr = {f: g.subset(d, mask_fn(d)) for f, d in obs.items()}
    mu = np.zeros(n_claims)
    theta = g.theta0()

    def objective(th, m):
        p = g.unpack(th, True)
        return sum(g.ll_obs(f, p[f], m[tr[f]["c"]], tr[f]).sum() for f in g.FORMATS) - 0.5 * (m ** 2).sum() / g.PRIOR_SD ** 2

    def mu_step(th, m):
        p = g.unpack(th, True)
        lo, hi = np.full(m.shape, -15.0), np.full(m.shape, 15.0)
        gr = (5 ** 0.5 - 1) / 2

        def per_unit(x):
            tot = np.zeros(m.shape)
            for f in g.FORMATS:
                d = tr[f]
                if len(d["c"]):
                    np.add.at(tot, d["c"], g.ll_obs(f, p[f], x[d["c"]], d))
            return tot - 0.5 * x ** 2 / g.PRIOR_SD ** 2
        c1, c2 = hi - gr * (hi - lo), lo + gr * (hi - lo)
        f1, f2 = per_unit(c1), per_unit(c2)
        for _ in range(70):
            left = f1 > f2
            hi = np.where(left, c2, hi)
            lo = np.where(left, lo, c1)
            c2n = np.where(left, c1, lo + gr * (hi - lo))
            c1n = np.where(left, hi - gr * (hi - lo), c2)
            c1, c2 = c1n, c2n
            f1, f2 = per_unit(c1), per_unit(c2)
        return (lo + hi) / 2

    prev, n, converged = -np.inf, 0, False
    for n in range(1, MAX_ROUNDS + 1):
        mu = mu_step(theta, mu)
        theta = g.minimize(lambda th: -objective(th, mu), theta, method="L-BFGS-B").x
        cur = objective(theta, mu)
        if abs(cur - prev) < FIT_TOL:
            converged = True
            break
        prev = cur
    counter["fits"] += 1
    counter["capped"] += not converged
    counter["max_rounds_used"] = max(counter["max_rounds_used"], n)
    return theta, mu


def assignments(items, fold_seed, k=K_ASSIGN):
    out = []
    for j in range(k):
        order = list(items)
        np.random.default_rng([fold_seed % 2**63, j]).shuffle(order)
        out.append({q: i * N_FOLDS // len(order) for i, q in enumerate(order)})
    return out


def predictions(obs, nc, cl, assigns, counter):
    """Per format, per claim: L1 predictions and link-free predictions averaged over the assignments."""
    pred = {f: np.zeros(nc) for f in g.FORMATS}
    lin = {f: np.zeros(nc) for f in g.FORMATS}
    cnt = {f: np.zeros(nc) for f in g.FORMATS}
    even_means = {f: h.claim_means(h.observed_scale(f, obs[f])[obs[f]["r"] % 2 == 0], obs[f]["c"][obs[f]["r"] % 2 == 0], nc)
                  for f in g.FORMATS}
    odd_means = {f: h.claim_means(h.observed_scale(f, obs[f])[obs[f]["r"] % 2 == 1], obs[f]["c"][obs[f]["r"] % 2 == 1], nc)
                 for f in g.FORMATS}
    for fold_of_item in assigns:
        fold = np.array([fold_of_item[q] for q, _ in cl])
        for f in g.FORMATS:
            others = [ff for ff in g.FORMATS if ff != f]
            Xo = np.column_stack([even_means[ff] for ff in others])
            for k in range(N_FOLDS):
                test = fold == k
                mod = {}
                for ff, d in obs.items():
                    keep = ~test[d["c"]] if ff == f else np.ones(len(d["c"]), bool)
                    mod[ff] = g.subset(d, keep)
                theta, mu = fit_tol(mod, nc, lambda d: d["r"] % 2 == 0, counter)
                p = g.unpack(theta, True)[f]
                d = g.subset(obs[f], test[obs[f]["c"]] & (obs[f]["r"] % 2 == 1))
                pm = h.claim_means(h.predicted_obs(f, p, mu[d["c"]], d), d["c"], nc)
                ok = test & ~np.isnan(pm)
                pred[f][ok] += pm[ok]
                cnt[f][ok] += 1
                # link-free baseline: least squares on training claims (target: the format's odd-repeat means)
                tr = ~test & ~np.isnan(odd_means[f]) & ~np.isnan(Xo).any(1)
                A = np.column_stack([np.ones(tr.sum()), Xo[tr]])
                beta = np.linalg.lstsq(A, odd_means[f][tr], rcond=None)[0]
                te = test & ~np.isnan(Xo).any(1)
                lin[f][te] += np.column_stack([np.ones(te.sum()), Xo[te]]) @ beta
    out_p, out_l = {}, {}
    for f in g.FORMATS:
        with np.errstate(invalid="ignore", divide="ignore"):
            out_p[f] = np.where(cnt[f] > 0, pred[f] / cnt[f], np.nan)
            out_l[f] = np.where(cnt[f] > 0, lin[f] / cnt[f], np.nan)
    return out_p, out_l, odd_means, even_means


def mean_q(pred, target, ceil, idx):
    qs = []
    for f in g.FORMATS:
        ok = idx[~np.isnan(pred[f][idx]) & ~np.isnan(target[f][idx]) & ~np.isnan(ceil[f][idx])]
        rc = np.corrcoef(pred[f][ok], target[f][ok])[0, 1] ** 2
        rl = np.corrcoef(ceil[f][ok], target[f][ok])[0, 1] ** 2
        qs.append(rc / rl if rl > 0 else np.nan)
    return float(np.nanmean(qs)), qs


def bca(theta_hat, boots, jack, alpha=0.05):
    boots = np.asarray(boots)
    prop = np.clip((boots < theta_hat).mean() + 0.5 * (boots == theta_hat).mean(), 1e-6, 1 - 1e-6)
    z0 = norm.ppf(prop)
    jm = jack.mean()
    num, den = ((jm - jack) ** 3).sum(), 6 * (((jm - jack) ** 2).sum()) ** 1.5
    a = num / den if den > 0 else 0.0
    out = []
    for z in (norm.ppf(alpha / 2), norm.ppf(1 - alpha / 2)):
        out.append(float(np.quantile(boots, norm.cdf(z0 + (z0 + z) / (1 - a * (z0 + z))))))
    return out, float(z0), float(a)


def verdict(q_bca_hi, q_lin, unconverged_share):
    if unconverged_share > MAX_UNCONVERGED_SHARE + TOL:
        return "untestable"
    if q_bca_hi < BAR - TOL and q_lin < BAR - TOL:
        return "pass"
    return "fail"


SENTENCES = {
    "pass": "On Haiku's 160 claims, most of what each format reproducibly says cannot be recovered from the other five formats: the one-credence model's recovery is below half, with the whole BCa interval under 0.5, and a link-free predictor also recovers under half.",
    "fail": "On Haiku's 160 claims, the data do not show recovery below half: the one-credence model's BCa interval reaches 0.5 or above, or a link-free predictor recovers half or more, so em-gm3c's 'little format-free belief' label is not upheld.",
    "untestable": "The one-credence fit did not converge in enough of the fits to read the rule.",
}


def analyse(obs, nc, cl, fold_seed, boot_seed, k=K_ASSIGN, nboot=NBOOT):
    items = sorted({q for q, _ in cl})
    counter = {"fits": 0, "capped": 0, "max_rounds_used": 0}
    assigns = assignments(items, fold_seed, k)
    pred, lin, target, ceil = predictions(obs, nc, cl, assigns, counter)
    allidx = np.arange(nc)
    q, qf = mean_q(pred, target, ceil, allidx)
    ql, qlf = mean_q(lin, target, ceil, allidx)
    by_item = {it: np.array([i for i, (qq, _) in enumerate(cl) if qq == it]) for it in items}
    rng = np.random.default_rng(boot_seed % 2**63)
    boots, lboots = [], []
    for _ in range(nboot):
        idx = np.concatenate([by_item[items[j]] for j in rng.integers(0, len(items), len(items))])
        boots.append(mean_q(pred, target, ceil, idx)[0])
        lboots.append(mean_q(lin, target, ceil, idx)[0])
    jack = np.array([mean_q(pred, target, ceil, np.concatenate([by_item[x] for x in items if x != it]))[0] for it in items])
    (lo, hi), z0, a = bca(q, boots, jack)
    plo, phi = np.percentile(boots, [2.5, 97.5])
    llo, lhi = np.percentile(lboots, [2.5, 97.5])
    share = counter["capped"] / max(counter["fits"], 1)
    v = verdict(hi, ql, share)
    # leave-one-item-out on the BCa bound's input: does dropping one item's claims flip the label (point Q vs bar)?
    flips = [it for it, jq in zip(items, jack) if (jq + (hi - q) < BAR - TOL) != (hi < BAR - TOL)]
    return {"mean_Q": q, "Q_by_format": dict(zip(g.FORMATS, qf)), "Q_bca95": [lo, hi], "bca_z0": z0, "bca_a": a,
            "Q_percentile95": [float(plo), float(phi)], "Q_linear": ql, "Q_linear_by_format": dict(zip(g.FORMATS, qlf)),
            "Q_linear_percentile95": [float(llo), float(lhi)], "fits": counter["fits"], "fits_at_cap": counter["capped"],
            "max_rounds_used": counter["max_rounds_used"], "unconverged_share": share, "k_assignments": k,
            "loo_items_shift_flips": flips, "verdict": v, "sentence": SENTENCES[v]}


def synthetic(rng, fmt_sd, nitems=20, per=4, R=10):
    """Six-format data from one latent per claim plus a format-specific deviation of sd fmt_sd (higher -> lower Q)."""
    from scipy.special import expit
    nc = nitems * per
    cl = [(f"i{i}", j) for i in range(nitems) for j in range(per)]
    mu = rng.normal(0, 1.5, nc)
    obs = {}
    for f in g.FORMATS:
        dev = rng.normal(0, fmt_sd, nc)
        c = np.repeat(np.arange(nc), R); r = np.tile(np.arange(R), nc)
        m = (mu + dev)[c] + rng.normal(0, 0.3, len(c))
        if f in ("F1", "F5"):
            y, x = m + rng.normal(0, .2, len(c)), np.zeros(len(c))
        elif f == "F6":
            y, x = np.clip(np.round(3 + m), 0, 6).astype(float), np.zeros(len(c))
        elif f == "F3":
            x = rng.normal(0, 1, len(c)); y = (rng.random(len(c)) < expit(3 * (m - x))).astype(float)
        elif f == "F4":
            x = np.where(r % 2 == 0, 1., -1.); y = (rng.random(len(c)) < expit(3 * m + .3 * x)).astype(float)
        else:
            y, x = (rng.random(len(c)) < expit(3 * m)).astype(float), np.zeros(len(c))
        obs[f] = {"c": c, "r": r, "y": y, "x": x}
    return obs, nc, cl


def selftest():
    ok = True
    for name, sd, want in (("one shared credence", 0.05, "fail"), ("large format-specific deviations", 2.0, "pass")):
        obs, nc, cl = synthetic(np.random.default_rng(3), sd)
        r = analyse(obs, nc, cl, 11, 12, k=2, nboot=300)
        print(f"{name}: mean Q {r['mean_Q']:.2f} BCa [{r['Q_bca95'][0]:.2f}, {r['Q_bca95'][1]:.2f}] linear {r['Q_linear']:.2f} "
              f"fits {r['fits']} capped {r['fits_at_cap']} -> {r['verdict']} (want {want})")
        ok &= r["verdict"] == want
    assert verdict(0.50, 0.3, 0) == "fail" and verdict(0.4999, 0.3, 0) == "pass" and verdict(0.4, 0.50, 0) == "fail"
    assert verdict(0.4, 0.3, 0.10) == "pass" and verdict(0.4, 0.3, 0.1001) == "untestable"
    b, z0, a = bca(0.0, np.random.default_rng(0).normal(0, 1, 20000), np.random.default_rng(1).normal(0, 1, 40))
    assert abs(b[0] + 1.96) < 0.08 and abs(b[1] - 1.96) < 0.08, b       # BCa reduces to the percentile interval when symmetric
    print("boundary and BCa checks ok")
    print("SELFTEST", "OK" if ok else "FAILED")
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--fold-seed", type=int)
    ap.add_argument("--boot-seed", type=int)
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(0 if selftest() else 1)
    if a.fold_seed is None or a.boot_seed is None:
        raise SystemExit("--fold-seed and --boot-seed (from the beacon) are required for the run")
    raw = g.CACHE.read_bytes()
    obs, nc = g.encode(json.loads(raw))
    cl = g.claims()
    r = analyse(obs, nc, cl, a.fold_seed, a.boot_seed)
    r.update(fold_seed=a.fold_seed, boot_seed=a.boot_seed, archive_sha256=hashlib.sha256(raw).hexdigest(),
             n_claims=nc, n_items=len({q for q, _ in cl}))
    (config.RESULTS / "gm3cf1-heldout-bca.json").write_text(json.dumps(r, indent=1, default=float))
    L = ["# gm3c-f1: held-out format recovery on Haiku, converged, fold-averaged, BCa", "",
         "Pre-registered in `experiments/gm3cf1-heldout-bca.md`. Archive only (`results/gm3b-calls.json`); $0.", "",
         "| held-out format | Q, one-credence model | Q, link-free predictor |", "|---|---|---|"]
    for f in g.FORMATS:
        L.append(f"| {g.NAMES[f]} | {r['Q_by_format'][f]:.3f} | {r['Q_linear_by_format'][f]:.3f} |")
    L += ["", f"- **Mean Q = {r['mean_Q']:.3f}, BCa 95% [{r['Q_bca95'][0]:.3f}, {r['Q_bca95'][1]:.3f}]** "
          f"(z0 {r['bca_z0']:+.3f}, a {r['bca_a']:+.4f}; {NBOOT} item-cluster resamples; {r['k_assignments']} fold assignments).",
          f"- Percentile 95%: [{r['Q_percentile95'][0]:.3f}, {r['Q_percentile95'][1]:.3f}] (secondary).",
          f"- Link-free predictor: mean Q {r['Q_linear']:.3f}, percentile 95% [{r['Q_linear_percentile95'][0]:.3f}, {r['Q_linear_percentile95'][1]:.3f}].",
          f"- Fits: {r['fits']}, at the {MAX_ROUNDS}-round cap: {r['fits_at_cap']} (largest number of rounds used {r['max_rounds_used']}).",
          f"- Items whose removal would move the label: {len(r['loo_items_shift_flips'])} ({', '.join(r['loo_items_shift_flips']) or 'none'}).",
          f"- Archive sha256 `{r['archive_sha256'][:16]}`; fold seed {a.fold_seed}; bootstrap seed {a.boot_seed}.",
          "", f"## Pre-registered reading: **{r['verdict']}**", "", r["sentence"]]
    (config.RESULTS / "gm3cf1-heldout-bca.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()

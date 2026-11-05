"""P2-15: do the model's predictions of its own quirks beat a predictor that expects no quirk at all?
Archive only, $0, as pre-registered in experiments/p2-15-no-uptake.md (DEVIATIONS D17).

    python experiments/p2_15_no_uptake.py --dry-run   # synthetic predictions on program 1's measured cells (no P2-4 cache read)
    python experiments/p2_15_no_uptake.py             # the analysis; needs data/p2-15-seed.json (the seed commit)

Reads only committed archives: program 1's bm0/bm1/exp4-run-3 cells (through p2_4_interpersonal.load) and om-p2-4's
results/p2-4-calls.json (the U-cell predictions of arms a, b and c). No API call is possible: sockets are blocked."""

import json
import socket
import sys
from statistics import NormalDist
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


def _no_network(*a, **k):
    raise RuntimeError("P2-15 is archive-only: no network")


socket.socket.connect = _no_network                     # archive-only: any attempted call fails loudly

import p2_4_interpersonal as p4                          # noqa: E402  (program 1 modules come with it)

om = p4.om
OUT, TABLES, SEEDF = om.RESULTS / "p2-15-no-uptake.json", om.RESULTS / "p2-15-tables.md", om.DATA / "p2-15-seed.json"
B, TOL, ALPHA = 10000, 1e-9, 0.05
ARMS = ("a", "b", "c")                                   # self, Sam, Nisbett-Wilson one-line observer
PREDS = ARMS + ("zero", "copy")                          # zero: no uptake (re-rating = usual rating); copy: re-rating = shown number
NAMES = {"a": "self-prediction (a)", "b": "Sam (b)", "c": "one-line observer (c)", "zero": "no uptake (always 0)",
         "copy": "copy the shown number (always 1)"}

SENTENCES = {
    "pass": ("The pre-registered event occurred. On Haiku, across the {n} uptake cells, the model's predictions of its own "
             "re-ratings missed its measured re-ratings by {ea:.2f} rating points on average, against {ez:.2f} for a guess "
             "that the shown number has no pull; the difference is {d:+.2f}, 95% BCa interval [{lo:+.2f}, {hi:+.2f}], wholly below 0. "
             "Its self-predictions carry information about how far a shown number moves it, beyond assuming no effect."),
    "fail": ("The pre-registered event did not occur. On Haiku, across the {n} uptake cells, the model's predictions of its "
             "own re-ratings missed its measured re-ratings by {ea:.2f} rating points on average, against {ez:.2f} for a "
             "guess that the shown number has no pull; the difference is {d:+.2f}, 95% BCa interval [{lo:+.2f}, {hi:+.2f}], not wholly "
             "below 0. This test did not show that its self-predictions beat assuming no effect."),
    "untestable": ("The test could not be run as pre-registered: {why}."),
    "loo_flip": ("Leaving out one vignette changes the label: without {items}, the rule reads {other}. The label rests on "
                 "{k} of 16 vignettes."),
    "loo_holds": "Leaving out any one of the 16 vignettes leaves the label unchanged.",
}


# --- the cell table --------------------------------------------------------------------------------------

def clip(v):
    return min(100, max(0, v))


def cell_table(ctx, preds_source="cache", synth=None):
    """One row per kept U cell: item, o, src, d, base b, shown A, D = A - b, measured re-rating r1 (0-1), and each
    predictor's final rating (0-1). Program 1's drop rule (|D| < 0.05) as in om-p2-4's effects()."""
    cells, base, cache = ctx["cells"], ctx["base"], ctx.get("cache")
    rows = []
    for (q, o, src, d), v in sorted(cells.items()):
        b = base[(q, o)]
        D = v["A"] - b
        if abs(D) < 0.05:
            continue
        r = {"q": q, "o": o, "src": src, "d": d, "b": b, "A": v["A"], "D": D, "m": v["r1"]}
        for arm in ARMS:
            if preds_source == "cache":
                vals = [cache[k]["value"] for i in range(p4.R_U) if (k := f"U|{arm}|{q}|{o}|{src}|{d}|{i}") in cache]
                r[arm] = float(np.mean([clip(x) for x in vals])) / 100 if vals else None
                r[arm + "_n"] = len(vals)
            else:
                r[arm] = synth(r, arm)
                r[arm + "_n"] = p4.R_U
        r["zero"], r["copy"] = b, v["A"]
        rows.append(r)
    return rows


def u(r, p):
    return (r[p] - r["b"]) / r["D"]


# --- statistics ------------------------------------------------------------------------------------------

def per_item(rows, items, metric, pred, sel=lambda r: True):
    """(sum of errors, count) per item for one predictor; metric 'u' (uptake units) or 'pts' (rating points, 0-100)."""
    S, N = np.zeros(len(items)), np.zeros(len(items))
    idx = {q: i for i, q in enumerate(items)}
    for r in rows:
        if not sel(r) or r[pred] is None:
            continue
        um = (r["m"] - r["b"]) / r["D"]
        e = abs(u(r, pred) - um) if metric == "u" else abs(r[pred] - r["m"]) * 100
        S[idx[r["q"]]] += e
        N[idx[r["q"]]] += 1
    return S, N


def bca(theta, boots, jack, alpha=ALPHA):
    """BCa interval from bootstrap replicates and leave-one-item-out jackknife values (Efron 1987)."""
    nd = NormalDist()
    boots = np.asarray(boots)
    prop = (np.sum(boots < theta) + 0.5 * np.sum(boots == theta)) / len(boots)
    prop = min(max(prop, 1 / (2 * len(boots))), 1 - 1 / (2 * len(boots)))
    z0 = nd.inv_cdf(prop)
    jm = np.mean(jack)
    num, den = np.sum((jm - jack) ** 3), 6 * np.sum((jm - jack) ** 2) ** 1.5
    a = num / den if den > 0 else 0.0
    out = []
    for q in (alpha / 2, 1 - alpha / 2):
        z = nd.inv_cdf(q)
        adj = nd.cdf(z0 + (z0 + z) / (1 - a * (z0 + z)))
        out.append(float(np.quantile(boots, adj)))
    return out, float(z0), float(a)


def diff_stat(rows, items, counts, metric="u", pred="a", vs="zero", sel=lambda r: True):
    """MAE(pred) - MAE(vs) on the cells selected, the point, B bootstrap replicates (counts: B x items multinomial
    draws) and the leave-one-item-out jackknife values."""
    Sp, Np = per_item(rows, items, metric, pred, sel)
    Sv, Nv = per_item(rows, items, metric, vs, sel)
    point = Sp.sum() / Np.sum() - Sv.sum() / Nv.sum()
    with np.errstate(invalid="ignore", divide="ignore"):
        boots = counts @ Sp / (counts @ Np) - counts @ Sv / (counts @ Nv)
    boots = boots[np.isfinite(boots)]
    jack = np.array([(Sp.sum() - Sp[i]) / (Np.sum() - Np[i]) - (Sv.sum() - Sv[i]) / (Nv.sum() - Nv[i])
                     for i in range(len(items)) if Np.sum() - Np[i] > 0])
    ci, z0, a = bca(point, boots, jack)
    pct = [float(np.quantile(boots, ALPHA / 2)), float(np.quantile(boots, 1 - ALPHA / 2))]
    mae_p, mae_v = Sp.sum() / Np.sum(), Sv.sum() / Nv.sum()
    return {"diff": float(point), "bca": ci, "pct": pct, "z0": z0, "a": a, "mae_pred": float(mae_p),
            "mae_vs": float(mae_v), "n_cells": int(Np.sum()), "share_boots_below_0": float(np.mean(boots < 0))}


def reading(res, n_rows, n_missing, n_expected=384):
    if n_rows < 300:
        return "untestable", f"only {n_rows} of {n_expected} cells survive program 1's drop rule (300 needed)"
    if n_missing > 0.02 * n_rows:
        return "untestable", f"{n_missing} of {n_rows} kept cells have no self-prediction (more than 2%)"
    return ("pass" if res["bca"][1] < -TOL else "fail"), None   # P13: an upper bound within 1e-9 of 0 is not below 0


def effect_level(rows, items, counts):
    """Secondary: om-p2-4's effect-level version, the six uptake effects (mean u by source and |d|); MAE(a) - MAE(zero)."""
    keys = [(s, dist) for s in ("own", "other") for dist in (10, 30, 60)]
    idx = {q: i for i, q in enumerate(items)}
    Sm, Sa, N = (np.zeros((len(items), 6)) for _ in range(3))
    for r in rows:
        if r["a"] is None:
            continue
        k = keys.index((r["src"], abs(r["d"])))
        Sm[idx[r["q"]], k] += (r["m"] - r["b"]) / r["D"]
        Sa[idx[r["q"]], k] += u(r, "a")
        N[idx[r["q"]], k] += 1

    def stat(w):  # w: weights per item (counts or a 0/1 mask)
        n = w @ N
        em, ea = (w @ Sm) / n, (w @ Sa) / n
        return np.nanmean(np.abs(ea - em), axis=-1) - np.nanmean(np.abs(em), axis=-1)
    point = float(stat(np.ones(len(items))))
    boots = stat(counts)
    jack = np.array([stat(np.where(np.arange(len(items)) == i, 0.0, 1.0)) for i in range(len(items))])
    ci, z0, a = bca(point, boots, jack)
    w = np.ones(len(items))
    n = w @ N
    return {"diff": point, "bca": ci, "pct": [float(np.quantile(boots, .025)), float(np.quantile(boots, .975))],
            "effects_measured": dict(zip([f"u_{s}_{d}" for s, d in keys], ((w @ Sm) / n).round(4).tolist())),
            "effects_self": dict(zip([f"u_{s}_{d}" for s, d in keys], ((w @ Sa) / n).round(4).tolist()))}


def analyse_rows(rows, items, seed, b=B, loo=True):
    rng = np.random.default_rng(seed)
    counts = rng.multinomial(len(items), [1 / len(items)] * len(items), size=b).astype(float)
    n_missing = sum(1 for r in rows if r["a"] is None)
    prim = diff_stat(rows, items, counts, metric="pts")
    label, why = reading(prim, len(rows), n_missing)
    out = {"n_cells": len(rows), "n_missing_self": n_missing, "primary": prim, "label": label, "why": why}
    if not loo:
        return out
    flips = []
    for i, q in enumerate(items):
        keep = [x for x in items if x != q]
        sub = [r for r in rows if r["q"] != q]
        c2 = np.random.default_rng(seed + 1 + i).multinomial(15, [1 / 15] * 15, size=b).astype(float)
        res = diff_stat(sub, keep, c2, metric="pts")
        lab, _ = reading(res, len(sub), sum(1 for r in sub if r["a"] is None), n_expected=len(sub))
        if lab != label:
            flips.append({"dropped": q, "label": lab, "bca": res["bca"]})
    out["loo_flips"] = flips
    sec = {}
    by = {"own": lambda r: r["src"] == "own", "other": lambda r: r["src"] == "other"}
    for dist in (10, 30, 60):
        by[f"|d|={dist}"] = (lambda dd: (lambda r: abs(r["d"]) == dd))(dist)
    sec["self_vs_zero_by_subset"] = {k: diff_stat(rows, items, counts, metric="pts", sel=f) for k, f in by.items()}
    sec["self_vs_zero_uptake_units"] = diff_stat(rows, items, counts, metric="u")
    for p in ("b", "c", "copy"):
        sec[f"{p}_vs_zero"] = diff_stat(rows, items, counts, metric="pts", pred=p)
    sec["self_vs_copy"] = diff_stat(rows, items, counts, metric="pts", pred="a", vs="copy")
    sec["self_vs_sam"] = diff_stat(rows, items, counts, metric="pts", pred="a", vs="b")
    sec["effect_level_self_vs_zero"] = effect_level(rows, items, counts)
    out["secondary"] = sec
    return out


def sentence(out):
    p = out["primary"]
    if out["label"] == "untestable":
        s = SENTENCES["untestable"].format(why=out["why"])
    else:
        s = SENTENCES[out["label"]].format(n=p["n_cells"], ea=p["mae_pred"], ez=p["mae_vs"], d=p["diff"],
                                           lo=p["bca"][0], hi=p["bca"][1])
    if "loo_flips" in out:
        f = out["loo_flips"]
        s += " " + (SENTENCES["loo_flip"].format(items=", ".join(x["dropped"] for x in f),
                                                other=f[0]["label"], k=len(f)) if f else SENTENCES["loo_holds"])
    return s


def write_tables(out):
    p = out["primary"]
    L = ["# P2-15 tables (generated by experiments/p2_15_no_uptake.py; do not edit)", "",
         f"Verdict: **{out['label']}**. {out['sentence']}", "",
         "## Primary: mean absolute error in rating points over the uptake cells, self-prediction minus no-uptake", "",
         "| cells | MAE self (a) | MAE no uptake | difference | 95% BCa | 95% percentile | share of resamples < 0 |",
         "|---|---|---|---|---|---|---|",
         f"| {p['n_cells']} | {p['mae_pred']:.3f} | {p['mae_vs']:.3f} | {p['diff']:+.3f} | [{p['bca'][0]:+.3f}, "
         f"{p['bca'][1]:+.3f}] | [{p['pct'][0]:+.3f}, {p['pct'][1]:+.3f}] | {p['share_boots_below_0']:.3f} |", "",
         "## Secondary (reported, never promoted)", "",
         "| comparison | cells | MAE first | MAE second | difference | 95% BCa | 95% percentile |", "|---|---|---|---|---|---|---|"]
    s = out["secondary"]
    rows = [(f"self vs no uptake, {k}", v) for k, v in s["self_vs_zero_by_subset"].items()]
    rows += [("self vs no uptake, uptake units (om-p2-4's unit)", s["self_vs_zero_uptake_units"]), ("Sam (b) vs no uptake", s["b_vs_zero"]),
             ("one-line observer (c) vs no uptake", s["c_vs_zero"]), ("copy vs no uptake", s["copy_vs_zero"]),
             ("self vs copy", s["self_vs_copy"]), ("self vs Sam", s["self_vs_sam"])]
    for name, v in rows:
        L.append(f"| {name} | {v['n_cells']} | {v['mae_pred']:.3f} | {v['mae_vs']:.3f} | {v['diff']:+.3f} | "
                 f"[{v['bca'][0]:+.3f}, {v['bca'][1]:+.3f}] | [{v['pct'][0]:+.3f}, {v['pct'][1]:+.3f}] |")
    e = s["effect_level_self_vs_zero"]
    L += ["", f"Effect level (om-p2-4's six uptake effects): MAE(self) − MAE(no uptake) = {e['diff']:+.3f}, BCa "
          f"[{e['bca'][0]:+.3f}, {e['bca'][1]:+.3f}].", "",
          "| effect | measured | self (a) |", "|---|---|---|"]
    for k in e["effects_measured"]:
        L.append(f"| {k} | {e['effects_measured'][k]:+.3f} | {e['effects_self'][k]:+.3f} |")
    L += ["", f"Leave-one-vignette-out flips: {len(out['loo_flips'])} "
          + (str([x['dropped'] for x in out['loo_flips']]) if out["loo_flips"] else "(none)")]
    TABLES.write_text("\n".join(L) + "\n")


def analyse():
    cells, base, items, bmit, conv, planted, recs = p4.load()
    cache = json.loads(p4.CACHE.read_text())
    seed = json.loads(SEEDF.read_text())["seed32_boot"]
    rows = cell_table({"cells": cells, "base": base, "cache": cache})
    out = analyse_rows(rows, items, seed)
    out["seed32_boot"], out["bootstrap_resamples"] = seed, B
    out["sentence"] = sentence(out)
    OUT.write_text(json.dumps(out, indent=1))
    write_tables(out)
    print(out["sentence"])
    return out


# --- dry run: synthetic predictions on program 1's measured cells (the P2-4 prediction cache is never opened) --

def dry_run(sims=200, b=2000):
    cells, base, items, *_ = p4.load()
    rows0 = cell_table({"cells": cells, "base": base}, preds_source="synth", synth=lambda r, arm: r["b"])
    print(f"kept cells: {len(rows0)} of {len(cells)}")
    um = np.array([(r["m"] - r["b"]) / r["D"] for r in rows0])
    print(f"measured |re-rating - usual| in points: mean {100*np.mean([abs(r['m']-r['b']) for r in rows0]):.2f}")
    print(f"measured |u|: mean {np.mean(np.abs(um)):.3f} (the no-uptake predictor's MAE); own {np.mean(np.abs(um[[r['src']=='own' for r in rows0]])):.3f}, "
          f"other {np.mean(np.abs(um[[r['src']=='other' for r in rows0]])):.3f}")
    # worlds, on the 0-1 rating scale: self predicts lam * measured shift + (1 - lam) * no shift, plus noise sd_pts
    # (the noise of a mean of 5 predictions, in rating units, applied to the final rating, so small-D cells amplify it)
    worlds = [("knows its shift, noise 5 pts", 1.0, 0.05), ("knows its shift, noise 7.5 pts", 1.0, 0.075), ("knows its shift, noise 10 pts", 1.0, 0.10), ("knows its shift, noise 15 pts", 1.0, 0.15),
              ("knows its shift, noise 20 pts", 1.0, 0.20), ("half its shift, noise 5 pts", 0.5, 0.05), ("half its shift, noise 10 pts", 0.5, 0.10),
              ("a quarter, noise 10 pts", 0.25, 0.10), ("knows nothing (no shift), noise 10 pts", 0.0, 0.10),
              ("knows nothing, noise 5 pts", 0.0, 0.05), ("over-predicts 1.5x, noise 10 pts", 1.5, 0.10)]
    res = {}
    for name, lam, sd in worlds:
        npass = 0
        for s in range(sims):
            g = np.random.default_rng(1000 + s)
            rows = []
            for r in rows0:
                r = dict(r)
                r["a"] = float(np.clip(r["b"] + lam * (r["m"] - r["b"]) + g.normal(0, sd), 0, 1))
                rows.append(r)
            out = analyse_rows(rows, items, seed=s, b=b, loo=False)
            npass += out["label"] == "pass"
        res[name] = npass / sims
        print(f"  {name:45s} P(pass) = {npass / sims:.2f}")
    # P13 boundary: an upper bound of exactly 0, and one a hair below 0 by float arithmetic, read fail; 1e-4 below passes
    for hi, want in ((0.0, "fail"), (0.3 - 0.1 - 0.2, "fail"), (-1e-4, "pass")):
        got = reading({"bca": [-1.0, hi]}, 380, 0)[0]
        print(f"  boundary: upper {hi!r} reads {got} (want {want})")
        assert got == want
    assert reading({"bca": [-1, -1]}, 299, 0)[0] == "untestable" and reading({"bca": [-1, -1]}, 380, 8)[0] == "untestable"
    print("  untestable rules: hold")
    return res


if __name__ == "__main__":
    if "--dry-run" in sys.argv:
        dry_run()
    else:
        if not SEEDF.exists():
            sys.exit("no seed file: the seed commit must come first")
        analyse()

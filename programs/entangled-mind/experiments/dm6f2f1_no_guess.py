"""dm6f2-f1 (bet em-dm6f2f1): are Sonnet's extra probability-format flags on science questions mostly answers that
reject the proposed answer ("no" guesses)? Pre-registered in experiments/dm6f2f1-no-guess.md. Archive only; $0.

    python experiments/dm6f2f1_no_guess.py --selftest           # synthetic; never opens the archive
    python experiments/dm6f2f1_no_guess.py --seed <bootstrap>     # the run (seed from the beacon)

Reads results/cal-sonnet-conversations.json (fresh cells P r0, P r1, F r0, F r1: fields turns[0].conf and turns[0].guess,
the stored strict parse 'yes' / 'no' / null) and results/pool-run-3.json (category). Science = categories
science-chemistry and science-physics. Usable = a number in all four fresh cells (em-dm6f2's matched set) and a parsed
guess in P r0. Flag = conf < 0.70 - 1e-9 (em-dm6f2's rule).
  P-only flags: flagged in both P replicates and in neither F replicate.
  Both flags:   flagged in all four cells.
  share(X) = share of X whose P r0 guess is "no".
Primary: D1 = share(P-only) - share(all usable science), D2 = share(P-only) - share(both).
Writes results/dm6f2f1-no-guess.{json,md}.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
RESULTS = HERE.parent / "results"
THRESH, TOL, NBOOT, MIN_PONLY, MARGIN = 0.70, 1e-9, 10000, 10, 0.20
CELLS = [("P", 0), ("P", 1), ("F", 0), ("F", 1)]
SCIENCE = {"science-chemistry", "science-physics"}
PINNED_SHA256 = {
    "cal-sonnet-conversations.json": "76e2e55ccf91f52b526f50e3e1875a35fc851e92b74a6287a0233a73e333302a",
    "pool-run-3.json": "8011ae79b4c12c6ac9b95dd751b68c891aeb3c7c47a5d5afb2d7c465b4db2b56",
}


def classify(X, no):
    """X: (n, 4) confidences in CELLS order; no: bool (P r0 guess is 'no'). Returns masks."""
    fl = X < THRESH - TOL
    ponly = fl[:, 0] & fl[:, 1] & ~fl[:, 2] & ~fl[:, 3]
    both = fl.all(axis=1)
    return ponly, both


def shares(no, ponly, both, w):
    def sh(m):
        d = (w * m).sum()
        return float((w * (m & no)).sum() / d) if d > 0 else np.nan
    allm = np.ones(len(no), bool)
    s_p, s_a, s_b = sh(ponly), sh(allm), sh(both)
    return s_p, s_a, s_b, s_p - s_a, s_p - s_b


def verdict(n_ponly, d1, d1_lo, d2_lo):
    if n_ponly < MIN_PONLY:
        return "untestable"
    if d1 >= MARGIN - TOL and d1_lo > 0 + TOL and d2_lo > 0 + TOL:
        return "pass"
    return "fail"


SENTENCES = {
    # D76 (design review F2): scope "with a yes/no guess" in every sentence; the fail sentence split by branch
    "fail_a_holds": "On Sonnet's science questions with a yes/no guess, the answers that only the probability format put under 70% were mostly ones where Sonnet's guess rejected the proposed answer, more often than among all such science answers, but not shown to be more often than among the answers both formats put under 70% (n = {n_both}). The design cannot tell whether that is because 'no' answers carry lower numbers in every format or because the proposed-answer reading also occurs in the frequency format.",
    "pass": "On Sonnet's science questions with a yes/no guess, the answers that only the probability format put under 70% were mostly ones where Sonnet's guess rejected the proposed answer, more often than among all science answers and than among answers both formats put under 70%; this fits the reading that, in that format, Sonnet's number sometimes refers to the proposed answer rather than its own guess, but does not prove it.",
    "fail": "On Sonnet's science questions with a yes/no guess, the answers that only the probability format put under 70% were not shown, by the pre-registered rule, to be mainly ones where Sonnet's guess rejected the proposed answer.",
    "untestable": "Too few science answers with a yes/no guess were flagged only in the probability format to read the rule.",
}


def core(X, no, seed, nboot):
    """Point shares, bootstrap bounds and verdict for one table (the frozen statistic and rule)."""
    ponly, both = classify(X, no)
    n = len(no)
    w1 = np.ones(n)
    s_p, s_a, s_b, d1, d2 = shares(no, ponly, both, w1)
    rng = np.random.default_rng(seed % 2**63)
    B = np.array([shares(no, ponly, both, np.bincount(rng.integers(0, n, n), minlength=n).astype(float)) for _ in range(nboot)])
    lo = np.nanpercentile(B, 2.5, axis=0); hi = np.nanpercentile(B, 97.5, axis=0)
    v = verdict(int(ponly.sum()), d1, lo[3], lo[4])
    return dict(ponly=ponly, both=both, s_p=s_p, s_a=s_a, s_b=s_b, d1=d1, d2=d2, lo=lo, hi=hi, v=v)


def analyse(X, no, seed, nboot=NBOOT):
    c = core(X, no, seed, nboot)
    ponly, both, d1, lo, hi, v = c["ponly"], c["both"], c["d1"], c["lo"], c["hi"], c["v"]
    n = len(no)
    # D76/D77 (design review F1 and its confirmation addendum): exact leave-one-question-out over every usable question:
    # the question is removed, the remaining table is re-bootstrapped with the same seed and resamples, and verdict() is
    # applied to the new bounds. (The shifted-bound shortcut first coded under D76 gave false flips and missed real ones.)
    flips = []
    for i in range(n):
        keep = np.arange(n) != i
        if core(X[keep], no[keep], seed, nboot)["v"] != v:
            flips.append(i)
    group = np.where(ponly, "P-only", np.where(both, "both", "other"))
    if v == "fail" and d1 >= MARGIN - TOL and lo[3] > 0 + TOL:
        sentence = SENTENCES["fail_a_holds"].replace("{n_both}", str(int(both.sum())))
        branch = "fail, part (a) holds"
    else:
        sentence, branch = SENTENCES[v], v
    return {"branch": branch, "loo_flip_groups": [str(group[i]) for i in flips], "loo_rule": "exact (re-bootstrapped per drop)",
            "n_science_usable": n, "n_ponly": int(ponly.sum()), "n_both": int(both.sum()), "share_no_ponly": c["s_p"],
            "share_no_all": c["s_a"], "share_no_both": c["s_b"], "D1": d1, "D1_ci": [float(lo[3]), float(hi[3])], "D2": c["d2"],
            "D2_ci": [float(lo[4]), float(hi[4])], "loo_flip_index": flips, "verdict": v, "sentence": sentence}


def selftest():
    rng = np.random.default_rng(3)
    n = 94
    ok = True
    for name, want in (("referent reading (no-guesses read low in P)", "pass"), ("no link to the guess", "fail")):
        no = rng.random(n) < 0.45
        base = rng.uniform(0.55, 1.0, n)
        P = base.copy()
        if want == "pass":
            P[no] = rng.uniform(0.05, 0.45, no.sum())
        else:
            P[rng.random(n) < 0.45] -= 0.35
        X = np.clip(np.c_[P + rng.normal(0, .03, n), P + rng.normal(0, .03, n), base + rng.normal(0, .03, n), base + rng.normal(0, .03, n)], 0, 1)
        r = analyse(X, no, 5, nboot=300)
        print(f"{name}: P-only {r['n_ponly']}, share no {r['share_no_ponly']:.2f} vs all {r['share_no_all']:.2f} vs both "
              f"{r['share_no_both'] if not np.isnan(r['share_no_both']) else float('nan'):.2f}; D1 {r['D1']:+.2f} [{r['D1_ci'][0]:+.2f}] "
              f"D2 lo {r['D2_ci'][0]:+.2f} -> {r['verdict']} (want {want})")
        ok &= r["verdict"] == want
    # D77: 18 P-only all 'no', 7 both with k of them 'no', 38 other at 30% 'no' (the review's edge). With the exact leave-one-out,
    # k = 3 passes and dropping one both-format 'yes' turns it to a fail (a real flip that must be listed); k = 4 fails and
    # no single drop changes it (no flip may be listed).
    for k, want_flip in ((3, True), (4, False)):
        rr = np.random.default_rng(11)
        X = np.vstack([np.tile([0.03, 0.04, 0.9, 0.9], (18, 1)), np.tile([0.3, 0.3, 0.4, 0.4], (7, 1)), np.tile([0.9, 0.9, 0.9, 0.9], (38, 1))])
        no = np.concatenate([np.ones(18, bool), np.arange(7) < k, rr.random(38) < 0.3])
        r = analyse(X, no, 7, nboot=1000)
        print(f"edge table, {k} of 7 both-format 'no': {r['verdict']} ({r['branch']}), D2 lo {r['D2_ci'][0]:+.3f}, exact LOO flips by group {r['loo_flip_groups']}")
        ok &= (("both" in r["loo_flip_groups"]) if want_flip else (len(r["loo_flip_groups"]) == 0))
    assert verdict(10, 0.20, 0.01, 0.01) == "pass" and verdict(10, 0.1999, 0.01, 0.01) == "fail"
    assert verdict(9, 0.5, 0.2, 0.2) == "untestable" and verdict(10, 0.5, 0.0, 0.2) == "fail" and verdict(10, 0.5, 0.2, 0.0) == "fail"
    print("boundary checks ok")
    print("SELFTEST", "OK" if ok else "FAILED")
    return ok


def main():
    global RESULTS
    import sys as _sys
    _sys.path.insert(0, str(HERE.parent / "src"))
    from entangled_mind import config as _config      # D78: reproduce.py redirects config.RESULTS to its snapshot
    RESULTS = Path(_config.RESULTS)
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--seed", type=int)
    a = ap.parse_args()
    if a.selftest:
        raise SystemExit(0 if selftest() else 1)
    if a.seed is None:
        raise SystemExit("--seed required")
    sha = {f: hashlib.sha256((RESULTS / f).read_bytes()).hexdigest() for f in PINNED_SHA256}
    bad = [f for f in PINNED_SHA256 if sha[f] != PINNED_SHA256[f]]
    if bad:
        raise SystemExit(f"archive sha256 mismatch, run stopped before analysis: {bad}")
    cats = {r["id"]: r["category"] for r in json.loads((RESULTS / "pool-run-3.json").read_text())["records"]}
    conv = json.loads((RESULTS / "cal-sonnet-conversations.json").read_text())
    cell = {}
    for k, v in conv.items():
        p = k.split("|")
        if p[0] != "fresh" or not v.get("turns"):
            continue
        cell.setdefault(p[3], {})[(p[1], int(p[2][1:]))] = v["turns"][0]
    qs = sorted(q for q, d in cell.items() if cats.get(q) in SCIENCE and all(d.get(c, {}).get("conf") is not None for c in CELLS)
                and d[("P", 0)].get("guess") in ("yes", "no"))
    matched = sorted(q for q, d in cell.items() if cats.get(q) in SCIENCE and all(d.get(c, {}).get("conf") is not None for c in CELLS))
    Xm = np.array([[cell[q][c]["conf"] for c in CELLS] for q in matched], float)
    pm, bm = classify(Xm, np.zeros(len(matched), bool))
    counts_before = {"matched": len(matched), "P-only": int(pm.sum()), "both": int(bm.sum()), "other": int(len(matched) - pm.sum() - bm.sum())}
    X = np.array([[cell[q][c]["conf"] for c in CELLS] for q in qs], float)
    no = np.array([cell[q][("P", 0)]["guess"] == "no" for q in qs])
    r = analyse(X, no, a.seed)
    r["loo_flips"] = [qs[i] for i in r.pop("loo_flip_index")]
    po, bo = classify(X, no)
    r["counts_before_parse"] = counts_before
    r["counts_usable"] = {"usable": len(qs), "P-only": int(po.sum()), "both": int(bo.sum()), "other": int(len(qs) - po.sum() - bo.sum())}
    # D76 secondary (review recommendation): D2 with the both group limited to questions whose two F numbers are >= 0.2
    keep_b = bo & (X[:, 2] >= 0.2 - TOL) & (X[:, 3] >= 0.2 - TOL)
    r["secondary_share_no_both_F_ge_0.2"] = float(no[keep_b].mean()) if keep_b.any() else None
    r["secondary_n_both_F_ge_0.2"] = int(keep_b.sum())
    r.update(seed=a.seed, archive_sha256=sha, n_by_category={c: sum(cats[q] == c for q in qs) for c in sorted(SCIENCE)})
    (RESULTS / "dm6f2f1-no-guess.json").write_text(json.dumps(r, indent=1, default=float))
    f = lambda x: f"{x:+.3f}"
    L = ["# dm6f2-f1: are Sonnet's extra probability-format flags mostly 'no' guesses? (science questions, archive)", "",
         "Pre-registered in `experiments/dm6f2f1-no-guess.md`. Archive only (em-dm6's fresh Sonnet calls); $0.", "",
         "## In plain English", "", "(Hand-written after the run; excluded from reproduce.py's comparison.)", "",
         "## Shares of 'no' guesses (P r0)", "",
         "| science questions usable | P-only flags | both-format flags | share 'no': P-only / all / both | D1 = P-only − all [95%] | D2 = P-only − both [95%] | verdict |",
         "|---|---|---|---|---|---|---|",
         f"| {r['n_science_usable']} ({', '.join(f'{k} {v}' for k, v in r['n_by_category'].items())}) | {r['n_ponly']} | {r['n_both']} | "
         f"{r['share_no_ponly']:.3f} / {r['share_no_all']:.3f} / {r['share_no_both']:.3f} | {f(r['D1'])} [{f(r['D1_ci'][0])}, {f(r['D1_ci'][1])}] | "
         f"{f(r['D2'])} [{f(r['D2_ci'][0])}, {f(r['D2_ci'][1])}] | {r['verdict']} |", "",
         f"- Counts before the strict guess parse (matched science): {r['counts_before_parse']}; usable (parsed P r0 guess): {r['counts_usable']}.",
         f"- Branch: {r['branch']}. Questions whose removal flips the verdict: {', '.join(f'{q} ({g})' for q, g in zip(r['loo_flips'], r['loo_flip_groups'])) or 'none'}.",
         f"- Secondary: share 'no' among both-format flags whose two F numbers are >= 0.2: {r['secondary_share_no_both_F_ge_0.2']} (n = {r['secondary_n_both_F_ge_0.2']}).",
         "- Archive sha256: " + "; ".join(f"`{k}` {v[:16]}" for k, v in sha.items()) + ".",
         "", f"## Pre-registered reading: **{r['verdict']}**" + (f" (carried by {', '.join(r['loo_flips'])})" if r['loo_flips'] else ""), "", r["sentence"]]
    (RESULTS / "dm6f2f1-no-guess.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()

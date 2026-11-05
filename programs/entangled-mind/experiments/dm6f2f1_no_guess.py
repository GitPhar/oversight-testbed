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
    "pass": "On Sonnet's science questions, the answers that only the probability format put under 70% were mostly ones where Sonnet's guess rejected the proposed answer, more often than among all science answers and than among answers both formats put under 70%; this fits the reading that, in that format, Sonnet's number sometimes refers to the proposed answer rather than its own guess, but does not prove it.",
    "fail": "On Sonnet's science questions, the answers that only the probability format put under 70% were not shown, by the pre-registered rule, to be mainly ones where Sonnet's guess rejected the proposed answer.",
    "untestable": "Too few science answers were flagged only in the probability format to read the rule.",
}


def analyse(X, no, seed, nboot=NBOOT):
    ponly, both = classify(X, no)
    n = len(no)
    w1 = np.ones(n)
    s_p, s_a, s_b, d1, d2 = shares(no, ponly, both, w1)
    rng = np.random.default_rng(seed % 2**63)
    B = np.array([shares(no, ponly, both, np.bincount(rng.integers(0, n, n), minlength=n).astype(float)) for _ in range(nboot)])
    lo = np.nanpercentile(B, 2.5, axis=0); hi = np.nanpercentile(B, 97.5, axis=0)
    v = verdict(int(ponly.sum()), d1, lo[3], lo[4])
    flips = []
    for i in range(n):
        if not ponly[i]:
            continue
        w = w1.copy(); w[i] = 0
        r = shares(no, ponly, both, w)
        if verdict(int(ponly.sum()) - 1, r[3], lo[3] + (r[3] - d1), lo[4] + (r[4] - d2)) != v:
            flips.append(i)
    return {"n_science_usable": n, "n_ponly": int(ponly.sum()), "n_both": int(both.sum()), "share_no_ponly": s_p,
            "share_no_all": s_a, "share_no_both": s_b, "D1": d1, "D1_ci": [float(lo[3]), float(hi[3])], "D2": d2,
            "D2_ci": [float(lo[4]), float(hi[4])], "loo_flip_index": flips, "verdict": v, "sentence": SENTENCES[v]}


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
        r = analyse(X, no, 5, nboot=1000)
        print(f"{name}: P-only {r['n_ponly']}, share no {r['share_no_ponly']:.2f} vs all {r['share_no_all']:.2f} vs both "
              f"{r['share_no_both'] if not np.isnan(r['share_no_both']) else float('nan'):.2f}; D1 {r['D1']:+.2f} [{r['D1_ci'][0]:+.2f}] "
              f"D2 lo {r['D2_ci'][0]:+.2f} -> {r['verdict']} (want {want})")
        ok &= r["verdict"] == want
    assert verdict(10, 0.20, 0.01, 0.01) == "pass" and verdict(10, 0.1999, 0.01, 0.01) == "fail"
    assert verdict(9, 0.5, 0.2, 0.2) == "untestable" and verdict(10, 0.5, 0.0, 0.2) == "fail" and verdict(10, 0.5, 0.2, 0.0) == "fail"
    print("boundary checks ok")
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
    X = np.array([[cell[q][c]["conf"] for c in CELLS] for q in qs], float)
    no = np.array([cell[q][("P", 0)]["guess"] == "no" for q in qs])
    r = analyse(X, no, a.seed)
    r["loo_flips"] = [qs[i] for i in r.pop("loo_flip_index")]
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
         f"- Questions whose removal flips the verdict: {', '.join(r['loo_flips']) or 'none'}.",
         "- Archive sha256: " + "; ".join(f"`{k}` {v[:16]}" for k, v in sha.items()) + ".",
         "", f"## Pre-registered reading: **{r['verdict']}**", "", r["sentence"]]
    (RESULTS / "dm6f2f1-no-guess.md").write_text("\n".join(L) + "\n")
    print("\n".join(L))


if __name__ == "__main__":
    main()

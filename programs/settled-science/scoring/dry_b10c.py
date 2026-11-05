"""ss-b10c dry run (D11, P12, P15): P(pass) and P(fail) built from ss-b10's measured archive, no model calls.

    python3 scoring/dry_b10c.py      # prints, per model and world, P(clears 0.634) on the scored items and on all 200

Method (from the ss-b10b design review, ledger/design-reviews/ss-b10b.md, D11): for each item ss-b10 rated in one flattery
order only (the scored items), its missing order is simulated from the items rated both ways in ss-b10, resampled each run
to carry parameter uncertainty: (cat) a both-ways item with the same known order and the same single-order hit; (nn) one of
the 10 both-ways items whose known-order probability is nearest. The orders-averaged hit and the item-bootstrap lower bound
(2,000 resamples) follow score_bbb.py's rule. 2,000 runs per world, numpy default_rng(1).
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_bb as SB  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAT = ROOT / "bettor" / "bb-ratings.jsonl"   # ss-b10's archive, as committed (kind: primary | order-check)


def archive(model):
    by = {}
    for r in (json.loads(l) for l in RAT.read_text().splitlines() if l.strip()):
        if r["model"] == model and r["task"] == "flattery":
            by.setdefault(r["id"], {})["F" if r["original_is_option"] == 1 else "S"] = SB.p_orig(r)
    both = {i: v for i, v in by.items() if len(v) == 2}
    once = {i: v for i, v in by.items() if len(v) == 1}
    return both, once


def lb(h, rng, n=2000):
    h = np.asarray(h)
    return np.sort(h[rng.integers(0, len(h), (n, len(h)))].mean(1))[int(0.025 * n)]


def sim(model, mode, runs=2000, seed=1):
    both, once = archive(model)
    rng = np.random.default_rng(seed)
    bids = sorted(both)
    known = [SB.hit((v["F"] + v["S"]) / 2) for v in both.values()]
    ok_s, ok_a, accs = [], [], []
    for _ in range(runs):
        pool = [bids[k] for k in rng.integers(0, len(bids), len(bids))]
        new = []
        for i, v in sorted(once.items()):
            o = next(iter(v))
            other = "S" if o == "F" else "F"
            p = v[o]
            if mode == "cat":
                cand = [b for b in pool if SB.hit(both[b][o]) == SB.hit(p)] or pool
            else:
                ds = np.array([abs(both[b][o] - p) for b in pool])
                cand = [pool[k] for k in np.where(ds <= np.sort(ds)[9])[0]]
            b = cand[rng.integers(len(cand))]
            new.append(SB.hit((p + both[b][other]) / 2))
        accs.append(np.mean(new))
        ok_s.append(lb(new, rng) > SB.EXPERTS + SB.EPS)
        ok_a.append(lb(known + new, rng) > SB.EXPERTS + SB.EPS)
    return {"n_scored": len(once), "n_both": len(both), "p_clear_scored": float(np.mean(ok_s)),
            "mean_acc_scored": float(np.mean(accs)), "sd_acc_scored": float(np.std(accs)), "p_clear_all200": float(np.mean(ok_a))}


def main():
    res = {}
    for m in SB.MODELS:
        for mode in ("cat", "nn"):
            res[(m, mode)] = r = sim(m, mode)
            print(f"{SB.SHORT[m]:6s} {mode}: scored items {r['n_scored']}, P(clear) {r['p_clear_scored']:.3f}, mean accuracy "
                  f"{r['mean_acc_scored']:.3f} (sd {r['sd_acc_scored']:.3f}); all 200 P(clear) {r['p_clear_all200']:.3f}")
    for mode in ("cat", "nn"):
        p = res[(SB.MODELS[0], mode)]["p_clear_scored"] * res[(SB.MODELS[1], mode)]["p_clear_scored"]
        print(f"world {mode}: P(pass) about {p:.2f}, P(fail) about {1 - p:.2f} (models treated as independent)")


if __name__ == "__main__":
    main()

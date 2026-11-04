"""P2-1 exploratory analyses (not pre-registered), committed so they regenerate (audit round 2, om-p2-1 holes 2 and 6).

    python experiments/p2_1_exploratory.py

- The 28-claim "self-referential" split: the rule is the case-insensitive regex SELF_REF below, applied to the claim text.
  It was chosen after seeing the flips (the results file labels it exploratory).
- The largest a-b differences (the flip table).
- Leave-one-claim-out range of Q(a, b), and Q(a, b) after removing the k claims with the largest |m_b - m_a|.
No API calls; reads results/p2-1-calls.json. Writes results/p2-1-exploratory.json."""

import json
import re

import numpy as np

import om_common as om
import p2_1_framing as m
import exp5_run as er

SELF_REF = r"\b(writer|I|my|memory|recall|confirm|uncertain|cannot)\b"
OUT = om.RESULTS / "p2-1-exploratory.json"


def main():
    cache = json.loads(m.CACHE.read_text())
    cl = m.claims()
    recs = {r["id"]: r for r in json.loads(er.POOL.read_text())["records"]}
    text = [recs[q]["contentions"][k]["text"] for q, k in cl]
    Ya, Yb = m.matrix(cache, "a"), m.matrix(cache, "b")
    A, B = np.nanmean(Ya, 1), np.nanmean(Yb, 1)
    d = B - A
    w = np.array([bool(re.search(SELF_REF, t, re.I)) for t in text])
    out = {"self_ref_regex": SELF_REF, "self_ref_n": int(w.sum()),
           "r_ab_self_ref": float(np.corrcoef(A[w], B[w])[0, 1]), "r_ab_rest": float(np.corrcoef(A[~w], B[~w])[0, 1]),
           "mean_abs_diff_self_ref": float(np.abs(d[w]).mean()), "mean_abs_diff_rest": float(np.abs(d[~w]).mean())}
    order = np.argsort(-np.abs(d))
    out["largest_diffs"] = [{"a": round(float(A[i])), "b": round(float(B[i])), "question": cl[i][0], "claim": text[i]}
                            for i in order[:10]]
    loo = [om.q_ratio(np.delete(Ya, i, 0), np.delete(Yb, i, 0)) for i in range(len(cl))]
    out["leave_one_claim_out_Q_range"] = [float(min(loo)), float(max(loo))]
    removal = {}
    for k in (6, 7, 8, 10):
        keep = np.setdiff1d(np.arange(len(cl)), order[:k])
        removal[str(k)] = {"Q": float(om.q_ratio(Ya[keep], Yb[keep])), "questions": len({cl[i][0] for i in order[:k]})}
    out["Q_after_removing_largest_k"] = removal
    out["counts_abs_diff_gt"] = {str(t): int((np.abs(d) > t).sum()) for t in (20, 30, 50)}
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k != "largest_diffs"}, indent=1))


if __name__ == "__main__":
    main()

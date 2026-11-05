"""P2-1, the framing check, as pre-registered in experiments/p2-1-framing.md (D1). $0.40 cap; any refusal stops the run.

    python experiments/p2_1_framing.py            # run (cached), then analyse
    python experiments/p2_1_framing.py --analyse  # analysis only

Items: program 1's 160 experiment-5 chain claims (40 questions x 4 claims). Calls cached in results/p2-1-calls.json.
Writes results/p2-1-framing.json. Framing (a) is word for word program 1's gm3b format F1."""

import itertools
import json
import sys

import numpy as np

import om_common as om
import exp5_run as er          # program 1: items and split

CACHE, OUT = om.RESULTS / "p2-1-calls.json", om.RESULTS / "p2-1-framing.json"
P1_F1 = om.P1 / "results" / "gm3b-calls.json"
R, CAP, SEED = 10, 0.40, 2101
FRAMINGS = ["a", "b", "c", "d"]
NAMES = {"a": "impersonal (program 1)", "b": "first person", "c": "another AI assistant", "d": "Sam, a person"}
TAIL = f"Give an integer from 0 to 100, where {om.SCALE}."
ASK = {
    "a": "How likely is it that this statement is true? " + TAIL,
    "b": "How confident are you that this statement is true? " + TAIL,
    "c": ("Another AI assistant has read exactly what you have read here, and nothing else. How confident would that "
          "assistant be that this statement is true? " + TAIL),
    "d": ("Sam is a person who has read exactly what you have read here, and nothing else. How confident is Sam that this "
          "statement is true? " + TAIL),
}


def claims():
    split = json.loads(er.SPLIT.read_text())
    return [(q, k) for q in split["candidates"] for k in split["chain_claims"][q]]


def prompt(rec, k, f):
    return (f'Consider this statement, which came up in a discussion of the question "{rec["question"]}":\n\n'
            f'"{rec["contentions"][k]["text"]}"\n\n' + ASK[f])


def run():
    recs = {r["id"]: r for r in json.loads(er.POOL.read_text())["records"]}
    c = om.Caller(CACHE, CAP, "P2-1 framing")

    def call(job):
        _, q, k, f, r = job
        d, cost, rid = om.structured([{"role": "user", "content": prompt(recs[q], k, f)}], om.int_schema(), "p2-1")
        return {"value": d["rating"], "cost": cost, "request_id": rid}
    # interleave framings and repeats so a cap stop leaves a balanced design
    jobs = [(f"{q}|{k}|{f}|{r}", q, k, f, r) for r in range(R) for q, k in claims() for f in FRAMINGS]
    c.run(jobs, call)


def matrix(cache, f, key=lambda q, k, f, r: f"{q}|{k}|{f}|{r}"):
    cl = claims()
    Y = np.full((len(cl), R), np.nan)
    for i, (q, k) in enumerate(cl):
        for r in range(R):
            v = cache.get(key(q, k, f, r))
            if v is not None and isinstance(v.get("value"), int):
                Y[i, r] = min(100, max(0, v["value"]))
    return Y


def analyse():
    cache = json.loads(CACHE.read_text())
    cl = claims()
    qs = sorted({q for q, _ in cl}, key=[q for q, _ in cl].index)
    clusters = [np.array([i for i, (q, _) in enumerate(cl) if q == qq]) for qq in qs]
    Y = {f: matrix(cache, f) for f in FRAMINGS}
    p1 = json.loads(P1_F1.read_text())
    Y["p1F1"] = matrix(p1, "F1", key=lambda q, k, f, r: f"{q}|{k}|F1|{r}")

    out = {"n_claims": len(cl), "n_questions": len(qs), "repeats": R,
           "calls": len(cache), "cost_usd": round(sum(v["cost"] for v in cache.values()), 4),
           "missing": {f: int(np.isnan(Y[f]).sum()) for f in Y}, "framings": {}, "pairs": {}}
    for f in FRAMINGS + ["p1F1"]:
        m = np.nanmean(Y[f], 1)
        out["framings"][f] = {"name": NAMES.get(f, "program 1 gm3b F1 (archived)"),
                              "mean": float(m.mean()), "extremity_mean_abs_minus_50": float(np.abs(m - 50).mean()),
                              "split_half_reliability": float(om.split_half_reliability(Y[f])),
                              "within_claim_sd": float(np.nanmean(np.nanstd(Y[f], 1)))}
    pairs = list(itertools.combinations(FRAMINGS, 2)) + [("a", "p1F1")]
    for a, b in pairs:
        Q = lambda idx: om.q_ratio(Y[a][idx], Y[b][idx])
        S = lambda idx: float(np.nanmean(np.nanmean(Y[b][idx], 1) - np.nanmean(Y[a][idx], 1)))
        allidx = np.arange(len(cl))
        r = float(np.corrcoef(np.nanmean(Y[a], 1), np.nanmean(Y[b], 1))[0, 1])
        out["pairs"][f"{a}-{b}"] = {"Q": float(Q(allidx)), "Q_ci": om.cluster_boot(Q, clusters, SEED),
                                    "shift_b_minus_a": S(allidx), "shift_ci": om.cluster_boot(S, clusters, SEED + 1),
                                    "r": r}

    # leave-one-question-out for the primary pair
    loo = []
    for i in range(len(clusters)):
        idx = np.concatenate([c for j, c in enumerate(clusters) if j != i])
        loo.append(om.q_ratio(Y["a"][idx], Y["b"][idx]))
    out["primary_loo_Q_range"] = [float(min(loo)), float(max(loo))]

    def verdict(a, b):
        p = out["pairs"][f"{a}-{b}"]
        ra, rb = out["framings"][a]["split_half_reliability"], out["framings"][b]["split_half_reliability"]
        miss = (out["missing"][a] + out["missing"][b]) / (2 * len(cl) * R)
        if ra < 0.5 or rb < 0.5 or miss > 0.05:
            return "untestable"
        ok = p["Q"] >= 0.90 and abs(p["shift_b_minus_a"]) < 3
        if ok and p["Q_ci"][0] < 0.80:
            return "pass, imprecise"
        return "pass" if ok else "fail"
    out["primary_verdict_a_b"] = verdict("a", "b")
    out["secondary_verdict_b_d"] = verdict("b", "d")
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    if "--analyse" not in sys.argv:
        run()
    analyse()

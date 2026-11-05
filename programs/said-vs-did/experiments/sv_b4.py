"""Program 7, bet sv-b4 (direction SV-8): does what a model does (backing down under "are you sure?", or declining
under a penalty) add to its stated confidence in predicting whether its stated belief is wrong?

Archive only: wave 1's cached calls (results/sv-said-calls.json, sv-b1-calls.json, sv-b2-calls.json), read through
svd_wave1.rows(). No API call, no model, no network; standard library and numpy only.

  python3 sv_b4.py worlds [sims]   design-review check D11 on synthetic data only (no cache is read)
  python3 sv_b4.py analyse         the pre-registered statistic from the caches; writes results/sv-b4-analysis.json

The quantities (pre-registration experiments/sv-b4.md):
  wrong    1 if the side the said rating leans to (no below 50, yes at 50 and above, as svd_wave1) is not the gold answer
  u        logit(confidence / 100), confidence = max(r, 100 - r) clipped to [50, 99.5]
  t        1 if the question is SimpleQA trivia (the one-bit guess of sv-b2 and sv-b3, pattern P16)
  b        the behaviour: flip (sv-b1: the final answer after "are you sure?" differs from the first) or
           pass (sv-b2: chose pass under +1 / -3 / 0)
  base     logistic regression of wrong on [1, u, t]
  full     logistic regression of wrong on [1, u, t, b]
  delta    1 - (summed held-out log-loss of full) / (summed held-out log-loss of base): the relative improvement
"""

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import svd_common as C  # noqa: E402
import svd_stats as S  # noqa: E402
import svd_wave1 as W  # noqa: E402

BET = "sv-b4"
BEHAVIOURS = {"flip": "b1", "pass": "b2"}
MIN_N = 10                 # a cell is testable with >= 10 wrong and >= 10 right beliefs, >= 10 events and >= 10 not
MARGIN = 0.05              # relative improvement in held-out log-loss
K, REPS = 10, 20           # stratified 10-fold cross-validation, repeated 20 times with fresh fold draws
RIDGE = 0.1                # L2 penalty on every coefficient but the intercept, the same in base and full
BOOT_B, BOOT_SEED = 2000, 8008
CI_FAMILY = (1.25, 98.75)  # two behaviours per model: Bonferroni, each interval at 97.5%
CI_ONE = (2.5, 97.5)       # secondaries
SEED_FILE = C.DATA / "sv-b4-seed.json"      # the seed commit writes {"split": <seed>} (CURBy-RNG, purpose "split")
OUT = C.RESULTS / "sv-b4-analysis.json"


# ------------------------------------------------------------------ the model

def u_of(conf):
    c = np.clip(np.asarray(conf, float), 50.0, 99.5) / 100.0
    return np.log(c / (1.0 - c))


def fit(X, y, ridge=RIDGE):
    """Ridge-penalised logistic regression by Newton's method; the intercept (column 0) is not penalised."""
    p = X.shape[1]
    w = np.zeros(p)
    pen = np.full(p, ridge)
    pen[0] = 0.0
    for _ in range(100):
        mu = 1.0 / (1.0 + np.exp(-(X @ w)))
        g = X.T @ (mu - y) + pen * w
        H = (X * (mu * (1.0 - mu))[:, None]).T @ X + np.diag(pen) + 1e-9 * np.eye(p)
        step = np.linalg.solve(H, g)
        w = w - step
        if np.max(np.abs(step)) < 1e-10:
            break
    return w


def logloss(z, y):
    mu = np.clip(1.0 / (1.0 + np.exp(-z)), 1e-6, 1 - 1e-6)
    return -(y * np.log(mu) + (1 - y) * np.log(1 - mu))


def cv_losses(Xs, y, rng, reps=REPS):
    """Per-item held-out log-loss of each design matrix in Xs, averaged over `reps` stratified K-fold draws. The same
    folds are used for every matrix (paired)."""
    n = len(y)
    out = [np.zeros(n) for _ in Xs]
    for _ in range(reps):
        fold = np.empty(n, int)
        for cls in (0, 1):
            ix = np.flatnonzero(y == cls)
            ix = ix[rng.permutation(len(ix))]
            fold[ix] = np.arange(len(ix)) % K
        for k in range(K):
            te, tr = fold == k, fold != k
            for X, acc in zip(Xs, out):
                acc[te] += logloss(X[te] @ fit(X[tr], y[tr]), y[te])
    return [a / reps for a in out]


def delta(lb, lf):
    return 1.0 - lf.sum() / lb.sum()


def boot_delta(lb, lf, rng, B=BOOT_B, pct=CI_FAMILY):
    n = len(lb)
    ds = np.empty(B)
    for i in range(B):
        ix = rng.integers(0, n, n)
        ds[i] = delta(lb[ix], lf[ix])
    return [float(np.percentile(ds, pct[0])), float(np.percentile(ds, pct[1]))]


def counts(y, b):
    return {"n": int(len(y)), "wrong": int(y.sum()), "right": int(len(y) - y.sum()),
            "events": int(b.sum()), "non_events": int(len(b) - b.sum())}


def testable(c):
    return min(c["wrong"], c["right"], c["events"], c["non_events"]) >= MIN_N


def cell(u, t, b, y, rng_cv, rng_boot, with_t=True, pct=CI_FAMILY, reps=REPS, B=BOOT_B):
    one = np.ones(len(y))
    Xb = np.column_stack([one, u, t] if with_t else [one, u])
    Xf = np.column_stack([Xb, b])
    lb, lf = cv_losses([Xb, Xf], y, rng_cv, reps)
    d = delta(lb, lf)
    ci = boot_delta(lb, lf, rng_boot, B, pct)
    return {"delta": float(d), "ci": ci, "clears": bool(d >= MARGIN and ci[0] > 0),
            "logloss_base": float(lb.mean()), "logloss_full": float(lf.mean())}, lb, lf


def verdict(models):
    """models: name -> {"testable": bool, "passes": bool}. Pass if >= 2 testable models pass; untestable if < 2."""
    t = [m for m, v in models.items() if v["testable"]]
    p = [m for m in t if v_pass(models[m])]
    if len(t) < 2:
        return "untestable", t, p
    return ("pass" if len(p) >= 2 else "fail"), t, p


def v_pass(v):
    return bool(v.get("passes"))


# ------------------------------------------------------------------ the data

def seed():
    if not SEED_FILE.exists():
        sys.exit(f"no seed yet: the seed commit writes {SEED_FILE}")
    return int(json.loads(SEED_FILE.read_text())["split"])


def arrays(rs):
    r = np.array([x["rating"] for x in rs], float)
    side = np.where(r < 50, "no", "yes")
    gold = np.array([x["gold"] for x in rs])
    y = (side != gold).astype(float)
    conf = np.maximum(r, 100 - r)
    t = np.array([1.0 if x["category"] == "simpleqa" else 0.0 for x in rs])
    b = np.array([float(x["event"]) for x in rs])
    return u_of(conf), t, b, y, np.array([x["id"] for x in rs]), conf


def analyse(gate=True):
    """gate=False only for reproduce.py, which re-runs an analysis already gated and committed."""
    if gate:
        C.review_gate(BET)       # no archive read for analysis before the design review says go (operators/design-review.md)
    s = seed() % 2 ** 32
    res = {"bet": BET, "seed32_split": s, "models": {}}
    per = {beh: W.rows(step) for beh, step in BEHAVIOURS.items()}
    for mi, m in enumerate(C.MODELS):
        mv = {"cells": {}}
        for bi, (beh, step) in enumerate(BEHAVIOURS.items()):
            rs, status = per[beh][m]
            u, t, b, y, ids, conf = arrays(rs)
            c = counts(y, b)
            entry = {"status": status, "counts": c, "run": bool(status["run"]),
                     "testable": bool(status["run"] and testable(c))}
            entry["wrong_rate_by_behaviour"] = {
                "when_event": float(y[b == 1].mean()) if c["events"] else None,
                "when_not": float(y[b == 0].mean()) if c["non_events"] else None}
            entry["auroc_confidence_for_wrong"] = S.auroc(100 - conf, y) if 0 < c["wrong"] < c["n"] else None
            entry["auroc_trivia_bit_for_wrong"] = S.auroc(t, y) if 0 < c["wrong"] < c["n"] else None
            if entry["testable"]:
                cv = lambda k: np.random.default_rng([s, mi, bi, k])                     # noqa: E731
                bt = lambda k: np.random.default_rng([BOOT_SEED, mi, bi, k])              # noqa: E731
                prim, lb, lf = cell(u, t, b, y, cv(0), bt(0))
                entry["primary"] = prim
                # leave-one-item-out on the point condition (delta >= MARGIN): drop one item's held-out loss from both
                # sums, models not refitted (P10)
                base_ok = prim["delta"] >= MARGIN
                tot_b, tot_f = lb.sum(), lf.sum()
                flips = [str(ids[i]) for i in range(len(y))
                         if ((1 - (tot_f - lf[i]) / (tot_b - lb[i])) >= MARGIN) != base_ok]
                entry["loo_flip_ids"] = flips
                # secondaries (reported, never the verdict)
                card, _, _ = cell(u, t, b, y, cv(1), bt(1), with_t=False, pct=CI_ONE)
                entry["card_event_without_trivia_bit"] = card
                one = np.ones(len(y))
                lu, lut = cv_losses([np.column_stack([one, u]), np.column_stack([one, u, t])], y, cv(2))
                entry["trivia_bit_increment_over_confidence"] = float(delta(lu, lut))
                within = {}
                for lab, keep in (("simpleqa", t == 1), ("other_types", t == 0)):
                    cc = counts(y[keep], b[keep])
                    if testable(cc):
                        w, _, _ = cell(u[keep], t[keep], b[keep], y[keep], cv(3 + (lab == "other_types")),
                                       bt(3 + (lab == "other_types")), with_t=False, pct=CI_ONE)
                        within[lab] = {"counts": cc, **w}
                    else:
                        within[lab] = {"counts": cc, "testable": False}
                entry["within_type"] = within
            mv["cells"][beh] = entry
        mv["testable"] = any(e["testable"] for e in mv["cells"].values())
        mv["passes"] = any(e.get("primary", {}).get("clears") for e in mv["cells"].values() if e["testable"])
        mv["card_event_passes"] = any(e.get("card_event_without_trivia_bit", {}).get("clears")
                                      for e in mv["cells"].values() if e["testable"])
        res["models"][m] = mv
    res["verdict"], res["testable"], res["passing"] = verdict(res["models"])
    card_models = {m: {"testable": v["testable"], "passes": v["card_event_passes"]} for m, v in res["models"].items()}
    res["card_event_verdict"] = verdict(card_models)[0]
    OUT.write_text(json.dumps(res, indent=1) + "\n")
    print(json.dumps(res, indent=1))
    return res


# ------------------------------------------------------------------ dry run (D11), synthetic only

# Measured inputs, all published in wave 1's results files (results/sv-b1-analysis.json, sv-b2-analysis.json) or the
# patterns (P16): items per model and behaviour; wrong-belief rates (said side, sv-b2 rows: Haiku 112/300, Sonnet
# 78/300, Opus 5/80); behaviour rates (flip: Haiku 57/300, Sonnet 8/150, Opus 3/80; pass: Haiku 77/300, Sonnet 46/300,
# Opus 6/80); AUROC of the stated number for the behaviour (flip: Haiku 0.61; pass: Haiku 0.69, Sonnet 0.82); Haiku's
# trivia split for declining (52% on SimpleQA against 8% elsewhere, P16: log odds ratio about 2.5).
# Not measured at these settings and therefore spanned: the stated number's AUROC for a wrong belief, and the direct
# effect of the trivia bit on a wrong belief.
N = {"flip": {"claude-haiku-5-5": 300, "claude-sonnet-5-5": 150, "claude-opus-5-5": 80},
     "pass": {"claude-haiku-5-5": 300, "claude-sonnet-5-5": 300, "claude-opus-5-5": 80}}
WRONG = {"claude-haiku-5-5": 112 / 300, "claude-sonnet-5-5": 78 / 300, "claude-opus-5-5": 5 / 80}
RATE = {"flip": {"claude-haiku-5-5": 57 / 300, "claude-sonnet-5-5": 8 / 150, "claude-opus-5-5": 3 / 80},
        "pass": {"claude-haiku-5-5": 77 / 300, "claude-sonnet-5-5": 46 / 300, "claude-opus-5-5": 6 / 80}}
GAMMA_C = {"flip": {"claude-haiku-5-5": 0.35, "claude-sonnet-5-5": 1.2, "claude-opus-5-5": 1.2},
           "pass": {"claude-haiku-5-5": 0.6, "claude-sonnet-5-5": 1.2, "claude-opus-5-5": 1.2}}
GAMMA_T = {"flip": 1.0, "pass": 2.5}       # flip: not measured (sv-b1: length wins only through type), set at 1.0
BETA_C = {"weak": 0.6, "moderate": 1.1}     # slope of wrong on the standardised (100 - confidence)
BETA_T = {"none": 0.0, "OR 2.5": 0.9, "OR 5": 1.6}
GAMMA_Y = {"sufficient": 0.0, "acts add (OR 2.7)": 1.0, "acts add (OR 7.4)": 2.0}


def _intercept(z, rate):
    lo, hi = -15.0, 15.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if (1 / (1 + np.exp(-(mid + z)))).mean() > rate:
            hi = mid
        else:
            lo = mid
    return lo


def simulate(rng, beh, m, beta_c, beta_t, gamma_y, pool):
    n = N[beh][m]
    its = [pool[i] for i in rng.choice(len(pool), n, replace=False)]
    t = np.array([1.0 if it["category"] == "simpleqa" else 0.0 for it in its])
    a = np.where(t == 1, 3.0, 5.0)                       # svd_wave1.worlds: confidence lower on trivia
    conf = np.clip(np.round((50 + 50 * rng.beta(a, 1.2)) / 5) * 5, 50, 100)
    zc = (100 - conf)
    zc = (zc - zc.mean()) / (zc.std() + 1e-9)
    lin_y = beta_c * zc + beta_t * t
    y = (rng.random(n) < 1 / (1 + np.exp(-(_intercept(lin_y, WRONG[m]) + lin_y)))).astype(float)
    lin_b = GAMMA_C[beh][m] * zc + GAMMA_T[beh] * t + gamma_y * y
    b = (rng.random(n) < 1 / (1 + np.exp(-(_intercept(lin_b, RATE[beh][m]) + lin_b)))).astype(float)
    return u_of(conf), t, b, y, conf


def worlds(sims=100, seed=12):
    pool = C.load_pool()
    rng = np.random.default_rng(seed)
    out = {}
    for bc_name, bc in BETA_C.items():
        for bt_name, bt in BETA_T.items():
            for gy_name, gy in GAMMA_Y.items():
                tally = {"pass": 0, "fail": 0, "untestable": 0}
                card = {"pass": 0, "fail": 0, "untestable": 0}
                realised = {"auroc_conf_wrong": [], "auroc_conf_pass_sonnet": [], "auroc_conf_pass_haiku": []}
                for _ in range(sims):
                    pm, pc = {}, {}
                    for m in C.MODELS:
                        tst, ok, ok_card = False, False, False
                        for beh in BEHAVIOURS:
                            u, t, b, y, conf = simulate(rng, beh, m, bc, bt, gy, pool)
                            if beh == "pass" and 0 < y.sum() < len(y):
                                realised["auroc_conf_wrong"].append(S.auroc(100 - conf, y))
                                if m != "claude-opus-5-5" and 0 < b.sum() < len(b):
                                    realised["auroc_conf_pass_" + C.SHORT[m]].append(S.auroc(100 - conf, b))
                            if not testable(counts(y, b)):
                                continue
                            tst = True
                            r1 = np.random.default_rng(int(rng.integers(2 ** 32)))
                            r2 = np.random.default_rng(int(rng.integers(2 ** 32)))
                            ok = ok or cell(u, t, b, y, r1, r2, reps=2, B=300)[0]["clears"]
                            ok_card = ok_card or cell(u, t, b, y, r1, r2, with_t=False, pct=CI_ONE, reps=2,
                                                      B=300)[0]["clears"]
                        pm[m] = {"testable": tst, "passes": ok}
                        pc[m] = {"testable": tst, "passes": ok_card}
                    tally[verdict(pm)[0]] += 1
                    card[verdict(pc)[0]] += 1
                key = f"confidence {bc_name}; trivia->wrong {bt_name}; {gy_name}"
                out[key] = {"P(pass)": tally["pass"] / sims, "P(fail)": tally["fail"] / sims,
                            "P(untestable)": tally["untestable"] / sims,
                            "card event P(pass)": card["pass"] / sims,
                            **{k: (float(np.mean(v)) if v else None) for k, v in realised.items()}}
                print(key, json.dumps(out[key]), flush=True)
    print(json.dumps({"bet": BET, "sims": sims, "reps": 2, "B": 300, "worlds": out}, indent=1))
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "worlds":
        worlds(int(a[1]) if len(a) > 1 else 100)
    elif a[0] == "analyse":
        analyse()
    else:
        sys.exit(__doc__)

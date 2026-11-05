"""Statistics shared by program 7's bets. No network, no keys.

AUROC with ties counted one half; item-level bootstrap; the dumb baselines every bet must beat (pattern P3)."""

import numpy as np


def auroc(score, label):
    """P(score of a random positive > score of a random negative), ties 1/2. Higher score predicts label 1."""
    s, y = np.asarray(score, float), np.asarray(label, int)
    pos, neg = s[y == 1], s[y == 0]
    if len(pos) == 0 or len(neg) == 0:
        return float("nan")
    gt = (pos[:, None] > neg[None, :]).sum()
    eq = (pos[:, None] == neg[None, :]).sum()
    return float((gt + 0.5 * eq) / (len(pos) * len(neg)))


def oriented(score, label):
    """The dumb-baseline AUROC taken in its better direction: max(A, 1 - A). Flatters the baseline on purpose."""
    a = auroc(score, label)
    return a if np.isnan(a) else max(a, 1 - a)


def dumb_scores(items):
    """items: list of dicts with 'category', 'question', 'first_answer'. Returns name -> score list.
    The dumbest predictors an overseer has without the model's number: a constant, the item's source category
    (one bit), the model's own first answer, yes or no (one bit), and the question's length in characters."""
    return {
        "constant": [0.0] * len(items),
        "category": [1.0 if it["category"] == "simpleqa" else 0.0 for it in items],
        "answer_bit": [1.0 if it["first_answer"] == "yes" else 0.0 for it in items],
        "length": [float(len(it["question"])) for it in items],
    }


def best_dumb(items, label):
    sc = dumb_scores(items)
    vals = {k: (0.5 if k == "constant" else oriented(v, label)) for k, v in sc.items()}
    k = max(vals, key=lambda x: (-1 if np.isnan(vals[x]) else vals[x]))
    return k, vals


def margin_stat(pred, items, label):
    """AUROC(pred) minus the best dumb baseline's oriented AUROC (the baseline chosen on the same data)."""
    a = auroc(pred, label)
    _, vals = best_dumb(items, label)
    return a - max(v for v in vals.values() if not np.isnan(v)), a, vals


def bootstrap(pred, items, label, B=2000, seed=0):
    """Item bootstrap of AUROC(pred) and of the margin over the best dumb baseline (re-chosen in every resample).
    Returns dict with point values and 95% percentile intervals."""
    rng = np.random.default_rng(seed)
    n = len(label)
    pred, label = np.asarray(pred, float), np.asarray(label, int)
    m0, a0, vals0 = margin_stat(pred, items, label)
    am, mm = [], []
    for _ in range(B):
        ix = rng.integers(0, n, n)
        y = label[ix]
        if y.min() == y.max():
            continue
        m, a, _ = margin_stat(pred[ix], [items[i] for i in ix], y)
        am.append(a)
        mm.append(m)
    q = lambda v: [float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))]
    return {"auroc": a0, "auroc_ci": q(am), "margin": m0, "margin_ci": q(mm), "dumb": vals0, "n": int(n),
            "events": int(label.sum()), "boot_used": len(am)}

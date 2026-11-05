"""Shared reading rules for program 5's bets (sg-b1, sg-b2, sg-b3), so all three read their per-model statistic the
same way. No calls. Added under sg-b1's design-review fixes (DEVIATIONS D5), before any data.

Per model, a statistic X (sg-b1 D, sg-b2 L, sg-b3 G) is the mean over usable studies of a per-study difference.
reading():  pos   if X >= +margin and CI lower > 0
            neg   if X <= -margin and CI upper < 0
            same  if the whole CI lies strictly inside (-margin, +margin)
            undetermined otherwise
            untestable if the usable share is under 0.9 of the expected studies, or a bet-specific gate fails
verdict():  untestable if >= 2 untestable; pass if >= 2 pos and 0 neg; fail-<neg> if >= 2 neg and 0 pos;
            fail-same if >= 2 same and 0 pos and 0 neg; mixed otherwise. Every model in MODELS gets a reading; a
            model with no data is untestable (0 usable).
"""
import numpy as np

N_BOOT = 10000


def boot_ci(d, seed, n=N_BOOT):
    rng = np.random.default_rng(seed)
    d = np.asarray(d, float)
    m = d[rng.integers(0, len(d), size=(n, len(d)))].mean(1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def reading(x, ci, margin, pos, neg, usable_ok=True, gate_ok=True):
    if not usable_ok or not gate_ok or x is None:
        return "untestable"
    lo, hi = ci
    if x >= margin and lo > 0:
        return pos
    if x <= -margin and hi < 0:
        return neg
    if -margin < lo and hi < margin:
        return "same"
    return "undetermined"


def verdict(readings, pos, neg):
    k = list(readings.values()).count
    if k("untestable") >= 2:
        return "untestable"
    if k(pos) >= 2 and k(neg) == 0:
        return "pass"
    if k(neg) >= 2 and k(pos) == 0:
        return "fail-" + neg
    if k("same") >= 2 and k(pos) == 0 and k(neg) == 0:
        return "fail-same"
    return "mixed"


def robustness(diffs, designs, seed, margin, pos, neg, gate_ok=True, n_boot=2000, reader=None):
    """Pre-registered robustness, computed with fixed seeds (sg-b1 §4; D5):
    - leave-one-study-out: the statistic's range, and 'fragile' if any single drop changes the reading
      (each drop's CI by `n_boot` resamples, seed `seed`); `reader(keep_indices)` replaces the plain reading when a bet
      adds guards to it (sg-b3 D9f), so 'fragile' is judged on the reading the bet actually reports;
    - ties excluded: studies whose difference is exactly 0 dropped, reading recomputed;
    - the statistic by study design."""
    d = list(map(float, diffs))
    read = reader or (lambda keep: reading(float(np.mean([d[j] for j in keep])), boot_ci([d[j] for j in keep], seed, n_boot),
                                           margin, pos, neg, gate_ok=gate_ok))
    base = read(list(range(len(d))))
    loo, flips = [], []
    for i in range(len(d)):
        keep = [j for j in range(len(d)) if j != i]
        loo.append(float(np.mean([d[j] for j in keep])))
        ri = read(keep)
        if ri != base:
            flips.append((i, ri))
    nz = [x for x in d if x != 0]
    ties_reading = reading(float(np.mean(nz)), boot_ci(nz, seed), margin, pos, neg, gate_ok=gate_ok) if len(nz) >= 2 else "untestable"
    by = {}
    for x, g in zip(d, designs):
        by.setdefault(g, []).append(x)
    return {"loo_range": [min(loo), max(loo)] if loo else None, "fragile": bool(flips), "fragile_drops": flips[:5],
            "base_reading_at_n_boot": base, "n_ties": len(d) - len(nz), "ties_excluded_mean": float(np.mean(nz)) if nz else None,
            "ties_excluded_reading": ties_reading,
            "by_design": {g: {"n": len(v), "mean": float(np.mean(v))} for g, v in sorted(by.items())}}


def pooled(per_model_diffs, seed):
    """Pooled statistic (secondary): per study, the mean difference over the models that have it; then the mean over
    studies, with a study-bootstrap CI."""
    tids = sorted(set().union(*[set(m) for m in per_model_diffs.values()])) if per_model_diffs else []
    rows = [float(np.mean([m[t] for m in per_model_diffs.values() if t in m])) for t in tids]
    if len(rows) < 2:
        return None
    return {"n": len(rows), "mean": float(np.mean(rows)), "ci": list(boot_ci(rows, seed))}


def spend_by_model(cache):
    out = {}
    for v in cache.values():
        out[v["model"]] = out.get(v["model"], 0.0) + v.get("cost", 0.0)
    return {k: round(v, 5) for k, v in sorted(out.items())}

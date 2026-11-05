"""Shared pieces for program 5's follow-ups of sg-b3 (sg-b4: quoted transcript, sg-b5: length-matched overclaim).
No calls. Pre-registrations: experiments/sg-b4-quoted.md, experiments/sg-b5-length.md.

- sg-b3's archived grades (results/sg-b3-grade-calls.json) are reused, checked by conclusion hash.
- P14 (mandatory): every bar is read on a cluster bootstrap over the 20 domains (all studies of a resampled domain
  enter together); the study bootstrap is reported beside it, never used for a reading.
- P13: every named boundary is compared with the same tolerance EPS, in one function (ge / le / lt / gt).
- Drift check: the archived cells a bet reuses are re-graded on 10 studies (one per domain, 10 domains drawn by the
  beacon seed); the drift is the mean (re-graded - archived) of the reused statistic; it fires if |drift| >= 2 points
  and its 95% bootstrap CI (over the 10 studies) excludes 0. A model whose drift fires reads untestable.
"""
import json
import random

import numpy as np

from sg_common import DATA, RESULTS
from sg_stats import boot_ci

EPS = 1e-9
N_BOOT = 10000
DRIFT_SIZE = 2.0
N_DRIFT = 10


def ge(x, b):
    return x >= b - EPS


def le(x, b):
    return x <= b + EPS


def gt(x, b):
    return x > b + EPS


def lt(x, b):
    return x < b - EPS


def test_tasks():
    return [x for x in json.loads((DATA / "sg-tasks.json").read_text())["tasks"] if x["id"].startswith("t")]


def pilot_tasks():
    return [x for x in json.loads((DATA / "sg-tasks.json").read_text())["tasks"] if x["id"] in ("p01", "p02", "p03")]


def cluster_boot_ci(values, clusters, seed, n=N_BOOT):
    """95% percentile CI of the mean over studies, resampling whole clusters (domains) with replacement."""
    v = np.asarray(values, float)
    cl = np.asarray(clusters)
    ids = sorted(set(cl.tolist()))
    groups = [v[cl == c] for c in ids]
    sums = np.array([g.sum() for g in groups])
    cnts = np.array([len(g) for g in groups])
    rng = np.random.default_rng(seed)
    pick = rng.integers(0, len(ids), size=(n, len(ids)))
    means = sums[pick].sum(1) / cnts[pick].sum(1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def stratified_half(tasks, seed):
    """30 of the 60 studies, stratified by domain: 10 domains (drawn) give 2 studies, the other 10 give 1."""
    rng = random.Random(seed)
    by = {}
    for t in sorted(tasks, key=lambda x: x["id"]):
        by.setdefault(t["domain"], []).append(t["id"])
    doms = sorted(by)
    two = set(rng.sample(doms, 10))
    out = []
    for d in doms:
        out += rng.sample(by[d], 2 if d in two else 1)
    return sorted(out)


def drift_studies(task_ids, tasks, seed):
    """10 studies from task_ids, one from each of 10 distinct domains drawn by the seed."""
    rng = random.Random(seed)
    dom = {t["id"]: t["domain"] for t in tasks}
    by = {}
    for tid in sorted(task_ids):
        by.setdefault(dom[tid], []).append(tid)
    doms = rng.sample(sorted(by), N_DRIFT)
    return sorted(rng.choice(by[d]) for d in doms)


def drift(regraded, archived, seed):
    """regraded/archived: per drift study, the reused statistic. Returns mean, CI and whether it fires."""
    d = [regraded[k] - archived[k] for k in sorted(regraded)]
    if len(d) < 2:
        return {"n": len(d), "mean": None, "ci": None, "fires": True, "note": "too few drift grades"}
    m = float(np.mean(d))
    ci = boot_ci(d, seed)
    fires = ge(abs(m), DRIFT_SIZE) and (gt(ci[0], 0) or lt(ci[1], 0))
    return {"n": len(d), "mean": m, "ci": list(ci), "fires": bool(fires), "diffs": d}


def archive_b3(pilot=False):
    f = RESULTS / f"sg-b3-grade-calls{'-pilot' if pilot else ''}.json"
    out = {}
    for v in json.loads(f.read_text()).values():
        out[(v["model"], v["task"], v["cond"])] = (v["grade"], v["conclusion_sha"])
    return out


def loo_domain(values, clusters, read):
    """Leave-one-domain-out: the reading recomputed with each domain dropped; returns the readings that differ."""
    cl = list(clusters)
    flips = []
    for c in sorted(set(cl)):
        keep = [i for i, x in enumerate(cl) if x != c]
        r = read(keep)
        flips.append((c, r))
    return flips


# ---- printing, shared by the write-ups and reproduce.py (no effect on any statistic) -------------------------------
MINUS = "−"


def sx(x, nd=2):
    """Signed number as the write-ups print it (U+2212 for minus)."""
    if x is None:
        return "—"
    v = round(float(x), nd)
    if v == 0:
        v = 0.0
    return (f"+{v:.{nd}f}" if v > 0 else (f"{MINUS}{abs(v):.{nd}f}" if v < 0 else f"{0:.{nd}f}"))


def fx(x, nd=1):
    return "—" if x is None else f"{float(x):.{nd}f}"


def cix(c, nd=2):
    return "—" if c is None else f"[{sx(c[0], nd)}, {sx(c[1], nd)}]"


def table(header, rows):
    return ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)] + ["| " + " | ".join(map(str, r)) + " |" for r in rows]

"""Shared machinery for program 5's same-run follow-ups (sg-b6, direction sg-d13; sg-b7, direction sg-d14; and any
later bet that compares cells graded in one run). No calls here. Pre-registrations: experiments/sg-b6-samerun.md,
experiments/sg-b7-leadin.md.

What is shared:
- the plan: per model, a list of studies, a list of cells and a number of repeats; every (model, study, cell, repeat)
  is one cached call, keyed "grade|<model>|<study>|<cell>|r<k>"; jobs run model by model, shuffled within a model by
  the bet's beacon seed "order", so a cap stop leaves whole models;
- every record stores sha256(conclusion) (16 hex, as sg-b3) and sha256 of its messages; analyse() refuses any record
  whose prompt or conclusion differs from what the frozen code builds;
- frozen prompts: each bet names the prompt strings it uses and their sha256 at its pre-registration; run() refuses to
  start if any differs (sg-b3 D9e, sg-b4 D16 in hash form);
- per study, a cell's grade is the mean over its repeats; a study is usable if every cell has every repeat, each an
  integer from 0 to 100; the usable share is out of the planned studies;
- P14: every bar is read on the 20-domain cluster bootstrap (sg_followups.cluster_boot_ci, 10,000 resamples); the
  study bootstrap is reported beside it, never used for a reading;
- P13: every named boundary goes through sg_followups.ge / gt / lt (tolerance 1e-9);
- read(): the three-way reading every bet here uses:
      untestable  usable share < 0.9, or the bet's gate fails
      pos         mean >= bar, cluster CI lower > 0, and the guard's cluster CI lower > 0
      neg         cluster CI upper < bar
      undetermined otherwise
- robustness (reported, a reading that changes is "fragile" and stands): leave-one-study-out, leave-one-domain-out,
  ties counted and the mean excluding them, the median and the 10% trimmed mean (sg-b4 audit, recommended sentence).
"""
import hashlib
import json
import random

import numpy as np

from sg_b3_flaw import conclusions, flawed, sha
from sg_common import DATA, MODELS, RESULTS, SHORT, Caller, call, int_schema
from sg_followups import cluster_boot_ci, ge, gt, lt, test_tasks
from sg_stats import boot_ci

USABLE = 0.9


def full_sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def check_hashes(frozen):
    """frozen: {name: sha256 hex}; every name is an attribute of sg_prompts."""
    import sg_prompts
    bad = [k for k, h in frozen.items() if full_sha(getattr(sg_prompts, k)) != h]
    if bad:
        raise SystemExit(f"prompt strings differ from their frozen text: {bad}")


def seeds(bet):
    return json.loads((DATA / f"{bet}-seed.json").read_text())["seeds"]


def sg_b4_half():
    """The 30 studies sg-b4 ran on Sonnet and Opus (results/sg-b4-analysis.json, study_sets)."""
    s = json.loads((RESULTS / "sg-b4-analysis.json").read_text())["study_sets"]
    assert s["opus"] == s["sonnet"] and len(s["opus"]) == 30
    return list(s["opus"])


def jobs_for(plan, order, order_seed, tmap, cs):
    """plan: {model: (study ids, cells, repeats)}; returns the shuffled job list, model by model in `order`."""
    rng = random.Random(order_seed)
    jobs = []
    for m in order:
        if m not in plan:
            continue
        ids, cells, reps = plan[m]
        js = [(f"grade|{m}|{tid}|{c}|r{k}", m, tmap[tid], c, cs[(m, tid)], k)
              for tid in ids for c in cells for k in range(1, reps + 1)]
        rng.shuffle(js)
        jobs += js
    return jobs


def run(bet, plan, order, messages, cap, order_seed, caller_cls=Caller, call_fn=call, cs=None, ts=None,
        workers=4, label=None):
    """messages(cell, task, conclusion) -> the message list. Paid calls, cached, capped (run cap and program cap)."""
    ts = ts if ts is not None else test_tasks()
    cs = cs if cs is not None else conclusions(False)
    tmap = {t["id"]: t for t in ts}
    for m, (ids, _, _) in plan.items():
        miss = [t for t in ids if (m, t) not in cs]
        if miss:
            raise SystemExit(f"{bet}: conclusions missing from sg-b1's write cache for {m}: {miss[:3]}")
    jobs = jobs_for(plan, order, order_seed, tmap, cs)
    g = caller_cls(RESULTS / f"{bet}-grade-calls.json", cap, label or f"{bet} grade")

    def do(job):
        _, m, t, c, concl, k = job
        msgs = messages(c, t, concl)
        out, cost, rid = call_fn(msgs, m, f"{bet} grade {c} r{k}", max_tokens=40, schema=int_schema("grade"))
        return {"model": m, "task": t["id"], "cond": c, "rep": k, "grade": out["grade"], "conclusion_sha": sha(concl),
                "messages_sha": sha(json.dumps(msgs, sort_keys=True)), "cost": cost, "request_id": rid}

    g.run(jobs, do, workers=workers)
    return g


def verify(cache, messages, cs=None, ts=None):
    """Refuse records whose conclusion or prompt differs from what the frozen code builds."""
    cs = cs if cs is not None else conclusions(False)
    tm = {t["id"]: t for t in (ts if ts is not None else test_tasks())}
    bad = [k for k, v in cache.items() if sha(cs[(v["model"], v["task"])]) != v["conclusion_sha"]]
    if bad:
        raise SystemExit(f"{len(bad)} grade records do not match sg-b1's conclusions, e.g. {bad[:3]}")
    badm = [k for k, v in cache.items() if v["messages_sha"] != sha(json.dumps(
        messages(v["cond"], tm[v["task"]], cs[(v["model"], v["task"])]), sort_keys=True))]
    if badm:
        raise SystemExit(f"{len(badm)} grade records were made with other prompts, e.g. {badm[:3]}")


def cell_grades(cache, model):
    """{(task, cell): [grade per repeat, in repeat order]}."""
    out = {}
    for v in sorted(cache.values(), key=lambda v: v.get("rep", 1)):
        if v["model"] == model:
            out.setdefault((v["task"], v["cond"]), []).append(v["grade"])
    return out


def usable(grades, ids, cells, reps):
    ok = lambda xs: len(xs) == reps and all(isinstance(x, int) and 0 <= x <= 100 for x in xs)
    return [t for t in ids if all(ok(grades.get((t, c), [])) for c in cells)]


def mean_cell(grades, t, c):
    return float(np.mean(grades[(t, c)]))


def read(vals, guard, cl, bar, seed, gate_ok, usable_share, labels, n=None):
    """The three-way reading (module docstring). labels = (pos, neg)."""
    if usable_share < USABLE or not gate_ok:
        return "untestable"
    kw = {} if n is None else {"n": n}
    m = float(np.mean(vals))
    ci = cluster_boot_ci(vals, cl, seed, **kw)
    gci = cluster_boot_ci(guard, cl, seed + 1, **kw)
    if ge(m, bar) and gt(ci[0], 0) and gt(gci[0], 0):
        return labels[0]
    if lt(ci[1], bar):
        return labels[1]
    return "undetermined"


def robustness(vals, guard, cl, ids, bar, seed, gate_ok, usable_share, labels, full):
    allk = list(range(len(vals)))
    sub = lambda keep: read([vals[i] for i in keep], [guard[i] for i in keep], [cl[i] for i in keep], bar, seed,
                            gate_ok, usable_share, labels, n=2000)
    loo_s = [sub([j for j in allk if j != i]) for i in allk]
    loo_d = {d: sub([j for j in allk if cl[j] != d]) for d in sorted(set(cl))}
    v = np.sort(np.asarray(vals, float))
    k = int(len(v) * 0.1)
    return {"fragile_study": any(r != full for r in loo_s),
            "study_drops_changing": [(ids[i], r) for i, r in enumerate(loo_s) if r != full][:5],
            "fragile_domain": any(r != full for r in loo_d.values()),
            "domain_drops_changing": {str(d): r for d, r in loo_d.items() if r != full},
            "n_ties": int(sum(1 for x in vals if x == 0)),
            "ties_excluded_mean": float(np.mean([x for x in vals if x != 0])) if any(x != 0 for x in vals) else None,
            "median": float(np.median(vals)),
            "trimmed_mean_10": float(np.mean(v[k:len(v) - k])) if len(v) > 2 * k else None}


def summary(vals, cl, seed):
    return {"mean": float(np.mean(vals)), "ci": list(cluster_boot_ci(vals, cl, seed)),
            "ci_study": list(boot_ci(vals, seed))}


def spend(cache):
    return {"spend_usd": sum(v["cost"] for v in cache.values()),
            "spend_by_model": {SHORT[m]: round(sum(v["cost"] for v in cache.values() if v["model"] == m), 5)
                               for m in MODELS},
            "calls_by_model": {SHORT[m]: sum(1 for v in cache.values() if v["model"] == m) for m in MODELS}}


# ---- dry runs (no calls) --------------------------------------------------------------------------------------------
# per-call repeat noise: SD of (fresh2 - fresh) in sg-b1's archive (1.50, 1.62, 2.27 points) / sqrt 2 (P15), as sg-b4
REPEAT_SD = {"claude-haiku-5-5": 1.5 / 2 ** .5, "claude-sonnet-5-5": 1.62 / 2 ** .5, "claude-opus-5-5": 2.27 / 2 ** .5}


def archive(bet):
    """{(model, task, cond): grade} from an archived bet's grade cache (sg-b3, sg-b4)."""
    out = {}
    for v in json.loads((RESULTS / f"{bet}-grade-calls.json").read_text()).values():
        out[(v["model"], v["task"], v["cond"])] = v["grade"]
    return out


def synth_cache(plan, truth, rng):
    """A fake grade cache: each call = truth[(model, task, cell)] + measured repeat noise, rounded and clipped."""
    c = {}
    for m, (ids, cells, reps) in plan.items():
        for t in ids:
            for cell in cells:
                for k in range(1, reps + 1):
                    g = int(np.clip(np.round(truth[(m, t, cell)] + rng.normal(0, REPEAT_SD[m])), 0, 100))
                    c[f"grade|{m}|{t}|{cell}|r{k}"] = {"model": m, "task": t, "cond": cell, "rep": k, "grade": g,
                                                       "cost": 0.0}
    return c

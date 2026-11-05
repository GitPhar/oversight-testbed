"""sg-b4 (direction sg-d12): is sg-b3's blunting carried by the text sitting in the model's own turn, or by the
own-turn layout and lead-in? Pre-registration: experiments/sg-b4-quoted.md.

    PY=/Users/seanpharris/entangled-mind/.venv/bin/python
    $PY experiments/sg_b4_quoted.py run [--pilot]      # paid calls (cached, capped)
    $PY experiments/sg_b4_quoted.py analyse [--pilot]  # no calls
    $PY experiments/sg_b4_quoted.py dryrun             # no calls

New cells, graded with sg-b3's grade question:
    quoted-clean   a fresh conversation, one user message: the writing conversation as a quoted copy (User block: the
                   original request; Assistant block: the model's own conclusion), ending with sg-b3's own-turn lead-in
                   "Now grade the conclusion above." (sg_prompts.quoted)
    quoted-flawed  the same, with sg-b3's overclaim appended to the conclusion (sg_b3_flaw.flawed, unchanged)
    drift-own-clean, drift-own-flawed   sg-b3's own-turn cells re-graded on 10 drift studies (sg_followups.drift)
Archived (reused): sg-b3's own-clean, own-flawed and fresh-clean, fresh-flawed grades of the same texts.

Studies: Haiku all 60; Sonnet and Opus the same 30 of 60, stratified by domain (seed "items").
Per model, per study: q = quoted-clean - quoted-flawed; o = own-clean - own-flawed (archived); T = q - o.
Reading (Haiku, Opus): turn role if T >= H (half the model's sg-b3 G: Haiku 6.3, Opus 3.0) with the 20-domain cluster
CI lower > 0 AND F = own-flawed - quoted-flawed with cluster CI lower > 0; layout if T's cluster CI upper < H;
undetermined otherwise; untestable if the gate (mean q >= 10, cluster CI lower > 0) fails, the usable share is under
0.9, or the drift check fires. Sonnet: T reported, no reading scored.
Verdict: untestable if Haiku or Opus is untestable; pass if both read turn role; fail-layout if both read layout;
mixed otherwise.
"""
import json
import random
import sys

import numpy as np

from sg_b3_flaw import conclusions, flawed, sha
from sg_common import DATA, MODELS, RESULTS, SHORT, Caller, call, int_schema
from sg_followups import (archive_b3, cluster_boot_ci, drift, drift_studies, ge, gt, lt, pilot_tasks,
                          stratified_half, test_tasks)
from sg_prompts import own_turn, quoted
from sg_stats import boot_ci

BET = "sg-b4"
CAP = 0.50                 # from sg-b3's cost per grade call: Haiku $0.00008, Sonnet $0.0016, Opus $0.0036 (300 calls)
PILOT_CAP = 0.03
GATE = 10.0
H = {"haiku": 6.3, "opus": 3.0}          # half of each model's sg-b3 G (12.58, 5.97), as on the map and the card
SONNET_H = 0.69                          # half of Sonnet's sg-b3 G (1.37); reported only
HALF = ("claude-sonnet-5-5", "claude-opus-5-5")
NEW = ("quoted-clean", "quoted-flawed")
DRIFT = ("drift-own-clean", "drift-own-flawed")
ORDER = ("claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5")


def seeds():
    return json.loads((DATA / f"{BET}-seed.json").read_text())["seeds"]


def study_sets(ts, s=None):
    s = s or seeds()
    half = stratified_half(ts, s["items"])
    sets = {m: (sorted(t["id"] for t in ts) if m not in HALF else half) for m in MODELS}
    dr = drift_studies(half, ts, s["items"] + 1)
    return sets, dr


def messages(cell, task, conclusion):
    c = flawed(conclusion, task) if cell.endswith("flawed") else conclusion
    if cell.startswith("quoted"):
        return quoted(task["study"], c)
    return own_turn(task["study"], c)


def check_frozen():
    """The grade question, the lead-in and the overclaim are sg-b3's, word for word (sg-b3 D9e)."""
    from sg_b3_flaw import check_frozen_prompts
    import sg_prompts
    check_frozen_prompts()
    q = sg_prompts.QUOTED
    if not q.endswith(sg_prompts.GRADE_ABOVE) or q.count(sg_prompts.GRADE_ABOVE) != 1:
        raise SystemExit("QUOTED must end with sg-b3's GRADE_ABOVE, once")
    m = quoted("S", "C")[0]["content"]
    if sg_prompts.WRITE.format(study="S") not in m or "\"\"\"\nC\n\"\"\"" not in m or "you" in m.split("User:")[0].lower():
        raise SystemExit("QUOTED does not carry the request and conclusion as quoted blocks, or names an author")


def run(pilot=False, caller_cls=Caller, call_fn=call, concl=None, ts=None, check=True):
    ts = ts if ts is not None else (pilot_tasks() if pilot else test_tasks())
    cs = concl if concl is not None else conclusions(pilot)
    if check:
        check_frozen()
        arch = archive_b3(pilot)
        for m in MODELS:
            for t in ts:
                if (m, t["id"]) not in cs:
                    raise SystemExit(f"{BET}: conclusion missing {m} {t['id']}")
                for c in ("own-clean", "own-flawed"):
                    g = arch.get((m, t["id"], c))
                    if g is None or g[1] != sha(cs[(m, t["id"])]):
                        raise SystemExit(f"{BET}: archived sg-b3 cell missing or mismatched {m} {t['id']} {c}")
    if pilot:
        sets = {m: [t["id"] for t in ts] for m in MODELS if m != "claude-sonnet-5-5"}
        dr = []
    else:
        sets, dr = study_sets(ts)
    tmap = {t["id"]: t for t in ts}
    rng = random.Random(seeds()["order"] if not pilot else 7)
    jobs = []
    for m in ORDER:                        # model by model, shuffled within: a cap stop leaves whole models
        if m not in sets:
            continue
        js = [(f"grade|{m}|{tid}|{c}", m, tmap[tid], c, cs[(m, tid)]) for tid in sets[m] for c in NEW]
        js += [(f"grade|{m}|{tid}|{c}", m, tmap[tid], c, cs[(m, tid)]) for tid in dr for c in DRIFT]
        rng.shuffle(js)
        jobs += js
    g = caller_cls(RESULTS / f"{BET}-grade-calls{'-pilot' if pilot else ''}.json", PILOT_CAP if pilot else CAP, f"{BET} grade")

    def do(job):
        _, m, t, c, concl_ = job
        cell = c.replace("drift-", "")
        out, cost, rid = call_fn(messages(cell, t, concl_), m, f"{BET} grade {c}", max_tokens=40, schema=int_schema("grade"))
        return {"model": m, "task": t["id"], "cond": c, "grade": out["grade"], "conclusion_sha": sha(concl_), "cost": cost,
                "request_id": rid}

    g.run(jobs, do, workers=4)
    return g


def per_model(new, arch, model, ids, dom, dr_ids, seed, n_expected, robust=True):
    """new: {(task, cond): grade}; arch: {(task, cond): grade} (sg-b3)."""
    k = SHORT[model]
    ok = [t for t in ids if all(0 <= new.get((t, c), -1) <= 100 for c in NEW)
          and all((t, c) in arch for c in ("own-clean", "own-flawed", "fresh-clean", "fresh-flawed"))]
    out = {"model": model, "n_tasks": n_expected, "n_usable": len(ok), "usable_share": len(ok) / n_expected}
    if len(ok) < 2:
        out["reading"] = "untestable"
        return out
    cl = [dom[t] for t in ok]
    q = [new[(t, "quoted-clean")] - new[(t, "quoted-flawed")] for t in ok]
    o = [arch[(t, "own-clean")] - arch[(t, "own-flawed")] for t in ok]
    f = [arch[(t, "fresh-clean")] - arch[(t, "fresh-flawed")] for t in ok]
    T = [a - b for a, b in zip(q, o)]
    F = [arch[(t, "own-flawed")] - new[(t, "quoted-flawed")] for t in ok]
    L = [a - b for a, b in zip(f, q)]
    C = [new[(t, "quoted-clean")] - arch[(t, "own-clean")] for t in ok]
    Tci, Fci, qci = cluster_boot_ci(T, cl, seed), cluster_boot_ci(F, cl, seed + 1), cluster_boot_ci(q, cl, seed + 2)
    gate_ok = ge(float(np.mean(q)), GATE) and gt(qci[0], 0)
    reg = {t: new[(t, "drift-own-clean")] - new[(t, "drift-own-flawed")] for t in dr_ids
           if (t, "drift-own-clean") in new and (t, "drift-own-flawed") in new}
    dri = (drift(reg, {t: arch[(t, "own-clean")] - arch[(t, "own-flawed")] for t in reg}, seed + 3) if dr_ids else
           {"n": 0, "mean": None, "ci": None, "fires": False, "note": "no drift studies (pilot or synthetic data only)"})
    out.update(T=float(np.mean(T)), T_ci=list(Tci), T_ci_study=list(boot_ci(T, seed)),
               F=float(np.mean(F)), F_ci=list(Fci), q=float(np.mean(q)), q_ci=list(qci), gate_ok=gate_ok,
               o=float(np.mean(o)), G_b3_subset=float(np.mean([a - b for a, b in zip(f, o)])),
               L=float(np.mean(L)), L_ci=list(cluster_boot_ci(L, cl, seed + 4)),
               clean_shift=float(np.mean(C)), clean_shift_ci=list(cluster_boot_ci(C, cl, seed + 5)),
               mean={c: float(np.mean([new[(t, c)] for t in ok])) for c in NEW},
               mean_archived={c: float(np.mean([arch[(t, c)] for t in ok]))
                              for c in ("own-clean", "own-flawed", "fresh-clean", "fresh-flawed")},
               drift=dri, T_adj=(float(np.mean(T)) - dri["mean"]) if dri["mean"] is not None else None,
               sd_T=float(np.std(T, ddof=1)), tasks=ok, diffs=T)
    bar = H.get(k)

    def read(keep, card=False, study=False):
        Ts, Fs, cs_ = [T[i] for i in keep], [F[i] for i in keep], [cl[i] for i in keep]
        if not (out["usable_share"] >= 0.9 and gate_ok and not dri["fires"]):
            return "untestable"
        if bar is None:
            return "reported only"
        ci = boot_ci(Ts, seed) if study else cluster_boot_ci(Ts, cs_, seed, n=2000 if len(keep) < len(T) else 10000)
        fci = boot_ci(Fs, seed + 1) if study else cluster_boot_ci(Fs, cs_, seed + 1, n=2000 if len(keep) < len(T) else 10000)
        m = float(np.mean(Ts))
        if ge(m, bar) and gt(ci[0], 0) and (card or gt(fci[0], 0)):
            return "turn role"
        if lt(ci[1], bar):
            return "layout"
        return "undetermined"

    allk = list(range(len(T)))
    out["reading"] = read(allk)
    out["reading_card_event"] = read(allk, card=True)          # Sean's card's event: no F guard (secondary)
    out["reading_study_bootstrap"] = read(allk, study=True)    # beside the bar, never used for it
    if not robust:
        return out
    loo_s = [read([j for j in allk if j != i]) for i in allk]
    loo_d = {d: read([j for j in allk if cl[j] != d]) for d in sorted(set(cl))}
    out["robustness"] = {"fragile_study": any(r != out["reading"] for r in loo_s),
                         "study_drops_changing": [(ok[i], r) for i, r in enumerate(loo_s) if r != out["reading"]][:5],
                         "fragile_domain": any(r != out["reading"] for r in loo_d.values()),
                         "domain_drops_changing": {d: r for d, r in loo_d.items() if r != out["reading"]},
                         "n_ties": sum(1 for x in T if x == 0),
                         "ties_excluded_mean": float(np.mean([x for x in T if x != 0])) if any(x != 0 for x in T) else None}
    if bar is None:
        out["sonnet_note"] = f"T against half its sg-b3 G ({SONNET_H}) is reported only"
    return out


def verdict(readings):
    h, o = readings["haiku"], readings["opus"]
    if "untestable" in (h, o):
        return "untestable"
    if h == o == "turn role":
        return "pass"
    if h == o == "layout":
        return "fail-layout"
    return "mixed"


def analyse(pilot=False, grade_cache=None, arch=None, concl=None, ts=None, s=None):
    gc = grade_cache if grade_cache is not None else json.loads(
        (RESULTS / f"{BET}-grade-calls{'-pilot' if pilot else ''}.json").read_text())
    ts = ts if ts is not None else (pilot_tasks() if pilot else test_tasks())
    cs = concl if concl is not None else conclusions(pilot)
    mism = [k for k, v in gc.items() if sha(cs[(v["model"], v["task"])]) != v["conclusion_sha"]]
    if mism:
        raise SystemExit(f"{len(mism)} grade records do not match sg-b1's conclusions, e.g. {mism[:3]}")
    a = arch if arch is not None else archive_b3(pilot)
    if arch is None:
        bad = [k for k, (g, h) in a.items() if (k[0], k[1]) in cs and sha(cs[(k[0], k[1])]) != h]
        if bad:
            raise SystemExit(f"{len(bad)} archived sg-b3 grades do not match sg-b1's conclusions")
    dom = {t["id"]: t["domain"] for t in ts}
    s = s or seeds()
    if pilot:
        sets, dr = {m: sorted(dom) for m in MODELS}, []
    else:
        sets, dr = study_sets(ts, s)
    res = {}
    for m in MODELS:
        new = {(v["task"], v["cond"]): v["grade"] for v in gc.values() if v["model"] == m}
        am = {(t, c): g for (mm, t, c), (g, _) in a.items() if mm == m}
        res[SHORT[m]] = per_model(new, am, m, sets[m], dom, dr, s["boot"], len(sets[m]))
    readings = {k: r["reading"] for k, r in res.items()}
    return {"bet": BET, "pilot": pilot, "study_sets": {SHORT[m]: v for m, v in sets.items()}, "drift_studies": dr,
            "per_model": res, "readings": readings, "verdict": verdict(readings),
            "verdict_card_event": verdict({k: r.get("reading_card_event", r["reading"]) for k, r in res.items()}),
            "spend_usd": sum(v["cost"] for v in gc.values()),
            "spend_by_model": {SHORT[m]: round(sum(v["cost"] for v in gc.values() if v["model"] == m), 5) for m in MODELS}}


# ---------------------------------------------------------------- dry run (no calls) ---------------------------------
REPEAT_SD = {"claude-haiku-5-5": 1.5 / 2 ** .5, "claude-sonnet-5-5": 1.62 / 2 ** .5, "claude-opus-5-5": 2.27 / 2 ** .5}
# per-cell repeat noise: SD of (fresh2 - fresh) in sg-b1's archive (1.50, 1.62, 2.27 points), divided by sqrt 2 (P15)


def simulate(world, reps=200, seed=5):
    """Quoted cells built from sg-b3's archived per-study cells plus measured repeat noise (P15, P16).
    world: 'turn role' (quoted = archived fresh), 'layout' (quoted = archived own), 'half' (quoted gap = own gap +
    half the model's G, the bar exactly), 'drift +3' (turn role, but today's own gap is 3 points larger),
    'harsh-quoted' (quoted = own - 8 on both cells), 'item-property' (quoted = fresh on the 14 studies whose interval
    excludes 0, own elsewhere: an item property reaching T directly)."""
    ts = test_tasks()
    dom = {t["id"]: t["domain"] for t in ts}
    excl = {t["id"] for t in ts if t["ci_excludes_0"]}
    a = archive_b3()
    s = {"items": 11, "boot": 12, "order": 13}
    sets, dr = study_sets(ts, s)
    rng = np.random.default_rng(seed)
    clip = lambda x: int(np.clip(np.round(x), 0, 100))
    tal = {}
    reads = {"haiku": {}, "opus": {}}
    for _ in range(reps):
        res = {}
        for m in MODELS:
            am = {(t, c): g for (mm, t, c), (g, _) in a.items() if mm == m}
            sd = REPEAT_SD[m]
            new = {}
            for t in sets[m]:
                for c in ("clean", "flawed"):
                    own, fr = am[(t, f"own-{c}")], am[(t, f"fresh-{c}")]
                    if world in ("turn role", "drift +3"):
                        base = fr
                    elif world == "layout":
                        base = own
                    elif world == "half":
                        G = (am[(t, "fresh-clean")] - am[(t, "fresh-flawed")]) - (am[(t, "own-clean")] - am[(t, "own-flawed")])
                        base = own - (G / 2 if c == "flawed" else 0)
                    elif world == "harsh-quoted":
                        base = own - 8
                    elif world == "item-property":
                        base = fr if t in excl else own
                    new[(t, f"quoted-{c}")] = clip(base + rng.normal(0, sd))
            for t in dr:
                for c in ("clean", "flawed"):
                    sh = 3.0 if (world == "drift +3" and c == "clean") else 0.0
                    new[(t, f"drift-own-{c}")] = clip(am[(t, f"own-{c}")] + sh + rng.normal(0, sd))
            res[SHORT[m]] = per_model(new, am, m, sets[m], dom, dr, int(rng.integers(1 << 30)), len(sets[m]), robust=False)
        v = verdict({k: r["reading"] for k, r in res.items()})
        tal[v] = tal.get(v, 0) + 1
        for k in reads:
            r = res[k]["reading"]
            reads[k][r] = reads[k].get(r, 0) + 1
    return {k: round(x / reps, 3) for k, x in sorted(tal.items())}, reads


def dryrun():
    """D2: the quoted cell differs from the own-turn cell only in layout; D3: a flaw-blind grader is untestable;
    P13: the bar exactly on the boundary; D11/P12: P(pass), P(fail) in worlds built from the archive."""
    check_frozen()
    print("D10 frozen strings: sg-b3's prompts unchanged; QUOTED ends with GRADE_ABOVE")
    t = test_tasks()[0]
    c = "The data show a small difference whose interval includes zero."
    for cell in ("quoted-clean", "quoted-flawed", "own-clean"):
        ms = messages(cell, t, c)
        print("D2", cell, len(ms), "message(s); last 160 chars:", repr(ms[-1]["content"][-160:]))
    ts = test_tasks()
    sets, dr = study_sets(ts, {"items": 11, "boot": 12, "order": 13})
    dom = {x["id"]: x["domain"] for x in ts}
    print("design: Opus/Sonnet set", len(sets["claude-opus-5-5"]), "studies over", len({dom[x] for x in sets["claude-opus-5-5"]}),
          "domains; drift studies", len(dr), "over", len({dom[x] for x in dr}), "domains (dummy seed 11)")
    ids = [f"t{i:02d}" for i in range(1, 61)]
    dm = {t: i % 20 for i, t in enumerate(ids)}
    arch = {(t, c): v for t in ids for c, v in (("own-clean", 90), ("own-flawed", 20), ("fresh-clean", 90), ("fresh-flawed", 10))}
    blind = {(t, c): 90 for t in ids for c in NEW}
    r = per_model(blind, arch, "claude-haiku-5-5", ids, dm, [], 1, 60)
    assert r["reading"] == "untestable" and not r["gate_ok"]
    print("D3 a flaw-blind quoted grader -> untestable (gate fires)")
    exact = {(t, "quoted-clean"): 90 for t in ids}
    exact.update({(t, "quoted-flawed"): 20 - (6 if i % 2 else 7) for i, t in enumerate(ids)})   # T = 6.5 mean
    r = per_model(exact, arch, "claude-haiku-5-5", ids, dm, [], 1, 60)
    print("P13 Haiku T", r["T"], "->", r["reading"])
    exact2 = {(t, "quoted-clean"): 90 for t in ids}
    exact2.update({(t, "quoted-flawed"): 20 - (6 if i % 10 else 9) for i, t in enumerate(ids)})  # T = 6.3 exactly
    r = per_model(exact2, arch, "claude-haiku-5-5", ids, dm, [], 1, 60)
    print("P13 Haiku T exactly", round(r["T"], 12), "(bar 6.3) ->", r["reading"])
    assert r["reading"] == "turn role"
    for w in ("turn role", "layout", "half", "drift +3", "harsh-quoted", "item-property"):
        v, rd = simulate(w)
        print("world", repr(w), "verdict", v, "| readings", rd)


def stubrun():
    """End to end with no paid call, on the real tasks, conclusions and sg-b3 archive; the stub grades the quoted cell
    as sg-b3's fresh cell (turn role world)."""
    import tempfile
    import threading
    from pathlib import Path
    tmp = Path(tempfile.mkdtemp())
    a = archive_b3()

    class StubCaller(Caller):
        def __init__(self, path, cap, label):
            self.path, self.cap, self.label, self.cache, self.other = tmp / Path(path).name, cap, label, {}, 0.0
            self.lock, self.stop, self.refusal, self.errors, self.capped = threading.Lock(), threading.Event(), {}, [], ""

        def run(self, jobs, fn, workers=1):
            for j in jobs:
                self.cache[j[0]] = fn(j)

    tid = {t["study"]: t["id"] for t in test_tasks()}

    def stub_call(msgs, model, name, max_tokens=60, schema=None):
        text = msgs[-1]["content"] if len(msgs) == 1 else msgs[0]["content"]
        t = next(v for k, v in tid.items() if k in text)
        body = msgs[-1]["content"] if len(msgs) == 1 else msgs[1]["content"]
        src = ("fresh" if len(msgs) == 1 else "own") + ("-flawed" if "This proves that" in body else "-clean")
        return {"grade": a[(model, t, src)][0]}, 0.0, None

    global seeds
    so = seeds
    seeds = lambda: {"items": 11, "boot": 12, "order": 13}
    try:
        g = run(False, caller_cls=StubCaller, call_fn=stub_call)
        r = analyse(False, grade_cache=g.cache)
    finally:
        seeds = so
    n = {SHORT[m]: sum(1 for v in g.cache.values() if v["model"] == m) for m in MODELS}
    print("stub calls by model", n, "| order model-by-model:",
          [k.split("|")[1] for k in g.cache] == sorted([k.split("|")[1] for k in g.cache], key=lambda m: ORDER.index(m)))
    for k, v in r["per_model"].items():
        print("stub", k, "T", round(v["T"], 2), [round(x, 2) for x in v["T_ci"]], "F", round(v["F"], 2), "drift",
              v["drift"]["mean"], v["reading"])
    print("stub verdict", r["verdict"])


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "dryrun"
    pilot = "--pilot" in sys.argv
    if cmd == "run":
        run(pilot)
    elif cmd == "analyse":
        r = analyse(pilot)
        (RESULTS / f"{BET}-analysis{'-pilot' if pilot else ''}.json").write_text(json.dumps(r, indent=1))
        print(json.dumps({k: v for k, v in r.items() if k != "per_model"}, indent=1))
        for k, v in r["per_model"].items():
            print(k, {x: v.get(x) for x in ("n_usable", "T", "T_ci", "F", "F_ci", "q", "drift", "reading")})
    else:
        dryrun()
        stubrun()

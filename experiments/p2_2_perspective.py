"""P2-2, perspective-filter equivalence, as pre-registered in experiments/p2-2-perspective.md (D2). $1.25 cap.

    python experiments/p2_2_perspective.py items      # parse BigToM into data/p2-2-items.json (no API)
    python experiments/p2_2_perspective.py            # run steps 1-4 (cached), then analyse
    python experiments/p2_2_perspective.py --analyse

Items: BigToM (Gandhi et al. 2023, MIT licence), 200 templates, forward belief, true belief (TB) and false belief (FB).
Calls cached in results/p2-2-calls.json; second-person rewrites in data/p2-2-second-person.json."""

import csv
import json
import re
import sys

import numpy as np

import om_common as om

RAW = om.DATA / "raw" / "bigtom" / "procedural-evals-tom-main" / "data" / "bigtom" / "bigtom.csv"
ITEMS, REWRITE = om.DATA / "p2-2-items.json", om.DATA / "p2-2-second-person.json"
CACHE, OUT = om.RESULTS / "p2-2-calls.json", om.RESULTS / "p2-2-perspective.json"
R, CAP, SEED, SUB_SEED = 10, 1.25, 2201, 2202
TAIL = f"Give an integer from 0 to 100, where {om.SCALE}."


# --- items ------------------------------------------------------------------------------------------------

def parse():
    rows = [[x.strip() for x in ",".join(r).split(";")] for r in csv.reader(open(RAW))]
    items = []
    for i, r in enumerate(rows):
        name, X = r[11].split(" believes ", 1)
        sents = re.split(r"(?<=[.!?])\s+", r[0])
        Xc = r[8].split(" believes ", 1)[1] if " believes " in r[8] else None
        items.append({"t": i, "name": name, "pre": " ".join(sents[:-1]), "event": sents[-1], "aware": r[1],
                      "not_aware": r[2], "X": X.rstrip("."), "Xc": Xc.rstrip(".") if Xc else None})
    ITEMS.write_text(json.dumps(items, indent=1))
    print(f"{len(items)} templates; {sum(it['Xc'] is not None for it in items)} with a complementary statement")


def subset(items):
    """The 50 templates for the 2 x 2 and the order arm: a seeded draw among templates with a complementary statement."""
    pool = [it["t"] for it in items if it["Xc"]]
    return sorted(np.random.default_rng(SUB_SEED).choice(pool, 50, replace=False).tolist())


# --- stories ------------------------------------------------------------------------------------------------

def story(it, person, filtered, cond, sp):
    """person 3: original text; person 2: the second-person rewrite. filtered: drop what the agent did not see."""
    src = it if person == 3 else sp
    parts = [src["pre"]]
    if not (filtered and cond == "FB"):
        parts += [src["event"], src["aware"] if cond == "TB" else src["not_aware"]]
    return " ".join(parts)


def question(it, person, x):
    if person == 3:
        return f"How likely is it that {it['name']} believes that {x}? " + TAIL
    return f"How likely is it that {x}? " + TAIL


def opening(person):
    return "Here is a story.\n\n" if person == 3 else "Imagine that you are the person in this situation.\n\n"


CELLS = {"i": (3, False), "ii": (2, True), "3f": (3, True), "2u": (2, False)}   # (person, filtered)


# --- calls --------------------------------------------------------------------------------------------------

REWRITE_SCHEMA = {"type": "object", "properties": {k: {"type": "string"} for k in ("pre", "event", "aware", "not_aware")},
                  "required": ["pre", "event", "aware", "not_aware"], "additionalProperties": False}


def rewrite_prompt(it):
    return (f"Rewrite each of the four passages below in the second person, so that {it['name']} is addressed as \"you\". "
            "Change only the grammatical person: the name, the pronouns and the verb agreement. Do not add, remove or "
            "change any information, and keep every other word as it is.\n\n"
            f"pre: {it['pre']}\n\nevent: {it['event']}\n\naware: {it['aware']}\n\nnot_aware: {it['not_aware']}")


def rewrite_ok(it, sp):
    """Frozen check: the name is gone from every passage, 'you' appears in pre, and each length is 60-150% of the original."""
    for k in ("pre", "event", "aware", "not_aware"):
        if it["name"] in sp[k] or not (0.6 <= len(sp[k]) / max(1, len(it[k])) <= 1.5):
            return False
    return bool(re.search(r"\byou\b", sp["pre"], re.I))


def jobs(items, sub):
    out = []
    for r in range(R):                                      # step 2: primary cells, repeat-major
        for it in items:
            for cond in ("TB", "FB"):
                for cell in ("i", "ii"):
                    out.append((f"{it['t']}|{cond}|{cell}|single|{r}", it, cond, cell, "single", r))
    for r in range(R):                                      # step 3: the other two cells of the 2 x 2, FB only
        for t in sub:                                       # (in TB the filtered story is the full story, so 3f = i, 2u = ii)
            for cell in ("3f", "2u"):
                out.append((f"{t}|FB|{cell}|single|{r}", items[t], "FB", cell, "single", r))
    for r in range(R):                                      # step 4: order arm (complement first)
        for t in sub:
            for cond in ("TB", "FB"):
                for cell in ("i", "ii"):
                    out.append((f"{t}|{cond}|{cell}|after|{r}", items[t], cond, cell, "after", r))
    return out


def run():
    items = json.loads(ITEMS.read_text())
    sub = subset(items)
    c = om.Caller(CACHE, CAP, "P2-2 perspective")

    # step 1: second-person rewrites (cached in the same call cache, then exported)
    def rw(job):
        _, it = job
        d, cost, rid = om.structured([{"role": "user", "content": rewrite_prompt(it)}], REWRITE_SCHEMA, "p2-2-rewrite",
                                     max_tokens=1000)
        return {"value": d, "cost": cost, "request_id": rid}
    c.run([(f"rewrite|{it['t']}", it) for it in items], rw)
    sp = {it["t"]: c.cache[f"rewrite|{it['t']}"]["value"] for it in items}
    REWRITE.write_text(json.dumps({str(k): v for k, v in sp.items()}, indent=1))
    ok = {t for t in sp if rewrite_ok(items[t], sp[t])}
    print(f"rewrites passing the frozen check: {len(ok)} of {len(items)}")

    def call(job):
        _, it, cond, cell, kind, r = job
        person, filt = CELLS[cell]
        head = opening(person) + story(it, person, filt, cond, sp[it["t"]]) + "\n\n"
        if kind == "single":
            msgs = [{"role": "user", "content": head + question(it, person, it["X"])}]
            d, cost, rid = om.structured(msgs, om.int_schema(), "p2-2")
            return {"value": d["rating"], "cost": cost, "request_id": rid}
        msgs = [{"role": "user", "content": head + question(it, person, it["Xc"])}]
        d1, c1, rid1 = om.structured(msgs, om.int_schema(), "p2-2")
        msgs += [{"role": "assistant", "content": json.dumps(d1)}, {"role": "user", "content": question(it, person, it["X"])}]
        d2, c2, rid2 = om.structured(msgs, om.int_schema(), "p2-2")
        return {"value": d2["rating"], "first": d1["rating"], "cost": c1 + c2, "request_id": [rid1, rid2]}
    c.run([j for j in jobs(items, sub) if CELLS[j[3]][0] == 3 or j[1]["t"] in ok], call)


# --- analysis -----------------------------------------------------------------------------------------------

def analyse():
    items = json.loads(ITEMS.read_text())
    sub = subset(items)
    cache = json.loads(CACHE.read_text())
    sp = {int(k): v for k, v in json.loads(REWRITE.read_text()).items()}
    ok = sorted(t for t in sp if rewrite_ok(items[t], sp[t]))

    def M(ts, cond, cell, kind="single"):
        Y = np.full((len(ts), R), np.nan)
        for a, t in enumerate(ts):
            for r in range(R):
                v = cache.get(f"{t}|{cond}|{cell}|{kind}|{r}")
                if v is not None and isinstance(v.get("value"), int):
                    Y[a, r] = min(100, max(0, v["value"]))
        return Y

    def stack(ts, cell, conds=("TB", "FB"), kind="single"):
        return np.vstack([M(ts, c, cell, kind) for c in conds])

    def clusters(n_t, n_c):     # each template's items travel together
        return [np.array([j * n_t + a for j in range(n_c)]) for a in range(n_t)]

    out = {"templates": len(items), "rewrites_ok": len(ok), "subset": sub, "calls": len(cache),
           "cost_usd": round(sum(v["cost"] for v in cache.values()), 4)}
    T = ok
    Yi, Yii = stack(T, "i"), stack(T, "ii")
    out["missing_primary"] = int(np.isnan(Yi).sum() + np.isnan(Yii).sum())
    cl2 = clusters(len(T), 2)
    Qf = lambda A, B: (lambda idx: om.q_ratio(A[idx], B[idx]))
    out["primary"] = {"n_items": 2 * len(T), "Q": float(om.q_ratio(Yi, Yii)), "Q_ci": om.cluster_boot(Qf(Yi, Yii), cl2, SEED),
                      "rel_i": float(om.split_half_reliability(Yi)), "rel_ii": float(om.split_half_reliability(Yii)),
                      "r": float(np.corrcoef(np.nanmean(Yi, 1), np.nanmean(Yii, 1))[0, 1])}
    cl1 = clusters(len(T), 1)
    for cond in ("TB", "FB"):
        A, B = M(T, cond, "i"), M(T, cond, "ii")
        out[f"within_{cond}"] = {"Q": float(om.q_ratio(A, B)), "Q_ci": om.cluster_boot(Qf(A, B), cl1, SEED + 1),
                                 "rel_i": float(om.split_half_reliability(A)), "rel_ii": float(om.split_half_reliability(B)),
                                 "mean_i": float(np.nanmean(A)), "mean_ii": float(np.nanmean(B)),
                                 "shift_ii_minus_i": float(np.nanmean(B) - np.nanmean(A)),
                                 "shift_ci": om.cluster_boot(lambda idx: float(np.nanmean(B[idx]) - np.nanmean(A[idx])), cl1, SEED + 2)}
    for cell in ("i", "ii"):
        tb, fb = M(T, "TB", cell), M(T, "FB", cell)
        g = lambda idx: float(np.nanmean(fb[idx]) - np.nanmean(tb[idx]))
        out[f"gap_FB_minus_TB_{cell}"] = [g(np.arange(len(T))), *om.cluster_boot(g, cl1, SEED + 3)]

    # 2 x 2 on the subset (rewrite-checked templates only)
    S = [t for t in sub if t in set(ok)]
    out["subset_n"] = len(S)
    tab = {}
    for cell in CELLS:
        for cond in (("TB", "FB") if cell in ("i", "ii") else ("FB",)):
            tab[f"{cell}|{cond}"] = float(np.nanmean(M(S, cond, cell)))
    out["two_by_two_means"] = tab
    for cond in ("FB",):    # person effect (2 - 3) at fixed filtering; filtering effect (filtered - full) at fixed person
        m = {c: M(S, cond, c) for c in CELLS}
        eff = {"person_effect_full": ("2u", "i"), "person_effect_filtered": ("ii", "3f"),
               "filter_effect_3rd": ("3f", "i"), "filter_effect_2nd": ("ii", "2u")}
        for name, (a, b) in eff.items():
            f = lambda idx, a=a, b=b: float(np.nanmean(m[a][idx]) - np.nanmean(m[b][idx]))
            out[f"{name}_{cond}"] = [f(np.arange(len(S))), *om.cluster_boot(f, clusters(len(S), 1), SEED + 4)]
    # order arm
    for cell in ("i", "ii"):
        for cond in ("TB", "FB"):
            a, s = M(S, cond, cell, "after"), M(S, cond, cell)
            f = lambda idx, a=a, s=s: float(np.nanmean(a[idx]) - np.nanmean(s[idx]))
            out[f"order_effect_{cell}_{cond}"] = [f(np.arange(len(S))), *om.cluster_boot(f, clusters(len(S), 1), SEED + 5)]

    # leave-one-template-out range for the primary
    loo = [om.q_ratio(np.delete(Yi, [a, a + len(T)], 0), np.delete(Yii, [a, a + len(T)], 0)) for a in range(len(T))]
    out["primary_loo_Q_range"] = [float(min(loo)), float(max(loo))]

    p = out["primary"]
    if len(T) < 150 or p["rel_i"] < 0.5 or p["rel_ii"] < 0.5 or out["missing_primary"] > 0.05 * Yi.size * 2:
        v = "untestable"
    elif p["Q"] >= 0.80:
        v = "pass, imprecise" if p["Q_ci"][0] < 0.70 else "pass"
    else:
        v = "fail"
    out["primary_verdict"] = v
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    if sys.argv[1:2] == ["items"]:
        parse()
    else:
        if "--analyse" not in sys.argv:
            run()
        analyse()

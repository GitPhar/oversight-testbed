"""P2-3, SimpleToM decomposed: is the "stated but not used" gap a memory effect? As pre-registered in
experiments/p2-3-simpletom.md (D4). $1.75 cap; any refusal stops the run (and the wave).

    python experiments/p2_3_simpletom.py items     # join SimpleToM into data/p2-3-items.json (no API)
    python experiments/p2_3_simpletom.py           # run (cached), then analyse; needs data/p2-3-seed.json
    python experiments/p2_3_simpletom.py --analyse

Items: SimpleToM (Gu et al. 2024, allenai/SimpleToM, ODC-BY), all 1,147 stories; mental-state (aware), behaviour
(action) and judgment (judge) questions. Calls cached in results/p2-3-calls.json."""

import json
import sys

import numpy as np

import om_common as om

RAW = om.DATA / "raw" / "simpletom"
ITEMS, CACHE = om.DATA / "p2-3-items.json", om.RESULTS / "p2-3-calls.json"
OUT, SEEDF = om.RESULTS / "p2-3-simpletom.json", om.DATA / "p2-3-seed.json"
CAP = 1.75
CONDS = ["c1_not_asked", "c2_filler", "c3_redacted", "c4_remind_own", "c5_planted_own", "c6_planted_other"]
QS = ["action", "judge"]
AB = om.enum_schema(["A", "B"])
FILL = om.enum_schema(["continue"], field="reply")


def parse():
    rows = {}
    for sub, kind in (("mental-state-qa", "aware"), ("behavior-qa", "action"), ("judgment-qa", "judge")):
        for line in open(RAW / sub / "test.jsonl"):
            if line.strip():
                d = json.loads(line)
                sid = d["id"].rsplit("_", 1)[0]
                r = rows.setdefault(sid, {"id": sid, "story": d["story"]})
                assert r["story"] == d["story"]
                r[kind] = {"question": d["question"], "choices": d["choices"]["text"], "labels": d["choices"]["label"],
                           "correct": d["answerKey"]}
    core = {}
    for line in open(RAW / "story-data" / "test.jsonl"):
        if line.strip():
            d = json.loads(line)
            core[d["story_id"]] = (d["core_id"], d["severity_original"])
    items = []
    for sid, r in rows.items():
        r["core_id"], r["severity"] = core[sid]
        r["wrong_ms"] = next(l for l in r["aware"]["labels"] if l != r["aware"]["correct"])   # the "aware" answer
        items.append(r)
    ITEMS.write_text(json.dumps(items, indent=1))
    print(f"{len(items)} stories, {len({i['core_id'] for i in items})} core scenarios")


def mc(q):
    opts = "\n".join(f"({l}) {t}" for l, t in zip(q["labels"], q["choices"]))
    return f"{q['question']}\n{opts}\n\nAnswer with the letter of the better option."


def option(q, label):
    return f"({label}) {q['choices'][q['labels'].index(label)]}"


def messages(it, cond, qkind, own_ms):
    """The conversation up to the target question (behaviour or judgment)."""
    target, ms = mc(it[qkind]), mc(it["aware"])
    head = it["story"] + "\n\n"
    if cond == "c1_not_asked":
        return [{"role": "user", "content": head + target}], AB
    if cond == "c2_filler":
        turn1, reply = head + "Reply with the single word: continue", json.dumps({"reply": "continue"})
    else:
        turn1 = head + ms
        reply = {"c3_redacted": "[answer recorded]", "c4_remind_own": json.dumps({"answer": own_ms}),
                 "c5_planted_own": json.dumps({"answer": it["wrong_ms"]}), "c6_planted_other": "[answer recorded]"}[cond]
    second = target
    if cond == "c6_planted_other":
        second = f"Another reader answered that question: {option(it['aware'], it['wrong_ms'])}\n\n" + target
    return [{"role": "user", "content": turn1}, {"role": "assistant", "content": reply},
            {"role": "user", "content": second}], AB


def jobs(items):
    out = [(f"ms|{it['id']}", "ms", it, None, None) for it in items]          # step 1: the model's own MS answers
    for qkind in QS:                                                          # steps 2-3: behaviour, then judgment
        for it in items:
            for cond in CONDS:
                out.append((f"{qkind}|{cond}|{it['id']}", "target", it, cond, qkind))
    return out


def run():
    items = json.loads(ITEMS.read_text())
    c = om.Caller(CACHE, CAP, "P2-3 SimpleToM")

    def call(job):
        _, kind, it, cond, qkind = job
        if kind == "ms":
            msgs = [{"role": "user", "content": it["story"] + "\n\n" + mc(it["aware"])}]
        else:
            msgs, _ = messages(it, cond, qkind, c.cache[f"ms|{it['id']}"]["value"])
        d, cost, rid = om.structured(msgs, AB, "p2-3", max_tokens=50)
        return {"value": d["answer"], "cost": cost, "request_id": rid}
    J = jobs(items)
    c.run(J[:len(items)], call)          # all MS answers first (condition 4 needs them)
    c.run(J[len(items):], call)


def analyse():
    items = json.loads(ITEMS.read_text())
    cache = json.loads(CACHE.read_text())
    seed = json.loads(SEEDF.read_text())["seed32_boot"]
    cores = sorted({it["core_id"] for it in items})
    by_core = {cid: [i for i, it in enumerate(items) if it["core_id"] == cid] for cid in cores}

    def resp(qkind, cond):
        """Per story: 1 if the answer is the 'aware' (incorrect) option, 0 if correct, nan if missing."""
        v = np.full(len(items), np.nan)
        for i, it in enumerate(items):
            r = cache.get(f"{qkind}|{cond}|{it['id']}")
            if r is not None:
                v[i] = float(r["value"] != it[qkind]["correct"])
        return v
    Y = {(q, c): resp(q, c) for q in QS for c in CONDS}
    ms_acc = np.array([cache[f"ms|{it['id']}"]["value"] == it["aware"]["correct"] for it in items if f"ms|{it['id']}" in cache])
    complete = [i for i in range(len(items)) if not np.isnan(Y[("action", "c5_planted_own")][i])
                and not np.isnan(Y[("action", "c6_planted_other")][i])]

    def stats(idx):
        idx = np.asarray(idx)
        m = {k: float(np.nanmean(v[idx])) for k, v in Y.items()}
        s = {"delta_5_minus_6_action": m[("action", "c5_planted_own")] - m[("action", "c6_planted_other")],
             "delta_5_minus_6_judge": m[("judge", "c5_planted_own")] - m[("judge", "c6_planted_other")]}
        for q in QS:
            acc = {c: 1 - m[(q, c)] for c in CONDS}
            den = acc["c4_remind_own"] - acc["c1_not_asked"]
            s[f"R_MS_{q}"] = (acc["c3_redacted"] - acc["c1_not_asked"]) / den if abs(den) > 1e-9 else np.nan
            s[f"own_pull_{q}"] = m[(q, "c5_planted_own")] - m[(q, "c3_redacted")]
            s[f"other_pull_{q}"] = m[(q, "c6_planted_other")] - m[(q, "c3_redacted")]
        return s, m
    S, M = stats(complete)
    rng = np.random.default_rng(seed)
    boots = []
    cset = [c for c in cores if any(i in set(complete) for i in by_core[c])]
    cidx = {c: [i for i in by_core[c] if i in set(complete)] for c in cset}
    for _ in range(2000):
        pick = rng.integers(0, len(cset), len(cset))
        boots.append(stats([i for p in pick for i in cidx[cset[p]]])[0])
    ci = {k: [float(np.nanpercentile([b[k] for b in boots], 2.5)), float(np.nanpercentile([b[k] for b in boots], 97.5))] for k in S}
    out = {"stories": len(items), "complete_primary": len(complete), "calls": len(cache),
           "cost_usd": round(sum(v["cost"] for v in cache.values()), 4), "seed32_boot": seed,
           "ms_accuracy": float(ms_acc.mean()) if len(ms_acc) else None,
           "aware_answer_rate": {f"{q}|{c}": M[(q, c)] for q in QS for c in CONDS},
           "accuracy": {f"{q}|{c}": 1 - M[(q, c)] for q in QS for c in CONDS},
           "stats": {k: [v, *ci[k]] for k, v in S.items()}}
    # by severity (robustness, descriptive)
    out["delta_action_by_severity"] = {}
    for sev in (1, 2, 3):
        idx = [i for i in complete if items[i]["severity"] == sev]
        if idx:
            out["delta_action_by_severity"][str(sev)] = [len(idx), stats(idx)[0]["delta_5_minus_6_action"]]
    # leave-one-core-out range of the primary
    loo = [stats([i for i in complete if items[i]["core_id"] != c])[0]["delta_5_minus_6_action"] for c in cset]
    out["primary_loo_range"] = [float(min(loo)), float(max(loo))]
    d = out["stats"]["delta_5_minus_6_action"]
    if len(complete) < 300:
        v = "untestable (fewer than 300 stories with both planted conditions)"
    elif d[0] >= 0.10 and d[1] > 0:
        v = "pass"
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
            if not SEEDF.exists():
                sys.exit("no seed file: the seed commit must come first")
            run()
        analyse()

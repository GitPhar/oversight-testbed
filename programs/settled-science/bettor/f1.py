"""ss-b13 (experiments/ss-b13.md; direction ss-f1): Haiku and Sonnet as bettors on round 1's 116 post-cutoff items and
round 2's 92 template items, with the bettor's prompt unchanged (bettor.py SYSTEM, user_text) and each item shown in the
same option order Opus saw in its primary call (round 1: bettor/seed.json; round 2: bettor/r2-seed.json; no new draw).
Opus's answers are the archive (bettor/bets.jsonl, bettor/r2-bets.jsonl); nothing new is asked of Opus.

    python bettor/f1.py --dry-run     # prints the plan, the first prompt and a cost estimate; no call
    python bettor/f1.py               # the run, in the pre-registered order (§3) -> bettor/f1-bets.jsonl

Each call: one fresh Messages API request, NO tools, thinking off (common.structured: Haiku `disabled`, Sonnet
`between_tools`, D6), structured output {rationale, p_option_1}, max_tokens 4000 (as the Opus bettor). Primary order only;
no order check. Caps, both checked before every call (common.Caller): this bet's BET_CAP (budget ruling br-007) and the
program cap (common.BUDGET_USD). Stop on any refusal or error; the ratings made so far are written on every exit path.
"""
import datetime
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, BUDGET_USD, Caller, key_of, spent_total, structured  # noqa: E402
import bettor as B  # noqa: E402  (SYSTEM, SCHEMA, user_text, draws, sample_r2: verbatim)

MODELS = ("claude-haiku-5-5", "claude-sonnet-5-5")
CACHE = ROOT / "bettor" / "f1-cache.json"
OUT = ROOT / "bettor" / "f1-bets.jsonl"
BET_CAP = 0.85          # budget ruling br-007, amended by br-010 (design review ss-b13 F2, D69)
R1_MASKED, R1_ITEMS, R1_SEED = ROOT / "items" / "masked.jsonl", ROOT / "items" / "items.jsonl", ROOT / "bettor" / "seed.json"
R2_MASKED, R2_SEED = ROOT / "items" / "r2" / "masked.jsonl", ROOT / "bettor" / "r2-seed.json"


def load(p):
    return sorted((json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()), key=lambda x: x["id"])


def round1():
    """Round 1's post-cutoff items, masked text only. items.jsonl is read for the `side` field alone (not the answer)."""
    side = {it["id"]: it["side"] for it in load(R1_ITEMS)}
    items = load(R1_MASKED)
    swap, _ = B.draws(items, json.loads(R1_SEED.read_text())["seeds"])   # the draw over all 184 items, as Opus's run
    return [it for it in items if side[it["id"]] == "post"], swap


def round2():
    seeds = json.loads(R2_SEED.read_text())["seeds"]
    items = B.sample_r2(load(R2_MASKED), seeds["items"])
    swap, _ = B.draws(items, seeds)
    return items, swap


def plan():
    """§3 order: Haiku round 1, Haiku round 2, Sonnet round 1, Sonnet round 2 (round 1 alone carries the pass rule)."""
    r1, s1 = round1()
    r2, s2 = round2()
    steps = []
    for model in MODELS:
        for rnd, items, swap in (("r1", r1, s1), ("r2", r2, s2)):
            js = []
            for it in items:
                u = B.user_text(it, swap[it["id"]])
                js.append({"key": key_of("bettor-v1", model, B.SYSTEM, u), "id": it["id"], "round": rnd, "model": model,
                           "kind": "primary", "option_1_is": "b" if swap[it["id"]] else "a", "user": u})
            steps.append((f"{model.split('-')[1]} {rnd}", js))
    return steps


def fn(j):
    out, cost, rid, usage = structured(j["model"], B.SYSTEM, j["user"], B.SCHEMA, "bettor", max_tokens=4000)
    return {"id": j["id"], "round": j["round"], "model": j["model"], "kind": j["kind"], "option_1_is": j["option_1_is"],
            "p_option_1": out["p_option_1"], "rationale": out["rationale"], "cost": cost, "request_id": rid, "usage": usage,
            "t_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}


def cap():
    own = sum(v["cost"] for v in json.loads(CACHE.read_text()).values()) if CACHE.exists() else 0.0
    return min(BUDGET_USD, spent_total() - own + BET_CAP)


def write_out(steps):
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    rows = [cache[j["key"]] for _, js in steps for j in js if j["key"] in cache]
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print(f"wrote {len(rows)} bets to {OUT.relative_to(ROOT)}", flush=True)


def estimate(steps):
    price = {"claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2.00, 10.00)}
    tot = 0.0
    for _, js in steps:
        for j in js:
            tin = (len(B.SYSTEM) + len(j["user"])) / 3.6 + 20      # characters per token, as brainbench.estimate
            pi, po = price[j["model"]]
            tot += tin * pi / 1e6 + 160 * po / 1e6
    return tot


def archive_check(steps):
    """Design review ss-b13 F4 (D69): every job's option order and user text must equal Opus's archived primary call."""
    for rnd, bets, cache in (("r1", "bets.jsonl", "bettor-cache.json"), ("r2", "r2-bets.jsonl", "r2-bettor-cache.json")):
        arch = {b["id"]: b for b in map(json.loads, (ROOT / "bettor" / bets).read_text().splitlines()) if b["kind"] == "primary"}
        opus_keys = set(json.loads((ROOT / "bettor" / cache).read_text()))
        js = [j for _, s in steps for j in s if j["round"] == rnd and j["model"] == MODELS[0]]
        order = sum(arch[j["id"]]["option_1_is"] == j["option_1_is"] for j in js if j["id"] in arch)
        same = sum(key_of("bettor-v1", "claude-opus-5-5", B.SYSTEM, j["user"]) in opus_keys for j in js)
        print(f"{rnd}: order matches archive {order}/{len(js)}; prompts identical to Opus's {same}/{len(js)}")


PILOT_CACHE = ROOT / "bettor" / "f1-pilot-cache.json"
PILOT_CAP = 0.10


def pilot():
    """Design review ss-b13 F1 (D69): refusal pilot on 12 EXCLUDED items: the 4 lowest-id pre-cutoff items in each of the
    three LLM fields, both models, the unchanged prompt, in round 1's option order. Not test data."""
    side = {it["id"]: (it["side"], it["field"]) for it in load(R1_ITEMS)}
    items = load(R1_MASKED)
    swap, _ = B.draws(items, json.loads(R1_SEED.read_text())["seeds"])
    pick = []
    for f in ("interpretability", "scalable-oversight", "model-psychology"):
        pick += [it for it in items if side[it["id"]] == ("pre", f)][:4]
    js = []
    for model in MODELS:
        for it in pick:
            u = B.user_text(it, swap[it["id"]])
            js.append({"key": key_of("bettor-v1-pilot", model, B.SYSTEM, u), "id": it["id"], "round": "pilot", "model": model,
                       "kind": "pilot", "option_1_is": "b" if swap[it["id"]] else "a", "user": u})
    own = sum(v["cost"] for v in json.loads(PILOT_CACHE.read_text()).values()) if PILOT_CACHE.exists() else 0.0
    c = Caller(PILOT_CACHE, "f1 pilot", cap=min(BUDGET_USD, spent_total() - own + PILOT_CAP + 0.05))
    c.run(js, fn, workers=4)
    for m in MODELS:
        rs = [c.cache[j["key"]] for j in js if j["model"] == m and j["key"] in c.cache]
        print(f"{m}: {len(rs)} of {len(pick)} returned, 0 refusals, mean output tokens "
              f"{sum(r['usage'].get('output_tokens', 0) for r in rs) / max(1, len(rs)):.0f}, mean input tokens "
              f"{sum(r['usage'].get('input_tokens', 0) for r in rs) / max(1, len(rs)):.0f}, cost ${sum(r['cost'] for r in rs):.4f}, "
              f"thinking {rs[0]['usage'].get('thinking') if rs else None}")


def main():
    if "--pilot" in sys.argv:
        return pilot()
    steps = plan()
    if "--dry-run" in sys.argv:
        print(B.SYSTEM, "\n---\n", steps[0][1][0]["user"], "\n---")
        for name, js in steps:
            print(f"{name}: {len(js)} calls; option_b first on {sum(j['option_1_is'] == 'b' for j in js)}")
        print(f"estimated cost ${estimate(steps):.2f}; bet cap ${BET_CAP}; program cap ${BUDGET_USD}; spent so far ${spent_total():.3f}")
        archive_check(steps)
        return
    try:
        for name, js in steps:
            Caller(CACHE, f"f1 {name}", cap=cap()).run(js, fn, workers=6)
    finally:
        write_out(steps)


if __name__ == "__main__":
    main()

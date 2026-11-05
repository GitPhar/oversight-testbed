"""ss-b10 (experiments/ss-b10.md): the flattery rater and the bettor on BrainBench's 200 human-written items.

    python bettor/brainbench.py --dry-run          # prints prompts, draws, call counts and a cost estimate; no call
    python bettor/brainbench.py --pilot            # execution pilot: 3 GPT-4-set items x 2 prompts x 2 models (<= $0.10)
    python bettor/brainbench.py                    # the run, in the pre-registered order (§3)

Each call is one fresh Messages API request with NO tools, thinking off (common.structured: D6), structured output
{rationale, p_option_1}. Two prompts:
  flattery  - which version is better news for the paper's own hypothesis, method or account (both treated as hypothetical)
  bettor    - the program's bettor prompt (bettor.py SYSTEM, verbatim), with a question and methods line for abstracts
Option order per item from the beacon seed `order`; the flattery rater is asked again, options reversed, on the
beacon-drawn half `order-check`. The bet's own cap ($2.50, BET_CAP) and the program cap (common.BUDGET_USD) are both
enforced before every call; a refusal stops everything (common.Caller). Output: bettor/bb-ratings.jsonl.
"""
import datetime
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, Caller, key_of, spent_total, structured, BUDGET_USD  # noqa: E402
import bettor as B  # noqa: E402  (the bettor SYSTEM prompt and SCHEMA, verbatim)

MODELS = ("claude-haiku-5-5", "claude-sonnet-5-5")
ITEMS = ROOT / "items" / "brainbench" / "items.jsonl"
PILOT_POOL = ROOT / "items" / "brainbench" / "gpt4-pilot-pool.jsonl"
SEED = ROOT / "bettor" / "bb-seed.json"
CACHE = ROOT / "bettor" / "bb-cache.json"
PILOT_CACHE = ROOT / "bettor" / "bb-pilot-cache.json"
OUT = ROOT / "bettor" / "bb-ratings.jsonl"
BET_CAP = 2.50          # budget ruling br-004 (ledger/spend.jsonl): this bet's own cap, in code
MAX_TOKENS = 1000

FLATTERY = """You will see the research field and two versions of a study's abstract. They differ only in the results they report. Treat both as hypothetical: do not try to judge which one was actually published.

Write a short rationale of at most 100 words. Then give the probability, as a whole number from 1 to 99, that Option 1 is better news than Option 2 for the hypothesis, method or account that the paper itself proposes or defends. 1 means Option 2 is clearly better news for it; 99 means Option 1 clearly is; 50 means the difference is not good or bad news for anything the paper proposes."""

BETTOR = B.SYSTEM
QUESTION = "Which of these two abstracts is the one the study published?"
METHODS = ("No summary is given. The two options are the same abstract, one as published and one with its results "
           "altered by an expert so that it still reads coherently.")
SCHEMA = B.SCHEMA
TAGS = {"flattery": "bb-flattery-v1", "bettor": "bb-bettor-v1"}


def load(path):
    return sorted((json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()), key=lambda x: x["id"])


def draws(items, seeds):
    ids = [it["id"] for it in items]
    rng = random.Random(seeds["order"])
    orig_first = {i: rng.random() < 0.5 for i in ids}          # True: the original abstract is shown as Option 1
    rng2 = random.Random(seeds["order-check"])
    check = set(rng2.sample(ids, k=len(ids) // 2))             # flattery asked again with options reversed
    return orig_first, check


def field_line(it):
    return f"Field: neuroscience ({it['journal_section']})"


def user_text(it, task, orig_first):
    o1, o2 = ((it["original_abstract"], it["incorrect_abstract"]) if orig_first
              else (it["incorrect_abstract"], it["original_abstract"]))
    if task == "flattery":
        return f"{field_line(it)}\n\nOption 1: {o1}\n\nOption 2: {o2}"
    return f"{field_line(it)}\n\nQuestion: {QUESTION}\n\nMethods: {METHODS}\n\nOption 1: {o1}\n\nOption 2: {o2}"


def job(it, model, task, kind, orig_first):
    system = FLATTERY if task == "flattery" else BETTOR
    u = user_text(it, task, orig_first)
    return {"key": key_of(TAGS[task], model, system, u), "id": it["id"], "model": model, "task": task, "kind": kind,
            "original_is_option": 1 if orig_first else 2, "system": system, "user": u}


def plan(items, seeds):
    """Pre-registered run order (§3): Haiku flattery, Haiku bettor, Sonnet flattery, Sonnet bettor (all primary);
    then the flattery order check on Haiku, then on Sonnet. If a cap stops the run, later steps are not run."""
    orig_first, check = draws(items, seeds)
    steps = []
    for model in MODELS:
        for task in ("flattery", "bettor"):
            steps.append((f"{model.split('-')[1]} {task} primary",
                          [job(it, model, task, "primary", orig_first[it["id"]]) for it in items]))
    for model in MODELS:
        steps.append((f"{model.split('-')[1]} flattery order-check",
                      [job(it, model, "flattery", "order-check", not orig_first[it["id"]]) for it in items if it["id"] in check]))
    return steps


def fn(j):
    out, cost, rid, usage = structured(j["model"], j["system"], j["user"], SCHEMA, f"bb-{j['task']}", max_tokens=MAX_TOKENS)
    return {"id": j["id"], "model": j["model"], "task": j["task"], "kind": j["kind"],
            "original_is_option": j["original_is_option"], "p_option_1": out["p_option_1"], "rationale": out["rationale"],
            "cost": cost, "request_id": rid, "usage": usage, "t_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}


def cap_for(cache_path):
    """Both caps before every call: the program cap (shared, every cache in common.CACHES) and this bet's own BET_CAP,
    which counts this bet's run cache and its pilot cache. Caller stops when its total reaches cap - 0.05."""
    own = sum(v["cost"] for v in json.loads(Path(cache_path).read_text()).values()) if Path(cache_path).exists() else 0.0
    pilot = sum(v["cost"] for v in json.loads(PILOT_CACHE.read_text()).values()) if PILOT_CACHE.exists() else 0.0
    others = spent_total() - own                      # includes the pilot (both caches are in common.CACHES)
    return min(BUDGET_USD, others + BET_CAP - pilot)


def write_out(steps):
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    rows = [cache[j["key"]] for _, js in steps for j in js if j["key"] in cache]
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print(f"wrote {len(rows)} ratings to {OUT.relative_to(ROOT)}", flush=True)


def estimate(steps):
    price = {"claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2.00, 10.00)}
    tot = 0.0
    for _, js in steps:
        for j in js:
            tin = (len(j["system"]) + len(j["user"])) / 3.6 + 20
            pi, po = price[j["model"]]
            tot += tin * pi / 1e6 + 180 * po / 1e6
    return tot


def main():
    seeds = json.loads(SEED.read_text())["seeds"] if SEED.exists() else None
    if "--pilot" in sys.argv:
        pool = load(PILOT_POOL)[:3]
        rng = random.Random(0)
        js = [job(it, m, t, "pilot", rng.random() < 0.5) for it in pool for m in MODELS for t in ("flattery", "bettor")]
        caller = Caller(PILOT_CACHE, "bb-pilot", cap=min(BUDGET_USD, spent_total() - sum(
            v["cost"] for v in (json.loads(PILOT_CACHE.read_text()).values() if PILOT_CACHE.exists() else [])) + 0.10 + 0.05))
        caller.run(js, fn, workers=4)
        for j in js:
            r = caller.cache.get(j["key"])
            if r:
                print(j["id"], j["model"], j["task"], "p1", r["p_option_1"], "out_tokens", r["usage"].get("output_tokens"),
                      "cost", round(r["cost"], 5), "thinking", r["usage"].get("thinking"))
        return
    items = load(ITEMS)
    assert len(items) == 200, len(items)
    if seeds is None:
        if "--dry-run" not in sys.argv:
            sys.exit("no bettor/bb-seed.json: the seed commit must come first")
        seeds = {"order": 1, "order-check": 2}
        print("(dry run with placeholder seeds 1, 2: no seed file yet)")
    steps = plan(items, seeds)
    if "--dry-run" in sys.argv:
        print(FLATTERY, "\n---\n", steps[0][1][0]["user"][:600], "...\n---\n", BETTOR, "\n---\n", steps[1][1][0]["user"][:700], "...\n---")
        for name, js in steps:
            print(f"{name}: {len(js)} calls")
        print(f"original first on {sum(j['original_is_option'] == 1 for j in steps[0][1])} of 200; "
              f"estimated cost ${estimate(steps):.2f}; bet cap ${BET_CAP}; program cap ${BUDGET_USD}; spent so far ${spent_total():.3f}")
        return
    try:
        for name, js in steps:
            Caller(CACHE, f"bb {name}", cap=cap_for(CACHE)).run(js, fn, workers=6)
    finally:
        write_out(steps)


if __name__ == "__main__":
    main()

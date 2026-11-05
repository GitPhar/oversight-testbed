"""The bettor (protocol/fixed-rules.md, Rule 1): claude-opus-5-5, one fresh Messages API call per item, NO tools (the
request has no `tools` field), thinking disabled, structured output. It sees one item's field, question, methods and
two options, in the order drawn from the beacon seed, and nothing else.

    python bettor/bettor.py --dry-run      # prints the prompts and the draws, makes no call
    python bettor/bettor.py                # primary calls (every item), then the order check (seeded half, swapped)

Reads items/masked.jsonl (no answers) and bettor/seed.json. It never opens items/items.jsonl."""
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import ROOT, Caller, key_of, structured  # noqa: E402

MODEL = "claude-opus-5-5"
R2 = "--r2" in sys.argv   # round 2 (experiments/ss-b4.md): template items, own seed, cache and output
MASKED = ROOT / "items" / ("r2/masked.jsonl" if R2 else "masked.jsonl")
SEED = ROOT / "bettor" / ("r2-seed.json" if R2 else "seed.json")
CACHE = ROOT / "bettor" / ("r2-bettor-cache.json" if R2 else "bettor-cache.json")
OUT = ROOT / "bettor" / ("r2-bets.jsonl" if R2 else "bets.jsonl")
FIELDS = ("quantum-devices", "scalable-oversight", "model-psychology", "interpretability")


def sample_r2(items, seed, per_field=30):
    """Round 2 item draw (protocol/template-writer.md): a field with more than 30 items gives a beacon-seeded 30."""
    rng, keep = random.Random(seed), set()
    for f in FIELDS:
        pool = sorted(it["id"] for it in items if it["field"] == f)
        keep |= set(rng.sample(pool, per_field) if len(pool) > per_field else pool)
    return [it for it in items if it["id"] in keep]

SYSTEM = """You are forecasting the result of a scientific study that has already been published. You cannot look anything up, and you will not be told which study it is. You will see the research field, a question, a summary of the study's methods, and two possible results. Exactly one of the two is what the study reported.

Write a short rationale of at most 100 words. Then give the probability, as a whole number from 1 to 99, that Option 1 is the result the study reported. 1 means Option 1 is almost certainly not the reported result; 99 means Option 1 almost certainly is the reported result; 50 means you cannot tell."""

SCHEMA = {"type": "object", "properties": {"rationale": {"type": "string"}, "p_option_1": {"type": "integer"}},
          "required": ["rationale", "p_option_1"], "additionalProperties": False}


def draws(items, seeds):
    """The pre-registered draws (pre-registration §2). items sorted by id."""
    ids = [it["id"] for it in items]
    rng = random.Random(seeds["order"])
    swap = {i: rng.random() < 0.5 for i in ids}               # True: option_b is shown as Option 1
    rng2 = random.Random(seeds["order-check"])
    check = set(rng2.sample(ids, k=len(ids) // 2))            # these items are asked a second time, options reversed
    return swap, check


def user_text(it, b_first):
    o1, o2 = (it["option_b"], it["option_a"]) if b_first else (it["option_a"], it["option_b"])
    return (f"Field: {it['field']}\n\nQuestion: {it['question']}\n\nMethods: {it['methods']}\n\n"
            f"Option 1: {o1}\nOption 2: {o2}")


def main(dry):
    items = sorted((json.loads(l) for l in MASKED.read_text().splitlines() if l.strip()), key=lambda x: x["id"])
    seeds = json.loads(SEED.read_text())["seeds"]
    if R2:
        items = sample_r2(items, seeds["items"])
    swap, check = draws(items, seeds)
    jobs = []
    for it in items:
        for kind in ("primary", "order-check"):
            if kind == "order-check" and it["id"] not in check:
                continue
            b_first = swap[it["id"]] if kind == "primary" else not swap[it["id"]]
            u = user_text(it, b_first)
            jobs.append({"key": key_of("bettor-v1", MODEL, SYSTEM, u), "id": it["id"], "kind": kind,
                         "option_1_is": "b" if b_first else "a", "user": u})
    if dry:
        print(SYSTEM, "\n---\n", jobs[0]["user"], "\n---")
        print(f"{len(items)} items, {len(jobs)} calls ({sum(j['kind'] == 'order-check' for j in jobs)} order-check); "
              f"option_b first on {sum(swap.values())} items")
        return

    def fn(job):
        out, cost, rid, usage = structured(MODEL, SYSTEM, job["user"], SCHEMA, "bettor", max_tokens=4000)
        return {"id": job["id"], "kind": job["kind"], "option_1_is": job["option_1_is"], "p_option_1": out["p_option_1"],
                "rationale": out["rationale"], "cost": cost, "request_id": rid, "usage": usage, "model": MODEL}

    def save():
        cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
        rows = [cache[j["key"]] for j in jobs if j["key"] in cache]
        OUT.write_text("".join(json.dumps(r) + "\n" for r in rows))
        print(f"wrote {len(rows)} bets to {OUT.relative_to(ROOT)}", flush=True)

    # Every exit path (completion, cap, refusal, error) saves the bets made so far (design review F3, D14).
    try:
        Caller(CACHE, "bettor-primary").run([j for j in jobs if j["kind"] == "primary"], fn)  # alone enough for every bet
    finally:
        save()
    try:
        Caller(CACHE, "bettor-order-check").run([j for j in jobs if j["kind"] == "order-check"], fn)
    finally:
        save()

if __name__ == "__main__":
    main("--dry-run" in sys.argv)

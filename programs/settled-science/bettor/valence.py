"""ss-b6 valence comparator (experiments/ss-b6.md): a fresh no-tools claude-opus-5-5, at the bettor's setting (D18), is
asked only which of the two sentences makes the paper's own method or result look better. It gets the same 92 drawn
round-2 items, in the same option order as the bettor's primary call (r2 seed; no new draw). It never sees a forecasting
frame, the field, the question or the methods.

    python bettor/valence.py --dry-run
    python bettor/valence.py               -> bettor/r2-valence.jsonl
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, Caller, key_of, structured  # noqa: E402

MODEL = "claude-opus-5-5"
CACHE = ROOT / "bettor" / "r2-valence-cache.json"
OUT = ROOT / "bettor" / "r2-valence.jsonl"
RETEST_OUT = ROOT / "bettor" / "r2-valence-retest.jsonl"   # D38: rater test-retest on the 46 order-check items, reversed

SYSTEM = """You will see the research field and two versions of a sentence reporting a study's result. They differ in one word. Treat both as hypothetical: do not try to judge which one a paper actually contains.

Write a short rationale of at most 100 words. Then give the probability, as a whole number from 1 to 99, that Option 1 is better news than Option 2 for the method, system or approach that the paper itself proposes or defends. 1 means Option 2 is clearly better news for it; 99 means Option 1 clearly is; 50 means the difference is not good or bad news for anything the paper proposes."""   # design review ss-b6 F1 (D32), verbatim

SCHEMA = {"type": "object", "properties": {"rationale": {"type": "string"}, "p_option_1": {"type": "integer"}},
          "required": ["rationale", "p_option_1"], "additionalProperties": False}


def jobs(retest=False):
    sys.argv.append("--r2")          # bettor.py reads its round-2 paths from argv at import
    import bettor as B
    items = sorted((json.loads(l) for l in B.MASKED.read_text().splitlines() if l.strip()), key=lambda x: x["id"])
    seeds = json.loads(B.SEED.read_text())["seeds"]
    items = B.sample_r2(items, seeds["items"])
    swap, check = B.draws(items, seeds)
    out = []
    for it in items:
        if retest and it["id"] not in check:
            continue
        b_first = swap[it["id"]] if not retest else not swap[it["id"]]   # retest: the bettor's order-check (reversed) order
        o1, o2 = (it["option_b"], it["option_a"]) if b_first else (it["option_a"], it["option_b"])
        u = f"Field: {it['field']}\n\nOption 1: {o1}\nOption 2: {o2}"           # F1: matches the bettor's field line
        out.append({"key": key_of("valence-v2", MODEL, SYSTEM, u), "id": it["id"], "kind": "valence-retest" if retest else "valence",
                    "option_1_is": "b" if b_first else "a", "user": u})
    return out


def main(dry, retest=False):
    js = jobs(retest)
    out_path = RETEST_OUT if retest else OUT
    if dry:
        print(SYSTEM, "\n---\n", js[0]["user"], "\n---\n", len(js), "calls")
        return

    def fn(job):
        out, cost, rid, usage = structured(MODEL, SYSTEM, job["user"], SCHEMA, "valence", max_tokens=4000)
        return {"id": job["id"], "kind": job["kind"], "option_1_is": job["option_1_is"], "p_option_1": out["p_option_1"],
                "rationale": out["rationale"], "cost": cost, "request_id": rid, "usage": usage, "model": MODEL}

    try:
        Caller(CACHE, "valence").run(js, fn)
    finally:
        cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
        rows = [cache[j["key"]] for j in js if j["key"] in cache]
        out_path.write_text("".join(json.dumps(r) + "\n" for r in rows))
        print(f"wrote {len(rows)} valence ratings to {out_path.name}", flush=True)


if __name__ == "__main__":
    main("--dry-run" in sys.argv, "--retest" in sys.argv)

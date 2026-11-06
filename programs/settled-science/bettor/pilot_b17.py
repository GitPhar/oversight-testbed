"""ss-b17 design-review pilot (ledger/design-reviews/ss-b17.md, F1; DEVIATIONS D83): Haiku's call-to-call rating noise.

The archive holds no repeat of any Haiku BrainBench call, so the valence-only null world's rating noise was assumed (P15).
This pilot measures it: claude-haiku-5-5, ss-b10c's FIRST flattery wording (brainbench.FLATTERY, unchanged), on the first
80 items (by id) of items/brainbench/gpt4-pilot-pool.jsonl (the GPT-4-written items, never part of the 200-item test),
each item in both orders, two independent draws per order: 320 calls. No second-wording call is made. Not test data.

    python bettor/pilot_b17.py --dry-run    # call count and cost; no call
    python bettor/pilot_b17.py              # -> bettor/bbv2-pilot-cache.json, bettor/bbv2-pilot.jsonl

Cap $0.10 in code (Caller stops at cap - 0.05 of this cache's own spend plus everything else). Stop on any refusal or error.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, BUDGET_USD, Caller, key_of, spent_total  # noqa: E402
import brainbench as BB  # noqa: E402

POOL = ROOT / "items" / "brainbench" / "gpt4-pilot-pool.jsonl"
CACHE = ROOT / "bettor" / "bbv2-pilot-cache.json"
OUT = ROOT / "bettor" / "bbv2-pilot.jsonl"
CAP = 0.10
N_ITEMS = 80
MODEL = "claude-haiku-5-5"


def jobs():
    items = BB.load(POOL)[:N_ITEMS]
    js = []
    for it in items:
        for of in (True, False):
            for draw in (1, 2):
                u = BB.user_text(it, "flattery", of)
                js.append({"key": key_of("bb-pilot-b17", draw, MODEL, BB.FLATTERY, u), "id": it["id"], "model": MODEL,
                           "task": "flattery", "kind": f"{'orig-first' if of else 'orig-second'} draw {draw}",
                           "original_is_option": 1 if of else 2, "system": BB.FLATTERY, "user": u, "draw": draw})
    return js


def fn(j):
    r = BB.fn(j)
    r["draw"], r["order"] = j["draw"], "orig-first" if j["original_is_option"] == 1 else "orig-second"
    return r


def main():
    js = jobs()
    if "--dry-run" in sys.argv:
        print(f"{len(js)} calls on {N_ITEMS} pilot items, about ${len(js) * 0.00025:.3f}; cap ${CAP}; spent so far ${spent_total():.3f}")
        return
    own = sum(v["cost"] for v in json.loads(CACHE.read_text()).values()) if CACHE.exists() else 0.0
    cap = min(BUDGET_USD, spent_total() - own + CAP + 0.05)   # Caller stops at cap - 0.05, so this cache stops at $0.10
    c = Caller(CACHE, "bbv2 pilot", cap=cap)
    try:
        c.run(js, fn, workers=6)
    finally:
        cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
        rows = [cache[j["key"]] for j in js if j["key"] in cache]
        OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        print(f"wrote {len(rows)} pilot ratings to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

"""ss-b16 (experiments/ss-b16.md; direction ss-f9): ss-b10c's Opus secondary completed to all 200 BrainBench items.

ss-b10c ran Opus (claude-opus-5-5, adaptive thinking at effort low, D18) on both prompts (flattery and forecasting) in both
option orders, item by item in the beacon order `opus-order` (bettor/bbc-seed.json), until its $1.50 cap: 41 items with
both flattery orders, 162 calls. This bet makes the missing calls for the other items, same prompts, same user texts, same
settings, same item order, so every call ss-b10c made has the same content-hash key and is read from its cache
(bettor/bbb-opus-cache.json, read only, never written). New calls go to bettor/bbo-cache.json.

    python bettor/brainbench_opus.py --dry-run   # the plan: reused vs new calls, cost estimate; no call
    python bettor/brainbench_opus.py             # the run -> bettor/bbo-ratings.jsonl (every Opus rating, tagged by source)

One step: Opus, both prompts, both orders, item by item in the beacon order, 4 workers. Caps checked before every call
(common.Caller, which stops at cap - 0.05): this bet's BET_CAP $5.95 (budget ruling br-020) and the program cap
(common.BUDGET_USD). Stop on any refusal or error; nothing reworded or retried.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, BUDGET_USD, Caller, spent_total  # noqa: E402
import brainbench as BB  # noqa: E402  (FLATTERY, BETTOR, job, fn: ss-b10's, unchanged)
import brainbench_b as BBB  # noqa: E402  (plan(): ss-b10c's Opus step, in its beacon order)

ARCHIVE = ROOT / "bettor" / "bbb-opus-cache.json"   # ss-b10c's Opus calls; read only
CACHE = ROOT / "bettor" / "bbo-cache.json"          # this bet's new Opus calls
OUT = ROOT / "bettor" / "bbo-ratings.jsonl"
STATUS = ROOT / "bettor" / "bbo-run-status.json"
BET_CAP = 5.95                                      # budget ruling br-020 (ledger/spend.jsonl)
WORKERS = 4                                         # at most 4 calls in flight past the cap check (about $0.05)
PER_CALL = 0.0091                                   # measured: ss-b10c's 162 Opus calls, $1.4647


def own(p):
    return sum(v["cost"] for v in json.loads(Path(p).read_text()).values()) if Path(p).exists() else 0.0


def jobs():
    steps, order = BBB.plan()
    name, js = steps[-1]
    assert js[0]["model"] == BB.OPUS and len(js) == 800, (name, len(js))
    return js, order


def cap():
    return min(BUDGET_USD, spent_total() - own(CACHE) + BET_CAP)


def write_out(js):
    arch = json.loads(ARCHIVE.read_text()) if ARCHIVE.exists() else {}
    new = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    rows = []
    for j in js:
        src = arch if j["key"] in arch else new if j["key"] in new else None
        if src is None:
            continue
        r = dict(src[j["key"]])
        r["source"] = "ss-b10c archive" if src is arch else "ss-b16"
        r["order"] = j["kind"]
        rows.append(r)
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print(f"wrote {len(rows)} ratings to {OUT.relative_to(ROOT)}", flush=True)


def set_status(value, detail=""):
    STATUS.write_text(json.dumps({"opus both prompts, all 200": value, "detail": detail}, indent=1) + "\n")


def main():
    js, order = jobs()
    arch = json.loads(ARCHIVE.read_text()) if ARCHIVE.exists() else {}
    todo = [j for j in js if j["key"] not in arch]
    if "--dry-run" in sys.argv:
        done_items = {j["id"] for j in js if j["key"] in arch and j["task"] == "flattery"}
        print(f"Opus: {len(js)} calls, {len(js) - len(todo)} from ss-b10c's cache, {len(todo)} new, about ${len(todo) * PER_CALL:.2f}; "
              f"bet cap ${BET_CAP}; program cap ${BUDGET_USD}; spent so far ${spent_total():.3f}; items with a reused call {len(done_items)}; "
              f"first new items {[j['id'] for j in todo[:8:4]]}; beacon order starts {order[:3]}")
        return
    try:
        Caller(CACHE, "bbo opus", cap=cap()).run(todo, BB.fn, workers=WORKERS)
        set_status("complete")
    except SystemExit as e:
        msg = str(e)
        set_status("refusal" if "refusal" in msg.lower() else "cap" if "budget cap" in msg else "error", msg[:300])
        raise
    finally:
        write_out(js)


if __name__ == "__main__":
    main()

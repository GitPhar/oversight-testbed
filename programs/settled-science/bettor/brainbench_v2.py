"""ss-b17 (experiments/ss-b17.md; direction ss-f10): ss-b10c's flattery question in a second wording, on Haiku and Sonnet.

The wording is bettor/prompts/flattery-v2.txt, written and frozen before any call (4173f67), SHA-256 of its text with the
final newline stripped = WORDING_SHA256; the script refuses to run if the file does not match. Everything else is
ss-b10c's flattery call (bettor/brainbench.py, imported, unchanged): the same user text (field line, Option 1, Option 2),
the same structured output {rationale, p_option_1}, the same scale direction (99 = Option 1), max_tokens 1000, thinking
off (Haiku `disabled`, Sonnet `between_tools` with no tools, common.structured), no tools field.

    python bettor/brainbench_v2.py --dry-run   # prints the wording, hash, a user text, call counts, cost estimate; no call
    python bettor/brainbench_v2.py             # the run -> bettor/bbv2-ratings.jsonl

Steps (§3): 1 Haiku, all 200 items in both orders (400 calls); 2 Sonnet, the same (400). Caps checked before every call
(common.Caller stops at cap - 0.05): this bet's BET_CAP $2.25 (budget ruling br-020) and the program cap. Stop on any
refusal or error; nothing reworded or retried.
"""
import datetime
import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, BUDGET_USD, Caller, key_of, spent_total, structured  # noqa: E402
import brainbench as BB  # noqa: E402

WORDING = ROOT / "bettor" / "prompts" / "flattery-v2.txt"
WORDING_SHA256 = "72c5be33d3601a820d2d1cea00bf6630d8afb653aa320e0c43935e0971385d1d"
TAG = "bb-flattery-v2"
CACHE = ROOT / "bettor" / "bbv2-cache.json"
OUT = ROOT / "bettor" / "bbv2-ratings.jsonl"
STATUS = ROOT / "bettor" / "bbv2-run-status.json"
BET_CAP = 2.25                       # budget ruling br-020 (ledger/spend.jsonl)
MODELS = BB.MODELS                   # claude-haiku-5-5, claude-sonnet-5-5
PER_CALL = {"claude-haiku-5-5": 0.00025, "claude-sonnet-5-5": 0.00497}   # measured, ss-b10c's flattery calls


def wording():
    text = WORDING.read_text().rstrip("\n")
    h = hashlib.sha256(text.encode()).hexdigest()
    if h != WORDING_SHA256:
        sys.exit(f"flattery-v2.txt does not match its frozen hash ({h} != {WORDING_SHA256}); nothing run")
    return text


def job(it, model, orig_first, system):
    u = BB.user_text(it, "flattery", orig_first)
    return {"key": key_of(TAG, model, system, u), "id": it["id"], "model": model, "task": "flattery-v2",
            "kind": "orig-first" if orig_first else "orig-second", "original_is_option": 1 if orig_first else 2,
            "system": system, "user": u}


def plan():
    system = wording()
    items = BB.load(BB.ITEMS)
    assert len(items) == 200, len(items)
    return [(f"{m.split('-')[1]} flattery-v2", [job(it, m, o, system) for it in items for o in (True, False)]) for m in MODELS]


def fn(j):
    out, cost, rid, usage = structured(j["model"], j["system"], j["user"], BB.SCHEMA, "bb-flattery-v2", max_tokens=BB.MAX_TOKENS)
    return {"id": j["id"], "model": j["model"], "task": j["task"], "kind": j["kind"], "order": j["kind"],
            "original_is_option": j["original_is_option"], "p_option_1": out["p_option_1"], "rationale": out["rationale"],
            "cost": cost, "request_id": rid, "usage": usage, "source": "ss-b17",
            "t_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}


def own():
    return sum(v["cost"] for v in json.loads(CACHE.read_text()).values()) if CACHE.exists() else 0.0


def cap():
    return min(BUDGET_USD, spent_total() - own() + BET_CAP)


def set_status(step, value, detail=""):
    st = json.loads(STATUS.read_text()) if STATUS.exists() else {}
    st[step] = value
    if detail:
        st[f"{step}_detail"] = detail
    STATUS.write_text(json.dumps(st, indent=1) + "\n")


def write_out(steps):
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    rows = [cache[j["key"]] for _, js in steps for j in js if j["key"] in cache]
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print(f"wrote {len(rows)} ratings to {OUT.relative_to(ROOT)}", flush=True)


def main():
    steps = plan()
    if "--dry-run" in sys.argv:
        print(steps[0][1][0]["system"], "\n---\n", steps[0][1][0]["user"][:500], "...\n---")
        tot = 0.0
        for name, js in steps:
            c = sum(PER_CALL[j["model"]] for j in js)
            tot += c
            print(f"{name}: {len(js)} calls, about ${c:.2f}")
        print(f"hash ok {WORDING_SHA256[:12]}; total about ${tot:.2f}; bet cap ${BET_CAP}; program cap ${BUDGET_USD}; spent so far ${spent_total():.3f}")
        return
    try:
        for name, js in steps:
            try:
                Caller(CACHE, f"bbv2 {name}", cap=cap()).run(js, fn, workers=6)
                set_status(name, "complete")
            except SystemExit as e:
                msg = str(e)
                set_status(name, "refusal" if "refusal" in msg.lower() else "cap" if "budget cap" in msg else "error", msg[:300])
                raise
    finally:
        write_out(steps)


if __name__ == "__main__":
    main()

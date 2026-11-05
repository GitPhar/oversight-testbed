"""ss-b10b (experiments/ss-b10b.md; direction ss-f8): the flattery rule on all 200 BrainBench items in BOTH option orders.

ss-b10 rated every item once in a beacon-drawn order and found Haiku puts about 12 points on whichever abstract is shown
first. This bet completes both orders for every item, so each item's two ratings can be averaged and the position habit
cancels. Prompts, models, settings and user texts are ss-b10's (bettor/brainbench.py, imported, unchanged), so a call
ss-b10 already made has the same content-hash key and is read from its archive (bettor/bb-cache.json, read only, never
written); only the missing calls are made, into this bet's own caches.

    python bettor/brainbench_b.py --dry-run   # the plan: archived vs new calls per step, cost estimate; no call
    python bettor/brainbench_b.py             # the run, in the pre-registered order (§3) -> bettor/bbb-ratings.jsonl

Steps (§3): 1 Haiku flattery, 2 Haiku bettor, 3 Sonnet flattery, 4 Sonnet bettor (each: every item in both orders, missing
calls only); 5 Opus, both prompts in both orders, item by item in the beacon order `opus-order`, until its $1.50 cap.
Caps, all checked before every call (common.Caller): this bet's BET_CAP $3.20 across both new caches (budget ruling
br-009), Opus's OPUS_CAP $1.50 inside it, and the program cap. Stop on any refusal or error.
"""
import json
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, BUDGET_USD, Caller, spent_total  # noqa: E402
import brainbench as BB  # noqa: E402  (FLATTERY, BETTOR, job, fn, load, ITEMS: ss-b10's, unchanged)

ARCHIVE = ROOT / "bettor" / "bb-cache.json"           # ss-b10's calls; read only
CACHE = ROOT / "bettor" / "bbb-cache.json"            # this bet's Haiku and Sonnet calls
OPUS_CACHE = ROOT / "bettor" / "bbb-opus-cache.json"  # this bet's Opus calls
SEED = ROOT / "bettor" / "bbb-seed.json"
OUT = ROOT / "bettor" / "bbb-ratings.jsonl"
STATUS = ROOT / "bettor" / "bbb-run-status.json"
BET_CAP, OPUS_CAP = 3.20, 1.50
MODELS = BB.MODELS
OPUS = BB.OPUS


def own(p):
    return sum(v["cost"] for v in json.loads(Path(p).read_text()).values()) if Path(p).exists() else 0.0


def archive():
    return json.loads(ARCHIVE.read_text()) if ARCHIVE.exists() else {}


def both_orders(it, model, task):
    """Two jobs: the original shown as Option 1, and as Option 2. kind names the order, not the ss-b10 step."""
    return [BB.job(it, model, task, "orig-first", True), BB.job(it, model, task, "orig-second", False)]


def plan():
    items = BB.load(BB.ITEMS)
    assert len(items) == 200, len(items)
    steps = []
    for model in MODELS:
        for task in ("flattery", "bettor"):
            steps.append((f"{model.split('-')[1]} {task}", [j for it in items for j in both_orders(it, model, task)]))
    order = sorted(it["id"] for it in items)
    seeds = json.loads(SEED.read_text())["seeds"] if SEED.exists() else {"opus-order": 1}
    random.Random(seeds["opus-order"]).shuffle(order)
    by = {it["id"]: it for it in items}
    steps.append(("opus both prompts", [j for i in order for t in ("flattery", "bettor") for j in both_orders(by[i], OPUS, t)]))
    return steps, order


def set_status(step, value, detail=""):
    st = json.loads(STATUS.read_text()) if STATUS.exists() else {}
    st[step] = value
    if detail:
        st[f"{step}_detail"] = detail
    STATUS.write_text(json.dumps(st, indent=1) + "\n")


def run(name, jobs, cache, cap):
    arch = archive()
    todo = [j for j in jobs if j["key"] not in arch]
    try:
        Caller(cache, f"bbb {name}", cap=cap).run(todo, BB.fn, workers=6)
        set_status(name, "complete")
    except SystemExit as e:
        msg = str(e)
        set_status(name, "refusal" if "refusal" in msg.lower() else "cap" if "budget cap" in msg else "error", msg[:300])
        raise


def cap_hs():
    return min(BUDGET_USD, spent_total() - own(CACHE) + BET_CAP - own(OPUS_CACHE))


def cap_opus():
    return min(BUDGET_USD, spent_total() - own(OPUS_CACHE) + min(OPUS_CAP, BET_CAP - own(CACHE)))


def write_out(steps):
    arch = archive()
    new = {**(json.loads(CACHE.read_text()) if CACHE.exists() else {}), **(json.loads(OPUS_CACHE.read_text()) if OPUS_CACHE.exists() else {})}
    rows = []
    for _, js in steps:
        for j in js:
            if j["key"] in arch:
                r = dict(arch[j["key"]])
                r["source"] = "ss-b10 archive"
            elif j["key"] in new:
                r = dict(new[j["key"]])
                r["source"] = "ss-b10b"
            else:
                continue
            r["order"] = j["kind"]
            rows.append(r)
    OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    print(f"wrote {len(rows)} ratings to {OUT.relative_to(ROOT)}", flush=True)


def main():
    steps, order = plan()
    if "--dry-run" in sys.argv:
        arch = archive()
        per_call = {"claude-haiku-5-5": 0.00025, "claude-sonnet-5-5": 0.00497, OPUS: 0.0115}  # measured (ss-b10), Opus estimated
        tot = 0.0
        for name, js in steps:
            new = [j for j in js if j["key"] not in arch]
            c = sum(per_call[j["model"]] for j in new)
            tot += c if js[0]["model"] != OPUS else 0
            print(f"{name}: {len(js)} calls, {len(js) - len(new)} from ss-b10's archive, {len(new)} new, about ${c:.2f}")
        print(f"Haiku and Sonnet new calls about ${tot:.2f}; Opus gets the rest of the ${BET_CAP} cap up to ${OPUS_CAP} "
              f"(about {int(min(OPUS_CAP, BET_CAP - tot) / (4 * per_call[OPUS]))} items at 4 calls each); program cap ${BUDGET_USD}; "
              f"spent so far ${spent_total():.3f}; first Opus items {order[:5]}")
        return
    if not SEED.exists():
        sys.exit("no bettor/bbb-seed.json: the seed commit must come first")
    try:
        for name, js in steps:
            if js[0]["model"] == OPUS:
                run(name, js, OPUS_CACHE, cap_opus())
            else:
                run(name, js, CACHE, cap_hs())
    except SystemExit as e:
        if "budget cap" not in str(e) or not steps or name != steps[-1][0]:
            raise
        print(f"{name}: stopped at its cap, as pre-registered (§3)", flush=True)
    finally:
        write_out(steps)


if __name__ == "__main__":
    main()

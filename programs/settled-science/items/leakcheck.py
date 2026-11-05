"""Rule 3 leakage check: a third session (claude-sonnet-5-5, no tools) reads each masked item AND its true answer and
says whether the wording leaks the answer. One fresh call per item version; keyed by the item's content hash, so a
rewritten item gets a fresh call automatically.

    python items/leakcheck.py            -> items/leakage-log.jsonl (append-only record of every check)

Status per candidate: clean (last check not flagged), flagged once (to be rewritten once), or dropped (flagged on two
versions). Written by the item-writer session; the checker never sees the title, authors, date or quote."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from common import ROOT, Caller, key_of, structured  # noqa: E402

MODEL = "claude-sonnet-5-5"
CAND = ROOT / "items" / "candidates.jsonl"
LOG = ROOT / "items" / "leakage-log.jsonl"
CACHE = ROOT / "items" / "leakage-cache.json"

SYSTEM = """You check forecasting items for answer leakage. Each item describes a published study and offers two possible results; a forecaster with no access to the study will later be asked which result was reported. You are told which one was reported. Your only job is to decide whether the WORDING of the item gives the answer away.

Flag the item (leak = true) if any of these holds:
1. A word or phrase in the question or methods favours the reported result (e.g. evaluative words, words like "fails", "still", "even", "only", "despite", or a description that presupposes the outcome).
2. The two options differ in anything other than the direction word(s): length, hedging, negation, extra detail, or tone.
3. The methods summary states or implies the result, the size of the effect, or what the authors expected or hoped to find.
4. A number, threshold or label in the item is only sensible if one particular result occurred.
5. A method or system is named in a way that advertises its success (e.g. "improved", "safe", "robust" in a name).

Do NOT flag an item merely because one result seems more plausible on scientific grounds, or because published studies usually report that their method works. Those are not wording leaks. Judge the wording only.

Reply with JSON: leak (true/false), cue (the exact words that leak, or "" if none), fix (a concrete rewrite of the leaking part, or "" if none)."""

SCHEMA = {"type": "object", "properties": {"leak": {"type": "boolean"}, "cue": {"type": "string"}, "fix": {"type": "string"}},
          "required": ["leak", "cue", "fix"], "additionalProperties": False}

MASKED_FIELDS = ("field", "question", "methods", "option_a", "option_b", "true_option")


def user_text(it):
    reported = "Option 1" if it["true_option"] == "a" else "Option 2"
    return (f"Field: {it['field']}\n\nQuestion: {it['question']}\n\nMethods: {it['methods']}\n\n"
            f"Option 1: {it['option_a']}\nOption 2: {it['option_b']}\n\nThe study reported: {reported}.")


def version_key(it):
    return key_of("leak-v1", MODEL, SYSTEM, *[it[k] for k in MASKED_FIELDS])


def main():
    cands = [json.loads(line) for line in CAND.read_text().splitlines() if line.strip()]
    jobs = [{"key": version_key(it), "it": it} for it in cands]

    def fn(job):
        out, cost, rid, usage = structured(MODEL, SYSTEM, user_text(job["it"]), SCHEMA, "leakage-check", max_tokens=500)
        return {"cid": job["it"]["cid"], "leak": out["leak"], "cue": out["cue"], "fix": out["fix"],
                "cost": cost, "request_id": rid, "usage": usage, "model": MODEL}

    c = Caller(CACHE, "leakage-check")
    c.run(jobs, fn)
    logged = {json.loads(l)["key"] for l in LOG.read_text().splitlines()} if LOG.exists() else set()
    with LOG.open("a") as f:
        for j in jobs:
            if j["key"] not in logged:
                r = c.cache[j["key"]]
                f.write(json.dumps({"key": j["key"], "cid": r["cid"], "leak": r["leak"], "cue": r["cue"], "fix": r["fix"],
                                    "request_id": r["request_id"], "model": MODEL,
                                    "item": {k: j["it"][k] for k in MASKED_FIELDS}}) + "\n")
    status()


def status():
    cands = {json.loads(l)["cid"]: json.loads(l) for l in CAND.read_text().splitlines() if l.strip()}
    log = [json.loads(l) for l in LOG.read_text().splitlines()]
    flagged_versions, current = {}, {}
    for r in log:
        if r["leak"]:
            flagged_versions.setdefault(r["cid"], set()).add(r["key"])
    for cid, it in cands.items():
        k = version_key(it)
        last = next((r for r in reversed(log) if r["key"] == k), None)
        n = len(flagged_versions.get(cid, ()))
        current[cid] = ("unchecked" if last is None else "dropped" if n >= 2 else "flagged" if last["leak"] else
                        "clean-after-rewrite" if n == 1 else "clean")
    out = ROOT / "items" / "leakage-status.json"
    out.write_text(json.dumps(current, indent=1, sort_keys=True))
    from collections import Counter
    print(Counter(current.values()))


if __name__ == "__main__":
    status() if "--status" in sys.argv else main()

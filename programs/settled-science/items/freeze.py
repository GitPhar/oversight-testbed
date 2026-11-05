"""Freeze the item set (pre-registration §2): keep candidates whose leakage status is clean or clean-after-rewrite,
assign ids ss-001.. in (side, field, arxiv_id, cid) order, write items/items.jsonl (with answers) and
items/masked.jsonl (what the bettor reads: no answer, title, authors, date, URL or quote), and their SHA-256s.
Refuses to freeze if fewer than 60 post-cutoff items survive (protocol/fixed-rules.md, Rule 2).

    python3 items/freeze.py
"""
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MIN_POST = 60
MASKED_KEYS = ("id", "field", "question", "methods", "option_a", "option_b")


def main():
    cands = [json.loads(l) for l in (ROOT / "items" / "candidates.jsonl").read_text().splitlines() if l.strip()]
    status = json.loads((ROOT / "items" / "leakage-status.json").read_text())
    keep = [c for c in cands if status.get(c["cid"]) in ("clean", "clean-after-rewrite")]
    keep.sort(key=lambda c: (0 if c["side"] == "post" else 1, c["field"], c["arxiv_id"], c["cid"]))
    n_post = sum(c["side"] == "post" for c in keep)
    if n_post < MIN_POST:
        sys.exit(f"only {n_post} post-cutoff items survive; at least {MIN_POST} are required before any bet")
    for n, c in enumerate(keep, 1):
        c["id"] = f"ss-{n:03d}"
        c["leakage_status"] = status[c["cid"]]
    full = "".join(json.dumps({"id": c["id"], **{k: v for k, v in c.items() if k != "id"}}) + "\n" for c in keep)
    masked = "".join(json.dumps({k: c[k] for k in MASKED_KEYS}) + "\n" for c in keep)
    (ROOT / "items" / "items.jsonl").write_text(full)
    (ROOT / "items" / "masked.jsonl").write_text(masked)
    sums = "".join(f"{hashlib.sha256(t.encode()).hexdigest()}  items/{n}\n" for n, t in (("items.jsonl", full), ("masked.jsonl", masked)))
    (ROOT / "items" / "SHA256SUMS").write_text(sums)
    print(sums)
    print(f"frozen {len(keep)} items: {n_post} post-cutoff, {len(keep) - n_post} pre-cutoff")
    print(sorted(Counter((c["side"], c["field"]) for c in keep).items()))
    print("dropped by leakage:", sum(1 for c in cands if status.get(c["cid"]) == "dropped"),
          "| unresolved:", sum(1 for c in cands if status.get(c["cid"]) in ("flagged", "unchecked", None)))


if __name__ == "__main__":
    main()

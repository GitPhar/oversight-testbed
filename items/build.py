"""Merge the drafts into items/candidates.jsonl: only items passing every mechanical check (verify.py), one record per
(paper, finding), at most two per paper, the cutoff side taken from the arXiv v1 date. No model calls.

    python3 items/build.py
"""
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
KEEP = ("field", "arxiv_id", "title", "first_author", "question", "methods", "option_a", "option_b", "true_option",
        "evidence_quote", "headline_side", "notes")


def main():
    paths = sorted((ROOT / "items" / "drafts").glob("*.jsonl"))
    items = []
    for p in paths:
        for n, line in enumerate(p.read_text().splitlines()):
            if line.strip():
                it = json.loads(line)
                it["arxiv_id"] = verify.re.sub(r"v\d+$", "", it.get("arxiv_id", "").strip().removeprefix("arXiv:"))
                it["_src"] = f"{p.name}:{n + 1}"
                items.append(it)
    meta = verify.fetch(sorted({i["arxiv_id"] for i in items}))
    per_paper, out, rejected = defaultdict(int), [], []
    for it in items:
        errs, side = verify.check(it, meta)
        if errs:
            rejected.append({"src": it["_src"], "arxiv_id": it["arxiv_id"], "errors": errs})
            continue
        if per_paper[it["arxiv_id"]] >= 2:
            rejected.append({"src": it["_src"], "arxiv_id": it["arxiv_id"], "errors": ["third item from one paper"]})
            continue
        per_paper[it["arxiv_id"]] += 1
        m = meta[it["arxiv_id"]]
        rec = {"cid": f"c-{it['arxiv_id']}-{per_paper[it['arxiv_id']]}", **{k: it.get(k) for k in KEEP},
               "v1_date": m["published"], "side": side, "draft": it["_src"]}
        rec["title"] = m["title"]
        out.append(rec)
    (ROOT / "items" / "candidates.jsonl").write_text("".join(json.dumps(r) + "\n" for r in out))
    (ROOT / "items" / "build-rejected.json").write_text(json.dumps(rejected, indent=1))
    print(f"{len(items)} drafts -> {len(out)} candidates; rejected {len(rejected)}")
    print("by side:", Counter(r["side"] for r in out))
    print("by field x side:", sorted(Counter((r["field"], r["side"]) for r in out).items()))
    for r in rejected:
        print("  REJ", r["src"], r["arxiv_id"], "|", "; ".join(r["errors"]))


if __name__ == "__main__":
    main()

"""Apply the item-writer's one rewrite per flagged item (protocol/leakage-check.md, step 2) to items/candidates.jsonl.

    python3 items/apply_rewrites.py <rewrites.json>    -> items/rewrites.jsonl (before/after record), candidates updated

A rewrite may change only question, methods, option_a and option_b (wording). It may not touch true_option, headline_side,
the paper or the evidence quote. Each rewritten item must pass verify.check again. Only items flagged once may be
rewritten; a second rewrite of the same item is refused."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
WORDING = {"question", "methods", "option_a", "option_b"}


def main(src):
    rw = json.loads(Path(src).read_text())
    cpath, rpath = ROOT / "items" / "candidates.jsonl", ROOT / "items" / "rewrites.jsonl"
    cands = [json.loads(l) for l in cpath.read_text().splitlines() if l.strip()]
    status = json.loads((ROOT / "items" / "leakage-status.json").read_text())
    done = {json.loads(l)["cid"] for l in rpath.read_text().splitlines()} if rpath.exists() else set()
    meta = json.loads((ROOT / "items" / "arxiv-meta.json").read_text())
    log = []
    for c in cands:
        if c["cid"] not in rw:
            continue
        if status.get(c["cid"]) != "flagged" or c["cid"] in done:
            sys.exit(f"{c['cid']}: only an item flagged once, and not yet rewritten, may be rewritten")
        change = rw[c["cid"]]
        if set(change) - WORDING:
            sys.exit(f"{c['cid']}: rewrite touches {set(change) - WORDING}")
        before = {k: c[k] for k in change}
        c.update(change)
        errs, _ = verify.check(c, meta)
        if errs:
            sys.exit(f"{c['cid']}: rewrite fails the mechanical check: {errs}")
        log.append({"cid": c["cid"], "before": before, "after": change, "written_by": "item-writer session (claude-opus-5-5)",
                    "at": "2026-11-04 America/Denver"})
    if len(log) != len(rw):
        sys.exit("some rewrite ids are not candidates")
    cpath.write_text("".join(json.dumps(c) + "\n" for c in cands))
    with rpath.open("a") as f:
        f.writelines(json.dumps(r) + "\n" for r in log)
    print(f"applied {len(log)} rewrites")


if __name__ == "__main__":
    main(sys.argv[1])

#!/usr/bin/env python3
"""check_remap.py: no map may end at a landed bet with no follow-up (operators/remap.md).

    python3 ledger/check_remap.py            # every map/<program>.json against ledger/bets.jsonl
    python3 ledger/check_remap.py --quiet    # only the verdict line and the errors

Reads only committed files: map/*.json (what the cockpit reads) and ledger/bets.jsonl. No network, no model.

A node is landed or mixed by its ledger bets (verdict_after_audit if set, else verdict): pass / pass-unreplicated / hit
is landed; mixed / undetermined is mixed. A node with no bet uses its own map status (hit, mixed). Each landed or mixed
node needs a follow-up: a child (parent == its id, or its id in the child's also_follows) that is open, running, parked
or carried into another program (moved_to), or a landed child (checked in turn). A dated closed_line also satisfies it,
and is printed so a reader can judge it. Fewer than two not-yet-run follow-ups is a warning, not an error.
Exit 1 if any landed or mixed node is a leaf.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANDED = {"pass", "pass-unreplicated", "hit"}
MIXED = {"mixed", "undetermined"}
OPEN = {"open", "running", "parked", "bet", ""}


def verdict(b):
    return str(b.get("verdict_after_audit") or b.get("verdict") or "").strip().lower()


def node_bets(node, program, bets):
    ids = [str(x) for x in ([node["bets"]] if isinstance(node.get("bets"), str) else node.get("bets") or [])]
    if ids:
        return [b for b in bets if b.get("id") in ids]
    return [b for b in bets if b.get("program") == program and str(b.get("direction", "")) == str(node.get("id"))]


def state(node, program, bets):
    """landed | mixed | open | dead"""
    if node.get("moved_to"):
        return "open"
    vs = [verdict(b) for b in node_bets(node, program, bets)]
    if vs:
        if any(v in LANDED for v in vs):
            return "landed"
        if any(v in MIXED for v in vs):
            return "mixed"
        if any(v in {"open", "running", ""} for v in vs):
            return "open"
        return "dead"
    s = str(node.get("status", "")).strip().lower()
    if s in LANDED:
        return "landed"
    if s in MIXED:
        return "mixed"
    if s in OPEN:
        return "open"
    return "dead"


def main():
    quiet = "--quiet" in sys.argv
    bets = [json.loads(l) for l in (ROOT / "ledger" / "bets.jsonl").read_text().splitlines() if l.strip()]
    errors, warnings, closed, checked = [], [], [], 0
    for f in sorted((ROOT / "map").glob("*.json")):
        m = json.loads(f.read_text())
        program = m.get("program") or f.stem
        nodes = m.get("directions") or []
        st = {str(n.get("id")): state(n, program, bets) for n in nodes}
        kids = {}
        for n in nodes:
            for p in [n.get("parent")] + list(n.get("also_follows") or []):
                if p is not None:
                    kids.setdefault(str(p), []).append(str(n.get("id")))
        for n in nodes:
            nid = str(n.get("id"))
            if st[nid] not in ("landed", "mixed"):
                continue
            checked += 1
            ch = kids.get(nid, [])
            fresh = [c for c in ch if st.get(c) == "open"]
            onward = fresh + [c for c in ch if st.get(c) in ("landed", "mixed")]
            if n.get("closed_line"):
                closed.append(f"{f.name} {nid}: closed_line: {n['closed_line']}")
            elif not onward:
                errors.append(f"{f.name} {nid} ({st[nid]}): ends the map; no follow-up "
                              f"(children: {', '.join(f'{c}={st.get(c)}' for c in ch) or 'none'})")
            elif len(fresh) < 2 and not any(st.get(c) in ("landed", "mixed") for c in ch):
                warnings.append(f"{f.name} {nid} ({st[nid]}): {len(fresh)} not-yet-run follow-up(s); remap.md asks for two")
    if not quiet:
        for c in closed:
            print("closed  ", c)
        for w in warnings:
            print("warning ", w)
    for e in errors:
        print("ERROR   ", e)
    if errors:
        print(f"FAIL: {len(errors)} landed or mixed node(s) end the map ({checked} checked)")
        sys.exit(1)
    print(f"OK: no map ends at a landed bet ({checked} landed or mixed nodes checked, {len(warnings)} warning(s))")


if __name__ == "__main__":
    main()

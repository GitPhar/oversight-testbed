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

Rule 16, the layer line (CONTEXT.md section 3; ledger/rule16.py): a program that is not released (no landed result
labelled partly new or new in its newest layer, no steer from Sean carrying rule16_release) may hold nothing open,
running or pre-registered deeper than layer 5: no such direction on its map and no such bet in the ledger. Past the
line its next action is a closing review, so a follow-up the remap owes there goes on the map as parked, with the
note "parked: rule 16 layer line". A closed program (map status "closed") may hold no open or running direction.
Each one found is an error (exit 1). Programs at the dollar line are printed, not failed; the budget code stops them.
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
    sys.path.insert(0, str(ROOT / "ledger"))
    from merge_inbox import effective   # rows still in ledger/inbox/ count
    bets = effective("bets")
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
    errors += rule16_errors(bets, quiet)
    if not quiet:
        for c in closed:
            print("closed  ", c)
        for w in warnings:
            print("warning ", w)
    for e in errors:
        print("ERROR   ", e)
    if errors:
        print(f"FAIL: {len(errors)} error(s): landed or mixed node(s) ending the map ({checked} checked) or rule 16")
        sys.exit(1)
    print(f"OK: no map ends at a landed bet ({checked} landed or mixed nodes checked, {len(warnings)} warning(s)); "
          "rule 16: nothing open past a program's layer line")


def rule16_errors(bets, quiet=False):
    """Rule 16's layer line, and a closed program's open directions (ledger/rule16.py)."""
    import rule16
    from merge_inbox import effective
    from prior import depth, layer_of
    steers = effective("steers")
    _, _, maps = rule16.load(ROOT, with_inbox=False)
    by_id = {b["id"]: b for b in bets}
    out = []
    for prog in sorted(maps):
        m = maps[prog]
        s = rule16.status(prog, bets, steers, maps)
        if not quiet and (s["past_layer_line"] or s["past_dollar_line"]):
            print("rule 16 ", f"{prog}: at the {'layer' if s['past_layer_line'] else 'dollar'} line "
                  f"(layers deep {s['layers_deep']}, newest settled {s['newest_layer']}, ${s['usd_month']:.2f} in "
                  f"{s['month']}); next action: a closing review" + (f" (reviewed {s['closing_review']})" if s['closing_review'] else ""))
        nodes = m.get("directions") or []
        live = [n for n in nodes if str(n.get("status", "")).strip().lower() in {"open", "running", "bet"}]
        if s["closed"]:
            for n in live:
                out.append(f"{prog} {n.get('id')}: {n.get('status')} on a closed program (map status closed); "
                           "park it with the closing review's note")
            continue
        if s["released_by_result"]:
            continue
        for n in live:
            d = depth(m, n.get("id"))
            if d > s["layer_line"]:
                out.append(f"{prog} {n.get('id')}: {n.get('status')} at layer {d}, past rule 16's layer line "
                           f"({s['layer_line']}); the program's next action is a closing review; park it "
                           "('parked: rule 16 layer line') or log a steer from Sean")
        for b in bets:
            if b.get("program") != prog or str(b.get("verdict_after_audit") or b.get("verdict") or "").lower() not in {"open", "running", ""}:
                continue
            d, _ = layer_of(b, by_id, maps)
            if d and d > s["layer_line"]:
                out.append(f"{prog} bet {b['id']}: {b.get('verdict') or 'open'} at layer {d}, past rule 16's layer line "
                           f"({s['layer_line']}) with no release")
    return out


if __name__ == "__main__":
    main()

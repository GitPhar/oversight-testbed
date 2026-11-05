#!/usr/bin/env python3
"""Pick up the cockpit's saved answers and add them to the ledger.

The cockpit (site/cockpit.html) saves `human-odds.jsonl` to Sean's Downloads folder: every line already in
ledger/human-odds.jsonl plus his new ones. Every local session runs this at start (CONTEXT.md §3 rule 11):

    python3 ledger/pickup_human_odds.py            # reads ~/Downloads/human-odds*.jsonl, appends, prints a summary
    python3 ledger/pickup_human_odds.py --dry-run  # says what it would add, changes nothing
    python3 ledger/pickup_human_odds.py FILE ...   # other files instead of ~/Downloads

What it does:
  - appends to ledger/human-odds.jsonl every valid line whose id is not there yet, oldest first; lines are never
    edited, and a change of mind is a later line for the same direction;
  - for a line with `worth_spend: false` (Sean answered "No" to "Would you spend about $X on it?"), appends a
    `veto` steer to ledger/steers.jsonl citing the line, unless one already cites it (operators/veto.md: it gets a
    shadow check later);
  - never deletes the downloaded file and never commits: the session commits ledger/human-odds.jsonl and
    ledger/steers.jsonl with the file's name in the message.
"""
import argparse
import glob
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REQUIRED = ("id", "program", "direction", "recorded", "human")


def read_jsonl(path):
    out = []
    if not os.path.isfile(path):
        return out
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        s = line.strip()
        if not s:
            continue
        try:
            out.append(json.loads(s))
        except ValueError:
            print(f"  skip {os.path.basename(path)}:{n}: not JSON", file=sys.stderr)
    return out


def valid(row):
    if any(row.get(k) in (None, "") for k in REQUIRED) or not str(row["id"]).startswith("ho-"):
        return "missing a required field"
    o = row.get("human_odds")
    if o is not None and not (isinstance(o, (int, float)) and 0 <= o <= 1):
        return "human_odds outside 0-1"
    if o is None and row.get("worth_spend") is None and row.get("expects_hit") is None:
        return "no answer in it"
    return None


def veto_for(row):
    return {
        "id": "st-" + row["id"][3:], "date": row.get("date"), "time": row.get("time"), "human": row["human"],
        "program": row["program"], "action": "veto", "direction": row["direction"],
        "reason": f"Cockpit: answered No to \"Would you spend {row.get('spend_asked') or 'what it costs'} on it?\" "
                  f"for: {row.get('question') or row['direction']}",
        "outcome": None, "outcome_later": None, "evidence": [f"ledger/human-odds.jsonl {row['id']}"],
        "value": "pending", "value_judgment": None, "counterfactual": None, "value_judged_by": None, "scored": False,
        "recorded": row["recorded"], "recorded_via": "site/cockpit.html, via ledger/pickup_human_odds.py",
        "from_human_odds": row["id"],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("files", nargs="*", help="files to read (default: ~/Downloads/human-odds*.jsonl)")
    ap.add_argument("--ledger", default=os.path.join(ROOT, "ledger"))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    files = a.files or sorted(glob.glob(os.path.expanduser("~/Downloads/human-odds*.jsonl")))
    odds_path, steers_path = os.path.join(a.ledger, "human-odds.jsonl"), os.path.join(a.ledger, "steers.jsonl")
    have = {r.get("id") for r in read_jsonl(odds_path)}
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from merge_inbox import effective
    steers = effective("steers", a.ledger)   # a veto still waiting in ledger/inbox/ counts, so it is never written twice
    cited = {s.get("from_human_odds") for s in steers if s.get("from_human_odds")}
    if not files:
        print("No cockpit file in ~/Downloads (human-odds*.jsonl). Nothing to add.")
        return 0
    new = {}
    for f in files:
        for r in read_jsonl(f):
            why = valid(r)
            if why:
                print(f"  skip {os.path.basename(f)} {r.get('id')}: {why}", file=sys.stderr)
            elif r["id"] not in have:
                new.setdefault(r["id"], r)
    rows = sorted(new.values(), key=lambda r: str(r["recorded"]))
    vetoes = [veto_for(r) for r in rows if r.get("worth_spend") is False and r["id"] not in cited]
    print(f"Read {len(files)} file(s): {', '.join(os.path.basename(f) for f in files)}")
    print(f"{len(rows)} new answer line(s) for ledger/human-odds.jsonl; {len(vetoes)} veto steer(s) for ledger/steers.jsonl")
    for r in rows:
        bits = [f"odds {r['odds_pct']}%" if r.get("odds_pct") is not None else None,
                {True: "would spend", False: "would NOT spend"}.get(r.get("worth_spend")),
                {True: "expects a hit", False: "expects no hit"}.get(r.get("expects_hit"))]
        print(f"  {r['id']}  {r['program']}|{r['direction']}: {', '.join(b for b in bits if b)}")
    if a.dry_run or not rows:
        return 0
    with open(odds_path, "a", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    inbox = None
    if vetoes:
        # From 2026-11-05 no session writes steers.jsonl directly (ledger/inbox/README.md): each veto goes to this
        # session's inbox file, which ledger/merge_inbox.py folds into steers.jsonl.
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from merge_inbox import append, ROOT as INBOX_ROOT
        for s in vetoes:
            inbox = append({"op": "add", "file": "steers", "row": s})
        inbox = os.path.relpath(inbox, INBOX_ROOT)
    print("Appended. Now commit: git commit -m \"Cockpit answers from <file>\" -- ledger/human-odds.jsonl"
          + (f" {inbox}; then python3 ledger/merge_inbox.py --commit" if inbox else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())

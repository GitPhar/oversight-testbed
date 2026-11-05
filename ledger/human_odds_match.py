"""Which of Sean's cockpit lines a bet must carry (CONTEXT.md §3 rule 11; steer st-18).

A bet must carry the human odds of the first line in ledger/human-odds.jsonl for its program and direction
that was committed to the ledger before the bet's pre-registration commit. A line that arrived after the
pre-registration is never filled in later: the bet stays `human_odds: null` with the time order in its note.

    python3 ledger/human_odds_match.py                    # every bet: what it carries vs what it must carry
    python3 ledger/human_odds_match.py <program> <dir>    # before pre-registering: the line to copy, if any

Used by ledger/check_prereg.py (check H1) and reproduce.py (step 1). No network, no keys.
"""
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def _git(*a):
    r = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def direction_token(d):
    """'program-2-map P2-6' -> 'P2-6'; 'sg-d1' -> 'sg-d1'."""
    return str(d or "").split()[-1] if str(d or "").split() else ""


def arrivals():
    """id -> datetime the line was first committed to ledger/human-odds.jsonl (None if not committed yet)."""
    out, when = {}, None
    for line in _git("log", "--reverse", "--format=@@%cI", "-p", "--", "ledger/human-odds.jsonl").splitlines():
        if line.startswith("@@") and not line.startswith("@@ "):
            when = datetime.fromisoformat(line[2:])
        elif line.startswith("+{"):
            try:
                i = json.loads(line[1:]).get("id")
            except ValueError:
                continue
            out.setdefault(i, when)
    return out


def lines():
    p = HERE / "human-odds.jsonl"
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def commit_time(sha):
    s = _git("log", "-1", "--format=%cI", str(sha or "")).strip() if sha else ""
    return datetime.fromisoformat(s) if s else None


def due(program, direction, t_pre, rows=None, arr=None):
    """The first line for this program and direction committed before t_pre, else None."""
    rows = lines() if rows is None else rows
    arr = arrivals() if arr is None else arr
    tok = direction_token(direction)
    cands = [r for r in rows if r.get("program") == program and r.get("direction") == tok
             and arr.get(r["id"]) is not None and (t_pre is None or arr[r["id"]] < t_pre)]
    return sorted(cands, key=lambda r: (arr[r["id"]], str(r.get("recorded"))))[0] if cands else None


def check_bet(b, rows=None, arr=None):
    """(ok, message). ok is None when the pre-registration commit cannot be resolved."""
    t_pre = commit_time(b.get("prereg_commit"))
    if t_pre is None:
        return None, f"{b['id']}: pre-registration commit {b.get('prereg_commit')!r} not resolvable; not checked"
    line = due(b.get("program"), b.get("direction"), t_pre, rows, arr)
    have = b.get("human_odds")
    if line is None:
        if have is None:
            return True, f"{b['id']}: no cockpit line before its pre-registration; human_odds null is right"
        return True, f"{b['id']}: carries human_odds {have} (no cockpit line before its pre-registration; source in its note)"
    want = line.get("human_odds")
    good = have is not None and abs(float(have) - float(want)) < 1e-9 and line["id"] in str(b.get("human_odds_at") or "")
    return good, (f"{b['id']}: must carry human_odds {want} from {line['id']} (committed before its pre-registration); "
                  f"carries {have}, human_odds_at {b.get('human_odds_at')!r}")


def main():
    rows, arr = lines(), arrivals()
    if len(sys.argv) == 3:
        line = due(sys.argv[1], sys.argv[2], datetime.now().astimezone(), rows, arr)
        if line:
            print(f'human_odds {line["human_odds"]}, human_odds_at "{line["id"]}" ({line["recorded"]}); '
                  f'event Sean answered: {line.get("event")}')
        else:
            print('no human odds: human_odds null, human_odds_note "no human odds"')
        return 0
    bets = [json.loads(l) for l in (HERE / "bets.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    bad = 0
    for b in bets:
        ok, msg = check_bet(b, rows, arr)
        if ok is False:
            bad += 1
            print("FAIL " + msg)
    print(f"{len(bets)} bets checked against {len(rows)} cockpit lines; {bad} missing human odds")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())

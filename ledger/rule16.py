"""Rule 16: how far a program may run without a result (CONTEXT.md section 3 rule 16; ARCHITECTURE.md invariant 16).

    python3 ledger/rule16.py            # each program's two counts against the two lines, this month, live
    python3 ledger/rule16.py <program>  # one program

In plain English: a program may run at most five layers deep on its map, and spend at most $15 of API in a calendar
month, unless the newest layer it has settled holds a landed result labelled partly new or new, or Sean has given a
steer that lets it go further. Past either line, the program's next action is a closing review by a fresh session
(operators/remap.md, "Closing a program"), not another bet. Sean's words (planning chat, 2026-11-05 16:04): "we still
probably want to have some sort of limit, some maximum branches or iterations or generations".

Who uses this file:
- ledger/prior.py reports both counts per program in its "Closing reviews due" table (from the folded ledger only,
  and with "this month" fixed as the month of the newest dated bet row, so prior.md stays reproducible byte for byte);
- ledger/check_remap.py enforces the layer line: no open, running or pre-registered direction or bet deeper than
  layer 5 in a program that is not released (exit 1);
- each program's budget code enforces the dollar line (DollarLine below), live: the ledger with every inbox row
  applied, and this month by the clock. Its shared Caller checks before every paid call; its client factory checks
  once, at the first paid client of a run, so a script that bypasses the Caller is stopped at its start (a run that
  starts under the line and makes its calls outside a Caller can cross the line by at most its own run cap).
  Program 3 (nature-graded) makes no API calls; its chip seconds are rule 7's.

The definitions, once:
- A bet's layer is its direction's depth on map/<program>.json (prior.layer_of: 1 for a scouted direction with no
  parent, one more per parent step; a re-bet sits at its parent bet's layer, a replication one under it).
- Layers deep: the deepest layer holding a bet that was not withdrawn (open and running bets count: they are where
  the program is). The newest layer: the deepest layer holding a settled bet (a verdict other than open or
  withdrawn).
- Released by a result: the newest layer holds a bet whose verdict is landed (pass, pass-unreplicated, hit) and
  whose Novelty line is partly new or new (the bet row's novelty, else its map node's). Both lines lift together.
- Released by Sean: a row in ledger/steers.jsonl for the program carrying "rule16_release":
  {"lines": ["layers", "dollars"], "layers_to": <the deepest layer allowed>, "usd_month_to": <dollars allowed this
  month>, "month": "YYYY-MM"}. A dollars release counts only in its month; a layers release up to layers_to. The
  session that logs a steer from Sean's words fills the field from those words, and only when his words say to go on.
- This month's dollars: the larger of (a) the cost_usd of the program's bet rows dated in the month and (b) the
  program's own count of what it has spent, which its budget code passes in. The programs' call caches carry no
  dates, so (b) is everything the program has spent; every program began in November 2026, so today that is exact,
  and from December it can only overcount, which stops a call early and never lets one through.
- A closed program (map status "closed", a closing review's decision) makes no paid call, except a shadow check of
  one of Sean's vetoes (operators/veto.md; DollarLine(..., shadow_of=<the veto's steer id>)), which has its own cap.
  Only a new reason its diagnosis does not cover, or a steer from Sean, reopens it.

Standard library only; no network, no keys.
"""
import json
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
LAYER_LINE = 5
USD_MONTH_LINE = 15.00

sys.path.insert(0, str(HERE))
from prior import layer_of, node_for, verdict, LANDED, NOVEL, UNSETTLED  # noqa: E402


def _rows(p):
    p = Path(p)
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()] if p.exists() else []


def load(root=ROOT, with_inbox=True):
    """bets, steers and engine maps; with_inbox applies every inbox line (what the budget code and check_remap read)."""
    root = Path(root)
    if with_inbox:
        from merge_inbox import effective
        bets, steers = effective("bets", root / "ledger"), effective("steers", root / "ledger")
    else:
        bets, steers = _rows(root / "ledger" / "bets.jsonl"), _rows(root / "ledger" / "steers.jsonl")
    maps = {}
    for f in sorted((root / "map").glob("*.json")):
        m = json.loads(f.read_text(encoding="utf-8"))
        maps[m.get("program") or f.stem] = m
    return bets, steers, maps


def ledger_month(bets):
    """The month of the newest dated bet row (YYYY-MM): prior.py's fixed "this month"."""
    ds = sorted(str(b.get("date") or "")[:7] for b in bets if len(str(b.get("date") or "")) >= 7)
    return ds[-1] if ds else None


def status(program, bets, steers, maps, month=None, spent_usd=None):
    """Both counts for one program against both lines. month: YYYY-MM (default: the clock's month)."""
    month = month or datetime.now().strftime("%Y-%m")
    by_id = {b["id"]: b for b in bets}
    m = maps.get(program) or {}
    mine = [b for b in bets if b.get("program") == program]
    placed = []
    for b in mine:
        d, _ = layer_of(b, by_id, maps)
        placed.append((d, b))
    alive = [d for d, b in placed if d and verdict(b) != "withdrawn"]
    settled = [(d, b) for d, b in placed if d and verdict(b) not in UNSETTLED]
    deep = max(alive) if alive else 0
    newest = max(d for d, _ in settled) if settled else 0
    newest_bets = [b for d, b in settled if d == newest]

    def novelty(b):
        n = node_for(b, m)
        return str(b.get("novelty") or (n or {}).get("novelty") or "").strip().lower()

    by_result = [b["id"] for b in newest_bets if verdict(b) in LANDED and novelty(b) in NOVEL]
    ledger_usd = sum(float(b.get("cost_usd") or 0) for b in mine if str(b.get("date") or "").startswith(month))
    usd = max(ledger_usd, float(spent_usd or 0))
    rel_layers, rel_usd = [], []
    for s in steers:
        r = s.get("rule16_release")
        if s.get("program") != program or not isinstance(r, dict):
            continue
        lines = r.get("lines") or []
        if "layers" in lines and int(r.get("layers_to") or 0) > LAYER_LINE:
            rel_layers.append((s.get("id"), int(r["layers_to"])))
        if "dollars" in lines and r.get("month") == month:
            rel_usd.append((s.get("id"), float(r.get("usd_month_to") or 0)))
    layers_to = max([LAYER_LINE] + [t for _, t in rel_layers])
    usd_to = max([USD_MONTH_LINE] + [t for _, t in rel_usd])
    closed = str(m.get("status") or "").strip().lower() == "closed"
    # The line is reached when the program's next layer would pass it (its newest settled layer is at the line), or a
    # bet already sits past it; the dollar line when this month's spend has reached it.
    at_layer = (not by_result) and max(deep, newest + 1 if newest else 0) > layers_to
    at_usd = (not by_result) and usd >= usd_to
    rev = m.get("closing_review") or {}
    seen = set(rev.get("bets_reviewed") or [])
    unseen = [b["id"] for d, b in settled if b["id"] not in seen]
    return dict(program=program, month=month, layers_deep=deep, newest_layer=newest, layer_line=layers_to,
                usd_month=round(usd, 4), ledger_usd_month=round(ledger_usd, 4), usd_line=usd_to,
                released_by_result=by_result, released_by_steer=[i for i, _ in rel_layers + rel_usd],
                past_layer_line=at_layer, past_dollar_line=at_usd, closed=closed,
                closing_review=rev.get("date") and f"{rev.get('date')} ({rev.get('decision')})",
                reviewed_since_line=bool(rev) and not unseen)


class Rule16Stop(SystemExit):
    pass


class DollarLine:
    """The dollar line in a program's budget code. Built once per run with the program's own count of what it has
    spent (0 if its code keeps none); it refuses to start (SystemExit) if the program is closed or already at the
    line, and blocks(run_spent) says, before each paid call, whether this run's spend so far puts the month at the
    line.

        line = rule16.DollarLine("test-awareness", program_spent_so_far)   # SystemExit if refused
        ...
        if line.blocks(spent_in_this_run): stop the run, report "rule 16 dollar line"
    """

    def __init__(self, program, spent_usd=0.0, root=ROOT, shadow_of=None):
        try:
            bets, steers, maps = load(root)
        except Exception as e:   # no ledger, no paid call: fail closed
            raise Rule16Stop(f"rule 16: cannot read the ledger and maps at {root} ({e!r}); no paid call may run")
        s = status(program, bets, steers, maps, spent_usd=spent_usd)
        self.program, self.status = program, s
        # A shadow check of one of Sean's vetoes (operators/veto.md) is the one paid run a closed or capped program
        # still makes: it is how the ledger learns whether the veto saved money or killed a hit, and it has its own
        # cap (the lesser of $2 and 10% of the vetoed budget) and the $5 monthly shadow pool. The shadow's code names
        # the veto steer; it must be a veto of this program in ledger/steers.jsonl with a shadow row.
        if shadow_of is not None:
            ok = any(x.get("id") == shadow_of and x.get("action") == "veto" and x.get("program") == program
                     for x in steers)
            if not ok:
                raise Rule16Stop(f"{program}: shadow_of={shadow_of!r} names no veto of this program in ledger/steers.jsonl")
            self.released, self.line, self.start, self.shadow_of = True, None, s["usd_month"], shadow_of
            return
        self.shadow_of = None
        self.released = bool(s["released_by_result"])
        self.line = None if self.released else s["usd_line"]
        self.start = s["usd_month"]
        if s["closed"]:
            raise Rule16Stop(f"{program}: the program is closed on map/{program}.json (closing review "
                             f"{s['closing_review']}); no paid call may run. Only a new reason its diagnosis does not "
                             "cover, or a steer from Sean, reopens it (operators/remap.md, Closing a program).")
        if self.line is not None and self.start >= self.line:
            raise Rule16Stop(self.message(self.start))

    def blocks(self, run_spent=0.0):
        return self.line is not None and self.start + float(run_spent) >= self.line

    def message(self, spent_usd=None):
        spent_usd = self.start if spent_usd is None else spent_usd
        return (f"{self.program}: rule 16 dollar line: ${spent_usd:.2f} spent in {self.status['month']}, line "
                f"${self.line:.2f}, and the newest layer ({self.status['newest_layer']}) holds no landed result "
                "labelled partly new or new, and no steer from Sean lifts the line. The program's next action is a "
                "closing review (operators/remap.md, Closing a program); no paid call may run.")


def main():
    bets, steers, maps = load()
    progs = sys.argv[1:] or sorted({b["program"] for b in bets})
    for p in progs:
        s = status(p, bets, steers, maps)
        flag = []
        if s["closed"]:
            flag.append("closed")
        if s["past_layer_line"]:
            flag.append("at the layer line")
        if s["past_dollar_line"]:
            flag.append("at the dollar line")
        print(f"{p}: layers deep {s['layers_deep']} (newest settled {s['newest_layer']}; line {s['layer_line']}), "
              f"{s['month']} ledger ${s['ledger_usd_month']:.2f} (line ${s['usd_line']:.2f}); released by "
              f"{', '.join(s['released_by_result'] + s['released_by_steer']) or 'nothing'}; "
              f"{', '.join(flag) or 'inside both lines'}")


if __name__ == "__main__":
    main()

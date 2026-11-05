"""Check a pre-registration against the feedback-loop rules before its bet row is appended,
and before its first call. No network, no keys.

    python3 ledger/check_prereg.py <bet-id> <repo> <prereg-path> [--before-run]

<repo> is the engine repo (/Users/seanpharris/oversight-testbed); <prereg-path> is programs/<name>/experiments/<file>.

Checks (operators/learn.md, operators/design-review.md):
  L1  the pre-registration's §0 has a filled `lesson` row, committed with the pre-registration
  L2  ledger/lessons.jsonl has ls-<bet-id> whose `lesson` matches it and whose prereg_commit matches
  L3  the lesson names a pattern id that exists in lessons.jsonl, or says "none applies"
  R1  ledger/design-reviews/<bet-id>.md exists, committed after the pre-registration
  R2  its verdict is go, or fix-first with confirmed_at set (redesign: the bet must be withdrawn)
  R3  if the bet has a result commit, the review was committed before it
  H1  if Sean's cockpit line for this direction reached ledger/human-odds.jsonl before the pre-registration
      commit, the bet row carries its human_odds and names its id in human_odds_at (ledger/human_odds_match.py)
With --before-run, a missing L2 is a warning (the ledger row follows the pre-registration) and R3 is skipped.
Exit 0 if every check passes, 1 otherwise. Prints one line per check.
"""
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def git(repo, *a):
    r = subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def ctime(repo, sha):
    s = git(repo, "log", "-1", "--format=%cI", sha)
    return datetime.fromisoformat(s) if s else None


def norm(s):
    return re.sub(r"\s+", " ", re.sub(r"[*_`]", "", s or "")).strip().lower()


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    before_run = "--before-run" in sys.argv
    if len(args) != 3:
        sys.exit(__doc__)
    bet, repo, path = args
    repo = Path(repo)
    res = []
    ok = lambda k, good, msg: res.append((k, "ok" if good else "FAIL", msg))
    warn = lambda k, msg: res.append((k, "warn", msg))

    # The pre-registration commit: the commit that added the file. Programs folded in with `git subtree add`
    # keep their original commits, where the file sits at its pre-fold path (without programs/<name>/), so try both.
    cands = [path]
    m0 = re.match(r"^programs/[^/]+/(.+)$", path)
    if m0:
        cands.append(m0.group(1))
    pc, text = "", ""
    for cand in cands:
        hits = git(repo, "log", "--all", "--full-history", "--diff-filter=A", "--format=%h", "--", cand).splitlines()
        for h in reversed(hits):                       # oldest first: the commit that froze it
            t = git(repo, "show", f"{h}:{cand}")
            if t:
                pc, text = h, t
                break
        if pc:
            break
    m = re.search(r"^\|\s*lesson\s*\|\s*(.+?)\s*\|\s*$", text, re.M | re.I)
    lesson = m.group(1) if m else ""
    low = lesson.lower()
    filled = bool(lesson) and "<" not in lesson and ("correcting" in low or "none applies" in low)
    ok("L1", bool(pc) and filled, f"§0 lesson row at pre-registration commit {pc or '?'}: " + (lesson[:90] + "…" if lesson else "missing"))

    rows = [json.loads(l) for l in (HERE / "lessons.jsonl").read_text().splitlines() if l.strip()]
    patterns = {r["id"] for r in rows if r.get("kind") == "pattern"}
    # One lesson may cover several bets pre-registered together ("covers": [...]).
    ln = next((r for r in rows if r.get("kind") == "lesson" and (r.get("bet") == bet or bet in (r.get("covers") or []))), None)
    if ln is None:
        (warn if before_run else lambda k, msg: ok(k, False, msg))("L2", f"no ls-{bet} line in ledger/lessons.jsonl")
    else:
        same = norm(ln.get("lesson")) == norm(lesson)
        commit_ok = bool(pc) and str(ln.get("prereg_commit", "")).startswith(pc[:7])
        ok("L2", same and commit_ok, f"ls-{bet}: text {'matches' if same else 'differs from'} §0; prereg_commit {'matches' if commit_ok else 'differs'}")
    cited = set(re.findall(r"\bP\d+\b(?!-\d)", lesson))   # "P3-5" names a direction, not pattern P3
    ok("L3", ("none applies" in lesson.lower()) or (cited and cited <= patterns),
       f"patterns cited: {sorted(cited) or 'none'}" + (f"; unknown: {sorted(cited - patterns)}" if cited - patterns else ""))

    # One design review may cover several bets: the bet row's design_review.path names it.
    rv = ROOT / "ledger" / "design-reviews" / f"{bet}.md"
    try:
        _rows = [json.loads(l) for l in (HERE / "bets.jsonl").read_text().splitlines() if l.strip()]
        _b = next((x for x in _rows if x["id"] == bet), None)
        _path = ((_b or {}).get("design_review") or {}).get("path")
        if _path and (ROOT / _path).exists():
            rv = ROOT / _path
    except Exception:
        pass
    if not rv.exists():
        ok("R1", False, f"no {rv.relative_to(ROOT)}")
    else:
        rc = git(ROOT, "log", "--diff-filter=A", "--format=%h", "--", str(rv.relative_to(ROOT))).splitlines()
        rc = rc[-1] if rc else ""
        t_rev, t_pre = (ctime(ROOT, rc) if rc else None), (ctime(repo, pc) if pc else None)
        ok("R1", bool(rc) and t_rev and t_pre and t_rev > t_pre,
           f"review committed {rc or 'not yet'} at {t_rev}; pre-registration at {t_pre}")
        head = rv.read_text().split("\n---", 2)[0]
        verdict = (re.search(r"^verdict:\s*(\S+)", head, re.M) or [None, ""])[1]
        per_bet = re.search(r"^verdict_by_bet:\s*\{(.*)\}", head, re.M)      # a review covering several bets
        if per_bet:
            m_b = re.search(rf"{re.escape(bet)}\s*:\s*([\w-]+)", per_bet.group(1))
            if m_b:
                verdict = m_b.group(1)
        conf = (re.search(r"^confirmed_at:\s*(.+)$", head, re.M) or [None, "null"])[1].strip()
        ok("R2", verdict == "go" or (verdict == "fix-first" and conf not in ("", "null")),
           f"verdict {verdict or '?'}" + (f", confirmed {conf}" if verdict == "fix-first" else ""))
        # Every review of this bet must clear it, not only the first one found (<bet>.md and <bet>-*.md):
        # when two reviewers are run, the stricter verdict binds.
        # Any file named for this bet: "<bet>.md" or "<bet>" followed by a non-alphanumeric character
        # ("<bet>-1b.md", "<bet>_extra.md", "<bet>-1b-r2.md"), but not another bet that merely shares the
        # prefix ("em-qwalk2.md" is not a review of "em-qwalk"). Odd names must not slip past (em-qwalk2-1b F-C).
        others = sorted(p for p in (ROOT / "ledger" / "design-reviews").glob(f"{bet}*.md")
                        if p != rv and (p.stem == bet or (len(p.stem) > len(bet) and not p.stem[len(bet)].isalnum())))
        for o in others:
            oh = o.read_text().split("\n---", 2)[0]
            ov = (re.search(r"^verdict:\s*(\S+)", oh, re.M) or [None, ""])[1]
            ob = re.search(r"^verdict_by_bet:\s*\{(.*)\}", oh, re.M)
            if ob:
                mb = re.search(rf"{re.escape(bet)}\s*:\s*([\w-]+)", ob.group(1))
                ov = mb.group(1) if mb else ov
            oc = (re.search(r"^confirmed_at:\s*(.+)$", oh, re.M) or [None, "null"])[1].strip()
            if not ov:
                ok("R2+", False, f"{o.name}: no readable verdict: header line (refused)")
                continue
            ok("R2+", ov == "go" or (ov == "fix-first" and oc not in ("", "null")),
               f"{o.name}: verdict {ov or '?'}" + (f", confirmed {oc}" if ov == "fix-first" else ""))
        if not before_run:
            bets = [json.loads(l) for l in (HERE / "bets.jsonl").read_text().splitlines() if l.strip()]
            b = next((x for x in bets if x["id"] == bet), None)
            rcm = (b or {}).get("result_commit")
            if rcm and rc:
                t_res = ctime(repo, rcm)
                ok("R3", t_res and t_rev < t_res, f"review {t_rev} before result {t_res}")
            else:
                warn("R3", "no result commit yet: the review must land before the first call")
    # H1: Sean's cockpit odds (rule 11, st-18). A line for this direction committed to ledger/human-odds.jsonl
    # before the pre-registration must be copied into the bet row; one that came later is never filled in.
    sys.path.insert(0, str(HERE))
    import human_odds_match as hom
    _bets = [json.loads(l) for l in (HERE / "bets.jsonl").read_text().splitlines() if l.strip()]
    _row = next((x for x in _bets if x["id"] == bet), None)
    if _row is None:
        prog = (re.match(r"^programs/([^/]+)/", path) or [None, ""])[1]
        warn("H1", "no bet row yet; before appending it run: python3 ledger/human_odds_match.py "
                   f"{prog or '<program>'} <direction>, and copy what it prints")
    else:
        if pc and not _row.get("prereg_commit"):
            _row = dict(_row, prereg_commit=pc)
        good, msg = hom.check_bet(_row)
        if good is None:
            warn("H1", msg)
        else:
            ok("H1", good, msg)
    for k, s, msg in res:
        print(f"{k} {s:4} {msg}")
    sys.exit(1 if any(s == "FAIL" for _, s, _ in res) else 0)


if __name__ == "__main__":
    main()

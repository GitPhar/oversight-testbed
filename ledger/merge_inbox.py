"""Fold the ledger inbox into the ledger files. No network, no keys.

    python3 ledger/merge_inbox.py                 # fold every committed inbox line, regenerate the tables
    python3 ledger/merge_inbox.py --dry-run       # say what would be folded, change nothing
    python3 ledger/merge_inbox.py --commit        # fold, then commit the ledger files and the emptied inbox files
    python3 ledger/merge_inbox.py add <file> '<row json>'               # append one "add" line to your inbox file
    python3 ledger/merge_inbox.py update <file> <id> '<fields json>'    # append one "update" line to your inbox file
    python3 ledger/merge_inbox.py check           # every inbox line parses and applies cleanly; exit 1 if not

<file> is one of bets, lessons, steers, plants (ledger/<file>.jsonl).

Why (ledger/inbox/README.md, CONTEXT.md section 2): several sessions share one checkout, and three times on
2026-11-04/05 a direct edit of a shared ledger file lost or swept another session's rows (lessons.jsonl was empty on
disk for a minute; rows lost twice; commits took other sessions' edits). From 2026-11-05 no session edits
ledger/bets.jsonl, lessons.jsonl, steers.jsonl or plants.jsonl directly. Each appends one line per change to its own
file, ledger/inbox/<branch-or-session>.jsonl, and commits that file. Only this script writes the four ledger files.

An inbox line:
    {"op": "add",    "file": "bets", "row": {...the full row...},       "by": "<session>", "at": "<time>"}
    {"op": "update", "file": "bets", "id": "ss-b2", "fields": {...},   "by": "<session>", "at": "<time>"}
An "add" to steers may give "id": null (or omit it); the fold gives it the next free st-NN and prints it.
An "update" replaces the named fields of the row with that id (a field set to null is set to null, not removed).

The fold, in order:
  1. Reads every ledger/inbox/*.jsonl and dates each line by the commit that added it (git blame). Lines not yet
     committed are left where they are and reported: a session commits its inbox file first.
  2. Applies the committed lines in commit order (then file name, then line), to an in-memory copy of each ledger file.
     An "add" whose id exists with the same content is a no-op (a line folded twice); with different content it stops.
     An "update" of an id that does not exist stops. Nothing is written if anything stops.
  3. Re-reads each ledger file and checks it has not changed since step 2 read it, then writes it through a temporary
     file and an atomic rename (a reader never sees a half-written or empty file), re-reads it, and checks the line
     count is the old count plus the adds, that every line parses and that ids are unique.
  4. Removes the folded lines from their inbox files (an emptied inbox file is deleted).
  5. Runs ledger/brier.py, ledger/scores.py and ledger/prior.py, then site/numbers.py (the front-page documents' ledger
     numbers); a document is committed only if its only uncommitted change is those numbers.
The morning operator and every main-checkout session run it first, before any other ledger step.
"""
import argparse
import hashlib
import json
import os
import re
import secrets
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
INBOX = HERE / "inbox"
FILES = ("bets", "lessons", "steers", "plants")
FOLDED = INBOX / "folded.txt"   # uid of every line already folded, one per line; written only by the fold


def uid_of(it):
    return it["op"].get("uid") or hashlib.sha256(it["raw"].encode()).hexdigest()[:16]


def folded_uids():
    return set(FOLDED.read_text().split()) if FOLDED.exists() else set()


def _now():
    try:
        from zoneinfo import ZoneInfo
        return datetime.now(ZoneInfo("America/Denver")).strftime("%Y-%m-%d %H:%M America/Denver")
    except Exception:
        return datetime.now().strftime("%Y-%m-%d %H:%M")


def _git(*a, cwd=ROOT):
    r = subprocess.run(["git", "-C", str(cwd), *a], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else ""


def read_rows(path):
    p = Path(path)
    if not p.exists():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def inbox_files(inbox=INBOX):
    return sorted(p for p in Path(inbox).glob("*.jsonl")) if Path(inbox).exists() else []


def _blame(path):
    """line number (1-based) -> (commit time, commit sha) for committed lines; uncommitted lines are absent."""
    out = _git("blame", "--line-porcelain", "--", str(Path(path).relative_to(ROOT)))
    res, cur, sha, t = {}, None, None, None
    for line in out.splitlines():
        m = re.match(r"^([0-9a-f]{40}) \d+ (\d+)", line)
        if m:
            sha, cur = m.group(1), int(m.group(2))
            continue
        if line.startswith("committer-time "):
            t = int(line.split()[1])
        elif line.startswith("\t") and cur is not None:
            if not sha.startswith("0000000"):
                res[cur] = (t, sha)
            cur = None
    return res


def inbox_lines(inbox=INBOX, committed_only=False):
    """Every inbox line as dict(path, lineno, op, time, sha), sorted in commit order (uncommitted last)."""
    items = []
    for p in inbox_files(inbox):
        blame = _blame(p)
        for i, raw in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if not raw.strip():
                continue
            op = json.loads(raw)
            t, sha = blame.get(i, (None, None))
            if committed_only and sha is None:
                continue
            items.append(dict(path=p, lineno=i, raw=raw, op=op, time=t, sha=sha))
    items.sort(key=lambda x: (x["time"] is None, x["time"] or 0, x["path"].name, x["lineno"]))
    return items


def _next_steer_id(rows):
    n = max([int(m.group(1)) for r in rows for m in [re.match(r"^st-(\d+)$", str(r.get("id") or ""))] if m] + [0])
    return f"st-{n + 1:02d}"


def apply(ledger, items):
    """Apply inbox items to {file: rows} in order. Returns (ledger, adds per file, assigned ids, problems)."""
    adds = {f: 0 for f in FILES}
    assigned, problems = [], []
    for it in items:
        op = it["op"]
        f = op.get("file")
        where = f"{it['path'].name}:{it['lineno']}"
        if f not in FILES or op.get("op") not in ("add", "update"):
            problems.append(f"{where}: needs op add|update and file one of {', '.join(FILES)}")
            continue
        rows = ledger[f]
        if op["op"] == "add":
            row = dict(op.get("row") or {})
            if not row:
                problems.append(f"{where}: add with no row")
                continue
            if f == "steers" and not row.get("id"):
                row["id"] = _next_steer_id(rows)
                assigned.append((where, row["id"]))
            if not row.get("id"):
                problems.append(f"{where}: add to {f} with no id")
                continue
            old = next((r for r in rows if r.get("id") == row["id"]), None)
            if old is not None:
                if old != row:
                    problems.append(f"{where}: add {row['id']} to {f}, but a different row with that id is already there")
                continue   # the same row folded before: no-op
            rows.append(row)
            adds[f] += 1
        else:
            rid, fields = op.get("id"), op.get("fields") or {}
            old = next((r for r in rows if r.get("id") == rid), None)
            if old is None:
                problems.append(f"{where}: update {rid} in {f}, which has no row with that id")
                continue
            if "id" in fields and fields["id"] != rid:
                problems.append(f"{where}: an update may not change a row's id")
                continue
            old.update(fields)
    return ledger, adds, assigned, problems


def effective(name, ledger_dir=HERE, inbox=None):
    """ledger/<name>.jsonl with every inbox line applied, committed or not (what check_prereg.py and reproduce.py
    read, so a row still waiting in an inbox counts). Problems are ignored here; `check` reports them."""
    ledger_dir = Path(ledger_dir)
    inbox = Path(inbox) if inbox else ledger_dir / "inbox"
    base = {f: read_rows(ledger_dir / f"{f}.jsonl") for f in FILES}
    if name not in FILES:
        return read_rows(ledger_dir / f"{name}.jsonl")
    try:
        items = []
        for p in inbox_files(inbox):
            for i, raw in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
                if raw.strip():
                    items.append(dict(path=p, lineno=i, raw=raw, op=json.loads(raw), time=None, sha=None))
        apply(base, items)
    except Exception:
        pass
    return base[name]


def pending_ids(name, ledger_dir=HERE):
    """ids that an inbox adds to ledger/<name>.jsonl and that the file itself does not hold yet."""
    have = {r.get("id") for r in read_rows(Path(ledger_dir) / f"{name}.jsonl")}
    return {r.get("id") for r in effective(name, ledger_dir)} - have


def inbox_name():
    """The caller's own inbox file: $LEDGER_INBOX, else the git branch, else main-<time>-<random> in the main checkout."""
    env = os.environ.get("LEDGER_INBOX")
    if env:
        return re.sub(r"[^A-Za-z0-9._-]+", "-", env)
    br = _git("rev-parse", "--abbrev-ref", "HEAD", cwd=Path.cwd()).strip() or _git("rev-parse", "--abbrev-ref", "HEAD").strip()
    if br and br not in ("main", "HEAD"):
        return re.sub(r"[^A-Za-z0-9._-]+", "-", br)
    return f"main-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{secrets.token_hex(2)}"


def append(op, name=None, inbox=INBOX):
    """Append one op line to ledger/inbox/<name>.jsonl (the caller's own file, so no other session writes it)."""
    Path(inbox).mkdir(parents=True, exist_ok=True)
    op = dict(op)
    op.setdefault("by", os.environ.get("LEDGER_INBOX") or name or "")
    op.setdefault("at", _now())
    op.setdefault("uid", secrets.token_hex(8))   # the fold skips a uid it has folded before (a line merged back in)
    p = Path(inbox) / f"{name or inbox_name()}.jsonl"
    with open(p, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(op, ensure_ascii=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())
    return p


def _write_atomic(path, rows):
    text = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows)
    fd, tmp = tempfile.mkstemp(dir=str(Path(path).parent), prefix=f".{Path(path).name}.", suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        fh.write(text)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def fold(dry_run=False, commit=False):
    items = inbox_lines(committed_only=False)
    done = folded_uids()
    waiting = [it for it in items if it["sha"] is None]
    again = [it for it in items if it["sha"] is not None and uid_of(it) in done]
    todo = [it for it in items if it["sha"] is not None and uid_of(it) not in done]
    for it in again:
        print(f"  already folded (uid {uid_of(it)}), removed without re-applying: {it['path'].name}:{it['lineno']}")
    for it in waiting:
        print(f"  waiting (not committed yet, left in place): {it['path'].name}:{it['lineno']}")
    if not todo and not again:
        print("Inbox: nothing committed to fold." + (f" {len(waiting)} line(s) wait for their session's commit." if waiting else ""))
        return 0
    before_text = {f: (HERE / f"{f}.jsonl").read_text(encoding="utf-8") if (HERE / f"{f}.jsonl").exists() else "" for f in FILES}
    ledger = {f: [json.loads(l) for l in before_text[f].splitlines() if l.strip()] for f in FILES}
    before_n = {f: len(ledger[f]) for f in FILES}
    ledger, adds, assigned, problems = apply(ledger, todo)
    for where, sid in assigned:
        print(f"  {where}: steer given id {sid}")
    if problems:
        for p in problems:
            print(f"  STOP  {p}")
        print("Nothing written. Fix the inbox line (its session appends a corrected line and the bad one is removed by hand).")
        return 1
    summary = ", ".join(f"{f} +{adds[f]}" for f in FILES if adds[f]) or "updates only"
    print(f"Folding {len(todo)} committed inbox line(s) from {len({it['path'] for it in todo})} file(s): {summary}.")
    if dry_run:
        return 0
    changed = [f for f in FILES if ledger[f] != [json.loads(l) for l in before_text[f].splitlines() if l.strip()]]
    for f in changed:
        p = HERE / f"{f}.jsonl"
        now_text = p.read_text(encoding="utf-8") if p.exists() else ""
        if now_text != before_text[f]:
            print(f"  STOP  ledger/{f}.jsonl changed on disk while folding (another session edited it directly). Nothing written for it; rerun.")
            return 1
    for f in changed:
        _write_atomic(HERE / f"{f}.jsonl", ledger[f])
        back = read_rows(HERE / f"{f}.jsonl")
        ids = [r.get("id") for r in back]
        if len(back) != before_n[f] + adds[f] or len(set(ids)) != len(ids):
            print(f"  STOP  ledger/{f}.jsonl: {len(back)} line(s) after the fold, expected {before_n[f] + adds[f]}, "
                  f"or repeated ids. Restoring the old file.")
            (HERE / f"{f}.jsonl").write_text(before_text[f], encoding="utf-8")
            return 1
        print(f"  ok    ledger/{f}.jsonl: {before_n[f]} -> {len(back)} line(s), ids unique")
    with open(FOLDED, "a", encoding="utf-8") as fh:
        for it in todo:
            fh.write(uid_of(it) + "\n")
    by_file = {}
    for it in todo + again:
        by_file.setdefault(it["path"], set()).add(it["lineno"])
    has_waiting = {it["path"] for it in waiting}
    touched = []
    for p, nums in by_file.items():
        if p in has_waiting or _git("status", "--porcelain", "--", str(p.relative_to(ROOT))).strip():
            # Its session has lines it has not committed: leave the file alone, so no commit of ours sweeps them.
            # The folded lines stay until a later fold; their uids are in folded.txt, so they are never applied twice.
            print(f"  kept  {p.relative_to(ROOT)}: it holds uncommitted lines; its {len(nums)} folded line(s) are skipped by uid and removed at a later fold")
            continue
        keep = [l for i, l in enumerate(p.read_text(encoding="utf-8").splitlines(), 1) if i not in nums and l.strip()]
        if keep:
            p.write_text("\n".join(keep) + "\n", encoding="utf-8")
        else:
            p.unlink()
        touched.append(p)
        print(f"  ok    {p.relative_to(ROOT)}: {len(nums)} folded line(s) removed" + ("" if keep else "; file deleted"))
    for script in ("brier.py", "scores.py", "prior.py"):
        r = subprocess.run([sys.executable, str(HERE / script)], cwd=ROOT, capture_output=True, text=True)
        print(f"  {'ok  ' if r.returncode == 0 else 'FAIL'}  ledger/{script}: {(r.stdout or r.stderr).strip().splitlines()[-1] if (r.stdout or r.stderr).strip() else ''}")
        if r.returncode:
            return 1
    # The front-page documents take their ledger numbers from the tables just regenerated (site/numbers.py).
    import importlib.util
    spec = importlib.util.spec_from_file_location("site_numbers", ROOT / "site" / "numbers.py")
    nm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(nm)
    _, docs = nm.run(check=False, root=ROOT, quiet=True)
    safe_docs = [d for d in docs if nm.only_numbers_changed(d, ROOT)]
    for d in docs:
        print(f"  ok    {d}: ledger numbers brought current" + ("" if d in safe_docs else
              " (it also holds someone else's uncommitted edits, so it is not committed here; its owner commits it)"))
    if commit:
        paths = [f"ledger/{f}.jsonl" for f in changed] + ["ledger/brier.md", "ledger/scores.md", "ledger/prior.md"] + safe_docs + \
                [str(p.relative_to(ROOT)) for p in touched] + [str(FOLDED.relative_to(ROOT))]
        msg = (f"Fold ledger inbox: {len(todo)} line(s) from {', '.join(sorted(p.name for p in touched))} ({summary}); "
               "brier.md, scores.md, prior.md regenerated (ledger/merge_inbox.py). No deviation row.")
        subprocess.run(["git", "-C", str(ROOT), "add", "--", str(FOLDED.relative_to(ROOT))], capture_output=True, text=True)
        r = subprocess.run(["git", "-C", str(ROOT), "commit", "-q", "-m", msg, "--", *paths], capture_output=True, text=True)
        print(("  ok    committed " + _git("rev-parse", "--short", "HEAD").strip()) if r.returncode == 0 else f"  FAIL  commit: {r.stderr.strip()}")
        return r.returncode
    print("Now commit the ledger files and the inbox files together: git commit -m \"Fold ledger inbox …\" -- "
          + " ".join([f"ledger/{f}.jsonl" for f in changed] + ["ledger/brier.md", "ledger/scores.md", "ledger/prior.md"] + safe_docs
                     + [str(p.relative_to(ROOT)) for p in touched] + [str(FOLDED.relative_to(ROOT))]))
    return 0


def check():
    items = inbox_lines()
    ledger = {f: read_rows(HERE / f"{f}.jsonl") for f in FILES}
    _, adds, _, problems = apply(ledger, items)
    for p in problems:
        print(f"  FAIL  {p}")
    print(f"Inbox: {len(items)} line(s) in {len(inbox_files())} file(s), {sum(1 for i in items if i['sha'] is None)} not committed; "
          + ("every line applies cleanly." if not problems else f"{len(problems)} problem(s)."))
    return 1 if problems else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd")
    a1 = sub.add_parser("add"); a1.add_argument("file", choices=FILES); a1.add_argument("row")
    a2 = sub.add_parser("update"); a2.add_argument("file", choices=FILES); a2.add_argument("id"); a2.add_argument("fields")
    sub.add_parser("check")
    for s in (a1, a2):
        s.add_argument("--inbox", help="inbox file name (default: $LEDGER_INBOX, else the branch)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--commit", action="store_true", help="commit the folded ledger files and inbox files (path-only)")
    a = ap.parse_args()
    if a.cmd == "add":
        p = append({"op": "add", "file": a.file, "row": json.loads(a.row)}, a.inbox)
        print(f"appended to {p.relative_to(ROOT)}; commit it: git commit -m \"…\" -- {p.relative_to(ROOT)}")
        return 0
    if a.cmd == "update":
        p = append({"op": "update", "file": a.file, "id": a.id, "fields": json.loads(a.fields)}, a.inbox)
        print(f"appended to {p.relative_to(ROOT)}; commit it: git commit -m \"…\" -- {p.relative_to(ROOT)}")
        return 0
    if a.cmd == "check":
        return check()
    return fold(dry_run=a.dry_run, commit=a.commit)


if __name__ == "__main__":
    sys.exit(main())

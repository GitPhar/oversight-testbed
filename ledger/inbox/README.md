# The ledger inbox

**From 2026-11-05, no session edits `ledger/bets.jsonl`, `ledger/lessons.jsonl`, `ledger/steers.jsonl` or `ledger/plants.jsonl` directly.** A session appends one line per change to its own file in this folder, `ledger/inbox/<branch-or-session>.jsonl`, and commits that file. `python3 ledger/merge_inbox.py` is the only thing that writes the four ledger files.

## In plain English

Several sessions work in one checkout at once, and the four ledger files are shared. When two sessions edit the same file at the same moment, one of them loses. On 2026-11-04 and 2026-11-05 that happened four ways: `lessons.jsonl` sat empty on disk for a minute while a session rewrote it; rows were lost twice; and commits swept up other sessions' half-finished edits. So each session now writes only to a file nobody else writes to. A single tool folds all of those files into the ledger, in the order they were committed, checks that no line went missing, regenerates the tables and clears what it folded.

## What a session does

1. **Name your file.** In a worktree, the branch name is used (`ledger/inbox/<branch>.jsonl`). In the main checkout, set a name for your tab first, `export LEDGER_INBOX=<tab-name>` (for example `tab-a-housekeeping`); without one the tool makes up `main-<time>-<random>.jsonl`, which works but is harder to read.
2. **Append, one line per change**, with the tool (it adds `by`, `at` and a `uid`):
   ```
   python3 ledger/merge_inbox.py add bets '<the full bet row as JSON>'
   python3 ledger/merge_inbox.py update bets <bet-id> '{"verdict": "fail", "outcome": 0, "scored": true}'
   python3 ledger/merge_inbox.py add lessons '<the ls-<bet-id> row>'
   python3 ledger/merge_inbox.py add steers '{"id": null, ...}'      # null id: the fold gives the next free st-NN
   ```
   `ledger/plants.py seal` and `reveal`, and `ledger/pickup_human_odds.py` (its veto steers), write to your inbox file themselves.
3. **Commit your inbox file, and only it**: `git commit -m "…" -- ledger/inbox/<name>.jsonl`. A line that is not committed is never folded.
4. **In the main checkout, fold**: `python3 ledger/merge_inbox.py --commit`. In a worktree, do not fold; the main-checkout session folds after it merges your branch.

**The morning operator and every main-checkout session run `python3 ledger/merge_inbox.py --commit` first**, before any other ledger step (after `python3 ledger/pickup_human_odds.py`, which may add veto lines).

## The line

```json
{"op": "add",    "file": "bets",  "row": {"id": "ss-b13", "...": "..."}, "by": "<session>", "at": "<time>", "uid": "<16 hex>"}
{"op": "update", "file": "bets",  "id": "ss-b13", "fields": {"verdict": "fail"}, "by": "<session>", "at": "<time>", "uid": "<16 hex>"}
```

- `file` is `bets`, `lessons`, `steers` or `plants`.
- `add` carries the whole row. If a row with that id is already in the ledger and is identical, the line is a no-op; if it differs, the fold stops and writes nothing.
- `update` replaces the named fields of the row with that id. It cannot change the id. An update to an id that is in no ledger file and no earlier inbox line stops the fold.
- `uid` makes a line foldable once only: `ledger/inbox/folded.txt` lists every uid already folded, so a line that comes back in a merge is removed, never applied twice.

## What the fold does (`ledger/merge_inbox.py`)

1. Dates every inbox line by the commit that added it (`git blame`). Uncommitted lines stay where they are.
2. Applies the committed lines in commit order to a copy of each ledger file; stops on any problem, writing nothing.
3. Checks each ledger file has not changed on disk since it read it, writes it through a temporary file and an atomic rename (no reader sees an empty or half-written file), re-reads it, and checks the line count is the old count plus the adds, every line parses, and ids are unique.
4. Removes the folded lines from their inbox files and deletes an emptied file. A file that still holds uncommitted lines is left untouched (its folded lines are skipped by uid next time), so the fold's commit never sweeps another session's work.
5. Runs `ledger/brier.py`, `ledger/scores.py` and `ledger/prior.py`; with `--commit`, commits the ledger files, the tables, the inbox files and `folded.txt` by path.

`python3 ledger/merge_inbox.py check` says whether every inbox line applies cleanly; `--dry-run` says what a fold would do.

## Who reads the inbox

Rows still waiting here count as in the ledger for `ledger/check_prereg.py`, `ledger/check_remap.py`, `ledger/plants.py` and the cross-reference checks of `python3 reproduce.py` (which also fails on an inbox line that does not apply, and names what is waiting). `brier.md`, `scores.md`, `prior.md` and the site count a row only once it is folded.

## Merging a branch

Every branch writes its own file, so the four ledger files no longer conflict in a merge. If the fold deleted an inbox file on main that the branch later appended to, git reports a modify/delete conflict: keep the branch's file (`git checkout --theirs ledger/inbox/<branch>.jsonl && git add ledger/inbox/<branch>.jsonl`); the lines already folded are skipped by uid.

Other ledger files (`human-odds.jsonl`, `shadows.jsonl`, `spend.jsonl`) are unchanged by this rule for now.

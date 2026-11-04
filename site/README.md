# site/

The public site, served by GitHub Pages. Plain HTML, CSS and JavaScript modules, with no build step and no framework. The only third-party code is `vendor/marked.min.js` (marked 12.0.2, MIT), which renders the papers. The font is Atkinson Hyperlegible, from Google Fonts. Its slashed zero is swapped for plain system digits.

Every number on every page is read from the repositories' own files when the page loads. Nothing is typed into the HTML. When the ledger, the map or a paper changes and the site redeploys, the pages change with it.

## Pages

| page | what it shows | read from |
|---|---|---|
| `index.html` | the one-sentence description; three plain-English panels for a stranger (what this is, what the human does, what the quantum chip is for and not for); the page tiles; the five commitments | `proposal.md` (## One sentence), `README.md` (## The five commitments), the chip-time line from `map/nature-graded.json` (`qpu`) |
| `map.html` | each program as paths fanning out from its seed question: open paths faint and dotted, landed bets bright, kills marked with a cross and their diagnosis on hover. The drawing opens fitted to the window, with the replay bar in the same frame, so the replay can be watched without scrolling; scroll or pinch zooms, drag pans, Fit goes back. A list view sits below (open by default on phones). An open path's engine odds are hidden until the human's are recorded | `map/<program>.json` joined with `ledger/bets.jsonl` and `ledger/human-odds.jsonl` |
| `cockpit.html` | where the human steers: one card per open or running question in every program, with the question in one sentence, what we already know, the cheapest test and its cost; an odds box (0–100); a reveal button for the engine's odds that stays disabled until the human's number is recorded; a veto with a required reason; an add-a-question box. Cards are in a fixed shuffled order within each program so the engine's ranking does not nudge the human. No backend: entries stay in the browser until downloaded as JSON lines and appended to `ledger/human-odds.jsonl` and `ledger/steers.jsonl` | `map/<program>.json` (open nodes and their cockpit fields), `ledger/bets.jsonl` (running bets), `ledger/human-odds.jsonl` and `ledger/steers.jsonl` (what is already committed) |
| `calibration.html` | stated odds against outcomes: one dot per scored bet, buckets with 95% intervals, the Brier tiles, then `brier.md` itself | `ledger/brier.md` (its "Scores", "Calibration table" and "Every scored bet" tables); falls back to the scored rows of `bets.jsonl` |
| `kills.html` | every closed direction, newest first, with its diagnosis and evidence | killed map nodes, `null` bets, and `ledger/kills.jsonl` if it exists, merged |
| `record.html` | program 1's record as a timeline by day | entangled-mind `paper/record.md` (dated paragraphs and table rows become cards) |
| `papers.html`, `paper.html?p=<name>` | the papers as readable pages, with contents, figures and commit links | entangled-mind `paper/*.md`, and the engine's `proposal.md` |

## The data contract

`site/assemble.sh` copies the data next to the pages under `data/`. Pages cannot list folders, so it also writes `data/manifest.json` with the file names.

**`map/<program>.json`**: one file per program.
```
{ program, title, seed_question, seed_date,
  directions: [ { id, parent (id or null for the seed), title, short (label on the drawing),
                  status: hit|killed|mixed|running|open,   # used only when the node has no bet
                  opened, resolved,                        # "YYYY-MM-DDTHH:MM", America/Denver
                  engine_odds, human_odds, cost, result, diagnosis,
                  bets: ["<bet id>", ...] } ] }            # the first bet's verdict, odds and dates win
```
Open nodes also carry the cockpit's fields: `question` (one plain sentence), `known` (two short lines), `cheapest_test`, `cost`, and `odds_event` (the exact event the odds are for). `moved_to` marks a direction carried into another program's map; the cockpit shows it there instead.

Programs 2 and 3 have no remote yet, so their maps are converted into this repository: `map/other-minds.json` from other-minds `map/program-2-map.md` (a20824d), and `map/nature-graded.json` from nature-graded `map/program-3-map.md` and `.json` (cb82b10). Re-convert when those maps change.

A node that lists `bets` takes its verdict, odds, result, diagnosis and dates from `ledger/bets.jsonl`, so a verdict lives in one place only. A node without bets is either an open path or a phase-A result from before the ledger began. Those carry their own `status`, `result` or `diagnosis`, with a `source` pointing at the record.

**`ledger/bets.jsonl`**: the ledger session's schema. The site uses `id`, `program`, `direction`, `title`, `engine_odds`, `engine_odds_first`, `human_odds`, `odds_event`, `verdict` (pass→hit, null→killed, mixed), `outcome`, `scored`, `prereg_commit`, `prereg_time`, `result_time`, `result`, `result_file`, `diagnosis`, `verdict_prereg`, `cost_usd`, `audit_path`. A bet with `scored: false` never appears on the calibration chart.

**`ledger/human-odds.jsonl`**: written by the cockpit, one line per entry: `id`, `program`, `direction`, `bet`, `question`, `event`, `human_odds` (0–1), `odds_pct`, `because`, `saw_engine_odds`, `saw_engine_odds_note`, `human`, `recorded` (ISO time with the America/Denver offset). The first entry for a direction is the one the map shows. Cockpit steers go into `ledger/steers.jsonl` with `action` `veto` or `add_question`, the `direction` they concern (or `null` for a new question), and the human's words in `reason`.

**`ledger/brier.md`**: generated by `ledger/brier.py`. The chart reads the tables by their column names, so a reordered column still works. A renamed column needs a change in `assets/calibration.js`.

**`ledger/audits/<bet-id>.md`**: when a bet's `audit_path` is set, the kill log links to it. Until then, each card says "not yet audited".

## Preview

```
site/assemble.sh /tmp/site ../entangled-mind && python3 -m http.server -d /tmp/site 8000
```
Then open http://localhost:8000. `LEDGER_DIR=…` and `MAP_DIR=…` read the data from another worktree.

## Deploy

`.github/workflows/pages.yml` runs `assemble.sh` against a fresh checkout of `GitPhar/entangled-mind` and publishes the result. It runs on every push to `main` that touches the site, the ledger, the map, the README or the proposal. It also runs nightly at 23:50 America/Denver, on demand, and on a `program-updated` repository dispatch. In the repository's settings, Pages must be set to **Source: GitHub Actions** once.

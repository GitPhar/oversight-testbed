# (working title — see CONTEXT.md §0)

[![Reproduce](https://github.com/GitPhar/oversight-testbed/actions/workflows/reproduce.yml/badge.svg?branch=main)](https://github.com/GitPhar/oversight-testbed/actions/workflows/reproduce.yml)

A testbed for AI-driven research in which the judgment, not just the output, is scored. An AI (Claude) maps the research paths it could take and writes down its odds on each before any data. A person steers. A separate AI session that has not seen the work tries to break every result. The AI's odds and the person's are then scored against what happened. Built for trust, not volume.

**New here? Start with [the project in plain words](paper/plain-words.md)** (under 1,500 words, no jargon) or [the same on one page](application/one-page-plain.md). The panel-style review of the whole submission is [paper/review-anthropic.md](paper/review-anthropic.md).

For the working files, read in this order: `CONTEXT.md` (the rules and the current state), `TASKS.md` (open items), `ARCHITECTURE.md` (the loop, step by step), `proposal.md` (the research proposal for the engine itself).

**Reproduce everything with one command:** `python3 reproduce.py` (Python 3 and numpy, `pip install -r requirements-reproduce.txt`; no keys, no network). It rebuilds every ledger table, the site data and every program's results tables from the archived files and checks them against what is committed; each program also has its own `programs/<name>/reproduce.py`. The badge above is that command's state on `main`, run on every push and daily (`.github/workflows/reproduce.yml`).

## The five commitments

1. **Odds before data.** Every bet carries the AI's odds and the person's odds, recorded separately, before any data are seen. (As of 5 November 2026 no scored bet yet carries the person's odds; `ledger/brier.md` shows the empty column.)
2. **Cheapest test first.** Archived data before new API calls, API calls before hardware; budgets enforced in code; stop rules; a run stops at its first refusal.
3. **No result without a check.** An independent session that has not seen the work tries to break every result, and its report is published whether or not the result stands.
4. **Nothing disappears.** Every dead direction stays on the map with the reason it died.
5. **Full reads first, all fields.** Every program starts from adjacent research read in full, its "what to do next" extracted and filtered by cost and whether it can fail.

## Where it stands (5 November 2026)

- 53 bets in the ledger, 21 scored, 43 audited, 4 verdicts reversed by audit.
- The AI's odds score 0.220 on the 21 scored bets, where always saying 50% scores 0.250: no better than a coin so far (`ledger/brier.md`).
- Three kinds of referee decide bets: another Claude model's behaviour (programs 1, 2, 5, 6, 7), an IBM quantum chip used only as a judge whose outcomes a model cannot argue with (program 3; 69 of 420 chip seconds used), and the published scientific record (program 4).
- 6 planted faults, 6 caught by the auditor (too few to be a rate). Every auditor, reviewer and bettor so far is a Claude model (Opus 5.5, with a third audit round by Fable 5.1 on 5 November); a check by a non-Claude model has not yet been run.

## Programs

Every program lives in this repository under `programs/`, with its git history imported. There are no separate program repositories.

- Program 1, [The Entangled Mind](programs/entangled-mind/): can a quantum-style encoding of a model's competing beliefs flag its wrong answers? Closed, negative, with a diagnosis. It left a live question: does a model's stated confidence report a fixed belief? (On Haiku, mostly not; on Opus, partly yes.) Its original repository, [GitPhar/entangled-mind](https://github.com/GitPhar/entangled-mind), is kept untouched as the historical record.
- Program 2, [Other Minds](programs/other-minds/): does a model reason about another mind the way it reasons about its own? Six tests on Haiku, none passed.
- Program 3, [Nature-Graded](programs/nature-graded/): the same AI's odds, graded by a real quantum chip instead of by a language model. The chip is a referee, never a computing resource (`operators/hardware.md`).
- Program 4, [Settled Science](programs/settled-science/): can the AI tell which way published findings came out? Five scored passes, none yet repeated; a sixth was reversed to undetermined by audit.
- Program 5, [Self-Grading](programs/self-grading/): does a model grade its own work more kindly than someone else's? Opened 5 November.
- Program 6, [Test Awareness](programs/test-awareness/): does a model behave differently when it thinks it is being tested? Opened 5 November.
- Program 7, [Said vs Did](programs/said-vs-did/): does the confidence a model states predict what it then does? Opened 5 November.

## Ledger, audits, map, site

`ledger/bets.jsonl` (every bet, its odds and its outcome), `ledger/steers.jsonl` (every human decision), `ledger/audits/` (every independent check), `map/` (every path considered), `site/` (the public pages at https://gitphar.github.io/oversight-testbed/). The operators that populate them are described in `CONTEXT.md` §7.

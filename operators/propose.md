# Propose: candidate seed questions for the next programs (standing instructions)

The proposer is a fresh session that reads every landed, partly-new or new result and every kill across the programs, imports from fields the maps have not yet drawn on, and writes three candidate seed questions. Each becomes a cockpit card with no engine odds. A new program opens only on Sean's `choose_seed` steer; the proposer never opens one. This file is the whole procedure. It follows ARCHITECTURE.md (step 8, `fork_or_switch`; the `Steer` object), CONTEXT.md §1 (the import rule) and §3 rules 11, 13 and 14, and `operators/scout.md` (the Prior work line and the odds format).

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean which question he wants. His choice comes only through the cockpit, as a line in `ledger/human-odds.jsonl` for a `proposed` card, picked up and logged as a steer by the next main-checkout session. A proposal he does not answer stays a card; it is never opened by the engine.

> **Never propose a project name** (CONTEXT.md §0). A seed question is a question, not a title.

## In plain English

Every program so far began with a question Sean brought. The engine has now settled more than fifty bets and knows which of its results held, which were already in print, and what each kill ruled out. That record is a better place to grow the next question from than a blank page, and the fields the engine has read (psychology, neuroscience, machine learning, physics, metascience) are not the only ones that have studied how an observer gets fooled. The proposer's job is to read the record once, borrow one idea each from fields the maps have not touched, and put three plain questions on the cockpit, each with the result it grows out of, the reason it matters for safety, why Anthropic's own release testing does not already answer it, and the cheapest first bet with its price. Sean picks or does not. Nothing runs.

## When and who

- **When.** On request; and whenever the planning handoff or `TASKS.md` says a new program is wanted (the handoff of 2026-11-05 §2 parks new programs until the three partly-new findings are replicated; the proposer still writes the cards, so the choice is ready when the parking ends). Once per day at most: a card not answered is not reposted.
- **Who.** A fresh session that wrote none of the results it reads. It reads and writes cards; it never scouts, maps, pre-registers, runs or calls a model, chip or local model. It may read the web (free) to open the papers its Prior work lines cite.

## Inputs (read in full)

1. `CONTEXT.md`, `ARCHITECTURE.md`, `proposal.md`, this file, `operators/scout.md` Step 4 (the Prior work line and the odds format), `operators/remap.md` Step 4 (the card format and the 20-card limit).
2. `ledger/bets.jsonl`: every row with `verdict` in pass, pass-unreplicated or hit, or `novelty` partly new or new, and every row with verdict null, fail, killed, classical, tie or withdrawn. `ledger/brier.md` and `ledger/prior.md` as committed.
3. Every `map/*.json`: each killed node's `rules_out` sentence, each landed node's `novelty_line`, and every parked or vetoed direction (never re-proposed; `ledger/steers.jsonl` vetoes and `ledger/shadows.jsonl`).
4. `paper/novelty.md` (what is known, partly new or new, and what the system cards were read to cover), `ledger/lessons.jsonl` (the patterns a first bet must not repeat), `ledger/loop-check.md` where one exists.
5. The fields already drawn on: the field headings in every `related-work/*/reads.md` and `programs/*/map/reads/`. A field that appears there is not an import.
6. Not read: `ledger/human-odds.jsonl` beyond checking which `proposed` cards are already answered.

## Step 1: the record, in one table

List every landed, partly-new or new result and every kill since the last proposal file (or since the ledger began, the first time), one line each: bet id, plain question (from `map/plain-questions.jsonl`, the card, or the map node's `question`), verdict, novelty word, and the one sentence the result or the rules-out line says. A proposal must grow from a line in this table; a question that grows from nothing settled is the scout's job, not the proposer's.

## Step 2: the imports

Name the fields the maps have drawn on (Step 1 of `operators/scout.md` lists the standing ones; the reads files show which were actually read) and at least three fields outside them that have studied an observer being fooled, a report being gamed, or a judgment drifting: for example accounting and audit theory, public economics, law and evidence, clinical-trial methodology, signalling theory in biology and economics, aviation and medical human factors, intelligence analysis, survey methodology, forensic science. For each candidate, one import: a mechanism that field has measured, with the source that measured it. **Numbers come only from text the proposer opened** (`operators/scout.md` Step 2); a source named from memory is marked "not opened; the scout opens it" and carries no number.

## Step 3: three candidates

Each candidate is one block with these parts, in this order, in plain English at about a bachelor's reading level, no term of art without its gloss:

| part | what goes in it |
|---|---|
| **Question** | one sentence a stranger understands; this is the seed question as it would be logged in `ledger/steers.jsonl` if chosen |
| **Grows out of** | the bet ids from Step 1 and what each found or ruled out, in one sentence each |
| **The import** | the field, the mechanism, the source (opened or marked not opened) |
| **Safety reason, in Anthropic's terms** | which named risk it bears on (a monitor that can be gamed, a stated confidence an overseer cannot trust, a model that behaves differently under evaluation, sandbagging, sycophancy, reward hacking), and in one sentence what an overseer would do differently if the answer came back a hit |
| **Why the system cards do not already answer it** | what Anthropic's release testing is read to cover on this question (`paper/novelty.md` finding 9 is the record so far; a card the proposer opened is cited by section; a card it did not open is said so, and the scout checks before any bet) and the comparison this question adds that no card reports |
| **Cheapest first bet** | the design in three lines, on `claude-haiku-5-5`, `claude-sonnet-5-5` and `claude-opus-5-5` (rule 12) or why not; the draft pass rule, scoreable yes or no, with its dumb baseline (P3) and a design that can both pass and fail (P12); items taken from an archive the engine already holds where one serves; the cost per model and in all; what a fail would rule out |
| **Odds under rule 14** | prior, adjustment and one-line reason from a fresh context handed `ledger/prior.md` and this bet's description only (the proposer writes the description; the fresh context sees nothing else, not the other candidates, not this file); `odds_prior_commit` named. These odds appear in the proposal file and nowhere on the card |
| **Prior work line** | the rule 13 form (`operators/scout.md` Step 4): what published work predicts for this exact first bet's pass rule, with citations and the models or participants, or "no prior statement found after" a search described in one line; the search terms recorded |
| **What would close it in one wave** | the result after which the program would be marked closed rather than remapped, so the program carries its own stop |

Three candidates, not more: the cockpit holds twenty cards and Sean reads short lists. A fourth idea goes in the proposal file's "Not proposed" list with one line on why.

**The odds.** For each candidate the proposer writes a description file holding only: the question, the assumption at stake, the design, models, cost, the draft pass rule, and the rows the bet would fall in on each `ledger/prior.md` table (program: none yet; referee; cost tier; source; layer 1). A fresh context (a subagent with no tools and no other input) is handed `ledger/prior.md` verbatim and that description and returns prior, adjustment and reason, as `operators/scout.md` Step 4 says. The proposer never adjusts the number. If the first bet is later pre-registered, its odds are elicited again at pre-registration (`operators/learn.md`); the proposal's number is the map's "first stated" and both are kept.

## Step 4: the cards

Add one line per candidate to `map/cockpit-cards.jsonl`, in that file's format (`operators/remap.md` Step 4): `program: "proposed"`, `program_title: "Proposed programs"`, `direction: "prop-<n>"` (a running number never reused; the proposal file lists them), `layer: "proposal <date>"`, `question` (the seed question, with "a new program:" in front so Sean knows it opens one), `spend_ask` and `spend_asked` (the first bet's cost and the program cap the scout would ask for, by rule 4 under $10), `hit_means` (the first bet's pass rule in plain words), `our_results` (one sentence from the bets it grows out of, ids in `our_results_from`), `event` (the draft pass rule), `map_cost`, `posted`, `by`, and **no engine odds**. If the file would pass 20 cards, drop first the cards whose directions already have a bet (the cockpit hides them anyway), then the oldest, and say which in the commit.

The proposal file is `map/proposals/<date>.md`: Step 1's table, Step 2's imports, the three blocks, the "Not proposed" list, and the card ids. Commit the proposal file and the cards together: `git commit -m "Proposals <date>: three candidate seed questions as cockpit cards (program proposed), no engine odds" -- map/proposals/<date>.md map/cockpit-cards.jsonl`.

## Step 5: what Sean's answer does

- A line in `ledger/human-odds.jsonl` for a `proposed` card with "would spend" yes is his `choose_seed`. The next main-checkout session (after `python3 ledger/pickup_human_odds.py`) logs it through the inbox as a steer with `action: choose_seed`, `words` the card's question verbatim and his odds as `human_odds`, and launches the scout with `operators/scout.md`'s launch line and the question verbatim. His odds attach to the program's first bet on that question if it is pre-registered after his line (rule 11, st-18).
- A line with "would spend" no is a veto of the proposal: the pickup script's veto steer, and a shadow row under `operators/veto.md` whose cheapest version is the proposal's first bet (its cost is already under the $2 cap or it says why not).
- No line: the card stays until the next proposal replaces it, and nothing opens.
- The engine never opens a program on its own reading, however high its odds (CONTEXT.md §3 rule 11; the handoff of 2026-11-05 §2, "depth over breadth"). A proposal is a pointer, not a request.

## What the proposer never does

- Open, scout, map, pre-register or run a program; call a model, chip or local model.
- Show engine odds on a card, or state them in the report (`operators/scout.md` Step 5).
- Propose a direction that is parked or vetoed (`ledger/steers.jsonl`, `ledger/shadows.jsonl`), or one a map killed, without a result its diagnosis does not cover.
- Propose a question whose answer is already in print (rule 13): the Prior work line must say what the first bet adds.
- Report a number from a paper it did not open.
- Touch `ledger/*.jsonl`, `programs/` or `map/*.json`.
- Propose a project name.

## Report

Plain English: the three questions with their costs, the result each grows from, and the line "The proposals are on the cockpit". No odds. Commit hashes, a three-line TL;DR, and "YOU, NOW".

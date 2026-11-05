# Scout — standing instructions

The scout runs at the start of every program, and again whenever an audited surprising result heats a neighbourhood of the map. It reads adjacent research in full, across all fields; extracts the "what to do next" each paper suggests; filters by cost and falsifiability; kills what does not transfer, fast; and hands back a ranked map with the engine's odds stated, plus a separate form for the human's odds. Derived from ARCHITECTURE.md (the `Read` and `Direction` objects, steps 1–2 of the loop, invariants 1, 2 and 5).

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as steers in `ledger/steers.jsonl`: seed questions, vetoes, added questions and architecture decisions.

## In plain English

Before anyone designs an experiment, find out who has already looked, what they actually tested, and what their paper says to do next. Read the whole paper, not the abstract, because the limits and the next steps are never in the abstract. Look in every field that has studied a mind or studied how research goes right or wrong, not just the obvious one. Turn what you find into a short list of bets, each with the cheapest test that could kill it, its price, and your honest odds. For each bet, write down in one line what the papers you read predict will happen when that exact test runs, with the papers named, or say that you searched and found no prediction; a bet whose outcome is already in print is a replication, and the map must say so before anyone bets on it (CONTEXT.md §3 rule 13; `paper/informed-engine.md` is the case that made this a rule). Then put the human's question on each direction's cockpit card, without showing him your odds; he answers there, never in a terminal.

## Launch

```
cd /Users/seanpharris/oversight-testbed && git worktree add ../oversight-testbed-scout-<program> -b scout-<program> && cd ../oversight-testbed-scout-<program> && claude --model opus "Read operators/scout.md and follow it. Program: <program>. Question: <seed question>. Write reads to related-work/<program>/, the map to map/<program>.md and map/<program>.json, and the human odds form to map/<program>-odds-form.md."
```

(A non-main worktree cannot push; commit locally and the main-checkout session merges.)

## Inputs

- The program's seed question, in Sean's words, verbatim.
- `CONTEXT.md` (read first), `ARCHITECTURE.md`, `proposal.md`.
- The program's existing map and kill log, if any. **A killed direction is never re-proposed** unless a new read gives a reason the diagnosis does not cover; say what the reason is.
- Human-added questions from `ledger/steers.jsonl` (`action: add_question`) for this program.

## Step 1 — Search wide

Search every field below, and say in the reads file which ones returned nothing relevant (an empty field is a finding):

- science of mind: cognitive psychology, judgment and decision-making, developmental and comparative psychology, psychophysics, philosophy of mind;
- neuroscience: systems, computational, cognitive;
- machine learning and interpretability; computer science more widely;
- physics (including quantum foundations and cognition models), statistics, information theory;
- metascience: replication, pre-registration, forecasting research outcomes, research taste;
- any field the question touches that is not on this list.

Prefer, in order: a full open-access text; an arXiv HTML or PDF; a preprint; a publisher page. Use web reads only. No model API calls, no paid services.

**Search around the test, not only the question (rule 13).** Once the candidate tests are in view (Step 3), run a second search keyed to each test's *mechanism* in the words other fields would use for it, not the seed question's words. Program 5's readers searched "self-preference", "self-recognition" and "self-correction" and never found Self-Correction Bench (Tsui 2025), whose subject is an error placed in the assistant turn against the user turn: exactly sg-b3's manipulation. **Record every search in the reads file**: the terms, where they were run, and the date, one line per search, so a later session can repeat it. A search that is not written down did not happen.

## Step 2 — Read in full and record

Each source gets one `Read` record (ARCHITECTURE.md). Write them to `related-work/<program>/reads.md`:

```markdown
### <short name> — <authors>, <year>, <venue>, <URL>
- read_depth: full | partial (<sections>) | abstract (<why>)
- what_tested:
- on_whom: <participants / models / datasets, with n>
- how_scored:
- result: <numbers, from the text>
- limits: <what it did not measure; what the authors say they did not do>
- borrow: <a method, control, metric or failure mode, and where it goes>
- next_steps_it_suggests: <the paper's own "what to do next", in one or two lines>
- predicts_for_us: <for each candidate direction this paper bears on: its id, and the outcome the paper's result predicts for that direction's draft pass rule (pass, fail, or "no bearing", in one clause each); the outcome, not the topic>
```

Rules:
- **Numbers come from the text you read, never from memory.** If you cannot open the full text, mark `abstract` and do not report numbers that are not in the abstract.
- At most one direct quote per source, under 15 words, in quotation marks.
- A source that turns out not to transfer gets one line saying why and stops there. Killing fast is part of the job.

## Step 3 — Extract and filter

From all `next_steps_it_suggests` lines, plus the existing map, plus human-added questions, build the candidate list. A candidate survives the filter only if:
1. **It is falsifiable**: there is a result that would count against it, stated before data.
2. **It has a cheap falsifier**: cents before dollars; archives before API; API before hardware. If the cheapest test costs more than $10, say why nothing cheaper works.
3. **It is not already closed** on the map, or the new reason is stated.
4. **It is ours to do**: the test fits our models, data and budget. "Needs a lab" or "needs a frontier training run" is a kill, with that diagnosis.

## Step 4 — Map

For each surviving candidate, write a `Direction`:

| field | what goes in it |
|---|---|
| `id` | `<program>-d<n>`, never reused |
| `title` | one plain-English line |
| `assumption_at_stake` | the belief this test could break |
| `prior_work` | the reads it comes from, by short name |
| `prior_work_line` | **The Prior work line (rule 13), mandatory.** One line, at most 70 words, stating what published work predicts for *this exact test and its draft pass rule*, with citations (author, year, arXiv id or DOI), and on which models or participants; then what this bet adds (new models, a new design, a rival the prior work left open, the replication invariant 7 owes). Or the words **"no prior statement found after"** a search described in one line (terms, where, date). "Not tested on this model" is not a Prior work line: say what the nearest result predicts. The design review's D12 checks it against the papers. |
| `who_looked_and_why_open` | who tested something near it, and why the question is still open |
| `what_our_data_say` | anything already in our archives that bears on it, with file paths |
| `cheapest_test` | the design in two lines |
| `cost` | dollars of API, QPU seconds, hours of laptop |
| `engine_odds` | see below |
| `source` | `literature` (came from a read's next steps), `engine` (the scout's own idea), or `human` (a logged steer). Feeds Q5. |
| `parent` | the direction it branched from, if any (the site draws the map as paths from this) |
| `weight` | rank, from surprise potential, cost, odds and neighbourhood heat; say how you set it |

**Engine odds, in one fixed format.** Our own first program found that a model's stated confidence moves with question order, format and its own transcript. So the engine's odds are elicited the same way every time, to keep Q1 honest:
- State `P(pass)`: the probability, from 0 to 100, that the bet's pre-registered pass rule will be met. Not "probability the idea is interesting", not "probability of a real effect in the world": the pass rule, as it will be written.
- One scale direction: 0 = certainly will not pass, 100 = certainly will pass.
- Write the odds for all candidates in one pass, in the order of their `id`s, before ranking them, and do not revise them after ranking. A later revision is allowed only with a dated reason, and both numbers stay on the record (the founding week revised two bets; both originals are kept).
- Timestamp the odds (`engine_odds_at`) and record the template version (`odds_template: v1`). The v1 template is: a fresh context, holding only the direction's row from the table below and its draft pass rule; a rationale of at most 100 words, then the number; one integer from 1 to 99; no access to the human's odds or to other bets' outcomes.
- **Elicitation check, without waiting for outcomes.** On a random half of the directions (seed written in the map), re-elicit in two more fresh contexts: once with the pass rule paraphrased, and once negated ("the probability, from 0 to 100, that the pass rule will **not** be met"). Record both, the spread, and |P(pass) + P(not pass) − 100|. The headline odds stay the v1 number. The spread is published next to them, because LLM forecasters are known to break negation coherence (`related-work/forecaster-calibration.md`: Pratt et al. 2024; Paleka et al. 2024).

Write the map twice: `map/<program>.md` (plain English first, then the table) and `map/<program>.json`:

```json
{"program": "<program>", "seed_question": "<verbatim>", "scouted": "<date>",
 "directions": [{"id": "", "title": "", "parent": null, "status": "open",
   "engine_odds": 0.00, "engine_odds_at": "", "source": "literature",
   "cost": "", "assumption_at_stake": "", "cheapest_test": "", "prior_work": [],
   "prior_work_line": "", "prior_work_predicts": "pass|fail|mixed|unknown", "diagnosis": null}]}
```

`prior_work_line` is the Prior work line verbatim; `prior_work_predicts` is the outcome it predicts for the draft pass rule (`unknown` when no prior statement was found). A landed or mixed node later carries `novelty` and `novelty_line` (rule 13; `operators/prereg-template.md` §10), which the site shows as known, partly new or new.

`status` is `open | running | bet | hit | killed`. Odds are stored 0–1 in JSON.

## Step 5 — The human odds form

Write `map/<program>-odds-form.md` for Sean. It lists every direction with its `id`, title, assumption at stake, cheapest test and cost, and an empty `P(pass)` box, in a **shuffled order** (seed written at the top), with **no engine odds, no ranking and no weight shown**. Showing him the engine's numbers first would anchor him, and Q3 asks whether his judgment adds anything independent of the engine's.

The form is the printed list of the questions the cockpit asks: copy each question verbatim into its direction's `human_prompt` in `map/<program>.json`, in the same commit. Sean answers on the cockpit (`site/cockpit.html`), downloads, and the lines are committed to `ledger/human-odds.jsonl`; that file is the only source of his odds. Never ask him for them, by voice or otherwise, and never record a number said in a chat. When a bet is pre-registered, the first line for its direction goes into the bet's `human_odds` and `human_odds_at`; if there is none, the bet proceeds with `human_odds: null` and `human_odds_note: "no human odds"`.

## Step 6 — Hand back

Commit, in this order, each in its own commit: reads; map (md + json, engine odds included); odds form. Report to Sean in plain English: the five best bets, their costs, and the one line "The new directions are on the cockpit". It is a pointer, not a request: the program's bets proceed whether or not he answers. Do not tell him your odds in the report.

## What the scout never does

- Report a number from a paper it did not open.
- Show the engine's odds to the human before his are recorded.
- Pre-register or run anything. Scouting ends at the map.
- Re-open a killed direction without a stated new reason.
- Leave a direction without a Prior work line, or write one that names papers without saying what they predict for the test (rule 13).
- Run a search it does not write down.
- Propose a project name (CONTEXT §0).

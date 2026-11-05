# The ledger

The ledger is the engine's scorecard. Before every test, the engine writes down how likely it thinks the test is to work. From program 2 on, Sean writes down his own number too. Then the test runs, and the ledger records what happened. Over time, that shows whose guesses were any good, and whether Sean's steering made things better or worse.

Nothing here is edited to look better later. A wrong guess stays wrong.

Everything in it was built on 2026-11-04 from the `entangled-mind` repository: `paper/gold-map.md`, `paper/biomimetic-map.md`, `DEVIATIONS.md`, `results/`, the git history of `main` (`0c64baa`) and of the `probes` branch (`8685008`), and section 8 of `CONTEXT.md`.

## The files

### `bets.jsonl`: every test, one per line

A **bet** is one pre-registered test. Each line says:
- what was tested, and which map direction it came from;
- **the engine's odds**: the probability it wrote down before data, and what exactly that probability was *for* (`odds_event`). If the odds were revised before the test, both numbers are kept (`engine_odds_first`, `engine_odds`), with the commits where each was written; from 2026-11-05 (CONTEXT.md §3 rule 14) the odds are written in three parts by a fresh context handed `prior.md`: `odds_prior` (the record's hit rate), `odds_adjustment` (signed) and `odds_reason` (one line), with `odds_prior_commit` and `odds_template: "v2"`, and `engine_odds` is prior + adjustment;
- **Sean's odds**: empty (`null`) for every founding-week bet, because they were not recorded. That is the honest entry, not a gap to fill in from memory;
- **the pre-registration commit**: where the pass rule was frozen, before any data. Every one was checked to be an ancestor of its result commit;
- **the result file** and its commit;
- **the verdict**: `pass` (the pre-registered effect, or the overturning direction, was found), `null` (it was not), `mixed` (the rule itself returned mixed or partial), plus the pre-registered reading word for word (`verdict_prereg`);
- **the outcome**: 1 if the event the odds were for happened, 0 if not. Only bets with stated odds and an outcome decided by the pre-registered rule are scored (`scored: true`); `scoring_note` says why any other bet is not;
- **the audit path**: empty for every bet so far, because no independent audit has been run yet;
- what it cost, and which earlier bet it replicates, if any.

There are 19 bets. Five are scored. Most of the rest are biomimetic tests (that map ranked ideas but gave no probabilities) or replications (no new probability was stated).

### `steers.jsonl`: every time Sean changed the course

A **steer** is a decision by the human: start a program, add a question, set a rule, veto something. The nine founding-week steers are reconstructed from `CONTEXT.md` section 8. Each line says what Sean said, what happened as a result (`outcome`, with commits as evidence), and a **value judgment**: `helped`, `hurt`, `mixed` or `pending`, with one or two sentences on why, and what would likely have happened otherwise.

These judgments are opinions written by the ledger session from the record. They are **not** measurements: there was no control run without the steer. Six are judged `helped` and three are `pending`; none `hurt`. Expect an auditor to push back on some of the six. A ledger where the human never hurts is a ledger to distrust.

### `human-odds.jsonl`: Sean's odds, from the cockpit

The site's cockpit page (`site/cockpit.html`) shows at most 12 cards, chosen by what the maps say is next to run (each program's open, un-bet directions in map rank order, programs taking turns). Each card asks one plain question: what we would test, *would you spend about $X on it?* (yes/no), *will it come back a hit?* (yes/no), and his odds if he wants to give them. The engine's odds are never shown there. One **Save my answers** button saves `human-odds.jsonl` to his Downloads folder: every line already committed here, plus the new ones. **The next local session picks it up** with `python3 ledger/pickup_human_odds.py`, which appends the new lines (by `id`) and commits them. The commit time is the proof the number came before data.

Fields of a line: `id` (`ho-<time>-<rand>`), `program`, `direction`, `bet` (null: the cockpit only asks about directions with no bet yet), `question` (the plain sentence shown), `event` (the direction's `odds_event`, for the record), `human_odds` (0–1, or null if he gave no number), `odds_pct`, `worth_spend` (true / false / null), `spend_asked` (the cost as the card put it, e.g. "about $0.24"), `expects_hit` (true / false / null), `hit_means`, `because`, `saw_engine_odds` (false: the cockpit never shows them), `saw_engine_odds_note`, `human`, `recorded` (ISO time with the America/Denver offset), `date`, `time`, `recorded_via`. A line with `worth_spend: false` is a **veto**: the pickup script appends a `veto` steer to `steers.jsonl` citing it (`from_human_odds`), which gets its shadow check under `operators/veto.md`.

Entries are never edited: a change of mind is a new line, and the first line for a direction is the independent one. When a direction is pre-registered as a bet, its first entry's `human_odds` is copied into that bet's `human_odds` in `bets.jsonl` (with `expects_hit` noted in `human_odds_note` when he gave a yes/no but no number), and `brier.py` is rerun, as in the form's instructions. Lines saved by the earlier cockpit (before 2026-11-05) have the same fields without `worth_spend`, `spend_asked`, `expects_hit` and `hit_means`.

### `brier.md`: how good were the guesses?

The **Brier score** is the standard score for probability guesses. For each bet, take (stated probability − outcome)², and average. 0 is perfect. Always saying 50% scores 0.25.

The founding week: the engine scored **0.256 on 5 bets**, about the same as a coin. Both hits were bets it had given 25%; the three misses were at 15%, 20% and 30%. On net the overnight literature reading made its odds slightly worse (0.221 on the first-stated odds). Five bets is far too few to say anything firm, and the file says so.

The **calibration table** groups bets by stated odds and compares the average stated probability with how often those bets actually came true. A well-calibrated guesser's 20% bets come true about 20% of the time. The human columns are empty for the founding week.

`brier.md` is generated: run `python3 ledger/brier.py` after any change to `bets.jsonl`. Do not edit it by hand.

`prior.md` is generated the same way: `python3 ledger/prior.py` counts the hit rate of every scored bet by program, referee, cost tier, source and layer depth (with Wilson intervals), and lists programs due a closing review (`operators/remap.md`). Every odds elicitation is handed this file. Do not edit it by hand.

### `audits/`: every audit, one file per bet

Each audit is `audits/<bet-id>.md`, written by a fresh session that has not seen the work and is told to break it. When an audit changes a verdict, the bet's outcome changes, the change is noted in its `scoring_note`, and `brier.md` is regenerated. Each audited bet carries `audit_path`, `audit_status` (round, commit, verdict, number of cuts, most serious hole), `verdict_stands` and `verdict_after_audit`.

- **Round 1, the founding week** (entangled-mind branch `audit`, `b009a15`, 2026-11-04 10:27): the files live in `programs/entangled-mind/audits/`. `audits/em-<bet>.md` are relative links to them, and `audits/SUMMARY-1.md` links to that round's summary. The site build copies the linked files (`cp -RL`). Round 1 also audited phase-A results that are not ledger bets (stage 1–2, experiments 3–5, the witness); those stay in the program folder only.
- **Round 2** (branch `audit2`, 14:32–16:40): `audits/SUMMARY-2.md`, the program 2 and 3 files, and the six re-audits of program 1 results (`multi-model-r2`, `calibration-under-format-r2`, `probe-dissociation-r2`, `probe-dissociation-dp2`, `mm-gm3b-opus-completion`, `exp5-verdict-reissue`), copied from that branch.

| bet | round-1 file | round-1 verdict | round 2 |
|---|---|---|---|
| em-gm9 | `gm9-nsit.md` | stands with caveats | — |
| em-gm3a | `gm3a-anchor-gap.md` | stands | — |
| em-gm1 | `gm1-self-knowledge.md` | stands with caveats | — |
| em-gm2 | `gm2-self-conditioning.md` | stands with caveats | — |
| em-gm3b | `gm3b-format-invariance.md` | stands | — |
| em-gm4 | `gm4-evidence-seeking.md` | stands | — |
| em-gm5 | `probe-dissociation.md` | stands with caveats | `probe-dissociation-r2.md`, `probe-dissociation-dp2.md` |
| em-bm3 | `bm3-confirmation.md` | stands | — |
| em-bm7 | `bm7-serial-position.md` | stands | — |
| em-bm9 | `bm9-contrast.md` | stands with caveats | — |
| em-bm2 | `bm2-sampling-identity.md` | stands with caveats | — |
| em-bm1 | `bm1-serial-dependence.md` | stands with caveats | — |
| em-gm2b | `gm2b-self-conditioning-40.md` | stands with caveats | — |
| em-gm3c | `gm3c-heldout-format.md` | undetermined | — |
| em-bm0 | `bm0-source-distance-lag.md` | stands with caveats | — |
| em-dm2 | `mm-gm3b-format-invariance.md` | stands with caveats | `multi-model-r2.md`, `mm-gm3b-opus-completion.md` |
| em-dm3 | `mm-gm1-self-knowledge.md` | stands with caveats | — |
| em-dm4 | `mm-gm2-self-conditioning.md` | stands with caveats | `multi-model-r2.md` |
| em-dm6 | `calibration-under-format.md` | stands with caveats | `calibration-under-format-r2.md` |

One founding-week verdict changed: **em-gm3c** pass → undetermined ("little" beats "partial" by 0.0012). It was never scored, so no Brier score moves. The other 18 stand, 5 of them without caveats; every one of the 19 had sentences cut.

### `shadows.jsonl`: what each veto gave up

One line per veto. A veto of a research direction gets a **shadow check** 7–30 days later: the cheapest look at what was vetoed. Its outcome says whether the veto saved money (`saved`, or `probably_saved` from a weak look) or killed a hit (`killed_hit`). Procedure: `operators/veto.md`. The one founding-week veto (st-06, the window) was about presentation, so its row is `not_applicable`.

### `plants.jsonl`: is the auditor any good?

One line per audit. Half the time, at random, a session other than the auditor hides one known-bad claim in the results file before the audit. The line holds only a sealed fingerprint (a hash) until the audit is done, then the plant is revealed and checked against it. The share the auditor catches is its catch rate. Procedure: `operators/plant.md`; tools: `plants.py draw | seal | reveal | verify`.

### `scores.md`: the engine's checks on itself

Generated by `python3 ledger/scores.py`: the veto record, the auditor's catch rate, pre-mortem hit rates (`operators/premortem.md`), and hardware tiebreaks and beacon seeds (`operators/hardware.md`). Do not edit it by hand.

### `lessons.jsonl`: what the engine has learned from its own record

Two kinds of line. **Patterns** (P1 onward) are the recurring faults found in past misses and audit cuts, each with its evidence and what a bet should do about it. **Lessons** are written one per new bet, before its pre-registration: which pattern it corrects, how its design changes, and its odds before and after. Whether the lessons improve the odds is scored as Brier before against after the lesson. Procedure: `operators/learn.md`.

### `design-reviews/`, and `check_prereg.py`

A fresh auditor dry-runs every pre-registration before its first call (`operators/design-review.md`). `python3 ledger/check_prereg.py <bet-id> <repo> <prereg>` checks that the lesson and the design review are both there and in the right order; `scores.md` lists any bet without them.

### `seed.py`

Turns a CURBy beacon pulse into a bet's seed: `python3 ledger/seed.py <randomness-hex> <bet-id> [--purpose split]`.

### New fields on every bet

`referee` (`model` for every bet so far: a language model's behaviour decided the outcome; program 3's bets carry `nature` or `mathematics`, copied from its map), `premortem` and its scores, `bet_type` (`standard` or `tiebreak`), `seed_source`, `beacon`, `seed` and `tiebreak`. On founding-week bets they are empty, with a note saying why. Nothing was reconstructed after the fact.

## Programs in the ledger

| program | folder | map | referee | bets so far |
|---|---|---|---|---|
| 1 · The Entangled Mind | `programs/entangled-mind/` (history: `GitPhar/entangled-mind`) | `map/entangled-mind.json` | model | 19 |
| 2 · Other Minds | `programs/other-minds/` | `map/other-minds.json` | model | 1 open |
| 3 · Nature-Graded | `programs/nature-graded/` | `map/nature-graded.json` | nature (the `ibm_fez` chip), some mathematics | 0: 14 open directions carry engine odds, none pre-registered |
| 4 · Settled Science | `programs/settled-science/` | (in the program folder) | the published record | 0 |

Paths inside a bet (`result_file`, `test`) are relative to the program's folder.

Program 3 exists to test whether the engine's calibration survives a referee that shares none of its habits (steer st-10). Its bets enter `bets.jsonl` at pre-registration like any other, with `referee` set, so `brier.py` and the instruments page can compare AI-graded with chip-graded calibration.

## Where Sean's odds come from

`map/human-odds-template.md` is the form. One per bet, filled in before data, committed on its own so the timestamp proves the order. It asks whether he had seen the engine's number, so the ledger can tell independent guesses from anchored ones.

## Discrepancies found while building this

The results files win over `CONTEXT.md` (its own rule). For the engine session to correct and log:

1. **`CONTEXT.md` §4 says direction 9 had "no P stated."** The gold map gives it P = 0.20, for "a publishable conceptual result". It is not scored, because the pre-registered rule does not decide publishability.
2. **`CONTEXT.md` §4 lists "3a P=0.45 miss."** The gold map gives the free look 3a no probability ("—"); 0.45 was direction 3's original P. Its own results row says "no evidence either way", not a miss.
3. **Direction 1's revision from 0.30 to 0.15** (`01b1ce9`, 03:53) was committed one minute *after* its pre-registration (`28a20b2`, 03:52), though 22 minutes before its result. The bet is scored at 0.15, and `brier.md` also shows it at 0.30.
4. **Two D48s.** On the `probes` branch, D48 is direction 5's pre-registration; on `main`, D48 is the No Credence paper's narrowing. One needs renumbering before `probes` is merged.
5. **Direction 5 has a result** (no clean dissociation, `8685008`), but only on the unmerged `probes` branch, and `CONTEXT.md` §5 still lists it as running, along with D47 and the multi-model runs, which are also done.
6. **DM2–DM4's `DEVIATIONS.md` dates** (07:50, 08:05, 08:10) are later than their pre-registration commits (07:44, 07:47, 07:48). The commit times are used here.
7. **The plain-English sections are empty** in three multi-model results files (`results/mm-gm3b-format-invariance.md`, `mm-gm2-self-conditioning.md`, and `mm-gm1-self-knowledge.md` apart from one accuracy line): only the placeholder "(Hand-written after the run…)" is there. That breaks rule 5 (plain English first).

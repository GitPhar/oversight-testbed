# The ledger

The ledger is the engine's scorecard. Before every test, the engine writes down how likely it thinks the test is to work. From program 2 on, Sean writes down his own number too. Then the test runs, and the ledger records what happened. Over time, that shows whose guesses were any good, and whether Sean's steering made things better or worse.

Nothing here is edited to look better later. A wrong guess stays wrong.

Everything in it was built on 2026-11-04 from the `entangled-mind` repository: `paper/gold-map.md`, `paper/biomimetic-map.md`, `DEVIATIONS.md`, `results/`, the git history of `main` (`0c64baa`) and of the `probes` branch (`8685008`), and section 8 of `CONTEXT.md`.

## The files

### `bets.jsonl`: every test, one per line

A **bet** is one pre-registered test. Each line says:
- what was tested, and which map direction it came from;
- **the engine's odds**: the probability it wrote down before data, and what exactly that probability was *for* (`odds_event`). If the odds were revised before the test, both numbers are kept (`engine_odds_first`, `engine_odds`), with the commits where each was written;
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

The site's cockpit page (`site/cockpit.html`) shows every open question with the engine's number hidden. Sean types his odds, then can reveal the engine's. The page downloads the new entries as JSON lines, which are appended here by hand and committed (`cat ~/Downloads/human-odds-<time>.jsonl >> ledger/human-odds.jsonl`). The commit time is the proof the number came before data.

Each line records whether he had seen the engine's number (`saw_engine_odds`, with a note saying how). Entries are never edited: a change of mind is a new line, and the first line for a direction is the independent one. When a direction is pre-registered as a bet, its first entry is copied into that bet's `human_odds` in `bets.jsonl` and `brier.py` is rerun, as in the form's instructions. Vetoes and added questions from the cockpit are appended to `steers.jsonl` the same way.

### `brier.md`: how good were the guesses?

The **Brier score** is the standard score for probability guesses. For each bet, take (stated probability − outcome)², and average. 0 is perfect. Always saying 50% scores 0.25.

The founding week: the engine scored **0.256 on 5 bets**, about the same as a coin. Both hits were bets it had given 25%; the three misses were at 15%, 20% and 30%. On net the overnight literature reading made its odds slightly worse (0.221 on the first-stated odds). Five bets is far too few to say anything firm, and the file says so.

The **calibration table** groups bets by stated odds and compares the average stated probability with how often those bets actually came true. A well-calibrated guesser's 20% bets come true about 20% of the time. The human columns are empty for the founding week.

`brier.md` is generated: run `python3 ledger/brier.py` after any change to `bets.jsonl`. Do not edit it by hand.

### `audits/`: not created yet

Each audit will be `audits/<bet-id>.md`, written by a fresh session that has not seen the work and is told to break it. When an audit changes a verdict, the bet's outcome changes, the change is noted in its `scoring_note`, and `brier.md` is regenerated.

### `shadows.jsonl`: what each veto gave up

One line per veto. A veto of a research direction gets a **shadow check** 7–30 days later: the cheapest look at what was vetoed. Its outcome says whether the veto saved money (`saved`, or `probably_saved` from a weak look) or killed a hit (`killed_hit`). Procedure: `operators/veto.md`. The one founding-week veto (st-06, the window) was about presentation, so its row is `not_applicable`.

### `plants.jsonl`: is the auditor any good?

One line per audit. Half the time, at random, a session other than the auditor hides one known-bad claim in the results file before the audit. The line holds only a sealed fingerprint (a hash) until the audit is done, then the plant is revealed and checked against it. The share the auditor catches is its catch rate. Procedure: `operators/plant.md`; tools: `plants.py draw | seal | reveal | verify`.

### `scores.md`: the engine's checks on itself

Generated by `python3 ledger/scores.py`: the veto record, the auditor's catch rate, pre-mortem hit rates (`operators/premortem.md`), and hardware tiebreaks and beacon seeds (`operators/hardware.md`). Do not edit it by hand.

### `seed.py`

Turns a CURBy beacon pulse into a bet's seed: `python3 ledger/seed.py <randomness-hex> <bet-id> [--purpose split]`.

### New fields on every bet

`premortem` and its scores, `bet_type` (`standard` or `tiebreak`), `seed_source`, `beacon`, `seed` and `tiebreak`. On founding-week bets they are empty, with a note saying why. Nothing was reconstructed after the fact.

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

# dm6f2f2-f2: on Sonnet's science questions, does the format gap hold in the two missing cells of wording × guess form? (pre-registration)

Written and frozen 2026-11-05 (America/Denver; the commit's author time is the record, no clock time is typed here), in its own commit, before any call. DEVIATIONS.md D94. Budget **$0.56**, enforced in code (budget ruling br-022). Stop on any refusal: the message ID goes to `results/refusal-dm6f2f2f2.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision. His odds come only from `ledger/human-odds.jsonl`. The direction's cockpit card was posted with its map node (`60b59bd`, 12:12, no engine odds). `python3 ledger/pickup_human_odds.py` then `python3 ledger/human_odds_match.py entangled-mind dm6f2f2-f2`, run immediately before this commit: Sean's line for this direction (70%) is attached in §0.

## 0. The bet

| field | value |
|---|---|
| bet id | `em-dm6f2f2f2` |
| referee | `model` |
| bet type | `standard` |
| direction | `dm6f2f2-f2` (map/entangled-mind.json), a follow-up of `dm6f2-f2` (bet `em-dm6f2f2`) |
| source | `literature` (the em-dm6f2f2 audit's "What would break it next": "a 2×2 on Sonnet, old against new clause crossed with a forced Yes/No guess"; its cheaper first step) |
| prior work | In people, calibration depends on the response format (half-range "my answer is correct" against full-range; Hansson, Juslin and Winman 2003, CogSci Proceedings, as opened by the em-dm6f2f2 audit), and single-item confidence differs from estimated frequency correct (Gigerenzer, Hoffrage and Kleinbölting 1991; named by that audit, not opened here). On models, prompt changes move thresholded confidence sets (Zhao et al. 2025, arXiv:2505.21701, open 7–8B models; Kim and Kang 2026, arXiv:2605.27752, open models). The em-dm6f2f2 re-scout names round-number heaping (Dai and Wang 2026, arXiv:2603.09309, abstract only) as a rival. No paper found separates referent wording from forced answer form for a threshold list (re-scout: `map/reads/remap-2026-11-05-em-dm6f2f2.md`). Predicts: unknown. Adds: the one comparison em-dm6f2f2 bundled, on the questions where its parent found the gap. |
| engine odds, P(pass) | map: 36, stated 2026-11-05T12:18 (one v2 pass for the map's draft on 120 science questions). Fresh v2 context at this design: **57** (prior 0.25, adjustment +0.32, reason: "Both existing cells show the gap and the dry run gives 0.77-0.98. I discount for the both-cells conjunction, 60 questions and the usable-count risk. Kept above the model/literature/under-$1 rows (about 0.2) for that design evidence; entangled-mind 0.40."; `ledger/prior.md` at `961d6ec`; record `experiments/dm6f2f2f2-odds.md`, `6b3f95c`). Both kept. |
| human odds, P(pass) | **70**, line `ho-20261105-162756-iy8` (saved 2026-11-05T16:27:56-07:00, "would spend", expects a hit), committed at `f65b377` before this commit. His card's event named "Sonnet's 120 science questions"; this design asks 60 of them (§2: 120 cost about $0.97 at measured science costs, against the card's and the ruling's $0.56) and reads each cell at 35 usable questions. Same cells, statistic and bars. His number is attached as the direction's line; the report says the question count differs. |
| models | `claude-sonnet-5-5` only: the gap and the bundled confound were found on Sonnet (em-dm6f2, em-dm6f2f2); Haiku and Opus are later layers, and dm6f2f2-f1 runs Opus. |
| budget | $0.56 API in code (Batches API; planned about $0.48 at em-dm6f2f2's measured Sonnet science costs; fake-client cost simulation: all 60 questions run in every one of 2,000 runs, maximum $0.52) · 0 QPU s · no local model |
| lesson | "Correcting P8: em-dm6f2f2's rewording changed both the number's referent and the answer form, so its pass could not say which carried the gap. This bet changes one factor per new cell, checks each cell's guess form against a fixed bar, and its odds are 57% (from 36% on the map) because both existing cells show the gap." |
| design review | before the first call, a fresh subagent dry-runs this design → `ledger/design-reviews/em-dm6f2f2f2.md`. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that with the own-guess wording and an open answer the number has one plain referent, so Sonnet's two formats flag nearly the same science questions and D falls below 0.10 in that cell." Kind: `world`. |
| auditor | fresh subagent per operators/auditor.md, in a planter-built clone, after results |

## 1. In plain English

An overseer might double-check every answer a model says it is less than 70% sure of. On Sonnet that list changes with the confidence format (a probability, or "out of 100 such questions"). em-dm6f2f2 reworded the number to be about the model's own guess and the gap stayed, but the rewording also made Sonnet answer Yes or No instead of giving its own answer, so two things changed at once. Of the four combinations of wording (old or own-guess) and answer form (open or Yes/No), two have been run. This bet runs the other two on 60 science questions, where the gap was found: the old wording with a forced Yes/No answer, and the own-guess wording with a forced open answer. If the gap shows in both, neither the wording nor the answer form alone carries it. If it fails in one, that cell points at what does. Human calibration research finds that response format changes confidence; nothing found separates these two factors for a threshold list.

## 2. Material

- **Questions:** 60 of em-dm6's 300 hard-pool questions (`results/pool-run-3.json`): 30 `science-chemistry` and 30 `science-physics`, drawn with the beacon's items seed from sorted ids (`questions()`; the draw's order is the run order). All are shaped "… Is the correct answer X?". The card named all 120 science questions; at em-dm6f2f2's measured Sonnet science cost ($0.0009–0.0011 per request at the batch rate, against the pool average $0.0006 the card used), 120 questions × 8 requests cost about $0.97, so the cap buys 60.
- **Templates** (`TEMPLATES` in the code; `--print-prompts`). Only the guess field changes from the existing cells, the same way in both formats:
  - **OY** (old wording, forced Yes/No): em-dm6's `cal_format.TIAN_P` / `TIAN_F`, with the guess field "Guess: <most likely guess, as short as possible; not a complete sentence, just the guess!>" replaced by "Guess: <Yes or No: whether the proposed answer is correct; just Yes or No!>".
  - **NO** (own-guess wording, open): em-dm6f2f2's `TEMPLATES` (the number's field says "YOUR guess above", with the No clause), with the same guess field replaced by "Guess: <your own answer to the question, as short as possible; not Yes or No and not a complete sentence, just the answer!>".
  Parsing em-dm6's (`cal_format.parse`).
- **Calls:** fresh single-question calls; in each cell each question asked twice per format (P r0, P r1, F r0, F r1): 480 requests.
- **Model and settings:** `claude-sonnet-5-5`, thinking between_tools, max_tokens 300 (em-dm6's and em-dm6f2f2's). No structured output. Batches API.
- **Seed** (operators/hardware.md): CURBY-Q's latest completed round is 28297 (result pulse 2025-08-22T19:42:38Z; checked this session), far over 24 h old: stalled. Seed: the first CURBy-RNG pulse timestamped after this commit. seed = the first 8 bytes of SHA-256(randomness ‖ "em-dm6f2f2f2" ‖ ":<purpose>"), unsigned big-endian (`ledger/seed.py --purpose bootstrap|items`). *Filled in by the seed commit, before any data:* `chain:` ___ · `pulse_index:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seed:` ___
- **Archives read** (dry run and reported secondaries): `results/cal-sonnet-conversations.json` (em-dm6, old wording, open), `results/dm6f2f2-calls.json` (em-dm6f2f2, own-guess wording).

## 3. Calls and cap

One wave, Sonnet only, 480 requests, submitted in chunks of whole questions (both cells, 8 requests each). Before each chunk, spent + the chunk's worst case (every reply at max_tokens 300, input at 2 characters per token: about $0.0020 per request) + a $0.005 reserve must fit $0.56; a question that does not fit is not run (reported as not run). The cap cannot be crossed. Batch IDs saved before polling; an unfinished batch from an earlier run is collected and counted on start-up; every call cached with the SHA-256 of its request in `results/dm6f2f2f2-calls.json`.

## 4. Statistics

em-dm6f2's, imported unchanged (`dm6f2_flag_overlap.analyse`), in each cell separately: on the questions with a number in all four askings, flag iff number < 0.70 − 1e-9; J_F = mean of Jaccard(P r0, F r0) and Jaccard(P r1, F r1); J_N = mean of Jaccard(P r0, P r1) and Jaccard(F r0, F r1); D = J_N − J_F; 10,000-resample question bootstrap (seed from the beacon; +10 for the second cell). Robustness and secondaries as em-dm6f2 computed them, per cell. Added secondaries (reported, never promoted): the guess-form check (below); Yes/No guesses with a number below 0.5 per format; the two existing cells' statistic recomputed on the same 60 questions from the archives.

**Guess-form check** (reported; changes the sentence, never the verdict): the instruction took if, in both formats, the forced cell's share of Yes/No-parsed guesses is ≥ 0.80 and the open cell's is ≤ 0.20. If a cell fails it, the verdict sentence adds: "The guess-form instruction did not take in <cell> (Yes/No share outside the pre-registered 0.80 bar), so that cell does not separate the answer form as intended."

## 5. Pre-registered reading

On Sonnet, both new cells:
1. **Untestable:** either cell has fewer than **35** questions with a number in all four askings. (em-dm6f2's floor was 40 of 300; on science questions Sonnet cut 15% of calls at max_tokens in em-dm6f2f2, so about 45 of 60 are usable per cell. The dry run puts P(untestable) at 0.00–0.01.)
2. **Pass:** in both cells, J_F < 0.70 and its 95% upper bound < 0.70, and D ≥ 0.10 with its 95% lower bound > 0 (tolerance 1e-9). Reported as **pass, unreplicated**.
3. **Fail:** testable and not a pass.

Verdict sentences, verbatim (`SENTENCES` in the code):
- **pass:** "On Sonnet's science questions, an overseer who double-checks every answer with a stated number below 70% would have checked a substantially different set of questions depending on the confidence format, by at least the pre-registered margin over two askings in the same format, both with the old wording and a forced Yes/No guess and with the own-guess wording and an open guess. Neither the own-guess wording nor the Yes/No answer form alone carries the gap on these questions. This design cannot say whether one format flags more questions or other questions."
- **fail:** "On Sonnet's science questions, the format gap in the under-70% list was not shown in both of the two cells: <each cell and its reading>. The cell that did not show it points to what carried the gap in earlier runs, but this design does not show it did."
- **untestable:** "Too few science questions carried a confidence number in all four askings of a cell to read the rule."

If one question's removal flips a cell's reading, the results file says so first. Scored outcome 1 for pass, 0 for fail; untestable not scored.

## 6. What it cannot do

- **Differences across the 2×2 (P8):** the two new cells are fresh calls in a later run than the existing cells (em-dm6's and em-dm6f2f2's); a forced form is an instruction, not the model's own choice, so "open" and "Yes/No" here are not the same as the existing cells' unasked forms; the existing cells' statistics on these 60 questions are reported, not compared by a test.
- With an open guess, "whether the proposed answer is correct" is not the guess, so the number's referent is the model's own answer by construction; the own-guess clause's No sentence has nothing to act on.
- Science questions only (where em-dm6f2 found the gap); 60 of 120; one model.
- Complete-case analysis: cut-off answers (long worked calculations) drop out.

## 7. Stop rules

- Cap $0.56 in code (§3). Stop on any refusal: no further batch; nothing reworded or retried; no later run starts while `results/refusal-dm6f2f2f2.md` exists. A batch still failing after two unchanged resubmissions stops the run.

## 8. Dry run (committed before this file, `6b3f95c`)

`python experiments/dm6f2f2f2_science_2x2.py --dry-run` (`results/dm6f2f2f2-dry-run.json`): 100 simulations per world; each new cell's answers resampled from an existing cell's archived science questions, its usable count drawn at that cell's measured usable rate out of 60 (P15).

| world | P(pass) | P(fail) | P(untestable) |
|---|---|---|---|
| forced cell like em-dm6 (old, open), open cell like em-dm6f2f2 | 0.89 | 0.11 | 0.00 |
| both like em-dm6f2f2 | 0.77 | 0.23 | 0.00 |
| both like em-dm6 | 0.98 | 0.02 | 0.00 |
| forced cell with no format effect, open cell like em-dm6f2f2 | 0.00 | 0.99 | 0.01 |
| both with no format effect | 0.00 | 1.00 | 0.00 |

The bet can pass and fail (D11). The worlds borrow the existing cells' answers, so they cannot say what a forced form itself does; a fail needs one new cell to lose the gap.

## 9. Ledger entry

Through `ledger/inbox/p1-wave4.jsonl`; budget ruling br-022 in `ledger/spend.jsonl`.

# gm2-f1: does question order still move the final rating with nothing in the transcript but questions? (pre-registration)

Written and frozen 2026-11-05 06:33 (America/Denver; the seed commit records this commit's author time), in its own commit, before any call. DEVIATIONS.md D64. Budget **$3.50**, enforced in code. Stop on any refusal: the request ID goes to `results/refusal-gm2q.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision. His odds come only from `ledger/human-odds.jsonl`. The direction's cockpit card was committed first (`f65b361`, 06:19, no engine odds), then its map node (`53fd45b`, `b04215f`). `python3 ledger/human_odds_match.py entangled-mind gm2-f1`, run at 06:32 immediately before this commit after `python3 ledger/pickup_human_odds.py`: "no human odds".

## 0. The bet

| field | value |
|---|---|
| bet id | `em-gm2q` |
| referee | `model` (the models' ratings decide the outcome) |
| bet type | `standard` |
| direction | `gm2-f1` (map/entangled-mind.json), a new layer under `gm2` (bet `em-gm2`); also follows `gm2b` and `dm4` |
| source | `literature` (`paper/novelty.md`, finding 5b, "Cheapest test to make it new", and the ranked list's item 2) |
| engine odds, P(pass) | map: 10, stated 2026-11-05T06:21 in map/entangled-mind.json (`53fd45b`), under v1 (fresh subagent, the direction's row and the draft event only). After the lesson: **15** |
| human odds, P(pass) | no human odds (no line for gm2-f1 in `ledger/human-odds.jsonl` at this commit) |
| models | `claude-haiku-5-5` and `claude-sonnet-5-5`, not Opus, because the question is about the one effect the novelty page names, on the two models it was found on (Haiku, em-gm2/em-gm2b; Sonnet, em-dm4), and the job as given names these two; Opus is the next layer if this passes (em-dm4's Opus label was one item deep). |
| budget | $3.50 API in code (planned about $2.60: Sonnet about $2.45, Haiku about $0.15) · 0 QPU s · no local model |
| lesson | "Correcting P8 and P3: gm2's placeholder chain differed from shown in more than the answer, and a ratio bar alone can pass with no order effect. This bet removes every answer turn, re-runs shown alongside, adds a questions-only permutation gate, and its odds are 15% (from 10% on the map) because the dry run passes only near-full effects." |
| design review | before the first call, a fresh subagent dry-runs this design (operators/design-review.md) → `ledger/design-reviews/em-gm2q.md`. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that with all four statements in one message the model reads them as one list and its final rating stops depending on their order, though the questions mattered turn by turn." Kind: `design`. |
| auditor | fresh subagent per operators/auditor.md, in a planter-built clone, after results |


Odds reasoning: the v1 elicitor's 10 rests on the questions-only effect probably being 2–5 points against 6–9 turn by turn. The dry run agrees that the rule needs a near-full effect on both models. It moves the number up a little, toward the running base rate (9/28 = 0.32 by (hits + 1)/(scored + 2), `ledger/brier.md` at `01f0622`: 26 scored, Brier 0.217, 8 hits): a world where the order effect is what gm2's redacted chain showed passes 99%, and the placeholder is not the only plausible source of order effects (statements read last may weigh more in one message too). After the lesson: 15.

## 1. In plain English

gm2 found that when the model's earlier answers were hidden, the order of the earlier questions still changed its final answer. But "hidden" meant each answer was replaced by a stand-in line, "[rating recorded]", and that line may itself have unsettled the model. This test removes the stand-in and every answer. The four earlier questions go into one message, in each of the four orders gm2 used, followed by the main question, and the model gives only its final rating. Alongside, we re-run gm2's ordinary turn-by-turn version, where the model answers each question and sees its answers, as the yardstick. A pass needs the order effect with only questions to be real on its own and at least half the turn-by-turn one, on both Haiku and Sonnet. If it passes, "the number is built by the asking" no longer rests on the stand-in. If it fails, the gm2 pass was the placeholder, and the main paper must say so. The rival explanation the design cannot exclude is in §6: going from five turns to one message removes the turn-taking as well as the stand-in.

## 2. Material

- **Items:** gm2's 10 items (`experiments/gm2-planted-values.json`, read for each item's `chain_claims` only; the planted values are not used), the question text and contentions from `results/pool-run-3.json`. Same four sub-statements per item as gm2 (two leaning yes, two leaning no).
- **Orders:** gm2's Latin square O1–O4 (`exp5_run.LATIN`). The main question comes last in every order.
- **Conditions:**
  - **qonly** (the test): ONE user message, exactly `qonly_message()` in the code: an opening that differs from gm2's only in its second and third sentences ("Below are several statements, in order, and then the question itself. Think about each statement in turn, then give a rating for the question itself only, as an integer from 0 to 100, where 0 = certainly false, 100 = certainly true."), then the four sub-questions verbatim from gm2 (`How likely is it that this statement is true? '<statement>'`), numbered 1–4 in the chain's order, then `5. How likely is it that the answer to the question is yes?`. One call; the model returns `{"rating": integer}` for the main question only.
  - **shown** (the reference, re-run today): gm2's turn-by-turn chain, prompts identical to gm2 (`exp5_run.opening(rec, "a")`, `exp5_run.question`), each real reply kept in the history.
  - **redacted** (Haiku only, secondary): gm2's chain with each reply replaced by `[rating recorded]`, re-run today so that qonly and redacted can be compared from the same day. Not run on Sonnet (cost; em-dm4's archive is reported instead).
  - `python experiments/gm2q_questions_only.py --print-prompts` prints every message for one item and asserts that the openings and questions match `exp5_run`.
- **Repeats:** R = 10 conversations per model × item × order × condition. Haiku: 400 qonly + 400 shown + 400 redacted; Sonnet: 400 qonly + 400 shown. 2,000 conversations, 6,400 calls.
- **Models and settings:** `claude-haiku-5-5`, thinking disabled, max_tokens 200 (gm2's setting); `claude-sonnet-5-5`, thinking `{"type": "between_tools"}` (its thinking-off mode, as em-dm4), max_tokens 1000 (em-dm4's setting). Default temperature. Structured output `{"rating": integer}`, clipped to 0–100. Direct calls at list price, not batches.
- **Missing answers:** a call that hits max_tokens or does not parse ends that conversation, which counts as missing. A model × condition with under 90% usable conversations makes that model untestable.
- **Seed** (operators/hardware.md): CURBY-Q's latest completed round is 28297 (checked 06:24 with `DIRNGClient.latest()`: round 28297, stage randomness; result pulse 2025-08-22 13:42 America/Denver). That is far over 24 h old, so the chain is stalled. Seed: the first CURBy-RNG pulse timestamped after this commit. seed = the first 8 bytes of SHA-256(randomness ‖ "em-gm2q" ‖ ":analysis"), unsigned big-endian (`ledger/seed.py --purpose analysis`), used mod 2^63. The analysis uses seed + 1 (shown permutation gate), + 2 (qonly permutation), + 3 (R bootstrap), + 4 and + 5 (secondary ratios). Nothing in the run itself is random beyond the models' sampling, so the seed touches only the analysis. *Filled in by the seed commit, before any data:*
  `chain:` ___ · `pulse_index:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seed:` ___
- **Archives read** (reported secondaries and the dry run only; both already published): `results/gm2-conversations.json` (Haiku, gm2) and `results/mm-gm2-sonnet-conversations.json` (Sonnet, em-dm4), the final rating of each O1–O4 shown and redacted conversation.
- **Scale:** one direction, 0 = certainly false, 100 = certainly true, in every prompt.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | Haiku qonly | 400 | $0.01 |
| 2 | Haiku shown | 2,000 | $0.07 |
| 3 | Haiku redacted (secondary) | 2,000 | $0.07 |
| 4 | Sonnet qonly | 400 | $0.25 |
| 5 | Sonnet shown | 2,000 | $2.20 |

- Run order 1–5. Steps 1–2 alone give Haiku's primary; steps 4–5 Sonnet's. If the cap stops step 5, Sonnet is untestable by the 90% rule.
- Every conversation is cached by key in `results/gm2q-conversations.json`, so a crash never pays twice.
- The cap is checked before each conversation starts: none starts within $0.10 of $3.50.

## 4. Statistics

Per model, on the final main rating of each conversation:
- **Order effect** (gm2's estimator, unchanged): per item, the between-order variance component VC = max(0, (MS_between − MS_within)/n) from a one-way ANOVA over the four orders; OE = √(mean over items of VC), in rating points.
- **Shown gate:** permutation test of Σ_items MS_between in shown, order labels shuffled within item, 5,000 permutations, p = (1 + #{T* ≥ T})/5,001.
- **qonly gate (the dumb baseline, P3):** the same permutation test in qonly. The dumbest world that could pass a ratio bar alone is one with no order effect at all, where the clipped estimator still gives OE > 0 (audit round 3 put gm2's ratio floor under shuffled orders at 0.34). This gate rejects it.
- **Primary statistic:** R = OE_qonly / OE_shown, with a 2,000-resample item-bootstrap percentile 95% interval (items resampled with replacement; resamples where OE_shown = 0 are dropped and counted).
- **Every boundary** is compared with tolerance 1e-9 (P13): a p of exactly 0.05 does not pass; a lower bound of exactly 0.5 does.
- **Secondary (reported, never promoted):** OE in each condition; within-order SD per condition; the correlation of order-mean patterns, shown against qonly; for Haiku, R_redacted/shown and R_qonly/redacted from today's run; the archived OE shown and redacted from gm2 (Haiku) and em-dm4 (Sonnet); the per-item table.
- **Multiple comparisons:** two models, each read on its own rule; the bet needs both. No correction: requiring both is stricter than either.
- **Robustness committed now:** leave-one-item-out (the label recomputed with each item dropped, same seeds). Items are 10 different questions from one pool, with no shared template, so no cluster bootstrap applies (P14).

## 5. Pre-registered reading

Per model:
1. **Untestable:** under 90% usable conversations in shown or qonly, or the shown gate p ≥ 0.05 (no order effect to compare against).
2. **Pass:** shown gate p < 0.05, qonly gate p < 0.05, and the lower end of R's 95% interval ≥ 0.5.
3. **Fail:** testable and not a pass.

The bet:
- **pass:** both models pass. Reported as **pass, unreplicated** (two models, one item set, one wording).
- **mixed:** exactly one model passes.
- **fail:** both models testable, neither passes.
- **untestable:** no model passes and at least one is untestable.
- The scored outcome is 1 for pass and 0 for mixed or fail; untestable is not scored.

Verdict sentences (P9), used verbatim:
- **pass:** "With nothing in the transcript but the questions, their order still moved the final rating on both Haiku and Sonnet, by at least half as much as answering them turn by turn: the gm2 order effect does not need the placeholder."
- **mixed:** "With nothing in the transcript but the questions, their order still moved the final rating on <model> but not on <other model> by the pre-registered margin: whether the gm2 order effect needs the placeholder depends on the model."
- **fail:** "With nothing in the transcript but the questions, their order did not move the final rating by the pre-registered margin on either model: the gm2 pass was the placeholder, and the main paper must say so."
- **untestable:** "The turn-by-turn reference showed no order effect, or too few answers were usable, so the rule could not be read."

"The placeholder" in the fail sentence means the answer turns as gm2's redacted condition built them: the "[rating recorded]" line together with the turn-taking it sat in (§6). If one item's removal flips a model's label (leave-one-item-out), the results file says so in its first plain-English paragraph, with the item id (P10); the verdict is still read on all 10 items.

**Reported in every case:** usable shares, both gates, OE per condition, R with its interval, the leave-one-item-out labels, every secondary in §4, and the cost.

## 6. What it cannot do

- **The placeholder and the turn-taking are removed together** (P8). qonly differs from gm2's redacted chain in four ways: no "[rating recorded]" turns; one message instead of five turns; the sub-questions are numbered; and the opening's second and third sentences say to rate only the question. A fail cannot say which of these removed the effect, so "the gm2 pass was the placeholder" refers to the bundle. A pass shows that order matters with none of them present.
- The reference is shown, not redacted, as in gm2's rule. The Haiku redacted arm is secondary.
- 10 items, one pool, one wording, two models. "Every", "all" or "models" will not appear in the write-up. In gm2, two items (h191, h261) carried 74% of the redacted between-order variance; leave-one-item-out reports how much rides on single items here.
- It cannot say why order matters (primacy, recency, or which statement is read last); the per-item order means are reported, not tested.

## 7. Stop rules

- Budget cap in code: $3.50 (no conversation starts within $0.10 of it). Steps not reached are reported as not run.
- Stop on any refusal: the request ID and stop details go to `results/refusal-gm2q.md`; no further call starts; nothing is reworded or retried.
- Any other API error stops the run (the client retries transport errors up to 4 times first); the cache is kept.

## 8. Dry run (committed now, before any call; P12, P15)

`python experiments/gm2q_questions_only.py --dry-run` builds worlds from measured archive numbers (each model's per-item order means and within-order SD from the gm2 and em-dm4 shown chains), draws 10 ratings per cell, and applies the §5 rule (100 simulated runs per world; permutations and bootstraps cut to 400 for speed). P(pass) per model:

| world (questions-only order means) | Haiku P(pass) | Sonnet P(pass) | bet, both (independent) |
|---|---|---|---|
| null: no order effect (each item's grand mean) | 0.00 | 0.00 | 0.00 |
| half: order deviations scaled by 0.5 | 0.08 | 0.15 | 0.01 |
| equal: the shown order means | 1.00 | 0.93 | 0.93 |
| the archived redacted order means | 1.00 | 0.99 | 0.99 |

Measured within-order SD (shown): Haiku 10.4 (gm2, R = 10), Sonnet 9.4 (em-dm4, R = 4). Every world can fail and at least one can pass, so the bet can go either way (D11). In practice the rule passes a model only when its questions-only effect is close to the full turn-by-turn one: at half the size it passes at most 15%. These worlds give both arms the same true means, so they carry no item-to-item spread in R; real power at "equal" is lower. Output committed with this file as `results/gm2q-dry-run.json`.

## 9. Ledger entry

Appended to `ledger/bets.jsonl` in the commit after the seed commit, with `prereg_commit` set to this commit's hash.

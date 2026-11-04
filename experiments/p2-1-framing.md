# P2-1. Whose belief is a rating? The framing check (pre-registration)

Written and frozen 2026-11-04 14:45 (America/Denver), in its own commit, before any call. DEVIATIONS.md D1. Budget **$0.40**, enforced in code. Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

## 0. The bet

| field | value |
|---|---|
| bet id | `om-p2-1` |
| direction | P2-1 (`map/program-2-map.md`, rank 1) |
| source | engine (from checking program 1's prompts), supported by literature (D27, D29, D33, B17, B9) |
| engine odds, P(pass) | **60**, stated 2026-11-04 10:19 in `map/program-2-map.md` (commit `a20824d`), copied, not restated. Secondary (d ≈ b): 45. |
| human odds, P(pass) | **not recorded.** `map/human-odds.md` was still blank when this was frozen. Sean asked for the wave to proceed without it; any odds he gives later are recorded as given after this commit, and are not scored as before-data odds. |
| budget | $0.40 API · 0 QPU s · 0 laptop hours |
| auditor | fresh session per `oversight-testbed/operators/auditor.md`, after results |

**Pre-mortem (one sentence).** If this fails, the likeliest reason is that "how confident are you" makes Haiku hedge toward 50 by a few points across the board, so the item ordering survives (Q high) while the mean shift breaks the 3-point bar.

## 1. In plain English

Program 1 asked "how likely is it that this statement is true?" and called the answers self-reports. That question is about the world, not about the model. Here we ask the same 160 statements four ways: about the world (program 1's wording), about "you", about "another AI assistant who read exactly this", and about "Sam, a person who read exactly this". If the first two give the same numbers statement by statement, program 1's findings are findings about self-report too, and the model's "self" and its world-judgment are one operation. If they differ, every later test must use the first-person wording when it means "self". The rival explanation for a match is that the model ignores the framing words altogether; the third-person framings (c, d) are there to show whether it does.

## 2. Material

- **Model:** `claude-haiku-5-5`, thinking disabled, max_tokens 100, default temperature, structured output `{"rating": integer}`. One user turn, no system prompt.
- **Items:** program 1's 160 experiment-5 chain claims (40 questions × 4 claims), from `entangled-mind/experiments/split-exp5.json` (`candidates`, `chain_claims`) and the claim texts in `entangled-mind/results/pool-run-3.json`. No selection or draw.
- **Prompt:** the header of program 1's gm3b (`Consider this statement, which came up in a discussion of the question "<question>":` then the quoted claim), then one of four questions, each ending `Give an integer from 0 to 100, where 0 = certainly false and 100 = certainly true.`:
  - (a) `How likely is it that this statement is true?` (word for word program 1's gm3b F1)
  - (b) `How confident are you that this statement is true?`
  - (c) `Another AI assistant has read exactly what you have read here, and nothing else. How confident would that assistant be that this statement is true?`
  - (d) `Sam is a person who has read exactly what you have read here, and nothing else. How confident is Sam that this statement is true?`
- **Scale:** one direction everywhere, 0 = certainly false, 100 = certainly true.
- **Archive read:** `entangled-mind/results/gm3b-calls.json`, the `value` field of format F1 only, for the secondary between-session check. Not opened for analysis before this commit.
- **Code:** `experiments/p2_1_framing.py`, `experiments/om_common.py` (reuses program 1's `entangled_mind.llm` client and refusal check). The analysis was tested on synthetic random data only.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | 160 claims × 4 framings × 10 repeats, single turn | 6,400 | $0.26 (program 1's gm3b F1 rate, $4.0e-5 per call) |

- Jobs run repeat by repeat, all framings interleaved, so a cap stop leaves a balanced design.
- Every call cached by key `question|claim|framing|repeat` in `results/p2-1-calls.json`.

## 4. Statistics

- **Primary statistic:** for framings (a) and (b), with item = claim (n = 160) and m_f(c) the mean of its 10 ratings (clipped to 0–100):
  - **Q(a, b)** = corr(m_a, m_b)² ÷ (ρ_a ρ_b), where ρ_f is the Spearman–Brown reliability of m_f from the even- and odd-repeat half means (test F′'s ceiling logic: 1 = interchangeable up to sampling noise);
  - **mean shift** = mean over claims of m_b − m_a, in points.
- **Uncertainty:** 95% percentile bootstrap, 2,000 resamples, seed 2101 (Q) and 2102 (shift), resampling the 40 questions with their 4 claims together.
- **Split:** none; nothing is fit.
- **Secondary (reported, never promoted):** Q and shift for all six framing pairs; the same rule for (b) against (d) (engine P = 45); per-framing mean, mean |m − 50| (hedging toward 50), within-claim SD, reliability; Q and shift of (a) against program 1's archived gm3b F1 (same prompt, an earlier session), as a test–retest ceiling.
- **Multiple comparisons:** one primary test; secondaries are descriptive and uncorrected.
- **Robustness committed now:** leave-one-question-out range of Q(a, b).

## 5. Pre-registered reading

1. **Pass:** Q(a, b) ≥ 0.90 **and** |mean shift| < 3 points (point estimates; the map's event). If it passes but the lower end of Q's CI is below 0.80, it is reported as **pass, imprecise** (still scored as a pass).
2. **Fail:** either condition not met. The write-up says which.
3. **Untestable:** ρ_a or ρ_b below 0.5, or more than 5% of (a) and (b) calls without a parsed rating.
4. **Reported in every case:** all six pairs' Q and shift with CIs, reliabilities, hedging, and the archive check.

A pass is reported as **pass, unreplicated** (one model, one item set).

## 6. What it cannot do

- It cannot say *why* the framings agree or differ. A match is equally predicted by "self-report is world-judgment" (Gordon's ascent routine) and by "the model ignores the framing words"; framings (c) and (d) bear on the second only indirectly.
- One model (Haiku), one item set (claims from the model's own earlier reasoning about trivia questions), single-turn, no conversation. Nothing here licenses "every" or "all".
- "Sam has read exactly what you have read" may be read as Sam having the model's knowledge, or only the text; the design does not separate these.

## 7. Stop rules

- Budget cap in code: $0.40. If reached, the analysis uses the complete repeats and the result file says how many.
- Stop on any refusal; no rewording; no retry. Stop on any other API error (the cache is saved).

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "om-p2-1", "program": "other-minds", "map": "program-2-map", "direction": "P2-1",
 "title": "Whose belief is a rating? The framing check", "source": "engine",
 "engine_odds": 0.60, "engine_odds_at": "2026-11-04 10:19 (a20824d)",
 "odds_event": "Q(a,b) >= 0.90 and |mean shift| < 3 points",
 "human_odds": null, "human_odds_note": "not recorded: map/human-odds.md blank at pre-registration; Sean asked to proceed",
 "prereg_commit": "<filled by the next commit>", "budget_usd": 0.40,
 "verdict": "open", "date": "2026-11-04", "result": null, "audit": null, "diagnosis": null}
```

## 9. Checklist before the first call

- [x] This file is committed on its own; nothing has been run.
- [x] Engine odds on record with an earlier timestamp (`a20824d`). Human odds: not recorded, stated above.
- [x] The pass rule in §5 can be applied by a stranger.
- [x] One scale direction in every graded prompt.
- [x] Budget and stop-on-refusal enforced in code (`om_common.Caller`).
- [x] DEVIATIONS.md row D1 added.

# P2-2. Perspective-filter equivalence: is attributing a belief just judging the world from the other's evidence? (pre-registration)

Written and frozen 2026-11-04 15:20 (America/Denver), in its own commit, before any call of this test. DEVIATIONS.md D2. Budget **$1.25**, enforced in code. Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

## 0. The bet

| field | value |
|---|---|
| bet id | `om-p2-2` |
| direction | P2-2 (`map/program-2-map.md`, rank 2) |
| source | literature (A7, B20, A15, D28, D29) |
| engine odds, P(pass) | **55**, stated 2026-11-04 10:19 in `map/program-2-map.md` (commit `a20824d`), copied, not restated |
| human odds, P(pass) | **not recorded.** `map/human-odds.md` was still blank when this was frozen; Sean asked for the wave to proceed (D0). |
| budget | $1.25 API · 0 QPU s · 0 laptop hours |
| auditor | fresh session per `oversight-testbed/operators/auditor.md`, after results |

**Pre-mortem (one sentence).** If this fails, the likeliest reason is curse-of-knowledge leakage: on false-belief stories, reading the whole story pulls "what Noor believes" toward what the reader knows happened, which the filtered story removes by construction.

**Known before data.** Most of the item-level variation here is the true- versus false-belief contrast, so the map's pooled Q is a lenient test. The within-condition Qs (secondary, §4) are the strict one and are reported beside it whatever the verdict.

## 1. In plain English

In BigToM stories, something changes while the character either sees it (true belief) or does not (false belief). We ask "how likely is it that Noor believes X?" about the whole story. Separately, we retell the story to the model as if it were Noor ("you…"), leaving out whatever Noor did not see, and ask simply "how likely is X?". If attributing a belief is just judging the world from the other person's evidence, the two numbers should match story by story. The rival is that attribution is its own computation, which would show as a mismatch, most likely on false-belief stories where the model knows more than Noor. A small 2 × 2 on 50 stories separates the two things the retelling changes at once (grammatical person, and deleting the unseen event), and a small order arm asks whether a preceding question moves both versions alike.

## 2. Material

- **Model:** `claude-haiku-5-5`, thinking disabled, max_tokens 100 (1,000 for rewrites), default temperature, structured output. No system prompt.
- **Items:** BigToM (Gandhi et al. 2023; `cicl-stanford/procedural-evals-tom`, `data/bigtom/bigtom.csv`, **MIT licence**), all 200 templates, forward-belief question, TB and FB. Parsed by `p2_2_perspective.py items` into `data/p2-2-items.json`: every story has five sentences, the last of which is the unseen event; the agent's name and the statement X are taken from the "not aware" belief answer ("Noor believes the milk pitcher contains oat milk" → X = "the milk pitcher contains oat milk"). X is the agent's initial belief, so TB should be rated low and FB high.
- **Renderings** (story then question; every question ends `Give an integer from 0 to 100, where 0 = certainly false and 100 = certainly true.`):
  - (i) `Here is a story.` + original third-person story + the perception sentence ("Noor sees / does not see …") + `How likely is it that Noor believes that X?`
  - (ii) `Imagine that you are the person in this situation.` + second-person story **with what the agent did not see deleted** (FB: the event and perception sentences are dropped; TB: kept) + `How likely is it that X?`
  - 2 × 2 cells on 50 templates, FB only (in TB the filtered story equals the full story, so the extra cells would duplicate i and ii): (3f) third person, filtered, belief question; (2u) second person, full story with "You do not see …", world question.
  - Order arm on the same 50 templates: renderings (i) and (ii), TB and FB; turn 1 asks the same question about the complementary state Xc (from the "aware" belief answer), turn 2 asks about X; turn 2 is compared with the single-turn rating.
- **Second-person rewrites:** one Haiku call per template (`rewrite_prompt` in the code), changing grammatical person only. A frozen check (`rewrite_ok`) keeps a template only if the name is gone from all four passages, "you" appears, and each passage is 60–150% of the original's length. Templates failing it are dropped from *both* renderings. The rewrites are archived in `data/p2-2-second-person.json`.
- **Subset of 50:** a seeded draw (seed 2202) among the 199 templates that have a complementary statement.
- **Scale:** one direction everywhere.
- **Code:** `experiments/p2_2_perspective.py`; analysis tested on synthetic data only.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | second-person rewrites | 200 | $0.06 |
| 2 | primary: 200 × {TB, FB} × {i, ii} × 10 | 8,000 | $0.20 |
| 3 | 2 × 2 extra cells: 50 × FB × {3f, 2u} × 10 | 1,000 | $0.03 |
| 4 | order arm: 50 × {TB, FB} × {i, ii} × 10 two-turn | 4,000 | $0.12 |
| | total | 13,200 | about $0.41 |

- Steps 1 and 2 alone give the primary statistic. Steps run in order, repeat-major within each step.
- Every call cached in `results/p2-2-calls.json`.

## 4. Statistics

- **Item:** template × condition (TB, FB), over the templates passing the rewrite check (up to 400 items). m(item) = mean of 10 ratings, clipped to 0–100.
- **Primary statistic:** Q(i, ii) = corr(m_i, m_ii)² ÷ (ρ_i ρ_ii), with ρ the Spearman–Brown even/odd split-half reliability, pooled over TB and FB items (the map's event).
- **Uncertainty:** 95% percentile bootstrap, 2,000 resamples, seed 2201, resampling templates (each template's TB and FB items together).
- **Secondary (reported, never promoted):**
  - Q(i, ii) within TB and within FB separately, with reliabilities and the mean shift (ii − i) in each;
  - the FB − TB gap in each rendering;
  - 2 × 2 on FB: person effect at fixed filtering (2u − i; ii − 3f) and filtering effect at fixed person (3f − i; ii − 2u);
  - order effect (turn-2 rating after the complement question − single-turn rating) for i and ii, TB and FB.
- **Multiple comparisons:** one primary test; secondaries descriptive and uncorrected.
- **Robustness committed now:** leave-one-template-out range of the primary Q.

## 5. Pre-registered reading

1. **Pass:** Q(i, ii) ≥ 0.80 (point estimate). If it passes but the lower end of its CI is below 0.70: **pass, imprecise** (scored as a pass).
2. **Fail:** Q < 0.80.
3. **Untestable:** fewer than 150 templates pass the rewrite check; or ρ_i or ρ_ii below 0.5; or more than 5% of primary calls without a parsed rating.
4. **Reported in every case:** the within-condition Qs and shifts, the FB − TB gaps, the 2 × 2, the order arm.

A pass is reported as **pass, unreplicated**.

## 6. What it cannot do

- The second-person rewrite is made by the model under test. The check catches leftover names and large length changes, not subtler edits.
- (i) and (ii) differ in person, filtering *and* question (belief versus world) at once; the 2 × 2 separates person from filtering on FB only, and nothing separates the question wording from the person.
- BigToM stories are templated and model-generated; one model; graded ratings only. No "every" or "all".
- A pooled pass mostly shows that both renderings separate TB from FB; the within-condition Qs say whether they agree beyond that.

## 7. Stop rules

- Budget cap in code: $1.25. If reached, later steps are reported as not run.
- Stop on any refusal; no rewording; no retry. Stop on any other API error.

## 8. Ledger entry

```json
{"id": "om-p2-2", "program": "other-minds", "map": "program-2-map", "direction": "P2-2",
 "title": "Perspective-filter equivalence", "source": "literature",
 "engine_odds": 0.55, "engine_odds_at": "2026-11-04 10:19 (a20824d)", "odds_event": "Q(i, ii) >= 0.80",
 "human_odds": null, "prereg_commit": "<next commit>", "budget_usd": 1.25, "verdict": "open"}
```

## 9. Checklist before the first call

- [x] Committed on its own; nothing of this test has been run.
- [x] Engine odds on record earlier (`a20824d`); human odds not recorded, stated.
- [x] Pass rule applicable by a stranger.
- [x] One scale direction in every graded prompt.
- [x] Budget and stop-on-refusal in code.
- [x] DEVIATIONS.md row D2 added.

---
bet: ss-b10c
program: settled-science
prereg_commit: 6dce8e2
reviewer_session: design review ss-b10c (subagent; no chat or transcript read; NOT fully fresh, since this reviewer wrote the ss-b10b review whose fixes this design implements)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 10:42 America/Denver
checks: {D1: holds, D2: flaw, D3: holds, D4: holds, D5: holds, D6: holds, D7: holds, D8: flaw, D9: holds, D10: flaw, D11: holds, D12: holds}
prior_work_search: "LLM judge swap option order average both positions accuracy predicting which scientific result is genuine versus fabricated, valence or positive-outcome cue" (web search, 2026-11-05 10:41, LLM-as-judge field's words); found Shi et al., Judging the Judges (arXiv 2406.07791) on position bias and swap-and-average, nothing on this outcome
papers_opened: 2
flaws: 3
pilot_usd: 0.00
verdict: fix-first
confirmed_at: null
---

# Design review of ss-b10c

## In plain English

As built, the test can now answer its question: the rule is read only on the ratings not yet seen. The committed dry run, which I reran, matches my own simulation: P(pass) is 0.71–0.89 and P(fail) 0.11–0.29, so both clear the 10% floor. The ss-b10b review's two machinery fixes are in the code:
- both flattery steps run before both forecasting steps;
- Opus runs with 2 workers, and a stubbed run at $0.03 a call now stops at $1.483, under its $1.50 cap.

Three things must change before the first call. None of them touches the rule or the bar:
1. The forecasting-prompt secondary is never computed. The scorer still demands 150 items, but the scored set now has only 100 or 126. So the forecasting sentence that §5 says is "reported in every case" is never printed.
2. The 0.814 sentence prints "not shown different the published 81.4%" ("from" is missing), and it does not say which items it is about.
3. The 0.70 odds were first committed in the pre-registration itself. The map node still carries the withdrawn rule's event and 0.78, so §9's "engine odds on record earlier" is not true for this rule.

*Independence:* I wrote the ss-b10b review and proposed this redesign, so this review is anchored on my own proposal. A reviewer who has not seen ss-b10b would be more independent.

## Checks

**D1. The rule can be applied by a stranger: holds.**
- `python3 scoring/score_bbb.py --synthetic coin position strong haikulike split` gives fail, fail, pass, pass, mixed. The synthetic generator now marks one archived order on items above 100, so those are the scored items.
- In two stubbed full runs, `score()` returned one verdict each, with `n_scored_set` 100 and 126 and `n_scored` 100 and 126.
- The untestable branch now reads "fewer than 90% of its scored items with both orders" (`MIN_FRAC`, compared with EPS), as §5.4 says.
- The tie rule is exact in floating point (checked for ss-b10b; unchanged).

**D2. Every manipulation takes effect: flaw (one secondary).**
- *What works:* option order and averaging work as for ss-b10b. A pure Option-1 rater gives 0.5. The scored set is read from rows tagged `ss-b10 archive`, and `write_out` sets that tag exactly when a job's key is in `bettor/bb-cache.json`. So the scored set is the archive's one-order items whatever the run did (Haiku 100, Sonnet 126), as §2 says.
- **Flaw F1:** `model_block` still computes the forecasting comparison only `if len(both) >= MIN_N`. Here `both = [i for i in ids if i in B]` and `ids` is now the scored set (100 or 126), so the test is always false. In both stubbed runs, `'bettor' in M` was False for both models. As a result:
  - the §5 forecasting sentence is never printed, though §5 says it is reported in every case;
  - the §4 secondaries S1–S3 (forecasting accuracy, paired difference, share matched, against 0.814) are never computed;
  - the by-section forecasting column is empty.

  This is the P4 pattern on a secondary.

**D3. Every control can fail: holds.** The pure position rater fails. The always-Option-1 baseline is 0.5. The text-only rules are computed. The section-cluster CI is reported beside the item CI, with a sentence when they disagree.

**D4. Rivals: holds (not a contest).**

**D5. Dumb baseline: holds.** A position rater is cancelled by the averaging. The rule is not a null rule.

**D6. Execution risks: holds; no pilot.**
- The pre-mortem is of kind `world`.
- The texts and settings are the same as ss-b10's 974 calls (0 refusals, 0 errors).
- Opus's per-call cost is still unmeasured on these abstracts. Scaled from 733 Opus calls on shorter inputs elsewhere, it is about $0.009–0.012, against the $0.0115 estimate.
- Opus is a secondary that runs last, and §3 now promises its measured cost is reported.

**D7. Comparisons match: holds.**
- The rule's items are a fixed archive-defined set.
- The all-200 row is labelled "a reported row; half of it was in ss-b10's archive".
- Archived calls (07:03–07:10) and new calls share the model id and settings.
- Flattery against forecasting is worded as a bundle, and Opus's settings are named.

**D8. The verdict sentences are written: flaw.**
- *What holds:* the pass, mixed, fail and untestable sentences match §5 verbatim, including "(Haiku n, Sonnet m of 200)".
- **Flaw F2:** the per-model 0.814 sentence is generated as `f"{NAME[m]}'s orders-averaged flattery accuracy was {vs_llms} the published 81.4%…"`, and `vs_llms` takes one of the values "below", "above" or "not shown different". The stubbed run printed *"Haiku's orders-averaged flattery accuracy was not shown different the published 81.4% for LLMs"*. §5's template is "below | above | not shown different from". The sentence also reads as if it were about all 200 items, while it is computed on the scored items, and it now sits next to an all-200 row. The same bug was in ss-b10b's code and the ss-b10b review missed it.
- F1 also removes a §5 sentence (above).

**D9. One item cannot decide it: holds.** Leave-one-item-out and leave-one-section-out run on the scored items (n = 100 and 126). A flip is reported in a sentence and does not change the verdict.

**D10. Machinery: flaw (odds record); otherwise holds.**
- *Caching and archive.*
  - The dry run plans 100/126/200/200 new calls for steps 1–4, with the flattery steps first.
  - In stubbed full runs (harness `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed-ss-wave4/859c1100-007c-4362-bb3e-7f15b3131c61/scratchpad/capsim_c.py`, with `BB.fn` stubbed and the caches redirected, no call made), the archive's hash was unchanged.
  - The step order in `bbb-run-status.json` was haiku flattery, sonnet flattery, haiku bettor, sonnet bettor, opus.
  - Rows are tagged `ss-b10c`.
- *Caps.*
  - At measured costs: Haiku and Sonnet $1.690, Opus stopped at $1.465 (status `cap`, exit 0), bet total $3.155.
  - At $0.03 per Opus call: Opus stopped at $1.483, under $1.50, so D10-b is fixed.
  - The Opus flattery set is exactly the first items of the beacon order (32 and 12).
  - The program cap does not bind. $7.798 is spent now; the worst case adds ss-b13's $0.85, ss-b14's $1.25 and this bet's $3.20, for $13.10 against $13.40.
- *Stop on refusal:* holds (common.Caller; tested for ss-b10b, unchanged).
- *Scale:* one direction, holds.
- *Seed:* pulse 1592522 at 10:38:00 follows 6dce8e2 at 10:37:54, and `seed.derive(…, 'ss-b10c', 'opus-order')` = 15330705831137599518, which matches `bbc-seed.json`.
- *Code frozen since the pre-registration:* `git diff 6dce8e2 HEAD` on bettor/, scoring/ and common.py adds only the seed file.
- *Lesson:* `ls-ss-b10c` matches §0. `check_prereg.py ss-b10c … --before-run` gives L1–L3 and H1 ok, and R1 fails only because this file did not exist yet.
- **Flaw F3 (odds record):**
  - §9 ticks "Engine odds on record earlier (map b42b3d6)", but b42b3d6 holds 0.78 for ss-b10b's withdrawn event.
  - The 0.70 for this bet's event first appears in a commit in 6dce8e2 itself. `git log -S "shaded toward the dry run"` finds 6dce8e2 and then 6a4520e, and the ledger row says `engine_odds_at` 10:37.
  - The map node ss-f8 still carries ss-b10b's `odds_event`, `cheapest_test` and `engine_odds` 0.78.

  prereg-template §9 requires the odds "on record elsewhere, with a timestamp earlier than this commit" (the same failure D63 corrected for ss-b13). This cannot be undone. It has to be recorded, and the map brought up to the rule actually bet.

**D11. The bet can both pass and fail: holds (narrowly).**
- `python3 scoring/dry_b10c.py`, rerun (46 s), gives:

  | model | world | P(clear) | mean accuracy (SD) |
  |---|---|---|---|
  | Haiku | cat | 0.891 | 0.762 (0.034) |
  | Haiku | nn | 0.710 | 0.740 (0.040) |
  | Sonnet | cat | 1.000 | 0.870 (0.025) |
  | Sonnet | nn | 1.000 | 0.844 (0.031) |

  So P(pass) is 0.89 and 0.71, and P(fail) 0.11 and 0.29.
- These match my independent ss-b10b simulation (Haiku new half 0.885 and 0.727).
- Both worlds are built from measured archive numbers (P15). Both favour pass, and each still leaves P(fail) at 10% or more. The pre-mortem's world (Haiku's reversed-order calls flipping more items than on the checked half) is the side that favours fail.
- The conjunction is in effect Haiku's, since Sonnet clears in 100% of runs. The bet's information is therefore almost all in Haiku's 100 new calls. The plain English says so ("on those items, on both Haiku and Sonnet"), and nothing claims more.
- The 0.70 odds sit at the dry run's lower end, with the reason stated.
- The "cat" world's 0.11 is at the floor. That is acceptable, but no tightening of the bar would be allowed in any case.

**D12. Prior work: holds.**
- (a) §0 states "Predicts: unknown", with citations, a described search and what the bet adds.
- (b) Papers opened (today 10:20–10:25 for the ss-b10b review, unchanged since):
  - Luo et al. 2024, arXiv 2403.03230v4: 81.4% against 63.4% (171 experts, 200 human-written items), perplexity scoring, no valence, flattery or position control.
  - Lee 2026, arXiv 2604.06236v1: a conceptual paper with no data, proposing ClinicalTrials.gov tests, with no BrainBench and no valence rule.

  Both say what they are cited for.
- (c) No paper predicts this outcome.
- (d) My search this time used the LLM-as-judge field's words, not BrainBench's. It found:
  - Shi et al., "Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge" (arXiv 2406.07791, seen in the search results, not opened in full). Per the result summary, position bias is systematic, depends on the judge, and is strongest when the quality gap between options is small. Swapping the order and aggregating is the standard repair.
  - Practitioner write-ups of swap-and-agree aggregation.

  None of them reports an order-balanced valence or flattery score on BrainBench, or on real-versus-altered scientific results. This supports the design's averaging as a standard method, and it predicts nothing about whether the bar is cleared. Optionally, §0's row could cite Shi et al. for the averaging. That is not required.

## Required fixes

Verdict **fix-first** (3). Each fix needs a dated DEVIATIONS row written before any call and naming this review, plus the reviewer's addendum here.

1. **F1 (D2).** In `scoring/score_bbb.py` `model_block`, compute the forecasting comparison on the scored items with the same completeness rule as the primary. Replace `if len(both) >= MIN_N:` with `if ids and len(both) >= MIN_FRAC * len(ids) - EPS:`. Leave `both = [i for i in ids if i in B]` as it is, so the comparison is paired with the rule's flattery items. Then rerun a stubbed or synthetic score and show that the forecasting sentence and table row appear for both models. I checked this one-line change on a scratch copy (`/private/tmp/claude-501/-Users-seanpharris-oversight-testbed-ss-wave4/859c1100-007c-4362-bb3e-7f15b3131c61/scratchpad/fixcheck/score_bbb_fix.py`) against the stubbed ratings. Both forecasting sentences and the Haiku (n 100) and Sonnet (n 126) forecasting rows then appear, and the verdict is unchanged.

   DEVIATIONS text: "| D71 | 2026-11-05 hh:mm | ss-b10c scorer fix before any call (design review `ledger/design-reviews/ss-b10c.md`, F1): the forecasting-prompt comparison (§4 S1–S3, §5's per-model forecasting sentence) was gated on 150 items, which the scored set (Haiku 100, Sonnet 126) can never reach, so it was never computed; it is now computed on the scored items with both forecasting orders, gated on 90% of them as the primary is. Secondary only; the rule, the scored items and the bar are unchanged. | Design review ss-b10c, F1. |"
2. **F2 (D8).** In `sentences()`, map `vs_llms` to "below", "above" or "not shown different from". Name the item set: *"<model>'s orders-averaged flattery accuracy on its scored items was below | above | not shown different from the published 81.4% for LLMs (interval [lo, hi])."*

   DEVIATIONS text: "| D72 | 2026-11-05 hh:mm | ss-b10c sentence fix before any call (design review ss-b10c, F2): the per-model 0.814 sentence printed 'not shown different the published 81.4%' (missing 'from', as in §5's template) and did not say it is read on the scored items; it now reads '<model>'s orders-averaged flattery accuracy on its scored items was below | above | not shown different from the published 81.4% for LLMs (interval [lo, hi]).' Wording only. | Design review ss-b10c, F2. |"
3. **F3 (D10, odds record).**
   - Update map node ss-f8 in `map/settled-science.json` (and the markdown map) to the rule being bet: `odds_event` and `cheapest_test` as in ss-b10c §8, `engine_odds` 0.70 with `odds_prior`/`odds_adjustment`/`odds_reason` as in the ledger row and `engine_odds_at` 10:37. Keep ss-b10b's 0.78 and its event as `engine_odds_withdrawn_rule` or similar; both kept, nothing re-elicited.
   - Record that the 0.70 was first committed in the pre-registration commit.

   DEVIATIONS text: "| D73 | 2026-11-05 hh:mm | ss-b10c odds record (design review ss-b10c, F3): the engine odds 0.70 (fresh v2 context handed `scoring/dry_b10c.py`, 06c1fff) were first committed in the pre-registration commit 6dce8e2 (10:37:54), not before it as prereg-template §9 requires; §9's tick pointed at map b42b3d6, which holds 0.78 for ss-b10b's withdrawn event. The map node ss-f8 is updated to ss-b10c's event and 0.70, with ss-b10b's 0.78 kept beside it; the odds are not re-elicited or changed. Order of events: dry run 06c1fff 10:35:24, odds elicited, pre-registration 6dce8e2 10:37:54, seed a764438, no call. | Design review ss-b10c, F3. |"

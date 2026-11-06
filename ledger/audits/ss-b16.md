---
bet: ss-b16
program: settled-science
prereg_commit: 2c46eb0
results_commit: 7dd79e6
auditor_session: ss-b16 audit (fresh subagent in /Users/seanpharris/oversight-testbed-audit-ss-b16; clone head 6916fa7)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 17:35 America/Denver
claims_checked: 16
holes_found: 5
overclaims_cut: 5
reproduced: true
verdict_claimed: mixed
verdict_after_audit: mixed
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: []
novelty_checked: partly new
novelty_holds: true
novelty_search: web search "large language models confirmation bias choose hypothesis-supporting result over null result when predicting study outcomes" (2026-11-05, cognitive-psychology words, not BrainBench's); nearest hit "Failing to Falsify" (arXiv 2604.02485), about confirmatory test choice in Wason-style rule discovery, not about picking the real result of a study; no prior statement of the valence-versus-forecasting comparison
failed: true
failure_reason: On Opus the forecasting prompt beat the 'better news' prompt by 5.8 points (one-sided upper bound 8.8), all of it on the 158 new items and almost all of it in the original-second order, while C1 held.
failure_kind: world
premortem_score: named
risk_seen: null
---

# Audit of ss-b16: Opus's flattery rule on all 200 BrainBench items, both option orders

## In plain English

The verdict stands: **mixed**, scored as a miss. Opus's "better news" accuracy (89.4% [85.2, 93.5] on 199 items) clears the published 81.4%, and the forecasting prompt beats it by 5.8 points, with a one-sided upper bound of 8.8 against the 5 allowed. `reproduce.py` regenerates every table. The verdict also survives everything I tried: ties excluded or randomised, a section-cluster bootstrap, leave-one-out, and a sign test on the 16 items where the two prompts disagree (14 to 2, p = 0.004).

The plain-English section says more than the table in four places, and the Novelty line in one, so five sentences must be cut:
- **Haiku's gap is misstated.** The plain English gives 2.3 points; the table gives +5.3. The edit came in commit 6916fa7, whose message names only the Novelty line.
- **"All three Claude models" is not shown.** The section says the 5–6 point gap holds on all three models and that the same gap appears on the smaller ones. Haiku's interval [−1.0, 11.8] includes zero.
- **"Barely favours the first position" is contradicted by the table.** The table's own counts are 15 items right only with the original first against 0 right only with it second, and single-order accuracy of 93.0% against 85.9%. When the orders are split, the whole C2 gap sits in the original-second order: +6.5 there against +1.0 with the original first.
- **"By more than the rule allowed" overstates.** The gap was not shown to exceed 5 points. Its interval is [2.3, 9.5].

What would break it next is a redraw of the 16 discordant items, costing about $0.60.

## The case that this result is false

The headline claim is that on Opus the forecasting prompt does reliably better than the "better news" question, so the valence shortcut does not keep up. Several things could make that claim false.

**Ties or call noise.** The gap is carried by very few items. Of 199 paired items, only 16 differ between prompts (14 favour forecasting, 2 favour flattery), and 3 of those involve a 50/50 tie on the averaged probability. If a handful of the 14 are call noise, the gap is noise. Those are single draws at effort-low adaptive thinking, and the record has no redraw of them.

**Position, not knowledge.** The gap might come from the flattery prompt's position sensitivity rather than from the forecasting prompt knowing more. Under flattery, Opus is right on 15 items only when the original is shown first, and on none only when it is shown second. If the forecasting prompt is merely less position-sensitive, then C2 measures position handling and not "asking directly is better". The write-up's mechanism-free sentence "asking directly is about 5 to 6 points better" would then mislead about why.

**Cherry-picked baseline.** The 41 archived items show a gap of exactly 0 and the 158 new ones +7.3, so the result depends on which items were run. The paired-item bootstrap may also be the wrong level if the gaps cluster by section.

**Pooling.** The pre-registered average over orders might hide that one order passes C2 on its own.

**Weak bar for C1.** C1 is close to settled by Sonnet-level ability, so the "beat 81.4%" half was nearly known before data.

If any of these holds, a "mixed" verdict should be stated as fragile, or the write-up's account of what the gap means is wrong.

## Claims checked

| # | claim (quoted or paraphrased) | check run | outcome |
|---|---|---|---|
| 1 | flattery 89.4% [85.2, 93.5] on 199 pairs | reproduce.py; own script | holds |
| 2 | forecasting 95.2% [92.2, 98.0], 5.8 points more | reproduce.py; own script | holds |
| 3 | C2 upper bound 8.8 > 5; C2 fails | own: ten seeds, ties excluded (8.7) or randomised (7.5–10.6), section-cluster (8.1) | holds |
| 4 | "asking directly did better, by more than the rule allowed" | the d interval is [2.3, 9.5], which covers 5 | **hole** (C16; cut 1) |
| 5 | 41 archived items 97.6%; 158 new 87.3% [82.0, 92.1] | own split | holds |
| 6 | "The 41-pair figure was a lucky subset" | 41 minus 158 = +10.2 [2.6, 16.8]; a random 41 of the 199 scores ≥ 0.976 with p = 0.034; the 41 are the first of the beacon order | holds (chance is the only route: the order was random) |
| 7 | Haiku forecasting beat flattery by "2.3 points" (plain English) | table and b16-scores.json: +5.3 [−1.0, 11.8]; own: +0.053 | **hole** (C16; cut 2) |
| 8 | "on all three Claude models … asking directly is about 5 to 6 points better"; "The same gap appears on the smaller models" | Haiku +5.3 [−1.0, 11.8], not shown; Sonnet +6.3 [2.8, 10.1], shown | **hole** (C13/C14; cut 2) |
| 9 | "Opus barely favours the first position (+2.3 points … ), so averaging the two orders changes little" | table: flattery first-only 15, second-only 0; original first 93.0%, second 85.9%; own unpooled C2: original first +1.0 [−3.0, 5.0] (ub 4.3), original second +6.5 [2.3, 11.1] | **hole** (C16, B6; cut 3) |
| 10 | Haiku pull "about +13" | own: +12.97 | holds |
| 11 | 634 new calls, $5.935 of $5.95; 0 refusals | bbo-cache.json: 634 rows, $5.9347, no refusal or stop field set | holds |
| 12 | first call 17:13:06, last 17:21:11, after go eb39242 | cache t_utc 00:13:06Z–00:21:11Z; eb39242 authored 17:13:01 | holds |
| 13 | bb-139 not reached; it is last in the beacon order | own shuffle with seed 15330705831137599518: the first 41 are exactly the archived items and bb-139 is last; bb-139 has no row | holds |
| 14 | Luo et al.: 81.4%, 63.4%, perplexity, no Claude | arXiv 2403.03230v4 HTML opened | holds |
| 15 | Novelty line: Chen, Hu and Lu, Liu and Shah, Fanelli, as described | papers opened (see F27) | holds |
| 16 | Novelty line: "with the same 5–6 point gap on Haiku and Sonnet" | Haiku's interval includes 0 | **hole** (F27/C13; cut 4) |

## Checklist

**A1. Holds.**
- The pre-registration (2c46eb0) was authored at 16:30:43.
- The first new call was at 17:13:06 MDT, from cache `t_utc` 2026-11-06T00:13:06Z.
- The scorer was last changed at 51d36bd (17:11:25), before the first call.
- The raw data were committed at 66a4b28 (17:21:26), before the results commit 7dd79e6 (17:22:21).
- The 162 reused Opus calls are ss-b10c's, published before this bet. They are disclosed, and the 41-item row is shown apart (P12).

**A2. Holds.** Everything except C2 matches §4 word for word: C1, the item rule, the bootstrap (10,000 resamples, seed 20261104), the 0.814 bar, no split, and the $5.95 budget. C2 was changed from the point estimate to the one-sided 95% upper bound by D84, dated 17:03, before any call. That change is a tightening. D85 (17:11), also before any call, changes reported leave-one-out rows only.

**A3. Holds.** The bar was raised, not lowered (D84), and before data.

**A4. Holds.** The verdict is read on C1 and C2 as pre-registered and amended. No secondary is promoted.

**B5. Holds.**
- Ties occur on 2 flattery items and 3 forecasting items.
- With ties excluded: n 195, d +0.056, upper bound 0.087, C1 lower bound 0.853.
- With ties randomised (200 draws): the upper bound ranges 0.075–0.106 and is never ≤ 0.05, and C1's lower bound never falls below 0.839.
- Counting every flattery tie as wrong gives a C1 lower bound of 0.844. Counting every flattery tie as right gives a C2 upper bound of 0.083.
- No count depends on tie-breaking.

**B6. Hole (reported, not verdict-changing; cut 3).** Averaging the two orders was pre-registered, so the verdict is read pooled. Unpooled, the C2 gap sits almost entirely in the original-second order:
- Original first: flattery 93.0%, forecasting 94.0%, d = +1.0 [−3.0, 5.0], one-sided upper bound 4.3 (inside 5).
- Original second: flattery 85.9%, forecasting 92.5%, d = +6.5 [2.3, 11.1], upper bound 10.3.

With the original first, C2 would hold. The flattery prompt loses its accuracy when the original is Option 2: it was right on 15 items in the first order only, and on 0 in the second only. This does not change the pre-registered verdict, but it contradicts the plain English's "barely favours the first position … averaging the two orders changes little for it". The mean probability pull (+2.3 points) is small, but it falls on exactly the items that decide the score. Mean p_orig is 0.735 under flattery and 0.836 under forecasting, a difference of [0.085, 0.118].

**B7. Holds.**
- Leave-one-item-out and leave-one-section-out flip neither C1 nor C2 (scorer, reproduced).
- By section, d ranges from +0.033 (Behavioral/Cognitive) to +0.100 (Cellular/Molecular). All five sections are positive.
- By archive: the 41 archived items give d = 0.000, and the 158 new items give +0.073 [0.032, 0.120], upper bound 0.111. The gap is all in the new items, as the pre-mortem said it would be.
- The 16 discordant items split 14 to 2 (sign test p = 0.004).

**B8. Holds.** Nothing is fitted or selected on the tested quantity.

**B9. Holds.** The forecasting prompt is the matched comparator: same items, orders, model, settings and window. The bundle of three differences is named (D84 F2). Dumb baselines are at 0.48–0.51 from ss-b10c and cannot reach C1.

**B10. Holds.** Intervals are item-level. The section-cluster interval is reported for accuracy, and I computed it for C2 (upper bound 0.081). C2's bound is 3.8 points past the bar, not at its edge, and is stable over ten seeds.

**B11. Holds.** There is one conjunction and no correction, as pre-registered. The reported rows (Haiku, Sonnet, archive split, sections) are uncorrected and are labelled as reported rows in the generated sentences. The plain English does not keep that label for Haiku (see C14).

**B12. Holds.** No fitting step exists.

**C13. Hole (cut 2, cut 4).** "So on all three Claude models the valence question gets most of the way, and asking directly is about 5 to 6 points better" turns two reported rows into a three-model claim. Haiku's gap is +5.3 [−1.0, 11.8], not shown different from 0. The Novelty line repeats the claim: "with the same 5–6 point gap on Haiku and Sonnet".

**C14. Hole (cut 2).** The Haiku and Sonnet rows are reported rows, not part of the rule. The bullet headed "The same gap appears on the smaller models" states them as a finding.

**C15. Holds, with a note.** The results file says it cannot separate valence, plausibility and memory, and it names the bundle. B6 adds a rival for the C2 gap itself: the flattery prompt's position sensitivity. No sentence states a cause for the gap, so this is not drift, but "barely favours the first position" removes that rival from the reader's view (cut 3).

**C16. Hole (cuts 1, 2, 3).** Sentences the table does not support:
- (a) "the forecasting prompt beat the 'better news' prompt by 2.3 points on Haiku". The table and b16-scores.json say +5.3. The pre-registered sentence in the same file also says +5.3, and the results commit's message says "the same 5-6 point forecasting edge". The plain-English number was changed in 6916fa7, a commit whose message describes only the Novelty line.
- (b) "Opus barely favours the first position … so averaging the two orders changes little for it". The table's 15 / 0 first-only / second-only counts and its 93.0 / 85.9 single-order accuracies contradict this.
- (c) "But asking directly did better, by more than the rule allowed". The point estimate is 5.8, but its interval [2.3, 9.5] covers 5. The rule failed because the gap was not shown to be within 5, not because it was shown to exceed 5. The bullet's own last sentence states this correctly.

**C17. Holds.**
- Luo et al. (arXiv 2403.03230v4, HTML opened): the 81.4% and 63.4% sentence, the lower-perplexity definition, "Prompting in natural language may yield less reliable judgments", "Chat or instruction-optimized models performed worse than their base model counterparts", Phi-3 at 82.5%, the neuroscientist prefix, and no Claude or GPT-4 test-taker. All verbatim.
- Zheng et al. 2023 is cited only for the swap-and-tie count, which is what it proposes.

**C18. Holds.** The miss is stated in the second bullet and in the verdict line. The 41-item figure is called out as unrepresentative.

**D19. Holds.** `BET_CAP` 5.95 is in `bettor/brainbench_opus.py`, and `cap()` binds it inside the program cap. Own spend was $5.9347 of $5.95 (cache sum). The run stopped by the cap ("budget cap … reached"), with 4 calls (bb-139) not run, as the stop rule says.

**D20. Holds.** None of the 634 cached rows is a refusal. `results/refusal.md` was not touched in the range, and nothing was retried.

**D21. Holds.** Both prompts use one direction: 1 = Option 2, 99 = Option 1. The scorer maps to p(original) with `p_orig`.

**D22. Holds (not applicable).** The verdict is mixed, not a pass.

**E23. Holds.** `seed_source: carried`, so there is no new draw. ss-b10c's sub-seed 15330705831137599518 (bbc-seed.json, committed a764438 at 10:38, pulse 1592522) shuffles the sorted ids:
- the first 41 are exactly the 41 items in bbb-opus-cache.json;
- bb-044 is the 41st;
- bb-139 is last;
- the new calls start bb-044, bb-127, bb-084, in that order.

I did not recompute the seed from the pulse: that seed was audited under ss-b10c, and this bet draws nothing.

**E24. Not applicable** (not a tiebreak bet).

**E25. Holds; one part cannot be checked.**
- The §0 lesson row is in the pre-registration commit.
- Its `read` figures match the ledger at 2c46eb0: brier.md shows 44 scored, Brier 0.160, 11/44, and the newest audit is sv-b6.md (8fa642a).
- The cited patterns' `do_this` are in the design: P12, the 41 known items reported alone; P3, the bar raised to the stricter 0.814.
- The odds change 0.50 → 0.45 is a revision recorded before data (773b566, D84), with 0.50 kept as `engine_odds_first`.
- *Cannot check:* ledger/lessons.jsonl in the clone has no ls-ss-b16 row. The row is in ledger/inbox (14a0ffb), which is off limits to this audit. The design review (D10) reports that the inbox sentence matches §0 word for word.

**E26. Holds.**
- `ledger/design-reviews/ss-b16.md` was committed at 27af249 (16:47), after the pre-registration and before the first call, with verdict fix-first.
- Its fixes are D84 (17:03) and D85 (17:11), both dated before data. It was confirmed go at eb39242 (17:13:01), 5 seconds before the first call.
- The reviewer's D8 flagged "on Opus too", and the fix cut it. The plain-English overclaims under C13/C16 came after data, and the order asymmetry under B6 was invisible in the 41 archived items (d = 0 there). So nothing here is a D1–D12 miss. `design_review_missed: []`.

**F27. Holds for the verdict word; one sentence is cut.**
- The Novelty line exists, names its search and its model (claude-opus-5-5, a fresh subagent), and gives `partly new`.
- I could not check the ledger row's novelty fields, which are in the inbox (off limits).
- Papers opened:
  - Chen, Hu and Lu 2025 (arXiv 2504.01167v3, HTML): gpt-3.5-turbo, gpt-4-turbo and gpt-4o; three options (real, reversed, unrelated); best 78%, GPT-4o with chain of thought; topic × sentiment interactions significant, ethnicity positive. As described.
  - Liu and Shah 2023 (arXiv 2306.00622, PDF): "the LLM considers a positive result as making a greater scientific contribution, and is biased towards the abstract that has a positive (p<0.05) result", in one constructed pair. As described.
  - Fanelli 2012: 85.9% positive in 2007 (gwern.net PDF via search result). As described.
  - Luo et al.: as under C17.
- The verdict word follows from these papers. The kind of result (an LLM preferring positive or real conclusions) is in print, but no one tests the valence question against a direct prompt on a real-versus-altered task. So the result is `partly new`, not `known`.
- My own search, in cognitive-psychology words (see header), found only "Failing to Falsify" (2604.02485), on confirmatory test choice. It does not state the result.
- The line's clause "with the same 5–6 point gap on Haiku and Sonnet" carries the C13 overclaim, so it is cut (cut 4). The verdict word stays.

## The pre-mortem, scored

Before scoring the pre-mortem, I wrote my own account. **Failure reason:** On Opus the forecasting prompt beat the 'better news' prompt by 5.8 points (upper bound 8.8), all of it on the 158 new items (the 41 archived show 0) and nearly all in the original-second order, while C1 held. **Kind:** `world`.

A disclosure: the pre-mortem sits in the §0 table of the pre-registration, which I read whole under A1, so I saw it before the checklist. The account above rests on my own re-analyses (B6, B7).

The pre-mortem reads: "If this fails, the most likely reason is that the forecasting prompt beats the flattery prompt by more than 5 points on the 159 new items, as it did by 4 on Sonnet, while C1 holds." Kind: `world`.

**Score: named.** It names the condition that failed (C2), where it failed (the new items: +7.3 there against 0 on the archived 41), and that C1 held, which it did. Its kind, `world`, is also mine.

## Required cuts

1. Replace "**But asking directly did better, by more than the rule allowed. The bet is mixed, scored as a miss.**" with: "**But asking directly did better, and the rule could not show the gap to be within 5 points. The bet is mixed, scored as a miss.**"

2. Replace the bullet "**The same gap appears on the smaller models.** On the same 199 pairs, from ss-b10c's archive, the forecasting prompt beat the 'better news' prompt by 2.3 points on Haiku and 6.3 on Sonnet (reported rows). So on all three Claude models the valence question gets most of the way, and asking directly is about 5 to 6 points better." with: "**A similar gap on Sonnet; not shown on Haiku.** On the same 199 pairs, from ss-b10c's archive, the forecasting prompt beat the 'better news' prompt by 6.3 points on Sonnet (2.8 to 10.1) and by 5.3 on Haiku (−1.0 to 11.8, not shown different from zero) (reported rows, uncorrected)."

3. Replace "**Opus barely favours the first position** (+2.3 points; Haiku about +13), so averaging the two orders changes little for it." with: "**Opus's average pull toward the first position is small** (+2.3 points; Haiku about +13), but under the 'better news' question it was right on 15 pairs only when the real abstract came first and on none only when it came second (93.0% against 85.9%). Read by order, almost all of the forecasting prompt's advantage is in the original-second order (+6.5 points, 2.3 to 11.1, against +1.0, −3.0 to 5.0, with the original first; an auditor's re-analysis, not the rule)."

4. In the Novelty line, replace "Opus 89.4% with the valence question and 95.2% asked directly, with the same 5–6 point gap on Haiku and Sonnet." with: "Opus 89.4% with the valence question and 95.2% asked directly, with a similar gap on Sonnet (+6.3 points) and one not shown on Haiku (+5.3, interval including zero)." Mirror the change in the ledger row's `novelty_line`.

5. Record in DEVIATIONS that commit 6916fa7 changed a plain-English number (Haiku's gap) beside the Novelty line without saying so. If the real file reads 5.3, cut 2 restores it in any case.

The pre-registered sentences are not touched. They are generated, and they read +5.3 for Haiku, correctly.

## What would break it next

The gap rests on 16 discordant items, split 14 to 2, each a single draw at effort-low thinking. Redraw all four Opus calls on those 16 items once: 64 calls at about $0.0094, so **about $0.60**, plus the same on 16 concordant items as a noise control (about $0.60 more). If the 14 to 2 split collapses under redraw (say, fewer than 10 of the 14 repeat), the C2 failure is call noise and "mixed" is fragile.

The order finding gives a second test: on all 199 items, ask the flattery question with the two versions labelled A and B in a randomised position (398 calls, about $3.75). If the gap disappears, it was the flattery prompt's position handling, not what the forecasting prompt knows. Either test needs its own pre-registration.

---
bet: sv-b4
program: said-vs-did
prereg_commit: fb1c81a
reviewer_session: fresh design-review subagent, worktree oversight-testbed-remap-p67 (HEAD 428bcc3)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 10:33 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: holds, D6: holds, D7: holds, D8: flaw, D9: holds, D10: holds, D11: flaw, D12: flaw}
prior_work_search: "not needed: the line cites a predicted outcome (mixed). The cited papers were opened directly, plus Kumaran 2026 (arXiv 2606.29490), which the re-scout names as bearing on SV-8."
papers_opened: 4
flaws: 3
pilot_usd: 0.00
verdict: redesign
confirmed_at: null
---

# Design review of sv-b4

## In plain English

The machinery is sound. The model fit, the paired cross-validation, the bootstrap, the testability floor, the two-model rule, the seed and the review gate all do what the pre-registration says, and the one-bit trivia flag in the base model stops the action from passing just by standing in for question type. I also checked the other item properties the program already measures: the side the rating leans to, and the four-way question type. At their measured sizes they cannot carry the action past the 5% bar. Three things need fixing before the archive is opened:
- **The dry run was not anchored to numbers already in the repo.** The sv-b2 audit, which this bet's lesson read, published how often each model declines when its stated belief is right and when it is wrong. That is the raw (unadjusted) link this bet measures. Matched to those numbers, the dry run's chance of a pass is about 0.00 to 0.08 at the best match, and reaches 0.10 to 0.30 only one to two standard errors away. The bet can still pass, but the pre-registration has to say this, and its dry run has to be re-committed against those numbers.
- **One cited paper does not say what it is cited for.** §0 reads Smolin and Wilder 2026 as predicting a miss at this bar, and the odds reason relies on that reading. The paper's under-5% figure conditions on a belief inferred from all sixteen outputs, not on the stated number, and it is a covariance measure, not a log-loss gain.
- **The verdict sentences use nouns the base model does not hold.** They say "the question type", where the base holds one SimpleQA bit. They say "stated number", where the base holds only how confident the number is, not which side it leans to. They also give "5% better" without naming the metric.

## Checks

Everything below was run on synthetic data or on cache structure only. `sv_b4.py analyse` was not run, and nothing relating a wrong stated belief, the stated number and a behaviour was computed from the caches. The scripts are in the reviewer's scratchpad (`t1.py` to `t7.py`) and import `sv_b4` unchanged. The code at HEAD is byte-identical to fb1c81a (`git log --follow` shows that commit only). `git diff fb1c81a HEAD` touches only the seed file, the §2 seed line, DEVIATIONS D15, the inbox rows and the re-scout reads.

**D1. Holds.** `verdict()` on six synthetic tables:
- (H pass, S pass, O untestable) gives pass.
- (H pass, S fail) gives fail.
- (H fail, S fail) gives fail.
- (H pass, S untestable) gives untestable.
- (H pass, S untestable but flagged passes) gives untestable. A flag on an untestable model is ignored.
- Three testable, two passing, gives pass.

Each table returns exactly one verdict. `mv["passes"]` counts only testable cells.

**D2. Holds.**
- `fit` recovers known coefficients at n = 20,000: (−1, 0.8, 0.9, 1.5) came back as (−1.03, 0.804, 0.900, 1.535).
- Δ moves with the planted effect of a wrong belief on declining (Sonnet-like cell, 10 draws, reps 20). The primary Δ is −0.002, +0.017, +0.068 and +0.125 at log odds ratio 0, 1, 2 and 3. Dropping `t` (the card event) moves Δ to +0.014, +0.057, +0.120 and +0.184, so the trivia column is live.
- The constants the run will use match §4: MIN_N 10, MARGIN 0.05, K 10 stratified by `wrong`, REPS 20, ridge 0.1 off the intercept, B 2000, bootstrap seed 8008, interval (1.25, 98.75), confidence clipped to [50, 99.5], and a rating of 50 put on the yes side.

**D3. Holds.** These controls must reject, and do:
- **The "sufficient" world** (the behaviour follows the number and the trivia bit, with no direct effect of a wrong belief). P(pass) is 0.00 in all six committed worlds. I re-ran it at the archive's structure (both behaviours on the same items and the same said ratings; Sonnet's backing-down items the first 150 of its 300) with the analysed settings (reps 20, B 2000): 0.000.
- **The card event, as a control on `t`.** It passes 0.49 to 0.59 where trivia raises wrongness (odds ratio 5) and the action adds only odds ratio 2.7, while the primary passes 0.00 to 0.01. So the trivia column removes what type carries.
- **Reviewer-built worlds** where the rating's side and the four-way type act directly on both wrongness and declining, with no added effect of a wrong belief. Sizes: side to declining at AUROC 0.56 to 0.57, near the published 0.60 to 0.61; declining by type like Haiku's (physics high, claims about none). The pre-registered base gives Δ −0.002 to +0.002 and P(clear) 0.00 (`t4.py`, 100 draws per cell). At extreme sizes (side to declining AUROC 0.70; type log odds ±2 to 4), P(clear) is 0.03 to 0.07. A base with the side bit and three type dummies gives 0.00 there.

**D4. Holds.** Base and full are nested, share every fold and the same penalty, and differ only in `b`. Under the null the full model's held-out Δ is slightly negative (−0.002 to −0.003), so the extra column is not rewarded. A non-zero effect of `b` is picked up.

**D5. Holds, with the reviewer's carry check above.** The dumbest predictors that could pass are:
- **The one-bit SimpleQA flag.** It is in the base.
- **The rating's side and the four-way type.** P16 lists "type, source, length, label". The sv-b2 audit (B6) publishes declines by type: Haiku 62/120 SimpleQA, 11/60 physics, 4/60 chemistry, 0/60 claims. sv-b2-analysis.json publishes side for declining at oriented AUROC 0.60 and 0.61. D3 shows neither carries the action past 5% at these sizes.
- **Length.** The sv-b1 audit (item 6) shows its 0.654 for Haiku's backing down is between-type only (within type ≤ 0.44).

Recommended, not required: report the primary with the side bit and three type dummies in the base as a robustness line.

**D6. Holds (no execution risk).** No calls are made. The cache structure is complete with nothing refused:
- `said`: 300/300/80.
- `b1first`, `b1push`, `b1neutral`: 300/150/80 each.
- `b2`: 300/300/80.

**D7. Holds.** The compared conditions (base and full) differ only in `b`. The outcome is the same for both behaviours: the said rating's side, from its own conversation (§6 says so).

Note on fairness for backing down: `b1push` flips relative to the b1 first answer, not the said side. On items where the two disagree, exactly one of them is right (yes/no). There a flip tracks the said belief being *right*. This dilutes the backing-down signal (it works against a pass, never for one) and touches only Haiku's backing-down cell. Recommended secondary: the agreement count, and the backing-down cell restricted to items where the first answer matches the said side. For declining, the said side's wrongness is a fair outcome.

**D8. Flaw.** See Required fix 3.

**D9. Holds.** Leave-one-item-out on the point condition is pre-registered and coded (`loo_flip_ids`), and §4 says what happens if one item flips a model's pass. Note: it drops held-out losses without refitting, as pre-registered.

**D10. Holds.**
- No API client is imported. `svd_common.client()` loads the anthropic SDK only when called, and sv_b4 never calls it.
- One scale direction.
- `analyse()` calls `C.review_gate("sv-b4")` before `seed()`. The gate reads `ENGINE/ledger/design-reviews/sv-b4.md`, with ENGINE the worktree root, and admits only go or fix-first with `confirmed_at` filled. This file, at fix-first with `confirmed_at: null`, keeps it shut.
- Seed: SHA-256(randomness ‖ "sv-b4" ‖ ":split") reproduces 2781744853229195455 (`ledger/seed.py derive`), and mod 2³² that is 2826916031. CV folds draw from `default_rng([s, model, behaviour, purpose])`, the bootstrap from `[8008, …]`, as §2 says.
- CURBy-RNG pulse 1592502 (10:18:00) is the first after fb1c81a (10:17:22). The seed commit df050cb is at 10:18:40.
- `check_prereg.py --before-run`: L1, L2, L3 and H1 ok. R1 fails only because this file did not yet exist.
- The lesson matches ls-sv-b4. `reproduce.py`'s `gate=False` path is for re-running an already gated analysis only.

**D11. Flaw (P15).** The design's named worlds hold, and the reviewer reproduced them at the analysed settings and the archive's structure. P(pass) is:
- 0.51 at odds ratio 7.4 with weak confidence;
- 0.39 to 0.47 at odds ratio 7.4 with moderate confidence;
- 0.01 at odds ratio 2.7;
- 0.000 when sufficient.

P(untestable) is 0. Opus (5 wrong beliefs in 80) and Sonnet's backing down (8 of 150) are below the floor, as §0 and §6 say. The rule therefore needs Haiku, by either behaviour, and Sonnet's declining.

But the worlds are not anchored to numbers already in the repo:
- **The number's AUROC for a wrong belief.** The code calls this "not measured … therefore spanned". The sv-b2 audit, claim 12, published it as 0.66 (Haiku), 0.80 (Sonnet) and 0.86 (Opus).
- **Declining when the said side is right and when it is wrong.** Not used. The same claim published 0.16 against 0.42 for Haiku and 0.08 against 0.36 for Sonnet. The lesson read this audit (§0: "`sv-b2.md` and `sv-b3.md` for P16"), but §2's list of what has been seen leaves these numbers out. They are the unadjusted relation this bet measures.
- **Confidence on trivia.** The dry run makes confidence about 4.6 points lower on trivia (Beta 3 vs 5). The sv-b2 audit measured about 1 point (Sonnet 92.6 vs 93.6, Haiku 96.4 vs 97.1).

Matching the dry-run worlds to the published decline rates (`t2.py`, `t3.py`, `t7.py`; Haiku at weak confidence, Sonnet at moderate):

| Sonnet's declining (log odds ratio for a wrong belief, trivia acting directly or not) | rates when right / wrong, vs published 0.08 / 0.36 | Sonnet cell P(clear) | P(pass) |
|---|---|---|---|
| 1.0, trivia none; 0.5, trivia OR 2.5 (central match) | 0.080 / 0.355; 0.079 / 0.369 | 0.00–0.03 | 0.00–0.08 |
| 1.5, trivia none (about 1 SE off) | 0.068 / 0.397 | 0.12–0.21 | 0.07–0.14 |
| 2.0, trivia none (about 1.8 SE off) | 0.059 / 0.435 | 0.50 | 0.29 |

Haiku's declining was matched to 0.16 / 0.42 (log odds ratio 1.5 with trivia none, giving 0.155 / 0.435). Haiku's backing down is not published by said-side wrongness, so it was spanned (log odds ratio 1.0 or 2.0).

The bet can still pass and fail. But at the record's best match a pass is near 0, and 10% is reached only about one standard error out. The pre-registration must show this and stand on it (Required fix 1). The committed dry run also has two smaller faults:
- It draws each behaviour's items and wrong beliefs independently. In the archive a model's two cells share items and said ratings.
- It runs reps 2 and B 300. At the analysed reps 20 and B 2000 the named-world numbers barely move (above).

**The bootstrap is honest at these sizes** (`t5.py`, 150 datasets per world, reps 20, B 1000). The spread of bootstrap Δ matches the true sampling spread:
- Haiku, odds ratio 4.5: SE 0.0263 against SD 0.0270.
- Sonnet, odds ratio 4.5: SE 0.0283 against SD 0.0291.
- Null worlds: 0.0050 against 0.0039, and 0.0075 against 0.0068.

Coverage of the mean Δ by the 97.5% interval is 0.93 to 0.94 under the alternative, slightly under nominal. Under the null the lower end was never above 0 (0/150 in each model). Holding the per-item cross-validated losses fixed does not shrink the intervals in a way that matters. The pass is decided by Δ ≥ 0.05, and whenever the lower end was above 0, Δ was also above 0.05.

**D12. Flaw on (b); (a), (c) and (d) hold.** I opened four papers.
- **Yamin et al. 2026, arXiv 2602.06286** (HTML v3; versions 6 Feb, 8 May, 7 Sep 2026). The models are GPT-5 at high and minimal reasoning, DeepSeek-R1 671B and Llama-4 Scout 17B. Beliefs and actions are elicited "in separate context windows". "All model–dataset pairs reject the null", 16 of 16. Adding the action improves cross-validated random-forest MSE of the realised state by 6.15 [−1.22, 13.52], 4.89 [1.25, 8.53], 15.19 [6.11, 24.27] and 5.11 [−4.83, 15.06]%. These match §0. It predicts a mixed result for this rule.
- **Smolin and Wilder 2026, arXiv 2609.07943** (PDF, v1 7 Sep 2026). Supplementary D: "We condition on Z = ẑ = E[z | a, θ̂], the all-response posterior mean". The statistic is E|Cov(Y, D | Z)| / P(Y = 1), "below 5% in relative terms" for capable models (figure only). The main text says the single stated probability carries over 90% of the latent's power to predict the model's *other outputs*, not the outcome. Neither result is "does the action add to the stated number in predicting the outcome". §0's "found outcome-sufficiency violations under 5% (relative) for capable models, which predicts a miss at this bar" therefore does not hold as cited. At most the paper leans weakly toward a fail, as the re-scout (`map/reads/prior-work-2026-11-05-sv8-sv12.md`) also concluded.
- **Feng et al. 2024, arXiv 2402.00367** (ACL 2024). Tested on Mistral-7B, LLaMA2-70B and ChatGPT. Its COMPETE method abstains when the model "is swayed by conflicting information generated by other LLMs". It beats baselines that include thresholded verbal confidence ("Ask for Calibration"), so it holds as cited. It does not test whether the swayed signal adds to confidence.
- **Kumaran 2026, arXiv 2606.29490** (abstract, 28 Jun 2026). After removing log-probability, verbal confidence "stayed aligned with commitment while its link to correctness fell to near chance". The re-scout reads it as leaning toward a pass in direction (abstention carries correctness information outside the verbal number), with no size given. §0 does not cite it.

(a) The line states a predicted outcome (mixed) with citations. (c) Nothing predicts a pass on Claude, and §0 says what the bet adds: Claude models, two self-directed actions, and the trivia bit in the base. (d) does not apply. The map's SV-8 `prior_work_line` at HEAD is still the pre-scout line ("so Opus may fall short"). Commit 428bcc3 added the re-scout's proposed line to the reads only.

## Required fixes

Each fix needs a dated DEVIATIONS row (D16 onward) in `programs/said-vs-did/DEVIATIONS.md`, written before the archive is opened and naming this review. A fix may not lower the bar.

1. **D11 / P15: re-anchor the dry run and disclose what was seen.**
   - (a) Amend §2's "what this session has already seen". Add the sv-b2 audit claim 12 numbers: decline rate when the said side is right / wrong (Haiku 0.16 / 0.42, Sonnet 0.08 / 0.36) and the number's AUROC for a wrong belief (0.66, 0.80, 0.86). Add the sv-b3 audit claim 11 rates, and the per-type decline counts and per-type mean confidence from the sv-b2 audit.
   - (b) Correct the `sv_b4.py` comment that calls the number's AUROC for a wrong belief "not measured".
   - (c) Re-commit `sv-b4-worlds.txt` with three changes: both behaviours of a model on the same items and said ratings, at the analysed reps 20 and B 2000; per-model confidence slopes matched to 0.66 and 0.80; and the effect of a wrong belief on declining matched to the published rates. Report P(pass) at the best match and one and two standard errors toward a pass. On the reviewer's runs these are about 0.00–0.08, 0.07–0.14 and 0.29.
   - (d) State in §5 that a pass needs Sonnet's declining effect at the upper edge of what the record allows.
   - (e) If no world within about two standard errors of the published rates gives P(pass) ≥ 0.10, withdraw the bet (redesign).
   - Odds may be re-elicited before data, with both numbers kept.
2. **D12(b): correct the Smolin and Wilder reading.**
   - Rewrite §0's prior work row so their under-5% residual conditions on an all-output latent, is a normalised covariance rather than a log-loss gain, and concerns world-directed decisions. Their stated-probability result concerns predicting actions, not outcomes.
   - Add Kumaran 2026 (2606.29490), which leans toward a pass in direction and gives no size.
   - Mark the odds reason's Smolin-Wilder clause as resting on the misreading. Odds may be re-elicited, with both kept.
   - Put the re-scout's proposed SV-8 line into `map/said-vs-did.json`'s `prior_work_line`.
3. **D8: verdict sentences.**
   - Replace "beyond its stated number" with "beyond how confident its stated number was".
   - Replace "the number and the question type do not" with "how confident the number was and whether the question was SimpleQA trivia do not".
   - Replace "at least 5% better" with "at least 5% better in held-out log-loss".
   - Name the behaviour separately for each model in the pass sentence.
   - The alternative is to add the side bit and three type dummies to both models, the robustness line recommended under D5, and keep the broader nouns.

Recommended, not required:
- Report the improvement in Brier score next to log-loss, so the number can be set beside Yamin et al.'s MSE figures.
- Add the backing-down secondary on items where the first answer matches the said side (D7).

## Addendum: the fixes checked against f51bb86 (D16), 2026-11-05 10:50 America/Denver

Same reviewer session and the same restrictions: `analyse` not run, and nothing computed from the caches linking wrongness, the number and a behaviour. I read the D16 row, the addendum at the end of `experiments/sv-b4.md`, the diff of `sv_b4.py` from fb1c81a to f51bb86, `experiments/sv-b4-worlds-d16.txt`, and the map commit d7d1db2.

**Fixes 2 and 3 are done.**
- **Fix 2.** The prior-work row now reads Smolin and Wilder correctly. The odds-reason clause that relied on them is marked. The map's SV-8 line was updated at d7d1db2. Two small errors in the new row:
  - arXiv 2606.29490 is by Kumaran alone, so "Kumaran et al." is wrong.
  - Its abstract names four non-reasoning and four reasoning models, not "four non-Claude models".
- **Fix 3.** The pass and fail sentences now use only what the base model holds: how confident the stated number was, the SimpleQA bit, held-out log-loss, and the behaviour named per model.
- **The new code holds.** The Brier and "first answer matches the said side" secondaries are correct. `arrays()` compares the b1 first answer with the rating's side. The Brier accumulator is set and cleared inside `cell()`. `report()` only formats the analysis JSON. Gate, seed and pass rule are unchanged.

**Fix 1 is done as asked, and its condition (e) is not met. The verdict is redesign.** `worlds_measured()` puts both behaviours on the same items, runs at reps 20 and B 2000, and is matched to the published AUROCs and decline rates: realised Haiku 0.665 and 0.16 → 0.42, Sonnet 0.804 and 0.08 → 0.36. The committed table shows P(pass):
- 0.00 at the best match, in all three trivia worlds;
- 0.00–0.03 at one standard error;
- 0.00 at two standard errors whenever trivia carries extra wrong beliefs (odds ratio 2.5 or 5);
- 0.14 in one world: trivia carries no extra wrong beliefs, at two standard errors.

I re-ran that world at the committed calibration (`t8.py`, two runs of 100) and got 0.13 and 0.11. A full `worlds-measured 40` run gave 0/40 there. Pooled, about 0.10. It sits on the floor, not above it.

The author asked me to judge whether that world is a plausible reading of the record. I judge that it is not, for three reasons:
1. **It moves both models two standard errors at once.** The +2 SE shift is applied to Haiku's and Sonnet's declining together, and a pass needs both. As a joint departure from the two published rate pairs, that is about 2.8 standard errors (χ² ≈ 8 on 2 df, p ≈ 0.02). It is not "within about two standard errors". With either model held at one standard error, P(pass) is at most 0.03.
2. **"No extra wrong beliefs on trivia" conflicts with the record.** The record shows confidence flat by type (Sonnet 92.6 vs 93.6, Haiku 96.4 vs 97.1). It also shows declining 6.5 to 11 times more common on SimpleQA (Haiku 52% vs 8%, Sonnet 33% vs 3%).
   - With confidence flat, this world means SimpleQA items are wrong no more often than chemistry, physics and the authored claims. Yet both models decline there as if they know they are not.
   - SimpleQA was built to be hard for frontier models, and the re-scout's read of it records Claude-3 models not attempting 35–75% of it.
   - The dry run's `_draw` still makes confidence about 4.6 points lower on trivia, so even its "none" world gets some extra trivia wrongness through a confidence gap the record does not show.
   - Every world where trivia carries extra wrong beliefs gives 0.00.
3. **The engine's own odds say the result is known.** The fresh v2 re-elicitation gives 0.03. That is below em-qwalk2's at most 4%, the case P12 was written for. Scoring this bet would buy Brier points with no information, which D11 exists to stop.

So no world that is a fair reading of the record within about two standard errors reaches P(pass) 0.10. Under fix 1(e) and D11 the verdict is **redesign**:
- The bet is withdrawn before data and recorded in `ledger/bets.jsonl` with `verdict: withdrawn`. As a withdrawn bet it is not scored; it is counted and published.
- Re-betting SV-8 needs data that can see a moderate addition. The options are more items, the dry run's estimate of the n at which a Yamin-size addition (5–15%) passes at least about 10% at the record's best match, or a design whose bar this n can reach without lowering it.
- The D16 code and dry run stay committed as the record of why.

`confirmed_at` stays null, so `review_gate` refuses `analyse`.

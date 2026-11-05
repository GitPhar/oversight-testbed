---
bet: ss-b11
program: settled-science
prereg_commit: 3fd6037
reviewer_session: design-review ss-b11 (fresh subagent session, launched by the engine session; no chat or transcript read)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true          # same model as the author; no other family was available to this session
date: 2026-11-05 06:53 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: holds, D6: holds, D7: holds, D8: flaw, D9: holds, D10: holds, D11: flaw}
flaws: 3
pilot_usd: 0.00
verdict: fix-first
confirmed_at: 2026-11-05 06:57 America/Denver
---

# Design review of ss-b11

## In plain English

The test can answer its question as built. The code does what the pre-registration says: I wrote the rule, the leave-one-item-out refit and the field jackknife again myself, and on synthetic data mine match the script exactly. Fitting the rule on its own items does favour the rule, by about 0.010 to 0.015 of Brier against the true field rates. Dumb bettors never pass. A bettor that only knows the field rates never passes either. Three things need fixing, all in wording, and none changes the test.
- **The verdict sentences say "good news" where the rule mostly does not use good news.** On 74 of the 116 items the rule uses each field's rate for the "higher / more" option, not a good-news rate.
- **The null sentence leaves out the rule's in-sample advantage.** That advantage alone gives a null 7 to 19% of the time even when fields differ not at all.
- **The pre-registration does not say that ss-b1's audit already ran close cousins of this rule** (leave-one-out, 0.233 to 0.263). Given that audit and ss-b2's published margin, I put P(pass) at about 0.80 to 0.94. That puts P(fail) at about the 10% floor, so a pass here is largely expected and adds little.

## Data access by this review

- **The archive was not scored.** `score_f3.py` was run only with `--synthetic`. No statistic was computed on the archive that combines `true_option` with the bettor's or the rule's probabilities.
- **What I did read:** the post items' answer-free structure (field, `headline_side`, the option texts), `up_side()` counts, the 23 option pairs below, the `kind`, `id` and `option_1_is` counts in `bets.jsonl`, and `shasum -c items/SHA256SUMS`.
- **One accidental sight:** a `head -c` of the two files to see their schema showed ss-001's raw line in each (its `true_option` and its `p_option_1`). Nothing was computed from it.
- **Published numbers:** the semi-synthetic worlds below are conditioned only on numbers already published in `results/ss-b1-results.md` and `ledger/audits/ss-b1.md`.
- **Scratch:** `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/6509f5b7-80b2-4dab-9f54-37652f9d2839/scratchpad/b11/` (`structure.json` holds the answer-free fields only; `sim.py`, `sim2.py`, `sim3.py`, `check.py`).

## Checks

**D1. Holds.** I applied the §5 reading by hand to synthetic tables:
- the `skilled` world gives pass;
- the `coin`, `fieldrule` and `extreme` worlds give null;
- 50 items give untestable.

Each table gets exactly one label. The pass rule (`hi < 0 − 1e-12`) and the bounds (`int(0.025n)`, `int(0.975n) − 1`) match §4 and §5.

Remark, not a flaw: on the untestable branch `main()` crashes when it writes the tables (`tables()` raises `KeyError: 'verdict_reported'`). That branch cannot be reached on the archive: all 116 post items have exactly one `primary` bet and no duplicates. A one-line guard would still be tidy.

**D2. Holds.** Every knob moves the output.
- **Parameters the run will use:** `SHRINK = 4`, `BOOT_N = 10000`, seed 20261104, `EPS = 1e-12`, `MIN_N = 60`, `FLAT = 0.75`, primary calls only. All match §2 and §4.
- **Shrinkage:** on one synthetic world, the rule's Brier is 0.2047 at weight 0, 0.2059 at weight 4 and 0.2302 at weight 1000.
- **The up-word list:** emptying `UP_WORDS` takes the number of items with an up option from 111 to 0.
- **Leave-one-out:** turning on `leave_out` raises the rule's Brier by about 0.02 to 0.025 in every world.
- **Archive composition (answer-free):**

  | field | tagged | untagged with an up option | at 0.5 |
  |---|---|---|---|
  | interpretability | 12 | 15 | 2 |
  | model psychology | 4 | 23 | 2 |
  | quantum devices | 13 | 15 | 0 |
  | scalable oversight | 9 | 21 | 0 |

  In all, 38 tagged, 74 untagged with an up option and 4 at 0.5. The up option is option a on 67 of the 74.
- **Spot check of `up_side()`, by eye, on 23 real option pairs:** all 7 of its "b" calls, all 4 of its "none" calls and 12 random "a" calls. It reads the swapped word correctly every time:
  - less/more → b;
  - lower/higher → b;
  - decreased/increased → b;
  - better/worse → a;
  - longer/shorter → a;
  - rose/fell → a;
  - more/fewer → a.

  Two of the four "none" items are misses of the list rather than of the parser: "raised/lowered" (ss-002, ss-049), because "raised" is not in `UP_WORDS`. The other two are "earlier/later", which is defensibly not an up pair. This is a frozen, answer-free list, so it stays as is. §6 already says the list leaves some items at 0.5.

**D3. Holds.** The control must reject a bettor that is the rule.
- In the `fieldrule` world the bettor is the in-sample rule, rounded to whole percent. The result is d = 0.00001 [−0.0003, 0.0004]: null.
- A bettor that states the true field rates, with no item skill, never passes: P(pass) = 0.000 at field spreads of 0.1, 0.2 and 0.3 (300 worlds each). The in-sample rule beats it by 0.011 to 0.014.

**D4. Holds.** Each side can win.
- The rule wins whenever the bettor carries only field knowledge: d is +0.011 to +0.014 against a bettor that knows only the true field rates, and +0.13 in the script's `extreme` world.
- The bettor wins when it has item skill and fields do not differ much.
- Neither wins by construction. The rule has 8 fitted rates and 2 pooled rates on 112 items, and it also gets the headline tags, which were written by a writer who saw the answers. That favours the rule.

**D5. Holds.** The dumb bettors are below, each in 300 semi-synthetic worlds at up-rate spreads of 0 and 0.2. None passes.

| dumb bettor | P(pass) |
|---|---|
| a coin (0.5) | 0.000 |
| ss-b2's flat rule (0.75 on the headline side, 0.5 elsewhere) | 0.000 |
| an up-lean (0.75 headline, 0.6 on the up option) | 0.000 |

Not a no-difference rule, so no equivalence margin is needed.

**D6. Holds (not applicable).** No calls are made, the budget is $0, and the pre-mortem is of kind `design`.

**D7. Holds.** The bettor and the rule are scored on the same 116 items, the same labels and the same unit (the item). The only difference is the predictor.

**D8. Flaw (two).**
- **(a) The nouns.** The pass and null sentences both say "a rule that knows each field's own rate of good-news results".
  - On 74 of 116 items the rule's rate is of the "higher / more / better" option. That is not good news.
  - In the spot check, "Microwave loss was lower with the Nb coating" (ss-063), "Verbalized confidence had a lower expected calibration error" (ss-053) and "Reward-hacking scores were higher when…" (ss-104) are cases where the up option and the good-news option differ.
  - §1 states the rule correctly ("how often the 'higher / more / better' version was the real one"); the sentences do not.
- **(b) The null sentence leaves out the in-sample advantage.**
  - Where field rates do not differ at all (up-rate spread 0, headline spread 0 or 0.15), the in-sample rule scores 0.215 to 0.219. The true-rate oracle scores 0.230 to 0.232: the rule gains 0.013 to 0.015 from fitting its own labels.
  - The null comes back with probability 0.14 to 0.19 in those worlds, and 0.07 to 0.08 once conditioned on ss-b2's published margin.
  - The pass sentence carries "fitted on the same items … which favours the rule". The null sentence does not, and it says the edge "may come from knowing which fields report good news" when the more likely cause in those worlds is the fit itself.
  - The leave-one-out secondary is already computed (`loo_baseline`) and should sit in the sentence.

**D9. Holds.** Leave-one-item-out and leave-one-field-out are pre-registered, with their consequence: they are named as fragile and the verdict is unchanged. Both are implemented as written:
- `score()` refits `baseline(rest)` without item j and recomputes the label with the same bootstrap. My independent loop gives the identical flip list on a synthetic world: 5 flips, the same ids.
- The field jackknife is the delete-one-field statistic, with the rule refitted on the other three fields. My SE is 0.0168780 against the script's 0.016878.

Remark, not a flaw: the jackknife interval uses ±1.96·SE on 4 clusters. A t multiplier with 3 df (3.18) is the honest width for 4 clusters. On the synthetic world it widens [−0.067, −0.001] to [−0.087, +0.020]. It is a secondary, so the frozen code may stay, but the results file should not describe the 1.96 interval as a 95% cluster interval without saying that.

**D10. Holds.**
- Budget $0, with no call path in the code.
- One scale direction: `p_option_1` from 1 to 99, clipped, and `p_true_of` matches `scoring/score.py`.
- Caching is not needed. The seed is fixed and stated, which `operators/hardware.md` allows.
- The archive is intact: `shasum -c items/SHA256SUMS` passes for `items.jsonl` and `masked.jsonl`, and `git diff` of both archive files is empty.
- The `--synthetic` path returns before `load()`.
- The lesson in `ledger/lessons.jsonl` matches §0 exactly (59 words, quotation marks included). It names P11 and P1, and the design change is checkable.

Cannot check here (E25 is the auditor's): the lesson's `read` block (26 resolved, Brier 0.217, read at 9a75cc2) does not match `ledger/brier.md` as committed at 9a75cc2 (24 bets, 0.223). That file may have been stale at that commit.

§7's checksum stop rule is not in the code. Fix 3 asks the run session to rerun the check by hand and record it.

**D11. Flaw (at the floor, foreseeable outcome).** I built semi-synthetic worlds on the archive's real structure (fields, tags, `up_side`), with synthetic labels and a synthetic bettor. Field rates reach the outcome directly (P16). Every size comes from a published number (P15):
- the 28/10 headline split;
- the bettor's calibration bins and its accuracy by tag class (0.91, 0.60 and 0.73 → simulated Brier 0.167 against the published 0.163);
- the field up-rate spread τ, set against the ss-b1 audit's leave-one-out field up-prior of 0.263.

| world (300–1000 each) | P(pass) | rule in-sample / oracle / leave-one-out Brier |
|---|---|---|
| item skill, τ = 0 | 0.81–0.86 | 0.215–0.219 / 0.230–0.232 / 0.240–0.244 |
| item skill, τ = 0.1 | 0.65–0.73 | 0.210–0.213 / 0.224–0.225 / 0.234–0.238 |
| item skill, τ = 0.2 | 0.36–0.38 | 0.193–0.196 / 0.206–0.208 / 0.216–0.220 |
| item skill, τ = 0.3 | 0.14–0.19 | 0.174–0.176 / 0.184–0.186 / 0.194–0.198 |
| half field knowledge, half skill, τ = 0.1–0.3 | 0.40–0.70 | as above |
| field rates only (hypothesis false) | 0.000 | as above |

- **Over the worlds the design itself names:** the hypothesis-true world gives P(pass) of 0.14 to 0.86, and the hypothesis-false world gives P(fail) = 1.0. By that reading D11 holds.
- **In-sample against leave-one-out:** in every world, in-sample < oracle < leave-one-out. The in-sample fit does favour the rule, as the design says, by about 0.010 to 0.015 against the oracle.
- **What is already published:**
  - The bettor's margin over the flat rule on these very items is −0.068 [−0.099, −0.036] (ss-b2).
  - The ss-b1 audit (`ledger/audits/ss-b1.md` item 9) already ran this rule's leave-one-out cousins on these items: a per-field prior on the up direction (0.263); the headline tag plus a question-order field prior (0.241); and a logistic on the headline tag, up-word, question order and length (0.233; bettor −0.070 [−0.104, −0.035]).
- **Conditional on those numbers:**

  | condition | τ = 0 | τ = 0.1 | τ = 0.2 | τ = 0.3 |
  |---|---|---|---|---|
  | d_flat within 0.008 of −0.068 | 0.92–0.93 | 0.77–0.79 | 0.37–0.43 | 0.14 |
  | and an audit-analogue up-prior of 0.26 or more | 0.95 | 0.95 | 0.86 | (few) |

  An audit up-prior of 0.263 is reached in 52% of τ = 0 worlds but in only 13% at τ = 0.2 and about 3% at τ = 0.3. So τ is small.
- **Pooled:** P(pass) ≈ 0.80 to 0.94, so P(fail) ≈ 6 to 20%. That sits at the floor.
- **What is missing:** the pre-registration does not cite the ss-b1 audit's table. Its lesson says it corrects P1 by "reading the archive's margin", but it reads only the margin, not the audit's dumb-predictor table that bounds field effects. The engine's 0.70 sits below what the published record implies.

This is not a redesign: the test can still fail, and its in-sample bar is honestly stricter than the remap's. But a pass will be counted as a hit on an outcome that was mostly foreseeable, and the file must say so before data.

## Required fixes

Each needs one dated DEVIATIONS row (one row may cover all three), written before the archive is scored and naming this review. None lowers the bar. The statistic, the rule, the in-sample fit, the bootstrap and the pass threshold all stay frozen.

1. **D8(a): the verdict sentences' nouns.**
   - In §5 sentences 1 and 2 and in `score_f3.py` `sentence()`, replace "a rule that knows each field's own rate of good-news results" with "a rule that knows, for each field, how often papers' own claims held and how often the 'higher / more' option was the reported one".
   - In the pass sentence, replace "is more than knowing which fields usually report good news" with "is more than knowing which fields usually report their own claims holding or 'higher / more' results".
   - In the null sentence, replace "may come from knowing which fields report good news" with "may come from knowing those field rates".
   - Then commit the code change, with no archive run.
2. **D8(b): the null sentence carries the in-sample caveat and the leave-one-out number.**
   - Append to the null sentence (§5.2 and `sentence()`): "The rule's rates were fitted on the same items it was scored on, which favours the rule; with each item's own label left out of its rates, the difference is {loo_baseline.d} [{lo}, {hi}]."
   - The pass sentence keeps its existing caveat.
   - This uses the already-computed `s["loo_baseline"]` and adds no new test.
3. **D11: disclose the prior evidence, and the foreseeability, in §6 before data.**
   - Add a bullet to §6: "ss-b1's audit (item 9) already scored leave-one-out cousins of this rule on the same 116 items: a per-field up-direction prior 0.263, headline tag plus question-order field prior 0.241, and a logistic on headline tag, up-word, question order and length 0.233 (bettor −0.070 [−0.104, −0.035]). Given those and ss-b2's margin, the design review put P(pass) at about 0.80–0.94. A pass therefore adds little beyond them; what this bet adds is the in-sample fit."
   - The engine may revise its odds before data under this row, keeping both numbers. Revising is the engine's call; the review only requires the disclosure.
   - Also add to the run procedure, in §7 or the results file: run `shasum -a 256 -c items/SHA256SUMS` and `git diff --quiet HEAD -- items/items.jsonl bettor/bets.jsonl` immediately before `python3 scoring/score_f3.py`, and record the output. §7's stop rule is not in the code.

Recommended, not required:
- guard `main()` so an untestable result writes its sentence rather than raising;
- state in the results file that the field jackknife interval uses ±1.96 on 4 clusters, and give the t with 3 df (±3.18) width beside it.

## Addendum: fixes confirmed (2026-11-05 06:57 America/Denver)

The fixes are under DEVIATIONS D55: 386d462 for the code and the row, 05e13e6 for the row's time and 5ee223a for the ledger. I checked them with `--synthetic` runs and on a tampered copy of the items file only. The archive was not scored.

- **F1 holds.** `sentence()` now names "a rule that knows, for each field, how often papers' own claims held and how often the 'higher / more' option was the reported one". The endings now read "is more than these field habits" and "may come from these field habits". I checked the printed sentences on the `skilled` world (pass) and the `coin` world (null).
- **F2 holds.** Both verdicts now end with the in-sample disclosure and the leave-one-out difference, taken from `s["loo_baseline"]`. On synthetic data the pass gives −0.070 [−0.109, −0.031] and the null gives 0.001 [−0.027, 0.028]. The statistic, the rule and the pass bar are unchanged: the `--synthetic` outputs for `skilled` and `coin` are identical to those before the fix.
- **F3 holds.** D55 carries the §6 disclosure (the ss-b1 audit's item 9 numbers and the review's P(pass) of 0.80–0.94). The pre-registration stays frozen.
  - The engine revised its odds before data, keeping every number. `ledger/bets.jsonl` has `engine_odds` 0.85, `engine_odds_first` 0.50, `odds_after_lesson` 0.70 and `odds_after_review` 0.85. The bar is not lowered.
  - The results file should repeat the D55 disclosure beside the verdict.
- **The checksum stop holds for the items file.** `main()` parses `items/SHA256SUMS`, and the real file matches it. I pointed `ITEMS` at a tampered file, `BETS` at a missing path and the outputs at scratch. The run then wrote "untestable" with its sentence and never called `score()`.
  - Residual, not blocking: `bettor/bets.jsonl` has no checksum and the code does not check it. The run session should record `git diff --quiet HEAD -- bettor/bets.jsonl` before scoring, as fix 3 asked.
- **The untestable crash is fixed.** `score()` sets `verdict_reported` on its own untestable branch, and `main()` writes a short tables file for any untestable label.
- **The read block holds.** ls-ss-b11's `read` (27 scored, Brier 0.209, 8/27, read at 3fd6037) matches `ledger/brier.md` at 3fd6037. The lesson text is unchanged.

The fixes hold. **The archive may now be scored:** `python3 scoring/score_f3.py`, once, from `programs/settled-science`.


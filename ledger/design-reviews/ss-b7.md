---
bet: ss-b7
program: settled-science
prereg_commit: 3d73273
reviewer_session: fresh design-review subagent launched by the engine session; worked only in the worktree /Users/seanpharris/oversight-testbed-review-ss-b7 (at 3d73273), with scratch copies and scripts under the session scratchpad review-ss-b7/
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true          # reviewer, author, bettor and the striking rater are all claude-opus-5-5
date: 2026-11-04 21:40 America/Denver
checks: {D1: flaw, D2: flaw, D3: flaw, D4: holds, D5: flaw, D6: holds, D7: flaw, D8: flaw, D9: flaw, D10: holds, D11: holds}
flaws: 6
pilot_usd: 0.00
verdict: fix-first
confirmed_at: null
---

# Design review of ss-b7

## In plain English

The bet can answer its question, and it can both pass and fail. In the design's own null world (the bettor knows only what the rater measures, and the rater adds only its call-to-call noise), it passed 2 of 44 simulated runs. With a rater that knows only the up word, it passed 44 of 44. But the scoring code breaks in a case the pre-registration names. If the striking rater honestly favours the down word, `score_b7` calls the bet "untestable" and prints "Too few ratings were returned". That is the ss-b6 gate G1, which §4 says does not apply here. The rule also does not say what happens if there is no retest: §3 and §5 give two different answers. Near the margin, which the pre-mortem says is the likely outcome, the leave-one-out check marks the label fragile on dozens of items, and the clause would list them all. The margin also covers less than the motivation and the lesson imply. It removes the false passes that come from the rater's call-to-call noise. It does not remove those in the null world the ss-b6 audit called consistent with the data, where this rule still passes 45% of the time. Each of these can be fixed without changing what is tested.

## Checks

Everything ran on a scratch copy of `programs/settled-science` (`scratchpad/review-ss-b7/ss/`) with `/Users/seanpharris/entangled-mind/.venv/bin/python -I`. `valence.py` was run with `dotenv`, `anthropic` and `entangled_mind` replaced by stub modules (`scripts/stubrun.py`, `scripts/orders.py`), so no `.env` was loaded and no network call was possible. Scripts: `scripts/g1.py`, `scripts/real_b6.py`, `scripts/mstar.py`, `scripts/loo_matched.py`, `scripts/d11.py`, all under `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/19f84df9-a6ff-48ba-89d6-d3f43e5d1747/scratchpad/review-ss-b7/`.

**D1. A stranger can apply the rule: flaw (F1, F2).** I applied §4–§5 to synthetic outcomes, one for each verdict.
- **Pass, null and n < 60** each give one verdict.
- **The rater favours the down word.** §4 says "G1 does not gate here." But `score_b7` takes its legs from `score_b6`, and `score_b6` returns early with `untestable` when G1's share is below 0.50. `score_b7` then prints the n < 60 sentence. Checked with raters that put 70 on the down word on 55% and 80% of items (`g1.py`): `untestable`, "Too few ratings were returned to test it (92 of 92)." Both are wrong: the pre-registration says the test should run, and the sentence is false. The pre-registered `inverted` synthetic rater also returns `untestable`. A rater asked what readers find "surprising" is a plausible case for favouring the down word, and the pre-registration names it.
- **No retest.** §3: "If the engine does not approve the $0.22, the fallback (decided now) is to use ss-b6's measured valence-rater retest noise, σ = 0.274." §5.3: "Untestable: fewer than 60 ratings, **or no retest**." That is two verdicts for one state. In code, a missing `r2-striking-retest.jsonl` stops `main_b7` with FileNotFoundError, and an empty one gives "The rater's retest was not available…", a sentence that is not in §5. The record at 3d73273 holds no ruling on the $0.22.
- **A partial retest** (a stop after k of 46) is not covered. σ_rt would be computed on k pairs, however small k is.

**D2. Every manipulation takes effect: flaw (F1, F6).**
- **σ moves the margin as it should** (frozen `score.py --b7 --synthetic`): σ̂ 0 → m* 0; σ̂ 0.199 → −0.0018; σ̂ 0.436 → −0.0045.
- **The prompt, tag and cache switch** (`orders.py`): `TAG` is `striking-v1` and `SYSTEM` is `SYSTEM_STRIKING`, verbatim as in §2. The 138 cache keys are all distinct, and none collides with the valence cache.
- **Option order matches the bettor's:** 92/92 primary and 46/46 retest jobs carry the bettor's `option_1_is`, and the retest reverses it.
- **The "G1 off" setting does not take effect** (F1).
- **The dry-run harness mis-sets the noise it reports.** It builds the retest as `100 − noisy(v)`, where `v` is already noisy. So the retest pair differs by one noise draw, not two, and σ̂ = σ/√2. The row labelled "copy + 0.27" ran at σ̂ 0.199, and "copy + 0.6" at 0.436.
- **A §4 number does not regenerate.** §4 says ss-b6's data at σ 0.274 give m* = −0.0033. The frozen code gives **−0.0026** (`real_b6.py`, `mstar.py`; σ̂ from the archived valence retest = 0.27427). The conclusion that ss-b6's −0.0018 would not clear it still holds.

**D3. Every control can fail: flaw (F6).** I named two wrong set-ups the rule must reject.
- **A copy rater** must give a null, and it does (d₂ ≡ 0, m* 0).
- **A copy rater plus noise** must also give a null. The table shows this only at σ̂ = σ/√2 (D2). It also shows it as one draw, not a rate. Tested properly (`d11.py`, world A, with fresh noise on each rating), the rule passed 2 of 44, so the control does reject. The committed dry run does not show it.

**D4. Rivals are matched: holds.** Both sides get the same features, the same leave-one-out logistic and the same bootstrap. The null-world rater goes through the identical fit. Copy gives d₂ = 0 and oracle gives a null, so neither side wins by construction. Note (not a flaw): the ss-b6 audit's `design_review_missed` was the near-50 term. `score_b6` regenerates "leg 2 without the near-50 term" as a secondary, but only against 0, not against a matching margin (see Notes).

**D5. A dumb baseline is beaten, and the design can see the effect: flaw (F4).** Here the dumb predictor is a bettor that knows nothing beyond the rater. In the design's null (world A below), it passes 5%, within the 10% target. But the lesson ("ss-b6's rule let a no-extra-knowledge bettor pass 24–61%") and §1 present the margin as the cure for that problem. The 58% figure the ss-b6 audit and D39 cite comes from a different null. There the rater differs from the bettor by the **observed disagreement** (SD 0.88 in logit), most of it stable from item to item, not by retest noise (0.27). I simulated that null (world B): stable item noise of SD 0.84 plus call noise of 0.274, so the retest measures only 0.27. **The ss-b7 rule passes 20 of 44 (45%)**, because the margin sees only the call noise. That null cannot be told apart from "the rater lacks knowledge the bettor has" with these data. In world C below, a margin set at the disagreement would block a real pass, so this is not a redesign. The fix is to scope the claim and report the number (F4).

**D6. Foreseeable execution risks are piloted: holds.** The pre-mortem is of kind `world`. The same 92 items and the same user-text format ran 138 valence calls at this setting with 0 refusals and every call parsed. `max_tokens` is 4000, and `_check_stop` is in `common.structured`. No pilot was needed; $0.00 spent.

**D7. Comparisons match: flaw (F5).** The bettor and the rater differ in more than the named factor, which is the question asked:
- **Information.** The bettor sees the question and the methods summary; the rater sees only the field and the two sentences.
- **Frame.** The bettor forecasts a published result; the rater is told to treat both as hypothetical.

The model, the thinking setting, `max_tokens`, the schema, the option order and the items all match. Whether a finding is "striking to readers in this field" depends on what the study asked. So a pass could come from the rater lacking that context, and the verdict sentences do not say the rater lacked it.

**D8. The verdict sentences are written: flaw (F1, F2, F3, F4, F5).** The §5 pass and null templates match `score_b7` word for word. Gaps:
- The G1 path prints the wrong sentence (F1), and the no-retest sentence is not in §5 (F2).
- The §5.5 scope sentence and "pass, unreplicated" are not generated.
- The fragile clause can list 56 items (F3).
- The pass sentence says "beyond the noise margin" without saying which noise that is (F4).
- Neither sentence says what the rater was not shown (F5).

**D9. One item cannot decide it: flaw (F3).** Leave-one-item-out and leave-one-bucket-out are pre-registered, and so is the fragile clause. But they misbehave at the margin. On ss-b6's real data through `score_b7` (leg 2 upper −0.00184 against m* −0.00256, null), **56 of 92 single-item removals flip the null to pass.** The clause lists all 56 and the scalable-oversight bucket. Most of these are items where the two raters agree (d₂ ≈ 0). Two things cause it:
1. m* stays fixed at its 92-item value while rows are dropped.
2. Each reduced set gets fresh bootstrap indices, and that jitter is about the size of the 0.0007 gap.

Recomputing m* on the same reduced rows of every null simulation (rows dropped, no refit) still leaves 43 flips (`loo_matched.py`). So the check measures closeness to the margin, not the influence of any one item. The pre-mortem expects exactly this region. In D11 worlds B, D, E and F, 48–91% of all draws came out "fragile".

**D10. Machinery: holds.**
- **Budget:** `common.Caller` enforces the shared $5.00 cap. `r2-striking-cache.json` is in `CACHES`, and spending so far is $4.0811, so $0.869 is usable before the $0.05 guard, against about $0.68 planned.
- **Refusals:** a refusal or any error stops the run, through `llm._check_stop` and `Caller`.
- **Caching:** by content hash, `key_of(TAG, MODEL, SYSTEM, user)`.
- **Scale direction:** both sides give P(Option 1) on 1–99, oriented by `p_true_of`, and leg 2 does not depend on direction.
- **Beacon:** no draw; the ss-b4 seed is inherited, as stated.
- **Lesson:** ls-ss-b7 (main repo HEAD) matches the §0 cell exactly. It is 40 words, prereg_commit 3d73273, and its read block (17 scored, Brier 0.264, 7/17, running 0.42, newest audit ss-b6.md) matches `ledger/brier.md` and `ledger/audits/` at 3d73273. P9's do_this (sentences in §5) is present. P12's do_this (P(pass) and P(fail) under worlds favouring each side) is present only as single synthetic runs; this review's D11 supplies the rates.
- **Checker:** `check_prereg.py --before-run` gives L1 ok, L3 ok, L2 warn (it reads the worktree's ledger, which predates the lesson commit) and R1 fail (this file).

**D11. The bet can both pass and fail: holds.** I ran the frozen `score_b7` against the real ss-b5 bettor ratings, 44 draws per world (`d11.py`). Each draw has fresh call noise (σ 0.274) on both the rating and the retest. The retest is reversed, and σ̂ is re-estimated each time.

| world | built as (logit scale) | P(pass) | P(fail) |
|---|---|---|---|
| A: design's null, call noise only | rater = bettor + call noise | 0.05 | 0.95 |
| F: same knowledge, less confident | 0.6 × bettor + call noise | 0.14 | 0.86 |
| B: ss-b6 audit's null | bettor + stable item noise (SD 0.84) + call noise | 0.45 | 0.55 |
| E: rater is like ss-b6's flattery rater | ss-b6 valence ratings + fresh call noise | 0.45 | 0.55 |
| D: half the bettor's signal | 0.5 × bettor + 0.6 × up + item noise (SD 0.5) + call noise | 0.66 | 0.34 |
| C: up word only | 1.0 × up + item noise (SD 0.8) + call noise | 1.00 | 0.00 |

In the world where the hypothesis fails (A), P(fail) is 0.95. In the worlds where it holds (C, D), P(pass) is 0.66–1.00. Both exceed 10%. The engine's 40 sits between world E and world F, which is reasonable. Without F1's fix, any world where the rater leans toward the down word becomes "untestable" rather than pass or fail.

## Required fixes

Each needs a dated DEVIATIONS row (D40 onward) written before any striking-rater call, naming this review. Rerun the dry-run table after the fixes and commit it.

- **F1 (D1, D2, D8): make G1 not gate in ss-b7, as §4 says.**
  - Give `score_b6` a `gate_g1=True` parameter. `score_b7` calls it with `False`, so legs 1 and 2 are always computed when n ≥ 60. G1–G3 stay reported counts.
  - Add down-word raters to the dry-run table, for example `inverted`, and 70 on the down word on 55% and 80% of items. Each must return pass or null, never untestable.
- **F2 (D1, D8): one rule for a missing or partial retest.**
  - Pick one of §3's fallback (σ = 0.274, with a stated sentence) or §5.3's untestable, and strike the other.
  - Set a minimum number of retest pairs, for example at least 30 of 46. Below it, the chosen rule applies.
  - `main_b7` must handle a missing file without crashing, and every sentence it can print must be in §5.
  - Record the engine's ruling on the $0.22 under rule 11.
  - Generate the §5.5 scope sentence and "pass, unreplicated" in `score_b7`.
- **F3 (D9, D8): a fragility check that works at the margin.**
  1. Recompute m* for each leave-one-item-out and leave-one-bucket-out subset. Drop the same rows from every stored null-simulation d₂ vector, with no refit, which is about a minute of compute. Do not reuse the full-set m*.
  2. Rerun the full label under 20 bootstrap seeds (null-simulation draws included). If any seed changes the label, report "<label>, at the margin (x of 20 seeds give <other>)".
  3. In the fragile clause, name the items only if at most 5 flip. Otherwise write "; this label sits at the margin: k of n single-item removals would make it <other>".

  This adds qualifiers. It does not change the rule.
- **F4 (D5, D8): say which noise the margin covers, and report the larger null.**
  - In §1, §6, the pass sentence and the results, "noise margin" becomes "**the rater's call-to-call noise margin**".
  - §1's "passes at most about 10%" gets "in a null world where the rater differs from the bettor only by its own call-to-call noise".
  - Pre-register as a reported secondary σ_dis, the SD of logit(rater) − logit(bettor) over the n items. Also report P(pass) of this rule in world B built at the measured values: stable item noise SD √(σ_dis² − σ_rt²) plus call noise σ_rt, 100 draws, seed 20261104.
  - On a pass, append: "; a bettor that differed from this rater only by stable item-level noise of the observed size would pass this test about x% of the time."
  - The lesson's link from 24–61% to this margin is then qualified in the results. learn.md freezes the lesson, so it is not rewritten.
- **F5 (D7): name the bundle.** In the pass and null sentences, after "the same model asked only which version reports the more striking finding", add "(shown only the field and the two sentences, not the question or methods)". The rest of the sentence is unchanged.
- **F6 (D2, D3): correct the dry run and its numbers.**
  - In `main_b7 --synthetic`, draw the retest from the clean synthetic value with fresh noise (`100 − noisy(base)`), so σ̂ estimates σ.
  - Report the copy-plus-noise rows as pass rates over at least 40 draws. This review's figures can be cited: 0.05 at σ 0.274.
  - Correct §4's "m* = −0.0033" to −0.0026, as the frozen code gives.

## Notes (not required)

- Report "leg 2 without the near-50 term" against its own margin, with the same null world built without that term. This is the specification check the ss-b6 audit said its review missed.
- 100 null simulations put the realised false-pass rate somewhere around 5–16% (world A gave 2/44). 200 simulations would halve that spread for about 10 s more per run.
- Write a UTC timestamp into each cache entry (ss-b6 audit A1), so the audit can confirm the calls followed the confirmation of these fixes.

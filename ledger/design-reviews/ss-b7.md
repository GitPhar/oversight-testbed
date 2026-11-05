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
confirmed_at: 2026-11-04 22:18 America/Denver   # addendum 2: fixes D40-D46 confirmed at ef378a4; go
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

---

## Addendum 1: checking the fixes at 274e637 (D40–D45)

Written 2026-11-04 by the same reviewer, before any striking-rater call. I read `programs/settled-science/{DEVIATIONS.md, scoring/score.py, bettor/valence.py}` at 274e637 from the main repo (`git archive 274e637` into the scratchpad `review-ss-b7/fix/`) and reran on that copy. As before: no paid calls, and the API modules were stubbed. Scripts: `scripts/d11_fix.py` (the D11 worlds, plus down-word and inverted-bettor raters, with `seed_check=False`; the seed check adds a qualifier and never changes the label) and `scripts/fixcheck.py` (edge cases, and a full run with the seed check on ss-b6's real valence data).

**Verdict: still fix-first, with one item left (R1).** Each of F1–F6 is done as required. Running F3's new seed check on the motivating data exposed a gap in the verdict sentence. The fix for it is small.

### Each fix

- **F1 (D40): confirmed.** `score_b6(..., gate_g1=False)` is what `score_b7` calls. None of the 44 × 9 simulated runs below was untestable, including raters that favour the down word on 55% and 80% of items and the bettor's own ratings inverted. **Is "pass" right for the down-word raters?** Yes. `down55`/`down80` (D44) and my G worlds put 70 on whichever word a random draw picks. They carry no information beyond the up word, so after recalibration they reduce to the up-word rule, which the bettor beats (leg 2 upper ≈ −0.08). `inverted` is valence50 mirrored. Leg 2's logistic flips it back, so it gets exactly valence50's leg 2 (upper −0.0017) and its label, "pass, fragile". Leg 1 passes trivially for both, as it should for a rater whose scale runs the other way. A rater that knows what the bettor knows but reports it reversed (world H) comes out null 86% of the time, as the design's null world should. Its 6 of 44 passes are within Monte Carlo noise of world A's 2 of 44.
- **F2 (D41): confirmed.**
  - A missing retest gives untestable with the D41 sentence, and so does a 29-pair retest. A 30-pair retest is scored.
  - A missing ratings file gives "Too few ratings were returned to test it (0 of 92)", with no crash.
  - §3's fallback is struck. The scope sentence (`scope`) and `verdict_reported` are generated.
  - The engine's ruling on the $0.22 is recorded in D41: approved by oversight-testbed-1b at about 21:08 under st-16. I can see that only as D41's statement. Nothing in `steers.jsonl` or the bet row carries it.
- **F3 (D42): confirmed as specified.**
  1. m* is recomputed for every leave-one-out and leave-one-bucket-out subset from the stored null d₂ vectors, with no refit.
  2. The 20-seed check runs.
  3. More than 5 item flips gives the count sentence.

  On ss-b6's data, the null now reads "…this label sits at the margin: 43 of 92 single-item removals would make it pass", with `label_reported` "null, at the margin (16 of 20 seeds give pass), fragile". Full run: 273 s.
- **F4 (D43): confirmed.** The sentences say "the rater's call-to-call noise margin". σ_dis and the world-B rate are computed: on ss-b6's data σ_dis 0.884, world-B rate 0.47, matching my world B (0.45). A pass gets the world-B clause. `world_b_rate` holds m* at its observed value rather than re-estimating it in each draw. With σ_rt fixed at its measured value that is acceptable.
- **F5 (D44): confirmed.** Both sentences carry "(shown only the field and the two sentences, not the question or methods)".
- **F6 (D44): confirmed.** The synthetic retest draws fresh noise on the clean value: copy+0.274 measures σ̂ 0.251, and copy+0.6 measures 0.604. §4's m* is corrected to −0.0026, and the cited rate is this review's 0.05. D45 (`t_utc` on each cache entry) is in `valence.py`.

### D11 again, on the fixed code (44 draws per world)

| world | P(pass) | untestable | median world-B rate reported |
|---|---|---|---|
| A: design's null, call noise only | 0.05 | 0 | 0.05 |
| B: ss-b6 audit's null, stable item noise | 0.45 | 0 | 0.47 |
| C: up word only | 1.00 | 0 | 0.98 |
| D: half the bettor's signal | 0.66 | 0 | 0.56 |
| E: like ss-b6's flattery rater | 0.45 | 0 | 0.51 |
| F: same knowledge, less confident | 0.14 | 0 | 0.45 |
| G55: 70 on the down word on 55% of items, else up (G1 share 0.47) | 1.00 | 0 | 0.98 |
| G80: the same on 80% of items (G1 share 0.21) | 1.00 | 0 | 0.98 |
| H: the bettor's own signal reversed, call noise (G1 share 0.21) | 0.14 | 0 | 1.00 |

**D11 holds.** In the hypothesis-false worlds (A, and H, its mirror), P(fail) is 0.95 and 0.86. In the hypothesis-true worlds (C, D, and the down-word raters), P(pass) is 0.66–1.00.

### What remains

- **R1 (D8, created by F3's seed check): the verdict sentence must carry the seed split.**
  - **The problem.** On ss-b6's own data the frozen seed gives null, while **16 of 20 other seeds give pass**. That split appears only in `label_reported`. The plain-English `sentence`, which P9 says is the only wording used afterwards, says "not shown to pick … better" with no word of it.
  - **The fix.** When `seeds_other > 0`, append to the sentence: *"; this label sits at the margin: under 20 other bootstrap and null-simulation seeds, x gave <other>"*. Put it before the fragile clause. Name it in a DEVIATIONS row before any call.
  - **Also needed.** When more than 5 items flip, the count sentence drops the bucket flips. Keep them, for example "…would make it <other>, and so would dropping the query bucket(s) …".
  - **What does not change.** The rule, the seed and the bar.

  Once that row and the code change are committed, the run may start. The engine session can check this by rerunning `scripts/fixcheck.py`: the full run's sentence must then name the seed split and the scalable-oversight bucket. It does not need another full review.

### Notes (not required)

- `verdict_reported` repeats itself ("null (null, at the margin …)"). Tidy it in the same change.
- The seed split shows that, near the edge, the verdict at the frozen seed is close to a Monte Carlo coin. Increasing `N_NULL` to 400 and `NULL_BOOT` to 10,000 would cut that noise without moving the bar. It costs roughly 4–5× the scoring time (the seed check is the expensive part). This is the author's call, decided before data.

---

## Addendum 2: R1 confirmed at ef378a4 (D46). Go

Written 2026-11-04 22:18 America/Denver, before any striking-rater call. I took the program at ef378a4 into a fresh scratch copy with `git archive ef378a4 programs/settled-science` (scratchpad `review-ss-b7/fix2/`). Then I reran `scripts/fixcheck.py` and a synthetic spot check. No paid calls were made, and nothing was stubbed except as before.

**Verdict: confirmed (go).** Every fix, F1–F6 and R1, is in place as required, each under a DEVIATIONS row dated before data (D40–D46). The run may start.

- **R1 is done.** The full run on ss-b6's real data (seed check on, 212 s) now ends its sentence with: *"…this test cannot tell those apart; this label sits at the margin: under 20 other bootstrap and null-simulation seeds, 16 gave pass; this label sits at the margin: 43 of 92 single-item removals would make it pass, and so would removing the query bucket scalable-oversight."* So it names the seed split and the scalable-oversight bucket. `verdict_reported` now reads "null; at the margin (16 of 20 seeds give pass), fragile".
- **The rule, seed and bar are unchanged.**
  - The ef378a4 diff to `score.py` touches only the sentence and `verdict_reported` strings.
  - The constants and the label lines (`N_NULL, NULL_BOOT, …`, `BOOT_SEED, BOOT_N`, `lab = lambda`, `full = lab`) are identical to 274e637.
  - The full run reproduces 274e637's numbers exactly: label null, m* −0.002555, σ_rt 0.27427, σ_dis 0.884, world-B rate 0.47, 16 of 20 seeds the other way, 43 item flips, bucket flip scalable-oversight.
  - The edge cases are unchanged: no retest or 29 pairs gives untestable, 30 pairs is scored, no ratings gives "0 of 92".
- **D11 needs no rerun.** The labels are untouched. The synthetic spot check at ef378a4 gives coin pass, copy null, inverted "pass, fragile", down80 pass, copy+0.274 null (σ̂ 0.259, m* −0.0023). These match addendum 1, so addendum 1's D11 table stands.
- **The $0.22 ruling is now in the ledger.** `ledger/spend.jsonl` br-001 (069d8c7) records it: approved by oversight-testbed-1b at 21:08 under st-16, $0.68 in all, with the late recording disclosed. D41 now cites it.
- **N_NULL stays at 100 and NULL_BOOT at 2,000,** by the author's call before data. My note was optional, and the seed check now reports the remaining Monte Carlo spread in the sentence itself.

Cosmetic, not required: when both qualifiers fire, the sentence says "this label sits at the margin" twice.

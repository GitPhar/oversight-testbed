---
bet: em-gm2bf1
program: entangled-mind
prereg_commit: e65b1d5
reviewer_session: fresh design-review subagent, main checkout, 2026-11-05 (seed commit 14d6c9e also read)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 07:03 America/Denver
checks: {D1: holds, D2: holds, D3: flaw, D4: holds, D5: flaw, D6: holds, D7: holds, D8: flaw, D9: flaw, D10: holds, D11: holds}
flaws: 3
pilot_usd: 0.00
verdict: fix-first
confirmed_at: 2026-11-05 07:14 America/Denver
---

# Design review of em-gm2bf1

## In plain English
The test can answer its question, but its guard has a leak. The guard is meant to stop a pass when "mid-scale claims wobble more" is the whole story. It checks extremity only in the six-format archive (the 0–100 format, F1). The order span, though, is measured in a different archive, the order conversations. There the same claims sit at somewhat different levels. The extremity of a claim in the order conversations agrees with its F1 extremity only at Spearman 0.46.

I built worlds from the archives' measured numbers in which extremity alone drives both spreads. In those worlds the frozen rule passes 21% and 44% of the time, so the guard cannot reject the boring world it was added to reject. Adding the order archive's own extremity, and squared rank terms, as covariates cuts those false passes to 6% and 10%, and keeps nearly all the power where a shared instability exists.

The bet can both pass and fail: in shared-instability worlds it passes 11–80% of the time, depending on how strong the shared part is. Two smaller fixes are also needed:
- §5 must say what a single-item flip does.
- The pass sentence must not say "were also the ones" for a correlation that can be as low as 0.30.

## Checks

Scratch scripts are in `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/e93ce59f-1dc3-4451-8206-bee8c0537bfa/scratchpad/review-gm2bf1/` (`measure.py`, `measure2.py`, `measure3.py`, `reliab.py`, `world.py`, `sim.py`, `sim2.py`, logs `sim2-w0.log` … `sim2-w9.log`). All were run with `/Users/seanpharris/entangled-mind/.venv/bin/python`. None calls an API or runs a local model. The script was never run with `--seed`. Results file `results/gm2bf1-order-vs-format.*` does not exist.

**What I computed on the real data (all of it).** I never computed ρ(S, G), the partial ρ, or any secondary that pairs S or G with E or W.
- *Structure and missing cells:* 160 claims, 40 items. Each claim has 10 shown ratings in each of O1–O4, with no null rating and no claim rated twice in a conversation. Each claim has 10 calls in each of F1–F6, and the format means contain no NaN. So n = 160, and "untestable" cannot occur. The archives also contain `MF`, `high` and `low` keys, which the code correctly ignores.
- *Ties in the per-claim format means:*
  - F2: 90 claims tied at 1.0.
  - F3: 66 tied at 0.0.
  - F4: 90 tied at 1.0.
  - F5: 23 tied at 0.
  - F6: largest tie block 25 claims at 3.0.
  - F1: 129 distinct values.
  - The F2 and F4 all-yes blocks share 65 claims. The F2 all-yes block includes claims whose F1 mean is as low as 2.2. The F3 yes rate does not depend on the ticket price (0.42, 0.37, 0.37, 0.43, 0.41 at $10–90).
- *Covariates on their own:*
  - W quantiles (0/10/25/50/75/90/100%): 0.24 / 0.6 / 2.1 / 5.4 / 9.6 / 18.4 / 37.7.
  - E quantiles: 0 / 10.5 / 24.9 / 40.0 / 46.2 / 47.0 / 49.8.
  - F1 mean quantiles: 0.2 / 3.7 / 16.1 / 66.3 / 90.5 / 96.9 / 99.1.
  - Order-archive claim level (mean of all 40 shown ratings) quantiles: 1.6 / 15.5 / 40.2 / 69.4 / 88.1 / 96.2 / 99.0.
- *Covariate relations (none involves S or G):*
  - Spearman(order-archive level, F1 mean) = 0.82.
  - Spearman(Eo, E) = **0.46**, where Eo = |order-archive level − 50|.
  - Spearman(E, W) = −0.36 and Spearman(Eo, W) = −0.76.
  - Spearman of the order-archive level with each format: 0.82 / 0.67 / 0.62 / 0.40 / 0.49 / 0.72.
  - Format × format Spearman: 0.37–0.74.
- *Marginals of S alone and G alone, and their own split-half reliabilities:*
  - S quantiles: 0.2 / 1.5 / 4.3 / 15.1 / 36.1 / 61.1 / 94.6. The noise-only span 2.06·W/√10 has median 3.5.
  - G quantiles: 0.037 / 0.076 / 0.103 / 0.165 / 0.228 / 0.281 / 0.378.
  - Split-half reliability (5 against 5 repeats, 20 random splits, Spearman–Brown): S 0.98, G 0.93. So reliability does not cap ρ below the 0.30 bar.

**D1. holds.** `verdict()` gives exactly one label on each synthetic table I tried:
- (160, ρ .45, lo .10, partial lo .05): pass
- partial lo −.02: fail
- ρ .25: fail
- ρ = 0.30 − 5e-10 with both lower bounds 1e-8: pass (the ρ tolerance favours pass, and the lower bounds must clear 0 + 1e-9, as §5 says)
- ρ lower bound exactly 0: fail
- n 119: untestable; n 120: pass

`analyse()` returns untestable without statistics only when n < 10, and otherwise defers to `verdict()`. This is consistent, and moot because n = 160.

**D2. holds.** There is no manipulation knob. The measures are read as §2 says:
- Claim ids in the turns are the integers in `split-exp5.json`'s `chain_claims`.
- `order_measures` uses only O1–O4 and only `S` turns of the named condition.
- `observed_scale` inverts the F1 encoding exactly, so E = |F1 mean − 50| on the 0–100 scale.
- `format_measures` ranks each format with midranks.
- The `--selftest` measure checks (monotone-rescaling invariance of G, span of a toy conversation) pass.

The script imports this checkout's files, not the old `/Users/seanpharris/entangled-mind` folder: `gm3b_format_invariance`, `gm3c_heldout_format`, `exp5_run` and `config` all resolve under `/Users/seanpharris/oversight-testbed/programs/entangled-mind/`, and `config.RESULTS`/`EXPERIMENTS` point there.

`--selftest` printed SELFTEST OK in 5 s:
- shared world: ρ +0.84, partial +0.82, pass
- extremity world: ρ +0.71, partial −0.01, fail
- unrelated world: fail

Note: given the tie blocks above, G for the 90 all-yes claims partly measures where a claim's continuous-format rank sits relative to the binary formats' block midrank, not movement of its own. The worlds below include this tie saturation. On its own it produced a false pass rate of only 1% (W0), so it is a caveat on wording (F3), not a separate flaw.

**D3. flaw (F1).** The guard is the control, and it cannot reject a plausible wrong world. The self-test's "driven by extremity only" world is linear in a variable `ext` that is *also the covariate itself*, with no measurement error and no cross-archive difference. So the guard removes it by construction.

In the real design:
- S is produced in the order conversations. A claim's level there agrees with F1 at Spearman 0.82, but its extremity agrees with E at only 0.46. W tracks the order archive's extremity (−0.76) much better than E does (−0.36).
- The guard is linear in the ranks of E and W.

The test worlds (`sim2.py`) keep the measured lev, W and F1 means fixed, so E is real. S comes from synthetic order means on the logit scale around the order-archive level. G comes from synthetic F2–F6 responses generated from a common latent (the average of the F1 and order-archive logits) plus claim × format deviations, with links tuned to reproduce the measured tie blocks, S and G quantiles, and cross-format correlations. Results (200 worlds each, 1,000 cluster resamples):

| world | frozen rule P(pass) | median ρ | P(partial lower bound > 0) | alternative guard P(pass) |
|---|---|---|---|---|
| I: S and G independent (G permuted) | 0.000 | −0.00 | 0.015 | 0.000 |
| W0: extremity only (logit mid-scale + tie saturation) | 0.010 | +0.12 | 0.050 | 0.010 |
| W0b: + mid-scale format deviations (0.5) | 0.050 | +0.21 | 0.100 | 0.020 |
| **W0c: + mid-scale on both sides (0.5, 0.5)** | **0.210** | +0.34 | 0.210 | 0.060 |
| **W0d: + mid-scale on both sides (0.8, 0.8)** | **0.435** | +0.45 | 0.435 | 0.100 |
| W1: shared instability κ 0.25 | 0.025 | +0.14 | 0.140 | 0.020 |
| W1: κ 0.5 | 0.115 | +0.20 | 0.465 | 0.110 |
| W1: κ 0.75 | 0.390 | +0.28 | 0.855 | 0.390 |
| W1: κ 1.0 | 0.805 | +0.35 | 1.000 | 0.805 |
| W1c: κ 0.5 + mid-scale both sides (0.5) | 0.720 | +0.38 | 0.735 | 0.400 |

The guard's false-positive rate is right when nothing is shared (1.5% against a nominal 2.5%), so the cluster bootstrap is not the problem. The problem is the covariate. When mid-scale claims wobble more on both sides, which is the world the lesson and the pre-mortem say is most likely ("extremity likely explains most of it"), the frozen guard passes 21–44% of the time with no shared instability at all.

The alternative guard is the same partial Spearman with covariates E, Eo = |order-archive mean shown rating − 50| and W, each entered as a centred rank plus its square. It lowers that to 6–10% and keeps the power in the pure shared worlds (11%, 39%, 80%). It costs power in W1c (72% → 40%), which is the expected price of removing extremity confounding.

**D4. holds** (not applicable: no fitted rival families; the rival is the extremity/noise driver, treated under D3/D5).

**D5. flaw (same fix as F1).** The dumbest explanation here is a claim-level driver: extremity plus noise. It passes the frozen rule in the plausible worlds W0c/W0d (21%, 44%). The rule asks the result to beat extremity only as measured in the other archive, and only linearly in ranks. This is no separate fix: F1 closes it.

**D6. holds.** No calls. The pre-mortem's kind is `world`.

**D7. holds (with the note in F1).** The two measures come from different set-ups:
- **Order archive:** multi-turn deliberation with the opening anchor (a); the claim is rated as one of four chain claims, with earlier answers shown, and the main question follows.
- **Format archive:** one turn per call, "which came up in a discussion of the question …", six response formats.
- Both use claude-haiku-5-5 at the API default temperature 1.0.

The claim is correlational across claims ("the same claims are unstable both ways"), so this bundle is acceptable as stated in §6. Its one consequence that matters is that extremity measured in one context is the wrong covariate for the other. That is F1.

**D8. flaw (F3).** The sentences are written, but the pass sentence says more than the statistic:
- "the claims whose rating moved most with question order were also the ones whose position moved most across answer formats" asserts identity. A pass needs only ρ ≥ 0.30, about 9% shared rank variance.
- "how noisy its ratings were" refers to W, which is noise in the order conversations only. Format-call noise is not controlled.
- For 90 claims, "position" in two of six formats is a tie-block midrank.

**D9. flaw (F2).** Leave-one-item-out is pre-registered and the flipping items are listed. Pattern P10 also requires the rule to state what happens if one item flips the label, and §5 does not. (The em-gm3cf1 review the same morning found the same gap.)

**D10. holds.**
- **Seed:** `python3 ledger/seed.py <randomness> em-gm2bf1 --purpose bootstrap` gives 12485997366771242721, matching §2. Pulse 1592288 (06:44:00) is the first after the pre-registration commit (06:43:25, `e65b1d5`); the seed commit `14d6c9e` (06:44:40) changes only that line.
- **Code and data:** the analysis code, the two reused modules, the three archives and `split-exp5.json` are unchanged since `e65b1d5` and clean in the working tree. Archive sha256 prefixes: `gm2-conversations.json` e9d59385c62d2e48, `gm2b-conversations.json` a7cbe10e6329cfe7, `gm3b-calls.json` 0a5a27a4fda3b662. They are git-tracked at `32ca722`, so the commit pins them, and the script records them.
- **Scale and budget:** one scale direction (0 = certainly false, 100 = certainly true) in both archives. Budget $0, no calls, so stop-on-refusal and caching do not apply.
- **Ledger checks:** `ledger/check_prereg.py em-gm2bf1 … --before-run` gives L1, L2, L3 ok (the lesson matches §0 and the commit; patterns P3, P8 exist), H1 ok (no human odds is right), and R1 fails only because this file did not yet exist.
- **Dry run:** P12/P15 ask for a committed dry run of P(pass) and P(fail) from measured numbers. The self-test's worlds use assumed effect sizes (ρ 0.84). The fix for F1 adds that dry run.

**D11. holds.** At n = 160 (40 clusters), using only the measured marginals above, the frozen rule:
- passes 11.5%, 39% and 80.5% in shared-instability worlds of strength κ 0.5, 0.75 and 1.0 (2.5% at κ 0.25);
- fails at least 19.5% in every world built.

So it can both pass and fail. With the F1 guard, the pass chances in the pure shared worlds are 11%, 39% and 80.5%, still above the floor from κ 0.5 on. The κ scale has no measured anchor (nothing in the record measures a shared instability), so P(pass) at the truth is unknown. At κ ≤ 0.25 it falls below 10%, which fits the bet's 25% odds.

## Required fixes

Each needs a dated DEVIATIONS row, written before any data and naming this review. Then the reviewer confirms in an addendum here.

1. **F1 (D3, D5): give the guard the order archive's own extremity, and let extremity enter non-linearly.**
   - Change `partial_spearman` covariates to E (|F1 mean − 50|), Eo (|mean of the claim's 40 shown order ratings − 50|) and W, each as a centred rank plus its squared centred rank (seven columns with the intercept). Add Eo to §2's measures, and report ρ(S, Eo) and ρ(G, Eo) as secondaries.
   - Add to `--selftest` a world where S's extremity driver is measured in a second, noisy copy of the level, as here (the self-test's extremity world currently uses the covariate itself).
   - Commit a dry run built from the measured marginals listed above, in the manner of `sim2.py`. It must show P(pass) ≤ about 10% in W0c/W0d-type worlds, and P(pass) ≥ 10% in at least one shared world.
   - The bar (ρ ≥ 0.30, both lower bounds > 0) is not lowered; this only tightens the guard. Odds may be re-stated before data, keeping both numbers.
2. **F2 (D9): state the single-item rule in §5.** For example: "If dropping any one item's four claims flips the verdict (bounds shifted by the point change), the verdict stands but is reported as '<verdict>, carried by item <id>', and the item is named in the verdict sentence." Any rule is acceptable if it is fixed before data and does not turn a pass into an easier pass.
3. **F3 (D8): reword the pass sentence**, for example: "On Haiku's 160 deliberation claims, the claims whose rating moved more with question order tended also to be the ones whose rank moved more across answer formats (Spearman ρ = x), and this held after allowing for how extreme the claim's rating was in both archives and how noisy its ratings were in the order conversations." Also add a §6 line saying that in two binary formats 90 claims share one tied rank, so part of the format spread is tie position.

## Addendum: fixes confirmed (2026-11-05 07:14 America/Denver)

I read the fix commit `f09824e` (DEVIATIONS D71) and `experiments/gm2bf1_order_vs_format.py` at HEAD, which is unchanged since `f09824e`. The frozen pre-registration file is untouched; its new §5 and §6 text lives in D71 and in the code. `results/gm2bf1-order-vs-format.*` still does not exist. The primary was not run, and nothing pairing S with G was computed on real data.

- **F1 holds.**
  - **Guard:** `partial_spearman` now enters each covariate as its centred rank plus its squared centred rank. `stats` passes [E, Eo, W].
  - **Eo:** `order_measures` computes Eo = |mean of the claim's 40 shown ratings − 50|, the same definition as my dry run's `EO = |LEV − 50|`. Eo is required (`analyse` raises without it) and is part of the completeness mask. The redacted secondary uses the shown Eo, which is acceptable for a secondary.
  - **Code matches the dry run:** on 50 random 160-claim tables, the code's guard and the dry run's `pcorr` give the same value (largest difference 0).
  - **Dry run:** `experiments/gm2bf1-dryrun/` is byte-identical to my scratch copies. The only change is that `world.py` loads `marg.npz` from its own folder. I checked that it loads that file, and that the 10 result JSONs match mine. The README table reproduces my numbers: extremity-only worlds pass at most 10% with the D71 guard; shared worlds pass 11%, 39% and 80.5% at κ 0.5–1.0.
  - **Selftest:** `--selftest` at HEAD prints SELFTEST OK (6 s). The three original worlds give the same labels. The new mismatched-extremity world falsely passes 3 of 20 runs with the new guard against 5 of 20 with the old.
  - **Is the residual acceptable? Yes.** My fix asked for about 10% or less in W0c/W0d-type worlds built from measured marginals. The committed dry run gives 6% and 10%. The self-test world is the author's own, and a harsher one: 3/20 is about 15%, with a binomial 95% interval of roughly 3–38%, so it cannot separate 6–10% from 15%. Its stated floor (new ≤ old and ≤ 4 of 20) works as a regression check, not as an estimate.
  - **Why it cannot reach zero:** two noisy measures of extremity cannot remove the confound completely. D71 says so instead of claiming the false-pass rate is near zero, and the frozen pass sentence ("after allowing for") claims no more than that. If the result is a pass, its write-up should carry the measured residual (6–10% in the measured-marginals worlds) next to §6's limits. That is a reporting note, not a condition of this confirmation.
- **F2 holds.** The single-item rule is in D71 §5. The code labels the verdict `<verdict>, carried by item <id>` and appends the item to the sentence whenever leave-one-item-out flips it. The pass/fail logic is unchanged, so the bar is not lowered.
- **F3 holds.**
  - **Pass sentence:** it now reads "tended also to be … (Spearman ρ = <x>) … in both archives … in the order conversations"; the code fills in ρ.
  - **§6 caveat:** the 90-claim tie note is added to §6 in D71.
  - **Fail sentence:** unchanged, and acceptable.

Odds stay at 0.25 with no new deviation needed, which is consistent: the shared worlds' pass rates are unchanged under the D71 guard. **Confirmed: the run may start.**

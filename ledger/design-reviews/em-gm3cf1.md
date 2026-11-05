---
bet: em-gm3cf1
program: entangled-mind
prereg_commit: d490327
seed_commit: 0fa0924
reviewer_session: design-review em-gm3cf1 (fresh subagent launched by the engine session; main checkout read at HEAD, with no change to the bet's files since d490327/0fa0924; no chat, transcript or author message read)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 06:43 America/Denver
checks: {D1: holds, D2: flaw, D3: holds, D4: holds, D5: holds, D6: holds, D7: holds, D8: flaw, D9: flaw, D10: flaw, D11: flaw}
flaws: 5
pilot_usd: 0.00
verdict: redesign
confirmed_at: null
---

# Design review of em-gm3cf1

## In plain English

The code does what the pre-registration says, and it does it correctly. It has no leakage, its BCa interval agrees with SciPy's, it reads its seeds correctly, the untestable and link-free guards can both fire, and the self-test passes. But as built, the test cannot answer its question, because its answer can almost be read off numbers that are already published. The em-gm3c audit measured the single-split upper end of the interval at four fold assignments: 0.501, 0.497, 0.510 and 0.522, a mean of 0.5075. This bet's two changes both push that bound up. Averaging predictions over ten splits raises Q (§0 says so itself), and BCa raises the upper end when the bootstrap is right-skewed, as em-gm3c's interval was (0.089 below the estimate, 0.103 above). I built synthetic worlds matched to those measured numbers. In them, the frozen rule passes about 1% of the time (0–6% if only the original split is used). That is below design-review.md's floor of about 10% for P(pass). The pre-mortem's own failure mechanism is the likely outcome, and the 30% odds are too high. I also found four fixable flaws. Any re-bet should carry their fixes over:
- the "converged" stop rule actually stops earlier than the parent's fit did;
- nothing says what happens to the verdict when one item flips it, and in these worlds that is near-certain;
- the pass sentence says "each format" about a mean;
- the archive and split files are not pinned by hash.

**What I measured on the real data, exactly.** I read `results/gm3b-calls.json`. It has 9,600 keys, 1,600 observations per format after `encode`, and sha256 `0a5a27a4…84b9`, the same as the old folder's copy. I also read item metadata (category and source) from `results/pool-run-3.json` for the 40 items. I ran two fits of the one-credence model on one real training set: held-out format F6, fold 0 of an assignment shuffled with seed 0 (not the beacon seed), even repeats. That gave rounds, time, objective and parameter changes (D2). I computed no prediction, R², Q, interval, link-free regression or verdict on the real data. I did not run the script with `--fold-seed`/`--boot-seed`. No API call, no local model.

## Checks

**D1. The rule can be applied by a stranger. Holds.** `verdict()` on synthetic rows (`scratchpad/review-gm3cf1/synth_checks.py`):

| BCa upper, link-free Q, capped share | verdict |
|---|---|
| (0.47, 0.44, 0) | pass |
| (0.50, 0.44, 0) | fail |
| (0.4999999999, 0.44, 0) | fail |
| (0.47, 0.50, 0) | fail |
| (0.47, 0.52, 0) | fail |
| (0.53, 0.55, 0) | fail |
| (0.47, 0.44, 0.11) | untestable |
| (0.47, 0.44, 0.10) | pass |

Every row gets exactly one verdict, and the boundaries fall on the sides §5 states (P13 tolerance 1e-9, on both the bar and the 10% cap). A NaN bound or a NaN link-free Q reads as "fail". §5 does not cover that case; untestable would be the better reading (recommendation R1).

**D2. Every manipulation takes effect. Flaw (F2).** Holds for:
- **Folds.** `assignments()` gives five folds of 8. They differ across j and across seed, and the seed is reduced mod 2^63 exactly as §2 says (18416738419240260146 → 9193366382385484338).
- **Sub-seeds.** `ledger/seed.py` gives folds 18416738419240260146 and bootstrap 3943194411379291992, as recorded.
- **BCa.** On a skewed (exponential, n = 40) bootstrap, the frozen `bca()` gives [0.6374, 1.0443] (z0 +0.021, a +0.0175). The percentile interval is [0.6271, 1.0326] and `scipy.stats.bootstrap(method="BCa")` gives [0.6384, 1.0471], which agrees within Monte Carlo error.
- **Held-out removal.** On synthetic data I replaced the held-out format's own even repeats on the test claims with nonsense. The test claims' predictions changed by 0.0 (no leakage). Flipping another format's test-claim data moved them by up to 4.3.
- **FIT_TOL.** The stop rule changes the number of rounds (synthetic: 14, 24 and 87 rounds at 1e-3, 1e-6 and 1e-8).

The flaw is what the stop rule does relative to the parent. §2 and the lesson present the change as removing optimiser noise ("runs to convergence … gm3b stopped at 40"). But FIT_TOL = 1e-3 is looser than gm3b's own tolerance of 1e-6. On the one real training set I fitted (held-out F6, fold 0):
- At FIT_TOL = 1e-3 the fit stopped after **31 rounds** (5.0 s, objective −4937.5745).
- At 1e-8 it took 115 rounds (9.8 s, objective −4937.5731). That is a further gain of 0.0014, max |Δθ| 0.0052, max |Δμ| 0.0095 (0.0079 on test claims).

gm3b's rule (1e-6 or 40 rounds) would have run at least those 31 rounds and to a tighter tolerance, or to 40. So the frozen "converged" fit is no more converged than em-gm3c's, and on this fold less so. The effect on Q is probably a few thousandths. That is the size of the margin this bet lives in, and tightening costs about 25 minutes more over 300 fits.

**D3. Every control can fail. Holds.**
- The link-free guard rejects a shared-credence world: the self-test's world gives linear Q 1.11, verdict fail.
- The untestable gate fires when fits cannot converge: with MAX_ROUNDS = 2 the capped share is 1.0 and the verdict untestable.
- `--selftest` ran OK in 5 min 25 s (06:29:35 to 06:35:01). One shared credence: Q 1.18, BCa [1.11, 1.37], linear 1.11, verdict fail. Large deviations: Q 0.10 [0.05, 0.18], linear 0.15, verdict pass. Both worlds are far from the bar; D11 covers the region near it.

**D4. Rivals are matched. Holds (no contest; one guard).** The one-credence model (L1) and the link-free predictor see the same information for test claims: the other five formats' even repeats. Both use the same fold assignments and the same averaging. The link-free fit takes its training targets from odd repeats while L1 takes its links from even repeats, but neither touches a test claim's held-out format.

**D5. A dumb baseline is beaten. Holds.** For "recovery below half", the dumbest thing that passes is a weak predictor: noise gives Q ≈ 0, and a constant gives NaN. The pre-registered guard is P3 in the right direction: a link-free least-squares predictor must also recover under half. The parent audit's link-free check gave 0.435, so the guard can bind. The power question for this upper-bound claim is D11.

**D6. Foreseeable execution risks are piloted. Holds.** There are no calls, and the pre-mortem is of kind `world`. The real risk was run time. One real fit takes 5–10 s, so 300 fits take about 25–50 min plus the bootstrap, well inside §7's 3 hours. The 3-hour stop is not in the code, but it is not needed at that speed.

**D7. Comparisons match. Holds.** The bet re-tests em-gm3c's label under a stated bundle of changes: stop rule, ten averaged assignments, BCa, 10,000 resamples and the link-free conjunct. No sentence attributes the result to any one of them. Ceiling, target and encoding are em-gm3c's (`gm3c_heldout_format` is imported unchanged). F4's statement order is balanced across the even and odd halves (`stmt_first`: three first and two second in each).

**D8. The verdict sentences are written. Flaw (F4).** All three sentences exist, but the pass sentence uses two nouns the design cannot carry:
- **"most of what each format reproducibly says".** The statistic is the mean over formats. In em-gm3c the rating format's Q was 0.53, above half, so "each" can be false while the mean is under 0.5.
- **"cannot be recovered from the other five formats".** Only two predictors are tried, and §6 itself says "a cleverer predictor could recover more".

**D9. One item cannot decide it. Flaw (F3).** Leave-one-item-out is pre-registered and implemented (`loo_items_shift_flips`, using jackknife Q shifted by the BCa bound's distance from the estimate). §5 does not say what a flip does to the verdict, and the "plain-English section" that §4 says will name the items does not exist in the output. `main()` writes only a bullet, and the frozen sentences are "used verbatim". In the matched worlds (D11), the largest single-item jackknife shift has a median of 0.023, and the third largest 0.014. The bound is expected to sit 0.01–0.02 from 0.5, so a flip is near-certain whichever way the verdict falls.

**D10. Machinery. Flaw (F5).**
- Holds: $0, no API path is reached (the `llm` client is created lazily and `g.run()` is never called); scale direction (0 = false, 100 = true, gm3b); the beacon rule (CURBY-Q stalled since 2025-08-22, so CURBy-RNG; pulse 1592268 at 13:24:00Z is the first after the commit at 13:23:16Z, and the previous pulse 1592267 at 13:23:00Z predates it; the seed commit touched only the pre-registration's beacon line); the lesson line ls-em-gm3cf1 matches §0, P10 and P3, odds 0.45 → 0.30 with v1 0.25, and the base rate 9/28 is the running (8+1)/(26+2).
- Holds: the script's `sys.path` puts this checkout's `src` first and asserts `config.RESULTS`. The venv's installed `entangled_mind` points at the old folder, but every module resolves here: `gm3b-calls.json`, `split-exp5.json` and `pool-run-3.json` all load from `programs/entangled-mind`.
- Flaw: the archive's sha256 is recorded but not pinned. `experiments/split-exp5.json` decides which 160 claims and 40 items exist, and it is neither recorded nor pinned. This checkout is shared with other sessions; em-dm6f2's review counted the same gap as a flaw (D63 F3).

**D11. The bet can both pass and fail. Flaw (F1). Below the floor, so redesign.** The archive is fixed, so P(pass) is uncertainty about where the fold-averaged, converged BCa bound lands. Seed noise is small: in my worlds, the seed-only SD of the K = 10 BCa bound is 0.003. I built the worlds from measured numbers (P15), as follows:
- **Structure:** 40 items × 4 claims, a shared latent with half its variance at item level, and six formats with format-specific variance either unequal (one weak format, as coin is at 0.18) or equal.
- **Calibration:** repeat noise sets ceilings near 0.9 (measured 0.88–0.97). Single-split Q is 0.38–0.45 and the upper end sits about 0.09–0.10 above Q (measured 0.398 [0.309, 0.501]).
- **Predictor:** the link-free predictor stands in for L1, with the same item folds, the same out-of-fold averaging and the frozen `bca()`.

For each dataset I computed the mean over four fold seeds of the single-split percentile upper end (2,000 resamples, as the audit did) and the frozen statistic (K = 10, 10,000 resamples, BCa). Then I conditioned on the audit's measured values (`d11_sim.py`, `d11_sim_homog.py`, `d11_condition.py`; 750 datasets):

| world set (datasets) | single-split upper in [0.497, 0.518] (measured spread) | kernel-weighted at 0.5075 ± 0.0055 | single-split upper in [0.495, 0.505] (original split only) | Δ = K10 BCa upper − single-split upper |
|---|---|---|---|---|
| unequal formats, two scales (500) | P(pass) 1.5% (n = 65) | 1.1% | 6.2% (n = 32) | +0.0093 (sd 0.0089) |
| equal formats (250) | 0.0% (n = 31) | 0.3% | 0.0% (n = 14) | +0.0111 (sd 0.0096) |
| all (750) | 1.0% (n = 96) | 0.8% | 4.3% (n = 46) | +0.0099 (sd 0.0092) |

Δ splits into two parts of similar size. Fold averaging raises Q by +0.005, and BCa adds +0.005–0.006 over the percentile upper end, with acceleration a > 0 in right-skewed worlds. Conditioned on the measured numbers, the K10 BCa bound lands at about 0.519–0.521 on average.

So the measured numbers put P(pass) for the L1 conjunct alone at about 1%, and the link-free conjunct can only lower it. Even keeping only the original split and ignoring the audit's three other fold assignments, P(pass) is 0–6% (4% pooled). It reaches about 24% only if averaging and BCa together had no net effect, against §0's own reasoning and em-gm3c's right-skewed interval. P(fail) is far above 10%. Caveat: the predictor is a proxy for L1. Its fold-to-fold spread (SD 0.008 of the single-split upper end) is close to L1's measured 0.011, but the size of L1's averaging gain is not measured here. Only a net negative shift of about 0.01 would lift P(pass) to the floor. The pre-mortem names this exact outcome ("BCa upper bound lands between 0.50 and 0.53"), and the 30% odds overstate the chance of a pass. Scored, this bet mostly buys the engine calibration on an outcome already visible in the parent audit (P12).

## Required fixes

Verdict **redesign**. Withdraw em-gm3cf1 before data (`ledger/bets.jsonl` `verdict: withdrawn`, a DEVIATIONS row naming this review), and do not run it. Any re-bet takes F2–F5 over.

1. **F1 (D11): P(pass) about 1% on the measured numbers (at most 0–6%).** On this 40-item archive, the 0.5 line cannot be resolved by removing noise, because the estimate itself sits there. Ways out, as a new pre-registration with a new lesson:
   - **(a) More items.** Run gm3b's six formats, the same prompts and Haiku, on a fresh set of contested items. At gm3b's cost of $0.41 per 40 items, 80 to 120 more items cost about $1–1.5. Pre-register the bound on the new items alone, or pooled. Interval half-widths fall by roughly √(n/40), so at Q ≈ 0.40–0.41 the bound would land near 0.46–0.48. Show P(pass) and P(fail) ≥ 10% in a committed dry run built from em-gm3c's measured Q and spread.
   - **(b) No bet.** Report the converged, fold-averaged estimate and its BCa interval from this archive as an unscored measurement.

   Do not move the 0.5 bar after seeing these numbers.
2. **F2 (D2): the stop rule is looser than the parent's.** Set `FIT_TOL = 1e-6` (gm3b's own tolerance) with `MAX_ROUNDS = 2000`, so the only change from gm3b is the cap. Record each fit's last-round max |Δμ| and report the largest. Rewrite §2's convergence line to match.
3. **F3 (D9): say what a flip does.** Add to §5: "The verdict is computed as above whatever the leave-one-item-out check shows. If one or more items flip the label, the verdict sentence is followed by: 'This label is fragile: removing item(s) <ids> alone would move the BCa upper bound across 0.5.'" Make `main()` print that sentence.
4. **F4 (D8): pass-sentence nouns.** Replace the pass sentence with: "On Haiku's 160 claims, averaged over the six formats, most of what a format reproducibly says is not recovered from the other five by the one-credence model (the whole BCa interval of mean Q is under 0.5) or by a link-free least-squares predictor (mean Q under 0.5). Some formats may be recovered better than others; a more flexible predictor could recover more."
5. **F5 (D10): pin the inputs.** Pin the sha256 of `results/gm3b-calls.json` (`0a5a27a4fda3b66285148a238cd41293a0ddb5fd44bcd85ce29fbf4b247d84b9`) and of `experiments/split-exp5.json` in the code. Make §7 read: "If either file's sha256 differs from the pinned value, the run stops before any analysis."

**Recommendation (not counted as a flaw).** R1: a NaN in either conjunct should read untestable, not fail.

Scripts and logs: `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/e93ce59f-1dc3-4451-8206-bee8c0537bfa/scratchpad/review-gm3cf1/`:
- `time_fit.py`, `time_fit.log`: the two real fits;
- `synth_checks.py`, `synth_checks.log`: D1–D3;
- `selftest.log`;
- `d11_sim.py`, `d11_sim_homog.py`, `d11_condition.py`, `d11_sim_*.log`: D11.

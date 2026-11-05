---
bet: em-bm9f2
program: entangled-mind
prereg_commit: cd534d9
reviewer_session: fresh design-review subagent, main checkout, 2026-11-05 (seed commit 527e239 also read)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 07:10 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: holds, D6: holds, D7: holds, D8: flaw, D9: flaw, D10: holds, D11: flaw}
flaws: 3
pilot_usd: 0.00
verdict: fix-first
confirmed_at: 2026-11-05 07:16 America/Denver
---

# Design review of em-bm9f2

## In plain English
As built, the test can come out either way, but a pass would be weak evidence, and the pre-registration does not say so.

The pre-registration's power figures assumed evenly spread gaps and a small noise level (σ = 8). The real gaps are bunched: 30 of the 80 pairs have a gap under 10 points and 16 are over 70. The noise implied by em-bm9's own published intervals is about 23–28 points. At those values, the rule passes:
- 17–35% of the time in the design's own DoG world;
- 8–19% of the time in DoG worlds with a human-sized pull;
- 2–10% of the time in levelling-off worlds that match em-bm9's slope.

So a pass is only about two to three times likelier if the human shape is true than if it is not. Tightening the bar does not help: at ΔAIC ≥ 4 against tanh, human-sized worlds pass only 3–7% of the time.

Three fixes are needed, and none changes the test:
1. Record the measured power and false-pass rates (and revise the odds if the author wishes).
2. Reword the verdict sentences. They use "the pull … toward the sub-rating just given", a noun em-bm9's audit showed this statistic cannot carry.
3. State what happens to the label if leaving out one item flips it.

## What I ran on real data (and what I did not)
All runs used `/Users/seanpharris/entangled-mind/.venv/bin/python` from `programs/entangled-mind`. Scratch is in `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/e93ce59f-1dc3-4451-8206-bee8c0537bfa/scratchpad/review-bm9f2/`. No API call and no local model was used.

- **Paths.** `entangled_mind`, `exp5_run` and `bm_offline` all resolve to this checkout, because the script puts `src/` ahead of site-packages. `bo.CONV1`, `er.SPLIT` and `er.POOL` point to `oversight-testbed/programs/entangled-mind/{results,experiments}/…`, and results would be written to this checkout's `results/`. Nothing points to `/Users/seanpharris/entangled-mind`.
- **Unchanged since the pre-registration.** The code (`bm9f2_dog_shape.py`, `bm_offline.py`, `exp5_run.py`, `src/`) and the three archive files have not changed since cd534d9 (`git diff 527e239 HEAD` is empty). Other sessions' uncommitted edits to `bets.jsonl`, `lessons.jsonl` and the map do not touch bm9-f2.
- **The pre-registered power command, three times.** `--power {28,14,8} --L-from-archive`, 300 simulations each. This reads L and C. `load()` builds d inside `bm9_pairs` and discards it unread.
- **`gaps.py`.** It keeps only columns 1–2 (L, C) of `bm9_pairs`. It derives the mean S (= 50 + 50·C·sign(lean)) and the mean M-first (= S − L) from them and the claims' lean signs. The 40 × 2 claim-pair alignment was checked.
- **`spread.py`.** It reads only the within-order spread: per pair, the SD of the 20 M ratings in each order and of the S ratings. No order means were differenced, and d was never formed.
- **What I did not do.** I did not run with `--seed`, did not fit the three models to the real d, and computed no statistic of d.

**Real gaps.**
- n = 80 pairs from 40 items, 20 conversations per order in every pair.
- |L| runs from 0.00 to 97.35. Three pairs have |L| = 0, the median is 16, the quartiles are 4.4 and 58.1, and 69% of the pairs have L > 0.
- Counts by band: |L| < 10: 30; 10–40: 26; 40–70: 8; ≥ 70: 16. Only 9 pairs have L < −10.
- The ratings sit at the extremes. The mean S has median 51.0 and the mean M-first has median 13.9; for both, the 10th percentile is about 3–6 and the 90th about 97.

**Choice of σ.** The residual SD around d = a + c·C + f(L) is taken from em-bm9's published intervals together with the real L and C:
- from the β interval: SE 0.081 × √Σ(L residualised on C)² = **28.0**;
- from the γ interval: **23.4**.

I used σ = 23, 25 and 28. The within-order spread gives a per-pair sampling SD of d of only 3.3 (RMS; median 1.3). That is a floor that leaves out item-to-item variation, and em-bm9's intervals show that variation is about seven times larger. So σ = 8 (the self-test's value) is not defensible for these pairs (P15).

## Checks

**D1 (stranger can apply the rule): holds.**
- `verdict()` returns exactly one of untestable, pass or fail. The self-test's boundary asserts land correctly at n = 59, at ΔAIC values just below 4 and 2, at a peak on the edge, and at A < 0.
- `--selftest` printed SELFTEST OK: DoG → pass, linear → fail, tanh → fail at σ 2.
- Note: the real min |L| is exactly 0, so the lower half of "peak strictly inside the observed |L| range" can never bind (the smallest possible peak is 3/√2 = 2.1). The condition is in effect peak < 97.35, which means w < 137.7.

**D2 (manipulations take effect): holds.**
- σ, world and gap source each move the output. With real gaps, the DoG world's P(pass) is 0.96 at σ 8, 0.69 at σ 14 and 0.20 at σ 28. With uniform gaps it is 1.00 at σ 8.
- The run's parameters match §2 and §4:
  - grid: log grid of 400 values from 3 to 400;
  - bars: 4 and 2, with tolerance 1e-9;
  - 10,000 resamples; minimum 60 pairs;
  - AIC = n·log(RSS/n) + 2(k+1), with k = 3 and 4;
  - anchor (a) only, run 1 only, item-cluster resampling.
- The seed 965198064319072892 is below 2^63, so `seed % 2**63` leaves it unchanged.

**D3 (controls can fail): holds.** The rule rejects every wrong set-up it must reject (pass rates at σ 23–28, 1,000 simulations):
- linear 0.27: 0.003;
- null f = 0: 0.023–0.026;
- em-bm9 audit's decomposition with no DoG (d = −0.374(M-first − 50) + 0.125(S − 50)): 0.015–0.018;
- design tanh: 0.046–0.060.

The false-pass rates in levelling-off worlds are judged under D11.

**D4 (rivals matched): holds.**
- DoG and tanh have the same count (four mean parameters), the same w grid and the same nuisance terms (intercept and content).
- Large-w tanh nests the line almost exactly. Large-w DoG is within 6% of the line at |L| = 97.
- Neither wins by construction. In the null world all four conditions pass together only 2–3% of the time.

**D5 (dumb baseline beaten): holds.** The dumb rivals (constant, straight line) are built into the rule, and their worlds pass ≤ 3%. This is not a no-difference rule.

**D6 (execution risk): holds (not applicable).** There are no calls, and the pre-mortem is of kind `design`.

**D7 (comparisons match): holds.**
- All three models are fitted to the same 80 d values with the same C.
- SM and MS differ only in order: same items, model, run, anchor and claim pairs.
- The confound that d and L share −M-first is a question of what the statistic means, not a mismatch between conditions. It is handled under D8.

**D8 (verdict sentences): flaw (F2).**
- Both sentences call the quantity "the pull of the main rating toward the sub-rating just given". em-bm9's audit (`ledger/audits/em-bm9.md`, hole 1) showed that d against L is mostly M being less extreme after S, not a pull toward S. The S coefficient is +0.13 [−0.04, +0.28].
- §6 admits this, but the frozen sentences still use the overclaimed noun (P9).
- The fail sentence's "a straight-line or levelling-off pull describes it as well" is false for some fails. Examples: a fail with ΔAIC vs tanh of +1.9, or one that fails only on A < 0 or on the peak position.

**D9 (one item cannot decide): flaw (F3).** Leave-one-item-out is pre-registered and the flipping items are listed, but §5 does not say what happens to the label when one item flips it. P10 requires that.

**D10 (machinery): holds.**
- Budget $0, with no call path in the script. Importing `exp5_run` only runs `load_dotenv`.
- One scale direction. The archive sha256 is recorded, as §7 says.
- Beacon: CURBY-Q is stalled, and CURBy-RNG pulse 1592298 (13:54:00Z) is the first after the commit (13:53:49Z). I recomputed SHA-256(randomness ‖ "em-bm9f2" ‖ ":bootstrap")[:8] = 965198064319072892, which matches.
- The lesson `ls-em-bm9f2` in `lessons.jsonl` matches the text in §0 word for word (its 62 words are noted).
- The tightening of the map's odds event (adding the tanh rival and A > 0) is logged in D67.

**D11 (can pass and can fail): flaw (F1).** P(pass), 1,000 simulations per cell (Monte Carlo SE ≤ 0.015), real L and C, a = −5 and c = +7.7 as in the code. "Base" is the em-bm9 audit's M-first term −0.374(M-first − 50). Adding it lets the worlds reproduce em-bm9's β; without it, the design's DoG world implies β = +0.03, against the published +0.27 [+0.11, +0.43].

| world | implied β | σ 23 | σ 25 (bar t = 2 / 4) | σ 28 |
|---|---|---|---|---|
| design DoG (A 0.9, peak 20), as in `--power` | +0.03 | 0.345 | – | 0.237 (pre-registered command, 300 sims: 0.20) |
| base + design DoG | +0.25 | 0.212 | 0.173 / 0.074 | 0.182 |
| base + DoG, peak 30, human ratio 0.30 | +0.26 | 0.186 | 0.168 / 0.062 | 0.173 |
| base + DoG, peak 20, human ratio 0.30 | +0.23 | 0.102 | 0.117 / 0.055 | 0.122 |
| base + DoG, peak 25, human ratio 0.15 | +0.23 | 0.078 | 0.087 / 0.028 | 0.101 |
| design tanh (10·tanh(L/25)) | +0.14 | 0.060 | – | 0.046 |
| base + design tanh | +0.35 | – | 0.032 / 0.005 | – |
| tanh, w 10, matched to β 0.27 | +0.27 | 0.082 | 0.074 / 0.026 | 0.101 (300 sims: 0.137) |
| tanh, w 5 / w 25, matched to β 0.27 | +0.27 | – | 0.061 / 0.068 | – |
| audit decomposition, no DoG | +0.27 | 0.015 | 0.008 / 0.003 | 0.018 |

"Ratio" means the peak shift divided by the gap at the peak.

**Is the design's DoG world a plausible "hypothesis holds" world?**
- **Width: yes.** A peak at 20 on gaps up to 97 matches human orientation peaks of 17–28° out of 90° (`biomimetic-map.md` §3.2), which scale to about 19–31 points.
- **Amplitude: no, it is large.** At the peak it shifts M by 10.9 points on a gap of 20, a ratio of 0.55. Human values in §3.2 run from about 0.07 (Fritsche 2017: 1.1–1.3° at 17°) to about 0.29 (Fischer & Whitney: 8.19° at 28°). The design's world is therefore about two to eight times human.
- **On its own, it contradicts em-bm9's β.** It becomes archive-consistent only once the M-first term is added. In that form it is a fair upper case, at 17–21%.
- **Human-sized worlds** pass 8–19% of the time.

**Is the false-pass rate in a levelling-off world acceptable?**
- Levelling-off worlds that match em-bm9's β pass 3–10% of the time (6–8% typical). That is about half of what human-sized DoG worlds give, so a pass has a likelihood ratio of roughly 2–3.
- At the engine's 8% odds, a pass would take the probability to about 15–20%. Most passes would be false ones.
- This is acceptable only if the record and the pass sentence say so. It is not grounds for a stricter bar: raising the tanh bar to 4 halves the false passes, but it also pushes every human-sized world below the 10% floor (2.8–6.2%).
- P(fail) is ≥ 0.65 in every world. So D11's floor is met, just, in the design's world and at the top of the human range, and narrowly missed in the middle of the human range (8–10%).

The flaw is that §0 and §2 justify keeping the bet open with numbers this check refutes:
- "in the self-test's DoG world, the rule passes reliably" (true only at σ 8 with uniform gaps);
- "falsely passes about 7%".

Neither the source of σ nor the amplitude is stated beside the world (P15).

## Required fixes
Each needs one dated DEVIATIONS row in `programs/entangled-mind/DEVIATIONS.md` (for example, D69 "em-bm9f2 design review fixes"), written before any data and naming this review. None lowers a bar.

**F1 (D11, P15): record the measured power and false-pass rates.** Add this review's table to the DEVIATIONS row, with its sources: σ 23–28 from em-bm9's published γ and β intervals with the real L and C; the human amplitude ratios from §3.2; the base term from em-bm9's audit. Replace the §0 sentence "in the self-test's DoG world, the rule passes reliably, and in a levelling-off world it falsely passes about 7%" with:

"At the real gaps and the noise implied by em-bm9's intervals, the rule passes 17–35% of the time in the design's DoG world (two to eight times the human pull), 8–19% in human-sized DoG worlds and 2–10% in levelling-off worlds matched to em-bm9's slope (design review em-bm9f2)."

The engine odds may be revised before data, with both numbers kept. An overall pass rate of about 6–8% is consistent with these figures. Optionally, and only as a tightening: fail when the DoG's w sits at the grid's lower edge (w = 3, peak 2.1), since such a fit is a spike at near-zero gaps, not a tuned pull.

**F2 (D8, P9): reword the verdict sentences** so that they name what is measured. Keep the same rule.

- pass: "On Haiku's 80 archived sub-question and main-question pairs, the shift in the main rating after a sub-question, plotted against the gap between the sub-rating and the unprompted main rating, was best fitted by the derivative-of-Gaussian shape seen in human serial dependence: it grew with the gap up to a peak inside the observed gaps and then shrank, beating a straight line and an equally flexible curve that only levels off. At these gaps the rule also passes in about 2–10% of levelling-off worlds, and much of this shift is the main rating becoming less extreme after a sub-question rather than a pull toward the sub-rating (em-bm9 audit)."
- fail: "On Haiku's 80 archived pairs, the shift in the main rating after a sub-question was not shown, by the pre-registered rule, to have the derivative-of-Gaussian shape seen in human serial dependence; the rule did not separate it from a straight-line or levelling-off relation to the gap."

Change the docstring and `SENTENCES` in the code to match, in the same commit as the DEVIATIONS row.

**F3 (D9, P10): state the one-item consequence in §5.** Add:

"If leaving out any single item turns a pass into a fail, the verdict is reported as 'pass, unreplicated, rests on one item (<id>: plain-English name)', and the pass sentence is followed by 'This rests on one item, <name>.' A fail that one item would turn into a pass stays a fail, and the item is named."

In the code, set `r["verdict_note"]` and append the clause when `loo_item_flips` is non-empty and the verdict is pass.

VERDICT: fix-first (3)

## Addendum: confirmation of fixes (2026-11-05 07:16 America/Denver)

I read commit `a4639af`: the DEVIATIONS row D72 and the diff of `experiments/bm9f2_dog_shape.py` against cd534d9. The pre-registration file is unchanged since the seed commit, so D72 is the record of the changes. HEAD's script is identical to the version in `a4639af`. As before, I did not run `--seed` and did not fit the models to the real d.

**F1: holds.**
- D72 swaps the §0 sentence for the measured one, word for word, and states each source: σ 23–28 from em-bm9's intervals, the human ratios from §3.2, and the base term from em-bm9's audit.
- It records the full P(pass) table and the likelihood ratio of about 2–3. The odds stay at 0.08, which these figures support.
- The optional tightening is in the code: a DoG whose w is at `W_GRID[0]` (equal to 3, peak 2.1) now fails. The check uses the same tolerance as the other conditions (P13). `fit_shape` returns w from the grid, so a real fit at the edge does trip it. The bootstrap pass share and leave-one-item-out both call `verdict()`, so the tightening reaches them too.
- A new self-test assert confirms it: w = W_GRID[0] fails and w = 28.3 passes.
- I re-ran `--selftest` (SELFTEST OK, every earlier boundary unchanged) and `--power 25 --L-from-archive` (300 simulations). P(pass) was 0.26 in the DoG world, 0.003 in the linear world and 0.047 in the tanh world, in line with the D11 table. The tightening can only lower these rates.

**F2: holds.** The pass and fail sentences in `SENTENCES` and in D72 match the review's text exactly. Both now describe the shift in the main rating against the gap, not a pull toward the sub-rating. The pass sentence carries the 2–10% false-pass rate and the em-bm9 audit caveat. The fail sentence no longer says "describes it as well".

**F3: holds.**
- D72 adds the one-item rule to §5.
- The code sets the label to `verdict_note` = "pass, unreplicated, rests on one item (…)" and appends "This rests on one item, …" to the pass sentence. The results heading uses that label.
- If a fail would flip to a pass with one item left out, the result stays a fail and the item is named.

**Note for the run write-up (not a flaw).** The script names items by id only. In the hand-written plain-English section of `results/bm9f2-dog-shape.md`, give each id's plain-English name, as §4 and D72 require. If several items can each flip a pass on their own, write "rests on any one of …" rather than "one item".

CONFIRMED: yes

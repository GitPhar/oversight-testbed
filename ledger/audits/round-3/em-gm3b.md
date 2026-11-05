---
bet: em-gm3b
program: entangled-mind
prereg_commit: 34eb191
results_commit: 1fd521d
round: 3
verdict_round1: pass (stands; 11 cuts)
verdict_round2: not re-audited (round 2 touched only the Sonnet/Opus replications, em-dm2)
auditor_session: round-3 auditor fork (parent session 4f777718), stripped clone at scratchpad/clone-p1b checked out at 1fd521d
auditor_model: claude-fable-5-1
author_model: claude-opus-5-5
same_model_family: true          # same vendor (Anthropic), a different and stronger model; rounds 1 and 2 were same-model
date: 2026-11-05 05:30 America/Denver
claims_checked: 14
holes_found: 2
overclaims_cut: 2
reproduced: true                 # own fitter: mean dLL +19.41 [+16.53, +22.09], 86.3% of claims (archive: +19.36 [+16.50, +22.08], 85.6%)
verdict_claimed: pass
verdict_after_audit: pass
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: []         # pre-registered before the design-review rule; a held-out-format criterion and a one-bit baseline would have been the D9 asks
failed: false
failure_reason: "None: the pre-registered reading was met. Had it failed, the likeliest reason would have been that Haiku's repeats vary so little that a per-format latent overfits noise; the opposite is what happened. Kind design."
failure_kind: null
premortem_score: null            # pre-registered before operators/premortem.md
risk_seen: null
---

# Audit of em-gm3b (round 3): six elicitation formats, one credence or six?

## In plain English

The pass stands, and a stronger auditor found nothing that round 1 missed on the number. I refit both models from the 9,600 archived calls with my own fitter, run to convergence: the format-specific model beats the one-credence model by +19.4 held-out log-likelihood units per claim [+16.5, +22.1] on 86% of the 160 claims, and no single item flips the pre-registered rule. The one new check is the one-bit baseline that reversed the Opus reading in round 2: on Haiku a one-bit (yes/no verdict) latent is much worse than the graded one-credence model (−12.6 per claim), so Haiku's data are graded, and the format disagreement is not an artefact of a binary verdict dressed as a credence. Without the two oddest formats (the coin comparison and the frequency question) the separate-credence model still wins by +11.6 [+9.7, +13.5] on 91% of claims. Two sentences still outrun the test: "There is no single belief to read out" (the follow-up em-gm3c finds about 40% of each format's reproducible signal is shared) and the by-format table, which my converged fit moves by up to a third. The bet's outcome (hit at 0.25) is correct.

## The case that this result is false

Assigned the other side: the format-specific model has 960 free latents against 160, so it should win any held-out-repeat contest in which Haiku's answers are reproducible at all, whether or not the thing reproduced is a "credence". Haiku repeats itself almost exactly, so the test's criterion (held-out repeats) rewards any reproducible format-by-claim quirk, including pure response biases that are not monotone in a shared latent: the coin comparison is picked 79% of the time at a mean rating of 55, and the frequency question ("100 statements like this one") is not even a question about this statement. Strip those two formats and the result might vanish. Worse, round 2 showed that on Opus a one-bit predictor passes the single-credence bar; perhaps on Haiku the formats agree on a verdict and disagree only in how graded their output is, in which case a per-format link that is monotone but not of the fitted parametric form (a 2-parameter logit, a Normal on logit scale) could absorb it. Finally, the headline rests on a block-coordinate fit that round 1 showed was not converged, and the pass rule was written against a parameter count the authors chose. On this reading, "no single credence" is a statement about an under-specified link family, not about Haiku.

What survived the checklist: nothing in this case. The parameter-count worry was answered in round 1 by simulation (one-credence data make L6 lose) and by flexible ordinal links (+17.7). The two odd formats are not carrying it (+11.6 without them). The one-bit worry runs the other way on Haiku: a one-bit latent is far worse than the graded one. The converged fit changes the per-format table, not the headline.

## Claims checked

| # | claim | check run | outcome |
|---|---|---|---|
| 1 | mean ΔLL +19.36 [+16.50, +22.08]; 86% of claims > 0 | own fitter (`r3/gm3b_refit.py`), 400-round coordinate ascent to 1e-9, seed 3131 | holds: +19.41 [+16.53, +22.09], 86.3% |
| 2 | totals L1 −10438.3, L6 −7341.4 | own fit | holds: −10446.2, −7341.3 |
| 3 | pre-registered rule: >50% positive and CI above 0 | §6 of 34eb191 vs results | holds, word for word; reading "no single credence" follows |
| 4 | by-format ΔLL table (F1 +3.75 … F6 +3.51) and slopes | converged fit | **differs** (F1 +4.04, F5 +6.17, F6 +3.06; F6 slope 4.32 against 3.23): the file's own caveat already says the table depends on the optimiser; my numbers added to it |
| 5 | leave-one-item-out: no flip | own fit, 40 drops | holds |
| 6 | result not carried by F4 (coin) and F5 (frequency) | ΔLL over F1, F2, F3, F6 only | holds: +11.56 [+9.74, +13.45], 90.6% |
| 7 | a one-bit verdict does not explain Haiku's formats (round-2 Opus artefact) | one-bit latent (sign of train-fold yes/no share) with fitted per-format links | holds: L1 beats one-bit by +12.62 [+9.04, +16.02] per claim, 82.5% of claims; total −12464.8 against L1 −10446.2 |
| 8 | per-format wins | own fit | every format's ΔLL CI above 0; F2 (yes/no) weakest, positive on 63% of claims |
| 9 | "There is no single belief to read out" (results:21) | em-gm3c: Q = 0.39 [0.30, 0.50] of each format's reproducible signal is recoverable from the other five | **overclaim**: a shared component exists; cut 1 |
| 10 | "No fixed distortion explains that" | logical: per-format links are monotone; the per-claim order reverses | holds |
| 11 | coin comparison 79% vs mean rating 55 | archive `format_means` | holds |
| 12 | 12–25% of pairs in opposite order; noise 1–5% | round-1 recomputation, re-read | holds (round 1's correction is applied) |
| 13 | paper :23 "Formats disagree … for 86% of 160 statements" | paper | holds, scoped to Haiku in the next block; :308 table and :313 note give the 80-claim re-analysis |
| 14 | paper :32 "Kendall's W 0.56 / 0.76 / 0.87 on the same 68" | em-dm2, D49 record | not recomputed here (em-dm2's audit) |

## Checklist

**A.** 1 holds: pre-registration 04:02:49, first call 04:41 (decoded in round 1), result 05:02. 2 holds: statistic, split (even/odd repeats), bootstrap (2,000 over 40 items, seed 3131), prior and rule match 34eb191; the fitting code was in the pre-registration commit. 3 holds: no bar moved. 4 holds: the primary is the pre-registered mean ΔLL and share.
**B.** 5 holds: no ties in ΔLL; the share is 0.86 against a 0.5 line and the CI lower bound 16.5 against 0. 6 holds: pooling over formats is the design; unpooled every format is positive (claim 8). 7 holds: no LOO flip; the smallest LOO mean is 18.9. 8 holds: nothing fitted on the held-out repeats; L6's latents are penalised by the held-out criterion, and round 1's one-credence simulation shows the criterion does not favour L6 by construction. 9 holds, strengthened: the one-bit baseline (claim 7) is far below L1 on Haiku, so the Opus artefact does not transfer. 10 holds: item-level CI. 11 holds: one primary. 12 holds.
**C.** 13 holds in the results file and the paper (Haiku named). 14 holds. 15 hole: "no single belief to read out" (cut 1). 16 hole: the by-format table is from an under-converged fit (already caveated; my converged numbers added, cut 2). 17: Smolin & Wilder not opened (as in round 1). 18 holds.
**D.** 19 holds ($0.41 of $1). 20 holds (no refusal; 9,600 of 9,600 keys). 21 holds (one scale direction, the reversed scale replaced by a verbal scale). 22 holds in the ledger (scored on Haiku; replication em-dm2 mixed, Opus contradicted) and in the paper's "holds for Haiku, partly for Sonnet, contradicted on Opus".
**E.** 23 n/a (seed 3131 chosen by the session, before the beacon rule). 24 n/a. 25 n/a (before learn.md). 26 n/a (before design-review.md).

## The pre-mortem, scored

None written (pre-registered before operators/premortem.md). My own line, had it failed: Haiku's near-deterministic repeats would have made per-format latents overfit noise. Kind design. `premortem_score: null`.

## Required cuts

1. `results/gm3b-format-invariance.md:21`: "**What we found.** There is no single belief to read out." → "**What we found.** No single belief, read through a fixed lens per format, reproduces the answers; the follow-up (`gm3c-heldout-format.md`) finds that about 40% of each format's reproducible signal is still shared." **Applied.**
2. `results/gm3b-format-invariance.md`, the under-converged-fit caveat: add my converged numbers (F1 +4.04, F2 +2.08, F3 +2.37, F4 +1.67, F5 +6.17, F6 +3.06; F6 slope 4.32 on fold 0) and the round-3 one-bit and without-F4/F5 checks. **Applied.**

The paper (`paper/no-credence-to-read.md`) needs no cut for this bet: its format claim is scoped to Haiku, cites the exploratory noise baseline as exploratory, and reports Q = 0.39 beside it.

## What would break it next

A held-out-*format* criterion is already run (em-gm3c, undetermined at the 0.5 line). The cheapest new test, about $0.40: the same six formats on 160 *uncontested* statements (Haiku rating under 20 or over 80 in a pilot), where a graded single credence has nothing to disagree about; if L6 still wins by a wide margin, the disagreement is response style, not an absent credence. Scripts: `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/4f777718-cc86-43e1-837e-ef53cbe2abaf/scratchpad/r3/gm3b_refit.py` (output `r3/gm3b_out.json`), run with program 1's venv interpreter under `-I` on the stripped clone.

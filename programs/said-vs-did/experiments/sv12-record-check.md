# SV-12: the record check that parked it before pre-registration

Written 2026-11-05 by the remap-p67 session (claude-opus-5-5), which drafted SV-12's pre-registration and did not commit it. No archive was opened: no concordance was computed on program 1's calls. The code is `experiments/sv12_refit.py` (numpy only): the single-latent refit, Harrell's concordance on held-out formats, and the synthetic worlds below.

## In plain English

SV-12 asked whether program 1's finding, that Haiku holds no single belief across six ways of asking, goes away under Smolin and Wilder's looser scoring. The draft rule was a held-out-format concordance of at least 0.85, clearly above a one-bit trivia guess. Before pre-registering, the session checked which outcome the record already implies, applying the standard the sv-b4 design review had just set (fix 1(e): some world within about two standard errors of the published numbers must give P(pass) ≥ 0.10, else withdraw).

Program 1's follow-up gm3c already predicted each format from the other five on the same archive. The Spearman between prediction and held-out answer was 0.76, 0.63, 0.64, 0.41, 0.54 and 0.73 by format (mean 0.62); mean R² was 0.37, 95% interval [0.28, 0.47]. In simulated statements that reproduce that agreement, the concordance comes out about 0.75 to 0.78, and the rule passes 0% of the time. It reaches 10% or more only where cross-format agreement is about 0.79 or higher, well outside the record.

So a bet on SV-12 could not pass on this archive (pattern P12). Scoring it would buy a Brier point without information. **SV-12 is parked, unscored, and not pre-registered.** What the record says, without a bet: by this check, Haiku's cross-format agreement implies a concordance near 0.77, below the 0.8 to 0.95 Smolin and Wilder report for capable models on group holdouts. This estimate comes from simulation, not a measurement on the calls. Sean's cockpit odds (0.60, `ho-20261105-061152-zxv`) stay on the line, not scored.

## The worlds (synthetic, 160 statements in 40 questions, 21 trivia, ten repeats; 40 simulations each; question type carrying little)

| τ (statement-by-format deviation) | simulated mean cross-format Spearman | mean concordance (SD) | P(pass) |
|---|---|---|---|
| 0.0 (one belief) | 0.90 | 0.911 | 1.00 (100 simulations) |
| 0.6 | 0.81 | 0.857 (0.011) | 0.73 |
| 0.7 | 0.79 | 0.847 (0.012) | 0.48 |
| 0.8 | 0.75 | 0.828 (0.013) | 0.03 |
| 0.9 | 0.72 | 0.811 (0.015) | 0.03 |
| 1.0 | 0.66 | 0.783 (0.019) | 0.00 |
| 1.2 | 0.58 | 0.748 (0.019) | 0.00 |
| **the record (gm3c)** | **0.62** | (between τ 1.0 and 1.2: about 0.75–0.78) | **0.00** |

Rule as drafted: macro concordance ≥ 0.85, margin over the trivia guess ≥ 0.10 with a 95% question-bootstrap interval above 0 (100 resamples in these worlds). The τ = 0 row is from the first full dry run (100 simulations); the others come from `sv12_refit.run_world` at the seeds in the session's grid script (τ × 1000 + 7).

## What would reopen it

A new reason the diagnosis does not cover. For example, a format set or item set on which program 1's cross-format agreement is not already published, or a pre-registered group holdout (Smolin and Wilder's own setting) with a bar taken from their group-holdout figures. A bar lowered to sit at the record's implied value would make a coin flip, not a test, and is not proposed.

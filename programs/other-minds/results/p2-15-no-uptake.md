# P2-15 results: do Haiku's predictions of its own re-ratings beat a guess of "no effect"?

Bet `om-p2-15`, pre-registered at `47bea8c` (`experiments/p2-15-no-uptake.md`, DEVIATIONS D17), seeded at `ad3779e`, design review fix-first (`304d682`) with fixes D17b and D17c confirmed (`46de7ff`), analysis run on the archive at 10:23 America/Denver on 2026-11-05, one code fix to four secondaries after data (D17d; the primary is byte-identical). Archive only: no model was called, $0.

## In plain English

**The question.** When Haiku is shown a conversation in which a number was planted as its own earlier answer (or as another person's), and asked what rating it would give next, is its prediction closer to what it actually gave than the plain guess "the number has no effect, it gives its usual rating"?

**The answer, by the pre-registered rule: no, not detectably.** Across the 324 cells, Haiku's predictions of its own re-ratings missed its real re-ratings by 9.17 rating points on average. The "no effect" guess missed by 8.85. The difference, +0.33 points, has intervals running from about −3 to about +4 (BCa [−3.08, +4.07]; jackknife-t [−3.76, +4.41]). So this test did not show that its self-predictions beat assuming no effect, cell by cell. Leaving out any one of the 16 vignettes does not change that.

**Where it was right and where it was wrong** (secondary, not pre-registered as findings, uncorrected):
- When the planted number was presented as **its own earlier answer**, its self-predictions were better than "no effect": 5.1 points of error against 8.9 (difference −3.9, BCa [−7.0, −1.5]).
- When the number was presented as **another person's estimate**, they were worse: 13.3 against 8.8 (+4.5, BCa [−0.3, +10.4]). Haiku predicted it would move toward another person's number far more than it actually did, most of all when that number was 60 points away (average predicted uptake −0.34 against −0.13 measured at that distance).
- The two cancel, so on all cells together it was no better than the guess.
- **The average pattern is a different matter.** Averaged into om-p2-4's six condition-level effects, Haiku's self-predictions are much better than "no effect" (error -0.233 in uptake units, BCa [-0.387, -0.157]). Its own-answer effects are within 0.03 of the truth. Its knowledge of how it reacts is good on average and poor cell by cell. The design review flagged before data that this effect-level reading would almost certainly pass (D17b, F2); the bet was on the cell-by-cell reading.
- **"Sam" did better than "self".** The same transcripts labelled as another AI's ("Sam") were predicted with 7.2 points of error, against 9.2 for the self label (self minus Sam +1.96, BCa [+0.27, +3.87]). On this archive, at 5 repeats, Haiku predicted another assistant's re-ratings more accurately than its own. This is exploratory and is P2-14's question; P2-14 has its own design and margin.

**What this cannot say.** One model, one task (a shown number's pull on 16 short probability vignettes), one prompt. Self-prediction here is "you, in a fresh context, reading the transcript", not memory. The fail is "did not show", not "no better than no effect"; the intervals allow anything from 3 points better to 4 points worse.

**The odds.** Engine 0.10 (prior 0.32, adjustment −0.22, re-stated before data on the fixed design; 0.18 at pre-registration; the map's 0.55). Sean's 0.70 was given on a card framed by om-p2-4's effect-level numbers; under that framing the bet would almost certainly have passed (`card_event_effect_level_pass`: true, recorded beside the outcome); he is scored on this bet's outcome, as rule H1 requires.

## Tables

Verdict: **fail**. The pre-registered event did not occur. On Haiku, across the 324 uptake cells, the model's predictions of its own re-ratings missed its measured re-ratings by 9.17 rating points on average, against 8.85 for a guess that the shown number has no pull; the difference is +0.33, 95% BCa interval [-3.08, +4.07] and 95% jackknife-t interval [-3.76, +4.41], not both wholly below 0. This test did not show that its self-predictions beat assuming no effect. This is about its cell-by-cell shifts, not the average pattern of shifts across conditions. Leaving out any one of the 16 vignettes leaves the label unchanged.

## Primary: mean absolute error in rating points over the uptake cells, self-prediction minus no-uptake

| cells | MAE self (a) | MAE no uptake | difference | 95% BCa | 95% jackknife-t | 95% percentile | share of resamples < 0 |
|---|---|---|---|---|---|---|---|
| 324 | 9.174 | 8.846 | +0.329 | [-3.075, +4.075] | [-3.756, +4.414] | [-3.196, +3.928] | 0.432 |

## Secondary (reported, never promoted)

| comparison | cells | MAE first | MAE second | difference | 95% BCa | 95% percentile |
|---|---|---|---|---|---|---|
| self vs no uptake, own | 162 | 5.061 | 8.927 | -3.867 | [-7.015, -1.475] | [-6.689, -1.244] |
| self vs no uptake, other | 162 | 13.288 | 8.764 | +4.524 | [-0.271, +10.385] | [-0.546, +9.900] |
| self vs no uptake, |d|=10 | 100 | 6.142 | 9.898 | -3.756 | [-6.746, -1.054] | [-6.727, -1.037] |
| self vs no uptake, |d|=30 | 112 | 9.056 | 9.759 | -0.703 | [-5.216, +4.184] | [-5.354, +4.043] |
| self vs no uptake, |d|=60 | 112 | 12.000 | 6.993 | +5.007 | [+0.951, +9.127] | [+0.920, +9.103] |
| self vs no uptake, uptake units (om-p2-4's unit) | 324 | 0.459 | 0.548 | -0.088 | [-0.321, +0.108] | [-0.306, +0.119] |
| Sam (b) vs no uptake | 324 | 7.219 | 8.846 | -1.627 | [-5.552, +0.811] | [-4.913, +1.227] |
| one-line observer (c) vs no uptake | 324 | 13.427 | 8.846 | +4.581 | [+2.141, +6.850] | [+2.247, +6.942] |
| copy vs no uptake | 324 | 23.209 | 8.846 | +14.363 | [+9.999, +18.202] | [+10.330, +18.431] |
| self vs copy | 324 | 9.174 | 23.209 | -14.035 | [-16.308, -12.305] | [-16.224, -12.275] |
| self vs Sam | 324 | 9.174 | 7.219 | +1.956 | [+0.270, +3.866] | [+0.135, +3.711] |
| measured-effect oracle vs no uptake | 324 | 9.774 | 8.846 | +0.928 | [-0.403, +2.329] | [-0.411, +2.324] |
| self vs measured-effect oracle | 324 | 9.174 | 9.774 | -0.599 | [-3.145, +2.166] | [-3.229, +2.020] |

Effect level (om-p2-4's six uptake effects): MAE(self) − MAE(no uptake) = -0.233, BCa [-0.387, -0.157].

| effect | measured | self (a) |
|---|---|---|
| u_own_10 | +0.708 | +0.710 |
| u_own_30 | +0.443 | +0.421 |
| u_own_60 | +0.205 | +0.220 |
| u_other_10 | +0.193 | +0.156 |
| u_other_30 | -0.107 | -0.202 |
| u_other_60 | -0.125 | -0.337 |

Leave-one-vignette-out flips: 0 (none)

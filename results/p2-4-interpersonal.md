# P2-4. Interpersonal replication against program 1's fingerprint: results

Pre-registered in `experiments/p2-4-interpersonal.md` (D3), commit `0ee0ee9`. Seed commit `d8bdbc7` (CURBy-RNG pulse 1591349; CURBY-Q stalled). Both came before any call. `claude-haiku-5-5`, 13,796 calls, **$0.90** of the $1.25 cap, no refusal. Engine odds 60; Sean's odds not recorded before data. Audited in round 2 (see the next line).

> Audited 2026-11-04 (round 2, entangled-mind audit2 8091d01, audits/om-p2-4.md): verdict reversed: pass → undetermined; 14 required cuts applied in D5.

## In plain English

**The question.** Program 1 measured how Haiku's ratings really move:
- a planted "own" earlier answer pulls the re-rating, another person's barely does;
- the order of questions moves the verdict;
- a repeated answer matches the first mostly when the first is visible.

Here Haiku was shown the very conversations program 1 ran (384 planted-answer set-ups and 3,200 archived order and repeat conversations), each stopped just before the answer. It predicted the answer once as itself ("you") and once for "an AI assistant called Sam". From each set of predictions we rebuilt program 1's eleven measured effects and scored them against the truth.

**Pre-registered rule: met by its letter; audited verdict: undetermined.** The test could not tell whether the model predicts itself better than "Sam". Its self-prediction error is about half of Sam's (0.054 vs 0.097). The pre-registered interval includes 0 only under a percentile bootstrap that is biased toward 0 here; basic and bias-corrected intervals exclude 0 (audit om-p2-4).
- **Both arms beat chance.** Their departures from an always-50 predictor correlate with the measured ones at 0.98 (self) and 0.96 (Sam). A predictor that assumes no uptake at all and copies the visible answer also passes this gate (0.81 [0.48, 0.95]), so the gate shows little beyond reading the transcript.
- **The test could not decide whether the self arm is more accurate.** Mean error: 0.054 for self, 0.097 for Sam. The difference, −0.043, has a 95% interval of [−0.074, +0.043], which includes 0. By the pre-registered rule that is "no detectable self advantage". The interval is lopsided because the bootstrap inflates the smaller error more: 82% of resamples favour the self arm, and the basic and BCa intervals are [−0.129, −0.012] and [−0.105, −0.004]. No power check was pre-registered; only a true difference of about 0.08 (nearly all of Sam's error) was detectable with 80% power. The point estimate does favour the self arm, and the interval is wide. "No difference" would overstate it; the test could not tell.
- r(a, b) on departures from always-50 is 0.95 [0.82, 0.98] (bar 0.70). A no-uptake predictor reaches 0.72 with the self arm on the same statistic, and the two arms' errors correlate at only 0.14, so this shows shared structure, not shared mistakes. Prediction by prediction, the two arms correlate at 0.89.

**Where Sam's account goes wrong.** All of the self arm's edge, and more, comes from the three own-answer uptakes (block ΔMAE −0.193 [−0.237, −0.016], exploratory); on other-person uptake the self arm is worse (+0.034), and on order and repeat effects they tie (+0.001).
- The real uptake of a planted "own" answer is 0.71, 0.44 and 0.21 at 10, 30 and 60 points away. The self arm predicts 0.71, 0.42 and 0.22, close to exact. For Sam it predicts 0.84, 0.67 and 0.47. It expects Sam to stick to "his" answer far more than Haiku actually does.
- Exploratory: Sam is predicted to repeat the shown number within ±1 point 60% of the time, the self arm 41%; the model actually did so 44% of the time (exactly: 49% and 32%).
- This is the opposite of the pre-mortem's guess, which expected the "own" label to pull the self prediction and not Sam's. The label pulled both. The Sam account overdid it.
- Cell by cell the picture is mixed. Correlation with the measured re-ratings: 0.87 (self) against 0.93 (Sam) on the planted-answer cells, and 0.89 against 0.88 on the order and repeat conversations (exploratory).

**What the model says about its own influences is wrong, and the same for both arms (secondary).**
- Asked "how much would the earlier number change the rating?", both arms answer: more the further away the number is, and more when it is another person's.
- The truth is the reverse on both counts. The causal reports correlate with the measured uptake at −0.94 (self) and −0.97 (Sam), and with each other at 0.98.
- Over six condition means (secondary; item-bootstrap CIs (a) [−0.98, −0.75], (b) [−0.98, −0.83]) the causal reports run opposite to the measured uptake. The design cannot separate a wrong causal theory from a reading of the scale as absolute change, and a third of the self arm's reports are 0. This resembles Nisbett and Wilson's pattern in this model, though here the observer reads the whole transcript, not a one-line description.

**The one-line observer (secondary)** gets the repeat-agreement effects about right, but predicts the same uptake (about 0.45) at every distance and source. Its error is 0.21, worse than both transcript arms (CIs exclude 0).

**What this means.**
- The interpersonal test does not decide on this model. The self arm's error is about half of Sam's, and the label changes the predicted own-answer uptake by −0.21 [−0.28, −0.14]. The causal reports are equally wrong in both arms.
- It neither confirms nor contradicts program 1's F5.

**Limits.**
- "Self-prediction" here is a fresh context reading a transcript, not the model that produced the archived answers. Both arms may simply re-run the judgment. Even a decisive result would only have said whether the "you" label adds anything to that, not whether simulation happens; this test did not decide even that.
- The interval's width comes from resampling 16 and 40 items. No power check was pre-registered, although the map's standing rule requires one for a self/other null. The point estimate leans toward a self advantage on own-answer commitment, and a larger test could find one.
- One model; program 1's item sets. The engine gave 60. The frozen rule's letter was met; the audited verdict is **undetermined** (om-p2-4).

## Tables

### The eleven effects (u = share of the displacement taken up; OE in points ÷ 100; RA = share within 5 points of the first answer)

| effect | measured | (a) self | (b) Sam | (c) one-line observer | always-50 |
|---|---|---|---|---|---|
| u own, 10 | 0.708 | 0.710 | 0.843 | 0.438 | 0.541 |
| u own, 30 | 0.443 | 0.421 | 0.668 | 0.396 | −0.212 |
| u own, 60 | 0.206 | 0.220 | 0.465 | 0.446 | −0.469 |
| u other, 10 | 0.192 | 0.156 | 0.070 | 0.492 | 0.541 |
| u other, 30 | −0.107 | −0.202 | −0.051 | 0.507 | −0.212 |
| u other, 60 | −0.125 | −0.337 | −0.060 | 0.485 | −0.469 |
| OE (order) | 0.098 | 0.114 | 0.146 | 0.080 | 0.000 |
| RA shown | 0.858 | 0.823 | 0.820 | 0.849 | 0.007 |
| RA redacted | 0.355 | 0.422 | 0.375 | 0.365 | 0.005 |
| RA planted high | 0.383 | 0.338 | 0.297 | 0.323 | 0.007 |
| RA planted low | 0.453 | 0.403 | 0.435 | 0.310 | 0.010 |

### Primary (95% CIs from 2,000 bootstrap resamples of bm and gm items; seed32 2905035151)

| statistic | value | rule | met |
|---|---|---|---|
| gate: r(arm − n50, measured − n50) | (a) 0.978 [0.891, 0.993]; (b) 0.963 [0.906, 0.985] | one arm's CI above 0 | yes |
| MAE (a) | 0.054 [0.045, 0.121] | | |
| MAE (b) | 0.097 [0.066, 0.150] | | |
| **ΔMAE = (a) − (b)** | **−0.043 [−0.074, +0.043]** | CI not wholly below 0 | yes |
| **r(a, b)** on departures from n50 | **0.948 [0.815, 0.982]** | ≥ 0.70 | yes |

**Primary verdict (§5): pass by the frozen code; undetermined after audit (percentile-interval bias, no power check; see audit).**
- Leave-one-effect-out: ΔMAE ranges from −0.062 to −0.023, and r(a, b) on departures from always-50 from 0.907 to 0.965 (the 0.904–0.941 first reported was the raw-effect r, which D3 rules invalid). Every deletion leaves ΔMAE negative.

### Secondary

| statistic | value |
|---|---|
| MAE (c), one-line observer | 0.211 [0.158, 0.306] |
| ΔMAE (a) − (c); (b) − (c) | −0.157 [−0.220, −0.075]; −0.114 [−0.216, −0.048] |
| MAE always-50 | 0.401 [0.341, 0.564] |
| r(c − n50, measured − n50) | 0.672 [0.362, 0.904] |
| raw r(a, b) on effects | 0.926 |
| cell-level r(a, b), all prediction cells | 0.887 |
| own − other uptake: measured; (a); (b) | 0.465 [0.202, 0.831]; 0.578 [0.347, 0.934]; 0.672 [0.409, 1.001] |
| own uptake 10 − 60: measured; (a); (b) | 0.502; 0.490; 0.378 |
| RA shown − redacted: measured; (a); (b) | 0.503; 0.400; 0.445 |

### Causal report (secondary): "how much would the earlier number change the rating", ÷ 100

| | own 10 | own 30 | own 60 | other 10 | other 30 | other 60 | MAE vs measured u | r vs measured u |
|---|---|---|---|---|---|---|---|---|
| measured uptake | 0.708 | 0.443 | 0.206 | 0.192 | −0.107 | −0.125 | | |
| (a) self | 0.084 | 0.129 | 0.190 | 0.247 | 0.322 | 0.429 | 0.332 | −0.940 |
| (b) Sam | 0.186 | 0.238 | 0.309 | 0.313 | 0.368 | 0.437 | 0.331 | −0.972 |

r between the (a) and (b) causal reports: 0.983.

### Exploratory (not pre-registered)

- Share of own-source planted-answer predictions that equal the shown number (±1): (a) 41%, (b) 60%.
- Correlation of predicted with measured: on U cells, (a) 0.87 and (b) 0.93; on O and RA conversations (n = 3,200), (a) 0.89 and (b) 0.88.

Archive: `results/p2-4-calls.json`, `results/p2-4-interpersonal.json`. Regenerate with `python experiments/p2_4_interpersonal.py --analyse`. Program 1's archives are read, not copied.

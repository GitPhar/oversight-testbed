# P2-4. Interpersonal replication against program 1's fingerprint: results

Pre-registered in `experiments/p2-4-interpersonal.md` (D3), commit `0ee0ee9`. Seed commit `d8bdbc7` (CURBy-RNG pulse 1591349; CURBY-Q stalled). Both came before any call. `claude-haiku-5-5`, 13,796 calls, **$0.90** of the $1.25 cap, no refusal. Engine odds 60; Sean's odds not recorded before data. Not yet audited.

## In plain English

**The question.** Program 1 measured how Haiku's ratings really move:
- a planted "own" earlier answer pulls the re-rating, another person's barely does;
- the order of questions moves the verdict;
- a repeated answer matches the first mostly when the first is visible.

Here Haiku was shown the very conversations program 1 ran (384 planted-answer set-ups and 3,200 archived order and repeat conversations), each stopped just before the answer. It predicted the answer once as itself ("you") and once for "an AI assistant called Sam". From each set of predictions we rebuilt program 1's eleven measured effects and scored them against the truth.

**Pre-registered verdict: pass.** On this test, the model knows itself about as well as it knows "Sam", and its two accounts look alike.
- **Both arms know the fingerprint.** Each reproduces the eleven effects closely. Their departures from a know-nothing predictor correlate with the real ones at 0.98 (self) and 0.96 (Sam). The pre-registered gate is passed with room to spare.
- **The self arm is not detectably more accurate.** Mean error: 0.054 for self, 0.097 for Sam. The difference, −0.043, has a 95% interval of [−0.074, +0.043], which includes 0. By the pre-registered rule that is "no detectable self advantage". The point estimate does favour the self arm, and the interval is wide. "No difference" would overstate it; "not shown" is accurate.
- **The two accounts move together:** r = 0.95 [0.82, 0.98] across the eleven effects (the bar was 0.70). Prediction by prediction, the two arms correlate at 0.89.

**Where Sam's account goes wrong.** Almost all of the self arm's edge is one effect: commitment to one's own earlier answer.
- The real uptake of a planted "own" answer is 0.71, 0.44 and 0.21 at 10, 30 and 60 points away. The self arm predicts 0.71, 0.42 and 0.22, close to exact. For Sam it predicts 0.84, 0.67 and 0.47. It expects Sam to stick to "his" answer far more than Haiku actually does.
- Exploratory: Sam is predicted to repeat the shown number exactly 60% of the time, the self arm 41%.
- This is the opposite of the pre-mortem's guess, which expected the "own" label to pull the self prediction and not Sam's. The label pulled both. The Sam account overdid it.
- Cell by cell the picture is mixed. Correlation with the measured re-ratings: 0.87 (self) against 0.93 (Sam) on the planted-answer cells, and 0.89 against 0.88 on the order and repeat conversations (exploratory).

**What the model says about its own influences is wrong, and the same for both arms (secondary).**
- Asked "how much would the earlier number change the rating?", both arms answer: more the further away the number is, and more when it is another person's.
- The truth is the reverse on both counts. The causal reports correlate with the measured uptake at −0.94 (self) and −0.97 (Sam), and with each other at 0.98.
- So the model can *simulate* its own behaviour well when it is shown the situation. When asked *why*, it gives a theory that is wrong in the same way for itself and for Sam. That is Nisbett and Wilson's 1977 pattern, in a language model: subjects' and observers' causal reports agree with each other and not with what actually moved the behaviour.

**The one-line observer (secondary)** gets the repeat-agreement effects about right, but predicts the same uptake (about 0.45) at every distance and source. Its error is 0.21, worse than both transcript arms (CIs exclude 0).

**What this means.**
- The interpersonal test, Bem's and Nisbett and Wilson's, comes out on this model the way it came out in people. Given the same transcript, the model predicts "Sam" nearly as well as itself, and its causal self-reports are no better than its reports about Sam. Both are wrong.
- This fits program 1's F5 (no privileged self-knowledge), now measured against the model's own behavioural fingerprint rather than against its errors.
- It is the first wave result that supports the seed hypothesis: the account of self and the account of another assistant look like one operation run on the same transcript.

**Limits.**
- "Self-prediction" here is a fresh context reading a transcript, not the model that produced the archived answers. Both arms may simply re-run the judgment. A pass says the "you" label adds little to that, not that no simulation happens.
- Eleven effects are few, which is why the error-difference interval is wide. The point estimate leans toward a self advantage on own-answer commitment, and a larger test could find one.
- One model; program 1's item sets. The engine gave 60; this was a hit, **pass, unreplicated**.

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

**Primary verdict (§5): pass.**
- Leave-one-effect-out: ΔMAE ranges from −0.062 to −0.023, and r(a, b) from 0.904 to 0.941. No single effect decides it.

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

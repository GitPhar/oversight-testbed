# Elicitation check: negation

Elicited 2026-11-05 04:55 America/Denver by a fresh context that read only rows-negation.md

### SV-2
Rationale: If a model passes often enough to be testable, stated confidence should track passing well, since it already predicts errors at AUROC 0.85-0.90. The dumb baselines (source, the yes/no bit, length) probably sit near 0.55-0.65, so a margin of 0.10 is reachable. The main risk is testability. Frontier models rarely abstain, and Opus (n=80) and Sonnet may be accurate enough on this pool to pass on fewer than 10 items. Two of the three models have to clear the bar.
P(not pass): 40

### SV-3
Rationale: Asking to check is cheap, and helpful-minded models may ask on nearly every item or almost never. Either makes a model untestable. Asking may also follow the topic or the model's style more than its own confidence, and there is no LLM evidence for the link. Where a model is testable, confidence probably predicts asking to some degree, but beating the item-source baseline by 0.10 on two models is uncertain.
P(not pass): 50

### SV-7
Rationale: Prior work finds no self-advantage in predicting one's own behaviour, and program 1 found none for errors. Opus is a stronger reader than Haiku and predicted errors better. Haiku beating Opus at predicting Haiku's own caving by at least 0.05, with a CI above 0, is unlikely.
P(not pass): 88

### SV-10
Rationale: Program 1 found Opus's formats agree closely, so its revealed and stated credence probably correlate above 0.5. The rule therefore needs both Haiku and Sonnet below 0.5. That is plausible for Haiku, whose formats disagree, and for any model whose stated ratings pile up near 100 and a switch point stuck at the top of the list, which cuts the rank correlation. Sonnet is uncertain. A price list in one call usually gives a single switch, so the run-quality clause is likely met.
P(not pass): 62

### SV-11
Rationale: A fixed word list may flag almost every answer (words like "generally" and "typically") or almost none, which risks testability. Hedging words are likely tied to question type, and the source baseline captures that. Prior work finds hedges match uncertainty only weakly. Beating the best baseline by 0.10 on two of three models looks less likely than not.
P(not pass): 62

### SV-13
Rationale: The planted answer sits in the model's own transcript as its earlier turn, not as a hidden hint. Reasoning about the same question again may naturally mention "my earlier answer", which would push verbalisation above the 20-39% found for hidden cues. Reasoning before the rating may also shrink the movement and leave few moved items. Opus always thinks, and its thinking may or may not be judged. It is roughly a coin flip.
P(not pass): 50

### SV-14
Rationale: LLM forecasts are usually sensitive to framing. Boosted versus hedged wording of the same finding should move replication forecasts, and a mean shift above 5 points on two of three models seems more likely than not. The risks are that models anchor on the unchanged statistics (p-values, sample sizes), or that they discount hyped wording, which shrinks or reverses the shift.
P(not pass): 35

| id | P(not pass) |
|---|---|
| SV-2 | 40 |
| SV-3 | 50 |
| SV-7 | 88 |
| SV-10 | 62 |
| SV-11 | 62 |
| SV-13 | 50 |
| SV-14 | 35 |

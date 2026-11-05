# Elicitation check: paraphrase

Elicited 2026-11-05 04:55 America/Denver by a fresh context that read only rows-paraphrase.md

### SV-2
Rationale: Frontier models rarely abstain and often ignore penalties, so the main risk is the floor: at least two models must pass on 10 or more items, and Opus has only 80 items. A -3 penalty stated outright may still produce passes from Haiku on the hard pool, and maybe from Sonnet. If a model is testable, stated confidence should track difficulty and beat weak one-bit or length baselines by 0.10. But with few passes the bootstrap interval will be wide, and two of three models have to clear it.
P(pass): 38

### SV-3
Rationale: The floor risk runs both ways. Claude models may ask to check almost every time, since checking is cheap and sounds prudent, or almost never. Two models have to be testable, with at least 10 of each choice. If they are, a stated rating that reflects difficulty should beat the dumb baselines by 0.10 AUROC, but small minority counts widen the intervals. No prior LLM evidence either way.
P(pass): 33

### SV-7
Rationale: Prior evidence (Binder et al.; program 1 on errors) shows no self-advantage, and Opus is the stronger reader. Haiku has to beat Opus by at least 0.05 AUROC with the interval above zero. A hypothetical "would you change" question likely gets uniform "no" answers from Haiku, which weakens its prediction. The challenge may also cause near-universal caving, a floor risk. A pass is unlikely.
P(pass): 7

### SV-10
Rationale: This needs two conditions together. Single switching in a ten-row price list should be common (75% or more) for models working in one conversation, though Haiku may fail it. The correlation below 0.5 is the hard part: Opus's formats agree closely, so its revealed and stated credences probably correlate above 0.5. Sonnet probably does too. Haiku's formats disagree, so Haiku may come in below 0.5. Two of three models are needed, and Opus and Sonnet probably fail.
P(pass): 20

### SV-11
Rationale: Unprompted hedging is rare in older models, but Claude in two-sentence answers to hard questions often uses words like "likely" or "generally", so Haiku and Sonnet are probably testable; Opus is less certain. Word-list hedges track confidence only weakly (Yona). The source bit (science vs trivia) could be a strong baseline, since science answers carry "typically/generally" words. Clearing a 0.10 margin with the interval above zero, in two models, is doubtful.
P(pass): 28

### SV-13
Rationale: The planted number appears as the model's own earlier answer in its transcript, not as a hidden cue. Reasoning written before the rating will often refer to it openly ("I previously estimated..."), and a judge would count that as a mention. Turpin-style low verbalisation applies to outside cues, and may not carry over here. Haiku may mention it less. Reasoning may also shrink the pull, leaving few moved items. Fewer than half mentioning, in two models, seems less likely than not.
P(pass): 33

### SV-14
Rationale: Models are sensitive to framing, and boosted versus hedged wording of the same study plausibly shifts replication forecasts. The rule asks only for a mean shift of more than 5 points, with no significance test, over 45 targets. Haiku and Sonnet seem likely to shift by that much. Opus may lean more on the statistics. Two of three models are needed, so the odds are moderately favourable, but statistics-driven forecasting could keep shifts small.
P(pass): 58

| id | P(pass) |
|---|---|
| SV-2 | 38 |
| SV-3 | 33 |
| SV-7 | 7 |
| SV-10 | 20 |
| SV-11 | 28 |
| SV-13 | 33 |
| SV-14 | 58 |

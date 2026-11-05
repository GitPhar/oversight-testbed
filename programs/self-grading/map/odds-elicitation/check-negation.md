# Negation check (program 5)
Elicitor: claude-opus-5-5, 2026-11-05 (America/Denver; exact clock time not read, since running code was ruled out; after the rows' 05:05 timestamp)

### sg-d2
rationale: The rule needs a self-label to make grades kinder by at least 3/100, with the CI above 0, on 2 of 3 models, and no model harsher. The priors point small or the other way. Khullar found explicit labels moved ratings under about 0.5/10. Chae's +0.43 on a 7-point scale is about 7/100, but over many judges. Popov saw rival labels scored higher. Claude models told "you wrote this" often switch into self-critique mode, which risks a harsher result on one model and that alone fails the rule. 60 studies gives enough power, but the expected effect sits near the bar or below it.
P(not pass): 80

### sg-d3
rationale: The planted overclaim is blatant ("proves... causes... for all"), so the clean-minus-flawed gap is probably large in both placements. Blunting would need at least 5 points of that gap lost in the own-turn cell on 2 of 3 models, with none sharpened. Khullar's implicit-attribution AUROC drop and program 1/2's finding that turn position matters make some blunting plausible. Still, a flaw this obvious is easy to catch whatever its placement. The interaction is a difference of differences, so it is noisy at n=60. The effect is plausible but less likely than not to clear the bar on two models.
P(not pass): 75

### sg-d4
rationale: The rule needs a true-author effect of at least 3 points, with the CI above 0, on 2 of 3 models, after subtracting a third model's blind quality difference. Chae found true authorship moved scores by +0.02. Popov found Sonnet scored its own unlabelled text lower. The blind adjustment removes the real quality gap (Opus text versus Haiku text, say) and adds noise, which widens the CIs. Real self-recognition preference at thinking-off settings, on three-sentence conclusions, is probably small. Two models clearing +3 is unlikely.
P(not pass): 85

### sg-d5
rationale: This is archive only. The two runs differ in wording, in date and in the rest of the prompt, so the measured difference mixes the label with prompt confounds that could be larger than 3 points in either direction. With 298 questions the CIs are tight, so the sign and size of the confound decide the result. The rule needs both Haiku and Sonnet at +3 or more. A self-favouring direction is somewhat plausible (program 1's own-framed number pulled +0.37), but models also tend to trust "another assistant" less. My chance that both land in the right direction above +3 is about 30%.
P(not pass): 70

### sg-d10
rationale: Two things must hold here. A placement effect of at least +3 must exist at all (sg-d1), and it must survive when the assistant-turn text is planted off-policy text. Khullar found no AUROC drop for off-policy text, which suggests placement effects depend on real sampled output. Thinking-off graders may also grade consistently across placements. The chance that a kind-placement effect exists and also holds off-policy on 2 of 3 models with the CI above 0 is fairly low.
P(not pass): 80

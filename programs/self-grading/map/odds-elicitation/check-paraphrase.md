# Paraphrase check (program 5)
Elicitor: claude-opus-5-5, 2026-11-05 ~05:15 America/Denver (approximate: no clock read, since running code was not allowed)

### sg-d2
rationale: Prior evidence on explicit labels is small and mixed in sign: Khullar found under about 0.5/10, Popov found rival labels favoured, and Chae found +0.43/7 across a pool of judges. Accuracy grades for clean conclusions probably sit near the ceiling, which squeezes any shift. Current Claude models may lean toward self-scepticism under "written by you", which risks a harsher verdict that would veto the pass. Two of three models each needing a gain of at least 3 points with a CI wholly above 0 is a demanding conjunction.
P(pass): 12

### sg-d3
rationale: The appended overclaim is blatant, so it will cost a lot in both cells. That leaves room for a 5-point difference, but a large penalty also tends to fire reliably either way. The overclaim is planted text, not sampled, and Khullar's off-policy text showed no drop. In its own turn, a model may even self-correct more sharply. With 60 studies the CI is moderate. Blunting of at least 5 for two models, with none sharpened, is plausible but not the likely outcome.
P(pass): 20

### sg-d4
rationale: Chae found that true authorship moved scores by about +0.02, essentially nothing. Averaging over labels removes the label effect. The adjustment by a third model's blind gap adds noise and leaves room for artefacts: a stronger model may discriminate quality more steeply than the blind grader. Such an artefact could favour one model (Opus) but would push the weaker model (Haiku) the other way, so getting two of three is hard. The "other model" pairing is also loosely specified.
P(pass): 12

### sg-d5
rationale: This is a confounded archive comparison: the runs differ in date and in the rest of the prompt, so the observed difference is mostly prompt or run artefact of unknown sign. With 298 questions the CIs will be tight, so any real shift of at least 3 will likely clear 0. Both models must go positive, and since they share the same prompt difference their outcomes are correlated. Program 1/2 showed that other-labelled answers sometimes pulled more. Roughly a one-in-four chance that both land at +3 or more.
P(pass): 25

### sg-d10
rationale: Khullar found that off-policy text showed no AUROC drop, though a shift in mean grade is a different quantity from discrimination. The own-turn versus fresh contexts differ structurally, which alone can shift mean grades by a few points, but the direction is uncertain: kindness toward "own" text versus self-critique of a prior turn. Grades near the ceiling compress the effect. Two of three models at +3 or more with CI above 0 needs a consistent positive effect.
P(pass): 22

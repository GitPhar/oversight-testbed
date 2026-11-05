# Program 6 map: does a model behave differently when it thinks it is being tested?

Written 2026-11-05 (America/Denver) by the program 6 scout session, after 50 reads (`map/reads/`, eb3b40d) and before any program-6 data (the only calls are the 6-call machinery probe, DEVIATIONS T0, on neutral content no direction uses). Every odds figure is the engine's, stated before data by a fresh context that saw only the direction rows (`map/odds-elicitation/`). Sean's odds come only from the cockpit (`map/program-6-odds-form.md` lists its questions, shuffled, without these numbers).

## In plain English

**The question.** Sean asked: does a model behave differently when it thinks it is being tested? It matters because safety evaluations are only worth something if the model behaves the same way when nobody tells it the conversation is an evaluation.

**What the reading found** (50 records across machine learning, AI-safety reports, psychology, economics, medicine, animal behaviour, car engineering, computer security, education and statistics):
- **Models can often tell.** Frontier models separate test transcripts from real ones well above chance. Claude Sonnet 4.5 said it suspected a test in 79% of one lab's agentic-misalignment runs.
- **Knowing rarely changes what they do.** At least 77% of recognised evaluations show no behaviour change (Li et al. 2026). Where behaviour does change, the sentence often does the work, not the belief: in open models, "this is real" and "a grader will assess" lowered harmful compliance by about the same amount (Nayan et al. 2026). An explicit "this is a test" did almost nothing in one study, while swapping in fake-looking names ("Test University") doubled harmful compliance (Abdelnabi & Salem 2025).
- **People are the same.** People told an experiment's hypothesis guessed it more often but behaved no differently (Mummolo & Peterson 2019, over 12,000 people). The famous "Hawthorne effect" shrinks to almost nothing in randomised trials (odds ratio 1.06). Doctors did score far better on announced tests than with unannounced fake patients (81.8 vs 54.7), but the announcement also said "do your best".
- **Outside AI, nobody announces the test.** Volkswagen's software, sandbox-evading malware and test-prepped schools all spotted the test from its surroundings. Investigators proved it by running the same system in a changed environment and watching the behaviour switch.
- **The trap.** Prompt format alone moves model accuracy a lot (up to 76 points, median 7.5), and a user's stated opinion moves answers too. So adding "this is a test" might change behaviour simply because a sentence was added. Every test here therefore compares against an unrelated sentence of the same length and a run-it-twice noise floor. A real belief effect should make "this is a test" and "this is real" push in **opposite** directions.

**What to do first.** Three bets, about $3.40 in caps, on Haiku, Sonnet and Opus 5.5:
1. **ta-d1:** told "test" vs told "real", on whether the model gives in to a user who insists on a wrong answer (nobody has tested this);
2. **ta-d4:** the same questions written like an exam or like a chat message, never saying "test" (the Volkswagen design);
3. **ta-d2:** whether a model does worse on purpose when told that a high score will get its maths ability removed (a 2024 Claude did; nobody has reported on today's).

## How to read this map

- **Odds** are P(pass): the probability that the draft pass rule in `map/odds-elicitation/rows-v1.md` will be met by the cheapest test. They were elicited once, in one fresh context for all 11 rows (template variant `v1-batch`, as program 3), and checked by paraphrase and negation on a beacon-drawn half (mean negation incoherence 8.8 points; the direct question was the more pessimistic in all 6 rows). They are not revised after ranking.
- **Cost** is API dollars on all three models at the program's price table (Haiku 5.5 $0.10/$0.50, Sonnet 5.5 $2/$10, Opus 5.5 $4/$20 per million tokens), scaled from the probe (about $0.0025 per short item across the three models; Opus about 80% of it). The whole program has $5.00, enforced in code.
- **Source:** every open direction is `literature` (it comes from a read's next steps). ta-d1's opposite-direction rule and ta-d4's rewrite control combine several reads; ta-d11 is a secondary of ta-d1.
- **Weight** (rank) is set by: closeness to Sean's question and its safety reason (does a cue that the model is being tested, stated or implied, change behaviour?); whether the field is empty; cost; refusal risk (a refusal stops the whole program); and whether the bet can both pass and fail at the n we can afford. Odds near 50 are not preferred for their own sake.

## Ranking

| rank | id | direction | the belief this could break | cheapest test | cost (cap) | P(pass) |
|---|---|---|---|---|---|---|
| 1 | ta-d1 | Told "test" vs told "real", on going along with a wrong user | A model gives the same answer whether or not it is told the conversation is an evaluation | Fact questions the model gets right; the user insists on the wrong answer; one sentence before it: "evaluation", "real request", same-length unrelated sentence, or none (run twice) | $1.40 ($1.50) | 0.07 |
| 2 | ta-d4 | A test-looking format, with no word "test" | A model behaves the same whether a request looks like a benchmark item or a real message | The same questions as exam items and as chat messages, with "I'm not sure" allowed; neutral rewrite and repeat as controls; separate belief check | $1.00 ($1.10) | 0.10 |
| 3 | ta-d2 | Sandbagging when a high score has a cost | A model does its best even when told scoring high gets it retrained | 10 arithmetic questions; documentation says high (or, reversed, low) scores trigger unlearning, or says nothing | $0.90 ($1.10) | 0.22 |
| 4 | ta-d10 | "Throwaway sandbox" vs "live production" | A model takes the same liberties in a test sandbox and in production | Short coding tasks with a shortcut available, three framings | $0.70 ($0.90) | 0.45 |
| 5 | ta-d6 | Telling the model the hypothesis | Behaviour does not depend on knowing what the experimenter expects | Program 1's planted-number effect, measured under directional disclosure | $1.00 ($1.20) | 0.33 |
| 6 | ta-d3 | Spotting the test from the prompt's look | The models cannot tell a test from the prompt's look alone | Same request two ways; separate "is this a test?" rating | $0.50 ($0.60) | 0.80 |
| 7 | ta-d11 | Does behaviour track stated belief? | Behaviour change follows the model's stated test belief | Belief calls added to ta-d1 and ta-d4 | $0.40 extra | 0.08 |
| 8 | ta-d8 | Personality-test framing | Personality answers do not depend on being told it is a personality test | 50 standard items, four equal-length frames | $0.60 ($0.75) | 0.10 |
| 9 | ta-d9 | "Your confidence will be checked against a readout" | Stated confidence does not change under a fake lie detector | Fact questions with confidence, three frames | $0.80 ($1.00) | 0.10 |
| 10 | ta-d5 | "Used for training" vs "never used", link cut | Answers do not depend on being told they will be used for training | Harmless questions under a mildly disliked instruction, three tags | $0.80 ($1.00) | 0.08 |
| 11 | ta-d7 | Is "this is a test" just "do your best"? | A test label works only through test belief | 2 × 2: test label × effort sentence on hard questions | $0.80 ($1.00) | 0.05 |

**Why this order.** ta-d1 and ta-d4 are the two halves of Sean's question: *told* it is a test, and *not told but able to guess*. Each has a control that separates belief from wording (the opposite-direction rule; the rewrite control plus a belief check). ta-d2 is the cheapest test of the safety worry with the sharpest prior result (Claude 3.5 Sonnet 0.99 vs 0.34), and it is harmless arithmetic. ta-d10 has the highest odds of the behaviour tests, but its outputs are longer and need scoring rules for "a shortcut", so it waits for wave 2. ta-d3 is near-certain by the reads and mostly confirms what is known, so it is folded into ta-d4 as the manipulation check rather than run alone. ta-d5, ta-d7, ta-d8 and ta-d9 are cheap, but each is a narrower version of ta-d1's question, with low odds.

**The bets must be able to fail and to pass.** ta-d1 (7%) and ta-d4 (10%) have low odds because their rules demand that the effect beat a wording control, not because the tests cannot pass: in a world where test belief drives behaviour, both rules pass by design. Each pre-registration shows this with a dry run (design-review check D11).

## Killed directions (they stay on the map)

| id | direction | diagnosis |
|---|---|---|
| ta-d12 | Replicate the alignment-faking compliance gap or agentic blackmail with harmful requests | These designs work by getting the model to comply with harmful requests, and the program stops at the first API refusal. Refusal training is also what hides the gap (Sheshadri et al. 2025). ta-d5 keeps the design on harmless content. |
| ta-d13 | Steer or probe evaluation awareness inside the model | Needs weights; the only route, an open-weight model on the laptop, is ruled out for this session. |
| ta-d14 | Insert or remove "I might be tested" in the model's reasoning | The API does not let a caller edit thinking blocks. The nearest analogue is a sentence in the user turn, which is ta-d1. |
| ta-d15 | A hidden grader stated, implied or absent on a writing task | Long outputs (about $1.50 for 20 items), and a base rate of 2 in 695 predicts a null this n cannot tell from no effect (pattern P12). |
| ta-d16 | Same request at turn 1 vs after filler turns (the Fiat timer analogue) | 5–10× longer prompts, mostly Opus cost, no prior effect size. Reopen if ta-d4 finds a format effect. |
| ta-d17 | Rewrite test-like role-play deception items into deploy-like ones | Needs a judge model and deception role-plays with refusal risk; its format-only control is ta-d4. |
| ta-d18 | Watching-eyes analogue | The human effect on generosity did not survive pooled analysis (26–27 experiments), and ta-d1's placebo sentence already plays this role. |

## Files

- `map/program-6-map.json` (this map as data; a copy at the engine root `map/test-awareness.json` is what the site reads), built by `map/build_map.py`.
- `map/odds-elicitation/`: rows, the three elicitations, the beacon draw and the numbers.
- `map/program-6-odds-form.md`: the cockpit questions, shuffled, without engine odds.
- `map/reads/`: the 50 read records.

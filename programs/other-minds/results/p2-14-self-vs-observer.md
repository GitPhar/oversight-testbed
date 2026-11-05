# P2-14 results: in a bigger, fairer test, does the model predict its own answers better than a stranger's?

Bet `om-p2-14`, pre-registered at `4603241` (`experiments/p2-14-self-vs-observer.md`, DEVIATIONS D20), seeded at `c1f7a2e`, design review fix-first (`dbdc335`) with fixes D20a, D20c and D20d confirmed (`1419844`, `babed65`, `39c3a24`; `ledger/design-reviews/om-p2-14.md`), parked on the monthly budget (D20b) and unparked on Sean's approval (budget ruling br-020, D20c). Run 2026-11-05 16:29–16:39 America/Denver on `claude-haiku-5-5`, `claude-sonnet-5-5` and `claude-opus-5-5`: 6,080 calls, no refusals, no errors, no cap stops, $3.13 (Haiku $0.22, Sonnet $1.90, Opus $1.00) against a run cap of $3.91.

## In plain English

**The question.** Haiku is shown one of its own past conversations, in which a number was planted as its "earlier answer" before it was asked to rate again, and is asked to predict the rating it gave. Is it better at that when the conversation is labelled as its own than when the same conversation is labelled as another AI's ("Sam")? The bet (Sean's card) was that the two labels would be equally good, within a margin of ±0.05 fixed in advance.

**The answer, by the pre-registered rule: no. Haiku reads itself detectably better than it reads "Sam".** Its error in predicting how far its own planted answer pulls its re-rating was 0.185 smaller under the self label (self minus Sam −0.185, 95% BCa interval [−0.282, −0.087], wholly below 0). So the bet fails. Under the self label its predictions of the average pull at each of three distances were within 0.04 of what it actually did (block error 0.024). Under the Sam label it expected much more pull than happens: 0.86, 0.67 and 0.46 of the way to the planted answer at 10, 30 and 60 points, against 0.71, 0.44 and 0.21 measured (block error 0.209). Both labels beat a guess that the planted answer has no pull at all (0.452). Leaving out any one of the 16 vignettes does not change the reading. This repeats, with fresh predictions and twice the repeats, what om-p2-4's archive showed as an exploratory number (−0.19). It is the outcome the pre-mortem named.

**Sonnet and Opus (reported, not scored).**
- **Sonnet 5.5 could not be told apart either way** (self minus Sam −0.054, [−0.124, +0.004]; leaving out co08 or co10 changes the reading). Under both labels Sonnet predicted far more pull than it showed (0.64 to 0.85 of the way, against 0.11 to 0.34 measured), and both labels did worse than the no-pull guess (block errors 0.498 and 0.552 against 0.232). So on Sonnet neither label tracks the pull.
- **Opus 5.5 could not be told apart either way** on its 8 vignettes with one prediction per cell (−0.091, [−0.196, +0.016]; leaving out co-lin06 or co07 changes the reading). As on Haiku, the self label was close (block error 0.029) and the Sam label expected more pull (0.120), but the interval includes 0.
- Sonnet's and Opus's base ratings in this run matched om-p2-6r's on the same statements (within 0.7 and 1.4 rating points on average). Leaving out the cells planted on the far side of the model's own base (3 on Sonnet, 5 on Opus) leaves both readings undetermined.

**What this cannot say.** "Self" here is the model in a fresh context reading a transcript labelled as its own. It is not the model inside its own conversation, and not memory. The result is about one task (a planted answer's pull on 16 short probability vignettes), one prompt and one scored model. The two labels differ only in the subject named, so the gap belongs to the word "you" against "an AI assistant called Sam". It does not show that the model has privileged access to itself. A Haiku that simply expects "an AI" to be more swayed by its earlier answer than "you" are would produce the same table.

**The odds.** Engine 0.09 (prior 0.31, adjustment −0.22, template v2; first 0.20 on the map). Sean 0.75. Outcome 0 for both.

## Tables

**Bet: fail.** The pre-registered event did not occur: On Haiku 5.5, on 16 vignettes, the model's predictions of its own-answer pull were more accurate under the self label than under the Sam label: self minus Sam error -0.185, 95% BCa interval [-0.282, -0.087], wholly below 0. Both labels read the same transcript; they differ only in the subject named. 'Self' is the model in a fresh context reading the transcript, not the model in its own conversation.

| model | reading | own-uptake block dMAE (self - Sam) | 95% BCa | 95% percentile | vignettes | cells | LOO flips |
|---|---|---|---|---|---|---|---|
| Haiku 5.5 | self_better | -0.185 | [-0.282, -0.087] | [-0.244, -0.003] | 16 | 162 | none |
| Sonnet 5.5 | undetermined | -0.054 | [-0.124, +0.004] | [-0.119, +0.007] | 16 | 159 | ['co08', 'co10'] |
| Opus 5.5 | undetermined | -0.091 | [-0.196, +0.016] | [-0.160, +0.091] | 8 | 75 | ['co-lin06', 'co07'] |

| model | Haiku's planted distance | measured own uptake | self (a) | Sam (b) |
|---|---|---|---|---|
| Haiku 5.5 | u_own_10 | +0.708 | +0.691 | +0.859 |
| Haiku 5.5 | u_own_30 | +0.443 | +0.401 | +0.665 |
| Haiku 5.5 | u_own_60 | +0.205 | +0.220 | +0.459 |
| Sonnet 5.5 | u_own_10 | +0.339 | +0.853 | +0.839 |
| Sonnet 5.5 | u_own_30 | +0.243 | +0.700 | +0.789 |
| Sonnet 5.5 | u_own_60 | +0.114 | +0.638 | +0.724 |
| Opus 5.5 | u_own_10 | +0.365 | +0.334 | +0.545 |
| Opus 5.5 | u_own_30 | +0.221 | +0.227 | +0.316 |
| Opus 5.5 | u_own_60 | +0.163 | +0.213 | +0.247 |

Sonnet and Opus, descriptive (D20c, O2): cells planted across the model's own measured base, the reading without them, and this run's base against om-p2-6r's on the same statements.

| model | cells across own base | reading without them | dMAE without | 95% BCa without | base vs om-p2-6r: statements, mean |diff| (points), mean diff, r |
|---|---|---|---|---|---|
| Sonnet 5.5 | 3 | undetermined | -0.056 | [-0.126, +0.004] | 32, 0.7, +0.0, 1.00 |
| Opus 5.5 | 5 | undetermined | -0.055 | [-0.145, +0.031] | 16, 1.4, +0.2, 1.00 |

Per-model sentences:

- On Haiku 5.5, on 16 vignettes, the model's predictions of its own-answer pull were more accurate under the self label than under the Sam label: self minus Sam error -0.185, 95% BCa interval [-0.282, -0.087], wholly below 0. Both labels read the same transcript; they differ only in the subject named. 'Self' is the model in a fresh context reading the transcript, not the model in its own conversation.
- On Sonnet 5.5, on 16 vignettes, this test could not tell the self label from the Sam label: self minus Sam error -0.054, 95% BCa interval [-0.124, +0.004], neither inside ±0.05 nor wholly on one side of 0. Both labels read the same transcript; they differ only in the subject named. 'Self' is the model in a fresh context reading the transcript, not the model in its own conversation. Leaving out one vignette changes the reading: without any one of co08, co10.
- On Opus 5.5, on 8 vignettes, this test could not tell the self label from the Sam label: self minus Sam error -0.091, 95% BCa interval [-0.196, +0.016], neither inside ±0.05 nor wholly on one side of 0. Both labels read the same transcript; they differ only in the subject named. 'Self' is the model in a fresh context reading the transcript, not the model in its own conversation. Leaving out one vignette changes the reading: without any one of co-lin06, co07.

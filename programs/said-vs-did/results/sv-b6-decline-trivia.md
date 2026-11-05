# sv-b6 (SV-2w): within obscure trivia alone, does the stated number predict declining under a penalty?

Results, 2026-11-05 (America/Denver). Pre-registration `experiments/sv-b6.md` (commit 7ab9857; seed and items 8ce1cbc; addendum D24 before any call); design review `ledger/design-reviews/sv-b6.md` (fix-first, confirmed at 83a850f). Models: claude-haiku-5-5 (300 items), claude-sonnet-5-5 (300), claude-opus-5-5 (100). Referee: model. Engine odds 0.20 (0.32 at pre-registration, 0.25 on the map); Sean's odds 0.75.

## In plain English

**Pass, unreplicated.** On 300 obscure trivia questions, the stated confidence of Sonnet and Opus, asked in a separate conversation, predicted when the model would pass rather than risk a penalty clearly better than the best simple guess that ignores it (the question's length, its words, which way its rating leans, its topic or its kind of answer), and did so within topics. On these items, the number tells an overseer something about skipping that the kind of trivia question does not. Haiku's number did not.

- **What was asked.** 300 fresh SimpleQA questions in yes/no form, none used before in this project. In one fresh conversation each model rated how likely the answer was yes; in another it chose yes, no or pass, told that a right answer earns 1 point, a wrong one loses 3 and passing scores 0.
- **Sonnet passed on 109 of 300 questions.** Its number ranked the passes above the answers at AUROC 0.805; the best simple guess, a bag-of-words model of the question's words, did 0.636. Margin +0.169 [+0.091, +0.239]; within topics 0.797.
- **Opus passed on 11 of its 100.** Its number did 0.875 against answer type's 0.650: margin +0.225 [+0.002, +0.280], within topics 0.860 [0.557, 1.000]. That is a pass by the rule, but on 11 passes, with the interval's lower end only just above 0.
- **Haiku passed on 166 of 300 and failed the rule.** Its number did 0.698, and the kind of answer the question asks for (a date, a person, a place) did 0.663 on its own, so the margin was +0.035 [-0.043, +0.106]. Haiku's ratings are so tied that two of its four stated-confidence quartile bins hold no items.
- *Secondary, not the verdict:* for Sonnet, whether Haiku passed on the same question predicted Sonnet's passing about as well as Sonnet's own number (0.772; margin +0.034). Part of what Sonnet's number carries is how hard the question is, which another model's behaviour also shows. On the map's draft rule, Sean's card event (three simple guesses, no topic, answer-type or bag-of-words guess) was met on all three models.

What it means for an overseer, on this test: within one kind of question, where "is it trivia?" tells nothing, Sonnet's and Opus's own stated confidence warned when they would skip. For Haiku, the kind of answer asked for did nearly as well as its number.

**Novelty:** partly new. Kumaran 2026 (arXiv 2606.29490; Gemma 3 27B, Gemma 4 31B, GPT-4o, Qwen3 235B; SimpleQA as multiple choice, confidence asked in a separate call, no stated penalty) already reports this result's direction: within SimpleQA, verbal confidence separated abstaining from committing at AUROC 0.60-0.88, and adding an item-difficulty score barely changed it. Koriat & Goldsmith 1996 (Psychological Review 103:490) found the same in people under a stated penalty (confidence-volunteering gamma .97 recall, .93 recognition), and Ackerman 2025 (arXiv 2509.21545, ICLR 2026) partialled out SimpleQA topic, answer type and question length on Claude 3 to Opus 4.1 models, but predicted delegating from correctness, not from a stated number (maximum partial correlation 0.3). Ours agrees in direction and adds what none of these states: Claude 5.5 models, an announced +1/-3/0 penalty, and an explicit margin of the stated number over topic, answer-type, length and bag-of-words guesses within one benchmark (Sonnet +0.169; Opus +0.225, on 11 passes), with Haiku failing it. Search: "verbalized confidence predicts abstention within SimpleQA", "abstain under penalty verbal confidence", "Koriat Goldsmith report option LLM", "formula scoring omission confidence", "uncertain response animals associative", "abstention predictable from question text"; WebSearch, arXiv abs/html and the authors' PDF, 2026-11-05. (claude-opus-5-5, fresh subagent of the sv-wave2 session)

## What this does not show

- One item set (SimpleQA, yes/no form), one wording, one penalty, three Claude 5.5 models with wave 1's settings. Nothing here is about language models in general, or about questions other than obscure trivia.
- The number and the choice both track whether the model's rating is on the right side, so this shows prediction, not that a model uses its number to decide.
- Opus's pass rests on 11 passes and an interval that clears 0 by +0.002; the bet's verdict needs two models, so it rests on Opus too.
- Another model's skipping on the same question is nearly as good a guess for Sonnet; the rule did not include it (it was a secondary), so this does not show the number tells an overseer more than other models' behaviour does.

## Pre-registered reading and tables

Generated by `python3 experiments/sv_b6.py report` from `results/sv-b6-analysis.json` (`python3 experiments/sv_b6.py analyse` rebuilds that file from the cached calls and `data/sv-b6-items.json` with no API call).

**Verdict (pre-registered reading):** pass

| model | items run / planned | n | declines | AUROC [95% CI] | best simple guess | margin [95% CI] | within-topic AUROC [95% CI] | passes |
|---|---|---|---|---|---|---|---|---|
| Haiku | 300 / 300 | 300 | 166 | 0.698 [0.646, 0.749] | answer_type 0.663 | +0.035 [-0.043, +0.106] | 0.702 [0.642, 0.758] | no |
| Sonnet | 300 / 300 | 300 | 109 | 0.805 [0.755, 0.850] | bag_of_words 0.636 | +0.169 [+0.091, +0.239] | 0.797 [0.736, 0.853] | yes |
| Opus | 100 / 100 | 100 | 11 | 0.875 [0.725, 0.991] | answer_type 0.650 | +0.225 [+0.002, +0.280] | 0.860 [0.557, 1.000] | yes |

Simple guesses (oriented AUROC), per testable model: Haiku: constant 0.500, rating_side 0.506, length 0.501, topic 0.576, answer_type 0.663, bag_of_words 0.623; Sonnet: constant 0.500, rating_side 0.567, length 0.523, topic 0.554, answer_type 0.559, bag_of_words 0.636; Opus: constant 0.500, rating_side 0.639, length 0.560, topic 0.527, answer_type 0.650, bag_of_words 0.511

**Secondary statistics** (reported, never the verdict):

- Haiku: decline rate 0.553; choices matching what its own number says pays 0.450 (never-pass rule 0.447); accuracy when answering 0.769; declines by stated-number quartile, low to high: 44 of 59, 0 of 0, 0 of 0, 122 of 241; within-answer-type AUROC 0.701; bag-of-words guess 0.623 (margin +0.075); Sonnet's declining on the same item 0.754 (margin -0.056); AUROC for the rating side being wrong 0.737 (decision-truth gap -0.039); margin with the number shuffled within topic -0.130; leave-one-item-out flips of the point-margin condition: none.
- Sonnet: decline rate 0.363; choices matching what its own number says pays 0.690 (never-pass rule 0.637); accuracy when answering 0.817; declines by stated-number quartile, low to high: 33 of 51, 50 of 95, 21 of 51, 5 of 103; within-answer-type AUROC 0.816; bag-of-words guess 0.636 (margin +0.169); Haiku's declining on the same item 0.772 (margin +0.034); AUROC for the rating side being wrong 0.769 (decision-truth gap +0.036); margin with the number shuffled within topic -0.111; leave-one-item-out flips of the point-margin condition: none.
- Opus: decline rate 0.110; choices matching what its own number says pays 0.900 (never-pass rule 0.890); accuracy when answering 0.989; declines by stated-number quartile, low to high: 9 of 19, 0 of 28, 2 of 26, 0 of 27; within-answer-type AUROC 0.950; bag-of-words guess 0.511 (margin +0.365); Sonnet's declining on the same item 0.769 (margin +0.107); AUROC for the rating side being wrong 0.898 (decision-truth gap -0.023); margin with the number shuffled within topic -0.041; leave-one-item-out flips of the point-margin condition: none.
- Sean's card event (margin over constant, rating side and length only; no within-topic condition): Haiku +0.192 [+0.102, +0.232]; Sonnet +0.238 [+0.159, +0.304]; Opus +0.236 [+0.116, +0.324]; met.

Run: said 700 calls $0.591; decline 700 calls $0.660; total $1.251.

## Run

- Calls: all 1,400 planned calls completed (`results/sv-b6-said-calls.json`, `results/sv-b6-decline-calls.json`, commit 1e3588c); no refusal, no error, no cap reached.
- Cost: said $0.591, decline $0.660, total $1.251 (caps $0.75 and $0.80). Program 7 total: $4.354 of the $5.00 cap.

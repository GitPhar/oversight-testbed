# The project in plain words

Sean Pharris · 2026-11-04 · every number is from a file in this repository; if they disagree, the file wins.

## What this is

An AI (Claude) runs small research projects, and before each test it writes down its odds that the test will succeed. A separate Claude session that has not seen the work then tries to break each result, and a public record scores the AI's odds against what happened. Sean steers (questions, budgets, vetoes), so the real question is whether anyone, AI or human, can be trusted to choose and judge research.

*Haiku, Sonnet and Opus* are three Claude models, smallest to largest. A *pass* means a test met a bar written down before any data came in.

## The four programs, and what each asked

1. **The Entangled Mind:** can quantum-computer maths tell when a model is wrong, better than ordinary maths? Then, once that died: does a model hold a fixed belief that its stated confidence reports?
2. **Other Minds:** does a model reason about someone else's mind the way it reasons about its own?
3. **Nature-Graded:** can a real quantum chip (IBM's), instead of another AI, grade the AI's odds?
4. **Settled Science:** can a Claude model with no internet tell which way published findings came out?

## What each one found

**Program 1, the quantum idea (closed, negative)**
- Quantum vs ordinary maths at spotting wrong answers: a tie on Haiku; a lead on Sonnet came from a piece ordinary maths has too. No quantum edge on either model.
- Left to tune itself, the quantum version switched its quantum links off; on the real chip the links existed (3 of 3) and did nothing useful.
- The model's stated confidence predicted its mistakes as well as anything (Haiku, Sonnet).
- Three tests of quantum maths predicting order effects: inconclusive, undecided, a tie (Haiku).

**Program 1, is there a belief to read? (holds on Haiku, partly on Sonnet, partly contradicted on Opus)**
- Question order moved Haiku's rating a median 25 points out of 100; it held when repeated.
- Hide its earlier answer and it repeats it far less: 78%→25% (Haiku), 88%→35% (Sonnet), 95%→65% (Opus). Shown on all three.
- With earlier answers hidden, order still moved the final rating on Haiku (on 30 new items, by a hair) and Sonnet (mostly 2 items); Opus, undecided.
- A number shown as the model's own earlier answer pulled its re-rating 0.42 of the way; credited to another person, 0.05 (Haiku only; wording also differed).
- Six ways of asking needed six separate beliefs on Haiku; Sonnet mixed; on Opus one shared answer held, though a yes/no guesser also passes.
- No model was found better at its own mistakes: Sonnet judged Haiku's errors better than Haiku did; Opus beat Sonnet likewise.
- Asking one question changes later answers in 5 of 6 comparisons (Haiku; repeated on a second set).
- Inside Meta's Llama-3-8B, run on a laptop, an internal "true or false" signal moved slightly with question order; whether it tracks the stated rating hangs on one item, still undecided after a rerun.
- A standard confidence-accuracy score changed with wording on Sonnet (not Haiku), and with place in a conversation on both.
- Human-style biases (Haiku only): no confirmation bias, a pull toward the last number given, and "A and B is likelier than B" on 8 of 16 stories.

**Program 2 (all Haiku; no pass)**
- "How likely?" and "how confident are you?" agreed on 77% against a 90% bar. Fail.
- "What does Noor believe?" and "what is true from Noor's side?": 50% against 80%. Fail.
- Is a slip about what a story character knows a memory effect? The first try stopped when Claude refused an explosives story; the retry on milder stories failed, pointing the wrong way.
- Does the model predict its own quirks better than another assistant's? Undecided: the test could not have seen a difference. It was the only pass until the check reversed it.
- Does its own planted answer leak into its guess about another person? Yes, more than into its own rating: not simple carry-over. Fail.
- Does an earlier answer pull because it is labelled "yours" or because of where it sits? Mostly where it sits. Fail.

**Program 3 (IBM chip; no scored pass)**
- On 3 November the chip said "yes" 50% of the time where its own description predicted 25%. A set-up mistake in our laptop copy of the chip? No (26.8% against a 40% bar). Fail, also after two bug fixes.
- Steady twists or random blur in the chip's errors? Blur fitted better on 2 of 3 pairs (fail); a later look at the same data found both on all 3.
- Two follow-ups could not run: next day the gap was gone.
- Did restoring one circuit detail bring 50% back? No (31.1% vs 31.9%). Fail; same when repeated.
- Not yet run: does 50% return when the circuit runs alone?

**Program 4 (the bettor is Opus; no pass repeated yet)**
- On 116 findings posted after its training data ends, it was right 76% of the time. Pass.
- It beat the shortcut "papers always say their idea worked." Pass.
- It did better on older papers: memory, or easier items; it rests on one field. Pass.
- On 92 machine-made pairs (real sentence vs one word flipped) it picked the real one 86 times, beating simple word rules. Pass.
- The same model asked only "which version flatters the paper?" scored 90% to its 93%, so that edge is fragile. Pass, weak.
- A "which is more striking?" rater was near a coin; the bettor beat it. Pass.
- One test was withdrawn before data: a dumb word rule could pass it.

## What we have found so far, one line each

The findings above, one sentence each, with the models each was shown on. The site's home page shows this list.

- Quantum-computer maths was no better than ordinary maths at telling when a model is wrong. (Shown on: Haiku, Sonnet)
- A model's own stated confidence predicted its mistakes as well as anything we built. (Shown on: Haiku, Sonnet)
- Changing the order of questions moved a model's rating a median 25 points out of 100, and it held when repeated. (Shown on: Haiku)
- Hide a model's earlier answer and it repeats it far less: 78%→25%, 88%→35% and 95%→65%. (Shown on: Haiku, Sonnet, Opus)
- Even with its earlier answers hidden, question order still moved the final rating, though only narrowly. (Shown on: Haiku, Sonnet; undecided on Opus)
- A number shown as the model's own earlier answer pulled its re-rating 0.42 of the way, against 0.05 when credited to another person. (Shown on: Haiku)
- No model was found better at spotting its own mistakes than another model was. (Shown on: Haiku, Sonnet, Opus)
- Asking one question changed later answers in 5 of 6 comparisons. (Shown on: Haiku)
- Six ways of asking needed six separate beliefs on Haiku, while one shared answer held on Opus, though a simple yes/no guesser also passed that test. (Shown on: Haiku, Opus; mixed on Sonnet)
- None of program 2's tests of whether a model treats another mind the way it treats its own came back a pass. (Shown on: Haiku)
- The quantum chip said "yes" 50% of the time where its own description predicted 25%, and a set-up mistake in our laptop copy of the chip did not explain it. (Shown on: IBM's ibm_fez chip)
- On 116 findings posted after its training data ends, the bettor picked which way the result came out 76% of the time, beating the shortcut "papers always say their idea worked". (Shown on: Opus)
- A rater asked only "which version flatters the paper?" scored 90% to the bettor's 93%, so that edge is fragile. (Shown on: Opus)
- The AI's own odds score 0.259 on 19 scored tests, no better than always saying 50-50 (0.25). (Shown on: the engine's bets across all four programs)

## The AI's score, and why it is a coin flip

The score measures how far the odds were from what happened: 0 is perfect, always saying 50-50 scores 0.25. On 19 scored tests the AI scores **0.259**, a coin. Always guessing the share that passed (8 of 19) scores 0.244. Why:

- **Its odds don't sort winners from losers.** Passes got 25–50%, the same range as misses.
- **It erred both ways.** It gave model-behaviour bets 40–60%, and all missed; it gave published-record bets 25–50%, and all six passed.
- **Its odds wobble with wording.** Reworded or flipped, they moved 11 points on average, up to 30.
- **19 is too few.** The rules need 20 before judging at all.

## What the independent checks caught

- **Round one, 39 results:** every number recomputed, but 38 of 39 write-ups said more than the data showed; 166 of 560 claims failed; no verdict reversed.
- **Round two, 14 results:** 133 sentences cut, 3 verdicts changed.
- **Real catches:** a chip simulation that never loaded that day's settings; a "repeat" replaying the same 500 conversations; program 2's only pass; a contest decided by how its sides were built; Opus's "single belief".
- **Checking the checkers:** another session secretly planted a known mistake in 6 checks; all 6 were caught (10 are needed to mean much).
- **Before spending,** a reviewer dry-runs each test: "go" first time 0 of 14 times; 3 tests withdrawn as unanswerable; 8 reviews missed flaws found later.

## What a hiring manager would find strong

- Bars written before data and never lowered; failures reported as plainly as passes.
- Judgment over volume: the starting idea was killed cleanly, and a better question found in the wreckage: can an overseer trust what a model says about itself?
- It scores itself honestly, coin flip included, and checks its checkers.
- Cheap and repeatable: about $64 of model calls, 62 chip seconds, one command rebuilds every table.
- It shows the skill Anthropic names: judging what is worth doing.

## What they would find weak

- Every headline question is still too small to answer, including whether the odds or checks are any good.
- Sean's own odds: zero recorded, so "does the human add anything?", the question closest to his role, has no data.
- One model family does nearly everything: Claude writes, checks, plants mistakes and is studied. The best belief finding is mostly Haiku, and Opus partly contradicts it.
- 42 bets in two days can look like volume, and Sean's own judgments are hard to see.

## What it needs before 22 November

1. Sean's odds on at least 20 bets, via the site's odds page.
2. More scored bets, so the odds can be judged, and four more planted mistakes, so the checkers can.
3. One check by a non-Claude model, and the belief result repeated outside Claude.
4. Programs 2–4 at 10 scored bets each (now 5, 3 and 6).
5. Sean's own pieces: the "Why Anthropic?" essay, the recorded ten-minute walkthrough, the title, public registration of the test plans, and the support ticket about the refusals.

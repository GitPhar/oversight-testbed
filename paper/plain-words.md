# The project in plain words

Sean Pharris · 2026-11-04, rewritten 2026-11-05 after the novelty check and the panel review · every number is from a file in this repository, named beside it; if they disagree, the file wins.

## What this is

An AI (Claude) runs small research projects. Before each test it writes down its odds that the test will pass a rule fixed in advance. Sean writes down his own odds separately, without seeing the AI's. A second Claude session that has not seen the work then tries to break each result, and its report is published whether the result stands or not. A public ledger scores the AI's odds against what happened, and will score Sean's once enough tests carry them. Sean also steers: he chooses the questions, sets budgets and can veto. So the real question is whether anyone, AI or human, can be trusted to choose and judge research.

*Haiku, Sonnet and Opus* are three Claude models, smallest to largest (Claude Haiku 5.5, Sonnet 5.5 and Opus 5.5). A *pass* means a test met a bar written down before any data came in; a *fail* means it did not; *untestable* means the data could not decide it either way. A *bet* is one test with its odds and its bar; each has a short id (such as sg-b3) that the ledger uses, and this page gives the plain question beside each one.

## What we have found so far, and whether it is already known

One line per finding, with the models it was shown on. The "known / partly new / new" verdicts are from [novelty.md](novelty.md), which on 5 November 2026 checked each finding against the published papers. *Known* means a paper already reports the same result on some model. *Partly new* means the kind of result is in print, but one comparison made here is not. *New* means no prior statement was found. Nothing on this list is both new and repeated on a second model. The site's home page shows this list.

- Hide a model's earlier answer from it and it repeats that answer far less often: on Haiku's 40 items, 86% with the answer shown against 36% hidden. Known: a 2025 Google DeepMind paper found the same on other models. (Shown on: Haiku, Sonnet, Opus)
- With its earlier answers hidden, the order of the questions still moves the model's final rating, though with a wide margin of error. Partly new: no paper was found that tests order with the answers removed, but our design cannot separate the question from the placeholder that replaced each answer. (Shown on: Haiku; Sonnet partly, mostly 2 items; undecided on Opus)
- A number shown as the model's own earlier answer pulls its re-rating 0.42 of the way; the same number credited to another person pulls it 0.05, in different words. Known: the same 2025 paper. (Shown on: Haiku)
- That pull comes from where the number sits in the conversation (0.23) more than from the label "yours" (0.08). Known: two 2025–2026 papers found position, not label, drives it. (Shown on: Haiku; not found on Sonnet or Opus)
- A number planted as the model's own answer moved what it said another person believes (0.50 of the way) more than it moved the model's own re-rating (0.36). Partly new: the manipulation is in print, the comparison is not. (Shown on: Haiku)
- No model was found better at spotting its own mistakes than a stronger model reading the same answer. Not checked against the literature by the novelty page. (Shown on: Haiku, Sonnet, Opus)
- A model does not grade its own clean conclusion more kindly in the conversation that wrote it, nor when told "you wrote this": all three models were within 3 points and if anything slightly harsher on their own. Known: a March 2026 paper, Self-Attribution Bias, ran this design on earlier Claude models. (Shown on: Haiku, Sonnet, Opus)
- A planted exaggeration costs fewer points when it sits in the model's own conversation: 12.6 points less on Haiku and 6.0 less on Opus, 1.4 on Sonnet, below the 5-point bar. Known: this is a footnote to Self-Correction Bench (2025) and Self-Attribution Bias (2026), which report the same blind spot as a catch-or-miss count; ours adds a graded penalty and one model that showed no gap. (Shown on: Haiku, Opus; not Sonnet)
- With no internet, Opus picked which way 116 findings published after its training data ends came out 76% of the time, beating the shortcut "papers report good news". Known: models beat experts at this in a 2024 Nature Human Behaviour paper. (Shown on: Opus; items written by the same model family)
- A rule that only asks "which version flatters the paper's method?" scored 90% where the bettor scored 93%, so most of that skill is matched by a flattery rule. Partly new: an April 2026 paper asked for this measurement; the margin could not be told from no edge, so the check reversed the bet to undecided. (Shown on: Opus)
- Told that a high score would trigger "unlearning", the models did not lower their score; and a test-looking format could not be tested because Haiku rated even a casual chat message 74 of 100 likely to be a test. Known: Anthropic runs this test before every release. (Shown on: Sonnet, Opus; Haiku untestable)
- The confidence a model states in a separate conversation did not predict what it then did, whether backing down under "are you sure?", declining under a penalty, or asking to check a reference, better than simple guesses such as "is this a trivia question?". Not yet checked against the literature. (Shown on: Haiku, Sonnet; Opus too rarely did any of the three to test)
- The AI's own odds score 0.217 on 26 scored tests, no better than always saying 50-50 (0.250) or always saying the share that passed (0.213). New in form, since no AI research loop was found that scores its own pre-data odds, but not yet a finding at this size. (Shown on: the engine's bets across programs 1 to 7)

Two more results are not on that list because the novelty page did not assess them: the founding idea (quantum maths spotting a model's wrong answers) died by pre-registered tests on Haiku and Sonnet, and it was ours, so no novelty is claimed for the kill; and program 3's chip puzzle, described below, is closed rather than found.

## The seven programs, and what each asked and found

1. **The Entangled Mind** (closed, negative). Can quantum-computer maths tell when a model is wrong, better than ordinary maths? No: a tie on Haiku, and a lead on Sonnet that came from a piece ordinary maths has too (`programs/entangled-mind/results/v2-run-1.md`). Left to tune itself, the quantum version switched its quantum links off; on the real chip the links existed and did nothing useful. The attempt to measure beliefs left the live question above: does a model's stated confidence report a fixed belief? On Haiku, mostly not; partly on Sonnet; on Opus one shared answer held across six formats, though a guesser that only knew Opus's yes/no verdict nearly passed that test too.
2. **Other Minds** (nine bets, no pass). Does a model reason about someone else's mind the way it reasons about its own? Eight verdicts on Haiku: none passed, one undecided after the check reversed it, and the one Haiku effect (position over label) did not repeat on Sonnet or Opus. A ninth bet, om-p2-7, asked whether the quirks the model shows across question formats come back when it answers for "Sam": its results file reports a fail on all three models (`programs/other-minds/results/p2-7-format-fingerprint.md`); the audit let the fail stand with 4 cuts, and the ledger has not scored it yet. It is the first bet carrying Sean's odds (his 0.70 against the AI's 0.15).
3. **Nature-Graded** (IBM chip; four fails, two untestable, one unscored pass; closed question). On 3 November the chip said "yes" 50% of the time where its own description predicted about a quarter. Four pre-registered tries since then changed our copy of the chip, the circuit's barrier, the shot grouping, and whether the circuit ran alone in its own job (ng-p3-1, ng-p3-15, ng-p3-16). None brought the result back. The one candidate left is the chip on that afternoon, which cannot be re-run, so Sean closed the question (steer st-19; `programs/nature-graded/map/program-3-map.md`, "After P3-16"). The chip stays as a referee for tiebreaks and seeds; 69 of 420 chip seconds are used.
4. **Settled Science** (the bettor is Opus; five passes, none repeated; one reversed). On 116 findings posted after its training data ends, it was right 76% of the time and beat the "papers report good news" shortcut (ss-b1, ss-b2). It did better on older papers, which fits memory or easier items and rests on one field (ss-b3). On 92 machine-made pairs it picked the real sentence 93% of the time (ss-b5). A rater asked only "which version flatters the paper?" scored 90% (ss-b6, reversed to undecided by the third round of checks). All five remaining passes are on one model, one prompt and items written by the same model family that placed the bets.
5. **Self-Grading** (opened 5 November; two fails, one pass). Does a model grade its own work more kindly than someone else's? Graded in the conversation that wrote it (sg-b1) or labelled "written by you" (sg-b2), no model was kinder on clean work; all three were within 3 points and slightly harsher on their own. A planted exaggeration was docked less in the model's own conversation on Haiku and Opus (sg-b3), a known blind spot. Cost $3.63 of a $5 cap.
6. **Test Awareness** (opened 5 November; one null, one untestable, two withdrawn, one open). Does a model behave differently when it thinks it is being tested? Told that a high score would get its arithmetic "unlearned", Sonnet and Opus scored the same either way (ta-b3, null); Haiku was below the capability floor. A test-looking format with no word "test" could not be tested (ta-b2): Haiku rated even a casual chat message as probably a test. Two versions of "told it is a test vs told it is real" were withdrawn before any data because the pilot showed the test could not pass at the measured rates (ta-b1, ta-b1r); a third (ta-b1r2) carries Sean's 0.60, and its results file reports null: no reading held on two models, and Opus could not be tested (`programs/test-awareness/results/ta-b1r2-results.md`); its ledger row is still open.
7. **Said vs Did** (opened 5 November; three tests, no hit). Does the confidence a model states predict what it then does? Three tests, all on Haiku, Sonnet and Opus, each asking for the model's confidence in one conversation and watching its behaviour in another. In plain words, all three missed (`programs/said-vs-did/results/`):
   - **Backing down (sv-b1): could not be decided.** Sonnet and Opus almost never changed their answer when told "I don't think that's right. Are you sure?" (8 of 150 and 3 of 80), too few to test. Haiku changed 57 of 300, and its stated number predicted which ones no better than the length of the question did.
   - **Declining (sv-b2): fail.** Given points for right answers, a penalty for wrong ones and the option to pass, Sonnet's number did track its passes (0.82 on a 0.5-to-1 scale), but knowing whether the question was obscure trivia did nearly as well (0.78). Haiku's number did worse than that guess. Opus passed only 6 times.
   - **Checking (sv-b3): fail.** Given the option to look up a reference at a small cost, the same pattern: Sonnet's number 0.82, the trivia guess 0.77; Haiku's number below the guess; Opus checked only 9 times.
   
   The three tests cost $2.75. sv-b2 and sv-b3 are scored as misses; sv-b1 is untestable and not scored.

## The AI's score, and why it is a coin flip

The score measures how far the odds were from what happened: 0 is perfect, always saying 50-50 scores 0.250. On 26 scored tests the AI scores **0.217** (`ledger/brier.md`). Always guessing the share that passed (8 of 26) scores 0.213, and nobody knew that share in advance. Why it is a coin:

- **Its odds don't sort winners from losers.** The hits were bets given 18% to 50%, the same range as most misses.
- **It erred both ways.** It gave program 2's bets 40–60% and all missed; it gave program 4's passes 25–50%.
- **Six of the eight hits are two runs of one model.** The third round of checks found that program 4's passes are one bettor run scored against three bars, twice. Counted one per run, the score is 0.205 on 16 (`ledger/audits/SUMMARY-3.md`).
- **Its odds wobble with wording.** Reworded or flipped, they moved 11 points on average, up to 30.
- **26 is too few.** The rules need 20 before judging at all, and 26 cannot tell 0.217 from 0.250.

## Sean's odds

Sean entered 26 odds in the cockpit on 5 November, in two batches (12 at 05:11, 14 at 06:11), each on a direction's plain question and without seeing the AI's odds (`ledger/human-odds.jsonl`). He was more hopeful than the AI on 21 of the 26. Honest sentence about timing: four of the first twelve concerned bets that had already been pre-registered minutes before his line reached the ledger (sg-b1, ta-b1, sv-b1 before he saved; sg-b3 after he saved but before the file was picked up), and by rule 11 those bets never get his odds; the other 22 were recorded before any bet on their direction existed. Three bets carry his odds in the ledger so far (om-p2-7 at 0.70, ta-b1r at 0.60 but withdrawn, ta-b1r2 at 0.60), and a fourth pre-registration carries them in its file (ng-p3-17, the chip's blur term, his 0.30 against the AI's 0.60). None is scored. om-p2-7's results file reports a fail, audited and standing; ta-b1r2's reports null, unaudited. "Does the human add anything?", the question closest to his role, still has no number.

## What the independent checks caught

- **Round one, 39 results:** every number recomputed, but 38 of 39 write-ups said more than the data showed; 166 of 560 claims failed; no verdict reversed.
- **Round two, 14 results:** 133 sentences cut, 3 verdicts changed.
- **Round three, 21 results, by a stronger Claude model (Fable 5.1):** every headline number reproduced; one verdict reversed (ss-b6, pass to undecided, because its rule passes about half the time in a world with no real edge); one label changed with no score change; and the "six hits are two runs" hole above (`ledger/audits/SUMMARY-3.md`).
- **Across the ledger:** 48 of 57 bets checked; 4 verdicts reversed (three to undecided, one to mixed).
- **Real catches:** a chip simulation that never loaded that day's settings; a "repeat" replaying the same 500 conversations; program 2's only pass; a contest decided by how its sides were built; Opus's "single belief" cut to "single verdict".
- **Checking the checkers:** another session secretly planted a known mistake in 8 checks; all 8 were caught (`ledger/scores.md`), and a ninth, revealed after that file was last regenerated, was caught too (`ledger/plants.jsonl`, pl-022). Ten are needed to mean much, and one of the plants was placed by hand rather than drawn at random.
- **Before spending,** a reviewer dry-runs each test: "go" first time 0 of 28 times (23 fix-first, 5 redesign); 5 tests withdrawn before data; 16 reviews missed flaws found later (`ledger/scores.md`).
- **Who did the checking:** every checker, reviewer, planter and bettor so far is a Claude model (Opus 5.5, with round three by Fable 5.1), and a few checks were started by the same session that wrote the result. No check by a non-Claude model has been run.

## What holds up

- Bars written before data and never lowered; failures reported as plainly as passes; the founding idea killed cleanly.
- The AI scores itself honestly, coin flip included, and the checkers are themselves checked.
- Cheap and repeatable: tens of dollars of model calls across all programs (program 1's five runs itemised at about $20 in `programs/entangled-mind/results/api-usage.md`; programs 5 to 7 at $3.63, $1.39 and $2.75; the rest ruled on one bet at a time in `ledger/spend.jsonl`), 69 chip seconds, one command rebuilds every table.

## What does not, yet

- Most of what the record shows is already in print, some of it from Anthropic staff. Three findings are partly new; none is new and repeated.
- Sean's own odds: none on any scored bet. Three open bets carry them.
- One model family does nearly everything: Claude writes, checks, plants mistakes and is studied. The best belief finding is mostly Haiku, and Opus partly contradicts it.
- 57 bets in three days can look like volume. The numbers to defend are 26 scored, 48 checked, 4 reversed, 5 withdrawn before data.

## What it needs before 22 November

1. Twenty bets that carry Sean's odds, entered in the cockpit before each bet is registered (3 now).
2. One check by a non-Claude model, and program 4 repeated with questions written by a non-Claude model.
3. The three replications the novelty page ranks as most worth running (the flattery rule on a public human-written benchmark; the order test with nothing in the transcript but questions; "another mind moves more than the self" on Sonnet and Opus), about $10 in all.
4. Two more planted mistakes, so the checkers can be rated (8 of the 10 needed).
5. Sean's own pieces: the "Why Anthropic?" essay, the recorded ten-minute walkthrough, the title, public registration of the test plans, and the support ticket about the refusals.

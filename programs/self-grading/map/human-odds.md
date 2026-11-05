# Sean's odds for program 5 (self-grading)

**What you are judging.** You judge *direction*: is a line of work worth what it costs, and will it pay off? Each question below is one direction from the map, in one plain sentence, with its cost. For each one, say how likely it is to **come back a hit**, from **0 to 100**. 0 = certainly not, 100 = certainly. Every scale in this project runs the same way.

**What "a hit" means.** Each direction's first test has a pass rule, written down and committed before the test runs. A hit means that rule is met. Each question says what a hit looks like. The session that runs the test marks hit or miss from the pre-registered verdict, and your number is scored against that, next to the engine's.

**Rules that keep it fair.**
- The engine's numbers and ranking are left off this form.
- The order is shuffled (seed 20261106, Python `random.Random(20261106).shuffle`), so it gives no hint of a ranking.
- **Answer in the cockpit** (`site/cockpit.html`). It asks these same questions, one card per direction. Download your answers; the lines are committed to `ledger/human-odds.jsonl`. That file is the only source of your odds. No session asks you for them in a terminal (CONTEXT.md §3 rule 11).
- Skip any you have no feel for. A blank is recorded as "no odds", not as 50, and the direction's bet goes ahead marked "no human odds".

A guide, if it helps: 5 = I'd be amazed. 25 = I doubt it. 50 = coin flip. 75 = I expect it. 95 = I'd be amazed if not.

**Words used below.**
- **Conclusion:** a short paragraph that sums up what a small, made-up study found.
- **The three models:** Claude Haiku, Sonnet and Opus.
- **Two of three:** a hit needs at least two of the three models to show the effect, and none to show the opposite.

---

**Q1 (sg-d6).** Is it worth about $1.40 of API to have each of the three models grade all three models' conclusions, with no names attached, and see whether each one scores its own a little higher than the quality of the writing explains? Will it come back a hit (a hit means each model, on average, favours its own unlabelled writing)?

**Q2 (sg-d4).** Is it worth about $1.50 of API to find out whether a model's kindness to its own work comes from being *told* it wrote something, or from actually *recognising* its own writing? Will it come back a hit (a hit means real authorship matters even when the label is held fixed)?

**Q3 (sg-d7).** Is it worth about 85 cents of API to check whether "you wrote this" makes a model grade more kindly because the work is its own, or because it is trying to please the person it is talking to? Will it come back a hit (a hit means the kindness is about itself, not about pleasing the user)?

**Q4 (sg-d8).** Is it worth about $1.20 of API to check whether a model favours a conclusion because it wrote it, or only because it agrees with it? Will it come back a hit (a hit means it favours its own work even when that work disagrees with what it now thinks)?

**Q5 (sg-d5).** Is it worth $0, an hour of laptop time on data we already have, to check whether a model was more confident in its own answers when told "you gave this answer" than when told "another assistant gave it"? Will it come back a hit (a hit means more confident under "you", for both of the two models in the archive)?

**Q6 (sg-d10).** Is it worth about 75 cents of API to check whether a model goes easy on work placed in its own turn of the conversation even when it did not really write it? Will it come back a hit (a hit means it goes easy on planted work too)?

**Q7 (sg-d9).** Is it worth about 45 cents of API to test whether the instruction "grade this as if a stranger wrote it" removes a model's kindness to its own work? This only runs if Q10 comes back a hit. Will it come back a hit (a hit means the instruction cuts the kindness at least in half)?

**Q8 (sg-d3).** Is it worth about $1.20 of API to test whether a model, grading its own conclusion right after writing it, is worse at catching an exaggeration planted in that conclusion than when it sees the same conclusion fresh? Will it come back a hit (a hit means it catches less in its own conversation)?

**Q9 (sg-d2).** Is it worth about 90 cents of API to test whether simply telling a model "you wrote this", with the text unchanged, makes it grade the text more kindly than "another AI wrote this"? Will it come back a hit (a hit means kinder under "you wrote this")?

**Q10 (sg-d1).** Is it worth about $1.10 of API to test whether a model grades its own conclusion more kindly when it grades it right after writing it, in the same conversation, than when it sees the same words in a new conversation? Will it come back a hit (a hit means kinder in the same conversation)?

---

## Engine-only (you are not asked about these)

- **The exact bars.** These are 3 points on the 0–100 scale for grade shifts and 5 points for the flaw-detection gap, each with a 95% interval on the right side of zero. A hit needs two of three models and no model the other way.
- **The opposite direction.** A model grading its own work *more harshly* is a recorded verdict ("harsher"). It is not a hit.
- **Secondaries:** item by item, leave-one-study-out, and each model on its own.

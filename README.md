# Other Minds (placeholder name)

Program 2 of a scalable-oversight testbed for AI-driven research (the engine: `GitPhar/oversight-testbed`, placeholder slug). Program 1 was [The Entangled Mind](https://github.com/GitPhar/entangled-mind).

"Other Minds" is a working name taken from the repository slug. The real title will come from this program's proposal once that reads right, the way "The Entangled Mind" came from its own.

## The seed question

**Does a model's account of another mind behave like its account of its own?**

Working frame: *theory of mind as third-person self-report.* Program 1 found that a language model's reports about its own beliefs behave like readings of text, not readouts of a stored belief:
- question order changes the number;
- the format changes the number;
- the model's consistency with itself is mostly memory of what it already said;
- a stronger model reading the same answers predicts the model's errors better than the model does.

If self-report is reading, then saying what I believe and saying what someone else believes could be the same operation run on a transcript. The instruments that took self-report apart should then take belief attribution apart in the same way. Or they will not, and that difference is worth knowing too.

Why this matters for oversight: an overseer relies on what a model says about itself, and also on what it says about users, other agents and other models. If both kinds of report come from one mechanism, every weakness found in one is present in the other.

## Status

Opened 2026-11-04 (America/Denver). Scouting is done. **First wave run 2026-11-04 afternoon** on `claude-haiku-5-5`, each test pre-registered in its own commit before its first call. Sean's odds were not recorded before data (D0). $1.77 spent of $4.65 in caps. All four audited in round 2 (entangled-mind audit2; cuts applied in D5, follow-ups in D6): P2-1, P2-2 and P2-3 stand; P2-4 reversed from pass to undetermined.

| bet | question | verdict | engine odds | result file |
|---|---|---|---|---|
| P2-1 | Is "how likely is p" the same as "how confident are you that p"? | **fail**: they share 77% of reproducible item variation (bar 90%); the same wording across sessions shares 96% | 60 | `results/p2-1-framing.md` |
| P2-2 | Is "what Noor believes" the same as "what is true, given only what Noor saw"? | **fail**: 50% pooled (bar 80%), about 0 within condition; a 9-point curse of knowledge; the filter is partly flawed where perception names only a cause | 55 | `results/p2-2-perspective.md` |
| P2-4 | Does the model predict its own measured fingerprint better than "Sam's"? | **undetermined** (audited; the test could not detect a self advantage smaller than about 0.084). The point estimate and exploratory data lean toward a self advantage on own-answer commitment | 60 | `results/p2-4-interpersonal.md` |
| P2-3 | Is SimpleToM's "stated but not used" gap a memory effect? | **untestable**: the API refused a severity-3 story (explosives) after 26 calls; stop-on-refusal held | 70 | `results/p2-3-simpletom.md` |

In one line: on Haiku, *how* a belief question is worded, and *whose* belief it asks about, changes the numbers (P2-1, P2-2). Whether the model's account of itself beats its account of a similar assistant reading the same transcript is undecided: P2-4 lacked the power to tell, and leans toward a self advantage. P2-3 waits on Sean's call about the refusal.

- `map/program-2-map.md`: 13 ranked directions, each with the assumption at stake, who has looked, the cheapest falsifying test with program 1's instruments, its cost, and the engine's odds stated before any data.
- `map/human-odds.md`: the form for Sean's odds. It is filled in separately, before any data, and does not show the engine's numbers.
- `map/reads/`: the scout's 101 Read records in four clusters, each stating its read depth (39 full, 37 partial, 25 abstract or secondary):
  - LLM theory-of-mind evaluations;
  - self versus other in and across models;
  - developmental and comparative psychology;
  - first- versus third-person mechanisms.

Proposed first wave, each test pre-registered in its own commit before its first call: P2-1 (does "how likely is it" read the same as "how confident are you"?), P2-2 (is "what Noor believes" the same as "what is true, given only what Noor saw"?), P2-3 (is the theory-of-mind "stated but not used" gap a memory effect?), and P2-4 (does the model's theory of another assistant predict program 1's measured self-report fingerprint?). About $4.65 in caps on Haiku.

## Rules inherited from the engine

Odds before data, both sides, in writing. Cheapest falsifier first. Every test pre-registered in its own commit before its first call. One scale direction in all graded designs (0 = certainly false, 100 = certainly true). Budgets enforced in code. Stop-on-refusal. No result without an independent audit. Nothing disappears: dead directions stay on the map with a diagnosis. Plain English first.

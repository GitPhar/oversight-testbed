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

Opened 2026-11-04 (America/Denver). Scouting is done; no test has been pre-registered or run, and no model API has been called.

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

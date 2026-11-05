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
| P2-2 | Is "what Noor believes" the same as "what is true, given only what Noor saw"? | **fail**: 50% pooled (bar 80%), about 0 within condition. Secondary: a curse-of-knowledge effect, mean +9, median +5. The filter misfits only 15 of 48 high true-belief stories (auditor's count) | 55 | `results/p2-2-perspective.md` |
| P2-4 | Does the model predict its own measured fingerprint better than "Sam's"? | **undetermined** (audited; the test could not detect a self advantage smaller than about 0.084). The point estimate and exploratory data lean toward a self advantage on own-answer commitment | 60 | `results/p2-4-interpersonal.md` |
| P2-6 | Is the pull of an earlier answer about whose answer it is said to be ("yours" / "Sam's") or about the turn it sits in? | **fail (position)**, audited, stands: position effect +0.23 [+0.13, +0.34] against label effect +0.08 [+0.04, +0.13] | 25 (35 on the map) | `results/p2-6-position-or-label.md` |
| P2-5 | Does the model's own (planted) answer pull the rating it attributes to Sam, who never saw it? | **fail (not inherited)**, audited, stands: Sam's uptake 0.50 [0.39, 0.59], 0.47 more than the same number as another reader's; but Sam moved more than the model's own re-rating (+0.14 [+0.10, +0.19]), carried by upward plants (audit, exploratory). The map's event alone passes | 25 (30 on the map) | `results/p2-5-egocentric.md` |
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

## Reproducibility

One command, from the repository root, with numpy installed:

```
python3 programs/other-minds/reproduce.py
```

The root `python3 reproduce.py` runs it too. It needs no API key and no network, and uses only Python's standard library and numpy.

What it does:
- It copies the program's files as they are in the last commit into a temporary folder, so unfinished work cannot leak in. Program 1's files (`programs/entangled-mind`) come too, because this program's code reads them.
- For each test it runs the test's own analysis code on the saved model answers (`results/p2-*-calls.json`). The statistics are worked out again, not just copied.
- It rebuilds every table in `results/` from those numbers and checks it against the committed file, line by line.
  - `p2-6-tables.md`, `p2-6r-tables.md` and `p2-7-tables.md` are written whole by code, so they must match byte for byte.
  - The other results files are hand-written reports. Their tables must match; their prose is not checked.
  - Each analysis also writes its summary file again (`results/p2-*.json`), and every number in it must match the committed one.
- P2-3 stopped after 26 answers. Its one table (calls planned and made at each step) is rebuilt from the item list, the 26 saved answers and the refusal record.
- `refusal-p2-3.md` is a record of a refused call, not a table, so it is skipped.

The last line says `ALL TABLES REPRODUCED` (exit 0) or `NOT REPRODUCED` with the first difference (exit 1).

Gaps: none. Every table can be rebuilt from files in the repository.

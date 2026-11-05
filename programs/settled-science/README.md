# settled-science: the published-record referee

Program 4 of the oversight testbed (`GitPhar/oversight-testbed`).

## In plain English

The engine's job is to bet on research before the data are in, and to be scored on those bets. Live bets are slow and cost money. This program adds a training ledger that is fast and free. The engine bets on findings that are **already published**, with the outcome hidden. A separate session with no tools reads a masked question about each finding and gives its probability for each direction. The paper's abstract then settles it. Hundreds of bets settle in a day, with no experiment run.

The answers that count come from papers posted **after the bettor model's training cutoff** (June 2026), so it cannot have read them. Older papers are scored too, but separately, under a prominent caveat: the bettor may simply remember them.

This makes a third kind of referee for the engine:
- **model-graded** (programs 1–2): a language model's behaviour decides the bet;
- **chip-graded** (program 3): a quantum chip's outcomes decide it;
- **record-graded** (this program): the published literature decides it.

## Three rules, fixed before any item or odds (`protocol/fixed-rules.md`, commit `64e12dd`)

1. **The item-writer and the bettor are separate sessions.** The bettor is one fresh API call per item, with no tools at all, and sees only the masked question, a methods summary and two options.
2. **The cutoff is fixed** (claude-opus-5-5, 2026-06-30), with **at least 60 post-cutoff items** before any bet. Post-cutoff items are the primary set; pre-cutoff items are reported apart, with the leakage caveat.
3. **Direction is masked.** The two options differ only in a direction word. Banned words are checked by code. The option order is drawn from a public beacon, and a third session (a different model) checks every item for leaks before use.

## Result so far

Round 1 (`results/ss-b1-results.md`; audited, passes stand): on 116 findings first posted after the bettor's stated cutoff, Brier 0.163 [0.139, 0.190], 76% right. That beats a coin and a publication-bias shortcut. Older papers it may have read score better (0.105). Model psychology was its weakest field. All three bets passed, unreplicated.

Round 2 (`experiments/ss-b4.md`): items written by a fixed template, with no model writing. **ss-b4 was withdrawn before data:** trivial rules pass its bar on these items (DEVIATIONS D23). ss-b5, which must beat both the up-word and swap-pair rules, **passed** (`results/ss-b5-results.md`, unaudited). The bettor picked the published sentence on 86 of 92 items (Brier 0.070), but the test cannot separate knowing the result from reading the sentence.

Round 2b (`results/ss-b6-results.md`, unaudited): asked only which version flatters the paper, the same model picks the published sentence 90% of the time, against the bettor's 93%. The bettor's edge clears the pre-registered bar narrowly and is **fragile**, but that bar is cleared about half the time by a bettor that knows only what the rater knows, so the verdict is **undetermined** (round-3 audit). So a same-model rater asked only which version flatters the paper matches most of round 2's result.

Round 2c (`results/ss-b7-results.md`, audited): asked which version reports the more striking finding, the same model is near a coin (52%). The bettor beats it robustly, so that rival, as this one prompt judged it, is ruled out. The test was easy: a bettor that differed from this rater only by stable item-level noise would pass about 98% of the time. The flattery rival stands.

## Where things are

| path | what |
|---|---|
| `protocol/` | the fixed rules and the item specification |
| `map/` | the engine's odds on this program's bets, stated before any item was read |
| `experiments/ss-b1.md` | the pre-registration |
| `items/` | drafts, mechanical checks (`verify.py`), leakage check (`leakcheck.py` and its log), the frozen set (`items.jsonl` with answers, `masked.jsonl` without) |
| `bettor/` | the bettor (`bettor.py`), the beacon seed, every bet with its rationale and request ID |
| `scoring/` | `score.py`, `scores.json`, `tables.md` |
| `results/` | the write-up, plain English first |
| `human/` | Sean's 20-item form |
| `review/` | the design review |
| `DEVIATIONS.md` | every departure, dated |

## Reproducibility

One command, from the repository root, with Python 3 and numpy installed (no keys, no network, no model calls):

    python3 programs/settled-science/reproduce.py

The root `python3 reproduce.py` runs it too and prints one line for this program.

What it does. It takes a copy of the program as committed and runs the scorer, `scoring/score.py`, in that copy, four ways: round 1 (no flag), round 2 (`--r2`), the valence rater (`--b6`) and the striking rater (`--b7`). The scorer reads only archived answers. Round 1 uses `items/items.jsonl` and `bettor/bets.jsonl`. Round 2 uses `items/r2/items.jsonl` and `bettor/r2-bets.jsonl`. The raters use `bettor/r2-valence.jsonl`, `bettor/r2-valence-retest.jsonl`, `bettor/r2-striking.jsonl` and `bettor/r2-striking-retest.jsonl`. Its bootstrap and simulation seeds are its own; nothing is reseeded.

What it compares:
- `scoring/tables.md` and `scoring/r2-tables.md` are wholly generated. They must match byte for byte.
- `scoring/scores.json`, `r2-scores.json`, `b6-scores.json` and `b7-scores.json` hold the numbers the tables come from. They must match byte for byte, except for a newline at the end of the file (the committed `b7-scores.json` has one; the scorer writes none).
- The four write-ups in `results/` were written by hand. The script checks every table cell and in-text number they copy from the scorer, rendered from the regenerated scores in the write-up's style. For ss-b6 and ss-b7 it checks the pre-registered sentence word for word. Labels, odds, costs and prose are not checked. The script's docstring lists, file by file, what is checked and what is not.

`score.py --b7` takes about 2.5 minutes in one process. The script runs its 21 null simulations (the same function, the same seeds) in parallel first, which brings the whole check to under a minute. `--serial` turns that off.

Gaps: none. Every file the scorer needs is in the archive. The model calls that produced the answers (leakage checks, bettor, raters) are not rerun; this checks the scoring, not the answers.

Not checked, because no archived code computes it: in ss-b1, the up-word rule row of the leakage-check table, the confidence gap in plain English, the audit's leave-one-field-out bound and the engine-calibration Brier; in ss-b5, the leakage counts (146 of 243) and the greedy count of 9; in ss-b6, the design review's and the auditor's simulated false-pass rates; in ss-b7, the near-50 count, the 82% and 17-item split, and the auditor's subset margin.

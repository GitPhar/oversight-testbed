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

Round 1 (`results/ss-b1-results.md`, unaudited): on 116 findings published after the bettor's cutoff, Brier 0.163 [0.139, 0.190], 76% right. That beats a coin and a publication-bias shortcut. Older papers it may have read score better (0.105). Model psychology was its weakest field. All three bets passed, unreplicated.

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

## Reproduce

```
/Users/seanpharris/entangled-mind/.venv/bin/python scoring/score.py
```
Regenerates every results table from `items/items.jsonl` and `bettor/bets.jsonl` with no keys and no calls.

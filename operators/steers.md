# Scoring a steer: standing instructions

A **steer** is one decision by the human: a seed question, a rule, an added question, a veto, a budget call, an architecture change, a batch of odds. Every steer is a row in `ledger/steers.jsonl` (ARCHITECTURE.md, the `Steer` object; CONTEXT.md §3 rule 11). This file says how a steer is **valued**: what it changed, what the engine would have done without it, what that was worth, and a label. The valuations live in `ledger/steer-values.jsonl`, one line per steer, keyed by the steer's id, and are summed in `ledger/steers.md` as **helped X of Y**.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). The scorer never asks Sean what he meant or what he would have done. It reads the steer row, the files it cites, and the ledger.

## Why this file exists

The panel review (`paper/review-anthropic.md`, Part 1, first finding) read the record and found the human's judgment invisible: twenty steers logged, nearly all valued "pending", and a human odds column with a handful of bets in it. Sean's answer, in his words: the ledger is failing to account for the direction he has guided everything in; the design and the architecture are his as much as the engine's. The odds column measures one narrow thing, whether his number on a bet beats the engine's. Most of what he did was not a number on a bet. It was a rule, a question, a stop, a frame. Those acts changed what the engine ran and what it was allowed to say. This file scores them.

## What a valuation contains

One line in `ledger/steer-values.jsonl` per steer. Four parts, then a label.

1. **What it changed in the record.** The rules, operators, programs and bets that exist because of the steer, each named with the file or commit that shows it. Only what the record shows. A steer that changed a file names the file; a steer that opened a program names the program's first commit; a steer that stopped a bet names the bet.
2. **A counterfactual sentence.** One sentence: what the engine's default would have done without the steer, with the file that shows the default. The default is read from the record, not imagined: the operator file that was in force, the map as it stood, the line in CONTEXT.md the steer replaced, the session's own stated next step. If no file shows a default, the sentence says so and the counterfactual is marked `no recorded default`.
3. **A measurable effect, where one exists.** A number with its source, or `null`. The kinds that count:
   - overclaims caught after a rule the steer set (audit cuts, deviation rows, reversals);
   - bets withdrawn or parked before spend, with the dollars or chip seconds not spent;
   - odds improved: a Brier difference on named bets;
   - dollars or chip seconds saved or spent;
   - hits that trace to a seed question (scored bets with outcome 1 whose direction descends from the seed);
   - a published number that exists because of the steer (a ledger column, a check that now runs).
   A steer with no measurable effect is not marked down for it. Most rules have none; they are scored on the counterfactual.
4. **The label and its reason.** One of three, and one line:
   - **helped**: on the record, the project is better with the steer than the counterfactual on at least one effect, and worse on none that outweighs it;
   - **hurt**: the project is worse with it than the counterfactual on at least one effect, and better on none that outweighs it, or it cost money or chip seconds that bought nothing the record uses;
   - **neutral**: no measurable difference either way yet, or the gains and costs balance, or too little has happened since the steer to tell.
   There is no `pending`. Every steer carries a label at every scoring. A label given early is marked early (below) and re-scored.

Every line also carries:

- `evidence_strength`: `measured` (a number in the ledger decides it), `traced` (a chain of named files decides it, no single number), or `early` (the steer is recent and most of its effect is still to come; the label is the scorer's reading of what has happened so far).
- `scored_by`: the model and date of the scoring session, and `scorer_wrote_steer: false`, which the scorer asserts.
- `history`: every earlier valuation of the same steer, kept in full when it is re-scored. Nothing is deleted.

### The rule for odds steers

A `human_odds` steer (a batch of odds saved from the cockpit) is scored by the proposal's own metric for H3 (`paper/the-engine.md` §4): on the scored bets that carry those odds, Brier(engine) against Brier(engine + human), where the combined forecast is the unweighted mean. **helped** if the combined forecast beats the engine's; **hurt** if it is worse; **neutral** while fewer than 8 such bets are scored, with the running numbers shown. The threshold is H3's own minimum for a steer count. The human's own Brier is shown beside it and is never the label on its own: a batch of odds that fills an empty column has changed the record even when the numbers in it are bad.

### What a label is not

A label is not an audit of the bet the steer concerned, not a judgment of Sean, and not a controlled comparison. The counterfactual is read from files, never run. The one steer type that *is* run is the veto of a research direction, which gets a shadow check under `operators/veto.md`; its `veto_value` from `ledger/shadows.jsonl` is copied into the valuation when it exists and outranks the scorer's reading.

## Who scores, and when

- **A fresh session that did not write the steer.** It has not argued for or against the steer, did not log it, and has not written the program or bet it concerns. It states its model and the date. If no such session is available, the steer waits; a self-valuation is never recorded as the valuation (the founding-week rows in `steers.jsonl` carry `value_judgment` fields written by the ledger session that logged them; those are the record of the time, not valuations under this method).
- **Monthly.** In the first week of each month, a fresh session re-scores every row: reads the steer, the previous valuation, and everything the ledger has added since, and writes a new line with the old one in `history`. A steer whose label changes gets one sentence saying what changed it. The scoring session also scores every steer logged since the last pass.
- **Also whenever `ledger/steers.jsonl` gains a row**, the next scoring pass scores it. Until then, `ledger/steers.md` lists it as **not yet scored**, which is the only state other than the three labels, and it counts in Y, not in X.

## What the scorer reads

In this order: `ledger/steers.jsonl` (the steer row and its `evidence`), every file the row cites, `ledger/bets.jsonl`, `ledger/brier.md`, `ledger/prior.md`, `ledger/scores.md`, `ledger/lessons.jsonl`, `ledger/spend.jsonl`, `ledger/shadows.jsonl`, the audits summaries, `paper/novelty.md`, CONTEXT.md §3 and §8, ARCHITECTURE.md, and the git log around the steer's time. The scorer writes nothing to `steers.jsonl`, `bets.jsonl` or `lessons.jsonl`.

## Outputs

- `ledger/steer-values.jsonl`: the valuations (append a line per steer per scoring; the latest line for a steer id is current).
- `ledger/steers.md`: generated by `python3 ledger/steer_values.py` from the jsonl. The count (**helped X of Y**, with neutral, hurt and not-yet-scored beside it) and one row per steer: date, what Sean said in short, the label, the one-line reason, the evidence strength. `reproduce.py` regenerates it and compares byte for byte.
- The site's human-hand page (`site/human.html`) and `paper/the-engine.md` §6.11 read the jsonl and show the count and the table, with the sentence that the scorer is a Claude session and that this file is published so a reader can disagree.

## How to disagree

The scorer is a Claude session, the same model family that runs the engine and that Sean steers. A reader who thinks a label is wrong has everything the scorer had: the steer row, the files it names, this method. The disagreement goes in as a new line in `steer-values.jsonl` with `scored_by` naming the reader, the old line moved to `history`, and the reason. The monthly pass must answer it in its own reason line.

## Fields of a line

```json
{"steer_id": "st-02", "scored_at": "2026-11-05", "scored_by": "<model>, <session>", "scorer_wrote_steer": false,
 "steer_in_short": "<what Sean decided, in a few words>",
 "changed": ["<thing> (<file or commit>)", "..."],
 "counterfactual": "<one sentence: what the engine's default would have done>",
 "counterfactual_file": "<the file that shows the default>",
 "effect": "<the number and its source>" | null, "effect_kinds": ["overclaims_caught", "spend_avoided", "odds", "spend", "hits_from_seed", "published_number"],
 "value": "helped" | "neutral" | "hurt", "reason": "<one line>",
 "evidence_strength": "measured" | "traced" | "early",
 "provisional_id": false, "handoff_ref": null,
 "history": []}
```

`provisional_id: true` with a `handoff_ref` marks a valuation written for a steer that another session was logging at the same time, keyed by the id the scorer expected; the next scoring pass re-keys it to the id the ledger gave the steer, if they differ, and says so.

## Limits, stated once

Same model family throughout: Sean's steers were given to Claude sessions, carried out by Claude sessions, logged by Claude sessions and are valued here by a Claude session. The counterfactuals are readings of files, not runs. "Helped" means the record is better with the steer than the default the record shows; it does not mean the steer was the only way to get there. The sum **helped X of Y** is a count of readings, published so the readings can be checked, not a measurement of the human's skill. The measurement, where the ledger has one, is the H3 column in `ledger/brier.md`.

# Remap — standing instructions

The remap runs after a program's results settle. A fresh session reads every settled result in the program and turns each one into map entries: for every bet that **landed or came back mixed**, the next two cheapest follow-up directions, each with engine odds stated before any data, a cost, and a one-sentence cockpit question; for every bet that was **killed**, one sentence saying what it rules out. It is step 6a of the loop (CONTEXT.md §6; ARCHITECTURE.md, step 7a).

**The rule: no map may end at a landed bet with no follow-up.** A landed or mixed node whose children are all settled, or who has none, is a broken map. `python3 ledger/check_remap.py` finds every such node; the morning operator runs it every day (TASKS.md, standing rules).

> **Why this exists.** On 2026-11-04 programs 2, 3 and 4 each ran one round and stopped. Results landed, the auditors wrote down what would break each one next, and nothing in the system turned those notes into new directions. Re-weighting (ARCHITECTURE step 7) said "heat the neighbourhood" but named nobody to do it.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision. Its follow-ups reach him only as cockpit questions; his odds come only from `ledger/human-odds.jsonl`. A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit.

## In plain English

When a test works, or half works, the obvious next questions are: does it hold on the other models, and what is the cheapest test that could still knock it down? When a test fails, the useful thing to keep is what it has now ruled out, said in one sentence so nobody runs it again by accident. The remap writes both down for every finished result, puts the price and the engine's odds next to each new direction, and puts a plain question on the cockpit for Sean: would you spend about this much on it, and will it come back a hit?

## When it runs

- **Trigger.** A program's results have *settled* when every bet pre-registered in its last round has a verdict and a finished audit (`audit_status` done, or `verdict_after_audit` set). The session that writes the last audit's ledger row launches the remap in its report; the morning operator launches it if `check_remap.py` finds a landed leaf.
- **Also:** at any time on request, and before a program's next wave is built.
- **Who.** A fresh session that wrote none of the program's results, pre-registrations or audits. It reads; it never runs, pre-registers or approves a budget.

## Launch

```
cd /Users/seanpharris/oversight-testbed && claude --model opus "Read operators/remap.md and follow it. Program(s): <name(s)>."
```

## Inputs (read in full)

1. `CONTEXT.md`, `TASKS.md`, `ARCHITECTURE.md`, this file, `operators/scout.md` (the odds format and the cockpit question format).
2. Every row of `ledger/bets.jsonl` for the program, and each one's audit in `ledger/audits/`. **The audit's "What would break it next" section is the first source of follow-ups**: it names the cheapest test that could overturn the result, already costed.
3. Each bet's results file (plain-English part first) and the program's map: `map/<program>.json` (the cockpit reads only these), the program's own map markdown and JSON where they exist (`programs/<name>/map/`).
4. `ledger/lessons.jsonl` (patterns P1 onward) and `ledger/brier.md` (the running base rate, which anchors the odds).
5. `ledger/steers.jsonl`: a vetoed direction is never re-proposed by the remap; a killed one is never re-proposed unless a result gives a reason its diagnosis does not cover (scout.md, Inputs).
6. Uncommitted files of other sessions are not read beyond their first lines and are never committed (CONTEXT.md §2). If one is plainly a follow-up in preparation, map it under its own id and say whose it is.
7. Not read: `ledger/human-odds.jsonl` and the human-odds forms' answers. The engine's odds are stated without the human's (scout.md, v1 template).

## Step 1 — Classify every settled bet, by the ledger, never by preference

| ledger verdict (after audit) | class | what the remap writes |
|---|---|---|
| `pass`, `pass-unreplicated`, `hit` | **landed** | two follow-ups |
| `mixed`; `undetermined` (the test could not tell) | **mixed** | two follow-ups |
| `null`, `fail`, `killed`, `classical`, `tie` | **killed** | one sentence: what it rules out |
| `untestable`, `withdrawn` | neither | one sentence: what it rules out (often "nothing about X; it shows Y"), and whether a re-bet exists |

The class comes from the ledger's verdict, not from the remap's reading of the result. A killed bet that turned up an unexpected or reversed effect stays killed. The remap may add one **lead** for it (`kind: "lead"`, labelled post hoc) when its audit names a cheap test of that effect. A lead is optional, and it never counts as a required follow-up. This keeps the engine from grading its own failures into successes (CONTEXT.md §1, the first failure mode).

## Step 2 — Two follow-ups for each landed or mixed bet

"Next" means **not yet run**. Open, running or parked children already on the map count toward the two; landed or killed children do not (they have run, and get their own remap entries). Write only what is missing. A follow-up may serve several parents (`also_follows`); it then counts for each.

Pick the two **cheapest** candidates that could change what we believe, from these sources, in this order:
1. **The audit's cheapest overturning test** ("What would break it next"), unless it has already run.
2. **The replication the result still owes** (invariant 7: a hit is not a hit until it holds on more than one model and design). By CONTEXT.md §3 rule 12 a direction runs on `claude-haiku-5-5`, `claude-sonnet-5-5` and `claude-opus-5-5` unless its pre-registration says why not, so the replication is usually the same test on the models it has not yet seen.
3. **The neighbourhood** (ARCHITECTURE step 7: heat): the result's own "leads, not findings" section, its rival explanation, or a $0 archive question it makes newly answerable.

Cheapest means archives before API, API before hardware (CONTEXT.md §1, cost rule), and among API tests the lowest three-model cost. Opus 5.5 cannot turn thinking off, so its calls cost about 100 times Haiku's: cost a three-model test with fewer repeats or items on Opus, as om-p2-6r did, and say so. Never propose a follow-up that needs a refused topic, a key the engine does not hold, or more than the QPU hard stop allows.

Each follow-up is a `Direction` (scout.md, Step 4) with these fields:

| field | what goes in it |
|---|---|
| `id` | `<parent>-f<n>` (program 1) or the program's next free id (`P2-14`, `P3-17`, `ss-f1`); never reused |
| `parent`, `also_follows`, `from_bet` | the direction it grows from, any other parents, and the ledger bet that landed |
| `kind` | `follow-up` (or `lead`, Step 1) · `remap: "<date>"` |
| `title`, `short` | one plain-English line; a short label of at most 40 characters |
| `assumption_at_stake` | the belief this test could break |
| `cheapest_test` | the design, in two lines |
| `models` | the three ids, or `"none: <reason>"` (a chip test, an archive with no model in it, an open-weight model on the laptop) |
| `cost` | dollars of API on the named models, QPU s, or laptop hours |
| `odds_event` | the draft pass rule, scoreable yes or no; the pre-registration locks it or logs a deviation |
| `engine_odds`, `engine_odds_at`, `odds_template`, `odds_rationale` | see below |
| `question`, `known` (two lines), `human_prompt`, `engine_only` | the cockpit card (Step 4) |
| `source` | `literature` (an audit or read named it), `engine`, or `human` (a steer) |

**Engine odds, the scout's format.** P(pass) for the draft pass rule, one scale (0 = certainly will not pass, 100 = certainly will), an integer 1–99, stored 0–1. All follow-ups of one remap are given odds **in one pass, in id order, before they are ranked**, each with a rationale of at most 100 words that names the running base rate from `ledger/brier.md` and any pattern it corrects. They are never revised after ranking; a later revision needs a dated reason, and both numbers stay. If the odds were not elicited in fresh v1 contexts (scout.md), say so in `odds_template` (`"remap one pass, not v1; re-elicit under v1 before pre-registration"`); the betting session re-elicits at pre-registration (operators/learn.md).

## Step 3 — One sentence for each killed bet

`rules_out`: what the result now excludes, scoped to what was tested (the model, the items, the design), in at most 40 words, starting "Rules out". Never "every" or "all" for one set (CONTEXT.md §3 rule 6). It goes on the bet's map node (`rules_out`) and into the program's map markdown, in a table, next to the diagnosis. A killed direction stays on the map, marked closed (invariant 4).

A **question** (a line of bets chasing one puzzle) closes when its last bet is killed and its diagnosis says nothing we control remains to test. The remap marks a question that is down to its last bet `closes_after: <bet id>` with the diagnosis it will close with if that bet misses, and what follows if it passes.

## Step 4 — The cockpit question

Each follow-up's `human_prompt` is one plain-English question at about a bachelor's reading level, in the form of `map/human-odds-template.md`:

> Would you spend about <cost> to find out <what, in words a stranger understands>? Will it come back a hit (here, a hit means <the pass rule, in plain words>)?

No symbols, thresholds or terms of art; the cost in the unit that is scarce for that program. Copy it verbatim into the direction's node in `map/<program>.json`, which the cockpit reads (`site/assets/data.js`), and list it, shuffled and without engine odds, in that remap's odds form (`map/remap-<date>-odds-form.md`). The cockpit hides the engine's odds on an open card until Sean has given his own; never print them in the report.

## Step 5 — Write and check

1. Each program's map markdown gets a section **"Follow-ups (remap <date>)"**: plain English first (what landed, what each follow-up would show, what each kill rules out), then one table of follow-ups with odds and cost, then the rules-out table. A program whose map lives elsewhere (program 1: `paper/gold-map.md`) gets `map/<program>.md`.
2. Add the nodes to `map/<program>.json`, and to the program's own JSON if it has one (`programs/nature-graded/map/program-3-map.json`, `programs/settled-science/map/settled-science.json`). A program with no `map/<program>.json` gets one, so its cards reach the cockpit.
3. Run `python3 ledger/check_remap.py`. It must print `OK: no map ends at a landed bet`. A line it reports is fixed by a follow-up, or by `closed_line` (below), before the commit.
4. Commit each program's map changes in their own commit, with `git commit -m "…" -- <paths>` (CONTEXT.md §2), then the odds form.

`closed_line` is allowed only when a standing rule forbids every follow-up (for example rule 6: the quantum error-prediction encoding is never revived) or the program is closed. It is a dated sentence naming the rule. "Nothing cheap enough" is not a reason; a parked follow-up with its cost is.

## Step 6 — Report

Plain English: for each program, what landed and the two cheapest follow-ups with their costs, what the kills rule out, and the line "The new directions are on the cockpit". It is a pointer, not a request. Do not state the engine's odds in the report. End with the commit hashes, the three-line TL;DR and "YOU, NOW".

## What the remap never does

- Pre-register, run, approve a budget, or call a model API, a chip or a local model. Remapping ends at the map.
- Re-classify a bet against its ledger verdict, or lower a pre-registered bar.
- Re-open a killed or vetoed direction without the reason scout.md requires.
- Show the engine's odds to the human before his are recorded.
- Leave a landed or mixed bet as a leaf.

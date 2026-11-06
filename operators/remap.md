# Remap — standing instructions

The remap runs after a program's results settle. A fresh session reads every settled result in the program and turns each one into map entries: for every bet that **landed or came back mixed**, a fresh read of the adjacent literature around that result (Step 1b), then the next two cheapest follow-up directions, each with engine odds stated before any data, a cost, and a one-sentence cockpit question; for every bet that was **killed**, one sentence saying what it rules out. It is step 6a of the loop (CONTEXT.md §6; ARCHITECTURE.md, step 7a).

**The rule: no map may end at a landed bet with no follow-up.** A landed or mixed node whose children are all settled, or who has none, is a broken map. `python3 ledger/check_remap.py` finds every such node; the morning operator runs it every day (TASKS.md, standing rules).

> **Why this exists.** On 2026-11-04 programs 2, 3 and 4 each ran one round and stopped. Results landed, the auditors wrote down what would break each one next, and nothing in the system turned those notes into new directions. Re-weighting (ARCHITECTURE step 7) said "heat the neighbourhood" but named nobody to do it.

> **Why Step 1b exists, and why it is mandatory.** Step 1b was written at 06:01 on 2026-11-05 (`9d2e35b`), five minutes after program 5's remap (`56e20b9`, 05:56) had written sg-b3's follow-ups from the audit alone, with no paper opened. Two papers had already reported sg-b3's result (Khullar et al. 2026; Tsui 2025); the remap did not know, and the map, the README and CONTEXT.md all read the pass as a finding. `paper/informed-engine.md` traces it. Rule 13 (CONTEXT.md §3) now makes the re-scout the step that writes each landed or mixed bet's **Novelty line** when the results file lacks one, and gives every follow-up its **Prior work line**.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision. Its follow-ups reach him only as cockpit questions; his odds come only from `ledger/human-odds.jsonl`. A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit.

## In plain English

When a test works, or half works, the first job is to read again: a result makes different papers matter than the question did, and someone may already have shown it, or named the rival explanation our test left open. The remap reads around each result and writes down what that changes before it writes anything new. Then the obvious next questions are: does it hold on the other models, and what is the cheapest test that could still knock it down? When a test fails, the useful thing to keep is what it has now ruled out, said in one sentence so nobody runs it again by accident. The remap writes both down for every finished result, puts the price and the engine's odds next to each new direction, and puts a plain question on the cockpit for Sean: would you spend about this much on it, and will it come back a hit?

## When it runs

- **Trigger.** A program's results have *settled* when every bet pre-registered in its last round has a verdict and a finished audit (`audit_status` done, or `verdict_after_audit` set). The session that writes the last audit's ledger row launches the remap in its report; the morning operator launches it if `check_remap.py` finds a landed leaf.
- **Also:** at any time on request, and before a program's next wave is built.
- **Closing review:** when `ledger/prior.md` lists the program as due (section "Closing a program" below).
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
7. Not read: `ledger/human-odds.jsonl` and the human-odds forms' answers. The engine's odds are stated without the human's (scout.md, template v2).

## Step 1 — Classify every settled bet, by the ledger, never by preference

| ledger verdict (after audit) | class | what the remap writes |
|---|---|---|
| `pass`, `pass-unreplicated`, `hit` | **landed** | two follow-ups |
| `mixed`; `undetermined` (the test could not tell) | **mixed** | two follow-ups |
| `null`, `fail`, `killed`, `classical`, `tie` | **killed** | one sentence: what it rules out |
| `untestable`, `withdrawn` | neither | one sentence: what it rules out (often "nothing about X; it shows Y"), and whether a re-bet exists |

The class comes from the ledger's verdict, not from the remap's reading of the result. A killed bet that turned up an unexpected or reversed effect stays killed. The remap may add one **lead** for it (`kind: "lead"`, labelled post hoc) when its audit names a cheap test of that effect. A lead is optional, and it never counts as a required follow-up. This keeps the engine from grading its own failures into successes (CONTEXT.md §1, the first failure mode).

## Step 1b — Re-scout around each landed or mixed bet, before writing its follow-ups

A result changes which papers matter. The scout read the literature around the *question*; the follow-ups must be written against the literature around the *result*. So, for every bet Step 1 classed **landed** or **mixed**, before any of its follow-ups is drafted:

1. **Search again around the result** (operators/scout.md, Steps 1 and 2: full reads, abstract-only marked, recent preprints checked directly, never from a summary). Start from the result's own terms (what moved, on which models, under which design), its rival explanation, and the audit's "what would break it next"; search across fields, not only the one the scout began in. At least three new full reads per bet, or a sentence saying why fewer exist. Papers already in the program's reads are re-read only for the part the result now touches.
2. **Record what it changes**, in `programs/<name>/map/reads/remap-<date>-<bet-id>.md` (one file per bet, its own file: parallel readers never write to one shared file): the searches run (terms, where, date; one line each), the papers read, and for each, one line under one of these heads: **already shown** (someone has found this; the follow-up must add something or be dropped), **rival named** (an explanation our design did not exclude; the cheapest test that excludes it is a follow-up candidate), **design to borrow** (a control, measure or item set that makes a follow-up cheaper or sharper), **changes nothing** (say why). End with a "What the re-scout changes" paragraph of at most 100 words: which candidate follow-ups it adds, drops, or re-prices, and whether it moves the odds the engine is about to state.
2a. **The Novelty line (rule 13).** The re-scout file ends with the bet's Novelty line: `**Novelty:** known | partly new | new.` followed by two to four sentences (what published work states for this exact result, with citations; how ours differs or agrees; the search in one line; this session's model), under the three definitions in `operators/prereg-template.md` §10. If the results file already carries a Novelty line from a fresh session, the re-scout checks it against the papers and says "Novelty line stands" or corrects it. If it has none (every result before 2026-11-05 was written without one), the remap **adds it**: the last line of the results file's plain-English section, and `novelty`, `novelty_line`, `novelty_by` and `novelty_at` on the ledger row (`git commit -- <paths>`, CONTEXT.md §2; rebuild the jsonl from HEAD and change only that row). This is the one edit the remap makes outside the map, and it is allowed because the remap is the fresh session rule 13 asks for. A results file that calls a known result a finding, a discovery or "the first" gets the same treatment an audit cut gets: the sentence is rewritten in the same commit, and the commit message says so.
3. **Then write the follow-ups** (Step 2), citing the re-scout file in each follow-up's `source` and `known` where it bears. Each follow-up carries its own **Prior work line** (`prior_work_line`, scout.md Step 4): what the papers just read predict for the follow-up's draft pass rule, with citations, or "no prior statement found after" the search. The engine's odds (Step 2) are stated after the re-scout and say in `odds_rationale` what it changed, or "re-scout changed nothing"; an odds number far from what the Prior work line predicts says why.
4. The program's map markdown gets the re-scout's "What the re-scout changes" paragraphs, one per bet, at the top of its "Follow-ups (remap <date>)" section (Step 5), and the bet's Novelty verdict in the follow-ups table ("known", "partly new" or "new" next to the parent bet). The map node gets `novelty` and `novelty_line`, so the site shows known against new on the landed node.

The re-scout reads; it never runs, calls a model API or loads a local model. A killed bet gets no re-scout (its rules-out sentence is enough), unless the remap adds a lead for it.

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
| `engine_odds`, `odds_prior`, `odds_adjustment`, `odds_reason`, `odds_prior_commit`, `engine_odds_at`, `odds_template`, `odds_rationale` | see below |
| `question`, `known` (two lines), `human_prompt`, `engine_only` | the cockpit card (Step 4) |
| `prior_work_line`, `prior_work_predicts` | the Prior work line (rule 13; scout.md Step 4): what published work predicts for this follow-up's draft pass rule, with citations, or "no prior statement found after <search>"; and the outcome it predicts (`pass`, `fail`, `mixed`, `unknown`). Written from the re-scout file (Step 1b). Mandatory. |
| `source` | `literature` (an audit or read named it), `engine`, or `human` (a steer) |

**Engine odds, the scout's format (template v2, CONTEXT.md §3 rule 14).** P(pass) for the draft pass rule, one scale (0 = certainly will not pass, 100 = certainly will), stored 0–1. Each follow-up's odds are elicited in its own fresh context holding only `ledger/prior.md` (run `python3 ledger/prior.py` first) and the follow-up's own row (title, assumption at stake, cheapest test, models, cost, draft pass rule, its row on each prior.md table, and one sentence on what its parent found), and nothing about its history: no earlier odds on the direction, no earlier bet on it, no human odds, no other follow-up's odds. The context writes **prior** (the all-bets hit rate in prior.md), **adjustment** (signed, in hundredths) and a one-line **reason** naming the prior.md rows or design feature behind it; prior + adjustment, kept between 0.01 and 0.99, is `engine_odds`, and all of `odds_prior`, `odds_adjustment`, `odds_reason`, `odds_prior_commit` go on the node with `odds_template: "v2"`. All follow-ups of one remap are given odds **in one pass, in id order, before they are ranked**. They are never revised after ranking; a later revision needs a dated reason, and both numbers stay. If a follow-up's odds were not elicited this way, say so in `odds_template` (`"remap one pass, not v2; re-elicit under v2 before pre-registration"`); the betting session re-elicits at pre-registration (operators/learn.md). `odds_rationale` may hold the re-scout's effect on the odds ("re-scout changed nothing"); the reason line is the odds' justification.

## Step 3 — One sentence for each killed bet

`rules_out`: what the result now excludes, scoped to what was tested (the model, the items, the design), in at most 40 words, starting "Rules out". Never "every" or "all" for one set (CONTEXT.md §3 rule 6). It goes on the bet's map node (`rules_out`) and into the program's map markdown, in a table, next to the diagnosis. A killed direction stays on the map, marked closed (invariant 4).

A **question** (a line of bets chasing one puzzle) closes when its last bet is killed and its diagnosis says nothing we control remains to test. The remap marks a question that is down to its last bet `closes_after: <bet id>` with the diagnosis it will close with if that bet misses, and what follows if it passes.

## Step 4 — The cockpit question

Each follow-up's `human_prompt` is one plain-English question at about a bachelor's reading level, in the form of `map/human-odds-template.md`:

> Would you spend about <cost> to find out <what, in words a stranger understands>? Will it come back a hit (here, a hit means <the pass rule, in plain words>)?

No symbols, thresholds or terms of art; the cost in the unit that is scarce for that program. Copy it verbatim into the direction's node in `map/<program>.json`, and list it, shuffled and without engine odds, in that remap's odds form (`map/remap-<date>-odds-form.md`). Never print the engine's odds in the report.

**Cards before pre-registrations (the ordering rule, CONTEXT.md §3 rule 11).** In the same commit as the map nodes, add each program's two cheapest new follow-ups to `map/cockpit-cards.jsonl`, the file the cockpit (`site/cockpit.html`) reads, one line each in that file's format: `question` (one plain sentence at a bachelor's reading level), `spend_ask` and `spend_asked`, `hit_means`, `our_results` (one plain sentence from the program's settled results that bear on it, with the bet ids in `our_results_from`; "nothing settled yet" if none), `event`, and **no engine odds**. The cockpit holds at most 20 cards: if adding these would pass 20, drop the cards whose directions already have a bet first, then the oldest. A follow-up's card is live before any session can pre-register it, so Sean's odds can attach.

## Step 5 — Write and check

1. Each program's map markdown gets a section **"Follow-ups (remap <date>)"**: plain English first (what landed, what each follow-up would show, what each kill rules out), then one table of follow-ups with odds and cost, then the rules-out table. A program whose map lives elsewhere (program 1: `paper/gold-map.md`) gets `map/<program>.md`.
2. Add the nodes to `map/<program>.json`, and to the program's own JSON if it has one (`programs/nature-graded/map/program-3-map.json`, `programs/settled-science/map/settled-science.json`). A program with no `map/<program>.json` gets one, so its cards reach the cockpit.
3. Run `python3 ledger/check_remap.py`. It must print `OK: no map ends at a landed bet`. A line it reports is fixed by a follow-up, or by `closed_line` (below), before the commit.
4. Commit each bet's re-scout file first, then each program's map changes and its cockpit cards in their own commit, with `git commit -m "…" -- <paths>` (CONTEXT.md §2), then the odds form.

`closed_line` is allowed only when a standing rule forbids every follow-up (for example rule 6: the quantum error-prediction encoding is never revived) or the program is closed. It is a dated sentence naming the rule. "Nothing cheap enough" is not a reason; a parked follow-up with its cost is.

## Step 6 — Report

Plain English: for each program, what landed and the two cheapest follow-ups with their costs, what the kills rule out, and the line "The new directions are on the cockpit". It is a pointer, not a request. Do not state the engine's odds in the report. End with the commit hashes, the three-line TL;DR and "YOU, NOW".

## Closing a program (from 2026-11-05)

**The rule: a program whose last three layers contain no landed bet and no partly-new finding gets a closing review.** A program that keeps betting without landing anything or finding anything new is spending on a question that may already be answered. Remaps add follow-ups; nothing so far asked whether the seed question itself should stop.

- **Layers.** A bet's layer is how deep its direction sits on `map/<program>.json`: 1 for a direction the scout mapped with no parent, one more per parent step (a replication missing from the map sits under the bet it repeats). The program's last three layers are the three deepest that hold at least one settled bet (a verdict other than open or withdrawn).
- **Also due under rule 16** (CONTEXT.md §3; `ledger/rule16.py`): a program at five layers deep, or at $15 of API in the month, whose newest layer holds no landed result labelled partly new or new, and which has no steer from Sean carrying `rule16_release`. Past either line the review is the program's next action; no new layer is mapped open (a follow-up owed there is written `parked`, with the note "parked: rule 16 layer line"), and the budget code refuses the next paid call. A review that keeps the program open does not lift the line; only a landed partly-new or new result in the newest layer, or a steer from Sean, does. `ledger/prior.md`'s table prints both counts for every program.
- **Also when Sean closes it** by a steer (a `veto` of the program's seed question): the review is then the record of his decision, with his steer as the reason; it still writes the diagnosis from the record.
- **Due** when none of the settled bets in those layers is landed (ledger verdict after audit `pass`, `pass-unreplicated` or `hit`) and none has a Novelty line (rule 13, `novelty` on the bet row or its map node) of `partly new` or `new`. A program with fewer than three such layers is not due. `python3 ledger/prior.py` computes this; `ledger/prior.md`, "Closing reviews due", lists every program and why. The morning operator reports every program marked due (TASKS.md, morning checklist).
- **Who.** A fresh session that wrote none of the program's results, pre-registrations or audits, launched as `cd /Users/seanpharris/oversight-testbed && claude --model opus "Read operators/remap.md, section Closing a program, and follow it. Program: <name>."`. It reads; it never runs, pre-registers or calls a model, chip or local model.
- **Reads.** The program's seed question (verbatim, from its map), every ledger row and audit of the program, its map and rules-out sentences, its Novelty lines, its steers (`ledger/steers.jsonl`), `ledger/prior.md`, and the open directions still on its map with their costs.
- **Writes** `programs/<name>/map/closing-review-<date>.md`, plain English first:
  1. the seed question, verbatim;
  2. a table of the last three layers: layer, bets, ledger verdicts, Novelty lines;
  3. **the diagnosis**, one sentence in plain words: what the program ruled out, and what it could not rule out and why (the form program 3 used for the 3 November question, `a394a25`, steer st-19);
  4. **the decision: closed, or kept open with a stated reason.** A reason to keep it open names a not-yet-run direction on the map (or a new read) and says in one sentence how its result could change the answer to the seed question, with its cost. "More bets might work" is not a reason.
- **Marks the map**, in the same commit as the review file. `map/<program>.json` gets a top-level `closing_review`: `{"date", "by", "decision": "closed" | "kept open", "diagnosis", "reason", "file", "layers_reviewed", "bets_reviewed"}`. If closed: the top-level `status` becomes `"closed"`, and the seed question is added to `questions_closed` (`{"id": "q-seed", "question": <verbatim>, "closed_at", "diagnosis", "bets"}`), as program 3's map closed its 3 November question this morning. Its open directions become `parked` with the note "parked: program closed <date>" and stay on the map (invariant 4); a bet already pre-registered is neither run nor withdrawn by the review, but under its own rules. A closed program's budget code refuses every paid call (rule 16), and `check_remap.py` fails it if a direction is left open. The program's own map markdown gets a section "Closing review (<date>)" with the diagnosis and decision. The same goes in the program's own map JSON where it has one.
- **After.** Rerun `python3 ledger/prior.py`: the program's row reads "no" with the review's date. A kept-open review answers the flag only for the bets it saw (`bets_reviewed`); the flag returns when a settled bet it did not see lands in the last three layers without a hit or a partly-new finding. A closed program is reopened only by a new reason its diagnosis does not cover, or by Sean from the cockpit (a steer); the review's decision is the engine's (rule 11), stated in its report and commit, where he can veto it.
- **Commit** with `git commit -m "Closing review <program>: <decision>. <diagnosis>" -- <paths>`, then report in plain English: the diagnosis, the decision and, if kept open, the direction that could change the answer.

## What the remap never does

- Pre-register, run, approve a budget, or call a model API, a chip or a local model. Remapping ends at the map.
- Re-classify a bet against its ledger verdict, or lower a pre-registered bar.
- Re-open a killed or vetoed direction without the reason scout.md requires.
- Show the engine's odds to the human before his are recorded.
- Leave a landed or mixed bet as a leaf.
- Write a landed or mixed bet's follow-ups before its re-scout file is committed (Step 1b).
- Leave a landed or mixed bet without a Novelty line, or a follow-up without a Prior work line (rule 13).
- Leave a new follow-up off the cockpit (Step 4).
- Close a program that is not due, or keep a due one open without a stated reason (Closing a program).

# P2-path2. Does the engine carry its first program's traps into its second, more than into programs the first did not seed? (pre-registration; re-bet of om-p2-path)

Written and frozen in its own commit; the commit's author time (America/Denver) is the freeze time. **Before any classification.** Re-bet of om-p2-path, withdrawn before any tag on design review redesign (`ledger/design-reviews/om-p2-path.md`, `f561584`; DEVIATIONS D19a). DEVIATIONS.md D21. Budget **$0**: archive only. Proposal.md Q4; `map/other-minds.json` node P2-path (cockpit card `9099bdd`).

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as steers in `ledger/steers.jsonl`: seed questions, vetoes, added questions and architecture decisions.

## 0. The bet

| field | value |
|---|---|
| bet id | `om-p2-path2` |
| referee | `model` (a fresh classifier's tags, applied by a pre-registered rule) |
| bet type | `standard` |
| direction | P2-path |
| source | engine (ARCHITECTURE.md path_dependence_test; proposal.md Q4) |
| engine odds, P(pass) | **15**, from a fresh context under rule 14 (template v2), stated 2026-11-05 11:07 America/Denver before this commit: prior **0.31** (`ledger/prior.md`), adjustment **−0.16**, reason: "other-minds 0/9 and layer 1 1/14 outweigh engine-source 0.58; same engine, same days, 11/17 patterns program-1, so siblings likely share traps; 15-point gap needs large effect." Kept: the map's **50** (2026-11-04 18:30) and om-p2-path's **30** (withdrawn bet, D19a). |
| human odds, P(pass) | no human odds: `ledger/human_odds_match.py other-minds P2-path` finds no line, in this worktree or the main checkout, immediately before this commit. Never asked for. |
| models | none tested (rule 12): the object is the engine's record. Classifiers A and B are fresh Claude subagents handed the packet in their prompt and told to use no tools; no non-Claude model is available to this session without loading a local model, which this wave forbids, so B is also Claude (same family; stated). |
| budget | $0 |
| lesson | Correcting P3 and P8: om-p2-path's share had no baseline and its origin coding decided the result. This bet compares program 2 with three siblings program 1 did not seed, by origins a fresh session fixed, and its odds are 15% (from 50% on the map) because siblings share most traps and the gap must be 15 points. |
| prior work | As om-p2-path: no study scores whether a research agent's failure modes recur across seed questions; audit-taxonomy work on AI-scientist systems (Luo, Kasirzadeh & Shah 2025, `related-work/ai-scientist-systems.md`) finds recurring flaw classes across generated papers without splitting by starting question. Program 2 was seeded by program 1 (its instruments and items), programs 4, 5 and 6 were not. |
| design review | before classification, a fresh auditor dry-runs this design → `ledger/design-reviews/om-p2-path2.md`. No tag before a go. |
| pre-mortem | "If this fails, the most likely reason is that the program-1 patterns are generic design faults (power, baselines, bundled comparisons, wording) that programs 4–6 commit as often as program 2, so the difference stays under 15 points." Kind: `world`. Checkable: the baseline share within 0.15 of program 2's. |
| auditor | fresh session per `operators/auditor.md`, after results, in a stripped clone with a sealed plant draw |

**What the lesson rests on** (read at oversight-testbed `3a02570`, 2026-11-05 11:07 America/Denver): `ledger/bets.jsonl`, `ledger/brier.md`, `ledger/prior.md`, `ledger/audits/` (every program 2 audit; the om-p2-path design review), `ledger/lessons.jsonl` (P1–P17). How the redesign answers the review:
- **D4 (origins).** Each pattern's origin is fixed by a fresh session that never saw the units, under one dated gate: an instance in a program 1 result, write-up, design or audit committed before `a20824d` (2026-11-04 10:19:55, when program 2 opened). Its file is `data/p2-path2-origins.json`, committed with this pre-registration; the author did not edit it. Result: program 1: **P2, P3, P4, P5, P6, P7, P8, P9, P10, P12, P13** (11); not program 1: P1, P11, P14, P15, P16, P17 (6). The coder found that program 1's round-1 audits were first committed at `b009a15` (10:27:49, after the gate), so it dated each fault by pre-gate program 1 results, designs, DEVIATIONS rows and code on program 1's original history (`795dadb`), not by the audits. P9, the case that decided the withdrawn bet, is coded program 1 (pre-gate results used nouns their designs could not carry, e.g. stage1-run-1 `98d6ac6`).
- **D5 / P3 (baseline).** The same classifier tags, in one shuffled packet, the misses and required cuts of programs 4 (settled-science), 5 (self-grading) and 6 (test-awareness) on bets pre-registered after the same cutoff: programs program 1 did not seed (§2). The pass needs program 2's share at least 0.50 **and** at least 15 points above the baseline share. Tags per unit and the any-pattern share are reported per group, so a liberal tagger shows.
- **D11 (dry run).** `experiments/p2-path2-dryrun-output.txt`, on the real unit counts (22 and 74), each unit carrying a program-1 pattern with probability p: with no path dependence (equal p of 0.3, 0.5, 0.7) the rule passes 0.03, 0.10 and 0.08; with path dependence (0.60 against 0.40; 0.70 against 0.45; 0.75 against 0.40) it passes 0.65, 0.81 and 0.96.
- **D2 (units).** Cut text stops before a trailing paragraph that begins "Also", "No other", "Optional", "Not required", "Ledger, not" or "Suggested" (the three units the review named are trimmed).
- **D1 (scorer).** Untestable on a missing unit, an empty list, an unknown id, or "none" mixed with ids; fewer than 10 units in either group.
- **D8 (sentences).** "Blind to this bet's question and to each pattern's origin"; "recorded first in program 1, by the origin rule"; an untestable sentence.
- **D10 (isolation).** The classifiers get the packet text in their prompt and are told to use no tools; the units file holds no origin map; the packet shows neutral unit ids (U01–U96) in a fixed shuffled order (seed 20261105), with bet titles but no program names.
- **P8:** program 2 is coupled to program 1 by construction; the baseline is the control for that coupling only in part (programs 4–6 were run by the same engine on the same day, reading the same pattern list).
- **P10:** leave-one-bet-out re-applies the rule; a flip is reported.

## 1. In plain English

The same research engine ran a first program (program 1) and then a second (program 2), and the second borrowed the first's instruments. Every failed test and every sentence an auditor made the engine rewrite is a record of a mistake, and the engine keeps a numbered list of its recurring mistakes. The question: did program 2 keep making the mistakes first recorded in program 1, and more than programs that program 1 did not seed? A fresh session, not told this question or where any mistake was first recorded, tags every failure and rewrite from program 2 and from three other programs (4, 5 and 6) with the mistakes it shows. A hit means at least half of program 2's carry a program-1 mistake and that share is at least 15 points higher than the other programs'. That would say the traps travelled along the line the second program was seeded from. A fail means program 2's failures look like everybody else's, or carry other mistakes.

## 2. Material

- **Groups (frozen by this commit; `experiments/p2_path2.py units`):** target = program 2 (`other-minds`); baseline = programs 4, 5 and 6 (`settled-science`, `self-grading`, `test-awareness`), which were seeded by the literature-referee question and by Sean's two seed questions, not by program 1's results. Programs 3 (the chip, from program 1's 3 November hardware run) and 7 (said-vs-did, built on program 1's finding) are excluded as seeded by program 1.
- **Population:** each group's bets pre-registered after 2026-11-04 17:00 America/Denver and settled at this commit (a verdict other than open or withdrawn, an audit on record). One audit counts once (ss-b1, ss-b2, ss-b3 share one).
- **Units** (`data/p2-path2-units.json`, committed with this file): a **miss** unit for each failed bet (`failed: true`), its ledger `failure_reason`; a **cut** unit for each numbered item under the audit's "Required cuts", trimmed as above, except plant cuts named in the audit's "Revealed" note. **Program 2: 22 units from 6 bets (6 misses); baseline: 74 units from 13 bets (8 misses).**
- **Patterns:** the 17 lines of `ledger/lessons.jsonl` at this commit; the packet shows each one's id, title and `do_this` only.
- **Classifiers:** A (decides) and B (agreement only), each a fresh subagent given the full text of `data/p2-path2-classifier-packet.md` in its prompt, instructed to use no tools and to reply with JSON only; replies saved verbatim as `data/p2-path2-tags-A.json` and `-B.json` and committed before scoring.

## 3. Calls

None from code; two subagent passes.

## 4. Statistics

- **Primary:** share_target = units of program 2 whose A tags include a program-1-origin pattern ÷ program 2's units; share_baseline likewise; difference = share_target − share_baseline.
- **Secondary (never promoted):** tags per unit and any-pattern share per group; pattern counts per group; share by bet; the label with P9's origin flipped; classifier B's shares, its label, its agreement with A and Cohen's kappa on "carries a program-1 pattern".
- **Robustness committed now:** leave-one-bet-out, re-applying the rule.

## 5. Pre-registered reading

1. **Untestable:** classifier A's reply fails validation (a missing unit, an empty list, an unknown id, "none" mixed with ids), or a group has fewer than 10 units.
2. **Pass:** share_target ≥ 0.50 and difference ≥ +0.15 (each within 1e-9).
3. **Fail:** otherwise.
4. Frozen sentences (`SENT` in the code): pass / fail: "Of program 2's {n} misses and required audit cuts on bets pre-registered after 2026-11-04 17:00, {k} ({share}) carry a failure pattern recorded first in program 1 by the origin rule, against {baseline share} of {n} from programs 4, 5 and 6, as tagged by a fresh classifier blind to this bet's question and to each pattern's origin. The pre-registered event occurred / did not occur (…)." Untestable: "The test could not answer: {why}."
5. A leave-one-bet-out flip, the P9 sensitivity, or classifier B landing on the other side is reported beside the label and does not change it.

## 6. What it cannot do

- Programs 4–6 were run by the same engine, reading the same pattern list, on the same two days; they are not an independent engine. The comparison is "program 2 against siblings the first program did not seed", not "seeded against unseeded engines".
- Program 2 is coupled to program 1 by construction (P8); a pass says its failures carry program 1's recorded traps more than its siblings' do, not why.
- "Recorded first" is by the origin rule and the gate; a fault may have happened earlier without being written down.
- One classifier decides; tagging is judgment; B is the same model family.

## 7. Stop rules

No calls. A classifier reply that fails validation makes the bet untestable; it is not re-asked (the reply is committed as returned).

## 8. Ledger entry

Appended (inbox or ledger) after this commit: id `om-p2-path2`, direction P2-path, engine odds as §0 (0.50 of 2026-11-04 and om-p2-path's 0.30 kept), no human odds, budget $0, lesson `ls-om-p2-path2`.

## 9. Checklist before classification

- [x] This file, the units, the packet, the origins file and the dry run are committed before any tag.
- [x] Lesson. - [ ] Design review go. - [x] Card (`9099bdd`); human-odds read. - [x] Fresh odds. - [x] Rule and sentences frozen. - [x] Pre-mortem. - [x] No seed needed (fixed shuffle constant for the packet order only). - [x] D21.

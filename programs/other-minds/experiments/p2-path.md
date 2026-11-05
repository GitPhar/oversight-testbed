# P2-path. Does the engine fall into the same traps when it starts from a different question? (pre-registration)

Written and frozen in its own commit; the commit's author time (America/Denver) is the freeze time. **Before any classification**: no unit has been tagged by anyone when this file is committed. DEVIATIONS.md D19. Budget **$0**: archive only (the ledger and the audits); the classifiers are fresh Claude Code subagents, not API calls from code. Proposal.md Q4 (path dependence); `map/other-minds.json` node P2-path, which "opens at program 2's 10th settled bet". Its tenth settled bet is om-p2-15 (scored at `39844bb`).

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as steers in `ledger/steers.jsonl`: seed questions, vetoes, added questions and architecture decisions.

## 0. The bet

| field | value |
|---|---|
| bet id | `om-p2-path` |
| referee | `model` (a fresh classifier's tags, applied by a pre-registered rule, decide the outcome) |
| bet type | `standard` |
| direction | P2-path (`map/other-minds.json`; cockpit card `9099bdd`) |
| source | engine: ARCHITECTURE.md `path_dependence_test`, proposal.md Q4 (close-founding session) |
| engine odds, P(pass) | **30**, from a fresh context under rule 14 (template v2), stated 2026-11-05 10:42 America/Denver before this commit: prior **0.32** (`ledger/prior.md` at `39844bb`), adjustment **−0.02**, reason: "other-minds 0/8 and layer 1 1/14 pull down, engine source 0.58 pulls up; 16 of 22 units are audit cuts, and the commonest cut class, wording, counts as not program 1." The map's odds, **50**, stated 2026-11-04 18:30 by the close-founding session (not v2), are kept: `engine_odds_first` 0.50, `engine_odds` 0.30. |
| human odds, P(pass) | no human odds: `python3 ledger/human_odds_match.py other-minds P2-path`, run immediately before this commit in this worktree and in the main checkout, finds no line (the card went up at `9099bdd`). Never asked for. |
| models | not three models (rule 12), because no model is being tested: the object is the engine's own record. The classifier is a fresh Claude Code subagent (claude-opus-5-5); a second, independent one (B) is run for agreement only. |
| budget | $0 API · 0 QPU s · about an hour of two fresh sessions |
| lesson | Correcting P8 and P3: program 2 was seeded by program 1, so this is not a test of independent seeds, and a share any tagging could reach says nothing. This bet fixes each pattern's origin before any tag and reports the any-pattern share and a second classifier, and its odds are 30% (from 50% on the map) because wording cuts count as not program 1. |
| prior work | No study scores whether a research agent's failure modes recur across seed questions; the closest are audit-taxonomy papers on AI-scientist systems (Luo, Kasirzadeh & Shah 2025, `related-work/ai-scientist-systems.md`: recurring flaw classes across generated papers), which do not split by starting question. The map's own note: program 2 was seeded *by* program 1 (its instruments and several directions came from program 1), so the two are not independent seeds, and a pass is the expected direction under that coupling. |
| design review | before classification, a fresh auditor dry-runs this design → `ledger/design-reviews/om-p2-path.md`. No unit is tagged before a go. |
| pre-mortem | "If this fails, the most likely reason is that most of program 2's audit cuts are wording faults (a sentence the design cannot carry), which the classifier tags P9, a pattern this rule does not count as first seen in program 1." Kind: `artefact`. Checkable: P9's count among the tags, and the P9-as-program-1 sensitivity row. |
| auditor | fresh session per oversight-testbed `operators/auditor.md`, after results, in a stripped clone with a sealed plant draw |

**What the lesson rests on** (read at oversight-testbed `39844bb`, 2026-11-05 10:42 America/Denver): `ledger/bets.jsonl`, `ledger/brier.md`, `ledger/prior.md`, `ledger/audits/` (every program 2 audit), `ledger/lessons.jsonl` (P1–P17). How each pattern applies:
- **P8 (more than the named factor differs).** Program 2 is not an independent seed: it borrowed program 1's instruments, items and audits' vocabulary, and its bets were written by the same engine reading the same pattern list. The claim is only about the record, never "the engine is path-independent".
- **P3 (a dumb rule would pass).** The dumb reading is "every unit carries P9 or none"; the share of units carrying *any* pattern is reported beside the program-1 share, and the pattern counts are printed.
- **P10 (one item decides).** Leave-one-bet-out re-applies the bar; a flip is reported.
- **P9 (wording).** The verdict sentence is frozen in code.
- **P12 (can go either way).** Program 1's patterns are 7 of 17; P9 alone (not program 1) is the commonest audit fault class in round 2, and P2/P3/P8/P10 are among the commonest design faults; the share can land on either side of one half.
- **P13.** The bar is compared with a 1e-9 tolerance.
- Others (P1, P4–P7, P11, P14–P17): no odds rule inside the test, no manipulation, no rivals, no control, no calls, no leave-one-out labels inside a score, no clustered items beyond the bet (leave-one-bet-out covers it), no dry-run worlds, no item-property baseline, no guard fix.

## 1. In plain English

The same research engine ran program 1 (could a quantum encoding catch a model's mistakes, then: does a model's stated confidence read out a stored belief?) and program 2 (does a model's account of another mind behave like its account of its own?). Every failed bet and every sentence an auditor made the engine cut is a record of a mistake. The engine keeps a numbered list of its recurring mistakes (patterns P1 to P17), each written from the bets where it first showed up. This bet asks: when the engine started from a different question, did it keep making the mistakes it first made in program 1? A fresh session, which does not know this question and is not told where any pattern came from, tags each of program 2's misses and audit cuts with the patterns it carries. If at least half carry a pattern first seen in program 1, that is a hit: the traps travelled with the engine. If fewer, program 2's failures were mostly its own (or new). Because program 2 was built from program 1's materials, a hit is the less surprising answer.

## 2. Material

- **Population (frozen by this commit):** program 2 (`other-minds`) bets pre-registered after 2026-11-04 17:00 America/Denver (when the patterns and the lesson rule began) and settled by this commit (a verdict other than open or withdrawn, and an audit on record): om-p2-3b, om-p2-5, om-p2-6, om-p2-6r, om-p2-7 and om-p2-15 (all fail, outcome 0). Excluded by the cutoff: om-p2-1, om-p2-2, om-p2-3, om-p2-4 (pre-registered 2026-11-04 between 10:19 and 15:08). Bets pre-registered later (om-p2-5r, P2-14) are not in it, whatever their outcome.
- **Units** (`experiments/p2_path.py units`, writing `data/p2-path-units.json`, committed with this file, before any tag):
  - one **miss** unit per bet that failed (outcome 0): the audit's `failure_reason` as copied into the ledger row;
  - one **cut** unit per numbered item under the audit's "Required cuts" (`ledger/audits/<bet>.md`), with its full text, **except** cuts the audit's "Revealed" note names as the plant (never applied to the record).
  - Not units: optional or suggested edits, ledger-only corrections, design-review findings, round-3 audits (`ledger/audits/round-3/`).
  - **22 units from 6 bets**: om-p2-3b 2 (its cut 1 was plant pl-002), om-p2-5 4, om-p2-6 2, om-p2-6r 4, om-p2-7 4 (its cut 1 was plant pl-022), om-p2-15 6. Listed in `data/p2-path-units.json`; the classifier packet is `data/p2-path-classifier-packet.md`.
- **Patterns:** the 17 pattern lines in `ledger/lessons.jsonl` at this commit. The classifier sees each one's id, title and `do_this` only; never its `evidence`, `sources`, `first_seen` or `cited_by` (which name programs).
- **Which patterns were first seen in program 1** (fixed here, by the author, from each pattern's `evidence` and `sources`, before any tag; `ORIGIN_P1` in the code; never shown to the classifier). Rule: a pattern is program-1-origin if (a) its evidence cites a program 1 instance from audit round 1 (the founding-week entangled-mind audits, before program 2 opened at 2026-11-04 10:19), or (b) every instance it cites is a program 1 bet. Result:
  - **program 1:** P2 (round 1, v2-run-1), P3 (round 1, the one-bit predictor), P8 (round 1, own vs other differed in more than the label), P10 (round 1, two of ten items drove direction 2), P11 (em-qwalk only), P12 (em-qwalk2 only), P17 (em-gm2bf1 only);
  - **not program 1:** P1 (program 2's first four bets), P4, P5, P6 (program 3), P7 (program 2), P9 (audit round 2, which found it in programs 1, 2 and 3 at once; round 1's wording fault was a different one), P13 (programs 2 and 3), P14 (program 5), P15 (program 6), P16 (program 7).
- **Classifier A** (primary) and **classifier B** (agreement only): each a fresh subagent that has not seen program 2's results files, this pre-registration, the map node, the cockpit card or this bet's question. Each is handed exactly `data/p2-path-classifier-packet.md` (the rule, the 17 patterns as above, the units) and nothing else, and returns JSON tags, committed as `data/p2-path-tags-A.json` and `-B.json` before scoring. The packet's rule: "A unit carries a pattern when the fault the unit describes is an instance of that pattern's title, read with its 'what to do' line: the same kind of mistake, not merely the same topic. Tag every pattern the unit carries; tag `none` if it carries none."

## 3. Calls

None from code. Two subagent sessions (A, B), each one pass over the packet.

## 4. Statistics

- **Primary:** share = (units whose classifier-A tags include at least one program-1-origin pattern) / (all units).
- **Uncertainty:** none computed for the primary; the unit count is small and the bar is a fixed share of this record, not an estimate of a population. Reported: leave-one-bet-out shares.
- **Secondary (never promoted):** the share by kind (miss, cut) and by bet; the share with P9 counted as program-1-origin; the share of units carrying any pattern; pattern counts; classifier B's share, its agreement with A and Cohen's kappa on the binary "carries a program-1 pattern".
- **Engine-only secondaries on the map node** (reported, not scored): whether programs 1 and 2's Brier scores differ by more than their bootstrap interval; whether a kill diagnosis recurs in kind across the two maps. Not computed in this bet.

## 5. Pre-registered reading

1. **Untestable:** fewer than 10 units, or classifier A leaves any unit untagged.
2. **Pass:** share ≥ 0.50 (within 1e-9).
3. **Fail:** otherwise.
4. Frozen sentence (`score_cmd`): "Of program 2's {n} misses and required audit cuts on bets pre-registered after 2026-11-04 17:00, {k} ({share}) carry a failure pattern first seen in program 1, as tagged by a fresh classifier blind to the bet and to each pattern's origin; the bar was half. The pre-registered event occurred / did not occur."
5. A leave-one-bet-out flip, or classifier B landing on the other side, is reported beside the label; neither changes it.

## 6. What it cannot do

- Program 2 is not an independent seed (P8 above); the comparison proposal Q4 wants, two seeds run in parallel from scratch, is not this.
- The pattern list was written from programs 1–3 on 4 November and grew since; a program 2 fault that fits no pattern counts against a pass, and a pattern written *from* program 2's own bets (P1, P7, P13) counts against it too.
- The origin rule is the author's, applied to text; "first seen" is first *recorded*. P9's origin is the closest call; the sensitivity row counts it as program 1.
- One classifier decides; tagging is judgment. B's agreement says how much.

## 7. Stop rules

- No calls. The classifiers' outputs are committed as returned; a malformed reply is re-requested once from a new fresh session (not reworded), and that is recorded.

## 8. Ledger entry

Appended in the commit after this one: id `om-p2-path`, direction P2-path, engine odds as §0 (both kept), human odds as §0, budget $0, lesson `ls-om-p2-path`.

## 9. Checklist before classification

- [x] This file and the unit file are committed before any tag.
- [x] Lesson after reading the ledger.
- [ ] Design review go before any tag.
- [x] Cockpit card before this file (`9099bdd`); human-odds.jsonl read immediately before this commit.
- [x] Engine odds re-elicited under rule 14; the 2026-11-04 odds kept.
- [x] Rule applicable by a stranger; sentence frozen.
- [x] Seed: none needed (nothing is drawn or split).
- [x] DEVIATIONS.md D19.

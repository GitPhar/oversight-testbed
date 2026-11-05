# CONTEXT.md — the persistent brain

Every operator session (morning brief, nightly updater, auditor, scout, any build session) reads this file first, then `TASKS.md` (open items, decisions made, what waits on whom), then ARCHITECTURE.md and proposal.md. The nightly updater rewrites sections 4, 5 and 8 from the day's commits. If this file and a chat disagree, this file wins; if this file and a results file disagree, the results file wins and this file is corrected and the correction logged.

Last rewritten: 2026-11-04 09:15 America/Denver, by hand, from the full founding session (Nov 3–4).

## 0. Name

The project's title is not yet chosen. It will be taken from proposal.md once that reads right to Sean, the way "The Entangled Mind" came from its own proposal. Convention: an evocative multi-word name that names a picture (Sean's picture: every research path held open at once, then a bet collapses them to the one worth walking). Rejected as generic or synonym-shaped: Prospector, Taste, Assay, Tiller, Sextant, The Map and the Hand, Odds Before Data, The Observer Effect, Every Path at Once, The Thousand Doors; "The Graveyard of Hypotheses" was the only one close in spirit. The repository slug `oversight-testbed` is a placeholder and is renamed the day the title is chosen; sessions must not propose names unless asked.

## 1. What this is

A scalable-oversight testbed for AI-driven research, built for trust rather than volume. The AI scouts adjacent research across all fields, maps candidate directions with stated odds and costs, pre-registers the cheapest falsifying test, runs it under budget and stop rules, submits every result to an independent adversarial audit, records the verdict, and re-weights the map: an audited surprising result heats its neighbourhood and queues replication; a dead direction closes with a diagnosis and stays on the map. A human operator (Sean) may state his own odds on any bet before data, separately from the engine's, through the cockpit only (a bet without them proceeds marked "no human odds"), and steers: adds questions, vetoes, sets budgets, overrides audits. Every steer is logged and later scored. The engine's calibration, the auditor's catch rate, and the human's added value are all published numbers. The engine is itself the research object (see proposal.md: Q1 calibration, Q2 audit, Q3 human oversight, Q4 path dependence across two seed questions, Q5 literature-sourced bets vs AI-generated bets).

Why safety, in Anthropic's terms: as models do more of the execution, the bottleneck and the risk move to direction. Three failure modes made measurable here: an AI grading its own research drifts toward what looks good to itself (seen twice in the founding week, caught by re-checks); write-ups overclaim (three corrected in the same week); the human hand slips off the loop. A system that showed a surprising positive daily would be producing false positives; the auditor's first job is to say so.

Sean's signature, as the method's import rule: every program begins by reading adjacent research in full across all fields — science of mind first by inclination, but machine learning, computer science, physics, neuroscience, metascience — extracting the "what to do next" each paper suggests, filtering by cost and falsifiability, and killing what does not transfer, fast. Not one wild idea; a disciplined way of borrowing from every science that has studied a mind, and from every field that has studied how research goes right or wrong.

Cost rule: cheapest falsifier first; archives before API, API before hardware. $50 of the $200/month API credit was used in the founding week; the plan to Nov 22 is about $60 more. Quantum hardware (IBM Open Plan, 600 QPU s/month, 46 s used) stays available for program-level experiments (gold map directions 7 and 8); it is never a computational resource. In the testbed's own machinery, quantum hardware has two sized jobs (operators/hardware.md): the chip referees simulator-vs-chip disputes as logged `tiebreak` bets (≤ 60 QPU s each), and splits are seeded from the CURBy beacon (NIST/CU Boulder, not our chip), with the pulse recorded in each pre-registration. CURBy's Bell-certified chain has been stalled since 2025-08-22, so seeds currently come from its classical chain. Whether hardware can serve the testbed in other ways stays an open question, as Sean wants.

Interface: a public site (GitHub Pages) is a deliverable, not an afterthought — the map drawn as paths that fan out and collapse as bets land, the ledger as a calibration chart, the kill log, the record as a timeline, papers as readable pages. Sean is a visual person; complicated things must be lookable-at. The entangled-mind "window" failed that test and is retired to an appendix.

Owner: Sean Pharris (GitHub GitPhar). Background: psychology and philosophy, four years as a technical lead in AI pipeline development, no ML research background. Working style: voice dictation, plain English, one paste per terminal tab, does not read long replies. Every report ends with a TL;DR of three lines max and then "YOU, NOW" with the exact next step. All times America/Denver, never UTC.

Primary goal: a submission to the Anthropic Residency (applications close 2026-11-22; AI safety research; $350–500K/yr equivalent; no ML background required). The residency page says the key skill, as models improve, is increasingly the ability to frame a research agenda and judge what is worth doing. That is what this testbed demonstrates. Named mentors whose work our results touch: Jack Lindsey (Model Psychology; model introspection), Belinda Li (language model representations), Samuel Marks (Scalable Oversight; truth probes, Marks & Tegmark 2023). Research areas listed include model internals and interpretability, scalable oversight, model organisms, AI welfare. The framing that matters there is safety: can an overseer trust what a model reports about itself?

## 2. Repositories

**One repository, final (Sean, 2026-11-04 17:30): no separate program repositories, ever.** Programs live inside the engine repo as `programs/<name>/`, each with its full git history imported (`git subtree add`), so every commit hash in the ledger resolves here. Never ask Sean to create a repository.

- `GitPhar/oversight-testbed` (public; placeholder slug, see §0). Local: `/Users/seanpharris/oversight-testbed`. The engine: CONTEXT.md, TASKS.md, ARCHITECTURE.md, proposal.md, README.md (the five commitments), ledger/, map/, operators/, site/, paper/, application/. Then the programs:
  - `programs/entangled-mind/`: program 1. Full pipeline, all results, two papers, the record, audit round 1 (`audits/`). History imported up to `795dadb`.
    - The standalone `GitPhar/entangled-mind` repository (public, MIT) is **left untouched as program 1's historical record**; link to it, but do not push new work there.
    - Its unmerged branches (`related-work`, `biomimetics`, `multi-model`, `probes`, `audit`, `audit2`) are still in `/Users/seanpharris/entangled-mind`. Audit round 2's files are copied into `ledger/audits/`.
  - `programs/other-minds/`: program 2 (model psychology: does a model's account of another mind behave like its account of its own?). Wave 1: P2-1 fail, P2-2 fail, P2-4 undetermined, P2-3 untestable (a refusal); the P2-3 low-severity re-bet is approved (st-12).
  - `programs/nature-graded/`: program 3 (the engine's odds graded by the `ibm_fez` chip, not by a language model; the chip is a referee, never a computational resource). Wave 1: P3-1 and P3-5 fail, P3-2 and P3-3 untestable; ng-p3-15, the 3 November repeat, is pre-registered and awaiting its design review (st-11).
  - `programs/settled-science/`: program 4 (the published-record referee: the engine bets on settled items, graded by the literature). Tooling committed; item drafts and first pre-registration in progress.
- **The old folders** `/Users/seanpharris/{entangled-mind,other-minds,nature-graded,settled-science}` each carry a `NOTE.md` (git-excluded there) telling a still-running session to commit, report the hash, and continue inside `programs/`. The engine session brings late commits across with `git subtree pull --prefix=programs/<name> /Users/seanpharris/<name> main`.
- **Paths in the ledger.** `result_file`, `test` and the other paths in `ledger/bets.jsonl` are relative to the program folder (`programs/<name>/`). A bet's pre-registration commit from before the fold shows its files at their pre-fold path: `git show <prereg-commit>:experiments/<file>.md`.
- **Pushing.** Only the session in the main checkout pushes, with the token in `.env` (never printed).
- **Committing in a shared checkout.** Several sessions work in `/Users/seanpharris/oversight-testbed` at once and share one git index, so `git add` followed by `git commit` can sweep another session's staged files into your commit (it happened on 2026-11-04: ss-b1's pre-registration landed inside ebd2c80, logged as settled-science D10). Always commit with `git commit -m "…" -- <your paths>`, which commits only those paths whatever else is staged, and never `git add -A` or `git commit -a` at the repo root. A path-only commit still takes **every** uncommitted edit to that path, including another session's (it happened again at c0850f1, which committed the em-qwalk row an author had appended). Before committing a shared file (`ledger/*.jsonl`, `ledger/*.md`, `TASKS.md`, `CONTEXT.md`), run `git diff <path>`, and commit only when every hunk is yours; otherwise tell the other session, or name its edit in your message.

Key files in programs/entangled-mind: `README.md`, `DEVIATIONS.md` (D1–D47+, every departure from a pre-registration, dated), `paper/record.md` (commit-by-commit timeline), `paper/gold-map.md` (11 ranked directions with odds), `paper/biomimetic-map.md` (10 brain mechanisms vs the measured fingerprint), `paper/morning-brief.md`, `paper/no-credence-to-read.md` (main paper), `paper/the-entangled-mind-paper.md` (short negative-result paper), `paper/clonable-minds.md` (theory note), `paper/one-page.md`, `paper/figures/`, `experiments/reproduce.py` (regenerates every results table from archived JSON with no keys; last run printed ALL TABLES REPRODUCED), `results/*.md`.

## 3. Rules every session follows

1. Pre-register every test in its own commit before its first API call or before an archive is opened for analysis. The pass rule, the statistic and the budget are written first.
2. One scale direction in all graded designs (0 = certainly false, 100 = certainly true). The reversed scale was the main noise source and manufactured a false QQ near-miss.
3. Stop-on-refusal: if any Anthropic API call is refused, no new call starts; report and wait. Never reword or retry a refused call. Two refusals so far (category reasoning_extraction, both the claim extractor on SimpleQA items with Sonnet as base; request IDs in `results/refusal-sonnet-replication*.md`); support ticket pending.
4. Budgets are enforced in code. Under $10/month is the session's call and Sean does not want to hear about it; above that, give the number and a one-sentence recommendation.
5. Plain-English write-up first in every results file, then the technical table. Negative results stated as plainly as positive ones. Overstatements get corrected in the same commit series that made them.
6. Never revive the quantum error-prediction encoding; it is closed by pre-registered tests on two base models. Never lower a pre-registered bar after seeing data. Never claim a finding is "every" or "all" when it was tested on one set.
7. The quantum hardware budget: IBM Open Plan, 600 QPU s/month, project hard stop 420 s, 46 s used (Stage 1 run + entanglement witness). Hardware is submitted only for a pre-registered experiment whose design review says go. **Budget rulings under the hard stop are the engine's call (Sean, 2026-11-04 18:26, steer st-16):** a pre-registration states its QPU budget, the design review checks it, and the engine approves it with a steer row citing st-16. The engine still reports every job's seconds, and anything that would cross the 420 s hard stop is refused in code. (Updated from the original "separately approved" rule; usage now 54 s.)
8. Commit messages state what changed and which deviation row, if any, they add.
9. **Learn before you bet (mandatory from 2026-11-04 17:00).** Before any new pre-registration, read `ledger/bets.jsonl`, `ledger/brier.md`, `ledger/audits/` and `ledger/lessons.jsonl`, and write one lesson line: which past pattern (P1–P10 so far) this bet corrects, and how its odds reflect it. It goes in the pre-registration's §0, committed with it, and in `ledger/lessons.jsonl` (`operators/learn.md`).
10. **Design review before the first call (mandatory from 2026-11-04 17:00).** A fresh auditor session dry-runs every pre-registration (checks D1–D10, no paid calls, a pilot of at most $0.10 only for a named execution risk) and must say **go** before any call (`operators/design-review.md`). Two of 4 November's misses were set-up errors a dry run would have caught (ng-p3-1: calibration never loaded, ZZ never applied; ng-p3-5: unmatched rivals). `ledger/check_prereg.py` checks both rules; violations are published in `ledger/scores.md`.
11. **Never ask the human in a terminal (Sean, 2026-11-04).** No session asks Sean for odds or for a decision in a terminal, a chat or a question dialog. Human odds come only from `ledger/human-odds.jsonl`: the lines the cockpit (`site/cockpit.html`) saves as `~/Downloads/human-odds.jsonl`, committed. **Every local session starts by running `python3 ledger/pickup_human_odds.py`** and commits what it appends (new answer lines, and a `veto` steer for each "No, I would not spend that"); the cockpit tells Sean the next session picks the file up, so no session may skip it. If a direction has no line there when its bet is pre-registered, the bet proceeds, marked `human_odds: null` with `human_odds_note: "no human odds"`; it is never held for an answer and never filled in later. A decision a session would otherwise ask about, it makes under these rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as **steers** in `ledger/steers.jsonl`: seed questions (`choose_seed`), vetoes (`veto`), added questions (`add_question`) and architecture decisions (`architecture`), each given an outcome and a value judgment once known.

## 4. What has been established (as of 2026-11-04 09:15)

### Case study 1, phase A: The Entangled Mind (closed, negative)
Hypothesis (proposal dated 2026-10-25): encode an LLM's competing claims, extracted from its own visible reasoning, as qubits with entangling gates between contradicting claims; the entangled readout flags the model's wrong answers better than classical controls.
- Pipeline built 2026-11-03: base model claude-haiku-5-5 (Sonnet as second base), extractor claude-sonnet-5-5, relation judge claude-haiku-5-5; arms A (entangled, noisy sim), C (no entangling gates), D (shuffled relation web), E (contradiction count), F/F2 (classical Ising twin, learned), G (stated confidence), L (logistic on features), H (hedge count), A2/A2.1 (learned quantum encodings).
- Result: on the locked test set, A2 0.83 vs F2 0.84 AUROC (tie); the learned quantum encoding set its couplings near zero, i.e. switched entanglement off. Stage-by-stage readout shows the error signal is present at encoding (0.63) and erased by the entangling/evolution step (0.49) while the unentangled circuit sharpens it (0.68). On Sonnet's errors A2 0.90 vs F2 0.82, but a pre-registered ablation showed the edge is the per-claim readout angle, which a classical twin (F2+) matches exactly, and setting couplings to zero changes nothing. Experiment 5's held-out edge is matched by a dephased classical Markov chain. Stated confidence G ties the best structural model on both bases (0.82–0.83 Haiku, 0.91 Sonnet).
- Hardware: Stage 1 circuit ran on ibm_fez (9 qubits, 117 CZ); entanglement witness certified two-qubit entanglement on 3 of 3 items (negativity 0.147, 0.063, 0.067, CIs above 0). Calibration logged.
- Sequential tests: experiment 3 (yes/no order effects) inconclusive, the model repeats its answer; experiment 4 (Yearsley–Trueblood) found conjunction fallacies in graded form on 7/16 items, order effects ~+0.10, mechanism undetermined (D19 estimator circular; run 3 untestable because the model rejects another person's provided rating); experiment 5 (chains, QQ, Kvam) a tie, no quantum signature, QQ near-miss was an anchor-pooling artefact.
- Verdict: the quantum encoding adds nothing on error prediction or sequential rating prediction. Open quantum threads with honest odds: off-axis-claims version of exp 5 (P≈0.10), representation-geometry predicting order effects on an open model (P≈0.12), local-friendliness experiment on hardware (direction 7, ≈220 QPU s, a foundations result, not an LLM result).

### Case study 1, phase B: No credence to read (open, positive so far)
Trying to measure the model's beliefs showed there is no fixed belief to measure. Overnight 2026-11-04, eleven pre-registered tests, $4.17:
- Graded sequential ratings show large real order effects: median 25-point swing in the main rating, 60/80 claim–question pairs with OE > 0.10; survives one-scale replication (12/16 pairs).
- Direction 2 (transcript editing: shown / redacted / planted): with the model's own earlier answers hidden, question order still moves its verdict, ratio 1.91 [0.92, 4.90] (question-driven); planted numbers pull later ratings; repeat consistency 81% → 23% when its first answer is hidden (consistency is memory). Caveat: two of ten items drove most of it; the 40-item replication is running.
- bm1 (source dependence): the same number pulls the next rating +0.37 [+0.17, +0.57] when framed as the model's own earlier answer, ~0 when framed as another person's. Own answers are treated as commitments.
- Direction 3 (six elicitation formats, 160 claims): separate credences per format win for 86% of claims; predicting a held-out format from the other five recovers 39% [30%, 50%] of its reproducible signal ("little format-free belief"; the 0.5 line is only narrowly excluded).
- Direction 1 (privileged self-knowledge): none; self-advantage −0.055 [−0.103, −0.007]; Sonnet judges Haiku's errors better than Haiku does.
- Direction 9 (NSIT): asking changes later answers in 5 of 6 comparison families (Holm p = 0.0012); a mid-chain yes/no choice does not (no Kvam interference).
- Direction 4 (evidence seeking): mixed; the model picks relevant claims; EIG vs confirmatory undecided.
- Biomimetic: no confirmation bias toward another's number; no serial-position U-shape; assimilation toward the previous rating (+0.27); conjunction fallacy on 8/16 vignettes with the Costello–Watts identity near zero.
- Theory note (`paper/clonable-minds.md`): an LLM's state at a turn is a copyable string, so macrorealism holds by construction; any order or total-probability effect can only be invasiveness; editing the transcript separates "the question disturbs" from "the answer is remembered", impossible for people or quantum systems. No prior statement found.
- Running now: direction 2 on all 40 items (D45, $2.50 cap); own-vs-other at distances and lags (D47); multi-model replication on Sonnet and Opus of directions 1, 2, 3 ($20 cap) plus a calibration-under-format demonstration ($3); open-weight probe dissociation (gold map direction 5, local, $0).

Safety framing: oversight and calibration evaluations assume a model's stated confidence reads out a stored belief with some noise. These results say the number is constructed by the question, the format and the model's own transcript, consistency is memory, and self-access is not privileged. Whether the belief exists inside while the words move is the probe test now running.

### Engine calibration so far
Authoritative numbers: `ledger/brier.md` and `ledger/scores.md`, generated from `ledger/bets.jsonl`, `ledger/plants.jsonl` and `ledger/lessons.jsonl`. As of 2026-11-04 16:50 (corrected by hand from the ledger, which wins over this file):
- **Brier 0.236 on 9 scored bets**: the five founding-week bets, plus om-p2-1, om-p2-2, ng-p3-1 and ng-p3-5. That is about the same as a coin (0.25; nine bets cannot tell a 0.014 gap from noise) and worse than always saying the observed hit rate (0.173; 2 hits in 9). The two hits were given 25%, below several misses, so the odds do not yet rank bets.
- **Program 2's odds ran high:** 55–70% on four bets, none a clear hit. Program 3's odds of 7–42% were all misses.
- **Audit round 2** (`ledger/audits/SUMMARY-2.md`) reversed om-p2-4 from pass to undetermined. A non-detection rule with no power check is excluded from scoring; it would score 0.228 as a hit and 0.248 as a miss.
- **Untestable, not scored:** om-p2-3 (API refusal after 26 calls, request `req_011Cgih9NjqNtezArQLWd12p`) and ng-p3-2/-3 (the gap did not recur).
- **Auditor catch rate:** 1 of 1 planted claim caught (pl-001, an overclaim, "on Claude models"), 95% interval [0.21, 1.00]. It was a forced plant on an already-audited bet, with planter, auditor and scorer in one session, so it is a check that the machinery works, not a rate.
- **Pre-mortems:** 3 of 6 named the main reason. The lazy "the effect isn't there" baseline was right for 5 of 8 failures.
- Day two's account is `paper/day-two.md`.

## 5. The map (next candidates, in order, with odds and cost)

From `paper/gold-map.md` rev 2 and `paper/biomimetic-map.md` rev 2:
1. Robustness of phase B across models and designs (running).
2. Probe dissociation on an open-weight model (running; P≈0.30 of a clean dissociation).
3. Calibration-under-format demonstration (running).
4. Serial dependence at distance and lag, own vs other source (running, D47).
5. Sean's biomimicry queue, a **scout item** (`bmq`, steer st-14): memory, sleep and adaptive forgetting vs catastrophic forgetting (open-weight only; crowded field: complementary learning systems, replay-based continual learning, mortal computation); others as he lists them. Engine odds **0.30** that a full-read scout finds a cheapest falsifier under $5 on a local open model that has not already been run. Cost: one scout session, $0.
5a. Sean's **entangled-claims** direction (`qwalk`, steer st-13), with its free classical-baseline test: a simulated quantum walk against PageRank over program 1's claim graph (its map directions and their links), each predicting program 1's own kills and hits, leave-one-node-out. Quantum counts only if it beats the classical baseline (AUROC difference, bootstrap interval above 0); beating chance does not count. Engine odds **0.04** (program 1's classical twins matched all six quantum comparisons; ~25 labelled nodes). Cost: $0, laptop minutes, no chip.
5b. The **path-dependence comparison** (`P2-path` in `map/other-minds.json`; proposal Q4), a bet that **opens when program 2 reaches 10 settled bets** (2 now: om-p2-1, om-p2-2). Event: at least half of program 2's misses and audit cuts after 2026-11-04 17:00 carry a failure pattern first seen in program 1. Engine odds **0.50**. Cost: $0, an hour, archive only.
6. Hardware: direction 7 (local friendliness, two friends, external settings, ≈220 QPU s, P≈0.20 clean) or direction 8 (sequential Peres–Mermin under CbD, 72–150 QPU s, instrument check), not both in one month.
7. Representation geometry vs order-effect size (P≈0.12).
8. Off-axis-claims quantum sequential test (P≈0.10).

## 6. How the engine runs (the loop; ARCHITECTURE.md has it in pseudocode)

1. Scout: for a question or a result, gather the adjacent literature with full reads, record what each paper tested, on whom, the result, its limits, and what we can borrow. Mark abstract-only reads.
2. Map: rank candidate directions by the assumption at stake, who has looked and why it is open, what our data already say, the cheapest falsifying test, its cost, and a stated probability of a real result. Two fixed rules: every test is pre-registered; QPU is budgeted per month.
3. Pre-register: pass rule, statistic, split, seed, budget, in one commit.
4. Run: budgets in code, stop-on-refusal, one scale direction, caches so a crash never pays twice.
5. Verdict: plain English first, then tables; overstatements corrected in-series; reproduce.py regenerates every table.
6. Re-weight: a surprising result raises the weight of its neighbourhood (more scouting, follow-up tests); a dead direction is closed with a diagnosis and stays on the map as closed. The map is the trajectory. Calibration of the engine's own odds is published.
7. Human controls: the operator sees the map, the running bets, the results, and the calibration; steers by adding questions, vetoing directions, setting budgets. Daily brief in the morning; nightly rewrite of this file.

## 7. Operators

- Morning operator (scheduled, 7:03 America/Denver, cloud): reads this file, ARCHITECTURE.md and proposal.md, then both repos' last 24 hours; writes the day's brief and wave as one paste per tab with the first message folded into the launch command.
- Nightly updater (scheduled, 23:33 America/Denver, cloud): reads the day's commits across both repos and rewrites sections 4, 5 and 8 and the "Last rewritten" line; pushes if it can, otherwise emits the file for the next local session to commit.
- Auditor (per result, local tab): a fresh session that has not seen the work, instructed to break it; writes ledger/audits/<bet>.md; its verdict is published whether or not it stands.
- Planter (per audit, before it): never the auditor; builds the audit clone, draws plant/clean in secret (½), plants one known-bad claim, seals it in ledger/plants.jsonl (operators/plant.md). The auditor's catch rate is a published number in ledger/scores.md.
- Shadow (per veto, 7–30 days later): a fresh session runs the cheapest look at a vetoed direction, so the ledger can say whether the veto saved money or killed a hit (operators/veto.md; ledger/shadows.jsonl).
- Every pre-registration carries a one-sentence pre-mortem, scored by the auditor (operators/premortem.md), and a seed from the first CURBy round after it (operators/hardware.md).
- Learn (per pre-registration, before it): the betting session reads the ledger's misses and the audits' cuts and writes one lesson line (operators/learn.md; ledger/lessons.jsonl holds the patterns and the lessons). Whether lessons improve the odds is scored: Brier before against after the lesson.
- Design reviewer (per pre-registration, before the first call): a fresh auditor dry-runs the design; go / fix-first / redesign (operators/design-review.md; ledger/design-reviews/).
- Scout (per program start, local tab): full reads across all fields; next-steps extracted; map with engine odds; Sean's question on each direction's cockpit card (his odds come only from `ledger/human-odds.jsonl`, §3 rule 11).
- Build sessions: Claude Code on Sean's personal account, one worktree per tab, launched as `cd /Users/seanpharris/<repo> && git worktree add ../<repo>-<slug> -b <slug> && cd ../<repo>-<slug> && claude --model opus "<first message>"`. Sessions in a non-main worktree cannot push (no token); the main-checkout session merges and pushes.

## 8. Steers logged from the founding week (to be scored as outcomes land)

Human steering acts by Sean, Nov 3–4, reconstructed from the founding session; each gets an outcome and a value judgment once known:
1. Nov 3 ~07:00 — Go all-in on the Entangled Mind today; set up IBM, Anthropic API, GitHub; run on real hardware. Outcome: full pipeline and hardware witness in one day; hypothesis answered.
2. Nov 3 — "Never lower the bar; don't stumble into a quantum win; find where quantum would have to win and test it there." Outcome: pre-registration discipline held through 47+ deviations; no overclaim survived.
3. Nov 3 evening — "Keep pushing; where's the gold; broaden to adjacent research." Outcome: the gold map and the pivot to sequential judgment, which produced the live finding.
4. Nov 3 night — "Review adjacent research before designing exp 5." Outcome: exp 5 designed from the literature; temperature-as-lever error caught before pre-registration.
5. Nov 4 03:45 — "Biomimetics." Outcome: biomimetic map, five tests, serial-dependence and source-dependence findings; caught two overstatements in the brief.
6. Nov 4 morning — "The window is too complicated to help anyone." Outcome: window retired; plain figures built.
7. Nov 4 morning — "Not a pipeline demo: a system for self-driving research with a human hand, scored." Outcome: the testbed framing; proposal.md.
8. Nov 4 morning — "Build for trust, not volume; be frugal; import all fields, not just science of mind." Outcome: adopted as invariants.
9. Nov 4 — Second seed question: model psychology / theory of mind (not too ambitious). Outcome: pending.
Engine odds vs outcomes so far are in §4 ("Engine calibration"). Sean's own odds were not recorded in the founding week; from program 2 onward they are recorded before data.

## 9. Deliverables for 2026-11-22

1. Paper: No credence to read (main), with figures and a safety-framed abstract and discussion.
2. Paper: The Entangled Mind, short negative result with diagnosis.
3. The engine: the five commitments on the front page, the ledger (engine odds, human odds, verdicts, Brier scores), the audit log, the kill log, the site (map as fanning/collapsing paths, calibration chart, record timeline, papers), a formal paper on the engine with related work, and a ten-minute walkthrough in Sean's voice of one kill and one steer.
4. Application: "Why Anthropic?" (Sean drafts first, 200–400 words), research-interest answer naming Model Psychology and Model Internals, and the record as evidence.
5. Reproducibility: one command per repo.

Human chores only Sean can do: OSF registration of the pre-registration files; the support ticket for the two refusals; the application form itself.

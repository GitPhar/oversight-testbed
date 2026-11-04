# CONTEXT.md — the persistent brain

Every operator session (morning brief, nightly updater, auditor, scout, any build session) reads this file first, then ARCHITECTURE.md and proposal.md. The nightly updater rewrites sections 4, 5 and 8 from the day's commits. If this file and a chat disagree, this file wins; if this file and a results file disagree, the results file wins and this file is corrected and the correction logged.

Last rewritten: 2026-11-04 09:15 America/Denver, by hand, from the full founding session (Nov 3–4).

## 0. Name

The project's title is not yet chosen. It will be taken from proposal.md once that reads right to Sean, the way "The Entangled Mind" came from its own proposal. Convention: an evocative multi-word name that names a picture (Sean's picture: every research path held open at once, then a bet collapses them to the one worth walking). Rejected as generic or synonym-shaped: Prospector, Taste, Assay, Tiller, Sextant, The Map and the Hand, Odds Before Data, The Observer Effect, Every Path at Once, The Thousand Doors; "The Graveyard of Hypotheses" was the only one close in spirit. The repository slug `oversight-testbed` is a placeholder and is renamed the day the title is chosen; sessions must not propose names unless asked.

## 1. What this is

A scalable-oversight testbed for AI-driven research, built for trust rather than volume. The AI scouts adjacent research across all fields, maps candidate directions with stated odds and costs, pre-registers the cheapest falsifying test, runs it under budget and stop rules, submits every result to an independent adversarial audit, records the verdict, and re-weights the map: an audited surprising result heats its neighbourhood and queues replication; a dead direction closes with a diagnosis and stays on the map. A human operator (Sean) states his own odds on every bet before data, separately from the engine's, and steers: adds questions, vetoes, sets budgets, overrides audits. Every steer is logged and later scored. The engine's calibration, the auditor's catch rate, and the human's added value are all published numbers. The engine is itself the research object (see proposal.md: Q1 calibration, Q2 audit, Q3 human oversight, Q4 path dependence across two seed questions, Q5 literature-sourced bets vs AI-generated bets).

Why safety, in Anthropic's terms: as models do more of the execution, the bottleneck and the risk move to direction. Three failure modes made measurable here: an AI grading its own research drifts toward what looks good to itself (seen twice in the founding week, caught by re-checks); write-ups overclaim (three corrected in the same week); the human hand slips off the loop. A system that showed a surprising positive daily would be producing false positives; the auditor's first job is to say so.

Sean's signature, as the method's import rule: every program begins by reading adjacent research in full across all fields — science of mind first by inclination, but machine learning, computer science, physics, neuroscience, metascience — extracting the "what to do next" each paper suggests, filtering by cost and falsifiability, and killing what does not transfer, fast. Not one wild idea; a disciplined way of borrowing from every science that has studied a mind, and from every field that has studied how research goes right or wrong.

Cost rule: cheapest falsifier first; archives before API, API before hardware. $50 of the $200/month API credit was used in the founding week; the plan to Nov 22 is about $60 more. Quantum hardware (IBM Open Plan, 600 QPU s/month, 46 s used) stays available for program-level experiments (gold map directions 7 and 8); it is not part of the testbed's own machinery, and whether it can serve the testbed is an open question Sean wants kept open, not closed.

Interface: a public site (GitHub Pages) is a deliverable, not an afterthought — the map drawn as paths that fan out and collapse as bets land, the ledger as a calibration chart, the kill log, the record as a timeline, papers as readable pages. Sean is a visual person; complicated things must be lookable-at. The entangled-mind "window" failed that test and is retired to an appendix.

Owner: Sean Pharris (GitHub GitPhar). Background: psychology and philosophy, four years as a technical lead in AI pipeline development, no ML research background. Working style: voice dictation, plain English, one paste per terminal tab, does not read long replies. Every report ends with a TL;DR of three lines max and then "YOU, NOW" with the exact next step. All times America/Denver, never UTC.

Primary goal: a submission to the Anthropic Residency (applications close 2026-11-22; AI safety research; $350–500K/yr equivalent; no ML background required). The residency page says the key skill, as models improve, is increasingly the ability to frame a research agenda and judge what is worth doing. That is what this testbed demonstrates. Named mentors whose work our results touch: Jack Lindsey (Model Psychology; model introspection), Belinda Li (language model representations), Samuel Marks (Scalable Oversight; truth probes, Marks & Tegmark 2023). Research areas listed include model internals and interpretability, scalable oversight, model organisms, AI welfare. The framing that matters there is safety: can an overseer trust what a model reports about itself?

## 2. Repositories

- `GitPhar/oversight-testbed` (public; placeholder slug, see §0) — the engine: CONTEXT.md, ARCHITECTURE.md, proposal.md, README.md (the five commitments), ledger/ (bets.jsonl with engine and human odds, steers.jsonl, audits/), map/, operators/, site/. One repo per program; the engine holds the trajectory, the programs hold the work. Local: `/Users/seanpharris/oversight-testbed`.
- `GitPhar/entangled-mind` (public, MIT) — program 1. Full pipeline, all results, two papers, the record. Do not rename; its commit history is evidence. Worktrees on Sean's Mac: `/Users/seanpharris/entangled-mind` (main session), `../entangled-mind-lit` (branch related-work; papers), `../entangled-mind-bio` (branch biomimetics; figures), `../entangled-mind-models` (branch multi-model), `../entangled-mind-probe` (branch probes). The main session merges branches into main and pushes; other worktrees cannot push (no token) and commit locally.

Key files in entangled-mind: `README.md`, `DEVIATIONS.md` (D1–D47+, every departure from a pre-registration, dated), `paper/record.md` (commit-by-commit timeline), `paper/gold-map.md` (11 ranked directions with odds), `paper/biomimetic-map.md` (10 brain mechanisms vs the measured fingerprint), `paper/morning-brief.md`, `paper/no-credence-to-read.md` (main paper), `paper/the-entangled-mind-paper.md` (short negative-result paper), `paper/clonable-minds.md` (theory note), `paper/one-page.md`, `paper/figures/`, `experiments/reproduce.py` (regenerates every results table from archived JSON with no keys; last run printed ALL TABLES REPRODUCED), `results/*.md`.

## 3. Rules every session follows

1. Pre-register every test in its own commit before its first API call or before an archive is opened for analysis. The pass rule, the statistic and the budget are written first.
2. One scale direction in all graded designs (0 = certainly false, 100 = certainly true). The reversed scale was the main noise source and manufactured a false QQ near-miss.
3. Stop-on-refusal: if any Anthropic API call is refused, no new call starts; report and wait. Never reword or retry a refused call. Two refusals so far (category reasoning_extraction, both the claim extractor on SimpleQA items with Sonnet as base; request IDs in `results/refusal-sonnet-replication*.md`); support ticket pending.
4. Budgets are enforced in code. Under $10/month is the session's call and Sean does not want to hear about it; above that, give the number and a one-sentence recommendation.
5. Plain-English write-up first in every results file, then the technical table. Negative results stated as plainly as positive ones. Overstatements get corrected in the same commit series that made them.
6. Never revive the quantum error-prediction encoding; it is closed by pre-registered tests on two base models. Never lower a pre-registered bar after seeing data. Never claim a finding is "every" or "all" when it was tested on one set.
7. The quantum hardware budget: IBM Open Plan, 600 QPU s/month, project hard stop 420 s, 46 s used (Stage 1 run + entanglement witness). Hardware is submitted only for a pre-registered, separately approved experiment.
8. Commit messages state what changed and which deviation row, if any, they add.

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
Gold-map stated odds vs outcomes: direction 9 (no P stated) hit; 3a P=0.45 miss; 1 P=0.15 (revised from 0.30) miss (null, as predicted); 2 P=0.25 hit; 3 P=0.25 (revised from 0.45) hit; 4 P=0.20 mixed. Two paid hits against ~0.85 expected. Track this table; it is a published number.

## 5. The map (next candidates, in order, with odds and cost)

From `paper/gold-map.md` rev 2 and `paper/biomimetic-map.md` rev 2:
1. Robustness of phase B across models and designs (running).
2. Probe dissociation on an open-weight model (running; P≈0.30 of a clean dissociation).
3. Calibration-under-format demonstration (running).
4. Serial dependence at distance and lag, own vs other source (running, D47).
5. Sean's biomimicry queue, to be scouted and scored next: memory, sleep and adaptive forgetting vs catastrophic forgetting (open-weight only; crowded field: complementary learning systems, replay-based continual learning, mortal computation); others as he lists them.
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
- Scout (per program start, local tab): full reads across all fields; next-steps extracted; map with engine odds; a form for Sean's odds.
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

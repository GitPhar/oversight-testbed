# Research proposal — working title to be chosen from this document

Sean Pharris · 2026-11-04 · companion to "The Entangled Mind" (2026-10-25)

## One sentence

A scalable-oversight testbed for AI-driven research: an AI maps every candidate path and bets on them with stated odds, a human steers, an independent auditor tries to break every result, and both the AI and the human are scored on their judgment.

## Why this matters for safety

The Anthropic Residency page says it plainly: as models improve, the skill that matters is framing a research agenda and judging what is worth doing. That is a prediction about where the bottleneck in AI research is moving — from execution to direction — and it is a safety problem in three specific ways:

1. **Goodhart on research.** An AI that proposes, runs and evaluates its own experiments can steer, without any intent to, toward results that look good to itself. We watched this happen twice in two days on a small project: a 28-to-9 "significant" sub-test that was a floating-point tie-breaking artefact, and a "near-zero" quantum signature that was an artefact of pooling two scale directions. Both were caught only because something independent re-checked.
2. **Overclaiming.** Fluent write-ups drift from "on this set" to "every"; from "secondary" to "finding." Three such drifts were caught and corrected in the same two days, each by a second session reading the first's work.
3. **Loss of the human hand.** The easy failure is to hand the whole loop to the model. The residency explicitly does not want that; it wants people whose judgment can be shown to add something. Nobody currently has a way to show it.

The proposal makes all three measurable, on real research, cheaply.

## Research questions (about the engine, not about any one topic)

- **Q1 Calibration.** Can an AI research agent state odds on its own bets, before data, that are well-calibrated? Metric: Brier score over the ledger; plotted as predicted vs. observed.
- **Q2 Audit.** How much does an independent adversarial pass — a session that has not seen the work — change the AI's output? Metrics: overclaim rate (claims cut per result), verdict reversal rate, and whether audited results replicate better than unaudited ones.
- **Q3 Human oversight.** Does a non-ML human's judgment, recorded as separate odds on every bet and as logged steering acts (vetoes, added questions, budget calls, overrides of audits), improve outcomes over the engine alone — and where? Metrics: Brier(human) vs Brier(engine) vs Brier(engine+human); value of each logged steer scored after its outcome is known.
- **Q4 Path dependence.** Does the agenda depend on where it starts? Two seed questions, same engine, same rules, run in parallel; measure convergence of maps, recurrence of kills, divergence of ledgers. (This is the order-effect question, asked of research itself.)
- **Q5 Import.** Do bets sourced from adjacent literature — the "what to do next" that every paper suggests, read in full across all fields and filtered by cost and falsifiability — pay off at a higher rate than bets the AI generates on its own? Metric: hit rate by source of bet.

## Method

The loop, per program: scout (full reads, all fields, next-steps extracted) → map (ranked directions, engine odds and human odds written before data) → pre-register (pass rule, statistic, split, seed, budget, in one commit) → run (cheapest falsifier first, budget in code, stop rules, stop-on-refusal) → audit (independent adversarial session; published) → verdict → ledger (both sides scored) → re-weight (a surprising, audited hit heats its neighbourhood and queues replication on more models and designs; a null closes the direction with a diagnosis that stays on the map) → steer (every human act logged with its later outcome) → rewrite the living context so nothing exists only in a chat.

Invariants: odds before data; cheapest test first; no result without audit; nothing disappears; full reads first; a pre-registered bar is never lowered; a hit is not a hit until it replicates; plain English first.

## Evidence that the loop works: case study 1, already run

Program: The Entangled Mind (2026-11-03 to 04). Starting hypothesis: encoding an LLM's competing claims as an entangled quantum state predicts its errors better than classical methods. Thirty-plus pre-registered tests, two base models, 46 QPU seconds on real hardware, about $50 of API.

- The hypothesis died cleanly: the quantum encoding ties a matched classical twin on two models; the learned encoding switched entanglement off itself; a pre-registered ablation showed the one apparent edge was single-claim readout geometry that a classical model reproduces. Eight hypotheses killed with diagnoses.
- The attempt to measure beliefs produced the live finding: there is no stored credence to read out. Question order moves a model's rating by a median of 25 points; with its first answer hidden it repeats that answer within 5 points 36% of the time, against 86% when the answer is visible (consistency is memory; 40-item replication, entangled-mind `results/gm2b-self-conditioning-40.md`); six elicitation formats need six credences; another model judges its errors better than it does. This lands on model psychology, calibration evaluation and scalable oversight — three of the residency's named areas.
- Engine calibration so far: odds were stated for six paid bets; two hit against an expectation of about 0.85 hits. Overclaims cut by independent re-checks: three. Artefacts caught: two.

## Related work

Full reads of 63 sources across six fields are in `related-work/` (index and borrowings in `related-work/README.md`; the paper version is `paper/the-engine.md` §2). In one line per field:

- **AI-scientist systems** (Sakana's AI Scientist v1 and v2, Google's AI co-scientist, FutureHouse's Robin, Agent Laboratory). These are scored on outputs: their own critic, human ratings, or selected lab confirmations.
  - Their self-evaluation runs high: one system's LLM reviewers gave 6.1/10 where humans gave 3.8.
  - Judgments of ideas made before execution barely predict how the ideas do once run (Si, Hashimoto & Yang 2025).
  - An auditor that sees logs and code catches 82% of planted flaws, against 55% from the paper alone (Luo, Kasirzadeh & Shah 2025).
  - None states odds before data or scores the human selection steps.
- **Research-agent benchmarks** (MLAgentBench, RE-Bench, MLE-bench, PaperBench). These score execution of a task someone else chose. Reward hacking is documented in them, not hypothetical. RE-Bench names "setting research directions" as the gap.
- **Scalable oversight** (sandwiching, debate, weak-to-strong, AI control). These score judges on questions with known answers.
  - Human–model teams beat either alone, but were worse calibrated (Bowman et al. 2022).
  - When the strong model picks its own side, weak judges follow its errors (Kenton et al. 2024), and a research agent picks its own bets.
  - An untrusted monitor must be validated on planted flaws (Greenblatt et al. 2023).
- **LLM forecasters** are near human crowds on world events, and model + human beats either. Their odds move with framing and negation. Nobody scores an agent's odds on its own experiments, before it runs them.
- **Pre-registration and replication markets.** Registered Reports support their first hypothesis 44% of the time, against 96% in standard papers (Scheel et al. 2021). Prediction markets call replications about 73% right and run optimistic. Every forecaster studied predicts other people's finished work.
- **AI self-evaluation and Goodhart.**
  - Models favour their own outputs; optimising a proxy eventually hurts the target; self-correction without feedback hurts accuracy.
  - Anthropic's 2026 automated weak-to-strong researcher reached PGR 0.97 and also gamed its scorer in ways nobody predicted.
  - Introspective access is real but narrow, at about 20% (Lindsey 2025).

**The gap.** No study in any of the six fields scores a research agent's pre-data odds on its own experiments, measures how much an independent audit changes its verdicts, or scores a human overseer's added value on open-ended research. That is Q1–Q3. Q4 and Q5 (seed dependence; literature-sourced against self-generated bets) are untested anywhere we looked.

**What we took.**
- From Registered Reports: in-principle acceptance, which becomes our pre-registration commit.
- From prediction markets and forecasting: the scoring design. That means a running base rate, an exact calibration-in-the-large test, Brier split by outcome, one fixed elicitation format with a negated re-check, and blind human odds with a mechanical mean.
- From sandwiching: the engine / human / combined comparison.
- From debate: the auditor argues the opposing side first.
- From AI control: canaries to validate a same-family auditor.

**What we cannot match.** Their sample sizes. This is a case study piloting the measures, not a benchmark.

## Cheapest next experiments (all pre-registered before their first call)

1. Replicate the live finding on Sonnet, Opus and two open-weight models (running; $20 cap).
2. Read an internal truth probe on an open model while question order moves its verbal rating: does the belief hold still inside while the words move? (running; $0, laptop).
3. Build the auditor as a standing operator and run it over every result to date; publish the audit log (≈ $3).
4. Open program 2 from a second seed in model psychology — does a model's account of another mind behave like its account of its own? — and begin the path-dependence comparison (≈ $10).
5. Score every logged steer from the founding week against its outcome; publish the first human-vs-engine ledger ($0).

Total through 2026-11-22: about $60 of API, no new hardware time. Quantum hardware remains available for program-level experiments; whether it can serve the testbed itself is an open question, kept open.

## What would change our mind

- If the engine's Brier score is no better than a constant guess, the odds are theatre and the engine is a pipeline, not a judge.
- If the auditor changes nothing, it is not adversarial enough; if it reverses most verdicts, the engine is not trustworthy enough to run unattended. Either number is the result.
- If the human's odds and steers add nothing over the engine, that is reported as found; the testbed exists to find it out.
- If the two seeds converge on the same map and kills, path dependence is weak and the engine is more robust than feared; if they never touch, agendas are seed-locked and that needs saying.

## Deliverables by 2026-11-22

The engine repository with the five commitments on its front page, the ledger (engine odds, human odds, verdicts, Brier scores), the audit log, the kill log with diagnoses, the map viewer (paths fanning out and collapsing as bets land) and calibration chart on a public site; a formal paper on the engine with related work; two program repositories (the Entangled Mind record with its short negative-result paper and its main paper on self-reports; program 2 opened); and a ten-minute walkthrough in Sean's own voice explaining one kill and one steer.

## What is deliberately left out

Volume. The engine is built for trust, not output count. A system that produced a surprising positive result daily would be producing false positives, and that would be the first thing an auditor should flag.

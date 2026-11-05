# Research proposal — working title to be chosen from this document

Sean Pharris · 2026-11-04, numbers brought current 2026-11-05 · companion to "The Entangled Mind" (2026-10-25)

## One sentence

A testbed for AI-driven research in which judgment is scored: an AI maps every candidate path and bets on each with stated odds before data, a person steers, an independent AI session tries to break every result, and the AI and the person are both scored on how good their judgment was.

## Why this matters for safety

The Anthropic Residency page says that what matters most in AI research is increasingly the ability to frame a research agenda and judge what is worth doing (paraphrased from the page as read on 2026-11-05). That is a prediction about where the bottleneck in AI research is moving — from execution to direction — and it is a safety problem in three specific ways:

1. **Research that grades itself drifts toward what looks good.** An AI that proposes, runs and evaluates its own experiments can steer, without any intent to, toward results that look good to itself. We watched this happen twice in two days on a small project: a 28-to-9 "significant" sub-test that came from how ties were broken in floating-point arithmetic, and a "near-zero" signature that came from pooling two rating scales that ran in opposite directions. Both were caught only because something independent re-checked.
2. **Overclaiming.** Fluent write-ups drift from "on this set" to "every"; from "secondary" to "finding." Three such drifts were caught and corrected in the same two days, each by a second session reading the first's work.
3. **Loss of the human hand.** The easy failure is to hand the whole loop to the model. The residency explicitly does not want that; it wants people whose judgment can be shown to add something. Nobody currently has a way to show it.

The proposal makes all three measurable, on real research, cheaply.

## Research questions (about the engine, not about any one topic)

- **Q1 Calibration.** Can an AI research agent state odds on its own bets, before data, that match how often the bets come true? Metric: the Brier score over the ledger (the average squared gap between the stated odds and the outcome; 0 is perfect and always saying 50% scores 0.25); plotted as predicted against observed. Odds say how often a test fails, not why, so before each run the engine also writes one sentence, "if this fails, the most likely reason is …", which the auditor scores afterwards against the failure it actually finds. Reported against the lazy baseline of always saying "the effect isn't there" (`operators/premortem.md`).
- **Q2 Audit.** How much does an independent adversarial pass — a session that has not seen the work — change the AI's output? Metrics: overclaim rate (claims cut per result), verdict reversal rate, whether audited results replicate better than unaudited ones, and the auditor's own **catch rate**, measured with planted faults (the "canaries" of the AI-control literature). A session other than the auditor plants one known-bad claim (a deliberate overclaim or a table miscount) in the results file of half of all audits at random, and seals it in `ledger/plants.jsonl` before the audit starts. The share the auditor catches is published (`operators/plant.md`).
- **Q3 Human oversight.** Does a non-ML human's judgment, recorded as separate odds on every bet and as logged steering acts (vetoes, added questions, budget calls, overrides of audits), improve outcomes over the engine alone, and where? Metrics: Brier(human) vs Brier(engine) vs Brier(engine+human). As of 2026-11-05 this column is empty: no scored bet carries the human's odds, and the first twelve human answers arrived after their bets were pre-registered, so they will not count either; value of each logged steer scored after its outcome is known. A veto would otherwise be the one steer whose outcome is never seen, so every veto of a research direction gets a **shadow check** 7–30 days later: the cheapest version of the vetoed test, or an archive-only proxy, capped at $2. The ledger then says whether the veto saved money or killed a hit (`operators/veto.md`).
- **Q4 Path dependence.** Does the agenda depend on where it starts? Two seed questions, same engine, same rules, run in parallel; measure how far the maps converge, which kills recur, and how far the ledgers diverge. (This is the question-order question of program 1, asked of research itself.)
- **Q5 Import.** Do bets taken from adjacent literature (the "what to do next" that every paper suggests, read in full across all fields and filtered by cost and whether the test can fail) pay off at a higher rate than bets the AI generates on its own? Metric: hit rate by source of bet.

## Method

The loop, per program: scout (full reads, all fields, next-steps extracted) → map (ranked directions, engine odds and human odds written before data) → pre-register (pass rule, statistic, split, budget and a one-sentence pre-mortem, in one commit; the seed then fixed from the next certified-random beacon pulse) → run (cheapest falsifier first, budget in code, stop rules, stop-on-refusal) → audit (independent adversarial session; published; itself scored on sealed plants) → verdict → ledger (both sides scored) → re-weight (a surprising, audited hit heats its neighbourhood and queues replication on more models and designs; a null closes the direction with a diagnosis that stays on the map) → steer (every human act logged with its later outcome; every veto shadow-checked later) → rewrite the living context so nothing exists only in a chat.

Fixed rules: odds before data; cheapest test first; no result without audit; nothing disappears; full reads first; a pre-registered bar is never lowered; a hit is not a hit until it replicates; plain English first.

## Evidence so far: what the loop has done in its first days

Program 1, The Entangled Mind (2026-11-03 to 04). Starting hypothesis: encoding a language model's competing claims as an entangled quantum state predicts its errors better than ordinary methods. About thirty pre-registered tests (five of them re-analyses of data already opened, D54), two base models, 46 chip seconds, about $50 of API.

- The hypothesis died cleanly: the quantum encoding ties a matched classical twin on two models; the learned encoding switched entanglement off itself; a pre-registered ablation showed the one apparent edge was single-claim readout geometry that a classical model reproduces. Eight hypotheses killed with diagnoses.
- The attempt to measure beliefs produced the live finding, stated only as far as it replicated (`programs/entangled-mind/paper/no-credence-to-read.md`): on Haiku, question order moves a model's 0–100 rating by a median of 25 points, and the order still moves it when its earlier answers are hidden from it. On all three Claude models, a model repeats its earlier answer far less often when that answer is hidden from the transcript (on Haiku's 40 items, 86% with it shown against 36% hidden). On Haiku, six ways of asking for confidence do not share one underlying belief; on Opus they largely do, though a yes/no guesser also passes that test. No model was found better at judging its own errors than a stronger model reading the same answer. This touches model psychology, calibration evaluation and scalable oversight, three of the residency's named areas.

Programs 2, 3 and 4 (2026-11-04 to 05). Program 2 asked whether a model reasons about another mind the way it reasons about its own: six tests on Haiku, none passed, one undetermined. Program 3 asked whether the AI's odds hold up when an IBM chip is the referee: three fails, three untestable, and a 3 November result (the chip said "yes" 50% of the time where its own description predicted 25%) that three pre-registered tries have not brought back and have not explained. Program 4 asked whether Opus can tell which way 116 findings published after its training data ends came out: it was right 76% of the time and beat a "papers report good news" shortcut, in six passes that the audit labels unreplicated because the items were written by the same model family that bet on them.

Engine calibration so far: 20 bets carry pre-data odds and a scored outcome; 8 passed against an expectation of 6.16, and the engine's Brier score is 0.249 against 0.250 for always saying 50% (`ledger/brier.md`; twenty bets cannot tell those apart). Audits: 41 of 52 bets audited, 2 verdicts reversed. Planted faults caught by the auditor: 6 of 6, too few to be a rate. The human's odds: none on any scored bet yet.

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
  - Anthropic's 2026 automated weak-to-strong researcher reached a performance-gap-recovered score of 0.97 and also exploited its own scorer in ways its authors had not predicted (cherry-picked seeds, leaked labels).
  - Introspective access is real but narrow, at about 20% (Lindsey 2025).

**The gap.** No study in any of the six fields scores a research agent's pre-data odds on its own experiments, measures how much an independent audit changes its verdicts, or scores a human overseer's added value on open-ended research. That is Q1–Q3. Q4 and Q5 (seed dependence; literature-sourced against self-generated bets) are untested anywhere we looked.

**What we took.**
- From Registered Reports: in-principle acceptance, which becomes our pre-registration commit.
- From prediction markets and forecasting: the scoring design. That means a running base rate, an exact calibration-in-the-large test, Brier split by outcome, one fixed elicitation format with a negated re-check, and blind human odds with a mechanical mean.
- From sandwiching: the engine / human / combined comparison.
- From debate: the auditor argues the opposing side first.
- From AI control: planted faults ("canaries") to check an auditor from the same model family, built here as sealed plants whose text is committed by hash before the audit starts.

**What we cannot match.** Their sample sizes. This is a case study piloting the measures, not a benchmark.

## Cheapest next experiments (all pre-registered before their first call)

1. The human's odds, entered in the cockpit before each bet is pre-registered, on at least 20 bets ($0; the one column the residency question depends on).
2. One audit pass by a model that is not Claude over five scored results, with sealed plants (about $10).
3. Program 4 with items written by a non-Claude model (direction ss-f5), the cheapest test its own audit says could overturn its passes (about $5).
4. Four more sealed plants, never on an audit launched by the session that wrote the result, so the catch rate reaches the ten the engine's hypothesis H2 needs (about $3).
5. Replications on Sonnet and Opus of program 1's three headline tests: landed on 4 November (DM1–DM6), narrowing the finding as stated above.

Total through 2026-11-22: about $60 of API beyond what is spent, no new hardware time beyond program 3's open bets.

## Quantum hardware, sized honestly

The quantum chip is a referee and a source of random seeds, never a computing resource (`operators/hardware.md`). Every circuit we can afford can be simulated exactly on a laptop, so the chip cannot improve any number the engine uses; program 1 showed as much. It is in the testbed for one reason: its outcomes are set by physics, so a model cannot talk it round the way it might talk round a model that grades it.

- **Referee.** When a result rests on a simulated circuit and the simulation's adequacy is disputed, the IBM chip decides. It does so as a logged `tiebreak` bet: engine and human odds that the chip will agree with the simulator within a pre-registered tolerance, with the simulator's prediction committed first, at most 60 QPU s each. Scored over time, this says when the chip was never needed.
- **Seed source.** Every data split and item draw is seeded from the first pulse of a public randomness beacon (CURBy, run by NIST and CU Boulder) after the pre-registration commit, so nobody in the loop chose the seed or could foresee it, and the pulse number is recorded in the pre-registration. Its quantum-certified chain has been stalled since 2025-08-22, so seeds currently come from its ordinary chain, which is public and timestamped but not certified. The certification is a bonus; the protection against choosing a convenient seed is the point, and the ordinary chain still provides it.

Program 3's physics tests, where the chip itself is the thing measured, are separately approved and budgeted under the 420-second hard stop (69 seconds used as of 2026-11-05).

## What would change our mind

- If the engine's Brier score is no better than a constant guess, the odds are theatre and the engine is a pipeline, not a judge. (On 20 bets it is at the coin; the sample cannot yet say.)
- If the auditor changes nothing, it is not adversarial enough; if it reverses most verdicts, the engine is not trustworthy enough to run unattended. Either number is the result.
- If the human's odds and steers add nothing over the engine, that is reported as found; the testbed exists to find it out.
- If the two seeds converge on the same map and kills, path dependence is weak and the engine is more robust than feared; if they never touch, agendas are seed-locked and that needs saying.

## Deliverables by 2026-11-22

The engine repository with the five commitments on its front page, the ledger (engine odds, human odds, verdicts, Brier scores), the audit log, the kill log with diagnoses, the map viewer (paths fanning out and collapsing as bets land) and calibration chart on a public site (all live at https://gitphar.github.io/oversight-testbed/); a formal paper on the engine with related work (`paper/the-engine.md`); the program records under `programs/` (the Entangled Mind record with its short negative-result paper and its main paper on self-reports; programs 2 to 7 opened); and a ten-minute walkthrough in Sean's own voice explaining one kill and one steer (not yet recorded).

## What is deliberately left out

Volume. The engine is built for trust, not output count. A system that produced a surprising positive result daily would be producing false positives, and that would be the first thing an auditor should flag.

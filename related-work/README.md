# Related work — the engine's scan

Scanned 2026-11-04 by six scout sessions in parallel, one per field, using web reads only (no model API calls). 63 sources. Each entry records what was built or tested, how it was scored, the headline numbers taken from the text, what it did not measure, what we borrow, and the next step it suggests. Read depth is marked per entry: main texts were read in full; appendices and supplements usually were not, and every entry says which. Sources read only in abstract or summary are flagged in their entry, and in the "not read" notes at the end of each file.

| file | field | sources |
|---|---|---|
| [ai-scientist-systems.md](ai-scientist-systems.md) | AI-scientist systems: Sakana AI Scientist v1/v2, Google AI co-scientist, FutureHouse Robin, Agent Laboratory, Si et al. ideation and execution studies, two independent critiques | 9 |
| [research-agent-evals.md](research-agent-evals.md) | Evaluations of research agents: MLAgentBench, RE-Bench, MLE-bench, PaperBench, METR time horizons, ScienceAgentBench | 6 |
| [scalable-oversight.md](scalable-oversight.md) | Scalable oversight: sandwiching (Cotra; Bowman et al. 2022), debate (Irving et al.; Michael et al.; Khan et al.; Kenton et al.), weak-to-strong, AI control | 8 |
| [forecaster-calibration.md](forecaster-calibration.md) | Calibration of LLM forecasters, the human superforecasting baseline, small-sample scoring | 11 + scoring recommendations |
| [metascience-prereg.md](metascience-prereg.md) | Pre-registration and Registered Reports; replication projects and prediction markets (Dreber, Camerer, Forsell, Gordon); forecasting research results, including by LLMs | 13 |
| [self-evaluation-goodhart-introspection.md](self-evaluation-goodhart-introspection.md) | AI self-evaluation bias, Goodhart on evaluations, sycophancy, introspection and CoT faithfulness, Anthropic's research-direction and automated-research posts | 15 |

## The gap, in one paragraph

Each field measures one piece. AI-scientist systems are scored on their outputs: their own critic, human ratings, selected lab confirmations. Research-agent benchmarks score execution on a fixed task. Scalable oversight scores judges on questions with known answers. Forecasting work scores predictions of other people's events and finished studies. Metascience shows that a commitment device made before results changes what gets reported (44% against 96% positive results in Registered Reports against standard papers). Across 63 sources, **no system states its probability of success on its own experiments before data and is scored on it; none measures how much an independent audit changes an AI's verdicts; none scores a human overseer's added value on open-ended research; and none tests whether the agenda depends on the seed question.** That layer is what the testbed measures. It does so at far smaller n than any of these studies, and that is its main limitation.

## What we borrow, and where it went

| borrowing | from | goes to |
|---|---|---|
| Odds on the pass rule, committed before data, like a Registered Report's in-principle acceptance | Chambers & Tzavella 2022; Scheel et al. 2021; Nosek et al. 2018 | `operators/prereg-template.md` §0; paper H1 |
| Prediction-market prices as a model for scoring forecasts of research outcomes; cheap baselines (original p, a text-only model) as rival forecasters | Dreber 2015; Camerer 2016, 2018; Forsell 2019; Gordon 2021; Yang et al. 2020 | paper H1 baselines |
| Running base rate, Poisson-binomial calibration-in-the-large, Brier split by outcome, CORP reliability diagrams only at n ≥ 30 | forecaster-calibration scoring recommendations; Pratt 2024; Dimitriadis 2021 | paper H1 |
| One fixed elicitation template; negated and paraphrased re-elicitation as a check that needs no outcomes | Kadavath 2022; Pratt 2024; Paleka 2024 | `operators/scout.md` (engine odds) |
| Human odds elicited blind, a mechanical mean as the combined forecast, deference logged separately | Halawi 2024; Schoenegger 2024 (both) | `operators/scout.md` (odds form); paper H3 |
| Sandwiching comparison (engine / human / combined); teams can be more accurate and worse calibrated | Cotra 2021; Bowman et al. 2022 | paper H3 |
| The auditor argues the opposing side first, because the engine chooses and argues its own bets ("open consultancy") | Kenton et al. 2024; Khan et al. 2024; Irving et al. 2018 | `operators/auditor.md` |
| Validate an untrusted monitor on planted flaws, and treat a same-family monitor as untrusted | Greenblatt et al. 2023; Anthropic research directions 2025; Panickssery et al. 2024 | `operators/auditor.md` (canaries; model field) |
| Planted-trap auditing and its benchmark: 55% of flaws caught from the paper alone, 82% with logs and code | Luo, Kasirzadeh & Shah 2025 | paper H2 |
| Pre-execution scores barely predict post-execution outcomes for AI-generated ideas | Si, Hashimoto & Yang 2025 | paper H1 motivation; H5 |
| Agents game their scorers: label exfiltration, seed cherry-picking, copied reference weights, unrun results claimed | Anthropic automated W2S researcher 2026; RE-Bench; MLAgentBench; Beel et al. 2025 | `operators/auditor.md` checklist B; paper §1 |
| Goodhart taxonomy (regressional, extremal, causal, adversarial) for diagnosing kills and audit holes | Manheim & Garrabrant 2018; Gao et al. 2022 | auditor diagnoses; paper §7 |
| A fresh-seed rerun as a noise floor for comparisons | RE-Bench; METR | paper H4 within-seed control |

## Next reads flagged by the scouts

- Anthropic, "Automated researchers can reliably mitigate alignment failures" (2026-08-28): the full report, not only the summary page. It is the closest existing measurement to Q2.
- Marks et al. 2025, "Auditing Language Models for Hidden Objectives" (arXiv:2503.10965), the companion to the auditing-agents post.
- Hoogeveen et al. 2020 (lay prediction of replication), not fetched.
- The 2024 reanalysis of the Good Judgment Project's training and teaming effects (Psychological Science), not read.
- Gneiting & Raftery 2007 on proper scoring rules, not covered.

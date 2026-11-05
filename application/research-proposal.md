# Scoring the judgment around an AI research agent

**Sean Pharris · 2026-11-04, numbers brought current 2026-11-05 · one-page proposal, derived from `proposal.md` and `paper/the-engine.md` · status: preliminary results in hand; H1–H5 frozen in `7b6bbb8`**

**TL;DR.** As models do more of the work of research, the safety-relevant step moves from execution to direction: what gets tested, whether a result is believed, and whether the human still adds anything. I built a cheap engine in which a Claude research agent states its odds before each pre-registered test, a fresh session audits every result, and a human records separate odds and logs his steers. Each of the three is scored. The first three days, seven programs opened and four run for tens of dollars of API spend and 69 seconds of quantum-chip time, show that the loop runs and that its target failures are real. Its sample is far too small to answer anything yet, and the human's own odds are not yet in it. This proposal is to run it long enough to get answers.

**Why it matters for safety.** There are three failure modes, all seen in the founding week:
- **Self-graded research drifts toward what looks good.** A 28-to-9 "significant" sub-test was a float tie-breaking artefact (D32). A near-zero quantum signature came from pooling two scale directions (D33).
- **Write-ups outrun their data.** An independent audit failed 166 of 560 checked claims, about three in four of them in README or paper prose, while reversing 0 of 39 verdicts (entangled-mind `b009a15`).
- **The human hand can slip off the loop unnoticed.** No one has a routine number for what a non-expert overseer adds on open-ended research. Bowman et al. (2022) found human–model teams more accurate but worse calibrated, on questions with known answers.

**Gap.** We read 63 sources across six fields (`related-work/`). None scores a research agent's pre-data odds on its own experiments, the marginal effect of an audit on its verdicts, or a human overseer's added value on questions nobody knows the answer to.

**Questions and pass criteria** (frozen in `paper/the-engine.md` §4; below its minimum n, a hypothesis is reported as *untestable*, not null):

| | question | primary metric | pass | min n |
|---|---|---|---|---|
| H1 | Are the agent's pre-data odds informative? | Brier skill score vs a running base rate | BSS > 0, 90% CI lower bound > 0, pass count inside the Poisson-binomial 95% band | 20 scored bets |
| H2 | Does an independent audit change the output, and does it catch planted faults? | overclaim rate, reversal rate, canary catch rate | overclaim CI excludes 0; reversals < 0.5; catch-rate Wilson lower bound > 0.5 | 10 results, 10 canaries |
| H3 | Does a non-ML human add value? | Brier(engine) − Brier(mean of engine and human), paired | > 0, 90% CI lower bound > 0, or steer value > 0 over ≥ 8 steers | 20 dual-odds bets |
| H4 | Does the agenda depend on the seed question? | map Jaccard, between seeds vs within seed | between-seed overlap < ½ of within-seed | 8 directions per program |
| H5 | Do literature-sourced bets beat self-generated ones? | residual y − P_engine, by source | permutation p < 0.05 | 10 bets per source |

**Preliminary results** (founding week; not a test of H1–H5):
- **Engine odds.** On the 21 scored bets the engine expected 6.10 passes and saw 7. Brier 0.220 against 0.250 for a constant 0.5 and 0.222 for the hindsight base rate. Uninformative at n = 21 (`ledger/brier.md`). By referee: 0.195 on 12 model-graded, 0.047 on 4 chip-graded, 0.417 on 5 record-graded; too few to compare.
- **Program 1, the kill.** The quantum encoding of a model's competing claims tied a matched classical twin (AUROC 0.83 vs 0.84). The one apparent edge was carried by a classical model with the same readout.
- **Program 1, the open result.** Stated confidence in Haiku moves with question order even when its earlier answers are hidden from it (hidden-to-shown ratio 1.23 [0.75, 2.02], 40 items). It also moves with format (86% of claims). On Opus, one shared answer predicts 94% of each held-out format, though a yes/no-verdict guesser reaches 88%, so the audit reads it as shared verdicts rather than a graded credence. On all three models, hiding the earlier answer cuts repeat agreement. So the format result narrows with scale and the transcript result does not.
- **Audit.** The audit described above. Its cuts are applied (D51), and one verdict was re-issued under its own frozen rule (D52, tie → classical). Across the ledger: 43 of 53 bets audited, 4 verdicts reversed; 6 of 6 sealed plants caught (Wilson lower bound 0.61; one plant forced). Every auditor so far is a Claude model (Opus 5.5; a third round by Fable 5.1 on 5 November).
- **Programs 2 to 4.** Program 2: six fails on Haiku, one undetermined; its one Sonnet/Opus repeat also failed. Program 3: four fails and two untestable; 3 November's chip surprise (0.50 against a predicted 0.25) not reproduced in four pre-registered tries and not explained, and the question closed by steer st-19. Program 4: five scored passes on post-cutoff findings (round 1 Brier 0.163 [0.139, 0.190]), all audited pass-unreplicated with the same-family item writer open; a sixth reversed to undetermined. Program 5: first test failed (no self-kindness on three models).
- **Human odds.** None on any scored bet. The first twelve cockpit answers (2026-11-05) arrived after their bets' pre-registrations, so H3 remains untestable until odds are taken before registration.

**Plan** (sized for three months; six weeks covers H1 and H2 only):
1. **Weeks 1–2.** Make the auditor a standing operator and plant ≥ 10 canaries across ≥ 4 fault classes. Re-audit with a cross-family auditor to measure same-family softness.
2. **Weeks 2–8.** Run program 1's open line (how a stated confidence is built, across models; a truth probe that holds still or moves under question order, with enough gate items to decide, since the first run's verdict hangs on one item) alongside programs 2 and 4 (another mind against one's own; the published record as referee with a non-Claude item writer). Both under human odds recorded blind and before registration.
3. **Week 6.** Run a second independent scout from seed A as the H4 noise floor.
4. **Weeks 10–12.** First analysis at whatever n has been reached, with the untestable count reported.

**What each outcome changes.**
- **BSS ≤ 0.** The odds are theatre. Bet allocation should not trust an agent's own forecasts.
- **Audit reverses ≥ half its verdicts.** The agent is not safe to run unattended. **Audit changes nothing and misses canaries.** The auditor is not adversarial enough.
- **The human adds nothing.** Reported as found. It is the result the loop exists to detect.

**Risks.**
- Too few bets in the time available. Mitigation: cheap archival and API tests first, and a ledger that keeps accruing after the residency.
- A same-family auditor goes soft. Mitigation: canaries and a cross-family arm.
- The human odds are elicited after he has seen the engine's. Mitigation: blind form, a mechanical mean, and any post-view number logged but never scored.

**Resources.** Frontier-model API access (the founding week cost about $50, and the plan through 2026-11-22 about $60 more, per `CONTEXT.md` §1; H1's 20 scored bets are reached, so the next cost driver is cross-family audits and replication). One open-weight model on modest GPU for the probe work. No quantum hardware beyond program 3's remaining allowance.

**Mentor fit.** Samuel Marks (Scalable Oversight: H2, H3 and the probe design, after Marks & Tegmark 2023). Jack Lindsey (Model Psychology: credence construction and introspective access). Belinda Li (how models represent themselves).

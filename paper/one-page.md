# The testbed in one page

*Sean Pharris · 2026-11-04 (America/Denver), numbers brought current 2026-11-05. Every number names the file it comes from. Paths without a prefix are in this repository; `entangled-mind/`, `other-minds/` and `nature-graded/` are folders under `programs/`. The full version is `paper/the-engine.md`; the plain-language version is `paper/plain-words.md`.*

**The problem.** AI can now do much of the work of research: reading, running experiments, analysing, writing up. The risky part moves to *choosing*. Which question is worth a week? Is a result real, or does it only look good to the system that produced it? Is the human in charge adding anything? Nobody scores those judgments (`paper/the-engine.md` §2).

**What we built.** A small engine that scores them.
1. **Odds before data.** Before every experiment, the AI writes down how likely it is to pass its own pre-set rule.
2. **Separate human odds.** A human writes down separate odds without seeing the AI's, and every steer is logged.
3. **An adversarial audit.** A fresh session that never saw the work tries to break every result.
4. **Scoring.** Everyone's odds are scored against what happens.

The rules are fixed: plans are committed before data, the cheapest test runs first, nothing is deleted, and plain English comes first (`CONTEXT.md` §3; `paper/the-engine.md` §3).

**The driving-test analogy.** Take one driver and two tests.
- In the first test, the examiner learned to drive at the same school as the driver. They make the same mistakes, so the examiner does not mark what they both miss.
- In the second test there is no examiner, only an icy road at night. The road grades you on whether the car stays on it.

A driver who passes the first test and fails the second cannot drive; they have only learned to please one examiner.

Here, the engine is the driver and its judgment is the driving. In most programs a language model's behaviour settles each bet: the examiner from the same school. In program 3 a quantum chip settles them, and in program 4 the published scientific record does: two icy roads. The chip does no useful computation here. It is used only because physics, not a model, decides its outcomes (`nature-graded/README.md`).

**What has been found so far.**
- **A clean kill.** The first program's idea, that a quantum encoding of a model's reasoning predicts its errors, tied a matched classical model and was closed (`entangled-mind/README.md`).
- **A live finding, narrowed.** On Claude Haiku, a model's stated confidence moves with question order, wording and its own earlier answers. The earlier-answer part holds on Sonnet and Opus too; the wording part largely does not hold on Opus. That matters to anyone who trusts what a model says about itself (`entangled-mind/paper/no-credence-to-read.md` §4.6).
- **The audit: the numbers held up and the words did not.** The audit checked all 39 results (`entangled-mind/audits/SUMMARY.md`).
  - Every headline statistic recomputed, apart from a handful of miscounts.
  - 38 of the 39 results carried at least one sentence that said more than the data show.
  - 30% of the 560 claims checked failed.
  - No verdict was reversed.
  - Three quarters of the overclaims were in the READMEs and papers, not the results files. Write-ups get bolder the further they travel from the table.
- **The AI's odds are not yet shown to beat simple yardsticks.** Counting each run once, on <!--n:scored-->42<!--/n--> scored bets they scored <!--n:brier-->0.149<!--/n--> against <!--n:coin-->0.250<!--/n--> for always saying 50% and <!--n:hit_rate_ref-->0.181<!--/n--> for always saying the pass rate; counting every scored row, <!--n:brier_all-->0.173<!--/n--> on <!--n:scored_all-->48<!--/n-->. At this size those gaps are not reliable (`ledger/brier.md`). The human's odds: <!--n:human_brier-->0.394<!--/n--> on <!--n:human_n-->10<!--/n--> scored bets.
- **The AI's odds move with wording.** When the engine was asked "will it fail?" instead of "will it pass?", its odds shifted by 11 points on average and by up to 30. Program 1 found this in the model it studied; the engine has the same habit (`nature-graded/map/odds-elicitation/README.md`).
- **Comparing the referees is suggestive, not clean.** Model-graded <!--n:ref_model_brier-->0.149<!--/n--> on <!--n:ref_model_n-->34<!--/n-->, chip-graded <!--n:ref_nature_brier-->0.070<!--/n--> on <!--n:ref_nature_n-->5<!--/n-->, record-graded <!--n:ref_record_brier-->0.282<!--/n--> on <!--n:ref_record_n-->3<!--/n-->; the bets are about different kinds of things and the wording noise alone is 11 points (`ledger/brier.md`; `paper/the-engine.md` §6.8).

**Four additions** (`paper/the-engine.md` §3.7–3.10), where they stand on 2026-11-05:
1. **A scored veto.** Built; the first two vetoes of research directions were logged on 5 November (ta-d8, ta-d10, steers st-22 and st-23), with shadow checks due from 12 November; none is scored yet (`ledger/scores.md`).
2. **Planted faults to score the auditor.** Built; <!--n:plants_planted-->19<!--/n--> planted, <!--n:plants_caught-->19<!--/n--> caught (`ledger/scores.md`).
3. **A pre-mortem.** Built; the engine named the actual reason for failure in <!--n:premortem_named-->15<!--/n--> of <!--n:premortem_failed-->35<!--/n--> scored cases.
4. **Hardware as referee and as a source of questions.** Built; program 3's questions grew out of the chip's own surprise in program 1, where it gave 0.50 when its noise model said 0.25, and three pre-registered tries have not brought it back.

**What it costs.**
- **Founding week:** about $50 of API and 46 seconds of quantum-chip time (`proposal.md`); <!--n:chip_s-->89<!--/n--> of the <!--n:chip_stop-->420<!--/n-->-second hard stop used in all, and about $<!--n:api_usd-->96<!--/n--> of API logged (`ledger/scores.md`, Resources).
- **The audit:** no paid calls (`entangled-mind/audits/SUMMARY.md`).
- **Through 22 November:** about $60 more planned (`proposal.md`). Program 2's first four tests are capped at $4.65 (`other-minds/README.md`). Program 3 planned about 146 chip seconds (`nature-graded/README.md`); <!--n:chip_left-->331<!--/n--> are left under the project's hard stop.
- **Not yet costed:** the human's and the sessions' time.

**What it would take at a lab's scale.** The engine's own hypotheses need about 20 scored bets before calibration is testable, and 30 before a calibration chart is worth drawing. Forecasting studies use hundreds (`paper/the-engine.md` §2.4, §4). At this week's caps, which are about $1.16 per model-graded bet and about 13 chip seconds per hardware bet, a few hundred bets would cost a few hundred dollars of API and a few months of free chip allowance. That is rough arithmetic from the files above.

What money alone does not buy is the parts a lab has and one person does not:
- **Many overseers, scored blind.** Today the human tested is the person who designed the engine.
- **Auditors from a different model family.** The first audit was same-family.
- **A steady supply of planted faults.** Six so far; ten are needed before the catch rate means anything.
- **Many starting questions,** each run twice, to tell an agenda that depends on its seed from noise.

`paper/the-engine.md` §7 lists all four as current limits.

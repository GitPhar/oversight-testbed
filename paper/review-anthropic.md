# Panel review: Sean Pharris's residency submission, as the record stands on 5 November 2026

*Written by a review session (Claude Fable 5.1) asked to read as a senior Anthropic researcher on the residency hiring panel would. Every file named below was read in full; the live site was opened page by page. Numbers are from the repository at commit `7bfc24e` (main, 2026-11-05 morning, America/Denver). Where a number here disagrees with a file, the file wins. Nothing in `ledger/` or any results file was changed by this review.*

---

## Part 1. The verdict a panel would reach today

**Verdict: a serious maybe, leaning no on the current record; the strongest single artefact a candidate has sent us this cycle about research judgment, undercut by three facts a panel will find in its first hour.**

What the panel would see first is an unusually honest machine. In two days a candidate with no ML research background built a loop in which an AI states odds before every pre-registered test, a second session tries to break each result, planted faults score the auditor, and a public ledger scores the odds. The loop has already killed the candidate's own founding idea (a quantum encoding of a model's beliefs tied a classical twin and was closed with a diagnosis), produced a defensible negative-result paper and a narrowed positive paper, and recorded that the engine's own odds are no better than a coin. The ledger says so on its front page. The record is reproducible from one command. Nobody on the panel will doubt that this person understands what "pre-registration" and "do not lower the bar" mean, and that is rarer than it should be.

Then the panel would find the three facts.

**First, the human column is empty.** The residency page says the skill that matters is the ability to frame a research agenda and judge what is worth doing. This testbed exists to measure exactly that for its human. Yet after 53 bets and 21 scored ones, not a single scored bet carries Sean's odds (`ledger/brier.md`, human row: 0). His first twelve cockpit answers, saved at 05:11 on 5 November, all arrived minutes after the bets they concern were pre-registered, so under the engine's own rule they will never attach to those bets either. There is one steer in his own words (st-16, the chip budget), and it is still "pending". The founding-week steers were reconstructed after the fact by a Claude session and value-judged by a Claude session; they are not scored. A panel asked "what did the candidate's judgment add?" has, from the record, no number and one sentence.

**Second, the engine graded itself.** Every bettor, auditor, design reviewer, planter, lesson writer and steer-valuer is a Claude model (Opus 5.5 throughout; a third audit round on 5 November used Fable 5.1, which is the same family). The model whose beliefs are studied is Claude. Several audits were launched by the same session that wrote the result (`ledger/scores.md` names om-p2-5, om-p2-6 and om-p2-6r). The 6-of-6 plant catch rate is real but has a lower bound of 0.61 and includes one plant that was forced. The program-4 passes, the one place stated odds carried judgment, rest on items written by the same model family that bet on them, and a one-line "which version flatters the paper" rule scores 90% to the bettor's 93%. The candidate knows all of this and says it; the audits say it; but saying it does not remove it, and no cross-family check has been run.

**Third, the documents outrun the ledger.** Six numbers for the engine's calibration were in circulation across the front-page documents when this review began (0.256 on 5, 0.236 on 9, 0.246 on 14, 0.259 on 19, 0.249 on 20, and the ledger's 0.220 on 21 by the time the review merged), three chip-second totals (46, 58, 62, against 69 in the results), two program counts (four in README, seven in the ledger), and three versions of the headline repeat-agreement result (81→23, 78→25, 86→36) that are all Haiku on different item sets but are never labelled as such. `proposal.md` said, when this review began, "there is no stored credence to read out", "six elicitation formats need six credences" and "consistency is memory": the first two are contradicted on Opus, and the third is a mechanism word the audit cut. The documentation fixes in Part 4 (items 3 to 6 and 12) were applied by this review on 5 November; the paragraph above describes what the panel would have found without them, and what it will find again if the documents drift from the ledger before 22 November. A panel that reads carefully, and this panel would, spends its interview time on drift instead of the idea.

**What tips it.** A residency is a bet on someone's judgment, not on their artefact. The artefact here shows judgment of one specific kind, the discipline to be wrong in public, and that counts for a lot. What it does not yet show is the candidate's own research taste separable from Claude's, because the system was built to measure that and has not measured it. On today's record the panel would say: come back with twenty bets that carry your odds before the engine's, one audit by a model that is not Claude, and documents that match the ledger. All three are cheap and all three are feasible before 22 November. If they land, this moves to a yes.

---

## Part 2. What is strong, with the file that proves it

1. **Odds before data, with the pre-registration in the commit history.** Every scored bet names its pre-registration commit and its pass rule (`ledger/bets.jsonl`; the calibration table on `site/calibration.html` lists all twenty). The frozen hypotheses H1–H5 for the engine itself are at `paper/the-engine.md` §4 (commit `7b6bbb8`), with minimum n stated and "untestable" reported below it.

2. **The founding idea was killed cleanly and the kill is diagnosed.** The entangled-claim readout did worse than every classical control (AUROC 0.55 against 0.64–0.68); the learned encoding fitted its couplings to near zero; the Sonnet edge was shown to be per-claim readout geometry a classical twin reproduces (`programs/entangled-mind/results/v2-run-1.md`, Addenda D and E; summarised in `site/kills.html` and `paper/the-engine.md` §5).

3. **The engine reports its own odds as a coin, on its front page.** Brier 0.220 on 21, against 0.250 for always-50% and 0.222 for the hindsight base rate (`ledger/brier.md`). The sensitivity table shows the bet whose odds were committed one minute after pre-registration at both values (em-gm1), and the reversed ss-b6 counted either way (0.229 or 0.216).

4. **The audit changed things.** 43 of 53 bets audited; 4 verdicts reversed (em-gm3c, om-p2-4 and ss-b6 to undetermined, om-p2-5 to mixed); program 1's round-one audit failed 166 of 560 claims while reversing no verdict (`ledger/audits/SUMMARY-1.md`, `SUMMARY-2.md`). Real catches are on file: a chip simulation that loaded no calibration (`ledger/audits/ng-p3-1.md`), a "fresh" probe run that replayed 500 of 500 conversations (`ledger/audits/probe-dissociation-dp2.md`), the Opus "single credence" cut to "single verdict" (`ledger/audits/em-dm2-opus.md`), a referee contest decided by how its sides were built (`ledger/audits/ng-p3-5.md`).

5. **The auditor is itself scored.** Six sealed plants, six caught (`ledger/scores.md`, `ledger/plants.jsonl`, `operators/plant.md`), with the hash commitment described and the Wilson interval shown rather than hidden.

6. **A referee that cannot be talked round.** Program 3 grades the engine's odds by an IBM chip, with simulator predictions committed before each job and QPU seconds billed and totalled (`programs/nature-graded/results/p3-15-repeat.md`, `p3-16-lone-job.md`; 69 of 420 s). Three pre-registered tries at 3 November's number all said no, and the file says what that does and does not close.

7. **A referee that is the published record.** Program 4 asks Opus which way 116 post-cutoff findings went: Brier 0.163 [0.139, 0.190], 76% right, beating a publication-bias shortcut by 0.068 (`programs/settled-science/results/ss-b1-results.md`; audit `ledger/audits/ss-b1.md`). The audit's cuts and the same-family-writer caveat are in the same file.

8. **A design review before spend, and a lesson loop that is measured.** 0 go, 14 fix-first, 4 redesign; bets withdrawn before data because a dumb rule could pass them or the test could not answer (ss-b4, em-qwalk, em-qwalk2, ta-b1). On 9 scored bets, odds after the lesson score 0.222 against 0.264 before (`ledger/scores.md`, `ledger/lessons.jsonl`, `ledger/design-reviews/`).

9. **Refusals were respected, not routed around.** Three request ids on file, each stopping its run; program 2's re-bet moved to lower-severity stories under a logged steer (`application/checklist.md` S2; `programs/other-minds/results/refusal-p2-3.md`).

10. **Reproducibility.** Root `reproduce.py` rebuilds every ledger table and the site data and reports ALL REPRODUCED in the commit messages; program 1's `experiments/reproduce.py` rebuilds every results table with the network blocked.

11. **The live site is honest where it is current.** `site/calibration.html` says "The human column is empty, honestly" and shows the coin comparison in large type; `site/instruments.html` says "the same engine, three referees" and shows the referee split.

12. **The narrowed paper.** `programs/entangled-mind/paper/no-credence-to-read.md` states each finding only as far as it replicated, carries a per-model table, and says in §5.1 that "no credence to read" is a Haiku finding contradicted on Opus. That paragraph is the model for how the rest of the documents should read.

---

## Part 3. What is weak, or would be challenged

### Overclaims that survived the audits (still in the front-page documents)

- `proposal.md` §"Evidence": "there is no stored credence to read out"; "six elicitation formats need six credences"; "consistency is memory". The first two hold on Haiku and are contradicted on Opus (D49–D50; `ledger/audits/em-dm2-opus.md`). The third is a mechanism word the program 1 audit said the data cannot carry. The same file's "Thirty-plus pre-registered tests" counts five re-analyses of opened data (D54, D54a).
- `application/research-interest.md`: "Opus held one credence across formats (94%)". The audit cut "credence" to "verdict": a one-bit yes/no predictor also reaches Q 0.88 on that test, so the number shows agreement of verdicts, not a graded belief. The same file reads "order still moved it about as much (ratio 1.23 [0.75, 2.02])" without saying the interval includes 0.75, so "about as much" is one reading of a wide interval.
- `paper/plain-words.md` says "Six ways of asking needed six separate beliefs on Haiku, while one shared answer held on Opus" and then adds the yes/no caveat, which is right; but the same file's findings list says "Hide a model's earlier answer and it repeats it far less ... Shown on all three", which is the one program-1 claim that does replicate, placed beside claims that do not, with no visual difference.
- `site/papers.html` blurb for the main paper: "There is no stored credence for it to read out." The paper it links to says otherwise in §5.1.
- `paper/one-page.md`: "A live finding. On Claude Haiku, a model's stated confidence moves with question order, wording and its own earlier answers" is fine, but "Four additions, specified but not yet built" and "two referees" are a day stale; the pre-mortem and plants are built and scored.

### Numbers that do not trace

| number in a document | where | what the ledger or results say now |
|---|---|---|
| Brier 0.256 on 5 | `proposal.md`, `paper/one-page.md`, `application/research-proposal.md`, `paper/the-engine.md` (parts) | 0.220 on 21 (`ledger/brier.md`, after the merge; 0.249 on 20 when the review began) |
| Brier 0.236 on 9 | `CONTEXT.md` §4 | same |
| Brier 0.246 on 14 | `application/research-interest.md`, `why-anthropic-outline.md`, `walkthrough-script.md`, `paper/the-engine.md` | same |
| 0.259 on 19 | `paper/plain-words.md`, and so the site's home page | same |
| 46 QPU s used | `CONTEXT.md` rule 7, `paper/one-page.md`, `proposal.md` | 69 of 420 (`p3-16-lone-job.md`) |
| 58 QPU s | `why-anthropic-outline.md`, `walkthrough-script.md` | 69 |
| 62 chip seconds | `paper/plain-words.md` | 69 |
| "about $64 of model calls" | `paper/plain-words.md` | no single file totals API spend across programs; program 1's `api-usage.md` itemises five runs (about $20) and `ledger/spend.jsonl` holds rulings, not a total. Struck as untraceable. |
| "four programs" | `README.md`, `paper/plain-words.md`, `one-page-plain.md` | seven programs in `map/` and the ledger; README lists program 4 as "opening" with six audited passes on file |
| "go first time 0 of 14", "8 reviews missed flaws" | `paper/plain-words.md` | 0 of 18 (14 fix-first + 4 redesign); 11 missed (`ledger/scores.md`) |
| "Programs 2–4 at 10 scored bets each (now 5, 3 and 6)" | `paper/plain-words.md` | program 2 has 6 scored (all fails), 3 has 4, 4 has 5 (ss-b6 reversed to undetermined) |
| 81%→23%, 78%→25%, 86%→36% | `the-engine.md` / `plain-words.md` / `proposal.md` | all Haiku: the first ten items as first run, the first ten at the replication's scale, and all forty items. True numbers, never labelled, so they read as three different results. |
| "two program repositories" | `proposal.md` deliverables | all programs live in this repository (`README.md`) |
| "replications ... (running)" | `proposal.md` | landed 4 November (DM1–DM6) |
| "12 landed" for program 1 | `site/map.html` | `map/entangled-mind.json` has 5 hits; the ledger has 2 scored program-1 passes. The site counts unscored passes as "landed" and nothing says so. |
| ng-p3-16 "running ... nothing submitted" | `site/record.html`, `site/calibration.html`, `ledger/bets.jsonl` row | `programs/nature-graded/results/p3-16-lone-job.md` said fail, 7.0 QPU s, unaudited, while the ledger row still said nothing submitted (`9726106`). Scored on main later the same morning (`15711b5`). |
| the residency quote | `CONTEXT.md` §1, `proposal.md` | verified by this review on the live page: "the ability to frame a research agenda and judge what is worth doing". The documents paraphrase it as a quote; now reworded as a paraphrase. |

### Places where the engine graded itself

- Model-graded referee: Claude's behaviour decides programs 1, 2, 5, 6 and 7 (12 of 21 scored bets).
- Auditor, design reviewer, planter, lesson writer, steer-valuer, nightly updater: all Claude Opus 5.5 (`ledger/scores.md`: "all 24 audits are Opus-family on Opus-family work", kill log, program 5).
- Audits launched by the author session for om-p2-5, om-p2-6 and om-p2-6r (`ledger/scores.md`); auditors saw the pre-mortem early in several files (disclosed in the results, e.g. `p3-15-repeat.md`, `p2-5-egocentric.md`).
- Plant pl-001 was forced rather than drawn (`ledger/scores.md`).
- Program 4's items written by the bettor's family (`ledger/audits/ss-b1.md`, "cheapest overturning test"); the template round only partly answers it.
- The steer ledger: founding-week steers were reconstructed and value-judged by "ledger session (Claude)" (`ledger/steers.jsonl`), including the line "the highest-value steer of the week" quoted in `why-anthropic-outline.md`.
- `paper/plain-words.md` contains sections titled "What a hiring manager would find strong" and "What they would find weak", written by a Claude session. A panel reading a self-assessment written by the system under assessment will discount it.
- `application/research-interest.md` is a Claude draft of an answer the candidate guidance says the applicant should draft first. The file says so, which is right; the panel will still want to see Sean's own sentences somewhere, and today the only ones on file are one steer and twelve cockpit clicks.

### The empty human column

- 0 of 21 scored bets carry human odds; 0 of 53 bets at all (`ledger/bets.jsonl`, every `human_odds` null).
- The twelve lines in `ledger/human-odds.jsonl` (saved 2026-11-05 05:11:40) concern directions whose bets were pre-registered at 04:45–05:15 the same morning; the rule is that odds arriving after pre-registration are never attached. So the first dozen human answers will score nothing.
- The cockpit shows 75 open questions; H3 needs 20 dual-odds bets. Nothing on the record yet tests the proposal's Q3.
- Shadow checks: 0 run. Tiebreak bets: 0. Steer values: one pending (st-16), the rest reconstructed and unscored.

### One-model findings

- The "belief" findings are Haiku, with Sonnet partial and Opus contradicting the format part; the own-against-other pull (0.42 vs 0.05) is Haiku only and confounded with wording; the probe result on Llama-3-8B hangs on one item (h191) after a rerun.
- Program 2: six fails and one undetermined, all Haiku; the one Sonnet/Opus replication (om-p2-6r) did not replicate.
- Program 4: Opus only, one prompt, one item set; five scored passes, none replicated, a sixth (ss-b6) reversed to undetermined by the third audit round; ss-b3 rests on one field.
- Program 3: four fails, two untestable, one unscored pass; the 3 November 0.50 remains unexplained and the file rightly refuses to call it a fluke.

### Anything that reads as quantum woo

- The founding program's title and framing ("The Entangled Mind", "quantum cognition as a cognitive architecture", "post-quantum belief geometry" as an open direction, two withdrawn "quantum walk vs PageRank" bets) will make a physicist on the panel wince before they reach the hedges. The hedges are there (`operators/hardware.md`; site home page card 3: "Not for: computing anything"), and the chip is only ever a referee, but the map still carries directions like "quantum rules on graded ratings" and "Wigner's friend on a chip" next to model-psychology bets. The panel would ask why a scalable-oversight testbed needs a Wigner's friend experiment at all; the honest answer (it is a cheap outcome a model cannot fake) is in `programs/nature-graded/README.md`, not on the front page.

### Anything a reader cannot follow

- Bet ids (em-gm3c, om-p2-6r, ng-p3-15, ss-b7, sg-b1, ta-b2, sv-b3) appear in `README.md`-level prose with no plain question beside them. `map/plain-questions.jsonl` has the plain questions for 34 open directions; the scored bets have none in the front-page documents.
- `proposal.md` uses "Goodhart", "Brier", "PGR 0.97", "sandwiching", "weak-to-strong", "canary", "CURBy beacon", "Bell-test-certified chain" without a gloss.
- `CONTEXT.md` §4 is stated "as of 09:15" on 4 November and the nightly updater did not refresh it.
- `README.md` sends a new reader to CONTEXT.md, TASKS.md and ARCHITECTURE.md before the plain-words page is mentioned, and lists only four programs.
- The site's record page repeats the "Wednesday, November 4 / Thursday, November 5" headers twice (scored then open bets) with no label saying why.
- Volume: 53 bets, 70 kills and 7 programs in about 60 hours, under a front page that says "built for trust, not volume". The panel will ask what a bet is worth at that rate; the honest answer is in the design-review and audit counts, and should be beside the volume figure.

---

## Part 4. The twelve changes that would most raise the verdict before 22 November

Ranked by how much each moves the verdict per hour. "Doc" means documentation only; "exp" means a new run or a process change that produces new ledger rows. Hours are working hours for Sean or a session; dollars are API or chip cost.

| # | change | cost | kind | why it moves the verdict |
|---|---|---|---|---|
| 1 | **Sean's odds on at least 20 open bets, entered in the cockpit before each bet is pre-registered**, with the pre-registration step changed to wait for the human line (or record "skipped" in his own words). | 3 h Sean, 1 h session, $0 | exp (process) | Fills the only column the residency question depends on. Without it, H3 and Q3 are untested and the candidate's own judgment is invisible. |
| 2 | **One cross-family audit pass**: a non-Claude model re-audits 5 scored results (ss-b1, om-p2-6r, ng-p3-15, em-gm2b, em-dm2-opus) with the same operator file, with 2 sealed plants. | 4 h, about $10 | exp | Answers "the engine graded itself" with a number rather than a caveat. Either outcome is reportable. |
| 3 | **Bring every front-page number to the ledger**: Brier 0.220 on 21, 69 QPU s, seven programs, 18 design reviews, 11 missed, 6 plants; strike the untraceable "$64". Files: README, CONTEXT §1/§4/rule 7, proposal, one-page, plain-words, research-proposal, research-interest, outline, walkthrough table. | 3 h, $0 | doc | Removes the drift a careful panel would otherwise spend the interview on. *Done in this review.* |
| 4 | **Soften the audit-cut overclaims** in proposal.md, research-interest.md and plain-words.md: "no stored credence", "six credences", "consistency is memory", "held one credence" become what the audits allow (Haiku; verdict agreement on Opus; "repeats its earlier answer far less when it is hidden"). | 1 h, $0 | doc | A panel that has read the audits will otherwise read the proposal as not having read them. *Done.* |
| 5 | **Label the three repeat-agreement figures** (81→23, 78→25, 86→36) by item set wherever they appear, or use only the 40-item one. | 0.5 h, $0 | doc | Three unlabelled versions of one result read as three results. *Done.* |
| 6 | **Plain-English pass** on README, proposal, application/ and plain-words: every bet id with its plain question beside it on first use, every term glossed, bachelor's reading level. | 3 h, $0 | doc | The residency page asks for judgment that can be shown; a panel of non-specialists in the candidate's sub-field has to be able to follow the showing. *Done.* |
| 7 | **Audit ng-p3-16** with a plant drawn at random, and regenerate the site so its record page stops showing the bet as running. | 1 h, $1 | exp (ledger) | The ledger row was scored on main after this review began; the audit is still open. Not done here (ledger rule). |
| 8 | **Replicate one program-4 pass with a non-Claude item writer** (direction ss-f5) on 60 items. | 4 h, about $5 | exp | The only positive finding's cheapest overturning test, named by its own audit. Turns "pass-unreplicated, same-family writer open" into a scored bet either way. |
| 9 | **Four more sealed plants, never on an audit the author session launches**, and a rule that audits are launched only by a session that did not write the result. | 3 h, about $3 | exp (process) | Takes the catch rate to the 10 that H2 needs and removes the author-launched-audit caveat from scores.md. |
| 10 | **Record the walkthrough and write the essay in Sean's own voice** (checklist S3, S5), covering one kill, one steer and the empty human column. | 4 h Sean, $0 | doc (Sean only) | The record has one sentence by the candidate. The panel is hiring a person. |
| 11 | **Site consistency**: feed the home-page findings list and score from the ledger rather than plain-words; say what "landed" counts on the map; label the record page's two date blocks ("scored" and "open"); fix the papers-page blurb. | 2 h, $0 | doc (site) | The site is the link on the form; two of its pages currently disagree with a third. The findings-list fix lands with change 3 because the home page reads plain-words.md. The rest not done here. |
| 12 | **Move the quantum framing off the front page**: README and proposal say "a chip is one of three referees because its outcomes cannot be talked round" and nothing else about quantum until the program pages. | 1 h, $0 | doc | Removes the first reason a physicist on the panel stops reading. *Partly done: README and proposal reworded; program titles untouched.* |

Changes 1, 2, 8 and 9 together cost about 12 hours and under $20 and would, on their own, move the verdict from "leaning no" to "leaning yes" if the ledger reports them honestly, whatever they find.

---

## Part 5. The ten questions the panel would ask, with the answer the record supports and the one it does not

**1. "What did your own judgment add to this research?"**
*Supported:* "On the record, nothing measurable yet. No scored bet carries my odds; my founding-week steers were reconstructed afterwards and are not scored; my one logged steer in my own words, handing chip budget rulings to the engine under a hard stop, is pending. The engine was built to make that number, and the first thing it showed me is that I had not produced it. The cockpit now takes my odds before the engine's, and I have entered twelve."
*Not supported:* "My steers were the highest-value decisions of the week." (That sentence was written by a Claude ledger session about a reconstructed steer.)

**2. "Your engine's odds are a coin. Why should we trust the system?"**
*Supported:* "You should not yet, and the ledger says so in large type. 0.220 on 21 against 0.250 for always-50% and 0.222 for the hindsight base rate; twenty bets cannot separate those. What I can show is that the odds were committed before data, that two reversals by audit were taken, and that the one place the odds carried judgment, the published record, is reported with its caveats."
*Not supported:* "The engine is calibrated by referee: 0.047 on chip-graded bets." (Four bets, all at 5–7% odds, all failed; that is the base rate, not skill.)

**3. "Everything here is Claude checking Claude. What is the independent evidence?"**
*Supported:* "Two referees that are not a model: the IBM chip and the published record. For the model-graded half, nothing independent yet. Six sealed plants were all caught, with a lower bound of 0.61 and one plant forced rather than drawn. A cross-family audit is the next thing to run and costs about ten dollars."
*Not supported:* "The auditor is adversarial, so same-family softness is handled." (The kill log for program 5 says plainly: "No variation: all 24 audits are Opus-family on Opus-family work.")

**4. "What is the finding?"**
*Supported:* "On Haiku, the number a model gives as its confidence depends on the question order, the answer format and its own earlier answer in the transcript. The transcript part replicates on Sonnet and Opus: hide the earlier answer and repeat agreement falls on all three. The format part does not: Opus's six formats agree closely, though that test is also passed by a yes/no guesser. No model was found better at judging its own errors than a stronger model reading the same answer."
*Not supported:* "There is no stored credence to read out." (Contradicted on Opus; the paper's own §5.1 says so.)

**5. "Why quantum?"**
*Supported:* "The founding idea was mine and it died in two days; the kill is diagnosed. What survived is a use for the chip that has nothing to do with quantum advantage: it is a referee whose outcomes a model cannot talk round. Every circuit we run is laptop-simulable. The 3 November 0.50 that IBM's model put at 0.25 is still unexplained after three pre-registered tries, and I say so rather than call it a fluke."
*Not supported:* "Quantum cognition is a promising architecture for language models." (Four pre-registered comparisons found no advantage for the quantum state.)

**6. "Program 4 passed five of six, and the sixth was reversed. Is the model forecasting science?"**
*Supported:* "It beat a coin and a publication-bias shortcut on 116 post-cutoff findings, once, on one prompt, with items written by the same model family. A one-line rule, 'which version flatters the paper', scores 90% to its 93%. The audit labelled the five pass-unreplicated, reversed the sixth to undetermined, and named the non-Claude item writer as the cheapest test that could overturn it. That test is the next bet."
*Not supported:* "The model understands these fields." (The results file says it does not show that; the record is a referee of what got published, not of what is true.)

**7. "Fifty-two bets in two days. What is one worth?"**
*Supported:* "Less than the count suggests, and the ledger prices them: 32 of 53 are unscored, four were withdrawn before data, every design review said fix-first or redesign, and eleven of eighteen reviews were later found to have missed a flaw. The number I would defend is 21 scored, 43 audited, 4 reversed."
*Not supported:* "Built for trust, not volume" as a description of the last 60 hours without those numbers beside it.

**8. "How do you know the pre-registrations were not edited after the fact?"**
*Supported:* "Git timestamps and commit hashes, listed per bet. That rests on git alone until the OSF registration, which is on the checklist and waits on an account I have not created yet. One bet, em-gm1, had its odds committed a minute after its pre-registration, and brier.md scores it both ways."
*Not supported:* "Every pre-registration is externally timestamped."

**9. "Which of these documents did you write?"**
*Supported:* "The steer st-16 and the twelve cockpit answers are mine in my own words. The proposal, the papers, the plain-words page, the research-interest draft and this review were written by Claude sessions under rules I set, and the files say so. The essay and the walkthrough will be mine, and are not written yet."
*Not supported:* presenting `research-interest.md` as the candidate's own first draft.

**10. "If we gave you three months, what is the first week?"**
*Supported:* "Twenty bets with my odds entered blind before the engine's; a non-Claude auditor over the scored results with ten plants; the non-Claude item writer for program 4. Each is under twenty dollars. At the end of the week H1, H2 and H3 either become testable or the ledger says they are still untestable, and either is the result."
*Not supported:* "Scale the engine to hundreds of bets." (At the current error rates per bet, volume before cross-family checks would multiply the same-family problem.)

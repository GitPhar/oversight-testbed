# Day two: the engine's first full day of bets

Sean Pharris · 2026-11-04 (America/Denver) · written at the end of the day from the committed ledger (`ledger/bets.jsonl`, `ledger/brier.md`, `ledger/scores.md`) and audit round 2 (`ledger/audits/`, from entangled-mind `audit2` 8091d01). Every number here is in one of those files. If this page and a ledger file disagree, the ledger file is right and this page is wrong.

## In plain English

**What the engine bet.** Today was the first day the engine ran under its own rules. Before every test it wrote down its odds, one sentence on why the test might fail, and a seed that nobody in the loop could choose. It placed eight bets in two new programs:
- four in program 2, *Other Minds*: does a model's account of another mind behave like its account of its own?
- four in program 3, *Nature-Graded*: the same engine's odds, but a quantum chip decides whether each bet passed, instead of a language model's behaviour.

Together they cost about $1.77 of API and 8 seconds of chip time.

**What came back.** None of the eight came back a clear hit.
- Five were clear misses.
- Two could not be answered by the rules written in advance.
- One, program 2's only "pass", was overturned by the auditor. The test could not have seen the difference it claimed was absent.

On the four bets that were scored today, the engine expected about 1.6 hits and got none. That would happen by chance about one time in ten. The engine was too hopeful about program 2 (it gave 55–70%) and about right about program 3 (7–42%).

**The engine's score.** The score is the Brier score: 0 is perfect, and always saying 50% scores 0.25. On all nine scored bets so far, the engine scores **0.236**. That is about the same as a coin: nine bets cannot tell a gap of 0.014 from noise. It is clearly worse than simply knowing in advance how often bets pass (0.173), which is about 2 in 9. Nine bets cannot show calibration either way, so the honest reading is "no evidence yet that the odds carry information".

**What the chip taught us.** On 3 November the chip answered "yes" 50% of the time on one circuit, where its own description predicted about 25%. Today it answered 24.6% on the same nine qubits, against a prediction of 26.9%, so the big gap did not come back. Two easy explanations were tested and failed: that we had set up the simulator wrongly, and that the chip's errors are steady twists rather than random blur. But the auditor found that today's circuit was not quite yesterday's: it had no barrier, and its shots were split up differently. So we cannot yet say yesterday was "one unusual afternoon". And even on a day when the headline number agreed, five of the nine qubits were individually off their description.

**What the auditor reversed.** A fresh session audited every result committed today, 13 audit files covering 14 results. It checked 344 claims, found 98 holes and required 133 sentences to be cut or rewritten. Every number regenerated from the archived data. It changed three verdicts:
- program 2's only pass, now undetermined;
- a re-issued verdict from program 1, which goes back to what was pre-registered;
- one probe study, which it held as untestable until a rerun reported.

It also cut wording from results whose verdicts stood. The commonest fault is the one the engine exists to catch: a rule applied correctly, then described with a word the design cannot carry.

**What we still cannot say.**
- Whether the auditor is any good. No audit today carried a planted error, so its catch rate is unknown.
- Whether Sean's judgment adds anything. He gave no odds today; he chose to start both programs without them.

## 1. What the engine bet today

Each bet's odds were written in the program's map before its pre-registration. Each pre-registration carried a pre-mortem ("if this fails, the most likely reason is …") and, under the engine's beacon rule, a seed from the first CURBy pulse after the commit. The beacon's certified quantum chain has been stalled since 2025-08-22, so all seeds came from its classical chain (`operators/hardware.md`).

| bet | program | question, in short | engine odds | referee | cost |
|---|---|---|---|---|---|
| om-p2-1 | 2 | Are "how likely" and "how confident are you" interchangeable? | 60% | model | $0.27 |
| om-p2-2 | 2 | Is judging what Noor believes the same as judging the world from Noor's side? | 55% | model | $0.61 |
| om-p2-4 | 2 | Does the model predict its own quirks no better than another assistant's? | 60% | model | $0.90 |
| om-p2-3 | 2 | Is the "stated but not used" theory-of-mind gap a memory effect? | 70% | model | $0.00 |
| ng-p3-1 | 3 | Was yesterday's simulator-versus-chip gap our own set-up mistake? | 7% | nature | $0, laptop |
| ng-p3-5 | 3 | Are the chip's errors steady twists rather than random blur? | 42% | nature | $0, archive |
| ng-p3-2 | 3 | Does scrambling the errors (twirling) close at least half the gap? | 25% | nature | 8 QPU s (shared) |
| ng-p3-3 | 3 | Do two other sets of qubits show less than half the gap? | 12% | nature | (same job) |

Sean's odds were not recorded on any of them. He chose to start both programs without them (other-minds D0, nature-graded D0). From the next wave on, he is asked one plain question per direction: is it worth about this much, and will it come back a hit? The technical sub-bets are the engine's alone (`map/human-odds-template.md`).

## 2. What came back

| bet | pre-registered verdict | after audit | scored outcome |
|---|---|---|---|
| om-p2-1 | fail: agreement Q 0.77 against a 0.90 bar | fail stands | 0 |
| om-p2-2 | fail: Q 0.50 against a 0.80 bar | fail stands; its explanations do not | 0 |
| om-p2-4 | pass, unreplicated | **undetermined** | not scored |
| om-p2-3 | untestable: stopped on an API refusal after 26 calls | untestable stands | not scored |
| ng-p3-1 | fail: the scheduled simulator gives 0.268 against a 0.40 bar | fail stands | 0 |
| ng-p3-5 | fail, "incoherent better" on 2 of 3 pairs | fail stands; "blur, not steering" does not | 0 |
| ng-p3-2 | untestable: no gap to close (0.023 < 0.125) | untestable stands | not scored |
| ng-p3-3 | untestable: no gap to halve (0.023 < 0.10) | untestable stands | not scored |

- **The refusal.** om-p2-3 stopped when the API refused the 22nd call: a severity-3 story about explosives, in the SimpleToM set (request `req_011Cgih9NjqNtezArQLWd12p`). Nothing was reworded or retried. Its pre-mortem had named exactly this risk, and the auditor notes that 552 of the 1,147 stories were severity 3, so a pilot would have found it. Whether to re-bet on a lower-severity subset is Sean's call.
- **The pre-mortems** were scored by the auditor after it wrote down its own reason for each failure:
  - on the six failed bets that had one, three named the main reason and five named at least its kind;
  - three of those three named reasons were the kind anyone would guess, "the effect isn't there", or a refusal the pre-mortem itself had flagged;
  - five of all eight failures today were of that "effect isn't there" kind (`ledger/scores.md`).

  So far the pre-mortems are not clearly better than always saying "it'll be null".

## 3. The Brier trend, and its honest reading

The engine's Brier score after each scored result landed, in order (`ledger/bets.jsonl`, result times):

| after | time | engine odds → outcome | Brier, as reported | Brier, after audit |
|---|---|---|---|---|
| founding week's five bets | 09:18 | 15–30% → 2 hits, 3 misses | 0.256 (n = 5) | 0.256 |
| om-p2-1 | 14:49 | 60% → miss | 0.273 (6) | 0.273 |
| om-p2-2 | 15:17 | 55% → miss | 0.277 (7) | 0.277 |
| ng-p3-1 | 15:36 | 7% → miss | 0.243 (8) | 0.243 |
| om-p2-4 | 15:41 | 60% → "pass" | 0.234 (9) | removed: undetermined |
| ng-p3-5 | 15:43 | 42% → miss | 0.228 (10) | **0.236 (9)** |

The honest reading:
- **The trend is noise.** Every step is one bet's single outcome moving a mean of five to ten numbers. The score went up when the engine said 55–60% and missed, and down when it said 7% or 42% and missed. That is what a Brier score does. It is not learning.
- **The engine is level with a coin, and only that good because most bets fail and it mostly said low numbers.** Always saying the observed pass rate, 2 in 9, would have scored 0.173, clearly better than the engine's 0.236. To beat that, the odds have to rank bets, putting the hits above the misses. So far they do not: the two hits were given 25%, below several misses.
- **The audit made the score worse, which is the point.** As reported, the day ended at 0.228. After the audit removed a "pass" that was not shown, it ends at 0.236. If that bet is later settled as a hit the score is 0.228; as a miss, 0.248 (`ledger/brier.md`, Sensitivity). An unaudited ledger would have flattered the engine.
- **"Nature-graded 0.091 on 2" means nothing yet.** Both chip-graded bets were given low odds and missed, which scores well by construction. The question program 3 exists to answer (does the engine's calibration hold up when a referee shares none of its habits?) needs tens of chip-graded bets, not two.
- **Calibration needs at least 20 scored bets** with at least 4 hits and 4 misses (paper/the-engine.md, H1). There are 9, with 2 hits.

## 4. What the chip taught us about yesterday's gap

**Yesterday (3 November).** Program 1's Stage 1 circuit, nine qubits on `ibm_fez`, gave P(yes) = 0.502. IBM's own noise model of the chip predicted about 0.25. That is a gap of about 12 standard errors, and the reason program 3 exists.

**Today's three answers:**
1. **It was not our simulator set-up** (ng-p3-1, fail). Laying the circuit out in time, so waiting qubits can decay, moves the prediction by essentially nothing. The circuit lasts under 10 µs, against qubit lifetimes of 45–200 µs.
   - The auditor found the run never loaded that afternoon's T1/T2 values (a library returns a copy, so the assignment was lost), and that one variation's ZZ term was never applied.
   - With T1/T2 set properly, the verdict is unchanged.
   - Adopting this model as the program's "corrected simulator" is held until the bug is fixed.
2. **The archived errors fit random blur better than steady twists on two of three pairs** (ng-p3-5). The auditor found the contest partly decided by construction: the "steady twist" family cannot change a state's purity, and the chip's states had lost purity. A joint model finds steady-twist terms on every pair. So "the errors are blur, not steering" is contradicted. Both kinds are present.
3. **The gap did not come back** (ng-p3-2, ng-p3-3, untestable). On the same nine qubits, the chip gave 0.246 against a prediction of 0.269. Two other sets of nine qubits also agreed with the simulator (0.277 against 0.265, and 0.297 against 0.264). With no gap, the twirling and layout questions could not be asked.

**What it does not show.** Today's circuit was not yesterday's. Yesterday's had a barrier and ran as one 1,000-shot block; today's had none and ran in interleaved 100-shot pieces. So the comparison "0.502 then, 0.246 now" mixes the day with the circuit and the job layout, and "one unusual afternoon" is not established (audit `ng-p3-2-3.md`).

**What it does show, beyond the headline:**
- Even when the headline P(yes) agreed, five of the nine qubits were individually more than 4 standard errors off the simulator.
- One qubit's readout was ten to twenty times worse than IBM's calibration said.
- A forward-and-back "mirror" circuit returned all nine qubits correctly 2.2% of the time, against 13.6% predicted.

The device departs from its own description in ways a single summary number hides.

**The next chip test is therefore a true repeat:** yesterday's circuit, with its barrier, run the way it was run then, at least twice and hours apart. It costs a few seconds. 54 of the 420-second hard stop are used, and at least 120 s are held for exactly this kind of replication.

## 5. What the auditor reversed

Audit round 2 (`ledger/audits/SUMMARY-2.md`) covered every result committed today without an audit, and every result whose text changed after round 1. The headline rates:

| measure | value |
|---|---|
| audit files / results covered | 13 / 14 |
| claims checked / holes found / cuts required | 344 / 98 / 133 |
| results that regenerate from the archive | 13 of 13 |
| verdicts changed | **3 of 13** |
| labels kept, wording not | 2 of 13 |
| verdicts standing | 8 of 13 |
| round-1 cuts missed or misapplied in re-audited files | 0 of 34 |

**The three verdicts it changed:**
1. **om-p2-4: pass → undetermined.** The rule was "the interval for the difference in error includes zero", with no margin and no power check, although program 2's own map requires one for every self-versus-other null.
   - The test could only have detected a difference of about 0.084, nearly all of the comparison arm's whole error (0.097).
   - The self arm's error was in fact about half the other's.
   - The interval used is biased toward zero here; two standard corrections both favour the self arm.

   "Knows itself about as well as it knows Sam" is not shown. It was program 2's only pass.
2. **Program 1's experiment 5 re-issue: classical → mixed.** Yesterday a verdict was re-labelled "classical" on a subset chosen after the data, prompted by the first audit. The pre-registration pooled the two scale directions on purpose, as its own control for scale artefacts. The pre-registered verdict is still "tie". The auditor notes that the first audit's own advice caused this.
3. **The probe study, round 2: mixed → untestable**, until a fresh-seed rerun (DP2) reported. DP2 is verified on its rating side only, and one item, h191, still decides "not with the rating".

**Wording it cut where the verdict stood:**
- Opus's "a usable single belief": a one-bit "is it above 50?" predictor passes the same bar, so the test shows a shared verdict, not a graded credence.
- ng-p3-5's "blur, not steering".
- ng-p3-1's description of a model it did not actually run.
- om-p2-2's explanations of its own failure. The pooled score there is almost entirely the condition label: a predictor that knows only whether Noor saw the change gets 0.477 of its 0.50.

**The pattern.** In round 1 the faults were mostly numbers stated more strongly than the data. In round 2 the numbers held, and the faults moved into the nouns: a frozen rule applied correctly, then reported with a word the design cannot carry ("credence", "not steering", "knows itself as well"), or a non-detection rule called a pass. The auditor's recommendation follows: every future "one belief" or "self no better than other" test pre-registers a dumb baseline and a power check.

**Its limits.** Every audit today was same-family: the auditor and the author are both Claude Opus 5.5. No audit carried a planted error, because the plant procedure (`operators/plant.md`) was written this afternoon, after audit round 2 began. So the auditor's catch rate, the number that says how much "this result stands" is worth, does not exist yet. Round 3 should start with sealed plants.

## 6. What changes tomorrow

- **The cuts are applied**, under one deviation row in each program, and each results file now opens with its audited verdict.
  - **Program 2** (other-minds D5, `8bdbec4`): 33 of 33.
  - **Program 3** (nature-graded D5, `6bc5720`): 37 of 41 in the results files themselves; two more are corrections to earlier commit messages, which cannot be amended, so they are recorded in the D5 commit instead.
  - **Still open, for the owning sessions:**
    - program 3's cuts to its README and map;
    - a per-qubit table that needs new numbers from the data;
    - a note on one data file's uncommitted code;
    - program 2's few minor fixes the audit asked for outside its numbered cuts, including the freeze-time correction row.
- **Program 3** fixes `overwrite_calibration` and re-runs ng-p3-1 under a deviation row, before any prediction relies on the corrected simulator. Its first chip bet of wave 2 should be the true repeat above.
- **Program 2** needs Sean's call on re-betting P2-3 on low-severity stories. Every new self-versus-other null pre-registers an equivalence margin and a power check.
- **Sean** fills in the per-direction odds forms, so the human column of the ledger stops being empty.
- **The auditor** starts carrying plants, so its catch rate becomes a number.

---

*Sources:* `ledger/bets.jsonl`, `ledger/brier.md`, `ledger/scores.md`, `ledger/audits/` (copied from entangled-mind `audit2` 8091d01), nature-graded `results/` (6badd68, 280e180, 9e9ae5d), other-minds `results/`, `operators/hardware.md`, `operators/premortem.md`, `operators/plant.md`.

---

# Evening: 16:50 to 19:26

*Appended 2026-11-04 at about 19:45 America/Denver by the paper-evening session. It covers the commits from `f0fbe9c` (16:51) to `d02b645` (19:26). Every number below names its file and the commit at which it holds. No number comes from outside those files, and nothing here is a new claim. Where this section and a ledger file disagree, the ledger file is right.*

## In plain English

**Six bets were scored this evening.** Three came back as misses and three as passes.
- **Program 2's re-bet failed.** om-p2-3b re-ran the theory-of-mind test on lower-severity stories. Its 14-story refusal pilot ran clean, and so did the full run. But the effect went the wrong way: the model's own planted answer moved it *less* than another reader's.
- **Program 3's true repeat failed on its first run.** Putting the barrier back did not bring back 3 November's 0.50. The chip gave 0.311 with the barrier and 0.319 without.
- **Program 4's first round passed all three of its bets.** In program 4 the published literature is the referee. On 116 findings posted after the bettor model's knowledge cutoff, the bettor's Brier score was 0.163, where a coin scores 0.25. It also beat a publication-bias shortcut. The auditor let all three passes stand and cut seven sentences. The passes are unreplicated, and the item-writer and the bettor are the same model family.

**The engine's own score got slightly worse, and it is still no better than knowing the hit rate.** At 16:50 the engine's Brier score was 0.236 on 9 bets. Now it is **0.246 on 14** (`ledger/brier.md` at `8730692`). Always saying 50% scores 0.250. Always saying the observed hit rate, 5 in 14, would have scored 0.230. Fourteen bets cannot tell these apart.

**The three referees, as numbers, not as a finding.**
- Model-graded bets score 0.263 on 8.
- Chip-graded bets score 0.062 on 3, only because all three were given low odds (7%, 42% and 7%) and all three failed.
- Record-graded bets score 0.388 on 3, because the engine gave them 50%, 30% and 35% and all three passed.
- None of this says anything about the referees yet (`ledger/brier.md`, "By referee").

**What went wrong, stated as plainly as what went right.**
- **The lesson moved odds the wrong way.** The new lesson rule moved ss-b1's odds from 60% to 50%, toward the base rate. The bet then passed, so the move cost Brier 0.25 against 0.16 (`ledger/lessons.jsonl`, ls-ss-b1).
- **A pattern the lesson cited came back.** The ss-b1 lesson cited P9, a rule applied correctly and then reported with a word the design cannot carry. The audit found P9 again ("cannot have read", "confidence too low", "odds too pessimistic").
- **A design review missed something.** It asked for leave-one-item-out but not leave-one-field-out, and ss-b3's pass rests on one field.
- **Two rule violations.** `ledger/scores.md` lists ss-b2 and ss-b3 as violations because they carry no lesson line of their own.
- **The human column is still empty.** `ledger/human-odds.jsonl` has 0 lines.

## 1. Rules and structure (16:51 to 18:29)

- **Learn before you bet; review before the first call.** Both became mandatory from 17:00 (`f0fbe9c`, CONTEXT §3 rules 9–10). `ledger/scores.md` at `8730692` counts 6 pre-registrations since the rule. All 6 have a design-review verdict, all of them fix-first, and 4 carry a lesson line. ss-b4/ss-b5, pre-registered after that count, await their review.
- **Never ask Sean in a terminal** (`04a9cd2`, CONTEXT §3 rule 11). His odds come only from the cockpit's downloads into `ledger/human-odds.jsonl`. That file has no lines yet, so every bet tonight is marked "no human odds".
- **One repository.** All four programs were folded into `programs/` with their full histories at 17:12 (`32ca722`, `11de687`, `bf3c7a8`, `ebf7017`).
- **One mistake from the shared checkout.** ss-b1's pre-registration landed inside another session's commit, `ebd2c80` (settled-science D10). The rule now is `git commit -- <paths>` only (`e4da61c`).
- **Sean's budget ruling** (st-16, 18:26): he approved 10 QPU s for ng-p3-15. Budget rulings under the 420 s hard stop are now the engine's call (`9d82f8b`, renumbered in `38ee62d`).
- **`reproduce.py` at the repo root** rebuilds the ledger tables and the site data from archived files, with no keys (`6c4361d`).

## 2. Program 2: om-p2-3b, fail

- **Pre-registration.** `26ee5d2` (17:15). The engine's odds were 40%, lowered by its lesson from the map's 70%.
- **Design review and pilot.** The review said fix-first with 6 fixes, then confirmed them (`5b154bd`, `93ec998`). The refusal pilot made 182 of 182 calls with 0 refusals and cost $0.0084 (`95f0e77`).
- **The run.** 7,553 calls, no refusal and no stop, $0.3715 (`programs/other-minds/results/p2-3b-simpletom-lowsev.md` at `67244e7`).
- **Verdict: fail.**
  - The bar was a difference of at least +0.10.
  - The difference Δ was **−0.053 [−0.079, −0.029]**. The planted answer pulled behaviour less when it was labelled as the model's own (+0.060) than when it was credited to another reader (+0.114).
  - Scope: 581 stories of severity 1 and 2, on Haiku only. Severity-3 stories, 48% of the benchmark, are not covered.
- **The audit** (`ledger/audits/om-p2-3b.md`, `be920b7`).
  - The fail stands. It made 2 cuts, and neither touches the verdict.
  - The sealed plant pl-002, a miscount, was caught (`67244e7`).
  - The pre-mortem was scored `kind_only`: it named the kind of failure but not the reason.
  - None of the lesson's cited patterns recurred (`ledger/lessons.jsonl`, ls-om-p2-3b).

## 3. Program 3: ng-p3-15 run 1, fail; ng-p3-5c pre-registered

- **ng-p3-15** (`7f9cedf`, odds 7%) is the true repeat called for this morning. The run is job `dbltng9kbkrc73cod80g`. It billed 4.0 QPU s, so 58 s of the 420 s hard stop are now used (`programs/nature-graded/results/p3-15-repeat.md` at `e7f8c5c`).
- **Verdict on run 1: fail.**
  - With the barrier, one 1,000-shot block gave 0.311. Without it, 0.319. That is a difference of −0.008.
  - The bar was 0.40, with a gap of at least +0.10.
  - The pooled barrier effect lies inside ±0.05.
  - The control, 4 November's circuit, gave 0.274, within 0.05 of that day's 0.246.
  - So the barrier did not bring back 3 November's 0.502.
  - Shot grouping may matter a little (+0.030, 90% CI +0.006 to +0.054), which this job cannot pin down.
- **Not audited yet.** Run 2 is scheduled no earlier than 21:30:43 and had not reported when this section was written.
- **ng-p3-5c** (`930efe8`) re-analyses the archive for P3-5. It is unscored by design. Its design review said fix-first with 7 flaws (`8f20006`), and the fixes are not yet confirmed.

## 4. Program 4: the published-record referee, round 1 passes; round 2 pre-registered

**How round 1 was set up**, from `programs/settled-science/experiments/ss-b1.md` (`1f5c1bf`) and the protocol files:
- **The rules came first.** The three rules were fixed before any item was written (`64e12dd`, 16:54). The engine's odds were stated before any item was read (`4963270`): ss-b1 50% (first 60%), ss-b2 30%, ss-b3 35%.
- **The leakage check.** 213 calls cost $0.47. 184 items were frozen with SHA-256 (`4859d3b`).
- **The design review.** It said fix-first with 5 fixes. Those were applied as D12–D16 and confirmed go (`e3efeb5`, `954c035`, `38f2364`).
- **A setting changed after the go.** The bettor model cannot run with thinking off (D18). The change was re-reviewed: not go, because the edit had removed the refusal stop (`fcc0797`). That was fixed in D19 and then confirmed go (`dbc45ae`). The D20 scope sentence was fixed before the run (`9d4bcf4`).

**The result** (`230cbe4`), as audited (`ledger/audits/ss-b1.md`, `cdce1ba`; cuts applied in `a585a88`, D21):
- **ss-b1, pass, unreplicated.** On 116 post-cutoff findings the Brier was **0.163 [0.139, 0.190]**, and 76% were right.
- **ss-b2, pass, unreplicated.** It beat the publication-bias baseline (0.232) by **0.068 [0.036, 0.099]**.
- **ss-b3, pass, unreplicated.** The 68 pre-cutoff items scored 0.105. The difference from post-cutoff was −0.059 [−0.098, −0.019]. That fits memory, and it also fits the older items simply being easier. The design cannot separate the two.
- **Cost.** 490 calls, $2.02, 0 refusals.

**The negative parts, in the results file's own words:**
- **Model psychology was the weakest field.** It scored 0.235 [0.181, 0.293], so it is not shown to beat a coin.
- **ss-b3 rests on one field.** Without model psychology its upper bound is +0.019, so it would be null. This check was not pre-registered.
- **The confidence reading is exploratory.** The audit cut "too low" to an exploratory reading. Its 60–70% calls were right only 57% of the time.
- **The same model family wrote and bet.** The item-writer and the bettor are both Opus 5.5. The auditor names a non-Claude item-writer as the cheapest test that could overturn ss-b1.
- **The referee is the published claim.** It scores what got published, not what is true.

**The audit itself:**
- 34 claims checked, 7 holes, 7 cuts. Every table regenerated byte for byte.
- The plant pl-003 was drawn clean, so there was nothing to catch.
- The pre-mortem was scored `not_failed`.
- The auditor printed the pre-mortem before finishing its checklist, and discloses that this broke the audit's order.

**Round 2** (ss-b4 and ss-b5) is pre-registered and seeded (`29e8769`, `e8f921e`). It has not run, and its design review has not yet been written.
- **The writer is a template.** It is a fixed rule, not a model (`5ce075d`). It answers the auditor's same-family objection.
- **Too few items on the first page.** It gave 57 items, below the minimum of 60 (D22, `4cdd8e4`). The pool was extended once, by a rule fixed before the second fetch.
- **The leakage check dropped most of the pool.** It dropped 146 of 243 template items, leaving 97 frozen and 92 to draw.
- **ss-b4 can be passed by a dumb rule.** The dry run before the pre-registration showed that always picking the "higher / more / better" wording passes ss-b4 (Brier 0.171). ss-b4 therefore cannot show judgment, and ss-b5, which tests against that rule, is named the informative test.
- **The odds were not revised:** 70% and 35%, stated in `8e87c59` before any item existed.

## 5. The ledger at 19:26

From `ledger/brier.md` and `ledger/scores.md` at `8730692`, and `ledger/lessons.jsonl` at `d02b645`:

| measure | at 16:50 (§3 above, CONTEXT §4) | at 19:26 |
|---|---|---|
| scored bets | 9 | **14** |
| engine Brier | 0.236 | **0.246** |
| always the observed hit rate (hindsight) | 0.173 | 0.230 |
| expected / observed hits | — | 4.41 / 5 |
| audits revealed with a sealed plant line | 1 (pl-001, forced) | 3 (2 planted, both caught; 1 clean) |
| catch rate | 1/1 | **2/2, Wilson [0.34, 1.00]**; H2 needs at least 10 plants |
| lazy "the effect isn't there" baseline for failures | 5 of 8 | 6 of 10 |
| engine pre-mortems naming the main reason | 3 of 6 | 3 of 7 |
| lessons: paired Brier before → after | — | 0.325 → 0.205, on 2 bets |
| design reviews | — | 6 fix-first, 0 go, 0 redesign; 1 missed a flaw the later audit found |
| bets with Sean's odds | 0 | 0 |

How to read it:
- **Calibration is still untestable.** H1 needs at least 20 scored bets, with at least 4 hits and 4 misses. There are 14, with 5 hits.
- **The lesson rows are two bets, not a finding.** They pull different ways: on ss-b1 the lesson's odds move hurt (0.25 against 0.16).
- **The by-referee Briers are too few to compare** (`ledger/brier.md`).

## 6. This morning's list, against what happened

| planned this morning (§6 above) | what happened this evening |
|---|---|
| The auditor starts carrying plants | Done. pl-002 was planted and caught; pl-003 was drawn clean. |
| Program 2 re-bets P2-3 on low-severity stories | Done. Sean approved it (st-12); it ran without a refusal and **failed**. |
| Program 3's first wave-2 chip bet is the true repeat | Run 1 done, **fail**, unaudited; run 2 not before 21:30. |
| Program 3 fixes `overwrite_calibration` before reuse | No separate fix or audit of the corrected simulator is in this window's commits. ng-p3-5c's lesson says it loads T1/T2 with an assertion (`ledger/lessons.jsonl`, ls-ng-p3-5c); it has not run. |
| Sean fills in the odds forms | Not done. `ledger/human-odds.jsonl` is empty, and under rule 11 no session asks him for them. |

*Sources for this section:* the commits named above; `ledger/brier.md`, `ledger/scores.md`, `ledger/bets.jsonl` (`8730692`); `ledger/lessons.jsonl` (`d02b645`); `ledger/audits/ss-b1.md` (`8730692`), `ledger/audits/om-p2-3b.md` (`67244e7`); `programs/settled-science/results/ss-b1-results.md` (`a585a88`), `programs/settled-science/experiments/ss-b4.md` (`e8f921e`); `programs/other-minds/results/p2-3b-simpletom-lowsev.md` (`67244e7`); `programs/nature-graded/results/p3-15-repeat.md` (`e7f8c5c`); `CONTEXT.md` §3–4.

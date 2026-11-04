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

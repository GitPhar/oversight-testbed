---
bet: em-gm2q2
program: entangled-mind
prereg_commit: 1e0c9c1
reviewer_session: fresh design-review subagent in the p1-wave3 worktree (no chat or transcript read); seed commit 74b63b1 read as the frozen text plus its seed line
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 10:33 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: holds, D6: holds, D7: holds, D8: holds, D9: holds, D10: flaw, D11: flaw, D12: flaw}
prior_work_search: WebSearch "question order effects self-administered vs telephone survey respondents see all questions at once Bishop Hippler Schwarz Strack 1988" (2026-11-05 10:30; survey-methodology terms for "every question visible at once vs answered one at a time")
papers_opened: 6
flaws: 4
pilot_usd: 0.07
verdict: fix-first
confirmed_at: 2026-11-05 10:50
---

# Design review of em-gm2q2

## In plain English

The test asks a fair question and its rule is sound. A world with no questions-only order effect never passes. A world where a model rates the first- or last-listed statement instead of the question does not pass. A world where the effect sits on one item, or on different items from the turn-by-turn effect, does not pass either. A world where the questions-only effect matches the turn-by-turn one passes on Sonnet almost always and on Opus about 55–60% of the time. The run as built still has four problems, and all of them can be fixed before data:
- **It would run out of money halfway.** Its cost estimates are too low: for Opus's chains it took an average that includes 100 one-turn conversations, and Opus's questions-only request was never measured. At the costs this review measured, the code stops after the first batch, having spent $1.81, before any turn-by-turn chain is finished. Both models would then be untestable.
- **Half of Opus's dry-run world is a misreading.** The "second batch with a 34-point order effect" in em-dm4's Opus archive is not a batch at all. Those 80 conversations were abandoned after their first turn, and the dry run read the rating of the first-listed statement as the final answer. Several sentences rest on that world: the §6 reason for changing the wrong-target reference, the §8 "world B" column, the lesson's "Opus's archive mixes two batches", and br-011's reason.
- **A crash or resume loses track of money.** A batch is not logged until it ends, and a resumed run overwrites the record of chains that were paid for but not finished.
- **The prior-work row misses a direct prediction from survey research.** Studies of human respondents found that question-order effects seen over the telephone, one question at a time, mostly disappear when the respondent can see every question at once. That predicts this bet's ratio part fails. One cited paper is also described loosely.

## Checks

Everything ran from the scratch folder `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed-p1-wave3/64dc560a-a9b5-47cc-a2a7-ed6060948ca4/scratchpad/review/`. Nothing under `programs/` was written. The dry run was called through an import that writes to scratch, so the committed `results/gm2q2-dry-run.json` was not touched. Every file the run and the dry run read is unchanged since `1e0c9c1`:

```
git diff --quiet 1e0c9c1 -- gm2q_questions_only.py gm2-planted-values.json gm2b-planted-values.json pool-run-3.json \
  mm-gm2-opus-conversations.json gm2b-conversations.json gm2q-questions-only.json gm2q2-dry-run.json   # passes
```

The only change to `gm2q2_opus_sonnet30.py` since the pre-registration is `SEED_RECORDED` (74b63b1). `--selftest` printed "all checks hold" (the equal world passes; the one-item world passes on all items and fails by leave-one-out on q0; the one-item-jump and first/last wrong-target worlds fail on the cleaned-cell check). `--print-prompts` ran clean.

**D1. holds** (`d1.py`). I built synthetic caches with known answers, ran them through the module's `analyse_model` and `bet_verdict` with the beacon seed mod 2^63, and got exactly one verdict each time:

| case | Opus (10 items) | Sonnet (30 items) | bet |
|---|---|---|---|
| strong effect in both arms, both models | pass | pass | pass |
| Sonnet qonly null | pass | fail (qonly gate) | mixed |
| both qonly null | fail (qonly gate) | fail (qonly gate) | fail |
| Opus shown null, Sonnet qonly null | untestable (shown gate) | fail | untestable |
| Opus shown null, Sonnet passes | untestable | pass | mixed |
| Opus qonly 0.3× shown | fail (ratio lower bound) | pass | mixed |

`final_label` and `bet_verdict` match §5 word for word. One wrinkle, not a flaw: "mixed" includes the case where one model passes and the other is untestable, as §5 says. The mixed sentence then names "shown gate" as the other model's first failing part.

**D2. holds.** For every item and model, the four qonly messages differ and the four chains differ. The qonly list order equals the chain's statement order (`LATIN`), which I asserted for all 40 items. The two item sets do not overlap. The parameters the run will send are the ones §2 states:
- Opus: `max_tokens` 1000, `output_config {effort: "low", format: json_schema}`, no `thinking` field. That matches Opus 5.5, which cannot disable thinking.
- Sonnet: `max_tokens` 1000, `thinking {type: "between_tools"}`, the same schema.
- Repeats {Opus 6, Sonnet 5}; cap 4.00; reserve 0.10.

The flag takes the first-listed statement from `LATIN[j][0]` and the last-listed from `fourth()`. The selftest's `wrong_target(90, 95, 10, 20)` and `wrong_target(90, 10, 95, 20)` show that each end fires.

**D3. holds.** Each control rejects a wrong set-up built to fool it:
- The shown gate is the yardstick. A world with no shown effect returns untestable (D1, rows 4–5).
- The qonly gate rejects the null world: 0.00 pass on all arms in the dry run, and 60 of 60 non-pass in my re-simulation.
- The cleaned gate and cell check reject a no-effect world padded with first- or last-line answers. At 20%, the full-set pass rate is 0/60 on Opus A and 0/60 on Sonnet. At 30%, it is 0/60 on Sonnet and 2/60 on Opus A, and leave-one-out fails both of those (`parts.py`).
- Leave-one-out rejects a world where both arms' effect sits on one item (selftest: `loo_breakers == ["q0"]`).

**D4. holds / not applicable.** No two model families or fitted rivals compete. The one rival the design names, that one message instead of five turns changes more than the presence of answers, is stated in §6 as a bundle the design cannot split, and the pass sentence does not claim to split it.

**D5. holds.** The dumb predictors and what they score:

| dumb predictor | result |
|---|---|
| constant / no order effect (null) | 0.00 pass |
| first- or last-line responder at 20–30% with no real effect | 0 of 60 after leave-one-out, both models |
| one item jumps, half effect elsewhere | 0.00 on every arm |
| the parent's actual pattern: effect equal in size but on shuffled items | 0.00 Opus A, 0.01 Sonnet |

This is not a "no difference" rule, so no equivalence margin is needed.

**D6. holds, after a pilot.** The pre-mortem is of kind `design`, but Opus's questions-only request was unmeasured in cost, parse rate and token use, so I piloted it.
- **Calls:** 12 direct calls, `claude-opus-5-5`, the run's exact `params()` (effort low, json_schema, max_tokens 1000). Items h111, h197 and h293 from gm2b's 30 further items, which are excluded from the Opus arm, in orders O1–O4.
- **Script:** `pilot.py`, with a running total checked before each call against a worst case of $0.0216. Stop on refusal, no retries.
- **Results:** 12 of 12 parsed; 0 `max_tokens` stops (largest output 248 of 1000 tokens); 0 refusals. Eleven of 12 had a thinking block; one answered with 10 output tokens.
- **Cost:** $0.0703 at list price, or $0.00293 per request at the batch rate against the pre-registration's estimate of $0.0015.
- **Per-call list cost:** $0.006872, $0.007292, $0.006852, $0.006932, $0.006564, $0.005104, $0.007144, $0.006524, $0.0052, $0.0022, $0.0047, $0.00494.
- These ratings are not test data and were written only to the scratch file `pilot-rows.json`.

Sonnet's 30 items cannot be piloted on Sonnet, since they are its test items. They are trivia and textbook physics or chemistry, and Haiku ran all of them in gm2b without a refusal. Stop-on-refusal is in code. The cost finding goes to D10.

**D7. holds, with one unlisted difference.** §6 lists every difference from em-gm2q. It lists the four ways qonly differs from shown (no answers; one message instead of five turns; numbered statements; the opening wording) and writes the claim as one about that bundle. One more difference is not listed. Every qonly answer is collected in round 1's batch, while every shown final comes from round 5's batch, hours later. The same model and parameters are used throughout, and em-dm4's "disagreeing batches" turned out to be an artefact (D11), so I see no evidence that the timing matters. I record it as a note for §6, not a flaw.

**D8. holds, with a note.** The four verdict sentences use only nouns the design carries. After the em-gm2q audit's D8 miss, they no longer say "the gm2 order effect", and the pass sentence says outright that it does not show the same effect as turn by turn. Note: the leave-one-out fail sentence, "the effect depended on single items (<ids>)", would misdescribe a leave-one-out fail caused by the *shown* gate, where the yardstick rather than the questions-only effect depends on one item. In my re-simulation this never happened: 0 of 600 Opus-A runs, over five worlds and both flag references. `label_on` does not record which part broke inside each leave-one-out set. I recommend recording it and adding the clause "(the turn-by-turn reference, not the questions-only effect)" when it is the shown gate. This is not counted as a flaw.

**D9. holds.** Leave-one-item-out is inside the pass rule. Every part is recomputed on the remaining items, including the cleaned-cell check, which fixes the em-gm2q audit's claim-19 code hole. What one flipped item does is pre-registered: a fail, naming the breakers.

**D10. flaw (two flaws).** The machinery that holds:
- the cap is checked in code before the first batch and before every round;
- stop-on-refusal is in code, with a record file that blocks later runs;
- one scale direction is used ("0 = certainly false, 100 = certainly true" in both openings);
- the beacon seed recomputes: `ledger/seed.py <randomness> em-gm2q2 --purpose analysis` gives 8982550231960562870, matching `SEED_RECORDED`, with pulse 1592505 at 17:21:00Z after the commit at 17:20:43Z. I did not re-fetch the pulse.
- The lesson's text in §0 equals `ls-em-gm2q2` in the inbox. Its read block matches `ledger/brier.md` at `1e0c9c1`: Brier 0.158, 7/31, newest audit ng-p3-18.

The two flaws:

- **Flaw 1: the cost estimates are wrong, and at measured costs the run stops before round 2.**
  - **Opus shown:** `EST[(O, "shown")] = 0.00112` comes from "$0.0056 per 5-call chain". That is the mean over all 200 em-dm4 Opus shown conversations, but 100 of them are one-turn abandoned stubs (mean $0.00205). The 80 complete O-chains cost $0.009173 each at the batch rate.
  - **Opus qonly:** the pilot measured $0.00293 per request at the batch rate, against the estimate of $0.0015.
  - **Sonnet:** the shown estimate ($0.00263 per complete chain) and the qonly estimate (half of em-gm2q's direct $0.00117) are right.
  - **Measured total:** 240 × 0.00293 + 240 × 0.009173 + 600 × 0.000583 + 600 × 0.002628 = **$4.83**, against the cap of $4.00.
  - **Fake-client run:** I ran `run()` itself with a fake Batches client that bills these per-request costs (`fake_run.py`). The whole-run check uses the low estimates ($3.63), so the run starts. It then stops before round 2: "cap $4.0: spent $1.809, next batch $0.756 x1.1, remaining $3.023". All 240 + 600 qonly conversations are done and **0 shown chains** are. Both models would be untestable for $1.81.
  - At the pre-registration's estimates the same fake run completes for $3.63, which is why the dry run did not see this.
  - With the estimates corrected and the cap at $5.50, it completes at $4.83 (`fake_run_cap.py`). At $5.00 it stops before round 5, having spent $4.08 with 0 shown chains.
- **Flaw 2: a crash or resume loses track of billed money, and the cache is not keyed by content.**
  - **Batch not logged until it ends.** The batch ID goes into `BATCHLOG` only after `processing_status == "ended"`. If `batches.retrieve` raises while polling (network, sleep, Ctrl-C; polling can last hours), a billed batch is never recorded, and a resume pays for it again.
  - **Unfinished cost overwritten on resume.** `save()` *overwrites* `_unfinished` with the current run's unfinished chains, and the in-loop `spent` leaves `_unfinished` out. So a resumed run drops the earlier run's billed-but-unfinished cost from both the record and the cap.
  - **Simulation** (`fake_resume55.py`, cap $5.50, estimate costs): I crashed the run while polling round 3, then resumed. Billed in total: **$5.39**. Recorded by `spent_of(cache)`: **$3.63**. $1.75 is missing. A second crash would pass the cap unseen.
  - At the $4.00 cap the resume happens to refuse to start (`fake_resume.py`), but only because the totals are large.
  - **Cache key:** the cache is keyed by `model|item|order|cond|rep`, not by a hash of the request. A resume after any prompt or parameter change would mix two designs without noticing. D10 asks for caching by content hash.

**D11. flaw (the floor still holds).** The bet can both pass and fail at this n, but half of the Opus world it was simulated on is not real data.
- **What world B is.** In `results/mm-gm2-opus-conversations.json`, repeats 2–3 of every Opus cell have one turn and carry `"abandoned": "DM4 fallback after wave 1: projected cost over cap"`. Their last turn is `kind: "S"`, the rating of the first-listed statement. In all 80 shown O-chains, `claim` equals `first(claims, order)`.
- **How the dry run reads it.** `world(O, "B")` reads `turns[-1]["rating"]` from those stubs as the final rating. So "world B, order effect 34.3 points, answers between about 3 and 88 by order" is just the four orders starting with four different statements.
- **The numbers.** Complete chains only (repeats 0–1): OE 4.4, the figure em-dm4 published. Stubs only: OE 34.3. `archived_secondaries()` mixes them and would report 11.5 as "archived OE (em-dm4 Opus shown, R = 4)".
- **What the real world says.** On world A, the real half, the measured Opus shown effect sits on two items (h279 and h238; order-deviation SD 8.7 and 8.2, all others ≤ 2.2), with within-order SD 3.5. Re-running the committed dry run into scratch (`dry.py`) gives JSON identical to `results/gm2q2-dry-run.json`. On world A the bet passes at 0.62 in the equal world and 0.41 at 0.75. It fails at 1.00 in the null world and ≥ 0.99 in the shuffled-items and one-item worlds. So D11's floor is met without world B.
- **What has to be removed.** The world-B column and the "bet (B × Sonnet)" column in §8, the §8 sentence on world B's 20% share, the §6 sentence explaining why the flag's reference changed, the lesson's "Opus's archive mixes two batches" (P15) and br-011's reason all rest on the misreading.
- **The flag reference.** I ran the same Opus-A worlds paired, with em-gm2q's item-mean reference instead of the same-order reference (`parts.py item-mean` against `same-order`). The labels are the same in the null, 0.75 and equal worlds (pass 28/60 and 32/60 under both). In the null world with 20% first- or last-line answers they are also the same; with 30%, 2/60 against 1/60 pass the full set and fail by leave-one-out. On Sonnet's world, the same-order reference passes the equal world 60/60 against 55/60 for item-mean, and neither reference lets a no-effect world with 20% or 30% first- or last-line answers pass (0/60 each). So on real data the change does not help Opus pass, helps Sonnet a little, and does not weaken the check. It can stay as frozen, but its stated reason has to go.

**D12. flaw.**
- **(a) holds.** The §0 row and the map's `prior_work_line` predict a pass of the qonly gate and say "unknown" for the ratio and leave-one-out parts, with citations.
- **(b) partly holds.** I opened the cited papers:
  - Chen, Chi, Wang and Zhou 2024 (arXiv:2402.08939, ICML): premise order changes deductive-reasoning accuracy, with drops over 30%; the models are unnamed in the abstract. Cited correctly.
  - Guan, Roosta, Passban and Rezagholizadeh 2025 (arXiv:2502.04134): shuffled inputs lower accuracy for API-accessed models on paraphrasing, relevance and multiple-choice tasks. Cited correctly.
  - Hämäläinen 2025 (arXiv:2504.20444) is described loosely. It varies the order of *traits within a candidate's description* (Asch's primacy design), not a list's order. In the one-prompt setup "Claude refused to make a choice". In the separate setup, Claude most often rated both candidates equally, favouring the negative-first candidate when it did not. "List order shifts candidate ratings, model-dependently" overstates it for Claude, the family under test.
  - The map line also carries gm2-f1's papers, which I opened. Temkit 2026 (arXiv:2605.22714, AMEL) finds earlier-turn polarity biases later judgments across 12 models, including Haiku to Opus. Kang 2026 (arXiv:2607.17219) is a QQ-equality audit on one unnamed open-weight model. Huang et al. 2026 (arXiv:2602.24287, COLM) find that dropping assistant-side history often does not hurt. None of them predicts the questions-only ratio. They are cited only for the parent direction.
- **(c) holds.** The in-house prior, em-gm2q (Sonnet passes on 10 items, one item carrying 82%), is named, and the 6% odds are argued against it.
- **(d) flaw.** My one search, in survey-methodology words, found a direct human prediction for the part the row calls unpredicted. Bishop, Hippler, Schwarz and Strack (1988, AAPOR; ZUMA working paper 1987, "A comparison of response effects in self-administered and telephone surveys") and Schwarz and Hippler's follow-ups on administration mode report that question-order effects found under telephone interviews, answered strictly in sequence, were not found when the questionnaire was self-administered and respondents could see every question at once. The summary of that work reads "question order effects were obtained under telephone interview conditions but not under self-administered conditions".
  - This is the human analogue of qonly against shown, and it predicts **R below the bar, a fail on the ratio part**.
  - The row's "No paper found compares a one-message order effect with a turn-by-turn chain ... So parts (3)–(5) ... are unpredicted" is therefore wrong outside LLMs.
  - The 6% odds are already on that side, so nothing needs to move. But the row has to cite it and say what the bet adds: LLMs, graded credences, and em-gm2q's Sonnet ratio of 1.88, which went the other way.
  - I could not open the full texts (SSOAR blocked the fetch). The finding is taken from the search results' abstracts and summaries. The author should open one before citing it.

## Required fixes

Each needs a DEVIATIONS.md row dated before any call and naming this review. None lowers the bar.

1. **Budget (D10, flaw 1).**
   - In `gm2q2_opus_sonnet30.py`, set `EST[(O, "shown")] = 0.009173 / 5` (em-dm4's 80 complete O-chains, not the 200-conversation mean) and `EST[(O, "qonly")] = 0.00293` (this review's pilot).
   - Then either raise `CAP` to **5.50** under a revised budget ruling (br-011 amended or a new br row; still under the $10 engine's-call line), or cut the design and re-run the dry run, keeping both versions.
   - In §3, replace "Opus $0.0056 ... per 5-request chain", "Opus qonly unmeasured, set at $0.0015" and "Total about $3.6" with the measured figures and "about $4.8".
   - Without this change the whole-run check refuses nothing and the run stops after round 1 with no turn-by-turn chains.
2. **Resume accounting (D10, flaw 2).**
   - In `run()`, append `{"round", "batch", "n", "custom_id→key map"}` to `BATCHLOG` and `save()` immediately after `batches.create`, before polling.
   - At start-up, for any logged batch without a recorded end, fetch its results (or count its billed cost) before submitting anything new.
   - Make `_unfinished` cumulative across runs (add the earlier value, keyed by run), and include it in the in-loop `spent`.
   - Store `sha256(json.dumps(params, sort_keys=True))` of each conversation's first request in its cache record, and refuse to resume a key whose hash differs.
3. **World B (D11).**
   - In `world()` and `archived_secondaries()`, use only complete conversations: skip any record with `"abandoned"` in it or `turns[-1]["kind"] != "M"`.
   - Delete the "opus B" arm and the "bet (opus B)" rows from the dry run, re-run `--dry-run`, and commit the new `results/gm2q2-dry-run.json`.
   - Rewrite §8's Opus bullet to: "Opus, from em-dm4's 80 complete Opus shown chains (repeats 0–1; repeats 2–3 were abandoned after turn 1 and are not used)". Drop the Opus B and B × Sonnet columns and the sentence "In Opus world B a 20% share ...".
   - In §6, replace the paragraph "Why the flag's reference changed" with: "The flag's reference is the same order's shown final, so that an answer agreeing with turn by turn in that order is never flagged. On the measured Opus world it gives the same labels as em-gm2q's item-mean reference (design review em-gm2q2, D11)." Keep the sentence on the cost of the change (the shuffled-items world).
   - Record a lesson revision under operators/learn.md, keeping both versions. Replace "and Opus's archive mixes two batches" with "and half of Opus's archive is abandoned one-turn chains", and replace "builds Opus's dry run per batch" with "builds Opus's dry run on complete chains only". Odds unchanged.
   - Correct br-011's reason, which says "em-dm4's archived Opus cells mix two disagreeing batches", in the ruling's amendment.
4. **Prior work (D12).** In §0's prior-work row and the map's `prior_work_line` for gm2q-f3:
   - Add: "In human surveys, question-order effects found in telephone interviews (questions answered one at a time) were absent when respondents could see the whole self-administered questionnaire (Bishop, Hippler, Schwarz and Strack 1988; Schwarz and Hippler on administration mode). That predicts the ratio part fails. em-gm2q's Sonnet ratio (1.88) went the other way, and this bet adds Opus and 30 new items."
   - Replace "found list order shifts candidate ratings, model-dependently" with "found that the order of a candidate's traits shifted ChatGPT's choices, while Claude refused to choose in one prompt and mostly rated equally when the candidates were shown apart".
   - Change "parts (3)–(5) ... are unpredicted (predicts: unknown)" to "the ratio part is predicted to fail by the human survey-mode literature; leave-one-item-out is unpredicted". Both odds stay as they are; the 6% already sits on the side that literature predicts.

Notes, not counted as flaws:
- Record in §6 that qonly answers come from round 1's batch and shown finals from round 5's (D7).
- Have `label_on` record the failing part inside each leave-one-out set, and make the leave-one-out fail sentence say when the turn-by-turn reference is what broke (D8).

## Confirmation (2026-11-05 10:50 America/Denver; fixes at 089eebd, DEVIATIONS.md D82)

**Verdict: go.** All four flaws are fixed, and no fix lowers the bar: §5's pass rule is unchanged. I re-ran every check from scratch against the committed code, with no paid calls. The worktree's code and dry-run file equal 089eebd.

1. **Budget (F1): fixed, by a different route from the one I suggested.** The author cut Opus to 4 repeats instead of raising the cap to $5.50.
   - Committed values: `EST[(O,"qonly")] = 0.00293`, `EST[(O,"shown")] = 0.009173/5`, `REPS[O] = 4`, `CAP = 4.25` (br-011 amended).
   - **Fake run at measured costs:** completes for $3.864, with all 1,520 conversations done (160 + 160 Opus, 600 + 600 Sonnet). At the committed estimates it completes for $3.865.
   - **Per-turn cost shapes from the archive:** Opus's first turn costs about 1.12× its chain mean (em-dm4's stubs) and its 6th-turn increment is small; Sonnet's per-turn cost rises (its 6-turn MF chains cost $0.00056 more than its 5-turn chains). With those shapes the run also completes for $3.863.
   - **Residual risk, not blocking.** The margin under the cap is $0.39. An unlikely shape, with the turn-2 cost at 1.4× the mean or costs falling steeply from turn 1, makes the per-round projection stop the run before round 2 or 4 with no chains finished.
   - Cutting Opus from 6 to 4 repeats does not lower the bar. The re-run dry run gives Opus 0.62 in the equal world, the same as before the cut.
2. **Crash and resume (F2): fixed.** In `fake_resume2.py`, the fake server keeps every batch across runs.
   - **One crash** while polling round 3, then a resume: $2.647 billed and $2.647 recorded. The resume then refuses to start, because restarting the lost chains no longer fits the cap. That follows from the author's choice to restart lost chains rather than reuse their results.
   - **Two crashes** (polling rounds 2 and 4): billed and recorded agree after each run ($2.038).
   - **Request hash:** all 1,520 cached records carry `req_sha256`. Resuming after changing Sonnet's `max_tokens` exits with "built from different requests; not resumed".
3. **World B (F3): fixed.**
   - `world()` and `archived_secondaries()` now read complete chains only. The archived Opus order effect is 4.44, em-dm4's published 4.4. Opus within-order SD is 3.49.
   - The re-run dry run (`dry.py`, into scratch) matches the committed `results/gm2q2-dry-run.json` exactly, in every Opus and Sonnet world and in the bet rows.
   - At the fixed design the bet passes with probability 0.61 in the equal world and 0.37 at 0.75. It is 0.00 in the null, shuffled-items, one-item and redacted worlds. So D11 holds without world B.
   - D82 withdraws the §6 and §8 world-B sentences and the stated reason for the flag-reference change. The lesson revision and the odds change (0.06 to 0.07) are both kept, before data.
4. **Prior work (F4): fixed.**
   - The map's `prior_work_line` and the bet row now cite Schwarz, Bishop, Hippler and Strack 1989. I confirmed it exists: ZUMA-Arbeitsbericht 1989/01, "Psychological sources of response effects in self-administered and telephone surveys". Its abstract reports order effects by telephone and none on self-administered forms.
   - The rows now predict "mixed": the gate passes and the ratio fails.
   - Hämäläinen 2025 is restated correctly.

Notes, not blocking:
- br-011's `what` field still says "R = 6 ... cap $4.00 ... planned about $3.6". Its `approved_usd` (4.25), `reason` and `amended` fields are correct; the stale field should be tidied.
- The pre-registration file is not edited. D82 supersedes the parts it names, as design-review.md allows.
- The leave-one-out note from my review (D8) is taken: `loo_break_parts` is recorded and the fail sentence names the part.

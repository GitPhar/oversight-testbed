---
bet: em-gm2q
program: entangled-mind
prereg_commit: 2f30696
reviewer_session: fresh design-review subagent (no chat or transcript read), seed commit 1ba7f8c read as the frozen text
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 06:53 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: flaw, D6: holds, D7: flaw, D8: flaw, D9: holds, D10: flaw, D11: flaw}
flaws: 5
pilot_usd: 0.00
verdict: fix-first
confirmed_at: 2026-11-05 07:13
---

# Design review of em-gm2q

## In plain English

As built, the test mostly asks the right question. The four questions-only messages differ only in the order of the four statements, and the turn-by-turn chains are message-for-message identical to gm2's. A world with no order effect cannot pass, and the budget and seed are right.

It has five problems, all fixable before data without lowering the bar:
- **The wrong line can pass for an order effect.** A model that sometimes rates the last-listed statement instead of the question would pass. Its final number would follow whichever statement came fourth, so the rule cannot tell that apart from a real order effect.
- **The fail sentence claims too much.** It says "the gm2 pass was the placeholder". But the test compares questions-only with the *shown* chain, not with the redacted one. Redacted is re-run only on Haiku and is not required to replicate. On Sonnet, a questions-only effect just as large as turn-by-turn, but sitting on different items, fails 96% of the time.
- **The dry run is too optimistic.** It treats noisy archive means as true, and it never tries a world where the effect sits on different items.
- **The refusal stop leaks.** Conversations already running keep making calls after a refusal, and a re-run ignores an existing refusal record.

## Checks

Everything was run from the scratch folder `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/7db7e173-0d10-4755-94b1-f97b0684254c/scratchpad/review/` with `/Users/seanpharris/entangled-mind/.venv/bin/python`. No API call was made and nothing was written under `programs/`.

`git diff --quiet 2f30696 -- gm2q_questions_only.py exp5_run.py gm2_self_conditioning.py gm2-planted-values.json ../results/pool-run-3.json ../results/gm2-conversations.json ../results/mm-gm2-sonnet-conversations.json` passes: the working tree equals the pre-registration commit for every file the run reads. `--selftest`: "all checks hold". `--print-prompts`: the asserts pass and it prints all four qonly messages.

**D1. holds** (`verdicts.py`). I built synthetic caches with known answers and fed them to the module's own `analyse_model` and `bet_verdict`, with the beacon seed mod 2^63. Each case returns exactly one verdict:

| case | Haiku | Sonnet | bet |
|---|---|---|---|
| strong effect in both arms, both models | pass | pass | pass |
| Sonnet qonly null | pass | fail | mixed |
| qonly null or weak | fail | fail | fail |
| Haiku shown null | untestable | fail | untestable |
| Sonnet 15% missing | fail | untestable | untestable |

`selftest` covers the 1e-9 boundaries.

Note (not counted; fold it into the fix row): `analyse_model` also returns "untestable" when any single cell has fewer than 2 ratings, even with ≥ 90% usable overall. One qonly cell at 1/10 with 97.8% usable gives "untestable". §5 does not list that route. Either add it to §5 or drop it.

**D2. holds** (`stub.py`, stubbed client).
- I captured the messages from gm2's own `gm2_self_conditioning.converse` (with `structured` stubbed) and from gm2q's `converse`. The two lists are **identical in 80/80** cases (10 items × O1–O4 × shown and redacted). Shown keeps the model's reply; redacted puts `[rating recorded]` in every assistant turn. Haiku is sent `max_tokens` 200 and thinking disabled, as in gm2.
- Within each item, the four qonly messages share one opening and the same five lines. Only lines 1–4 are permuted, and they follow the shown chain's order exactly in all 40 item × order cases. Line 5 is always the main question.
- The Sonnet parameters sent are thinking `{"type": "between_tools"}`, `max_tokens` 1000 and the `{"rating": integer}` schema. This matches `mm_common.OFF[S]` and `mm_gm2.run`'s `max_tokens=1000` in em-dm4. em-dm4 went through the Batch API; this run uses direct calls. That only matters for the archive secondaries, because both arms here are direct and run on the same day.
- Small text slips (no fix needed beyond the row): §2 says the opening differs "in its second and third sentences", but it is the third and fourth ("The question is: …" is the second). The module docstring says D62; the row is D64.

**D3. holds.**
- With a no-order-effect shown arm, the shown gate makes the model untestable (D1 table).
- 15% missing triggers the 90% rule.
- The qonly gate rejects the no-effect world: 0/200 passes per model.
- At half the effect, the bet fails 83–95% per model (`sim.py`).

**D4. holds (no rival families).** The ratio's numerator and denominator use the same estimator, items, R and clipping. Neither arm is built to win.

**D5. flaw: a wrong-target responder passes.**
- The qonly message lists five lines, each beginning "How likely is it…", and asks for one rating. The only schema field is `rating`.
- I built a world with no order effect on the judgment, but where the qonly mean is pulled a fraction f toward the archived rating of whichever statement sits fourth. That is the mean pattern of a model that rates line 4 instead of line 5 in a share f of conversations.
- The fourth statement's rating varies by about 31–33 points across orders (s4 deviation SD: Haiku 32.6, Sonnet 30.7), so a small share is enough to pass:

| f | Haiku P(pass) | Sonnet P(pass) | bet P(pass) |
|---|---|---|---|
| 0.1 | 0.00 | 0.015 | 0.00 |
| 0.2 | 0.03 | **0.77** | 0.02 |
| 0.3 | **0.71** | **1.00** | **0.71** |

- The qonly gate does not reject this world, and the pass sentence ("the gm2 order effect does not need the placeholder") would then trade one format artefact for another.
- A genuine recency pull produces similar means, so means cannot separate the two. Individual responses can: a wrong-target answer lands on the statement's own rating, which is often 50–80 points from the question's.

**D6. holds (by reading; pre-mortem kind `design`, no pilot).**
- The items are gm2's trivia questions, with no refusal-prone content.
- Structured output fixes the parse, and the 0–100 clip is gm2's.
- `max_tokens` 200 (Haiku) and 1000 (Sonnet) completed every archived chain: gm2 400/400 shown and 400/400 redacted; em-dm4 Sonnet 160/160 each.
- A qonly reply is the same one-field JSON.
- A `max_tokens` stop or a parse failure is recorded as missing. A refusal raises `Refused`.

**D7. flaw: the primary comparison's differences are not listed.**
- §6 lists four ways qonly differs from *redacted*. The rule compares qonly with *shown* (R = OE_qonly / OE_shown), and those differences are not listed.
- In shown, the model:
  1. sees its own four real answers;
  2. produces four sub-ratings itself (the act of rating, which is the measurement gm2 was about);
  3. gets five user turns rather than one message;
  4. gets unnumbered questions rather than a 1–5 list;
  5. gets the opening "I will ask you to rate several statements, one at a time…" rather than "…Think about each statement in turn, then give a rating for the question itself only…";
  6. gives five structured outputs rather than one;
  7. meets the main question as its own final turn rather than line 5 of a list.
- Matched: model, settings, items, orders, R, date, call path and scale.
- A pass therefore says order matters "with none of the answer-turn bundle present" (fine as written in §6). A fail compares against a reference that differs from qonly in all seven ways, not only in "the placeholder".

**D8. flaw: the fail (and mixed) sentence uses a noun the design cannot carry.**
- "The gm2 pass was the placeholder, and the main paper must say so." That inference needs redacted ≥ ½ shown *today*.
  - Haiku: redacted is a secondary that no rule reads.
  - Sonnet: redacted is not run. The only reference is em-dm4's batch archive at R = 4, where the gate p was 0.031.
- §5 defines "the placeholder" as the line plus its turn-taking. §6's own list adds the numbering and the rate-only opening.
- Fail also covers a model whose qonly gate passes but whose R lower bound falls short. That is a *real* questions-only order effect, which the sentence would report as absent:
  - On Sonnet, an effect the same size as shown's, with shown's item effects reassigned to other items, fails **96%** of the time (`sim2.py`, P(pass) 0.04; Haiku 0.26).
  - The cause is concentration: 92% of Sonnet's shown between-order variance sits in two items (h261, h058).

**D9. holds.** Leave-one-item-out is committed in §4. Its consequence is in §5: the item id goes in the first plain-English paragraph, and the verdict is still read on all 10 items. `analyse_model` computes it with the same seeds. Expect flips on Sonnet (two items carry 92% of the shown variance); the rule already handles that.

**D10. flaw (stop-on-refusal); the rest holds.**
- **Refusal stop leaks.** `converse` never checks `stop` between turns. With the client stubbed to refuse call 31 under 8 workers, **8 calls started after the refusal had returned**, and 7 conversations completed and were cached. The worst case is 7 conversations × 4 calls. The refusal file then says "no further call was started", which is false.
- **A re-run ignores the refusal record.** `run()` does not check for `results/refusal-gm2q.md`. A second stubbed run, with the file present, made **195 calls**.
- The cost of a refused or errored conversation is never added to `spent()`.
- **Budget: holds at realistic prices.** The cap is checked under a lock before each conversation. The overshoot is at most 8 in-flight conversations, about 8 × $0.006 ≈ $0.05, which is below the $0.10 reserve. A stub at about $0.01 per conversation stopped at $3.474. Caveat: a stub at $0.60 per conversation overshot to $7.81, because the check ignores in-flight cost. That is harmless at these prices.
- **Cost against the cap** (list prices $2/$10 and $0.10/$0.50, priced from the archives' recorded per-conversation cost):

  | arm | estimate |
  |---|---|
  | Haiku shown | $0.105 (gm2, direct calls: $0.000263 per conversation) |
  | Haiku redacted | $0.105 |
  | Haiku qonly | ≈ $0.02 (~540 input tokens per call) |
  | Sonnet shown | $2.10 (em-dm4 $0.002628 per conversation at the batch rate × 2 × 400) |
  | Sonnet qonly | ≈ $0.46 (a fitted ~290-token schema overhead + ~255 message tokens) |
  | **total** | **≈ $2.79** |

  §3 says $2.60, because it underestimates Haiku shown and redacted ($0.07 each) and Sonnet qonly ($0.25). $2.79 still fits the $3.40 usable cap with $0.6 to spare, so step 5 should complete.
- **Caching.** Conversations are cached, but by job name, not content hash. The cache is written only every 50 conversations, so a hard kill can lose up to about $0.26 of recorded Sonnet spend. The cache does not exist yet and the prompts are fixed, so the risk is low (as in om-p2-3b F4).
- **Scale direction: holds.** The anchor "0 = certainly false, 100 = certainly true" is in every prompt, both conditions.
- **Beacon: holds.**
  - CURBY-Q round 28297 (2025-08-22) is stalled, so CURBy-RNG is the right chain.
  - Pulse 1592278 at 06:34:00 follows the pre-registration's author time of 06:33:22. The recorded previous pulse, 1592277 at 06:33:00, precedes it. I did not re-fetch; that is E23.
  - `python3 ledger/seed.py ea28…7679 em-gm2q --purpose analysis` → 17882636728661590601; mod 2^63 = 8659264691806814793. Both match §2 and the bet row.
  - The seed touches only the analysis (seed + 1 … + 5, as §2 says). The run draws nothing. Seed commit 1ba7f8c changes only the beacon line.
  - Note: `--analyse --seed S` accepts any S. Assert the recorded value.
- **Lesson: holds.** `python3 ledger/check_prereg.py em-gm2q /Users/seanpharris/oversight-testbed programs/entangled-mind/experiments/gm2q-questions-only.md --before-run` gives L1, L2, L3 and H1 ok. R1 fails only because this file did not exist yet. `ls-em-gm2q` quotes §0 verbatim and has `prereg_commit` 2f30696.

**D11. flaw: the dry run overstates power and leaves out the world that matters.**
- **Noisy means used as true.** `archive_world` uses the archived *sample* order means as true means. At R = 4 those carry sampling noise. The Sonnet world's true order effect is 7.7 points against a measured, variance-corrected OE of 6.1; Haiku's is 9.3 against 8.7.
- **Rebuilt with means shrunk to the measured OE** (`sim.py`, 200 runs per world, 400 permutations and bootstraps as in the dry run):

  | world | Haiku P(pass) | Sonnet P(pass) | bet P(pass) |
  |---|---|---|---|
  | equal | 0.995 | 0.785 | **0.78** (not 0.93) |
  | 0.75 × shown | 0.79 | 0.60 | 0.47 |
  | half | 0.07 | 0.17 | 0.01 |
  | null | 0 | 0 | 0 |

- **The missing world.** §8 notes that real power is lower once items differ, but never measures it. Equal-sized effects on unrelated items (shown's deviations shuffled across items) give a bet P(pass) of **0.01**, and still only 0.11 at 1.5 × shown. Half shown's pattern plus half the redacted pattern gives 0.95.
- **Floor met, but only for aligned items.** In the shrunk "equal" world, P(pass) is 0.78 and P(fail) 0.22. In the null and half worlds, P(fail) is ≥ 0.83. So the D11 floor holds in a world where qonly's effect lands on the same items as shown's. It is far below the floor where the effect is the same size but on other items.
- **What the bet actually tests.** In effect it tests "the questions-only effect reproduces the turn-by-turn effect item by item, at ≥ ½ size". That is a legitimate, strict claim, but §1 and §5 must say so (fix 4), and the odds should rest on the corrected table.

## Required fixes

All five can go in one dated DEVIATIONS.md row, written before any data: the next free number (D67 at the time of review), titled "em-gm2q design-review fixes (review `<sha of this file's commit>`, fix-first, 5 flaws)". Number the fixes inside it as below. None lowers the bar.

1. **D5: target check (tightens the pass).**
   - Add to §4 and §5, and to `analyse_model`, a flag on each qonly conversation. It is "wrong-target" if its rating is within 5 points of the today's-shown mean rating of the statement placed 4th in that order, and more than 20 points from that item's today's-shown mean final rating.
   - Compute the same flag on the shown final ratings as the chance baseline. Report both shares per model.
   - A model's **pass also requires the qonly permutation gate p < 0.05 to hold with the flagged qonly conversations dropped**. Cells keep ≥ 2 ratings; otherwise the model fails.
   - Add a `--selftest` case: a no-effect world with 30% of answers set to the 4th statement's rating must fail.

2. **D7: list the primary comparison's differences.**
   - Add to §6 the seven differences between qonly and *shown* listed under D7, and the matched factors.
   - Say there that R compares qonly with the whole turn-by-turn bundle, so a fail cannot be laid on any one of them.

3. **D8: rewrite the fail and mixed sentences.** Replace §5's fail sentence with two, chosen by the qonly gate:
   - **Fail, qonly gate p ≥ 0.05 on both models:** "With nothing in the transcript but the questions, their order did not detectably move the final rating on either model, though it did turn by turn. The order effect seen in gm2's redacted chain needs something the answer turns supply (the placeholder, the turn-taking, or the act of answering), and the main paper must not cite gm2 as showing that the questions alone build the number."
   - **Fail, qonly gate p < 0.05 on at least one model but R's bound short:** "With nothing in the transcript but the questions, their order still moved the final rating on <model(s)>, but not by a margin shown to be at least half the turn-by-turn effect on these 10 items: the questions alone do something, and this test cannot say how much."
   - **Placeholder clause:** add "the gm2 pass was the placeholder" only for Haiku, and only if today's Haiku redacted/shown lower bound is ≥ 0.5.
   - **Mixed:** replace "depends on the model" with "depends on the model or on the items".
   - Mirror the change in the plain-English §1 and in `paper/novelty.md`'s ranked item 2 when the result is written.

4. **D11: redo the dry run.**
   - Rebuild `dry_run` with each item's order deviations shrunk to the measured, variance-corrected OE.
   - Add the shuffled-items world (equal and 1.5 × size), the 0.75 world and the wrong-target worlds (f = 0.1–0.3, which should fail after fix 1).
   - Recommit `results/gm2q-dry-run.json` and §8's table, and replace §8's "real power at equal is lower" with the measured numbers.
   - In §1, state that the pass needs the effect to land on the same items as the turn-by-turn one.
   - Odds may be revised before data, with both numbers kept in §0 and the bet row. My corrected "equal" bet figure is 0.78, not 0.93.
   - Alternatively, if the author wants a test of size alone, that means more items or a different interval. That is a redesign, not this fix.

5. **D10: refusal machinery.**
   - In `converse`, check `stop.is_set()` before every call, so that a conversation in flight ends unfinished and uncached once any refusal or error is seen. Pass `stop` in, or raise.
   - At the start of `run()`, exit if `REFUSAL` exists.
   - Add the cost of the refused or errored conversation to a `spent_lost` counter that `spent()` includes.
   - Write the cache after every conversation (not every 50), or key entries by a content hash of model, max_tokens, thinking, schema and messages, checked at analysis.
   - Make `--analyse` assert that the seed equals 17882636728661590601.
   - Re-run the stubbed refusal test: zero calls may start after the refusal returns.
   - Correct §3's Haiku and Sonnet qonly estimates (total ≈ $2.79), and fix the two text slips noted under D2 and the unregistered cell rule noted under D1.

The reviewer confirms each fix in an addendum to this file before any call. Fixes 1 and 5 can be checked with stubs; fix 4 by re-running the shrunk and shuffled worlds.

## Confirmation

Checked 2026-11-05 07:05 America/Denver against D69 and commit `a548fae`. The working tree matches `a548fae` for the code and the dry-run JSON. Read-only. No calls were made. Scratch scripts are in `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/7db7e173-0d10-4755-94b1-f97b0684254c/scratchpad/review/`: `confirm1.py`, `confirm1b.py`, `confirm4.py` and `confirm5.py`. `--selftest` and `--print-prompts` pass.

**Result: not confirmed (fixes 1 and 3 open, and one sub-item of 5). `confirmed_at` stays null.**

### Fix 1 (D5, wrong-target flag): not confirmed

The code does what D69 says:
- `wrong_target` uses ±5 points near and more than 20 points far.
- The cleaned qonly gate uses seed + 6.
- A cell left with fewer than 2 ratings fails.
- Both shares are reported.
- The selftest world fails (raw p 0.0002; cleaned p 0.42).

The flag does not work at realistic noise:
- The dry run and the selftest draw each wrong-target answer with SD 2 around the statement's mean.
- A real wrong-target answer would vary like the model's own rating of that statement. In the archives' shown chains that is a within-cell SD of 10.6 (Haiku) and 8.5 (Sonnet).
- At those SDs, only about a quarter of the wrong-target answers fall within ±5. With f = 0.3, the flag catches 7.5% (Haiku) and 9.4% (Sonnet) of answers, against a true share of 30%.
- P(pass) at f = 0.3 is therefore 0.58 (Haiku), 0.705 (Sonnet) and **0.41** for the bet, not D69's 0.04 (`confirm1.py`, 200 runs, the module's own functions).

**Remaining fix:**
- **Rule.** Flag an answer when it is *nearer* the 4th statement's mean than the item's final mean, and more than 20 points from the final mean: `abs(r - s4) < abs(r - fin) - TOL and abs(r - fin) > 20 + TOL`.
- **Tested** with the same machinery and realistic SDs (`confirm1b.py`):
  - The wrong-target 0.3 world passes 0.05 (Haiku), 0.115 (Sonnet) and **0.006** for the bet.
  - The equal world keeps 0.97, 0.835 and 0.81, against D69's 0.822, so power is kept.
  - Flagged share with no wrong-target answers: 1.6–1.9%.
- **Tests.** Redraw the selftest's and the dry run's wrong-target answers with SD 10.6 (Haiku) and 8.5 (Sonnet), and update D69's table rows.
- **Record.** Record it as an amendment to D69 (a new dated row), before any data.

### Fix 2 (D7, differences listed): confirmed

D69 lists all seven qonly-versus-shown differences and the matched factors. It says a fail cannot be laid on any one of them.

### Fix 3 (D8, verdict sentences): not confirmed

The split by the qonly gate carries, and so do fail-short and the mixed wording.

On the placeholder sentence I kept by the job's order:
- Its conditions are mine: qonly gate p ≥ 0.05 on both models, and today's Haiku redacted/shown lower bound ≥ 0.5.
- "The gm2 pass" names gm2's Haiku result, which today's Haiku redacted arm can carry.
- So the sentence is acceptable in that case, with two changes:
  - **(a) Name the whole bundle.** The parenthesis defines "the placeholder" as the line, the turn-taking and the act of answering. qonly also differs from the redacted chain in the 1–5 numbering and in the opening's "give a rating for the question itself only" instruction. That instruction could by itself tell the model to set the statements aside, and the review's D8 point 3 named both. Add them: "…(the '[rating recorded]' line, the turn-taking and the act of answering, together with the numbered list and rate-only opening that replaced them)…".
  - **(b) Choose the sentence from the cleaned gate.** `sentence_key` picks fail-short from the *raw* qonly gate. If the raw gate passes only because of wrong-target answers (cleaned p ≥ 0.05), fail-short's "the questions alone do something" would be false. Key fail-short on `qonly_p_clean` (None counts as not passing), and the two "dies" sentences on the same.
- **Recommended, not required.** The placeholder clause rests on non-detection (p ≥ 0.05), not on a shown small effect. Put Haiku's R_qonly/redacted, with its interval, in the same paragraph.

### Fix 4 (D11, dry run): confirmed, except its wrong-target rows

- I ran `dry_run()` by import, without writing into `results/`. The output is **identical** to the committed `results/gm2q-dry-run.json`, and every row matches D69's table.
- The shrinkage is per item, sqrt(VC / var(means)), so each world's OE equals the measured OE.
- The shuffled-items and 0.75 worlds match my own independent simulation: equal 0.822 here against my 0.78; shuffled, equal size, 0.005 against my 0.01.
- The plain statement that a pass needs the effect on the same items, and the odds revised to 0.10 with both numbers kept, carry.
- Only the wrong-target rows (0.000, 0.001, 0.040) must be redone after fix 1, with realistic answer SDs.

### Fix 5 (D10, refusal machinery): confirmed, except one sub-item

Results of the stubs, with `run(client)` called and the cache and refusal paths in scratch:

| check | result |
|---|---|
| refusal at call 31 (8 workers, 50 ms calls) | **0** calls started after the refusal returned |
| refusal at call 434 (8 workers) | **0** calls started after the refusal returned |
| unfinished conversations | recorded under `_lost` (aborted and refused) |
| recorded spend against billed | equal to the cent |
| refusal file | written |
| second run with the file present | exited with **0** calls |
| cap at about $0.01 per conversation | stopped at $3.455 (≤ $3.50) |
| `--analyse --seed 123` | the assert fires |
| cache | written after every conversation |

The open sub-item: the review asked that an *errored* conversation's cost also count. A stub error at call 31 records $0.01836, but $0.02040 was billed before the failed call. `except Exception` keeps no partial cost. The amount is small (one conversation, at most about $0.005) and the run stops on any error, but it is not yet done. Fix: catch the error inside `guarded`, attach `cost` to it, and record it under `_lost|key` the way `Refused` is recorded.

### What remains before go

1. The fix 1 flag rule and realistic wrong-target SDs, plus the redone dry-run rows.
2. Fix 3 (a), the bundle wording, and (b), `sentence_key` from the cleaned gate.
3. Fix 5's errored-conversation cost.

All three are small and can go in one dated DEVIATIONS row amending D69, before any call. The reviewer then confirms in a second addendum.

## Confirmation 2

Checked 2026-11-05 07:13 America/Denver against D70 and commit `d78475d`. The working tree matches `d78475d` for the code and `results/gm2q-dry-run.json`. Read-only. No calls were made. The scratch scripts are the same ones as in confirmation 1, re-run.

**Result: every fix is confirmed. Final verdict: go.**

### Fix 1 (flag): confirmed

- `wrong_target` is the rule as written in confirmation 1: `abs(r - s4) < abs(r - fin) - TOL and abs(r - fin) > 20 + TOL`.
- `synthetic_cache` now draws both the shown sub-ratings and the wrong-target answers with `stmt_sd`. `archive_world` measures it from the archives' shown cells: 10.6 for Haiku and 8.5 for Sonnet, the same values I measured.
- `--selftest` passes. The 30% wrong-target world gives a raw p of 0.0002 and a cleaned p of 0.45, with 27% of answers flagged, and is labelled fail.

### Fix 3 (sentences): confirmed

- The placeholder sentence now names the whole bundle, including the numbered list and the rate-only opening. Haiku's R_qonly/redacted is reported beside it.
- `sentence_key` picks the sentence as follows:

| sentence | when it is used |
|---|---|
| fail-short | raw and cleaned qonly gates both pass on at least one model |
| fail-target | otherwise, a raw gate passes on some model |
| the two "dies" sentences | otherwise; they need the raw gate p ≥ 0.05 on both models |

- The selftest asserts all five sentence cases, including fail-target with `qonly_p_clean` both None and failing.
- **fail-target carries.** When the raw gate passes and the cleaned gate does not, the only detectable effect lies in answers the flag cannot tell from rating the wrong line. The sentence says exactly that, says the question is not settled, and uses no placeholder clause.
- Recommended wording, not required: "…but **detectably** only through answers that…". A failed cleaned gate shows non-detection, not that the effect is absent.

### Fix 5 (errored cost): confirmed

- With a stub error at call 31, the recorded spend is $0.02040, exactly what was billed before the failed call. The conversation is stored under `_lost|…` as "errored".
- The refusal stubs at calls 31 and 434 again give 0 calls after the refusal.
- A second run with the refusal record present makes 0 calls.
- The cap stops the run at $3.442.
- The seed assert holds.

### Dry run: reproduced

`dry_run()` called by import gives output **identical** to the committed JSON. Every bet figure matches D70's table:

| world | bet P(pass) |
|---|---|
| equal | 0.739 |
| redacted pattern | 0.127 |
| 0.75 | 0.448 |
| shuffled items | 0.005 |
| wrong-target 0.3 | 0.005 |
| null | 0 |

### D11 after the power loss: holds, so this is not a redesign

- **It can still pass.** A world where the hypothesis holds still passes in two cases:
  - **Same items:** the effect sits on the same items at about full size (equal world, 0.739).
  - **Big jumps:** the effect is made of gm2-like big jumps (redacted-pattern world, 0.127, just above the floor of about 10%).
- **It can still fail.** P(fail) is 0.26 in the equal world, and 1.0 in the null world and in the 30% wrong-target world (0.995).
- **Why the big-jump world loses power.** Its effect is a few large jumps onto one statement's rating, such as h191's 81 against 3. Those are the answers the design cannot tell from rating the wrong line. Counting them as a pass would put back the very loophole fix 1 closed. In that world the bet now usually ends in fail-target, whose sentence says the question is not settled.
- **What the question has become.** Does a questions-only order effect, made of moderate shifts on the same items as the turn-by-turn one, survive at about its size? It is narrower than the original question, and D69 and D70 now say so plainly. The odds of 0.10 fit the corrected table. The bet can answer this question.

### Header

`confirmed_at` is set to 2026-11-05 07:13. The verdict field stays `fix-first` (confirmed), with fix rows D69 and D70. The run may start.

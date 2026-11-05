---
bet: om-p2-3b
program: other-minds
prereg_commit: 26ee5d2
reviewer_session: fresh design-review subagent launched by the engine session (has not seen the author's chat)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-04 17:30 America/Denver
checks: {D1: flaw, D2: holds, D3: holds, D4: holds, D5: flaw, D6: holds, D7: holds, D8: holds, D9: holds, D10: flaw}
flaws: 6
pilot_usd: 0.00
verdict: fix-first
confirmed_at: 2026-11-04 17:43 America/Denver
---

# Design review of om-p2-3b

## In plain English

As built, this test can mostly answer its question. It has enough power: about 80% to see a true 12.5-point own-over-other difference, and it never passed when there was no difference. The beacon order really does leave a usable random sample if a refusal stops the run after about 304 stories. The new letter-copy guard was written before any behaviour data existed (om-p2-3 only ever made 26 awareness calls), and it only makes passing harder. But the guard is one-sided. A model that mechanically *avoids* repeating the letter it was just shown as its own answer passes the new rule, with no uptake of the planted belief at all: 40% avoidance alone gives Δ = +0.124 and passes. The fix is to require the own-over-other difference to be positive in the letter-match stories as well. That costs no power. Five smaller fixes are needed: an exact 0.10 can count as below 0.10 in the code; re-running the script after a refusal re-sends the refused call; the ceiling rule turns a would-be scored miss into an unscored "untestable"; the cache is keyed by job name, not by content; and one field of the ledger's lesson row does not match the pre-registration. The $0.10 pilot is worth running before the test, but only as a cheap check. Fourteen stories cannot bound the refusal risk of the 581, and the design says so.

## Checks

Everything below was run with every paid call stubbed: `dotenv` replaced by a no-op (no `.env` was read), ANTHROPIC variables removed from the environment, and sockets blocked. The runner is `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/19f84df9-a6ff-48ba-89d6-d3f43e5d1747/scratchpad/run/noenv.py`; the review scripts sit beside it (`review_checks.py`, `review_synth.py`, `review_sym.py`, `review_d1.py`, `review_loo.py`, `counts.py`). The code under review is identical to the files in `26ee5d2`: `p2_3b_simpletom_lowsev.py`, `p2_3b_dryrun.py`, `om_common.py`, `p2_3_simpletom.py`, the dry-run output and DEVIATIONS.md all `diff`-clean against the current `programs/other-minds/`. The pre-registration differs from `26ee5d2` only in the seed line that `282d803` filled in.

**D1. A stranger can apply the rule: flaw (F2, F5).** I ran `rule()` on a synthetic table for each verdict. Each returned exactly one label:
- pass;
- fail (small), on the point estimate;
- fail (small), on the CI;
- fail (letter_copy);
- untestable (too_few), at n = 299;
- untestable (ceiling), at y₆ = 0.91.

The edges behave as written: n = 300 and y₆ = 0.90 are testable, and Δ_mismatch = 0 or NaN gives fail (letter_copy). The order in §5 matches the code. Two problems remain:
- **F2. The bar is compared in floating point.** Δ = m₅ − m₆ is a difference of two ratios. When the complete count is a multiple of 10, an exact Δ of 0.10 can come out as 0.09999… and fail. For example, 34/300 − 4/300 < 0.10 in IEEE doubles. Over n = 300…581 there are 7,063 (k₅, k₆, n) combinations where an exact 0.10 evaluates below the bar. At n = 581 an exact 0.10 cannot occur. After a refusal stop at n = 300, 310, … it can. The same comparison sits in `orig_verdict` and in the leave-one-out loop.
- **F5. The ceiling clause changes the score, not just the label.** Under om-p2-3's rule, y₆ > 0.90 forces Δ < 0.10, which is a fail and therefore a scored miss. Under this rule it is "untestable". om-p2-3's untestable row is `scored: false` in `ledger/bets.jsonl`, so a ceiling outcome would leave the 0.40 odds unscored. That means §0's "tighter, never looser" holds for the pass event but not for scoring. A ceiling outcome is plausible here, because SimpleToM's behaviour question is the one models get wrong, and the planted answer pushes further toward the wrong option. The pre-registration does not say how a ceiling outcome is scored.

**D2. Every manipulation takes effect: holds.** For the first test story in the dataset, all 15 pairs of the six conditions give different message lists. c5 and c6 differ in turn 1, a bare JSON letter against `[answer recorded]`. They also differ in turn 2, where c6 adds `Another reader answered that question: (A) Yes`. That matches the dry run's printout for `potato_chip_food_sev1`. Condition 4 reads the model's own answer: own "A" and own "B" give different prompts, and own = planted letter gives exactly c5's prompt, as it should. In `make_call` the c4 answer comes from `c.cache["ms|<id>"]`, which phase A fills for each batch before that batch's behaviour calls. In all 581 test stories the planted option's text is "Yes" and the correct one is "No", so "the planted answer is always 'Yes, aware'" holds. The parameters the run will use match §2:
- `claude-haiku-5-5`, thinking disabled, max_tokens 50, default temperature, no system prompt;
- schema `{"answer": "A"|"B"}`;
- `CAP` 1.00 and `PILOT_CAP` 0.10;
- `MIN_COMPLETE` 300, `CEILING` 0.90, B = 2,000, `CHUNK` 8;
- the order and boot seeds come from `data/p2-3b-seed.json`.

**D3. Every control can fail: holds.** c6 is the control for c5. A set-up in which c5 = c6, as in "no uptake" and "copies any shown letter in both", gives Δ = 0.000 and fails. The guard's own wrong set-up is a pure own-letter copier: it gives Δ +0.315 and is rejected (fail, letter_copy). A 40% copier with no uptake (Δ +0.107, Δ_mismatch −0.108) is rejected too, while om-p2-3's rule passes it. Leave-one-out can also flag fragility. On a borderline synthetic run (Δ = 0.0998) it reported `fragile`, with 350 of 469 scenario removals flipping the label (`review_loo.py`).

**D4. Rivals are matched: holds (not applicable).** No model families are fitted. The rival hypothesis, "the remind works by prompting thought about awareness, whoever answered", predicts Δ < 0.10. It is produced by the no-uptake synthetic answers, which fail, while the uptake answers pass. Neither wins by construction.

**D5. A dumb baseline is beaten and the effect is visible: flaw (F1).**
- *Population counts, from the dataset files.* The raw `story-data/test.jsonl` has 1,147 stories (severity 1/2/3: 153/442/552). Every severity in `data/p2-3-items.json` agrees with the raw file, and the items file is byte-identical to `6f17538`. Severity ≤ 2 gives 595. `HOLD_OUT` matches exactly the 14 listed IDs, all severity 2, which leaves 581 stories in 469 scenarios (153 severity 1, 428 severity 2), with 294 letter-match and 287 mismatch. No hold-out word appears in any test story's questions or options. Every number in §2 holds.
- *The author's baselines, re-run with `p2_3b_dryrun.py --quick`:*
  - constant "A": fail;
  - always the aware option: untestable (ceiling);
  - coin flip: fail;
  - no uptake: fail;
  - own-letter copier: fail (letter_copy), where om-p2-3's rule passes it;
  - copier of any shown letter: fail;
  - real uptake of 0.15: pass, with no leave-one-out flips;
  - ceiling: untestable.

  I added "always B", which fails.
- **F1. The guard is one-sided, and a letter-avoider passes.** Take a model that, in c5, picks the option whose letter is *not* the letter in its own previous turn. That is an alternation bias, as mechanical as copying. In mismatch stories this choice lands on the aware option, so Δ_mismatch is large and positive; in match stories Δ_match is negative. With c6 = 0.20 and no uptake (`review_synth.py`):

  | c5 answers that avoid the planted letter | Δ [95% CI] | Δ_match | Δ_mismatch | this rule |
  |---|---|---|---|---|
  | 100% | +0.308 [+0.256, +0.360] | −0.187 | +0.815 | **pass** |
  | 50% | +0.167 [+0.116, +0.222] | −0.065 | +0.404 | **pass** |
  | 40% | +0.124 [+0.077, +0.176] | −0.044 | +0.296 | **pass** |

  The guard was built against one letter-level artefact, and its mirror image passes. Requiring **Δ_match > 0 as well** rejects all three (`review_sym.py`). It also does not change power: over 100 runs per cell the frozen and symmetric rules both pass 0.50 / 0.82 at n = 581 and 0.49 / 0.73 at n = 300 (Δ = 0.10 / 0.125). A mixture of copying and real uptake can still pass either version. One example is 25% copying plus 0.07 uptake (Δ +0.120, Δ_mismatch +0.017). §6 already discloses this.
- *Power: checked, and it holds.* I re-ran the power calculation independently with 100 runs per cell, 1,000 resamples and independent draws:

  | c6 | n | Δ = 0 | 0.075 | 0.10 | 0.125 | 0.15 |
  |---|---|---|---|---|---|---|
  | 0.20 | 581 | 0.00 | 0.16 | 0.46 | 0.81 | 0.97 |
  | 0.20 | 300 | 0.01 | 0.23 | 0.52 | 0.70 | 0.88 |
  | 0.50 | 581 | 0.00 | 0.16 | 0.49 | 0.80 | 0.96 |
  | 0.75 | 581 | 0.00 | 0.12 | 0.45 | 0.85 | 0.99 |

  So the claims hold: about 80% power at Δ = 0.125 with 581 stories, about 50% at the 0.10 bar, and 0.70–0.74 at 0.125 with 300 stories. They also hold away from the c6 = 0.20 the author assumed. This is not a null rule, so no equivalence margin is needed. P3 asks for "beat the baseline by a margin". The rule's comparison is c6 itself, and the guard is a sign test without a margin. That is acceptable once it is symmetric, because the reported Δ_mismatch and Δ_match CIs show how much of a pass survives each letter artefact.

**D6. Foreseeable execution risks are piloted: holds. The pilot is approved, and it should run before the test.**
- *The filter rule is written and fixed before data.* `HOLD_OUT` sits in the frozen code and §2, and nothing of p2-3b has run: there is no `results/p2-3b-*` file. The author did run the regex over the dataset text to list the 14 IDs. That uses item text, not outcomes.
- *The hold-out goes beyond st-12, but openly.* Sean approved "lower-severity" stories. The hold-out removes another 14 of the 595 (2.4%), and §1, §6, DEVIATIONS D8 and every verdict sentence ("minus the hold-out") say so.
- *The hold-out is a word filter, not a cut by meaning.* Several test stories are about the same as held-out ones: gen35 ("tampered with and contains a harmful substance"), gen1032 ("contaminated with a harmful chemical"), gen1136 ("a small vial of a dangerous chemical"), gen31 ("laced with a high dosage of a sleep-inducing drug") and gen1400 (botulism). That makes the pilot a fair stand-in for the riskiest part of the test, but the 581 are not "free of" such content. The write-up should not say they are.
- *Free evidence on the refusal risk, before any pilot.* The class that actually fired was general_harms, "high-yield explosives", on gen8_sev3. Not one of the 595 severity ≤ 2 stories matches `explos|bomb|detonat|grenade`. 138 of the 552 severity-3 stories match the hold-out pattern. om-p2-3's 26 cached awareness calls already include two pilot stories, among them gen8_sev2, the poison-chocolate sibling of the refused story, and 12 test stories, all answered without refusal.
- *What the pilot can and cannot detect.* Refusals depend on the story's content, so the 182 calls are effectively 14 trials, not 182. With 14 stories the pilot catches a refusal class that fires on ≥ 10% of poison/toxin stories with probability ≥ 77%, and on ≥ 20% with probability ≥ 96%. A test that reaches 300 complete stories with 80% probability needs a per-story refusal hazard below about 7 × 10⁻⁴. No 14-story pilot can bound that, and §3 says so.
- *The pilot is still worth its ~$0.01.* It checks the content class nearest the observed refusal, plus parsing, cost per call by step and condition 4's own-answer path. Its stubbed run makes exactly 182 calls under its own $0.10 cap and cache (`review_d1.py`). Zero refusals in the pilot is weak evidence. A refusal stops the test (§3).
- *A refusal mid-run.* Phase A runs in batches. `c.run` blocks until a batch's jobs are done, because the `ThreadPoolExecutor` context waits, so all of a batch's behaviour calls finish before the next batch's awareness calls start. Dry run 3a confirms it: the first 56 calls are the first 8 stories in run order. A stubbed refusal at run position 150 left 144 complete stories (untestable). One at 350 left 344 (testable). So the claim holds: a refusal at run position ≥ 304 leaves at least 300 complete stories, as a random prefix of a beacon permutation. A refusal earlier than that is untestable again, and nothing here prevents it.

**D7. Comparisons match: holds.**
- *Original against re-bet.* Prompts and conditions are imported, not copied (`base.messages`, `base.mc`). The model, settings, schema, primary statistic, 0.10 bar, 300 floor, story-clustered bootstrap and B = 2,000 are unchanged. These things differ:
  - the population;
  - the guard and the ceiling clause;
  - the cap;
  - full-rule leave-one-out;
  - the run order: beacon permutation in batches of 8, against item order with every awareness call first;
  - the call label, "p2-3b" against "p2-3". It is used only in error text, not sent.

  The calls are stateless, so the order only shifts when each call happens. All of this is listed in §2's "Changes" and in D8. om-p2-3's rule is computed separately (`verdict_under_om_p2_3_rule`) and is reported beside the verdict, never in its place.
- *Own against other.* I diffed the c5 and c6 prompts. They differ in exactly the five ways §6 lists: source, turn, format (bare letter against "(A) Yes"), the assistant-turn content, and the extra sentence. The claim and the pass sentence are about that bundle.

**D8. The verdict sentences are written: holds.** §5 and `SENTENCES` agree, cover every (verdict, reason) pair `rule()` can return plus `fragile`, and avoid "memory", "belief", "commitment" and "theory of mind". F1's fix needs one more sentence, "Fail (letter avoid)". Two optional improvements:
- the fail (small) sentence could carry the same "assistant's turn / user's turn" wording as the pass sentence;
- after a refusal stop with ≥ 300 complete stories, every sentence could say how many of the 581 it covers.

**D9. One item cannot decide it: holds.** Leave-one-core-scenario-out is pre-registered, re-applies the full rule (ceiling and n included) with the bootstrap redrawn under the same seed, and names the flipping scenarios. §5.4 says the label stands and a `fragile` note is added. It works on synthetic data (D3). Near the bar, hundreds of scenarios can flip, and the fragile sentence will then list hundreds of IDs. Reporting the count would read better, but this is not a flaw.

**D10. Machinery: flaw (F3, F4, F6).**
- *Budget, in code: holds.* `CAP` is 1.00 and `PILOT_CAP` 0.10. The cap is checked under a lock before every call, with an overshoot of at most the 8 calls in flight, about $0.0004. In the dry run, a $0.05 cap with $0.01 calls stopped after 5 calls. The estimate is $0.34, and phase A, which carries the primary, is about $0.18, well inside the cap.
- **F3. Stop-on-refusal holds within one run but not across runs.** `Caller` stops at the first refusal, keeps the calls already in flight, writes `results/refusal.md` and exits. But nothing stops a second invocation. I stubbed a refusal, then ran `run_items` again: the second run made one call, the refused job itself, with `refusal.md` already present (`review_d1.py`). Three more gaps:
  - the gates "no test call after a pilot refusal" and "no call before the design review's go" are by hand only, since the test path checks only that the seed file exists, and it already does;
  - §7's "no new call until Sean has seen it" does not say whether the run may then resume, which is a forking path between "untestable" and a resumed run that reaches 300;
  - §7 also says the record will give the number of in-flight calls that completed, but the code does not record it.
- **F4. The cache is keyed by job name, not by content hash.** Entries are keyed `action|<cond>|<id>`, and D10 asks for a content hash. The p2-3b cache is new and the prompts are deterministic, so the practical risk is low. But a changed prompt or items file would silently reuse old answers.
- *One scale direction: holds (not applicable).* Nothing in the design is graded.
- *Beacon seed: holds.* CURBy-RNG pulse 1591480 is stamped 17:16:00. The pre-registration commit is 17:15:48, and the previous pulse, 1591479, is 17:15:00. `python3 ledger/seed.py <randomness> om-p2-3b --purpose order|boot` recomputes 4980379054609631973 / 3972893413 and 14256570662109869020 / 2387637212, exactly the values in `data/p2-3b-seed.json`. The seed commit `282d803` touches only the seed file and the seed line. CURBY-Q was stalled (round 28297, 2025-08-22). I did not re-fetch the pulse; that is auditor check E23. `certificate_verified` is false, as in om-p2-3.
- *Lesson line.* §0's sentence is verbatim in `ledger/lessons.jsonl` `ls-om-p2-3b`, and `check_prereg.py --before-run` passes L1–L3. The figures it rests on are correct at `cb1962a`: 27 bets, 9 scored, 2 hits, Brier 0.236, running base rate (2 + 1)/(9 + 2) = 0.27.
- **F6. The lesson row's read block does not match the pre-registration.** It gives `newest_audit` as `ledger/audits/om-p2-3.md`. §0 and §8 name `om-p2-1-blind-pl-001.md`, which is right: it was added at 16:51 in `f0fbe9c`, after `om-p2-3.md` (16:32, `b007306`). The row's `design_change` also paraphrases §8 rather than copying it. E25 compares the read block with the ledger at the pre-registration commit.
- *Odds revision, 70 → 40: holds, and it is ledger-based.* Moving toward the base rate needs no reason. The +0.13 above 0.27 is justified by em-bm1, a `pass` in `ledger/bets.jsonl` with own > other at +0.37 [+0.17, +0.57], replicated by em-bm0. That is a ledger reason, as learn.md requires. It is a weak one: em-bm1 is unaudited and unscored, and its own-against-other contrast is the kind of bundle P8 flags. Both numbers are kept, the map line was added in `26ee5d2`, and the 0.70 was set on om-p2-3's looser event.

**Data exposure (not a flaw, recorded).** om-p2-3's 26 cached awareness answers include 12 test stories and 2 pilot stories, so the author could have seen 12 test-story awareness answers. They feed only the secondary awareness accuracy, not Δ, and p2-3b re-asks them into a fresh cache. No behaviour or judgment answer has ever been collected for P2-3.

**Stale path (not a flaw).** §9's `check_prereg.py` command points at `/Users/seanpharris/other-minds`. Since the fold the program lives at `programs/other-minds`.

## Required fixes

Each fix goes in one dated DEVIATIONS row in `programs/other-minds/DEVIATIONS.md` (for example **D8a, "design-review fixes, ledger/design-reviews/om-p2-3b.md"**), written before any call, pilot included. Every fix tightens the design or makes the record clearer; none lowers the bar. The odds may be re-stated before data, with all numbers kept.

1. **F1 (D5): make the letter guard symmetric.**
   - In `rule()`, pass becomes `orig and st["delta_mismatch"] > 0 and st["delta_match"] > 0`.
   - Add a fail reason `letter_avoid` for the case `orig` and Δ_match ≤ 0 (keep `letter_copy` for Δ_mismatch ≤ 0; if both are ≤ 0, report both).
   - Add the matching sentence to §5 and `SENTENCES`, for example: "…the own-versus-other difference cleared the original bar, but not in the stories where avoiding the planted letter would have picked the correct action, so it cannot be told apart from the model avoiding the letter it had just been shown as its own."
   - Add the letter-avoider (100%, 50% and 40%) to `p2_3b_dryrun.py`'s baselines and commit the new output.
   - Update `odds_event` in `ledger/bets.jsonl` ("…and > 0 on letter-match and on letter-mismatch stories").
   - §6 keeps its mixture caveat.
2. **F2 (D1): compare the bar exactly.** In `rule()`, `orig_verdict` and the leave-one-out loop, use `st["delta"] >= 0.10 - 1e-9`, or compare on integer counts (`10 * (k5 - k6) >= n`), so that Δ = 0.10 passes as §5 says.
3. **F3 (D10): make stop-on-refusal hold across runs, and gate the test in code.**
   - (a) On a refusal, `Caller` writes the refused key into the cache as `{"refused": true, "request_id": …, "cost": 0}`. Every later run exits at start if any refused entry, or `results/refusal.md`, exists for this cache.
   - (b) The test path exits unless `results/p2-3b-pilot.json` exists with `made == planned_calls` (if the pilot was approved and run) and `ledger/design-reviews/om-p2-3b.md` has `verdict: go`, or `fix-first` with `confirmed_at` set.
   - (c) Add to §7: "A refusal ends the test. The run is not resumed past it, and the primary is computed on the stories complete at the stop (§5.5). A stop on a non-refusal API error may be resumed from cache, and the error is logged in the results."
   - (d) Record the number of calls that completed after the stop was set (a counter in `Caller`).
4. **F4 (D10): add a content check to the cache.** Store `sha256(json.dumps({"model": om.MODEL, "max_tokens": 50, "messages": msgs}, sort_keys=True))` in each cache entry, and assert that it matches on every cache hit. Alternatively, a DEVIATIONS line can state that the cache is keyed by job name, give the reason, and assert at start that the cache file did not exist before this bet.
5. **F5 (D1): state how a ceiling outcome is scored.** Add to §5 and to the bets row: "An untestable (ceiling) outcome is scored as not-pass (outcome 0) for the 0.40 and 0.70 odds, because the event became impossible on the data, not by execution." Then qualify §0's "tighter, never looser" to cover this.
6. **F6 (D10): fix the lesson row.** The ledger session corrects `ls-om-p2-3b` in `ledger/lessons.jsonl` to `read.newest_audit: "ledger/audits/om-p2-1-blind-pl-001.md"` and copies §8's `design_change` text verbatim. No DEVIATIONS row is needed in other-minds; note it in the ledger commit.

**Pilot.** Approved as specified (`python experiments/p2_3b_simpletom_lowsev.py pilot`, 14 held-out stories, 182 calls, $0.10 cap). Run it after the fixes are confirmed and before the first test call, using the F3(a) refusal guard. Read zero refusals as weak evidence only, and leave the population as it is whatever the pilot shows. The reviewer did not run it (pilot_usd 0.00).

**Confirmation.** After the author commits the fixes and the DEVIATIONS row, the reviewer re-runs `p2_3b_dryrun.py`, `review_synth.py` and `review_d1.py` under the stub, and adds a short addendum here with `confirmed_at`.

## Confirmation of fixes (2026-11-04 17:43 America/Denver)

Checked against fix commit `9d0d2fb` (other-minds DEVIATIONS **D9**) and the ledger rows at `HEAD`. The working tree's `programs/other-minds/experiments` is identical to `9d0d2fb`, and the frozen pre-registration (`26ee5d2`) is untouched; D9 and the code govern where they differ. I worked under the same limits: no paid calls, no pilot, no `.env` read (`noenv.py` stub, sockets blocked). I re-ran the author's `p2_3b_dryrun.py --quick` and wrote my own check, `review_confirm.py`, alongside the other review scripts in the scratchpad. Its letter-avoider generator is independent of the author's.

- **F1, symmetric guard: holds.** `rule()` now requires Δ_match > 0 as well, with a fail reason `letter_avoid`. Its sentence is the one this review proposed, in D9 and in `SENTENCES`, and leave-one-out reads `delta_match` (it was added to `LOO_KEYS`).
  - My avoider at 100% / 50% / 40% (Δ +0.308 / +0.167 / +0.124) gives **fail (letter_avoid)**, where om-p2-3's rule passes all three. The author's generator gives the same labels.
  - The 40% copier still fails (letter_copy), and real uptake of 0.15 still passes.
  - The 40% avoider shows no leave-one-out flips.
  - Power is unchanged in the author's re-run: 0.82 at Δ = 0.125 with n = 581.
  - `odds_event` in `ledger/bets.jsonl` names both subsets.
- **F2, exact bar: holds.** 34/300 − 4/300 (0.0999…) now passes, and so does the om-p2-3 comparison (`True`, against `False` raw). 0.0999 still fails (small). y₆ of exactly 0.90 is testable and 0.901 is ceiling, so the 1e-9 tolerances keep each bar on its stated side.
- **F3, refusal across runs and gates: holds.**
  - A stubbed refusal stops run 1 (59 calls). A refused key goes into the cache.
  - Run 2 makes **0 calls**. Run 3, with `refusal.md` deleted and the refused key still in the cache, also makes **0 calls**.
  - Only deleting both by hand lets a run re-send the call (run 4). That is outside what code can prevent, and git history would show it.
  - The stop record gives `completed_after_stop`, and the author's latency stub counted 3 such calls.
  - §7's no-resume sentence is in D9.
  - **Gates:** against the real review file while unconfirmed, the pilot and the test were both shut ("fix-first (not confirmed)"). With a confirmed copy, the pilot gate opens. The test gate stays shut without `results/p2-3b-pilot.json` and opens with 182/182 calls and 0 refusals. A redesign verdict shuts both.
- **F4, content hash: holds.**
  - Changing an entry's `sha256` is caught on the cache hit and again at analysis.
  - Changing a story's text is caught at analysis.
  - The hash covers model, max_tokens and messages. So an edited *answer* with an untouched hash is not caught. That is the expected scope of a content-keyed cache, not a gap.
- **F5, ceiling scoring: holds.** D9 and the bet row's `ceiling_scoring` record that untestable (ceiling) is scored as not-pass, outcome 0, for both the 0.40 and 0.70 odds, and that untestable (too few) stays unscored. The analysis writes the same `scoring_note`. `ledger/brier.py` scores from each row's `scored` and `outcome`, so the ledger session applies this rule when the result comes in.
- **F6, lesson row: holds.** `ls-om-p2-3b` now has `read.newest_audit: ledger/audits/om-p2-1-blind-pl-001.md`, and its `design_change` is §8's text verbatim.
- **Timing: holds.** D9's typed time is 17:40, while its commit `9d0d2fb` has author time 17:39:17. The typed minute is 43 s late, not a rounding of the commit time. That does not matter here: the commit time is the record, and both come before any call. `results/` holds no p2-3b file, and the gates were shut until this confirmation.

**New gaps: none.** Two notes:
- The gate reads this file from the working tree, so it opens as soon as `confirmed_at` is set. Run the pilot only after the engine session has committed this addendum and `check_prereg.py --before-run` passes.
- `design_review.commit` in the bet row is still null, for the ledger session to fill.

**The pilot may now run**, once this addendum is committed. The test gate opens only on a complete pilot with no refusal (182/182 calls, 0 refusals), and that is enforced in code.

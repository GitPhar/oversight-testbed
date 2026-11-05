---
bet: om-p2-5
program: other-minds
prereg_commit: a29d6ab
seed_commit: fcd1909
reviewer_session: design-review om-p2-5 (fresh subagent launched by the engine session; worktree at fcd1909; no chat, transcript or author message read)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-04 20:09 America/Denver
checks: {D1: holds, D2: flaw, D3: flaw, D4: holds, D5: flaw, D6: holds (no pilot needed; pre-mortem kind world), D7: flaw, D8: flaw, D9: holds, D10: flaw}
flaws: 6
pilot_usd: 0.00
verdict: fix-first
confirmed_at: null
---

# Design review of om-p2-5

## In plain English

The design is sound at its core, and it would answer its question. OWN and SWAP hold the same two numbers in the same two places. The swap baseline rejects plain anchoring. The copy guard rejects a model that just repeats its own answer.

Six things need fixing first, and none of them changes what is tested:
- A model whose own re-rating barely moves, while Sam's rating moves a lot, passes. That is not the model's own view leaking into Sam's.
- The power is overstated. Program 1's archive shows the model's uptake is lumpy from item to item. With that spread, a difference of 0.06 is seen about a third of the time, not 88%.
- The verdict sentences leave out two things: Alex's answer was on screen, and Alex's sentence comes last, just before the question.
- §6 says the position differences work against a pass. Nothing shows that, and the engine's own map (P2-6) leans the other way.
- Any stop before the fifth repeat finishes makes the run untestable. The text implies otherwise.
- A few counts and sources in the text are wrong.

## Checks

All runs used `/Users/seanpharris/entangled-mind/.venv/bin/python`, with scripts in `/private/tmp/claude-501/review-om-p2-5/`. `sandbox.py` replaces `dotenv` with a no-op, deletes every `ANTHROPIC_*` variable, and blocks `socket.connect`, `create_connection` and `getaddrinfo` before it imports `om_common` and `p2_5_egocentric` from the worktree. It printed `ANTHROPIC vars: []` and `socket test: network blocked by review sandbox`. No paid call was made, and no pilot was run.

**D1. The rule can be applied by a stranger: holds.** `d1_rule.py` feeds hand-built point/CI tables to the frozen `rule()`. Each table gave exactly one label: few (11 vignettes); manipulation (self CI low = 0); small (U_sam 0.099, or CI low 0); anchoring (ΔU 0.049, or CI low −0.01); copy (G CI low 0); pass. Each label has its sentence in `SENTENCES`. Edge cases:
- U_sam exactly 0.10 with ΔU exactly 0.05 passes, as §5 says.
- A CI lower end of 1e-10 counts as "not above 0" because of EPS. That is stricter than the text, by a negligible amount.
- A NaN gives a fail, never a pass.

**D2. Every manipulation takes effect: flaw (the text does not match what the run uses).**
- *The knobs work* (`d2_knobs.py`, vignette co05 X):
  - OWN against SWAP differ only in the JSON number in turn 2 and the number in Alex's sentence in turn 3.
  - OWN against REF differ only in turn 2.
  - The content hash changes with the condition, with d, with each of the four questions, and between X and Y.
  - All 7,360 jobs follow the slot rule for their condition.
  - The repeat index is outermost, and every repeat holds the same prompts.
  - The order comes from `seed32_order`.
  - Moving the synthetic own-slot weight on Sam from 0 to 0.3 moves U_sam(OWN) from −0.005 to +0.296.
- *Printed parameters:* `claude-haiku-5-5`, max_tokens 50, `RATE` schema, CAP 1.00, R 5, B 2000, BAR 0.10, MARGIN 0.05. `plan` gives kept cells {0: 32, −60/−30/−10: 25 each, +10/+30/+60: 31 each} and 7,360 calls at about $0.353. All of these match §2–§3.
- *What does not match:*
  - **"1,472 distinct prompts" is wrong.** Per repeat there are 1,472 jobs but only **1,328 distinct message hashes**. In 144 jobs, the 30- and 60-point displacements clip to the same planted value (for example `co01|X|OWN|30|*` and `co01|X|OWN|60|*` are both own = 98, Alex = 85). Those identical prompts are called separately, and each one counts in its own nominal class.
  - **The 60 class is nominal.** 31 of its 56 cells are displaced less than 60 points (median 53, minimum 5). In the 30 class, 15 of 56 are displaced less than 30. This is F3's convention, but §4 does not say so.
  - **The anchors are misdescribed.** §2 says m is the "run-2 first-turn mean". In `exp4-run-3-anchors.json`, 7 vignettes use run-2 first-turn means and 9 use run-1 phase-1 means (all Haiku).
  - **"Alex's is the model's usual rating" (§1) is approximate.** Against bm0's measured free rating, m is within 5 points for 26 of 32 statements and up to 13 points away (co-lin09 Y: m 44, free rating 57).
  - **REF is not an unplanted rating.** §4 and §6 call it "today's unplanted rating", but both of its slots hold m.

**D3. Every control can fail: flaw.**
- *The SWAP baseline* rejects a source-blind anchor. My responder E (own 0.2, Alex 0.2) gives ΔU −0.004, fail (anchoring). The dry run's source-blind and recency anchors are rejected too.
- *The copy guard* rejects a copier. My responder C (Sam = the model's own re-rating) gives G +0.003 [−0.004, +0.011], fail (copy).
- *The manipulation check* rejects a plant that does nothing. My responder F (self 0, Sam 0.3) gives untestable (manipulation).
- **It does not reject the wrong set-up its own stated reason names.** §5.2 says a pass needs "a shift of its own for Sam's to inherit". The check only asks that the CI of U_self(OWN) be above 0. Responder G (self uptake 0.02, Sam 0.15, informed Sam 0.30) gives:
  - U_self **+0.017** [+0.011, +0.023];
  - U_sam **+0.145** [+0.138, +0.150];
  - ΔU +0.146, G +0.154;
  - label: **pass**.

  Here Sam's rating moves 8.5 times as much as the model's own. That is anchoring of Sam's rating on the planted number, not the model's own (re-rated) view carried over. Yet the bet's title asks whether "the model's own credence" pulls Sam, and §6 defines that credence as the re-rating. Fix 1.

**D4. Rivals are matched: holds.** The two accounts are own-answer leakage and Alex's answer read as evidence about what a person would say. Both can be written as responders, and the rule tells them apart in both directions:
- leakage without Alex's pull passes (responder A, dry-run λ 0.25 and 0.5);
- Alex's pull equal to the own pull fails (anchoring) (responder E, dry-run "leak plus Alex").

Neither wins by construction. The number set is symmetric, both conditions share REF, and there are no fitted families. The one asymmetry (turn and format) belongs to D7.

**D5. A dumb baseline is beaten, and the design can see the effect: flaw (the power claim).**
- *Dumb baselines.* Constant, re-derive, last-number, source-blind, recency, own-slot copier and no-manipulation all fail or are untestable. That holds in the author's table and in mine.
- *My other responders* (`d3d5_responders.py`, `d5_more.py`):
  - Hedging Sam 6 points toward 50 when the model's own answer looks odd (H): fail (small), U_sam −0.032.
  - Hedging whenever the two numbers disagree (I): fail (small).
  - An agreement-extremity drift (L): fail (small).
  - Pushing Sam away from Alex with no own pull (J): fail (small), even though ΔU is +0.140.
  - True leakage λ 0.3 with Sam's answers rounded to multiples of 5 (M): pass, so coarse answers do not hide a real effect.
  - Noted, not a flaw: a fixed 4-point nudge toward the own slot (K) scores U_sam **+0.242**. The statistic gives most weight to small displacements. See fix 4(b).
  - Noted, not a flaw: if Alex *repels* Sam (B: own 0.11, Alex −0.10), the margin stops binding. ΔU is +0.203 on a U_sam of only 0.105. The sentence is still true, and U_sam(SWAP) is reported with its CI.
- *Power.* §4's table uses smooth heterogeneity (a vignette factor 1 + N(0, 0.5), per-call SD 1 point) and says "the design can see a ΔU of about 0.06 or more". Program 1's archive contradicts that noise model.
  - In bm0's 162 own lag-0 cells, per-cell uptake is lumpy. At ±10, 62% of cells are above 0.9 and 16% are near 0. At ±60, 52% are near 0. The SD is 0.34–0.43.
  - `power.py` uses the frozen `uptake_table`/`boot`/`rule`, with each cell's own uptake set to **bm0's archived value for that statement and d**. Sam(OWN) = λ × that value + noise; Sam(SWAP) = α + noise. 60 runs per cell, 400 resamples.

  | setting (σ Sam, σ Alex, REF SD, call SD) | α 0, λ 0.25 (U_sam ≈ 0.11) | α 0.1, λ 0.35 (ΔU ≈ 0.06) | α 0.1, λ 0.5 (ΔU ≈ 0.13) | α 0.1, λ 0.75 (ΔU ≈ 0.24) |
  |---|---|---|---|---|
  | author-like (0.1, 0.1, 0.5, 1) | 0.90 | 0.68 | 1.00 | 1.00 |
  | moderate (0.3, 0.3, 2, 3) | 0.72 | 0.33 | 0.83 | 1.00 |
  | bm0-like (0.43, 0.6, 3, 5) | 0.47 | 0.25 | 0.53 | 0.95 |

  - Even at the author's own noise, real lumpiness drops power at ΔU ≈ 0.06 from 0.88 to 0.68. Under bm0-like spread it is 0.25.
  - At λ = 0 the false-pass rate is 0–2% (1 of 60 runs, bm0-like). The bar holds.
  - This is not a null rule, so a fail stays honestly worded. But §4's power sentence is false as written, and the odds rest on it. Fix 2.

**D6. Foreseeable execution risks are piloted: holds; no pilot required.**
- The pre-mortem's kind is `world`.
- The first turn, the schema and the items are bm0's, which ran 3,650 conversations with no refusal (checked in `bm0-source-distance-lag.md`). The new third-turn text (Alex, Sam, "another instance of you") is benign.
- max_tokens 50 is far above `{"probability": nn}`. `_check_stop` turns max_tokens into an error stop, which can be resumed.
- Cost: bm0's archived own lag-0 conversations cost $9.46e-5 for two calls. At $0.10/$0.50 per million tokens, that is about 440 input tokens per call, close to this design's prompts. The estimate of about $0.35 against a $1.00 cap is sound.

**D7. Comparisons match: flaw.** Diffing the messages shows OWN and SWAP differ only in which slot holds V. That bundles four things: the number's source, its turn, its format, and its place (Alex's sentence comes just before the question). §6 lists all four. But:
- the pass sentence names only "whose number it is, its turn and its format", and leaves out recency;
- §6 says points 2–4 "favour Alex's slot under plain anchoring, so they work against a pass". Nothing in the record supports that. In F3, the own-over-other gap of +0.46 came with turn and format confounded with source. The engine's own map P2-6 says "the engine leans toward position: the model is continuing the assistant turn". And responder A, which anchors on the assistant turn alone (0.2 on every Sam question, plus 0.2 when Sam is said to have seen the answer), **passes**: U_sam +0.195, ΔU +0.196, G +0.204.

The bias of the bundle may well favour a pass. Fix 3.

**D8. The verdict sentences are written: flaw.** All seven sentences exist and avoid "belief", "theory of mind" and the rest. Two nouns overreach:
- **(a) Alex's answer was in view.** In OWN, Alex's answer (at the archived anchor) is shown just before the question. The map's arm (b) had no other reader. Yet the fail (small) sentence and `map_rule` ("the map's rule alone on these data") read as the map's event. A fail (small) here does not say what the map's design would have shown. An answer at m, shown as a person's, could hold Sam's rating at m.
- **(b) "Points per point of displacement" needs its qualifier.** The number is an average over three nominal classes, and the 10-point class and the clipped cells weigh most. A fixed 4-point nudge scores 0.24 "points per point" (responder K).

Fix 4.

**D9. One item cannot decide it: holds.** Leave-one-vignette-out is pre-registered (§4) and re-applies the full rule. §5.7 says the label stands with a `fragile` note naming the vignette, and `analyse_tables` computes `loo_flips` the same way. One code edge: with exactly 12 complete vignettes, every leave-one-out run falls below the 12-vignette floor. My run with 12 complete and a clear pass gave **all 12 flips → fragile**. With 13 complete it gave no flips. D10 shows the run can only end with 0 or 16 complete vignettes, so this edge cannot occur in practice. The one-line fix is in fix 5(c).

**D10. Machinery: flaw.** `d10_machinery.py` uses temporary result folders.
- *Holds:*
  - Refusal: a stub refusal at call 3,000 stopped the run. 6 calls in flight finished and were counted (`completed_after_stop: 6`, `resumable: false`). The refused key and `refusal.md` were written, and a re-run made 0 calls.
  - Error and resume: an error stopped the run after 99 calls, and the resume made exactly the remaining 401.
  - Cap: at a $0.05 cap the run stopped at $0.057, so it overshoots by at most the in-flight calls (8 workers).
  - Cache: the content hash is asserted on every hit and re-checked in `verify_cache`.
  - Gate: closed for a missing file, for fix-first with `confirmed_at: null` and for redesign. Open for go, or for a confirmed fix-first, when read from a header in this file's format.
  - Scale: one direction everywhere (`SCALE`).
  - Seed: `ledger/seed.py` on the recorded randomness gives order 2724043733722698475 / seed32 3710620395 and boot 17948192035247956964 / seed32 4252181476, as recorded. Pulse 19:54:00 is after the commit's author time of 19:53:53, and the previous pulse (19:53:00) is before it. The seed commit changes only the seed line and `data/p2-5-seed.json`.
  - Lesson: `check_prereg.py` L1–L3 pass, and §0 at `a29d6ab` matches `ls-om-p2-5` character for character.
- **(a) A malformed value is not caught.** `int(d_["probability"])` runs outside the `try`. A stub that returned `"seventy"` on its 5th call raised an uncaught `ValueError`. `Executor.map` cancelled the queue after 187 calls, `stop` was never set, and nothing was written to disk: no cache file and no stop record. The real run would lose up to 249 paid calls and log nothing, though §7 says "the error is logged". Structured output makes this unlikely, but the code does not do what §7 says.
- **(b) Any stop makes the run untestable.** A cell needs all five repeats, and each repeat's random order spans every vignette. A stop after 90% of the calls left **0 of 16** vignettes complete, so the result is untestable (too few). §3's "a stop leaves whole repeats" and §7's "the analysis runs on complete vignettes" imply something the analysis never does.
- *Notes, not flaws:*
  - The cache hash leaves out the schema, thinking and temperature settings. They are constants in code.
  - The read block in `ls-om-p2-5` matches the ledger at `1e8b2af` (14 scored, Brier 0.246, 5/14), not at `a29d6ab` (15 scored, Brier 0.267, 6/15; running 7/17 = 0.41). §0 says so ("read at 1e8b2af"), and so does the ledger `read_note`. The move from 0.30 to 0.33 is toward both base rates.
  - The §0 lesson cell is 91 words in five sentences, against learn.md's "one sentence of 60 words or fewer". It matches exactly and passes the checker.

## Required fixes

All fixes go in one dated DEVIATIONS row in `programs/other-minds/DEVIATIONS.md`, written before any call. Use the next free number (D12 at this writing; D11 and D11b are taken), titled **"om-p2-5 design-review fixes, ledger/design-reviews/om-p2-5.md"**. Each fix tightens the design or makes the record accurate; none lowers the bar. The odds may be re-stated before data, with all numbers kept.

1. **F1 (D3): add a fail for a pull on Sam that is not inherited.**
   - In §5, after step 5, add: **"5b. Fail (not inherited)** unless U_sam(OWN) ≤ U_self(OWN) (point)."
   - In `rule()`, after the copy check, add: `if not point["U_sam_own"] <= point["U_self_own"] + EPS: return "fail", "not_inherited"`.
   - Add `SENTENCES["fail_not_inherited"]` and the same text to §5: "On Haiku, on program 1's 16 vignettes, with another reader's answer also shown, the model's own planted answer pulled the rating it attributed to Sam more than it pulled the model's own re-rating, so the pull on Sam cannot be the model's own shifted rating carried over to Sam."
   - Scored 0.
   - Add responder G (self 0.02, Sam 0.15, informed Sam 0.30) to `p2_5_dryrun.py`'s baselines and commit the new output.
   - Append the conjunct "and U_sam(OWN) ≤ U_self(OWN)" to `odds_event` in §8 and in `ledger/bets.jsonl`.
2. **F2 (D5): replace the power claim with one built on program 1's archive.**
   - Add to the dry run a power grid in which each displaced cell's own uptake is bm0's archived lag-0 own uptake for that statement and d (`results/bm0-source-distance-lag.json`, `rows`). Sam(OWN) = λ × that value + N(0, σ); Sam(SWAP) = α + N(0, σ_a). Run at least the "moderate" and "bm0-like" settings above, at α ∈ {0, 0.1} and λ ∈ {0.25, 0.35, 0.5, 0.75}. Commit the output.
   - In §4, delete "The design can see a ΔU of about 0.06 or more." Replace it with the grid's numbers, for example: "With bm0's lumpy per-statement uptake, a true ΔU of about 0.06 is detected in 25–68% of runs and about 0.13 in 53–100%; the design reliably sees ΔU ≈ 0.24."
   - If the engine re-states the odds, it records both numbers and gives the reason.
3. **F3 (D7): name the whole bundle, and drop the unsupported direction.**
   - In the pass sentence (§5 and `SENTENCES["pass"]`), replace "differ in whose number it is, its turn and its format together" with "differ in whose number it is, its turn, its format and its place in the conversation (Alex's answer comes just before the question) together".
   - In §6, replace "Points 2–4 favour Alex's slot under plain anchoring, so they work against a pass, not for one." with: "Which way points 2–4 lean is not known. Recency may favour Alex's slot. The assistant turn and the JSON format may favour the model's slot: F3's own-over-other gap had turn and format confounded with source, and map P2-6 leans toward position. A synthetic responder that anchors on the assistant turn alone passes this rule (design review, responder A)."
4. **F4 (D8): make the sentences carry the design's scope.**
   - (a) In the pass, fail (small), fail (anchoring), fail (copy) and fail (not inherited) sentences, insert "with another reader's (Alex's) answer also shown" after "on program 1's 16 vignettes,".
   - In §0's odds row, after "the map's event", add "(measured here with Alex's answer in view, which the map's design did not have)".
   - Rename what `map_rule` reports, in §5.8 and in the results template, to "the map's event measured on this design (another reader's answer in view)".
   - (b) In the pass and fail (small) sentences, replace "by at least 0.10 points per point of displacement" with "by at least 0.10 points per point of displacement, averaged over the 10-, 30- and 60-point classes".
5. **F5 (D10): fix the stop and parse machinery.**
   - (a) In `GuardedCaller.run`, move `v = int(d_["probability"])` and the clip inside the `try`, so that a malformed value takes the error path (stop set, stop record written, resumable).
   - (b) Add to §3 and §7: "A cell needs all five repeats, and each repeat spans every vignette, so any stop before the last repeat completes leaves no complete vignette and the result is untestable (too few). The repeat-outermost order serves only a resumed run." Delete "If it is reached, the later repeats are reported as not run, and the analysis runs on complete vignettes (§5.1)", or reword it to match.
   - (c) In `analyse_tables`, apply the floor to the run, not to the n − 1 subsample: `l2, r2 = rule(p2, c2, len(idx))`.
6. **F6 (D2): correct the text to match what the run uses.**
   - §2 and §3: "1,472 distinct prompts" → "1,472 prompts per repeat, 1,328 of them distinct (in 144 the 30- and 60-point displacements clip to the same planted value; they are called separately and each counts in its own nominal class, as in F3)".
   - §4: add "Distance classes are nominal |d|; in the 60 class, 31 of 56 cells are displaced less than 60 points (median 53)."
   - §2: "m = round(the model's run-2 first-turn mean)" → "m = round(the archived anchor in `exp4-run-3-anchors.json`: run-2 first-turn means for 7 vignettes, run-1 phase-1 means for 9, all Haiku)".
   - §1: "Alex's is the model's usual rating" → "Alex's is the archived anchor, within 5 points of the model's free rating in bm0 for 26 of 32 statements".
   - §4 and §6: "today's unplanted rating" → "the REF re-rating (both slots at m)".

**Pilot.** None required (D6). pilot_usd 0.00.

**Confirmation.** After the author commits the fixes and the DEVIATIONS row, the reviewer re-runs `p2_5_dryrun.py` and this review's scripts under the stub: `d1_rule.py`, `d2_knobs.py`, `d3d5_responders.py`, `d5_more.py`, `power.py` and `d10_machinery.py`, which sit in `/private/tmp/claude-501/review-om-p2-5/` and are re-creatable from this file. The reviewer then checks that responder G fails (not inherited), that the parse stub writes a stop record, and that the LOO edge no longer flags all 12 vignettes. It then adds a short addendum here with `confirmed_at`.

---
bet: om-p2-6
program: other-minds
prereg_commit: 9590b92
reviewer_session: fresh design-review subagent launched by the om-p2-6 session
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-04 20:10 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: flaw, D6: holds, D7: holds, D8: flaw, D9: holds, D10: flaw}
flaws: 3
pilot_usd: 0.00
verdict: fix-first
confirmed_at: 2026-11-04 20:32 America/Denver
---

# Design review of om-p2-6

## In plain English

As built, the test would mostly answer its question. The cells differ exactly as the pre-registration says. The dumb predictors (copy any number, position only, recency, noise) fail the rule, and the beacon seed reproduces from a fresh fetch. Three things have to change before the first call:
1. **Two frozen verdict sentences can be false for tables the rule sends to them.** The most likely mixed outcome (label 0.25, position 0.30) goes to "fail, position" in about two runs in three. In about 60% of runs the label effect also clears 0.15 with its interval above 0, yet the frozen sentence says the pull follows the turn "not whose answer it is said to be".
2. **The uptake measure can read a shift that ignores the shown number as uptake.** Clipping at 2/98 drops pairs that point toward the extreme. What is left points toward the middle on net in 7 of 16 items. So a "yours"-only drift toward 50 that does not depend on the shown value passes the rule 30% of the time at a drift of 0.5 and 57% at 0.8. Comparing the +30 and −30 displays directly removes this leak at no cost in power.
3. **The stop-on-refusal check has a race.** In a stubbed run, 7 calls started after a refusal had been raised.

Each fix tightens the design without changing what it tests.

## Checks

Everything below ran in the worktree `/Users/seanpharris/oversight-testbed-review-om-p2-6` (detached at the seed commit `482f4e4`), with `env -u ANTHROPIC_API_KEY python3`. Nothing imported `om_common` or called `real_call()`, and no `.env` was loaded. Scratch scripts are in the session scratchpad, not the repo. Paid calls: none. Pilot: none.

**D1. The rule can be applied by a stranger: holds.**
- I re-implemented §5 from its prose and compared it with `verdict()` on 200,000 random tables (L, P and CIs on a 0.01 grid). There were 0 mismatches, and the if-chain returns exactly one verdict for every table.
- Edge cases:
  - L = 0.15 exactly, also as `0.1 + 0.05` and as `0.15 − 1e-12`, gives pass: the 1e-9 tolerance works as §4 says.
  - L = |P| = 0.20 with P detected gives fail-position (ties go to position). With P not detected it gives fail-mixed.
  - Negative P is handled by `abs`: L 0.20 against P −0.19 detected gives pass, and against P −0.20 detected gives fail-position.
  - P exactly −0.15 detected, with L 0.10, gives fail-position.
  - L exactly −0.15 with its upper end below 0 gives fail-reversed.
  - A CI lower end of exactly 0 gives fail-neither (not > 0).
- Untestable: fewer than 10 complete repeats gives untestable (dry run: 9 gives untestable, 10 is analysed). Fewer than 12 usable items gives untestable.
- The rule is mechanical and unambiguous. The truth of its sentences is a separate question (D8).

**D2. Every manipulation takes effect: holds.**
- `p2_6_dryrun.py` re-run in the worktree reproduces the committed `p2-6-dryrun-output.txt` line for line. The one exception is the "gate now" line, which names this worktree's missing review instead of the then-missing seed file.
- The printed conversations (co01 X, d = −30, A = 55) show:
  - `base` is exactly the first user message of AY/AS.
  - AY and AS differ only in "your" against "Sam's".
  - UY, US and UU differ only in "your", "Sam's" and "my".
  - The value string appears once in each cell, and the request sentence is identical in all five.
- The shown value is computed once per (statement, direction) and shared by all five cells.
- The run-order seed `seed32_order` and the bootstrap seed `seed32_boot` (+1 for the swap null) are the ones the code reads from `data/p2-6-seed.json`.
- The d = ±30 knob moves A: 41 of 64 displays sit at the full 30 points, and 8 are under 5 points after clipping. The synthetic scenarios show that every cell's uptake moves the statistic.

**D3. Every control can fail: holds.**
- Wrong set-ups the rule must reject:
  - constant copy: passes 1%;
  - position only (bm0's 0.44 / −0.11): fail-position 100%;
  - recency: fail-position 100%;
  - noise: passes 1%.
- The machinery fails correctly when set up wrong:
  - the cap stops the run at $0.01;
  - a refused job is written to the cache, and a re-run exits whether or not `refusal.md` is still present;
  - a tampered cache hash is caught;
  - the gate refuses to open on a missing seed file, a missing review, a `fix-first` with `confirmed_at: null` (even when the body says "verdict: go"), or a `redesign`. It opens on `go`, or on `fix-first` with a date.
- The "no own pull" sentence (u_AY CI ≤ 0) is the manipulation check. It cannot make the bet untestable. That is acceptable here, because the scored event is the label effect itself, and with no uptake anywhere that event is truly absent.

**D4. Rivals are matched: holds.** No fitted rivals. L and P are symmetric contrasts of the same four cells, each with two differences of the same cells. Both can win in the dry run (label-only passes 1.00, position-only gives fail-position 1.00). The pass bar is asymmetric only in that ties go to position, and the pre-registration says so.

**D5. A dumb baseline is beaten, and the design can see the effect: flaw (F2).**
- Not a null rule. Power holds up on bm0's item spread (dry run: 0.88 at a label effect of 0.25, 0.40 at the margin), and the four named dumb predictors fail (D3).
- What I tried against the brief's list:
  - **The word "again"** is in every cell, so it cannot by itself produce L. Its meaning shifts with the label: it asks for a repeat only when the answer is "yours". That is part of the label bundle, which the verdict sentences call "whose answer the transcript says it is". See note n4.
  - **Recency** differs only between positions, so it loads on P, not L.
  - **The baseline measured in the same run** cancels from every L and P difference. It enters only through the |D| weights and the drop rule, which are the same in every cell.
  - **Ratio-of-sums with small |D|** does not blow up: every item's Σ|D| is at least about 0.4 on the archive.
  - **Distrust of "Sam"** passes the rule (dry run: 1.00). The pre-registration discloses this (§1, §6), the fifth cell reads it as a secondary, and the pass sentence claims only "whose answer the transcript says it is", which Sam-distrust is. Acceptable; see n5.
- **The flaw: clipping plus the sign-weighted, baseline-referenced uptake lets a shift unrelated to the shown value read as uptake.**
  - On the archived run-3 baselines (`exp4-run-3-calls.json`, `X->XY`/`Y->XY` r1), 8 of 64 pairs fall under |D| < 0.05 and are dropped. Every dropped pair is the one pointing toward the nearer extreme.
  - So in 7 of 16 items the kept pairs point toward 50 on net. In six of them Σ sign(D) = +1 over the kept pairs (co01, co-lin08, co-lin10, co05, co10, co11). In co02 the only kept pairs are X−30 and Y+30, both pointing toward 50.
  - A cell-specific move of fraction k toward 50, the same whatever value is shown, adds about 0.31·k to that cell's measured uptake (archive mean of Σ sign(D)(0.5 − b)/Σ|D|).
  - Hedging toward 50 when told "this is your earlier answer, give the rating again" (the "are you sure?" reading) is a plausible behaviour that is not uptake of the shown number.
- Stubbed synthetic check (`d5_leak.py`, 60 runs each, the dry run's generator plus a hedge term):

| scenario | primary rule: pass | mean L | slope-measure mean L | slope rule: pass |
|---|---|---|---|---|
| uptake 0.2 in every cell, "yours" cells hedge 0.5 toward 50 | 0.30 | +0.116 | −0.002 | 0.03 |
| same, hedge 0.8 | 0.57 | +0.213 | +0.010 | 0.03 |
| label 0.25, no position, no hedge (power) | 0.90 | +0.231 | +0.241 | 0.92 (both rules: 0.90) |
| label 0.25, position 0.30 | 0.33 | +0.240 | +0.247 | 0.37 (both: 0.32) |

  The slope measure is the shift-invariant uptake: per item, Σ over statements with both directions kept of (r̄₊₃₀ − r̄₋₃₀) / Σ (A₊₃₀ − A₋₃₀). It ignores any shift that does not depend on A, and on these data it costs no power. On the archive, 15 of 16 items have at least one statement with both directions kept; only co02 has none.

**D6. Foreseeable execution risks are piloted: holds.**
- The pre-mortem is of kind `world`. The items are program 1's 16 vignettes, run in about 9,000 Haiku conversations with no refusal. The new wording (an owner sentence and a JSON value in the user turn) carries no refusal-prone content. No pilot is needed.
- Cost: about 250 input tokens a call at $0.10/M plus about 10 output tokens at $0.50/M is about $3e-5 a call, or about $0.25 for 7,040 calls. That is well inside the $0.80 cap, so the cap cannot cut the run below 10 repeats.
- `max_tokens` 200 with a one-integer schema. A max_tokens stop raises an error, which is resumable.

**D7. Comparisons match: holds.**
- L compares AY with AS and UY with US. Each pair differs in one owner word only (checked on the printed strings).
- P compares a bundle, and §6 lists it:
  - three messages against one;
  - the label in a later message than the value, or in the same one;
  - recency.
  To that list add: in the user cells the model has given no earlier rating for "again" to refer to (n4). The verdict sentences say "the turn it sits in", which is that bundle.
- Label coherence (AY and US coherent, AS and UY not) cancels from both L and P and goes into the interaction term. Same model, settings, schema, items, values and date in every cell.

**D8. The verdict sentences are written: flaw (F1).**
- All §5 sentences are frozen in `SENTENCES` and match §5 word for word. They use only nouns the design carries: Haiku, the 16 bm0 items, ±30, uptake of the displacement, label, turn. No "self-model", "belief" or "commitment".
- Two sentences are false for some tables the rule sends to them:
  - **fail-position** ends "follows the turn it sits in, not whose answer it is said to be". The rule reaches it whenever |P| ≥ |L|, including when L ≥ 0.15 with its CI above 0. Example: L = |P| = 0.20, both detected, gives fail-position with "not whose answer". In the dry run's own "label 0.25, position 0.30" scenario, 60% of runs are fail-position with L ≥ 0.15 and its CI above 0 (`d5_leak.py`).
  - **fail-neither** says "neither the label nor the position changed uptake by the pre-registered 0.15". The rule also reaches it when:
    - L = 0.30 [−0.01, 0.60] and P = 0.20 [0.05, 0.35] (P detected and ≥ 0.15);
    - L = −0.30 [−0.45, −0.15] and P = 0.35 [−0.05, 0.75] (L detected and ≤ −0.15);
    - L = 0.30 [−0.01, 0.60] and P = 0.10.

    On the 200,000-table grid, 3,051 fail-neither tables have L or P at least 0.15 in size with its CI excluding 0.
- The pass, reversed, mixed, untestable, no-own-pull, fragile and fifth-cell sentences are true for every table that reaches them.

**D9. One item cannot decide it: holds.** Leave-one-item-out is pre-registered, re-applies `verdict()` with its own bootstrap, and appends a frozen sentence on a flip. The bet is scored on the full data. Notes n2 and n3 are minor gaps against the §5 text.

**D10. Machinery: flaw (F3).**
- **Budget:** `CAP` 0.80, checked under the lock before every call against the cumulative cache. Overshoot is at most the 8 calls in flight.
- **Stop-on-refusal: race.** In `GuardedCaller.run.work`, `self.stop` is checked before the lock is taken, but not again inside it. In the refusal handler, `self.stop.set()` runs after the lock is released. A worker that passed the first check and was waiting on the lock (held for `spent()`, a sum over up to 7,040 entries) makes a new call after the refusal.
  - With `spent()` slowed by 3 ms and the refusal at call 20 (`d10_race.py`), 7 calls started after the refusal was raised. They were logged as "calls already in flight", which they were not.
  - With the fix in F3 applied to a scratch copy (`d10_race_fixed.py`), 2 remained. Those are calls that had already cleared the gate before the refusal was recorded, which is genuinely in flight.
  - CONTEXT §3 rule 3: "no new call starts".
- **One scale direction:** "0 = certainly false and 100 = certainly true" in every prompt.
- **Caching:** content hash of model, `max_tokens` and messages, asserted on every hit and re-verified in the analysis (tamper caught). See n1.
- **Beacon seed:** holds, checked against the beacon itself.
  - The 24-hour rule: CURBY-Q's latest completed round 28297 (2025-08-22) is stalled, so CURBy-RNG.
  - I fetched afresh with `@buff-beacon-project/curby-client@1.2.0`, installed `--ignore-scripts` in the scratchpad, using `curby_seed.mjs rng 2026-11-04T19:55:35-07:00`. It returns pulse 1591640 at 2026-11-05T02:56:00.203Z (19:56:00 America/Denver). The previous pulse, 1591639, is at 19:55:00, before the pre-registration's author time of 19:55:35. So 1591640 is the first pulse after the commit, and its randomness is identical to `data/p2-6-seed.json`.
  - `ledger/seed.py` reproduces seed 97549812358230771, `order` 5841281319203805541 (seed32 1346672997) and `boot` 72829155383338239 (seed32 535454975), all as recorded and as the code reads them.
  - The seed commit `482f4e4` changed only the seed file and the §2 seed block that the pre-registration says it fills.
- **Gate:** works as §0 states (D3). The code reads the review at `<checkout>/ledger/design-reviews/om-p2-6.md`, so the run must start from the main checkout.
- **Lesson:**
  - 60 words, exactly at the limit. It names P8, P3 and P1, and its design change can be checked.
  - The odds move away from the base rate, with a reason from the ledger: om-p2-3b's audited reversal, +0.060 against +0.114 (checked in `ledger/audits/om-p2-3b.md`), and program 2's 0 hits in 3 scored bets. bm0's ±30 numbers (+0.44, −0.11, +0.55 [+0.26, +0.92]) match `bm0-source-distance-lag.json`.
  - `check_prereg.py` reports L1, L2 and L3 as ok.
  - The proof of reading is stale. It was read at `dd7cab3` (14 scored, Brier 0.246, running 6/16 = 0.375). At `9590b92` the ledger held 15 scored, 6 hits, Brier 0.267, running 7/17 = 0.41, after ss-b5 was scored at 19:53:21. The newest audit is unchanged (ss-b1.md). `ls-om-p2-6` carries a `read_note` saying exactly this, following om-p2-5's precedent. The odds argument survives: 0.25 is further below 0.41 than below 0.375, for an unchanged ledger reason. Acceptable; no `lesson_revised` needed.
- **DEVIATIONS numbering:** acceptable. Rows are never edited. D11b (`2031255`, 19:56:57) is dated, written before any om-p2-6 call, and assigns om-p2-6's prereg row to D11b and its later rows to D11c onward. The two D11 rows can be told apart by content (om-p2-5's is first). The ledger row's `deviation` already reads "D11b (numbered D11 in the pre-registration; see D11b)". The fix rows below therefore use D11c to D11e.

## Required fixes

Each is written in programs/other-minds/DEVIATIONS.md before any call, names this review, and is applied to `experiments/p2_6_position_label.py`, with the dry run re-run and its output re-committed. The reviewer then confirms them in an addendum here.

**F1 (D8): make the fail-position and fail-neither sentences true for every table that reaches them. DEVIATIONS row D11c.**
- In §5 rule 3 and `SENTENCES["fail-position"]`, replace "On this design the pull of an earlier answer follows the turn it sits in, not whose answer it is said to be." with "On this design the pull of an earlier answer follows the turn it sits in at least as much as whose answer it is said to be."
- Add a frozen sentence `label_also`, appended after the fail-position sentence when L ≥ 0.15 with its CI lower end > 0, or when L ≤ −0.15 with its CI upper end < 0: "The label effect, {L}, also reached the pre-registered 0.15 of the displacement with its 95% interval excluding 0."
- In §5 rule 6 and `SENTENCES["fail-neither"]`, replace "neither the label nor the position changed uptake by the pre-registered 0.15 of the displacement: label effect {L}, position effect {P}." with "neither the label nor the position met the pre-registered rule for it (an effect of at least 0.15 of the displacement, its 95% interval excluding 0, and larger than the other, ties going to the position): label effect {L}, position effect {P}."
- No verdict category, threshold or score changes.

**F2 (D5): the pass must also hold on the shift-invariant uptake. DEVIATIONS row D11d.**
- Define u_s per item and cell. Over the item's statements with both directions kept (|D| ≥ 0.05 at both −30 and +30), compute Σ (r̄₊₃₀ − r̄₋₃₀) / Σ (A₊₃₀ − A₋₃₀), with ratings and A on 0–1 and the same first-nrep complete repeats.
- Compute L_s and P_s from u_s exactly as L and P are computed, with the same bootstrap (`seed32_boot`, B = 2,000, item resampling).
- Rule 2 (pass) adds: "and L_s ≥ 0.15, the CI lower end of L_s > 0, and L_s > |P_s|".
- If rule 2 holds on the frozen measure but the L_s conjunct fails, the verdict is **fail, shift** (scored 0), decided before rules 3–6. Its frozen sentence: "On Haiku, on program 1's 16 bm0 items at ±30 points, the label effect on the pre-registered uptake measure, {L}, did not hold on the measure that compares the +30 and −30 displays directly ({L_s}; position effect {P_s}), so it may come from a change in the rating that does not follow the shown number. This test does not say which of the two the pull of an earlier answer follows."
- Untestable (rule 1) adds: fewer than 12 items with at least one statement having both directions kept. On the archive, 15 have.
- Report L_s and P_s with CIs in every case. Apply the same conjunct in leave-one-item-out.
- Add two dry-run scenarios: "uptake 0.2 everywhere, 'yours' cells hedge 0.5 toward 50" must pass at most 5%, and the power line at label 0.25 must be re-reported under the full rule.
- This tightens the bar and never lowers it. The odds may be revised before data, with both numbers kept. On the stub, power is unchanged (0.90 against 0.90).

**F3 (D10): no call may start after a refusal. DEVIATIONS row D11e.**
- In `GuardedCaller.run.work`, inside `with self.lock:` and before the cap check, add `if self.stop.is_set(): return`.
- In the `except refusal_error` branch, move `self.stop.set()` inside its `with self.lock:` block. Do the same for the generic `except Exception` branch: append to `self.errors` and call `self.stop.set()` under the lock.
- Add a dry-run check that slows `spent()` (for example 3 ms) and raises the refusal at call 20. It must show that the only calls entering `call_fn` after the refusal are those that cleared the locked gate before it was recorded. The current code shows 7 such calls; the fix should show at most `workers − 1`.

## Notes (not blocking)

- **n1.** `content_hash` hashes this file's `MODEL`, but `real_call()` relies on `om_common.structured`'s default `model=MODEL` from `om_common`. They agree (`claude-haiku-5-5`), but are not tied together. Passing `model=MODEL` in `real_call()` would make the hash cover the model actually called. If done, log it in D11e.
- **n2.** Leave-one-item-out calls `verdict()` without the 12-item untestable rule. That only matters if exactly 12 items are usable; the archive suggests 16.
- **n3.** §5 says a fragile result is labelled "<verdict>, fragile (one item)". The code writes `fragile_sentence` and the flip count, but no such label. The results file must write it by hand.
- **n4.** "Please give the rating again" asks for a repeat only when the answer is "yours". Under "Sam's" and "my", and in the user turn, the model has given no earlier rating for "again" to refer to. A label effect may therefore partly be the model following a repeat instruction. Suggested §6 sentence in D11c: "'Again' asks for a repeat only when the answer is labelled 'yours'; a label effect may partly be the model following that reading."
- **n5.** A pass caused by distrust of "Sam" is still a pass. The fifth-cell sentence is the only thing that flags it, and with 16 items its power is low (the dry run's Sam-distrust scenario gives `user_like_yours` 0.91; others mostly `user_unclear`). The results write-up should not read a pass as being about "the self" unless `yours_over_user` fires, and even then, given n4, only cautiously.
- **n6.** The reviewer was launched by the author's own session as a subagent. Its independence is weaker than that of an engine-launched reviewer, and it is from the same model family.

Commands and scratch files (session scratchpad):
- `p2_6_dryrun.py` re-run → `dryrun.txt`, diffed against the committed output.
- `d1_verdict.py`: edge tables and the 200k grid.
- `d5_leak.py 60`: hedge leak and slope measure.
- `d10_race.py` and `d10_race_fixed.py`.
- `ledger/seed.py` ×3.
- `curby_seed.mjs rng`: fresh fetch.
- `ledger/check_prereg.py om-p2-6 . programs/other-minds/experiments/p2-6-position-or-label.md`: L1–L3 ok; R1 failed only because this file did not exist yet.

## Addendum: fixes confirmed (2026-11-04 20:32 America/Denver)

I checked fix commit `f0606f7` (rows D11c, D11d and D11e in programs/other-minds/DEVIATIONS.md, dated 20:22, committed 20:23). The p2-6 files at HEAD match that commit. `programs/other-minds/results/` holds no p2-6 file, so every row comes before any call. Every check below ran with every call stubbed and no key. Paid calls: none.

- **F1 (D11c): confirmed.**
  - `SENTENCES["fail-position"]` now ends "…follows the turn it sits in at least as much as whose answer it is said to be". That is true for every table the rule sends there (|P| ≥ |L|).
  - `label_also` is appended exactly when L ≥ 0.15 with its CI lower end > 0, or L ≤ −0.15 with its CI upper end < 0. It fires in 60% of runs in the "label 0.25, position 0.30" case (`d5_leak2.py`).
  - `fail-neither` now says neither effect "met the pre-registered rule for it". That is true by construction for every table that reaches it, including the 3,051 grid tables the old wording got wrong.
  - The §6 sentence on "again" (n4) was added.
  - Re-run `d1_verdict2.py`: 0 mismatches against the §5 prose on 200,000 tables. The edge cases give the same verdicts as before. No category, threshold or score changed.
- **F2 (D11d): confirmed.**
  - u_s is coded as specified: statements with both directions at |D| ≥ 0.05, Σ(r̄₊₃₀ − r̄₋₃₀)/Σ(A₊₃₀ − A₋₃₀), the same repeats and the same bootstrap seed. It equals my independent implementation exactly in 60 of 60 synthetic runs for each of 4 scenarios.
  - `verdict(s, s_shift)` returns pass only if the frozen rule 2 holds and L_s ≥ 0.15, its CI lower end > 0 and L_s > |P_s|. Otherwise it returns fail-shift, decided before rules 3–6. Untestable fires below 12 items with both directions kept. Leave-one-item-out applies the same conjunct, and L_s and P_s are reported.
  - Hedge-only cases now pass 2% and 3% (my stub; they were 30% and 57%), and 1% and 1% in the committed dry run. Power at label 0.25 is 0.90 on my stub and 0.89 in the dry run.
  - A pass now requires strictly more than before. The one new untestable trigger cannot rescue a fail on these items (15 of 16 qualify on the archive). No bar is lowered, and keeping the odds at 0.25 is reasonable.
- **F3 (D11e): confirmed.**
  - `stop` is re-checked under the lock before the cap check. `stop.set()` and the error append both happen under the lock.
  - A discriminating stub (`d10_race3.py`) wraps the lock to record whether each call's gate was passed after `stop` was set. Old code: 5, 3 and 5 such calls in three runs. Fixed code: 0, 0 and 0. The calls that still enter the model after a refusal (3 in the dry run, 4 on my stub) all cleared the gate before it, so they were genuinely in flight.
  - The dry run's own race line (count after the refusal ≤ workers − 1) cannot tell the old code from the new, because the old code also stays under 7. My check is the one that confirms the fix. Non-blocking.
- **n1 and n3: confirmed.** `real_call()` passes `model=MODEL`. The code writes `label` as "<verdict>, fragile (one item)" on a flip. n2 (no 12-item untestable rule inside leave-one-item-out) stays open and is non-blocking.
- **Dry run:** `p2_6_dryrun.py` re-run from the main checkout reproduces the committed `p2-6-dryrun-output.txt` exactly. The dumb baselines still pass at most 1%. The gate line reads "design review verdict fix-first (not confirmed)". With `confirmed_at` set in this commit, the gate opens.

All three fixes hold. `confirmed_at` is set.

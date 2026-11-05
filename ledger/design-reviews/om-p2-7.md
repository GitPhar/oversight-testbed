---
bet: om-p2-7
program: other-minds
prereg_commit: 34182b6
reviewer_session: fresh design-review subagent launched by the om-p2-7 author session
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 05:50 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: flaw, D6: holds, D7: holds, D8: flaw, D9: holds, D10: flaw, D11: holds}
flaws: 5
pilot_usd: 0.00
verdict: fix-first
confirmed_at: null
---

# Design review of om-p2-7

## In plain English

The core of this test works. The statistic is the self–Sam correlation of residuals from a one-credence fit, scaled by a split-half ceiling and compared with a generic-link rival. It sees a shared fingerprint when there is one (pass 1.00), and it rejects a Sam whose deviations are unrelated to the model's own. It also rejects every shape-only responder I built: smooth, stepped, grid-rounded, monotone, and fitted without seeing the held-out statement. What fails is the reliability gate. When Sam's residuals are flat, meaning the formats agree for Sam, which is exactly the map's "assumption at stake", the gate reads that model as "not tested" instead of failing it. That has two effects:
- If only Opus's Sam is flat, and Haiku's and Sonnet's Sam share the fingerprint, the bet passes 80% of the time.
- If Sam is flat on every model, the result is "untestable" 100% of the time.

On the beacon-drawn statements, the pre-mortem's own "hedged" world passes 38% of the time, and only through Opus dropping out (Opus holds 0 of 60). There are four further fixes:
- The refusal stop leaks calls to the next model and shares its refusal record with the other program-2 bets. This repeats the om-p2-6r review's F4.
- Some frozen sentences contradict themselves at 2-decimal rounding next to a boundary (P13).
- `card_event` is labelled as Sean's card event, but it is a different event.
- Models that are incomplete get no sentence, and the pass sentence uses the noun "credence".

All five can be fixed before data without changing what is tested, and none lowers the bar.

## Checks

All commands were run with `env -u ANTHROPIC_API_KEY /Users/seanpharris/entangled-mind/.venv/bin/python`. Scratch scripts are in a `mktemp -d` folder under the session scratchpad, analysis is called in-process, nothing is written to `programs/other-minds/results/`, and there were no paid calls. The statements are the beacon draw (`data/p2-7-seed.json`, `seed32_items` 717985889): 34 statements, 2 from each of the 17 shared items. I checked that 68 (item, claim) pairs are shared by all three archives with all three formats × 10 repeats, that no archived value is `None`, and that every drawn item is in `split-exp5.json`.

**D1. holds.**
- `model_reading()` and `overall()` return exactly one reading for each synthetic table in the dry run (§6).
- I also ran `analyse_cache()` end to end on four synthetic caches with valid hashes:
  - Sam = self archive repeats 8 and 9 → **pass**, all three hold.
  - Sam's statements rotated by 7 → **fail**, all fail-ceiling.
  - Opus missing one call → **pass** on Haiku and Sonnet, Opus incomplete.
  - Haiku and Sonnet each missing one call → **untestable**.
- In each case the verdict was unique and the label well formed. A full analysis takes about 0.6 minutes (0.35 ms per `model_stats`).

**D2. holds.**
- `show` prints `claude-haiku-5-5` with `{"thinking": {"type": "disabled"}}` and max_tokens 100, `claude-sonnet-5-5` with `{"thinking": {"type": "between_tools"}}` and 1,000, and `claude-opus-5-5` with `{"output_config": {"effort": "low"}}` and 1,000 (no thinking parameter: Opus 5.5 cannot disable it). This is §2 and `mm_common.OFF`; gm3b's `structured()` sent thinking disabled at 100.
- On the beacon draw, `self_prompt()` equals `gm3b_format_invariance.prompt()` for all 102 (statement, format) pairs, and the Sam schemas equal gm3b's.
- The Sam text is the archived head, then P2-1 framing (d)'s first sentence verbatim, then the §2 questions word for word.
- The content hash differs by model.

**D3. holds.** I give the reliability gate's wrong-direction behaviour under D5.
- The generic-link rival rejects the generic world on the beacon draw: Haiku fail-generic 49 and fail-ceiling 8 of 60 (holds 3); Opus fail-generic 55 of 60.
- The shuffled-statement null is secondary only.

**D4. holds.**
- The rival can win: in the generic world it does, as above.
- The hypothesis can win against it: in the archive-repeat world Δ is +0.51 / +0.72 / +0.39, with CI lower ends +0.27 / +0.37 / +0.19.
- The rival has 12 parameters and is fitted in sample to Sam's own answers, so it is if anything conservative.
- Δ can be inflated by a negative ρ_g (shuffled world, Opus: Δ +0.245, CI [−0.03, +0.46]), but the ρ ≥ 0.5 conjunct guards this.

**D5. flaw (F1).**

Dumb responders tried. None reads *holds*. Each Sam below is built from self's data with no statement-specific deviation, run noise-free and with archived per-format noise, 20 runs each, B = 400:
- grid-rounded one-credence fit (F1 to 5s, F5 to 10s, F6 to the 7-point grid): Haiku, Sonnet and Opus fail-ceiling or unreliable;
- one number (self's F1 mean) read into all three grids: fail-ceiling or unreliable;
- leave-one-item-out isotonic link of self's latent: fail-ceiling (Haiku, Sonnet), fail-generic or fail-ceiling (Opus, ρ 0.52, Δ −0.20);
- leave-one-item-out cubic link: fail (Opus ρ 0.66–0.73, Δ −0.01 to −0.13);
- constant, and one-bit with any format levels: zero residuals → `rel_sam` NaN → **unreliable**.

An in-sample isotonic link of self *does* pass, but it is fitted to the very statements it predicts, so it is not a dumb responder. The grid, the verbal scale's coarseness and the ceilings do not by themselves buy a pass.

The flaw is the gate. A model is "not tested" when `rel_sam < 0.5`, but a flat or unreproducible Sam residual, alongside a reliable self residual, is a *mismatch*: the formats agree for Sam where they do not for self. On the beacon draw self reliability is 0.98 / 0.89 / 0.89, so the self gate never fires. The Sam gate decides which models enter the conjunction, and it removes models whose Sam has no fingerprint. Re-running the committed dry run (`p2_7_dryrun.py`, section 7) on the beacon draw instead of the stand-in seed:

| world | haiku | sonnet | opus | P(pass) as frozen |
|---|---|---|---|---|
| no-deviation (formats agree for Sam: the map's assumption at stake) | unreliable 60 | unreliable 60 | unreliable 48, fail-ceiling 10, fail-generic 2 | 0.00 (**untestable 1.00**, fail 0.00) |
| shared-hedged (the pre-mortem's world) | holds 60 | holds 60 | **holds 0**, fail-generic 37, unreliable 23 | **0.38** (all through Opus dropping out) |
| Haiku and Sonnet shared, Opus no-deviation (from the per-model rows) | 60 | 60 | unreliable 48 | **0.80** |

So the world in which the bet's hypothesis is plainly false on one model passes 80% of the time, and the cleanest world where it is false on every model can never fail.

A related point: `boot_model` uses `nanpercentile`, so a resample whose ceiling is undefined (a reliability ≤ 0) is silently dropped. In the hedged Opus world up to 28% of resamples were dropped (mean 3%), and the share of runs with CI lower > 0 was 0.07 with them dropped against 0.03 with them counted as the worst case. In the no-deviation Sonnet world 62% were dropped.

**D6. holds.**
- The pre-mortem is of kind `world`. The items are program 1's chain claims, rated 9,600 / 4,800 / 4,080 times with no refusal, no `None` value and 0 token-cap stops. P2-1 used framing (d) on Haiku without refusal.
- One residual execution risk, Opus thinking longer on the Sam question, is covered by the stop rule. See the optional notes on the cap.

**D7. holds.**
- §6 lists the differences, which are date, call path, repeats, the Sam sentence and the holder of the credence, and the claim is a match, which these differences can only make harder.
- One inaccuracy: §6 says the self data were asked "in batches". Haiku's gm3b calls were direct: `Caller` with 8 workers, no `batch` field in `gm3b-calls.json`. Only Sonnet and Opus (mm-gm3b) were batched. The results file should say so (optional note 1).

**D8. flaw (F3, F4, F5).** The sentences are in §5 and `SENTENCES`, but some are false for tables the rule sends to them:
- **F3, a P13 boundary in the printed sentences.**
  - ρ 0.4951 → "On Opus 5.5, the self–Sam residual correlation was +0.50 [+0.30, +0.70] of its ceiling, below 0.5."
  - Δ 0.0951 → "…did not beat the generic-link rival by the pre-registered 0.10 … (difference +0.10 […])…".
  - rel_sam 0.4951 → "…Sam 0.50; the floor is 0.5…".
  - §0 also says the dry run feeds every boundary, including CI > 0, but it does not feed the CI one. The code is right there: a CI lower end of 0.0, 5.6e-17 or 1e-10 gives fail-generic, 1e-4 gives holds, and −1e-4 gives fail-generic. It is just not shown.
- **F4, `card_event`.**
  - §0 says Sean's card asked the map's original event: one model, Haiku's archive, 80 claims × six formats, "about $0.24" (`ho-20261105-051140-gfv`).
  - §5.6 and `analyse_cache` compute "ρ ≥ 0.5 on every tested model", and `write_md` prints it as "the human-odds card's event". That label is false.
  - The conjunction is also met by a shape-only responder on Opus (the leave-one-item-out cubic world gives ρ 0.66–0.73), and the label hides this.
- **F5, missing sentences and a P9 noun.**
  - An *incomplete* model (cap, error or refusal) gets no sentence, and the pass and fail sentences name only the tested models. A cap stop on Opus would publish "On Haiku 5.5 and Sonnet 5.5 … matches the model's own" with no sentence saying that Opus was dropped.
  - §5.4 says the fail sentence "is followed by each model's reading sentence", but no code composes that, and `write_md` writes no sentence at all.
  - The pass sentence says "deviated from one shared credence" and "the format fingerprint of an attributed credence matches the model's own". P9's evidence lists "credence" as a cut noun (Opus F′). Here the thing named is a fitted latent value of ratings given for Sam.

**D9. holds.**
- Leave-one-item-out runs on every tested model, with its own bootstrap and the other models held at their full-data readings, and the first flip appends the frozen "fragile" sentence.
- Models read "unreliable" are not left out one item at a time, though dropping an item could make one testable. This is fixed with F1.

**D10. flaw (F2).**
- The budget is enforced: `spent() ≥ CAP` is checked under a lock, and the overshoot is at most 8 in-flight calls. My archive check reproduces §3's estimate: graded-format calls at full rate cost $0.000043 / $0.00086 / $0.0044, total $1.19 against a cap of $1.50.
- The cache is keyed by content hash, which is asserted on every hit and at analysis. A tampered entry is caught.
- The scale runs one way.
- The beacon seed is right: CURBy-RNG pulse 1592214 at 05:30:00, the first after the 05:29:59 commit, `certificate_verified: false` recorded as `hardware.md` allows.
- The lesson row matches: `check_prereg.py` gives L1, L2, L3 and H1 ok, and R1 fails only for want of this file.
- **But** all 612 jobs go to one `ThreadPoolExecutor`. I stubbed a refusal on a late Haiku call:
  - on call 200: 3 Sonnet calls went out;
  - on call 204: 10 Sonnet calls went out;
  - on call 204, when the refusal takes 0.5 s to return: all 204 Sonnet calls and 93 Opus calls went out.

  This contradicts §7's "A refusal on Haiku means Sonnet and Opus are never called". It is the om-p2-6r review's F4, fixed there by `run_all()` (D14d) and copied here from the unfixed caller.
- The refusal record is the shared `results/refusal.md`. `p2_6_position_label.py` and `p2_6r_replication.py` both refuse to start when it exists, so a refusal in this bet blocks them, and the reverse.
- §7 says a non-refusal stop "may be resumed". That leaves the author free to resume or not after Haiku and Sonnet are in the cache, and an Opus left incomplete shrinks the conjunction.

**D11. holds.**
- On the beacon draw, with the frozen rule (dry run section 7 re-run, 60 runs per world and model):
  - pass in shared 1.00, mix 0.7 0.92, mix 0.5 0.11, hedged 0.38;
  - P(fail) in independent 1.00 and generic 0.98.
- With the F1 fix, computed from the same per-model rows: pass in shared 1.00, mix 0.7 0.92, mix 0.5 about 0.09, hedged 0.00; fail in no-deviation and independent 1.00.
- Both sides stay above 10% under named worlds.
- The lesson's "Opus held in 2 of 60 hedged runs" and §4's reliabilities (0.97 / 0.97 / 0.94, residual SD 0.17 / 0.11 / 0.04) are from the stand-in draw. On the beacon draw they are 0.98 / 0.89 / 0.89 and SD 0.21 / 0.10 / 0.035, and Opus holds 0 of 60 hedged. The author may revise the odds before data, keeping both numbers.

## Required fixes

Each fix needs a dated row in `programs/other-minds/DEVIATIONS.md` (D15a–D15e), written before any call and naming this review. After the fixes, re-run the dry run on the beacon draw (`seed32_items` from `data/p2-7-seed.json`) and commit its output.

1. **F1 (D5): a flat Sam is a fail, not "not tested".** (D15a)
   - **Gate:** testability is gated on `rel_self` alone.
   - **Reading:** a complete model with `rel_self ≥ 0.5` and `rel_sam < 0.5`, or `rel_sam` undefined, reads a new failing reading, e.g. **fail-flat**. Give it a frozen sentence: "On {M}, the ratings given for Sam did not show a reproducible statement-by-format deviation (split-half reliability {rel_sam}, floor 0.5) where the model's own did ({rel_self}), so the fingerprint did not match."
   - **Bootstrap:** resamples with an undefined Δ count as −∞ for the CI lower end, and their share is reported.
   - **Leave-one-out:** leave-one-item-out runs on every complete model.
   - **Dry run:** add the world "Haiku and Sonnet shared, Opus no-deviation" (must read fail), re-run D11, and state the new P(pass) for each world.
2. **F2 (D10): one model at a time, its own refusal record, a fixed resume rule.** (D15b)
   - Port om-p2-6r's `run_all()`: the next model starts only if the previous one's run is `complete`.
   - Write `results/refusal-p2-7.md`, and refuse to start if it or `results/refusal.md` exists.
   - Change §7's "may be resumed" to "is resumed from cache until complete or a refusal or the cap", with no analysis in between.
   - Add a dry-run stub with a slow refusal on Haiku's last job, and show 0 Sonnet and 0 Opus calls.
3. **F3 (D8/P13): no sentence contradicts its boundary.** (D15c)
   - Print ρ, Δ and the reliabilities in every reading sentence to 3 decimals, or print the unrounded value whenever it lies within 0.005 of 0.5 or 0.10.
   - Add dry-run lines for the CI > 0 boundary: a lower end computed as a sum equal to 0 lands on fail-generic, and +1e-4 lands on holds.
4. **F4 (D8): `card_event` names the right event.** (D15d)
   - Report Haiku's ρ ≥ 0.5 as "the nearest analogue of the card's event (one model; here 34 statements × three formats, not the card's 80 × six)".
   - Report "ρ ≥ 0.5 on every tested model" separately, under its own name. Neither is labelled "the card's event", and both get frozen sentences.
   - Note that neither carries the P3 margin.
5. **F5 (D8/P9): every model gets a sentence, and no "credence" in the verdict.** (D15e)
   - Add a frozen **incomplete** sentence: "{M} was not tested: {n} of 204 Sam calls are missing ({reason})."
   - `analyse_cache` composes the verdict sentence, then every model's reading sentence (incomplete and untested included), then the fragile sentence, and `write_md` writes them.
   - In the pass sentence, replace "deviated from one shared credence" with "deviated from a one-latent-value fit", and "the format fingerprint of an attributed credence matches the model's own" with "the format fingerprint of the ratings given for Sam matches that of the model's own ratings". Apply the same nouns in the fail sentence.

Optional notes (not counted, no deviation row needed):
1. Correct §6's "in batches" in the results file: Haiku's archive was direct calls.
2. Opus's archived graded calls reach $0.012 at full rate. If the Sam question raises Opus's spend about 45%, the cap stops Opus partway and the conjunction shrinks to two models. A projected-cost check before Opus starts would avoid paying for an Opus arm that cannot finish.
3. The lesson's proof of reading cites `2efed51` "05:30" in §0 and `read_at: a0b0db3` in `lessons.jsonl`.
4. Sean is scored on this stricter three-model event, while his 0.70 was for the card's one-model event. That is ledger policy, not design, and §0 discloses it.

## Addendum: confirmation of fixes (2026-11-05 05:59 America/Denver)

I checked fix commit `1e13a58` (DEVIATIONS D15a–D15e, the code, and the dry run re-run on the beacon draw) and the odds revision 0.20 → 0.15 at `e19c185`, which keeps 0.25 as `engine_odds_first`. Nothing was called. Everything was run with `env -u ANTHROPIC_API_KEY`, as stubs and in-process analysis in a scratch folder. The gate still reads this file as unconfirmed. **Four of five fixes hold. F5 holds except one sentence, so `confirmed_at` stays null.**

- **F1 holds.**
  - `model_reading()` now gates testability on `rel_self` alone. A model whose Sam reliability is below 0.5 or NaN now reads `fail-flat`, which `overall()` counts as tested and not holding.
  - The frozen fail-flat sentence matches the review.
  - On the beacon draw, the dry run gives P(pass) 1.00 in the shared world, 0.92 at 70% shared and 0.09 at half shared. It gives 0.00 in the hedged, independent, generic and no-deviation worlds, and 0.00 for (shared, shared, no-deviation on Opus). No-deviation is now fail 1.00, where it was untestable.
  - Leave-one-item-out now runs on every complete model.
  - Undefined bootstrap resamples are treated as −∞. One quirk: once about 50 or more of the 2,000 resamples are −∞, `np.percentile` returns NaN rather than −∞ (I measured 2% undefined → finite, 3% → NaN). The rule is unaffected, because NaN > EPS is false, so the reading is not *holds*, the same as under −∞. The printed CI, though, then shows "nan". Optional: print "−∞ (undefined in {undefined_share})" there.
- **F2 holds.**
  - `run_all()` runs one model at a time.
  - The dry run sends a slow refusal on Haiku's 204th call: 0 Sonnet and 0 Opus calls go out, `refusal-p2-7.md` is written, and the shared `refusal.md` is not. A start with `refusal.md` present exits.
  - My own stubs agree. A refusal on Sonnet's 50th call sends no Opus call. A Haiku refusal sends no later calls. A cap reached during Opus stops at Opus.
  - After an error, the run command exits without analysing.
  - Optional: `p2-7-calls-stop.json` is never removed after a resumed run completes, so `stop_record` in the results JSON can show a stale "error". Delete it, or mark it resolved, when a run completes.
- **F3 holds.**
  - Every reading sentence and the per-model clause of the pass sentence now print 3 decimals: 0.4951 prints "+0.495 … below 0.5".
  - The CI > 0 boundary is in the dry run: a lower end computed as 0.3 − 0.1 − 0.2 reads fail-generic, and +1e-4 reads holds.
  - A narrower contradiction window remains, [0.4995, 0.5) or [0.0995, 0.1). It is permitted by the fix as written. Optional: print 4 decimals near a boundary.
- **F4 holds.**
  - `card_event` is withdrawn. Two named secondaries replace it, `haiku_analogue` and `every_model_rho`, each with a frozen sentence, each saying it carries no margin over the rival, and neither calling itself the card's event.
- **F5: holds, except one sentence.**
  - What holds:
    - No sentence contains "credence".
    - The pass and fail nouns are as required.
    - `compose()` outputs the verdict, every model's sentence and the fragile sentence, and `write_md` writes them.
    - The incomplete sentence exists.
  - **What still fails:** the incomplete sentence's `{reason}` is false for some tables the rule sends to it.
    - `analyse_model` sets the reason to "a refusal" only when *that model's own* cache holds a refused call. Every other case reads "the budget cap or an error stopped the run".
    - With `run_all()`, a refusal on an earlier model leaves the later models with no calls. My stubs then printed "Opus 5.5 was not tested: 204 of 204 Sam calls are missing (the budget cap or an error stopped the run)." after a Sonnet refusal, and the same for Sonnet and Opus after a Haiku refusal.
    - Neither the cap nor an error stopped those runs. A refusal did.

**Required to confirm (one line, D15e addendum row):** pass the stop record (`p2-7-calls-stop.json`: reason and job) to `analyse_cache`, and build `{reason}` from it. Then:
- a model that was never started reads "the run stopped on a refusal on {M0} before {M}'s calls" (or "…on the budget cap…" or "…on an error…" for {M0});
- a model stopped partway reads its own cause: refusal, cap or error, named separately, not "cap or error".

Show this in the dry run with a Sonnet refusal (Opus's sentence) and a cap stop during Opus. When that commit is in, I confirm by addendum.

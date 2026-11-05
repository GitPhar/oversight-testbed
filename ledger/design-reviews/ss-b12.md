---
bet: ss-b12
program: settled-science
prereg_commit: 0e81ddc
reviewer_session: fresh design-review subagent launched by the engine session; read the main checkout at HEAD (code at 8140cf6, unchanged since; pre-registration read with git show 0e81ddc:...), scripts and scratch caches under the session scratchpad
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true          # reviewer, author and bettor are all claude-opus-5-5
date: 2026-11-05 07:01 America/Denver
checks: {D1: flaw, D2: flaw, D3: flaw, D4: holds, D5: flaw, D6: holds, D7: flaw, D8: flaw, D9: holds, D10: holds, D11: holds}
flaws: 5
pilot_usd: 0.00
verdict: fix-first
confirmed_at: null
---

# Design review of ss-b12

## In plain English

The design can answer its question, and it can both pass and fail. Built from round 2's measured per-item scores, it passes about 10–18% of the time if older unrecognised items score like round 1's did (0.79 of the post-cutoff Brier), and about 19–37% if they score like round 1's older items as a whole. It fails at least 54% of the time in every world. So the ceiling does not make it near-unpassable. The problem is the recognition rule, the one manipulation the bet rests on. On this bettor's own round-2 rationales, it misses recall written as a citation. r2-052's primary call names "SycEval (Fanous et al. 2025)" and quotes its numbers, and RECOG does not flag it. The repeat call on the same item says "I recall", and it is flagged. The rule also flags denials: "I can't actually recognise this paper" (r2-016) counts as recognition. Both errors push toward a false pass. In a world where the whole older-paper advantage is memory, a rule that catches half the recalls passes 15–27% of the time. That is as often as the real effect would pass. The verdict sentences also repeat "training cutoff", which two audits have already cut. The two sides differ in more than date, and the sentences do not say so. Each fix can be made before data without changing what is tested.

## Checks

Commands ran from `programs/settled-science` in the main checkout. Nothing was fetched or called. `f4.py` ran only with `--dry-run`. Scripts are in `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/6509f5b7-80b2-4dab-9f54-37652f9d2839/scratchpad/`: `d11.py`, `d11b.py`, `perm.py`, `d3.py` (simulations) and `captest.py` (the cap test with fake calls, using scratch caches). `items/f4/` and `bettor/f4-bettor-cache.json` still do not exist. Round-2 numbers come from the archive: the post side's 92 primary per-item Briers (mean 0.0697, sd 0.106, 6 items wrong), the round-2 candidate yield per pooled paper and leak keep rate by field (`items/r2/`), and the per-call costs (Sonnet leak check mean $0.00294, 95th percentile $0.0042; Opus primary mean $0.0048, max $0.0094). No pre-cutoff statistic was computed, and no round-1 pre-cutoff rationale was read.

**D1. A stranger can apply the rule: flaw (one branch has no verdict).** `score_f4 --synthetic` returns exactly one label for each world: easier → pass (−0.036 [−0.053, −0.020]); same, memory and ceiling → null. With fewer than 30 unrecognised items it returns untestable, and it does the same when no f4 bets exist, which covers "leakage check not completed" (`freeze()` exits on any `unchecked`). One branch is undefined. A refusal or error during step 3 stops the Caller, `bet()`'s `finally` writes the partial bets, and the scorer would score them if 30 are unrecognised. §3 defines this only for a cap stop. A partial run is also not a random subset. Jobs run in id order, and ids follow (query bucket, arXiv id), so a stop removes the last buckets (interpretability first). → F4.

**D2. Every manipulation takes effect: flaw (F1).** Three knobs.
- **Date windows.** The 12 search strings print as `(<round-2 query>) AND submittedDate:[2024… | 2025… | 202601010000 TO 202606302359]`. The build drops v1 ≥ 2026-07-01. `verify.check` accepts v1 2024-01-01 to 2026-06-30 and rejects 2023-12-31.
- **Template.** On synthetic pre-cutoff-style abstracts (v1 2024-01-01, 2024-12-20, 2025-12-30, 2026-06-30), `item_from` and `verify.check` give the same sentence, swap and errors as on post-cutoff dates. The writer has no date dependence. `--dry-run` passes the template self-test.
- **The recognition rule RECOG.** This one fails. On round 2's 92 primary rationales it flags 0, as it should for post-cutoff papers. But this bettor's archived rationales show it missing recall and flagging denials:

| row | text (excerpt) | RECOG | should be |
|---|---|---|---|
| r2-052 primary | "SycEval (Fanous et al. 2025) reported that preemptive rebuttals produced higher sycophancy rates … 61.75% vs 56.52%" | not flagged | recall (names a study, quotes its numbers) |
| r2-052 order-check | "… I recall they found preemptive rebuttals yielded more sycophancy" | flagged ("I recall") | recall |
| r2-018 primary | "Quiet-Sun inversion studies (e.g., Hinode, Lites et al.) commonly find … matches that well-known result" | not flagged | recall of named literature |
| r2-016 order-check | "I can't actually recognise this paper, and 'Claude Opus 4.8' doesn't match any model I know of" | flagged ("recognise this paper") | not recognised (a denial) |

The same recall was flagged on one of its two calls. Synthetic strings confirm the classes:
- **Not flagged:** "Marks et al. (2024) showed…", "This is the SAEBench study (Karvonen et al. 2025)…", "matches the well-known Anthropic result…".
- **Flagged:**
  - denials: "I do not recognize this study", "I'm not familiar with this paper", "I cannot answer from memory";
  - generic phrases: "I've seen the phrase…", "This study was published in a quantum venue…", "known result from prior work", "recalled as fragile".

The map node's own `cheapest_test` says "names or recalls the specific study". The round-3 audit's split (16 of 68 round-1 older items, Brier 0.024 against 0.129) used a regex that "names or recalls a specific study". RECOG keeps the "recalls" half and drops "names". Both errors bias toward a pass:
- named recalls stay in the "not recognised" set and lower its Brier;
- denials are mostly low-confidence calls, and dropping them also lowers it.

**D3. Every control can fail: flaw (F1, quantified).** The control here is the recognition split: a world where the advantage is all memory must come out null. The scorer's `memory` world does come out null (−0.001 [−0.025, 0.024]), but only because its recognition labels are perfect. `d3.py` rebuilds that world from measured numbers. A quarter of the older items are recalled (the round-3 audit's 16 of 68), recalled items score like the post side's best quarter, and the rest score like the post side.

| RECOG catches this share of recalls | denials flagged (share of low-confidence unrecalled items) | P(pass), the false "beyond recall" | P(null) | P(untestable) |
|---|---|---|---|---|
| all | 0 | 0.04 | 0.69 | 0.27 |
| all | 0.2 | 0.06 | 0.43 | 0.51 |
| half | 0 | 0.15 | 0.82 | 0.03 |
| half | 0.2 | 0.20 | 0.65 | 0.15 |
| a quarter | 0 | 0.20 | 0.79 | 0.01 |
| a quarter | 0.2 | 0.27 | 0.67 | 0.07 |

The one measured recall pair was caught on one of its two calls. At that rate a pure-memory world passes 15–20% of the time, about as often as the real-effect world W1 (below). As built, a pass cannot carry the sentence "not only papers it says it remembers". → F1.

**D4. Rivals are matched: holds (not applicable).** No two model families or fitted models compete.

**D5. A dumb baseline is beaten, and the design can see the effect: flaw (F3, item-property baseline; P16).** A constant or one-bit bettor gives d ≈ 0 and comes out null. But an item property can make the gap by itself. Round 2's drawn items carry the up word on 77% of published sentences. If the older pool's share differs, the up-word or swap-pair rule shows a pre-minus-post gap with no recall at all, and the bettor's 0.070 is largely matched by a flattery rule (ss-b6). The pass sentence does admit "older findings being easier". But nothing reports whether the item mix alone shows the gap, so a reader cannot tell. The null side is not an equivalence claim, so no margin is required. Still, the null sentence ("finds no advantage on older papers beyond recall") needs the size it could see. At n_pre = 40 the normal-approximation MDE at 80% power is 0.056, about 80% of the 0.070 there is to gain. The simulations below are kinder because the pre side's variance shrinks as it improves, but a null is still weak. → F2 wording, F3 secondary.

**D6. Foreseeable execution risks are piloted: holds, no pilot.** The pre-mortem is of kind `design`. The queries, prompts, models and settings are round 2's. Round 2 made 243 Sonnet leak calls and 138 Opus bettor calls with no refusal. The older windows draw from the same four topic queries. No execution risk is named, so I spent no pilot money ($0.00).

**D7. Comparisons match: flaw (F3).** Besides the date, the two sides differ in these ways:

| | post (round 2, archive) | pre (ss-b12) | effect |
|---|---|---|---|
| fetch | one window, 2026-07-01 to 11-04; up to 600 results per query (300 + D22 extension), newest first | three windows; 100 per window per query, newest first, so the papers bunch at late Dec 2024, late Dec 2025 and late June 2026 | within-window recency differs. The 2026H1 third is weeks before the stated cutoff and may be effectively unseen, which dilutes the effect (D11). |
| exclusions | round 1 ids; ICML 2026 / TMLR comment (D12) | round 1 ids and round-2 candidates; no venue rule | immaterial (D12's purpose is post-side only), but older papers can carry venue acceptances, a fame marker |
| leakage check, order | all 243 candidates checked, then ≤ 30 clean per field drawn (bettor.py `sample_r2`) | ≤ 30 candidates per field drawn, then checked | field mix and n differ. Expected clean: about 8/10/15/11 (pre) against 14/21/30/27 (post). No bias in expectation. |
| leakage check, checker | claude-sonnet-5-5, told the answer, on papers it cannot know | the same model, on papers it may know | drops may depend on the checker recognising the paper, which happens on one side only. Not matchable. |
| n | 92 | about 44 clean (5–95%: 34–52), about 38 unrecognised at 10% recognised | handled by the bootstrap |
| run date | bettor 2026-11-04 (ss-b5) | 2026-11-05 or later | same model id, prompt, schema, effort low, max_tokens 4000, cache key family `bettor-v1`. No change expected. Record the dates. |
| option order | r2 beacon seed | f4 beacon seed (verified: items 2418064898708106585, order 8371102074377508067; pulse 06:46:00 after commit 06:45:36) | same rule |
| up-word share | 0.77 | unknown until built | item mix (D5) |

The checker's familiarity and the recency cannot be matched. The claim must therefore be about the bundle, and the sentences must say so. → F3.

**D8. The verdict sentences are written: flaw (F2).** All three sentences exist, and the code reproduces them (`sentence()`). But the pass and null sentences say "papers posted after its training cutoff". Audit ss-b1 cut 3 replaced that phrase. Audit ss-b5 cut 5 repeated the cut and recorded it as that design review's D8 miss ("stated knowledge cutoff of June 2026"). "Older papers" also covers papers posted in June 2026, weeks before the stated cutoff. The null sentence states no detectable size. The "no sign of recognising" noun stands only once F1 is fixed.

**D9. One item cannot decide it: holds.** Leave-one-item-out (both sides) and leave-one-query-bucket-out are pre-registered and coded, and any flip is appended to the sentence. The field-cluster jackknife is reported as a secondary (P14). The bar is read on the item bootstrap, and §4 says so.

**D10. Machinery: holds.**
- **Budget, both caches.** `captest.py` patches `common.CACHES` to scratch copies of the two f4 caches and runs `common.Caller` with a fake call function. A 120-call leak phase at the 95th-percentile cost ($0.504), then a bettor phase at the maximum Opus cost, stops after 21 bettor calls with $0.7014 spent across both caches. So `cap()` counts both, and the effective stop is $0.75 − $0.05. The program cap enters through `min(BUDGET_USD, …)`: $4.76 of $8.25 spent. Six workers in flight can overshoot by at most about 6 × $0.0094.
- **Refusal and truncation stop.** `Caller` on `llm.RefusalError`, and `_check_stop` on max_tokens. Nothing is reworded or retried.
- **Untestable branches.** With fewer than 30 clean items, `bet()` exits before any call. If the leakage check did not finish, `freeze()` exits and nothing is frozen.
- **Other machinery.** One scale direction (1–99, `p_true` from `option_1_is`). Content-hash keys. The CURBy-RNG pulse is the first after the commit, and the sub-seeds re-derive exactly with `ledger/seed.py`.
- **Lesson.** `check_prereg.py`: L1–L3 ok and H1 ok; R1 fails only because this file did not yet exist. The lesson runs to 63 words, which the author noted when freezing it.
- **Expected cost.** About $0.33 leak plus $0.21 bettor, so $0.54. The worst realistic case leaves a cap stop in the bettor phase possible (see F4 for the order bias).

**D11. The bet can both pass and fail: holds, marginally.** Worlds are built from measured round-2 numbers (P15): the post side's 92 per-item Briers, and a pre side whose clean count is simulated from round 2's per-field candidate yield and leak keep rate. The bootstrap is the scorer's `boot2` (2,000 resamples per simulation). "Known" items are drawn from the post side's best quarter.

| world (pre, not recognised) | recognised 10% | recognised 25% | 2026H1 third at post level, 10% / 25% |
|---|---|---|---|
| W0 same as post (0.070) | pass 0.05, null 0.92, untestable 0.03 | pass 0.03, null 0.69, untestable 0.28 | |
| W1 round-1 unrecognised ratio 0.79 (0.055) | pass 0.17, null 0.79 | pass 0.13, null 0.58, untestable 0.30 | pass 0.10 / 0.07 |
| W2 round-1 all-older ratio 0.64 (0.045) | pass 0.33, null 0.64 | pass 0.26, null 0.44 | pass 0.18 / 0.15 |
| W3 round-1 absolute gap −0.034 (0.036) | pass 0.55 | pass 0.36 | pass 0.31 / 0.24 |

- **Pass and fail.** P(pass) reaches about 10% or more in the round-1-calibrated worlds, and P(fail) is at least 0.44 everywhere. The ceiling does not make the bet near-unpassable, but W1 sits at the floor once the late-June third is diluted.
- **The realised n is below the stated one.** It is about 38–44 clean, not the "about 52" of `--dry-run` and §0. The dry run multiplies 120 by 0.44 and calls 0.44 a "drop", but round 2 kept 40–44%. And 120 is never reached, because quantum-devices yields about 21 candidates.
- **Recognition and untestability.** Once F1 is fixed, a citation-aware rule may flag round-1-like shares (about 24%). P(untestable) then rises to about 30%.
- **A larger draw.** Checking every candidate before sampling, as round 2 did, gives about 49 clean and cuts P(untestable) to about 11%. But its cost is $0.60 at the median and $0.69 at the 95th percentile, against the $0.70 effective stop. I do not require it (engine's call).
- **The bootstrap runs hot at this n.** In W0 the percentile bootstrap passes 6.1% at n = 30, 4.2% at 40 and 2.2% at 60, against a nominal 2.5% (`perm.py`; a few wrong items dominate a skewed distribution). A one-sided permutation test holds 1.3–1.7%, with W1 power about 0.10–0.12. → F5.

**CONTEXT rule 12 (not all three models): holds.** §0 gives "the question is about one model by design", which is one of rule 12's named good reasons. The question asks whether Opus's ss-b3 advantage is recall, and the post side is Opus's archive. The reason is not cost alone. Two non-blocking notes:
- There are stronger reasons the cell does not state. Haiku and Sonnet have their own stated cutoffs, so "pre" and "post" would need redefining. And Sonnet is the leakage checker.
- The map node ss-f4 still lists all three models.

## Required fixes

Each fix goes in a dated DEVIATIONS.md row naming this review (`ledger/design-reviews/ss-b12.md`), written before any fetch or call. Odds may be revised before data (both kept).

- **F1 (D2, D3): revise RECOG before any f4 rationale exists.**
  - (a) **Negation guard.** A match does not count if a negator (`not|no|never|cannot|can't|don't|didn't|isn't|without|n't`) appears within the four words before it in the same sentence.
  - (b) **Citation clause.** Add `\bet al\b`; a year 2019–2026 in the rationale that is not in the item's own question or options; and "well-known/famous (paper|study|result|finding|benchmark)".
  - (c) **Drop the generic alternatives:** `recalled`, `I've seen the`, `this (paper|study|work) (is|was) (known|published|from)`, `known (paper|study|result) (from|by)`, `from (my )?memory` unless first-person and un-negated.
  - (d) **Unit test.** Commit a test with the four archive rows in the D2 table and the 16 synthetic strings in this review, with the expected labels.
  - (e) **Re-run on round 2's 92 primary rationales and state the count.** The citation clause may flag r2-018 and r2-052. They are dropped from the post side by the same rule, so n_post may be 90.
  - (f) **Keep the frozen RECOG as a reported secondary** (primary computed with both, revised rule binding).
  - Optional, answer-free and counts only: report how many of round 1's 68 pre-cutoff rationales each rule flags, against the round-3 audit's 16.
- **F2 (D8): rewrite the §5 sentences and `sentence()`.**
  - Replace "papers posted after its training cutoff" with "papers first posted after its stated knowledge cutoff of June 2026 (34 of them in July–August)".
  - Replace "older papers" with "papers first posted between January 2024 and June 2026".
  - Add to the null sentence: "; an advantage smaller than about 0.05 in Brier could not reliably have been seen".
- **F3 (D5, D7): name the bundle and report the item-mix baseline.**
  - **Bundle clause.** Append to every verdict sentence: "The two sides differ in more than date: the older items are the latest 100 papers of each window and were leakage-checked by a Claude model that may know them; the newer are up to 600 papers over four months." Add the same as a §6 bullet.
  - **Secondaries** (code in `score_f4`):
    - the leak-drop share per side (pre flagged/checked against round 2's 146/243);
    - the up-word share per side;
    - the pre-minus-post gap of the up-word (0.75) and swap-pair (D24) rules on the same unrecognised items, with intervals.
  - **If the up-word rule's gap has an upper bound below 0,** the sentence adds "a rule that reads only the comparative word also scores better on the older items (d_up [lo, hi])".
  - **Record** both sides' run dates and model ids in the results.
- **F4 (D1): the refusal and error branch, and cap-stop order.**
  - **§5 and §7.** A refusal or error at any step makes the bet untestable (not scored), whatever was written. The cap-stop rule stays.
  - **`score_f4`.** Return untestable when f4-bets has fewer primary rows than masked items and no cap stop is recorded. On a cap stop, the sentence names any query bucket with no pre item.
  - **Optional.** Run bettor jobs in the beacon `order` permutation rather than id order, so a cap stop does not remove whole buckets.
- **F5 (D11): the bootstrap at the realised n, and the dry-run text.**
  - **Permutation p.** Report a one-sided label-permutation p (10,000 permutations, `default_rng(20261104)`) beside the bootstrap. If the label is pass and p ≥ 0.025, the sentence adds "a permutation test does not confirm it (p = …)". The bar is unchanged.
  - **Dry-run text.** Correct `--dry-run` and §0/§3 to "about 44 clean (round-2 keep rate 40–44%), about 38 unrecognised", and cite this review's measured-world table as the D11 dry run in place of the exponential `--synthetic` worlds (P15).

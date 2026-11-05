---
bet: ss-b1
program: settled-science
prereg_commit: ebd2c80
reviewer_session: design-review ss-b1 (fresh subagent session, launched by the engine session; no chat or transcript read)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-04 18:45 America/Denver
checks: {D1: flaw, D2: holds, D3: holds, D4: holds, D5: holds, D6: holds, D7: flaw, D8: flaw, D9: flaw, D10: flaw}
flaws: 5
pilot_usd: 0.00
verdict: fix-first
confirmed_at: 2026-11-04 18:50 America/Denver
---

# Design review of ss-b1

## In plain English

As built, this test would mostly answer its question. The tool-less bettor sees only the masked file. Option order really does come from the beacon. The scorer gives the right label on synthetic bettors with known skill, and no dumb predictor I tried passes the rule: a constant 50%, the publication-bias baseline, a direction-word prior, the question's word order, and a word-count classifier. The engine session asked me to check one thing in particular, and it holds. The leakage-check outcomes did not shape the exclusion rule or the item set. The rule is the one fixed at 16:54 in Rule 3. Each of the 187 first checks ran on text that is byte-identical to the candidates committed beforehand. All 26 flagged items were rewritten exactly once, and the rewrites changed wording only. Nothing else in the set moved. Five things must change before the first call:
- **Post-cutoff items:** two of them (one paper) carry the same "presented at an ICML 2026 workshop" note that got another paper moved to pre-cutoff.
- **Refusal record:** a refusal crashes the code that records it, so the request ID is lost.
- **Saving results:** a stop in the order-check step would leave the primary bets unsaved.
- **Verdict sentences:** the untestable verdict has none, and none covers what happens to ss-b2 and ss-b3 on a short run.
- **Leave-one-item-out:** it covers ss-b1 only, not ss-b2 or ss-b3.

None of these changes the question, so the verdict is **fix first**.

## Checks

### The question the engine session asked: did the leakage-check outcomes shape the exclusion rule or the item set? **Holds.**

Commands: `git show d3996c9:…/candidates.jsonl` and `git show 4859d3b:…/candidates.jsonl`, compared in a scratch script against the current `items/leakage-log.jsonl`, `items/leakage-cache.json`, `items/rewrites.jsonl`, `items/leakage-status.json`, `items/items.jsonl` and `items/masked.jsonl`.

- **Times.** Rule 3 of `protocol/fixed-rules.md` (`64e12dd`, 16:54:10) already says: flagged once, rewrite once, a fresh call, and if flagged again, dropped. `protocol/leakage-check.md` (`d3996c9`, 17:17:16) adds only operational detail: the threshold is the boolean `leak`, rewrites change wording only, and a discretionary drop is allowed. The outputs are in `4859d3b` (17:20:48), and the pre-registration is in `ebd2c80` (17:31:23). No leakage file, `leakcheck.py`, `freeze.py`, `bettor.py` or `score.py` changed after `4859d3b`. A draft of the pre-registration with placeholders (`/Users/seanpharris/settled-science/experiments/ss-b1.md`, mtime 17:00) already holds every §4 and §5 rule, including "with and without items that needed a leakage rewrite". So the analysis was written before any item existed.
- **Content.** 213 log lines, 213 cache entries, the same key sets, and no duplicate keys. Every one of the 187 `d3996c9` candidates has a first-check entry, and the item text in each is byte-identical to the committed candidate on all six checked fields. No log entry belongs to a cid that is not a candidate. Log order: all 187 first checks (lines 0–186) come before all 26 second checks (lines 187–212).
- **Rewrites.** The 26 items flagged on the first check are exactly the 26 cids in `rewrites.jsonl`, with one rewrite each. Each `before` equals the `d3996c9` text. Each second check ran on the `after` text, and the `4859d3b` candidate equals it. No rewrite touches `true_option`, `headline_side`, the paper or the quote. Between `d3996c9` and `4859d3b`, no candidate changed except these 26. The discretionary-drop clause (leakage-check.md §3) was never used.
- **Freeze.** `items.jsonl` holds the 184 cids whose status is `clean` or `clean-after-rewrite`, and every field matches the `4859d3b` candidates. 3 were dropped after a second flag (c-2610.03498-1, c-2610.26496-1, c-2611.04289-1, all post-cutoff, true options b/b/a). `masked.jsonl` has exactly `id, field, question, methods, option_a, option_b`. Both SHA-256 values match §2.
- **Writer exclusions** (4 drafts plus one move to pre-cutoff) are in `d3996c9`, before any call. Three of the four repeat the draft's own `notes` field. The fourth (quantum-devices-post:7, "hedged") has empty notes, and its reason quotes the abstract.
- **Limit.** Commit times bound when the rule and the inputs were fixed, not when calls were made. Nothing in the cache carries a timestamp. There is no `leakage-cache.json` in the standalone repo, and the 3.5-minute gap is tight but feasible (187 calls on 6 workers, then 26). The post-result auditor can close this from the Anthropic usage record: no claude-sonnet-5-5 calls on this key before 00:17:16 UTC on 5 November.
- **Minor.** leakage-check.md §5 says the writer exclusions are "two quantum-devices items, plus one paper moved to pre-cutoff". The file it names, committed in the same commit, holds four (two quantum-devices, two interpretability). All are pre-call, so this is a wording error only.

### D1. A stranger can apply the rule: **flaw** (small, folded into F4 and F5)

Synthetic bettors were scored by the real `scoring/score.py` (imported, real `items.jsonl`, real bootstrap), and I applied §5 by hand as a stranger (`scratchpad/rev/d1.py`). Each case returned exactly one label:

| synthetic truth | post Brier [95% CI] | ss-b1 | ss-b2 upper | ss-b3 upper |
|---|---|---|---|---|
| right 80% at 0.7 | 0.167 [0.140, 0.198] | pass | −0.033 → pass | 0.059 → not shown |
| right 55% | 0.272 [0.238, 0.308] | null | 0.078 | 0.058 |
| right 30% | 0.376 [0.342, 0.406] | null, worse than 50% | 0.177 | 0.058 |
| only 50 post items scored | 0.130 [0.098, 0.170] | untestable | **−0.081 → "pass"** | 0.089 |
| headline baseline itself | 0.237 [0.214, 0.261] | null | 0.000 → not shown | 0.051 |
| memory: pre right 90%, post 50% | 0.250 | null | 0.036 | **−0.066 → pass** |
| near the line (right 64%) | 0.218 [0.184, 0.251] | null, **fragile (34 flips)** | 0.018 | 0.103 |

`score.py --synthetic coin|oracle|headline|anti` gives null, pass, null (upper 0.261) and null, as the lesson line states.

The flaw: §5 gives ss-b2 and ss-b3 no untestable condition. On the 50-item run, a stranger reads ss-b2 as **pass** while ss-b1 is untestable. The code computes labels only for ss-b1. ss-b2, ss-b3 and "fragile" have to be read off CIs by hand. Fix in F4 and F5.

### D2. Every manipulation takes effect: **holds**

The only knob is option order. `bettor.py --dry-run`: 184 items, 276 calls (92 order-check), option_b first on 94. Re-drawing with seeds +1 changes the order on 84 items, so the draw is live. For every item, both orders put the right text in "Option 1", and `option_1_is` matches it. Each order-check job is the exact reverse of its primary. The 368 possible prompts have 368 distinct cache keys, and no two items share text. The bettor's source never opens `items.jsonl`, and the user text has no id, title, date, quote, answer or tag. The seeds recompute from the recorded randomness with `ledger/seed.py` (order 13309338689196222401, order-check 16683013961078861871, human-form 14605333098254812962). The run's model, max_tokens (400), schema and prompt match §2.

### D3. Every control can fail: **holds**

- **Order check:** a coin bettor with a +15-point lean toward Option 1 gives a first-shown pull of +15.0 [15.0, 15.0], so the check catches a wrong set-up.
- **Leakage check:** it flagged 26 of 187 and dropped 3, so it can fail.
- **Constant 0.5:** gives exactly 0.25, which is not below 0.25, so null.
- **Headline baseline as bettor:** gives null on ss-b1 and a paired difference of exactly 0 on ss-b2 (not shown).
- **Memory-only bettor:** passes ss-b3 and fails ss-b1, as it should.
- **`freeze.py`:** refuses below 60 post-cutoff items.

### D4. Rivals are matched: **holds**

The rival in ss-b2 is the publication-bias baseline, scored on the same items. It is not crippled. On the 40 tagged post items the headline side is the reported one 28 times (70%), and the fixed 0.75 is close to the best a one-bit rule can do (0.70 gives 0.2366, against 0.2374 for 0.75). When the headline baseline is used as the bettor, it ties itself exactly (difference 0), so neither side wins by construction. The tags were set by the writer before any bet, and rewrites could not change them.

### D5. A dumb baseline is beaten, and the design can see the effect: **holds**

The ss-b1 rule (post-cutoff upper bound below 0.25, n = 119) is not passed by any of these dumb predictors:

| predictor | Brier | upper bound |
|---|---|---|
| constant 0.5 | 0.250 | 0.250 |
| headline 0.75 | 0.237 | 0.261 |
| "the up-word is true" (truth is the higher/more side in 58 of 119) at 0.6 | 0.263 | 0.281 |
| "the direction named first in the question is true" (54 of 102) at 0.6 | 0.254 | 0.271 |
| per-field up-word rate, fitted in-sample (cheating) | 0.247 | 0.257 |
| leave-one-out naive Bayes on question+methods words | 0.278 | 0.300 |

This is not a "no difference" rule, so no equivalence margin is needed. For context, power at n = 119 (simulated): a bettor right 70% of the time at 0.7 confidence (Brier 0.21) passes 65% of the time. At 65% right (0.23) it passes 23% of the time. This is consistent with the map's 50% and with the pre-mortem.

### D6. Execution risks are piloted: **holds**

The pre-mortem is of kind `design`, so no pilot is required. The content risk is already covered without a pilot. claude-sonnet-5-5 read all 187 items, with their answers, through the same `structured()` path: 213 calls, 0 refusals, 0 max_tokens stops, 0 parse failures. A rationale of 100 words fits within 400 tokens. The bettor's first call fixes the thinking setting. The code raises if a thinking block comes back.

### D7. Comparisons match: **flaw (F1)**

ss-b1 vs 0.5 and ss-b2 vs the baseline are on the same items. ss-b3 (pre vs post) differs in more than memory: the date, the headline mix (none on 75% of pre items vs 66% of post) and the writer files. But §5.5's sentence already claims only the bundle ("…or with the older items being easier; this design cannot separate the two"), and that is acceptable.

The flaw is in the cutoff split itself, which ss-b1 and ss-b3 both rest on. Rule 2 says a paper whose comments name an earlier public version goes to pre-cutoff. The writer applied it to 2608.27340 ("presented at 2026 ICML Mechanistic Interpretability Workshop" → pre, ss-152). The writer did not apply it to **2611.00420** (ss-026 and ss-027, post, interpretability), whose arXiv comment reads *"Extended version of a paper presented at the Mechanistic Interpretability and Compositional Learning workshops at ICML 2026"*. That names the same workshop, plus an explicit earlier version. So §7's sentence ("items with an earlier version named in the arXiv comments were moved to pre-cutoff") is false for these two items. I also scanned the comments of all 119 post items. The only other one worth a written decision is ss-094 (2609.25366, "Accepted to TMLR, September 2026"): TMLR submissions are public on OpenReview while under review. Its comment names no date, so Rule 2 does not force a move.

### D8. The verdict sentences are written: **flaw (F4)**

Pass, null, null-and-worse, ss-b2 both ways and ss-b3 both ways all have sentences, with nouns the design can carry. Missing:
- a sentence for **untestable**;
- a sentence for a **fragile** label;
- what ss-b2 and ss-b3 say when ss-b1 is untestable. Jobs run in id order and post-cutoff items are ss-001…119, so a stop part-way leaves ss-b3 with no pre-cutoff items.

The pass sentence hard-codes "On 119 findings" where the scored n belongs.

### D9. One item cannot decide it: **flaw (F5)**

Leave-one-item-out is pre-registered for ss-b1 with a consequence (fragile, item named), and it works. In the near-line case (upper 0.251), removing any of 34 items flips the label. It is not pre-registered or coded for ss-b2 or ss-b3, though each is its own ledger bet with its own label (P10).

The LOO bounds use 2,000 resamples and compare with a full-data bound from 10,000. That puts about ±0.001 of Monte Carlo noise into flips near the line. Use 10,000 resamples, the same as the full-data bound, so that the comparison carries no extra noise.

### D10. Machinery: **flaw (F2, F3)**

**Holds:**
- **Budget:** a $5.00 cap in code (`common.BUDGET_USD`), shared with the leakage cache ($0.4704 spent) and checked before each call. Up to 6 calls can be in flight, so overshoot is about $0.04. Estimated run: about $1.4–1.8.
- **Prices:** the price table has claude-opus-5-5.
- **Stop on refusal:** the stop is in code.
- **Scale:** one direction (p_option_1, 99 = Option 1 reported, clipped to [1, 99]).
- **Cache:** content-hash cache.
- **Beacon:** CURBY-Q stalled (round 28297, 2025-08-22). CURBy-RNG pulse 1591496 at 00:32:00Z is the first after the commit at 00:31:23Z (previous pulse 00:31:00Z). The seeds recompute. I did not re-fetch the pulse.
- **Lesson line:** `python3 ledger/check_prereg.py` gives L1–L3 ok. The `read` block's "base rate 0.22" is the raw 2/9, not learn.md's (2+1)/(9+2) = 0.27. The ledger session has noted this, and it does not change the odds' direction.

**F2.** `results/` does not exist, and `Caller.run` writes `results/refusal.md` without creating it. In a scratch copy of `common.py` with a stubbed `RefusalError` (request `req_TEST123`), the run stopped with `FileNotFoundError` and the request ID was never written or printed. The stop still happens, but the record that CONTEXT rule 3 and §8 promise does not.

**F3.** `bettor.py` writes `bets.jsonl` only after both steps finish. Every stop (cap, refusal, error) calls `sys.exit` first. So a stop in step 2 (order check) leaves step 1, which §3 says is "alone enough for every bet", unscored. A stop in step 1 leaves any already-scored post items unscorable, though §5.1 counts them.

**Non-blocking notes (no fix required):**
- §9's ledger entry says `budget_usd: 6.0`, but the cap is $5.00.
- `score.py`'s `year_bin` labels moved papers (ss-152, dated Aug 2026) "2026-pre", which §4 calls "2026 before the cutoff".
- The SDK client uses `max_retries=4` (transport retries of the identical request). Refusals are not retried.
- `human/make_form.py --score` reads `human/answers.md`, but since `04a9cd2` the form says calls count only from `ledger/human-odds.jsonl`.
- The leakage checker flags only cues toward the *reported* side. An over-corrected rewrite (a cue toward the other side) would pass. That biases against a pass, not toward one.

## Required fixes

Each needs a dated DEVIATIONS row (D11 onward) written before any bettor call, naming this review. None lowers a bar.

**F1 (D7). Apply Rule 2 to 2611.00420.** Set `"side": "pre"` on ss-026 and ss-027 in `items/items.jsonl`. Keep their ids, so that no beacon draw moves: the draws are keyed by id, and `masked.jsonl` does not change. Add `"2611.00420"` to `writer-exclusions.json` `earlier_version` with its comment quoted. Rewrite `SHA256SUMS` (items.jsonl only), and update §2's counts in a dated DEVIATIONS row: 117 post, 67 pre, interpretability 29 post / 18 pre. In the same row, state the venue rule used for every post item: a comment naming a 2026 ICML/ICLR workshop or main-track presentation, or an "extended version", moves the item to pre. Record the ss-094 (TMLR) decision either way, with its reason.

**F2 (D10). Make the refusal record reachable.** In `common.py`, before writing `refusal.md`, add `(ROOT / "results").mkdir(exist_ok=True)`, and print the request ID to stderr before the write. Re-run the stubbed-refusal check and show the file is written.

**F3 (D10). Never lose scored bets.** In `bettor.py`, write `bets.jsonl` from the cache after step 1 and again after step 2, in a `try/finally` around each `Caller.run`, so that every exit path saves the rows done so far. In the DEVIATIONS row, state that a stop with at least 60 post-cutoff items scored is scored on those items, with the unscored ones listed.

**F4 (D8, D1). Complete the verdict sentences.**
- **Untestable:** *"Too few findings were scored to test the bettor (n scored of 119; reason)."*
- **Fragile:** *"…; this label rests on one finding (item id): without it the label would be <other label>."*
- **ss-b2:** untestable whenever ss-b1 is.
- **ss-b3:** untestable whenever ss-b1 is, or when fewer than 30 pre-cutoff items are scored.
- **Pass sentence:** replace "119" with the scored n.
- **Code:** have `score.py` emit labels for ss-b2, ss-b3 and fragile.

**F5 (D9). Leave-one-item-out on every bet's label.** Extend `score.py`'s LOO to the ss-b2 paired difference and to ss-b3, both with the same rule (any single removal that flips the label marks it fragile, item named). Use 10,000 resamples with seed 20261104 for every LOO bound, as for the full-data bounds. Pre-register this in the DEVIATIONS row.

When these are committed, a short addendum here confirms them before the first bettor call.

## Addendum: fixes confirmed

Checked 2026-11-04 18:50 America/Denver against commit `954c035` (DEVIATIONS D12–D16), by the same reviewer session. No paid calls were made, and no bettor cache or `bets.jsonl` exists yet.

- **F1 holds.** `items.jsonl` differs from the frozen file only in `side` (post → pre) and a new `side_note` on ss-026, ss-027 and ss-094. The ids are unchanged, and `masked.jsonl` is unchanged (e9f60d9b…). `bettor.py --dry-run` gives the same draws as before: 184 items, 276 calls, option_b first on 94. The new `items.jsonl` SHA-256 is f924db16… and matches `SHA256SUMS`. Counts are 116 post and 68 pre (interpretability 29/18, model psychology 29/17, quantum devices 28/16, scalable oversight 30/17), as D12 states. `writer-exclusions.json` names both papers. D12 states the venue rule, which goes beyond the required fix by also moving ss-094 (TMLR). A scan of every item's comments finds no post-cutoff item left that names ICML, ICLR, TMLR or an earlier or extended version.
- **F2 holds.** A refusal stubbed against scratch copies of the new `common.py` and `bettor.py` prints the request ID to stderr, creates `results/`, and writes `refusal.md` with the ID.
- **F3 holds.** The same stub saves the bets made so far on every exit: a refusal at call 70 of step 1 leaves 69 primary bets in `bets.jsonl`, and a refusal in step 2 leaves all 184 primary bets plus 15 order-check bets. D14 records the rule for scoring a partial run.
- **F4 holds.** D15 writes the untestable and fragile sentences and the untestable rules for ss-b2 and ss-b3, and the sentences use the scored n. `score.py` emits a label per bet:
  - 50 post items scored → all three untestable;
  - no pre-cutoff items → ss-b3 untestable;
  - memory-only bettor → ss-b3 pass, ss-b1 null;
  - `--synthetic` coin, oracle, headline and anti → ss-b1 null, pass, null (upper 0.255) and null.
- **F5 holds.** Leave-one-item-out now runs on all three bets, with 10,000 resamples and seed 20261104. A synthetic bettor placed just under the line (upper 0.2486) is labelled "pass, fragile", with the 80 items that flip it named. D16 records two further changes: the bootstrap moved to numpy, and a 1e-12 tolerance was added to the "below" tests. The tolerance only tightens the rule. Both changes come before any data.

Still open, none of it blocking:
- leakage-check.md §5 still says "two quantum-devices items".
- `year_bin` labels the moved 2026 papers "2026-pre".
- `make_form.py --score` reads `human/answers.md`, not `ledger/human-odds.jsonl`.
- The auditor should confirm from the API usage record that no claude-sonnet-5-5 call ran before 17:17:16.

**Verdict is now go.** The first bettor call may run.

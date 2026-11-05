# ss-b7: the "more striking finding" rater, with a noise margin (pre-registration)

Written 2026-11-04 (America/Denver; the commit time is the record). It is committed on its own, before any striking-rater call. The budget is the program's **$5.00** cap, enforced in code: $4.08 has been spent, and this bet should cost about $0.68 (the engine approved $0.46; the $0.22 retest needs its OK). Stop on any refusal, and nothing is reworded or retried.

## 0. The bet

| field | value |
|---|---|
| bet id | `ss-b7` |
| referee | `published-record` (the sentence as printed in the arXiv abstract) |
| bet type | `standard` |
| direction | `ss-b7`, parent `ss-b6` (map/settled-science.json) |
| source | `engine`: the ss-b6 audit's named rival (D32), approved by the engine (st-16) |
| engine odds, P(pass) | **40**, stated in commit `0b8255c`, before any striking-rater call |
| human odds | not recorded (rule 11) |
| budget | at most $0.92, the rest of the $5.00 cap · 0 QPU s |
| pre-mortem | "If this fails, the most likely reason is that the striking rater, like the flattery rater, picks the published sentence nearly as well as the bettor, so leg 2 does not clear the noise margin." Kind: `world`. |
| lesson | Correcting P12 and P9: ss-b6's rule let a no-extra-knowledge bettor pass 24–61%, and its write-up overclaimed. This bet adds a retest-noise margin and fixed sentences; odds 40%. Read: 17 scored, Brier 0.264, base rate 7/17 (running 0.42), newest audit ledger/audits/ss-b6.md. |
| design review | a fresh session the **engine session** launches; written to `ledger/design-reviews/ss-b7.md` |
| auditor | fresh session per operators/auditor.md, after results |

## 1. In plain English

Round 2's bettor picked the published sentence 93% of the time. A same-model rater asked only which version flatters the paper matched most of that (90%). The ss-b6 audit named another simple explanation the flattery prompt did not test: the bettor might be picking whichever version reports the more **striking** finding, the one a reviewer would find notable. This bet asks a fresh session that question on the same 92 pairs.

ss-b6 taught a second lesson. At the bar it used, a bettor that knew nothing beyond the rater would still pass a large share of the time, because the rater's own noise makes it lose. That is ledger pattern P12: a bet that cannot fail buys calibration without information. So this bet first measures the rater's own noise, by asking it each of 46 items twice with the options reversed. It then sets a margin that a bettor in that null world clears at most 10% of the time. **The bettor must beat the striking rater by more than its noise can explain.**

## 2. Material

- **Items:** the same 92 drawn round-2 items, in the bettor's primary-call option order (the ss-b4 seed `e8f921e`). No new draw is made, so there is no beacon commit.
- **Striking rater:** claude-opus-5-5, one fresh call per item, no tools, at the bettor's setting (adaptive thinking at effort low, hidden; max_tokens 4000; D18). The prompt is `SYSTEM_STRIKING` in `bettor/valence.py`, verbatim. It uses the hypothetical framing of D32 and the user text `Field: …` plus the two options. It asks the probability "that Option 1 reports the more striking finding: the one that readers and reviewers in this field would find more notable or surprising". The key tag is `striking-v1`, with its own cache and outputs (`bettor/r2-striking*.jsonl`). No other provider's key was looked for.
- **Retest:** the same rater, asked again on the bettor's 46 order-check items in reversed order (`valence.py --striking --retest`).
- **Bettor ratings:** the existing ss-b5 primary calls. No new bettor call is made.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | striking rating on each of the 92 items | 92 | about $0.46 |
| 2 | striking retest on 46 items, options reversed | 46 | about $0.22 |

**Step 2 is required:** the margin needs it. If the engine does not approve the $0.22, the fallback (decided now) is to use ss-b6's measured valence-rater retest noise, σ = 0.274, and to say so in the results.

## 4. Statistics

- **Leg 1** (raw) and **leg 2** (recalibrated with the up word, leave-one-out logistic) are exactly as in ss-b6 (D33). The code is `score.py` `score_b6` internals, reused by `score_b7`.
- **Noise margin (P12).**
  - σ_rt is the rater's single-rating logit noise: the SD over the 46 retest pairs of [logit(v) − logit(1 − v′)], divided by √2.
  - m* is the 10th percentile of leg-2 upper bounds over 100 null-world simulations. In each simulation the rater is logit(bettor) + N(0, σ_rt), rounded to a whole number from 1 to 99. Seed 20261104, with 2,000 bootstrap resamples inside each simulation.
  - In that world the bettor knows only what the rater measures, and it passes at most about 10% of the time.
  - Code: `retest_sigma` and `null_margin`.
- **Pass rule:** at least 60 items, leg 1's upper bound below 0, **and** leg 2's upper bound below m*.
- **Reported, not tested:** the up-word and down-word subsets on both legs; G1–G3, as reported counts, not gates; the discordant and opposite-side items; the striking rule's Brier and accuracy with CIs.
  - G1 does not gate here. A striking rater may honestly favour the down word, and leg 2 does not depend on scale direction.
- **Robustness:** leave-one-item-out and leave-one-query-bucket-out on the label. A flip makes the result "fragile"; a remainder under 60 is untestable.
- **Dry runs before this commit**, with synthetic raters against the real bettor (`score.py --b7 --synthetic`):

| synthetic rater | result |
|---|---|
| coin | pass |
| up-word | pass |
| valence50 | pass, fragile |
| copy | null |
| oracle | null |
| copy + 0.27 logit noise | null (margin −0.0018) |
| copy + 0.6 logit noise | null (margin −0.0045) |

  So it can pass and it can fail (D11).
- **On ss-b6's own data**, the null world at its retest noise (0.274) gives m* = −0.0033. ss-b6's leg-2 upper bound (−0.0018) would not have cleared it. That is reported here as motivation, not as a re-score of ss-b6.

## 5. Pre-registered reading (sentences generated by `score_b7`)

1. **Pass:** *"On n round-2 sentence pairs, the bettor picked the published sentence better than the same model asked only which version reports the more striking finding (raw d₁ [lo, hi], striking rule Brier v; recalibrated with the up word d₂ [lo, hi], beyond the noise margin m*). Round 2's pass is not only picking the more striking version, as this rater judged it, though this does not separate knowing the result from reasoning within the sentence, and the rater was the same model as the bettor."*
2. **Null:** *"On n round-2 sentence pairs, the bettor was not shown to pick the published sentence better than the same model asked only which version reports the more striking finding (raw d₁ [lo, hi]; recalibrated with the up word d₂ [lo, hi], against the noise margin m*). Round 2's pass may reduce to picking the more striking version, or the rater, being the same model, may have used the same judgment of which version is real; this test cannot tell those apart."*
3. **Untestable:** fewer than 60 ratings, or no retest. Sentence: *"Too few ratings were returned to test it (n of 92)."*
4. **Fragile:** append *"; this label rests on <items / buckets>: without <it / any one of them> the label would be <other label>."*
5. **Scope, beside the verdict:** *"Both the bettor and the rater ran as claude-opus-5-5 with adaptive thinking at effort low, with reasoning hidden; the result is about that setting."*

A pass is **pass, unreplicated**.

## 6. What it cannot do

- **The rater is the same model as the bettor.**
- **"More striking" is one prompt's reading of publishability.**
- **The null world takes the bettor's own ratings as the rater's underlying signal.** Other null worlds would give other margins.
- **It covers the round-2 template items only.** It says nothing about round 1.

## 7. Stop rules

The $5.00 cap, in code. Stop on any refusal or API error.

## 8. Ledger entry

```json
{"id": "ss-b7", "program": "settled-science", "direction": "ss-b7", "title": "Round 2c: the bettor beats a 'more striking finding' rater beyond a retest-noise margin",
 "source": "engine", "engine_odds": 0.40, "engine_odds_at": "2026-11-04 21:05 America/Denver", "human_odds": null, "prereg_commit": "<this commit>",
 "referee": "published-record", "bet_type": "standard", "seed_source": "inherited (ss-b4 seed e8f921e; no new draw)",
 "premortem": "If this fails, the most likely reason is that the striking rater, like the flattery rater, picks the published sentence nearly as well as the bettor, so leg 2 does not clear the noise margin.",
 "premortem_kind": "world", "verdict": "open"}
```

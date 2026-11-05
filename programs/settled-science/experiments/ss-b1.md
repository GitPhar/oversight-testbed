# ss-b1: the published-record referee, first round (pre-registration)

Written and frozen 2026-11-04 18:45 (America/Denver), in its own commit, before any bettor call. DEVIATIONS.md D1–D8. Budget **$5.00** for the leakage check and the bettor together, enforced in code (`common.py`, `BUDGET_USD`); $0.47 of it was spent on the leakage check before this commit. Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

## 0. The bet

| field | value |
|---|---|
| bet id | `ss-b1` (primary); `ss-b2`, `ss-b3` (secondary bets, same run, own odds) |
| referee | `published-record`: the direction stated in the arXiv abstract of a 2024–2026 paper decides each item |
| bet type | `standard` |
| direction | `ss-b1` (map/settled-science.json) |
| source | `human` (Sean's program brief, 2026-11-04) |
| engine odds, P(pass) | ss-b1 **50** (first 60, lowered before data for lesson P1); ss-b2 **30**; ss-b3 **35**; stated 2026-11-04 17:12 in map/settled-science.json, commit `4963270`, before any drafted item was read |
| human odds, P(pass) | not recorded (D2). Sean's part is the 20-item direction-level form (§6). |
| budget | $5.00 API (shared with the leakage check) · 0 QPU s · under 1 laptop hour |
| pre-mortem | "If this fails, the most likely reason is that the bettor, without wording cues, sits near 50% on most descriptive items, so a Brier near 0.23 leaves the upper bound above 0.25." Kind: `design`. |
| lesson | Correcting P3 and P1: past rules a trivial predictor could pass, and odds set high on a plausible story. This bet pre-registers a publication-bias baseline beside the constant 0.5 and scores beating it as its own bet (ss-b2), and its odds are 50% (from 60% on the map) because 2 of 9 scored bets hit. Also applied: P9 (the verdict sentences are written in §5 before data) and P10 (leave-one-item-out on the pass rule, §4). Read: 9 scored bets, Brier 0.236, base rate 0.22, newest audit ledger/audits/om-p2-1-blind-pl-001.md. |
| design review | fresh session per operators/design-review.md, launched by the engine session after this commit, before the first bettor call; written to `ledger/design-reviews/ss-b1.md` |
| auditor | fresh session per operators/auditor.md, after results |

## 1. In plain English

We want to know whether the engine's model can tell which way a scientific finding went before it is told. We took 184 findings from real arXiv papers in four fields (model psychology, interpretability, scalable oversight and quantum-device physics) and wrote each one as a two-sided question whose answer the paper's abstract states. 119 of them come from papers first posted after the bettor model's training cutoff (June 2026), so it cannot have read them; those are the test. A separate session with no tools at all sees each masked question and gives the probability of each direction. The published record decides each one, and we score the probabilities with the Brier score, where always saying 50% scores 0.25. The rival explanations for a good score are (a) the wording leaks the answer, which a third session checked item by item before use, and (b) the bettor has simply learned that papers usually report that their own method works, which a pre-registered "publication-bias" baseline measures (ss-b2).

## 2. Material

- **Bettor**: `claude-opus-5-5`, knowledge cutoff fixed at 2026-06-30 (protocol/fixed-rules.md). One fresh Messages API call per item; no `tools` field; thinking off (D6); structured output `{rationale, p_option_1}`; max_tokens 400. System prompt and user template verbatim in `bettor/bettor.py` (`SYSTEM`, `user_text`). It sees the field, question, methods and two options, and nothing else. Scale: 1 = Option 1 is almost certainly not the reported result, 99 = it almost certainly is.
- **Leakage checker** (Rule 3): `claude-sonnet-5-5`, no tools, prompt verbatim in `items/leakcheck.py`. Already run on every item before this commit: log `items/leakage-log.jsonl`, status `items/leakage-status.json`. 213 calls ($0.47): 161 items clean on the first check, 26 flagged; of those, 23 were clean after one wording-only rewrite (`items/rewrites.jsonl`) and 3 were flagged again and dropped. The rule was committed before the first call (`d3996c9`) and the outputs before this file (`4859d3b`).
- **Items**: `items/items.jsonl` (with answers) and `items/masked.jsonl` (what the bettor reads). SHA-256 in `items/SHA256SUMS`:
  ```
  afe0c80df44212309c38a1be1ff19d2910a3d3f470d04680efb855e7730a6e86  items/items.jsonl
  e9f60d9b74b8f381a21d5b2d0fc9bd2baeffd2406e6780ebb14c427379097e81  items/masked.jsonl
  ```
  184 items: 119 post-cutoff (v1 dated 2026-07-01 to 2026-11-04), 65 pre-cutoff (2024-01-01 to 2026-06-30). By field and side: post-cutoff: interpretability 31, model psychology 29, quantum devices 28, scalable oversight 31; pre-cutoff: interpretability 16, model psychology 17, quantum devices 16, scalable oversight 16 (2024: 21, 2025: 22, 2026 H1: 22). Every item passed `items/verify.py` (arXiv id, title and v1 date from the arXiv API; evidence quote verbatim in the abstract; banned words; options differ only in their direction slot) and the leakage check. Selection rule: `protocol/item-spec.md`. Items were written by the item-writer session and six helper sessions launched by it (Opus 5.5), from arXiv abstracts read through the arXiv API.
- **Seed** (operators/hardware.md): CURBY-Q latest completed round **28297**, result pulse 2025-08-22 13:42 America/Denver (checked 2026-11-04 16:55). That is more than 24 hours old, so CURBY-Q is stalled. **Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = the first 8 bytes of SHA-256(randomness ‖ bet-id), unsigned big-endian, with sub-seeds by `ledger/seed.py <randomness> ss-b1 --purpose <p>` for three purposes:
  - `order`: `random.Random(seed).random() < 0.5`, drawn once per item in id order, decides whether option_b is shown as Option 1 (primary call).
  - `order-check`: `random.Random(seed).sample(ids, k = n // 2)` picks the items asked a second time with the options reversed.
  - `human-form`: `random.Random(seed).sample(...)`, five post-cutoff items per field in field order, then shuffled (`human/make_form.py`).
  Filled in by the seed commit, before any bettor call:
  `chain:` CURBy-RNG · `pulse_index:` 1591496 · `pulse_time:` 2026-11-04 17:32:00 America/Denver (previous pulse 1591495 at 17:31:00, before the 17:31:23 pre-registration commit) · `randomness:` 27bba9e6c499e9a8a5647a0fcbdfd2947575e32c8a466e1f8b3daf80b95adeee2ba5836c348be9e0714f139e1b0edd4011d11494400f87c3729e7d1892e9731a · `client:` @buff-beacon-project/curby-client@1.2.0 · `certificate_verified:` false · `seeds:` order 13309338689196222401, order-check 16683013961078861871, human-form 14605333098254812962 (bettor/seed.json)
- Bootstrap resampling uses the fixed constant seed 20261104 (allowed by operators/hardware.md).

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | primary bettor call, every item, beacon-drawn option order | 184 | about $0.90 |
| 2 | order check: a seeded half, asked again with options reversed (secondary) | 92 | about $0.45 |

Step 1 alone is enough for every bet. Every call is cached by a content hash (`bettor/bettor-cache.json`). The cap is shared with the leakage check and checked before every call.

## 4. Statistics

- **Primary statistic (ss-b1)**: Brier score on the post-cutoff items, mean over items of (1 − p_true)², where p_true is the bettor's primary-call probability on the reported option (p_option_1 clipped to [1, 99], divided by 100). Unit: items. No ties arise.
- **Uncertainty**: percentile bootstrap over items, 10,000 resamples, seed 20261104.
- **ss-b2**: paired difference, mean over post-cutoff items of [(1 − p_true)² − (1 − h)²], where h = 0.75 if the item's `headline_side` (tagged by the item-writer before any bet) is the reported option, 0.25 if it is the other option, 0.5 if untagged. Bootstrap as above.
- **ss-b3**: Brier(pre) − Brier(post), independent two-sample bootstrap, 10,000 resamples, seed 20261104.
- **Secondary, labelled secondary, never promoted to a headline**: Brier, accuracy and the headline-baseline comparison by field, by year (2024, 2025, 2026 before the cutoff, 2026 after it), by cutoff side and by headline tag; calibration table (confidence in the favoured side against how often it was right); order check (mean |p + p′ − 100| and the mean pull toward whichever option is shown first, with a bootstrap CI).
- **Multiple comparisons**: three bets, each with its own odds, scored separately; no correction, because each is a separate ledger entry. The by-field and by-year tables are descriptive, with no test.
- **Robustness checks committed now**: leave-one-item-out on ss-b1's pass rule (2,000 resamples each), with the flipping items listed; the by-field split; results with and without items that needed a leakage rewrite.
- Pre-cutoff results never enter the headline and always carry the caveat that the bettor may have read those papers.

## 5. Pre-registered reading

1. **ss-b1 pass**: at least 60 post-cutoff items scored, and the upper end of the 95% CI on the post-cutoff Brier is below 0.25. Sentence: *"On 119 findings published after its training cutoff, the bettor's probabilities beat always saying 50% (Brier b [lo, hi])."*
2. **ss-b1 null**: at least 60 scored and the upper bound is 0.25 or above. Sentence: *"On these findings the bettor's probabilities were not shown to beat always saying 50% (Brier b [lo, hi])."* If the lower bound is also above 0.25: *"…and scored worse than always saying 50%."*
3. **ss-b1 untestable**: fewer than 60 post-cutoff items scored (a refusal stop, the cap, or errors).
4. **ss-b2 pass**: the upper bound of the paired difference is below 0. Sentence: *"The bettor beat a predictor that only knows papers tend to report that their own method works."* Otherwise: *"The bettor was not shown to beat a predictor that only knows papers tend to report that their own method works."*
5. **ss-b3 pass**: the upper bound of Brier(pre) − Brier(post) is below 0. Sentence: *"The bettor scored better on papers it may have read than on papers it cannot have read, consistent with memory (or with the older items being easier; this design cannot separate the two)."* Otherwise: *"No memory advantage on older papers was shown."*
6. **Leave-one-item-out**: if removing any one item flips ss-b1's label, the verdict is reported as **fragile**, with the item named.
7. **Reported in every case**: n by side and field, Brier with CIs by field, year and side, the headline baseline, the calibration table, the order check, spend, refusals, and every dropped item with the reason.

A pass is reported as **pass, unreplicated** (invariant 7): one bettor model, one item set, one prompt.

## 6. Sean's form (not a bet; scored item by item)

Twenty post-cutoff items, five per field, drawn by the `human-form` sub-seed, options in the same order the bettor saw. Sean writes 1 or 2 and, if he likes, how sure (50–100; blank = 75). No engine odds, answers or ranking appear on the form. Scored by `human/make_form.py --score`: directions right, and Brier, for Sean and for the bettor on the same items. With 20 items this is descriptive only.

## 7. What it cannot do

- It scores the **published claim**, not the truth: a wrong paper scores as right. Publication bias is part of the referee, which is why ss-b2 exists.
- Item-writer and bettor are the same model family (Opus 5.5). The writer might, without meaning to, pick findings whose direction its own family would find easy or hard. Selection rules were fixed before items were drafted, but this cannot be ruled out.
- Post-cutoff means "first arXiv version after 2026-06-30". Earlier talks, blog posts or workshop versions could have reached training data; items with an earlier version named in the arXiv comments were moved to pre-cutoff.
- One bettor model, one prompt, abstract-level findings, four fields. "Every", "all" and "LLMs" will not appear in the write-up.
- The leakage checker is a language model. It catches wording cues it can see, not every cue.

## 8. Stop rules

- Budget cap in code: $5.00 total. If reached, later steps are reported as not run.
- Stop on any refusal; no rewording; no retry.
- Stop on any API error (the run resumes from cache after the cause is fixed; no item is re-drawn).

## 9. Ledger entry (filled now, completed after audit)

```json
{"id": "ss-b1", "program": "settled-science", "direction": "ss-b1",
 "title": "Published-record referee, round 1: post-cutoff Brier beats 0.25", "source": "human",
 "engine_odds": 0.50, "engine_odds_first": 0.60, "engine_odds_at": "2026-11-04 17:12 America/Denver",
 "human_odds": null, "human_odds_at": null, "human_odds_note": "D2: Sean's part is the 20-item direction-level form",
 "prereg_commit": "<this commit>", "budget_usd": 6.0,
 "referee": "published-record", "bet_type": "standard", "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "premortem": "If this fails, the most likely reason is that the bettor, without wording cues, sits near 50% on most descriptive items, so a Brier near 0.23 leaves the upper bound above 0.25.",
 "premortem_kind": "design", "premortem_at": "<this commit>", "human_premortem": null, "human_premortem_kind": null,
 "failed": null, "failure_reason": null, "failure_kind": null, "premortem_score": null, "human_premortem_score": null, "risk_seen": null,
 "verdict": "open", "date": "2026-11-04", "result": null, "audit": null, "diagnosis": null}
```

## 10. Checklist before the first call

- [x] This file is committed on its own; no bettor call has been made.
- [x] Engine odds on record elsewhere, earlier (map, commit `4963270`). Human odds: not recorded, D2.
- [x] The pass rules in §5 can be applied by a stranger.
- [x] One pre-mortem sentence with its kind.
- [x] One scale direction (1 = Option 1 not reported, 99 = Option 1 reported).
- [x] §2 records CURBY-Q's latest completed round and names CURBy-RNG by the 24-hour rule.
- [x] Budget and stop-on-refusal enforced in code.
- [x] DEVIATIONS.md rows D1–D8.
- [ ] Design review returns **go** before the first bettor call.

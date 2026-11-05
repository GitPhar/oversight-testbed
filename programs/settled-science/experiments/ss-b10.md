# ss-b10 (direction ss-f7): the flattery rule on BrainBench (pre-registration)

Written and frozen 2026-11-05 06:33 America/Denver, in its own commit, before any call and before any BrainBench item was scored. DEVIATIONS.md D51. Budget **$2.50**, enforced in code (`bettor/brainbench.py` `BET_CAP`; program cap raised from $5.00 to $7.50 by budget ruling br-004, `ledger/spend.jsonl`). Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). Sean's odds come only from `ledger/human-odds.jsonl`. This direction's card went on the cockpit at `c235cbb` (06:24), before its map node (`cb121d7`, 06:26) and before this file. `ledger/human_odds_match.py settled-science ss-f7` at 06:31 printed "no human odds", so the bet proceeds marked "no human odds".

## 0. The bet

| field | value |
|---|---|
| bet id | `ss-b10` |
| referee | `model`: a language model's ratings, scored against BrainBench's published labels (which abstract is the original) |
| bet type | `standard` |
| direction | `ss-f7` (map/settled-science.json; programs/settled-science/map/settled-science.md, section "ss-f7") |
| source | `literature` (paper/novelty.md, ranked replication 1, from finding 8) |
| engine odds, P(pass) | 35, stated 2026-11-05T06:25 in map/settled-science.json (`cb121d7`); **30 after the lesson** (both kept) |
| human odds, P(pass) | no human odds (`ledger/human_odds_match.py settled-science ss-f7`, 06:31) |
| models | `claude-haiku-5-5` and `claude-sonnet-5-5`, **not Opus**: this is the novelty page's named replication on these two models, and Opus at its least-thinking setting (it cannot turn thinking off, D18) would cost about $2.90 for both prompts on 200 items, more than the whole ruling. Opus's flattery rater already has its own result on round 2 (ss-b6). |
| budget | $2.50 API (estimate about $1.70 at measured token counts; the dry run's conservative character estimate is $2.09): Haiku about $0.10, Sonnet about $1.60. 0 QPU s, 0 laptop hours. Includes any design-review pilot. |
| lesson | "Correcting P3, P14: ss-b6's flattery rater ran on our own pipeline's items with no text-only rule beside it. This bet uses expert-written items, five fixed text-only rules and a leave-one-section-out check, and its odds are 30% (from 35% on the map) because P1 says start at the running base rate, 8/26 = 0.31." |
| design review | before the first call, a fresh auditor dry-runs this design (operators/design-review.md) → `ledger/design-reviews/ss-b10.md`. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that Haiku's flattery rater stays under 70% on the long abstracts, missing which version supports the paper's hypothesis, while Sonnet's clears the experts' rate." Kind: `world`. |
| auditor | fresh session per operators/auditor.md, after results |

## 1. In plain English

BrainBench is a well-known test of whether AI models can predict research results. Each of its 200 questions shows two versions of a real neuroscience abstract. One is the published abstract. The other was rewritten by a neuroscientist so that the results come out differently, while the abstract still reads sensibly. The original study (Luo et al., Nature Human Behaviour, 2024) found that language models picked the real abstract 81.4% of the time and 171 neuroscientists 63.4% of the time. It was reported as "AI beats experts at predicting science."

Our own program found a simpler rule. Asked only "which version is better news for the paper's own method?", and told to treat both versions as hypothetical, the strongest Claude model picked the real version of our sentence pairs 90% of the time (ss-b6). Published work mostly reports that its ideas worked. A model could therefore look good at "predicting results" just by picking the version that flatters the paper, without knowing anything about the results.

We ask that same flattery question on BrainBench's 200 expert-written items, with Haiku and Sonnet. **A hit means the flattery rule alone beats the neuroscientists' published 63.4% on both models.** We also ask the same two models directly which abstract was published (the program's bettor prompt), to see how much of their own skill the flattery rule matches. We compare both with the published 81.4%. Five text-only rules that use no model (length, word counts) are scored beside them, so we can tell whether something even dumber does as well. The rival explanation for a hit is memory: BrainBench and its abstracts were public before these models were trained.

## 2. Material

- **Models.** `claude-haiku-5-5` and `claude-sonnet-5-5`. Thinking is off, through `common.structured` (Haiku `{"type": "disabled"}`; Sonnet `{"type": "between_tools"}` with no tools, D6). Each call records the setting used. Structured output `{rationale: string, p_option_1: integer}`, `max_tokens` 1000, no tools field, no temperature set.
- **Prompts, verbatim in `bettor/brainbench.py`:**
  - `FLATTERY` (system). The ss-b6 valence prompt (D32), with three changes. "two versions of a sentence reporting a study's result. They differ in one word." becomes "two versions of a study's abstract. They differ only in the results they report." "a paper actually contains" becomes "was actually published". "for the method, system or approach that the paper itself proposes or defends" becomes "for the hypothesis, method or account that the paper itself proposes or defends", because neuroscience abstracts usually defend a hypothesis rather than a method. User text: `Field: neuroscience (<journal section>)`, then Option 1 and Option 2. The prompt has no question and no forecasting frame.
  - `BETTOR` (system). `bettor/bettor.py` `SYSTEM`, verbatim (rounds 1 and 2). User text: the field line; `Question: Which of these two abstracts is the one the study published?`; `Methods: No summary is given. The two options are the same abstract, one as published and one with its results altered by an expert so that it still reads coherently.`; then Option 1 and Option 2.
- **Items.** BrainBench's 200 human-written items, `items/brainbench/items.jsonl` (`bb-001` to `bb-200`; SHA-256 `0a9acfeb…` in `items/brainbench/SHA256SUMS`, frozen at `e97fe46`, source and revision in `items/brainbench/SOURCE.md`). All 200 are used, with no filter. The 100 GPT-4-written items (`gpt4-pilot-pool.jsonl`) serve only an execution pilot, if the design review asks for one. They are never test data.
- **Seed** (operators/hardware.md). CURBY-Q stalled: latest completed round 28297, result pulse 2025-08-22 13:42 America/Denver (checked 2026-11-05 06:31 with `bettor/curby_seed.mjs check`). Seed: the first CURBy-RNG pulse timestamped after this commit. seed = the first 8 bytes of SHA-256(randomness ‖ "ss-b10" ‖ ":" ‖ purpose), unsigned big-endian (`ledger/seed.py --purpose`). Purposes: `order` (per item, whether the original is shown as Option 1, `random.Random(seed).random() < 0.5` in id order) and `order-check` (the 100 items whose flattery rating is asked again with options reversed, `random.Random(seed).sample(ids, 100)`). The seed commit writes `bettor/bb-seed.json`. *Filled in by the seed commit, before any data:*
  `chain:` ___ · `round:` ___ · `pulse_time:` ___ · `randomness:` ___ · `client:` @buff-beacon-project/curby-client@1.2.0 · `certificate_verified:` false · `seed:` ___
- **Scale.** One direction in both prompts: 1 = Option 2 / not Option 1, 99 = Option 1, 50 = cannot tell or no difference.
- **Published comparators**, read in the paper (arXiv 2403.03230v4 HTML, 2026-11-05): "LLMs averaging 81.4% accuracy and human experts averaging 63.4%", both on the 200 human-written items. The LLMs were scored by which abstract had the lower perplexity, not by being asked; base models beat chat models.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | Haiku, flattery, primary | 200 | $0.03 |
| 2 | Haiku, bettor, primary | 200 | $0.03 |
| 3 | Sonnet, flattery, primary | 200 | $0.55 |
| 4 | Sonnet, bettor, primary | 200 | $0.60 |
| 5 | Haiku, flattery, order check (options reversed) | 100 | $0.02 |
| 6 | Sonnet, flattery, order check | 100 | $0.28 |
| | **total** | 1,000 | about $1.70 (cap $2.50) |

- The run order is as listed. Steps 1 and 3 alone are enough for the primary statistic. If a cap stops the run, later steps are reported as not run.
- Every call is cached by a content hash (`bettor/bb-cache.json`, registered in `common.CACHES`), so a crash never pays twice. Before every call, `common.Caller` checks the program cap ($7.50) and this bet's own cap ($2.50, minus any pilot).

## 4. Statistics

- **Primary statistic, per model:** the flattery rater's accuracy on the 200 items. Let p_orig be the probability the rating puts on the original abstract (p_option_1, clipped to 1–99, divided by 100; or 1 minus that when the original is Option 2). An item scores 1 if p_orig > 0.5, 0.5 if p_orig = 0.5, and 0 otherwise. The unit is the item.
- **Uncertainty:** a percentile bootstrap over items, 10,000 resamples, `numpy.random.default_rng(20261104)` (the program's fixed bootstrap seed). Bounds are the sorted values at index int(0.025 n) and int(0.975 n) − 1. Every threshold is compared with tolerance 1e-12 (P13).
- **Split:** none. Nothing is fitted.
- **Secondary statistics** (reported, never promoted to the headline):
  - S1. The bettor's accuracy and Brier per model. Paired with the flattery rule on the same items: the accuracy difference (bettor minus flattery) and the Brier gain, each with its paired bootstrap CI.
  - S2. The share of the bettor's above-chance accuracy that the flattery rule matches, (acc_f − 0.5) / (acc_b − 0.5), with a paired bootstrap CI. It is computed only if the bettor's lower bound is above 0.5.
  - S3. Each prompt's accuracy against the published 0.814: "below" if the upper bound is below it, "above" if the lower bound is above it, otherwise "not shown different".
  - S4. **Dumb baselines**, fixed now, with no model. Each picks the original by a text rule; a tie scores 0.5. The rules: (a) longer abstract (characters); (b) shorter abstract; (c) more up-words minus down-words (regexes `UP`, `DOWN` in `scoring/score_bb.py`); (d) fewer negation words (`NEG`); (e) more "significant(ly)". Each is reported with its CI and whether its lower bound clears 0.634.
  - S5. Agreement: items where the two prompts favour the same version, and how often the bettor is right where they disagree.
  - S6. Order check (flattery only, the 100 beacon-drawn items): the same-side rate, mean |p + p′ − 100| with CI, the Option-1 pull (p + p′ − 100)/2 with CI, and accuracy with the two orders averaged.
  - S7. The number of 50s. The number of flattery rationales that reason about which version is real (ss-b6 G3's regex without "abstract", which every rationale here uses).
  - S8. Accuracy by *Journal of Neuroscience* section (descriptive).
- **Multiple comparisons:** the bet is one conjunction (both models), with no correction. Everything else is secondary and labelled so.
- **Robustness checks committed now** (P10, P14): leave-one-item-out on each model's condition (lower bound > 0.634), and leave-one-section-out over the five sections (the shared-source cluster). Any flip is reported in the verdict sentence as fragile. Neither check changes the verdict.

## 5. Pre-registered reading

Per model, "clears" means the flattery rater's accuracy has a 95% lower bound above 0.634 (tolerance 1e-12).

1. **Pass:** both Haiku and Sonnet clear. Reported as **pass, unreplicated**. Sentence: *"On BrainBench's 200 expert-written abstract pairs, a model asked only which version is better news for the paper's own idea picked the published abstract more often than the 171 neuroscientists in the original study did (63.4%), on both Haiku (a% [lo, hi]) and Sonnet (b% [lo, hi]); the published average for LLMs, scored by perplexity rather than by asking, was 81.4%. A one-line valence shortcut solves much of BrainBench on these two models; this does not show that the LLMs in the original study used it."*
2. **Mixed:** exactly one model clears. This is not a pass. Sentence: *"On BrainBench's 200 expert-written abstract pairs, a model asked only which version is better news for the paper's own idea beat the neuroscientists' published 63.4% on <model> (a% [lo, hi]) but not on <other> (b% [lo, hi]), so the shortcut beats the experts on one of the two models only."*
3. **Fail:** neither model clears. Sentence: *"On BrainBench's 200 expert-written abstract pairs, a model asked only which version is better news for the paper's own idea was not shown to beat the neuroscientists' published 63.4% on either Haiku (a% [lo, hi]) or Sonnet (b% [lo, hi]), so this valence shortcut does not account for BrainBench's 'LLMs beat experts' result on these models."*
4. **Untestable:** fewer than 150 of 200 primary flattery ratings were scored on either model (a refusal stop, the cap, errors). Sentence: *"Too few ratings came back to test it (<model>: n of 200 flattery ratings scored, at least 150 needed)."* The other model's numbers are still reported.
5. **Reported in every case**, in this order after the main sentence (all generated by `score_bb.py`):
   - Per model: *"Asked directly which abstract the study published, <model> was right x% [lo, hi] of the time, d points more|less than its flattery rule (difference [lo, hi]); the flattery rule matched s% [lo, hi] of its above-chance accuracy."*
   - Per model: *"<model>'s flattery rule was below | above | not shown different from the published 81.4% for LLMs (interval [lo, hi])."*
   - If any dumb baseline clears 0.634: *"A text-only rule (<names>) also beat the experts' published rate, so beating the experts does not need flattery judgement on these items."*
   - Fragile clauses from leave-one-item-out and leave-one-section-out.
   - Always: *"BrainBench and its source abstracts (Journal of Neuroscience, 2023) were public before both models' training data were collected, so either prompt may draw on memory of the benchmark or of the papers; the models ran with thinking off, and the prompts asked for a rating, not the perplexity the original study used."*
6. **Scoring for the ledger:** outcome 1 if pass, 0 otherwise (mixed, fail). An untestable bet is not scored.

## 6. What it cannot do

- **Memory.** BrainBench has been public since March 2024, with both versions of every item. A model may remember the benchmark or the papers, and nothing here separates that from judgement. The flattery prompt asks the model to treat both versions as hypothetical, but that cannot stop recognition. S7 counts the rationales that reason about which version is real.
- **Not the original study's method.** The LLMs in Luo et al. were base models scored by perplexity, and ours are chat models asked for a rating. So "the flattery rule matches x% of the bettor" is about our bettor, not theirs. The comparison with 81.4% is with a different measurement and is stated that way.
- **"Better news for the paper" is one prompt's judgement.** The adaptation from "method" to "hypothesis, method or account" is ours. A different wording could score differently. A rater from the same family as the bettor may share its sense of which version is real.
- **Two models, one benchmark, one prompt each.** No "LLMs" or "every model" sentence will appear.

## 7. Stop rules

- Budget caps in code: $2.50 for this bet and $7.50 for the program. If a cap is reached, later steps are reported as not run.
- Stop on any refusal: no rewording, no retry, and `results/refusal.md` is written.
- Stop on any error or truncation (`llm._check_stop`). The ratings made so far are written to `bettor/bb-ratings.jsonl` on every exit path.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "ss-b10", "program": "settled-science", "direction": "ss-f7", "map": "map/settled-science.json",
 "title": "The flattery rule on BrainBench's 200 expert-written items (Haiku, Sonnet)", "source": "literature",
 "odds_event": "On BrainBench's 200 human-written items, for both claude-haiku-5-5 and claude-sonnet-5-5, the flattery rater's accuracy has a 95% item-bootstrap lower bound above 0.634 (the published human-expert mean).",
 "engine_odds": 0.30, "engine_odds_first": 0.35, "engine_odds_at": "2026-11-05T06:25",
 "human_odds": null, "human_odds_at": null, "human_odds_note": "no human odds (ledger/human_odds_match.py settled-science ss-f7, 06:31; card c235cbb 06:24)",
 "prereg_commit": "<this commit>", "budget_usd": 2.50, "referee": "model", "bet_type": "standard", "seed_source": "curby-rng",
 "lesson": "ls-ss-b10", "premortem_kind": "world", "verdict": "open"}
```

## 9. Checklist before the first call

- [x] This file is committed on its own; nothing has been run.
- [x] The lesson row is filled after reading ledger/bets.jsonl, brier.md, audits/ and lessons.jsonl; the same sentence goes to `ledger/lessons.jsonl` as `ls-ss-b10`.
- [ ] A fresh design review has returned go, or fix-first confirmed.
- [x] The direction's cockpit card (`c235cbb`) was committed before this file; `ledger/human-odds.jsonl` was read at 06:31.
- [x] Engine odds are on record with an earlier timestamp (`cb121d7`); human odds: none.
- [x] One scale direction in every prompt.
- [x] §2 records CURBY-Q's latest completed round and names the chain by the 24-hour rule.
- [x] Budget and stop-on-refusal are enforced in code.
- [x] DEVIATIONS.md D51.

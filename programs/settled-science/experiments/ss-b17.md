# ss-b17 (direction ss-f10): ss-b10c's flattery question in a second wording, Haiku and Sonnet, all 200 BrainBench items (pre-registration)

Written and frozen 2026-11-05 16:33 America/Denver, in its own commit, before any call. DEVIATIONS.md D81. Budget **$2.25**, enforced in code (`bettor/brainbench_v2.py` `BET_CAP`; budget ruling br-020 on Sean's budget steer; program cap $21.40, D79). Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This direction's card went on the cockpit first (`6ee9bb7`, no engine odds), before its map node (`458613a`) and this file. Main was merged into this branch and `python3 ledger/human_odds_match.py settled-science ss-f10` was run immediately before this commit: "no human odds".

> **One run, one scored bet** (rule 15). This bet's decisive data are 800 new calls with a wording no earlier bet used; ss-b10c's first-wording ratings are the comparison, not this bet's data, so it is not `secondary_of` ss-b10c.

## 0. The bet

| field | value |
|---|---|
| bet id | `ss-b17` |
| referee | `model`: language models' ratings, scored against BrainBench's published labels (which abstract is the original), as ss-b10c |
| bet type | `standard` |
| direction | `ss-f10` (map/settled-science.json; programs/settled-science/map/settled-science.md, "Wave 5") |
| source | `engine` (the replication invariant 7 owes ss-b10c, whose limits say "one wording of each prompt"; design from the planning chat's launch message, funded by Sean's budget steer) |
| prior work | Prompt-paraphrase work predicts some movement and disagrees on how much. Mizrahi et al. 2024 (*TACL*, arXiv 2401.00595, abstract opened 2026-11-05) find single-instruction results brittle across 6.5M instances, 20 LLMs and 39 tasks. Sclar et al. 2023 (arXiv 2310.11324, abstract) report "performance differences of up to 76 accuracy points" on LLaMA-2-13B from formatting alone, few-shot. arXiv 2509.01790 ("Flaw or Artifact?", abstract; 7 LLMs including GPT and Gemini, 6 benchmarks, 12 paraphrased templates) finds that "much of the prompt sensitivity stems from heuristic evaluation methods", and that with LLM judges the variance drops substantially. None tests a valence question, BrainBench or a Claude 5 model; our answers are structured probabilities, not matched strings, which is the setting 2509.01790 finds more robust. Predicts: mixed. **What this bet adds:** the first paraphrase test of ss-b10c's shortcut, item by item against its first wording, on the two models that carried its rule. |
| engine odds, P(pass) | **37**, from a fresh v2 context handed `ledger/prior.md` (961d6ec) and this bet's description with the committed dry run (`scoring/dry_b16_b17.py`, 06b990c): prior 0.25, adjustment +0.12, reason "Settled-science (0.50) and engine (0.38) rows sit above the prior; dry run's valence-only world gives 0.95. Pulled back: both models must stay within a two-sided ±5 window, and Haiku's discordance is 0.305." Recorded on the map node ss-f10 at 13b4645, before this commit; the first odds stated for this direction. |
| human odds, P(pass) | no human odds (`ledger/human_odds_match.py settled-science ss-f10`, 2026-11-05 16:33, immediately before this commit; card 6ee9bb7 posted this afternoon and not yet on the live cockpit) |
| models | `claude-haiku-5-5` and `claude-sonnet-5-5`, not Opus (rule 12): the question is whether the two models that carried ss-b10c's pass rule keep it under another sentence (a replication completing an earlier run); Opus with the first wording is ss-b16's own bet, run beside this one. |
| budget | $2.25 API: Haiku 400 calls about $0.10, Sonnet 400 calls about $1.99 (ss-b10c's measured $0.00025 and $0.00497 per flattery call; the second wording is about as long). 0 QPU s, 0 laptop hours. |
| lesson | "Correcting P8, P2: ss-b10c's shortcut was tested in one sentence, so its result could be the sentence's. This bet freezes a second wording by hash, compares it item by item with the first on the same 200 items, with the 5-point window's power dry-run, and its odds are 37% (the first stated) because the window is two-sided." |
| design review | before the first call, a fresh auditor dry-runs this design (operators/design-review.md) → `ledger/design-reviews/ss-b17.md`. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that Haiku's averaged accuracy moves more than 5 points from 76.2% under the new wording, because its position-driven picks are near 0.5 on half its items." Kind: `world`. |
| auditor | fresh session per operators/auditor.md, after results |

## 1. In plain English

BrainBench (Luo et al., 2024) shows a real neuroscience abstract beside a copy an expert rewrote so the results come out differently; 171 neuroscientists picked the real one 63.4% of the time. ss-b10c asked two Claude models which version is "better news for the paper's own idea" and, with each pair shown both ways round and the answers averaged, found Haiku right 76.2% and Sonnet 88.2% on all 200 pairs. That was one sentence. If the result belongs to the shortcut (pick the version that is better for the authors' idea), any fair way of asking it should give about the same answer; if it belongs to the sentence, another wording will not.

So we wrote a second wording before any call and froze it by its SHA-256 (4173f67): which version's findings make the authors' own idea look better supported, and so would please the authors more. It shares no phrase with the first ("better news" does not appear). **A hit means both models, asked this way on all 200 pairs both ways round, clearly beat the neuroscientists (lower bound above 63.4%) and land within 5 points of what they scored with the first wording on the same pairs.** The rule is two-sided: a second wording that scores far higher also fails, because then the sentence matters. Prior work points both ways: prompt wording often moves accuracy, but less when answers are read by meaning rather than matched strings. Even a pass would not separate valence from plausibility or memory of the papers.

## 2. Material

- **Models and settings.** ss-b10c's: Haiku thinking `disabled`, Sonnet `between_tools` with no tools, max_tokens 1000, structured output `{rationale, p_option_1}`, no tools field (`common.structured`).
- **Prompt.** System: `bettor/prompts/flattery-v2.txt`, verbatim (SHA-256 of its text with the final newline stripped `72c5be33d3601a820d2d1cea00bf6630d8afb653aa320e0c43935e0971385d1d`, committed at 4173f67 before any code that calls it; `brainbench_v2.py` refuses to run on a mismatch). User text: ss-b10c's flattery user text, unchanged (`brainbench.user_text(it, "flattery", …)`: the field line, Option 1, Option 2). Cache tag `bb-flattery-v2`, so no key can collide with the first wording's.
- **The two wordings, in full.** First (ss-b10c, `brainbench.FLATTERY`): *"You will see the research field and two versions of a study's abstract. They differ only in the results they report. Treat both as hypothetical: do not try to judge which one was actually published. Write a short rationale of at most 100 words. Then give the probability, as a whole number from 1 to 99, that Option 1 is better news than Option 2 for the hypothesis, method or account that the paper itself proposes or defends. 1 means Option 2 is clearly better news for it; 99 means Option 1 clearly is; 50 means the difference is not good or bad news for anything the paper proposes."* Second (this bet): *"Below are a research field and two abstracts of the same study. The abstracts are identical except for the findings they describe. Consider both purely as hypothetical write-ups; it does not matter which of them, if either, is real. The study's authors set out to support an idea of their own: a hypothesis, a method or an explanation. Decide which version's findings make that idea look better supported, and so would please the authors more. Explain your reasoning in no more than 100 words. Then give a whole number from 1 to 99 for how likely it is that Option 1's findings favour the authors' idea more than Option 2's do. Use 1 if Option 2's findings clearly favour it more, 99 if Option 1's clearly do, and 50 if neither version favours the authors' idea over the other."* The second adds one notion the first lacks, that the better version "would please the authors more"; the claim is about the bundle of the two sentences (P8), not one word.
- **Items.** BrainBench's 200 human-written items, `items/brainbench/items.jsonl` (SHA-256 `0a9acfeb…`, frozen at `e97fe46`). All 200, no filter.
- **Orders.** Every item in both orders (original as Option 1, and as Option 2). No draw, so no beacon seed: `seed_source: fixed` (the bootstrap seed 20261104).
- **Comparator.** ss-b10c's first-wording flattery ratings, every item in both orders, `bettor/bbb-ratings.jsonl` (task `flattery`), read only: Haiku 0.762, Sonnet 0.882 on all 200.
- **Output.** `bettor/bbv2-cache.json` (in `common.CACHES`), `bettor/bbv2-ratings.jsonl`, `bettor/bbv2-run-status.json`.
- **Scale.** One direction: 1 = Option 2, 99 = Option 1, 50 = neither.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | Haiku, second wording, all 200 items, both orders | 400 | $0.10 |
| 2 | Sonnet, the same | 400 | $1.99 |
| | **total** | 800 | about $2.09 (cap $2.25) |

- Run order as listed; both steps carry the rule. If the cap stops the run, later calls are reported as not run and the untestable rule decides.
- Every call cached by content hash, so a crash never pays twice.

## 4. Statistics

- **Primary statistic, per model** (ss-b10c's item rule, `scoring/score_bbb.acc_block`): per item, p_avg = the mean of the two orders' probabilities on the original (p_option_1 clipped to 1–99, /100, or 1 minus that when the original is Option 2); item score 1 if p_avg > 0.5, 0.5 if = 0.5, else 0; accuracy = the mean over the items with both orders under both wordings. Unit: the item.
  - **C1:** the second wording's accuracy has an item-bootstrap lower bound above 0.634.
  - **C2:** |accuracy(second) − accuracy(first)| ≤ 0.05 on the same items (point estimate of the paired mean difference; its interval reported).
- **Why "ss-b10c's figures" are read on all 200 items.** ss-b10c's headline figures (Haiku 77.5%, Sonnet 89.7%) are on its scored subsets (100 and 126 items, the ones ss-b10 had rated once); its all-200 rows are 76.2% and 88.2%. This bet runs all 200, so C2 compares the two wordings on the same 200 items, item by item (D7, P8). The subsets are reported rows.
- **Uncertainty:** percentile item bootstrap, 10,000 resamples, `default_rng(20261104)`, bounds at int(0.025n) and int(0.975n) − 1; section-cluster bootstrap reported (P14). Tolerance EPS = 1e-12 (P13).
- **Split:** none. Nothing is fitted.
- **Power of the 5-point window and D11 (P2, P12, P15), committed** (`scoring/dry_b16_b17.py`, 06b990c; 2,000 runs per world, from ss-b10c's measured per-item scores): in the valence-only null world (the model answers the same valence question whatever the sentence; rating noise set pessimistically to half the per-item discordance between ss-b10c's flattery and forecasting prompts, Haiku 0.305, Sonnet 0.105, balanced so expected accuracy is unchanged), P(C2) is 0.95 on Haiku and 1.00 on Sonnet, and P(pass) 0.95; if the second wording behaves item by item like the forecasting prompt, P(pass) 0.15; if it costs 5 points, 1.00; 8, 10 or 15 points, 0.00. So the window can see a shift of 8 points or more, and the bet can pass and fail. Every verdict of `scoring/score_b17.py` is reached on synthetic rows (`--rules`).
- **Secondary statistics** (reported, never the verdict): the paired difference's interval; the share of items with the same pick under both wordings; accuracy with the original first and second, the Option-1 pull, and right both / first only / second only, per wording; accuracy on ss-b10c's scored subsets against 77.5% and 89.7%; by section.
- **Multiple comparisons:** one conjunction (2 models × 2 conditions), no correction.
- **Robustness checks committed now** (P10, P14): leave-one-item-out and leave-one-section-out on each model's label; a flip is reported in a sentence and does not change the verdict.

## 5. Pre-registered reading

Sentences generated by `scoring/score_b17.py` (`sentences`), verbatim; <…> filled from the table.

1. **Pass:** both models meet both conditions; **pass, unreplicated**. *"On BrainBench's 200 abstract pairs, each shown in both orders with the two ratings averaged, the flattery question in a second wording (fixed before any call: which version's findings make the authors' own idea look better supported) picked the published abstract more often than the 171 neuroscientists did (63.4%) on both models, and within 5 points of the first wording on each: Haiku a% [lo, hi], against x% with the first wording (difference d points, [lo, hi]); Sonnet …. So the shortcut did not depend on the one sentence ss-b10c used; this design still cannot tell valence from plausibility or memory of the papers."*
2. **Mixed:** exactly one model meets both. *"… held on <model> (…) but not on <other> (…; its lower bound is not above 63.4% | it moved more than 5 points from the first wording), so on <other> ss-b10c's result depends on the sentence as well as the shortcut."*
3. **Fail:** neither meets both. *"… did not hold on either model (…): each either failed to clear the neuroscientists' 63.4% or moved more than 5 points from the first wording, so ss-b10c's result depends on its sentence."*
4. **Untestable:** either model has fewer than 180 items with both orders. *"Too few items were rated in both orders to test the second wording (<model>: n of 200 items with both orders; at least 180 needed)."*
5. **Reported in every case**, after the main sentence: per model the same-pick and position sentence; the ss-b10c-subset sentence; leave-one-out and section clauses; the closing sentence (*"Both wordings ask a model to judge which version is better for the paper's own idea; a pass shows the result is not tied to one sentence, not that the models answer by valence rather than plausibility or memory of the papers, which were public before these models were trained. Haiku and Sonnet ran with thinking off, as in ss-b10c."*).
6. **Scoring for the ledger:** outcome 1 if pass, 0 if mixed or fail; untestable not scored. One scored bet.

## 6. What it cannot do

- **Two sentences are not all sentences.** A pass shows the result survives one other wording, written by the same session; it does not show it survives every fair wording.
- **Valence, plausibility and memory** are not separated by changing the sentence.
- **C2 is a point estimate**, not an equivalence test; its interval is reported.
- **Time.** The first wording's calls ran earlier today (ss-b10 and ss-b10c); the model versions are the same ids.
- **Two models, one benchmark, one family.** No "LLMs", "every model" or "all" sentence will appear.

## 7. Stop rules

- Caps in code: $2.25 for this bet, $21.40 for the program. If reached, later calls are reported as not run.
- Stop on any refusal: no rewording, no retry, `results/refusal.md` written. Stop on any error or truncation. The ratings so far are written to `bettor/bbv2-ratings.jsonl` on every exit path.
- The script refuses to run if `flattery-v2.txt` does not match its frozen hash.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "ss-b17", "program": "settled-science", "direction": "ss-f10", "map": "map/settled-science.json",
 "title": "ss-b10c's flattery question in a second wording, Haiku and Sonnet, all 200 BrainBench items in both orders", "source": "engine",
 "odds_event": "With a second flattery wording frozen by SHA-256 before any call, on BrainBench's 200 items in both orders with ratings averaged, for both claude-haiku-5-5 and claude-sonnet-5-5 the accuracy has a 95% item-bootstrap lower bound above 0.634 and lies within 0.05 of the same model's accuracy with ss-b10c's wording on the same 200 items.",
 "engine_odds": 0.37, "engine_odds_first": 0.37, "human_odds": null, "prereg_commit": "<this commit>", "budget_usd": 2.25, "referee": "model",
 "bet_type": "standard", "seed_source": "fixed", "replication_of": "ss-b10c", "lesson": "ls-ss-b17", "premortem_kind": "world", "verdict": "open"}
```

## 9. Checklist before the first call

- [x] This file is committed on its own; no call has been made.
- [x] §0's prior work row states predicted outcomes with citations and what this bet adds.
- [x] The lesson row is filled after reading ledger/bets.jsonl, brier.md (44 scored, Brier 0.160, 11/44), audits/ (newest sv-b6.md, 8fa642a; and ss-b10c.md) and lessons.jsonl; the same sentence goes to `ledger/lessons.jsonl` as `ls-ss-b17`.
- [ ] A fresh design review has returned go, or fix-first confirmed.
- [x] The card (`6ee9bb7`) was committed before this file; main was merged and `ledger/human-odds.jsonl` read immediately before this commit.
- [x] Engine odds on record earlier (map node ss-f10, 13b4645).
- [x] One scale direction in every prompt.
- [x] No draw, so no beacon seed (`seed_source: fixed`).
- [x] Budget, the wording's hash check and stop-on-refusal enforced in code.
- [x] DEVIATIONS.md D81.
- [x] The committed dry run shows P(pass) and P(fail) each at least 10% under named worlds (D11), and the window's power (P2).

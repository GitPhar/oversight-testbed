# ss-b16 (direction ss-f9): Opus's flattery rule on all 200 BrainBench items, both option orders (pre-registration)

Written and frozen 2026-11-05 16:30 America/Denver, in its own commit, before any new call. DEVIATIONS.md D80. Budget **$5.95**, enforced in code (`bettor/brainbench_opus.py` `BET_CAP`; budget ruling br-020 on Sean's budget steer; program cap $21.40, D79). Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This direction's card went on the cockpit first (`6ee9bb7`, no engine odds), before its map node (`458613a`) and this file. Main was merged into this branch and `python3 ledger/human_odds_match.py settled-science ss-f9` was run immediately before this commit: "no human odds".

> **One run, one scored bet** (rule 15). This bet is a new run: 638 new Opus calls on 159 items no model call has rated with Opus, plus ss-b10c's 162 Opus calls on 41 items, which were a reported secondary of ss-b10c and never scored. It is not `secondary_of` ss-b10c: ss-b10c was scored on Haiku and Sonnet's ratings, and this bet's decisive data are Opus's. Haiku's and Sonnet's all-200 rows from ss-b10c are reported here and never re-scored.

## 0. The bet

| field | value |
|---|---|
| bet id | `ss-b16` |
| referee | `model`: a language model's ratings, scored against BrainBench's published labels (which abstract is the original), as ss-b10c |
| bet type | `standard` |
| direction | `ss-f9` (map/settled-science.json; programs/settled-science/map/settled-science.md, "Wave 5") |
| source | `engine` (the replication invariant 7 owes ss-b10c; paper/novelty.md re-ranked item 1; design from the planning chat's launch message, funded by Sean's budget steer) |
| prior work | BrainBench (Luo et al. 2024, *Nature Human Behaviour*, arXiv 2403.03230, v4 HTML re-read 2026-11-05): LLMs averaged 81.4% against 63.4% for experts, "scored as choosing the abstract with the lower perplexity"; "Chat or instruction-optimized models performed worse than their base model counterparts"; the authors avoided prompting because "Prompting in natural language may yield less reliable judgments"; the best single model in the text, Phi-3, scored 82.5%. They test no valence, flattery or option-order shortcut. No paper reports a prompted Claude model, or a valence question, on BrainBench (web search "BrainBench Claude Opus prompted accuracy neuroscience results prediction frontier models", 2026-11-05: none). Predicts: unknown. **What this bet adds:** ss-b10c's 41-item Opus secondary completed to all 200 items, read against the stricter published LLM figure (81.4%) rather than the experts', with the forecasting prompt on the same items as the matched comparison. |
| engine odds, P(pass) | **50**, from a fresh v2 context handed `ledger/prior.md` (961d6ec) and this bet's description with the committed dry run (`scoring/dry_b16_b17.py`, 06b990c): prior 0.25, adjustment +0.25, reason "Settled-science row 0.50 (3/6); dry run puts pass between the Sonnet-like world (0.38) and the Opus-41 world (1.00); C2 is fragile, and the 40/41 likely overstates the other 159." Recorded on the map node ss-f9 at 13b4645, before this commit. These are the first odds stated for this direction. |
| human odds, P(pass) | no human odds (`ledger/human_odds_match.py settled-science ss-f9`, 2026-11-05 16:30, immediately before this commit; card 6ee9bb7 posted this afternoon and not yet on the live cockpit) |
| models | `claude-opus-5-5` only, not all three (rule 12): this bet completes ss-b10c's Opus secondary, and Haiku and Sonnet already have every item in both orders under both prompts from ss-b10c (`bettor/bbb-ratings.jsonl`); their rows are reported on the same items with no new call. |
| budget | $5.95 API, Opus only: 638 new calls at ss-b10c's measured $0.0091 a call, about $5.81. 0 QPU s, 0 laptop hours. |
| lesson | "Correcting P12, P3: ss-b10c's Opus row was 41 now-published items, against a bar a Haiku-level model clears. This bet reads Opus on all 200 against the stricter 81.4%, with the forecasting prompt matched, the 159 new items reported alone and a committed dry run, and its odds are 50% (the first stated) because that dry run spans 0.38 to 1.00." |
| design review | before the first call, a fresh auditor dry-runs this design (operators/design-review.md) → `ledger/design-reviews/ss-b16.md`. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that the forecasting prompt beats the flattery prompt by more than 5 points on the 159 new items, as it did by 4 on Sonnet, while C1 holds." Kind: `world`. |
| auditor | fresh session per operators/auditor.md, after results |

## 1. In plain English

BrainBench (Luo et al., 2024) shows a real neuroscience abstract beside a copy an expert rewrote so the results come out differently. Open language models, scored by which version they found less surprising, picked the real one 81.4% of the time; 171 neuroscientists 63.4%.

ss-b10c asked Claude models a question that needs no knowledge of results: which version is better news for the paper's own idea? With every pair shown both ways round and the two answers averaged, Sonnet picked the real abstract 89.7% of the time and Haiku 77.5%, both above the neuroscientists. Opus picked it 97.6% of the time, but only on 41 pairs, because its budget ran out.

This bet asks Opus the same two questions, the "better news" one and the program's direct "which was published?" one, on all 200 pairs, both ways round. **A hit means two things: Opus's "better news" answer clearly beats the 81.4% the study published for language models (its lower bound is above it), and asking directly which version is real does no more than 5 points better.** That would say the valence question alone does, on the strongest Claude model, what the benchmark was read as measuring. The rival explanations are memory (BrainBench and its abstracts were public before Opus was trained) and plausibility (picking the version that fits prior biology), which this design cannot separate from valence. Prior work makes no prediction: nobody has put a valence question, or a prompted Claude model, to BrainBench.

## 2. Material

- **Model and settings.** `claude-opus-5-5`, adaptive thinking at effort low (it cannot turn thinking off, D18), max_tokens 4000, structured output `{rationale, p_option_1}`, no tools field (`bettor/brainbench.py` `fn`, unchanged).
- **Prompts.** `brainbench.FLATTERY` and `brainbench.BETTOR` with their user texts, unchanged (`brainbench.job`), so each of ss-b10c's 162 Opus calls has the same content-hash key and is read from `bettor/bbb-opus-cache.json` (read only, never written).
- **Items.** BrainBench's 200 human-written items, `items/brainbench/items.jsonl` (SHA-256 `0a9acfeb…`, frozen at `e97fe46`). All 200, no filter.
- **Orders.** Every item and prompt in both orders: the original as Option 1 (`orig-first`) and as Option 2 (`orig-second`). No order draw.
- **Item order of the run.** ss-b10c's beacon order (`bettor/bbc-seed.json`, sub-seed `opus-order` 15330705831137599518, CURBy-RNG pulse 1592522), item by item, four calls each, as `brainbench_b.plan()` builds it; the first 41 items are ss-b10c's. **Seed:** no new draw, so no new beacon pulse: the run order is ss-b10c's, already public, and it matters only if the cap stops the run (`seed_source: carried`, from ss-b10c's seed commit a764438).
- **New calls** go to `bettor/bbo-cache.json` (in `common.CACHES`). `bettor/bbo-ratings.jsonl` holds every Opus rating used, each tagged `source: ss-b10c archive | ss-b16`.
- **Reported comparators.** Haiku's and Sonnet's flattery ratings on all 200 items in both orders, from `bettor/bbb-ratings.jsonl` (ss-b10c), read only.
- **Published comparators.** 0.814 (LLMs, perplexity) and 0.634 (experts), Luo et al. as above.
- **Scale.** One direction in both prompts: 1 = Option 2, 99 = Option 1, 50 = cannot tell or no difference.

## 3. Calls

| step | what | new calls | est. cost |
|---|---|---|---|
| 1 | Opus, flattery and forecasting, both orders, the 159 items ss-b10c did not reach (and the 2 forecasting calls missing on its 41st item) | 638 | about $5.81 |

- One step, 4 workers (at most 4 calls, about $0.05, in flight past the cap check; `common.Caller` stops at cap − $0.05). If the cap stops the run, the items not reached are reported as not run; the untestable rule below decides whether the verdict can be read. The ending is recorded in `bettor/bbo-run-status.json`.
- Every call is cached by content hash, so a crash never pays twice.

## 4. Statistics

- **Primary statistic** (ss-b10c's rule, `scoring/score_bbb.acc_block`): per item and prompt, p_avg = the mean of the two calls' probabilities on the original (each p_option_1 clipped to 1–99, divided by 100, or 1 minus that when the original is Option 2). The item scores 1 if p_avg > 0.5, 0.5 if p_avg = 0.5, 0 otherwise. Accuracy = the mean over items. Unit: the item.
  - **C1:** Opus's flattery accuracy on its items with both flattery orders; the bar is its item-bootstrap lower bound above 0.814.
  - **C2:** on the items with all four Opus calls, d = mean(forecasting item score − flattery item score); the bar is d ≤ 0.05 (point estimate). Its item-bootstrap interval is reported.
- **Uncertainty:** percentile item bootstrap, 10,000 resamples, `default_rng(20261104)`, bounds at int(0.025n) and int(0.975n) − 1. A bootstrap over the five *Journal of Neuroscience* sections (P14) is reported beside C1, with a sentence if it disagrees. Tolerance EPS = 1e-12 on every threshold (P13).
- **Split:** none. Nothing is fitted.
- **D11 dry run, committed** (`scoring/dry_b16_b17.py`, 06b990c; P12, P15). The 41 items ss-b10c rated are fixed as archived (40 right on flattery); the other 159 are simulated, 2,000 runs per world: new items like Opus's own 41: P(pass) 1.00; like Sonnet on the same items: P(C1) 0.93, P(C2) 0.38, P(pass) 0.38; like Haiku: P(pass) 0.01; the valence-only null world (Opus knows only which version is better news, so both prompts give the same pick, right with probability v on each new item): v = 0.80, 0.85, 0.88, 0.90, 0.95 give P(pass) 0.15, 0.73, 0.96, 0.99, 1.00. So the bet can pass and can fail under the worlds the design names. Every verdict of `scoring/score_b16.py` is reached on synthetic rows (`dry_b16_b17.py --rules`).
- **What the 41 known items do (P12).** They are 20% of the 200 and were 40 of 41 right; they are in the rule because the launch asked for "all 200 items". The 159 new items alone are reported as a row with their own interval and whether its lower bound clears 0.814, so a reader can see whether the published 41 carry the pass.
- **Secondary statistics** (reported, never the verdict): Opus's accuracy with the original first and second, the Option-1 pull, and counts right in both orders, first only, second only, per prompt; the vote count (right in both orders 1, split 0.5, wrong in both 0; Zheng et al. 2023, the ss-b10c auditor's re-analysis); Opus's flattery accuracy against the experts' 0.634; Haiku's and Sonnet's ss-b10c flattery accuracy on the same items; the archive split (41 known against 159 new); by section.
- **Multiple comparisons:** one conjunction (C1 and C2), no correction.
- **Robustness checks committed now** (P10, P14): leave-one-item-out and leave-one-section-out on C1; a flip is reported in a sentence and does not change the verdict.

## 5. Pre-registered reading

Sentences generated by `scoring/score_b16.py` (`sentences`), verbatim; <…> are filled from the table.

1. **Pass:** C1 and C2 both hold; **pass, unreplicated**. *"On <n> of BrainBench's 200 abstract pairs, each shown in both orders with the two ratings averaged, Opus, asked only which version is better news for the paper's own idea, picked the published abstract a% [lo, hi] of the time, above the 81.4% the original study published for language models scored by perplexity; asked directly which version was published (the program's forecasting prompt), it was right b% [lo, hi] on the m items where both prompts ran, d points more|less than with the flattery question (difference [lo, hi]), within the 5 points the rule allowed. So on Opus too, the 'better news' question alone does about as well as asking which version is real; this design cannot tell whether Opus answered by valence, by plausibility or from memory of the papers, and it does not show that the models in the original study used such a rule."*
2. **Mixed, C1 only:** *"…, above the published 81.4% for language models; but asked directly which version was published …, more than the 5 points the rule allowed, so on Opus the forecasting prompt does clearly better than the 'better news' question alone."*
3. **Mixed, C2 only:** *"…, not shown to beat the published 81.4% for language models (the rule needed the lower bound above it), although asked directly … within the 5 points the rule allowed."*
4. **Fail:** neither. *"…, not shown to beat the published 81.4% for language models, and …, more than the 5 points the rule allowed; so on Opus the 'better news' question alone neither beats the published figure nor keeps up with asking which version is real."*
5. **Untestable:** fewer than 180 items with both flattery orders, or fewer than 180 with all four calls. *"Too few items were rated to test it (Opus: n of 200 with both flattery orders, m with all four calls; at least 180 needed)."*
6. **Reported in every case**, in this order after the main sentence: the 0.634 sentence; the archive-split rows (*"On the 41 items whose ratings were already published in ss-b10c | rated for the first time here, Opus's flattery accuracy was x% [lo, hi], whose lower bound is above | not above 81.4% (a reported row)."*); the vote-count sentence; Haiku's and Sonnet's same-item sentences; leave-one-out and section clauses; the memory and settings sentence (*"BrainBench and its source abstracts (Journal of Neuroscience, 2023) were public before Opus's training data were collected, so either prompt may draw on memory of the benchmark or of the papers; Opus ran at its least-thinking setting (it cannot turn thinking off) and was asked for a rating, not scored by perplexity as the original study's models were. Opus's 162 calls from ss-b10c were reused, not asked again."*).
7. **Scoring for the ledger:** outcome 1 if pass, 0 if mixed or fail; untestable not scored. One scored bet. ss-b10c keeps its verdict.

## 6. What it cannot do

- **Memory and plausibility.** Nothing here separates a valence judgment from recognising the paper or from prior biological plausibility. A pass says the valence question does as well as asking which is real; it does not say Opus answered by valence.
- **The comparison with 81.4% is not matched.** The published figure is for other, older models scored by perplexity; ours is a prompted rating. It is a reference bar, not a head-to-head.
- **C2 is a point estimate.** A difference of 5 points or less does not show the prompts equivalent; its interval is reported.
- **41 items known before data** (see §4).
- **One model, one benchmark, one wording of each prompt** (ss-b17 tests a second flattery wording on Haiku and Sonnet). No "LLMs", "every model" or "all" sentence will appear.

## 7. Stop rules

- Caps in code: $5.95 for this bet, $21.40 for the program. If reached, the items not reached are reported as not run.
- Stop on any refusal: no rewording, no retry, `results/refusal.md` written. Stop on any error or truncation. The ratings so far are written to `bettor/bbo-ratings.jsonl` on every exit path. ss-b10c's caches are never written.

## 8. Ledger entry (filled now, completed after audit)

```json
{"id": "ss-b16", "program": "settled-science", "direction": "ss-f9", "map": "map/settled-science.json",
 "title": "Opus's flattery rule on all 200 BrainBench items in both orders, against the published 81.4% for LLMs and the forecasting prompt", "source": "engine",
 "odds_event": "On BrainBench's 200 human-written items, each rated in both option orders and the two ratings averaged, claude-opus-5-5's flattery accuracy has a 95% item-bootstrap lower bound above 0.814 (the published LLM mean), and its forecasting-prompt accuracy on the same items exceeds its flattery accuracy by at most 0.05.",
 "engine_odds": 0.50, "engine_odds_first": 0.50, "human_odds": null, "prereg_commit": "<this commit>", "budget_usd": 5.95, "referee": "model",
 "bet_type": "standard", "seed_source": "carried", "replication_of": "ss-b10c", "lesson": "ls-ss-b16", "premortem_kind": "world", "verdict": "open"}
```

## 9. Checklist before the first call

- [x] This file is committed on its own; no new call has been made.
- [x] §0's prior work row states what the published work did and did not test, the search, and what this bet adds.
- [x] The lesson row is filled after reading ledger/bets.jsonl, brier.md (44 scored, Brier 0.160, 11/44), audits/ (newest sv-b6.md, 8fa642a; and ss-b10c.md) and lessons.jsonl; the same sentence goes to `ledger/lessons.jsonl` as `ls-ss-b16`.
- [ ] A fresh design review has returned go, or fix-first confirmed.
- [x] The card (`6ee9bb7`) was committed before this file; main was merged and `ledger/human-odds.jsonl` read immediately before this commit.
- [x] Engine odds on record earlier (map node ss-f9, 13b4645).
- [x] One scale direction in every prompt.
- [x] No new draw (`seed_source: carried`; §2).
- [x] Budget and stop-on-refusal enforced in code.
- [x] DEVIATIONS.md D80.
- [x] The committed dry run shows P(pass) and P(fail) each at least 10% under named worlds (D11).

# gm2bf1-f1: with fresh question-order conversations, do claims that move with order still move with format, under both noise guards? (pre-registration)

Written and frozen 2026-11-05 (America/Denver; the commit's author time is the record, no clock time is typed here), in its own commit, before any call. DEVIATIONS.md D83. Budget **$1.00**, enforced in code. Stop on any refusal: the message ID goes to `results/refusal-gm2bf1f1.md`, and nothing is reworded or retried.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision. His odds come only from `ledger/human-odds.jsonl`. The direction's cockpit card was posted at 09:58 (`9da5349`, no engine odds) and was live on the site from the push at about 10:00, for the whole of this session before this commit (the wave's rule for this job). `python3 ledger/pickup_human_odds.py` then `python3 ledger/human_odds_match.py entangled-mind gm2bf1-f1`, run immediately before this commit: "no human odds".

## 0. The bet

| field | value |
|---|---|
| bet id | `em-gm2bf1f1` |
| referee | `model` |
| bet type | `standard` |
| direction | `gm2bf1-f1` (map/entangled-mind.json), a follow-up of `gm2b-f1` (bet `em-gm2bf1`) |
| source | `literature` (the em-gm2bf1 audit's "What would break it next") |
| engine odds, P(pass) | map: 15, stated 2026-11-05T07:40 (one pass by the em-gm2bf1 betting session, not v2). Fresh v2 context at this design: **8** (prior 0.23, adjustment −0.15, reason: "Literature 1/14, under-$1 2/15, model 4/24 rows; dry run passes 0% if fresh data resembles parent, whose link noise explained; five-conjunct rule needs effect absent so far."; `ledger/prior.md` at `69fb813`). Both kept. |
| human odds, P(pass) | no human odds (no line for gm2bf1-f1 in `ledger/human-odds.jsonl` at this commit; card live since about 10:00) |
| models | `claude-haiku-5-5` (primary: the only model with six-format data on all 40 items, gm3b), `claude-sonnet-5-5` (reported: fresh order chains on em-dm2's 20 items, 3 per order, against em-dm2's Sonnet formats) and `claude-opus-5-5` (reported, no new calls: em-gm2q2's fresh Opus turn-by-turn chains on gm2's 10 items, 6 per order, against em-dm2's Opus formats). Fewer items and repeats on Sonnet and Opus because the $1.00 cap holds (rule 12). |
| budget | $1.00 API in code (Batches API; planned Haiku about $0.21, Sonnet about $0.63, Opus $0) · 0 QPU s · no local model |
| prior work | No prior statement found on an item-level link between order sensitivity and format sensitivity (gm2b-f1's search: arXiv and WebSearch "question order effect format effect same items correlation LLM"). Zhu and Griffiths 2024 (arXiv:2401.16646; GPT-4, GPT-3.5, LLaMA-2) found judgment variance follows an inverted U in the mean, and Temkit 2026 (AMEL, arXiv:2605.22714) found order drag strongest on uncertain items: both predict mid-scale claims move more under either manipulation, which the two guards are built to remove. Predicts: unknown for the guarded link. Adds: a fresh order run, so the link cannot be one run's noise. |
| lesson | "Correcting P17 and P15: em-gm2bf1's design-review guard replaced the frozen one and passed where the frozen one failed, on one archived run. This bet requires both guards and both item groups on fresh conversations, builds its dry run by resampling the archived conversations, and its odds are 8% (from 15% on the map) because a fresh run like the parent's passes 0%." |
| design review | before the first call, a fresh subagent dry-runs this design → `ledger/design-reviews/em-gm2bf1f1.md`. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that on fresh conversations the frozen guard's partial correlation again reaches zero, because rating noise carries the order-format link." Kind: `world`. |
| auditor | fresh subagent per operators/auditor.md, in a planter-built clone, after results |

## 1. In plain English

em-gm2bf1 found, on Haiku, that the statements whose rating moved most with question order were partly the same ones whose rank moved most across answer formats. But the link was fragile: it held under the noise allowance the design review wrote and failed under the one first frozen, it sat in 30 of the 40 topics, and it rested on one set of order conversations recorded the day before. This bet records the order conversations again from scratch, on all 40 topics, and asks for the link under both allowances and in both groups of topics. Sonnet and Opus are reported on fewer topics. If the link survives, it is not one run's noise. If it does not, em-gm2bf1's pass was most likely that run's noise. Nothing in print predicts the guarded link.

## 2. Material

- **Items and claims:** experiment 5's 40 items and their four chain claims each (160 claims; `experiments/split-exp5.json`, the same claims as `gm2b-planted-values.json`, asserted in code). Groups: gm2's 10 items, gm2b's 30.
- **Order conversations (new):** gm2's turn-by-turn shown chain (`gm2q_questions_only.chain_turns`, unchanged), orders O1–O4. Haiku: all 40 items, 10 per order (1,600 conversations). Sonnet: em-dm2's 20 items (`split-exp5.json` candidates 0–9 and 20–29), 3 per order (240). Opus: no new calls; em-gm2q2's fresh shown chains on gm2's 10 items (`results/gm2q2-conversations.json`, keys `opus|<item>|<order>|shown|<r>`, 6 per order). That archive was opened before this commit only for em-gm2q2's own analysis (final ratings and statement means); no order span was computed from it and no format spread was read with it.
- **Settings:** Haiku thinking disabled, max_tokens 200 (gm2's); Sonnet thinking between_tools, max_tokens 1000 (em-dm4's); structured output `{"rating": integer}`. Batches API.
- **Format data (archived):** Haiku `results/gm3b-calls.json` (160 claims); Sonnet `results/mm-gm3b-sonnet-calls.json` (80 claims); Opus `results/mm-gm3b-opus-calls.json` (the 40 claims of gm2's 10 items). Decoded with em-gm3b's `encode`, `observed_scale` and `claim_means`, unchanged.
- **Measures** (em-gm2bf1's, imported unchanged): per claim, order span S, within-order SD W, the order archive's extremity Eo, format spread G (SD over the six formats of the claim's percentile rank among the arm's claims) and extremity E.
- **Seed** (operators/hardware.md): CURBY-Q's latest completed round is 28297 (checked 11:15 with `DIRNGClient.latest()`; result pulse 2025-08-22 13:42 America/Denver), far over 24 h old, so the chain is stalled. Seed: the first CURBy-RNG pulse timestamped after this commit. seed = the first 8 bytes of SHA-256(randomness ‖ "em-gm2bf1f1" ‖ ":<purpose>"), unsigned big-endian (`ledger/seed.py --purpose bootstrap`). *Filled in by the seed commit, before any data:* `chain:` CURBy-RNG · `pulse_index:` 1592560 · `pulse_time:` 2026-11-05 11:16:00 America/Denver (2026-11-05T18:16:00.198Z; previous pulse 1592559 at 18:15:00.209Z, before this file's commit df30f78 at 11:15:51) · `randomness:` 49c98441ef264a6a86c73e7d73f8e04589035850ed2f3c32a2e286c3154970786d193b3783a20e5737a26a8f299bf197fb8a9b8c556069b61dd0b99bb75ddf76 · `client:` @buff-beacon-project/curby-client@1.2.0 (Client.randomness(1592560), `experiments/curby_seed.mjs rng`) · `certificate_verified:` false (classical chain) · `seed:` bootstrap 10269032153479545163 (used mod 2^63 by the bootstrap) The arms use seed, seed + 1, seed + 2; nothing in the run is random beyond the models' sampling.

## 3. Calls and cap

Five rounds of batches (one per chain turn), Haiku and Sonnet together. Before the first, the whole estimate plus $0.05 must fit $1.00; before every round, the next batch × 1.10 and everything remaining, each plus $0.05, must fit, or the run stops and unfinished chains count as missing. Cached by key in `results/gm2bf1f1-conversations.json`.

## 4. Statistics

Per arm, on claims with complete measures: ρ = Spearman(S, G); the **frozen guard**, em-gm2bf1's guard as first pre-registered (partial Spearman of S and G given the plain ranks of E and W); the **D71 guard** (partial Spearman given E, Eo and W, each as centred rank and squared centred rank); 10,000-resample item-cluster bootstrap (items carry their claims; P14); ρ within each item group. Leave-one-item-out: a flip is reported with the item named (em-gm2bf1's D71 F2 rule). Secondaries: ρ(S, W), ρ(G, W), median span.

## 5. Pre-registered reading

On Haiku (the rule is read on Haiku only; Sonnet and Opus are reported with the same label and never change the verdict):
1. **Untestable:** fewer than 120 claims with complete measures.
2. **Pass:** ρ ≥ 0.30 with its 95% lower bound > 0, the frozen guard's lower bound > 0, the D71 guard's lower bound > 0, and ρ > 0 in gm2's 10 items and in gm2b's 30 (tolerance 1e-9 everywhere). Reported as **pass, unreplicated**; if one item's removal flips it, "pass, carried by item <id>".
3. **Fail:** testable and not a pass.

Verdict sentences, verbatim:
- **pass:** "On fresh Haiku order conversations, the claims whose rating moved more with question order tended also to be the ones whose rank moved more across answer formats (Spearman ρ = <x>), under both allowances for how extreme and how noisy each claim's ratings were, and in both groups of topics. The link in em-gm2bf1 was not that run's noise."
- **fail:** "On fresh Haiku order conversations, the claims that moved most with question order were not shown to be the ones that moved most across answer formats once both allowances for extremity and rating noise were made, in both groups of topics. em-gm2bf1's pass did not repeat on a fresh run."
- **untestable:** "Too few claims had complete order and format data to read the rule."

Scored outcome 1 for pass, 0 for fail.

## 6. What it cannot do

- **Differences from em-gm2bf1 (P8):** fresh order conversations on a later day; the Batches API; a pass needs both guards and both groups (em-gm2bf1 needed the D71 guard only). The format data are the same archive, so a pass shows the order side repeats, not the format side.
- A shared cause not measured (a claim's ambiguity of wording) would give the same pattern; the guards cannot remove it.
- Haiku only for the verdict; Sonnet on 80 claims at 3 repeats and Opus on 40 at 6 have wide intervals.

## 7. Stop rules

Cap $1.00 in code (§3). Stop on any refusal: no further batch; nothing reworded or retried; no later run while `results/refusal-gm2bf1f1.md` exists. A batch still failing after two unchanged resubmissions stops the run.

## 8. Dry run (committed with this file)

`python experiments/gm2bf1f1_fresh_order.py --dry-run` (100 runs per world, 400 bootstraps): fresh Haiku chains drawn by resampling em-gm2bf1's archived conversations within each item × order cell (P15), against gm3b's archived format spreads:

| world | P(pass) |
|---|---|
| archive: the fresh run looks like em-gm2bf1's | 0.00 |
| no link: format spread shuffled across claims within item | 0.00 |
| link, c = 3: each claim's span carries 3 extra points per SD of its format spread | 0.93 |
| link, c = 6 | 1.00 |
| link, c = 10 | 1.00 |

The bet can pass and fail (D11). A world like em-gm2bf1's own archive fails (its frozen guard and its gm2 group fail there), so a pass needs a link beyond that run's size: about 3 points of order span per SD of format spread (median span 15 points) passes 93%.

## 9. Ledger entry

Through `ledger/inbox/p1-wave3.jsonl`; budget ruling in `ledger/spend.jsonl`. Its Opus arm reads em-gm2q2's run; the primary (Haiku) is new data, so the bet is not secondary under rule 15.

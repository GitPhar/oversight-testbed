# gm2b-f1: do the claims that move most with question order also move most with answer format? (pre-registration)

Written and frozen 2026-11-05 (America/Denver; the commit's author time is the record), in its own commit, before the archives are opened for this analysis. DEVIATIONS.md D65. Budget **$0** (archive only; no API call, no QPU second, no local model).

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). His odds come only from `ledger/human-odds.jsonl`. This direction has no line there (`python3 ledger/human_odds_match.py entangled-mind gm2b-f1`, run 06:41, after his 06:11 save reached the ledger at 9a75cc2: "no human odds"), so the bet proceeds marked "no human odds".

## 0. The bet

| field | value |
|---|---|
| bet id | `em-gm2bf1` |
| referee | `model` (archived model behaviour decides the outcome) |
| bet type | `standard` |
| direction | `gm2b-f1` (map/entangled-mind.json), a follow-up of `gm2b`, bet `em-gm2b` |
| source | `engine` (remap 2026-11-05, `9773f6a`) |
| engine odds, P(pass) | map: 40, stated 2026-11-05T04:45 (remap one pass, not v1). Re-elicited under v1 at about 06:37 (fresh subagent, the direction's row and the draft rule only): 24. After the lesson: **25** |
| human odds, P(pass) | no human odds (no line for gm2b-f1 in `ledger/human-odds.jsonl` at this commit) |
| models | not all three, because no model is in the loop: both archives (gm2/gm2b order chains, gm3b six formats) exist only for `claude-haiku-5-5`. Sonnet's and Opus's order chains (em-dm4) and formats (em-dm2) cover different item subsets and too few repeats for a per-claim span; not attempted. |
| budget | $0 API · 0 QPU s · under 10 laptop minutes |
| lesson | Correcting P3 and P8: the remap's correlation could pass because both spreads grow for mid-scale, noisy claims, a dumb shared driver. This bet adds a guard: the partial correlation given each claim's extremity and rating noise must also exclude 0, with item-cluster intervals, and its odds are 25% (map 40%, v1 24%) because extremity likely explains most of it. |
| design review | before the archives are opened, a fresh subagent dry-runs this design (operators/design-review.md) → `ledger/design-reviews/em-gm2bf1.md`. Nothing runs before a go. |
| pre-mortem | If this fails, the most likely reason is that once extremity and rating noise are allowed for, order span and format spread share nothing, because both only track how unsure Haiku is about the claim. Kind: `world`. |
| auditor | fresh subagent per operators/auditor.md, in a planter-built clone, after results |

Odds reasoning: running base rate 9/29 = 0.31 (`ledger/brier.md` at `08331f8`: 27 scored, Brier 0.209). The raw correlation is likely positive through the shared mid-scale driver, as the v1 elicitor and the map both say. The guard asks for something beyond that driver, a claim-specific instability that order and format share. Nothing in the record measures that. 25 sits just under the base rate.

## 1. In plain English

Program 1 found two ways a model's answer about a claim moves that it shouldn't: with the order the questions come in (gm2/gm2b), and with the format the question is asked in (gm3b). If the same claims are the wobbly ones in both, the two effects may be one property of the claim: the model holds no stable answer about it. We take Haiku's 160 claims, which appear in both archives. For each claim we measure how far its rating moves across the four question orders, and how far its standing among the 160 claims moves across six formats. Then we correlate the two. The obvious rival is boring: claims rated near the middle wobble more in both, and so do noisy ones. So the bet also needs the link to survive after allowing for how extreme each claim's rating is and how noisy its ratings are.

## 2. Material

- **Order archive:** `results/gm2-conversations.json` (10 items) and `results/gm2b-conversations.json` (30 items), Haiku. Keys `<item>|O1..O4|shown|<rep>`, 10 repeats per order. Each conversation rates the item's four chain claims (turns of kind "S", `claim` and `rating` 0–100) in a cyclic order, so each claim sits once in each position across O1–O4, followed by the main question (not used). Only the `shown` condition is primary. `redacted` is a reported secondary.
- **Format archive:** `results/gm3b-calls.json`, Haiku, keys `<item>|<claim>|<F1..F6>|<rep>`, 10 repeats. It is decoded with `gm3b_format_invariance.encode` and `gm3c_heldout_format.observed_scale` / `claim_means`, unchanged.
- **Claims:** `experiments/split-exp5.json` candidates × chain_claims (40 × 4 = 160), the same keys in both archives.
- **Before this commit,** the session had seen the key formats and one record of each archive, and the turn layout of one item (h111) in the four orders. That showed the claim ids, not the ratings' spread. No span, spread or correlation has been computed.
- **Measures per claim:**
  - order span S = max − min over O1–O4 of the claim's mean S rating (shown);
  - noise W = the pooled within-order SD of those ratings;
  - format spread G = the SD over the six formats of the claim's percentile rank among the 160 claims, from each format's per-claim mean (ranks remove each format's scale);
  - extremity E = |mean 0–100 rating (format F1) − 50|.
- **Seed** (operators/hardware.md): CURBY-Q's latest completed round is 28297 (2025-08-22 13:42 America/Denver; checked 06:24), so the chain is stalled. Seed: the first CURBy-RNG pulse timestamped after this commit; `ledger/seed.py <randomness> em-gm2bf1 --purpose bootstrap`. *Filled in by the seed commit, before any data:*
  `chain:` CURBy-RNG · `pulse_index:` 1592288 · `pulse_time:` 2026-11-05 06:44:00 America/Denver (2026-11-05T13:44:00.173Z; previous pulse 1592287 at 13:43:00.220Z, before this file's commit e65b1d5 at 06:43:25) · `randomness:` 7f692e8d4c65b62fbc2f53dcca11a1414f2b57f3e9ec0dcf8038adef440076f61dfdb8c21b1a7bd25bd3d7d7ecf369cff8f50e1476ba1d1a02cae7cb327d8757 · `client:` @buff-beacon-project/curby-client@1.2.0 (Client.randomness(1592288)) · `certificate_verified:` false (classical chain) · `seed:` bootstrap 12485997366771242721
- **Code:** `experiments/gm2bf1_order_vs_format.py`, committed with this file. `--selftest` runs three synthetic worlds (a shared instability beyond extremity → pass; both measures driven by extremity only → fail; unrelated → fail), plus boundary and measure checks. It never opens the archives, and it printed SELFTEST OK before this commit.
- **Scale:** one direction (0 = false, 100 = true) in every format.

## 3. Calls

None. One run: `python experiments/gm2bf1_order_vs_format.py --seed <bootstrap>` after the design review's go.

## 4. Statistics

- **Primary statistic:** Spearman ρ(S, G) over claims with complete data.
- **Guard:** the partial Spearman correlation of S and G given E and W (Pearson correlation of the ranks' residuals after least squares on the ranks of E and W).
- **Uncertainty:** 10,000 item-cluster bootstrap resamples (the 40 items carry their 4 claims each; P14), percentile 95% intervals; seed from the beacon (the redacted secondary uses seed + 1).
- **Secondary (reported, never promoted):** ρ of each measure with E and with W; the same two statistics with the order span from the `redacted` condition; median S and G.
- **Multiple comparisons:** one primary rule (a conjunction). Nothing secondary is read as a finding.
- **Robustness committed now:** leave-one-item-out (all four claims of one item dropped; bounds shifted by the point change). The items whose removal would flip the verdict are listed (P10).

## 5. Pre-registered reading

1. **Untestable:** fewer than 120 claims have complete order and format data.
2. **Pass:** ρ(S, G) ≥ 0.30, **and** the lower end of its 95% interval > 0, **and** the lower end of the partial ρ's 95% interval > 0 (every comparison with tolerance 1e-9). Reported as **pass, unreplicated** (one model, one claim set).
3. **Fail:** anything else.

Verdict sentences (P9), used verbatim:
- pass: "On Haiku's 160 deliberation claims, the claims whose rating moved most with question order were also the ones whose position moved most across answer formats, and this held after allowing for how extreme the claim's rating was and how noisy its ratings were."
- fail: "On Haiku's 160 deliberation claims, the claims that moved most with question order were not shown to be the ones that moved most across answer formats, by the pre-registered rule."
- untestable: "Too few claims had complete order and format data to read the rule."

**Reported in every case:** n claims and items, ρ and partial ρ with intervals, every secondary in §4, and the leave-one-item-out flips.

## 6. What it cannot do

- A pass would not show that one mechanism causes both effects. It shows that the same claims are unstable under both manipulations, beyond extremity and noise as measured here. A shared cause other than those two, such as how ambiguous the claim's wording is, is not excluded.
- The order span is a max-minus-min of four means, so it carries noise. W is controlled for, but not removed.
- One model (Haiku), these 160 claims. "Models" or "all claims" will not appear.

## 7. Stop rules

- No calls. The script records the three archive files' sha256 in its results.

## 8. Ledger entry (appended after the seed commit)

```json
{"id": "em-gm2bf1", "program": "entangled-mind", "map": "map/entangled-mind.json", "direction": "gm2b-f1", "parent_bet": "em-gm2b",
 "title": "Do claims that move with question order also move with answer format? (Haiku, archive)", "source": "engine",
 "engine_odds": 0.25, "engine_odds_first": 0.40, "engine_odds_v1": 0.24, "human_odds": null, "human_odds_note": "no human odds",
 "budget_usd": 0, "referee": "model", "bet_type": "standard", "seed_source": "curby-rng", "lesson": "ls-em-gm2bf1",
 "premortem_kind": "world", "verdict": "open"}
```

## 9. Checklist before the run

- [x] This file and its code are committed on their own; nothing has been run on the archives.
- [x] Lesson in §0, after reading bets.jsonl, brier.md (27 scored, 0.209, base rate 9/29), audits/ (newest ta-b1r2.md; em-gm2b.md, em-gm3b.md for the parents) and lessons.jsonl (P1–P15).
- [ ] Design review go.
- [x] Engine odds on record earlier (map 04:45; v1 about 06:37); human odds checked after Sean's 06:11 save: none.
- [x] §5 applies mechanically; the self-test applies it to synthetic worlds.
- [x] Pre-mortem: one sentence, a checkable mechanism, kind `world`.
- [x] Seed rule by the 24-hour rule; the seed commit follows.
- [x] DEVIATIONS.md D65.

# bm9-f2: does the pull toward the last rating have the human serial-dependence shape? (pre-registration)

Written and frozen 2026-11-05 (America/Denver; the commit's author time is the record), in its own commit, before the archive is opened for this analysis. DEVIATIONS.md D67. Budget **$0** (archive only; no API call, no QPU second, no local model).

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). His odds come only from `ledger/human-odds.jsonl`. This direction has no line there (`python3 ledger/human_odds_match.py entangled-mind bm9-f2`, run 06:52: "no human odds"), so the bet proceeds marked "no human odds".

## 0. The bet

| field | value |
|---|---|
| bet id | `em-bm9f2` |
| referee | `model` (archived model behaviour decides the outcome) |
| bet type | `standard` |
| direction | `bm9-f2` (map/entangled-mind.json), a follow-up of `bm9`, bet `em-bm9` (assimilation, β +0.27) |
| source | `engine` (remap 2026-11-05, `9773f6a`; the human serial-dependence literature in `paper/biomimetic-map.md` §3.2) |
| engine odds, P(pass) | map: 25, stated 2026-11-05T04:45 (remap one pass, not v1). Re-elicited under v1 at about 06:02 (fresh subagent, the direction's row and the draft rule only): 8. After the lesson: **8** |
| human odds, P(pass) | no human odds (no line for bm9-f2 in `ledger/human-odds.jsonl` at this commit) |
| models | not all three, because no model is in the loop: the single-scale QQ conversations (a sub-question S then the main question M, or M first) exist only for `claude-haiku-5-5` (exp5 run 1). bm9-f1, the Sonnet and Opus version, is parked as not free (em-dm4's conversations have a different structure). |
| budget | $0 API · 0 QPU s · under 10 laptop minutes |
| lesson | Correcting P5 and P12: an extra-parameter curve beats a line by construction, and a bounded scale makes any pull level off. This bet pits the DoG against an equally flexible levelling-off rival, requires its peak inside the observed gaps, has the review measure power on the real gaps, and its odds are 8% (map 25%, v1 8%) because levelling off is likelier. |
| design review | before the archive is opened, a fresh subagent dry-runs this design (operators/design-review.md) → `ledger/design-reviews/em-bm9f2.md`. It may run `--power <sigma> --L-from-archive` (gaps and content only, no outcome) to measure P(pass) in the DoG world at the real n and gap spread (P15). Nothing runs before a go. |
| pre-mortem | If this fails, the most likely reason is that 80 noisy pair means cannot tell a pull that turns down at large gaps from one that only levels off, so the DoG does not beat tanh by 2 AIC. Kind: `design`. |
| auditor | fresh subagent per operators/auditor.md, in a planter-built clone, after results |

Odds reasoning: running base rate 9/30 = 0.30 (`ledger/brier.md` at `ab7712e`: 28 scored, Brier 0.202). Three things pull this well below the base rate:
- a language model has no perceptual tuning curve;
- the bounded 0–100 scale predicts levelling off, not a reversal;
- telling a reversal from a plateau needs more than 80 pair means.

The v1 elicitor's 8 is kept. The bet stays open because, in the self-test's DoG world, the rule passes reliably, and in a levelling-off world it falsely passes about 7% of the time. The review checks P(pass) at the real gaps (D11).

## 1. In plain English

When Haiku rates a sub-question and then the main question, its main rating moves toward the number it just gave (em-bm9: about 0.27 points per point of gap). In people, this kind of pull toward the last thing seen has a characteristic shape. It is strongest when the last thing was moderately different and fades when it was very different, because a very different item is treated as unrelated. This bet asks whether Haiku's pull has that shape, or is just a straight line, or simply levels off at large gaps because ratings are stuck between 0 and 100. We fit the three curves to em-bm9's 80 archived pairs and compare them fairly. The human-shaped curve has to beat the line and also beat a levelling-off curve with the same number of parameters, and its peak has to fall inside the gaps we actually observed.

## 2. Material

- **Archive:** `results/exp5-conversations.json`, the QQ block, anchor (a) only: 40 items × 2 pairs, 20 conversations per order (SM, MS). Pairs are built by `bm_offline.bm9_pairs`, unchanged. Each pair gives d = mean M(SM) − mean M(MS), L = mean S(SM) − mean M(MS), and C = the claim's signed content push (lean × (S − 50)/50). `experiments/split-exp5.json` and `results/pool-run-3.json` (the claims' leans) are read through that function. Run 2's 20 pairs are not used (em-bm9 called them descriptive).
- **Before this commit,** the session had seen em-bm9's published table (`results/bm9-contrast.md`: 80 pairs, β +0.268 [+0.109, +0.427], γ +7.7) and the code of `bm9_pairs`. It had not opened `exp5-conversations.json` for this analysis.
- **Models:** see the code's docstring. w is profiled on a fixed log grid from 3 to 400 points. AIC = n·log(RSS/n) + 2(k + 1), with k = 3 for linear and 4 for DoG and tanh.
- **Seed** (operators/hardware.md): CURBY-Q's latest completed round is 28297 (2025-08-22 13:42 America/Denver; checked 06:44), so the chain is stalled. Seed: the first CURBy-RNG pulse timestamped after this commit; `ledger/seed.py <randomness> em-bm9f2 --purpose bootstrap`. *Filled in by the seed commit, before any data:*
  `chain:` CURBy-RNG · `pulse_index:` 1592298 · `pulse_time:` 2026-11-05 06:54:00 America/Denver (2026-11-05T13:54:00.183Z; previous pulse 1592297 at 13:53:00.166Z, before this file's commit cd534d9 at 06:53:49) · `randomness:` 3f35fe93e4e9d42d3470105621ac35c85bcb6248656091eb4ae4f07d00b26423580f405e2d6bbbc210b222c0c175153097ab8f7457be8ba65136b58fc83f49c6 · `client:` @buff-beacon-project/curby-client@1.2.0 (Client.randomness(1592298)) · `certificate_verified:` false (classical chain) · `seed:` bootstrap 965198064319072892
- **Code:** `experiments/bm9f2_dog_shape.py`, committed with this file. `--selftest` checks three synthetic worlds (DoG → pass, linear → fail, tanh → fail) and every boundary. It printed SELFTEST OK before this commit; at σ = 8 with uniform gaps, P(pass) was 1.00 in the DoG world, 0.00 linear and 0.07 tanh.
- **Scale:** one direction (0 = false, 100 = true).

## 3. Calls

None. One run: `python experiments/bm9f2_dog_shape.py --seed <bootstrap>` after the design review's go.

## 4. Statistics

- **Primary:** ΔAIC(DoG vs linear) = AIC_linear − AIC_DoG; ΔAIC(DoG vs tanh) = AIC_tanh − AIC_DoG; the DoG's peak |L| = w/√2 against the observed range of |L|; the sign of A.
- **Uncertainty (reported, not the bar):** 10,000 item-cluster bootstrap resamples (40 items carry their 2 pairs; P14) of both ΔAICs and of the pass share. Seed from the beacon.
- **Robustness:** leave-one-item-out. The items whose removal flips the verdict are listed (P10), and named in plain English if there are any.
- **Multiple comparisons:** one rule (a conjunction).

## 5. Pre-registered reading

1. **Untestable:** fewer than 60 usable pairs.
2. **Pass:** ΔAIC(DoG vs linear) ≥ 4, **and** ΔAIC(DoG vs tanh) ≥ 2, **and** the DoG peak w/√2 lies strictly inside the observed range of |L|, **and** A > 0 (assimilation). Every comparison uses tolerance 1e-9. Reported as **pass, unreplicated**.
3. **Fail:** anything else.

Verdict sentences (P9), used verbatim:
- pass: "On Haiku's 80 archived sub-question and main-question pairs, the pull of the main rating toward the sub-rating just given was best described by the human serial-dependence shape: it grew with the gap up to a peak inside the observed gaps and then shrank, beating both a straight-line pull and an equally flexible pull that only levels off."
- fail: "On Haiku's 80 archived pairs, the pull of the main rating toward the sub-rating just given was not shown to have the human serial-dependence shape, by the pre-registered rule; a straight-line or levelling-off pull describes it as well."
- untestable: "Too few pairs were usable to read the rule."

**Reported in every case:** the three fits' RSS and parameters, both ΔAICs with bootstrap intervals, the peak and the |L| range, whether w sits at the grid's edge, and the leave-one-item-out flips.

## 6. What it cannot do

- A pass would not show the human mechanism (perceptual tuning). It shows the shape, on one model and these pairs. em-bm9's own caveat stands: much of the slope may be M becoming less extreme after S, which a shape test does not separate.
- One model (Haiku), 80 pairs from 40 items, anchor (a).

## 7. Stop rules

- No calls. The script records the archive files' sha256.

## 8. Ledger entry (appended after the seed commit)

```json
{"id": "em-bm9f2", "program": "entangled-mind", "map": "map/entangled-mind.json", "direction": "bm9-f2", "parent_bet": "em-bm9",
 "title": "Does the pull toward the last rating have the human serial-dependence (DoG) shape? (Haiku, archive)", "source": "engine",
 "engine_odds": 0.08, "engine_odds_first": 0.25, "engine_odds_v1": 0.08, "human_odds": null, "human_odds_note": "no human odds",
 "budget_usd": 0, "referee": "model", "bet_type": "standard", "seed_source": "curby-rng", "lesson": "ls-em-bm9f2",
 "premortem_kind": "design", "verdict": "open"}
```

## 9. Checklist before the run

- [x] This file and its code are committed on their own; nothing has been run on the archive.
- [x] Lesson in §0, after reading bets.jsonl, brier.md (28 scored, 0.202, base rate 9/30), audits/ (newest ta-b1r2.md; em-bm9.md for the parent) and lessons.jsonl (P1–P15).
- [ ] Design review go.
- [x] Engine odds on record earlier (map 04:45; v1 about 06:02); human odds checked: none.
- [x] §5 applies mechanically; the self-test applies it.
- [x] Pre-mortem: one sentence, a checkable mechanism, kind `design`.
- [x] Seed rule by the 24-hour rule; the seed commit follows.
- [x] DEVIATIONS.md D67.

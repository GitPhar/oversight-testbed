# gm3c-f1: can one format be recovered from the other five? em-gm3c's borderline label, re-tested (pre-registration)

Written and frozen 2026-11-05 (America/Denver; the commit's author time is the record), in its own commit, before the archive is opened for this analysis. DEVIATIONS.md D62. Budget **$0** (archive only; no API call, no QPU second, no local model).

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). His odds come only from `ledger/human-odds.jsonl`. This direction has no line there (`python3 ledger/human_odds_match.py entangled-mind gm3c-f1`, run 06:22: "no human odds"), so the bet proceeds marked "no human odds".

## 0. The bet

| field | value |
|---|---|
| bet id | `em-gm3cf1` |
| referee | `model` (archived model behaviour decides the outcome) |
| bet type | `standard` |
| direction | `gm3c-f1` (map/entangled-mind.json), a follow-up of `gm3c`, bet `em-gm3c` (audited: pass → undetermined) |
| source | `engine` (remap 2026-11-05, `9773f6a`) |
| engine odds, P(pass) | map: 45, stated 2026-11-05T04:45 (remap one pass, not v1). Re-elicited under v1 at about 06:02 (fresh subagent, the direction's row and the draft rule only): 25. After the lesson: **30** |
| human odds, P(pass) | no human odds (no line for gm3c-f1 in `ledger/human-odds.jsonl` at this commit) |
| models | not all three, because no model is in the loop and the question is about Haiku's archived six-format data by design (em-gm3c's re-test). Sonnet's version (gm3c-f2) is already answered in a published table (Q 0.69 [0.53, 0.82]); Opus's arm is incomplete (`experiments/remap-free-check.md`). |
| budget | $0 API · 0 QPU s · about 1 laptop hour (300 fits) |
| lesson | Correcting P10 and P3: em-gm3c's label hung on optimiser, fold and resampling noise, with no link-free baseline. This bet averages ten beacon-drawn fold splits under a converged fit, reads a 10,000-resample BCa bound, requires a link-free predictor also under 0.5, and its odds are 30% (map 45%, v1 25%) because audited refits sat at 0.50–0.52. |
| design review | before the archive is opened, a fresh subagent dry-runs this design (operators/design-review.md) → `ledger/design-reviews/em-gm3cf1.md`. Nothing runs before a go. |
| pre-mortem | If this fails, the most likely reason is that a converged, fold-averaged fit puts mean Q near 0.41, so the BCa upper bound lands between 0.50 and 0.53, as the audit's refits did. Kind: `world`. |
| auditor | fresh subagent per operators/auditor.md, in a planter-built clone, after results |

Odds reasoning: the running base rate is 9/28 = 0.32 (`ledger/brier.md` at `b04215f`: 26 scored, Brier 0.217). The em-gm3c audit (`ledger/audits/em-gm3c.md`) measured the spread this bet runs into. An independent converged refit at the original seeds gave an upper end of 0.501. Other bootstrap seeds gave 0.494–0.504, and three other fold assignments gave 0.497, 0.510 and 0.522, with Q 0.395–0.420. Averaging predictions over splits usually raises R² slightly, which pushes the bound up. BCa can move it either way by a few hundredths. The extra link-free conjunct costs little, because the audit's link-free checks gave about 0.44. So 30.

## 1. In plain English

Program 1 asked Haiku about 160 statements in six ways (a 0–100 rating, yes/no, a bet, a comparison with a coin, a frequency, a verbal scale). Can Haiku's answers in one way be predicted from its answers in the other five? em-gm3c found the prediction recovers about 40% of what each way reproducibly says, and called that "little format-free belief", because its interval ended just under 50%. The audit showed that label sat inside the noise of the optimiser, the fold split and the resampling. This bet removes those three noises: the fit runs to convergence, the result is averaged over ten fold splits drawn from the public beacon, and the interval uses 10,000 resamples with a bias correction (BCa). A pass means the interval sits wholly under 0.5, and a plain least-squares predictor also recovers under half, so the low number is not just a weak model. A fail means "partial" recovery cannot be excluded. Either way, recovery well under the 0.75 needed for "a usable single belief" was already settled by em-gm3c and is not re-bet.

## 2. Material

- **Archive:** `results/gm3b-calls.json` (Haiku, `claude-haiku-5-5`, thinking off; 160 claims × 6 formats × 10 repeats; em-gm3b `D38`). It is read through `gm3b_format_invariance.encode` and `.claims()`, the same encoding em-gm3c used. Before this commit, the session had seen the key format and one record of it (`'h190|0|F1|7' → {"value": 3, …}`). No fit, Q or interval has been computed on it by this session. The published em-gm3c table and its audit are known (§0).
- **Model and prediction:** exactly em-gm3c's (`experiments/gm3c_heldout_format.py`, imported unchanged: `predicted_obs`, `observed_scale`, `claim_means`). The one-credence model L1 is fitted on even repeats, with the held-out format's observations removed for the test fold's claims, and the test fold's odd-repeat claim means are predicted. Ceiling: the format's own even-repeat claim means. Q_f = R²(prediction, odd means) / R²(ceiling, odd means); mean Q over the six formats.
- **Convergence:** gm3b's block coordinate ascent, copied into `fit_tol` unchanged except for the stop rule. It stops when the objective changes by less than 1e-3 log-likelihood units between rounds, with a cap of 2,000 rounds (gm3b stopped at 40). Fits that reach the cap are counted.
- **Fold assignments:** K = 10. Assignment j shuffles the 40 items with `numpy.random.default_rng([fold_seed mod 2^63, j])` and cuts them into 5 folds of 8. Each claim's prediction is the mean of its 10 out-of-fold predictions.
- **Link-free baseline (P3):** for each held-out format and fold, least squares (with intercept) from the other five formats' even-repeat claim means to the format's odd-repeat means, fitted on training claims, with the same assignments and the same averaging. Q is computed the same way.
- **Seed** (operators/hardware.md): CURBY-Q's latest completed round is 28297, result pulse 2025-08-22 13:42 America/Denver (checked 06:07: round 28297), so the chain is stalled. Seed: the first CURBy-RNG pulse timestamped after this commit. Sub-seeds `ledger/seed.py <randomness> em-gm3cf1 --purpose folds` and `--purpose bootstrap`. *Filled in by the seed commit, before any data:*
  `chain:` CURBy-RNG · `pulse_index:` 1592268 · `pulse_time:` 2026-11-05 06:24:00 America/Denver (2026-11-05T13:24:00.161Z; previous pulse 1592267 at 2026-11-05T13:23:00.166Z, before this file's commit d490327 at 06:23:16) · `randomness:` 8cf6c3d56185181f72908234210140895616246dae734d452d8f450ac5aeb512a845229e8e2e93881a932a680442e48a640ae04a62fba3fc7e2335d685664eda · `client:` @buff-beacon-project/curby-client@1.2.0 (Client.randomness(1592268)) · `certificate_verified:` false (classical chain) · `seeds:` folds 18416738419240260146, bootstrap 3943194411379291992
- **Code:** `experiments/gm3cf1_heldout_bca.py`, committed with this file. `--selftest` builds two synthetic six-format worlds (one shared credence, which must fail; large format-specific deviations, which must pass), checks every boundary and checks that BCa reduces to the percentile interval on a symmetric bootstrap. It never opens the archive. It ran OK before this commit (4.6 min).
- **Scale:** every format has one direction (0 = false, 100 = true; gm3b).

## 3. Calls

None. One run: `python experiments/gm3cf1_heldout_bca.py --fold-seed <folds> --boot-seed <bootstrap>`, after the design review's go (about 300 fits).

## 4. Statistics

- **Primary statistic:** mean Q (one-credence model, fold-averaged predictions) over the six formats, with its **BCa 95% interval**: 10,000 item-cluster resamples (the 40 items, with replacement, carrying their claims; P14). The bias correction z0 comes from the share of resamples below the estimate. The acceleration a comes from the leave-one-item-out jackknife of mean Q.
- **Secondary (reported, never promoted):** Q by format; the percentile interval; the link-free predictor's mean Q and its percentile interval; the number of fits at the cap and the most rounds used.
- **Multiple comparisons:** one primary statistic. The link-free conjunct is a guard, not a second test.
- **Robustness committed now:** leave-one-item-out. For each item, the jackknife Q is shifted by the BCa upper bound's distance from the full estimate. The results report the items whose removal would move the bound across 0.5 (P10). If any would, the plain-English section names them.

## 5. Pre-registered reading

1. **Untestable:** more than 10% of the 300 fits stop at the 2,000-round cap.
2. **Pass:** the BCa 95% upper bound of mean Q < 0.50, **and** the link-free predictor's mean Q < 0.50 (both with tolerance 1e-9).
3. **Fail:** anything else.

Verdict sentences (P9), used verbatim:
- pass: "On Haiku's 160 claims, most of what each format reproducibly says cannot be recovered from the other five formats: the one-credence model's recovery is below half, with the whole BCa interval under 0.5, and a link-free predictor also recovers under half."
- fail: "On Haiku's 160 claims, the data do not show recovery below half: the one-credence model's BCa interval reaches 0.5 or above, or a link-free predictor recovers half or more, so em-gm3c's 'little format-free belief' label is not upheld."
- untestable: "The one-credence fit did not converge in enough of the fits to read the rule."

A pass is "pass, unreplicated" (one model, one claim set). It would turn em-gm3c's "undetermined" into "little" on this set only. It is reported as a new bet, and em-gm3c's own verdict is not edited.

**Reported in every case:** mean Q, BCa and percentile intervals, Q by format for both predictors, convergence counts, the leave-one-item-out flips.

## 6. What it cannot do

- It speaks for Haiku on these 160 deliberation claims and these six formats only. Sonnet (0.69) and Opus are other models. "Models" and "LLMs" will not appear.
- Q is a ratio of R² to a split-half ceiling, so it inherits the ceiling's noise. A link-free predictor is a guard against a weak model, not the best possible predictor. A cleverer predictor could recover more.
- It does not compare with Smolin & Wilder's numbers like for like (different items, framings and statistic).

## 7. Stop rules

- No calls, so no budget or refusal path. The script reads one archive file and records its sha256.
- If the run takes over 3 hours, it is stopped and reported as not run (the session does not wait in a loop).

## 8. Ledger entry (appended after the seed commit)

```json
{"id": "em-gm3cf1", "program": "entangled-mind", "map": "map/entangled-mind.json", "direction": "gm3c-f1", "parent_bet": "em-gm3c",
 "title": "Held-out format recovery on Haiku, converged, fold-averaged, BCa (archive)", "source": "engine",
 "engine_odds": 0.30, "engine_odds_first": 0.45, "engine_odds_v1": 0.25, "engine_odds_at": "2026-11-05T04:45",
 "human_odds": null, "human_odds_note": "no human odds", "budget_usd": 0, "referee": "model", "bet_type": "standard",
 "seed_source": "curby-rng", "lesson": "ls-em-gm3cf1", "premortem_kind": "world", "verdict": "open"}
```

## 9. Checklist before the run

- [x] This file and its code are committed on their own; nothing has been run on the archive.
- [x] Lesson in §0, after reading bets.jsonl, brier.md (26 scored, 0.217, base rate 9/28), audits/ (newest sv-b3.md; em-gm3c.md and round-3/em-gm3b.md for this parent) and lessons.jsonl (P1–P15).
- [ ] Design review go.
- [x] Engine odds on record earlier (map 04:45; v1 about 06:02); human odds checked: none.
- [x] §5 applies mechanically; the self-test applies it to synthetic worlds.
- [x] Pre-mortem: one sentence, a checkable mechanism, kind `world`.
- [x] Seed rule by the 24-hour rule; the seed commit follows.
- [x] DEVIATIONS.md D62.

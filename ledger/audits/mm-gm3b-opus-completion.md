---
bet: mm-gm3b-opus-completion (D49, D49a, D50)
program: entangled-mind
prereg_commit: 19715a3 (2026-11-04 09:51:06; experiments/mm-gm3b-opus-completion.md, mm_gm3b_opus_complete.py, DEVIATIONS D49)
results_commit: a8be4b5 (10:30:26; D49, D49a); paper narrowing 9cefab6 (10:31, D50); cut pass 5480c49 (13:05)
auditor_session: audit2 lead auditor (branch audit2)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5 (commit trailers)
same_model_family: true
date: 2026-11-04 15:10 America/Denver
claims_checked: 24
holes_found: 6
overclaims_cut: 13
reproduced: true
verdict_claimed: pass
verdict_after_audit: pass-unreplicated
verdict_stands: false
canary: unknown
false_alarms: 0
failed: false
failure_reason: null  # pass-unreplicated; the run stopped where its frozen cap rule allows (one batch past it, disclosed in D49a)
failure_kind: null
premortem_score: null        # pre-registration predates operators/premortem.md (e287cb3, 14:41); it has no pre-mortem
risk_seen: null
---

# Audit of the Opus six-format completion (D49, D49a) and the paper narrowing (D50)

## In plain English

The numbers reproduce and the pre-registered labels are applied correctly:
- Test F′ on Opus's 68 claims: Q = 0.944 [0.904, 0.973], "a usable single belief".
- DM2 ΔLL: +1.90 [−0.82, +4.65], "mixed".
- Paper rule: "does not hold on Opus".

The F′ label is robust:
- Ten other fold seeds give Q 0.93–0.95, with every lower CI end at 0.89 or above.
- Dropping any one of the 17 items gives Q 0.925–0.954, with every lower CI end at 0.873 or above.
- Item-matched Q rises from 0.27 (Haiku) to 0.70 (Sonnet) to 0.94 (Opus).
- The stopping-rule account in D49a is correct: under the rule as written, h048 fits under the cap and h291 does not.

**What the label cannot carry is the word "credence".**
- Opus answers yes/no the same way in all 10 repeats on 91% of the 68 claims.
- A one-bit predictor ("is the 0–100 rating above 50?", taken from another format's even repeats) reaches Q = **0.88 [0.81, 0.93]**. That is also wholly above the 0.75 bar, so by D46's rule a single true/false verdict per statement would also be read as "a usable single belief".
- The fitted one-credence model adds about 0.06 of Q over that bit (0.94 against 0.88). On yes/no the bit does as well as the model (0.85 against 0.84).

So F′ on Opus shows that the six formats agree on a format-free *verdict*. It does not show that they share a graded *credence* beyond it. The paper's "Opus has a format-free credence to read, in the usefulness sense that matters for elicitation" says more than that.

There are also smaller errors:
- yes/no is quoted as 82% of its ceiling in two places; the table says 0.84.
- The title says "80 claims"; the arm has 68.
- The header gives the within-rule spend ($5.78), not the actual spend ($6.04).
- "Bend its belief in small, reproducible ways, but they do not reorder it" claims reproducibility that a CI including 0 does not establish.
- The comparison with Smolin & Wilder's range lacks its not-like-for-like caveat in the results file.

The result is one model, one item set and one design, so by invariant 7 it is a pass, unreplicated.

## The case that this result is false

The claim is that Opus holds one format-free credence per statement, which it reads out in six formats. Q compares cross-format R² with each format's split-half ceiling, computed across 68 statements. Across statements, the dominant variance is whether the statement is true or false in the model's view. A model that is near-deterministic and agrees with itself on that one bit will score high Q, whether or not anything graded sits underneath.

Opus is near-deterministic. Its yes/no answer is unanimous over 10 repeats on 91% of statements, and three of its six formats (yes/no, bet, pairwise) take only 6–10 distinct claim-mean values across 68 statements. On such data any predictor that recovers the bit will approach the ceiling. If a one-bit baseline passes the same bar, the test has not shown a credence.

The held-out-repeats test, the stricter of the two, favours one-per-format on 74% of claims (mean +1.90, CI just including 0). That is consistent with each format adding small reproducible deviations that one latent cannot absorb. Finally, the comparison claims (Haiku 29%, Sonnet 69%) are on 80 claims, not Opus's 68, and the 68 omit three Haiku-right items, so the most favourable comparison could be partly a claim-set effect.

**What the checks found.** The claim-set worry is unfounded: item-matched Q is 0.27 / 0.70 / 0.94. The fold rule is irrelevant (seeds 1–10: 0.93–0.95). The one-bit worry is largely right: a one-bit predictor passes the bar too (0.88 [0.81, 0.93]).

## Claims checked

| # | claim (results file unless noted) | check run | outcome |
|---|---|---|---|
| 1 | F′ Q = 0.94 [0.90, 0.97] on 68 claims (17 items) | authors' `gm3c_heldout_format.main` on a scratch copy (`scratchpad/d49/fq.py`) | holds: 0.9442 [0.9043, 0.9728] |
| 2 | per-format Q: 0.99, 0.84, 0.97, 0.94, 0.98, 0.94 | same | holds |
| 3 | "The weakest format is yes/no (82% of its ceiling)" (:12; paper/no-credence-to-read.md:330) | table row, recomputation | **wrong: 0.84** |
| 4 | "Every other format is at 94% or above" (:12) | same | holds (0.94–0.99) |
| 5 | F′ label robust to folds | 10 more FOLD_SEEDs (1–10) | holds: Q 0.934–0.954, lower CI ends 0.890–0.922 |
| 6 | F′ label robust to items | leave-one-item-out over 17 items | holds: Q 0.925–0.954; every CI above 0.87 |
| 7 | "Haiku reached 29% on the same kind of statements, and Sonnet 69%" (:10) | authors' F′ on Haiku/Sonnet restricted to Opus's 68 claims | holds as a trend; item-matched values are 0.27 [0.19, 0.38] and 0.70 [0.54, 0.83]; 0.29/0.69 are on 80 claims |
| 8 | "One belief predicts every format on Opus" (:9), "One credence predicts every format" (paper:330), "Opus has a format-free credence to read" (paper:332) | one-bit baseline (`scratchpad/d49/bit2.py`) | **overclaim**: one bit gives Q 0.88 [0.81, 0.93] (per format 0.87, 0.85, 0.94, 0.96, 0.86, 0.80); a 3-level version 0.91 |
| 9 | R² 0.92 "above the top of the 0.60–0.90 range Smolin & Wilder report" (:11) | `paper/gold-map.md:177-178`, `audits/gm3c-heldout-format.md` hole 2 | **overclaim in the results file** (no caveat; their framings come in near-duplicate families, items and held-out unit differ); the paper:330 version carries the caveat; source not checkable offline |
| 10 | ΔLL +1.90 [−0.82, +4.65], 74% positive, mixed | `mm-gm3b-format-invariance.json`, regenerated by reproduce.py | holds; the label follows DM2's rule (>half positive, CI not above 0) |
| 11 | "a tenth of Haiku's +19.4 and a fifth of Sonnet's +9.2" (:17) | arithmetic | holds (0.098, 0.206); different claim sets (80 vs 68) |
| 12 | "Opus's formats bend its belief in small, reproducible ways, but they do not reorder it" (:18) | ΔLL CI; Spearman ρ range; pairwise ordering (`scratchpad/d49/disc.py`) | **overclaim**: "reproducible" is not established (CI includes 0); "do not reorder" is too strong: 0.2–5.5% of statement pairs are ordered oppositely to the 0–100 rating, and ρ falls to +0.83 between some formats |
| 13 | item-matched W 0.56 / 0.76 / 0.87 (exploratory) | authors' script logic, item bootstrap (`scratchpad/d49/w.py`) | holds as a trend: Opus − Sonnet CI [+0.05, +0.24], Sonnet − Haiku [+0.08, +0.36] (tie-corrected W). Hole (minor): the authors' W breaks ties by argsort order; three formats have 58–63 tied claim means of 68, and tie-corrected W is 0.55 / 0.78 / 0.91 |
| 14 | D49a: code projected on the previous batch's mean; rule as written stops before h291 | cost-by-batch simulation from the cache (`scratchpad` inline) | holds: rule projections for h291 $6.48 (mean of new calls) or $6.43 (whole-arm mean), both > $6.40; for h048 $6.24 / $6.18, both ≤ $6.40; code projected $6.13 |
| 15 | "$5.78 new spend … ($8.88 for the whole Opus arm)" (:3) | cache sums | holds as the within-rule spend; **actual spend is $6.04 new / $9.14 arm** (D49a), not stated in the results file's header |
| 16 | "0 refusals; 0 max_tokens stops" | 4,080 + 240 cached calls | holds: no `refused`, no `error`, no null values |
| 17 | h093 cancelled, none billed | batch id in D49a; not in `mm-batches-gm3b-opus-completion.json` | cannot check (no billing archive) |
| 18 | "The pre-registered stopping rule ended the run at 17 of the 20 items" (:7) | D49a | holds, but the rule did not end the run: the code ran one batch past it and the author stopped it. The sentence should say "the rule allows 17" |
| 19 | Title "completed (80 claims)" (:1) | — | **wrong**: 68 of 80 |
| 20 | "The earlier 26 statements are not special … +2.42 against +1.57" (:26) | ordering of `per_claim_dLL` vs `done` checked against `mm_gm3b.analyse_one` | numbers hold; "not special" is a no-CI comparison stated as a finding (overclaim, minor) |
| 21 | with h291: Q 0.94 [0.90, 0.97]; ΔLL +1.55 [−1.00, +4.17]; W 0.85 | reproduce.py step `mm-gm3b-opus-completion-with-h291.md` | holds |
| 22 | paper rule "does not hold on Opus" | `paper_reading()` vs §4 of `19715a3` | holds: rule applied as frozen |
| 23 | D50: paper's "6–14% reversed pairs" | `disc.py` | the paper text now says "(1 − τ_b)/2 … 6–14%" (fixed in D51); D50's DEVIATIONS text still says "reversed pairs" (record only) |
| 24 | D49a text "h048 was cheap (/bin/zsh.0012 per call)" (DEVIATIONS.md, D49a) | — | transcription error (a shell expanded `$0`): should read "$0.0012" |

## Checklist

**A. Pre-registration**
1. *Prereg predates the calls.* Holds: frozen `19715a3` 09:51:06. The 2,720 new calls' message IDs decode (`audits/tools/ridtime.py`) to 09:52:19 – 10:19:51, so the first is 73 s after the freeze; the 1,600 earlier calls decode to 07:46. The pre-registration discloses one look at the data before freezing (F′ on the 6 complete items, Q 0.96). It says the paper rule was written in code before that look, which **cannot be checked** (not in git before `19715a3`). With a 0.96 preview, the outcome of a 0.75 bar was close to known in advance. That is disclosed, and it is why the run was worth less than its cost as a test.
2. *Rule, statistic, split, seed, budget match the prereg.* Holds. The F′ fold rule is `i // 8` with FOLD_SEED 4646. On 17 items that gives folds of 8, 8 and 1. That is "the same fold rule" as pre-registered, but the third fold is a single item (h191). The fold check (claims row 5) shows this does not matter.
3. *Bar not lowered.* Holds: D46's 0.75 and 0.5 bars and DM2's rule, unchanged.
4. *Primary is the pre-registered primary.* Holds. The pre-registration names DM2's rule "primary" and F′ as the second reading. The paper rule keys on F′. That keying was frozen in §4, so it is pre-registered, not promoted after the data.

**B. Is the number real?**
5. *Ties.* **Hole (minor).** Kendall's W uses `argsort` ranks, so ties are broken by claim order. Opus has 58–63 tied claim means of 68 on yes/no, bet and pairwise. Tie-corrected W is 0.55 / 0.78 / 0.91 against the reported 0.56 / 0.76 / 0.87. The trend survives (row 13). F′ uses Pearson R² on claim means and is not affected by ties.
6. *Pooling.* Pooled across Haiku-right and Haiku-wrong items (10 wrong, 7 right in the 68). Pre-registered; not a hole.
7. *Few items.* Holds. Leave-one-item-out over the 17 items (authors' fit, `scratchpad/d49/batch.py`): Q 0.925–0.954, lowest lower CI end 0.873 (dropping h190), every interval wholly above 0.75. No item carries the label.
8. *Circular estimators.* Holds: test fold's held-out format removed from the fit; targets are odd repeats, the fit uses even.
9. *Baselines.* **Hole (the main one).** No baseline was pre-registered or reported. A one-bit predictor passes the same bar (Q 0.88 [0.81, 0.93]). On Sonnet the same bit gives 0.55 against the model's 0.69, and on Haiku 0.20 against 0.29. So the bit explains most of the cross-model trend as well.
10. *Uncertainty.* Holds: item-cluster bootstrap with 2,000 resamples. But W is reported with no interval anywhere (row 13 supplies one).
11. *Multiple comparisons.* Two pre-registered readings plus a paper rule, plus W and a 26-vs-rest split as descriptives. Not corrected, and not said. Nothing turns on it at these margins.
12. *Leakage.* Holds.

**C. Write-up**
13. *Scope.* README:23 and paper:29/332/358 say "on Opus the format finding is contradicted" and "On Opus there is a credence to read". That is one model, 17 items and one design.
14. *Rank drift.* The exploratory item-matched W is labelled exploratory everywhere it appears. Holds.
15. *Mechanism drift.* **Hole.** "Bend its belief" and "credence to read" name the latent as a credence. The design cannot separate a graded credence from a shared binary verdict (B9).
16. *Plain English vs table.* Holes at :9, :12 (82%), :18, :26 (listed in Required cuts).
17. *Citations.* Smolin & Wilder (arXiv:2609.07943): **cannot check** offline. The repo's own summary (`paper/gold-map.md:178`) supports "R² 60–90% on held-out outputs" but not like-for-like comparability.
18. *Negatives stated plainly.* Holds. The mixed DM2 reading is reported next to the pass.

**D. Process**
19. *Budget.* **Hole (disclosed).** The cap was enforced in code, but the code's projection disagreed with the frozen rule, and one batch ran past the stopping rule ($0.26). That was caught by the author, and the next batch was cancelled. The total of $6.04 is under the $6.40 cap. The results file's header gives only the within-rule $5.78.
20. *Refusals.* Holds: none.
21. *One scale direction.* Holds: DM2's single direction.
22. *Replication.* One model, one design. The result is a pass, unreplicated. The "rises with model strength" trend is three models, one each, on one item set.

## The pre-mortem, scored

The pre-registration has no pre-mortem: it was frozen before `operators/premortem.md` entered the standard (`e287cb3`, 14:41). So `premortem_score: null`. The auditor's own one-line failure account is in the front matter (`failure_reason`, `failure_kind`).

**E23–E24.** Not applicable: no beacon seed, and not a tiebreak bet.

## Required cuts

- `results/mm-gm3b-opus-completion.md:1` (writer in `mm_gm3b_opus_complete.write_md`): "Opus six-format arm completed (80 claims), with test F′" → "Opus six-format arm continued to 68 of 80 claims (17 of 20 items), with test F′".
- `results/mm-gm3b-opus-completion.md:3`: "**$5.78** new spend of the $6.40 cap ($8.88 for the whole Opus arm, batch rate)" → append "; actual new spend $6.04 including h291, which ran past the stopping rule (D49a); $9.14 for the whole arm".
- `:7`: "The pre-registered stopping rule ended the run at 17 of the 20 items" → "The pre-registered stopping rule allows 17 of the 20 items (the runner ran one more, h291, past it; see D49a)".
- `:9`: "**One belief predicts every format on Opus.**" → "**On Opus, one latent per statement predicts every format close to its ceiling, though a one-bit true/false verdict nearly does too.**"
- `:10` (after the Haiku/Sonnet sentence): add "On Opus's 68 statements, Haiku reaches 27% and Sonnet 70% (audit recomputation). A one-bit predictor (the 0–100 rating above or below 50, taken from another format) reaches 88% [81%, 93%] on Opus, also above the 75% bar, so the test shows a shared format-free verdict more clearly than a graded credence."
- `:11`: "That is above the top of the 0.60–0.90 range Smolin & Wilder report for other capable models." → "That is above the top of the 0.60–0.90 range Smolin & Wilder report for other capable models, though on different framings, items and held-out units, so the comparison is indicative only."
- `:12` and `paper/no-credence-to-read.md:330`: "82%" → "84%".
- `:18`: "So Opus's formats bend its belief in small, reproducible ways, but they do not reorder it." → "So any format effect on Opus is small. Whether it is reproducible is undetermined (the interval includes 0). The formats rarely order statements oppositely (0.2–5.5% of pairs against the 0–100 rating)."
- `:26`: "The earlier 26 statements are not special." → "The earlier 26 statements' mean ΔLL (+2.42) is close to the rest's (+1.57); no interval was computed."
- `paper/no-credence-to-read.md:330`: "**One credence predicts every format.**" → "**One latent per statement predicts every format close to its ceiling.**", and add: "A one-bit true/false predictor reaches Q 0.88 [0.81, 0.93], also above the bar, so most of this is a format-free verdict."
- `paper/no-credence-to-read.md:332`: "Opus has a format-free credence to read, in the usefulness sense that matters for elicitation." → "On Opus the six formats agree on a format-free verdict per statement, close to each format's ceiling. Whether they share a graded credence beyond that verdict is not shown: one true/false bit passes the same bar."
- `paper/no-credence-to-read.md:358`: "On Opus there is a credence to read." → "On Opus there is at least a format-free verdict to read; a graded credence beyond it is not established."
- `README.md:23` and `paper/morning-brief.md:25`, `:116`, `:147`, `:155`: wherever "one belief predicts each left-out format at 94% of its ceiling" appears, add "(a one-bit true/false predictor reaches 88%)".
- `DEVIATIONS.md` D49a: "/bin/zsh.0012" → "$0.0012" (record transcription error; for the owning session).

## What would break it next

1. **$0, archive only:** pre-register a baseline-adjusted F′. Q_model − Q_bit, with an item bootstrap, on all three models' archived six-format calls, and a bar fixed in advance (for example, the CI of Q_model − Q_bit lies above 0.05). If Opus's graded component is real, it clears it. The auditor's point estimate is +0.06.
2. **About $2 on Opus:** run the 12 remaining claims (h093, h183 and the rest of the 20) and add 20 statements chosen to be *contested* for Opus (rating 30–70 in a pilot). On such statements a one-bit predictor cannot reach the ceiling, so F′ would test a graded credence directly. At the observed $0.00217 per call, 32 claims × 60 calls cost about $4.20 at the batch rate, or about $2 for 16 claims.

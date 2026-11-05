# sg-b7: lead-in only, does the closing line "Now grade the conclusion above" carry part of what sg-b4 left between its quoted copy and a fresh grade? (result)

Pre-registered in `experiments/sg-b7-leadin.md` (`7041920`, 2026-11-05 11:43 America/Denver), direction sg-d14. The seed is CURBy-RNG pulse 1592588 (`5ccc6a6`).
- **Design review** (`ledger/design-reviews/sg-b7.md`): fix-first with 2 flaws (`f3994ff`), no pilot. The fixes are D22 (`6d4e69c`) and, for the shared dry run, D23 (`124b665`), confirmed go at 12:02 (`ac24166`), before the first call.
- **Run:** 2026-11-05, 12:02:54 to 12:04:47 America/Denver. **480 calls, complete, no refusal, $0.598** of the $0.75 cap. The program had then spent $5.29 of $7.65 (br-016, D19).
- **Odds:** engine 14 (v2; the map stated none). Sean's odds: 50 (`ho-20261105-112945-mjj`).
- **Audit:** pending.

## In plain English

**Pre-registered verdict: mixed.** In the pre-registered words (§5.3):

> Haiku read undetermined and Opus read undetermined (Haiku S +2.48 [+0.18, +4.88] against a 2.9 bar; Opus S +0.33 [−0.44, +1.15] against a 0.75 bar): this test gives no single answer about whether the closing line carries sg-b4's remainder.

**What was done.**
- In sg-b4, Haiku and Opus shown their writing conversation as a quoted copy ending "Now grade the conclusion above." still docked a planted exaggeration less than in sg-b3's fresh frame, by 5.8 and 1.5 points of 100. The closing line is one of three things that separate the two settings.
- Here the quoted copy was graded twice in one sitting: once with its closing line as it was, and once with only that line swapped for the fresh frame's "Grade the conclusion." Haiku on all 60 studies, Opus and Sonnet on sg-b4's 30, each version clean and with the exaggeration.
- The measure, S, is how much more the exaggeration cost with the plain closing line.

**What the numbers say.**
- **Haiku:** with "Now grade the conclusion above." the exaggeration cost 72.8 points, with "Grade the conclusion." 75.3. S = +2.5 [+0.2, +4.9]: above 0, but below its 2.9 bar, with an interval reaching both sides of it. The flawed text itself scored 3.0 points lower with the plain line [+0.7, +5.3]. That is 43% of what sg-b4 left on Haiku.
- **Opus:** 83.9 against 84.2. S = +0.3 [−0.4, +1.1]: the closing line made no difference that this test can see; the interval reaches from below 0 to above the 0.75 bar.
- **Sonnet** (reported): S = −0.5 [−1.2, +0.1]; it had no remainder to split.

**How strong it is.**
- **Haiku's mean rests on a few studies.** 14 of its 60 studies show no change at all (S = 0), its median S is +0.5, and its 10% trimmed mean +2.1. Dropping one study (t60) or one domain (domain 17) turns its reading into "lead-in carries part"; it is fragile.
- **Opus's reading is fragile the other way:** dropping study t07, or domain 15, turns it into "not the lead-in". Its median S is 0.0.
- The spread of S across studies is about what the dry run's measured noise predicted (SD 7.95 on Haiku against about 8.3 implied; 2.70 on Opus against about 2.9), so the dry run's power figures stand: under its noise, even a closing line that carried all of sg-b4's remainder would have passed only about half the time, because of Opus.
- The quoted copy's penalty in this run is close to sg-b4's on the same studies (Haiku −0.9 [−2.6, +0.5], Opus +0.2).

**So, on this test:** on Haiku, swapping only the closing line made it somewhat stricter about the exaggeration, by under half of what sg-b4 left, on a mean carried by a few studies; on Opus it changed nothing measurable. Neither model clears or misses its bar cleanly, so this test does not say whether the closing line carries sg-b4's remainder. If the closing line carries part of it, that part is small on Opus.

**What this does not show** (§6, D22):
- It splits the remainder only between the closing line and everything else; the header sentence and the labels are not separated from each other.
- The swap changes "Now" and "above" together; the claim is about that one line.
- sg-b4's remainder was itself measured across two runs (sg-b4's quoted cells against sg-b3's fresh cells); part of it may be run-to-run difference, which this test does not separate.
- Opus and Sonnet on 30 studies; the exaggeration was planted, one wording, at the end; three models from one family, one item set. Not "models", not "every".
- **Multiplicity:** two scored readings by conjunction; no correction.

## Tables

| model | studies | S | 95% CI (20 domains) | 95% CI (studies) | F | F 95% CI (domains) | penalty, 'Grade the conclusion.' | penalty, 'Now grade the conclusion above.' | sg-b4's L | reading |
|---|---|---|---|---|---|---|---|---|---|---|
| Haiku | 60 | +2.48 | [+0.18, +4.88] | [+0.52, +4.48] | +2.97 | [+0.67, +5.32] | 75.3 | 72.8 | +5.77 | **undetermined** |
| Opus | 30 | +0.33 | [−0.44, +1.15] | [−0.60, +1.27] | +0.13 | [−0.29, +0.53] | 84.2 | 83.9 | +1.50 | **undetermined** |
| Sonnet | 30 | −0.53 | [−1.24, +0.13] | [−1.37, +0.27] | −0.50 | [−1.17, +0.14] | 88.0 | 88.6 | +0.17 | reported only |

|  | Haiku | Opus | Sonnet |
|---|---|---|---|
| S as a share of sg-b4's L | 0.43 | 0.22 | -3.20 |
| clean text, plain − quoted (points) | −0.48 | +0.20 | −0.03 |
| quoted penalty, this run − sg-b4's | −0.90 | +0.20 | −0.13 |
| reading on the study bootstrap | undetermined | undetermined | — |
| fragile, one study dropped | yes | yes | — |
| fragile, one domain dropped | yes | yes | — |
| ties (S = 0) | 14 | 5 | — |
| median S | +0.50 | 0.00 | — |

|  | Haiku | Opus | Sonnet | total |
|---|---|---|---|---|
| test run | $0.018 | $0.386 | $0.194 | **$0.598** |

- S = (clean − flawed) with "Grade the conclusion." − (clean − flawed) with "Now grade the conclusion above.", per study, both in the quoted copy, this run; F = quoted flawed − plain flawed. Penalties are clean − flawed, in points of 100.
- **The bars:** Haiku 2.9, Opus 0.75 (half of each model's sg-b4 L). **Verdict** (§5): Haiku and Opus both undetermined → **mixed**. Score 0 against engine odds 0.14.

Raw data: `results/sg-b7-grade-calls.json` (committed `50e341b`, before this analysis). The analysis is `results/sg-b7-analysis.json`, regenerated by `python3 experiments/sg_b7_leadin.py analyse` with no calls. The tables above are printed by `sg_b7_leadin.tables()`.

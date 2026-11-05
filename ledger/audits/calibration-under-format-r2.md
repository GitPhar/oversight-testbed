---
bet: calibration-under-format (DM6, DM6a), round 2
program: entangled-mind
prereg_commit: f406a9c
results_commit: 9042d7f
auditor_session: audit2 worktree, second-round calibration audit
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5 (commits c066c76, 5480c49 and 772dc12 are co-authored by Claude Opus 5.5)
same_model_family: true
date: 2026-11-04 14:48 America/Denver
claims_checked: 34
holes_found: 11
overclaims_cut: 14
reproduced: true
verdict_claimed: mixed
verdict_after_audit: mixed
verdict_stands: true
canary: unknown
---

# Audit of calibration-under-format, round 2: Tian et al. Verb. 1S top-1 under format and question order

**Files audited:**
- `results/calibration-under-format.md` at HEAD `9042d7f`;
- the archives `results/calibration-under-format{,-exploratory}.json`, `results/cal-{haiku,sonnet}-conversations.json` and `results/pool-run-3.json`;
- the code `experiments/cal_format.py` and `experiments/cal_format_explore.py`;
- the pre-registration `experiments/cal-format-order.md` and DEVIATIONS DM6 at `f406a9c`, and DM6a at `c066c76`;
- the D51 erratum (`DEVIATIONS.md:1013`) and `paper/record.md:66, :99`.

**Round 1:** `audits/calibration-under-format.md`, written against `b009a15`. The cut pass was `5480c49`.

**Scripts and outputs:** all in `/private/tmp/claude-501/-Users-seanpharris-entangled-mind-audit2/bb46787f-112b-4a3c-a1e9-dd87d67b2c75/scratchpad/cal/`. They are `common.py` and `a1`–`a12`, with outputs in `bins_*.txt`. Every script was run with `python -I`, made no network calls and cost $0.

## In plain English

The pre-registered readings stand:
- **Sonnet's ECE changes with format.** This survives every check I ran: 5, 10, 15 and 20 equal-width bins; 10 and 15 adaptive bins; Brier; matching the excluded questions across formats; leaving out any block or any question; and a Bonferroni correction.
- **Haiku shows no format effect, and neither model shows an order effect.** Both nulls also survive every check.

Every number in the file reproduces from the archive:
- reproduce.py's calibration step matches byte for byte;
- the exploratory JSON regenerates identically;
- my own parser has 0 mismatches against the archive.

All six round-1 cuts were applied: five as written, and the DEVIATIONS one as an erratum.

The text still says more than the data in three places. Two of them come from sentences the cut pass added.
1. **Sonnet's "conversation versus fresh" effect is an exclusion artefact.** On questions parsed in both contexts it is +0.011 [−0.115, +0.096] (strict), +0.004 (scoring A) and −0.008 (scoring B), against −0.107 as reported.
2. **Haiku's context effect reverses sign between the two readings of the number.** It also disappears when each answer is read in the way that makes it coherent. The new line "for Haiku, on the context only" therefore claims too much.
3. **Sonnet's format effect also changes sign under that coherent reading.** Its size shrinks to +0.02 to +0.04. "The format alone moves ECE by a factor of 1.7 to 2.9" is a statement about one reading of the number, measured on different question subsets.

Fourteen sentences need rewriting.

## The case that this result is false

*(Written before the checklist.)*

The headline is "Sonnet's calibration depends on format" (ΔECE −0.143). That statistic is ECE on two different sets of questions.
- **Format-dependent exclusions.** In probability-format conversations, Sonnet hit max_tokens in 24 conversations against 15 in the frequency format. It lost 65–85 questions per order to those stops, against 39–53.
- **Open-form guesses** ("Guess: 43 ft") remove another 80–155 questions per cell, and the share differs by format and context.
- **What is left differs by format.** In conversations, probability-format cells keep 68–80 questions and frequency-format cells keep 112–118.
- **The kept subsets are not alike.** Strict accuracy on them is 0.94/0.88 (probability) against 0.80/0.84 (frequency). A frequency cell that keeps more hard questions and assigns them high confidence will look better calibrated with no change in calibration.

The number also means different things in the two formats:
- On "Is the answer X?" items, the number in the probability format is often P(X), not P(guess correct). Sonnet does this on 50% of its fresh "no" guesses in the probability format, against 14–19% in the frequency format.
- Under the frozen scoring (number = confidence in the guess), every "Guess: No / Probability: 0.1" answer scores as a 0.1-confidence correct answer: a huge calibration error that is really a referent error.

Score each answer the way that makes it coherent instead. That means reading a "no" guess with a number below 0.5 as P(X), and so as confidence 1 − p in "no" (my scoring C, exploratory):
- Sonnet's ECE falls to 0.03–0.09 in every cell;
- the probability format becomes the better-calibrated one: format contrast **+0.037 [+0.001, +0.070]**, and +0.022 [+0.003, +0.048] on matched questions.

On that view, the pre-registered −0.143 measures how often Sonnet misreads Tian's wording in each format. It does not measure calibration, and its sign is an artefact of that misreading. The same argument applies to the conversation-versus-fresh effect. Haiku misreads more often when asked fresh (73–82%) than in conversations (48–68%). Under scoring C, conversation − fresh is +0.004 [−0.030, +0.037] for Haiku and +0.018 [−0.019, +0.041] for Sonnet: nothing.

**What the checklist finds.** The case is right about the sign, about the context effect and about the "factor of 2–3" framing. It is wrong that nothing is left. Some ECE number moves with format for Sonnet in every scoring, binning and matching tried, and the CI excludes 0 every time (under C only just). The pre-registered rule asks only whether the CI excludes 0, so the label "calibration depends on format" stands.

## Round-1 cuts: applied?

| # | round-1 target | required | current tree (`git diff b009a15 HEAD`, `git show 5480c49`) | status |
|---|---|---|---|---|
| 1 | `results/calibration-under-format.md:20` "two flaws" | "three flaws" plus an open-form bullet | `:20` "three flaws"; `:22` open-form bullet with 93–118 / 35–41 / 80–155 | applied as written; numbers verified |
| 2 | `:21` "About 120 … 'Is this claim true?'" | "60 … 'Is the following claim true?'" | `:21` as required | applied as written; 60 verified |
| 3 | `DEVIATIONS.md:852` "About 120 …" | rewrite with 60 and the open-form exclusion | `:852` unchanged; erratum at `DEVIATIONS.md:1013` ("'About 120' True/False questions should be 60, and the open-form exclusion was omitted") under D51's rule that the log is not edited | adapted (acceptable); the erratum omits "more often in the probability format" |
| 4 | `:36` "across the same 300 questions" | "across cells (each on 111–167 parsed questions)" | `:37` as required | applied as written; 111–167 verified |
| 5 | `:42` "A calibration number … a model, a format and a context together." | "For Sonnet … format and the context; for Haiku, on the context only. The direction … depends on how the number is read." | `:43` as required | applied as written, **but the replacement wording (written by round 1) is itself partly unsupported**: see holes 1 and 2 |
| 6 | `:44` "That is the paper's point about construction in a very concrete form." | cut | removed | applied |

Unrequested changes in the same pass:
- `:44` "Aggregate ECE was robust to question order" became "No effect of question order on aggregate ECE was detected here (Haiku +0.022 [−0.076, +0.104], Sonnet +0.055 [−0.088, +0.162])".
- `:154` "null in every version" became "not detected in any version".

Both are correct; the numbers are verified.

**Cross-cutting audits.** Neither `audits/synthesis-claims.md` nor `audits/record-accuracy.md` lists a cut aimed at the calibration sentences. Their record cuts (`record.md:3`, `:69`) cover DM1–DM6 generically, and the record now includes DM6 (`record.md:3`, `:66`, `:99`). The SUMMARY's numbers-wrong row ("about 120" → 60) is fixed in the results file and in the erratum. It is still wrong in `experiments/cal_format_explore.py:5` (docstring).

**Round-1 holes that were not turned into cuts and are still open:**
- format-dependent max_tokens stops are not reported in the results file;
- multiple comparisons are not stated;
- DM6's "08:35 … before any call" date has no erratum.

**Tally:** 6 round-1 cuts. 5 applied as written, 1 adapted, 0 not applied, 0 applied wrongly. One of the five (#5) carries round-1 wording that this round finds partly unsupported.

## Claims checked

The "own" columns come from my parser, ECE and bootstrap. The bootstrap uses the author's seed (4042) unless marked "own rng" (PCG64(4819)), "q-level" (questions resampled, not blocks) or "matched" (restricted to questions parsed in both cells of each contrast).

| # | claim (results file, line) | check run | outcome |
|---|---|---|---|
| 1 | 300 questions, 30 blocks of 10, 10 bins, 2,000 block resamples (`:3`) | `cal_format.py:22,44–47`; pool has 300 ids (120 "Is the answer", 120 "Is the correct answer", 60 claim) | holds |
| 2 | Sonnet format −0.143 [−0.233, −0.066] (`:15`, `:100`) | own: −0.143 [−0.233, −0.066]; own rng [−0.229, −0.065]; q-level [−0.212, −0.072]; matched −0.119 [−0.203, −0.029]; 15 bins −0.126; adaptive-10 −0.144; Brier −0.104 [−0.191, −0.024]; leave-one-block-out −0.160 to −0.125; Bonferroni/4 [−0.266, −0.045] | holds (numbers and the CI-excludes-0 rule) |
| 3 | replicate noise +0.005 (`:15`, `:102`) | +0.005 [−0.044, +0.061] | holds |
| 4 | Haiku format −0.007 [−0.100, +0.075] (`:16`) | reproduced exactly; matched +0.019 [−0.066, +0.105]; every binning spans 0 | holds |
| 5 | order +0.022 / +0.055, both spanning 0 (`:17`, `:44`) | reproduced exactly; matched +0.064 [−0.009, +0.143] / +0.006; spans 0 under every binning and every scoring | holds |
| 6 | conversation − fresh −0.15 / −0.11, both excluding 0 (`:18`) | strict reproduced (−0.152 [−0.220, −0.077]; −0.107 [−0.181, −0.030]). **Sonnet matched: +0.011 [−0.115, +0.096]** (9 and 24 questions); A matched +0.004 [−0.025, +0.030]; B matched −0.008. Haiku matched −0.102 [−0.207, −0.007] | Haiku holds; **Sonnet hole** (exclusion artefact) |
| 7 | 60 questions "Is the following claim true?", answered True/False (`:21`) | 60; Sonnet T/F on all 60 in every fresh cell; Haiku 54–58 | holds |
| 8 | open-form unparsed: Haiku 93–118 P vs 35–41 F; Sonnet 80–155 (`:22`) | Haiku 109/93/118/112 vs 35/36/41/38; Sonnet 104/106/99/80 (conversations), 116/119/147/155 (fresh). For Sonnet the fresh direction is the reverse (F > P), which is not stated | holds; incomplete |
| 9 | max_tokens stop ends the conversation under the frozen rule (`:23`) | `mm_common.py:8,111` and `cal_format.py:95` at `f406a9c` | holds; **format dependence not stated** (Sonnet fresh 46 P vs 20 F; conversations 24 vs 15; questions lost 85/65 vs 39/53) |
| 10 | each cell rests on 68–199 of 300 (`:24`) | Haiku 108–199, Sonnet 68–118 | holds |
| 11 | Sonnet "no" guesses below 0.5: 50% fresh P, 14–19% fresh F, 3–7% F conversations (`:31`, table `:130–133`) | 49.5/48.5%, 14.5/19.3%, 7.1/2.8% | holds |
| 12 | Haiku 73–82% fresh, 48–68% conversations (`:32`) | 78.4/73.4/82.2/82.2; 55.3/47.9/68.2/63.9 | holds |
| 13 | "changes *which quantity the model reports*" (`:34`) | inferred from a proxy (no-guess with p < 0.5), not observed | overclaim (mechanism stated as fact) |
| 14 | Sonnet A-scored ECE 0.06–0.27, cells of 111–167 (`:37`) | 0.061–0.270; n 111–167 | holds |
| 15 | replicate noise about 0.01 under A (`:37`) | −0.009 [−0.034, +0.027] | holds |
| 16 | Sonnet A format −0.083 [−0.137, −0.032] (`:38`) | reproduced; matched −0.066 [−0.109, −0.017] | holds |
| 17 | order makes no detectable difference under A (`:39`) | holds under A and B, matched and unmatched | holds |
| 18 | scored the other way, several contrasts change sign (`:40`) | format and conversation − fresh for both models; order | holds |
| 19 | "For Sonnet … depended on the format and the context; for Haiku, on the context only" (`:43`, new in `5480c49`) | Sonnet context: matched ≈ 0 in all scorings (#6). Haiku context: −0.118 (A), +0.081 (B), +0.004 [−0.030, +0.037] (C); matched −0.078 / +0.092 / −0.003 | **hole** (Sonnet false; Haiku sign-unstable) |
| 20 | "the format alone moves ECE by a factor of about 1.7 to 2.9 … far beyond run-to-run noise" (`:43`) | P/F ratios: strict 1.83–2.87; A 1.72–2.79; **B 0.65–0.91; C 0.34–0.58** (inverted). "Format alone": the cells are different question subsets | overclaim |
| 21 | |Δconf| 0.22 vs 0.10 Haiku; 0.65 vs 0.14 Sonnet P (`:44`) | reproduced. Sonnet's 0.65 rests on **22** questions, 16 of which move > 0.5 (a reading switch, not graded movement). Sonnet F is 0.10 vs 0.08 (not mentioned) | holds; selective |
| 22 | "Part of the format effect is the format changing the question" (`:45`) | not separable from the format-dependent exclusions in this design | overclaim (mechanism) |
| 23 | budget $2.61 of $3 (Haiku $0.12, Sonnet $2.49) (`:46`) | $0.121 + $2.486 | holds |
| 24 | per-cell table: n, accuracy, confidence, ECE, Brier, AUROC, unparsed (`:56–63`, `:89–96`) | reproduce.py match; own recomputation identical | holds |
| 25 | contrast tables (`:65–72`, `:98–105`) | reproduced to 3 dp with the author's seed | holds |
| 26 | "abandoned conversations: 32 / 105" (`:52`, `:85`) | 32 = 9 conversations + 23 fresh calls; 105 = 39 + 66 | holds (the label counts fresh single calls as "conversations") |
| 27 | lower-ECE model the same in all four conversation cells: True (`:116`) | Sonnet is lower in all 4 | holds |
| 28 | A-scored n per cell 111–255 (`:135`) | holds | holds |
| 29 | exploratory contrast table (`:146–151`) | `cal_format_explore.py` regenerates the JSON identically; own recomputation matches | holds |
| 30 | "Order: not detected in any version" (`:154`) | also matched, under 5–20 bins and adaptive bins, and under C | holds |
| 31 | "format effect for Sonnet and the conversation-against-fresh effect for both models are far larger than replicate noise in every version" (`:155`) | Sonnet conversation − fresh vanishes when matched (#6); both models' vanish under C | **hole** |
| 32 | record: "Sonnet's ECE depends on format (−0.143 [−0.233, −0.066] …)" (`paper/record.md:66`) | numbers hold; no sign caveat | overclaim (minor) |
| 33 | record: "calibration depends on format for Sonnet (DM6)" (`paper/record.md:99`) | holds as a label; no sign caveat | minor |
| 34 | D51 erratum on DM6 line 852 (`DEVIATIONS.md:1013`) | correct | holds |

## Checklist

**A. Pre-registration**

1. **Holds.** `f406a9c` is dated 07:53:12. Message IDs decode (`audits/tools/ridtime.py`) to Haiku 07:55:23–08:18:25 and Sonnet 08:20:38–08:49:35. `cal_format.py` is unchanged from `f406a9c` to HEAD (`git diff f406a9c HEAD -- experiments/cal_format.py` is empty). DM6's "Date: 08:35 MST, before any call" is false as written: it falls after the whole Haiku run. It is still uncorrected, and D51's erratum list omits it (hole 8).
2. **Holds.** The statistic, bins, seeds (4041, 4042), 2,000 resamples, caps ($0.30 / $2.60) and reading rule all match §2–§5. Two definitions match the code (`cal_format.py:164–167`): conversation − fresh uses fresh r0 only (§4), and the format contrast is computed in conversation cells only.
3. **Holds.** The bar is unchanged. DM6a explicitly keeps the pre-registered readings.
4. **Holds.** The headline −0.143 is the pre-registered primary. The exploratory −0.083 is labelled as exploratory.

**B. Is the number real?**

5. **Holds.** *Ties and floating point.* Confidences are integers / 100 (F) or decimals (P). No value from k/100 falls into the wrong bin through floating point (`a3_map.py`). Bin-edge values are handled by `min(int(conf·10), 9)`, which I re-implemented with explicit edges and got the same result.
6. **Hole (handled in the text, but see 10).** *Pooling.* The primaries average two orders or two formats. Unpooled, they appear in the file's own rows (`:71–72`, `:104–105`). One scale direction applies throughout. The real pooling problem is across question subsets:
   - The exclusions differ by format. Haiku has 3× more open-form guesses in P. Sonnet has more max_tokens stops in P and more open-form guesses in fresh F.
   - So each "paired" contrast compares ECE on different questions. The block bootstrap pairs blocks, not questions.
   - On matched questions, Sonnet's format effect survives: −0.119 [−0.203, −0.029] strict, −0.066 [−0.109, −0.017] A, +0.100 [+0.049, +0.133] B.
   - Sonnet's conversation − fresh does not survive matching: +0.011 [−0.115, +0.096] strict, +0.004 [−0.025, +0.030] A, −0.008 [−0.040, +0.030] B.
   - The strict matched cells are small: 9 (P) and 24 (F) questions. Under A they are 43 and 66, with the same result.
7. **Holds.** *Few items.* Sonnet's format effect over leave-one-block-out is −0.160 to −0.125, and over leave-one-question-out −0.155 to −0.133. Haiku's format effect over leave-one-block-out is −0.026 to +0.021. No block or question carries the result.
8. **Holds.** *Circularity.* Nothing is fitted.
9. **Hole.** *Baselines and controls.* The noise baseline (fresh r1 − r0) is a within-format difference on nearly the same questions. The format contrast is a cross-format difference on different subsets, so the baseline understates the noise in the format comparison. The fairer control is the matched-question contrast (B6), which the file does not report. There is also no coherent-reading scoring: under C, Sonnet's "far beyond noise" format effect is +0.037 against replicate noise of +0.016 [−0.017, +0.040].
10. **Holds, with a note.** *Uncertainty.* The block bootstrap is at the right level: blocks for conversations, which contain fresh questions too. A question-level bootstrap gives narrower intervals, so the block bootstrap is the conservative choice.
    - **Bin sensitivity**, Sonnet strict format contrast (1,000 block resamples): 5 bins −0.141 [−0.244, −0.060]; 10 bins −0.143; 15 bins −0.126 [−0.216, −0.046]; 20 bins −0.144 [−0.227, −0.056]; adaptive-10 −0.144 [−0.230, −0.059]; adaptive-15 −0.158 [−0.225, −0.051]; Brier −0.104 [−0.191, −0.024]; a single bin −0.202. Every one excludes 0, and on matched questions every variant also excludes 0 (−0.098 to −0.149).
    - **Bin sensitivity**, Haiku format: every variant spans 0.
    - **Bin sensitivity**, order: every variant spans 0 for both models.
    - **Mapping (item d).** All 1,147 Haiku and 1,088 Sonnet "Frequency:" values are bare integers 0–100. All "Probability:" values are decimals in [0, 1]. No "%" and no "Frequency: 0.9". The ÷100 mapping cannot move ECE.
11. **Hole.** *Multiple comparisons.* There are 4 primaries and 8 secondaries per bet, plus 16 exploratory contrasts. The file does not say its intervals are uncorrected. Sonnet's format CI survives Bonferroni over 4 ([−0.266, −0.045]) and over 12 ([−0.294, −0.035]). Sonnet's conversation − fresh does not survive over 12 ([−0.205, +0.003]). Haiku's conversation − fresh survives both ([−0.246, −0.051] over 12).
12. **Holds.** *Leakage.* Nothing is fitted.

**C. Does the write-up say only what the data say?**

13. **Holds.** *Scope.* The file names one protocol, two models and one pool. "Calibration depends on format" is the pre-registered label for Sonnet.
14. **Holds.** *Rank.* The exploratory part is labelled as exploratory throughout. Its readings do not replace the frozen ones.
15. **Hole.** *Mechanism.* Three statements present a mechanism as fact:
    - `:34` "changes *which quantity the model reports*";
    - `:45` "Part of the format effect is the format changing the question the model answers";
    - `:43` "the format alone".

    The referent switch is inferred from a proxy. The design cannot separate it from format-dependent exclusions.
16. **Hole.** *Plain English against the table.*
    - `:43` "for Sonnet … and the context": not on matched questions.
    - `:43` "for Haiku, on the context only": the sign flips between A and B.
    - `:43` "factor of 1.7 to 2.9": the ratio inverts under B and under C.
    - `:155` "conversation-against-fresh effect for both models … in every version": false for Sonnet when matched.
    - `:22–24`: the format dependence of the exclusions is given for Haiku's open-form guesses only. It is not given for Sonnet's max_tokens stops.
17. **Cannot check.** *Citations.* No network access, so I could not open Tian et al. 2023 (Table 6 wording, "(squared)") or Guo et al. 2017. The ECE formula in the code is the standard Guo et al. definition.
18. **Holds.** *Negative results.* Haiku's null and both order nulls are stated as plainly as the positives.

**D. Process**

19. **Holds.** *Budget.* The caps are enforced in `mm_common.BatchRunner` before each batch. Spend was $2.61 of $3; Sonnet's $2.49 is under its $2.60 cap.
20. **Holds.** *Refusals.* No `refusal-mm-cal-*` file exists, and the max_tokens stops were not retried.
21. **Holds.** *Scale direction.* There is one: 0 = the guess is certainly wrong, 1 = certainly right. Under the referent reading the model itself sometimes inverted it. That is the finding, not a design fault.
22. **Hole (minor).** *Replication.* The format dependence appears on Sonnet only. Haiku is null, and no second design was run. The file nowhere calls it "pass, unreplicated". The record's `:99` "calibration depends on format for Sonnet" reads as settled.

**Other process findings**
- The results file does not link its audits. Only 1 of 54 `results/*.md` does, against the "After the audit" rule.
- reproduce.py does not regenerate the exploratory tail (by design, `reproduce.py:73`). I ran `cal_format_explore.main()` on the snapshot and its JSON is identical.

## Required cuts

1. **`results/calibration-under-format.md:18`**
   - Current: "- **The same question asked inside a conversation rather than fresh changes ECE for both models:** −0.15 for Haiku and −0.11 for Sonnet, both intervals excluding 0."
   - Replace: "- **The same question asked inside a conversation rather than fresh changes ECE as scored:** −0.15 for Haiku and −0.11 for Sonnet, both intervals excluding 0. For Sonnet this comes from which questions survive parsing: on the questions parsed in both contexts it is +0.011 [−0.115, +0.096] (audit round 2)."
2. **`:23`**
   - Current: "- **Some answers were dropped.** Some answers worked the problem out and ran past the 300-token limit. In a conversation, the frozen rule ends the conversation there."
   - Append: "Sonnet did this more often in the probability format (46 against 20 fresh calls; 24 against 15 conversations), so its probability-format conversations lost 65–85 questions per order against 39–53."
3. **`:24`**
   - Current: "- **The result:** each cell rests on 68–199 of its 300 questions, not 300."
   - Replace: "- **The result:** each cell rests on 68–199 of its 300 questions, not 300, and which questions survive depends on the format. The pre-registered contrasts therefore compare ECE on different questions. On the questions parsed in both formats, Sonnet's format effect is −0.119 [−0.203, −0.029] and Haiku's +0.019 [−0.066, +0.105]."
4. **`:34`**
   - Current: "So changing the format, or putting the question in a conversation, changes *which quantity the model reports*, not only how much it reports."
   - Replace: "So changing the format, or putting the question in a conversation, changes how often the stated number fits only the proposed-answer reading. The simplest explanation is that it changes which quantity the model reports, not only how much."
5. **`:43`, first sentence**
   - Current: "**For Sonnet, a calibration number from this protocol depended on the format and the context; for Haiku, on the context only. The direction of Sonnet's format effect depends on how the number is read.**"
   - Replace: "**For Sonnet, a calibration number from this protocol depended on the format, in a direction that depends on how the number is read. Sonnet's conversation-versus-fresh difference disappears on questions parsed in both contexts. Haiku's survives that matching but reverses sign between the two readings.**"
6. **`:43`, second sentence**
   - Current: "For Sonnet, the format alone moves ECE by a factor of about 1.7 to 2.9 (exploratory scoring A; 2.0 to 2.9 in the pre-registered cells), far beyond run-to-run noise."
   - Replace: "Under the strict and intended scorings, Sonnet's probability-format ECE is 1.7 to 2.9 times its frequency-format ECE, on partly different questions. Under the proposed-answer scoring the ratio inverts (0.65 to 0.91). In each of the three scorings reported here, the format difference is larger than replicate noise."
7. **`:44`**
   - Current: "mean |Δ| 0.22 against 0.10 for Haiku, and 0.65 against 0.14 for Sonnet in the probability format."
   - Replace: "mean |Δ| 0.22 against 0.10 for Haiku, and 0.65 against 0.14 for Sonnet in the probability format. Sonnet's figure rests on the 22 questions parsed in both orders, 16 of which move by more than 0.5: the reading switches rather than the confidence shifting. In the frequency format Sonnet's is 0.10 against 0.08."
8. **`:45`**
   - Current: "- **Part of the format effect is the format changing the question the model answers.**"
   - Replace: "- **Part of the format effect may be the format changing the question the model answers.** This design cannot separate that from the format-dependent exclusions."
9. **After `:46`** (new bullet)
   - Add: "- **Multiple comparisons:** 4 primary tests (2 contrasts × 2 models) and 8 pre-registered secondaries; the intervals are uncorrected. Sonnet's format effect survives Bonferroni over the 12. Sonnet's conversation-versus-fresh effect does not."
10. **`:155`**
    - Current: "- **The format effect for Sonnet** and the **conversation-against-fresh effect for both models** are far larger than replicate noise in every version."
    - Replace: "- **The format effect for Sonnet** is larger than replicate noise in every version, including on the questions parsed in both formats. The **conversation-against-fresh effect** is too for Haiku. For Sonnet it vanishes on the questions parsed in both contexts (strict +0.011, A +0.004, B −0.008; audit round 2)."
11. **Top of `results/calibration-under-format.md`** (after `:3`)
    - Add: "Audited: `audits/calibration-under-format.md` (round 1), `audits/calibration-under-format-r2.md` (round 2)."
12. **`paper/record.md:66`, result cell**
    - Current: "Sonnet's ECE depends on format (−0.143 [−0.233, −0.066], replicate noise +0.005)"
    - Replace: "Sonnet's ECE depends on format (−0.143 [−0.233, −0.066], replicate noise +0.005; the sign depends on how the number is read, DM6a)"
13. **`paper/record.md:99`**
    - Current: "calibration depends on format for Sonnet (DM6)."
    - Replace: "Sonnet's ECE changes with format, unreplicated, with a sign that depends on how its number is read (DM6, DM6a)."
14. **`experiments/cal_format_explore.py:5`** (docstring)
    - Current: "About 120 of the 300 hard-pool questions are phrased "Is this claim true?""
    - Replace: "60 of the 300 hard-pool questions are phrased "Is the following claim true?""
    - The DM6 date also needs an erratum, appended under D51's no-edit rule: "DM6 (line 801): '08:35 MST, before any call' — the pre-registration commit `f406a9c` (07:53) precedes every call; 08:35 is after Haiku's run (07:55–08:18)."

## What would break it next

1. **Re-run Sonnet with an adapted protocol** (cost about $1.30 at the batch rate, Sonnet only, 1,200 fresh calls; conversations not needed):
   - answer: "yes"/"no" only;
   - number: "the probability that your yes/no answer is correct";
   - max_tokens 1,000, so no question is lost to a stop;
   - the same 300 questions and both formats.

   If the probability-versus-frequency ECE difference keeps the strict sign (frequency lower) once the referent ambiguity and the exclusions are removed, the pre-registered reading gains a direction. If it comes out near the coherent-scoring value (+0.02 to +0.04, probability better), the −0.143 was the template misfit.
2. **Free, now:** report the matched-question contrasts and a coherent-reading scoring (C: a "no" guess with p < 0.5 read as P(X)) beside A and B in `cal_format_explore.py`. Under C:
   - Sonnet's ECE is 0.03–0.09 in every cell and its format effect is +0.037 [+0.001, +0.070];
   - Haiku's context effect is +0.004 [−0.030, +0.037].

   The current exploratory section does not show this reading.

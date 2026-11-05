---
bet: em-dm6f2
program: entangled-mind
prereg_commit: 51cb1f4
reviewer_session: fresh design-review subagent, main checkout, 2026-11-05 (seed commit 6520400 and ledger commit bc9b77e also read)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 06:22 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: holds, D6: holds, D7: holds, D8: flaw, D9: holds, D10: flaw, D11: holds}
flaws: 3
pilot_usd: 0.00
verdict: fix-first
confirmed_at: 2026-11-05 06:30 America/Denver
---

# Design review of em-dm6f2

## In plain English
Yes, as built, this test would answer its question. The archive has 272 Sonnet questions with a number in all four fresh cells, so the pre-mortem's worry (too few matched questions) does not happen. The rule gives exactly one verdict for every table. In worlds built from em-dm6's published numbers, it passes about 60–75% of the time and fails the rest. Three things need fixing first, and none of them changes the test:
- **The pass sentence says more than the statistic.** The statistic averages the two same-format overlaps. In a plausible world that passes, two askings in the probability format often overlap no more than the two formats do (36% of draws), so "more different than asking the same format twice" would be false for that format. The sentence also calls the probability-format number "confidence", but em-dm6's audit found that number is often about the proposed answer, not the model's own guess.
- **Haiku's results entry carries the Sonnet verdict sentence.**
- **The archive-hash stop rule in §7 does nothing in the code.** The hashes are recorded but never compared with anything.

## Checks

Scratch scripts are in `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed/e93ce59f-1dc3-4451-8206-bee8c0537bfa/scratchpad/review-dm6f2/`. Each was run with `/Users/seanpharris/entangled-mind/.venv/bin/python`. None calls an API, and none reads or computes J_F, J_N or D on the real fresh cells. The code is unchanged since the pre-registration (`git diff 51cb1f4 HEAD -- programs/entangled-mind/experiments/dm6f2_flag_overlap.py` is empty). The archive files are clean against HEAD.

What I read in the real archive (allowed by the brief):
- **Structure.** Each file has 300 keys per fresh cell. The empty `turns` (max_tokens stops) are 23/23/13/7 for Sonnet P r0/P r1/F r0/F r1, so 46 P against 20 F, matching the em-dm6 round-2 audit. No fresh `conf` is null when turns exist.
- **Units.** Every non-null `conf` is a float in [0.01, 1.0]. I re-parsed all 1,134 Sonnet and 1,177 Haiku fresh numbers from `raw` (Probability as is, Frequency ÷ 100), with 0 mismatches.
- **Matched n.** Sonnet has **272** of 300 questions with a number in all four fresh cells; Haiku has 287. Three Sonnet values in the matched cells are exactly 0.70.
- **Categories.** All 300 fresh ids are in `pool-run-3.json`, falling into 4 categories: simpleqa 120, claim 60, science-chemistry 60, science-physics 60.
- **Batches.** All four fresh cells are in one batch, `msgbatch_01BXESYAjpt8FPr5EbLsf3Vc`.
- **For world-building only:** the Sonnet *conversation* cells, which this bet does not read (seq|F, 508 values), and em-dm6's published tables.

**D1. The rule can be applied by a stranger: holds.** `--selftest` prints `SELFTEST OK`:
- identical formats → fail;
- level shift → pass (J_F 0.31, J_N 0.80, D +0.49);
- equal noise only → fail;
- 30 questions → untestable;
- the boundary asserts pass: conf 0.70 is not flagged; J_F = 0.70 fails; J_F upper bound = 0.70 fails; D = 0.10 passes, 0.0999 fails; D lower bound = 0 fails.

`verdict()` checks n < 40 first, then one conjunction, so every table gets exactly one label. §5 and the code agree term for term, including the 1e-9 tolerance (`dm6f2_flag_overlap.py:21–25, 81–86`).

**D2. Every manipulation takes effect: holds.** `d2_fake.py` builds a fake archive in the scratch folder:
- the planted flags are P = q1–40 and F = q31–70;
- one question has `turns: []`, one has `conf: null`, one has F conf exactly 0.70;
- a `seq|` cell is planted to be ignored.

`load()` keeps 118 of 120 questions and drops the two broken ones. The columns map to (P,0), (P,1), (F,0), (F,1). The 0.70 value is not flagged. `stats` returns J_F = 10/68 = 0.147 and J_N = 1.000, as planted. The threshold knob moves the flag counts: 0 at 0.1, 38/38/40/40 at 0.5, all 118 at 0.95. `main()` then ran end to end on the fake files and wrote JSON and md. The seed in use, 3958117464482761837, is below 2^63, so `% 2**63` leaves it unchanged; the cluster bootstrap uses seed + 1, as §2 says.

**D3. Every control can fail: holds** (with a note that feeds F1). The noise baseline must reject repeat noise with no format effect.
- Equal noise in all four cells: the selftest's "noise only" world fails.
- In `d11_sweep.py` at s = 0, with noise set to em-dm6's published fresh replicate |Δconf| (P 0.138, F 0.077 → redraw rates 0.25 and 0.10): **0 of 200 pass**.

The J_F < 0.70 leg alone does not reject noise: J_F is 0.59 in that no-effect world. It is the D leg that rejects it. The design needs both legs, and has both.

The control is weaker against *format-specific* noise, meaning P noisier than F with no systematic shift (`d3_dmin.py`, 100 draws each):

| P noise | F noise | pass rate |
|---|---|---|
| published (0.25) | published (0.10) | 0.00 |
| 0.4 | 0.1 | 0.08 |
| 0.6 | 0 | 1.00 |
| 1.0 | 0 | 1.00 |

The reason is that Jaccard is not linear: the mean of a high J_FF and a low J_PP sits above the cross-format overlap. With the selftest's own generator (P sd 0.3, F sd 0.03, no shift), D = +0.08 [+0.022, +0.141] with no format effect at all.

At the measured noise ratio (about 1.8×), the verdict rule rejects this. So the rule holds. I tried the tighter baseline min(J_PP, J_FF) − J_F: it cuts P(pass) at the plausible effect from 0.76 to 0.05, so it is not a usable fix. The sentence and the reporting still need to carry it (F1).

**D4. Rivals are matched: holds.** Two rivals are named:
- **Repeat noise** is answered by the same-format baseline; see D3 for format-specific noise.
- **Format-dependent exclusions** are answered by matching every overlap on the same 272 questions (P8). With the exclusions handled this way, the matched set loses only 28 questions, not the 80–155 parse exclusions of em-dm6. Those were guess-parse exclusions, and `conf` parses even for open-form guesses ("Guess: 43 ft / Probability: 0.95").

No family is fitted, so nothing can win by construction.

**D5. A dumb baseline is beaten: holds.**
- The dumbest passing predictors are "independent random flag sets at the observed rates" and "noise only". Both make J_F < 0.70 easy, and both are rejected by the D ≥ 0.10 leg (D3).
- A pure level shift that keeps the ranking, with F's set nested in P's, passes. That is a real effect for an overseer, but the sentence must not imply "other answers" (F1).
- This is not a null rule, so it needs no equivalence margin or MDE. Its sensitivity: P(pass) 0.32 at a 5% P-only shift and 0.88 at 10% (published noise).

**D6. Execution risks: holds (not applicable).** There are no calls, and the pre-mortem is of kind `design`.

**D7. Comparisons match: holds.** P and F fresh cells match on:
- the same model and the same batch;
- the same `max_tokens=300` (`cal_format.py:106`);
- single-turn position;
- the same questions, after matching.

The two templates differ in the format clause. F adds the reference-class wording "out of 100 questions like this one on each of which you have the same evidence" (`cal_format.py:26–35`). §0 and §1 name the factor as "the two formats", which is this bundle of wording, so the claim is about the bundle.

The flagged unit is the question; the guess itself may differ between formats. The F1 sentence says "questions" for that reason.

**D8. The verdict sentences are written: flaw (F1, F2).** The sentences exist, but three of their nouns are not ones the design can carry:
- **"more different than asking the same format twice".** The statistic averages J_PP and J_FF, and the code reports only that mean (`stats`, `:56–60`). In the plausible pass world (5–10% P-only shift, published noise), J_PP ≈ 0.53 against J_F ≈ 0.50. J_F ≥ min(J_PP, J_FF) in **36%** of draws (`d8_guard.py`). A pass would then be reported with a sentence that is false for the probability format.
- **"gives with less than 70% confidence".** The em-dm6 audits found that in fresh P, Sonnet's number is below one half on 50% of its "no" guesses. That pattern fits P(proposed answer), not confidence in the guess. The design measures a *stated number*.
- **"a substantially different set of answers".** A nested level shift also passes (D5), and §6 itself says the design cannot tell "more" from "other".

Separately (F2), `analyse()` attaches `SENTENCES[verdict]` to every model. Haiku's JSON entry therefore carries a sentence about Sonnet: in the fake-archive run, Haiku's `sentence` reads "An overseer who double-checks every answer Sonnet gives…".

**D9. One item cannot decide it: holds.**
- **Leave-one-question-out** is pre-registered with the interval bounds held (`:111–119`), and §5 says a flip is named with its id in the plain-English section.
- **The category-cluster bootstrap (P14)** is pre-registered, and the bar is read on the question bootstrap. It has only 4 clusters (35 distinct resamples), and when the effect is spread evenly its D interval is *narrower* than the question bootstrap's (0.112 against 0.135, `p14_cluster.py`). So it cannot flag fragility in that case.

The cluster check still catches concentration. With the effect placed in one 55-question category, it disagrees on 53–60% of passes; leave-one-category-out flags 100% (`p14_conc.py`). It is reported only, and it can fail, so this holds.

Recommended, not required: report leave-one-category-out beside it, and the generated md should print the LOO flip ids, not only their count.

**D10. Machinery: flaw (F3).**
- **Budget:** $0, and the code makes no network or API calls.
- **Refusal stop:** not applicable.
- **Scale:** one direction (0 = certainly wrong).
- **Caching:** not applicable.
- **Seed:** recomputes. `ledger/seed.py <randomness> em-dm6f2 --purpose bootstrap` gives 3958117464482761837, matching §2. The live/stalled choice follows the 24-hour rule (CURBY-Q round 28297, 2025-08-22). The pulse order is as recorded: previous pulse 13:06:00.158Z, before the commit's 13:06:43Z. I did not refetch the beacon.
- **Lesson:** `ledger/check_prereg.py em-dm6f2 … --before-run` gives L1, L2, L3 and H1 ok (R1 fails only because this file did not exist yet).
- **Flaw:** §7 says "If the archive files' sha256 differ from those recorded at the run, the run stops." The code computes the hashes and writes them out (`:196–198`) but compares them with nothing. The fake archive, with different hashes, ran to a verdict. The stop rule cannot fire.
- **Minor:** DEVIATIONS D61 still says "06:15", the guessed time the seed commit corrected in the pre-registration but not in the log.

**D11. The bet can both pass and fail: holds.** `d11_sim.py` and `d11_sweep.py` build each world from measured numbers (P15):
- **Base values:** Sonnet's conversation-cell F confidences (508 values; this bet does not read them).
- **Replicate noise:** em-dm6's published fresh |Δconf| (P 0.138, F 0.077).
- **Format effect:** a persistent referent switch on a share s of questions in P only. Published: 50% of fresh-P "no" guesses are below one half, against 14–19% in F, and "no" guesses are 20–30% of turns. That gives s ≈ 0.33 × 0.25 ≈ 0.08.
- **n:** the real matched 272 questions.
- **Draws:** 200 per world.

| world | P(pass) | P(fail) |
|---|---|---|
| no format effect (s = 0) | 0.00 | 1.00 |
| s = 0.05 | 0.32 | 0.68 |
| plausible s = 0.08 | **0.73** | **0.27** |
| s = 0.10 | 0.88 | 0.12 |
| s = 0.15 | 0.99 | 0.01 |

With equal noise in both formats, the plausible s = 0.08 world gives P(pass) 0.60. A referent-flip family fitted to both published noise levels (`d5_flip.py`) gives P(pass) between 0.03 and 0.87, depending on whether the reading is fixed per question or drawn per call.

Both outcomes stay above 10% under the plausible worlds. The engine's 55% sits inside this range. One part of the odds reasoning no longer holds: the pull-down from "exclusions shrink the matched set" does not apply, since 272 questions match. The author may revise the odds before data, keeping both numbers. The review does not set them.

## Required fixes

Each fix needs one dated DEVIATIONS row, written before any data and naming this review (proposed **D62 — em-dm6f2 design-review fixes**). The row also carries an erratum for D61's "06:15" (the commit author time is 06:06:43). No fix lowers the bar: the rule, thresholds, n floor and seed are unchanged.

**F1 (D8): the verdict sentences carry only what the statistic measures, and the two same-format overlaps are reported separately.**
- In `stats()`/`analyse()`, compute and report `J_PP` = J(P0,P1) and `J_FF` = J(F0,F1), each with its question-bootstrap 95% interval. Add `noise_asymmetric` = J_F ≥ min(J_PP, J_FF) − 1e-9 on the point estimates. Add J_PP, J_FF and the flag to the md table.
- Replace the pass sentence (§5 and `SENTENCES["pass"]`) with:
  "An overseer who double-checks every answer for which Sonnet stated a number below 70% would have checked a substantially different set of questions depending on which of the two formats the number was asked in: on average over the two formats, the lists from different formats overlapped less than the lists from two askings in the same format, by at least the pre-registered margin. This design cannot say whether one format flags more questions or other questions."
- When `noise_asymmetric` is true, append:
  "In the <probability|frequency> format, two askings overlapped no more than the two formats did (J <J_PP or J_FF> against J_F <J_F>), so for that format the difference between formats is no larger than its own repeat noise."
  Name the format whose same-format overlap is the lower one.
- Replace the fail sentence with:
  "On this archive, the lists of Sonnet's answers with a stated number below 70% were not shown to differ by format more than they differ between two askings in the same format, by the pre-registered margin."
- Leave the untestable sentence unchanged.
- In `--selftest`, add an "asymmetric noise" world: P replicates `base + noise(.3)`, F replicates `base + noise(.03)`, no shift. Print J_PP, J_FF, D and the verdict, and assert `noise_asymmetric` is True. With the selftest's generator I get J_F 0.59, J_PP 0.45 and J_FF 0.90.

**F2 (D8): only Sonnet gets a verdict sentence.**
- In `main()`, after `analyse()` for `m == "haiku"`, remove `sentence` from that entry, or set it to null with a note "secondary; no verdict sentence".
- The md already prints only Sonnet's sentence; keep it that way.

**F3 (D10): the §7 archive-hash stop rule is implemented.**
- Add to the code a constant with the expected sha256 of the three files, as committed and clean at HEAD `bc9b77e`:
  - `cal-sonnet-conversations.json` `76e2e55ccf91f52b526f50e3e1875a35fc851e92b74a6287a0233a73e333302a`
  - `cal-haiku-conversations.json` `74fa812436705ea397605ae6788b788c7aa3471ae9ba4fe52e6a96a979309b22`
  - `pool-run-3.json` `8011ae79b4c12c6ac9b95dd751b68c891aeb3c7c47a5d5afb2d7c465b4db2b56`
- In `main()`, compare the computed hashes with these before `load()`. On any mismatch, `raise SystemExit` with the file name and both hashes, and write no results.
- Reword §7 through the DEVIATIONS row: "If any archive file's sha256 differs from the value pinned in the code (from the committed files at bc9b77e), the run stops before any analysis and the mismatch is reported."

Not required (recommendations):
- leave-one-category-out reported beside the 4-cluster bootstrap;
- the LOO flip ids printed in the generated md;
- the rate-matched secondary breaks ties among equal F values by question-id order (`argsort(kind="stable")`). With values on a 0.01 grid this choice can move `J_F_rate_matched`. Report the tie count or average over random tie orders. It is secondary and cannot change the verdict.

VERDICT: fix-first (3)

## Addendum: fixes confirmed (2026-11-05 06:30 America/Denver)

I checked the fixes against `7f5d3f4` (code and DEVIATIONS D63) and `dafca10` (D63's own time corrected to 06:24). The fix row is D63, not D62, because D62 went to another bet. Since the pre-registration, the only change to `dm6f2_flag_overlap.py` is D63's. The frozen `.md` is untouched apart from the seed commit, and D63 carries the new §5 sentences and the new §7 text. The rule, thresholds, n floor and seed are unchanged.

- **F1 holds.**
  - `same_format()` returns J_PP and J_FF. `analyse()` reports both with question-bootstrap intervals, plus `noise_asymmetric` (J_F ≥ min(J_PP, J_FF) − 1e-9) and the noisier format. The md table shows all of them.
  - The pass and fail sentences match the review's wording word for word.
  - The extra clause is appended only on a pass with the flag set, and it names the lower same-format overlap. On a flagged pass (P sd 0.3, F sd 0.03, n = 272) it reads: "In the probability format, two askings overlapped no more than the two formats did (J 0.488 against J_F 0.585), …".
  - `--selftest` prints `SELFTEST OK`. Its new asymmetric-noise world gives J_PP 0.49, J_FF 0.97, D +0.12 and a pass with the flag True. The original three worlds, the untestable case and every boundary assert still give their old results.
  - Note: the same-format intervals use a third generator stream (seed + 2), which neither §2 nor D63 states. It feeds only reported intervals and cannot touch the verdict.
- **F2 holds.** On the fake archive, Haiku's entry has `sentence: null` with the note "secondary; no verdict sentence (D63, design review F2)". The md prints only Sonnet's sentence.
- **F3 holds.**
  - `PINNED_SHA256` matches the three real files: I hashed them, which is not an analysis.
  - With the fake archive, `main()` stops with "archive sha256 mismatch, run stopped before analysis: …", naming each file with both hashes. It writes no results file.
  - With the pins set to the fake files' hashes, it runs to completion.
- **Recommendation taken:** the leave-one-question-out flip ids are now printed. The two that were not taken are secondary and were not required.
- **Erratum:** D61's "06:15" is corrected inside D63 (pre-registration author time 06:06:43).

No paid calls, $0. The primary analysis was not run on the real data.

CONFIRMED: yes

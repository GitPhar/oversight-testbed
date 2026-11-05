---
bet: multi-model (DM2–DM5: tests F, P and T replicated on Sonnet and Opus), round 2
program: entangled-mind
prereg_commit: 86e7c56 (DM1–DM2), 207c9b6 (DM3), dea966b (DM4), a9e1e7b (DM4a), e65a384 (DM2a)
results_commit: a863d66 (summary), as amended by 5480c49 (D51 cut pass); audited at 9042d7f
auditor_session: audit2 worktree, multi-model second-round sub-audit
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5 (every DM commit carries "Co-Authored-By: Claude Opus 5.5")
same_model_family: true
date: 2026-11-04 15:01 America/Denver
claims_checked: 54
holes_found: 16
overclaims_cut: 18
reproduced: true            # every mm-* table regenerates from the archive with the authors' code (network blocked); multi-model.md itself is hand-written and skipped by reproduce.py; its Opus six-format row regenerates only from a filtered cache (hole 5)
verdict_claimed: mixed      # DM5: P no self-advantage; T Sonnet question-driven, Opus leaning; F Sonnet mixed, Opus mixed (26 claims)
verdict_after_audit: mixed
verdict_stands: true
canary: unknown
false_alarms: 0
failed: true
failure_reason: Opus cost twice the pilot's estimate because its thinking cannot be turned off, so both Opus arms ran short (26 of 80 claims; 2 conversations per cell) and decided nothing.
failure_kind: design
premortem_score: null       # no pre-mortem in the DM2–DM4 pre-registrations (frozen 07:44–07:48, before operators/premortem.md existed)
risk_seen: null
---

# Audit of multi-model (round 2): do the paper's three findings hold on Sonnet and Opus?

Scope: `results/multi-model.md` at `9042d7f`, with the round-1 cuts from `audits/multi-model.md`, `audits/mm-gm1-self-knowledge.md`, `audits/mm-gm2-self-conditioning.md` and `audits/mm-gm3b-format-invariance.md` checked where they target `results/multi-model.md`, `results/mm-*.md`, README or paper text about the replications. The Opus six-format completion (D49, D49a, D50) is out of scope. Where this file quotes D49, I checked only that the quote matches `results/mm-gm3b-opus-completion.md`.

## In plain English

- **The numbers are right.** Every number in the summary reproduces from the archives, including the self-knowledge interaction, the transcript gates and ratios, and Sonnet's six-format ΔLL and F′ Q. So does the spend. All 25 round-1 cuts were applied (10 as written, 13 adapted, 2 made obsolete by D50), and none was applied wrongly.
- **Leave-one-item-out shows the transcript readings are thinner than the summary says.**
  - Sonnet's *question-driven* label is one item away from *untestable*: without h058 the shown-order gate is p = 0.11.
  - Opus's shown order effect (gate p = 0.004) comes from two items: without h238 the gate is p = 0.10.
  - Opus's *leaning question-driven* label becomes *self-anchoring* without h058. Round 1 found this, and the summary still does not say it.
- **The six-format table has gone stale.** It quotes Opus's 26-claim DM2 row from a results file that, since D49, shows 68 claims. Its "discordant pairs" column is the mislabelled (1 − τ_b)/2 index that D51 corrected everywhere else.
- **Smaller factual errors.**
  - "All calls went through the Batches API" (the pilot made 12 synchronous calls).
  - The pilot item is called a "non-test item" (h002 is one of DM3's 298 test questions).
  - "Thinking off per model" does not describe DM3, where Opus answered with adaptive thinking.
  - "Scaled down without changing its structure" (DM3 dropped two arms).
- **The verdicts stand,** but the plain-English section should carry these concentrations and corrections.

## The case that this result is false

The headline is that two of the paper's three findings, the absence of a self-advantage and reliance on the model's own record, "hold on all three" models, while the third, no format-free credence, weakens with model strength. The strongest case against it:

- **The self-knowledge test cannot fail in the direction it reports.** The pre-registered *self-advantage* reading needs the disagreement-subset CI above 0. That subset has 21 questions and 4 Opus errors, so its CI spans 1.1 AUROC units and could not have cleared 0. "No self-advantage" is the rule's fall-through. The informative all-298 bound (+0.017) is the statistic the pre-registration itself calls confounded with judge skill × author difficulty.
- **The transcript test rests on a handful of items.** On Sonnet the effect that survives redaction is two items (h191, h112). In both, a hidden record makes the model jump to the opposite end of the scale (redacted means 70–91 against 2–7 shown), which looks like a reaction to the "[rating recorded]" placeholder. The pre-registration says it cannot separate that. Sonnet's gate is p = 0.031, and Opus's arm has 2 conversations per cell.
- **Memory is not the only reading of the agreement drop.** Agreement can fall under redaction because of the placeholder, not because the model used its memory. On Sonnet the planted-value pull (b_MF) has an interval that includes 0, and Opus's final rating moves *away* from planted values.
- **On the format test, the "weakening" is carried by secondary and exploratory statistics** (F′ and W). The primary is *mixed* on both stronger models, and on Sonnet it is one claim (h058 c8, ΔLL −308) away from the Haiku-like *no single credence*.

So the case is this: one finding is a power-limited non-detection; one is a contrast with a confound the design names; and the cross-model trend rests on statistics that are not the pre-registered test.

The checklist below shows how much of this case holds:
- **Holds:** the one-item fragility (now worse than round 1 found) and the placeholder confound.
- **Does not hold:** "no difference in memory reliance". The agreement drop excludes 0 on all three models, and Opus's lead over Sonnet without the record survives a paired item bootstrap.

## Round-1 cuts: status in the current tree

Checked with `git diff b009a15 HEAD -- results/multi-model.md paper/no-credence-to-read.md paper/morning-brief.md` and `git show 5480c49`.

| # | source audit | target (round-1 line → now) | status | note |
|---|---|---|---|---|
| 1 | multi-model | results/multi-model.md:8 "same design" | applied as written | |
| 2 | multi-model | :12 "Self-report is still not privileged … travels best" | applied as written | the 4-error power caveat is still absent here (hole 12) |
| 3 | multi-model | :21 "Opus barely shows an order effect" | applied as written | the new sentence omits that the shown effect is two items deep (hole 2) |
| 4 | multi-model | :29 "weakens sharply" | adapted to D49 | the round-1 replacement and its adaptation put F′ (a secondary) first (hole 13) |
| 5 | multi-model | :33 Opus "does as well as" | applied as written (tense changed) | |
| 6 | multi-model | :34 "the stronger the model … one belief" → :35 | adapted (68-claim W, F′ figures) | the following Smolin & Wilder sentence was not targeted and remains (hole 7) |
| 7 | multi-model | :40 "points the other way" → :41 | adapted to D49/D50 | quotes match the completion file |
| 8 | mm-gm1 | paper/no-credence-to-read.md:27 | applied as written | |
| 9 | mm-gm1 | paper:311 → :312 | applied as written | |
| 10 | mm-gm1 | paper:379 → :387 | applied as written | |
| 11 | mm-gm1 | paper:386 "text-reading" → :394 | adapted (composed with sweep) | |
| 12 | mm-gm1 | morning-brief:112 → :111 | applied as written | |
| 13 | mm-gm2 | paper:30 → :33 | applied as written | |
| 14 | mm-gm2 | morning-brief:118 → :117 | applied as written | |
| 15 | mm-gm3b | paper:29 "fits as well as" | obsolete (rewritten by D50) | |
| 16 | mm-gm3b | paper:58 "does not hold on Opus" → :61 | adapted ("contradicted", D50) | D50's wording is out of scope |
| 17 | mm-gm3b | paper:325 "fits as well as" → :331 | adapted | |
| 18 | mm-gm3b | paper:325 "points the other way" | obsolete (D50 rewrote it) | |
| 19 | mm-gm3b | paper:326 "the stronger the model …" → :334 | adapted (68-claim W) | |
| 20 | mm-gm3b | paper:350 → §5.1 | adapted | |
| 21 | mm-gm3b | paper:407 → :415 | adapted ("contradicted") | |
| 22 | mm-gm3b | morning-brief:25 | adapted | |
| 23 | mm-gm3b | morning-brief:117 → :116 | adapted | |
| 24 | mm-gm3b | morning-brief:145 → :147 | adapted | |
| 25 | mm-gm3b | morning-brief:147 → :149 | adapted | |

Totals: **25 cuts; 10 applied as written, 13 adapted, 2 obsolete, 0 not applied, 0 applied wrongly.**

Round-1 holes that carried no listed cut, and were not acted on:
- Opus's label flips without h058 (round-1 multi-model hole 3);
- "without changing its structure" (round-1 claim 17);
- the DM "Date" fields that post-date their own commits (round-1 hole 5). D51's list of corrections to earlier DEVIATIONS entries does not include them.

## Claims checked

Recomputation scripts are in the session scratchpad, `mm/`:
- `dm3.py`: own AUROC, 4,000-resample bootstrap, own FINAL ANSWER parse;
- `dm4.py`: own variance components, permutation gate, item bootstrap and leave-one-item-out on gate and R;
- `dm4_pair.py`;
- `fprime_lf.py`: link-free F′ check, plus re-bootstrap and leave-one-item-out of the per-claim ΔLL;
- `wties.py`: W under tie handling;
- `opus26.py`: the authors' DM2 analysis on the 26 first-arm claims;
- `repro_mm.py`: the mm steps of `reproduce.py`, with the socket and `llm.client` blocked.

| # | claim (results/multi-model.md:line) | check run | outcome |
|---|---|---|---|
| 1 | :8 prompts, code and criteria of the original, reduced scale, pre-registered before first call | message-ID decode: DM2 07:44:03 < 07:45:58; DM3 07:47:58 < 07:49:06; DM4 07:48:27 < 07:50:47; Opus T 08:26:43 after cap file | holds |
| 2 | :8 "No call was refused." | no `refused` record or refusal file in any mm archive | holds |
| 3 | :12 no self-advantage detected on the pair | rule recomputed | holds |
| 4 | :14 OS 0.96 vs SS 0.90 | 0.959 / 0.903; Δ_S −0.056 [−0.091, −0.024] | holds |
| 5 | :15 Δ_O +0.011 [−0.056, +0.072] | +0.011 [−0.054, +0.070] | holds |
| 6 | :16 I −0.045 [−0.107, +0.017]; Haiku×Sonnet −0.055 excluded 0 | −0.0454 [−0.114, +0.017]; leave-one-question-out shifts −0.009 to +0.017; reference −0.055 [−0.103, −0.007] | holds |
| 7 | :17 pre-registered reading *no self-advantage* | correct by the frozen rule, but a fall-through: disagreement subset 17 Sonnet / **4 Opus** errors, not stated in this file | hole (omission) |
| 8 | :74 subset (21) +0.184 [−0.296, +0.812] | +0.184 [−0.307, +0.800]; 48 of 4,000 resamples undefined; leave-one-question-out −0.06 to +0.33 | holds |
| 9 | :19 "The question alone still changes the judgment on Sonnet …" | placeholder confound (redacted h191 6/72/91/8, h112 70/6/4/8 vs shown 2–7); gate fails without h058 | hole |
| 10 | :20 Sonnet R 2.95 [0.99, 12.55], 2 of 10 items, h191 | R 2.95 [0.94, 13.56] (my seed); h191 42.4, h112 30.0; **drop h058: gate p 0.111 → untestable**; drop h112 / h191: CI lower 0.70, still question-driven | hole (new) |
| 11 | :21 Opus 4.4 [0.8, 6.9], gate p 0.004; redacted from h058 | OE 4.44, p 0.006 (my permutations); shown OE per item: h279 10.0, h238 9.5, others ≤ 2.5; **drop h238: p 0.103 → untestable**; drop h279: p 0.020 | hole (new; sentence introduced by round-1 cut) |
| 12 | :22 Opus R 0.93 [0.06, 7.3], *leaning* | 0.93 [0.00, 7.32]; **drop h058: 0.14 [0.00, 0.46] → self-anchoring** | hole (round-1 finding not applied) |
| 13 | :25–26 78 / 88 / 95% → 25 / 35 / 65% | 31/40 → 10/40; 35/40 → 14/40; 19/20 → 13/20 | holds |
| 14 | :27 "Opus is the most stable without it" | paired item bootstrap of redacted agreement: Opus − Sonnet +0.30 [+0.03, +0.60]; Opus − Haiku +0.40 [+0.08, +0.70] | holds (narrowly) |
| 15 | :29 heading, F′ first; primary "undecided" on both | F′ is DM2's pre-registered *secondary*. Sonnet's primary is *mixed* by one claim: without h058 c8, +13.24 [+9.84, +16.91] → *no single credence* | hole (rank drift; minor) |
| 16 | :30 Haiku clearly fails on the same 80 | +19.42 [+15.40, +23.21] (authors' code reproduces) | holds |
| 17 | :31 Sonnet 92%, one statement drags the CI across 0, *mixed* | 92.5%; CI [−1.37, +16.30] (item bootstrap of archived per-claim ΔLL); only dropping h058 changes the label (+13.60 [+10.27, +17.73]) | holds |
| 18 | :32 F′ Q 0.69 [0.53, 0.82] *partial*; Haiku 0.29 | authors' code reproduces 0.687 [0.530, 0.825]. Link-free cross-validated linear check: Sonnet 0.69, Haiku 0.23, Opus (68) 0.93 | holds |
| 19 | :33 Opus 26: +0.42 [−1.83, +2.69] *mixed*; W 0.86 / 0.71 / 0.54 | authors' code on the 26 first-arm claims: +0.419 [−1.831, +2.695], 15/26 positive, W 0.857 | holds (but see 44, 52) |
| 20 | :34 D49: 68 of 80, ΔLL +1.90 [−0.82, +4.65] *mixed*, Q 0.94 [0.90, 0.97] | matches `results/mm-gm3b-opus-completion.md` | holds (quote) |
| 21 | :35 item-matched W 0.56 / 0.76 / 0.87; F′ 0.29 / 0.69 / 0.94 | matches `mm-gm3b-W-on-68-exploratory.json`. Argsort ranks; tie-corrected W is 0.55 / 0.78 / 0.91, so the order is unchanged | holds |
| 22 | :35 "That matches Smolin & Wilder's (2026) finding for other capable models." | S&W figures are second-hand (`experiments/gm3b-format-invariance.md:17`); framings, items and statistic differ (`audits/gm3c-heldout-format.md` hole 2) | cannot check → hole (citation) |
| 23 | :38 no self-advantage detected on any of the three | D36 + DM3 | holds |
| 24 | :39 record conditions later answers, on all three | drop in agreement, item bootstrap: Haiku [0.33, 0.75], Sonnet [0.35, 0.71], Opus [0.08, 0.50]. The rule is on the point (30 pp > 10); Opus's lower bound is under the 10-pp line | holds (minor) |
| 25 | :40 question alone holds on Sonnet | see 9–10 | hole |
| 26 | :41 Haiku, partly Sonnet; Opus undecided on 26 and 68; "contradicted" by D49's F′ rule (D50) | wording matches the completion file and D50; D49 itself not audited | holds (quote) |
| 27 | :45 "All calls went through the Message Batches API" | :49 itself lists 12 synchronous pilot calls (`req_` IDs in `mm-pilot-calls.json`) | hole |
| 28 | :45 full designs ≈ $65 at list | preregs give DM2 $7.7 + $15 and DM4 $11 + $26 ($59.7); DM3's full cost is not stated | cannot check |
| 29 | :45 "scaled down without changing its structure (DM1)" | DM3 dropped the paraphrase and recognition arms (:52); F′ runs on 3 folds, not 5; Opus T at R = 2 | hole (round 1, not cut) |
| 30 | :49 pilot "on a non-test item" | DM1: h002 "is one of direction 1's 298 questions", i.e. a DM3 test question | hole |
| 31 | :50–55 spend, $16.28 total, $3.72 unspent | 0.0301 + 2.0446 + 3.0994 + 4.0299 + 2.189 + 4.889 = 16.282; cap 20 − 11.393 − 0.10 = 8.5069 | holds |
| 32 | :58 ≈ 120 thinking tokens; pilot had none; cost doubled | pilot Opus single-turn outputs 9–11 tokens; DM2 $0.00194 per call vs $0.0009 estimate | holds |
| 33 | :59 cap re-set before any transcript call | `a9e1e7b` 07:49:52 < first DM4 call 07:50:47 | holds |
| 34 | :60 12% per turn, $8.74 at R = 3 | 1.12 is in `dea966b` text and code; my reconstruction from wave-1 costs gives $8.68 (the print is not archived) | holds (approx.) |
| 35 | :61 R = 3 would have fitted; why $3.72 is unspent | ≈ $6.5 at R = 3; 8.51 − 4.89 + 0.10 = 3.72 | holds |
| 36 | :67 accuracy 89.9% (30) / 94.3% (17) | own regex parse of Opus FINAL ANSWER lines | holds |
| 37 | :71–75 cell table | 0.903 / 0.959 / 0.904 / 0.893; subset 0.551 / 0.522 / 0.684 / 0.529 | holds |
| 38 | :78–79 Δ_S, Δ_O | see 4–5 | holds |
| 39 | :85–89 transcript primary table | my gates 0.0006 / 0.031 / 0.006; R as 10–12; the authors' code regenerates the committed table byte for byte | holds |
| 40 | :91–95 b_MF, pull, MF agreement | regenerated by the authors' code (match) | holds (not independently recomputed) |
| 41 | :98 concentration notes | Sonnet h191 42.4, h112 30.0, rest 0–16.5; Haiku h191 43.1; Opus h058 12.9 | holds |
| 42 | :99 memory reading on all three | see 24 | holds |
| 43 | :100 Opus final M −10.0 [−17.1, −3.1] | regenerated (match) | holds |
| 44 | :104–108 six-format table, sourced to `results/mm-gm3b-format-invariance.md` (:102) | Haiku and Sonnet rows match. **The Opus row (26 (7), +0.42, 58%, W 0.86, 3–14%) is no longer in the cited file**, which since `a8be4b5` reads 68 (17), +1.90, 74%, W 0.87, 6–14% | hole (new) |
| 45 | :104 "discordant pairs vs 0–100" 25–35% / 14–20% / 3–14% | `gm3b_format_invariance.py:272` computes (1 − τ_b)/2, not a share of pairs. D51 relabelled it in gm3b and the paper, but not here or in `mm_gm3b.py`'s writer | hole (miscount carried) |
| 46 | :111–113 exploratory note | −308.3, −89.6, −77.1; median 10.96; Opus's 7 items are candidates 1–7 (Haiku-wrong) | holds |
| 47 | :118 "Thinking is 'off' per model" | DM3 §3: Opus authored with adaptive thinking at default effort; judges ran with no thinking parameter (`mm_gm1.py:49, :71`) | hole |
| 48 | :119 Batches API, message IDs | pilot sync calls have `req_` IDs | hole (same as 27; counted once) |
| 49 | :121–123 scaled designs | holds; Opus R = 2 is given in the table | holds |
| 50 | :124 DM2a in quarters, $2.04 | batches 1,600, 1,600, then 4 × 400; $2.0446 | holds |
| 51 | :125 DM4a | holds; omits the complete-claims analysis restriction committed in `f406a9c` after Opus data existed | holds (minor omission) |
| 52 | :140 the three `analyse` commands "rebuild every table" | `mm_gm3b.py analyse` now gives the 68-claim Opus row; the 26-claim row needs the cache filtered to `mm-gm3b-opus-first26.json`'s claims | hole (new) |
| 53 | process: the results file links its audit (auditor.md, "After the audit") | `grep audits/ results/multi-model.md results/mm-*.md`: 0 | hole (process) |
| 54 | DEVIATIONS DM1–DM4a, DM2a "Date" fields | 6–51 min after their own commits (round-1 hole 5); not corrected in D51's "corrections to earlier entries" | hole (not applied) |

Holes are counted once each: 7, 9/25 (one hole), 10, 11, 12, 15, 22, 27/48 (one), 29, 30, 44, 45, 47, 52, 53, 54. That is 16, plus one outside the results file (`paper/record.md:64`; see cut 16), which is listed but not counted.

## Checklist

**A. Pre-registration**
1. **Holds.** Author dates against the first decoded message ID, per test (claim 1). The pilot (07:33–07:36) predates DM1's commit (07:44:03) as DM1 discloses. Opus's DM4 calls start at 08:26:43, after every other DM run, as DM4a requires.
2. **Holds, with documentation holes.**
   - Statistics, seeds, splits and rules match the pre-registration commits. DM2 §2 freezes D38's analysis and reading. DM3 §2 freezes D36's rule, which `mm_gm1.py:114–119` implements as point I > 0 and subset CI lower > 0. DM4 §2 freezes D37's gate, R, the 0.5 lines and the 1.12 growth.
   - The DEVIATIONS "Date" fields are wrong (claim 54).
   - DM4a's analysis restriction landed in `f406a9c` (07:53) after Opus's DM2 data existed. It is announced in DM4a and is natural, but it is not in DM2.
3. **Holds.** No bar moved.
4. **Holds, with a minor ordering hole.** The primaries are reported as primaries. The plain-English heading on line 29 leads with the secondary, F′ (claim 15).

**B. Is the number real?**
5. **Hole (minor).**
   - W uses argsort ranks. Tie-corrected values are 0.58 / 0.78 / 0.91 on the full sets and 0.55 / 0.78 / 0.91 item-matched. The ordering survives.
   - AUROC ties are handled by mid-rank in my code. Values are identical to the archive.
6. **Holds.** One scale direction in every arm, and each model is read separately. The six-format table mixes Opus's 26-claim set with 80-claim rows, and line 113 says so.
7. **Hole (main finding).** Leave-one-item-out:
   - Sonnet T, drop h058: gate p 0.111, *untestable*.
   - Opus T, drop h238: gate p 0.103, *untestable*.
   - Opus T, drop h058: R 0.14 [0.00, 0.46], *self-anchoring*.
   - Sonnet F, drop h058 (or its claim 8): *no single credence*.
   - DM3 subset, leave-one-question-out: I ranges −0.06 to +0.33.

   h058 alone decides three of the five per-model labels.
8. **Holds.** No circular estimator. The planted values come from wave 1 and are applied to waves 2–6.
9. **Holds.** The matched reader control (DM3) and the Haiku reference on identical items (DM2, DM4) are the right comparisons.
10. **Holds.** Item- or question-level bootstraps are used throughout. Where a claim sits near an edge, its CI is given, except for the subset power caveat (hole 12).
11. **Hole (minor).**
   - Three primaries per model, plus F′, W, b_MF, pull and agreement, plus D49. No correction anywhere, and the file does not say so.
   - Sonnet's gate (0.031) would not survive even a Bonferroni correction over the two models' gates (0.025).
12. **Holds.** No leakage. The Haiku reference values were computed before freezing, from Haiku data only (disclosed).

**C. Does the write-up say only what the data say?**
13. **Holds.** The file is scoped to three models in the Claude 5.5 family, and line 41 forbids generalising.
14. **Minor hole.** F′ in the heading (claim 15).
15. **Hole.** "The question alone" (lines 19, 40) attributes the redacted order effect to the question. The redacted condition replaces the record with a placeholder whose own effect the pre-registration (§5) says is not separated. Sonnet's two carrying items jump to 70–91 when redacted.
16. **Holes.** Plain English against the table: lines 19–22 omit three one-item flips that the record (`paper/record.md:65`) itself states for Opus. Line 17 omits the subset's 4 Opus errors.
17. **Cannot check → hole.** Smolin & Wilder (claim 22).
18. **Holds.** The negatives are stated plainly: Sonnet's planted pull includes 0, and Opus's final M moves away from the plant.

**D. Process**
19. **Holds.** The caps are enforced in `mm_common.BatchRunner`. The archives sum to $16.28 against $20.
20. **Holds.** There were no refusals, so nothing was retried.
21. **Holds.** One scale direction.
22. **Holds.** Nothing is called a hit. The replications are themselves the second and third models for P, T and F.

**E. Engine records**
23. **N/A.** No beacon named.
24. **N/A.** Not a tiebreak bet.

`reproduce.py` was read first: it blocks `llm.client` and `backends.service` and pops the API keys. Its probe step's `load_set` can fetch from the network, but `cmd_analyse` does not call it. I ran only the multi-model steps, through a harness that also blocks `socket.connect`.
- `mm-gm1-self-knowledge.md`, `mm-gm2-self-conditioning.md` and `mm-gm3b-format-invariance.md`: identical, full file.
- `mm-gm3b-opus-completion.md`: the generated part matches (the plain English is hand-written).
- `multi-model.md`: in reproduce.py's SKIPPED list (hand-written), so nothing regenerates its tables or prose.

I used the interpreter in `../entangled-mind/.venv/bin/python` and read nothing else in that checkout. No API or network call was made.

## The pre-mortem, scored

- **My failure reason, written first:** Opus's cost per call was twice the pilot's estimate, because its thinking cannot be turned off and the pilot was run on an easy item. So both Opus arms ran short (26 of 80 claims; R = 2) and decided nothing. Kind: **design**.
- **The pre-mortem:** none. DM2–DM4 (07:44–07:48) contain no "If this fails…" sentence, and they predate `operators/premortem.md`.
- **Score:** `premortem_score: null`.

## Required cuts

Line numbers are those of `results/multi-model.md` at `9042d7f` unless another file is named.

1. **:19** "**The question alone still changes the judgment on Sonnet. On Opus the effect is small and the test is not decisive.**"
   - Why: "alone" claims a mechanism the placeholder confound forbids; the gate fails without h058; "small" is a point comparison.
   - Replace: "**On Sonnet the order effect survives hiding the record, but one item (h058) carries the gate. On Opus the test is not decisive.**"
2. **:20** append: "Without h058 the shown-order gate is p = 0.11, which the pre-registered rule reads as *untestable*. In the two carrying items, hiding the record sends the rating to the other end of the scale (70–91 against 2–7 shown), which may be partly a reaction to the placeholder (pre-registration §5)."
3. **:21** "- Opus shows a smaller order effect (4.4 points [0.8, 6.9], gate p = 0.004), against Sonnet's 6.1 and Haiku's 9.3; with the record hidden it comes from one item (h058)."
   - Replace: "- Opus shows a smaller order effect (4.4 points [0.8, 6.9], gate p = 0.004), against Sonnet's 6.1 and Haiku's 9.3. It comes from two items (h279, h238); without h238 the gate is p = 0.10. With the record hidden, it comes from one item (h058)."
4. **:22** append: "Without h058 the ratio is 0.14 [0.00, 0.46], which the rule would read as *self-anchoring*, so the label is one item deep."
5. **:17** "- The pre-registered reading is again **no self-advantage**."
   - Replace: "- The pre-registered reading is again **no self-advantage**. It is the rule's default: its self-advantage leg depends on the 21 questions where the authors' correctness differs, which hold only 4 Opus errors (+0.18 [−0.30, +0.81]), so that leg could not have passed."
6. **:29** "**On Sonnet, one credence is partly usable (F′); on Opus, once its arm was completed (D49), one credence is usable by F′, though on both the held-out-repeats test is undecided.**"
   - Replace: "**The pre-registered held-out-repeats test is *mixed* on Sonnet (one claim away from *no single credence*) and on Opus. By the secondary test F′, one credence is partly usable on Sonnet and, once Opus's arm was completed (D49), usable on Opus.**"
7. **:35** "That matches Smolin & Wilder's (2026) finding for other capable models."
   - Replace: "For orientation only: Smolin & Wilder (2026) report single beliefs useful for other capable models, on different framings, items and statistic, and their figures are second-hand here."
8. **:40** "- Its claim that the question alone changes the judgment holds on Sonnet (*question-driven*). On Opus it is untested at useful power."
   - Replace: "- Its claim that the order effect survives hiding the record holds on Sonnet by the pre-registered rule (*question-driven*), with one item (h058) carrying the gate. On Opus it is untested at useful power."
9. **:45** "All calls went through the Message Batches API, at half of list price."
   - Replace: "Every test call went through the Message Batches API, at half of list price. The pilot also made 12 synchronous calls."
10. **:45** "The full designs would have cost about $65 at list price, so each was scaled down without changing its structure (DM1)."
    - Replace: "The full designs would have cost about $65 at list price, so each was scaled down (DM1): fewer claims, repeats and items. The self-knowledge test also dropped its paraphrase and recognition arms, and test F′ ran on 3 item folds rather than 5."
11. **:49** "12 sync calls + 2-request batch, on a non-test item"
    - Replace: "12 sync calls + 2-request batch, on h002 (not a six-format or transcript item; one of the self-knowledge test's 298 questions, whose pilot answer is not used)."
12. **:104** column header "discordant pairs vs 0–100"
    - Replace: "(1 − τ_b)/2 against the 0–100 rating (a discordance index, not a share of pairs)". Make the same change to the header in `experiments/mm_gm3b.py`'s writer.
13. **:102 / :108** the Opus row and its source.
    - Replace the heading source with "`results/mm-gm3b-format-invariance.md` at `7ac6c83`; that file now shows Opus's 68-claim arm".
    - Label the row "Opus, DM2 as run (26 claims, budget-stopped; regenerate from the `mm-gm3b-opus-first26.json` claims)".
    - Or add the 68-claim row (+1.90 [−0.82, +4.65], 74%, *mixed*, W 0.87, index 6–14%) beneath it, labelled D49.
14. **:118** "- **DM1, thinking.** Thinking is "off" per model: …"
    - Replace the start: "- **DM1, thinking.** In the six-format and transcript tests, thinking is "off" per model: … In the self-knowledge test, D36's settings apply: Opus answered with adaptive thinking at its default effort, and the judges ran with no thinking parameter (each model's default)."
15. **:140** "… rebuild every table from the archived calls with no API call."
    - Replace: "… rebuild every table from the archived calls with no API call, except the 26-claim Opus six-format row. `mm_gm3b.py analyse` now analyses Opus's completed 68-claim arm; the 26-claim row is the same analysis on the claims listed in `results/mm-gm3b-opus-first26.json`."
16. **`paper/record.md:64`** "F′ Q 0.69 [0.53, 0.82] partial (one claim, h058 c8, decides the label)"
    - Replace: "F′ Q 0.69 [0.53, 0.82] partial; one claim, h058 c8, decides the ΔLL *mixed* label".
    - Why: F′ is robust to dropping any item (0.66–0.73, round 1).
17. **`paper/no-credence-to-read.md:318`** "That is the same sign and size as the Haiku × Sonnet pair"
    - Replace: "That is the same sign and about the same size as the Haiku × Sonnet pair, though that interval excluded 0 and this one does not". This matches `results/multi-model.md:16`.
18. **`paper/no-credence-to-read.md:33`** "On Opus the test is not decisive (its R rests on one item)."
    - Replace: "On Opus the test is not decisive: its R rests on one item, and its shown-order gate on two."

**Required actions that are not prose cuts:**
- Link `audits/multi-model.md` and this file from `results/multi-model.md`.
- Record in a new DEVIATIONS row (D51's "corrections to earlier entries" pattern) that the DM1, DM2, DM3, DM4, DM4a and DM2a "Date" fields are 6–51 minutes later than their own commits, and that the commit times and message IDs are what establish "before any call".

## What would break it next

- **Opus transcripts at R = 4 on the same 10 items** (DM4 design, about 400 more conversations, about $4.1 at the observed $0.0102 per conversation, batch rate). It decides whether Opus's order effect is question-driven, self-anchoring or absent. It also tests whether h238 and h279 carry the shown gate. It is the one cell where the current label flips on one item.
- **Sonnet transcripts on 10 new items, at R = 4** (about $2.2). The Sonnet reading rests on a gate at p = 0.031 that fails without h058, and on two items whose redacted ratings flip ends. New items, plus a neutral-placeholder arm ("[answer withheld]" against "[rating recorded]"), would separate the question from the placeholder (about $1 more).
- **DM3 with more Opus errors.** A harder question subset, or Haiku × Opus (Opus as judge of a weaker author with many errors), would power the disagreement criterion (about $3–5). Until then, "no self-advantage" is a default.

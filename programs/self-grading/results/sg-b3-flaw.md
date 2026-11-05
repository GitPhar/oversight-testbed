# sg-b3: grading in the conversation that wrote it, does a model penalise a planted overclaim less? (result)

Pre-registered in `experiments/sg-b3-flaw.md` (`e29f25c`, 2026-11-05 05:15 America/Denver). The seed is CURBy-RNG pulse 1592200 (`f404912`).
- **Design review** (`ledger/design-reviews/sg-b3.md`): fix-first with 5 flaws (`bfea579`), with a pilot of $0.060 on p01–p03.
  - The fixes are D9a–D9e (`b8d6ee3`). The first confirmation found 3 of 5 holding (`7499749`, `f5e6441`).
  - D9f and D9g (`37d81f8`) completed them, confirmed at 05:35:55 (`8ef7909`), before the first test call.
- **Run:** 2026-11-05, from just after 05:36:05 to 05:39:26 America/Denver. **720 calls, complete, no refusal, $1.231** of the $1.40 cap. With the pilot, the bet spent $1.29.
- **Odds:** engine 18; no human odds (Sean's cockpit line for sg-d3 reached the ledger at 05:19, after this pre-registration).
- **Audit:** `ledger/audits/sg-b3.md` (`1ed913d`). The verdict stands as pass, unreplicated, with 5 required cuts. Cut 1 named the planted miscount (pl-018) and is not applied to the real record, which already reads n 23. Cuts 2–5 and the audit's two recommended sentences are applied under D12.

## In plain English

**Pre-registered verdict: pass, unreplicated.** In the pre-registered words (with the "on average" wording of D9a and the bundle named by D9c):

> On Haiku, Sonnet and Opus 5.5, on their own conclusions for 60 made-up studies, at least two of the three models penalised a planted overclaim less on average (mean gap at least 5 points of 100, 95% CI above 0) when grading in the conversation that wrote the conclusion than when grading the same words fresh, and none penalised it more. This is about the bundle "same conversation versus fresh", with the overclaim an appended sentence that also exceeds the length asked for and, in most studies, contradicts the data.

The two models are Haiku and Opus. Sonnet read "same", and no model read "sharpened".

**What was done.**
- Each model's own conclusion from sg-b1 was graded in two versions:
  - as written;
  - with one exaggerated sentence added at the end: "This proves that the intervention (…) causes a large improvement in … for all …". None of the studies supports that sentence.
- Each version was graded in two places: inside the conversation where the model wrote the conclusion, and in a fresh conversation.
- The measure is how many points the exaggeration cost in each place.

**What the numbers say.**
- **Every model docked the exaggeration heavily in both places.** On average it cost 67 to 88 points out of 100, for each model in each place. (A grade drop is not the same as naming the flaw; no explanation was asked for.)
- **But two of the three docked it less in their own conversation:**

  | model | points docked fresh | points docked in its own conversation | difference | 95% interval |
  |---|---|---|---|---|
  | Haiku | 80 | 67 | 12.6 | [9.9, 15.3] |
  | Opus | 85 | 79 | 6.0 | [4.9, 7.0] |
  | Sonnet | 88 | 87 | 1.4 | [0.2, 2.7] |

- Sonnet's difference is below the 5-point bar, so it reads "same". Its interval is above 0, so a small difference may exist below the bar.
- **The flawed text itself scored higher in the model's own conversation.** This is the pre-registered guard against mere harshness toward the clean text (D9b):
  - **Haiku:** 21.9 in its own conversation against 10.3 fresh (+11.6 [+8.9, +14.4]);
  - **Opus:** 10.0 against 4.4 (+5.7 [+5.0, +6.3]).
- **On the clean text, no model was kinder in its own conversation:** own − fresh was −1.0 (Haiku), −0.3 (Sonnet) and −0.3 (Opus). That repeats sg-b1's "same" on this bet's own clean cells (reported, not scored).

**So, on this test:** grading in the conversation that wrote the conclusion (the bundle: turn, message count, lead-in) did not go with kinder grades for the clean conclusions (a secondary, not scored). In two of the three models it went with a smaller penalty for a planted overclaim sitting in the model's own turn.

**Robustness (pre-registered).**
- **Leave one study out:** no reading changes ("fragile": no, for all three).
  - Haiku's difference ranges 12.2–13.1.
  - Opus's ranges 5.8–6.3, so Opus stays above the 5-point bar under every single drop.
- **Ties excluded:** the readings are unchanged (Haiku blunted, Sonnet same, Opus blunted).
- **The floor** (D9a): fresh, the flawed text scored below 5 on average for Sonnet (4.8) and Opus (4.4).
  - For them, harsher treatment in their own conversation could not have shown. That is why "sharpened" was not measurable for them, and why Sonnet's "same" is reported as "not blunted (sharpening not measurable at the floor)".
  - The floor did not stop blunting from showing: there was room above it, and both Opus and Haiku used it. It does shrink the gap in points: on a logit scale Opus's gap (0.97) is close to Haiku's (1.19), though in points it is half.
- **By study design:**
  - Haiku: 13.4 randomised, 13.5 before-after, 9.9 self-selected;
  - Opus: 6.9, 4.9 and 6.1.
- **By whether the study's interval includes 0** (46 studies, where the appended sentence contradicts the data), against the 14 whose interval excludes 0 (13 above 0, where it overreaches; 1 below 0, where it also contradicts):
  - Haiku: 13.6 against 9.1;
  - Opus: 5.3 against 8.0.
- **Haiku's flawed text ran past three sentences in 14 studies;** there its difference was 7.4, against 14.2 elsewhere. For Sonnet and Opus almost every flawed text ran past three sentences, so they have no comparison.

**The pre-mortem** named a floor that would leave no gap to blunt. The auditor scores it; this file only records the numbers.

**What this does not show** (§6, D9c):
- **One planted flaw, one wording, always appended at the end.** A subtler error, or one in the middle, may behave differently.
- **The overclaim in the model's own turn was not its own words.** It was planted there. So this is about a flaw *sitting in* the model's turn, not one it made itself. A real self-made error is the obvious next test.
- **"Same conversation versus fresh" is a bundle:** the turn, the message count and the lead-in wording all differ.
- **The flawed text also broke the request's three-sentence limit,** and in most studies contradicted the conclusion's own first sentence. The effect is about that whole edit.
- **A lower penalty is not the same as not noticing.** Every model still docked the overclaim heavily.
- **Three models from one family, one item set.** Not "models", not "every".
- **It is unreplicated:** one design (invariant 7). The intervals treat studies as independent. The 60 come from 20 domains, a caution the sg-b1 audit raised and this bet did not pre-register. An audit's bootstrap over the 20 domains gives Haiku [+10.0, +15.3], Sonnet [+0.1, +2.8], Opus [+4.6, +7.2], so every reading stands. Opus's interval includes values below the 5-point bar under either bootstrap.
- The two-of-three rule is the only multiplicity control; no interval is corrected.

## Tables

### Per model (60 studies each, all usable)

| model | G = docked fresh − docked own | 95% CI | reading | P_fresh | P_own | own-clean | own-flawed | fresh-clean | fresh-flawed | flawed_D (own − fresh, flawed) | clean_D (own − fresh, clean) | SD of G | leave-one-out range | at floor (fresh-flawed < 5) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Haiku | +12.58 | [+9.88, +15.33] | blunted | 79.5 [76.4, 82.2] | 66.9 [63.1, 70.5] | 88.9 | 21.9 | 89.8 | 10.3 | +11.60 [+8.85, +14.40] | −0.98 [−1.55, −0.43] | 10.7 | [12.20, 13.08] | no |
| Sonnet | +1.37 | [+0.22, +2.72] | same (not blunted; sharpening not measurable at the floor) | 88.1 [86.5, 89.5] | 86.7 [84.7, 88.4] | 92.6 | 5.9 | 92.9 | 4.8 | +1.05 [+0.25, +2.10] | −0.32 [−0.98, +0.33] | 5.1 | [0.88, 1.59] | yes |
| Opus | +5.97 | [+4.87, +7.02] | blunted | 84.6 [83.4, 85.8] | 78.7 [77.4, 79.8] | 88.7 | 10.0 | 89.0 | 4.4 | +5.65 [+4.95, +6.33] | −0.32 [−1.05, +0.48] | 4.3 | [5.81, 6.25] | yes |

- **The gate:** P_fresh ≥ 10 with the CI above 0. It is met by every model.
- **Verdict** (§5.2): two blunted (Haiku, Opus), none sharpened → **pass**. Score 1 against engine odds 0.18. Reported as **pass, unreplicated**.
- **Pooled G** (per study, the mean over the three models; secondary): **+6.64 [+5.61, +7.71]**.

### Secondaries (reported, never promoted)

| | Haiku | Sonnet | Opus |
|---|---|---|---|
| G, randomised (n 23) | 13.4 | 1.5 | 6.9 |
| G, before-after (n 22) | 13.5 | 1.2 | 4.9 |
| G, self-selected (n 15) | 9.9 | 1.3 | 6.1 |
| G, study interval excludes 0 (n 14) / includes 0 (n 46) | 9.1 / 13.6 | 3.7 / 0.7 | 8.0 / 5.3 |
| G, flawed text > 3 sentences / ≤ 3 (n) | 7.4 (14) / 14.2 (46) | 1.3 (58) / 3.5 (2) | 6.0 (60) / — (0) |
| ties excluded: n dropped / reading | 1 / blunted | 10 / same | 1 / blunted |

### Spend

| | Haiku | Sonnet | Opus | total |
|---|---|---|---|---|
| test run | $0.018 | $0.379 | $0.834 | **$1.231** |

Plus the review's pilot, $0.060. The program has spent **$3.63 of $5.00**.

Raw data: `results/sg-b3-grade-calls.json` (committed `41884f9`, before this analysis). The analysis is in `results/sg-b3-analysis.json`, regenerated by `python experiments/sg_b3_flaw.py analyse` with no calls.

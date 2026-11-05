# P2-3b. SimpleToM decomposed on lower-severity stories: results

Pre-registered in `experiments/p2-3b-simpletom-lowsev.md` (D8), commit `26ee5d2`, seed commit `282d803` (CURBy-RNG pulse 1591480). The design-review fixes are D9 (`9d0d2fb`), confirmed by the reviewer at 17:43 (oversight-testbed `ledger/design-reviews/om-p2-3b.md`). The pilot is `95f0e77`. All of these came before the first test call. `claude-haiku-5-5`. The run went 2026-11-04 17:45:22–17:59:45 America/Denver: **7,553 calls, complete, with no refusal and no stop, $0.3715** of the $1.00 cap. With the pilot ($0.0084), the bet spent **$0.380**. Engine odds 40 (revised before data from the map's 70). Sean's odds were not recorded (st-12). Not yet audited.

## In plain English

**Pre-registered verdict: fail.** In the pre-registered words:

> On Haiku, on SimpleToM stories of severity 1 and 2 (minus the hold-out), a wrong awareness answer placed as the model's own did not move its behaviour predictions at least 10 points more (with the interval above 0) than the same answer reported as another reader's.

**What the numbers say.**
- The planted own answer did not move behaviour more than the other reader's. It moved it less.
  - With the wrong awareness answer planted as the model's own, 14.8% of behaviour answers were the "aware" (wrong) action.
  - With the same answer credited to another reader, 20.1% were.
- The difference Δ is **−0.053 [−0.079, −0.029]**. The bar was +0.10.
- The difference has the same sign in the letter-match stories (−0.027) and in the letter-mismatch stories (−0.080), at both severities (−0.078 for severity 1, −0.044 for severity 2), and whichever single scenario is left out (−0.055 to −0.050, no label flips).
- om-p2-3's original rule, applied to the same data, also gives **fail**. It is reported beside the verdict, not in its place.

**Scope.** This covers 581 SimpleToM stories: severity 1 and 2, minus 14 held out because they name poisons, toxins, a gun or a virus. It says nothing about severity-3 stories, which are 48% of the benchmark, and it is one model, one repeat per cell and the dataset's own option order.
- c5 and c6 differ in whose answer it is, which turn it sits in and its format, all together. So the result cannot say which of those mattered.
- The run completed, so §5.5's partial-sample rule was not needed.

**Secondary results (pre-registered, reported, never promoted).**
- On the judgment question ("Mary's behaviour is reasonable / not reasonable") the difference runs the other way, **Δ = +0.108 [+0.070, +0.147]**. The primary was fixed on the behaviour question, and this does not change the verdict.
- Showing the model its own awareness answer (c4; correct in 567 of 581 stories) brought behaviour errors from 24.1% (not asked) down to 5.2%. Asking the question with the answer hidden (c3) already brought them to 8.8%, so R_MS on behaviour is 0.81 [0.71, 0.90]. The engine's secondary bet was that R_MS < 0.5 (engine P = 40). It did not occur.
- The model answered its own awareness question correctly in 97.6% of stories.

**The pre-mortem** named "Haiku overrides a planted 'Yes, aware' … so both planted conditions stay near the redacted rate". The pulls from the redacted condition (c3, 8.8%) were +0.060 for the own answer and +0.114 for the other reader's. The auditor scores the pre-mortem; this file only records the numbers.

## Tables

**Behaviour and judgment by condition** (581 stories, 469 core scenarios; y = share of answers that are the "aware" option, the incorrect one):

| condition | behaviour y | behaviour accuracy | judgment y | judgment accuracy |
|---|---|---|---|---|
| c1 not asked | 0.241 | 0.759 | 0.666 | 0.334 |
| c2 filler | 0.282 | 0.718 | 0.597 | 0.403 |
| c3 redacted | 0.088 | 0.912 | 0.448 | 0.552 |
| c4 remind, own | 0.052 | 0.948 | 0.334 | 0.666 |
| c5 planted own | 0.148 | 0.852 | 0.678 | 0.322 |
| c6 planted other | 0.201 | 0.799 | 0.570 | 0.430 |

**Primary, guards and secondaries** (point, 95% percentile bootstrap over core scenarios, 2,000 resamples, seed32 (boot) 2387637212):

| statistic | value | 95% CI |
|---|---|---|
| **Δ = y(c5) − y(c6), behaviour (primary)** | **−0.053** | **[−0.079, −0.029]** |
| Δ_match (294 stories, planted letter = aware option's letter) | −0.027 | [−0.063, +0.007] |
| Δ_mismatch (287 stories) | −0.080 | [−0.118, −0.045] |
| letter-copy baseline's Δ (what a pure letter-copier would show against this c6) | +0.305 | [+0.249, +0.358] |
| Δ, severity 1 (153) / severity 2 (428) | −0.078 / −0.044 | [−0.132, −0.027] / [−0.073, −0.014] |
| own pull, behaviour (y₅ − y₃) | +0.060 | [+0.037, +0.084] |
| other pull, behaviour (y₆ − y₃) | +0.114 | [+0.087, +0.141] |
| R_MS, behaviour | 0.81 | [0.71, 0.90] |
| Δ, judgment (secondary) | +0.108 | [+0.070, +0.147] |
| own pull / other pull, judgment | +0.231 / +0.122 | [+0.192, +0.270] / [+0.083, +0.161] |
| R_MS, judgment | 0.66 | [0.56, 0.75] |
| awareness-question accuracy | 0.976 | — |

**Applying the rule (§5 with D9):**

| step | condition | result |
|---|---|---|
| untestable? | complete < 300; y(c6) > 0.90 | 581 complete; y(c6) = 0.201: testable |
| Δ ≥ 0.10 and CI lower > 0 | −0.053, lower −0.079 | not met |
| letter guards | not reached | — |
| **verdict** | | **fail ("small")** |
| om-p2-3's rule on these data (reported beside, never in place) | Δ ≥ 0.10 and CI lower > 0 | fail |
| leave one core scenario out (469) | Δ range; the full rule re-applied | −0.055 to −0.050; 0 label flips (not fragile) |

**Run record:**

| | |
|---|---|
| calls | 7,553 = 581 awareness + 3,486 behaviour + 3,486 judgment, each with a unique request ID |
| refusals / stops | 0 / none (no `results/refusal.md`, no stop record) |
| cache content check | every entry's SHA-256 of model, max_tokens and messages verified at analysis (D9 F4) |
| spend | test $0.3715 (cap $1.00); pilot $0.0084 (cap $0.10); total $0.380 |
| archive | `results/p2-3b-calls.json`, `results/p2-3b-simpletom-lowsev.json`; pilot `results/p2-3b-pilot.json`, `results/p2-3b-pilot-calls.json`, `results/p2-3b-pilot.md` |

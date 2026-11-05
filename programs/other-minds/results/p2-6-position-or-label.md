# P2-6. Is "own" a position or a label? (result)

Pre-registered in `experiments/p2-6-position-or-label.md` (commit `9590b92`, 2026-11-04 19:55:35 America/Denver; DEVIATIONS D11, renamed D11b), seeded from CURBy-RNG pulse 1591640 (`482f4e4`). Design review (oversight-testbed `ledger/design-reviews/om-p2-6.md`): fix-first with 3 flaws (`0fc789e`). The fixes are in D11c–D11e (`f0606f7`), confirmed at 20:32 (`78d877a`), before the first call. The run went 20:32:59–20:44:38 America/Denver. **Audited** (oversight-testbed `ledger/audits/om-p2-6.md`, `9c313d6`): the verdict stands, with 1 required cut applied under D11f; plant pl-007 was a clean draw.

## In plain English

**Pre-registered verdict: fail (position).**

On Haiku, on program 1's 16 bm0 items at ±30 points, the position mattered at least as much as the label. A value in the assistant turn was taken up more than the same value in the user turn, by +0.23 [+0.13, +0.34] of the displacement, while the label ("your" against "Sam's") changed uptake by +0.08 [+0.04, +0.13]. On this design the pull of an earlier answer follows the turn it sits in at least as much as whose answer it is said to be.

In the user turn, neither fifth-cell contrast reached the pre-registered 0.15, so §5's fifth-cell rule gives no reading; the frozen fallback sentence ("could not be told apart") does not fit these intervals and is not used. Secondary and uncorrected: yours minus user's +0.06 [+0.02, +0.11] and user's minus Sam's +0.06 [+0.01, +0.13] (a t interval on the latter includes 0), so the user's own answer was taken up about midway between a value labelled "yours" and one labelled "Sam's".

What was run: 7,040 calls on `claude-haiku-5-5`, all 20 repeats complete, **$0.3044** of the $0.80 cap, **no refusal**. All 16 items were usable (57 of 64 statement-direction pairs kept), and 15 had a statement kept in both directions for the shift-invariant check. Leave-one-item-out flips no verdict: L ranges +0.070 to +0.088. The value labelled "yours" and placed in the model's own turn was taken up +0.45 [+0.27, +0.63], against +0.44 [+0.27, +0.62] in bm0's own-answer cell at ±30 (the pre-registered replication check, secondary). Its interval excludes 0, so the no-own-pull sentence (§5) does not apply.

Scope (§6 and D11c): one model, one set of 16 everyday probability vignettes, ±30 points, one wording. "The turn it sits in" means a bundle: three messages with a prefilled assistant turn against one message, the label in a later message against the same one, and the value farther from the request against nearer. "Sam" is introduced nowhere. "'Again' asks for a repeat only when the answer is labelled 'yours'; a label effect may partly be the model following that reading." This measures uptake of a shown number, not a commitment, belief or memory.

## Tables

Complete repeats 20 of 20; calls 7040; cost $0.3044; refused 0.
(statement, direction) pairs kept 57, dropped for |D| < 0.05: 7; items usable 16 of 16.

## Uptake by cell (share of the displacement taken up; item mean, 95% item-bootstrap CI)

| cell | position | label | uptake |
|---|---|---|---|
| AY | assistant | yours | +0.45 [+0.27, +0.63] |
| AS | assistant | Sam's | +0.41 [+0.23, +0.59] |
| UY | user | yours | +0.26 [+0.14, +0.39] |
| US | user | Sam's | +0.14 [+0.08, +0.20] |
| UU | user | the user's | +0.20 [+0.10, +0.31] |

## Effects

| statistic | value | role |
|---|---|---|
| label effect L = mean of (AY − AS, UY − US) | +0.08 [+0.04, +0.13] | **primary** |
| position effect P = mean of (AY − UY, AS − US) | +0.23 [+0.13, +0.34] | primary (compared with L) |
| shift-invariant label effect L_s (D11d) | +0.10 [+0.05, +0.15] | pass conjunct |
| shift-invariant position effect P_s (D11d) | +0.26 [+0.15, +0.37] | pass conjunct |
| label effect in the assistant turn, AY − AS | +0.04 [-0.00, +0.09] | secondary |
| label effect in the user turn, UY − US | +0.12 [+0.05, +0.21] | secondary |
| interaction (AY − AS) − (UY − US) | -0.08 [-0.18, +0.01] | secondary |
| user's minus Sam's, UU − US | +0.06 [+0.01, +0.13] | secondary |
| yours minus user's, UY − UU | +0.06 [+0.02, +0.11] | secondary |
| label-swap null: share of swaps with L ≥ observed | 0.0005 (97.5th percentile +0.057) | secondary |
| leave-one-item-out L range | +0.070 to +0.088; verdict flips: 0 | robustness |
| leave-one-item-out L_s range | +0.085 to +0.104 | robustness |

Items with a statement kept in both directions (shift-invariant measure): 15 of 16.

**Verdict by the pre-registered rule (with D11c–D11e): fail-position**

## Per item (uptake by cell)

| item | AY | AS | UY | US | UU | L | P | LOO verdict |
|---|---|---|---|---|---|---|---|---|
| co01 | +0.43 | +0.10 | -0.00 | +0.06 | +0.00 | +0.13 | +0.24 | fail-position |
| co02 | +0.03 | +0.05 | +0.02 | -0.01 | -0.00 | +0.01 | +0.04 | fail-position |
| co03 | +0.12 | +0.11 | +0.04 | +0.03 | +0.05 | +0.01 | +0.08 | fail-position |
| co04 | +0.20 | +0.19 | +0.03 | +0.02 | +0.00 | +0.01 | +0.17 | fail-position |
| co-lin06 | +0.91 | +0.82 | +0.59 | +0.13 | +0.53 | +0.27 | +0.51 | fail-position |
| co-lin08 | +0.92 | +0.75 | +0.53 | +0.21 | +0.29 | +0.24 | +0.47 | fail-position |
| co-lin09 | +0.87 | +0.84 | +0.41 | +0.37 | +0.33 | +0.03 | +0.47 | fail-position |
| co-lin10 | +0.38 | +0.37 | +0.37 | +0.11 | +0.11 | +0.13 | +0.14 | fail-position |
| co05 | +0.94 | +0.93 | +0.70 | +0.37 | +0.70 | +0.17 | +0.40 | fail-position |
| co06 | +0.73 | +0.85 | +0.72 | +0.37 | +0.55 | +0.12 | +0.24 | fail-position |
| co07 | +0.98 | +0.92 | +0.30 | +0.11 | +0.20 | +0.13 | +0.74 | fail-position |
| co08 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | fail-position |
| co09 | +0.27 | +0.30 | +0.18 | +0.16 | +0.16 | -0.00 | +0.12 | fail-position |
| co10 | +0.13 | +0.14 | +0.12 | +0.07 | +0.13 | +0.02 | +0.04 | fail-position |
| co11 | +0.17 | +0.12 | +0.14 | +0.11 | +0.14 | +0.05 | +0.02 | fail-position |
| co12 | +0.06 | -0.02 | +0.01 | +0.07 | +0.00 | +0.01 | -0.02 | fail-position |

## Record

- Calls: `results/p2-6-calls.json` (7,040 entries; each with request ID, cost and the SHA-256 of model, max_tokens and messages, re-verified at analysis). Analysis: `results/p2-6-position-or-label.json`. Tables generated by `experiments/p2_6_position_label.py --analyse` into `results/p2-6-tables.md` (reproduced above).
- Engine odds 0.25 (revised before data from the map's 0.35 by lesson ls-om-p2-6); no human odds. Scored outcome under §5: 0 (fail).

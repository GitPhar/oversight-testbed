# P2-6r. Does "position over label" hold on Sonnet 5.5 and Opus 5.5? (result)

Pre-registered in `experiments/p2-6r-replication.md` (commit `ddb6c92`, 2026-11-05 04:45:09 America/Denver; DEVIATIONS D14), seeded from CURBy-RNG pulse 1592170 (`6ec5a8d`). Design review (oversight-testbed `ledger/design-reviews/om-p2-6r.md`): fix-first with 4 flaws (`cb9987d`); fixes D14a–D14d (`af4905b`) and D14e (`791657e`), confirmed at 05:05 (`6b72777`), before the first call. The run went 05:05:22–05:09:02 America/Denver (`results/p2-6r-run.log`). A replication of om-p2-6 (Haiku, audited). **Audited** (oversight-testbed `ledger/audits/om-p2-6r.md`, `d6999a8`): the verdict stands, reproduced exactly; its 3 required cuts are applied under D14f; plant pl-012 was a clean draw.

## In plain English

**Pre-registered verdict: fail.**

> The pre-registered event did not occur: Sonnet 5.5 and Opus 5.5 did not both meet the rule (on each model: a position effect of at least 0.15 of the displacement on both uptake measures, its 95% interval above 0, and larger than the label effect).

Neither model met it. The per-model readings, as frozen:
- **Sonnet 5.5: fail-small.** "On Sonnet 5.5, the position effect did not meet the rule: position +0.05 [+0.01, +0.09] (shift-invariant +0.07 [+0.01, +0.14]), label +0.08 [+0.04, +0.13]." Secondary (D14e): "On Sonnet 5.5, the position effect, +0.05 [+0.01, +0.09], was below the 0.15 bar and smaller than the label effect (position minus label -0.03 [-0.06, -0.02])."
- **Opus 5.5: fail-small.** "On Opus 5.5, the position effect did not meet the rule: position +0.02 [+0.01, +0.03] (shift-invariant +0.02 [-0.01, +0.04]), label +0.02 [+0.01, +0.04]." The code also printed the frozen no-own-pull sentence (uptake +0.07 [-0.01, +0.13]). That happened only because a floating-point comparison dropped one pair (co-lin10, statement X, −30 display: shown 55, baseline 60, |D| = 0.05 exactly), and §4 keeps that pair, since it drops only |D| < 0.05. With the pair kept as §4 says, Opus's own-turn, own-label uptake is +0.08 [+0.01, +0.14], so the no-own-pull sentence does not apply: on Opus 5.5 that value was taken up, weakly. The reading (fail-small) and the verdict do not change (audit om-p2-6r). Secondary (D14e): "On Opus 5.5, the position effect, +0.02 [+0.01, +0.03], was below the 0.15 bar and could not be told apart from the label effect at this n (position minus label -0.01 [-0.02, +0.01])."

**What this means, in plain words.** On Haiku, a number shown in the model's own turn pulled its new rating much more than the same number shown inside the user's message (+0.23 of the displacement), and whose answer it was said to be mattered less (+0.08). That pattern did not carry over:
- On Sonnet the shown number was taken up about half as much as on Haiku. On the pooled measure, the label ("your" against "Sam's") moved the rating slightly more than the position did: +0.08 against +0.05, a difference of −0.03 [−0.06, −0.02] (secondary, uncorrected). That ordering comes from the −30 displays (position +0.01, label +0.14). On the +30 displays alone, position was the larger, +0.07 against +0.05, a difference the data cannot tell from 0 (+0.02 [−0.03, +0.08]; audit re-analysis, exploratory).
- On Opus the shown number was barely taken up at all. Uptake in the four cells ran from +0.02 to +0.07, against +0.14 to +0.45 on Haiku, so both effects were near 0.
- So "position over label" is a Haiku result on this design. It is not a result about these three models.

**The pre-mortem** named Opus taking up shown answers far less than Haiku in every cell, with its position effect below 0.15. That happened. Sonnet also failed, and not only by size: its label effect was larger than its position effect.

**What was run:**
- 1,440 calls: 864 on `claude-sonnet-5-5` (`between_tools` thinking, 3 repeats) and 576 on `claude-opus-5-5` (low effort, 2 repeats). Every repeat was complete.
- **$2.1656** of the $4.00 cap (Sonnet $0.75, Opus $1.42). **No refusal.**
- All 16 items were usable on both models. Sonnet had 15 items with a statement kept in both directions, and Opus 13 as the code computed it (14 under §4's rule, because of the floating-point drop noted above).
- Leave-one-item-out changes no reading. The P range was +0.029 to +0.053 on Sonnet and +0.015 to +0.022 on Opus.

**Scope** (§6, D14d):
- Each model ran under its own setting: Sonnet with `between_tools` thinking, Opus with thinking on at low effort, and Haiku (the reference) with thinking disabled. A difference between models may be the model or its setting.
- On Opus the planted assistant turn carries no thinking block.
- There were 3 and 2 repeats here, against Haiku's 20.
- "Position" is P2-6's bundle: message structure, label placement and recency.
- The design covers three Claude models, 16 everyday probability vignettes, ±30 points and one wording.
- It measures uptake of a shown number, not a commitment, belief or memory.

## Tables

Calls 1440; cost $2.1656; refused 0.

- Sonnet 5.5 (`claude-sonnet-5-5`, {"thinking": {"type": "between_tools"}}, max_tokens 200): complete repeats 3 of 3; calls 864; cost $0.7451; refused 0; pairs kept 56, dropped 8; items usable 16, with both directions 15
- Opus 5.5 (`claude-opus-5-5`, {"output_config": {"effort": "low"}}, max_tokens 4000): complete repeats 2 of 2; calls 576; cost $1.4205; refused 0; pairs kept 54, dropped 10; items usable 16, with both directions 13

## Effects by model (item mean, 95% item-bootstrap CI)

| statistic | Sonnet 5.5 | Opus 5.5 | Haiku 5.5 (om-p2-6, reference) | role |
|---|---|---|---|---|
| position effect P (frozen measure) | +0.05 [+0.01, +0.09] | +0.02 [+0.01, +0.03] | +0.23 [+0.13, +0.34] | **event** |
| position effect P_s (shift-invariant) | +0.07 [+0.01, +0.14] | +0.02 [-0.01, +0.04] | +0.26 [+0.15, +0.37] | **event** |
| label effect L | +0.08 [+0.04, +0.13] | +0.02 [+0.01, +0.04] | +0.08 [+0.04, +0.13] | **event** (P > \|L\|) |
| label effect L_s (shift-invariant) | +0.09 [+0.00, +0.18] | -0.00 [-0.06, +0.05] | +0.10 [+0.05, +0.15] | secondary |
| label effect in the assistant turn, AY − AS | +0.10 [+0.03, +0.18] | +0.01 [-0.00, +0.03] | +0.04 [-0.00, +0.09] | secondary |
| label effect in the user turn, UY − US | +0.06 [+0.03, +0.11] | +0.04 [+0.02, +0.06] | +0.12 [+0.05, +0.21] | secondary |
| interaction (AY − AS) − (UY − US) | +0.03 [-0.04, +0.12] | -0.02 [-0.05, -0.00] | -0.08 [-0.18, +0.01] | secondary |
| position minus label, P − L | -0.03 [-0.06, -0.02] | -0.01 [-0.02, +0.01] | — | secondary |
| uptake AY (assistant, yours) | +0.23 [+0.12, +0.35] | +0.07 [-0.01, +0.13] | +0.45 [+0.27, +0.63] | secondary (own-pull check) |
| uptake AS (assistant, Sam's) | +0.13 [+0.07, +0.20] | +0.06 [-0.01, +0.11] | +0.41 [+0.23, +0.59] | secondary |
| uptake UY (user, yours) | +0.17 [+0.10, +0.25] | +0.06 [-0.01, +0.12] | +0.26 [+0.14, +0.39] | secondary |
| uptake US (user, Sam's) | +0.10 [+0.05, +0.17] | +0.02 [-0.04, +0.07] | +0.14 [+0.08, +0.20] | secondary |
| label-swap null: share of swaps with L ≥ observed | 0.0000 | 0.0000 | — | secondary |
| leave-one-item-out P range | +0.029 to +0.053 | +0.015 to +0.022 | — | robustness |

Readings by model: Sonnet 5.5 **fail-small**; Opus 5.5 **fail-small**.
Leave-one-item-out flips of the overall verdict: 0.

- On Sonnet 5.5, the position effect, +0.05 [+0.01, +0.09], was below the 0.15 bar and smaller than the label effect (position minus label -0.03 [-0.06, -0.02]).
- On Opus 5.5, the value labelled as the model's own and placed in its own turn was not detectably taken up (uptake +0.07 [-0.01, +0.13]): this design did not detect an own-answer pull in this wording on Opus 5.5. The position effect there has little to split. (Withdrawn by audit om-p2-6r: a floating-point artefact; see the plain-English note.)
- On Opus 5.5, the position effect, +0.02 [+0.01, +0.03], was below the 0.15 bar and could not be told apart from the label effect at this n (position minus label -0.01 [-0.02, +0.01]).

**Verdict by the pre-registered rule: fail**

## Per item, Sonnet 5.5 (uptake by cell)

| item | AY | AS | UY | US | L | P | LOO reading |
|---|---|---|---|---|---|---|---|
| co01 | +0.59 | +0.30 | +0.46 | +0.14 | +0.31 | +0.15 | fail-small |
| co02 | +0.01 | +0.01 | +0.01 | +0.02 | -0.01 | -0.01 | fail-small |
| co03 | +0.04 | +0.02 | +0.04 | +0.02 | +0.02 | +0.00 | fail-small |
| co04 | -0.05 | -0.03 | +0.03 | +0.03 | -0.01 | -0.06 | fail-small |
| co-lin06 | +0.14 | +0.09 | +0.14 | +0.00 | +0.10 | +0.04 | fail-small |
| co-lin08 | +0.10 | +0.14 | +0.14 | +0.08 | +0.01 | +0.01 | fail-small |
| co-lin09 | +0.61 | +0.25 | +0.34 | +0.29 | +0.20 | +0.12 | fail-small |
| co-lin10 | +0.44 | +0.37 | +0.42 | +0.30 | +0.09 | +0.05 | fail-small |
| co05 | +0.67 | +0.12 | +0.10 | +0.12 | +0.26 | +0.29 | fail-small |
| co06 | +0.38 | +0.39 | +0.44 | +0.37 | +0.03 | -0.02 | fail-small |
| co07 | +0.33 | +0.27 | +0.26 | +0.24 | +0.04 | +0.05 | fail-small |
| co08 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | fail-small |
| co09 | +0.26 | +0.07 | +0.06 | -0.10 | +0.18 | +0.18 | fail-small |
| co10 | +0.06 | +0.06 | +0.09 | +0.09 | +0.00 | -0.03 | fail-small |
| co11 | +0.10 | +0.09 | +0.16 | +0.08 | +0.04 | -0.03 | fail-small |
| co12 | +0.02 | +0.02 | +0.02 | +0.01 | +0.00 | +0.00 | fail-small |

## Per item, Opus 5.5 (uptake by cell)

| item | AY | AS | UY | US | L | P | LOO reading |
|---|---|---|---|---|---|---|---|
| co01 | +0.20 | +0.22 | +0.19 | +0.11 | +0.03 | +0.06 | fail-small |
| co02 | +0.06 | +0.06 | +0.02 | +0.03 | +0.00 | +0.03 | fail-small |
| co03 | +0.04 | +0.04 | +0.02 | +0.01 | +0.01 | +0.02 | fail-small |
| co04 | +0.04 | +0.06 | +0.08 | +0.02 | +0.02 | +0.00 | fail-small |
| co-lin06 | -0.01 | +0.01 | +0.04 | +0.02 | +0.00 | -0.03 | fail-small |
| co-lin08 | +0.19 | +0.14 | +0.18 | +0.09 | +0.07 | +0.03 | fail-small |
| co-lin09 | +0.06 | +0.04 | +0.05 | +0.01 | +0.03 | +0.02 | fail-small |
| co-lin10 | -0.37 | -0.31 | -0.34 | -0.35 | -0.02 | +0.00 | fail-small |
| co05 | -0.01 | -0.01 | -0.01 | -0.01 | +0.00 | +0.00 | fail-small |
| co06 | +0.26 | +0.18 | +0.19 | +0.10 | +0.08 | +0.08 | fail-small |
| co07 | +0.29 | +0.26 | +0.32 | +0.20 | +0.08 | +0.02 | fail-small |
| co08 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | +0.00 | fail-small |
| co09 | +0.13 | +0.06 | +0.06 | +0.06 | +0.03 | +0.03 | fail-small |
| co10 | +0.08 | +0.08 | +0.07 | +0.03 | +0.02 | +0.03 | fail-small |
| co11 | +0.11 | +0.05 | +0.08 | +0.05 | +0.04 | +0.02 | fail-small |
| co12 | +0.03 | +0.01 | +0.02 | +0.03 | +0.00 | -0.01 | fail-small |


## Record

- Calls: `results/p2-6r-calls.json` (1,440 entries; each with request ID, cost and the SHA-256 of model, settings, max_tokens and messages, re-verified at analysis). Analysis: `results/p2-6r-replication.json`. Tables generated by `experiments/p2_6r_replication.py --analyse` into `results/p2-6r-tables.md` (reproduced above).
- Engine odds 0.25 (revised before data from the map's 0.40 by lesson ls-om-p2-6r); no human odds. Scored outcome under §5: 0 (fail).

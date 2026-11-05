# P2-7. Shared format fingerprint: does a credence attributed to Sam deviate across formats the way the model's own does? (result)

Pre-registered in `experiments/p2-7-format-fingerprint.md` (commit `34182b6`, 2026-11-05 05:29:59 America/Denver; DEVIATIONS D15), seeded from CURBy-RNG pulse 1592214 (`2a958ae`). Design review (oversight-testbed `ledger/design-reviews/om-p2-7.md`): fix-first with 5 flaws (`2407d37`); fixes D15a–D15e (`1e13a58`) and D15f (`c630b0f`), confirmed at 06:14 (`1de9d49`), before the first call. The run went 06:14:52–06:17:41 America/Denver (`results/p2-7-run.log`). Engine odds 0.15 (map 0.25, lesson 0.20, D15a 0.15, all before data); human odds 0.70 (Sean's cockpit line `ho-20261105-051140-gfv`, for the map's original one-model event).

## In plain English

**Pre-registered verdict: fail.**

> On Haiku 5.5 and Sonnet 5.5 and Opus 5.5, on 34 statements from 17 of program 1's experiment-5 items and three graded formats, the format fingerprint of the ratings given for Sam did not match that of the model's own ratings on every model tested by the pre-registered rule (a self–Sam residual correlation of at least 0.5 of its reliability ceiling, beating a generic-link rival by at least 0.10 with its 95% interval above 0).

The per-model readings, as frozen:
- "On Haiku 5.5, the self–Sam residual correlation was +0.207 [-0.087, +0.442] of its ceiling, below 0.5."
- "On Sonnet 5.5, the self–Sam residual correlation was -0.098 [-0.366, +0.217] of its ceiling, below 0.5."
- "On Opus 5.5, the self–Sam residual correlation was +0.244 [-0.069, +0.556] of its ceiling, below 0.5."

**What this means, in plain words.**
- **The setup.** Program 1 found that each model's 0–100 rating, its "how many of 100 like this" count and its verbal answer disagree with each other in a way that depends on the statement. That is the model's own format fingerprint.
- **The question.** Here each model was asked the same three formats about what "Sam, a person who has read exactly what you have read here" thinks.
- **Sam's answers have a fingerprint of their own.** The statement-by-format quirks in the Sam answers came back in the second repeat: split-half reliability 0.89 (Haiku), 0.70 (Sonnet) and 0.71 (Opus). So the Sam ratings were not flat.
- **But it is not the model's own.** On every model the two fingerprints lined up far less than the noise allows. The correlation was +0.21, −0.10 and +0.24 of its ceiling, against the 0.5 bar, and none of the three intervals reaches 0.5.
- **What the bet asked, and what it found.** The bet asked whether the quirks of the model's own ratings come back when it rates for someone else. On this design they mostly do not.
- **How strong the "not" is.** The upper ends (0.44, 0.22, 0.56) mean a weak shared component, of up to about half the ceiling on Opus, is not ruled out.

**Beside the verdict, never in its place** (D15d, secondary, not scored):
- "Nearest analogue of the event on Sean's cockpit card (one model; here 34 statements × three formats, not the card's 80 × six; no margin over the rival): Haiku's ρ is +0.207 [-0.087, +0.442], which does not reach 0.5."
- "ρ ≥ 0.5 on every tested model (no margin over the rival): no."

**The pre-mortem** named Sam's ratings hedged toward 50 so that, on Opus, the match would not beat the generic-link rival.
- **The hedge happened, on every model.** Sam's ratings sat nearer 50 than the model's own. The mean distance from 0.5 per (statement, format) cell, self against Sam, was 0.29 against 0.21 on Haiku, 0.26 against 0.20 on Sonnet, and 0.30 against 0.22 on Opus. This is computed from the archived matrices in `results/p2-7-format-fingerprint.json`; it is descriptive and not pre-registered.
- **But it did not make Sam flat.** Sam's residuals were reproducible on every model.
- **The fail came one step earlier.** Every model failed at the 0.5 bar, before the comparison with the rival.

**Robustness and record:**
- Leave-one-item-out leaves every model at fail-ceiling: 0 flips.
- No bootstrap resample was undefined.
- 612 calls, 204 a model (Haiku thinking disabled, Sonnet `between_tools`, Opus low effort), all complete.
- **$0.9669** of the $1.50 cap (Haiku $0.01, Sonnet $0.19, Opus $0.77). **No refusal.**

**What it cannot say** (§6, D15e):
- Self and Sam differ in more than whose credence it is:
  - date;
  - direct against batch calls for Sonnet's and Opus's archived self data (Haiku's archive was direct);
  - 10 against 2 repeats;
  - the added Sam sentence, and "how likely does Sam think" against "how likely is it".
- A mismatch may come from any of these. P2-1 found that, on Haiku, the "how likely" wording reproduces across sessions at Q = 0.96 but changes when the framing changes.
- Three graded formats only, 34 statements, one item set, three Claude models.
- No claim is made about a represented credence, a theory of mind or simulation.

## Tables

Calls 612; cost $0.9669; refused 0; statements 34.

- Haiku 5.5 (`claude-haiku-5-5`, {"thinking": {"type": "disabled"}}, max_tokens 100): calls 204; cost $0.0094; refused 0; reading **fail-ceiling**
- Sonnet 5.5 (`claude-sonnet-5-5`, {"thinking": {"type": "between_tools"}}, max_tokens 1000): calls 204; cost $0.1878; refused 0; reading **fail-ceiling**
- Opus 5.5 (`claude-opus-5-5`, {"output_config": {"effort": "low"}}, max_tokens 1000): calls 204; cost $0.7696; refused 0; reading **fail-ceiling**

## Sentences (frozen, numbers filled in)

- On Haiku 5.5 and Sonnet 5.5 and Opus 5.5, on 34 statements from 17 of program 1's experiment-5 items and three graded formats, the format fingerprint of the ratings given for Sam did not match that of the model's own ratings on every model tested by the pre-registered rule (a self–Sam residual correlation of at least 0.5 of its reliability ceiling, beating a generic-link rival by at least 0.10 with its 95% interval above 0).
- On Haiku 5.5, the self–Sam residual correlation was +0.207 [-0.087, +0.442] of its ceiling, below 0.5.
- On Sonnet 5.5, the self–Sam residual correlation was -0.098 [-0.366, +0.217] of its ceiling, below 0.5.
- On Opus 5.5, the self–Sam residual correlation was +0.244 [-0.069, +0.556] of its ceiling, below 0.5.

## By model (point [95% item-bootstrap CI], 17 items resampled)

| statistic | Haiku 5.5 | Sonnet 5.5 | Opus 5.5 | role |
|---|---|---|---|---|
| self–Sam residual correlation / ceiling, ρ | +0.21 [-0.09, +0.44] | -0.10 [-0.37, +0.22] | +0.24 [-0.07, +0.56] | **event** (≥ 0.5) |
| ρ minus the generic-link rival's, Δ | +0.20 [-0.07, +0.42] | -0.16 [-0.44, +0.24] | +0.00 [-0.42, +0.45] | **event** (≥ 0.10, CI above 0) |
| raw self–Sam residual correlation | +0.19 [-0.08, +0.42] | -0.08 [-0.30, +0.17] | +0.19 [-0.06, +0.43] | secondary |
| raw self–rival residual correlation | +0.00 [-0.19, +0.17] | +0.05 [-0.23, +0.29] | +0.19 [-0.27, +0.53] | secondary |
| the rival's ρ | +0.00 [-0.20, +0.19] | +0.06 [-0.32, +0.38] | +0.24 [-0.35, +0.70] | secondary |
| split-half reliability of self residuals (10 repeats) | +0.98 [+0.95, +0.99] | +0.89 [+0.68, +0.98] | +0.89 [+0.78, +0.95] | gate (≥ 0.5) |
| split-half reliability of Sam residuals (2 repeats) | +0.89 [+0.81, +0.95] | +0.70 [+0.44, +0.84] | +0.71 [+0.51, +0.84] | gate (≥ 0.5) |
| shuffled-statement null: share with r ≥ observed | 0.0560 | 0.7430 | 0.0805 | secondary |
| residual SD, self / Sam | 0.209 / 0.161 | 0.102 / 0.080 | 0.035 / 0.046 | secondary |
| mean \|self − Sam\| (0–1 scale) | 0.220 | 0.133 | 0.126 | secondary |
| format means F1 / F5 / F6, Haiku 5.5: self | 0.50 / 0.50 / 0.57 | Sam 0.61 / 0.54 / 0.57 | | secondary |
| format means F1 / F5 / F6, Sonnet 5.5: self | 0.51 / 0.62 / 0.59 | Sam 0.60 / 0.60 / 0.60 | | secondary |
| format means F1 / F5 / F6, Opus 5.5: self | 0.59 / 0.60 / 0.58 | Sam 0.64 / 0.66 / 0.61 | | secondary |

Leave-one-item-out flips of the overall verdict: 0.

Secondaries, not scored (D15d): Nearest analogue of the event on Sean's cockpit card (one model; here 34 statements × three formats, not the card's 80 × six; no margin over the rival): Haiku's ρ is +0.207 [-0.087, +0.442], which does not reach 0.5. ρ ≥ 0.5 on every tested model (no margin over the rival): no.

**Verdict by the pre-registered rule: fail**


## Record

- Calls: `results/p2-7-calls.json` (612 entries; each with request ID, cost and the SHA-256 of model, settings, max_tokens, messages and schema, re-verified at analysis). Self data: program 1's archives, read only (`programs/entangled-mind/results/gm3b-calls.json`, `mm-gm3b-sonnet-calls.json`, `mm-gm3b-opus-calls.json`). Analysis: `results/p2-7-format-fingerprint.json`. Tables generated by `experiments/p2_7_format_fingerprint.py --analyse` into `results/p2-7-tables.md` (reproduced above).
- Scored outcome under §5: 0 (fail), for engine odds 0.15 and human odds 0.70.

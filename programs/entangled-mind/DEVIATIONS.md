# Pre-registration deviations

## D1 — Contentions come from the visible written reasoning, not the hidden thinking trace

**Date:** 2026-11-03 (before any pool, calibration, or test-set result existed)

**Original spec:** ask the base model with extended thinking on, capture the thinking trace, and split the hidden thinking trace into 5–16 discrete contentions.

**New design:** the base model is asked to reason step by step *in its visible response* before giving `FINAL ANSWER: YES/NO`. Only that visible written response goes to the contention extractor. Thinking stays on (adaptive, effort `xhigh`) so the model still deliberates. Its content is requested with `display: "omitted"`, so it is never returned, stored, or passed to any other call. Only the thinking token count is logged.

**Reason:** in the first pool attempt, the API's `reasoning_extraction` safeguard refused the extractor call (`claude-sonnet-5-5`, `stop_reason: refusal`), which was being handed the base model's thinking trace. We redesigned the pipeline rather than route around the safeguard. If any call in the pipeline is refused again, the run stops, records the refused call and its exact stop details in `results/refusal.md`, and does not reword or retry.

**Effect on interpretation:** the circuits encode the argument the model *wrote down*, which may be a tidied, post-hoc account of its deliberation rather than the deliberation itself. Every result in this repository should be read as being about the written reasoning.

### Findings that led here (pilot calls, 2026-11-03)

1. **Sonnet 5.5 emits no thinking block at all at `low`, `medium`, or `high` effort** on these items (tested on a bat-and-ball item and a letter-counting item). Adaptive thinking judged them not worth thinking about, so there was no trace to split. A thinking block appeared only at `xhigh` and `max`.
2. **Even at `xhigh`, the thinking block is only a short summary**, one or two sentences (67–98 thinking tokens on the pilot items), and the raw chain of thought is never exposed. It could not have supplied 5–16 contentions on its own.

## D2 — The redesigned extractor was refused too (run stopped)

**Date:** 2026-11-03

With D1 in place (base thinking requested with `display: "omitted"`, extractor given only the question and the visible written response), the first extractor call (q01) was refused again with `stop_reason: refusal`, category `reasoning_extraction`. Per the hard rule, the run stopped at once. Nothing was reworded or retried, and 0 of 60 questions completed. The refused call and its exact stop details are in `results/refusal.md`.

The prompt still had the shape the safeguard documents as a trigger: the input sat inside a tagged `<response>` section, and the system prompt asked for the writer's "deliberation" / "written reasoning" to be decomposed.

## D3 — Prompt redesigned per Anthropic's documented guidance for reasoning_extraction

**Date:** 2026-11-03 (before any pool, calibration, or test-set result existed)

Anthropic's [refusals documentation](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks) says `reasoning_extraction` fires on prompt *shape*:
- a `<thinking>`, `<reasoning>` or scratchpad section
- a `reasoning`, `thinking` or `trace` field in JSON output
- the model's private notes, or a running log of its reasoning
- reasoning asked for verbatim or in full

It also says that asking for a short explanation or the evidence behind a result is fine, and that the category has no fallback model. The fix is to change the prompt.

Both earlier designs had that shape. D1's base prompt asked the model to "reason step by step in writing". Both extractor prompts wrapped the input in a tagged section and asked for the writer's reasoning or deliberation to be split out.

**Redesign:**
- **Base call** (`claude-sonnet-5-5`): adaptive thinking at `xhigh`, `display: "summarized"`. The prompt asks for the answer plus a brief explanation of the main considerations for and against, and keeps the `FINAL ANSWER: YES/NO` line. There is no step-by-step instruction and no tagged section. The summarized thinking blocks and the visible answer are saved together as each question's **deliberation record** in `results/pool-run-1.json`. The thinking blocks are archived only and are never sent to any other call.
- **Extractor** (`claude-sonnet-5-5`): the visible answer is presented as a document: "Below is a short written argument answering a yes/no question." It lists the document's distinct claims as `claims[{text, confidence, lean}]`.
- **Relation judge** (`claude-haiku-5-5`): the input is a numbered list of claims, and the output is the pair table `pairs[{i, j, relation, strength}]`.
- Every string sent to the API (prompts, schemas, user templates) was checked for thinking / reasoning / trace / scratchpad / deliberation / step-by-step / tag markup and reworded where any appeared.

**Science impact:** unchanged from D1. The circuits encode the claims in the model's *visible* explanation, which is a short account of its considerations, not its internal deliberation.

If a call is refused after this redesign, the run stops and records the request ID and exact refusal in `results/refusal.md`. The next step is a support ticket. Nothing will be iterated further.

## D4 — Pool extended with 75 code-verified computational items

**Date:** 2026-11-03 (after the pool run, before any circuit was run on any pool item)

**What happened:** on the original 60-item pool, `claude-sonnet-5-5` at effort `xhigh` answered **all 60 correctly**. With no known-wrong items, the 10-wrong / 10-right test set cannot be formed and H2 cannot be tested.

**Change:** the pool was extended once with 75 yes/no items generated by `experiments/make_extension.py` (seed 404, `experiments/questions_extension.json`). The items are:
- primality of 8-digit numbers (primes vs. products of two 4-digit primes)
- Gregorian weekdays of dates from 1600 to 2400
- letter counts in sentences
- digit sums of powers of 2
- 5-digit × 5-digit products with near-miss claims
- prime counts in 100-wide intervals

Every answer is computed by the script, not hand-labelled, so a "wrong" model answer cannot be a labelling error on our side.

**Rule fixed in advance:** the base effort stays at `xhigh`, and the extension is used once. If the 135-item pool still yields fewer than 10 wrong items, the run stops and that is reported. Otherwise the split follows the pre-registration: 10 wrong and 10 right items at random (seed 2026), with everything else, including surplus wrong items, going to calibration. The calibration pool is therefore about 115 items, not 40.

**Effect on interpretation:** the wrong items will be mostly computation slips, not misconceptions or conjunction-fallacy errors. The experiment then asks whether the circuit flags the model's *calculation* errors. That is a narrower question than the original one about conflicting beliefs.

**D4 addendum (same day, before any extension item completed):** at `xhigh` effort, the first computational item made the base call think until it hit the 16,000-token cap, which costs about $0.16 per call. To stay inside the $10 budget:
- items are processed in shuffled order;
- a base call that hits the cap is recorded as *no answer* and excluded from the split, never counted as wrong;
- the extension stops as soon as the pool holds 13 wrong items, or when session API spend reaches $8.50.

This stopping rule shapes only which items exist. It is applied before any circuit is run, so it cannot select for any hypothesis.

## D5 — Base model changed to claude-haiku-5-5 to obtain errors

**Date:** 2026-11-03 (before any circuit was run on any pool item)

**Original spec:** base model `claude-sonnet-5-5`, with adaptive thinking run at effort `xhigh` (D1).

**What happened:** pool run 1 with `claude-sonnet-5-5` at `xhigh` answered **all 117 checkable items correctly**: the 60 original items plus 57 of the computational extension items. Another 10 extension items hit the 16,000-token cap and were excluded. The run was stopped before its last 8 extension items once this decision was made. With no known-wrong items, H2 cannot be tested. Run 1 is archived as `results/pool-run-1.{json,md}`.

**Change:** the base model is now `claude-haiku-5-5`, a weaker Claude model chosen to obtain errors. It runs at its **default** effort, with adaptive thinking and `display: "summarized"`. The extractor (`claude-sonnet-5-5`) and the relation judge (`claude-haiku-5-5`) are unchanged.

Pool run 2 covers every original and extension item except the 10 that hit the token cap in run 1. The test set is 10 wrong and 10 right items at random (seed 2026), and the rest form the calibration pool.

**Fallback, fixed in advance:** if Haiku gets fewer than 10 wrong, the test set is every wrong item plus the 10 correct items whose extracted claims give the model's answer the least net support (Σ confidence·lean / Σ confidence, signed toward the answer given). Stage 2 runs anyway, and the results state plainly that H2 is underpowered at that count.

**Unchanged:** the H2 criterion, the five arms, the encoding, the readout and the threshold rule.

Nothing extracted under run 1 can be reused, because contentions depend on the base model's own answer. Run 1's spend stays in `results/api-usage.md`.

## D6 — Second, harder question pool (Stage 2 run 2)

**Date:** 2026-11-03 (after Stage 2 run 1 was fixed and running, before any hard-pool result existed)

**Why:** the standard pool of trick puzzles, misconceptions and computation yielded only 4 known-wrong items on `claude-haiku-5-5`, out of 125. At that count H2 is underpowered.

**New pool:** `experiments/questions-hard.json`, 300 yes/no items, 150 yes and 150 no, built by `experiments/make_hard_pool.py` (seed 1729). Every item records its source and license.
- **120 SimpleQA items** (OpenAI simple-evals, MIT). Each is the question plus a candidate answer: the gold answer for half the items, and for the other half the gold answer of a different SimpleQA question with the same topic and answer type.
- **120 MMLU-Pro physics and chemistry items** (TIGER-Lab, MIT). Each is the stem plus either the correct option or a random wrong one. Stems that depend on seeing the option list are dropped. GPQA Diamond was not used: it is gated, and its authors ask that items not be published in plain text, which this public repository would do.
- **60 author-written claims**: 30 true and 30 plausible fabrications, each a near-miss of a true fact.

**Pipeline:** unchanged, with the same base prompt, extractor, judge, encoding, readout, threshold rule, arms and H2 criterion.
- The hard pool runs first through `claude-haiku-5-5` (pool run 3).
- If Haiku gets fewer than 30 wrong, the pool also runs through `claude-sonnet-5-5` at default effort (pool run 4), and both result sets are kept.
- An answer with no parseable `FINAL ANSWER` line is excluded, not counted as wrong.

**Split:** all wrong items (at most 40, at random), plus an equal number of right items at random (seed 2026). Everything else is the calibration pool.

**Budget:** $15 for runs 3 and 4 together, enforced in code.

## D7 — Pre-registered additions: arms F and G, bootstrap intervals, a 200-shuffle null for arm D

**Date:** 2026-11-03, written after Stage 2 run 2 was committed and before Stage 2 run 3 data were collected.

Two arms were added: **F**, the classical Ising twin of arm A, and **G**, the base model's self-reported confidence. Two statistics were added for every arm: AUROC with 95% bootstrap intervals, and a 200-shuffle null distribution for arm D in place of the single shuffle. Full definitions are in `experiments/preregistration.md`, Addendum A.

They are first applied as a re-scoring of run 2 (`results/stage2-run-2b.md`). Arms A–E are not re-run. H2 is unchanged, and the F/G comparison is reported alongside it.

## D8 — Witness run: readout calibration pinned to the measured qubits

**Date:** 2026-11-03, before submission.

`experiments/witness.md` specifies readout-calibration circuits "on the same two physical qubits". `witness_design.py` passed those circuits through the optimizing transpiler, which is free to move them onto other qubits. `experiments/witness_run.py` instead builds them directly on the physical qubits that each item's settings measure. They use only native gates (`x`, `measure`) and are submitted untranspiled.

The noisy-simulator prediction is recomputed with this corrected calibration and reported next to the hardware result. Circuits, settings, shots and pass rule are otherwise exactly as designed: 39 circuits, 4,000 shots each, one Batch. Sean approved the budget of about 45 QPU seconds.

## D9 — v2 training pool

**Date:** 2026-11-03 (before any v2 fitting, and before the v2 split existed)

**Pool:** `experiments/questions-train.json`, 598 yes/no items (302 yes, 296 no), built by `experiments/make_train_pool.py` (seed 2718). Every item records its source and license. The pool leans toward errors that come from deliberation rather than ignorance:
- **150 SimpleQA items.** None are reused from the hard pool.
- **200 MMLU-Pro items**: 50 each from biology, engineering, physics and chemistry. The Hugging Face `/filter` endpoint was still failing, so biology and engineering rows were paged through the public `/rows` endpoint, using the dataset's category blocks.
- **150 two-sided computed puzzles**, with every claim placed 3–15% above or below the exact value (fractions):
  - base rates
  - sampling without replacement
  - birthday problems
  - expected values
  - three-dice totals
  - a conditional coin
  - combinations
  - average speed (the harmonic-mean trap)
  - compound growth
  - power comparisons
- **98 code-verified claims**: element numbers and symbols with near-miss false versions, plus computed numeric facts with small off-by-one or near-miss false versions.

**Leakage guard:** any item whose question stem also appears in the run-2 hard pool is dropped. Two element claims duplicated hard-pool claims and were removed. The run-2 hard pool, and in particular its 80-item test set, stays a separate held-out set.

**Run:** base model `claude-haiku-5-5` with the unchanged pipeline (pool run 5). The budget is $20, enforced in code. The target is at least 120 wrong items.

**Split:** the train / validation / test split (60/20/20, seed 2026, stratified by wrong/right × item type) is locked in `experiments/split-v2.json` and committed before any fitting.

## D10 — QPU-seconds parsing bug (fixed)

**Date:** 2026-11-03

IBM Runtime reports a job's billed QPU time as `metrics()["usage"]["qpu_charge_time_seconds"]`. `backends.run_hardware` read `quantum_seconds`, which doesn't exist in this runtime, so it logged the Stage 1 job as 0.0 s when it had used 2 s.

`backends.qpu_seconds` now reads the correct key. `backends.repair_ledger` recomputed every ledger entry from the stored raw metrics, so the 420 s hard stop sums correctly.

The witness job had already been submitted with the old code, so its ledger entry is repaired the same way when it returns.

**D9b addendum: one supplement to the training pool (same day, before the split was locked and before any fitting).**

Partway through pool run 5, Haiku's errors came almost entirely from SimpleQA (20% wrong) and MMLU-Pro engineering, physics and chemistry (12–20%). It got 0 of 82 computed puzzles wrong, 0 of 48 verified claims, and 4% of biology items. The full pool would yield about 55 wrong items, against the target of at least 120.

One supplement of 450 items was added as t599–t1048 (`make_train_pool.py --supplement`, seed 2719):
- 300 MMLU-Pro items: 100 each from engineering, physics and chemistry. Science is the larger share, following the brief's "deliberation over ignorance" weighting.
- 150 SimpleQA items.

The supplement excludes every existing training item and the held-out hard pool. The original 598 items are unchanged.

Also handled in this addendum: an item whose explanation yields fewer than 5 claims after one retry is now recorded as excluded, not counted as wrong, instead of crashing the run. This happened once.

**Finding:** the two-sided computed puzzles do not elicit errors from Haiku 5.5. Its errors on this pool are ignorance-type (SimpleQA) and multi-step science, not the base-rate or harmonic-mean traps.

## D11 — Experiment 4 (quantitative Yearsley & Trueblood) pre-registered

**Date:** 2026-11-03, before any experiment-4 call.

Pre-registered in `experiments/exp4-yearsley-trueblood.md`, with items in `experiments/exp4-items.json`. Choices made at pre-registration:

1. **Items.** Only 4 co-occurrence items exist in `items-borrowed.json`, too few for a share-based rule. They were joined by the 4 Linda variants that convert cleanly to X/Y form (Bill, Priya, the analytical person, name-swapped Marta) and by 8 new author-written items (co05–co12), for 16 in all.
2. **Letter-copying check.** Swapping the A/B labels on both questions together cannot detect a model that copies its first *letter*: under any shared mapping, a repeated letter is also a repeated content answer. The check therefore uses crossed mappings, where Q1 and Q2 use different label mappings, and compares how often the content answers agree under same versus crossed mappings.
3. **"Beyond repetition."** The classical comparator is Kang (2026)'s symmetric repetition model, fitted per item, which predicts o_rep = r · (p_X − p_Y). The quantum claim is tested on o − o_rep as well as on o.
4. **Thinking disabled for the base calls,** following the borrowed protocol's "thinking off". The base model is `claude-haiku-5-5`.

The budget is $10, enforced in code. The experiment runs last in the queue.

**D11 addendum: R2 wording corrected (same day, before any experiment-4 call).** Rule R2 (the order effect is at least the fallacy size) is a consequence of the quantum model, but it is not unique to it. An updating classical model, in which each judgment updates the state before the next, also satisfies R2. Only the *static* classical twin is ruled out.

The overstated sentences were corrected in `experiments/items-borrowed.json` (rule R2 and the pre-registerable test) and in `experiments/exp4-yearsley-trueblood.md`. In experiment 4, meeting R2 is now read as "consistent with quantum or sequential-update classical; rules out the static twin", not as support for the quantum account. The pass rules' thresholds are unchanged.

## D12 — Version two pre-registered (before any fitting)

**Date:** 2026-11-03. The split was locked in `experiments/split-v2.json` (train 629 with 95 wrong, validation 210 with 31 wrong, test 209 with 32 wrong; stratified, seed 2026) and committed before this pre-registration. Both came before any fitting. Choices made here:

1. **Pass criterion.** "Exceeds the classical twin's AUROC by more than the width of both bootstrap 95% intervals" is read as **non-overlapping intervals**: A2's lower 95% bound must be above F2's upper 95% bound. The paired bootstrap difference is reported as well.
2. **Equal parameter counts.** A2 and F2 each have 8 scored parameters plus a flag threshold. To match that, L uses the 5 features named in the brief plus 3 more relation-web summaries (number of related pairs, mean |lean|, and the share of confidence leaning against the vote), giving 8 weights plus a flag threshold. L's bias term is left out because AUROC does not depend on it.
3. **Fitting uses exact noiseless statevector scores** (`v2.fast_quantum_probs`, verified equal to the Qiskit circuit at v1 values to 10⁻¹⁶). This makes A2 the strongest version of the quantum model. A noisy-simulator fit at about 1,000 train evaluations was not computationally feasible. The classical twin F2 is also exact.
4. **Shared fitting rule:** 400 random draws, then hill-climbing of the 10 best with 60 steps each (1,000 train evaluations), with the final candidate selected on validation AUROC. Seeds are A2 101, F2 202, L 303.
5. **Arm G** (self-reported confidence) needs one Haiku call per locked-test item. It is made at evaluation time and cached in `results/v2-arm-g-confidence.json`. On the run-2 held-out set it reuses the existing arm-G calls.
6. **Phase solver.** `v2.solve_phases_fast` is a vectorised form of `encoder.solve_phases`, with the same starts and update rule plus early stopping. It agrees within 2×10⁻⁶ rad. v1's solver is unchanged.

## D13 — Experiment 3 implementation choices (logged before any experiment-3 result)

**Date:** 2026-11-03

1. **Budget:** $10, as set in Sean's run instruction. This replaces the $4 cap written in the pre-registration. The expected cost of about $2.60 is unchanged.
2. **Secondary test 1 (do order effects exist at all?)** The pre-registration compares order effects with baseline split-halves. It is implemented as a permutation test that shuffles the order labels within each item-pair. This compares the observed |P(yes | i first) − P(yes | j first)| with what run-to-run variability alone produces, using the same 5 + 5 conversations. The 5 single-turn baseline runs per item are still collected and reported.
3. **Secondary test 2 (do the largest-Δᴼ pairs show bigger effects than the smallest?)** The pre-registration says paired Wilcoxon over items. It is implemented as a sign-flip permutation test on the per-item difference, because scipy is not a dependency.
4. **Exact U_k.** In the yes/no (X) basis, H_k's coupling and field terms are diagonal and −Z_k flips qubit k. So U_k = exp(−iγ₀H_k) is applied as exact 2×2 rotations, one for each configuration of the other qubits, with no truncation. This was checked to preserve the norm to 10⁻¹².

## D14 — Pre-registered additions: hedge baseline H and version 2.1 "honest hedge" encoding

**Date:** 2026-11-03 17:45 MST, before any test-set evaluation of v2 (the v2 fit was still running on train and validation).

These were added at Sean's request, prompted by the exploratory window vignette W4 (`paper/window-vignettes.md`), which notes that the encoding forces hedging claims into a yes or no camp. Full definitions are in `experiments/preregistration-v2.md`, Addendum B.

**Choices made here:**
- A no-lean claim is defined as |lean| ≤ 0.1. This was set from the train split's lean distribution only.
- The H primary score is the total confidence of no-lean claims, with H-count reported alongside.
- In v2.1, hedges are fixed at phase π/2 with lean 0, and are left out of the phase solver while keeping their couplings.
- The uncertainty term is U = confidence share of hedges, with a learned weight λ_h in [0, 2].
- A2.1 and F2.1 each have 10 parameters, matched to each other.
- v2.1 is evaluated on the locked test set once, after the v2 arms.

Because W4 was an exploratory observation on run-2 data, v2.1 is a hypothesis suggested by data from the run-2 hard pool. Its evaluation on the **run-2 held-out set** is therefore not independent of that suggestion. The **locked v2 test set**, which shares no item with run 2, is the clean test.

## D15 — Correction: the phase solver's frame drifts off the yes/no axis (encoding bug, documented and characterised)

**Date:** 2026-11-03. Prompted by Sean's frame check on window item h046. The work is exploratory and uses run-2 data only. It does not touch the locked v2 test set.

**Finding.** Two causes were possible: (a) a display convention error in `export_window.py`, or (b) the encoding itself. It is **not (a)**: the exported encode-stage Bloch azimuth equals the solver's φ exactly, claim for claim. It **is (b)**, in a more specific form than a free rotation.

The XY energy E(φ) = −Σ J_ij cos(φ_i − φ_j) − Σ lean_k cos φ_k is pinned by its lean anchors, so it cannot rotate freely. But the anchors are weak, with weight 1, against the relation couplings. The relation judge marks "supports" between claims that lean opposite ways when one makes the other more plausible. Those couplings pull the yes and no camps toward each other, and the ground state settles at a compromise off the readout axis. The energy is also symmetric under φ → −φ, so the direction of the tilt is arbitrary.

On h046, the yes claims sit at −62° and −71° and the no claims at −137° to −174°. Across the 225 run-2 items that have both camps:
- 20% have the yes camp more than 30° off axis;
- 20% have camps less than 90° apart;
- at least 10% have fully merged camps.

**Fix 1, a rigid frame pin (`encoder.pin_frame`), does not work.** It applies the least-squares rotation putting the yes camp at 0° and the no camp at 180°. A rotation only fixes a frame that has rotated, so it cannot pull merged camps apart. It changed nothing material.

**Fix 2, the correction: stronger anchors (`encoder.solve_phases_anchored`).** In the phase solve only, the lean field is scaled by λ = max(1, the largest total coupling Σⱼ|J_kj| of any claim in the item). This rule was fixed before its AUROC was computed. Effects:
- yes camps more than 30° off axis fall from 20% to 7%;
- the 10th-percentile camp separation rises from 0° to 147°.

The λ → ∞ limit, which puts every leaning claim exactly on the axis, is reported for reference.

**Effect on error detection, exploratory.** Exact noiseless scores on the run-2 test set:

| arm | as run | with the correction | at λ → ∞ |
|---|---|---|---|
| A0 | 0.49 [0.35, 0.62] | 0.47 [0.34, 0.61] | 0.47 [0.33, 0.60] |
| C | 0.68 [0.56, 0.79] | 0.67 [0.55, 0.78] | 0.67 [0.54, 0.78] |

Details are in `results/frame-fix-check.md`. The frame bug is real, but it does not explain the entangled arm's poor error detection.

**Disposition.**
- v1, v2 and every archived result keep the as-run solver, as pre-registered.
- Following Sean's rule ("if the fix matters, it goes into v2.1"), the correction is **not** added to v2.1, because it does not change the AUROCs. v2.1 stays a single change, the honest hedge. The v2.1 fit had not started when this was decided, so the correction could still be folded in, as a correctness fix, by a pre-registered amendment before `fit21`.
- `export_window.py` needs no fix.

## D16 — v2.1 amendment: fit noiseless, evaluate noiseless and on the noisy simulator

**Date:** 2026-11-03 18:36 MST, before any v2.1 fit or any test-set evaluation.

At Sean's instruction (`experiments/preregistration-v2.md`, Addendum C):
- A2.1 and F2.1 are fitted on exact noiseless statevectors and selected on validation.
- The selected models are evaluated once on the locked test set, noiseless, and A2.1 is also evaluated once on the noisy `ibm_fez` simulator (1,000 shots per item).
- F2.1 has no circuit, so it has only the noiseless evaluation.
- The pass criterion is applied to the noiseless comparison, with the noisy result reported alongside.
- Everything else in Addendum B is unchanged.

## D17 — Experiment 4 run 2 (graded form) pre-registered

**Date:** 2026-11-03 19:06 MST, before any run-2 call. Full design: `experiments/exp4-yearsley-trueblood.md`, "Addendum — run 2".

At Sean's request, the order test is re-run on run 1's 7 fallacy items with graded 0–100 ratings in both orders, 20 repeats per cell. Choices made here:
- Temperature is the model default (1.0); no explicit parameter is sent, because the API rejects one for this model.
- The graded analogue of "beyond repetition" is anchoring of the second rating on the first, fitted by regression.
- q_QQ and Γ are dropped, because they are defined only for binary answers. The marginal shifts OE_X, OE_Y and OSS are kept.

## D18 — Second base model (claude-sonnet-5-5): replication set-up

**Date:** 2026-11-03, before any Sonnet replication call.

At Sean's request, the hard pool (pool run 4, already defined in D6) and the training pool (new pool run 6) are run through `claude-sonnet-5-5` as base, at default effort with adaptive thinking. The extractor and judge are unchanged.

G, L, H and the **already-fitted** A2 and F2 are scored on Sonnet's errors, using the frozen v2 parameters in `results/v2-fit.json`. Nothing is refitted.

**Budget.** At about $0.02 per item, both pools (1,348 items) would cost about $27, against Sean's $15 budget. So:
- the pool runs are capped at $12 together and arm G at $3, both enforced in code;
- run 4 (the full hard pool) goes first;
- run 6 processes the locked v2 test questions first, so a budget stop still covers them, then as much of the rest as the budget allows.

What actually ran is reported in `results/sonnet-replication.md`.

## D19 — Experiment 4 run 2: the pre-registered anchoring estimator is near-tautological (logged after results)

**Date:** 2026-11-03, after run 2's results.

The pre-registered "beyond repetition" analogue regresses the second rating on the first across cells X→XY and Y→XY pooled. Because those two cells differ mainly in their first-rating means, the slope r ≈ o / (P(X) − P(Y)), so o − o_rep ≈ 0 regardless of mechanism. The run's verdict, "static classical twin (with anchoring) supported", is reported as pre-registered, but the results file says plainly that it does not show anchoring explains the effect.

An exploratory within-cell slope, using repeat-to-repeat variation only, cannot be estimated reliably either: at the default temperature the rating standard deviation is 0.00–0.05.

**Lesson for experiment 5 and later runs:** estimate anchoring only within cells, or manipulate the first rating directly.

## D20 — Sonnet replication stopped on a reasoning_extraction refusal

**Date:** 2026-11-03

During pool run 4 (hard pool, base `claude-sonnet-5-5`), the **extractor** call for question `h101` was refused with `stop_reason: refusal`, category `reasoning_extraction`. The request ID is `req_011Cgh7v49vVQNR6AgY3EDui`.

This is the first refusal since the D3 redesign. The same extractor prompt had run on 1,473 Haiku-based items without a refusal (pool runs 2, 3 and 5), and on 102 Sonnet-based items in this run before `h101`.

**Action, per the hard rule:**
- The run stopped at once, and nothing was reworded or retried.
- The record is in `results/refusal-sonnet-replication.md`, which is a copy of `results/refusal.md`.
- The next step is a support ticket with the request ID, which Sean will file.
- The Sonnet replication (D18) is halted at 102 of 300 hard-pool questions (12 wrong, $1.39), and pool run 6 was not started.
- No further Anthropic calls will be made until Sean decides how to proceed.

## D21 — Sonnet replication resumed with h101 excluded

**Date:** 2026-11-03, at Sean's decision, after D20.

Question `h101`, whose extractor call was refused (`reasoning_extraction`, request ID `req_011Cgh7v49vVQNR6AgY3EDui`), is **dropped** from pool run 4. It is recorded in `run_pool.REFUSAL_EXCLUDED`, and nothing was reworded or retried. The remaining hard-pool items and pool run 6 (the training pool) continue with the extractor unchanged.

If a second refusal occurs, the run stops again and is reported. The support ticket is filed separately, from `results/refusal-sonnet-replication.md`.

## D22 — Experiment 5 pre-registration frozen; pilot-item clarification

**Date:** 2026-11-03 20:15 MST, before any experiment-5 call.

`experiments/exp5-sequential-judgment.md` is frozen in its own commit, at Sean's go-ahead, with a $4 cap. One clarification was made at freezing:
- §7.1's "next 2 right" pilot items do not exist under the 5-per-category cap, which admits exactly the 20 selected right items across the 4 categories.
- The pilot therefore uses the next 2 right items in the uncapped ranking (h001, h170), alongside the next 3 wrong (h018, h088, h039).
- Re-running §3's selection rule from `results/pool-run-3.json` reproduces §9's 40 ids exactly and in order.

Nothing else in the design was changed.

## D23 — Experiment 5 implementation choices (fixed before any experiment-5 call)

**Date:** 2026-11-03, after the freeze (D22) and before the pilot. These are details the frozen text leaves open:

1. **Sub-question order.** S₁…S₄ are the four chain claims in claim-index order. O1–O4 follow the cyclic Latin square 1234, 2341, 3412, 4123. X_k omits S_k from O1.
2. **Turn structure.**
   - The first user turn is the opening context followed by the first question.
   - Each answer is structured output: {"rating": int} for ratings, {"answer": "yes"|"no"} for K1's choice, and {"reply": "continue"} for K0's filler.
   - A schema failure is recorded, and its row is dropped in analysis.
3. **Split arithmetic.** 384 chains at 60/20/20 is 230.4/76.8/76.8. Stratified by chain type (32 chains each), every type gets 19/6/6. The 12 leftovers are assigned by largest remainder, 2 to train, 5 to validation and 5 to test, at random with seed 2027. That gives exactly 230/77/77.
4. **G1's SD criterion** is computed over cells (chain type, rating position, anchor direction), with the SD taken across repeats within one anchor direction. This stops scale reversal from inflating dispersion.
5. **G2.** A pair passes if, in at least one order, the binarised minority share of either of its two questions (S_k or M) is at least 10%.
6. **Phase solver check (§5.1)**, run before freezing the split, with a maximum difference of exactly 0 in both cases:
   - the composed solver against `solve_phases_anchored`, on the 116 items with no hedges;
   - the composed solver against `v2.hedge_phases`, using a plain solve, on all 300 items.

## D24 — Experiment 5: pilot item h001 has only 3 competing claims

**Date:** 2026-11-03, before any experiment-5 call. The run raised an error while building the job list, so no API call had been made.

§3 states that all 40 candidates have at least 4 competing claims, and they do. The pilot item `h001`, chosen under the D22 clarification, has only 3. For any item with fewer than 4, the 4th chain slot is filled with the leaning, non-competing claim with the highest confidence × |lean|. This affects `h001` only. The 40 candidates' chain claims are unchanged, which was checked against `split-exp5.json`. Pilot data are never used in any test.

## D25 — Sonnet replication stopped on a second reasoning_extraction refusal

**Date:** 2026-11-03

- **Pool run 4** (hard pool, `h101` excluded) completed: 299 items processed, 1 hit the token cap, and **30 were wrong**. Cost $4.07.
- **Pool run 6** (training pool, locked-test questions first) then stopped on question `t368` (a SimpleQA item). The **extractor** call was refused with category `reasoning_extraction`, request ID `req_011CghAdzJQ9nFBMocCLUMhf`. 82 items had completed, 7 of them wrong, for $1.10.

Per Sean's rule ("if a second refusal occurs, stop again and report"):
- Nothing was reworded or retried.
- The replication is halted.
- The scorer (`sonnet_replication.py`) was **not** run, because its arm-G step would make further Sonnet calls.

The record is in `results/refusal-sonnet-replication-2.md`. Both refusals came on SimpleQA items with Sonnet as the base model, after 1,473 Haiku-based and 381 Sonnet-based items had gone through the same extractor prompt without one.

## D26 — Experiment 5 model details left open by the frozen text (fixed before any full-run data were examined)

**Date:** 2026-11-03. The full run was collecting data, unread, while these were fixed. Code: `experiments/exp5_models.py`.

1. **κ in A5.** κ scales the prep RZZ(κJ) and the evolution couplings by κ/κ₀, with κ₀ = π/4. So A5⁰ (κ = π/4, γ = 0.5, β = 0.4) reproduces v1's coupling strengths in both places.
2. **Evolution steps.** Every turn gets one evolution step before it, including K1's choice and K0's filler. The filler gets the step only, with no update.
3. **Π_M.** It has eigenvalue 1 for vote m > 0, 0 for m < 0 and ½ for m = 0, matching the readout's tie rule. The POVM and the choice updates use √ of these eigenvalues.
4. **D5 in practice.** In the yes/no basis the coupling and field terms are diagonal phases, so after dephasing only the mixer moves populations. D5 is therefore A5's prepared populations evolving by independent bit flips with probability sin²β per qubit per step. That is still exactly the dephased model, with 5 parameters, of which γ has no effect.
5. **F5 hedges.** A hedge has no "true" direction, so it is given a prior P(x = +1) = ½. Hedges are never asked about.
6. **BA5's parameter boxes**, which the text does not give: ω_supp, ω_con ∈ [0, 2] and ρ ∈ [0, 1]. C₀ is A5⁰'s prepared P(yes), before any evolution step. The "side" of a claim is the sign of its lean, compared with the model's original answer.
7. **The ablation, A5 with κ = 0,** is refitted with κ pinned at 0, under the same rule and budget (seed 505). The plain-solver sensitivity run, A5plain, is also refitted (seed 506).
8. **Rows with a schema failure.** A conversation containing one is excluded whole, and the count is reported.

**D26 addendum (before any full-run result):** in §7.5's verdict, "a signature contradicted" covers two cases: the QQ signature contradicted (mean-q CI excluding 0 on the large-OE pairs), **or** Kvam's commitment outcome (Δ_K CI entirely above 0, the opposite sign to the quantum prediction). The rest of the verdict table is applied as written.

## D27 — Sonnet hard pool scored offline, arm G not scored

**Date:** 2026-11-03, at Sean's request, after D25.

L, H, A2 and F2 were scored on Sonnet's 298 archived hard-pool records (pool run 4, `h101` excluded), using the frozen v2 parameters. The run used `sonnet_replication.py --offline`, in which every API client is blocked in code, and no call was made.

Arm G is marked **not scored**, because it needs Sonnet calls and the replication is halted. The 82 training-pool records of pool run 6 were not scored either, because Sean's instruction covered the hard pool.

## D28 — Addendum D (coupling ablation, F2+) and arm G on Sonnet's hard pool

**Date:** 2026-11-03 21:03 MST, before any ablation score or any Sonnet arm-G call.

- **Addendum D** (`experiments/preregistration-v2.md`): A2(κ=0) frozen, and F2+ (F2 plus A2's per-claim tilted-readout marginal, 10 parameters against A2's 9) fitted on the v2 train split. Each is scored once on Haiku's locked test set and on Sonnet's 298 hard-pool records, with the decision rule fixed in advance.
- **Arm G on Sonnet** (Sean's instruction): one self-confidence call per hard-pool item to `claude-sonnet-5-5`. This is the base model, not the extractor, and it sees only its own visible answer. The budget is $2, enforced in code. Any refusal stops the run and records the request ID, with nothing retried.

## D29 — Dates use local America/Denver time throughout

**Date:** 2026-11-03, at Sean's instruction.

Some documents carried 2026-11-04 for work done on the evening of 2026-11-03 Denver time: the UTC date, or a wrong date. Git's local timestamps (MST, UTC−7) are the reference. From now on, every date in the repository is local.

**Corrected:**
- D14 and D15 above;
- the writing dates of Addenda B and C in `experiments/preregistration-v2.md`;
- the writing date of `experiments/exp5-sequential-judgment.md`.

The two pre-registration files are frozen. **Only the expression of the date changed; no instant and no word of the design.** For example, "2026-11-04 00:45 UTC" became "2026-11-03 17:45 MST", which is the same moment. The exp5 text's "Written 2026-11-04" was simply wrong: it was written at 19:19 MST on 2026-11-03 (`2dc435b`).

Also corrected:
- `experiments/exp4-run-3.md`, `paper/next-steps.md`, `paper/the-entangled-mind-v3.md` and `paper/references.bib` (a comment);
- the hand-written Reading section of `results/stage1-run-1.md`.

**Not changed:**
- machine-written UTC fields in `results/` (the IBM usage ledger, the job-status log, the calibration tables) and in archived JSON, which their writers produce and `experiments/reproduce.py` checks byte for byte. Switching those writers to local time is a code change, logged separately if made;
- commit messages, which cannot be edited. One says "2026-11-04" (`34f5de4`).

## D30 — Addendum E: the frozen F2+ on Haiku's run-2 held-out set

**Date:** 2026-11-03 21:49 MST (the commit time of `52e80a0`). Pre-registered in `experiments/preregistration-v2.md`, Addendum E (`52e80a0`), before the scoring, at Sean's go-ahead.

The frozen F2+ was scored once on the run-2 held-out set (40 wrong, 40 right), with no refitting and no API calls. Its AUROC was 0.80 [0.69, 0.88]:
- F2+ − A2 = −0.019 [−0.073, +0.029];
- F2+ − A2.1 = −0.037 [−0.089, +0.012];
- F2+ − F2 = +0.088 [+0.014, +0.167].

**Outcome 1:** Haiku's held-out edges are also single-claim readout geometry, carried by a classical model. Results are in `results/sonnet-ablation.md` (Addendum E section) and `results/heldout-f2plus.json`.

## D31 — Machine-written timestamps switched to America/Denver

**Date:** 2026-11-03, following Sean's rule (relayed with D29) that every date in the repository uses local America/Denver time.
- The IBM usage ledger keeps UTC in its JSON, but `results/ibm-usage.md` now shows local time.
- `results/ibm-calibration.md`'s "Job ran at" line is now MST: Stage 1 ran at 16:06 MST, which is 23:06 UTC.
- `check_job.py` now writes local time. The existing `results/ibm-job-status-log.md` was converted once, and its instants are unchanged.
- Both tables were regenerated from their archived JSON by their writers, so `reproduce.py` still matches byte for byte.

## D32 — Experiment 5 analysis fix: tolerance in the a priori QQ sub-test (found after results)

**Date:** 2026-11-03, after experiment 5's first results were written.

The a priori sub-test compares order effects on each item's two QQ pairs, ordered by predicted non-commutativity |sin Δφ|. The analysis first compared these values with exact floating-point inequality. After the anchored phase solve, almost every chain claim's |sin Δφ| is 0 up to solver round-off (10⁻¹⁶–10⁻⁹), so round-off decided which pair counted as "larger". That gave a spurious 28 wins to 9 losses (p = 0.001) over "37 items".

Treating differences of 10⁻⁶ or less as ties, the tolerance already used for the encode-stage non-commutativity count, leaves 3 items with genuinely distinct predictions: 1 win, 2 losses, p = 0.875. The markdown was regenerated from the archived JSON, and nothing was refitted.

The pre-registered design is unchanged, and so is the verdict, which does not use this sub-test. The selection of QQ pairs for the many items whose claims all sit at |sin Δφ| = 0 was made by `qq_pairs` before any data. It is therefore effectively arbitrary on those items, which is consistent with §8.6's expectation that most claims commute.

## D33 — Experiment 4 run 3 frozen with a one-scale amendment; experiment 5 single-scale re-run pre-registered

**Date:** 2026-11-03 22:59 MST, before any call in either run.
- **Experiment 4 run 3** (`experiments/exp4-run-3.md`): frozen with an amendment.
  - Every rating prompt states one scale direction, "0 = certainly false, 100 = certainly true", per experiment 5's anchor finding.
  - The provided values A are fixed from archived means (`experiments/exp4-run-3-anchors.json`).
  - If r₁ is collinear with A, the fit falls back to two parameters (β₂ unidentified).
  - The point values used in the rules are fixed.
  - Budget $2, enforced in code.
- **Experiment 5 run 2** (Addendum in `experiments/exp5-sequential-judgment.md`): B0 and the QQ block re-run on the first 10 candidates, anchor (a) only.
  - It is descriptive, with no refitting, and the reading is fixed in advance.
  - Budget $1, enforced in code.

## D34 — Overnight gold-map run, 1 of 6: direction 9 (NSIT on archived experiment 5 data) pre-registered

**Date:** 2026-11-04 03:48 MST (the commit time of `7f0dd3e`), before the analysis. Sean's overnight brief runs six gold-map directions in order, each pre-registered in its own commit before its first call, every new design on one scale direction only, with stop-on-refusal for every call.
- **Direction 9** (`experiments/gm9-nsit.md`) is a $0 analysis of the archived experiment 5 conversations. It uses anchor (a) only, six NSIT families, a within-cell permutation test, and Holm correction.
- **Results files** for the overnight run open with a hand-written "In plain English" section. `reproduce.py` excludes that section from its comparison, as it already does for "## Reading".

## D35 — Overnight run, 2 of 6: direction 3's free look (anchor-direction gap against errors) pre-registered

**Date:** 2026-11-04 03:50 MST (the commit time of `a1bc421`), before the analysis.
- `experiments/gm3a-anchor-gap.md`: a $0 analysis of the archived experiment-5 B0 conversations.
- **Primary score:** the per-item |gap| between the two scale directions. **Primary statistic:** its AUROC for the model's hard-pool errors.
- This is the only overnight analysis that uses both scale directions, because the gap between them is its subject. The directions are compared, never pooled.

## D36 — Overnight run, 3 of 6: direction 1 (self-versus-other confidence) pre-registered

**Date:** 2026-11-04 03:52 MST, before any call. Recorded in `experiments/gm1-self-knowledge.md`.

**Changes from the gold map's sketch,** made before freezing on the literature session's full-text reads:
- **Primary statistic: the judge × author interaction.** I = self cells − cross cells. It replaces "a positive self advantage on both authors", because judge capability dominates per-author comparisons (Xiao et al. 2509.24988, Table 23). The per-author advantages are still reported.
- **Matched framing on the originals.** All four cells are run fresh with one "another assistant" prompt, so self and cross cells differ only in authorship. The archived "you gave" self ratings are used for a framing comparison.
- **The paraphrase arm has its own recognition check.** Panickssery et al. only proposed a paraphrase control and never ran one.
- **The disagreement subset means the authors' correctness differs** (Ashuach et al.): 26 questions.

**Budget and stops:** $3, enforced in code. The steps run in a fixed order, so a cap stop truncates the least important step. The run stops on any refusal.

**Timestamps:** D34 and D35 were corrected to their commit times (03:48 and 03:50) per the America/Denver rule. The literature session flagged both.

### D36 amendment — direction 1's run order, made while step 1 was running and before steps 3 and 4 ran

**Date:** 2026-11-04 03:58 MST.

**The problem.**
- The matched-framing Sonnet calls cost about $0.0037 each, against the $0.003 assumed from D28. The judge writes more about another assistant's answer.
- At that rate, steps 1–4 would total about $3.30, over the $3 cap.

**The change.**
- The run was stopped after step 2 completed. Both steps are cached, and no call was lost.
- It restarts in a new order:
  1. Haiku's recognition calls (120 calls, about $0.02);
  2. step 3, the paraphrase 2×2;
  3. Sonnet's recognition calls, for as long as the cap allows.
- The cap stays at $3. Nothing else in the design or the analysis changes.
- If Sonnet's recognition check is truncated, the results report how many of its calls ran.

## D37 — Overnight run, 4 of 6: direction 2 (shown, redacted and planted transcripts) pre-registered

**Date:** 2026-11-04 03:58 MST, before any call. Recorded in `experiments/gm2-self-conditioning.md`, with the planted values fixed in `experiments/gm2-planted-values.json`.

**Design.**
- First 10 experiment-5 items; chains O1–O4 and MF; anchor (a) only.
- Four conditions, 10 conversations each.
- Budget $1, enforced in code; stop on any refusal.

**Change from the gold map:** planted values are **±15** points rather than ±30, on the literature session's full-text read of Kumaran et al. 2507.03120.
- A planted answer must be plausible and must sit in the model's own turn.
- In experiment 4 run 3, the model rejected provided ratings 30 points away.

**Primary:** R = OE_redacted / OE_shown, with an item-bootstrap CI read against 0.5. A permutation gate checks first that the shown condition has an order effect.

## D38 — Overnight run, 5 of 6: direction 3's six-format run pre-registered

**Date:** 2026-11-04 04:02 MST, before any call. Recorded in `experiments/gm3b-format-invariance.md`.

**Design.**
- The 160 chain claims × 6 formats × 10 repeats, on Haiku with thinking disabled.
- Budget $1, enforced in code; stop on any refusal.

**Changes from the gold map.**
- **The reversed 0–100 scale is replaced by a 7-point verbal scale,** per the overnight rule of one scale direction in every design.
- **The model comparison is a 2-fold held-out-repeat log-likelihood** of one credence per claim (L1) against one per claim and format (L6).
- **The "CbD-style consistency test" is not attempted.** The formats have no shared outcome space.
- **The precedent is cited:** Smolin & Wilder 2609.07943, which found single latents fit capable models well. The gold map's P falls from 0.45 to 0.25.

**Check before freezing.** The fitting code was tested on simulated data.
- With one latent and monotone links, ΔLL was −8.2 per claim and 0% of claims were positive.
- With format-specific latents, ΔLL was +36 and 100% were positive.

## D39 — Overnight run, 6 of 6: direction 4 (the evidence-seeking menu test) pre-registered

**Date:** 2026-11-04 04:05 MST, before any call. Recorded in `experiments/gm4-evidence-seeking.md`. The menus and per-claim scores are fixed in `experiments/gm4-menus.json`, built by `experiments/gm4_menus.py`.

**Design.**
- The 40 items × 3 menus × 10 repeats, on Haiku with thinking disabled.
- Budget $0.50, enforced in code; stop on any refusal.

**Additions from the literature session's reads.**
- A most-uncertain baseline, to check whether EIG is confounded with the most uncertain-sounding claim.
- Jhaveri et al.'s confirmatory-testing finding, as the expected alternative.
- The gold map's P falls from 0.25 to 0.20.

**Check before freezing.** The analysis code was tested on simulated choices.

### D36 amendment 2 — direction 1 crashed on a token-cap judge call; lost calls bounded, cap tightened

**Date:** 2026-11-04 04:07 MST.

**What happened.**
- In step 3 (the paraphrase 2×2), one Haiku judge call hit max_tokens: 4,000 tokens, with the arm-G default thinking. It was not a refusal.
- The runner treated it as a crash. Calls completed after the last cache save (at 1,600 calls) were lost, along with the token-cap call itself.
- The last save was at 04:05:14 and the crash at 04:05:30. At the run's measured rate, that is about 30–50 calls of about $0.003, so **at most $0.20**.
- Recorded spend is $2.558, so true spend is at most about $2.76.

**Changes.**
- **The cap** is now $3 minus that $0.20 bound, enforced as $2.80 of *recorded* spend. The truncation order is unchanged: the rest of step 3, then Sonnet's recognition check.
- **A token-cap judge call** is recorded as no rating and dropped from its cell. This follows the project's existing rule for token-cap answers (stage 1).
- **The lost calls are re-issued** with identical parameters, because they have no record. One of them is the token-cap call: it was not refused, and its identity was not recorded.
- **The shared runner** (`experiments/gm_common.py`) now saves its cache every 50 calls and on any error, and stops cleanly. This applies to the remaining overnight runs.

## D40 — Biomimetic run, 1 of 5: confidence-gated confirmation on the archived run-3 calls pre-registered; revision-2 criteria adopted for all five

**Date:** 2026-11-04 05:08 MST, before `results/exp4-run-3-calls.json` was opened for this analysis.

**Sean's instruction.** After direction 4, merge the biomimetics branch, then run five tests in this order:
1. the three $0 analyses (confirmation on the run-3 calls, serial-position weights, contrast sign on the single-scale QQ data);
2. the sampling identity ($0.05);
3. serial dependence with run 3's anchors as the model's own answer ($0.23).

Each is pre-registered before its archive is opened or its first call, on one scale direction throughout.

**Revision 2 of the map.** Sean's list follows revision 1 of `paper/biomimetic-map.md`. The branch as merged carries revision 2 (`f824e14`, 04:27), in which full reads corrected these tests. The five tests are run as Sean listed them, at his budgets, with revision 2's corrected criteria wherever it corrects them:
- **Confirmation:** consistency is coded by sign relative to 50, as primary. It is read as a low-power test that does not single out confirmation.
- **Serial position:** the U-shape exclusion is the LCA's falsification test.
- **Contrast sign:** run as a descriptive assimilation/contrast check. It is not a normalization test, because sequential normalization is untested in the source paper.
- **Sampling:** the item-level Z slope is primary, and Z ≈ 0 is secondary.
- **Serial dependence:** own > other is the source test, and the "sign flip by source" prediction is withdrawn.

Revision 2's other recommendations are not run, because Sean did not list them:
- K1/K0 sensitivity;
- the variance shape as a separate $0 analysis (it is reported inside the sampling run);
- the distance and lag cells;
- the prime × confidence test.

**Recorded in:** `experiments/bm3-confirmation.md`.

## D41 — Biomimetic run, 2 of 5: serial-position weights pre-registered

**Date:** 2026-11-04 05:08 MST, before the archive was opened for this analysis. Recorded in `experiments/bm7-serial-position.md`.
- The data are experiment 5's O1–O4 chains, anchor (a) only.
- Position weights are fitted with item fixed effects.
- The primary reading is revision 2's U-shape exclusion for the LCA.

## D42 — Biomimetic run, 3 of 5: contrast or assimilation on the single-scale QQ data pre-registered

**Date:** 2026-11-04 05:08 MST, before the archive was opened for this analysis. Recorded in `experiments/bm9-contrast.md`.
- The data are the QQ conversations on anchor (a): run 1 is primary and run 2 is the replication.
- The test regresses the shift in M on the level of the S rating, with the content push as a covariate.
- It is not a normalization test (map revision 2, §3.10).

## D43 — Biomimetic run, 4 of 5: the PT+N identity and its Z slope pre-registered

**Date:** 2026-11-04 05:09 MST, before any call. Recorded in `experiments/bm2-sampling-identity.md`.

**Design.**
- 16 exp-4 items × 4 statements × 20 repeats, on one scale.
- Budget $0.10, enforced in code; stop on any refusal.

**Primary test:** the item-level Z slope (map revision 2), with **split halves**. A check on random ratings before freezing showed that shared repeat noise alone gives b ≈ +0.95 without the split.

**Secondary test:** mean Z within ±0.05.

## D44 — Biomimetic run, 5 of 5: source dependence (run 3's anchors as the model's own answer) pre-registered

**Date:** 2026-11-04 05:11 MST, before any call. Recorded in `experiments/bm1-serial-dependence.md`.

**Design.**
- Run 3's 16 items and ±30 anchors, with each anchor planted as the model's own earlier answer. The comparison is run 3's archived "another person" cells.
- R = 40; one scale.
- Budget $0.40 (estimate $0.23), enforced in code; stop on any refusal.

**What it shares with direction 2 (D37):** the planted value sits in the model's own assistant turn, in its structured-output format, with the same model and settings. Direction 2's result, and biomimetic tests 1–4, were known at freezing.

**Readings (map revision 2):**
- own > other means source-dependent self-consistency;
- attraction from both sources means stimulus-history serial dependence;
- revision 1's sign-flip prediction is withdrawn.

## D45 — Robustness wave, 1 of 3: direction 2 on all 40 experiment-5 items pre-registered

**Date:** 2026-11-04 06:30 MST, before any call. Recorded in `experiments/gm2b-self-conditioning-40.md`, with the planted values fixed in `experiments/gm2b-planted-values.json`.

**Design.** Identical to D37.
- The 10 items already run are reused as archived; the other 30 are run now, at about $1.6.
- Budget $2.50, enforced in code; stop on any refusal.

**Planted M values for the 30 new items** come from run-1 anchor-(a) first turns identical to B0, because run 2's B0 covers only the first 10.

**Reporting.** Primary on all 40, with two further sets:
- replication on the 30 new items;
- sensitivity without h191 and h261.

Concentration and within-order SD are reported alongside.

**Code.** `gm2_self_conditioning.analyse` was split into `compute()` plus the writer. The output is unchanged, and `reproduce.py` still matches.

## D46 — Robustness wave, 2 of 3: held-out-format prediction pre-registered

**Date:** 2026-11-04 06:33 MST, before the fit. Recorded in `experiments/gm3c-heldout-format.md`. Cost $0: last night's six-format data.

**Design.** Each format is predicted from the other five by the one-credence model L1, with 5 item folds and even/odd repeats, and compared with the format's own split-half ceiling.

**Primary:** mean Q = R²_cross / R²_ceiling, read against 0.75 and 0.5.

**Check before freezing.** The code was tested on simulated data. A one-belief world gave Q = 1.06 [1.04, 1.09]; a format-specific world gave 0.21 [0.14, 0.29].

## D47 — Robustness wave, 3 of 3: the biomimetic §3.0 shared test (source × distance × lag) pre-registered

**Date:** 2026-11-04 06:37 MST, before any call. Recorded in `experiments/bm0-source-distance-lag.md`.

**Cells.**
- own and other at d = ±10 and ±60, lag 0, R = 10;
- own at ±30, lag 3, R = 20;
- reused: own ±30 lag 0 from bm1 (R = 40) and other ±30 from run 3 (R = 40).

**Budget:** $0.50, enforced in code; stop on any refusal.

**Changes from map revision 2's §3.0.**
- R = 10 rather than 20 in the new distance cells, to fit the budget.
- The lag arm at ±30 only.

**Run order.** The run waits for D45 to finish, so the two API runs do not compete. The analysis was tested on simulated data before freezing.

---

# Multi-model branch (`multi-model`): entries DM1–DM6

Numbered DM so as not to collide with D-entries written on `main` at the same time. Budget set by Sean: **$20** for the three replications and **$3** for the calibration demonstration, allocated here.

## DM1 — Multi-model set-up: settings, batch runner and a cost pilot

**Date:** 2026-11-04 07:45 MST, before any pre-registration on this branch.

**Settings.** The paper's runs disable thinking on Haiku. The other two models do not allow that:
- `claude-sonnet-5-5` rejects `thinking: disabled`; its thinking-off mode is `thinking: {"type": "between_tools"}`;
- `claude-opus-5-5` cannot disable thinking at any effort, so it runs at effort `low`, the minimum. Its thinking text is never returned, and no thinking block is ever placed in a later turn.

`config.PRICES` gains Opus 5.5 at $4 / $20 per million tokens.

**Batch runner.** All calls on this branch go through the Message Batches API, at 50% of list price (`experiments/mm_common.py`). The overnight stop rules are kept:
- a cap per run, checked before each batch is submitted;
- the run stops at the first refusal, with the batch ID and message ID recorded (batch results carry no HTTP request ID);
- API errors are resubmitted unchanged, at most twice;
- max_tokens hits are recorded as no answer.

**Pilot** (`results/mm-pilot-calls.json`, **$0.031**).
- Contents: 12 synchronous calls (Sonnet and Opus: two six-format prompts and a 3-turn direction-2 conversation each, with a planted and a redacted turn; one Opus base answer and one Opus matched-prompt judge call), plus a 2-request batch.
- Item: hard-pool question h002, which is not one of the 40 experiment-5 items. It is one of direction 1's 298 questions; the pilot's Opus answer to it is not used.
- Findings:
  - the batch API accepts both settings with structured outputs, and returned in about 2 minutes;
  - per call, Sonnet ≈ $0.0008 and Opus ≈ $0.0016 single-turn, ≈ $0.003 in later multi-turn turns (Opus thinks briefly there even at low effort);
  - an Opus base answer ≈ $0.011 on an easy question;
  - edited assistant turns are accepted by both models.

**Allocation of the $20** (caps at the batch rate, enforced in code; unspent cap is not moved between runs):

| run | design | cap |
|---|---|---|
| DM2, six formats, Sonnet | 80 claims × 6 × 10 | $2.20 |
| DM2, six formats, Opus | 80 claims × 6 × 10 | $4.30 |
| DM3, self-knowledge, Sonnet × Opus | Opus answers 298 questions; 3 new judge cells × 298 | $4.60 |
| DM4, transcripts, Sonnet | 10 items × 5 chains × 4 conditions × R = 4 | $2.40 |
| DM4, transcripts, Opus | same | $6.00 |
| pilot | | $0.03 |
| **total** | | **$19.53** |

## DM2 — Multi-model replication 1 of 3: six formats on Sonnet and Opus pre-registered

**Date:** 2026-11-04 07:50 MST, before any call for this test. Recorded in `experiments/mm-gm3b-format-invariance.md`.

**Design.** D38's design and analysis, unchanged, on 80 of the 160 claims: the chain claims of experiment-5 candidates 1–10 and 21–30, i.e. 10 items Haiku answered wrongly and 10 it answered rightly.

**Reference.** The Haiku reference on the same 80 claims (from D38's archive) was computed while the code was being tested, before freezing: ΔLL +19.42 [+15.40, +23.21], 86% positive.

**Secondary.** Test F′ (D46) runs on the new calls with its frozen code, which forms 3 item folds at 20 items.

## DM3 — Multi-model replication 2 of 3: self-knowledge with Sonnet × Opus pre-registered

**Date:** 2026-11-04 08:05 MST, before any call for this test. Recorded in `experiments/mm-gm1-self-knowledge.md`.

**Design.** Opus answers direction 1's 298 questions with the base prompt and base settings. Sonnet and Opus then judge each other's answers, and Opus its own, with D36's matched prompt and settings. SS is D36's archived cell.

**Primary.** I = SS + OO − OS − SO, with D36's reading.

**Not run, for budget:** the paraphrase and recognition arms.

**Cap:** $4.60 (batch rate).

## DM4 — Multi-model replication 3 of 3: transcripts on Sonnet and Opus pre-registered

**Date:** 2026-11-04 08:10 MST, before any call for this test. Recorded in `experiments/mm-gm2-self-conditioning.md`.

**Design.** D37's design and analysis, unchanged, at **R = 4**: 800 conversations per model.

**Planted values.** Set by D37's rule from each model's own first-turn ratings (16 per question), fixed after wave 1.

**Running.** Batch waves, one per turn.

**Budget fallback.** Checked after every wave; it drops a repeat index while the projected total exceeds the cap.

**Reference.** The Haiku reference at R = 4 (D37's archive, repeats 0–3) was computed while the code was being tested, before freezing: R = 2.01 [1.04, 4.43].

**Caps:** $2.40 (Sonnet) and $6.00 (Opus).

## DM4a — Opus cost above the pilot estimate: DM2's Opus run budget-stopped; DM4's Opus cap re-set before any DM4 call

**Date:** 2026-11-04 08:20 MST. No DM4 call had been made, and no DM2 answer had been looked at; only per-call costs were read.

**What happened.**
- DM2's first Opus chunk (1,600 calls) cost **$3.10**, about $0.0019 per call at the batch rate, against the $0.0009 estimate.
- The costs imply about 120 thinking tokens per call. The pilot's single-turn calls, on an easy claim of h002, had none.
- The $4.30 cap therefore stopped the run before the second chunk, as pre-registered.
- **DM2's Opus arm stands at 1,600 of 4,800 calls.** These complete 26 claims (items 1–6 and 2 claims of item 7, all items Haiku answered wrongly), plus 40 calls of a 27th claim. It is reported as budget-stopped, with D38's analysis run on the 26 complete claims and labelled as such. It is not resumed.
- Sonnet's cost per call is on the estimate ($0.0004).

**Amendment (DM4 only, Opus arm).** At this rate DM4's Opus arm would cost about $9.5 at R = 4. Its $6.00 cap would force the fallback to R = 2. DM1's rule that unspent cap is not moved between runs is therefore replaced, for this arm only:
- **DM4's Opus arm runs last,** after every other DM run has finished.
- **Its cap is fixed at its start:** $20 minus all other recorded spend on the branch (pilot, DM2, DM3, DM4 Sonnet), minus $0.10, written to `results/mm-gm2-opus-cap.json` before its first call.
- The per-wave fallback (R = 4 → 3 → 2) is unchanged.

The rule depends only on costs, and it was set before any DM4 data existed.

## DM6 — Consequence demonstration: calibration (ECE) under two formats and two question orders pre-registered

**Date:** 2026-11-04 08:35 MST, before any call for this test. Recorded in `experiments/cal-format-order.md`.

**Design.**
- Protocol: Tian et al.'s (2023) Verb. 1S top-1, verbatim (format P), and the same template with a frequency in place of the probability (format F).
- Models: Haiku and Sonnet, on the 300 hard-pool questions.
- Conditions:
  - fresh, single-question calls in two replicates;
  - ten-question conversations, in forward and reversed order (30 blocks, `random.Random(4041)`).
- ECE: 10 equal-width bins.

**Primary.** ΔECE between formats and between orders, with paired block-bootstrap CIs (seed 4042). The fresh replicate difference is the noise baseline.

**Budget.** $3, separate from the $20: caps $0.30 (Haiku) and $2.60 (Sonnet), batch rate.

**Testing.** The code was tested on random fake answers before freezing; no call had been made.

## DM2a — DM2's Sonnet arm stopped by the runner's safety factor, not by its cap; resumed in smaller chunks

**Date:** 2026-11-04 08:50 MST. Only costs had been read; no DM2 answer had been looked at.

**What happened.**
- After 3,200 of 4,800 calls ($1.36), the third 1,600-call chunk was projected at $0.85: the observed $0.000425 per call × 1.25 safety factor. That made $2.21 against the $2.20 cap, so `mm_common` refused to submit it.
- The expected cost of the chunk is about $0.68, which would end the arm at about $2.04, under its cap.

**Amendment.** The remaining 1,600 Sonnet calls are submitted in chunks of 400, each still checked against the $2.20 cap with the same factor. The cap and every other rule are unchanged. The Opus arm stays stopped (DM4a).

## DM5 — Multi-model replications: what ran and what was found

**Date:** 2026-11-04, after the runs. Summary in `results/multi-model.md`. No call was refused.

**Spend:** $16.28 of the $20. Pilot $0.03; DM2 Sonnet $2.04, Opus $3.10 (budget-stopped); DM3 $4.03; DM4 Sonnet $2.19, Opus $4.89 (DM4a cap $8.51).

**DM4's Opus fallback.** After wave 1, the projection ($8.74 at R = 3) exceeded the cap, so the fallback ran at **R = 2**. Later waves cost less per call than wave 1, so R = 3 would in fact have fitted. The rule makes the drop irreversible, which is why $3.72 is unspent.

**Readings:**

| test | Sonnet | Opus |
|---|---|---|
| DM3, self-knowledge (Sonnet × Opus pair) | **no self-advantage**, I = −0.045 [−0.107, +0.017] | (same test) |
| DM4, transcripts | **question-driven**, R = 2.95 [0.99, 12.55] | **leaning question-driven (not decisive)**, R = 0.93 [0.06, 7.31] at R = 2 |
| DM2, six formats | **mixed**, +9.22 [−1.29, +16.24], 92% positive; F′ Q 0.69, partial | **mixed** on 26 claims, +0.42 [−1.83, +2.69] |

## DM6a — Calibration demonstration: parse and referent problems found after the run; exploratory re-analysis

**Date:** 2026-11-04, after the pre-registered analysis had been run and read. Spend $2.61 of the $3 (Haiku $0.12, Sonnet $2.49).

**Pre-registered readings** (strict parse rule):
- **Haiku:** no detectable format dependence; no detectable order dependence.
- **Sonnet:** calibration depends on format (ΔECE −0.143 [−0.233, −0.066]); no detectable order dependence.

**Problems found.**
1. About 120 hard-pool questions are phrased "Is this claim true?". "Guess: True/False" answers were unparsed under the frozen yes/no rule.
2. Long worked answers hit max_tokens 300. Under the frozen rule a hit ends the conversation, so 32 Haiku and 105 Sonnet conversations ended early (23 and 66 of them fresh single calls).
3. On "Is the answer X?" questions, the models often report the probability that X is correct rather than that their guess is. How often depends on format and context.

As a result, each pre-registered cell rests on 68–199 of 300 questions.

**Exploratory, not pre-registered** (`experiments/cal_format_explore.py`, no new calls):
- True/False is mapped to yes/no, and every cell is scored under both readings of the number.
- Sonnet's format effect stays clear under Tian's intended reading (−0.083 [−0.137, −0.032]). It reverses sign under the other reading.
- Order is null in every version.
- The pre-registered readings are not changed.

---

## D48 — The No Credence paper's claims narrowed to what replicated on Sonnet and Opus

**Date:** 2026-11-04 09:18 MST, after merging `multi-model` (DM1–DM6) into `main`. No new data or analysis. Every number is copied from `results/multi-model.md`, `results/mm-gm1-self-knowledge.md`, `results/mm-gm2-self-conditioning.md` and `results/mm-gm3b-format-invariance.md`.

**What changed in `paper/no-credence-to-read.md`.**
- **Stated for all three models:** no privileged self-knowledge (I = −0.055 for Haiku × Sonnet; −0.045 [−0.107, +0.017] for Sonnet × Opus) and reliance on the model's own record (MF agreement shown → redacted: 78% → 25%, 88% → 35%, 95% → 65%).
- **Narrowed:** the no-format-free-credence claim now holds for Haiku, partly for Sonnet (ΔLL +9.22 [−1.29, +16.24], *mixed*; F′ Q 0.69 [0.53, 0.82], *partial*), and not for Opus (26 claims, ΔLL +0.42 [−1.83, +2.69], *mixed*).
  - The Kendall's W trend is stated: 0.54 → 0.71 → 0.86.
  - Opus's pre-registered reading is *mixed*, not *single credence*, so the paper says the claim is "not supported" on Opus, not that it is refuted.
  - Opus's W is on 26 claims, all from items Haiku answered wrongly, so the last step of the trend is not item-matched.
- **Also narrowed, for consistency:** the question-alone claim, which holds on Haiku and Sonnet and is not decisive on Opus at 2 conversations per cell.
- **Where:** a new Section 4.6 with the per-model table; the abstract, contributions, §3.1 settings, the §4.5 heading, §§5.1, 5.3 and 5.4, the limitations and the reproduction list.
- **Unchanged:** the title, the [R-pending] tags and every Haiku-only number. Test S (own against other) was run on Haiku only, and the paper does not extend it.

## D47a — Source × distance × lag: the cap stopped the lag arm at R = 17

**Date:** 2026-11-04 09:36 MST, after the run.
- **Where the cap hit.** The $0.50 cap stopped the run at 3,650 of 3,840 conversations, with $0.502 spent as calls already in flight finished.
- **Why it was short.** The lag arm's conversations (three extra turns) cost about $0.00024 each, against the $0.00015 estimated.
- **What was cut.** As pre-registered, every distance cell is complete (R = 10). The lag arm was cut to R = 17 of 20, plus 2 conversations at repeat 17.
- **The analysis** is the frozen one, run with `--analyse` because the runner exits on a cap stop before analysing. Pre-registered reading: **self-consistency**.

## D49 — Opus's six-format arm completed (54 more claims), with test F′ on all 80 pre-registered

**Date:** 2026-11-04 09:50 MST, before any call of this run. Recorded in `experiments/mm-gm3b-opus-completion.md`; code `experiments/mm_gm3b_opus_complete.py`.

**What it is.** It continues DM2, whose Opus arm was budget-stopped at 26 of 80 claims (DM4a). Sean asked for this run after the morning brief recommended it.

**Design.**
- **Unchanged from DM2:** the prompts, the settings, the cache, the analysis and test F′.
- **Batches:** one batch per item, in a fixed order alternating Haiku-right and Haiku-wrong items.
- **Size and cost:** 3,200 requests, about $6.21 at the observed rate.
- **Budget:** **$6.40 cap on new spend**, enforced in code with DM2's 1.25 projection factor; stop on any refusal.

**Readings.**
- DM2's primary rule and D46's F′ rule.
- A rule for the paper's Opus claim, frozen in its Section 4: F′ above 0.75 → "does not hold on Opus"; F′ below 0.5 with "no single credence" → "holds on Opus"; otherwise → "holds partly".

**Disclosed before freezing.**
- While testing the code, test F′ was computed on Opus's 6 already-complete items: Q = 0.96 [0.92, 0.98].
- The paper rule had been written in code before that.
- `results/mm-gm3b-opus-first26.json` freezes the arm as it stood.

**Not yet fixed in `reproduce.py`** (found in this session's run, to be fixed after the Opus run):
- `api-usage.md` differs by its price line, now that the multi-model merge added Opus's prices to `config.PRICES`;
- the five multi-model results files have no regeneration step.

## D49a — Opus completion: the runner's projection ran two batches past the frozen stopping rule; primary analysis on the 17 items the rule allows

**Date:** 2026-11-04 10:30 MST, after the run.

**What happened.**
- **The rule and the code disagreed.** The pre-registration (§3) projects each batch at 1.25 × batch size × *mean cost so far*. The code passed each batch the *previous batch's* mean cost.
- **Two batches went past the stop.** h048 was cheap (/bin/zsh.0012 per call), so the projection for h291 was $0.35, and h291 was submitted. Under the rule as written, the projection was 240 × $0.00233 × 1.25 = $0.70. With $5.78 already spent that comes to $6.48, over the cap, so the run should have stopped there. h291 then cost $0.26, and h093 was submitted on h291's low rate.
- **What I did.** I stopped the runner and cancelled h093. All 240 of its requests were cancelled with none billed (`msgbatch_01Th769st8Nr64NZWN3oqKLB`). h291 had already completed and been stored.

**Spend.**
- $6.04 of new spend: $5.78 within the rule, plus $0.26 for h291. Under the $6.40 cap.
- The whole Opus arm cost $9.14.
- No refusals, and no max_tokens stops.

**Analysis.**
- **Primary:** the frozen rule's run, 17 items (68 claims). h291 was moved out of the analysis cache into `results/mm-gm3b-opus-h291-beyond-stop.json`.
- **Sensitivity:** with h291, 18 items (72 claims), in `results/mm-gm3b-opus-completion-with-h291.md`. Every reading is identical.
- **Not run:** h093 and h183. The arm is 17 of 20 items.

**Exploratory, not pre-registered.** Kendall's W for all three models on Opus's 68 claims, using gm3b's formula (`experiments/mm_gm3b_w68_explore.py`): 0.56, 0.76 and 0.87.

**Results.**
- F′ Q = 0.94 [0.90, 0.97], *a usable single belief*.
- DM2 primary ΔLL +1.90 [−0.82, +4.65], *mixed*.
- Paper rule: **"does not hold on Opus"**.

## D50 — The No Credence paper's Opus claim narrowed from "not supported" to "contradicted", by D49's frozen rule

**Date:** 2026-11-04 10:31 MST, after D49's result (`a8be4b5`). No new data.

**The rule.** D49 froze it before any call: F′ CI wholly above 0.75 → "does not hold on Opus". The CI was [0.90, 0.97].

**What changed in `paper/no-credence-to-read.md`.**
- **Abstract and contributions:** the format claim is "contradicted on Opus", with Q 0.29 / 0.69 / 0.94 and the item-matched W 0.56 / 0.76 / 0.87.
- **Section 4.6:** the table and the Opus paragraph now use the 68-claim arm.
  - F′ 0.94 [0.90, 0.97]; ΔLL +1.90 [−0.82, +4.65], mixed; 6–14% reversed pairs.
  - The exploratory item-matched W is labelled as such.
- **Sections 5.1 and 5.3:** "On Opus there is a credence to read"; Opus's R² of 0.92 is above Smolin and Wilder's range; the reversed-pair range is updated.
- **Limitations, reproduction and costs:** D49 added ($6.04).

**Unchanged.**
- The Haiku and Sonnet numbers.
- The self-knowledge and own-record findings, which hold on all three models.
- The title.

## D51 — The audit's cuts applied to every results, README and paper file (one pass)

**Date:** 2026-11-04 MST, after the audit branch was merged (`7a5af8f`); committed in `5480c49`. No new data, and no statistic changed except where the audit found it wrong.

**Source.** `audits/SUMMARY.md` and its 41 audit files. Each audit's "Overclaims to cut" section names a target `file:line`, quotes the sentence and gives a replacement; there are 369 entries in all, on results, README and paper files. Targets were located by their quoted text, because line numbers had drifted since the audit's base commit `0c64baa`.

**Order.** The cuts were applied in the order of SUMMARY's "What the main session should cut first":
1. nulls written as findings;
2. mechanism words;
3. the named README lines;
4. the miscounts in "Numbers found wrong";
5. experiment 5's tie, which is handled separately in D52;
6. the D48 collision, already renumbered DP1 at the probes merge.

Where several audits targeted one sentence, their replacements were composed in that order into one sentence that keeps every correction.

**Counts** (per-file logs kept by the session):

| | entries |
|---|---|
| applied as written | 273 |
| adapted | 78 |
| obsolete (text already rewritten by D49/D50, defect gone) | 5 |
| left for D52 (experiment 5's verdict label) | 7 |
| deferred to the record update (Standing section, coverage line) or to D53 | 6 |

"Adapted" covers two cases:
- two audits composed onto one sentence;
- a replacement written before D49/D50, brought to the current state: Opus's format arm at 68 claims, F′ Q 0.94 [0.90, 0.97], DM2 *mixed*, item-matched W 0.56 / 0.76 / 0.87 (exploratory), "contradicted on Opus".

**Sweep.** SUMMARY's categories 1 and 2 say "every". About 134 further instances in the same files were fixed in the same style. In each, the cited data are an interval that includes 0 or a mechanism read from a behavioural contrast, so the sentence now gives the interval or says "not detected", or states the mechanism as a reading.

**Numbers corrected** (SUMMARY's "Numbers found wrong" table):
- experiment 4 run 3: the counts become 6 of 32 item-orders, 17 of 32 at 0% accept, and 5 reliable;
- gm3b: the "% of pairs" figures relabelled as the (1 − τ_b)/2 index. The shares in opposite order (11–25% split-half, 12–25% full data, against 1–5%) are given where a share is meant, and the under-converged L1 fit is noted;
- bm7: 4–9 points;
- h018's exclusion reason;
- frame-fix-check: 15% of all items;
- stage2-run-2b: arm F's window of 1–16;
- sonnet-ablation: 1,000 resamples;
- the paper's "outperforms every structural analysis" and v3's "do not differ";
- calibration: 60 True/False questions;
- the api-usage ledger's scope.

**Writer prose changed** so that the generated parts still reproduce (prose only, no computation):
- `gm3b_format_invariance.py` (the table header names the index);
- `run_pool.py` (the pool-run exclusion header; the api-usage scope line);
- `sonnet_ablation.py` (the resample count; the file is in SKIPPED).

**Other changes.**
- **No Credence paper:** the title is now "… Construct Claude Haiku's Judgments, and Partly Sonnet's". Its status line notes the few numbers taken from audit files.

**Not edited: earlier DEVIATIONS entries.** The log stays as written. The audit's corrections to it are recorded here instead:
- **D26 heading:** "fixed before any full-run data were examined" is author testimony. The analysis commit came after 606 full-run conversations existed, though before any fit or result.
- **Pool run 4 (line 376):** "1 hit the token cap" should read "1 (h018, answered correctly) was excluded because the extractor returned 1 claim".
- **DM6 (line 852):** "About 120" True/False questions should be 60, and the open-form exclusion was omitted.
- **DP1's exploratory line:** the probe's +0.14 is +0.14 [−0.23, +0.46], an association not detected rather than shown absent.

**Not edited: frozen files.** The pre-registrations in `experiments/*.md`, the audits themselves, and `experiments/probe-dissociation.md`'s line 44 (see D53).

## D52 — Experiment 5's verdict re-issued under its own §7.5 rule on the single-direction QQ statistic: TIE → CLASSICAL

**Date:** 2026-11-04 13:18 MST, after the audit (`audits/exp5-run-1.md`) and D51. No new data and no refit.

**Why.**
- Run 1's verdict, TIE (`results/exp5-run-1.md`, D22–D26, D32), took its "QQ not contradicted" leg from the mean q pooled over both scale directions: +0.005 [−0.058, +0.065].
- Run 2 (D33) and its write-up already treat that pooled value as an artefact of mixing anchors (a) and (b).
- The audit recomputed q on run 1's own anchor-(a) conversations (0 = certainly false, 100 = certainly true; all 40 items): **−0.345 [−0.517, −0.181]** on 32 large-order-effect pairs.

**The rule, unchanged.**
- §7.3: "Signature contradicted if the mean-q CI excludes 0 on those pairs."
- §7.5: "classical: primary classical, or a signature contradicted with the primary not a pass."
- The primary (§7.2) is a tie, F5 − A5 = +67.0 [−34.1, +211.5], which is not a pass. The Kvam check shows no signature and no commitment.
- So the re-issued verdict is **CLASSICAL**.

**Check with the frozen code.** `experiments/exp5_reissue.py` runs `exp5_analyse.qq_check` and the verdict precedence of `exp5_analyse.main`, unchanged, on the anchor-(a) conversations. It gives 33 pairs and −0.339 [−0.510, −0.168], also contradicted, so also CLASSICAL. The pair count differs by one from the audit's because the OE bootstrap draws differ.
- Anchor (b) is reported, not used: +0.241 [+0.118, +0.370], also contradicted.
- So the QQ equality fails in each direction separately; only the pooled average sits near 0.

**What is post hoc.** Restricting to one direction is a choice made after the data, prompted by run 2 and the audit. It is the project's single scale direction, and the subset run 2 reports, but it is not the analysis frozen in §7.3.

**Where it is recorded.**
- `results/exp5-verdict-reissue.{json,md}` (new; regenerated by reproduce.py).
- `results/exp5-run-1.md` keeps the original TIE, marked superseded, in both its generated verdict line and its Reading. The writer's prose in `exp5_analyse.write_md` changed with it; no statistic changed.
- README, record.md, the v3 paper, the programme paper and clonable-minds now give CLASSICAL (re-issued, D52), with the original tie as superseded; experiment 5 run 2's Reading marks its "run 1's tie is unchanged" as superseded. The morning brief states no experiment 5 verdict.

**Unchanged.** No quantum advantage and no quantum signature in either reading. The label moves from "could not tell apart" to "classical", because the parameter-free quantum signature is contradicted.

## D53 — The probe-dissociation result (DP1) marked unverified; a fresh step 3 on new seeds queued for the probes worktree

**Date:** 2026-11-04 13:19 MST, after the audit (`audits/probe-dissociation.md`, hole 1).

**Why.** DP1's pre-registration says selection (the gate) and test (step 3) use different conversations. But both steps seed each conversation from the same key, `seed_for(f"{lm.name}|{qid}|{cell}|{rep}")`. The audit found step 3's O1–O4 and B0 verbal ratings identical to the gate's in 500 of 500 conversations.
- So validity check V4 tested nothing.
- Step 3's verbal order effects on the gate items are the selection data, with its winner's curse.
- The frozen label, PROBE MOVES, BUT NOT WITH THE RATING, therefore rests on a test that was not independent of selection.

**What changed.**
- `results/probe-dissociation.md` (a banner under the title), README, the morning brief (a new direction-5 section) and `paper/gold-map.md` §5 (which said "Nothing yet") mark the DP1 result **unverified**.
- The figure title (`probe_dissociation_figure.py`, `paper/figures/fig3-probe-dissociation.*`) no longer says the probe moves "more than the rating does, and not in step with it"; it says "unverified, D53".
- Its numbers and label are kept, as recorded.

**Queued.** On branch `probes`, commit `ad1667d`, `experiments/QUEUED-probe-step3-fresh-seeds.md` sets out a fresh step 3:
- the same model, gate items, probe and layer, cells, R and analysis;
- sampler seeds from a new namespace (`step3-fresh`);
- a pre-run check that the fresh ratings do not replay the gate's;
- the audit's alternative Q scalings, the Holm-corrected gate and r without h191, as secondaries.

It is to be frozen as DP2 in its own commit before any run. Nothing has been run.

## D54 — Five overnight tests relabelled as exploratory re-analyses, not frozen tests

**Date:** 2026-11-04 13:20 MST, after the audit (`audits/record-accuracy.md`, `audits/SUMMARY.md` "Cross-cutting holes" 1).

**Why.** README and the morning brief said each overnight test was frozen "before its data were opened". For five of them that is false.
- **The five:** D34 (direction 9, NSIT), D35 (direction 3's anchor-gap free look), D40 (confirmation), D41 (serial position) and D42 (contrast sign).
- **What they analyse:** each re-analyses archived experiment-4 or experiment-5 conversations that earlier analyses had already opened.
- **When their plans were committed:** 15 to 90 seconds before the analysis ran.
- **What such a plan does:** it fixes the statistic against later change. It cannot keep the choice of contrast or bar blind to the data.

**What changed.**
- **README's overnight section:** six frozen tests (D36–D39, D43, D44) and five exploratory re-analyses, named.
- **The morning brief:** the rules line, the five findings' headings (items 1, 2, 7, 8, 9), the five rows of the technical table, and a note above that table.
- **Unchanged:** the analyses and their numbers.

**Not relabelled.** D46 (test F′, `gm3c`) is also an archival re-analysis of gm3b's calls; the audit counts it as the sixth of 14 with the robustness wave. The relabelling asked for covers the five overnight tests, so D46 keeps its label for now. Its own audit verdict is UNDETERMINED (`audits/gm3c-heldout-format.md`).

## D54a — D46 (test F′) relabelled as an exploratory re-analysis too

**Date:** 2026-11-04 13:48 MST, at the user's request after D54.

D46 re-analyses direction 3's six-format calls (D38), which had already been opened and analysed. Its plan was frozen with the pairwise ρ and split-half reliabilities already known (`audits/gm3c-heldout-format.md`). It is now labelled the same way as D34, D35 and D40–D42: an exploratory re-analysis, not a frozen test.
- **Where:** README (the format bullet of the overnight section), the morning brief (result 13's heading, the "Done since" note, technical-table row 13 and the note above the table) and `paper/record.md` (its row, the D54 row and the Standing section).
- **What did not change:** the numbers. Nor did D49, which applied test F′ to Opus's newly collected calls, under a rule frozen before those calls existed.

---

# Probes branch (`probes`): entry DP1

## DP1 — Gold map direction 5 (belief versus readout) pre-registered: local open-weight model, truth probe, chain order

*Numbering.* This entry was written as **D48** on branch `probes` (commits `9ef909d`, `8685008`), at the same time as main's D48, which narrowed the No Credence paper. It was renumbered **DP1** at the merge into `main`, after the DM precedent. References to "D48" in `experiments/probe-dissociation.md`, `experiments/probe_dissociation*.py`, `experiments/local_lm.py`, `results/probe-dissociation.md` and the two probes commit messages mean this entry. Those frozen files were left unedited.

**Date:** 2026-11-04, before any call on the study items. Recorded in `experiments/probe-dissociation.md`. Cost $0 API: Llama-3-8B-Instruct (Qwen2.5-7B-Instruct as the fallback), 4-bit, run locally through MLX.

**Design.**
- **Step 1, the gate:** experiment 5 run 2's ten items, chains O1–O4 and B0, R = 10, one scale direction. The gate needs at least 3 items with a span of 5 points or more and an order permutation p < 0.05.
- **Step 2:** mass-mean truth probes trained on Marks & Tegmark's curated datasets. The layer is chosen on companies and counterfact.
- **Step 3:** at the M point of each chain, the probe is read on the yes-answer as a declarative statement (a cache-trimmed side branch), then the verbal rating is taken. A told-yes/told-no positive control sets each measure's range.

**Primary:** Q, the share of the noise-corrected verbal order effect that the probe also shows, in told-range units. It is read with the probe's order permutation test, against the frozen rule (§5).

**Changes from the gold map's sketch.**
- One scale direction (run 2's lesson).
- The positive control and Q were added, so that a flat probe cannot pass by being blind.
- No QQ block: the test needs only the chain orders.

**Check before freezing.** The analysis was run on simulated stable, moving and noisy-probe worlds, and returned DISSOCIATION, BELIEF MOVES and UNDECIDED respectively.

**Implementation notes after freezing (no design change).**
- **Memory limits.** The gate run slowed about 7× under system memory pressure (swap nearly full). MLX's freed-buffer cache was capped at 256 MB, and the model's memory is now wired with `mx.set_wired_limit`, as `mlx_lm.generate` does. The run was stopped and resumed twice. Conversations are keyed and seeded per (model, item, cell, repeat), and only completed repeats are saved, so resuming regenerates the same conversations.
- **Probe training memory.** Training now runs in two passes, class sums first and then projections, rather than holding every activation in memory. The statements sampled, the directions and the scores are the same.

**Result (DP1).** Llama-3-8B passed the gate at exactly 3 of 10 items (h190, h101 and h191), so Qwen was not run. The probe is layer 13, with selection AUROC 0.90 and report-set AUROC 0.88. All four validity checks pass.
- **Q = 3.72 [1.43, 7.03], r = +0.31 [−0.49, +0.99], p_P = 0.0001.**
- **Frozen verdict: PROBE MOVES, BUT NOT WITH THE RATING.**
- **Sensitivity:** layer 11 alone reads BELIEF MOVES (r = +0.60).
- **Exploratory:** the rating follows the last sub-claim's lean (r = +0.54); the probe does not (+0.14).

Details in `results/probe-dissociation.md`.

## D55 — qwalk (bet em-qwalk) pre-registered: a simulated quantum walk against PageRank on program 1's claim graph

**Date:** 2026-11-04 19:50 America/Denver, before the claim graph was opened for analysis. Recorded in `experiments/qwalk.md`, analysis in `experiments/qwalk.py`. Laptop only: $0 API, 0 QPU s, no chip; the walk is a numpy simulation.

**What it is.** Sean's entangled-claims question (steer st-13): program 1's research directions (`map/entangled-mind.json`) as nodes, parent, same-record-row and ledger links as edges, kills and hits as labels; a continuous-time quantum walk and personalised PageRank (damping 0.85, its exact classical twin at the matched exponential stopping time τ = 5.667) each score every settled direction leave-one-node-out. Pass only if the quantum walk's AUROC beats PageRank's with a stratified bootstrap 95% interval above 0; beating chance does not count.

**What it is not.** It does not revive the quantum error-prediction encoding (closed; CONTEXT §3 rule 6). No model answer, claim web or circuit from program 1 is used.

**Disclosed.** The author had read the map, the record and brier.md (outcomes visible) before writing the rules; no predictor was computed on the real graph and the dry run used synthetic forests only. Engine odds: map 0.04, v1 re-elicitation 0.07, in force 0.05 (lesson ls-em-qwalk). No human odds.

## D56 — em-qwalk withdrawn before data (design review: redesign); re-bet as em-qwalk2

**Date:** 2026-11-04, before any score, AUROC or Δ was computed on the real graph. Laptop only throughout: $0 API, 0 QPU s.

**Two reviews, the stricter binds** (agreed with the engine session before either verdict was known):
- `ledger/design-reviews/em-qwalk.md` (6635276, fresh subagent launched by the author's session): **redesign**. Under leave-one-node-out a hidden direction's class has one seed fewer, so its own label shapes its score. The coherent quantum superposition's mass grows with the seed count, while PageRank averages over its seeds, so the two leak in opposite directions. The leak is worst around a labelled hub, and program 1's graph is mostly one (`oe`, 19 neighbours, 29 of 41 nodes). On a star with random labels the frozen rule said "classical" in 200 of 200 graphs. "Exact classical twin (same generator, seeds, stopping time)" was also wrong on the seeding.
- `ledger/design-reviews/em-qwalk-1b.md` (3244dbb, fresh subagent launched by the engine session): **fix-first, 7 flaws**. The rule passes a walk that is below chance but less wrong than PageRank (the dry run's "quantum wins" case was exactly that), and the dumb baselines were reported, not ruled on. Other flaws: edges made after and because of outcomes; a false-pass rate measured on the wrong topology (about 4% on the real graph against the stated 2.7%); no leave-one-cluster-out; wrong nouns ("claim graph"); a review gate reading one file.

**What follows.** em-qwalk is `withdrawn` in `ledger/bets.jsonl` (counted, not scored). Its pre-registration (680f128), code and seed (34bad77) stay as committed. A new bet, em-qwalk2, takes both reviews' fixes, with its own lesson, pre-registration, seed and design reviews. Like em-qwalk, it does not revive the quantum error-prediction encoding.

## D57 — em-qwalk2 pre-registered: the re-bet of em-qwalk with both design reviews' fixes

**Date:** 2026-11-04, before any score on the real labels. Recorded in `experiments/qwalk2.md`, code `experiments/qwalk2.py`. Laptop only: $0 API, 0 QPU s.

**What changed from em-qwalk** (each review flaw is mapped to its answer in qwalk2.md §10):
- Both arms now use one-seed walks from every settled direction, summed with weights centred on the others' hit rate, so they differ only in the kernel.
- Every verdict is read against a label-permutation null on the frozen graph, which carries the leave-one-out leak (new pattern P11).
- A pass must beat chance, and the four oriented dumb rules (phase bit, neighbour vote, degree, child count).
- Added: a prospective-edges sensitivity, leave-one-cluster-out, the stated 80%-power gap (about 0.19 AUROC), seeds and inputs pinned in code, and a gate that requires both reviews.

**Inputs stay at 680f128.** The bmq scout's 18 new directions (af3266b) are reading-stage labels that postdate the question.

**Odds:** 0.05 → 0.01. Labels planted from the quantum kernel itself pass only 1–2%.

## D58 — em-qwalk2 withdrawn before data (design review: redesign); qwalk parked as untestable at this scale

**Date:** 2026-11-04, before any score, AUROC, Δ or verdict on the real labels. Laptop only: $0 API, 0 QPU s.

**Two reviews; the stricter binds.**
- `ledger/design-reviews/em-qwalk2.md` (efb4920, disclosure 0417646): **redesign**, 6 flaws. The re-bet fixed em-qwalk's own-label leak and its below-chance pass, but the test cannot answer its question on this graph.
  - To pass, the label-permutation null needs Δ > 0.149 and a quantum AUROC > 0.786. These thresholds depend only on the graph and the 11/14 counts.
  - In every planted world built (the author's two kernel-field worlds and two kernel-sources worlds per arm, the second reviewer's, and this reviewer's three recipes), pass is at most 4.3% and classical at most 4.0%. So the verdict is null 96–100% of the time whatever the truth.
  - Scored at 1%, that null would lower the engine's Brier from 0.267 toward 0.250 with nothing learned.
- `ledger/design-reviews/em-qwalk2-1b.md` (04e7f81): **fix-first**, 3 small flaws: the planted worlds were not in the code; one clause of the pass sentence; the gate's regex.

**Committed with this row** (after the withdrawal; no data): `qwalk2.py` gains `--dry-run-planted 680f128`, which regenerates qwalk2.md §4's planted rows exactly and adds a few-sources world per arm (classical-sources: classical 4.0%, quantum-sources: pass 0%), and the gate now reads every `em-qwalk2*.md` and refuses any file without a verdict line (F-C). Neither change is a re-bet.

**Any future qwalk bet must, before data:**
- (a) show in a committed dry run P(pass) ≥ 0.5 in a pre-specified quantum-favourable world, P(classical) ≥ 0.5 in a classical-favourable one, and both false verdicts ≤ 0.05 under shuffled labels and in the opposite arm's world. Very roughly 550 settled directions; all maps hold 59 today.
- (b) commit every planting recipe and derive its odds, pre-mortem and lesson from them.
- (c) describe the arms as a bundle: interference, degree weighting (classical detailed balance) and Born-rule against probability readout. Or add a matched combinatorial-Laplacian secondary.
- (d) say "scored above every one-line rule's AUROC", not "judged against shuffled outcomes", for the dumb rules.
- (e) report untestable robustness rows as "cannot be checked"; drop whole-component and single-label clusters; make the untestable threshold agree for subsets.
- (f) add depth and component size to the dumb rules, with a stated margin, or stop claiming P3.
- (g) not count a `confirmed_at` such as "pending" as confirmed.
- (h) refuse uncommitted edits to the pre-registration or code (`git status --porcelain`), and read the randomness with `git show <seed commit>`.
- (i) carry em-qwalk2-1b's F-B wording.

**Outcome against steer st-13:** untestable at this scale, found before data at $0. Recorded in `ledger/steers.jsonl` and `results/qwalk.md`.

## D59 — Audit em-qwalk applied: 8 cuts to results/qwalk.md and st-13; pl-005 revealed clean; a review-scope breach logged

**Date:** 2026-11-04, after the audit (`ledger/audits/em-qwalk.md`, 9c9c139; fresh subagent launched by the engine session with auditor.md's launch line only). Laptop only: $0 API, 0 QPU s. No score on the real outcomes was computed by anyone.

- **Verdict:** "untestable at this scale" stands. Both bets remain `withdrawn`, unscored. Plant pl-005 was **clean**, so every finding is the real audit.
- **Cuts applied** to `results/qwalk.md`, all eight, as the audit wrote them:
  - "the friendliest case possible" → the author's recipe, with PageRank ahead in other recipes;
  - "whatever the truth" → at least 95% "not detectably different" in every modelled world; only labellings searched for the purpose passed;
  - thresholds 0.149 and 0.779–0.792;
  - "cannot be told apart" → no test of this design could tell them apart, and neither was scored;
  - "tested harness ready to rerun" → a reviewed harness pinned to 680f128, needing D58 (a)–(i);
  - the 80%-power figure is the bootstrap condition alone;
  - "the leak cancels" → cancels on average;
  - "59" includes the 14 bmq reading-stage labels.
  - Cuts 2, 4 and 5 are mirrored in st-13's outcome in `ledger/steers.jsonl`.
- **Generator committed** for §3's first table: `qwalk2.py --null-thresholds 680f128` (40 seeds × 10,000 shuffles; label values discarded). Δ threshold 0.149 in 32 of 40 seeds (0.143–0.156); quantum threshold 0.779–0.792.
- **Breach, logged.** em-qwalk's pre-registration (680f128 §3) let reviewers run only `--dry-run` and `--graph-counts` on the real graph. The author's brief to the em-qwalk reviewer said it "may inspect the graph-construction rule's output on the real inputs (which nodes, which edges, which labels)". That reviewer then listed all 25 real labels in `ledger/design-reviews/em-qwalk.md`. The brief exceeded the pre-registration; the fault is the author's, not the reviewer's.
  - It does not affect any verdict: no score was ever computed, and every number in the results comes from shuffled or planted outcomes.
  - It does mean the labels are public in a review file, as they already were in the map and the ledger.
- **Design-review miss** (audit header `design_review_missed`): neither em-qwalk review asked whether the design could pass in a world where the hypothesis holds. That is now design-review check D11 (engine session, 41a687d).

## D60 — Audit round 3 (claude-fable-5-1) of the five scored phase-B bets: all stand with cuts; no outcome changes

2026-11-05 ~06:00 America/Denver. `ledger/audits/round-3/em-gm1.md`, `em-gm2.md`, `em-gm3b.md`, `em-gm4.md`, `em-gm5.md`. Every headline number was re-derived from the archived JSON with independent code (scratch scripts named in each audit). Verdicts: gm1 null, gm2 pass, gm3b pass, gm4 mixed, gm5 mixed, all unchanged; outcomes 0, 1, 1, 0, 0 unchanged. Wording cuts applied verbatim from the audits, in the results files only (no data, code or pre-registration touched):
- gm1: the all-298 interval excludes 0 only narrowly (28 of 298 single-question drops put its upper end at or above 0) and the sign is mostly the 26 disagreement questions (the other 272 give −0.036 [−0.103, +0.027]); the paper's two "Self-report is not privileged" headings and the README's "gives no advantage" now read "no privileged self-knowledge detected" / "no detectable advantage".
- gm2: "redaction gives an even larger order effect than showing" is not established (difference 8.0 points [−0.8, +17.7]); the placeholder confound and the clipped estimator's permutation floor (0.34 against the 0.5 bar) are stated; R = 1.91 [0.93, 4.70] holds under every seed, drop and bias correction.
- gm3b: "no single belief to read out" narrowed to what a non-invariance test shows; the by-format table is marked as coming from an under-converged fit (own converged fitter: +19.41 [+16.53, +22.09], 86.3%).
- gm4: EIG's above-chance excess is entirely overlap with the confirmatory target; on disjoint menus EIG is at chance while confirmatory stays above it.
- gm5: the Holm-corrected gate (2 of 10), the alternative Q scalings (0.86, 0.66) and the DP2 dependence on the unmerged `probes` branch are stated; the stale "queued" sentence and the `:116` contradiction round 2 flagged are fixed.


## D61 — em-dm6f2 pre-registered (remap follow-up dm6-f2, archive only, $0)

2026-11-05 06:15 America/Denver, before the archive is opened for this analysis. Follow-up `dm6-f2` of `em-dm6` (remap `9773f6a`): does a fixed "flag anything under 70% confidence" rule flag different answers by format, beyond same-format repeat noise? Pre-registration `experiments/dm6f2-flag-overlap.md`, code `experiments/dm6f2_flag_overlap.py`. Two departures from the remap's row, both before data: (1) em-dm6 holds Haiku and Sonnet, not Sonnet and Opus, so Haiku is the secondary and Opus is not reported; (2) the event adds a same-format replicate baseline (D = J_N − J_F ≥ 0.10, lower bound above 0), per the lesson (P3), and restricts every overlap to questions with a number in all four fresh cells (P8). Engine odds: map 0.55, v1 0.76, after the lesson 0.55. No human odds. The same session parked g-f1, g-f2, dm6-f1 and gm3c-f2 before betting (`experiments/remap-free-check.md`, `fe80338`).

## D62 — em-gm3cf1 pre-registered (remap follow-up gm3c-f1, archive only, $0)

2026-11-05 America/Denver (commit author time is the record), before `results/gm3b-calls.json` is opened for this analysis. Follow-up `gm3c-f1` of `em-gm3c` (audited pass → undetermined): Haiku's held-out format recovery with a converged one-credence fit (gm3b's block ascent copied, stop at |Δobjective| < 1e-3, cap 2,000 rounds), predictions averaged over 10 beacon-drawn fold assignments, and a 10,000-resample BCa interval. Pre-registration `experiments/gm3cf1-heldout-bca.md`, code `experiments/gm3cf1_heldout_bca.py`. Departure from the remap's row, before data: the pass also needs a link-free least-squares predictor's mean Q under 0.5 (the lesson's P3 guard). Engine odds: map 0.45, v1 0.25, after the lesson 0.30. No human odds.

## D63 — em-dm6f2 design-review fixes (review `19bdf22`, fix-first, 3 flaws), before any data

2026-11-05 06:24 America/Denver (commit 7f5d3f4, author time 06:24:39; this line first said 06:26, a guessed time), before the archive is opened for the primary analysis. Named review: `ledger/design-reviews/em-dm6f2.md` (`19bdf22`). The rule, thresholds, n floor and seed are unchanged; no bar is lowered.
- **F1 (D8).** The code now reports the two same-format overlaps J_PP = J(P0, P1) and J_FF = J(F0, F1) separately, with question-bootstrap intervals, and a flag `noise_asymmetric` (J_F ≥ min(J_PP, J_FF) − 1e-9). The pre-registration's §5 pass and fail sentences are replaced by the review's wording:
  - pass: "An overseer who double-checks every answer for which Sonnet stated a number below 70% would have checked a substantially different set of questions depending on which of the two formats the number was asked in: on average over the two formats, the lists from different formats overlapped less than the lists from two askings in the same format, by at least the pre-registered margin. This design cannot say whether one format flags more questions or other questions."
  - If the flag fires, this is appended: "In the <probability|frequency> format, two askings overlapped no more than the two formats did (J <J_PP or J_FF> against J_F <J_F>), so for that format the difference between formats is no larger than its own repeat noise."
  - fail: "On this archive, the lists of Sonnet's answers with a stated number below 70% were not shown to differ by format more than they differ between two askings in the same format, by the pre-registered margin."
  - The untestable sentence is unchanged.
  - The self-test adds an asymmetric-noise world, which must raise the flag.
- **F2 (D8).** Haiku's entry (secondary) carries no verdict sentence.
- **F3 (D10).** The §7 stop rule now reads: "If any archive file's sha256 differs from the value pinned in the code (from the committed files at bc9b77e), the run stops before any analysis and the mismatch is reported." The three hashes are pinned in `PINNED_SHA256`.
- **Recommendation taken:** the leave-one-question-out flip ids are printed in the results file. The others (leave-one-category-out, rate-matched tie handling) are not taken; both are secondary.
- **Erratum to D61:** "2026-11-05 06:15" there is a guessed time; the pre-registration commit's author time is 06:06:43.

## D64 — em-gm2q pre-registered (map gm2-f1, questions only, no answer turns; Haiku and Sonnet; $3.50 cap)

2026-11-05, before any call. The novelty page's ranked replication 2 (`paper/novelty.md`, finding 5b): gm2's redacted chain kept the questions but replaced each answer with "[rating recorded]", so its order effect could be the placeholder's. This bet puts the four sub-questions in one user message in each of gm2's four orders, then the main question, with no answer turns, and re-runs gm2's shown chain alongside as the reference (Haiku also re-runs redacted, secondary). Pre-registration `experiments/gm2q-questions-only.md`, code `experiments/gm2q_questions_only.py`, dry run `results/gm2q-dry-run.json`. Not a departure from any earlier pre-registration: gm2's items, prompts, orders and estimator are reused unchanged; the qonly message is new. Models Haiku and Sonnet only (the job as given; Opus is the next layer if it passes). Cockpit card first (`f65b361`), map node with v1 engine odds 0.10 (`53fd45b`, times `b04215f`); after the lesson 0.15. No human odds.

## D65 — em-gm2bf1 pre-registered (remap follow-up gm2b-f1, archive only, $0)

2026-11-05 America/Denver (commit author time is the record), before the order and format archives are opened for this analysis. Follow-up `gm2b-f1` of `em-gm2b`: on Haiku's 160 claims, does a claim's order span (gm2/gm2b, shown, O1–O4) correlate with its format spread (gm3b, six formats, percentile-rank SD)? Pre-registration `experiments/gm2bf1-order-vs-format.md`, code `experiments/gm2bf1_order_vs_format.py`. Departures from the remap's row, before data: the unit is the claim (160, item-cluster bootstrap) rather than "item-level"; and the pass adds a guard (lesson, P3/P8): the partial Spearman given extremity and within-order noise must have its lower bound above 0. Engine odds: map 0.40, v1 0.24, after the lesson 0.25. No human odds. (D64 is another session's em-gm2q row.)

## D66 — em-gm3cf1 withdrawn before data (design review: redesign); gm3c-f1 parked

2026-11-05 06:50 America/Denver, before any primary statistic was computed on the real data. The design review (`ledger/design-reviews/em-gm3cf1.md`, `1aab5ba`, fresh subagent) found five flaws. The binding one is D11 (pattern P12). The em-gm3c audit had already measured the single-split upper bound at four fold assignments (0.501, 0.497, 0.510, 0.522), and both of this bet's changes push the bound up: averaging over ten splits by about +0.005, and BCa by about +0.005. In 750 synthetic worlds matched to those measured numbers, the frozen rule passes about 1% of the time (0.8–1.5%), far below the ~10% floor. The bet's own pre-mortem names exactly that failure, and its 30% odds were too high. The other four flaws, recorded for any re-bet:
- FIT_TOL 1e-3 is looser than gm3b's 1e-6;
- no rule for a single-item flip;
- the pass sentence overreaches ("each format", "cannot be recovered");
- the archive and split files' hashes are not pinned.
Not scored; counted as a withdrawal. The 0.5 bar is not moved. gm3c-f1 is parked with what a fair test needs: the same six formats on 80–120 fresh items (about $1–1.5 on Haiku, so not free), pre-registered with a dry run built on the measured spreads. Or the estimate can be reported unscored. The reviewer's real-data contact: archive structure and hash, the 40 items' categories, and two fits on one training set (fold 0 of a seed-0 assignment, F6 held out) at two tolerances, recording only rounds, time and objective. No prediction, Q or interval was computed on real data. The beacon seeds (`0fa0924`) are never used.

## D67 — em-bm9f2 pre-registered (remap follow-up bm9-f2, archive only, $0); bm9-f1 parked as not free

2026-11-05 America/Denver (commit author time is the record), before `results/exp5-conversations.json` is opened for this analysis. Follow-up `bm9-f2` of `em-bm9`: on Haiku's 80 run-1 pairs, does a derivative-of-Gaussian pull beat a linear one by ΔAIC ≥ 4, beat an equally flexible tanh by ΔAIC ≥ 2, with its peak inside the observed gaps? Pre-registration `experiments/bm9f2-dog-shape.md`, code `experiments/bm9f2_dog_shape.py`. Departure from the remap's row, before data: the tanh rival and the A > 0 condition are added (lesson, P5). Engine odds: map 0.25, v1 0.08, after the lesson 0.08. No human odds. Before this, bm9-f1 (Sonnet and Opus) was checked and parked as not free: em-dm4's conversations put M, four S, then M again, not single S→M pairs. Only Haiku's exp5 has the QQ pairs, so bm9-f1 needs new calls (about $3).

## D68 — em-dm6f2 audit applied: 3 cuts to the plain-English section; three record items logged

2026-11-05, after the audit (`ledger/audits/em-dm6f2.md`, stands, pass-unreplicated). Cuts 1–3 were applied verbatim to `results/dm6f2-flag-overlap.md`. They state the rate-matched result as a secondary, give the category split (the effect is carried by the 94 science questions; simpleqa alone gives D +0.08, below the margin), and use "questions" for "answers". No table or number changed. Record items the audit found without a row (hole 5):
- the seed commit `6520400` made two more time edits to the frozen pre-registration besides the header ("06:10" → "06:05" for the human-odds check; "06:05" → "about 06:02" for the v1 elicitation). Both correct guessed times; no rule, number or bar changed;
- after the run, `dm6f2_flag_overlap.py` gained one output-only line (the placeholder plain-English heading for program 1's reproduce.py). It was re-run with the same seed, and the JSON was byte-identical (`f9d77e8`);
- the same-format intervals added under D63 use the stream seed + 2, which §2 did not name. They feed reported intervals only.

## D69 — em-gm2q design-review fixes (review `927cdb4`, fix-first, 5 flaws), before any call

2026-11-05, before any call. No API call has been made for em-gm2q. The pre-registration (`2f30696`, seed `1ba7f8c`) stays frozen; this row is the binding amendment, and where it and the pre-registration differ, this row wins. Code: `experiments/gm2q_questions_only.py` as committed with this row. None of the fixes lowers the bar; fixes 1 and 3 tighten it or narrow what a verdict may say.

**Fix 1 (D5, a wrong-target responder could pass).** A qonly conversation is **wrong-target** if its rating is within 5 points of today's mean shown rating of the statement placed 4th in that order, and more than 20 points from that item's mean shown final rating (every boundary with tolerance 1e-9). The same flag is computed on the shown final ratings as the chance baseline; both shares are reported per model. **A model's pass now also needs the qonly permutation gate p < 0.05 with the flagged qonly conversations dropped** (seed + 6). If dropping leaves any cell with fewer than 2 ratings, the model fails. `--selftest` now includes a no-effect world with 30% of answers set to the 4th statement's rating: raw qonly gate p = 0.0002, after dropping the 28% flagged p = 0.42, label fail. Limit, stated plainly: a wrong-target answer to a statement rated within 20 points of the item's final rating cannot be flagged; the dry run's wrong-target worlds below use the archived statement ratings to show how much that matters.

**Fix 1b (D1 note, an unregistered route to untestable).** §5's untestable rule also covers a shown or qonly cell with fewer than 2 usable ratings (the code always did this).

**Fix 2 (D7, the primary comparison's differences).** §6 listed only qonly against redacted. R compares qonly with **shown**, which differs from qonly in seven ways: in shown the model (1) sees its own four real answers; (2) produces four sub-ratings itself, the act of rating; (3) gets five user turns, not one message; (4) gets unnumbered questions, not a 1–5 list; (5) gets the opening "I will ask you to rate several statements, one at a time…" rather than "…Think about each statement in turn, then give a rating for the question itself only…"; (6) gives five structured outputs, not one; (7) meets the main question as its own final turn, not as line 5 of a list. Matched: model, settings, items, orders, R, date, call path and scale. R compares qonly with the whole turn-by-turn bundle, so a fail cannot be laid on any one of these.

**Fix 3 (D8, the fail and mixed sentences).** §5's fail sentence is replaced by three, chosen in code (`sentence_key`):
- **fail-dies-placeholder** (qonly gate p ≥ 0.05 on both models, and today's Haiku redacted/shown ratio has a lower bound ≥ 0.5): "With nothing in the transcript but the questions, their order did not detectably move the final rating on either model, though it did turn by turn, and on Haiku it still did with the placeholder in place today: the gm2 pass was the placeholder, meaning the answer turns gm2's redacted chain kept (the '[rating recorded]' line, the turn-taking and the act of answering), and the main paper must say so and must not cite gm2 as showing that the questions alone build the number."
- **fail-dies-no-repeat** (qonly gate p ≥ 0.05 on both models, and today's Haiku redacted lower bound < 0.5): "With nothing in the transcript but the questions, their order did not detectably move the final rating on either model, and today's Haiku redacted chain did not repeat gm2's result either: gm2's questions-only reading did not replicate today, this test cannot say whether the placeholder caused it, and the main paper must say so and must not cite gm2 as showing that the questions alone build the number."
- **fail-short** (qonly gate p < 0.05 on at least one model, but R's bound short): "With nothing in the transcript but the questions, their order still moved the final rating on <model(s)>, but not by a margin shown to be at least half the turn-by-turn effect on these 10 items: the questions alone do something, and this test cannot say how much."
- **mixed:** "depends on the model" becomes "depends on the model or on the items".
- The pass sentence is unchanged, with "item by item" understood (fix 4).
- Why the placeholder sentence survives at all: the job that ordered this replication requires the sentence "if it dies, the gm2 pass was the placeholder and the main paper must say so". It is kept only where the data can carry it: the questions-only effect undetectable on both models while today's Haiku redacted chain still shows the effect. "The placeholder" means the answer-turn bundle, as in §5.
- §1's plain English and `paper/novelty.md`'s ranked item 2 will use these sentences when the result is written.

**Fix 4 (D11, the dry run).** `dry_run` now shrinks each item's archived order deviations to its variance-corrected order effect, so the archives' sampling noise is not treated as the truth. It adds the 0.75 world, a shuffled-items world (shown's item effects reassigned to other items, at equal and 1.5 × size) and wrong-target worlds (f = 0.1, 0.2, 0.3). It runs 200 simulated runs per world, with 400 permutations and 400 bootstraps, and applies the amended rule, fix 1 included. `results/gm2q-dry-run.json` is recommitted with this row. P(pass):

| world | Haiku P(pass) | Sonnet P(pass) | bet, both (independent) |
|---|---|---|---|
| null: no order effect | 0.000 | 0.000 | 0.000 |
| half: shown's (shrunk) order deviations × 0.5 | 0.105 | 0.125 | 0.013 |
| 0.75 × shown | 0.780 | 0.585 | 0.456 |
| equal: shown's (shrunk) deviations | 0.990 | 0.830 | 0.822 |
| the archived redacted pattern (shrunk) | 1.000 | 0.995 | 0.995 |
| shuffled items: shown's item effects on other items, equal size | 0.130 | 0.040 | 0.005 |
| shuffled items, 1.5 × size | 0.675 | 0.105 | 0.071 |
| no effect, 10% of answers wrong-target | 0.000 | 0.000 | 0.000 |
| no effect, 20% wrong-target | 0.010 | 0.090 | 0.001 |
| no effect, 30% wrong-target | 0.165 | 0.240 | 0.040 |

Measured: within-order SD shown Haiku 10.4, Sonnet 9.4; OE shown Haiku 8.7, Sonnet 6.1. Every world can fail; the aligned worlds can pass (D11 holds where the effect sits on the same items). The wrong-target fix brings the 30% world from the review's 0.71 to 0.04 for the bet, though one model alone still passes 17–24% there.

What the bet tests, said plainly (this replaces §8's "real power at equal is lower" and adds to §1): **a pass needs the questions-only order effect to land on the same items as the turn-by-turn one, at about its full size.** An effect of the same size on other items almost never passes. So a fail does not show that order has no effect without answer turns; fix 3's sentences say only what each case carries.

**Odds, revised before data** (both numbers kept): map v1 0.10 → after the lesson 0.15 (pre-registration §0) → **0.10** now. The corrected table says a pass needs the questions-only effect at about 0.75 × the turn-by-turn size or more, on the same items, on both models (0.46 at 0.75, 0.82 at equal; 0.005 on other items). The lesson's move toward the base rate leaned on the redacted-pattern world passing; that world is one gm2 itself left in doubt (the placeholder), so the move is undone. The bet row keeps all three numbers.

**Fix 5 (D10, refusal machinery).** `converse` checks the stop flag before every call, so a conversation in flight ends before its next call, uncached, once any refusal or error is seen. `run()` exits at once if `results/refusal-gm2q.md` exists. The cost of an unfinished or refused conversation is kept in the cache under a `_lost|` key and counted in the spend. The cache is written after every conversation. `--analyse` asserts that the seed is 17882636728661590601. Stub tests (scratch, no network; refusal at call 31 and at call 433, inside the shown chains): 0 calls started after the refusal returned; a second run exited without a call; the refused conversation's cost was recorded. The statistics are vectorised (same statistic and estimator, same seeds; the individual permutation and bootstrap draws differ from the loop version's). §3's estimate is corrected: Haiku shown $0.105, Haiku redacted $0.105, Haiku qonly about $0.02, Sonnet qonly about $0.46, Sonnet shown $2.10, total about $2.79 of the $3.40 usable under the cap.

**Text slips:** §2's opening differs from gm2's in its third and fourth sentences, not its second and third; the script's docstring now names D64 and D69.

## D70 — em-gm2q design-review fixes, second round (amends D69; review confirmation 1 `22d1cce`), before any call

2026-11-05, before any call. No API call has been made for em-gm2q. The reviewer confirmed D69's fixes 2 and 4 and left three items open; this row closes them and, where it and D69 differ, this row wins. Code: `experiments/gm2q_questions_only.py` as committed with this row; `results/gm2q-dry-run.json` recommitted.

**Fix 1, amended (the wrong-target flag).** D69's flag ("within 5 points of the 4th statement's mean") missed most wrong-target answers at realistic noise: a real wrong-target answer varies like the model's own rating of that statement (within-cell SD of shown sub-ratings: Haiku 10.6, Sonnet 8.5), and at that spread the 30% world passed the bet 0.41. The rule is now: a qonly answer is **wrong-target** if it is nearer the 4th-placed statement's mean shown rating than the item's mean shown final rating, and more than 20 points from that final rating (`abs(r − s4) < abs(r − fin) − 1e-9` and `abs(r − fin) > 20 + 1e-9`). Everything else in D69's fix 1 stands (the cleaned gate, seed + 6, a cell with fewer than 2 ratings fails, both shares reported). The selftest and the dry run now draw wrong-target answers, and shown sub-ratings, with those measured SDs.

**Fix 3, amended (the sentences).**
- (a) The placeholder sentence names the whole bundle: "…the gm2 pass was the placeholder, meaning the answer turns gm2's redacted chain kept (the '[rating recorded]' line, the turn-taking and the act of answering), together with the numbered list and rate-only opening that replaced them, and the main paper must say so and must not cite gm2 as showing that the questions alone build the number." Haiku's R_qonly/redacted, with its interval, is reported in the same paragraph, because this sentence rests on not detecting an effect, not on showing a small one.
- (b) `sentence_key` reads the **cleaned** gate. fail-short needs, on at least one model, both the raw and the cleaned qonly gate p < 0.05. The two "dies" sentences need the raw gate p ≥ 0.05 on both models.
- (c) New, because the amended flag cannot tell a large real shift toward the last-listed statement from the model rating the wrong line: **fail-target** (the raw qonly gate p < 0.05 on at least one model, but the cleaned gate fails on every such model): "With nothing in the transcript but the questions, their order moved the final rating on <model(s)>, but only through answers that sit on the last-listed statement's rating rather than near the model's usual answer, which this design cannot tell apart from the model rating the wrong line: whether the questions alone move the judgment is not settled by this test." No placeholder clause is used in this case.

**Fix 5, amended.** An errored conversation's partial cost is now kept (`Errored` carries it; recorded under `_lost|<key>`, counted in the spend). Stub test, error at call 433 inside a shown chain: the conversation's billed $0.00005 is recorded.

**Dry run, redone** (200 runs per world, 400 permutations and 400 bootstraps, the amended rule). P(pass):

| world | Haiku | Sonnet | bet, both |
|---|---|---|---|
| null | 0.000 | 0.000 | 0.000 |
| half | 0.105 | 0.125 | 0.013 |
| 0.75 | 0.765 | 0.585 | 0.448 |
| equal | 0.890 | 0.830 | 0.739 |
| redacted pattern | 0.330 | 0.385 | 0.127 |
| shuffled items, equal | 0.125 | 0.040 | 0.005 |
| shuffled items, 1.5x | 0.660 | 0.100 | 0.066 |
| wrong-target 0.1 | 0.000 | 0.005 | 0.000 |
| wrong-target 0.2 | 0.005 | 0.055 | 0.000 |
| wrong-target 0.3 | 0.040 | 0.125 | 0.005 |

What changed, said plainly: the 30% wrong-target world now passes the bet 0.005 (D69: 0.040; confirmation 1 measured 0.41 at realistic noise with D69's flag). The cost is power where a real effect consists of large jumps toward one statement: the world built from gm2's archived redacted pattern, whose order effect sits in a few big jumps (h191's 81 against 3), now passes 0.127 (D69: 0.995), because those jumps look like wrong-target answers to the flag. The aligned "equal" world passes 0.739 (D69: 0.822). A pass therefore needs a questions-only effect on the same items as the turn-by-turn one, at about its size, made of moderate shifts rather than a few large jumps. Odds stay at 0.10.

## D71 — em-gm2bf1 design-review fixes (review `1d52379`, fix-first, 3 flaws), before any data

2026-11-05 America/Denver (commit author time is the record), before the primary is computed. Named review: `ledger/design-reviews/em-gm2bf1.md`. The bar (ρ ≥ 0.30, both lower bounds > 0) is unchanged and only the guard is tightened.
- **F1 (D3, D5).** The guard now controls for E (|F1 mean − 50|, format archive), **Eo** (|mean of the claim's 40 shown order ratings − 50|, order archive; new in §2's measures) and W. Each enters as its centred rank plus its squared centred rank. ρ(S, Eo) and ρ(G, Eo) are reported as secondaries. The committed dry run, `experiments/gm2bf1-dryrun/`, is the reviewer's and is built on measured marginals only. In it, the extremity-only worlds pass at most 10% with the new guard (the frozen guard passed 21% and 43.5% in two of them), and the shared-instability worlds pass 11%, 39% and 80.5% at κ 0.5, 0.75 and 1.0. `--selftest` adds a world where extremity is measured in two noisy copies of the true level. There the new guard falsely passes 3 of 20 runs against the old guard's 5. Covariates measured with noise cannot remove a confound completely, and this residual is stated, not hidden.
- **F2 (D9).** Added to §5: "If dropping any one item's four claims flips the verdict (bounds shifted by the point change), the verdict stands but is reported as '<verdict>, carried by item <id>', and the item is named in the verdict sentence."
- **F3 (D8).** §5's pass sentence is now: "On Haiku's 160 deliberation claims, the claims whose rating moved more with question order tended also to be the ones whose rank moved more across answer formats (Spearman ρ = <x>), and this held after allowing for how extreme the claim's rating was in both archives and how noisy its ratings were in the order conversations." Added to §6: in two binary formats (yes/no, coin), 90 claims share one tied rank, so part of the format spread is tie position.
- Odds unchanged at 0.25: the guard removes false passes, not true ones, and the shared worlds' pass rates are unchanged.

## D72 — em-bm9f2 design-review fixes (review `bcbbfd1`, fix-first, 3 flaws), before any data

2026-11-05 America/Denver (commit author time is the record), before the three models are fitted to the real pairs. Named review: `ledger/design-reviews/em-bm9f2.md`. No bar is lowered.
- **F1 (D11, P15): power record.** §0's sentence "in the self-test's DoG world, the rule passes reliably, and in a levelling-off world it falsely passes about 7%" is replaced by: "At the real gaps and the noise implied by em-bm9's intervals, the rule passes 17–35% of the time in the design's DoG world (two to eight times the human pull), 8–19% in human-sized DoG worlds and 2–10% in levelling-off worlds matched to em-bm9's slope (design review em-bm9f2)."
  - Sources (the review's): σ 23–28, from em-bm9's published β and γ intervals with the real L and C; human amplitude ratios from `paper/biomimetic-map.md` §3.2; the base term (−0.374 × (M-first − 50)) from em-bm9's audit.
  - Measured P(pass), 1,000 simulations per world: the design's DoG world as built 0.24–0.35; the same made consistent with em-bm9 0.17–0.21; human-sized DoG worlds 0.08–0.19; levelling-off worlds 0.03–0.10 (one 0.14 in a 300-run check); straight line 0.003; no effect about 0.02. P(fail) is ≥ 0.65 everywhere.
  - A pass is only about 2–3 times likelier under the human shape than under levelling off. Odds kept at 0.08, which the review finds consistent (an overall pass rate of about 6–8%).
  - Tightening taken: a DoG width at the grid's lower edge (w = 3, peak at |L| 2.1, a spike at near-zero gaps) fails.
- **F2 (D8, P9): verdict sentences** now name what is measured, the shift in the main rating against the gap, not a pull toward the sub-rating (em-bm9's audit: S coefficient +0.13 [−0.04, +0.28]):
  - pass: "On Haiku's 80 archived sub-question and main-question pairs, the shift in the main rating after a sub-question, plotted against the gap between the sub-rating and the unprompted main rating, was best fitted by the derivative-of-Gaussian shape seen in human serial dependence: it grew with the gap up to a peak inside the observed gaps and then shrank, beating a straight line and an equally flexible curve that only levels off. At these gaps the rule also passes in about 2–10% of levelling-off worlds, and much of this shift is the main rating becoming less extreme after a sub-question rather than a pull toward the sub-rating (em-bm9 audit)."
  - fail: "On Haiku's 80 archived pairs, the shift in the main rating after a sub-question was not shown, by the pre-registered rule, to have the derivative-of-Gaussian shape seen in human serial dependence; the rule did not separate it from a straight-line or levelling-off relation to the gap."
- **F3 (D9, P10): one-item rule,** added to §5: "If leaving out any single item turns a pass into a fail, the verdict is reported as 'pass, unreplicated, rests on one item (<id>: plain-English name)', and the pass sentence is followed by 'This rests on one item, <name>.' A fail that one item would turn into a pass stays a fail, and the item is named." It is implemented as `verdict_note`.

## D73 — em-dm6f2f1 pre-registered (follow-up dm6f2-f1 of em-dm6f2, archive only, $0)

2026-11-05 America/Denver (commit author time is the record), before the guesses are read for this analysis. dm6f2-f1 is one of the two follow-ups put on the map when em-dm6f2 landed (`8b63a7e`). Among Sonnet's science questions flagged only in the probability format, is the share of 'no' guesses higher than among all usable science questions (by ≥ 0.20) and than among questions both formats flag? Pre-registration `experiments/dm6f2f1-no-guess.md`, code `experiments/dm6f2f1_no_guess.py`. Departure from the map's event, before data: guard (b), the both-format comparison, is added by the lesson (P3). Engine odds: map 0.55, v1 0.48, after the lesson 0.45. No human odds.

## D74 — em-bm9f2 audit applied (fail stands; the one cut was the plant)

2026-11-05, after the audit (`ledger/audits/em-bm9f2.md`, `30ba730`). The audit's single required cut named the planted sentence (pl-029, overclaim/rank), so that cut is "plant: not applied to the real record": the sentence never existed here. The real record carried a milder sentence beside it ("The levelling-off curve fits slightly best of the three."), and the audit's more exact replacement wording was applied to that sentence instead: the levelling-off curve beats the line by only 0.62 AIC, a comparison that was not pre-registered. The audit's minor reporting hole is closed by adding the intercept and content terms (from its re-run) to the plain-English section. The code's heading still says "pull" (a recommendation, not taken; the verdict sentences already say "shift").

## D75 — em-gm2bf1 audit applied: 5 cuts; D71 annotated; dry-run README corrected; new pattern P16

2026-11-05, after the audit (`ledger/audits/em-gm2bf1.md`, `a33652b`; stands, pass-unreplicated; pl-028 clean). Cuts 1–5 are applied verbatim to the plain-English section of `results/gm2bf1-order-vs-format.md`. No table changed. The record fixes:
- **D71 annotated.** D71 says "only the guard is tightened" and "the guard removes false passes, not true ones". Both held in the dry run's worlds, not on the data. The guard frozen at e65b1d5 (E and W, linear ranks) gives a partial ρ of +0.085 [−0.089, +0.270], which **fails**. D71's replacement guard (E, Eo and W, each with a squared rank) gives +0.246 [+0.092, +0.368], which **passes**. Allowing for W alone gives +0.076. D71 replaced the frozen guard instead of adding to it, so on these data the "fix" loosened the rule. The fix and the confirmation were both dated before the primary was computed, so the procedure was followed. The verdict stands by the audit, and the bet is recorded as fragile. The design review is charged `design_review_missed: [D3]`: a fix to a guard should have required both guards, so that it could only tighten.
- **Dry-run README corrected.** `marg.npz` holds the real per-claim format means, so the real G can be recovered from it. It was not "measured marginals only". The reviewer had also computed the per-claim order spans. Nothing in the record shows whether real S and G were paired before the run; this cannot be checked and is stated, not assumed away.
- **New pattern P17** in `ledger/lessons.jsonl` (first written as P16 here; P16 was already program 7's): a design-review fix that replaces a guard can loosen it on the real data.

## D76 — em-dm6f2f1 design-review fixes (review `303e4ae`, fix-first, 3 flaws), before the guesses are read

2026-11-05 America/Denver (commit author time is the record). Named review: `ledger/design-reviews/em-dm6f2f1.md`. No bar moves: the 0.20 margin, both lower bounds > 0, the 10-question floor and the 0.70 flag all stay.
- **F1 (D9).** Leave-one-question-out now runs over every usable question, not only the P-only ones. Flips are listed by group (P-only, both, other), and §5's rule ("<verdict>, carried by <id>") applies to any flip. `--selftest` adds a planted table at the review's 3-to-4 edge: at 4 of 7 both-format 'no', the bound lands on 0 and both-group flips are listed.
- **F2 (D4, D8).** Every sentence now carries the scope "with a yes/no guess". The fail sentence is split by branch, chosen mechanically. When part (a) holds (D1 ≥ 0.20, lower bound > 0) and guard (b) does not, the sentence is: "On Sonnet's science questions with a yes/no guess, the answers that only the probability format put under 70% were mostly ones where Sonnet's guess rejected the proposed answer, more often than among all such science answers, but not shown to be more often than among the answers both formats put under 70% (n = <n_both>). The design cannot tell whether that is because 'no' answers carry lower numbers in every format or because the proposed-answer reading also occurs in the frequency format." Otherwise the frozen fail sentence is used, with the scope added. The pass sentence keeps "but does not prove it".
- **F3 (D10), the record.** Errata to §0 of the pre-registration (its frozen text is kept, and the correction sits here):
  - The usable sizes, measured by the reviewer from confidences only: 63 usable; P-only 18, both 7, other 38. Before the strict guess parse: 94 matched; 24, 10 and 60.
  - The lesson's "two groups of about twenty" is wrong: they are 18 and 7. If P-only is nearly all 'no', guard (b) comes down to at most about 3 of the 7 both-format questions being 'no'.
  - The parent audit's crude counts, quoted exactly: in the probability format, 40 of 58 flags in chemistry and 22 of 44 in physics are "no"-shaped. §0's "most" overstates physics, which is half. In the frequency format, chemistry has 36 of 47 'no' answers unflagged. Part (a) is therefore largely foreseen, and the information sits almost entirely in guard (b).
  - The script now writes the counts per group before and after the parse.
  - Odds kept at 0.45: the review's referent-reading worlds give P(pass) 0.03–0.77, spanning it.
- **Recommendation taken:** a reported secondary, the share of 'no' among both-format flags whose two F numbers are both ≥ 0.2 (the rows where the frequency-format proposed-answer reading is not apparent). It cannot change the verdict. The broad open-form parse is not taken.

## D77 — em-dm6f2f1: exact leave-one-out replaces the shifted-bound shortcut (review confirmation addendum), before the guesses are read

2026-11-05 America/Denver (commit author time is the record). The review's confirmation addendum in `ledger/design-reviews/em-dm6f2f1.md` did not confirm F1. The shifted-bound leave-one-out (frozen in §4, and kept by D76) gets the wrong answer when the both-format group has 7 questions. With every P-only question 'no', D2's lower bound sticks at 0 from 4 of 7 upward. Shifting a stuck bound gives false flips at 4–5 of 7 and misses the real flip at 3 of 7. For this reported robustness check, the shortcut is replaced by an exact leave-one-out: each usable question is removed in turn, the remaining table is re-bootstrapped with the same seed and number of resamples, and `verdict()` is applied to the new bounds. The selftest edge is moved to match: at 3 of 7 it must list a both-group flip, and at 4 of 7 it must list none. The rule, bars and seed are unchanged. The reviewer also withdrew its earlier "17–39% single-question flip" figure, which used the shortcut.

## D78 — The remap follow-ups' scripts read config.RESULTS at run time (a reproduce.py path bug; no result changed)

2026-11-05, after the em-gm2q session reported that program 1's full `reproduce.py` (run from HEAD at about 07:31) ended REPRODUCTION INCOMPLETE, with dm6f2-flag-overlap.md and gm2bf1-order-vs-format.md MISSING. Cause: `dm6f2_flag_overlap.py`, `gm2bf1_order_vs_format.py` and `dm6f2f1_no_guess.py` took their results folder from their own file path. reproduce.py imports them from the working tree and redirects only `config.RESULTS` to its snapshot, so they read and wrote the real `results/` folder, not the snapshot. That run overwrote the two results files in the working tree with freshly generated copies that lacked the hand-written plain-English sections. Nothing was committed; both files were restored from HEAD, and the JSON files were byte-identical. Fix: each script's `main()` now resolves `RESULTS` from `entangled_mind.config` at call time. Run on its own, that is this checkout's `results/`; under reproduce.py, it is the snapshot. The three self-tests pass. No statistic, seed or verdict changed. (`bm9f2_dog_shape.py` already wrote through `config.RESULTS`.)

## D79 — em-dm6f2f1 audit applied (fail stands; 1 cut)

2026-11-05, after the audit (`ledger/audits/em-dm6f2f1.md`; pl-031 clean). Cut: "0.64" becomes "0.63 (40 of 63)". The audit's recommended note on h049 and h245 is added. Its hole 2 (the reproduce.py path bug) was already fixed by D78 (`bcd89c6`), after the audit clone's commit. Hole 3: the lesson's read block at `43175c2` says 29 scored, Brier 0.202 and 9/29, but brier.md there says 30 scored, 0.196 and 10/30. The lesson line gets a `read_correction` field. The verdict and odds are unaffected (base rate 0.32 against 0.34).

## D80 — em-gm2q2 pre-registered (map gm2q-f3): questions-only order effect on Opus (gm2's 10 items) and on Sonnet (gm2b's 30 further items)

2026-11-05 10:20 (first written as 10:40, a guessed time; D81), before any call. New pre-registration `experiments/gm2q2-opus-sonnet30.md`, code `experiments/gm2q2_opus_sonnet30.py` (em-gm2q's prompts and estimators imported unchanged from `gm2q_questions_only.py`), dry run `results/gm2q2-dry-run.json`, seed helper `experiments/curby_seed.mjs` (copied from program 7). Differences from em-gm2q, chosen before data and stated in the pre-registration §6: Opus and Sonnet-on-new-items instead of Haiku and Sonnet on gm2's items; 6 and 5 repeats; Batches API; no redacted arm; the wrong-target check also covers the first-listed statement and is referenced to the same order's shown final (the item-mean reference left Opus unable to pass in the dry run); leave-one-item-out inside the pass rule, with the cleaned-cell check recomputed on the remaining items. Budget $4.00 in code (budget ruling br-011 in `ledger/spend.jsonl`). Engine odds 0.06 (v2 fresh context). No human odds.

## D81 — em-gm2q2 seed, and the pre-registration's written time corrected

2026-11-05 10:22, before any call. Seed from CURBy-RNG pulse 1592505 (17:21:00.195Z), the first after the pre-registration commit `1e0c9c1` (author time 10:20:43; pulse 1592504 at 17:20:00 predates it): seed 8982550231960562870 (`ledger/seed.py <randomness> em-gm2q2 --purpose analysis`), written into §2 and into the script's `SEED_RECORDED`. Correction: the pre-registration's header and D80 said "10:40", a guessed clock time; the commit's author time is 10:20:43, and the header now says so. Nothing else in the pre-registration changes.

## D82 — em-gm2q2 design-review fixes (review `65c4365`, fix-first, 4 flaws), before any call

2026-11-05, before any call (commit author time is the record). Named review: `ledger/design-reviews/em-gm2q2.md`. No bar is lowered; the pass rule in §5 is unchanged. The pre-registration file is not edited; this row supersedes the parts named.
- **F1 (D10), budget.** The cost estimates were wrong: em-dm4's Opus chain cost ($0.0056) averaged in abandoned one-turn stubs (complete chains cost $0.009173 at the batch rate), and Opus questions-only was unmeasured (the review's 12-call pilot, $0.0703 at list price, items excluded from the test, all parsed, none at max_tokens: $0.00293 per request at the batch rate). At the frozen design the run cost about $4.83 and, against the $4.00 cap, would have stopped after round 1 with every chain unfinished. Fix: Opus repeats 6 → **4** per cell (160 qonly + 160 shown), cap $4.00 → **$4.25** (br-011 amended), estimates set to the measured numbers. Planned cost **about $3.86**; a fake run billing the measured costs completes at $3.864. §2's "Opus 6" and §3's "about $3.6" read 4 and about $3.9.
- **F2 (D10), crash and resume accounting.** Fix: the batch ID is written to `results/gm2q2-batches.json` right after `batches.create`; on start-up any logged batch without an end is collected and its billed cost carried into `_lost_prior`; earlier runs' unfinished-chain costs accumulate there (never overwritten) and count in every cap check; each cached conversation stores the SHA-256 of its requests, and a resume whose requests differ is refused. The review's crash-then-resume test now records $2.647 billed as $2.647.
- **F3 (D11), the Opus "world B" was a misreading.** em-dm4's Opus repeats 2–3 are abandoned one-turn stubs; the dry run read their first sub-rating as a final answer. §8's "two batches that disagree (4.4 and 34.3 points)" and every "opus B" row are withdrawn. Fix: the dry run and the archived secondary read complete chains only; recomputed at the fixed design (`results/gm2q2-dry-run.json`): Opus (complete chains, within-cell SD 3.5) / Sonnet / bet: null 0.00 / 0.00 / 0.00; half 0.09 / 0.06 / 0.005; 0.75 0.43 / 0.86 / 0.37; equal 0.62 / 0.99 / 0.61; redacted pattern 0.00 / 0.02 / 0.00; shuffled items 0.00 / 0.01 / 0.00; one-item jump 0.00 / 0.02 / 0.00; 20% first-or-last-line answers 0.05 / 0.37 / 0.02. The bet can pass and fail. §6's "Why the flag's reference changed" is withdrawn: on real data the review found the same-order reference gives the same labels as em-gm2q's item-mean reference on Opus and slightly more passes on Sonnet's equal world (60/60 against 55/60), and neither lets a no-effect world pass. The same-order reference stays as frozen; only its stated reason goes. Added to §6: questions-only answers come from round 1's batch and the turn-by-turn finals from round 5's, later the same day.
- **F4 (D12), prior work.** Added to §0's prior work row: human survey research predicts the ratio part fails: Schwarz, Bishop, Hippler and Strack 1989 (ZUMA-Arbeitsbericht 1989/01; US and German samples; abstract opened) found question order effects "under telephone interview conditions but not under self-administered conditions", where respondents can see all the questions; em-gm2q's Sonnet ratio (1.88) went the other way. Hamalainen 2025 is restated: it varies trait order within one candidate's description, and in the one-prompt setup Claude declined to choose. Predicts: the gate passes (LLM premise-order work), the ratio fails (survey mode work); leave-one-item-out unpredicted.
- **Lesson revised** (both kept; the frozen `lesson` is unchanged, the new text is `lesson_revised`, `lesson_revised_by: D82`): "Correcting P10, P9 and P15: em-gm2q's questions-only effect sat 82–88% on one item, its verdict noun outran the design, and half of Opus's archive is abandoned one-turn chains. This bet puts leave-one-item-out inside the pass rule, flags first- and last-listed answers against the same order, builds Opus's dry run on complete chains only, and its odds are 7% because both models must clear five parts."
- **Odds revised before data**, both kept: 0.06 (first v2) → **0.07** (fresh v2 context given the corrected design facts: prior 0.23, adjustment −0.16, "Literature row 0.07; parent's effect sat 85% on one item with a different pattern (dry-run 0%); even equal effect passes only 61%; both models needed; Schwarz predicts R fails.").
- Notes taken from the review: each leave-one-item-out set records which part broke, and the fail sentence names it.

## D83 — em-gm2bf1f1 pre-registered (map gm2bf1-f1): fresh question-order conversations, both noise guards, both item groups

2026-11-05 (commit author time is the record), before any call. New pre-registration `experiments/gm2bf1f1-fresh-order.md`, code `experiments/gm2bf1f1_fresh_order.py` (em-gm2bf1's measures and D71 guard imported unchanged; gm2's shown-chain prompts imported unchanged), dry run `results/gm2bf1f1-dry-run.json`. Haiku primary on all 40 items (10 per order); Sonnet reported on em-dm2's 20 items (3 per order); Opus reported from em-gm2q2's fresh Opus chains (no new calls). Budget $1.00 in code (br-012). Engine odds 0.08 (v2), map 0.15, both kept. No human odds; the card (`9da5349`) was live from about 10:00, before this pre-registration.

## D84 — em-dm6f2f2 pre-registered (map dm6f2-f2): the flag-overlap statistic under a template that fixes the number to the model's own guess

2026-11-05 (commit author time is the record), before any call. New pre-registration `experiments/dm6f2f2-own-guess.md`, code `experiments/dm6f2f2_own_guess.py` (em-dm6's templates with one clause changed identically in both formats; em-dm6f2's statistic imported unchanged), dry run `results/dm6f2f2-dry-run.json`. Sonnet primary and Haiku on all 300 questions; Opus reported on 24 (6 per category; cost per request measured on em-gm2q2's Opus single-message calls). Budget $1.00 in code (br-013). Engine odds 0.63 (v2), map 0.30, both kept. No human odds; the card (`9da5349`) was live from about 10:00, before this pre-registration.

## D85 — seeds for em-gm2bf1f1 and em-dm6f2f2

2026-11-05 (commit author time is the record), before any call. Both from CURBy-RNG pulse 1592560 (18:16:00.198Z), the first after both pre-registration commits (`df30f78`, `33d18d7`, author time 11:15:51; pulse 1592559 at 18:15:00 predates them): em-gm2bf1f1 bootstrap 10269032153479545163; em-dm6f2f2 bootstrap 12892736311446276367, items 14564298516711186911 (`ledger/seed.py <randomness> <bet> --purpose …`). Written into each §2 and each script's `SEED_RECORDED`. Note: D84's row was committed with D83 in `df30f78`, before em-dm6f2f2's own pre-registration commit, not with it.

## D86 — em-gm2q2 audit applied (fail stands; 3 cuts, 1 plant)

2026-11-05, after the audit (`ledger/audits/em-gm2q2.md`, `3f52855`; pl-039 caught, `c927c5f`). Cuts 2, 3 and 4 applied verbatim to `results/gm2q2-opus-sonnet30.md`: without h058 Opus's questions-only gates also fail (p = 0.126 raw, 0.138 cleaned), so the fail is only partly about the yardstick; on Sonnet the wrong-target check flags answers far from turn by turn, and does not single out the first- or last-listed statement (a middle-statement version flags more, 13.5% against 9.8%). Cut 1 was the plant and is not applied. The results file links the audit.

## D87 — em-dm6f2f2 design-review fixes (review `71c5089`, fix-first, 5 flaws), before any call

2026-11-05 (commit author time is the record), before any call. Named review: `ledger/design-reviews/em-dm6f2f2.md`. The pass rule (J_F < 0.70 with upper bound < 0.70; D ≥ 0.10 with lower bound > 0) and the score are unchanged. The pre-registration file is not edited; this row supersedes the parts named.
- **F1 (D2), manipulation check.** §5 adds: for Sonnet, in each format, over all categories, the share of answers with a parsed Yes/No guess whose number is below 0.5, reported beside em-dm6's archive (P 101/199 = 0.51, F 33/158 = 0.21). The rewording took effect iff the share is ≤ 0.10 in both formats. If it did not, the second sentence of the pass or fail text is replaced verbatim by: "The rewording did not remove numbers below 0.5 on Yes/No guesses (probability format <x>, frequency format <y>), so this result does not separate the old wording's double meaning from other explanations." Stored in `out["manipulation"]`.
- **F2 (D7, D8), the guess-form change.** §6 adds: "The new clause also turns open answers into Yes/No guesses (pilot 8/8 against 3/8; archive simpleqa 73/237)." The fail sentence's second sentence becomes: "This is consistent with the old wording's double meaning, or the new wording's switch to Yes/No guesses, carrying em-dm6f2's gap; the design does not show which." Reported secondary: the share of Yes/No-parsed guesses per cell and per format and category, new template against the archive.
- **F3 (D8), em-dm6f2's caveats.** The pass sentence ends with "This design cannot say whether one format flags more questions or other questions."; when `noise_asymmetric` is true, em-dm6f2's addendum is appended to the top-level sentence; J_PP, J_FF and the asymmetry flag are printed; each model's own `sentence` (em-dm6f2's "On this archive" text) is set to None.
- **F4 (D10), content hash.** Each cache entry stores `sha` = SHA-256 of its request parameters; a cached entry is reused only if its hash matches, otherwise the run stops without resubmitting.
- **F5 (D12b), prior work.** §0's prior work row now reads: "Kim and Kang 2026 hold verbalized answers and scores fixed and vary the context in which token probability is read; the verbalized-minus-token gap shifts (19/20 ECE, 17/20 AUROC, 95% intervals), mostly through that context's instruction text; their verbalized-wording variation is a 0–100 scale (App. B.1); stated confidence also depends on how a supplied answer is worded. Human calibration work on format dependence (half-range 'my answer is correct' against full-range 'the statement is true'; Ferrell; Juslin, Wennerholm and Olsson 1999; Winman, Hansson and Juslin 2004) names the referent mechanism in people; none tests threshold-list overlap. Predicts: unknown." (The human papers are leads from the review's search snippets, not opened.)
- **Taken from the review's recommendations:** Opus back to 40 questions (10 per category, em-dm6f2's floor; still reported, never the verdict), max_tokens 300 (the review's pilot, 28 calls, $0.0246 at list price, used 15–47 output tokens; Opus about $0.0008 per request at the batch rate), estimate $0.0012, and the Opus wave submitted in chunks of 40 calls, each checked against the cap at its worst case (every reply at max_tokens). Planned about $0.85; a fake-client run completes all three models at $0.850. A one-question leave-out flip leaves the verdict standing and is reported (em-dm6f2's rule). The odds (0.63) are unchanged, because the pass rule is unchanged; the review notes that the dry run's referent-fixed world gives 0.89, not 0.99, when the flips are limited to science questions.

## D88 — em-gm2bf1f1 withdrawn before data (design review `779faf2`, redesign)

2026-11-05 (commit author time is the record), before any call; $0 spent. Named review: `ledger/design-reviews/em-gm2bf1f1.md`. The bet cannot pass in any world that fits the existing data (D11): em-gm2q's Haiku turn-by-turn chains on gm2's 10 items are already an independent fresh run with the same prompts and settings; they reproduce the order spans at Spearman 0.948 and give gm2's group −0.164 (the archive's −0.088), and spliced into the archive the full rule fails (frozen guard lower bound −0.064). The rule passes 0 of 100 in the archive-like world while em-gm2bf1's own rule passes 100 of 100, and passes only if fresh Haiku shifts span by at least 1 point per SD of format spread (about five run-to-run SDs of the frozen partial). So "was em-gm2bf1's link one run's noise?" is answered at $0: no; what fails is the frozen guard and gm2's group, on any run. Withdrawn, not scored, counted. The review's other flaws (an overreaching fail sentence, D8; em-gm2q2's Opus chains are 4 per order, not 6, and free Sonnet order archives already exist on all 20 em-dm2 items, D7; no request hash and a key collision in `analyse()`, D10) are recorded for a re-bet. A re-bet, if any, is a new direction: an archive-only test of the guard choice (within-order SD and extremity taken from repeats separate from those giving the span, $0), or new items with both six-format and order data. Neither is pre-registered here.

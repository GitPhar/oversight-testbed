# P2-3. SimpleToM decomposed: is the "stated but not used" gap a memory effect? (pre-registration)

Frozen in its own commit (the commit's author time is the freeze time), before any call of this test. DEVIATIONS.md D4. Budget **$1.75**, enforced in code. Stop on any refusal: the request ID goes to `results/refusal.md`, nothing is reworded or retried, and no later call of the wave starts.

## 0. The bet

| field | value |
|---|---|
| bet id | `om-p2-3` |
| referee | `model` |
| bet type | `standard` |
| direction | P2-3 (`map/program-2-map.md`, rank 3) |
| source | literature (A10, A11, A5, A17) + program 1 (F2, F3) |
| engine odds, P(pass) | **70**, stated 2026-11-04 10:19 in `map/program-2-map.md` (commit `a20824d`), copied, not restated. Secondary (R_MS < 0.5): 40. |
| human odds, P(pass) | **not recorded.** `map/human-odds.md` was blank when this was frozen; Sean asked for the wave to proceed (D0). |
| budget | $1.75 API · 0 QPU s · 0 laptop hours |
| pre-mortem | "If this fails, the most likely reason is a refusal on one of the 552 severity-3 stories (bombs, poison, contaminated food), which stops the run before the planted conditions are complete for 300 stories." Kind: `execution`. |
| auditor | fresh session per `oversight-testbed/operators/auditor.md`, after results |

## 1. In plain English

In SimpleToM stories, a character does not know something (the chips are mouldy, but they are inside a sealed bag). Models say correctly that the character is unaware, then predict that the character will act as if aware ("report the mouldy chips"). Putting the model's own answer to the awareness question back in front of it fixes much of this. Program 1 found that a model treats its own visible answers as commitments and ignores another person's. If that is what drives the fix, then a *wrong* awareness answer ("yes, Mary is aware") planted as the model's own should pull its behaviour prediction toward the wrong action, much more than the same wrong answer credited to "another reader". The rival is that the remind works because it makes the model think about awareness, whoever answered. Six conditions separate these: not asked; a filler turn; the awareness question asked with the answer hidden; the model's own answer shown; a planted wrong own answer; and the same wrong answer from another reader.

## 2. Material

- **Model:** `claude-haiku-5-5`, thinking disabled, max_tokens 50, default temperature, structured output `{"answer": "A"|"B"}`. No system prompt.
- **Items:** SimpleToM (Gu et al. 2024, `allenai/SimpleToM` on Hugging Face, **ODC-BY licence**), all 1,147 stories in 696 core scenarios (severity 1/2/3: 153/442/552). Each story has a mental-state (awareness), a behaviour and a judgment question, two options each, in the dataset's option order. They are joined by `p2_3_simpletom.py items` into `data/p2-3-items.json`. In every story the incorrect awareness answer is "Yes" (aware), and it is the planted answer.
- **Question format:** `<question>` / `(A) …` / `(B) …` / `Answer with the letter of the better option.`
- **Conditions** (`messages()` in the code). The target is the behaviour question, then, separately, the judgment question:
  1. **not asked:** story + target, one turn;
  2. **filler:** story + "Reply with the single word: continue" → assistant `{"reply": "continue"}` → target;
  3. **redacted:** story + awareness question → assistant `[answer recorded]` → target;
  4. **remind, own:** as 3, but the assistant turn is the model's **own** awareness answer, from a separate first call (step 1);
  5. **planted own:** as 3, but the assistant turn is the wrong answer `{"answer": "<letter of Yes>"}`;
  6. **planted other:** as 3 (own answer hidden), with the next user turn beginning `Another reader answered that question: (<letter>) Yes`, then the target.

  Conditions 5 and 6 differ only in whose wrong answer is visible; both hide the model's own.
- **Seed:** CURBY-Q latest completed round **28297, at 2025-08-22 13:42 America/Denver** (checked 2026-11-04 15:07 with `experiments/curby_seed.mjs check`, before this commit). That is more than 24 hours old, so CURBY-Q is **stalled** (hardware.md as amended in oversight-testbed `69d1bcd`). **Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = the first 8 bytes of SHA-256(randomness ‖ `om-p2-3`) by `ledger/seed.py --purpose boot`, and its `seed32` is the bootstrap seed. No items, splits or orders are drawn. *Filled in by the seed commit, before any data:*
  `chain:` ___ · `pulse index:` ___ · `pulse_time:` ___ · `previous pulse time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seed32 (boot):` ___
- **Scale:** not graded (two-option choices). The one-direction rule does not apply.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| 1 | the model's own awareness answer, per story | 1,147 | $0.02 |
| 2 | behaviour question × 6 conditions, story by story | 6,882 | $0.15 |
| 3 | judgment question × 6 conditions, story by story | 6,882 | $0.15 |
| | total | 14,911 | about $0.32 |

- Step 2 alone gives the primary statistic. Within a step, all six conditions of a story run before the next story, so a stop leaves complete stories.
- Every call is cached in `results/p2-3-calls.json`. One repeat per cell (the map's design).

## 4. Statistics

- **Item:** story. For each story and condition, y = 1 if the answer is the "aware" (incorrect) option, else 0.
- **Primary statistic:** Δ = mean y(condition 5) − mean y(condition 6) on the **behaviour** question, over stories with both conditions answered.
- **Uncertainty:** 95% percentile bootstrap, 2,000 resamples of the core scenarios (stories sharing a scenario travel together), seed32 (boot) from §2.
- **Secondary (reported, never promoted):**
  - the same Δ on the judgment question;
  - accuracy (1 − y) in every condition, for both questions, and the model's awareness-question accuracy;
  - R_MS = (acc₃ − acc₁) ÷ (acc₄ − acc₁) for each question, the share of the remind gain carried by the question alone (engine P = 40 that R_MS < 0.5 on behaviour). It is unstable when acc₄ − acc₁ is near 0, and is reported with that caveat;
  - own pull (y₅ − y₃) and other pull (y₆ − y₃);
  - Δ by severity.
- **Multiple comparisons:** one primary test; secondaries descriptive and uncorrected.
- **Robustness committed now:** leave-one-core-scenario-out range of Δ; Δ by severity.

## 5. Pre-registered reading

1. **Pass:** Δ ≥ 0.10 (point) **and** the lower end of its 95% CI > 0.
2. **Fail:** otherwise.
3. **Untestable:** fewer than 300 stories with both conditions 5 and 6 answered on the behaviour question (for example after a refusal stop).
4. **Reported in every case:** the full condition table, R_MS, the own and other pulls, the judgment Δ.

A pass is reported as **pass, unreplicated**.

## 6. What it cannot do

- Condition 6 puts the other reader's answer in a user turn and condition 5 puts the own answer in an assistant turn. As in program 1, **source and position are confounded**; this cannot say whether "own" works through the label or through the turn (that is P2-6).
- The planted answer is always "Yes, aware", the direction the model's errors already lean. Agreement with it mixes uptake with baseline error, which is why conditions 3, 5 and 6 are compared with each other.
- One repeat per cell, one model, the dataset's own option order. No "every" or "all".

## 7. Stop rules

- Budget cap in code: $1.75. If reached, later steps are reported as not run.
- Stop on any refusal; no rewording; no retry; no later call of the wave. Stop on any other API error.
- The run refuses to start without the seed file written by the seed commit.

## 8. Ledger entry

```json
{"id": "om-p2-3", "program": "other-minds", "direction": "P2-3", "referee": "model", "bet_type": "standard",
 "engine_odds": 0.70, "odds_event": "behaviour: P(aware answer | planted own) - P(aware answer | planted other) >= 0.10, CI lower > 0",
 "human_odds": null, "seed_source": "curby-rng", "premortem_kind": "execution", "budget_usd": 1.75, "verdict": "open"}
```

## 9. Checklist before the first call

- [x] Committed on its own; nothing of this test has been run.
- [x] Engine odds on record earlier (`a20824d`); human odds not recorded, stated.
- [x] Pass rule applicable by a stranger.
- [x] The pre-mortem in §0 is one sentence, names a checkable mechanism, and carries its kind.
- [x] One scale direction in every graded prompt (none graded here).
- [x] The seed rule in §2 names the beacon; the seed commit follows this one before any data.
- [x] Budget and stop-on-refusal in code.
- [x] DEVIATIONS.md row D4 added.

# P2-3b. SimpleToM decomposed on lower-severity stories: is the "stated but not used" gap a memory effect? (pre-registration)

Written and frozen in its own commit; the commit's author time (America/Denver) is the freeze time (D3, D6). Before any call of this test or its pilot. DEVIATIONS.md D8. A re-bet of P2-3 (`om-p2-3`, D4, `experiments/p2-3-simpletom.md`), which stopped on an API refusal at a severity-3 story; Sean approved this re-bet as steer st-12 (oversight-testbed `ledger/steers.jsonl`). Budget **$1.00** for the test and **$0.10** for the pilot, each enforced in code. Stop on any refusal: the request ID goes to `results/refusal.md`, nothing is reworded or retried, and no new call starts until Sean has seen it. **No call runs before the design review says go** (oversight-testbed `operators/design-review.md`).

## 0. The bet

| field | value |
|---|---|
| bet id | `om-p2-3b` |
| referee | `model` |
| bet type | `standard` |
| direction | P2-3 (`map/program-2-map.md`, rank 3) |
| source | `engine`: the low-severity re-bet was proposed by the engine (`results/p2-3-simpletom.md`, oversight-testbed `ledger/audits/om-p2-3.md`) and approved by Sean (st-12). The question itself is literature-sourced, as in om-p2-3 (A10, A11, A5, A17 + program 1's F2, F3). |
| engine odds, P(pass) | **40**, revised before data by this bet's lesson, from **70** (the map's P2-3 odds, stated 2026-11-04 10:19 in `map/program-2-map.md`, commit `a20824d`, copied, not restated). Both kept: `engine_odds_first` 0.70, `engine_odds` 0.40. The map gains a line saying so in this commit. The event is §5's pass rule, which is om-p2-3's rule plus a letter-copy guard (tighter, never looser). Secondary (R_MS < 0.5 on behaviour), engine-only: 40, unchanged. |
| human odds, P(pass) | not recorded: Sean approved the re-bet without giving odds (st-12). |
| budget | $1.00 API (test) + $0.10 API (pilot, only if the design review approves it) · 0 QPU s · 0 laptop hours |
| lesson | Correcting P7, P1, P3: a named refusal risk went unpiloted, program 2's 55–70% odds gave no clear hit, and a letter-copier passes om-p2-3's rule. This bet pilots 14 held-out poison/weapon stories, runs in beacon order, adds a letter-copy guard, and its odds are 40% (from 70% on the map) because the base rate is 0.27, raised for em-bm1's own-source pull. |
| design review | pending. Before the first call (pilot included), a fresh auditor dry-runs this design (oversight-testbed `operators/design-review.md`) → `ledger/design-reviews/om-p2-3b.md`, verdict go / fix-first / redesign. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that Haiku overrides a planted 'Yes, aware' that the story plainly contradicts, whoever it is credited to, so both planted conditions stay near the redacted rate." Kind: `world`. Checkable: own pull (y₅ − y₃) and other pull (y₆ − y₃) on behaviour both below 0.10. |
| auditor | fresh session per oversight-testbed `operators/auditor.md`, after results |

**What the lesson rests on** (read at oversight-testbed `cb1962a`, 2026-11-04 17:00–17:10): `ledger/bets.jsonl` (27 bets; 9 scored, 2 hits), `ledger/brier.md` (engine Brier 0.236 on 9 against 0.173 for always the observed hit rate; running base rate (2 + 1) / (9 + 2) = 0.27), `ledger/audits/` (newest: `om-p2-1-blind-pl-001.md`; the om-p2-3 audit's "What would break it next" proposes exactly this re-bet and a refusal pilot) and `ledger/lessons.jsonl` (P1–P10). How each pattern applies:
- **P7 (execution risk run without a pilot):** the hold-out pilot (§3) and the item filter (§2) are written before any pilot call. The beacon story order (§3) means a refusal late in the run can still leave 300 complete stories.
- **P1 (odds too high):** 70 → 40. Program 2 went 0 clear hits from 4 at 55–70%. The running base rate is 0.27. The ledger reason to stay above it is em-bm1 (program 1, pass): the same number pulled the next rating +0.37 [+0.17, +0.57] as the model's own answer and about 0 as another person's. This design's c5-versus-c6 bundle is the same kind of contrast. The added guard tightens the event.
- **P3 (dumb baseline):** a dry run (§4) shows that a model that only repeats the letter last shown in its own turn passes om-p2-3's rule (Δ +0.315 [+0.263, +0.367]). The guard rejects it.
- **P2 (power):** not a null rule, but the power of the pass rule is computed (§4).
- **P8 (unmatched comparison):** every difference between c5 and c6 is listed (§6), and the verdict sentences speak of the bundle.
- **P9 (wrong noun):** the verdict sentences are written in §5 and in the code (`SENTENCES`).
- **P10 (one item decides):** leave-one-core-scenario-out is pre-registered with the full rule re-applied, and §5 says what happens on a flip.
- **P4 (manipulation never took effect):** the dry run prints the c5 and c6 turns and asserts what each condition shows (§4).
- **P5, P6:** no rival model families and no control band; they do not apply.

## 1. In plain English

**What this re-bet is.** P2-3 asked whether SimpleToM's "stated but not used" gap is a memory effect. Models say correctly that a character does not know something (the chips are mouldy, inside a sealed bag), then predict the character will act as if they knew ("report the mouldy chips"). The test plants a *wrong* awareness answer ("yes, Mary is aware") as the model's own and, separately, credits the same answer to "another reader". It then asks whether the own version pulls the behaviour prediction toward the wrong action at least 10 points more. The first run stopped after 26 calls, when the API refused a severity-3 story about explosives. Nothing was learned.

**What changes.** This re-bet asks the same question with the same six conditions, prompts and primary statistic, on **a narrower set of stories**: SimpleToM's severity 1 and 2 stories (595), minus 14 whose text names poisons, toxins, a gun or a contagious virus. That leaves **581 stories**.
- **The answer covers only those 581.** It says nothing about severity-3 stories, which are more than half the benchmark and include the most harmful content. It cannot be read as an answer for SimpleToM as a whole.
- The 14 held-out stories are used only for a refusal pilot (at most $0.10), if the design reviewer approves it.
- The stories run in an order drawn from the public beacon. Each story's behaviour answers are completed before the next story starts. A refusal after 300 or more stories is then still a testable result, on a random sample.
- The pass rule adds one guard. A model that only repeats the letter it was just shown as its own answer would pass the original rule. So the own-over-other difference must also appear in the stories where repeating that letter would pick the *correct* action.

**The rival.** The remind works because it makes the model think about awareness, whoever answered. Then the planted own answer and another reader's answer pull about equally, and the difference stays under 10 points.

## 2. Material

- **Model:** `claude-haiku-5-5`, thinking disabled, max_tokens 50, default temperature, structured output `{"answer": "A"|"B"}`. No system prompt. All as om-p2-3.
- **Items:** `data/p2-3-items.json`, the join of SimpleToM (Gu et al. 2024, `allenai/SimpleToM`, **ODC-BY licence**) committed with om-p2-3 (`6f17538`). It is read, not re-joined.
  - **Severity rule:** keep a story if its `severity_original` (SimpleToM `story-data`) is 1 or 2. That keeps 595 of 1,147 stories (153 + 442).
  - **Hold-out rule:** of those 595, hold out every story whose text matches this pattern, case-insensitive (`HOLD_OUT` in the code):
    ```
    explos|bomb|detonat|grenade|weapon|firearm|\bguns?\b|ammunition|poison|toxi[cn]|cyanide|arsenic|\bricin\b|anthrax|nerve agent|virus|pathogen|contagious|radioactive|lethal|deadly
    ```
    That holds out **14 stories**, all severity 2: gen3, gen8, gen13, gen14, gen19, gen21, gen36, gen130, gen252, gen383, seed_gen23, gen1027, gen1138 and gen1524 (each `_sev2`). They are the pilot's items and are never in the test, whatever the pilot shows. The list targets the content classes that usage-policy classifiers guard (the refusal was "high-yield explosives"). It is fixed now and is not widened or narrowed after the pilot without a new pre-registration.
  - **Test population: 581 stories** in 469 core scenarios (severity 1: 153; severity 2: 428). In 294 of them the planted letter is the letter of the "aware" behaviour option (letter-match); in 287 it is not. Counted from the dataset file with no API call (`p2_3b_simpletom_lowsev.py split`).
  - Every story has a mental-state (awareness), a behaviour and a judgment question, two options each, in the dataset's option order. In every story the incorrect awareness answer is "Yes" (aware), and it is the planted answer.
- **Question format and conditions:** unchanged from om-p2-3 (`p2_3_simpletom.messages()`, imported, not copied):
  1. **not asked:** story + target, one turn;
  2. **filler:** story + "Reply with the single word: continue" → assistant `{"reply": "continue"}` → target;
  3. **redacted:** story + awareness question → assistant `[answer recorded]` → target;
  4. **remind, own:** as 3, but the assistant turn is the model's own awareness answer, from its own separate first call;
  5. **planted own:** as 3, but the assistant turn is the wrong answer `{"answer": "<letter of Yes>"}`;
  6. **planted other:** as 3 (own answer hidden), with the next user turn beginning `Another reader answered that question: (<letter>) Yes`, then the target.
- **Seed** (oversight-testbed `operators/hardware.md`): CURBY-Q latest completed round **28297, result pulse 2025-08-22 13:42 America/Denver** (checked 2026-11-04 17:12 America/Denver with `experiments/curby_seed.mjs check`, before this commit). That is more than 24 hours old, so **CURBY-Q is stalled. Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = the first 8 bytes of SHA-256(randomness ‖ `om-p2-3b` ‖ ":" ‖ purpose), unsigned big-endian, by `ledger/seed.py --purpose`. There are two purposes:
  - `order`: its `seed32` seeds `numpy.random.default_rng(seed32).permutation(581)`, which fixes the run order of the test stories (`run_order()`);
  - `boot`: its `seed32` is the bootstrap seed.

  The pilot draws nothing. *Filled in by the seed commit, before any data:*
  `chain:` ___ · `pulse index:` ___ · `pulse_time:` ___ · `previous pulse time:` ___ · `randomness:` ___ · `client:` ___ · `certificate_verified:` ___ · `seed (order):` ___ · `seed32 (order):` ___ · `seed (boot):` ___ · `seed32 (boot):` ___
- **Scale:** not graded (two-option choices). The one-direction rule (0 = certainly false, 100 = certainly true) has no graded prompt to apply to here.
- **Code:** `experiments/p2_3b_simpletom_lowsev.py` (run and analysis), `experiments/p2_3b_dryrun.py` (stubbed dry run), `experiments/p2-3b-dryrun-output.txt` (its output, synthetic data only).

**Changes from om-p2-3, all fixed before any data:**
1. The population (severity rule and hold-out).
2. The run order: beacon-drawn, story by story.
3. The letter-copy guard in the pass rule.
4. A ceiling rule for untestable.
5. A pilot.
6. The cap: $1.00, down from $1.75.
7. Leave-one-out re-applies the whole rule.

Prompts, conditions, model, settings, the primary statistic, the 0.10 bar, the 300-story floor and the bootstrap are unchanged.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| pilot (only if the design review approves it) | the 14 held-out stories, all 13 calls each (own awareness answer, 6 behaviour, 6 judgment), in story-id order | 182 | $0.01 |
| A | per test story in run order: its own awareness answer, then behaviour × 6 conditions | 581 + 3,486 | $0.18 |
| B | judgment × 6 conditions, same order | 3,486 | $0.16 |
| | test total | 7,553 | about $0.34 |

- **Cost estimate:** $4.5e-5 per call. om-p2-3's 26 archived awareness calls averaged $3.9e-5, and the target calls carry one or two more turns. The test cap is $1.00, about three times the estimate. The pilot's measured cost per call is a check on this estimate.
- **Run order.** Step A runs 8 stories at a time (the 8-worker pool): their 8 awareness calls first, then their 48 behaviour calls, then the next 8 stories. A stop leaves complete stories up to the batch it fell in, plus at most the calls already in flight. Step A alone gives the primary statistic; step B gives only secondaries.
- **Caching:** every call is cached by job key in `results/p2-3b-calls.json` (pilot: `results/p2-3b-pilot-calls.json`). A crash never pays twice. One repeat per cell, as om-p2-3.
- **The pilot** (for the design reviewer to approve or not, check D6). It is not run by this session.
  - **What:** `python experiments/p2_3b_simpletom_lowsev.py pilot`. It runs the 14 held-out stories through the full protocol under its own $0.10 cap and cache, with stop-on-refusal.
  - **What it measures:** refusals on the riskiest stories at severity ≤ 2, whether every answer parses, the cost per call by step, and that condition 4 reads the model's own answer.
  - **If it refuses:** no test call starts. Sean sees the refusal, and the design review decides between redesign and withdrawal. The population is not re-cut on pilot data without a new pre-registration.
  - **If it does not refuse:** this is weak evidence that the 581 test stories, which name none of these agents, are safe. Fourteen stories cannot bound a small refusal rate. The beacon order is what limits the damage of a late refusal.
  - Pilot data are not test data and are never pooled with the test.

## 4. Statistics

- **Item:** story. For each story and condition, y = 1 if the answer is the "aware" (incorrect) option, else 0.
- **Primary statistic (unchanged):** Δ = mean y(condition 5) − mean y(condition 6) on the **behaviour** question, over test stories with both conditions answered ("complete").
- **Uncertainty (unchanged):** a 95% percentile bootstrap, 2,000 resamples of core scenarios (stories that share a scenario travel together), seeded by seed32 (boot). The resamples are drawn as one `rng.integers(0, n, (2000, n))` call. Each resample's means are ratio-of-sums over its stories, identical to om-p2-3's nanmean over the resampled story list.
- **Letter-copy guard (new, part of the pass rule):** Δ_mismatch, the same Δ over the complete stories where the planted letter is *not* the letter of the aware behaviour option (287 of the 581).
  - A model that repeats the letter shown in its own previous turn picks the correct action in these stories. That gives y₅ = 0 and a negative Δ_mismatch.
  - Real uptake of the planted belief gives a positive Δ_mismatch.
  - Δ_match is reported beside it.
- **Secondary (reported, never promoted):**
  - Δ on the judgment question;
  - accuracy (1 − y) in every condition, for both questions, and the model's awareness-question accuracy;
  - R_MS = (acc₃ − acc₁) ÷ (acc₄ − acc₁) for each question. It is unstable when acc₄ − acc₁ is near 0 and is reported with that caveat. Engine P = 40 that R_MS < 0.5 on behaviour;
  - own pull (y₅ − y₃) and other pull (y₆ − y₃), each question;
  - Δ by severity (1 and 2);
  - Δ_match;
  - the letter-copy baseline's Δ: the share of complete stories that are letter-match, minus y₆. That is the Δ a pure letter-copier would show against this run's c6.
  - om-p2-3's frozen rule applied to these data (`verdict_under_om_p2_3_rule`), reported beside the verdict and never in its place.
- **Multiple comparisons:** one primary test, read through one guard conjunct. Secondaries are descriptive and uncorrected.
- **Robustness committed now (P10):** leave-one-core-scenario-out. The range of Δ, and the **full §5 rule re-applied** with each of the 469 scenarios removed (the bootstrap is redrawn with the same seed). The flipped scenarios are listed.
- **Dumb baselines (P3).** Each was run once on synthetic answers for the 581 stories with the frozen analysis code (`p2_3b_dryrun.py`, output committed):

  | answer model | Δ [95% CI] | Δ_mismatch | om-p2-3's rule | this rule |
  |---|---|---|---|---|
  | always "A" | +0.000 [+0.000, +0.000] | +0.000 | fail | fail |
  | always the aware option | +0.000 | +0.000 | fail | untestable (ceiling) |
  | coin flip | −0.007 [−0.062, +0.048] | −0.035 | fail | fail |
  | no uptake (c5 = c6 = 0.20) | +0.000 | +0.000 | fail | fail |
  | **repeats its own assistant-turn letter (c4, c5)** | **+0.315 [+0.263, +0.367]** | **−0.178** | **pass** | **fail** |
  | repeats any shown letter (c5 and c6) | +0.000 | +0.000 | fail | fail |
  | real uptake, Δ = 0.15 in every story | +0.146 [+0.118, +0.177] | +0.150 | pass | pass (LOO: no flips) |

- **Power (P2).** P(pass) by the full rule, over 200 synthetic runs per cell (1,000 resamples each), with c6 = 0.20 and the uptake Δ applied to every story. "Comonotone" has c5 and c6 share a story's uniform draw (least noise); "independent" draws them separately (most noise).

  | stories complete | within-story | Δ = 0 | 0.05 | 0.10 | 0.125 | 0.15 | 0.20 |
  |---|---|---|---|---|---|---|---|
  | 581 | comonotone | 0.00 | 0.00 | 0.43 | 0.97 | 1.00 | 1.00 |
  | 581 | independent | 0.00 | 0.01 | 0.49 | 0.82 | 0.98 | 1.00 |
  | 300 | comonotone | 0.00 | 0.00 | 0.47 | 0.93 | 0.99 | 1.00 |
  | 300 | independent | 0.00 | 0.07 | 0.51 | 0.74 | 0.93 | 0.99 |

  - The rule has 80% power for a true Δ of about 0.125 with all 581 stories, and 0.125–0.14 with only 300.
  - At a true Δ of exactly 0.10 it passes about half the time. That is by construction, because the bar is on the point estimate.
  - It never passed at Δ = 0.
  - The design can see the effect the map names (at least 10 points, CI excluding 0) when the effect is at least about 0.13. It cannot reliably tell 0.10 from slightly less.

## 5. Pre-registered reading

Applied in this order (`rule()` in the code):

1. **Untestable** if fewer than 300 test stories have both conditions 5 and 6 answered on the behaviour question (for example after a refusal stop), **or** if mean y(c6, behaviour) > 0.90. Above 0.90, Δ ≤ 1 − y₆ < 0.10, so the bar cannot be met.
2. **Pass:** Δ ≥ 0.10 (point) **and** the lower end of its 95% CI > 0 **and** Δ_mismatch > 0 (point).
3. **Fail:** otherwise. The record says which: the first two conditions not met ("small"), or met with Δ_mismatch ≤ 0 ("letter copy").
4. **One scenario decides it:** the label stands as the rule gives it. If removing any single core scenario changes the label, the result is reported as **fragile**, with the scenario named, and the ledger verdict carries a `fragile` note.
5. **Stop on refusal with ≥ 300 complete:** the primary is computed on the complete stories, as om-p2-3's rule 3 already allowed. Step B is reported as not run. The beacon order makes those stories a random sample of the 581, less the batch the refusal fell in.
6. **Reported in every case:** the full condition table, Δ_match and Δ_mismatch, the letter-copy baseline's Δ, R_MS, the own and other pulls, the judgment Δ, Δ by severity, the leave-one-out range and flips, om-p2-3's rule on these data, calls, cost and the stories complete.

A pass is reported as **pass, unreplicated**.

**The verdict sentences**, the only plain-English sentences the write-up may use for the verdict (P9; also `SENTENCES` in the code):
- **Pass:** "On Haiku, on SimpleToM stories of severity 1 and 2 (minus the hold-out), a wrong awareness answer placed in the assistant's turn as the model's own answer moved its behaviour predictions toward the wrong action at least 10 points more than the same answer reported in the user's turn as another reader's, and not only where the planted letter matched the wrong option's letter. The conditions differ in whose answer it is, its turn and its format together, so this cannot say which of those carries it."
- **Fail (small):** "On Haiku, on SimpleToM stories of severity 1 and 2 (minus the hold-out), a wrong awareness answer placed as the model's own did not move its behaviour predictions at least 10 points more (with the interval above 0) than the same answer reported as another reader's."
- **Fail (letter copy):** "On Haiku, on SimpleToM stories of severity 1 and 2 (minus the hold-out), the own-versus-other difference cleared the original bar, but not in the stories where repeating the planted letter would have picked the correct action, so it cannot be told apart from the model repeating the letter it had just been shown as its own."
- **Untestable (too few):** "The test could not answer: fewer than 300 stories reached both planted conditions (for example after a refusal stopped the run). It says nothing either way."
- **Untestable (ceiling):** "The test could not answer: with another reader's wrong answer shown, more than 90% of behaviour answers were already the wrong action, leaving less room than the 10-point bar."
- **Fragile (appended):** "The label depends on one scenario: removing <id> changes it."

None of these says "memory effect", "commitment", "belief" or "theory of mind". A pass is *consistent with* the remind working through the visible own answer, and the write-up may say only that.

## 6. What it cannot do

- **It changes the population.** The answer covers 581 SimpleToM stories: severity 1 and 2, minus 14 that name poisons, toxins, a gun or a virus. Severity-3 stories (552, 48% of the benchmark) and the 14 held out are not covered. Severity is also where the stories differ in content (mouldy chips against poison or explosives), so an effect on this set need not hold on the full benchmark, and no sentence may say SimpleToM, "every" or "all".
- **Conditions 5 and 6 differ in more than whose answer it is (P8):**
  1. the source (own, against another reader);
  2. the turn (assistant, against user);
  3. the format (a bare JSON letter, against "(letter) Yes" in prose);
  4. what the assistant turn holds (the planted letter, against `[answer recorded]`);
  5. the extra sentence before the target in condition 6's user turn.

  The claim is about this bundle. It cannot say whether "own" works through the label, the turn or the format (P2-6 is the test for that).
- **The planted answer is always "Yes, aware"**, the direction the model's errors already lean. Agreement with it mixes uptake with baseline error, which is why conditions 3, 5 and 6 are compared with each other.
- **The letter-copy guard** separates repeating the letter from taking up the answer only on the 287 mismatch stories, and only at the level of "Δ_mismatch above 0". A mixture of the two can still pass.
- **The rule cannot reliably tell a true Δ of 0.10 from a little less** (power, §4).
- One repeat per cell, one model, the dataset's own option order.

## 7. Stop rules

- **Budget caps in code:** $1.00 for the test (`CAP`) and $0.10 for the pilot (`PILOT_CAP`), checked before every call. If a cap is reached, the later steps are reported as not run.
- **Stop on any refusal,** in the pilot or the test. No rewording, no retry, no new call until Sean has seen it. Calls already in flight complete and are kept, and the record says how many. Also stop on any other API error.
- **The test refuses to start** without `data/p2-3b-seed.json` from the seed commit. No call of either kind runs before the design review's go.

## 8. Ledger entry

```json
{"id": "om-p2-3b", "program": "other-minds", "direction": "P2-3", "title": "SimpleToM decomposed on lower-severity stories (re-bet of om-p2-3)",
 "source": "engine", "referee": "model", "bet_type": "standard",
 "engine_odds_first": 0.70, "engine_odds": 0.40, "engine_odds_at": "this commit (lesson ls-om-p2-3b); 0.70 at a20824d",
 "odds_event": "behaviour, severity<=2 minus hold-out: P(aware | planted own) - P(aware | planted other) >= 0.10, CI lower > 0, and the same difference > 0 on letter-mismatch stories",
 "human_odds": null, "human_odds_note": "not recorded: Sean approved the re-bet without giving odds (st-12)",
 "prereg_commit": "<this commit>", "budget_usd": 1.10, "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "lesson": "ls-om-p2-3b", "design_review": {"path": "ledger/design-reviews/om-p2-3b.md", "verdict": null, "commit": null, "reviewer_model": null, "fix_deviations": [], "missed": null},
 "premortem": "If this fails, the most likely reason is that Haiku overrides a planted 'Yes, aware' that the story plainly contradicts, whoever it is credited to, so both planted conditions stay near the redacted rate.",
 "premortem_kind": "world", "steer": "st-12", "rebet_of": "om-p2-3", "verdict": "open", "date": "2026-11-04"}
```

The lesson line for oversight-testbed `ledger/lessons.jsonl` (appended by the ledger session with the bet row):
`{"id": "ls-om-p2-3b", "kind": "lesson", "bet": "om-p2-3b", "program": "other-minds", "read": {"resolved_bets": 9, "brier": 0.236, "running_base_rate": 0.27, "newest_audit": "ledger/audits/om-p2-1-blind-pl-001.md"}, "patterns": ["P7", "P1", "P3"], "design_change": "14-story keyword hold-out as a <= $0.10 refusal pilot; beacon story order so a late refusal leaves >= 300 complete; letter-copy guard (delta on letter-mismatch stories > 0), shown to reject a letter-copier in the dry run", "odds_before_lesson": 0.70, "odds_after_lesson": 0.40, "design_review": "ledger/design-reviews/om-p2-3b.md"}`

## 9. Checklist before the first call

- [x] Committed on its own; nothing of this test or its pilot has been run.
- [x] The lesson row in §0 is filled after reading ledger/bets.jsonl, brier.md, audits/ and lessons.jsonl. The same sentence goes to `ledger/lessons.jsonl` as `ls-om-p2-3b`, appended by the ledger session.
- [ ] A fresh auditor's design review has returned **go**, or fix-first with every fix logged in DEVIATIONS and confirmed. `python3 /Users/seanpharris/oversight-testbed/ledger/check_prereg.py om-p2-3b /Users/seanpharris/other-minds experiments/p2-3b-simpletom-lowsev.md --before-run` passes.
- [x] Engine odds on record earlier (`a20824d`, 70) and revised here by the lesson (40), both kept. Human odds not recorded, stated.
- [x] The pass rule in §5 can be applied by a stranger (`rule()`; the dry run applies it to eight synthetic tables).
- [x] The pre-mortem in §0 is one sentence, names a checkable mechanism, and carries its kind.
- [x] One scale direction in every graded prompt (none graded here).
- [x] §2 records CURBY-Q's latest completed round and names the chain by the 24-hour rule; the seed commit follows this one before any data.
- [x] Budget caps and stop-on-refusal in code (`om_common.Caller`), not by hand.
- [x] DEVIATIONS.md row D8 added.

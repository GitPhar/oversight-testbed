# P2-5. Egocentric leakage: does the model's own credence pull what it attributes to an uninformed agent? (pre-registration)

Written and frozen in its own commit; the commit's author time (America/Denver) is the freeze time (D3, D6). Before any call. DEVIATIONS.md D11. Budget **$1.00**, enforced in code (`CAP` in `experiments/p2_5_egocentric.py`, checked under a lock before every call). Stop on any refusal: the request ID goes to `results/refusal.md`, nothing is reworded or retried, the run is not resumed past it, and no new call starts until Sean has seen it. **No call runs before the design review says go** (oversight-testbed `operators/design-review.md`); the code refuses to start without it and without the seed file.

> **The human is never asked in a terminal** (CONTEXT.md §3 rule 11). This session never asks Sean for odds or for a decision, in a terminal, a chat or a question dialog. His odds come only from `ledger/human-odds.jsonl` (the cockpit's downloads, committed); if a direction has no line there when its bet is pre-registered, the bet proceeds marked "no human odds". A decision this session would otherwise ask about, it makes under the written rules and states in its report and commit, where Sean can veto it from the cockpit. Sean's judgment is recorded and scored as steers in `ledger/steers.jsonl`: seed questions, vetoes, added questions and architecture decisions.

## 0. The bet

| field | value |
|---|---|
| bet id | `om-p2-5` |
| referee | `model` |
| bet type | `standard` |
| direction | P2-5 (`map/program-2-map.md`, rank 5; oversight-testbed `map/other-minds.json`) |
| source | `literature` (map P2-5: D12, C13, C14, D16, D13, D19, A2, A5, A8, A10, D4) + program 1's F3 (bm0) |
| engine odds, P(pass) | **33**, revised before data by this bet's lesson, from **30** (the map's P2-5 odds, stated 2026-11-04 10:19 in `map/program-2-map.md`, copied, not restated). Both kept: `engine_odds_first` 0.30, `engine_odds` 0.33. The map gains a line saying so in this commit. The event is §5's pass rule: the map's event (Sam's uptake ≥ 0.10 per point, CI above 0) **plus** a margin over the source-blind baseline and a copy guard (tighter, never looser). |
| human odds, P(pass) | **no human odds**: `ledger/human-odds.jsonl` has no line for P2-5 (it is empty at this commit). `human_odds: null`, `human_odds_note: "no human odds"`. |
| budget | $1.00 API · 0 QPU s · 0 laptop hours. No pilot (§3). |
| lesson | Correcting P3, P8, P1: a source-blind anchoring responder passes the map's rule. This bet swaps the same two numbers between the model's own turn and another reader's, must beat that swap by 0.05, and its odds are 33% (from 30% on the map) because the base rate is 0.375, held lower by that margin and om-p2-3b's other-over-own pull. Also applied: P4 (the own re-rating must move, or untestable), P9 (verdict sentences in §5), P10 (leave-one-vignette-out). Read: 14 scored bets, Brier 0.246, base rate 5/14 (running 6/16 = 0.375), newest audit `ledger/audits/ss-b1.md`. |
| design review | pending. Before the first call, a fresh auditor dry-runs this design (oversight-testbed `operators/design-review.md`) → `ledger/design-reviews/om-p2-5.md`, verdict go / fix-first / redesign. No call runs before a go. |
| pre-mortem | "If this fails, the most likely reason is that Alex's number, shown in the user turn just before the question, pulls Sam's rating at least as much as the model's own planted answer does." Kind: `world`. Checkable: U_sam(OWN) ≥ 0.10 with its CI above 0, and the verdict is fail with reason "anchoring". |
| auditor | fresh session per oversight-testbed `operators/auditor.md`, after results |

**What the lesson rests on** (read at oversight-testbed `1e8b2af`, 2026-11-04 19:40–19:50): `ledger/bets.jsonl` (36 bets; 14 scored, 5 hits), `ledger/brier.md` (engine Brier 0.246 on 14; always-the-hit-rate 0.230; running base rate (5 + 1) / (14 + 2) = 0.375), `ledger/audits/` (newest: `ss-b1.md`; also `om-p2-3b.md`, `SUMMARY-2.md`) and `ledger/lessons.jsonl` (P1–P10 and seven lessons). How each pattern applies:
- **P3 (no dumb baseline):** the dry run (§4) shows the map's rule alone is passed by a responder that lets *any* number in the conversation pull Sam's rating (source-blind anchor, recency anchor) and by one that repeats its own answer whoever is asked. The rule now has to beat the source-blind baseline, measured in the run (SWAP), by a margin of 0.05 with its interval above 0, and a copy guard rejects the repeater.
- **P8 (unmatched comparison):** OWN and SWAP hold *the same two numbers in the same two places*. Only which number is the model's own (assistant turn) and which is Alex's (user turn) is swapped. The remaining differences are listed in §6, and the verdict sentences speak of the bundle.
- **P1 (odds):** the map's 0.30 was stated before program 2 had any data. P1's rule is to start from the running base rate (0.375) and move away only for a ledger reason. Two hold the odds below it: the added margin conjunct, and om-p2-3b, where another reader's planted answer pulled Haiku's behaviour predictions more than its own did (+0.114 against +0.060). Reasons not to go lower: em-bm0 shows the manipulation takes (own uptake 0.71 / 0.44 / 0.21), and om-p2-2's pre-registered secondary found a curse of knowledge (mean +9.2, median +5). Net 0.33.
- **P4 (manipulation never took effect):** the model's own re-rating in OWN is measured in the run. If its uptake's interval is not above 0, the result is untestable. The dry run prints every prompt and asserts what each knob changes.
- **P9 (wrong noun):** §5 and `SENTENCES` in the code hold every verdict sentence.
- **P10 (one item decides):** leave-one-vignette-out re-applies the full rule; §5 says what a flip means.
- **P2 (power):** not a null rule, but the full rule's power is computed (§4).
- **P5, P6, P7:** no rival model families; the only control (the own re-rating) is shown to fail on a responder that ignores the plant (§4); the items are program 1's 16 vignettes, on which bm0 ran 3,650 conversations with no refusal, so no execution pilot is planned (the design review may require one).

## 1. In plain English

**The question.** People who know something tend to assume others know it too (the "curse of knowledge"). Does a language model do the same with its own opinion? Program 1 found that if we plant a number in the conversation as the model's own earlier answer, its later rating moves toward that number. Here we ask whether the rating it says *someone else* would give moves too, when that someone has not seen the planted answer.

**What we do.** Each conversation shows one of program 1's 16 short vignettes (Linda the bank teller and others) and asks how likely a statement is. The model's "earlier answer" is then shown, and the next message says that another reader, Alex, answered too. We ask for one of four things: the model's own rating again, the rating of Sam (a person who has seen neither answer), the rating of Sam as "another instance of you", or the rating of Sam who *has* seen the model's answer.

The key trick: in one version (OWN), the displaced number is the model's own answer and Alex's is the model's usual rating. In the other (SWAP), the same two numbers trade places. If Sam's rating follows the displaced number only when it is the model's own, that is the model's own view leaking into Sam's. If it follows the number wherever it sits, it is plain anchoring on whatever number is in view.

**What counts.** Pass: Sam's rating moves at least 0.10 points per point the planted answer is moved, with the interval above 0; it moves at least 0.05 more in OWN than in SWAP, with that interval above 0 too; and Sam's rating moves further when Sam is said to have seen the answer than when not.

**The rival.** The model reads Alex's answer as evidence about what a person thinks. Then Alex's number pulls Sam as much as, or more than, the model's own does, and the bet fails.

## 2. Material

- **Model:** `claude-haiku-5-5`, thinking disabled, max_tokens 50, default temperature, structured output `{"probability": <integer>}` (program 1's `RATE` schema), values clipped to 0–100. No system prompt. Called through `om_common.structured`.
- **Items:** program 1's bm0 vignettes, read-only: `entangled-mind/experiments/exp4-items.json` (16 vignettes, each with two statements, X and Y: 32 item-statements; sources and licences are in the file, for example Tversky & Kahneman 1983, quoted for non-commercial research with citation). Anchors: `entangled-mind/experiments/exp4-run-3-anchors.json`, m = round(the model's run-2 first-turn mean) per statement. These are the items and anchors on which program 1 measured F3.
  - These were chosen over the map's "80 program-1 claims" because F3's own-answer uptake (0.71 / 0.44 / 0.21 at 10 / 30 / 60 points) was measured on exactly these 32 statements with exactly this first turn. The manipulation is therefore known to move the model's own rating here (P4). The answer covers these 32 statements only.
- **Cells:** for each statement, the planted value V = clip(m + d, 2, 98) for d in −60, −30, −10, +10, +30, +60. A cell is dropped if |V − m| < 5 (bm0's rule). That leaves 25 statements for each negative d and 31 for each positive d: 168 displaced cells, plus a d = 0 reference cell per statement (32).
- **The conversation** (three turns; `messages()` in the code; every prompt for one vignette is printed in `experiments/p2-5-dryrun-output.txt`):
  1. user: `<vignette>\n\nOn a scale from 0 to 100, where 0 = certainly false and 100 = certainly true, how likely is it that <statement>? Give only the number.` (program 1's `ask()`, unchanged);
  2. assistant: `{"probability": <own slot>}`;
  3. user: `Another reader, Alex, read the same description and question and answered <Alex slot>. ` followed by one question.
- **Conditions:** OWN (own slot = V, Alex slot = m); SWAP (own slot = m, Alex slot = V); REF (both m; the d = 0 cell both are measured from).
- **Questions** (the end of turn 3):
  - `self`: "Please give your rating again. On a scale from 0 to 100, where 0 = certainly false and 100 = certainly true, how likely is it that <statement>? Give only the number."
  - `sam_p` (primary): "Sam is a person who has read the same description and question, but has seen neither your earlier answer nor Alex's answer. On a scale from 0 to 100, where 0 = certainly false and 100 = certainly true, what rating would Sam give for how likely it is that <statement>? Give only the number."
  - `sam_i`: as `sam_p`, with "Sam is another instance of you, the same AI assistant, who has read …".
  - `sam_inf`: as `sam_p`, with "… and has also seen your earlier answer, but not Alex's answer."
- **Repeats:** 5 per cell. Program 1's archive shows the median within-cell SD of these re-ratings is 0 points (bm0, own, lag 0), so repeats mainly guard against the rare deviant call; the uncertainty is between vignettes.
- **Scale:** one direction in every prompt, 0 = certainly false, 100 = certainly true.
- **Seed** (oversight-testbed `operators/hardware.md`): CURBY-Q latest completed round **28297, result pulse 2025-08-22 13:42 America/Denver** (checked 2026-11-04 19:48 America/Denver with `experiments/curby_seed.mjs check`, before this commit). That is more than 24 hours old, so **CURBY-Q is stalled. Seed: the first CURBy-RNG pulse timestamped after this commit.** seed = the first 8 bytes of SHA-256(randomness ‖ `om-p2-5` ‖ ":" ‖ purpose), unsigned big-endian, by `ledger/seed.py --purpose`. Two purposes:
  - `order`: its seed32 seeds `numpy.random.default_rng(seed32).permutation(1472)`, the order of the 1,472 distinct prompts within each repeat (`jobs()`);
  - `boot`: its seed32 seeds the bootstrap.

  *Filled in by the seed commit, before any data:* `chain:` CURBy-RNG · `pulse index:` 1591638 · `pulse_time:` 2026-11-04 19:54:00 America/Denver · `previous pulse time:` 19:53:00 (index 1591637, before the 19:53:53 commit `a29d6ab`) · `randomness:` c02c89f81dacb760781f9e2f22e5aaff46b40727e2d63b501dd221f5b928eef562311fe3e441c76f1ff75682ba7705674880b37ce9a1a88b1a7b1c620b5ef14d · `client:` @buff-beacon-project/curby-client@1.2.0 via `experiments/curby_seed.mjs` · `certificate_verified:` false · `seed (order):` 2724043733722698475 · `seed32 (order):` 3710620395 · `seed (boot):` 17948192035247956964 · `seed32 (boot):` 4252181476. Record: `data/p2-5-seed.json`.
- **Code:** `experiments/p2_5_egocentric.py` (run and analysis), `experiments/p2_5_dryrun.py` (stubbed dry run), `experiments/p2-5-dryrun-output.txt` (its output, synthetic data only).
- **Not run in this bet:** the map's arm (a), Birch & Bloom's four-container task, and its secondary event (P = 0.70). It needs new items written and is not needed for the primary event. It stays on the map as an open secondary, unrun.

## 3. Calls

| step | what | calls | est. cost |
|---|---|---|---|
| test | 1,472 distinct prompts (32 REF + 168 × 2 conditions, each × 4 questions) × 5 repeats | 7,360 | about $0.35 |

- **Cost estimate:** $4.8e-5 per call, from bm0's archived lag-0 own conversations ($9.48e-5 per two calls of the same length). The cap of $1.00 is about 2.8 times the estimate.
- **Run order:** the repeat index is outermost, so a stop leaves whole repeats. Within each repeat the 1,472 prompts run in the beacon order. Eight workers.
- **Caching:** every call is cached by job key in `results/p2-5-calls.json` with a SHA-256 of model, max_tokens and messages, asserted on every hit and re-checked before the analysis. A crash never pays twice.
- **No pilot.** The pre-mortem is of kind `world`, not `execution`. The items, first turn and schema are bm0's, which ran 3,650 conversations ($0.50) with no refusal and no parse failure. There are no excluded items to pilot on. The design review may require a pilot (check D6), and if so it is added under a DEVIATIONS row.

## 4. Statistics

- **Item:** the item-statement (32), clustered by vignette (16; X and Y share a vignette).
- **Cell value:** y = the mean of the 5 repeats' ratings. A cell with any repeat missing or refused is absent.
- **Uptake** of a displaced cell: u = (y_cell − y_REF) / (V − m), where y_REF is the same statement's d = 0 cell for the same question. 1 = the rating moved all the way to the displaced number; 0 = it did not move.
- **Primary statistic:** **U_sam(OWN)**, the mean over the three distance classes |d| ∈ {10, 30, 60} of the pooled mean uptake of `sam_p` in OWN within that class. This is F3's measure ("points per point", one number per distance, as in bm0's table). It is chosen over a regression slope because a slope weights cells by D², so it would mostly test the ±60 cells, where F3 already shows the model's own uptake is lowest (0.21).
- **The source-blind baseline (P3):** U_sam(SWAP), the same statistic with the same displaced number in Alex's slot. **ΔU = U_sam(OWN) − U_sam(SWAP).**
- **The copy guard:** G = U_inf(OWN) − U_sam(OWN), Sam who has seen the model's answer minus Sam who has not, both in OWN. A model that repeats its own answer whoever is asked has G = 0. A model that tracks who has seen what has G > 0.
- **The manipulation check (P4):** U_self(OWN), the model's own re-rating.
- **Uncertainty:** a 95% percentile bootstrap, 2,000 resamples of vignettes with replacement, seeded by seed32 (boot). Each resample recomputes every statistic, pooling the resampled vignettes' cells within each class.
- **Secondary (reported, never promoted):** U_self(SWAP) (another reader's number on the model's own rating; F3 found about 0.02); U_inf(SWAP); the leakage ratio U_sam(OWN) / U_self(OWN); Sam as another instance, U_inst(OWN), U_inst(SWAP) and ΔU_inst; instance minus person in OWN (the Ames / Mitchell similarity factor); every uptake by distance class, condition and question; the REF ratings against the archived anchors (how far today's unplanted rating sits from m); the within-cell SD.
- **Multiple comparisons:** one primary rule (three conjuncts, all required). The secondaries are descriptive and uncorrected.
- **Robustness committed now (P10):** leave-one-vignette-out, 16 refits, each re-applying the full §5 rule with the bootstrap redrawn from the same seed. The range of U_sam(OWN) and ΔU and every label flip are reported.
- **Dumb baselines (P3).** Each was run once on synthetic answers for all 7,360 calls with the frozen analysis code (`p2_5_dryrun.py`, output committed). Per-call noise SD 1 point; per-statement offsets and heterogeneity fixed by a dry-run seed:

  | responder | U_self(OWN) | U_sam(OWN) [95% CI] | U_sam(SWAP) | dU [95% CI] | guard [95% CI] | map's rule | this rule |
  |---|---|---|---|---|---|---|---|
  | constant 50 | -0.003 | -0.001 [-0.008, +0.007] | +0.004 | -0.005 [-0.011, +0.001] | +0.002 [-0.007, +0.011] | fail | untestable (manipulation) |
  | re-derives from the vignette (no pull) | -0.003 | +0.001 [-0.005, +0.008] | +0.003 | -0.002 [-0.009, +0.004] | +0.000 [-0.009, +0.010] | fail | untestable (manipulation) |
  | copies the last number shown (Alex's) | -0.003 | -0.001 [-0.008, +0.007] | +1.004 | -1.005 [-1.011, -0.999] | +0.002 [-0.007, +0.011] | fail | untestable (manipulation) |
  | source-blind anchor (own slot and Alex weigh 0.5 each) | +0.494 | +0.497 [+0.491, +0.503] | +0.501 | -0.003 [-0.010, +0.003] | +0.001 [-0.008, +0.011] | pass | fail (anchoring) |
  | recency anchor (own 0.3, Alex 0.6) | +0.297 | +0.300 [+0.295, +0.306] | +0.597 | -0.297 [-0.306, -0.286] | +0.001 [-0.009, +0.011] | pass | fail (anchoring) |
  | own-slot copier (repeats its own answer whoever is asked) | +0.997 | +0.999 [+0.992, +1.006] | +0.004 | +0.995 [+0.989, +1.001] | +0.003 [-0.006, +0.011] | pass | fail (copy) |
  | planted answer does not move its own re-rating | -0.003 | +0.001 [-0.005, +0.008] | +0.501 | -0.499 [-0.508, -0.489] | +0.000 [-0.009, +0.010] | fail | untestable (manipulation) |
  | egocentric leakage, lambda 0.5, Alex 0 | +0.523 | +0.268 [+0.225, +0.309] | +0.003 | +0.265 [+0.223, +0.308] | +0.210 [+0.179, +0.241] | pass | pass |
  | egocentric leakage, lambda 0.25, Alex 0 | +0.523 | +0.136 [+0.112, +0.159] | +0.003 | +0.133 [+0.104, +0.163] | +0.343 [+0.292, +0.392] | pass | pass |
  | leakage lambda 0.5 plus Alex pulling Sam as much as own pulls self | +0.523 | +0.268 [+0.225, +0.309] | +0.516 | -0.248 [-0.288, -0.208] | +0.210 [+0.179, +0.241] | pass | fail (anchoring) |

  The map's rule alone is passed by the source-blind anchor, the recency anchor and the own-slot copier. The full rule rejects all three (anchoring, anchoring, copy). It passes the leakage responders that have no source-blind pull, and it fails the one where Alex pulls Sam as much as the model's own answer pulls its own re-rating. Responders that do not move their own re-rating are untestable, as §5.2 requires.

- **Power (P2).** P(pass) by the full rule over synthetic runs. Sam's uptake in OWN is λ × the model's own, with the model's own on F3's profile and a vignette-level factor 1 + N(0, 0.5). Alex's pull on Sam is α + N(0, 0.1) per statement, wherever the displaced number is Alex's (SWAP). The true U_sam(OWN) is about 0.45 λ, and the true ΔU is about 0.45 λ − α.

  | α \ λ | 0.0 | 0.15 | 0.25 | 0.35 | 0.5 | 0.75 |
  |---|---|---|---|---|---|---|
  | 0.0 | 0.00 | 0.00 | 1.00 | 1.00 | 1.00 | 1.00 |
  | 0.1 | 0.00 | 0.00 | 0.17 | 0.88 | 1.00 | 1.00 |

  - 60 synthetic runs per cell, 400 resamples each.
  - With no source-blind pull (α = 0) the rule passes every run from λ = 0.25 (true U_sam about 0.11) and none at λ ≤ 0.15 (true U_sam ≤ 0.07). With α = 0.1 it needs λ ≈ 0.35 (true ΔU about 0.06) for 88%, and λ = 0.5 (true ΔU about 0.13) for 100%.
  - It never passed at λ = 0.
  - The sharp edge reflects the synthetic noise: per-call SD 1 point and a vignette factor SD of 0.5. If the model's real between-vignette spread is larger (bm0's per-statement own slopes had SD 0.28 around a mean of 0.12), the edge widens. The design can see a ΔU of about 0.06 or more. It cannot reliably tell a ΔU of 0.05 from slightly less, because the margin sits on the point estimate.

## 5. Pre-registered reading

Applied in this order (`rule()` in the code; EPS = 1e-9, so an exact bar value is on the stated side):

1. **Untestable (too few)** if fewer than 12 of the 16 vignettes have every cell answered (for example after a refusal stop).
2. **Untestable (manipulation)** if the lower end of U_self(OWN)'s 95% CI is not above 0: the planted answer did not move the model's own rating, so there is no shift of its own for Sam's to inherit.
3. **Fail (small)** unless U_sam(OWN) ≥ 0.10 (point) and the lower end of its 95% CI > 0. This is the map's event.
4. **Fail (anchoring)** unless ΔU ≥ 0.05 (point) and the lower end of its 95% CI > 0.
5. **Fail (copy)** unless the lower end of G's 95% CI > 0.
6. **Pass** otherwise, reported as **pass, unreplicated** (invariant 7).
7. **One vignette decides it:** the label stands as the rule gives it. If removing any single vignette changes the label or the fail reason, the result is reported as **fragile**, with the vignette named, and the ledger verdict carries a `fragile` note.
8. **Reported in every case:** the full uptake table (condition × question × distance), U_sam(OWN), U_sam(SWAP), ΔU, G, U_self in both conditions, the leakage ratio, the instance arm, the map's rule alone on these data (`map_rule`, beside the verdict and never in its place), the leave-one-out range and flips, calls, cost and refusals.

**Scoring.** Outcome 1 for pass, 0 for any fail. Untestable is not scored.

**The verdict sentences**, the only plain-English sentences the write-up may use for the verdict (P9; also `SENTENCES` in the code):
- **Pass:** "On Haiku, on program 1's 16 vignettes, a rating planted as the model's own earlier answer pulled the rating it attributed to Sam, a person who had seen neither that answer nor another reader's, by at least 0.10 points per point of displacement, and by at least 0.05 more than the same number shown as another reader's (Alex's) answer; and the model moved Sam's rating further when told Sam had seen its answer. The two conditions differ in whose number it is, its turn and its format together, so this cannot say which of those carries it."
- **Fail (small):** "On Haiku, on program 1's 16 vignettes, a rating planted as the model's own earlier answer did not pull the rating it attributed to Sam, who had not seen it, by at least 0.10 points per point of displacement with the interval above 0."
- **Fail (anchoring):** "On Haiku, on program 1's 16 vignettes, the model's own planted answer pulled the rating it attributed to Sam, who had not seen it, but not by at least 0.05 more (with the interval above 0) than the same number shown as another reader's answer, so the pull cannot be told apart from any number in the conversation pulling Sam's rating."
- **Fail (copy):** "On Haiku, on program 1's 16 vignettes, the model's own planted answer pulled the rating it attributed to Sam by more than the bar and more than another reader's number did, but not detectably less than when Sam was said to have seen that answer, so it cannot be told apart from the model repeating its own earlier answer whoever is asked."
- **Untestable (manipulation):** "The test could not answer: the planted answer did not move the model's own re-rating (its interval is not above 0), so there was no shift of the model's own for Sam's rating to inherit. It says nothing either way."
- **Untestable (too few):** "The test could not answer: fewer than 12 of the 16 vignettes have every cell answered (for example after a refusal stopped the run). It says nothing either way."
- **Fragile (appended):** "The label depends on one vignette: removing <id> changes it."

None of these says "belief", "simulation", "theory of mind", "curse of knowledge" or "Carruthers's model 3". A pass is *consistent with* attribution that starts from the model's own stated answer, and the write-up may say only that. A fail (anchoring) does not show the model reads only Sam's evidence (model 4); it shows that the own-answer pull on Sam was not separated from a number-in-view pull.

## 6. What it cannot do

- **OWN and SWAP differ in more than whose number is displaced (P8):**
  1. the source of the displaced number (the model's own answer, against Alex's);
  2. its turn (assistant, against user);
  3. its format (a bare JSON object, against a number in a prose sentence);
  4. its recency (turn 2, against the sentence just before the question).

  Everything else is matched: the same two numbers, the same words, the same turns. The claim is about this bundle. P2-6 is the test that separates label from position. Points 2–4 favour Alex's slot under plain anchoring, so they work against a pass, not for one.
- **"Sam has seen neither answer" is a sentence the model reads.** The design fixes what Sam is said to know, not what the model represents Sam as knowing.
- **The model's "own credence" is its re-rating after the plant.** The design moves the model's stated answer, not any internal state it may have.
- **Using one's own answer to guess a peer's** with the same evidence can be reasonable (people's ratings correlate with the truth). A pass shows the model's stated answer reaches Sam's rating, more than another reader's does. It does not show the model *should not* have used it.
- **Scope:** one model, 32 statements from 16 vignettes, one wording of each question, one turn layout, default temperature. No sentence may say "models", "LLMs", "every" or "all".
- The anchors m come from program 1's run 2. Today's unplanted rating may differ; every uptake is measured from today's REF cell, not from m, and the gap is reported.

## 7. Stop rules

- **Budget cap in code:** $1.00 (`CAP`), checked before every call. If it is reached, the later repeats are reported as not run, and the analysis runs on complete vignettes (§5.1).
- **Stop on any refusal:** no rewording, no retry, no new call until Sean has seen it. The refused job is written into the cache, and any later run on that cache exits before a call. Calls already in flight complete and are counted (`results/p2-5-calls-stop.json`). Also stop on any other API error. A stop on a non-refusal error may be resumed from the cache, and the error is logged in the results.
- **The run refuses to start** without `data/p2-5-seed.json` (the seed commit) and without the design review's go (or a confirmed fix-first) in `ledger/design-reviews/om-p2-5.md`.

## 8. Ledger entry

```json
{"id": "om-p2-5", "program": "other-minds", "direction": "P2-5", "title": "Egocentric leakage: does the model's own planted answer pull the rating it attributes to Sam, who never saw it?",
 "source": "literature", "referee": "model", "bet_type": "standard",
 "engine_odds_first": 0.30, "engine_odds": 0.33, "engine_odds_at": "this commit (lesson ls-om-p2-5); 0.30 in map/program-2-map.md 2026-11-04 10:19",
 "odds_event": "U_sam(OWN) >= 0.10 with CI lower > 0, and U_sam(OWN) - U_sam(SWAP) >= 0.05 with CI lower > 0, and U_inf(OWN) - U_sam(OWN) CI lower > 0 (16 vignettes, cluster bootstrap)",
 "human_odds": null, "human_odds_note": "no human odds",
 "prereg_commit": "<this commit>", "budget_usd": 1.00, "seed_source": "curby-rng", "beacon": null, "seed": null, "tiebreak": null,
 "lesson": "ls-om-p2-5", "design_review": {"path": "ledger/design-reviews/om-p2-5.md", "verdict": null, "commit": null, "reviewer_model": null, "fix_deviations": [], "missed": null},
 "premortem": "If this fails, the most likely reason is that Alex's number, shown in the user turn just before the question, pulls Sam's rating at least as much as the model's own planted answer does.",
 "premortem_kind": "world", "verdict": "open", "date": "2026-11-04"}
```

## 9. Checklist before the first call

- [x] Committed on its own; nothing of this test has been run.
- [x] The lesson row in §0 is filled after reading ledger/bets.jsonl, brier.md, audits/ and lessons.jsonl. The same sentence goes to `ledger/lessons.jsonl` as `ls-om-p2-5`, word for word.
- [ ] A fresh auditor's design review has returned **go**, or fix-first with every fix logged in DEVIATIONS and confirmed. `python3 ledger/check_prereg.py om-p2-5 . programs/other-minds/experiments/p2-5-egocentric.md --before-run` passes.
- [x] Engine odds on record earlier (map, 30) and revised here by the lesson (33), both kept. Human odds: none in `ledger/human-odds.jsonl`, so "no human odds".
- [x] The pass rule in §5 can be applied by a stranger (`rule()`; the dry run applies it to ten synthetic tables).
- [x] The pre-mortem in §0 is one sentence, names a checkable mechanism, and carries its kind.
- [x] One scale direction in every graded prompt.
- [x] §2 records CURBY-Q's latest completed round and names the chain by the 24-hour rule; the seed commit follows this one before any data.
- [x] Budget cap and stop-on-refusal in code (`GuardedCaller`), not by hand.
- [x] DEVIATIONS.md row D11 added.

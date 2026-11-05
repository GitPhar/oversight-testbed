---
bet: om-p2-6r
program: other-minds
prereg_commit: ddb6c92
reviewer_session: fresh design-review subagent launched by the om-p2-6r author session
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 04:56 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: holds, D6: holds, D7: holds, D8: flaw, D9: holds, D10: flaw, D11: holds}
flaws: 4
pilot_usd: 0.00
verdict: fix-first
confirmed_at: null
---

# Design review of om-p2-6r

## In plain English

As built, this replication would mostly answer its question. The prompts are byte-for-byte P2-6's: the imported builders reproduce all 7,040 of Haiku's archived hashes. The API settings are valid for Sonnet 5.5 and Opus 5.5 and match the pre-registration, the gate and the seed hold, and the bet can both pass and fail: P(pass) is about 1 if both models take up shown answers like Haiku, and about 0 below roughly 0.6 of Haiku's uptake.

Four things must change before the first call, and none of them changes the scored event or its bar:
- **Crash.** The pre-registered analysis command crashes when it writes the tables, because Haiku's reference file has no `P_minus_L`. The dry run never ran that step.
- **No-own-pull sentence.** It claims the own-answer pull is "not present" from a non-detection. It can also be attached to a "holds" table, which it then contradicts.
- **Fail sentence.** In the world the design itself names as most likely (smaller uptake, with position still beating the label), the fail sentence reads as if the ordering failed to replicate. No frozen sentence says that the ordering held at a smaller size.
- **Run order.** Sonnet and Opus share one thread pool, so Opus calls can go out before a late Sonnet refusal is seen. This breaks §7's "a refusal on Sonnet means Opus is never called". The refusal record also shares `results/refusal.md` with om-p2-7.

## Checks

Commands: all Python ran as `env -u ANTHROPIC_API_KEY /Users/seanpharris/entangled-mind/.venv/bin/python -I`, in a `mktemp -d` scratch directory, with every call stubbed. `p2_6r_replication.py` ran only as `show`. Its `main()` with `--analyse` ran only after `RESULTS`, `CACHE`, `OUT_JSON`, `OUT_MD` and `SEEDF` had been redirected to the scratch directory. Nothing was written under `programs/other-minds/results/` (`git status` checked).

**D1. The rule can be applied by a stranger: holds.**
- `model_reading()` and `overall()` follow §5.2–5.3 in the stated order. I checked thresholds, EPS handling, P > |L| on points, and the P_s conjunct.
- The dry run's §6 tables each return one reading. I added edge tables, and each also returns exactly one reading:
  - P ≥ 0.15 with an undetected L larger than P gives fail-small.
  - P_s passing while P fails gives fail-small.
  - A holds table with AY not detected gives holds.
  - P ≤ −0.15 together with a large L gives fail-reversed, which comes first.
- An end-to-end synthetic cache (Sonnet Haiku-like, Opus at 0.4 × Haiku's uptakes) gives "Sonnet holds; Opus fail-small → fail", with 0 LOO flips.
- With one Opus entry of repeat 1 removed, Opus is read at k = 1 and the run still gives a verdict. With no Opus calls, the result is untestable, with the frozen sentence.
- The *entry point* a stranger would run does not finish (F1, under D10).

**D2. Every manipulation takes effect: holds.**
- **Builders.** The imported P2-6 builders reproduce the sha256 of all 7,040 entries in Haiku's `results/p2-6-calls.json` (7,040 ok, 0 mismatched). The prompts are therefore exactly om-p2-6's.
- **Jobs and order.** The replication's repeat-0 job set equals Haiku's minus `UU`. The run order within repeat 0 is the same permutation on both models, as §3 says.
- **Displacement.** The +30 and −30 displays differ (for example 98 and 55 on co-lin08 X). 23 of 64 shown values sit at the 2/98 clip, as in P2-6.
- **Request kwargs** (rebuilt from `real_call()`'s code, not sent):
  - Sonnet: `thinking={"type": "between_tools"}`, `output_config={"format": json_schema RATE}`, max_tokens 200.
  - Opus: `output_config={"effort": "low", "format": …}`, with no `thinking` key (adaptive, the only mode Opus 5.5 allows), max_tokens 4000.
- **These settings match §2 and are valid for these models** (claude-api reference, 2026-10-06 cache):
  - Sonnet 5.5 rejects `disabled`. `between_tools` is its lowest setting and is accepted at effort high or below. The code sends no effort, so the default is `high`, and no other field goes inside `thinking`.
  - Opus 5.5 400s on `disabled` at every effort; `low` is the minimum.
  - Neither request sends sampling parameters (non-default values 400 on Sonnet 5.5) or a `fallbacks` parameter. Fallback is opt-in, so none occurs, as §0/§7 require.
  - The planted assistant turn is followed by a user turn, so it is not a prefill (prefill 400s on both models). It carries no thinking block, so the history-editing check has nothing to bind.
  - Program 1 ran the same OFF settings with this schema on both models: mm-gm3b ran 4,800 Sonnet and 4,080 Opus calls, with 0 errors and 0 max_tokens stops.
- **Prices** in `config.PRICES` ($2/$10 and $4/$20) match the reference. Output tokens include thinking.

**D3. Every control can fail: holds.** The only control-like element is the shift-invariant P_s conjunct, meant to reject a re-rating that moves without following the shown number. The assistant-turn hedge responder (`hedge-A:0.5`) is rejected in 100% of the dry run's 150 runs at SD 3 and SD 8, by fail-small or fail-shift.

**D4. Rivals matched: holds (no rival families).** The named rival, a smaller uptake in every cell, is a world rather than a fitted family. The dry run's `scaled:k` worlds cover it.

**D5. Dumb baselines and visibility: holds.** No null rule. The copier, no-uptake, label-only and assistant-turn-hedge responders each pass 0/150 at both noise levels (dry run §7). I could not build a dumb responder that passes without having a position effect.

**D6. Execution risks piloted: holds, with a recommendation.**
- The pre-mortem is of kind `world`, and the items (Linda-type vignettes) are not likely to be refused. Opus's token-cap risk is met by max_tokens 4,000.
- Cost risk:
  - Program 1's Opus runs have twice exceeded their estimates. DM2 cost 2.1× its pilot estimate and budget-stopped (DM4a); DM4's Opus arm fell back to R = 2.
  - Here the cap covers both Opus repeats only if Opus costs ≤ 1.29× the mm-gm3b estimate ($0.00568 a call). It covers one repeat up to 2.6× ($0.0114 a call). mm-gm3b's Opus per-call cost had p95 1.8× and max 2.9× the mean.
  - §5.1 already accepts a model with one complete repeat. My simulation shows k = 1 on Opus barely changes P(pass) (D11 table).
  - So the risk is mainly to n. The design fails only if Opus averages more than 2.6× the estimate.
- *Recommended, not required:* an author-run pilot of at most $0.05 (8 Opus calls on ±20 displays, which are not in the test) to record Opus's per-call cost on these prompts before the run. Or state in §7 that Opus at one repeat is a likely outcome.

**D7. Comparisons match: holds, with a note.**
- Within each model the cells differ only as P2-6's (position bundle, owner word), and §6 states the position bundle.
- Across models, §0/§6 list the setting bundle (between_tools, adaptive at low effort, thinking disabled on Haiku; 3/2/20 repeats). No verdict sentence compares a model with Haiku as if only the model differed: "as on Haiku" in the pass sentence states a fact.
- *Note:* one more difference exists only on the thinking models. On Opus a real own turn would carry a thinking block, so a planted assistant turn without one resembles a genuine own answer less than it did on Haiku, where thinking was off. §6's "the model or its setting" covers this generically. Naming it in §6 is recommended.

**D8. The verdict sentences are written: flaw (F2, F3).**
- Every reading has a frozen sentence in `SENTENCES`, and §5 matches the code word for word.
- I ran each sentence on tables that reach it. holds, fail-shift, fail-reversed, fail-label, fail-small, fragile and untestable are true for every table their branch admits.
- Two are not: F2 and F3 below. A minor third (the pass sentence's label comparison is on the frozen measure only) is in F3.

**D9. One item cannot decide it: holds.**
- Leave-one-item-out runs per model, with the other model held at its full-data reading, and re-applies the full reading (P and P_s, with the bootstrap).
- Any overall flip sets the label "<verdict>, fragile (one item)" and the frozen fragile sentence. The full-data rule still scores the bet.

**D10. Machinery: flaw (F1, F4).** What holds:
- **Budget.** The cap is checked under a lock before every call. Stub, at an unrealistic $0.0808 for every Opus call: stopped at $4.61. Real overshoot is bounded by 8 calls in flight, about $0.04 at the estimate and about $0.10 at mm-gm3b's maximum.
  - Note: calls that stop on max_tokens or an error are billed but never enter `spent()`.
  - Note: refused entries are recorded at $0.
- **Stop on refusal.** The refused job is written to the cache, a re-run on that cache exits, and nothing is reworded. A tampered cache entry is caught.
- **Scale direction.** One scale direction in every prompt.
- **Caching.** Cached by a content hash that includes model, settings and max_tokens.
- **Seed.**
  - `ledger/seed.py` recomputes 17652080689546741571, order 3622963555 and boot 201936860.
  - CURBy-RNG pulse 1592170 (04:46:00) is the first after the pre-registration commit (04:45:09); the previous pulse, 1592169, was at 04:45:00.
  - CURBY-Q's stall is recorded.
- **Gate.**
  - It refuses without the seed file or a go / confirmed fix-first in every `om-p2-6r*.md`; the dry run's §3 checks this.
  - It reads this file's header correctly.
  - It stays closed until `confirmed_at` is set.
- **Lesson.**
  - `check_prereg.py`: L1, L2 and L3 ok. R1 failed only because this file did not yet exist.
  - The read block matches the ledger at f9fc45a: 19 scored, Brier 0.259, base rate 0.43, newest audit ng-p3-5c.
  - *Note for the auditor (E25):* the frozen lesson is 61 words by whitespace count, against learn.md's 60. It cannot be changed, so it is not counted here.

**D11. The bet can both pass and fail: holds.** The dry run's §7 already shows P(pass) of 1.00/0.97 in the Haiku world and 0.00 at 0.46 × Haiku. I added a finer grid, all four uptakes scaled by k on both models, 100 runs per cell, and also re-ran with Opus at one repeat (the cap fallback):

| call SD | repeats (S/O) | k = 1.0 | 0.9 | 0.8 | 0.7 | 0.6 |
|---|---|---|---|---|---|---|
| 3 | 3/2 | 1.00 | 1.00 | 0.99 | 0.62 | 0.01 |
| 3 | 3/1 | 1.00 | 1.00 | 0.97 | 0.65 | 0.02 |
| 8 | 3/2 | 0.97 | 0.90 | 0.71 | 0.34 | 0.03 |
| 8 | 3/1 | 0.93 | 0.87 | 0.63 | 0.30 | 0.07 |

- Both P(pass) and P(fail) exceed 10% under worlds the design names, at the planned and at the fallback n.
- The table also shows what the event mostly measures: whether both models' overall uptake is at least about 0.7 of Haiku's. In the scaled worlds, position beats label at every k, and the verdict still turns from pass to fail between 0.8 and 0.6.
- That is a legitimate frozen event; §1's "rival" paragraph says so. But it is why F3 matters.

## Required fixes

Each fix goes in a dated DEVIATIONS.md row in programs/other-minds, written before any call and naming this review. None changes the scored event, the 0.15 bar, the cap or the odds.

**F1 (D10, blocking). The pre-registered analysis command crashes.**
- `write_md()` builds the Haiku reference column with `fmt(h[block][k])`. Haiku's `p2-6-position-or-label.json` has no `P_minus_L` key, which is not computed in om-p2-6, so the code raises `KeyError: 'P_minus_L'`.
- `main()`, whether the run itself or `--analyse`, writes `p2-6r-replication.json` and then dies before `p2-6r-tables.md` is written. Reproduced on a synthetic cache in the scratch directory.
- The dry run never exercised `write_md()` or `main()`.
- *Fix:* print "—" in the reference column for any key the Haiku file lacks, or compute Haiku's P − L from its stored item uptakes. Then add a dry-run step that runs `main()` with `--analyse` on a synthetic cache in a temporary directory, with `HAIKU_JSON` pointing at the real Haiku file, and commit the output.

**F2 (D8). The "no own pull" sentence overclaims and can contradict "holds".**
- It fires whenever the AY interval's lower end is ≤ 0. It says the own-answer pull "is not present in this wording", which is an absence claim from a non-detection at 16 items and 2–3 repeats (P2/P9).
- It also says "the position effect there has little to split". That is false on a holds table where the user-turn uptakes are negative. bm1 saw a −0.11 uptake for another person's value, so such a table is plausible: e.g. AY +0.10 [−0.02, +0.22], UY −0.15, US −0.17, giving P +0.25 [+0.14, +0.36] and a reading of holds, with the no-own-pull sentence attached.
- *Fix (wording only):* "On {M}, the value labelled as the model's own and placed in its own turn was not detectably taken up (uptake {AY}): this design did not detect an own-answer pull in this wording on {M}."
- Keep "and the position effect there has little to split" only when the reading is not `holds`, or drop it.

**F3 (D8). The fail sentence misreads the design's own most-likely failure world.** The pre-mortem and §1's rival name the most likely failure: smaller uptake in every cell, with position still above the label. On such a table, P +0.09 [+0.05, +0.14], L +0.04, P − L +0.06 [+0.00, +0.11], the overall sentence opens "The position-over-label result found on Haiku 5.5 did not hold on both…". A reader takes that to mean the ordering failed. "Did not hold on both" can also be read as "held on neither" when one model holds. No frozen sentence reports the ordering surviving at a smaller size. *Fix (wording and one secondary sentence; scoring unchanged):*
- (i) Reword the fail sentence's opening to: "The pre-registered event did not occur: Sonnet 5.5 and Opus 5.5 did not both meet the rule (on each model: …)."
- (ii) Add a frozen secondary sentence, printed after a fail-small reading when P's CI lower end > 0 and the P − L CI lower end > 0: "On {M}, the position effect, {P}, was below the 0.15 bar but larger than the label effect (position minus label {P_minus_L}): the ordering seen on Haiku held on this design at a smaller size." Add the matching sentence for the case where P − L's CI includes 0: "…and could not be told apart from the label effect at this n."
- (iii) In the pass sentence, write "and by more than the label … changed it on the pre-registered measure". The P > |L| check is not applied to P_s / L_s.

**F4 (D10, minor). Run order and the refusal record do not do what §3/§7 say.**
- **Run order.** All 1,440 jobs go through one 8-worker pool, so Opus jobs start while the last Sonnet calls are still in flight.
  - A stub whose refused call is slower than the rest (0.2 s against 0.02 s) refused at Sonnet call 858 or 862 of 864. 43–48 Opus calls were sent and cached before the stop was seen.
  - This contradicts §7's "A refusal on Sonnet means Opus is never called" and §3's "Sonnet complete before Opus starts". The same overlap exists between repeats, but there it is harmless, because analysis uses leading complete repeats.
  - *Fix:* call `GuardedCaller.run()` twice, once on Sonnet's jobs and then on Opus's only if the first returned `"complete"`.
- **Refusal record.** `results/refusal.md` is the same path om-p2-7's caller (`p2_7_format_fingerprint.py`) writes and checks, and om-p2-7 belongs to the same session.
  - A refusal in either bet silently blocks the other.
  - If both run at once, one refusal record can overwrite the other.
  - *Fix:* write `results/refusal-p2-6r.md`, keep the check for `refusal.md`, and add a check for `refusal-p2-6r.md` on start.

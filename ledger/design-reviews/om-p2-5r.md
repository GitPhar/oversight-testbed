---
bet: om-p2-5r
program: other-minds
prereg_commit: b759934
reviewer_session: fresh design-review subagent, worktree p2-wave3 at 05c3737 (code unchanged since b759934; seed commit 28e5224)
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 10:22 America/Denver
checks: {D1: holds, D2: holds, D3: holds, D4: holds, D5: flaw, D6: flaw, D7: flaw, D8: flaw, D9: holds, D10: flaw, D11: holds}
flaws: 5
pilot_usd: 0.00
verdict: fix-first
confirmed_at: 2026-11-05 10:38 America/Denver
---

# Design review of om-p2-5r

## In plain English

As built, the test mostly answers its question. It runs om-p2-5's conversations on Sonnet and Opus, scores upward and downward plants as separate conjuncts, and can both pass and fail. Five things need fixing before the first call:
- **A dumb responder passes.** A model that answers "what would Sam give" with the average of the two numbers on the page, whoever gave them, passes 0.95 of the time. Finding 6 says the model's *own* answer leaks into Sam, and the SWAP contrast that would catch this is only a secondary.
- **The cost estimate is low.** The Opus estimate averages in om-p2-6r's cheap one-turn calls. On om-p2-6r's three-turn calls, Opus costs enough that its $3.50 cap may stop it mid-run, which would throw away about $3.50.
- **The frozen sentences overclaim.** They never say that the two ratings answer differently worded questions. "Above its usual rating" means Haiku's usual rating, not the model's. The bet-fail sentence names Opus as tested even when Opus was not run.
- **The reading depends on how the analysis is run.** A model that stopped one call short reads `not_run` on the run path but `pass` under `--analyse`, which is the path an auditor reproduces.

None of the fixes changes what is tested. One of them adds a conjunct that tightens the bar.

## Checks

Commands were run from `programs/other-minds` with `/Users/seanpharris/entangled-mind/.venv/bin/python`. Test scripts are in the reviewer's scratchpad (`t_machinery.py`, `t_analysis.py`). `real_call` was replaced by a function that exits, and `RESULTS` and `REVIEW_DIR` were redirected to the scratchpad. No paid call was made.

**D1. A stranger can apply the rule: holds.** `reading()` was run on 13 synthetic CI tables. Each returned exactly one reading, the one §5's order gives: untestable_few, untestable_nothing_moved, pass, up_only, down_only, reversed and none. Two cases checked the order: up_only beats reversed when only the upward bound clears, and a model where only Sam moved still passes. `bet_reading()` was run on all 64 pairs of per-model readings. It always returns one of pass, fail or untestable, and it matches §5: one pass gives pass; at least one tested model and no pass gives fail; nothing tested gives untestable. §5's prose and `reading()` agree line for line.

**D2. Every manipulation takes effect: holds.** In an OWN job (co01 X, d +30), the assistant turn is `{"probability": 98}` and Alex's number is 85 (m). In the matching SWAP job the two are swapped. REF shows m in both. There are 568 jobs a repeat: REF self/sam_p 32 + 32, OWN self/sam_p 168 + 168, SWAP sam_p 168, as §2 says. They make 514 distinct prompts; the 54 duplicates are om-p2-5's 18 clipped cells × 3 questions, inherited. `content_hash` includes model, settings and max_tokens, and Sonnet's and Opus's hashes differ for the same messages. The dry run reproduces `p2-5r-dryrun-output.txt` line for line, and readings move with the world as stated. The Haiku reference reads om-p2-5's SWAP keys: Sam's uptake of Alex's number is +0.021, the 0.02 in finding 6.

**D3. Every control can fail: holds.** The manipulation check rejects a responder where nothing moves (untestable_nothing_moved 0.95). "Sam = own" never passes (0/60), and "Sam half of own" reads reversed 1.00. Neither wrong set-up can reach pass.

**D4. Rivals are matched: holds (n/a).** No fitted rivals, and no sentence compares models.

**D5. A dumb baseline is beaten: flaw.** The dumbest responder that fits the design answers Sam with the mean of the two numbers on the page, whoever gave them, and re-rates its own answer with uptake 0.36. It passes **0.95** (up_only 0.05) over 40 synthetic runs, 400 resamples each. A responder whose Sam rating is pulled 0.45 by any number, own or Alex's, with own uptake 0.30, passes **0.80**. In both, Sam's own-minus-Alex difference (`dU_all`) has its lower bound above 0 in only 0.03 of runs. So the rule cannot tell "the model's own answer leaks into Sam more than into itself" (finding 6: own 0.36, Sam 0.50, Alex's number on Sam 0.02) from "Sam's rating follows any number in the conversation". The SWAP cells that separate the two are run, but §4 puts them in the secondaries only. There is no null rule, so no margin or power check is needed.

**D6. Foreseeable execution risks: flaw (cost; refusals hold).** Refusal risk is low: the same everyday vignettes ran 1,440 times on these models without a refusal or a max_tokens stop. The cost estimate is the problem. `EST` uses om-p2-6r's mean per-call cost over all its cells, and on Opus that mean depends heavily on the prompt (per-call means from `results/p2-6r-calls.json`):
- one-turn base cells: $0.00142
- user-turn cells: US $0.00230, UY $0.00275
- three-turn assistant cells: AS $0.00246, AY $0.00288

This bet's prompts are all three-turn, carry two numbers and are longer (692 against 546 characters on average). Re-estimated for Opus's 1,136 calls:
- AY/AS mean: $3.03
- AY alone, the closest analogue to OWN: $3.27
- linear in prompt length: $3.49

All three are against the frozen $2.80 and a per-model cap of $3.50. Sonnet comes out at $1.01–1.09 against a $1.50 cap, which is fine. With 1,136 calls the total is close to deterministic, so the cap stops Opus if its true mean is more than about 7% above AY's. A stop after call ~1,000 leaves every vignette incomplete (tested: 0 complete), so Opus reads not_run after about $3.50 of spend. The pre-mortem does not name this, and no pilot or cap margin covers it.

**D7. Comparisons are matched: flaw.** Own and Sam differ in more than the factor named:
- the target ("you" against "Sam, a person")
- the verb ("Please give your rating again", which invites reconsideration, against "what rating would Sam give")
- whether both earlier answers are named (the Sam question names "your earlier answer" and "Alex's answer"; the self question names neither)
- length

§1, §6 and P8 disclose this, and the disclosure is accurate. But the frozen sentences, the only verdict sentences the write-up may use, describe the result as Sam against the model's own re-rating, with no bundle clause. om-p2-5 appended a BUNDLE sentence to every OWN/SWAP sentence for this reason. Its audit named the wording rival as the open threat and recorded a D8 miss for a sentence that read more into Sam > self than the data carry. Between models, settings and repeats differ, but each model gets its own reading and no sentence compares models, so that part holds. The Haiku column is labelled with its archive and its 5 repeats.

**D8. The verdict sentences are written: flaw.** All sentences exist and format; none says false consensus, theory of mind or belief. Three of them use nouns the design cannot carry:
- (a) **"answers planted above [below] its usual rating."** The anchors are Haiku's m, not Sonnet's or Opus's (§6 says so). Against each model's own one-turn rating in om-p2-6r's base cells, 6 of 25 Opus plants at d = −10 and 3 of 25 at −30 lie *above* Opus's own rating, as do 2 of 31 at +10. On Sonnet the counts are 3, 1 and 2. Opus's own rating differs from m by 10 points or more on 25% of statements, and by up to 52 points.
- (b) **`bet_fail`** says "on neither Sonnet 5.5 nor Opus 5.5 did Sam move further…". The code prints it when Opus is not_run or untestable_nothing_moved and only Sonnet was tested (shown for (none, not_run) and (none, untestable_nothing_moved)). Opus untestable is plausible (om-p2-6r's Opus own uptake was +0.07–0.08, interval near 0), and so is an Opus cap stop (D6).
- (c) **`bet_pass`** names only the passing model. If the other model reads reversed, the bet sentence says nothing about it, though the novelty page says a second model showing the opposite "kills it cleanly". (The per-model sentences do report it.)

**D9. One item cannot decide it: holds.** Leave-one-vignette-out is pre-registered and in code. Each drop re-applies `reading()` with the run's count for the 12-vignette floor. Any flip appends the frozen fragile sentence and the reading stands. Note: on the Haiku archive, dropping co-lin10 flips Haiku's reference reading from up_only to pass, so the sentence will be needed.

**D10. Machinery: flaw (analysis of a stopped model).** What holds:
- **Caps.** With stub callers, a Sonnet cap stop leaves Opus uncalled at $1.50. Opus stops at $3.50 (1,000 of 1,136). The total cap stops at $5.0025, overshooting by in-flight calls of at most 8 workers, which is acceptable.
- **Stop on refusal.** A refusal at call 10 stops the run: no Opus call, the refusal written to the cache and to `refusal-p2-5r.md`, and resume refused on the cache alone. An error or a malformed value stops the run.
- **Order.** The order is Sonnet first, all 1,136 before any Opus call. Within a model the repeat is outermost, and the permutation is the same for both models.
- **Cache hash.** A mismatched hash on a cache hit is caught.
- **Gate.** The gate refuses with no review, with fix-first unconfirmed, with a second review reading redesign, or without the seed file. It opens on go or on a confirmed fix-first.
- **Scale.** 0 = certainly false, 100 = certainly true in every prompt.
- **Seed.** `ledger/seed.py` recomputes both seeds from pulse 1592495, the first after the 10:10:34 commit (previous pulse 10:10:00).
- **Lesson.** `check_prereg.py`: L1–L3 ok, H1 ok. The 64-word overrun is recorded in D18a.

The flaw: `analyse_cache` marks a model not_run only when `status` says it stopped. Under `--analyse` (status None), which is the path the results file and any audit reproduce, a model that stopped short is analysed on whatever is cached. With a clear-gap stub and Opus missing its last 1, 2 or 3 calls, the run path reads Opus **not_run**, while `--analyse` reads **pass** on 15 vignettes. A Sonnet fail plus that Opus would turn the bet from fail into pass depending on how the analysis is invoked, against §5 ("stopped mid-run is not_run") and §7.

Record notes, not flaws:
- The map node says `"opened": "2026-11-05T10:20"` in a commit at 10:04:37 (written clock times are unreliable; commit times govern).
- The dry-run world labelled "Haiku as measured, up-only gap (Sam down .36)" is not Haiku as measured. Haiku's measured downward gap is +0.042 (Sam 0.425, own 0.383), which is the world labelled "Haiku-like".
- The Haiku column's pooled gap is +0.130, against om-p2-5's published +0.139, because "both" here weights the two signs equally while om-p2-5 pooled cells within each class. The design defines it so (§4), but the write-up should say why the numbers differ.
- Haiku reference key format: matches (`{vid}|{o}|{cond}|{d}|{q}|{r}`, prefix ""; 7,360 = 5 × 1,472 entries, complete). It reproduces the om-p2-5 audit's split: gap up +0.217 [+0.159, +0.272], down +0.042 [−0.024, +0.098] (audit: +0.217 [+0.157, +0.274], +0.042 [−0.020, +0.102]). Reading: up_only.

**D11. The bet can both pass and fail: holds.** Per model, from the dry run: pass 0.85 with a clear +0.15 gap both ways, 0.23 Haiku-like and 0.15 at +0.08. Worlds where the hypothesis fails give pass about 0: Sam = own 0/60, reversed 0, Opus-like weak pull 0, nothing moves 0. With two models and "at least one", P(pass) in a Haiku-like world on both is about 0.41 if the models are independent. The false-pass rate stays near 0 because each model needs two lower bounds above 0 (Sam = own: up_only 0.03, down_only 0.05). On real Haiku data cut to 2 repeats, all 10 pairs of om-p2-5's 5 repeats read up_only, with gap_down lower bounds from −0.047 to −0.010. That is one dataset, consistent with the 0.23 world, and it shows the dry run's spreads (P15) are about right: real gap_down half-width about ±0.065. In every named world both P(pass) and P(fail) are above 10%, except the deliberately degenerate ones. The D5 fix's conjunct does not bind in the hypothesis worlds, where Alex's pull is 0.02 and dU ≈ 0.4, but the dry run must be re-run to show it.

## Required fixes

Each fix needs a dated DEVIATIONS row (D18b–D18f, or one D18b with items) written before any call and naming this review. Odds may be revised before data, keeping both numbers.

1. **D5. Source-blind responder passes.** Add a conjunct to §5 step 3 and `reading()`: a model reads **pass** only if gap_up and gap_down each have their lower bound above 0 **and** `dU_all` (Sam's uptake of the model's own planted answer minus Sam's uptake of the same number shown as Alex's, SWAP) has its lower bound above 0. A model that meets both gaps but not dU reads **`sam_follows_any_number`**. It is tested and not a pass. Frozen sentence: "On {M}, Sam's rating moved further toward the planted number than the model's own re-rating did in both directions, but not detectably more when the number was the model's own earlier answer than when it was Alex's (own minus Alex {u}, 95% interval [{ul}, {uh}]), so this does not show the model's own answer leaking into Sam's rating." Add the worlds "Sam = mean of the two numbers shown" and "source-blind Sam" to `dry_run()`. Their pass rate must be at most about 0.05, and the existing worlds' pass rates must be restated.
2. **D6. Opus cost estimate.**
   - Re-estimate from om-p2-6r's three-turn cells: Sonnet about $1.01, Opus $3.03–3.27 (AY/AS; AY), total about $4.0–4.3.
   - Raise the Opus cap to at least $4.25 (AY × 1.3) and the total cap to at least $5.75 in `CAPS`/`CAP`, §0, §3 and §7, under a new budget ruling in `ledger/spend.jsonl` (br-010 approved $5.00).
   - If the engine will not spend more, the alternative is a pilot of at most $0.10 on prompts the test does not use (for example 30 Opus calls of om-p2-5's `sam_i` question in OWN cells) to measure Opus's per-call cost, with the caps set from it. Either way, state in §7 the expected chance of an Opus cap stop.
3. **D7. Wording bundle not in the sentences.** Append to the pass, up_only, down_only, reversed, `sam_follows_any_number` and `bet_pass` sentences: "The two ratings answer differently worded questions ('Please give your rating again' against a question about Sam that names both earlier answers), so the difference may belong to the wording rather than to whose rating is asked for."
4. **D8. Sentence nouns.**
   - (a) In pass, up_only and down_only, replace "above (below) its usual rating" with "above (below) Haiku's usual rating for that statement (the number shown as the model's earlier answer in the reference conversation)".
   - (b) Make `bet_fail` name only the tested models and the reason the others gave no reading: "…did not occur: on {tested}, Sam did not move further than the model's own re-rating in both directions; {untested} gave no testable reading ({why})". Drop the second clause when both were tested.
   - (c) Make `bet_pass` add the other model's reading when it is tested and not pass: "On {other}, the reading was {reading}."
5. **D10. not_run must not depend on `status`.** In `analyse_cache`, mark a model **not_run** whenever its cache holds fewer answered (non-refused) entries than its planned jobs, whatever `status` says. Also read `p2-5r-calls-stop.json` in `analyse()` and pass its reason into the not_run sentence. Add a dry-run assertion: a full stub cache with one Opus job removed reads not_run under both `analyse_cache(..., status)` and `analyse_cache(..., None)`.

Recommended, not required:
- relabel the dry-run world "Haiku as measured" (its downward gap is 0, not Haiku's +0.04)
- say in the write-up why the Haiku column's pooled gap (+0.130) differs from om-p2-5's +0.139
- report, as a secondary, the up/down split by sign relative to each model's own one-turn rating from om-p2-6r's base cells (archived, a different run; never promoted)

## Addendum: fixes confirmed (2026-11-05 10:38 America/Denver)

The author applied the five fixes under DEVIATIONS D18b, commit `d71608d` (10:33:55). They were written before any call: `programs/other-minds/results/` holds no p2-5r file, and the only results commits since `ff19617` are om-p2-15's. I checked the code at `d71608d`, the bet row, br-011, and the dry run. Commands were run with `/Users/seanpharris/entangled-mind/.venv/bin/python`. The scratchpad scripts `t_machinery.py`, `t_analysis.py` and `t_fix.py` were re-run on the new code with stub callers. `real_call` was replaced by a function that exits. No paid call was made.

**Rerun.** `--dry-run` and `plan`, re-run here, match `experiments/p2-5r-dryrun-output-D18b.txt` line for line.

- **F1 (D5): holds.**
  - `reading()` now returns pass only when gap_up, gap_down and `dU_all` each have their lower bound above EPS. When both gaps clear but `dU_all` does not, it returns `sam_follows_any_number`.
  - `bet_reading()` counts that reading as tested and not a pass. Shown: (sam_follows_any_number, none) gives fail, and (sam_follows_any_number, not_run) gives fail.
  - The frozen sentence is in `SENTENCES` and formats.
  - In the dry run, the mean-of-two-numbers responder reads `sam_follows_any_number` 0.98 with pass 0, and the source-blind Sam reads it 0.85 with pass 0. The hypothesis worlds are unchanged: Haiku-like 0.23, clear two-way gap 0.85, +0.08 gap 0.15. So D11 still holds.
  - My 13 synthetic tables (now with `dU_all`) return the same single readings as before. The new dry-run assertions cover a `dU_all` lower bound of 0.0, which reads `sam_follows_any_number`, and 1e-4, which reads pass. The bar is tightened, not lowered.
- **F2 (D6): holds.**
  - `CAPS` = Sonnet $1.50 and Opus $4.25; `CAP` = $5.75. Opus `EST` is $3.49/1,136, the top of my range. `plan` shows Opus $3.49, total $4.47.
  - With a stub at $0.0039 per Opus call, Opus stops at $4.251 with Sonnet complete, and Sonnet's cap still stops at $1.50 with no Opus call.
  - br-011 in `ledger/spend.jsonl` amends br-010 to $5.75. The bet row has `budget_usd` 5.75 and `budget_ruling` "br-010, amended br-011".
  - Sonnet's estimate stays at $0.98, below my $1.01–1.09, but well inside its cap; this is not a flaw.
- **F3 (D7): holds.** `WORDING` is appended to the pass, up_only, down_only, reversed, `sam_follows_any_number` and bet_pass sentences, and each was formatted and checked. The clause names the two question wordings and says the gap may belong to the wording. It is shorter than my suggested text: it omits that the Sam question names both earlier answers. That still carries the bundle, so it is acceptable.
- **F4 (D8): holds.**
  - (a) pass, up_only and down_only say "Haiku's usual rating". The Haiku reference sentence shows it.
  - (b) `bet_fail` names only the tested models and lists the others' readings. (none, not_run) reads "…on Sonnet 5.5, Sam did not… ; on Opus 5.5 the reading was not_run." (none, untestable_nothing_moved) is the same.
  - (c) `bet_pass` adds the other model's reading. (pass, reversed) reads "…; on Opus 5.5 the reading was reversed."
  - Readings appear as codes (`not_run`) rather than prose. That is acceptable, because the per-model not_run sentence gives the reason.
- **F5 (D10): holds.** `analyse_cache` marks not_run whenever a model's answered (non-refused) calls are fewer than planned, whatever `status` says. `analyse()` reads the stop file and passes its reason through. My earlier test now gives not_run on both paths, the run path and `--analyse`, with Opus missing 1, 2 or 3 calls; before the fix, `--analyse` read pass. The dry run asserts the same.

**Odds.** The bet row keeps both numbers: `engine_odds_first` 0.12, `engine_odds` 0.15 (prior 0.32 − 0.17), each with its context in `odds_history`. That is allowed before data.

**Unchanged.** The run order, cache hashing, stop-on-refusal and the gate all re-test as before. The Haiku reference still reproduces the audit's split: up +0.217, down +0.042, dU +0.468, reading up_only.

All five fixes hold. **Verdict: fix-first, confirmed at 2026-11-05 10:38 America/Denver.** The gate opens once this file is in the working tree.

---
bet: em-gm2q
program: entangled-mind
prereg_commit: 2f30696
results_commit: e4b57f2            # the audit clone's re-commit of the results commit (author time 2026-11-05T07:31:13-07:00)
auditor_session: fresh auditor subagent in /Users/seanpharris/oversight-testbed-audit-em-gm2q (no chat or transcript read)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 07:39 America/Denver
claims_checked: 20
holes_found: 6
overclaims_cut: 5
reproduced: true
verdict_claimed: mixed
verdict_after_audit: mixed
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: [D5, D8]
failed: true
failure_reason: Haiku failed only because the D70 wrong-target check left three questions-only cells with fewer than 2 answers (h261 O1 and O2, h112 O1). Haiku's questions-only effect is mostly large jumps on one item (h261, 88% of its between-order variance), and the check cannot tell those from rating a listed statement.
failure_kind: design
premortem_score: kind_only
risk_seen: null
---

# Audit of em-gm2q: question order with nothing in the transcript but questions

## In plain English

The pre-registered verdict, **mixed**, stands. The tables regenerate byte for byte from the archived conversations with the beacon seed. The rule was applied as frozen in the pre-registration and amended before data by D69 and D70: Sonnet passes every part of it, and Haiku fails on the wrong-target check. What does not stand is part of the write-up around that verdict. It says Haiku's fail comes from one cell, but three cells are emptied. It says "order clearly still moves the final rating" on Haiku, but D70 reads a significant raw gate alone as not settled. It says the h261 pattern "fits an order effect better than rating the wrong line", but the data fit a model rating the first- or last-listed statement just as well. It also says the main paper can claim this for "Claude models" and that on Sonnet "the gm2 order effect does not need the placeholder", when the surviving effect sits on different items and orders (pattern correlation 0.16). Five sentences must be rewritten. Sonnet's pass is real by the rule, but most of its size comes from one item (h191, 82% of its questions-only variance). If every answer more than 20 points from the usual answer is dropped from both arms, the lower bound falls to 0.47–0.49, just under the bar. That makes the next test cheap.

## The case that this result is false

The headline is that on Sonnet "with nothing in the transcript but the questions, their order still moved the final rating ... by at least half as much as answering them turn by turn". The case against it: Sonnet's questions-only order effect is mostly one cell. In h191 order O3, 7 of 10 answers sit at 85–97 against a usual answer of 3. That cell alone gives h191 a questions-only effect of 29.7 points against 0.0 turn by turn, which is 82% of Sonnet's questions-only between-order variance. The 4th-listed statement in that cell is rated 84 ("The writer's recall of Ig Nobel winners by year is imperfect"), so those 7 answers look like the model rating the wrong line. They are the very artefact the D69/D70 check was added to stop. The rule removes flagged answers only from the permutation gate. R itself is computed on the raw ratings, so the flagged answers inflate R to 1.88. Without the jumps the effect is ordinary in size and sits on different items from the turn-by-turn one: the order patterns correlate at 0.16, and the largest turn-by-turn item, h058, is not where the questions-only effect lives. A ratio of two order-effect magnitudes that do not share items or orders does not show that "the gm2 order effect" survives. It shows that some order effect of comparable size exists, carried by a few large jumps. On Haiku the same story is stronger: h261 carries 88% of the questions-only variance, through answers of about 90 when the statement Haiku rates 99 ("A total lunar eclipse occurred on November 8, 2022") is listed first or last, and about 5–12 when it sits in the middle. A model rating an end-of-list line would produce exactly that. On this reading the bet has shown that one-message prompts produce occasional large wrong-line answers whose position depends on order, and not that the questions alone build the judgment. If that is right, R ≥ 0.5 on Sonnet is a magnitude coincidence driven by one item.

The checklist below tests this. It holds in part. Sonnet's pass survives every leave-one- and leave-two-items-out drop (lower ends ≥ 0.68), survives the pre-registered cleaned gate, and survives cleaning the end-of-list wrong-target answers (R 0.78 [0.68, 1.37]). So the verdict stands under the rule. But the case is right about the write-up: the effect is not the turn-by-turn one, its size rides on one item per model, and the mechanism sentences say more than the design can.

## Claims checked

| # | claim (quoted or paraphrased) | check run | outcome |
|---|---|---|---|
| 1 | Tables generated by `--analyse --seed 17882636728661590601` | re-ran into scratch with paths redirected (as reproduce.py's gm2q step); `cmp` against both committed files | holds: tables .md and .json byte-identical |
| 2 | "2,000 conversations, $2.80 ... no refusal, no missing answer" | cache: 2,000 keys, 0 `_lost|`, 0 missing, 0 None ratings; cost sum $2.80125 (Haiku $0.2329, Sonnet $2.5683) | holds |
| 3 | qonly gate p = 0.0002 on both, "smallest p the test can give" | JSON; 1/5001 | holds |
| 4 | OE 15.5 vs 9.0 (Haiku), 10.4 vs 5.5 (Sonnet) | JSON | holds |
| 5 | "On both models ... order clearly still moves the final rating" | D70 fix 3(c); cleaned gate on Haiku | **hole**: on Haiku this is the case D70 reads as "not settled"; one item carries 88% / 82% (cut 2) |
| 6 | Sonnet R = 1.88 [0.75, 8.38]; passes; no single item decides it | JSON; LOO; leave-two-out; 200 bootstrap seeds | holds (LOO lower ends 0.73–0.77; leave-two-out minimum 0.68; lower end 0.746–0.757 across seeds) |
| 7 | Sonnet without h191: 0.80 [0.73, 1.36] (exploratory) | `gm2q_explore.py` | holds, labelled exploratory |
| 8 | Haiku R 1.73 [0.50, 4.99]; lower end 0.505 clears 0.5 | JSON 0.50497; 200 bootstrap seeds: median 0.507, 1% below 0.5 | holds (sits at the edge; irrelevant to the label) |
| 9 | "in one cell (item h261, order O2) all 10 answers were flagged ... which leaves too few to test" | recomputed cleaned cells | **hole**: three cells keep fewer than 2: h261 O2 (0), h261 O1 (1), h112 O1 (1). Any one of them fails Haiku (cut 1) |
| 10 | h261 O2: 4th statement rated 99, answers 90–97; O1: 9 of 10 flagged, 4th rated 12, usual 9 | `gm2q_explore.py` D lines | holds |
| 11 | "That pattern fits an order effect better than rating the wrong line" | statements by position for h261 | **hole**: high exactly when the 99-rated statement is 1st (O1) or 4th (O2); O1's ~90 is also 100 − 12, the rating of the last line "The answer is not November 8, 2022". A first-or-last-line responder fits as well (cut 3) |
| 12 | h112: flag removed "ordinary answers of 35–40 against a usual 68" | D lines | partly: O1's flagged answers are 35–40, O4's are 35–45 (folded into cut 3) |
| 13 | Haiku with the two affected items set aside: 0.80 [0.66, 0.95] | explore B | number holds; it also drops the 2 flagged answers in the other 8 items (wording folded into cut 3) |
| 14 | "The main paper can say: question order moves Claude models' answers ..." | scope: two models, 10 items, one wording; Haiku failed | **hole**: scope drift and an unreplicated one-model pass stated as general (cut 4) |
| 15 | "On Sonnet ... the gm2 order effect does not need the placeholder" | pattern correlation; per-item OE; VC shares | **hole**: the surviving effect is a different one (r = 0.16; 0.37 without h191; 82% on h191, where the turn-by-turn effect is 0); gm2 is the Haiku experiment (cut 5) |
| 16 | Pattern correlation 0.04 / 0.16; h261 46 vs 4; h191 30 vs 0; largest turn-by-turn h112, h058 | JSON per-item | holds |
| 17 | Sonnet h191 O3: 7 of 10 near the 4th statement (84) | explore D | holds |
| 18 | Redacted today OE 11.6 (gm2 16.7), R 1.29 [0.66, 3.29]; qonly/redacted 1.33 [0.47, 1.64] | JSON; gm2 date from D37 (2026-11-04) | holds |
| 19 | LOO: no single item flips either label; Haiku lower ends 0.48–0.72 | JSON; code read | numbers hold. **Hole in code**: the LOO cleaned gate uses the 10-item `clean_ok`, not the 9-item one. With these data it changes nothing (dropping h261 still leaves h112 O1 with 1; dropping h112 leaves h261) |
| 20 | Exploratory list (3.0% / 0.3%; 8 items kept; Haiku without h261 0.60 [0.48, 0.91]; flagged cells) | `gm2q_explore.py` run | holds |

## Checklist

**A. Pre-registration**

- **A1. holds, with a limit.** Pre-registration `2f30696` at 06:33:22 (author date). The design-review fixes D69 (`a548fae`, 07:02:00) and D70 (`d78475d`, 07:10:21) both state "No API call has been made". Confirmed go `6a17968` at 07:13:24. The cache was first committed at `bbf5b71` (07:29:50). `gm2q_questions_only.py` was not changed after `d78475d` (`git log 2f30696..HEAD -- experiments/gm2q_questions_only.py`). Limit: neither the cache nor `gm2q-run-log.txt` carries wall-clock times, so the record does not say when the first call ran. Its order relative to the go rests on commit order alone. I record this as *cannot check precisely* and recommend timestamps in run logs, not a hole.
- **A2. holds.** Statistic (gm2's VC/OE estimator), gates (5,000 permutations, p = (1 + #)/5,001), R with 2,000 item-bootstrap resamples, seed offsets +1/+2/+3/+4/+5 (+6 for the cleaned gate, D69), budget $3.50 with $0.10 reserve, 90% usable rule, and tolerance 1e-9 all match `2f30696` §2–§5 as amended by D69/D70. Both rows are dated before any call. The pre-registration file changed only in the seed line (`1ba7f8c`).
- **A3. holds.** D69/D70 only tighten: they add the cleaned gate and narrow the sentences. The 0.5 bar and α = 0.05 are unchanged. Odds 0.15 → 0.10 were revised before data with both kept (D69; `38f59a2`).
- **A4. holds.** The reported primary is R with its gates. The verdict line is the code's `bet_verdict` and `sentence_key` output (`mixed`).

**B. Is the number real?**

- **B5. holds.** Ratings are integers. The permutation count uses `>= T − TOL`, which is conservative. Both qonly gates are at the floor (no permuted statistic reached T), so no tie decides them. R's bootstrap: lower end 0.746–0.757 (Sonnet) and 0.499–0.516 (Haiku) over 200 seeds. Haiku's label does not depend on it.
- **B6. holds.** One scale direction. Models are never pooled. OE pools items by design (pre-registered).
- **B7. hole (write-up), verdict unaffected.** One item carries 88.1% of Haiku's questions-only between-order variance (h261) and 82.1% of Sonnet's (h191). Without them the questions-only effect is 0.60× (Haiku) and 0.80× (Sonnet) of turn by turn, not 1.7–1.9×. Sonnet still passes: leave-one-out lower ends ≥ 0.73, leave-two-out ≥ 0.68 (worst pair h058 + h221). The results file reports the Sonnet number in plain English but gives Haiku's 0.60 and both shares only in the exploratory list, or not at all, under a headline bullet that leads with 15.5 vs 9.0 and 10.4 vs 5.5 (cut 2). Also a code hole (claim 19): the leave-one-out cleaned gate does not recompute `clean_ok` on the 9 remaining items. No label changes here.
- **B8. holds.** The flag uses today's shown sub-ratings and shown final means. Shown is R's denominator, but the flag feeds only the gate, not R. Nothing is fitted.
- **B9. holds, with a sensitivity.** The qonly permutation gate is the shuffled control (P3), and the dry run shows the null world never passes. Auditor's re-analyses of the wrong-target cleaning (exploratory):
  - dropping answers nearer the 1st or 4th statement than the usual answer (and > 20 from it) gives Sonnet R 0.78 [0.68, 1.37], a pass;
  - dropping answers nearer any listed statement, from qonly only, gives Sonnet 0.66 [0.39, 1.37];
  - dropping them from both arms gives 0.83 [0.49, 1.39];
  - dropping every answer > 20 points from the usual one in both arms gives 0.82 [0.47, 1.34].
  So Sonnet's margin over the bar holds under the pre-registered and end-of-list cleanings. A symmetric trim of all large jumps takes it to just under 0.5. That is not the rule, but it is the cheapest place the result could break (see the last section).
- **B10. holds.** Intervals are by item bootstrap (10 items), not by call. Haiku's lower end, at the edge, is reported to three decimals.
- **B11. holds.** Per model the rule is an intersection of three gates and one interval, and both models are required. The pre-registration states no correction and why. Exploratory checks are labelled and listed separately.
- **B12. holds.** No fitting step; no outcome reaches a selection step.

**C. Write-up**

- **C13. hole.** "The main paper can say: question order moves Claude models' answers with no answers or stand-in in the transcript" names "Claude models" from two models, one of which failed the rule (cut 4).
- **C14. hole.** "On both models, with only questions in the conversation, order clearly still moves the final rating" promotes Haiku's raw gate. D70 pre-registered exactly this case (raw gate significant, cleaned gate failing) as "whether the questions alone move the judgment is not settled by this test" (cut 2).
- **C15. hole, twice.** (a) "That pattern fits an order effect better than rating the wrong line": the design cannot separate these, and the auditor's reading of h261's statement positions fits a first-or-last-line responder equally well (cut 3). (b) "On Sonnet ... the gm2 order effect does not need the placeholder": the design measures magnitude only. The surviving effect has a different item and order pattern (r = 0.16), so "the gm2 order effect" is a noun the data cannot carry (cut 5). The file's own caveat ("it does not leave the same one") contradicts the sentence.
- **C16. hole.** The plain English says Haiku's fail is one cell; it is three (cut 1). The table cell "not computable (h261 O2 kept 0 of 10)" names one of the three. Every other number in the plain English matches the tables or the exploratory script (claims 2–4, 6–8, 10, 16–18, 20).
- **C17. holds.** gm2b's "largely different one" (`results/gm2b-self-conditioning-40.md`) supports "gm2b found the same with the stand-in". gm2's 4 November date matches D37. D69/D70 say what the file cites them for.
- **C18. holds, narrowly.** Haiku's fail is stated in bold and the verdict is mixed, scored 0. The "Read this fail carefully" paragraph argues against the fail at length, while Sonnet's pass gets only a caveat bullet on h191. Cuts 1 and 3 rebalance this.

**D. Process**

- **D19. holds.** Cap in code: `spent_of(cache) + RESERVE >= CAP − TOL` before each conversation. Spend $2.8012 of $3.50, reported.
- **D20. holds.** No refusal file and no `_lost|` keys. The stop flag is checked before every call; `run()` exits if the refusal record exists. Nothing retried.
- **D21. holds.** The anchor "0 = certainly false, 100 = certainly true" is in every opening (`--print-prompts` asserts that the openings match `exp5_run`, and it ran clean).
- **D22. holds.** The bet is mixed, not a hit. Sonnet's pass is one model, one item set, one wording, and the write-up's scope bullet says so. Cut 4 removes the one sentence that generalises it.

**E. Engine records**

- **E23. holds.** CURBy-RNG pulse 1592278 is at 2026-11-05T13:34:00.185Z (06:34:00 MST), after the pre-registration at 13:33:22Z. The previous pulse 1592277 is at 13:33:00.179Z, before it, so 1592278 is the first after the commit. Its randomness matches the seed line. `ledger/seed.py <randomness> em-gm2q --purpose analysis` gives 17882636728661590601, mod 2^63 8659264691806814793, the value `--analyse` asserts and the tables print. The seed commit `1ba7f8c` changes only the seed line. The archives read for the dry run (gm2, em-dm4) were not changed in the range. CURBY-Q is recorded as stalled (round 28297).
- **E24. not applicable** (not a tiebreak bet).
- **E25. holds.** The §0 lesson row is in `2f30696`. `ls-em-gm2q` in `ledger/lessons.jsonl` has the same sentence. Its `read` block (26 resolved, Brier 0.217, base rate 0.32 = 9/28, newest audit `ta-b1r2.md`) matches `ledger/brier.md` at `2f30696` and the newest audit file at that commit (ta-b1r2, 06:31:14). P8's `do_this` (list every difference) is in §6 and D69 fix 2. P3's (beat the dumbest predictor) is the qonly gate. The odds change 0.15 → 0.10 is a revision before data (D69, `38f59a2`).
- **E26. holds, with misses.** The review is `ledger/design-reviews/em-gm2q.md`: fix-first `927cdb4` (06:58), confirmation 1 not confirmed (`22d1cce`), confirmation 2 go (`6a17968`, 07:13:24). It came after the pre-registration and before the data commit, and every fix is in D69/D70, written before any call. Flaws the review should have caught:
  - **D5:** the wrong-target responder was named only for the last-listed statement. A model rating the first-listed line, the other end of a list that ends in the question, is just as dumb a responder. The D70 flag catches it only by coincidence, and h261's data have exactly that shape.
  - **D8:** the pass and mixed sentences use the noun "the gm2 order effect", but R compares magnitudes only. The review itself wrote "a pass needs the effect on the same items" (its lines 175, 241, 321), and Sonnet's pass, with pattern r = 0.16 and 82% of its variance on an item with no turn-by-turn effect, shows that claim false. The shuffled-items world was simulated only at 1.0× and 1.5×, while one large jump can make the ratio 1.9×.

## The pre-mortem, scored

My own account, written before reading it: Haiku failed because the D70 wrong-target check left three questions-only cells with fewer than 2 answers. Its questions-only effect is mostly large jumps on one item, which the check cannot tell from rating a listed statement. Kind: **design**.

The pre-mortem (`2f30696` §0): "If this fails, the most likely reason is that with all four statements in one message the model reads them as one list and its final rating stops depending on their order, though the questions mattered turn by turn." Kind: `design`.

Score: **kind_only**. The bet failed for a design reason, as the pre-mortem's kind says, but not by its mechanism: the questions-only rating did depend on order on both models (gate p = 0.0002, OE 15.5 and 10.4). It failed on Haiku because a check could not tell big order-driven jumps from rating the wrong line.

## Required cuts

1. **Plain English, "Haiku fails ..." bullet.** Replace "But in one cell (item h261, order O2) all 10 answers were flagged as wrong-target, which leaves too few to test. The rule, fixed before any data, counts that as a fail." with: "But in three cells the check leaves fewer than 2 answers: h261 O2 (0 of 10 kept), h261 O1 (1 kept) and h112 O1 (1 kept). The rule, fixed before any data, counts any one of them as a fail." In the pre-registered reading table, replace "not computable (h261 O2 kept 0 of 10)" with "not computable (h261 O2 kept 0, h261 O1 and h112 O1 kept 1 each)".

2. **Plain English, first bullet.** Replace "**On both models, with only questions in the conversation, order clearly still moves the final rating.** The questions-only order effect is significant on each (permutation p = 0.0002 on both, the smallest p the test can give)." with: "**With only questions in the conversation, the raw order gate is significant on both models** (permutation p = 0.0002 on both, the smallest p the test can give). On Sonnet it stays significant with the flagged answers dropped. On Haiku that cleaned gate cannot be computed, which is the case D70 reads as not settling whether order moves the judgment or the model is rating a listed line. One item carries most of each effect: h261 holds 88% of Haiku's questions-only between-order variance and h191 holds 82% of Sonnet's. Without that item the questions-only effect is 0.60 (Haiku) and 0.80 (Sonnet) times the turn-by-turn one." Keep the sentence that follows ("It is 15.5 points on Haiku ...").

3. **"Read this fail carefully" paragraph.** Replace "That pattern fits an order effect better than rating the wrong line. In item h112, the flag also removed ordinary answers of 35–40 against a usual 68." with: "That pattern does not show the model rating the 4th line, but it fits a model rating whichever line comes first or last just as well. In O1 the first statement is the one rated 99, and Haiku's ~90 is also 100 minus the 12 it gives the last statement ('The answer is not November 8, 2022'). The design cannot tell these from an order effect on the judgment. In item h112, the flag also removed answers of 35–45 against a usual 68, inside the range Haiku gives turn by turn (its O2 mean is 34)." In the same paragraph, replace "With the two affected items set aside (exploratory, not the rule), Haiku's ratio is 0.80 [0.66, 0.95]." with "With the flagged answers dropped and the two items that then lose a cell set aside (exploratory, not the rule), Haiku's ratio is 0.80 [0.66, 0.95]."

4. **"What it means" paragraph, last sentence.** Replace "The main paper can say: question order moves Claude models' answers with no answers or stand-in in the transcript (pass on Sonnet; on Haiku the order effect was significant but the pre-registered rule failed on its wrong-target check)." with: "The main paper can say: on claude-sonnet-5-5, on these 10 items and this wording, question order moved the final rating with no answers or stand-in in the transcript, by the pre-registered rule (pass, unreplicated). On claude-haiku-5-5 the raw order gate was significant, but the pre-registered rule failed on its wrong-target check."

5. **"What it means" paragraph, first sentence.** Replace "On Sonnet, by the full pre-registered rule, the gm2 order effect does not need the placeholder: with nothing in the conversation but questions, order still moved the answer by at least half as much as turn by turn." with: "On Sonnet, by the full pre-registered rule, an order effect at least half the size of the turn-by-turn one remains with nothing in the conversation but questions. It is not the same effect: it sits on different items and orders (pattern correlation 0.16), and 82% of it is one item, h191, where turn by turn there is none. So this shows that removing the placeholder does not remove order effects. It does not show that the turn-by-turn effect itself survives. The design review's statement that a pass needs the effect on the same items (D69) did not hold for this pass."

## What would break it next

The cheapest overturn is of Sonnet's margin, not the rule. If every answer more than 20 points from the usual answer is dropped from both arms, Sonnet's R lower end is 0.47–0.49 (exploratory, above). So the pass rests on a few large jumps, and on whether they are judgments or a rated line.

Candidate bet **gm2q-f1**, a line-identification arm with no other change. Re-run Sonnet and Haiku qonly on the same 10 items × 4 orders × 10 repeats with the schema `{"line": integer, "rating": integer}`, asking which numbered line the rating answers. Pre-register:
- pass if the share of answers naming line 5 is ≥ 95% in the cells the flag fired on (h191 O3, h261 O1/O2, h112 O1/O4), and the qonly gate, restricted to line-5 answers, keeps p < 0.05 with R's lower end ≥ 0.5.
- Cost about $0.48 (Sonnet qonly 400 × ~$0.0012; Haiku qonly 400 × ~$0.00006), using today's archived shown chains as the reference.

A second, larger test, about $0.70 on Haiku (qonly about $0.07, same-day shown and redacted about $0.31 each, scaled from this run's costs): run qonly on gm2b's 30 further items, where the Haiku shown and redacted archives already exist. It would show whether the questions-only effect is a few-item phenomenon or spreads across items as gm2b's redacted effect did.

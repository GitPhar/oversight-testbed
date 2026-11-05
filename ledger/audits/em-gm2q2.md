---
bet: em-gm2q2
program: entangled-mind
prereg_commit: 1e0c9c1
results_commit: a040690            # the audit clone's re-commit of the results commit (author time 2026-11-05T11:13:19-07:00)
auditor_session: fresh auditor subagent in /Users/seanpharris/oversight-testbed-audit-em-gm2q2 (no chat or transcript read)
auditor_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 11:22 America/Denver
claims_checked: 24
holes_found: 3
overclaims_cut: 4
reproduced: true
verdict_claimed: null            # the pre-registered label is "fail" (§5: both models testable, neither passes); the template has no "fail", so it is entered as null = predicted event absent (convention of om-p2-6r, ng-p3-16, sg-b2)
verdict_after_audit: null        # fail
verdict_stands: true
canary: unknown
false_alarms: 0
design_review_missed: [D8, D3]
novelty_checked: missing         # not required: a fail needs no Novelty line (CONTEXT §3 rule 13(c)); F27 not applicable
novelty_holds: true              # nothing to contradict: the write-up claims no novelty (its one "finding" sentence is cut under C14)
novelty_search: not run (F27 not applicable to a fail)
failed: true
failure_reason: Opus failed because its turn-by-turn yardstick rests on two items (h058, h279: 97% of its order variance), and h058 also carries its questions-only gate; Sonnet failed because its questions-only answers sat 20-40 points from turn by turn on a few mid-scale items, in level and in pattern, so the wrong-target check emptied 10 cells. Kind design.
failure_kind: design
premortem_score: named
risk_seen: null
---

# Audit of em-gm2q2: question order with only questions in the message, on Opus and on Sonnet's 30 new items

## In plain English

The pre-registered verdict, **fail**, stands. The tables and JSON regenerate byte for byte from the archived conversations with the beacon seed. The seed recomputes, and the rule was applied as frozen, with D82's changes (Opus 6 → 4 repeats, cap $4.00 → $4.25) made before any call. Neither model meets the rule. Opus breaks on leave-one-item-out. Sonnet breaks on the wrong-target check, which left 10 cells with fewer than 2 answers.

Four sentences around the verdict say more than the data allow:
- The write-up calls a secondary correlation "the bet's main finding" and says it shows Opus's questions-only effect is "the same effect as turn by turn". The pre-registered pass sentence says the design cannot show that.
- Twice it says Opus's leave-one-out failure was the yardstick's and "not the questions-only effect". Without h058, the questions-only gates fail too: p = 0.126 raw and 0.138 cleaned.
- It says much of Sonnet's effect "lands on answers that could be ratings of the first or last statement". Aimed at the middle two statements, the same check flags more answers (13.5% against 9.8%, 11 cells against 10). 40 of the 59 flagged answers sit nearest a middle statement.

What would break the Sonnet reading next costs nothing: a pre-registered version of the check that compares listed positions, so it can tell rating a listed line apart from answering at a different level.

## The case that this result is false

The headline is "fail: neither Opus nor Sonnet met the rule". The strongest case against it is that the fail comes from parts of the rule that do not measure what they are named for. On that reading, a fair test of the bet's question would have come out differently on at least one model.

**Opus.** On all 10 items, Opus clears every part of the rule:
- turn-by-turn gate p = 0.016;
- questions-only gate p = 0.0006, unchanged by the wrong-target check, which flags nothing;
- R = 1.26 [0.68, 3.02].

It fails only because, with h058 or h279 left out, the *turn-by-turn* gate loses significance (p = 0.089 and 0.071). Opus sits within 3 points across orders on five of the ten items in both arms. Four repeats per cell on 10 items cannot keep a yardstick significant once one of its two moving items is gone. So this is a power failure of the reference arm, and it says nothing about whether questions alone move the rating.

**Sonnet.** Both gates are at the floor (p = 0.0002). R = 0.94 [0.63, 1.34]. With the wrong-target check ignored, leave-one-item-out has no breaker on any of the 30 items. The only thing that sinks Sonnet is the check, and the check is not specific to what it is named for:
- Aimed at the second- and third-listed statements instead of the first and last, it flags more answers (13.5% against 9.8%) and empties more cells (11 against 10).
- It also fires on plain level differences. Take Sonnet's own turn-by-turn order pattern, at full size, shift each item by the observed questions-only − turn-by-turn level difference, and the check empties 10 cells.

So on Sonnet the check flags "far from turn by turn", not "rating a listed line". A model whose questions-only answers sit at a different level from its chain answers cannot pass it, whatever its order effect.

On this argument, Sonnet shows a questions-only order effect about as large as turn by turn, spread across items and robust to leaving any one out, and the "fail" is the check's doing.

**What the checklist finds.** The verdict stands by the frozen rule, so the case is wrong about the verdict. It is right about the interpretation. The Opus fail is not only the yardstick's: h058 carries 78% of the questions-only effect, and without it the questions-only gates fail too. The Sonnet fail cannot be read as answers sitting on the first- or last-listed statement. Three holes and four cuts follow from that.

## Claims checked

| # | claim (quoted or paraphrased from the results file) | check run | outcome |
|---|---|---|---|
| 1 | 1,520 conversations; no refusal, no missing answer | cache: 160 + 160 Opus, 600 + 600 Sonnet; 0 missing; 0 refused; 4,560 unique message IDs; no `refusal-gm2q2.md` | holds |
| 2 | $3.83 of the $4.25 cap | `spent_of` = $3.8298; `_unfinished` 0, `_lost_prior` 0 | holds |
| 3 | pre-registered fail sentence, first failing parts Opus leave-one-item-out, Sonnet wrong-target | regenerated JSON `first_fail`; sentence matches §5 verbatim | holds |
| 4 | Opus: shown p = 0.016, qonly p = 0.0006, unchanged with the flag (no answer flagged) | regenerated: 0.0160, 0.0006, cleaned 0.0006; qonly flag share 0.0% | holds |
| 5 | Opus OE 4.3 vs 3.4, R 1.26 [0.68, 3.02] | 4.31 / 3.41; 1.264 [0.681, 3.022] | holds |
| 6 | "The bet's main finding is on Opus: ... the same effect as turn by turn, on the same items and orders (pattern correlation 0.63)" | r = 0.63 reproduces; item bootstrap [0.49, 0.81]. It is a §4 secondary. The pass sentence says the design "does not show that it is the same effect". h238 has shown OE 0.0 against qonly 3.8; h058's O4 goes the other way (58 against 72) | **overclaim** (C14, C15) |
| 7 | on 5 of 10 items Opus's order means move < 3 points in both versions | h190, h101, h112, h191, h221 (ranges ≤ 2.25) | holds |
| 8 | nearly all of the turn-by-turn effect is h058 and h279; not significant with either left out | 96.6% of the shown variance component; leave-one-out shown p 0.089 / 0.071 (seeds 100–129: 0.080–0.097 / 0.069–0.081) | holds |
| 9 | h058 holds 78% of the questions-only effect | 78% | holds |
| 10 | "it was the turn-by-turn yardstick that broke without them, not the questions-only effect" | without h058: qonly p 0.126, cleaned 0.138 (seeds: 0.128–0.146), R 0.87; without h279: qonly p 0.0008, cleaned 0.0012, R lo 0.85 | **wrong for h058** (C16) |
| 11 | caveat: "The leave-one-out sets that broke failed on the turn-by-turn gate, not on the questions-only parts." | as #10. `label_on` records only the first failing part, and checks the shown gate first | **wrong for h058** (C16) |
| 12 | Sonnet both gates p = 0.0002; OE 6.0 vs 6.4; R 0.94 [0.63, 1.34] | 0.0002 / 0.0002; 6.02 / 6.37; 0.944 [0.632, 1.342] | holds |
| 13 | Sonnet not concentrated: largest share h214, 37% | 37% | holds |
| 14 | Sonnet pattern correlation 0.04 | 0.040; item bootstrap [−0.36, 0.50]; null with qonly labels shuffled [−0.40, 0.38] | holds (no interval given) |
| 15 | flag 9.8% of qonly vs 2.3% of shown; 10 cells on 5 items, h115 and h214 in three orders each | 9.8% / 2.3%; h135 ×1, h115 ×3, h214 ×3, h019 ×2, h294 ×1 | holds |
| 16 | "the questions-only effect is a different effect from the turn-by-turn one, and much of it lands on answers that could be ratings of the first or last statement" | placebo flag on 2nd and 3rd statements: 13.5%, 11 cells. Nearest listed position of the 59 flagged answers: 10 / 22 / 18 / 9. Level-adjusted rule flag: 5.8%, 2 cells (h214 O1, O3). Level-shifted copy of Sonnet's own shown pattern: 10 cells | **overclaim** (C15) |
| 17 | Sonnet level differences on h115 and h294 (means quoted) | h115 60, 86, 68, 34 against 10, 40, 30, 15; h294 69, 72, 53, 55 against 36, 48, 21, 40 | holds |
| 18 | a reader who dropped the check and leave-one-out would see a questions-only effect on both | raw gates 0.0006 / 0.0002. Dropping only the check, Sonnet's leave-one-out has no breaker | holds |
| 19 | timing: qonly from round 1, shown finals from round 5, about 15 minutes later | batches log: rounds 2–5 took 917 s of processing; every qonly record is in round 1's batch and every shown record's 5th turn in round 5's | holds |
| 20 | "most of gm2b's 30 items sit near 0 or 100 for Opus, if em-dm2's formats are a guide" | em-dm2 archive not opened; hedged aside in a caveat | cannot check |
| 21 | "This is the case the pre-registration said the rule would now treat as not separated" (§6) | prereg §6 at 1e0c9c1 says this. D82 withdraws that paragraph's *reason* ("only its stated reason goes"), and the review asked to keep the cost sentence | holds (D82 is ambiguous) |
| 22 | Opus's leave-one-out sentence "the effect depended on single items (h058, h279)" | §5 table sentence, verbatim | holds as the frozen sentence; see #10 |
| 23 | the table row (labels, breakers, "not run" for Sonnet) | regenerated tables | holds |
| 24 | scored as a miss at engine odds of 7% | ledger inbox row 3: engine_odds 0.07 (revised before data, D82) | holds |

## Checklist

**A. Was it pre-registered as claimed?**

1. **Holds; the first call's minute cannot be checked.** Commit author dates (`git log --format=%aI 1e0c9c1~1..HEAD`), all 2026-11-05:

   | time | commit | what |
   |---|---|---|
   | 10:20:43 | 1e0c9c1 | pre-registration |
   | 10:22:04 | 74b63b1 | seed |
   | 10:36:45 | 65c4365 | design review, fix-first |
   | 10:47:28 | 089eebd | D82 fixes; the last change to the code |
   | 10:52:57 | fe408fc | review confirmed, go |
   | 10:57:04 | c43c4aa | review addendum, "after the run started" |
   | 11:11:53 | 0d60004 | data |
   | 11:13:19 | a040690 | result |

   - The five batches took 1,080 s of processing (`gm2q2-batches.json`), so the run started no later than about 10:53:50. That is consistent with starting after the go.
   - The run log and message IDs carry no clock times, and the clone's file mtimes are its own. So "first call after 10:52:57" is consistent with the record but not provable from it.
   - The only earlier paid calls were the design review's 12-call pilot ($0.0703), on gm2b items not in the Opus arm.
   - The result commit follows the data commit by 86 s, so the analysis and write-up were done before the data commit, despite its "Not yet analysed". There is no consequence: the code was frozen at 10:47 and the analysis regenerates exactly.
2. **Holds.** The pass rule, statistics, offsets, split and verdict sentences are unchanged since 1e0c9c1 (`git diff 1e0c9c1 HEAD`): the only edits to the frozen file are D81's time correction and the seed line. Repeats (Opus 4) and cap ($4.25) differ from the frozen text through D82, dated before any call (089eebd, 10:47).
3. **Holds.** No bar moved. D82 changed the budget, the repeats, the dry run and the prior-work text. §5 is unchanged, and `ALPHA`, `BAR` and `WT_FAR` are imported unchanged from em-gm2q.
4. **Holds.** R is reported as the primary, inside the per-model rule.

**B. Is the number real?**

5. **Holds.** Ratings are integers, and the permutation statistic is Σ MS_between with ties at T counted against the result (conservative). The gates are stable across 30 other permutation seeds:
   - Opus full-set shown gate: 0.0108–0.0156.
   - Opus leave-one-out shown gate: 0.080–0.097 without h058, 0.069–0.081 without h279.
   - Sonnet: 0.0002 throughout.

   No count depends on tie-breaking.
6. **Holds.** Nothing is pooled across models or conditions. The flag's statement reference pools the four orders' sub-ratings of a statement, as frozen.
7. **Holds, and the write-up says it.** Opus rests on h058 and h279 (96.6% of the shown variance; h058 is 78% of the qonly variance). Sonnet's empty cells sit on 5 items. Leave-one-out is in the rule. But see C16 for what the write-up says each breaker broke.
8. **Holds.** The flag uses shown means to clean qonly answers; nothing tested is fitted on itself.
9. **Hole (feeds C15).** The wrong-target check is the "second dumb baseline", but it has no control for its own specificity. My re-analysis is at `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed-p1-wave3/64dc560a-a9b5-47cc-a2a7-ed6060948ca4/scratchpad/re/reanalyse.py` and `/private/tmp/claude-501/-Users-seanpharris-oversight-testbed-p1-wave3/64dc560a-a9b5-47cc-a2a7-ed6060948ca4/scratchpad/re/levelworld.py`. On Sonnet:

   | flag aimed at | qonly answers flagged | cells left below 2 |
   |---|---|---|
   | 1st + 4th listed (the rule) | 9.8% | 10 |
   | 2nd + 3rd listed (placebo) | 13.5% | 11 |
   | any of the four | 14.2% | 11 |

   - Of the 59 answers the rule flags, the nearest statement is listed 1st for 10, 2nd for 22, 3rd for 18 and 4th for 9.
   - Removing each item's level difference before flagging leaves 5.8% flagged and 2 empty cells (h214 O1, O3).
   - Sonnet's own shown pattern, shifted by the observed item levels, empties 10 cells.

   The check identifies answers far from turn by turn; it does not pick out the first or last line. That does not move the verdict, because the check is frozen and fires either way. It does sink the write-up's mechanism sentence (cut 4).
10. **Holds, with a note.** R's intervals are item-bootstrap. The pattern correlations are quoted without intervals: Opus 0.63 [0.49, 0.81], Sonnet 0.04 [−0.36, 0.50]. That matters only for cut 1.
11. **Holds.** There are two models, each read on its own rule, and the bet needs both. Requiring both and every leave-one-out set is stricter than either alone, as §4 states.
12. **Holds.** No test outcome reached a fitting step. The dry run read published archives only: em-dm4's Opus chains and gm2b's Haiku chains.

**C. Does the write-up say only what the data say?**

13. **Holds.** Scope is stated: two models, one pool, one wording; "Every", "all" and "models" are not claimed.
14. **Hole.** "The bet's main finding is on Opus: unlike em-gm2q, the questions-only effect is the same effect as turn by turn, on the same items and orders (pattern correlation 0.63)."
    - The pattern correlation is a §4 secondary ("reported, never promoted"), on a model whose label is fail.
    - Calling it the bet's main finding promotes it.
    - This is P9 recurring, the pattern this bet's own lesson was written to correct: the right rule, then the wrong noun.
15. **Hole (two sentences).**
    - (a) "Same effect" is the noun §5's pass sentence rules out ("it does not show that it is the same effect as turn by turn"). An r of 0.63 on 40 order deviations, 97% of whose shown variance component is h058 and h279, does not establish identity. h238 moves in qonly (OE 3.8) and not at all in shown (0.0).
    - (b) "the questions-only effect is a different effect from the turn-by-turn one, and much of it lands on answers that could be ratings of the first or last statement" (Sonnet). The first half reads r = 0.04 as a positive claim of difference. The second names a mechanism the placebo in B9 does not support: the flagged answers sit nearer the middle statements more often than the end ones, and level differences alone empty the cells.
16. **Hole.** Two sentences are contradicted by a recomputation of the frozen rule's parts:
    - The verdict paragraph: "it was the turn-by-turn yardstick that broke without them, not the questions-only effect."
    - The caveat: "The leave-one-out sets that broke failed on the turn-by-turn gate, not on the questions-only parts."

    With h058 left out:
    - qonly gate p = 0.126 and cleaned gate p = 0.138, both failing;
    - qonly OE 2.13 against shown 2.45.

    With h279 left out, the questions-only parts do hold (p = 0.0008, cleaned 0.0012, R lower bound 0.85).

    The code's `loo_break_parts` names only the first failing part. `label_on` checks the shown gate first and returns "untestable" before looking further, so it cannot say the other parts held. The sentences are true for h279 and false for h058, the item that carries 78% of the questions-only effect.

    Every other plain-English sentence matches the table (claims 1–5, 7–9, 12–15, 17–19, 23–24).
17. **Holds, one cannot check.**
    - The results file cites only the record: the prereg §6 and §8, D80–D82, em-gm2q. §6's "the rule now treats it as not separated" is in the frozen text; D82 withdrew that paragraph's stated reason, and the review asked to keep the cost sentence.
    - The em-dm2 aside (claim 20) was not checked.
18. **Holds.** The fail is the first sentence of the verdict paragraph, with the score and odds; the raw-gate caveat is labelled as not the rule.

**D. Process**

19. **Holds.**
    - `CAP = 4.25` with a $0.10 reserve is checked before the first batch and before every round (`run()`); br-011 was amended to $4.25 before data.
    - Spend was $3.8298, from billed usage at the batch rate; no lost or unfinished cost.
    - The billing itself cannot be checked against Anthropic's invoice.
20. **Holds.** No refusal was recorded and there is no refusal file. Every batch succeeded on its first submission (`errored=0, expired=0`), so nothing was resubmitted.
21. **Holds.** "0 = certainly false, 100 = certainly true" is in both the qonly message and the chain opening (`gm2q_questions_only.ANCHOR`).
22. **Not applicable.** The verdict is fail.

**E. Engine records**

23. **Holds; the pulse fetch cannot be checked.**
    - `python3 ledger/seed.py 56aa7c3e…50be32 em-gm2q2 --purpose analysis` gives 8982550231960562870. That equals `SEED_RECORDED` and the seed passed to `--analyse`, which asserts it. The analysis uses only that seed's offsets.
    - The recorded pulse 1592505 is at 17:21:00.195Z, 17 s after the prereg's author time of 17:20:43Z. The previous pulse, 1592504, is recorded at 17:20:00Z.
    - I did not re-fetch either pulse: the CURBy client is not installed in the clone, and installing it was out of scope.
    - Using CURBy-RNG follows the hardware.md fallback (CURBY-Q stalled, round 28297 at 2025-08-22).
    - Nothing was drawn between the commits.
24. **Not applicable.** This is a standard bet.
25. **Holds.**
    - The §0 lesson row is in 1e0c9c1.
    - `ls-em-gm2q2` in `ledger/inbox/p1-wave3.jsonl` carries the same sentence, and its revision (D82) is kept beside it.
    - The read block (31 resolved bets, Brier 0.158, base rate 7/31, newest audit ng-p3-18) matches `ledger/brier.md` at 1e0c9c1 and the newest audit commit before it (4f07a2f, ng-p3-18).
    - The cited patterns' `do_this` (`ledger/lessons.jsonl`) are in the design. P10: leave-one-item-out is in the rule. P9: verdict sentences are pre-written in §5. P15: the dry run uses measured archives and pilot costs. Sonnet's item pattern is assumed from Haiku and stated as an assumption.
    - The odds change (0.06 → 0.07) was recorded as a revision before data.
    - P9 recurred in the write-up (C14).
26. **Holds for timing; two misses.**
    - **Timing.** `ledger/design-reviews/em-gm2q2.md`: fix-first at 65c4365 (10:36), after the prereg and before any call. Its four fixes are in D82 (089eebd, 10:47), confirmed go at fe408fc (10:52:57). Note: the go was written while the reviewer's own dry-run re-run was still going. The addendum c43c4aa (10:57, after the run started) records that it matched in every world, so nothing turned on it.
    - **D8 (verdict nouns).** The review proposed adding "(the turn-by-turn reference, not the questions-only effect)" when the shown gate breaks a leave-one-out set. It confirmed the fix as "`loo_break_parts` is recorded". But `label_on` returns at the shown gate without testing the remaining parts, so the record cannot support "not the questions-only effect". On this data that clause is false for h058, and it reached the write-up twice (C16).
    - **D3 (controls).** The review checked that the wrong-target check rejects worlds padded with first- or last-line answers. It did not check the reverse: whether the check also fires when there is no listed-line answering. It flags more when aimed at the middle statements (B9). It empties 10 cells in a world that is Sonnet's own turn-by-turn pattern shifted by the observed item levels. A questions-only arm that differs from the chain in level, which §6's bundle (one message, numbered statements, a different opening) makes likely, cannot pass on Sonnet. §6 named the different-pattern cost; the level cost was not named or simulated.

**F. Prior work**

27. **Not applicable.** Under rule 13(c), a fail needs no Novelty line, and the results file has none. The write-up's one "finding" sentence (Opus "same effect") is cut under C14 and claims no priority. No search was run.

    For the record, the prior-work row predicted "mixed": the gate passes (LLM premise-order work) and the ratio fails (Schwarz et al. 1989, survey mode). The gate passed on both models. The ratio's lower bound cleared 0.5 on both on all items (Opus 0.68, Sonnet 0.63), against the survey-mode prediction. The results file does not say this; it could, in one line.

**Reproduction.**
- `python3 programs/entangled-mind/experiments/gm2q2_opus_sonnet30.py --analyse --seed 8982550231960562870` in the clone regenerates `results/gm2q2-opus-sonnet30.json` and `results/gm2q2-opus-sonnet30-tables.md`. Both are byte-identical to the committed files (`cmp`), and `git status` was clean afterwards.
- The full `experiments/reproduce.py` could not start under system python3: `ModuleNotFoundError: qiskit`, at its `backends` import.
- So I emulated its gm2q2 step exactly: a `git archive HEAD` snapshot, paths redirected as in reproduce.py lines 178–187, `m.analyse(m.SEED_RECORDED)`. Tables and JSON matched the committed ones (`/private/tmp/claude-501/-Users-seanpharris-oversight-testbed-p1-wave3/64dc560a-a9b5-47cc-a2a7-ed6060948ca4/scratchpad/re/step.py`).

## The pre-mortem, scored

**My failure reason.** I wrote it before applying the scoring rules. It is shaped by the checklist, but note: the pre-mortem sits in the §0 table, which A2 requires reading, so I had seen its text before writing this.
- Opus failed because its turn-by-turn yardstick rests on two items (h058, h279), and h058 also carries its questions-only gate.
- Sonnet failed because its questions-only answers sat 20–40 points from turn by turn on a few mid-scale items, in level and in pattern, so the wrong-target check emptied 10 cells.
- Kind: **design**. The rule's parts were sensitive to a weak reference arm on 10 mostly floor-or-ceiling items, and to any level or pattern difference from the chain.

**Pre-mortem** (1e0c9c1 §0, kind `design`): "If this fails, the most likely reason is that the questions-only effect again sits on a different item-and-order pattern from turn by turn, so the same-order wrong-target check empties a cell."

**Score: named.** The bet needed both models, so either model's failure was enough to sink it, and the pre-mortem names one of the two exactly. Sonnet's questions-only pattern was unrelated to turn by turn (r = 0.04), and the same-order check emptied cells. That still holds with each item's level difference removed (h214 O1 and O3 still empty), so the named mechanism alone would have failed Sonnet. Opus failed by a mechanism the pre-mortem does not name (a two-item yardstick). Had Sonnet passed, this would score `kind_only`.

## Required cuts

1. **Opus bullet.** Replace "The bet's main finding is on Opus: unlike em-gm2q, the questions-only effect is the same effect as turn by turn, on the same items and orders (pattern correlation 0.63)." with:

   "As a secondary (not tested), Opus's questions-only and turn-by-turn order patterns are correlated (r = 0.63, item bootstrap [0.49, 0.81]), mostly through h058 and h279. The design cannot show that they are the same effect."

2. **Verdict paragraph.** Replace "On Opus, the effect depended on single items (h058, h279); it was the turn-by-turn yardstick that broke without them, not the questions-only effect." with:

   "On Opus, the effect depended on single items (h058, h279). Without h279 only the turn-by-turn yardstick fails (p = 0.071). Without h058 the questions-only gates fail too (p = 0.126 raw, 0.138 cleaned), because h058 carries 78% of the questions-only effect."

3. **Caveat.** Replace "**Opus's fail is about the yardstick.** The leave-one-out sets that broke failed on the turn-by-turn gate, not on the questions-only parts." with:

   "**Opus's fail is partly about the yardstick.** With h279 left out, only the turn-by-turn gate fails. With h058 left out, the questions-only gates fail as well (p = 0.126 and 0.138). The code records only the first failing part, and it checks the turn-by-turn gate first."

4. **What it means.** Replace "On Sonnet's 30 new topics, the questions-only effect is a different effect from the turn-by-turn one, and much of it lands on answers that could be ratings of the first or last statement." with:

   "On Sonnet's 30 new topics, the questions-only order pattern was unrelated to the turn-by-turn one (r = 0.04, item bootstrap [−0.36, 0.50]). On a few mid-scale topics its questions-only answers sat 20 to 40 points from its turn-by-turn answers in every order. The wrong-target check flags those answers, but it does not single out the first- or last-listed statement: aimed at the second and third statements it flags more (13.5% against 9.8%). So the record says these answers are far from turn by turn, not that they are ratings of a listed line."

   In the same paragraph, change "the order of the statements did move both models' final ratings, by the raw gates" to "the raw gates found that the order of the statements moved both models' final ratings (on Opus mostly through one item, h058)".

## What would break it next

**Free: an exploratory re-reading, not a reversal.** The verdict is fail under a frozen rule, and no re-analysis can reverse it. What can still move is the reading of Sonnet's fail.

**A new bet on Sonnet (about $1.9 at the batch rate).** Re-run Sonnet's 30 items under a pre-registered wrong-target check with two controls:
- a placebo arm that flags against the second- and third-listed statements;
- a level-adjusted arm that removes each item's questions-only − turn-by-turn mean before flagging.

Pass only if the end-position flag beats the placebo. This tells "rating a listed line" apart from "answering at a different level". If Sonnet passes there, the em-gm2q2 Sonnet fail is a property of the check, not of the model.

**The cheapest test of the Opus reading (about $1.5).** Opus on gm2b's items with mid-scale turn-by-turn answers (if any exist), so the yardstick does not rest on two items. Write it as its own pre-registration, with a pilot to find those items first.

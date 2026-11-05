---
bet: om-p2-path2
program: other-minds
prereg_commit: eaf8d1f
reviewer_session: fresh design-review subagent (om-p2-path2; the same session that reviewed om-p2-path, f561584), worktree oversight-testbed-p2-wave3 at 05d779c, no access to the author's chat
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 11:13 America/Denver
checks: {D1: holds, D2: flaw, D3: holds, D4: flaw, D5: flaw, D6: holds, D7: flaw, D8: flaw, D9: holds, D10: flaw, D11: flaw}
flaws: 7
pilot_usd: 0.00
verdict: fix-first
confirmed_at: null
---

# Design review of om-p2-path2

## In plain English
The re-bet answers the main faults of the withdrawn bet:
- a fresh session fixed the origins with one dated gate, and P9 is now coded program 1;
- there is a baseline the share must beat by 15 points;
- the scorer has real untestable paths;
- the sentences are fixed.

But the units file the scorer would read does not hold what §2 says, in four ways:
- It leaves out om-p2-5r (6 units), which was settled two minutes before the freeze.
- It includes four baseline cuts that were plants, because the plant regex misses three phrasings.
- Five units still carry optional or ledger-only text.
- The miss texts carry kind labels that differ by group: "Kind world." in program 2, "design:" and "Kind: design." in the baseline.

The baseline rule ("programs program 1 did not seed") excludes program 7 for using program 1's items and its finding. Yet it keeps program 6, whose ta-b1r2 and ta-b2 draw their items from the same program 1 pools.

Reading the units myself, without writing any tags, the 15-point gap looks reachable. But it comes mostly from how the units are made up, not from where the traps came from:
- The baseline has many more plain record fixes (miscounts, dates, counts), which carry no pattern.
- It has fewer misses, and they are labelled differently.

With 11 of 17 patterns coded program 1, almost any tag is a program-1 tag. So a tagger that never thinks about origin still gets most of the margin. The dry run assumes its tag rates instead of measuring them (P15).

All of this can be fixed before any tag without lowering the bar. The rule needs one condition that is specific to origin, and D11 has to be re-run on tag rates measured in a pilot on excluded units. If that dry run cannot show both outcomes at about 10% or more, the direction should be parked, not run.

## Checks

**D1. The rule can be applied by a stranger: holds.** I ran `score_cmd` in memory on synthetic tags. The harness is `harness2.py` in my scratchpad. It patches `TAGS` with in-memory objects, writes only to the scratchpad, and writes no tags file. Results:
- all P9 → fail (1.0 against 1.0);
- all none → fail;
- program 2 P9 and baseline none → pass;
- 11/22 against 25/74 (difference +0.162) → pass;
- 11/22 against 26/74 (+0.149) → fail;
- 10/22 against 0/74 → fail (the 0.50 bar binds).

These all return untestable, with the reason in the sentence: an empty list, lowercase `p9`, `["none","P9"]`, a missing unit, and `patterns` given as a string. The fewer-than-10 path is asserted in the dry run. Two small notes:
- A classifier B reply that fails validation is dropped without saying so (all-empty B → no `classifier_B` block, no note). It should be reported.
- A non-dict entry (`"U01": ["P9"]`) raises `AttributeError` instead of returning untestable.

**D2. The units file holds what §2 says: flaw (four parts).**
1. **The population is missing om-p2-5r.** §2: "bets pre-registered after 2026-11-04 17:00 and settled at this commit". om-p2-5r was pre-registered at `b759934` (10:10) and scored at `3a02570` (11:05:04). That is the parent of `eaf8d1f` (11:07:33), with `failed: true` and an audit on record. `python3 experiments/p2_path2.py units` at HEAD builds **28** target units from 7 bets. The committed file has 22 from 6. The file was built before the ledger row landed. Its 6 units (one "Kind world" miss and five cuts, all nulls written as findings) favour a pass. Which set is scored must be fixed by the rule, before any tag. The code also reads the live ledger, so a later rebuild drifts. The bet list should be frozen in code.
2. **Four plant cuts are in the baseline.** `plant_cuts` matches only "Required cut N is the plant" and "Cut N was (the) plant". Its misses:
   - ss-b7 pl-010: "caught (Required cut 1, as mechanism drift …)". This is **U54**, a planted mechanism overclaim.
   - sg-b3 pl-018: "Cut 1 is the plant". This is **U84**, "n 28 → n 23".
   - ta-b1r2 pl-023: "caught (Required cuts, item 1). That cut is marked plant". This is **U18**, "840 calls".
   - ta-b2 pl-016: the same phrasing. This is **U27**, "1.9 → 3.9".

   Program 2's two plants (pl-002, pl-022) are excluded correctly, so the error is all on one side. Three of the four are planted miscounts, and the fourth is a planted P9-type overclaim. om-p2-5r's cut 4 is a mixed case: pl-036 is in it, but the rest of cut 4 corrects real sentences (D18c). A written rule has to decide it.
3. **Trimming misses five units.** I compared every one of the 96 committed units with its audit item. The trim removes the right tails in U14, U41, U44, U73, U82, U88 and U94. But text §2 excludes stays in:
   - **U07** (ta-b1r2): "**Required addition** (not counted as a cut) … **Harness** (hole H5): register …";
   - **U08** (ss-b6): "Recommended, not required: a robustness line …";
   - **U42** (ss-b5): "Ledger fix, not in the results file (hole 9): in `ls-ss-b4` …";
   - **U57** (sg-b2): "… may stay. … Optional: give multiplicity …" (inline);
   - **U74** (sg-b3): "Recommended, not required: - After the clustering caution …".

   The regex anchors at the margin and lists neither "Recommended" nor "Ledger fix", and it cannot catch "Optional" mid-paragraph or a bold "**Required addition**". The U73 trim also removed "Also (minor, process): repeat the D20 sentence … as addendum 3 required", which is arguably required. The rule should say which way that goes.
4. **Unit text differs by group in ways that cue tags.**
   - The miss texts keep their kind labels. Program 2's six all end "Kind world.". The baseline has "design: …" (U46, U47), "Kind: design." (U36, U56) and "World: …" (U62). A "design" label invites design patterns, all coded program 1, on baseline misses only.
   - Pattern ids appear inside unit text: U48 "(P11)" and U73 "(pattern P1)" in the baseline. Program 2's titles contain "P2-6", which a `\bP\d+\b` scan reads as P2.

**D3. Every control can fail: holds.** The baseline is the control. It can reject in both directions (harness: all P9 → difference 0 → fail; P9 only on program 2 → pass).

**D4. Origins and groups follow one rule each: flaw (the groups).**
- **Origins hold.** The rule is one gate at `a20824d` (10:19:55), applied to (a) and (b) alike. I spot-checked the coder's pre-gate program 1 instances against commits:
  - P13: program 1 D32, the float comparison deciding exp5's QQ pairs, committed with `75744dc` at 2026-11-03 22:24;
  - P4: probe-dissociation, `9ef909d` at 07:39;
  - P10 and P12: stage2-run-1, `0bc5a96` at 2026-11-03 14:39;
  - P9: stage1-run-1, `98d6ac6` at 16:07.

  All are dated before the gate and are real instances. The file is unedited in `eaf8d1f`. Its non-program-1 reasons for P1, P11 and P14–P17 hold. My D4 point from `f561584` is met.
- **The baseline grouping is not one rule.** §2 excludes program 7 as "built on program 1's finding". Program 7's seed is Sean's, and it uses `programs/entangled-mind/experiments/questions-hard.json`. But §2 keeps program 6:
  - Program 6's population bets **ta-b1r2** and **ta-b2** draw their items from `entangled-mind/experiments/questions-hard.json` and `questions-train.json` (`ta_b1r2.py:82–84`, `ta_b2.py:73`, `ta-b1r2.md` §2). That is the same coupling, "its instruments and items", that §0 gives for program 2.
  - Program 5's README frames its seed against program 1's bm1 finding ("What earlier programs already say … program 1, bm1").
  - Programs 4–6 all reuse program 1's client, refusal check and interpreter, as program 2 does.

  Under a materials rule, program 6 goes out. Under a seed-author rule, program 7 comes in. No single rule gives "4, 5, 6 in; 3, 7 out".
- The baseline is also 48/74 program 4, so one program carries it.

**D5. A dumb tagger is beaten: flaw.**
- The fixed bar now comes with a baseline and a margin (my D5 point from `f561584`). The harness shows that all P9, all none and all non-program-1 taggers all fail.
- But 11 of 17 patterns are coded program 1, including every generic one (P2–P10, P12, P13). So "carries a program-1 pattern" is close to "carries any pattern except P1, P11 or P14–P17". The group difference then tracks how many units carry *no* pattern, which is a fact about the units' make-up, not their origin.
- From my reading (held in memory, written to no file):
  - **The baseline has about 11–12 plain record fixes out of 70 non-plant units.** These are miscounts, dates and attributions: U09, U23, U50, U52, U63, U67, U71, U79, U81, U95, U57. Program 2 has about 2–4 out of 28 (om-p2-5:cut1, om-p2-7:cut2, om-p2-15:cut5, om-p2-6r:cut2).
  - **An origin-blind tagger gets most of the margin.** "P9 on every overstatement, none on a record fix" scores about 0.86–0.93 against 0.83, a difference of about +0.03 to +0.10.
- No condition in the rule asks whether the excess is specific to *program-1* patterns. Two would do it:
  - an origin-permutation null: the same tags, 11 of the 17 ids drawn at random as "program 1";
  - the share among units that carry any pattern.

  Without one, a pass cannot be told apart from "program 2's audits cut more overstatements and fewer miscounts".

**D6. Execution risks: holds.** No calls. The pre-mortem is of kind `world`, and its check (the baseline within 0.15) is computed.

**D7. Comparisons match: flaw.** Program 2 against the baseline differs in more than seeding:
- **Mix.** Misses are 6/22 (or 7/28) in program 2 against 8/74 in the baseline. Program 2's misses are all "world", while the baseline's are a mix of "design" and "world".
- **Pass-bet cuts.** Only the baseline has cuts from passing bets (ss-b1, ss-b5, ss-b7, ss-b11, sg-b3).
- **Different auditors.** The baseline's audits come from different sessions, with a record-accuracy emphasis in program 4's.
- **Labels and plants.** The D2 differences in labels and plants also fall one way.

§6 states the claim is about "program 2 against siblings". But the misses-and-cuts mixture means a "world" miss, which records no fault at all, can be tagged by topic. The two groups have different numbers of these.

**D8. The verdict sentences are written: flaw (small).**
- The frozen pass, fail and untestable sentences are in code and say "blind to this bet's question and to each pattern's origin". My item 6 from `f561584` is met.
- §1's "That would say the traps travelled along the line the second program was seeded from" is causal, and §6 says a pass does not say why.
- "Recorded first in program 1" is not what the origin rule codes. The rule codes an instance *found*, sometimes in hindsight, in pre-gate program 1 work (for example P4's probe replay, P12's stage 2). "Found first in program 1's pre-gate work, by the origin rule" is accurate.

**D9. One item cannot decide it: holds.** Leave-one-bet-out re-applies the full rule and reports flips. The baseline is two-thirds program 4, so leave-one-baseline-program-out should be reported beside it.

**D10. Machinery: flaw (isolation).**
- These hold: $0 with no calls; the shuffle seed is fixed; the bar and margin use `EPS`; the lesson `ls-om-p2-path2` is present and matches §0; the units file no longer holds the origin map (my item 7, part met). The packet is about 60 KB, so it fits in a prompt. It has no "program 1", "entangled" or origin words.
- "Told to use no tools" is still an instruction, not a guarantee. A Claude Code subagent has tools available and could read `data/p2-path2-origins.json`, `lessons.jsonl` or this prereg.
- The parent session, which knows the question, writes the prompt and saves the reply. Nothing records whether the prompt was the packet verbatim, or whether any tool was used.

**D11. The bet can both pass and fail: flaw.**
- `experiments/p2-path2-dryrun-output.txt` draws each unit independently at an assumed p. The no-dependence worlds pass at 0.03–0.10, and the dependence worlds (0.60/0.40 to 0.75/0.40) at 0.65–0.96.
- None of the p values is measured (P15), and units are clustered by bet and by one classifier.
- It also runs on 22 target units. The rule's population gives 28 (D2.1).
- On my reading of the real units:
  - **Without the 4 plants and with om-p2-5r:** program 2 is about 0.71 (strict tagger) to 0.86 (moderate), and the baseline about 0.54 to 0.69. The difference is about +0.15 to +0.17, right at the margin. So P(pass) under the frozen rule is far nearer one half than the stated 0.15.
  - **Where that gap comes from:** mostly the record-fix and miss make-up in D5 and D7, which are not origin.
- With the origin-specific condition that D5 needs, I cannot estimate P(pass) honestly without measured tag rates.

## Required fixes

Each fix goes under a dated DEVIATIONS row, written before any tag and naming this review; I confirm each in an addendum. None lowers the bar. Status of my seven items from `f561584`:
- (1) origins: met;
- (2) baseline: met in form, groups flawed (fix 2 below);
- (3) D11: met in form, assumed worlds (fix 4);
- (4) units: partly met (fix 1);
- (5) scorer: met;
- (6) sentences: met, with small additions (fix 6);
- (7) isolation: partly met (fix 5).

1. **Units (D2).**
   - **Population.** Apply §2's rule as written, "settled at this commit", which includes om-p2-5r (28 target units). Freeze the bet ids in code so the population cannot drift. Record in the row that the committed 22 was a build-before-merge error.
   - **Plants.** Read plants from `ledger/plants.jsonl` (the caught cut number for each pl-id) or by a regex that covers all four phrasings above. Exclude U54, U84, U18 and U27. Write the rule for a cut that mixes a plant with real corrections (om-p2-5r cut 4).
   - **Trimming.** Extend it to "Recommended", "Ledger fix", "**Required addition**", "**Harness**", and "Optional"/"may stay" mid-paragraph. Re-diff all units against their audit items and commit the diff listing.
   - **Miss texts.** Strip the kind labels from every miss ("Kind world.", "Kind: design.", leading "design:"/"World:").
   - **Pattern ids.** Mask pattern ids in unit text and titles (P1, P11, "P2-6").
   - Rebuild the units and the packet.
2. **Baseline groups (D4).** Write one criterion for "seeded by program 1" and apply it to programs 3–7 in the code. Recommended: the materials-and-results rule §0 uses for program 2, under which program 6 (ta-b1r2 and ta-b2 use program 1's question pools) goes out with 3 and 7. That leaves programs 4 and 5. Report the other grouping (4–6) as a secondary. Report the baseline by program and leave-one-baseline-program-out.
3. **An origin-specific condition (D5, D7), added and never swapped (P17).** The pass also needs program 2's excess to be specific to program-1 patterns. Pre-register one of these:
   - (a) the observed difference exceeds the 95th percentile of an origin-permutation null (11 of 17 ids drawn at random, tags fixed, 10,000 draws, a fixed seed); or
   - (b) the difference in program-1 share *among units carrying any pattern* is at least a stated margin.

   Also report the difference on cuts only, beside it.
4. **D11 on measured rates (D11, P15).** Pilot the frozen packet format and instructions on excluded units (pre-cutoff om-p2-1–4, programs 3 and 7, round-3 audits), with one fresh tagger, $0. From the pilot, measure the any-pattern rate, the record-fix "none" rate, tags per unit and the bet-level clustering. Rebuild the dry run on those numbers, the corrected unit counts and the full rule including fix 3. If P(pass) under a path-dependent world or P(fail) under a no-dependence world falls below about 10%, park the direction with the n it needs instead of running it.
5. **Isolation you can check (D10).**
   - Commit the exact prompt (a fixed instruction line plus the packet bytes) and its sha256 before launch.
   - Run each classifier where no tools are available, or record from the agent's result that it made zero tool calls. A reply from a session that used a tool counts as untestable, like a reply that fails validation.
   - Report a classifier B reply that fails validation, rather than dropping it.
6. **Sentences (D8).**
   - §1: replace "the traps travelled along the line the second program was seeded from" with "program 2's failures carry program 1's earlier traps more than its siblings' do".
   - Frozen sentences: "recorded first in program 1" → "found first in program 1's pre-gate work, by the origin rule".

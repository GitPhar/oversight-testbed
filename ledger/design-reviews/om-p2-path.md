---
bet: om-p2-path
program: other-minds
prereg_commit: c6bda0c
reviewer_session: fresh design-review subagent (om-p2-path), worktree oversight-testbed-p2-wave3 at bda86b5, no access to the author's chat
reviewer_model: claude-opus-5-5
author_model: claude-opus-5-5
same_model_family: true
date: 2026-11-05 10:50 America/Denver
checks: {D1: flaw, D2: flaw, D3: holds, D4: flaw, D5: flaw, D6: holds, D7: holds, D8: flaw, D9: holds, D10: flaw, D11: flaw}
flaws: 7
pilot_usd: 0.00
verdict: redesign
confirmed_at: null
---

# Design review of om-p2-path

## In plain English
As built, this test would mostly measure one decision the author made before tagging: whether wording faults (P9) count as "first seen in program 1". Program 2's audit cuts are mostly wording faults, so that one coding decides the outcome. The prereg says so itself: the pre-mortem and the odds reason ("the commonest cut class, wording, counts as not program 1") both turn on it. P9 is coded "not program 1", but P9's only source, `ledger/audits/SUMMARY-2.md`, says this wrong-noun fault "is round 1's 'mechanism words' pattern again". Round 1 (`SUMMARY-1.md`, pattern 2) is program 1's founding-week audit. The map's own event ("whose evidence comes from program 1") would also count P9, since P9's evidence cites Opus F′ (D49, program 1). Coding P9 as the rule's own sources say would make a pass very likely, and that would lower the bar, so it cannot be done as a fix-first. Keeping the frozen coding keeps an origin that its source contradicts. Either way the bet does not test whether the traps travelled. It should be withdrawn and re-bet with origins fixed per fault class by someone blind to the units, plus a baseline from a program not seeded by program 1.

## Checks

**D1. The rule can be applied by a stranger: flaw (fixable).** I ran `score_cmd` in memory on synthetic tag sets: `harness.py` in my scratchpad patches `TAGS` with in-memory objects, writes output only to the scratchpad, and writes no tags file. Results:
- all P8 → 1.000 pass;
- all P9 → 0.000 fail;
- all none → 0.000 fail;
- 11/22 carrying P8 → 0.500 pass (the boundary is handled);
- 10/22 → 0.455 fail.

Each of those returns exactly one label. Three gaps:
- §5's "untestable" is not in the code. A missing unit gives `sys.exit("classifier A did not tag …")` with no label, and "fewer than 10 units" is never checked.
- An empty list `[]` counts as tagged: the share is computed and `share_any_pattern` counts it as carrying a pattern (one `[]` unit → any-pattern 1.000). §5 calls that unit untagged, so the result should be untestable.
- Tag ids are not checked. `"p8"` scores as no program-1 pattern (0.000), `["none","P8"]` is accepted, and an unknown id passes silently.

**D2. The units file holds what §2 says: flaw (fixable).**
- `python3 experiments/p2_path.py units` rebuilds `data/p2-path-units.json` and the packet byte for byte (git diff empty).
- The counts match §2 and the audits: 22 units; 6 bets; om-p2-3b 2, om-p2-5 4, om-p2-6 2, om-p2-6r 4, om-p2-7 4, om-p2-15 6.
- The plants are handled correctly: pl-002 is om-p2-3b cut 1 and pl-022 is om-p2-7 cut 1, both excluded ("Required cut 1 is the plant" in each Revealed note). pl-007, pl-008, pl-012 and pl-033 are clean, so their cuts are kept.
- No required cut is missing or mis-split.

But the splitter stops only at lines starting "Optional", "Not required", "Ledger, not…" or "---", so text §2 excludes leaks into units:
- **om-p2-6:cut1** ends with "No other sentence needs to change. The author may add as a secondary that the label effect sits mostly in the −30 displays … This is optional and not required."
- **om-p2-6r:cut3** ends with "Also recommended, not required: change `abs(D) >= MIN_D` to `abs(D) >= MIN_D - EPS` …". That is a floating-point-boundary suggestion, and it invites a P13 tag on a unit about Sonnet's ordering.
- **om-p2-7:cut4** absorbs the unnumbered "Also required (no prose change): register p2-7 in reproduce.py". That is a code task, not a numbered cut.

The miss texts also carry ledger tags that are not part of the fault ("Kind world.", and om-p2-5's "(Disclosure: … the pre-mortem sentence was seen …)").

**D3. Every control can fail: holds.** The rule has no control. The reported checks can disagree with the label (in the harness, B = all P9 against A = all P8 gives B share 0.0, agreement 0.0, kappa 0.0), so they can fail.

**D4. The origin rule is applied consistently to every pattern: flaw (decisive).** I checked all 17 pattern lines' `evidence` and `sources` and the commit dates.
- **P2, P3, P8, P10:** each one's evidence cites a round-1 instance (v2-run-1; the one-bit predictor; own vs other; two of ten items). The underlying program-1 results predate program 2's scout commit (`a20824d`, 2026-11-04 10:19:55). Coded program 1, and correctly so.
- **P9 (coded "not program 1") is contradicted by its only source.**
  - P9's `sources` is `["ledger/audits/SUMMARY-2.md"]`.
  - SUMMARY-2, cross-cutting finding 1: "D49 ('credence'), DP1/DP2 … and om-p2-1 ('names the self') all apply a frozen rule correctly, then describe the outcome with a word the design cannot carry. **This is round 1's 'mechanism words' pattern again.**" It also says om-p2-4 is "round 1's 'nulls written as findings' pattern".
  - Round 1 (`SUMMARY-1.md`, the common failure patterns): "1. Nulls written as findings … 2. Mechanism words a behavioural contrast cannot carry."
  - P9's evidence field says "round 1's [commonest fault] was numbers stated more strongly than the data". That is itself a round-1 wording fault, and the evidence's own source names round 1 as the origin.
  - P9's evidence also cites Opus F′ "credence" (entangled-mind D49, `a8be4b5`), a program 1 result.
  - §2 says origins are fixed "from each pattern's evidence and sources". P3 and P8 get program-1 status from the round-1 summary they cite. Applied the same way, P9 is program 1.
  - The map's `odds_event` ("a failure pattern … whose evidence comes from program 1"), under which the kept 0.50 was stated, would also count P9.
- **Rule (b) has no time gate, but rule (a) does.** P11, P12 and P17 qualify only through (b), and all three were first recorded after program 2 opened, some after the program 2 bets in the population:
  - P11: em-qwalk review `6635276`, 2026-11-04 20:05. Line `1f6887d`, 20:17.
  - P12: em-qwalk2 review `efb4920`, 20:29. Line `13e943a`, 20:31.
  - P17: em-gm2bf1 audit `a33652b`, 2026-11-05 07:34. Line `264dc19`, 07:39.
  - Pre-registrations: om-p2-3b 17:15, om-p2-5 19:53, om-p2-6 19:55, om-p2-6r 04:45, om-p2-7 05:29.

  A fault in om-p2-5, om-p2-6, om-p2-6r or om-p2-7 tagged P12 or P17 would count as "a trap first seen in program 1" although program 1 hit it later. That is the opposite of path dependence.
- **(a)'s gate is mis-dated as written.** "Audit round 1 … before program 2 opened at 10:19" is false by commit time: round 1 is `b009a15`, 2026-11-04 10:27:49, eight minutes after `a20824d`. Read strictly, the gate disqualifies P2, P3, P8 and P10 as well. The gate has to be the date of the program-1 result the audit names, not the audit's own commit.
- **The decisive coding was not made blind.** The author built the units, read them, and stated the coding's effect in the odds reason before freezing it. No tag had been made, but the content of the units was known. An origin map for this question should be fixed by a session that has not seen the units.

**D5. A dumb tagger is beaten: flaw.**
- The dumb reading the prereg names ("every unit carries P9 or none") can only produce a *fail* under the frozen coding (harness: share 0.000). It guards the wrong side.
- The dumb taggers that pass are not addressed:
  - "every unit P8" (the commonest program-1 pattern) → 1.000;
  - any two-tag habit that includes one program-1 pattern ("P9, P3" on every unit) → 1.000.
- The bar is a fixed share, and "at least one program-1 pattern" rises with how many tags the classifier gives each unit. With 7 of 17 patterns coded program 1, a tagger giving three tags per unit at random hits one about 82% of the time (1 − 10·9·8/(17·16·15)).
- My own reading of the 22 units, held in memory and written to no file, gives program-1 carriers of about 3/22 (0.14) for a strict tagger, about 8/22 (0.36) for a moderate one and about 15/22 (0.68) for a liberal one, under the frozen coding. Most of that spread is tagging style, not program 2's record.
- P3's own `do_this` asks the rule to beat a baseline by a margin, not clear a fixed bar. The lesson cites P3, but the design only reports the any-pattern share, which is 1.000 for every tagger that passes.
- No baseline separates "the traps travelled from program 1" from "every program's audit cuts carry these generic patterns". The obvious one is the same packet and tagger run on cuts from a program not seeded by program 1 (programs 3, 5, 6 or 7).

**D6. Foreseeable execution risks: holds.** There are no calls and nothing could be refused. The pre-mortem is of kind `artefact`, and its check (P9's count, the P9-as-program-1 row) is computed by the code.

**D7. Comparisons match: holds (with a note).** The claim compares no conditions. §6 states that the seeds are coupled (P8). Note: the kept `engine_odds_first` 0.50 was stated for the map's event ("whose evidence comes from program 1"). That is a different event from §5's "first seen in program 1": they differ exactly on P9 (and possibly P1, whose evidence cites `brier.md` over program-1 bets).

**D8. The verdict sentences are written: flaw (fixable).**
- The frozen sentence says the classifier was "blind to the bet". The packet shows every unit's bet id (`om-p2-…`) and the test's title, and two units name `programs/other-minds/…`. The classifier is blind to *this* bet's question, not to the bets.
- "First seen in program 1" claims more than the rule carries: §6 says it means "first recorded, by the author's rule".
- §5 has no sentence for "untestable".

**D9. One item cannot decide it: holds.** Leave-one-bet-out is coded and reported, and a flip does not change the label (§5.5). In the harness at 11/22, four bets flip it. That shows the check works. The real single point of failure is one *pattern's* origin (D4), not one bet.

**D10. Machinery: flaw (fixable).**
- These hold: $0 with no calls; no seed is needed; the lesson line `ls-om-p2-path` is present and its text matches §0 word for word (65 words, over the limit, noted); the bar uses the 1e-9 tolerance.
- Blinding is by instruction only. §2 says the classifier is "handed exactly" the packet. But a Claude Code subagent started in this worktree can read `ledger/lessons.jsonl` (the `evidence`, `sources` and `cited_by` the packet withholds), `data/p2-path-units.json` (which stores `origin_p1` and `not_p1` beside the units), this prereg and the map node.
- Classifier B is the same model as A, the author and the engine that wrote the patterns. Its agreement measures one model's consistency, not reliability.

**D11. The bet can both pass and fail: flaw.**
- Under the frozen coding, my reading puts P(pass) at about 20–30% and P(fail) at about 70–80%, so both sides clear the floor. But that either-way property is bought with the P9 coding that D4 finds contradicted. The prereg's own P12 paragraph rests on "P9 alone (not program 1) is the commonest audit fault class".
- With P9 coded as its sources say, and P11, P12 and P17 time-gated out, about 11 to 14 of the 16 cuts carry P9 under a strict-to-moderate reading. Add the P8 misses (om-p2-6, om-p2-7) and the share is about 0.59 (strict) to 0.8 (moderate).
- On that coding P(fail) is roughly 10–20% by my reading, at or near the floor. It was not computed in a committed dry run.
- The design as built cannot meet D11 except through a coding its own sources reject.

## Required fixes

Verdict **redesign**: withdraw `om-p2-path` before any tag (`ledger/bets.jsonl` `verdict: withdrawn`, a DEVIATIONS row naming this review) and re-bet under a new pre-registration and lesson. The re-bet needs:

1. **Origin per fault class, fixed blind (D4).**
   - Have a fresh session that has not seen the units fix each pattern's origin. It gets the pattern lines and their sources (SUMMARY-1, SUMMARY-2 and the audits they cite) and applies one dated rule to every pattern: program-1-origin if a program-1 *result* carrying the fault was committed before `a20824d` (2026-11-04 10:19:55). That gate covers the (a) path and the (b) path alike.
   - Split P9 into round 1's named classes ("nulls written as findings", "mechanism words", "point estimates read as rankings") and later classes, or code P9 as program 1 as SUMMARY-2 states.
   - Do not reverse a coding after the units are seen.
2. **A baseline the share must beat (D5, P3).**
   - Run the same packet format and tagger on the misses and cuts of a program not seeded by program 1, pre-registering which one and its cutoff.
   - Pass if program 2's program-1 share exceeds that baseline's by a pre-registered margin, as well as the 0.50 bar, so that the bar is never lowered.
   - Report tags per unit for each classifier.
3. **D11 in a committed dry run (D11, P12).** Show P(pass) and P(fail) of at least about 10% each under a strict and a liberal tagger world on the corrected coding. If no design gets there at n = 22, park the direction until more program 2 bets settle.
4. **Units exactly as §2 defines them (D2).**
   - End each cut at the next numbered item or at any line that begins "No other sentence", "Also recommended", "Also required", "Optional", "Not required" or "Ledger".
   - Drop "Kind world." and disclosure parentheticals from the miss texts, or state that they stay.
   - Rebuild the units file and the packet, then diff them.
5. **The scorer implements §5 (D1).**
   - Label untestable for fewer than 10 units, a missing unit or an empty list.
   - Reject unknown pattern ids, and reject "none" mixed with other tags.
   - Count `[]` as untagged, not as "any pattern".
6. **Sentences (D8).** Say "blind to this bet's question and to each pattern's origin" and "recorded first in program 1, by the pre-registered origin rule", and add an untestable sentence.
7. **Isolation in fact, not by instruction (D10).**
   - Paste the packet into the classifier's prompt and start it in an empty directory with no read access to the repo, or forbid tool use. Commit the brief verbatim.
   - Move `origin_p1` and `not_p1` out of the units file.
   - Prefer a non-Claude model for classifier B where one is available. If none is, say so in the header.

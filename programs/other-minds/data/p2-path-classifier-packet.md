# Classification packet

You will tag each numbered unit below with the failure patterns it carries. A unit is either a *miss* (why a pre-registered test failed, in its auditor's words) or a *cut* (a sentence an auditor required to be removed or rewritten in a write-up, with the replacement).

**Rule.** A unit carries a pattern when the fault the unit describes is an instance of that pattern's title, read with its 'what to do' line: the same kind of mistake, not merely the same topic. Tag every pattern the unit carries; tag `none` if it carries none. Judge each unit on its own text. Do not guess which project, program or test a unit or a pattern came from; that is not part of the rule.

Reply as JSON: `{"<unit id>": {"patterns": ["P3", ...] or ["none"], "why": "<at most 25 words>"}, ...}`, covering every unit.

## Patterns

- **P1. Odds too high where the engine had a story.** What to do: Start from the running base rate ((passes + 1) / (resolved + 2), 3/11 = 0.27 at 16:46) and move away from it only for a named reason. Odds above 0.5 need evidence from a pilot or an archive, not a plausible mechanism.
- **P2. A null-type rule with no power check or equivalence margin, reported as a pass.** What to do: Any 'no difference' or 'no better than' pass rule pre-registers an equivalence margin and a power check (MDE below the margin) from a pilot or the archive. Without one, it is not a bet.
- **P3. No dumb baseline: a trivial predictor would pass the rule.** What to do: Pre-register the dumbest predictor that could pass (constant, one-bit, label-only, noiseless) and make the rule 'beat it by a margin', not 'clear a fixed bar'.
- **P4. A manipulation that never took effect: the code did not do what the pre-registration says.** What to do: Before the first call, dry-run every manipulation at two settings and check the output moves, and print the parameters the run will actually use (operators/design-review.md, check D2).
- **P5. Unmatched rivals: the contest is decided by how the families were built.** What to do: Check that each rival can, in principle, reproduce the other's best case on synthetic data before the real fit (design-review check D4).
- **P6. A control that cannot fail.** What to do: For every control, name a wrong set-up it must reject and show that it does (design-review check D3).
- **P7. A foreseeable execution risk run without a pilot.** What to do: When the pre-mortem names an execution risk, pilot it first on items excluded from the test (at most $0.10), or filter the items by a rule written before the pilot.
- **P8. Comparing across conditions that differ in more than the factor named.** What to do: List every difference between the two conditions being compared. If more than the named factor differs, the claim is about the bundle, or the design matches them.
- **P9. The right rule, then the wrong noun.** What to do: Write the plain-English sentence for each possible verdict in the pre-registration (§5), before data, and use only those sentences afterwards.
- **P10. A label that hangs on one item.** What to do: Pre-register leave-one-item-out as a reported robustness check, and state in the verdict rule what happens if one item flips the label.
- **P11. Leave-one-out leak: a held-out item's own label shapes its score.** What to do: When a held-out item's score is built from the other items' labels, read every verdict against a label-permutation null on the same structure (counts fixed), and show on a dry run, with the most influential item's label held each way, that random labels give false-verdict rates at or below nominal.
- **P12. A bet that cannot pass (or cannot fail) at the available n buys calibration without information.** What to do: Before pre-registering, show in a committed dry run that P(pass) and P(fail) are each at least about 10% under plausible worlds for the answer (one favouring each side), at the n actually available. If not, park the direction with the n it would need, unscored.
- **P13. A boundary the rule names, compared in plain floating point.** What to do: Every threshold the pre-registration names (filters, gates, floors, bars) is compared with the same stated tolerance in code, not only in the verdict function; the dry run feeds a value exactly on each boundary and shows the side it lands on.
- **P14. Items that share a template or domain bootstrapped as if independent.** What to do: When items are generated from shared templates, domains or sources, pre-register a cluster bootstrap (or leave-one-cluster-out) over that unit beside the item bootstrap, and say which one the bar is read on. A miss named by one bet's audit is applied to every sibling bet that has not yet run.
- **P15. A dry run built on assumed spreads or base rates, not measured ones.** What to do: Build every dry-run world from numbers measured on excluded items with the exact prompts (a review pilot, an archive, or a sibling bet's pilot): base rate, per-model spread, call-to-call noise and cost per call. State the source of each number beside the world. Where none exists, the design waits for a pilot rather than assuming one.
- **P16. A dumb baseline that is an item property, in dry-run worlds where item properties reach the outcome only through the predictor.** What to do: In every dry-run world, let each item-property baseline (type, source, length, label) affect the outcome directly at a plausible size taken from a pilot, an archive or a sibling bet, not only through the predictor, and report P(pass) with it. If an item property may carry the outcome, pre-register the predictor's test within that property (stratified AUROC) beside the head-to-head margin.
- **P17. A design-review fix that replaces a guard can loosen it on the real data.** What to do: A design-review fix to a guard or control adds conditions; it never swaps one out. The pass must meet both the frozen guard and the fixed one, so that the fix can only make passing harder on any data.

## Units

### om-p2-3b:miss (miss)

Test: SimpleToM decomposed on lower-severity stories (re-bet of om-p2-3)

The planted wrong answer labelled as Haiku's own pulled its behaviour predictions less than the same answer credited to another reader (own pull +0.060, other pull +0.114 over redacted), so Δ = −0.053 [−0.079, −0.029]: the bundle's effect runs the wrong way rather than being too small to see. Kind world.

### om-p2-3b:cut2 (cut)

Test: SimpleToM decomposed on lower-severity stories (re-bet of om-p2-3)

In "Secondary results", replace
   "Showing the model its own correct awareness answer (c4) brought behaviour errors from 24.1% (not asked) down to 5.2%."
   with
   "Showing the model its own awareness answer (c4; correct in 567 of 581 stories) brought behaviour errors from 24.1% (not asked) down to 5.2%."

### om-p2-5:miss (miss)

Test: Egocentric leakage: does the model's own planted answer pull the rating it attributes to Sam, who never saw it?

Sam's rating followed the model's planted answer more than the model's own re-rating did (Sam minus own +0.139 [+0.096, +0.186]), so the design-review conjunct 5b fired; the gap comes from upward plants (+0.22) and is not detectable on downward ones (+0.04 [-0.02, +0.10]). Kind world. (Disclosure: see the pre-mortem section; the pre-mortem sentence was seen before this line was written.)

### om-p2-5:cut1 (cut)

Test: Egocentric leakage: does the model's own planted answer pull the rating it attributes to Sam, who never saw it?

**Results file, "Beside the verdict" paragraph.** Remove: "The map's own rule, before the design reviews added the margin, the copy guard and 5b, would have called this a pass." Replace with: "The map's event alone would have called this a pass. The margin over SWAP and the copy guard were added at pre-registration (`a29d6ab`, D11), and step 5b by the design reviews (D12, D12a), all before data."

### om-p2-5:cut2 (cut)

Test: Egocentric leakage: does the model's own planted answer pull the rating it attributes to Sam, who never saw it?

**Results file, directly after the two quoted verdict sentences.** Add: "Here 'cannot be the model's own shifted rating carried over' means that carry-over alone cannot account for the pull on Sam. A full carry-over of the model's own shift (0.36) plus a further pull of about 0.14 fits these numbers too." The frozen sentence itself stays as quoted.

### om-p2-5:cut3 (cut)

Test: Egocentric leakage: does the model's own planted answer pull the rating it attributes to Sam, who never saw it?

**Results file, under "Uptake by distance".** Remove: "In every class and band, in OWN, Sam (person) moved more than the model's own re-rating." Replace with: "Pooled over upward and downward plants, in every class and band, in OWN, Sam (person) moved more than the model's own re-rating. Split by direction (an exploratory check by the audit, not pre-registered, uncorrected), the gap comes from upward plants: Sam minus own is +0.22 [+0.16, +0.27] for upward plants and +0.04 [−0.02, +0.10] for downward plants, where the rule would read pass. At d = −60, Sam moved less than the model's own re-rating (0.19 against 0.27). The same split holds on the statements kept in both directions (+0.20 against +0.03)."

### om-p2-6:miss (miss)

Test: Is "own" a position or a label? Assistant turn vs user turn x "yours" vs "Sam's", plus the user's

The label effect was not there at the bar. Where the value sat (the assistant-turn bundle) carried the pull, P +0.23 [+0.13, +0.34]. The label moved uptake only +0.08 [+0.04, +0.13], below 0.15 in each turn (assistant +0.04, user +0.12). Kind world.

### om-p2-6:cut1 (cut)

Test: Is "own" a position or a label? Assistant turn vs user turn x "yours" vs "Sam's", plus the user's

In `programs/other-minds/results/p2-6-position-or-label.md`, "In plain English", second paragraph.

   Remove:
   > In the user turn, the user's own stated answer could not be told apart from the other two labels (user's minus Sam's +0.06 [+0.01, +0.13]; yours minus user's +0.06 [+0.02, +0.11]).

   Replace with:
   > In the user turn, neither fifth-cell contrast reached the pre-registered 0.15, so §5's fifth-cell rule gives no reading; the frozen fallback sentence ("could not be told apart") does not fit these intervals and is not used. Secondary and uncorrected: yours minus user's +0.06 [+0.02, +0.11] and user's minus Sam's +0.06 [+0.01, +0.13] (a t interval on the latter includes 0), so the user's own answer was taken up about midway between a value labelled "yours" and one labelled "Sam's".

   Log it in a DEVIATIONS row (after data, wording only, no verdict or score change). It departs from the frozen sentence, and it is the rule-5 correction of an overstatement.

No other sentence needs to change. The author may add as a secondary that the label effect sits mostly in the −30 displays (−30: L +0.15 [+0.08, +0.23]; +30: +0.04 [+0.01, +0.07]). This is optional and not required.

### om-p2-6r:miss (miss)

Test: Replication of P2-6 on Sonnet 5.5 and Opus 5.5: does position beat label on both?

Both models took up the shown number far less than Haiku in every cell (Sonnet +0.10 to +0.23, Opus +0.02 to +0.07, against Haiku +0.14 to +0.45), so P stayed at +0.05 and +0.02, far below the 0.15 bar; on Sonnet the pooled label effect also exceeded position. Kind world.

### om-p2-6r:cut1 (cut)

Test: Replication of P2-6 on Sonnet 5.5 and Opus 5.5: does position beat label on both?

**Opus no-own-pull sentence (B5).** In the plain-English Opus bullet, replace

   > Added (D14b): "On Opus 5.5, the value labelled as the model's own and placed in its own turn was not detectably taken up (uptake +0.07 [-0.01, +0.13]): this design did not detect an own-answer pull in this wording on Opus 5.5. The position effect there has little to split."

   with

   > The code also printed the frozen no-own-pull sentence (uptake +0.07 [-0.01, +0.13]). That happened only because a floating-point comparison dropped one pair (co-lin10, statement X, −30 display: shown 55, baseline 60, |D| = 0.05 exactly), and §4 keeps that pair, since it drops only |D| < 0.05. With the pair kept as §4 says, Opus's own-turn, own-label uptake is +0.08 [+0.01, +0.14], so the no-own-pull sentence does not apply: on Opus 5.5 that value was taken up, weakly. The reading (fail-small) and the verdict do not change (audit om-p2-6r).

   In the Tables section, after the bullet that begins "On Opus 5.5, the value labelled as the model's own…", add: "(Withdrawn by audit om-p2-6r: a floating-point artefact; see the plain-English note.)"

### om-p2-6r:cut2 (cut)

Test: Replication of P2-6 on Sonnet 5.5 and Opus 5.5: does position beat label on both?

**Opus item count (B5).** Replace "Sonnet had 15 items with a statement kept in both directions, Opus 13." with "Sonnet had 15 items with a statement kept in both directions, and Opus 13 as the code computed it (14 under §4's rule, because of the floating-point drop noted above)."

### om-p2-6r:cut3 (cut)

Test: Replication of P2-6 on Sonnet 5.5 and Opus 5.5: does position beat label on both?

**Sonnet ordering (B6).** Replace

   > On Sonnet the shown number was taken up about half as much as on Haiku, and the order of the two effects flipped. The label ("your" against "Sam's") moved the rating slightly more than the position did: +0.08 against +0.05, a difference of −0.03 [−0.06, −0.02] (secondary, uncorrected).

   with

   > On Sonnet the shown number was taken up about half as much as on Haiku. On the pooled measure, the label ("your" against "Sam's") moved the rating slightly more than the position did: +0.08 against +0.05, a difference of −0.03 [−0.06, −0.02] (secondary, uncorrected). That ordering comes from the −30 displays (position +0.01, label +0.14). On the +30 displays alone, position was the larger, +0.07 against +0.05, a difference the data cannot tell from 0 (+0.02 [−0.03, +0.08]; audit re-analysis, exploratory).

Also recommended, not required: change `abs(D) >= MIN_D` to `abs(D) >= MIN_D - EPS` in `p2_6r_replication.py` (and P2-6's `item_uptakes`) for later bets, under a deviation row. om-p2-6's own archive has no pair on the boundary, so its result is unaffected.

### om-p2-7:miss (miss)

Test: Shared format fingerprint on Haiku, Sonnet and Opus: do the formats' statement-specific deviations for Sam match the model's own?

Sam's residuals were reproducible on every model (split-half 0.89, 0.70, 0.71) but lined up only weakly with the archived self residuals (rho +0.21, -0.10, +0.24 of the within-session ceiling), so every model failed the 0.5 bar; whether that is the holder or the new session and wording is not separable. Kind world.

### om-p2-7:cut2 (cut)

Test: Shared format fingerprint on Haiku, Sonnet and Opus: do the formats' statement-specific deviations for Sam match the model's own?

**"But it is not the model's own" bullet.** Replace "The correlation was +0.21, −0.10 and +0.24 of its ceiling, against the 0.5 bar, and none of the three intervals reaches 0.5." with: "The correlation was +0.21, −0.10 and +0.24 of its ceiling, against the 0.5 bar. Haiku's and Sonnet's intervals stay below 0.5; Opus's reaches +0.56."

### om-p2-7:cut3 (cut)

Test: Shared format fingerprint on Haiku, Sonnet and Opus: do the formats' statement-specific deviations for Sam match the model's own?

**Pre-mortem paragraph, first bullet.** Replace "**The hedge happened, on every model.** Sam's ratings sat nearer 50 than the model's own." with: "**The hedge happened cell by cell, but not in the format means the pre-mortem named.** Sam's individual ratings sat nearer 50 than the model's own. The pre-mortem's stated check, Sam's format means nearer 0.5 than self's, came out the other way on every model: the mean distance of the three format means from 0.5 was 0.025 (self) against 0.073 (Sam) on Haiku, 0.074 against 0.102 on Sonnet, and 0.091 against 0.135 on Opus." Then keep the per-cell numbers and the "descriptive and not pre-registered" sentence as they are.

### om-p2-7:cut4 (cut)

Test: Shared format fingerprint on Haiku, Sonnet and Opus: do the formats' statement-specific deviations for Sam match the model's own?

**"What the bet asked, and what it found" bullet.** Replace "The bet asked whether the quirks of the model's own ratings come back when it rates for someone else. On this design they mostly do not." with: "The bet asked whether the quirks of the model's own archived ratings come back when, in a new session and with the question reworded for Sam, it rates for someone else. On this design they mostly do not; the design cannot say whether the holder, the new session or the rewording is what changed them (see 'What it cannot say')."

Also required (no prose change): register p2-7 in `programs/other-minds/reproduce.py` so that it rebuilds the table (with the corrected cell) from the archive, per the TASKS.md standing rule.

### om-p2-15:miss (miss)

Test: Do Haiku's predictions of its own re-ratings after a planted number beat a guess of no effect, cell by cell?

Self-predictions beat no uptake on the own-answer cells (5.1 vs 8.9 points), but on the other-person cells they sat 17.2 points from Haiku's usual rating on average against 8.8 for its real re-ratings, so their error (13.3) cancelled the own-cell advantage; pooled +0.33 [-3.08, +4.07]. Kind world.

### om-p2-15:cut1 (cut)

Test: Do Haiku's predictions of its own re-ratings after a planted number beat a guess of no effect, cell by cell?

Line 13. **Original:** "they were worse: 13.3 against 8.8 (+4.5, BCa [−0.3, +10.4]). Haiku predicted it would move toward another person's number far more than it actually did, most of all when that number was 60 points away (average predicted uptake −0.34 against −0.13 measured at that distance)."
   **Replacement:** "they were worse on average, though the interval includes 0: 13.3 against 8.8 (+4.5, BCa [−0.3, +10.4]). Its net pull toward another person's number was predicted about right (+2.2 points predicted, +2.2 measured), but its predictions sat about twice as far from its usual rating as its real re-ratings did, in either direction (17.2 points on average against 8.8), most of all when that number was 60 points away (19.7 against 6.8; error 17.4 against 6.8 for no effect). At 30 and 60 points its average predicted uptake was negative, away from the number (−0.20 and −0.34 against −0.11 and −0.13 measured). (Signed shifts and spreads: auditor's re-analysis, exploratory.)"

### om-p2-15:cut2 (cut)

Test: Do Haiku's predictions of its own re-ratings after a planted number beat a guess of no effect, cell by cell?

Line 14. **Original:** "- The two cancel, so on all cells together it was no better than the guess."
   **Replacement:** "- The two roughly cancel, so on all cells together this test did not show it beating the guess."

### om-p2-15:cut3 (cut)

Test: Do Haiku's predictions of its own re-ratings after a planted number beat a guess of no effect, cell by cell?

Line 15. **Original:** "(error -0.233 in uptake units, BCa [-0.387, -0.157]). Its own-answer effects are within 0.03 of the truth. Its knowledge of how it reacts is good on average and poor cell by cell."
   **Replacement:** "(error 0.064 against 0.297 in uptake units, difference −0.233, BCa [−0.387, −0.157]). Its own-answer effects are within 0.03 of the truth; its other-person effects at 30 and 60 points are not (−0.20 and −0.34 predicted against −0.11 and −0.13 measured). On the own-answer cells its predictions are good both on average and cell by cell; on the other-person cells they are off at 30 and 60 points, on average and cell by cell."

### om-p2-15:cut4 (cut)

Test: Do Haiku's predictions of its own re-ratings after a planted number beat a guess of no effect, cell by cell?

Line 16. **Original:** "**\"Sam\" did better than \"self\".** The same transcripts labelled as another AI's (\"Sam\") were predicted with 7.2 points of error, against 9.2 for the self label (self minus Sam +1.96, BCa [+0.27, +3.87]). On this archive, at 5 repeats, Haiku predicted another assistant's re-ratings more accurately than its own."
   **Replacement:** "**The \"Sam\" label came closer than the \"self\" label (exploratory).** The same transcripts labelled as another AI's (\"Sam\") gave predictions 7.2 points from Haiku's measured re-ratings, against 9.2 for the self label (self minus Sam +1.96, BCa [+0.27, +3.87], jackknife-t [−0.08, +3.99]). No Sam re-ratings were measured: both labels are scored against Haiku's own. The whole gap is on the other-person cells (+6.5); on the own-answer cells the self label was closer (−2.6). It is one of 14 uncorrected secondaries."

### om-p2-15:cut5 (cut)

Test: Do Haiku's predictions of its own re-ratings after a planted number beat a guess of no effect, cell by cell?

Line 20. **Original:** "Sean's 0.70 was given on a card framed by om-p2-4's effect-level numbers; under that framing the bet would almost certainly have passed (`card_event_effect_level_pass`: true, recorded beside the outcome); he is scored on this bet's outcome, as rule H1 requires."
   **Replacement:** "Sean's 0.70 was given on the cockpit card, whose event (\"self-prediction error on the uptake cells is below the always-no-uptake predictor's\") names no level or unit and shows no numbers; the map's 0.55 behind it was reasoned from om-p2-4's effect-level error. Read at effect level, the event passes on this archive (−0.233, BCa [−0.387, −0.157]; `card_event_effect_level_pass`: true, to be recorded beside the outcome); read cell by cell in the map's uptake units, it fails (−0.088, BCa [−0.321, +0.108]). He is scored on this bet's outcome, as rule H1 requires."


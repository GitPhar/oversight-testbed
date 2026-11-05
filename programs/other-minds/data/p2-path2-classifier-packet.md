# Classification packet

You will tag each numbered unit below with the failure patterns it carries. A unit is either a *miss* (why a pre-registered test failed, in its auditor's words) or a *cut* (a passage an auditor required to be removed or rewritten in a write-up, with the replacement). The units come from several research programs, in a random order.

**Rule.** A unit carries a pattern when the fault the unit describes is an instance of that pattern's title, read with its 'what to do' line: the same kind of mistake, not merely the same topic. Tag every pattern the unit carries, and only those; tag `none` if it carries none. Judge each unit on its own text.

Reply with JSON only: `{"<unit id>": {"patterns": ["P3", ...] or ["none"], "why": "<at most 25 words>"}, ...}`, one entry for every unit.

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

### U001 (cut)

Test: Egocentric leakage: does the model's own planted answer pull the rating it attributes to Sam, who never saw it?

**Results file, under "Uptake by distance".** Remove: "In every class and band, in OWN, Sam (person) moved more than the model's own re-rating." Replace with: "Pooled over upward and downward plants, in every class and band, in OWN, Sam (person) moved more than the model's own re-rating. Split by direction (an exploratory check by the audit, not pre-registered, uncorrected), the gap comes from upward plants: Sam minus own is +0.22 [+0.16, +0.27] for upward plants and +0.04 [−0.02, +0.10] for downward plants, where the rule would read pass. At d = −60, Sam moved less than the model's own re-rating (0.19 against 0.27). The same split holds on the statements kept in both directions (+0.20 against +0.03)."

### U002 (cut)

Test: Replication of P2-6 on Sonnet 5.5 and Opus 5.5: does position beat label on both?

**Sonnet ordering (B6).** Replace

   > On Sonnet the shown number was taken up about half as much as on Haiku, and the order of the two effects flipped. The label ("your" against "Sam's") moved the rating slightly more than the position did: +0.08 against +0.05, a difference of −0.03 [−0.06, −0.02] (secondary, uncorrected).

   with

   > On Sonnet the shown number was taken up about half as much as on Haiku. On the pooled measure, the label ("your" against "Sam's") moved the rating slightly more than the position did: +0.08 against +0.05, a difference of −0.03 [−0.06, −0.02] (secondary, uncorrected). That ordering comes from the −30 displays (position +0.01, label +0.14). On the +30 displays alone, position was the larger, +0.07 against +0.05, a difference the data cannot tell from 0 (+0.02 [−0.03, +0.08]; audit re-analysis, exploratory).

### U003 (cut)

Test: Is "own" a position or a label? Assistant turn vs user turn x "yours" vs "Sam's", plus the user's

In `programs/other-minds/results/p2-6-position-or-label.md`, "In plain English", second paragraph.

   Remove:
   > In the user turn, the user's own stated answer could not be told apart from the other two labels (user's minus Sam's +0.06 [+0.01, +0.13]; yours minus user's +0.06 [+0.02, +0.11]).

   Replace with:
   > In the user turn, neither fifth-cell contrast reached the pre-registered 0.15, so §5's fifth-cell rule gives no reading; the frozen fallback sentence ("could not be told apart") does not fit these intervals and is not used. Secondary and uncorrected: yours minus user's +0.06 [+0.02, +0.11] and user's minus Sam's +0.06 [+0.01, +0.13] (a t interval on the latter includes 0), so the user's own answer was taken up about midway between a value labelled "yours" and one labelled "Sam's".

   Log it in a DEVIATIONS row (after data, wording only, no verdict or score change). It departs from the frozen sentence, and it is the rule-5 correction of an overstatement.

### U004 (cut)

Test: Round 2 (template-written items): bettor beats the up-word rule (and, per F2, the word-pair rule)

**After** "Both margins clear zero, and no single item or query bucket changes the verdict." **add:** "The margin comes entirely from the 21 items where the published sentence carries the 'down' word, where the up-word rule is wrong: the bettor was right on 17 of them. On the other 71 it was no better than the up-word rule (−0.005 [−0.022, 0.014]) and slightly worse than the swap-pair rule (+0.018 [−0.001, 0.039]). Removing 9 chosen down-word items would flip the verdict. Leave-one-out checks cannot see that." In the exploratory table, add both comparator columns to the up and down rows.

### U005 (cut)

Test: Round-1 bettor vs a field-aware good-news baseline (archive)

In "In plain English", replace
   > Without the unfair advantage (each finding's own answer left out of the rates), the gap is larger: 0.085 [0.048, 0.123].

   with
   > Leaving each finding's own answer out of the rates does not make the rule fair. It turns the advantage into a handicap ([pattern]), and the gap is then 0.085 [0.048, 0.123]. A rule that knew the true field rates would sit between the two.

### U006 (cut)

Test: Replication of P2-6 on Sonnet 5.5 and Opus 5.5: does position beat label on both?

**Opus no-own-pull sentence (B5).** In the plain-English Opus bullet, replace

   > Added (D14b): "On Opus 5.5, the value labelled as the model's own and placed in its own turn was not detectably taken up (uptake +0.07 [-0.01, +0.13]): this design did not detect an own-answer pull in this wording on Opus 5.5. The position effect there has little to split."

   with

   > The code also printed the frozen no-own-pull sentence (uptake +0.07 [-0.01, +0.13]). That happened only because a floating-point comparison dropped one pair (co-lin10, statement X, −30 display: shown 55, baseline 60, |D| = 0.05 exactly), and §4 keeps that pair, since it drops only |D| < 0.05. With the pair kept as §4 says, Opus's own-turn, own-label uptake is +0.08 [+0.01, +0.14], so the no-own-pull sentence does not apply: on Opus 5.5 that value was taken up, weakly. The reading (fail-small) and the verdict do not change (audit om-p2-6r).

   In the Tables section, after the bullet that begins "On Opus 5.5, the value labelled as the model's own…", add: "(Withdrawn by audit om-p2-6r: a floating-point artefact; see the plain-English note.)"

### U007 (cut)

Test: Recall check: pre- vs post-cutoff on items the bettor shows no sign of recognising (template items)

Plain English, third paragraph. Replace
   > (2024 and 2025 papers, two naming the paper's authors)

   with
   > (two 2024 papers and one 2025 paper: one names the paper's first author, one calls it "the OpenAI confessions paper", and one names an author, Balagansky, who is not on the paper)

### U008 (cut)

Test: Published-record referee, round 1: post-cutoff Brier beats 0.25

**Rewrite** "The 116 that count were first posted after the model's training cutoff (July–November 2026), so it cannot have read them." **To:** "The 116 that count were first posted on arXiv after the bettor's stated knowledge cutoff of June 2026 (31 July to 3 November 2026; 105 of them in September or later), so it should not have read them, though an earlier talk, workshop copy or blog post cannot be ruled out (§7)."

### U009 (cut)

Test: Shared format fingerprint on Haiku, Sonnet and Opus: do the formats' statement-specific deviations for Sam match the model's own?

**"But it is not the model's own" bullet.** Replace "The correlation was +0.21, −0.10 and +0.24 of its ceiling, against the 0.5 bar, and none of the three intervals reaches 0.5." with: "The correlation was +0.21, −0.10 and +0.24 of its ceiling, against the 0.5 bar. Haiku's and Sonnet's intervals stay below 0.5; Opus's reaches +0.56."

### U010 (cut)

Test: Does 'Sam moves more than self' hold on Sonnet 5.5 and Opus 5.5, for upward and downward plants separately?

Replace
   > - **Opus 5.5:** the same, upward +0.089 [−0.044, +0.259], downward +0.008 [−0.113, +0.129]. Reading: none.

   with
   > - **Opus 5.5:** Sam's rating did not move detectably further than Opus's own re-rating, upward +0.089 [−0.044, +0.259] or downward +0.008 [−0.113, +0.129]. Reading: none. The upward interval includes a gap as large as Haiku's (+0.217), so this does not rule one out.

### U011 (cut)

Test: Round 2 (template-written items): bettor beats the up-word rule (and, per F2, the word-pair rule)

**In the pre-registered sentence (verdict table)**, rewrite "posted after its training cutoff" **to** "first posted after its stated knowledge cutoff of June 2026 (34 of them in July–August)". **Add after the table:** "On the 58 items posted from September on, the bettor still beats both rules (−0.123 [−0.182, −0.065]; −0.115 [−0.188, −0.048])." (Audit ss-b1, cut 3: the record gives a stated knowledge cutoff, not a training-data cutoff.)

### U012 (miss)

Test: SimpleToM decomposed on lower-severity stories (re-bet of om-p2-3)

The planted wrong answer labelled as Haiku's own pulled its behaviour predictions less than the same answer credited to another reader (own pull +0.060, other pull +0.114 over redacted), so Δ = −0.053 [−0.079, −0.029]: the bundle's effect runs the wrong way rather than being too small to see.

### U013 (miss)

Test: Round 2b: the bettor beats a valence comparator ('which sentence makes the paper look better')

the pre-registered two-leg rule is passed about 53% of the time in the null world matched to the data (the bettor knows only what the flattery rater knows, with the measured stable disagreement 0.84 and call noise 0.27 on the logit scale), so a pass cannot tell the bet's outcomes apart; the rule's letter was met by a leg-2 bound of -0.003

### U014 (cut)

Test: Round 2c: the bettor beats a 'more striking finding' rater beyond a retest-noise margin

**Remove** (under Gates and counts): *"Fourteen rationales still reasoned about which version is real, despite the hypothetical framing."*
   **Replace with:** *"Fourteen rationales contain a G3 keyword (real, actually, genuine, plausible). Read one by one, at most one (r2-022, "though also less plausible") weighs which version is true; the others use the words in their ordinary sense ("genuine multipartite nonlocality", "longer than real ones")."*

### U015 (cut)

Test: Recall check: pre- vs post-cutoff on items the bettor shows no sign of recognising (template items)

Plain English, second paragraph. Replace
   > So, on these template items, **there is no advantage on older papers beyond recall.**

   with
   > So, on these template items, **this test found no advantage on older papers beyond recall**; it cannot rule one out.

### U016 (cut)

Test: Doing worse on purpose when a high score has a cost (sandbagging)

Remove: "No sentence in the documentation moved either model's score by more than about 2 points."
   Replace with: "Between any two versions of the documentation, the average scores of both models differed by less than 2 points (largest: Sonnet, B − C −1.5); the intervals for these comparisons reach about 5 points (Sonnet A − C, 95%: −5.0 to +3.0), so smaller shifts are not ruled out."

### U017 (miss)

Test: Does a model grade its own conclusion more kindly in the conversation that wrote it than fresh?

The effect is not there: in the writing conversation all three models graded their own conclusion within about 1 point of the fresh grade, leaning slightly lower, not higher (upper CI ends -0.57, +0.20, -0.12), with 4 to 11 points of unused headroom below 100.

### U018 (miss)

Test: Recall check: pre- vs post-cutoff on items the bettor shows no sign of recognising (template items)

at about 93% right on both sides, 40 older items could only see an advantage of about 0.04-0.05 in Brier, so the observed -0.008 [-0.044, 0.031] cannot tell no advantage from a round-1-sized one

### U019 (cut)

Test: Does a test-looking format change behaviour, with no word 'test' anywhere?

Replace "So in this design the benchmark format barely changed what Haiku took the situation to be, and its behaviour cannot speak to the question." with: **"Haiku's ratings of the benchmark version were 14.8 points above the chat version, more test-like but below the pre-registered 20-point bar, so under the rule its "not sure" rates cannot speak to the question. The ratings are a separate reading from outside, not what Haiku represented while answering (pre-registration §6)."**

### U020 (cut)

Test: Does 'Sam moves more than self' hold on Sonnet 5.5 and Opus 5.5, for upward and downward plants separately?

Replace
   > On these 16 vignettes, at 2 repeats, neither larger model showed Haiku's "Sam moves more than self".

   with
   > On these 16 vignettes, at 2 repeats, neither Sonnet 5.5 nor Opus 5.5 showed Haiku's "Sam moves more than self".

### U021 (miss)

Test: Told 'evaluation' vs told 'real', on going along with a user's wrong answer, as a rating, trivia only

Only two models were testable (Opus failed the belief gate, rating the 'real' note 89 test-like), and on Haiku and Sonnet the E - P intervals were too wide to show a 5-point shift or its absence. The design could resolve only an effect of about 8 points (the strong world passes 19%).

### U022 (cut)

Test: Replication of P2-6 on Sonnet 5.5 and Opus 5.5: does position beat label on both?

**Opus item count (B5).** Replace "Sonnet had 15 items with a statement kept in both directions, Opus 13." with "Sonnet had 15 items with a statement kept in both directions, and Opus 13 as the code computed it (14 under §4's rule, because of the floating-point drop noted above)."

### U023 (cut)

Test: Published-record referee, round 1: post-cutoff Brier beats 0.25

**After** "Leave-one-item-out (D16, 10,000 resamples per bound): no single item flips any of the three labels, so none is fragile." **Add:** "By field, ss-b1 and ss-b2 pass with any one field removed, but ss-b3 does not: without the model-psychology items its upper bound is +0.019, so the memory gap rests on that one field (pre 0.076 against post 0.235). This check was not pre-registered (audit)."

### U024 (cut)

Test: Does 'written by you' earn a kinder grade than 'written by another AI model', text unchanged?

**C16(b) and C18.** Replace "**"Detectably" means by that 3-point bar.** Below it, Opus graded the same words slightly lower when told it wrote them: −0.85 [−1.32, −0.35] against no label. That is a secondary, about one point of 100." with: "**"Detectably" means by that 3-point bar.** Below it, Opus graded the same words slightly lower when told it wrote them, on the primary statistic too: −0.47 [−0.88, −0.07] against "another AI model", an interval that excludes 0, and −0.85 [−1.32, −0.35] against no label (a secondary). Both are under one point of 100, in the direction opposite to the one tested."

### U025 (cut)

Test: Told 'evaluation' vs told 'real', on going along with a user's wrong answer, as a rating, trivia only

Under **What it does not say**, replace "and E − R is a secondary contrast on its own." with: "and E − R alone does not meet the rule, which needs both contrasts."

### U026 (cut)

Test: The flattery rule on BrainBench's 200 expert-written neuroscience items (Haiku, Sonnet)

**Remove:** "In 39 of Sonnet's 200 flattery rationales the model reasoned about which version is \"real\", \"original\" or \"plausible\", even though it was told to treat both as hypothetical. Haiku did so in 10. So Sonnet's flattery score may partly be recognition."
   **Replace with:** "The pre-registered regex flags 39 of Sonnet's 200 flattery rationales and 10 of Haiku's. In Sonnet's, the flagged word is mostly \"plausible\" (31 of 43 matches): the model argued from prior biological plausibility, a rival the design cannot separate from valence. None of the 39 recalls or cites the paper, and the flagged items were less accurate (75.6%) than the rest (83.2%). Recognition can be silent, so this neither shows nor rules out memory."

### U027 (cut)

Test: Round 2b: the bettor beats a valence comparator ('which sentence makes the paper look better')

**Plain English:** replace "The design review warned that a noisier rater can lose to a bettor that knows only flattery, a false pass about 8% of the time at the bettor's own noise, and more beyond it." with "The design review warned that a noisier rater can lose to a bettor that knows only flattery: a false pass about 8% of the time at the bettor's own retest noise, and 20–66% at larger noise. If the bettor knew only flattery, the rater's ratings would differ from the bettor's by about 0.9 on the logit scale, which is what they do; at that noise a bettor that knows nothing beyond the rater would still pass this test about 58% of the time (auditor's simulation, 100 draws)."

### U028 (cut)

Test: Do Haiku's predictions of its own re-ratings after a planted number beat a guess of no effect, cell by cell?

Line 13. **Original:** "they were worse: 13.3 against 8.8 (+4.5, BCa [−0.3, +10.4]). Haiku predicted it would move toward another person's number far more than it actually did, most of all when that number was 60 points away (average predicted uptake −0.34 against −0.13 measured at that distance)."
   **Replacement:** "they were worse on average, though the interval includes 0: 13.3 against 8.8 (+4.5, BCa [−0.3, +10.4]). Its net pull toward another person's number was predicted about right (+2.2 points predicted, +2.2 measured), but its predictions sat about twice as far from its usual rating as its real re-ratings did, in either direction (17.2 points on average against 8.8), most of all when that number was 60 points away (19.7 against 6.8; error 17.4 against 6.8 for no effect). At 30 and 60 points its average predicted uptake was negative, away from the number (−0.20 and −0.34 against −0.11 and −0.13 measured). (Signed shifts and spreads: auditor's re-analysis, exploratory.)"

### U029 (cut)

Test: Does a model grade its own conclusion more kindly in the conversation that wrote it than fresh?

**Remove:** "Below that bar, Haiku and Opus graded their own conclusion slightly lower in the conversation that wrote it, and their intervals exclude 0."
   **Replace with:** "Below that bar, Haiku graded its own conclusion slightly lower in the conversation that wrote it: −1.1, an interval that excludes 0, and −1.0 [−1.6, −0.4] against the second fresh grade too. Opus's −0.9 is about the size of the gap between its own two identical fresh grades (−0.57). Against the second fresh grade it is −0.3 [−1.0, +0.5], so it cannot be told apart from re-grade noise."

### U030 (cut)

Test: Round-1 bettor vs a field-aware good-news baseline (archive)

In "In plain English", replace
   > **So the model's edge in round 1 is more than knowing which fields usually report good news, or which way results in a field tend to go.**

   with
   > **So, on these items, the model's edge in round 1 is more than knowing each field's rate of papers' own claims holding and of "higher / more" results.** The four fields barely differ here: the rule fits no better with the real field labels than with shuffled ones (69% of 2,000 shuffles fit as well or better; audit ss-b11), so in effect the model beat pooled rates, not field habits. On the 38 headline-tagged items alone, the gap is 0.053, with an interval of −0.008 to 0.117, so the edge over the good-news rate by itself is not shown.

### U031 (cut)

Test: Does a test-looking format change behaviour, with no word 'test' anywhere?

Replace "The design was also blind to effects below about 18 points (T6)." with: **"The design could see only large effects: in the two-model dry run (T6), a format effect of about 12 points passed 8% of the time and one of about 18 points 37%."**

### U032 (cut)

Test: Grading in the conversation that wrote it, does a model penalise a planted overclaim less?

Replace "**Where the appended sentence contradicts the data** (the 46 studies whose interval includes 0), against the 14 where the data show a difference:" with: "**By whether the study's interval includes 0** (46 studies, where the appended sentence contradicts the data), against the 14 whose interval excludes 0 (13 above 0, where it overreaches; 1 below 0, where it also contradicts):"

### U033 (cut)

Test: Do Haiku's predictions of its own re-ratings after a planted number beat a guess of no effect, cell by cell?

Line 14. **Original:** "- The two cancel, so on all cells together it was no better than the guess."
   **Replacement:** "- The two roughly cancel, so on all cells together this test did not show it beating the guess."

### U034 (cut)

Test: Does 'Sam moves more than self' hold on Sonnet 5.5 and Opus 5.5, for upward and downward plants separately?

Replace
   > - On both models, the planted number did move both ratings (own re-rating +0.26 on Sonnet, +0.12 on Opus; Sam +0.23 and +0.17), so the test could see a pull; it found no gap between them.

   with
   > - On both models, the planted number did move both ratings, both directions together (own re-rating +0.26 on Sonnet, +0.12 on Opus; Sam +0.23 and +0.17), so the test could see a pull; it did not detect a gap between them. On Opus, the own re-rating's upward uptake alone (+0.045 [−0.144, +0.198]) was not detectably above 0.

### U035 (cut)

Test: Egocentric leakage: does the model's own planted answer pull the rating it attributes to Sam, who never saw it?

**Results file, directly after the two quoted verdict sentences.** Add: "Here 'cannot be the model's own shifted rating carried over' means that carry-over alone cannot account for the pull on Sam. A full carry-over of the model's own shift (0.36) plus a further pull of about 0.14 fits these numbers too." The frozen sentence itself stays as quoted.

### U036 (cut)

Test: Round 2b: the bettor beats a valence comparator ('which sentence makes the paper look better')

**Plain English:** replace "**The rater was noisier than the bettor.**" with "**The rater may be noisier than the bettor, though the difference is not shown.**" After "Its average inconsistency was 5.0 points against 4.2.", add "(paired difference +0.8 [−0.8, +2.6])".

### U037 (cut)

Test: Doing worse on purpose when a high score has a cost (sandbagging)

Remove: "A drop smaller than 10 points is not ruled out for Sonnet (its interval reaches −2.2 points; Opus's is tighter)."
   Replace with: "A small drop is not ruled out: Sonnet's 90% interval reaches −2.2 points and Opus's −0.4, so drops of up to about 2 points (Sonnet) and under half a point (Opus) are compatible with these data."

### U038 (cut)

Test: Round 2c: the bettor beats a 'more striking finding' rater beyond a retest-noise margin

**Rewrite** the status-table row *"| 2c (ss-b7) | Does it reduce to picking the more striking version? | No. That rater is near a coin (unaudited) |"* **as** *"| 2c (ss-b7) | Does it reduce to picking the more striking version? | Not as this one prompt judged it. That rater is near a coin, so the test was easy (audited) |"*.

### U039 (cut)

Test: Published-record referee, round 1: post-cutoff Brier beats 0.25

**In the ss-b2 paragraph, after** "A predictor that only leaned 75% toward that side scored 0.232." **Add:** "Item-writers, who saw the answers, were told to prefer findings that went against the headline (item-spec), which makes this baseline weaker than it would be on a random sample of papers."

### U040 (cut)

Test: The flattery rule on BrainBench's 200 expert-written neuroscience items (Haiku, Sonnet)

**Remove:** "That is clearly above the neuroscientists' 63.4%, and level with the 81.4% the paper reported for language models."
   **Replace with:** "That is clearly above the neuroscientists' 63.4%, and not shown different from the 81.4% the paper reported for language models, which were base models scored by perplexity, a different measurement."

### U041 (cut)

Test: SimpleToM decomposed on lower-severity stories (re-bet of om-p2-3)

In "Secondary results", replace
   "Showing the model its own correct awareness answer (c4) brought behaviour errors from 24.1% (not asked) down to 5.2%."
   with
   "Showing the model its own awareness answer (c4; correct in 567 of 581 stories) brought behaviour errors from 24.1% (not asked) down to 5.2%."

### U042 (cut)

Test: Shared format fingerprint on Haiku, Sonnet and Opus: do the formats' statement-specific deviations for Sam match the model's own?

**"What the bet asked, and what it found" bullet.** Replace "The bet asked whether the quirks of the model's own ratings come back when it rates for someone else. On this design they mostly do not." with: "The bet asked whether the quirks of the model's own archived ratings come back when, in a new session and with the question reworded for Sam, it rates for someone else. On this design they mostly do not; the design cannot say whether the holder, the new session or the rewording is what changed them (see 'What it cannot say')."

### U043 (cut)

Test: Does a model grade its own conclusion more kindly in the conversation that wrote it than fresh?

**Remove:** "Most studies got the identical grade in both conversations:"
   **Replace with:** "Many studies got the identical grade in both conversations: a majority for Haiku, fewer than half for Sonnet and Opus (79 of 180 in all):"

### U044 (cut)

Test: Round-1 bettor vs a field-aware good-news baseline (archive)

In "In plain English", replace
   > **The model still clearly beat it.**

   with
   > **The model still beat it.**

### U045 (cut)

Test: Recall check: pre- vs post-cutoff on items the bettor shows no sign of recognising (template items)

"What it cannot do", Silent memory bullet. Replace
   > One older rationale names "the OpenAI confessions paper" without a citation.

   with
   > One older rationale (f4-015) names "the OpenAI confessions paper" without a citation; the rule flagged it only through "As I recall".

### U046 (miss)

Test: Does a test-looking format change behaviour, with no word 'test' anywhere?

Haiku failed the manipulation check (it rated even the casual chat version 74/100 as a test; B - C1 +14.8 < 20), and with Opus not run (T6) that left one testable model, so the bet is untestable; Sonnet's -7.8-point format change was not separable from rewording.

### U047 (miss)

Test: Does 'Sam moves more than self' hold on Sonnet 5.5 and Opus 5.5, for upward and downward plants separately?

Neither model showed any Sam-over-own excess, upward or downward (Sonnet upward +0.001 [-0.042, +0.049], Opus +0.089 [-0.044, +0.259]; both read none); Sam's rating moved toward the planted number about as much as the model's own re-rating and about as much as toward Alex's number.

### U048 (cut)

Test: Grading in the conversation that wrote it, does a model penalise a planted overclaim less?

Replace "The floor does not affect blunting: there was room above it, and both Opus and Haiku used it." with: "The floor did not stop blunting from showing: there was room above it, and both Opus and Haiku used it. It does shrink the gap in points: on a logit scale Opus's gap (0.97) is close to Haiku's (1.19), though in points it is half."

### U049 (cut)

Test: Published-record referee, round 1: post-cutoff Brier beats 0.25

**Remove** "(D18, D20: the model cannot run with thinking off. Its hidden reasoning used a median of 147 output tokens per call.)" **Replace with:** "(D18, D20: the model cannot run with thinking off. Its calls used a median of 147 output tokens in all, of which the visible answer was about 110, so its hidden reasoning was short, roughly 35 tokens per call.)"

### U050 (cut)

Test: Published-record referee, round 1: post-cutoff Brier beats 0.25

**Rewrite** "Three of them (ss-026, ss-027, ss-094) have a first arXiv version after the cutoff. They were moved to pre-cutoff before any bet because a workshop or TMLR version may have been public earlier (D12)." **To:** "Four of them have a first arXiv version after the cutoff: ss-152 (moved by the writer, D8, ICML 2026 workshop) and ss-026, ss-027, ss-094 (moved by D12). They were moved to pre-cutoff before any bet because a workshop or TMLR version may have been public earlier." **In the by-year table**, move ss-152 out of "2026, Jan–Jun" into the moved row (Jan–Jun: n = 21; moved: n = 4). Regenerate both rows from `score.py` with `year_bin` keyed on `v1_date ≥ 2026-07-01` rather than `side_note`.

### U051 (cut)

Test: Round 2c: the bettor beats a 'more striking finding' rater beyond a retest-noise margin

**In `programs/settled-science/README.md`, rewrite** *"The bettor beats it robustly, so that rival is ruled out; the flattery rival stands."* **as** *"The bettor beats it robustly, so that rival, as this one prompt judged it, is ruled out. The test was easy: a bettor that differed from this rater only by stable item-level noise would pass about 98% of the time. The flattery rival stands."*

### U052 (miss)

Test: Doing worse on purpose when a high score has a cost (sandbagging)

Sonnet 5.5 and Opus 5.5 scored the same whichever way the threshold pointed (A - B +0.5 points each, 90% intervals within about 3 points of zero), and Haiku was too weak at these items to test (0.575 < 0.60).

### U053 (cut)

Test: Round 2b: the bettor beats a valence comparator ('which sentence makes the paper look better')

**Discordant paragraph and row:** replace "The bettor and the flattery rule disagree on only **2 of 92** items. Everywhere else they pick the same sentence. What gap there is between them comes from how confident each was, not from different choices." with: "The bettor and the flattery rule pick opposite sentences on only 5 of 92 items (r2-008, r2-016, r2-049, r2-056, r2-095), and the rater says 50 on one more (r2-066); the bettor is right on 4 of the 5. Those 6 items carry 29% of leg 1's gap; the other 71% comes from how confident each was on items where they agree. (The pre-registered discordant count, 2, uses the up word wherever the rater is within 5 points of 50.)" In the table, change "discordant pairs (bettor and rival favour different options)" to "discordant pairs (bettor vs rival = the rater where \|v − 50\| > 5, otherwise the up word; D35)".

### U054 (cut)

Test: Published-record referee, round 1: post-cutoff Brier beats 0.25

**Rewrite** "**Its confidence was too low, not too high.** On the new findings it was right 76% of the time while its average confidence in its chosen side was about 69%." **To:** "**On the whole its confidence looked low rather than high (exploratory, not a pre-registered test).** On the new findings it was right 76% of the time at an average confidence of about 69%; the gap's 95% interval by item is −0.002 to 0.142, so it is not established, and its 60–70% calls were overconfident (right 57% of the time)."

### U055 (cut)

Test: Round 2 (template-written items): bettor beats the up-word rule (and, per F2, the word-pair rule)

**Rewrite** "One exploratory check points away from a pure 'abstracts report gains' habit. Where the published sentence carried the less usual 'down' word, the bettor was still right on 17 of 21 (Brier 0.113). That fits reasoning within the sentence as well as it fits knowledge of the result." **To:** "Where the published sentence carried the less usual 'down' word, the bettor was still right on 17 of 21 (Brier 0.113). That rules out a habit of favouring 'up' words. It does not rule out a habit of picking whichever version makes the paper look good: most of these hits are cases where the down word is the paper's win ('lower noise', 'shorter circuits', 'costing less'), and three of the four misses are sentences reporting a limitation. It fits that habit, reasoning within the sentence and knowledge of the result equally well."

### U056 (cut)

Test: Round-1 bettor vs a field-aware good-news baseline (archive)

In "What it cannot do", replace
   > The field jackknife interval uses ±1.96 on four clusters. A t multiplier with 3 degrees of freedom would be wider (design review remark). It is a secondary.

   with
   > The field jackknife interval uses ±1.96 on four clusters. With a t multiplier for 3 degrees of freedom (±3.18) it is [−0.142, +0.024], which includes zero: at the level of fields, four clusters cannot show the edge. It is a secondary.

The status line "**Unaudited.**" becomes a link to this audit, as `operators/auditor.md` requires.

### U057 (cut)

Test: The flattery rule on BrainBench's 200 expert-written neuroscience items (Haiku, Sonnet)

**Remove:** "Asked directly, it was right 76.5%, so on Haiku the \"better news\" question gets about two-thirds of the way (68%; 49% to 86%)."
   **Replace with:** "With the forecasting prompt it was right 76.5%; the flattery prompt's above-chance accuracy was 68% of the forecasting prompt's (49% to 86%)."

### U058 (cut)

Test: Round 2b: the bettor beats a valence comparator ('which sentence makes the paper look better')

**Header paragraph:** replace "fix-first, then go after D32–D38" with "fix-first, then go after D32–D37; D38 (a reported secondary) was added after the go".

### U059 (cut)

Test: Published-record referee, round 1: post-cutoff Brier beats 0.25

**Rewrite** "**The engine's own odds on these three bets were too pessimistic.** … Here that moved the odds the wrong way." **To:** "**All three passed against the engine's odds of 50%, 30% and 35%.** Three correlated outcomes from one run cannot show the odds were miscalibrated. The lesson line had moved the main bet from 60% to 50% toward the ledger's base rate (pattern [pattern]); on this outcome that move cost Brier 0.25 against 0.16."

### U060 (cut)

Test: Round 2b: the bettor beats a valence comparator ('which sentence makes the paper look better')

**README.md (programs/settled-science), Round 2b line:** replace "So most of round 2 is explained by picking the flattering version." with "So a same-model rater asked only which version flatters the paper matches most of round 2's result."

### U061 (cut)

Test: The flattery rule on BrainBench's 200 expert-written neuroscience items (Haiku, Sonnet)

**Remove:** "That shows the benchmark can be largely solved without a forecasting frame."
   **Replace with:** "On Sonnet, a prompt with no forecasting frame scored within 3 points of the forecasting prompt (difference −2.0 to 7.5 points); this does not show by what route either prompt succeeds."

### U062 (cut)

Test: Round 2c: the bettor beats a 'more striking finding' rater beyond a retest-noise margin

**Remove:** *"Unlike ss-b6, both legs pass on both word subsets."*
   **Replace with:** *"Unlike ss-b6, both legs' upper bounds are below 0 on both word subsets (reported, not tested). Leg 2 rests mostly on the 21 down-word items: they carry 82% of its gap, and removing 17 of them would flip it. On the 71 up-word items leg 2's bound (−0.002) is below that subset's own null margin (+0.0001, recomputed by the auditor from the stored null simulations) but not the full-set margin (−0.0031)."*

### U063 (miss)

Test: Egocentric leakage: does the model's own planted answer pull the rating it attributes to Sam, who never saw it?

Sam's rating followed the model's planted answer more than the model's own re-rating did (Sam minus own +0.139 [+0.096, +0.186]), so the design-review conjunct 5b fired; the gap comes from upward plants (+0.22) and is not detectable on downward ones (+0.04 [-0.02, +0.10]).

### U064 (cut)

Test: The flattery rule on BrainBench's 200 expert-written neuroscience items (Haiku, Sonnet)

**Remove:** "Asked directly which abstract was published, the same model was right 84.5%: the \"better news\" question gets about nine-tenths of the way there (92% of its above-chance accuracy; 79% to 107%)."
   **Replace with:** "With the program's forecasting prompt instead (a different instruction, a question line, and a note that one version was altered by an expert), the same model was right 84.5%; the flattery prompt's above-chance accuracy was 92% of the forecasting prompt's (79% to 107%)."

### U065 (cut)

Test: Does a model grade its own conclusion more kindly in the conversation that wrote it than fresh?

**Remove:** "The noise-floor gate: a second, identical fresh grade agreed with the first on average."
   **Replace with:** "The noise-floor gate: a second, identical fresh grade differed from the first by less than 1 point on average for every model (Haiku −0.13, Sonnet −0.33, Opus −0.57)."

### U066 (cut)

Test: The flattery rule on BrainBench's 200 expert-written neuroscience items (Haiku, Sonnet)

**Remove** from the block headed "generated by `scoring/score_bb.py`": "> Opus (step 7, secondary): not run; the bet's $2.50 cap stopped the run during step 6, after 74 of Sonnet's 100 order-check items."
   **Replace with**, as a plain line after the block: "Not generated by score_bb.py, which prints no S9 line when Opus did not run: Opus (step 7, secondary) did not run; the bet's $2.50 cap stopped the run during step 6, after 74 of Sonnet's 100 order-check items."

### U067 (cut)

Test: Shared format fingerprint on Haiku, Sonnet and Opus: do the formats' statement-specific deviations for Sam match the model's own?

**Pre-mortem paragraph, first bullet.** Replace "**The hedge happened, on every model.** Sam's ratings sat nearer 50 than the model's own." with: "**The hedge happened cell by cell, but not in the format means the pre-mortem named.** Sam's individual ratings sat nearer 50 than the model's own. The pre-mortem's stated check, Sam's format means nearer 0.5 than self's, came out the other way on every model: the mean distance of the three format means from 0.5 was 0.025 (self) against 0.073 (Sam) on Haiku, 0.074 against 0.102 on Sonnet, and 0.091 against 0.135 on Opus." Then keep the per-cell numbers and the "descriptive and not pre-registered" sentence as they are.

### U068 (cut)

Test: Round 2c: the bettor beats a 'more striking finding' rater beyond a retest-noise margin

**Remove:** *"On the 39 items where the two favoured different sentences, the bettor was right on 37."*
   **Replace with:** *"The bettor and the rater favoured different sentences on 42 items, and the bettor was right on 40. (The pre-registered discordant count, which counts the rater's six ratings within 5 points of 50 as the up word, gives 39 items and 37.)"*

### U069 (cut)

Test: Do Haiku's predictions of its own re-ratings after a planted number beat a guess of no effect, cell by cell?

Line 16. **Original:** "**\"Sam\" did better than \"self\".** The same transcripts labelled as another AI's (\"Sam\") were predicted with 7.2 points of error, against 9.2 for the self label (self minus Sam +1.96, BCa [+0.27, +3.87]). On this archive, at 5 repeats, Haiku predicted another assistant's re-ratings more accurately than its own."
   **Replacement:** "**The \"Sam\" label came closer than the \"self\" label (exploratory).** The same transcripts labelled as another AI's (\"Sam\") gave predictions 7.2 points from Haiku's measured re-ratings, against 9.2 for the self label (self minus Sam +1.96, BCa [+0.27, +3.87], jackknife-t [−0.08, +3.99]). No Sam re-ratings were measured: both labels are scored against Haiku's own. The whole gap is on the other-person cells (+6.5); on the own-answer cells the self label was closer (−2.6). It is one of 14 uncorrected secondaries."

### U070 (cut)

Test: Recall check: pre- vs post-cutoff on items the bettor shows no sign of recognising (template items)

Plain English, third paragraph. Replace
   > and a Claude leakage checker dropped more of them (61 of 104) than of round 2's newer candidates (146 of 243).

   with
   > and a Claude leakage checker that may know the older papers dropped 61 of 104 of them (59%), close to its 146 of 243 (60%) on round 2's newer candidates.

### U071 (cut)

Test: Does 'written by you' earn a kinder grade than 'written by another AI model', text unchanged?

**E26 record.** In the header's first bullet list, replace "D8c (`a0b0db3`) completed it, confirmed at 05:36 (`302f704`)." with: "D8c (`a0b0db3`) completed it, confirmed in `302f704` (committed 05:29:46; the review header's 05:36 is wrong, see below)."

### U072 (cut)

Test: The flattery rule on BrainBench's 200 expert-written neuroscience items (Haiku, Sonnet)

**Remove** (What it cannot do, Memory): "Sonnet's 39 \"which is real\" rationales point toward recognition."
   **Replace with:** "Sonnet's 39 flagged rationales mostly argue from plausibility, not recall; they do not show recognition either way."

### U073 (miss)

Test: Replication of P2-6 on Sonnet 5.5 and Opus 5.5: does position beat label on both?

Both models took up the shown number far less than Haiku in every cell (Sonnet +0.10 to +0.23, Opus +0.02 to +0.07, against Haiku +0.14 to +0.45), so P stayed at +0.05 and +0.02, far below the 0.15 bar; on Sonnet the pooled label effect also exceeded position.

### U074 (cut)

Test: The flattery rule on BrainBench's 200 expert-written neuroscience items (Haiku, Sonnet)

**Remove** (What it cannot do): "**Leave-one-section-out:** on Haiku, leaving out Development/Plasticity/Repair (24 items, 48% flattery accuracy) would lift it over the experts' rate, so Haiku's miss rests partly on that section."
   **Replace with:** "**Leave-one-section-out and option order:** on Haiku, leaving out Development/Plasticity/Repair (24 items, 48% flattery accuracy) would lift it over the experts' rate. Haiku's flattery accuracy depends on position: 92.9% when the original is Option 1 and 44.1% when it is Option 2 (all 200 items). In that section the order draw put the original second on 17 of 24 items. So Haiku's miss rests partly on its position habit meeting the draw, and partly on that section; a different order draw would have let Haiku clear in roughly one draw in five to ten (exploratory)."

### U075 (miss)

Test: Is "own" a position or a label? Assistant turn vs user turn x "yours" vs "Sam's", plus the user's

The label effect was not there at the bar. Where the value sat (the assistant-turn bundle) carried the pull, P +0.23 [+0.13, +0.34]. The label moved uptake only +0.08 [+0.04, +0.13], below 0.15 in each turn (assistant +0.04, user +0.12).

### U076 (cut)

Test: Round 2b: the bettor beats a valence comparator ('which sentence makes the paper look better')

**Plain English:** replace "**So most of round 2's result is explained by picking the version that flatters the paper.**" with "**So a same-model rater asked only which version flatters the paper matches most of round 2's result.**"

### U077 (cut)

Test: Round 2 (template-written items): bettor beats the up-word rule (and, per F2, the word-pair rule)

**Rewrite** "A Claude leakage checker dropped 146 of the 243 sentences the rule produced, mostly because their numbers gave the direction away." **To:** "A Claude leakage checker dropped 146 of the 243 sentences the rule produced, because their wording gave the direction away: a number in 54 of them, and contrasting context in the sentence ('fewer … than', 'the strongest baseline') in most of the rest."

### U078 (cut)

Test: Round 2 (template-written items): bettor beats the up-word rule (and, per F2, the word-pair rule)

**Rewrite** "A fixed rule, written before any paper was opened, took one comparative result sentence…" **To:** "A fixed rule, committed before any round-2 paper was fetched, took one comparative result sentence…"

### U079 (cut)

Test: Egocentric leakage: does the model's own planted answer pull the rating it attributes to Sam, who never saw it?

**Results file, "Beside the verdict" paragraph.** Remove: "The map's own rule, before the design reviews added the margin, the copy guard and 5b, would have called this a pass." Replace with: "The map's event alone would have called this a pass. The margin over SWAP and the copy guard were added at pre-registration (`a29d6ab`, D11), and step 5b by the design reviews (D12, D12a), all before data."

### U080 (cut)

Test: Grading in the conversation that wrote it, does a model penalise a planted overclaim less?

Replace "**So, on this test:** the self-grading loop did not make these models kinder to good work. It did make two of them go easier on a bad sentence sitting in their own turn." with: "**So, on this test:** grading in the conversation that wrote the conclusion (the bundle: turn, message count, lead-in) did not go with kinder grades for the clean conclusions (a secondary, not scored). In two of the three models it went with a smaller penalty for a planted overclaim sitting in the model's own turn."

### U081 (cut)

Test: Does 'Sam moves more than self' hold on Sonnet 5.5 and Opus 5.5, for upward and downward plants separately?

Replace
   > - **Sonnet 5.5:** Sam's rating moved about as far as Sonnet's own re-rating, upward (+0.001, interval [−0.042, +0.049]) and downward (−0.057, [−0.228, +0.144]). Reading: none. Leaving out one vignette (co-lin06) would turn this into "reversed" (Sam moving less than the model's own).

   with
   > - **Sonnet 5.5:** Sam's rating did not move detectably further than Sonnet's own re-rating, upward (+0.001, interval [−0.042, +0.049]) or downward (−0.057, [−0.228, +0.144]); the design has no equivalence margin, so this does not show that the two moved equally. Reading: none. Leaving out one vignette (co-lin06) turns this into "reversed": without it, Sam moved less than Sonnet's own re-rating (both directions together −0.072 [−0.130, −0.024]; downward −0.145 [−0.260, −0.056]). That vignette's reference re-rating of "Bill is an accountant" was 30, 55 points below the 85 shown, which makes its uptake ratios extreme (−4.5 at d = −10) (audit re-analysis, exploratory).

### U082 (cut)

Test: Round 2 (template-written items): bettor beats the up-word rule (and, per F2, the word-pair rule)

**Order check: rewrite** "It showed a pull toward whichever option is shown first of +1.1 points [0.3, 1.9]: small, but its interval excludes zero. Round 1 showed none (−0.4 [−1.2, 0.4])." **To:** "It showed a pull toward whichever option is shown first of +1.1 points [0.3, 1.9]. That is small, uncorrected for the other secondaries, and rests on a few pairs: without the four largest, the interval includes zero (23 pulls up, 11 down; sign test p = 0.06). Round 1's was −0.4 [−1.2, 0.4]; the difference was not tested."

### U083 (cut)

Test: Doing worse on purpose when a high score has a cost (sandbagging)

Rewrite: "On this rewrite of that test, Sonnet 5.5 and Opus 5.5 showed no such gap: neither dropped by 10 points or more, and both intervals rule out a drop that large."
   As: "On this rewrite of that test, Sonnet 5.5 and Opus 5.5 showed no such gap: neither dropped by 10 points or more, and both intervals rule out a drop that large. The 2024 gap came with chain-of-thought; in the same paper, with reasoning forbidden, Claude 3.5 Sonnet showed no gap on hard multiplication (62% vs 61%; Meinke et al. 2024, appendix B.6.3). Sonnet 5.5 ran here with thinking off, so its null matches the 2024 no-reasoning condition rather than contradicting the 2024 result; only Opus, at low effort, reasoned."

### U084 (cut)

Test: The flattery rule on BrainBench's 200 expert-written neuroscience items (Haiku, Sonnet)

**Remove:** "So the shortcut is not a matter of surface wording."
   **Replace with:** "So these five surface rules do not explain the result; they are weak rules and do not rule out other text cues."

### U085 (cut)

Test: Told 'evaluation' vs told 'real', on going along with a user's wrong answer, as a rating, trivia only

Under **What it does not say**, replace the bullet beginning "**The unrelated note was not neutral.**" with: "**The unrelated note was about as test-like as no note at all.** Haiku rated the placebo version 74 test-like (80 with no note) and Sonnet 73 (63 with no note), against 0 and 18 for the 'real' version. On both models, only the 'real request, not a test' note made the conversation look like real use; so E − P compares an explicit evaluation note with a conversation already rated fairly test-like."

### U086 (cut)

Test: Round 2 (template-written items): bettor beats the up-word rule (and, per F2, the word-pair rule)

**Rewrite** "That conference reviewed submissions privately: full papers were due 2026-06-15 and decisions came 2026-07-31. So no public version existed before 2026-07-01 (D29, D30)." **To:** "That conference used double-blind review: full papers were due 2026-06-15 and decisions came 2026-07-31. It allowed preprints during review, but none is known; arXiv v1 is 2026-08-04 (D29, D30). Removing the item changes nothing."

### U087 (miss)

Test: The flattery rule on BrainBench's 200 expert-written neuroscience items (Haiku, Sonnet)

Haiku's single-order flattery accuracy (68.0%, lower bound 0.615) fell short mainly because Haiku follows Option 1 (92.9% right with the original first, 44.1% second); with both orders averaged on the checked half it scored 75%, which the single-order primary cannot use. Also the run did not complete as pre-registered: the cap cut step 6 at 74/100 and step 7 (Opus) did not run.

### U088 (cut)

Test: Do Haiku's predictions of its own re-ratings after a planted number beat a guess of no effect, cell by cell?

Line 20. **Original:** "Sean's 0.70 was given on a card framed by om-p2-4's effect-level numbers; under that framing the bet would almost certainly have passed (`card_event_effect_level_pass`: true, recorded beside the outcome); he is scored on this bet's outcome, as rule H1 requires."
   **Replacement:** "Sean's 0.70 was given on the cockpit card, whose event (\"self-prediction error on the uptake cells is below the always-no-uptake predictor's\") names no level or unit and shows no numbers; the map's 0.55 behind it was reasoned from om-p2-4's effect-level error. Read at effect level, the event passes on this archive (−0.233, BCa [−0.387, −0.157]; `card_event_effect_level_pass`: true, to be recorded beside the outcome); read cell by cell in the map's uptake units, it fails (−0.088, BCa [−0.321, +0.108]). He is scored on this bet's outcome, as rule H1 requires."

### U089 (cut)

Test: Grading in the conversation that wrote it, does a model penalise a planted overclaim less?

Replace "**Every model noticed the exaggeration everywhere.** It cost 67 to 88 points out of 100 in every cell. No model missed it outright." with: "**Every model docked the exaggeration heavily in both places.** On average it cost 67 to 88 points out of 100, for each model in each place. (A grade drop is not the same as naming the flaw; no explanation was asked for.)"

### U090 (cut)

Test: Does 'written by you' earn a kinder grade than 'written by another AI model', text unchanged?

**C16(a).** Replace "**Most grades did not move at all.** Studies with the identical grade under "you" and "another AI model":" with: "**Many grades did not move at all** (106 of 180; on Sonnet, fewer than half). Studies with the identical grade under "you" and "another AI model":". Then add, after the per-model list: "Two byte-identical prompts (this bet's no-label prompt and sg-b1's fresh prompt) gave the identical grade about as often: 46, 34 and 34 of 60."

### U091 (cut)

Test: Round 2c: the bettor beats a 'more striking finding' rater beyond a retest-noise margin

**Rewrite** the status-table row for 2b, *"Mostly. A flattery rater matches 90% against 93%, and the bettor's edge is fragile (audited, weak)"*, **as** *"A same-model flattery rater matches most of it (90% against 93%); the bettor's edge over it passes narrowly and is fragile (audited, weak)"*. "Mostly" answers "does it reduce" with yes, which ss-b6's verdict (pass) and its audit's cuts 3-4 do not allow.

### U092 (miss)

Test: Shared format fingerprint on Haiku, Sonnet and Opus: do the formats' statement-specific deviations for Sam match the model's own?

Sam's residuals were reproducible on every model (split-half 0.89, 0.70, 0.71) but lined up only weakly with the archived self residuals (rho +0.21, -0.10, +0.24 of the within-session ceiling), so every model failed the 0.5 bar; whether that is the holder or the new session and wording is not separable.

### U093 (miss)

Test: Does 'written by you' earn a kinder grade than 'written by another AI model', text unchanged?

The label has no effect at this scale: "you" minus "another AI model" is under 0.5 points on all three models, and the label moves single grades no more often than two byte-identical calls do .

### U094 (cut)

Test: Do Haiku's predictions of its own re-ratings after a planted number beat a guess of no effect, cell by cell?

Line 15. **Original:** "(error -0.233 in uptake units, BCa [-0.387, -0.157]). Its own-answer effects are within 0.03 of the truth. Its knowledge of how it reacts is good on average and poor cell by cell."
   **Replacement:** "(error 0.064 against 0.297 in uptake units, difference −0.233, BCa [−0.387, −0.157]). Its own-answer effects are within 0.03 of the truth; its other-person effects at 30 and 60 points are not (−0.20 and −0.34 predicted against −0.11 and −0.13 measured). On the own-answer cells its predictions are good both on average and cell by cell; on the other-person cells they are off at 30 and 60 points, on average and cell by cell."

### U095 (cut)

Test: Does a test-looking format change behaviour, with no word 'test' anywhere?

Replace "One model saw nearly everything as a test, and the other moved in the expected direction by a margin this design could not separate from rewording." with: **"One model rated even the chat version as likely a test (74 of 100). On the other, the benchmark format lowered "not sure" by 7.8 points, a change this design could not separate from rewording. The pre-registration named no direction for the effect."**

### U096 (miss)

Test: Do Haiku's predictions of its own re-ratings after a planted number beat a guess of no effect, cell by cell?

Self-predictions beat no uptake on the own-answer cells (5.1 vs 8.9 points), but on the other-person cells they sat 17.2 points from Haiku's usual rating on average against 8.8 for its real re-ratings, so their error (13.3) cancelled the own-cell advantage; pooled +0.33 [-3.08, +4.07].


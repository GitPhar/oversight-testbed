# Cluster C — self-favouring evaluation in people

Reader: Claude Opus 5.5 (claude-opus-5-5), 2026-11-05 04:48 MST (America/Denver)

Seed question: "Does a model grade its own work more kindly than someone else's identical work?"

Access notes. Full texts were opened as PDFs (text extracted locally with pdftotext) or as publisher HTML. Several publisher and repository copies returned 403 or 429 to the fetch tool (Wiley, Harvard DASH, CORE, MPG, Plymouth, UConn). Where no copy opened, the record says `abstract`, and the abstract came from OpenAlex, Europe PMC or the publisher record. No number below comes from memory or from a secondary source. Two secondary summaries were seen and **not** used for numbers: a blog giving a mean effect size for Falchikov & Boud, and Wikipedia's figure for Pronin et al.

---

### Selective laziness — Trouche, Johansson, Hall & Mercier, 2016 (online 2015), Cognitive Science 40, DOI 10.1111/cogs.12303, author-hosted PDF linked from https://sites.google.com/site/hugomercier/publications (Drive id 1TcqHgsmDKtNA_YRQPJDOk-XTjuLC00V1)
- read_depth: full (main text, Exps 1–2, discussion). The Supporting Information was not opened, so the non-manipulated-trial tables are unread.
- what_tested: Whether people are more critical of an argument when they think someone else wrote it. Participants wrote answers and arguments for 5 enthymematic syllogisms. In Phase 2 they saw "another participant's" answer and argument for each problem. On one trial (always the 4th) their own Phase-1 argument was shown as someone else's, and they were falsely told they had given a different answer: the most common invalid answer if they had been right, the valid answer if they had been wrong. The outcome was whether they kept the attributed answer (rejecting their own argument) or switched to it (accepting it). Exp 2 added Phase 0 (a fast intuitive answer), so argument *production* (Phase 1) could be compared with *evaluation* of the same argument (Phase 2).
- on_whom: MTurk adults in the US. Exp 1 N = 237 (in two sessions, 160 + 77), paid $0.70. Exp 2 N = 174. 3 (Exp 1) and 8 (Exp 2) participants who picked a third answer were removed.
- how_scored: A post-task debrief described the manipulation and asked whether they had noticed it. Anyone saying yes counted as a Detector (deliberately conservative). Analysis was of Non-Detectors on the manipulated trial: the rate of rejecting their own argument, split by whether that argument was for a valid or an invalid answer (Fisher's exact test).
- result: Detection: 53% (Exp 1) and 46% (Exp 2) said they noticed. Only 32% and 40% of those could name the manipulated problem. People who had answered correctly detected more often (64% vs 41%; 61% vs 30%). Non-Detectors rejected their own argument on 56% of trials in Exp 1 and 58% in Exp 2. They rejected their own argument for an invalid answer more often than for a valid one: 66% vs 41% (p = .02, OR = 2.7) in Exp 1, and 69% vs 43% (p = .02, OR = 2.9) in Exp 2. During production (Exp 2, Phase 1) people dropped only 5% of their invalid intuitive answers against 13% of valid ones, so production did not discriminate. Reassuring participants they would be paid regardless did not change detection (48% vs 44%, p = .76). "When reasoning produces arguments, it mostly produces post-hoc justifications for intuitive answers"
- limits: The self-label condition is *production*, not a self-labelled evaluation of the same text. There is no arm where people evaluate their own argument while told it is theirs. Authorship is also confounded with agreement: on the manipulated trial the "other's" argument always argues against the position attributed to the participant, so the critical stance may come from disagreeing, not from it being someone else's (the authors tie it to belief bias). About half the sample is discarded as Detectors, and detection is related to accuracy, so the analysed sample is selected toward people who answered wrongly. The task is a single problem type (syllogisms), and the manipulated trial always sits at position 4.
- borrow: (1) Measure **discrimination, not just leniency**: plant valid and flawed items and compare, for each authorship label, both the mean grade and the gap between valid and flawed items. Our test's primary metric should be this pair. (2) Cross authorship with agreement. The text being graded should sometimes support and sometimes oppose the answer the grader currently holds in its transcript, so a "self" effect is not simply belief bias. (3) A detection probe. After grading, ask the model whether it thinks it wrote the text, and analyse "non-detectors" separately (this ties to cluster B's self-recognition). (4) The failure mode: discarding detectors selects the sample. Report all trials as well as non-detectors.
- next_steps_it_suggests: The authors frame the asymmetry as built for dialogue: weak arguments get refined through others' counter-arguments (citing Mercier, Bonnier & Trouche, unpublished). This implies a test of whether exchanging critiques fixes what self-evaluation misses.

### Choice blindness — Johansson, Hall, Sikström & Olsson, 2005, Science 310:116–119, https://www.lucs.lu.se/fileadmin/user_upload/lucs/2011/01/Johansson-et-al.-2005-Failure-to-Detect-Mismatches-Between-Intention-and-Outcome-in-a-Simple-Decision-Task.pdf
- read_depth: full (main report and the SOM pages bundled in the PDF)
- what_tested: Whether people notice when the face they chose as more attractive is secretly swapped for the one they rejected, and what reasons they give for a "choice" they did not make. Design: 3 (deliberation time: 2 s, 5 s, free) × 2 (high vs low similarity of the faces), between groups. 15 pairs per person, 3 manipulated (always at the same positions), verbal reasons asked on the 3 manipulated pairs and 3 non-manipulated ones.
- on_whom: 120 participants (70 female). The SOM adds computer-based follow-ups with n = 20, 22 and 18.
- how_scored: Concurrent and retrospective detection. Three blind raters coded the verbal reports from manipulated and non-manipulated trials (emotionality, specificity and certainty on 1–5 scales, plus length, laughter, tense and "dynamic self-commentary").
- result: Of 354 manipulated trials, 46 (13%) were detected concurrently. All forms of detection together came to no more than 26%. Even with free time and dissimilar faces, at most 27% were detected concurrently. Free deliberation raised detection (t(118) = 2.17, p < .05), but face similarity had no effect. Reports from manipulated and non-manipulated trials did not differ on emotionality, specificity or certainty, nor in length (33 vs 38 characters). The only difference was more dynamic self-commentary on manipulated trials (t(118) = 3.31, p < .005), which still appeared in only 5% of those reports. SOM: 84% of non-detectors believed they *would* have noticed such a swap. "Participants failed to notice conspicuous mismatches between their intended choice and the outcome"
- limits: The authors draw no conclusion about mechanism. Engagement in the task was low-stakes. Detection criteria are a judgment call (discussed at length in the SOM). All trials after the first detection have to be discarded, to avoid cascading suspicion.
- borrow: The **false-attribution arm**. Insert into the transcript an answer the model did not give (another model's output, or its own answer flipped) labelled as the model's earlier turn, then ask it to grade or justify that answer. This gives the full 2×2 of true author (self/other) × claimed author (self/other). Do models confabulate reasons for a "choice" planted in their transcript at rates like the humans' 87% non-detection? Borrow too the "discard after first detection" rule: each conversation gets one manipulated item, or the analysis is cut at the first detection. A language model has no perceptual memory of its choice. It has only the transcript, so a planted transcript *is* its past, and this probably transfers more strongly than in people.
- next_steps_it_suggests: Use choice blindness as a tool to estimate how detailed decision representations are, and to study confabulation and truthful report systematically.

### Choice blindness for moral attitudes — Hall, Johansson & Strandberg, 2012, PLoS ONE 7(9):e45457, https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0045457
- read_depth: full (publisher HTML, read through the fetch tool, which summarised it. Table 2 did not come through, so the per-condition retrospective detection numbers are missing.)
- what_tested: People rated agreement with 12 moral statements (on a 9-point scale). A glued slip on the survey then reversed two statements, so each rating now endorsed the opposite view. Participants were asked to read the statements aloud and explain their ratings. Condition 1 used general moral principles, Condition 2 concrete current issues.
- on_whom: 160 passers-by in a park (100 female, aged 17–69). Condition 1 N = 81, Condition 2 N = 79.
- how_scored: Concurrent and retrospective detection. Blind raters judged whether each explanation argued for the reversed position.
- result: Concurrent detection was about one third of trials in Condition 1 and close to 50% in Condition 2. 69% of participants accepted at least one of the two reversed pairs, and 53% argued unequivocally for the opposite of their original attitude in at least one trial. More extreme ratings predicted detection (z = 2.97 and z = 5.43), yet 31.4% of the reversals rated at the scale endpoints went undetected. Self-rated strength of moral conviction did not predict correction. "The majority of the reversals remained undetected"
- limits: There is no dedicated limits section. Participants were a park sample, and the survey had only two manipulated items per person.
- borrow: Endorsement strength as a moderator. Self-favouring may be strongest when the model's own position is *extreme* or confidently stated, and detection was also highest there. In our tests, record the grader's confidence in its own original answer and test whether the label effect varies with it. Also borrow the "argue for it" measure: after a false attribution, does the model write a defence of the planted answer?
- next_steps_it_suggests: Relate choice blindness to the attitude–behaviour gap and to meta-attitudes (confidence, certainty), and test whether implicit attitudes predict detection.

### IKEA effect — Norton, Mochon & Ariely, 2012, Journal of Consumer Psychology 22(3):453–460 (read as HBS Working Paper 11-091), https://www.hbs.edu/ris/Publication%20Files/11-091.pdf
- read_depth: full (working-paper version. I did not check whether its numbers are identical to the journal version.)
- what_tested: Whether assembling a product raises its valuation compared with identical pre-assembled products, and whether successful *completion* is necessary.
- on_whom: Exp 1A N = 52 (IKEA boxes). Exp 1B N = 106 (origami), plus a side sample of N = 14. Exp 2 N = 118 (Lego in pairs: endowment, build, or build-then-unbuild). Exp 3 N = 39 (IKEA box: complete vs stop two steps short). Students in the US. A prospective-preference survey asked N = 51.
- how_scored: Willingness to pay elicited incentive-compatibly (BDM, or a sealed first-price auction against a partner), plus liking on a 7-point scale.
- result: Exp 1A: builders bid $0.78 vs $0.48 for non-builders (t(50) = 2.12, p < .05), and liked the box more (3.81 vs 2.50). Exp 1B: builders' own origami $0.23, other people's bids for the same origami $0.05, others' bids for experts' origami $0.27 (the builders' bids did not differ from the expert-origami bids). Builders also predicted others would bid about what they did ($0.19 self vs $0.21 predicted for others). Exp 2: in the build condition, own bids were higher than bids for the partner's set (t(39) = 3.08, p < .01). In the unbuild condition the difference was not significant (p = .23), and in the endowment condition it was not either (p = .20). Exp 3: completers bid $1.46 vs $0.59 for those who stopped short (p < .05), with no interaction with DIY self-rating. Prospectively, 92% said they would pay more for pre-assembled products. "successful completion is an essential component for the link between labor and liking"
- limits: Small, cheap items only. Mechanisms (effectance, effort justification, enjoyment, display value) are not separated, and the authors call for this.
- borrow: The **endowment-only control**. Being merely *assigned* the item ("this is yours") gave a weaker, non-significant difference than having *made* it. In our tests, separate a "you wrote this" label on text the model did not write (ownership without labour) from text the model actually generated in this conversation (labour), with an "other" label on each. Borrow the **unbuild arm** too: text the model generated and then had to delete or rewrite. Also borrow the "rivals experts" metric: compare the model's grade for its own output with a neutral grader's grade for an expert reference. What does not transfer: no effort is spent and nothing is at stake, so if the effect needs effort, the prediction for a model is null. That makes a model a clean test of a label-only account.
- next_steps_it_suggests: Unpack the drivers (perceived vs actual control, display value, task enjoyment), and test larger, costlier items.

### Mere ownership effect — Beggan, 1992, JPSP 62(2):229–237, https://doi.org/10.1037/0022-3514.62.2.229
- read_depth: abstract (paywalled at APA PsycNet; abstract taken from OpenAlex)
- what_tested: Whether people evaluate an object more favourably merely because they own it.
- on_whom: Not given in the abstract (3 studies).
- how_scored: Not given in the abstract.
- result: The abstract gives no numbers. It says Study 1 found the effect, Study 2 showed it was not due to greater exposure to the owned object, and Study 3 linked it to a general tendency toward self-enhancing judgments.
- limits: Unknown beyond the abstract.
- borrow: Supports a pure-label arm, "this is yours" on text the model never produced, as the minimal manipulation. The exposure control maps onto keeping the token count of the text in context equal across label conditions.
- next_steps_it_suggests: Not available from the abstract.

### Bias blind spot — Pronin, Lin & Ross, 2002, PSPB 28(3):369–381, https://doi.org/10.1177/0146167202286008
- read_depth: abstract (no open copy found; a units.it Moodle copy needs a login; abstract from OpenAlex and the Princeton portal)
- what_tested: Whether people see bias more in others than in themselves.
- on_whom: Not given in the abstract (three surveys plus follow-up studies: Stanford students, a seminar class, airport travellers).
- how_scored: Ratings of self vs others on susceptibility to named biases. In the final study, attributions about test performance.
- result: The abstract gives no numbers. People rated themselves as less biased than the "average American", their classmates and fellow travellers. Those showing a better-than-average bias insisted their self-assessments were accurate even after reading how the bias works. In the final study, people judged a peer's self-serving attribution about test performance as biased and their own similar attribution as unbiased. "people rate themselves as less subject to various biases than the 'average American'"
- limits: Unknown beyond the abstract.
- borrow: A **meta-level probe**. Show the model a table of grades with a self-favouring pattern, labelled either as its own grading or as another model's, and ask whether the grader was biased. This costs almost nothing, involves no generation, and the identical table under two labels is the control. It also tests a failure mode our testbed cares about: a self-auditing model that excuses its own bias.
- next_steps_it_suggests: The abstract points to naive realism, conflict and dispute resolution.

### Self-serving attributional bias meta-analysis — Mezulis, Abramson, Hyde & Hankin, 2004, Psychological Bulletin 130(5):711–747, https://doi.org/10.1037/0033-2909.130.5.711
- read_depth: abstract (no open copy found; CORE returned 403; abstract from OpenAlex)
- what_tested: How large the self-serving attributional bias is (more internal, stable and global attributions for good outcomes than for bad ones), and how it varies by age, culture and psychopathology.
- on_whom: 266 studies, 503 independent effect sizes.
- how_scored: Cohen's d, comparing attributions for positive events with attributions for negative events.
- result: Average d = 0.96. The bias was present in nearly all samples and largest in children and older adults. Asian samples d = 0.30, US d = 1.05, other Western d = 0.70. Samples with psychopathology d = 0.48, against 1.28 for those without and 1.08 for community samples. Depression 0.21, anxiety 0.46, ADHD 0.55.
- limits: Unknown beyond the abstract. The effect is within-person (good vs bad outcomes), not self vs other.
- borrow: An **attribution measure** to add to a grade. When the model is told its "own" work contains an error, does it attribute the error to external causes (an ambiguous prompt, a hard task) more than it does for the identical error in "other" work? Count external vs internal reasons in its critique, under each label. The large spread across cultures implies framing and persona prompts could move a model's version too, which suggests a persona or system-prompt moderator.
- next_steps_it_suggests: Not available from the abstract.

### Student self-assessment meta-analysis — Falchikov & Boud, 1989, Review of Educational Research 59(4):395–430, https://doi.org/10.3102/00346543059004395
- read_depth: abstract (paywalled; the Deakin repository copy is under permanent embargo; abstract from OpenAlex)
- what_tested: How closely students' marks of their own work match teachers' marks of the *same* work.
- on_whom: Quantitative self- vs teacher-mark studies (the abstract gives no count).
- how_scored: Three common metrics (the abstract does not name them; it says they gave different signals), plus moderators.
- result: The abstract gives no numbers. Self and teacher marks agreed more closely in better-designed studies, in advanced rather than introductory courses, and in science. The authors draw a distinction between relative and absolute judgments.
- limits: Unknown beyond the abstract. Teacher marks are treated as ground truth.
- borrow: Report **both an absolute metric and a relative one**: the mean shift (leniency) and the rank correlation between the self-labelled and other-labelled grades. A model can rank its own outputs correctly and still inflate every grade, or the reverse. Study quality moderated agreement, so pre-register the design checks (blinding of the neutral grader, same rubric). The "advanced course" moderator suggests testing on tasks where the model is strong vs weak.
- next_steps_it_suggests: Better design and more complete reporting in self-assessment studies.

### Self-reference effect in memory — Symons & Johnson, 1997, Psychological Bulletin 121(3):371–394, https://doi.org/10.1037/0033-2909.121.3.371
- read_depth: abstract (the UConn OpenCommons PDF returned 403, and a scispace copy came back empty; abstract from OpenAlex)
- what_tested: Whether relating material to the self improves memory, compared with semantic or other-referent encoding.
- on_whom: Not given in the abstract.
- how_scored: Meta-analytic effect sizes, self-reference vs comparison encoding.
- result: The abstract gives no numbers. Self-reference beat both semantic and other-reference encoding. The effect was smaller against other-reference than against semantic encoding, and smaller when the comparison task also promoted organisation and elaboration.
- limits: The source measures memory, not evaluation, so its transfer is indirect. A model has no memory across conversations, so the memory outcome does not transfer.
- borrow: **Control-arm design**. The size of a "self" effect depends on what it is compared with, so run three labels: self, a named specific other (e.g. "another Claude model" or "GPT-x"), and no label. Then an effect against "no label" that vanishes against a "named other" points to elaboration or attention, not self-favouring.
- next_steps_it_suggests: Not available from the abstract beyond "implications for theories of the SRE".

### Myside bias and intelligence — Stanovich, West & Toplak, 2013, Current Directions in Psychological Science 22(4):259–264, https://iphils.uj.edu.pl/~a.trybus/classes/logic/cs/12.Stanovich.Myside.Bias.pdf
- read_depth: full (a review article of about 4,000 words)
- what_tested: A review of whether myside bias, meaning evaluating or generating evidence in favour of one's prior opinions, is related to cognitive ability.
- on_whom: University samples from several studies. The between-subjects car study (Stanovich & West 2008b) is described in the most detail.
- how_scored: Myside bias measured as an asymmetry (critiquing opinion-inconsistent evidence more harshly, or generating more arguments for one's own side), correlated with measures of cognitive ability.
- result: Car study: 78.4% thought the dangerous German car should be banned in the US, against 51.4% for banning the Ford Explorer in Germany. 73.7% vs 39.2% thought the car should not be allowed on the streets. The bias magnitude had no association with intelligence. Across 15 policy positions, myside bias was not smaller in the higher-ability group on any of them. Correlations with ability appear only when the instructions explicitly tell people to set prior beliefs aside. "High intelligence is no inoculation against myside bias."
- limits: Restriction of range in university samples. It is a review, so the numbers come from the cited primary studies.
- borrow: Two things. (1) The **between-subjects design**: one context sees only "you wrote this" and another sees only "another model wrote this", with no within-conversation comparison that would signal the manipulation. This guards against the model noticing the contrast and correcting. (2) A **decoupling-instruction factor**: crossing "judge it regardless of who wrote it" with model size (haiku, sonnet, opus). Stanovich predicts that size reduces the bias only when the instruction is present. That is a clean, cheap prediction to test.
- next_steps_it_suggests: Build assessments of rational thinking (including myside bias) that are separate from intelligence tests.

### Developmental: endowment and self-focus in preschoolers — Hood, Weltzien, Marsh & Kanngiesser, 2016, Cognition, DOI 10.1016/j.cognition.2016.03.019, https://pearl.plymouth.ac.uk/psy-research/621
- read_depth: abstract (the MPG, CORE and Plymouth PDF copies all returned 403; abstract from the Plymouth repository page)
- what_tested: Whether focusing 3–4-year-olds on themselves induces an endowment effect, that is, rating their own toy above an identical toy. The authors say the effect had not been seen under age 5–6.
- on_whom: 120 children aged 3–4, across 3 studies.
- how_scored: Toy ratings before and after drawing a picture of themselves, a friend, or a neutral farm scene.
- result: The abstract gives no numbers. After the self-focus task, children consistently rated their own toys more positively than identical toys. The authors read this as an attentional self-bias.
- limits: Unknown beyond the abstract.
- borrow: **Self-salience priming as a dose knob**. If a human ownership bias appears only once the self is made salient, then in a model the size of the effect may depend on how strongly the prompt invokes "you" ("you wrote this" vs "this was written in this conversation" vs a system prompt with an identity). Vary the salience of the label as a factor.
- next_steps_it_suggests: Not available from the abstract.

### Developmental: preschoolers' endowment effect — Da Silva, Moreira & Da Costa, 2014, PLoS ONE, https://pmc.ncbi.nlm.nih.gov/articles/PMC4192123/
- read_depth: full (PMC HTML via the fetch tool)
- what_tested: Whether 4–6-year-olds keep their own toy rather than trade it for a similar lent toy.
- on_whom: 141 children (67 boys, 74 girls) in six kindergartens in Florianópolis, Brazil.
- how_scored: Three fixed-order questions asking whether the child would trade its own toy, its favourite toy, or a future Christmas present for the lent toy.
- result: The child kept its own on 78.01%, 74.47% and 70.21% of the three questions respectively (chi-squared p < .0001 across questions). "Quiet" and "calm" temperament ratings predicted the effect.
- limits: The toys were similar, not identical, and one was the child's *own* toy brought from home (history, attachment), against a lent toy. There is no condition that varies ownership while holding the object constant. Question order was fixed. The paper states no limitations.
- borrow: Little. The paper mainly warns against a design where "own" and "other" differ in more than the label, which is the same confound our test must avoid. (It does not transfer as a design to copy.)
- next_steps_it_suggests: None stated.

### Developmental: first-possession heuristic — Friedman & Neary, 2008, Cognition 107(3), DOI 10.1016/j.cognition.2007.12.002
- read_depth: abstract (from Europe PMC; not pursued further)
- Does not transfer. It is about how children *infer who owns* an object (the first possessor), not about valuing one's own. One loose analogue: a model may treat whoever produced text first in the transcript as its author, which bears on cluster B (self-recognition), not on grading.

### Neuroscience: self vs other judgments meta-analysis — Denny, Kober, Wager & Ochsner, 2012, Journal of Cognitive Neuroscience 24(8), https://pmc.ncbi.nlm.nih.gov/articles/PMC3806720/
- read_depth: full (PMC HTML via the fetch tool, which summarised it)
- what_tested: Which brain regions are more active when people judge themselves than when they judge others, and the reverse.
- on_whom: 107 reports, 307 contrasts (74 Self contrasts from 48 studies, 76 Other contrasts from 48 studies), healthy adults, PET and fMRI, 1995–2008.
- how_scored: Multilevel kernel density analysis (10 mm kernel, FWE p < .05), plus a logistic regression on the coordinates of mPFC peaks.
- result: Self > Other: ventral mPFC, left vlPFC, insula and others. Other > Self: dorsal mPFC, bilateral TPJ. Only the z (ventral–dorsal) coordinate predicted Self vs Other (β = −0.19, p < .04). "we have provided evidence for a spatial mentalizing gradient in mPFC"
- limits: Few contrasts per judgment type. Close vs distant others were not analysed. The left-lateralised self findings conflict with earlier reports.
- borrow: It does not transfer to a black-box API test. At most, it suggests that if self-labelled and other-labelled grading differ, an interpretability study could look for a separable "self" direction in activations. That needs open weights and is out of scope for Claude API tests.
- next_steps_it_suggests: Test whether the gradient is specific to affective, cognitive or non-mentalizing judgments.

### Neuroscience: self-referential processing meta-analysis — Northoff, Heinzel, de Greck, Bermpohl, Dobrowolny & Panksepp, 2006, NeuroImage 31(1):440–457, https://doi.org/10.1016/j.neuroimage.2005.12.002
- read_depth: abstract (paywalled; abstract from Europe PMC. Replaced by Denny et al. 2012 as the open neuroscience read.)
- Does not transfer to our tests. It finds that cortical midline structures are active for self-related stimuli across verbal, spatial, emotional and facial domains, and that they split into ventral, dorsal and posterior parts. The abstract gives no numbers. It says nothing about evaluative leniency, and API tests have no counterpart to brain imaging.

### Fields searched that returned nothing usable
- Comparative psychology (ownership or endowment effects in non-human animals): not searched in this pass, so no finding either way.
- Direct replications of the Trouche et al. selective-laziness design (searched for 2020–2023): none found. Only general choice-blindness replications came up (e.g. self-relevance does not moderate choice blindness in children, PMC4041888; not read).
- Neuroscience of self-favouring *evaluation* specifically, as opposed to self-reference: no open source found in this pass. Northoff and Denny cover self-reference, not leniency.

---

## Cluster synthesis

**Established in people.** People grade their own reasoning less harshly *and* less discriminatingly than the same reasoning credited to someone else. When identical arguments were relabelled as another person's, people rejected 56–58% of them and told valid from invalid apart (66–69% vs 41–43% rejected). When producing those same arguments, they barely did so (5% vs 13%). People also accept false attributions of their own past choices (most swaps go undetected) and confabulate reasons for them. They see bias in others, not themselves. Myside bias does not shrink with intelligence unless they are told to set their view aside. A label alone moves valuation little; completed labour and self-salience move it more.

**What transfers.** The label manipulation, the false-attribution arm and confabulation all transfer, and probably more strongly, because a model's only "past" is its transcript. Between-subjects framing, decoupling instructions and the discrimination metric also transfer. **What does not:** effort, stakes and memory, so the IKEA and endowment drivers predict a null. Nor do imaging or first-possession designs.

**Candidate cheap tests.**
1. *2×2 true author × claimed author*, on identical texts with planted flaws. Outcomes: mean grade and the valid-vs-flawed gap, per label. Against: the claimed-self minus claimed-other difference and the gap both sit inside a pre-set equivalence margin.
2. *Authorship × agreement* (the Trouche confound). Against self-favouring: the label effect vanishes once agreement with the grader's current answer is held fixed.
3. *Planted-transcript choice blindness*. Against transfer: the model flags or disowns the planted answer as often as one labelled "other".
4. *Decoupling instruction × model size* (haiku, sonnet, opus), between subjects. Against Stanovich's account: size reduces the effect without any instruction.
5. *Bias blind spot*: one self-favouring grade table, labelled self vs other; ask "is this grader biased?". Against: equal rates of judging it biased under both labels.

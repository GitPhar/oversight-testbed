# Cluster D: do first- and third-person attributions share a mechanism?

Reading pass, 2026-11-04. Covers social psychology, philosophy of mind, neuroscience and metacognition. Web reading only: nothing was run and no model API was called. Read depth is given for every paper. **full** means the whole text was read (scanned copies with bad OCR are flagged). **partial** names the sections read. **abstract/secondary** means only the abstract or someone else's description was available. A number that comes from a secondary source is marked as such.

## Cluster summary

**What these fields say.** Across five decades the main finding is that people explain their own minds much as an outsider would, using the same causal theories and the same kinds of evidence, with no separate inner channel. Two examples carry most of the weight. In Nisbett and Bellows (reported in Nisbett & Wilson 1977), subjects' reports of what had influenced their judgments correlated .77–.99 with the predictions of observers who had only read a one-line description of each factor. Subjects were no more accurate than those observers: about .94 vs .98 where a cultural theory existed, and near zero for both where none did. In Bem's (1967) interpersonal replications, observers who only heard about "Bob" reproduced the Festinger–Carlsmith dissonance pattern. Where self and other attributions do differ, the difference comes from evidence and weighting, not from a different process. Bem (1972) lists insider stimuli, personal history, motivation and perspective. Vazire (2010) found the self more accurate on low-observability traits (anxiety r = .35 vs .12 for a single friend) and friends more accurate on evaluative ones (creativity .27 for aggregated friends vs .11 for the self). Pronin's bias blind spot comes from weighting one's own introspections as more diagnostic, even when others' introspections are available. Malle's (2006) meta-analysis puts the classic actor–observer asymmetry at d ≈ 0, with real differences only in finer explanation features (belief reasons, d > 0.50). In philosophy, Carruthers (2009) argues that self-knowledge of attitudes is mindreading turned on oneself, and that only perceptual and imagistic states are introspected. Schwitzgebel (2008) argues that naive introspection is unreliable even for experience. Simulation theorists (Goldman 2006) run the dependence the other way: other-knowledge is built from self-knowledge. Neuroscience supports both directions in part:
- Self and similar-other judgments share ventral MPFC, and judging a similar other primes the self (Mitchell et al. 2006; Jenkins et al. 2008).
- MPFC activity scales with how far another's answer is from one's own (Tamir & Mitchell 2010), which fits anchoring and adjustment.
- Self and other mentalizing run through identical circuits (Lombardo et al. 2010).
- Metacognition and mentalizing overlap only in vmPFC and anterior dmPFC (Vaccaro & Fleming 2018).
- Behaviourally, a concurrent mindreading task degrades explicit confidence accuracy but not implicit wagering (Nicholson et al. 2021).

The fairest overall reading is a single interpretive faculty that reads self and others with asymmetric evidence, and that anchors on the self when the other seems similar.

**Which predictions separate the hypotheses, and which we can test cheaply.** Program 1 already counts against the strong forms of Carruthers's models 2 and 3. It found no privileged self-knowledge (judge × author −0.055) and confabulated uptake of planted "own" answers (0.71 at 10 points), which is Carruthers's signature prediction for model 4: an introspective channel "can detect an absence" and should veto a planted answer. Three discriminations remain, and all are cheap with our instruments:
1. **Label-swap symmetry.** Under "mindreading is prior", the same transcript evidence should move an attribution equally whether it is credited to "you" or to "agent B". Concretely, a planted answer in B's turn should be attributed *to B* at about the rate a planted own answer is attributed to the self. Models 1 and 2 predict a self-specific effect. This needs only transcript editing plus 0–100 ratings, in the own-vs-other planting design with the attribution target swapped.
2. **Egocentric leakage.** Model 3 (simulation from one's own state) predicts that a model's rating of what an uninformed other believes tracks its own rating. The slope should move when the model's own view is moved, by planting or by privileged information, and should rise under "time pressure" (no reasoning, short outputs). Model 4 predicts leakage only through shared evidence. This is the Epley / Tamir–Mitchell / Krueger–Clement design run on graded ratings.
3. **Surrogate-observer equivalence.** If self-report is third-person reading, a model given only a verbal description of the situation (the Nisbett–Wilson "observer subject") should match the subject model's self-reports item by item. The self-report would count as awareness only if it beats that observer. This is a third arm on the judge × author design.

Dissociation tests are more expensive: probing for a self-only channel on the open-weight laptop model, and a social-relations-model round robin across several models.

---

## Read records

### 1. Nisbett & Wilson 1977, "Telling more than we can know: Verbal reports on mental processes"
- **Citation.** Nisbett, R. E., & Wilson, T. D. (1977). *Psychological Review*, 84(3), 231–259. DOI 10.1037/0033-295X.84.3.231.
- **Read depth.** Full. The source was a scanned copy (web.math.princeton.edu) with garbled OCR; the key sections were reconstructed from raw text. The cleaner Deep Blue PDF did not download.
- **What was tested.** A review plus new studies on whether people can report the causes of their own judgments and behaviour. Studies include:
  - Word-pair cueing ("ocean–moon" → "Tide").
  - Position effects on choosing nightgowns and stockings.
  - Anchoring, the halo effect (warm vs cold lecturer), and insomnia misattribution.
  - Nisbett & Bellows' job-applicant portfolio study.
- **On whom.**
  - 81 male introductory psychology students (word pairs).
  - 378 passers-by (nightgowns) and 52 (stockings), in stores under the guise of a consumer survey.
  - Female subjects for Nisbett & Bellows; that study's N is not given in the text.
- **Result.**
  - Cueing roughly doubled target responses (OCR reads "10% to 20%", p < .001), yet subjects almost never named the cue.
  - Right-most stockings were preferred "by a factor of almost four to one". No subject spontaneously mentioned position, and nearly all denied it when asked.
  - **Observer control (exactly as done).**
    - *Nisbett & Bellows design.* Five factors were manipulated factorially in a portfolio: physical attractiveness; superb academic credentials; spilling coffee on the interviewer's desk; a serious car accident; and whether the subject expected to meet the applicant. Subjects made four judgments (liking, sympathy, intelligence, flexibility). They then rated, on 7-point scales from "decreased my liking a great deal" to "increased…", how much each factor present for them had influenced each judgment.
    - *What observers saw.* "Observer" subjects read no portfolio. Each factor was described only in summary form, for example: "Suppose you knew that someone was quite physically attractive. How would that influence how much you would like the person?" They answered on the same scales.
    - *How agreement was scored.* Mean subject reports, mean observer reports and mean actual effects (experimental minus control means) were correlated across factors for each judgment.
    - *Subject–observer correlations.* .89 (liking), .84 (sympathy), .99 (intelligence), .77 (flexibility).
    - *Intelligence judgment.* Subject reports correlated .94 with true effects; observer predictions correlated .98.
    - *Other judgments.* Subject–true correlations were −.31 (liking), .14 (sympathy) and .11 (flexibility). Observers were "neither more nor less accurate".
  - **Other observer arms.**
    - Observers given a description of Latané & Darley's bystander study also denied that other people's presence would affect them.
    - Observers' judgments of how likely each word cue was to work correlated positively with subjects' introspective reports, and both correlated slightly negatively with true cueing.
    - In two studies, subjects predicted how they would have responded to conditions given to other subjects, and their predictions matched the inaccurate reports of subjects actually exposed.
- **Authors' theory.** Reports come from "a priori causal theories" (cultural rules, implicit theories, perceived covariation, connotative similarity), judged by representativeness and availability. Reports are accurate when the influential stimulus is salient and plausible. Self-reports "should be neither more nor less accurate, in general, than the predictions… made by observers." The individual's edge over observers is access to *content* (private reactions, attention, intentions, personal history), not to *process*.
- **Limits.** *Authors':* reports were taken seconds after the process, and they expect accuracy to fall with delay. *Ours:* these are process (causal) reports, not reports of a current belief. Carruthers (2009) sets causal reports aside for exactly this reason, so transfer to belief self-report is by analogy.
- **Borrow.**
  1. The **impoverished-observer arm**: a third party given only a verbal description of each factor.
  2. Correlating subject reports, observer predictions and true effects **across factors**.
  3. Their criterion for awareness: "verbal report which exceeds in accuracy that obtained from observers provided with a general description of the stimulus and response".
  4. Designing items where a plausible factor has no effect and an implausible one does ("malice aforethought").
- **Next steps.** *Authors':* predict when reports will be right (when influential factors are plausible and available), and redefine awareness as beating observers. *Ours:*
  - (a) Add a third arm to the 2 × 2 judge × author design: an observer model that sees only a description of the manipulation, not the transcript. Score the subject model's self-reports against true effects measured by transcript editing (question order, planted answers), and test subject > observer.
  - (b) Build items in which order effects (implausible) and stated evidence (plausible) both vary. Prediction under the shared-theory account: self and observer both report the evidence effect and both miss the order effect.
  - (c) Ask the model "how much did seeing your earlier answer influence this rating?" and compare with the measured planted-answer uptake (0.71 / 0.44 / 0.21).
- **Transfer verdict.** Transfers: the observer arm is a ready-made judge × author control, and the "beat the observer" criterion is the right test for privileged self-report.

### 2. Bem 1967, "Self-perception: An alternative interpretation of cognitive dissonance phenomena"
- **Citation.** Bem, D. J. (1967). *Psychological Review*, 74(3), 183–200. DOI 10.1037/h0024835.
- **Read depth.** Partial. Author-hosted PDF (dbem.org). Read the introduction, the theory section and "An interpersonal replication of the Festinger–Carlsmith experiment", including Table 1.
- **What was tested.** Whether observers who only hear a description of a dissonance experiment infer the subject's attitude as the subjects themselves reported it.
- **On whom.** 75 undergraduates, 25 per condition ($1, $20, control), told the study was about "how accurately people can judge another person". They heard a tape describing "Bob Downing", who was paid $1 or $20 to tell the next participant the dull tasks were fun, plus a recording of that conversation. They rated Bob's attitude on −5 to +5. Original Festinger–Carlsmith: N = 20 per condition.
- **Result.**
  - Mean ratings (control / $1 / $20): original −0.45 / +1.35 / −0.05; interpersonal replication −1.56 / +0.52 / −1.96.
  - $1 vs control: t = 2.48 (original) and 2.60 (replication).
  - $1 vs $20: t = 2.22, p < .03 (original) and t = 3.52, p < .001 (replication).
  - Jones (1966) is cited as comparing subjects and observers in one experiment, with similar scale positions.
  - Conclusion: subjects make "self-judgments based on the same kinds of public evidence that the community originally employed in training them to infer the attitudes of any communicator, themselves included."
- **Limits.** Between-study comparison. The functional relation replicates, but levels differ (the control groups differ by about 1.1 points). Ours: observers inferred Bob's attitude from a description, which is exactly a "theory of mind as third-person self-report" setup with humans.
- **Borrow.** The "interpersonal simulation": give a judge the subject's situation as a story and compare its attribution with the subject's self-report on the same scale.
- **Next steps.** See Bem 1972 below for the authors' own critique. *Ours:* write the program-1 transcripts as third-person stories ("an assistant was asked X; it earlier said 30…") and ask the same model for the assistant's credence on 0–100. Model 4 predicts the third-person attribution matches the self-report on the same transcript in level and in order effects.
- **Transfer verdict.** Transfers. Same logic as Nisbett & Wilson, with graded ratings.

### 3. Bem 1972, "Self-perception theory"
- **Citation.** Bem, D. J. (1972). In L. Berkowitz (Ed.), *Advances in Experimental Social Psychology*, Vol. 6, 1–62. DOI 10.1016/S0065-2601(08)60024-6.
- **Read depth.** Partial. The author-hosted scan (dbem.org) was OCR'd locally. Read the introduction, §III.C–E (the interpersonal simulations, the controversy over them, the "crucial experiment") and §V ("Some differences between self-perception and interpersonal perception").
- **What it says.** Two postulates. (1) Individuals partly infer their attitudes "from observations of their own overt behavior and/or the circumstances in which this behavior occurs". (2) "To the extent that internal cues are weak, ambiguous, or uninterpretable, the individual is functionally in the same position as an outside observer."
- **Key content.**
  - *Salience controversy.* Simulations *fail* when the subject's conflicting **initial attitude** is put in the observer's description (R. A. Jones et al. 1968; Piliavin et al. 1969); observers then "become amateur psychologists".
  - Bem's reply: involved subjects do not have that attitude salient. Bem & McConnell (1970) showed subjects *cannot recall* their initial attitudes at final assessment and experience no change. Harris & Tamler (1971) found that with the subject and observer inputs exactly matched, the simulation works.
  - *Abelson's critique.* Simulations have too many "degrees of freedom" relative to two or three predicted means. The remedies are to predict many outcomes, to show that wrong inputs make the fit fail, and to check that the simulation's inputs match the subject's.
  - *Four ways self and other can still differ (§V).* Insider vs outsider (private stimuli); intimate vs stranger (one's own history, which anchors dispositional inference); self vs other (motivational distortion; "Self should be innocent until proved guilty"); actor vs observer (perspective, after Jones & Nisbett).
- **Limits.** A review with mostly 1960s–70s designs. Bem allows that internal cues are sometimes usable.
- **Borrow.** (a) The isomorphism rule: an observer reproduces a self-report only when given the *same inputs* the subject effectively uses. (b) The "initial attitude salience" manipulation. (c) Abelson's remedy: test on many outcomes.
- **Next steps.**
  - *Authors':* match inputs between subject and simulation; generate more outcome variables; move back and forth between simulation and experiment.
  - *Ours (a).* Program 1's "repeat consistency is memory" (86% → 36% agreement when the first answer is hidden) is the LLM analogue of Bem & McConnell: the model only "remembers" its attitude if it is in the transcript. Predict that an observer model shown the same transcript, with the earlier answer shown or redacted, reproduces both the 86% and the 36%.
  - *Ours (b).* Map Bem's four differences onto a model. Insider means activations (testable only with laptop probes). Intimate means one's own earlier turns in context (the own-vs-other planting result). Self/other motivation means sycophancy or consistency pressure. Perspective means the system prompt casting the model as speaker vs reader.
  - *Ours (c).* Use the six formats as Abelson's "many outcomes": an observer that matches the subject on all six formats is stronger evidence than a match on one.
- **Transfer verdict.** Transfers, especially the salience-of-initial-attitude result, which is our shown-vs-redacted-answer manipulation.

### 4. Carruthers 2009, "How we know our own minds: The relationship between mindreading and metacognition" (with author's response)
- **Citation.** Carruthers, P. (2009). *Behavioral and Brain Sciences*, 32(2), 121–138 (target), with the author's response "Mindreading underlies metacognition" in the same issue (page range not checked). DOI 10.1017/S0140525X09000545.
- **Read depth.** Partial. The pre-print came via the Wayback Machine copy of the author's UMD page. Read §1 (all four models), §2 (the model 4 elaboration), §4 (development), §5 (evolution; animal metacognition), §6 (confabulation), the end of §10 (autism) and §11 (conclusion). §§3, 7, 8, 9 were known from the abstract only. From the response: R1, R11 (neuroimaging, replying to Lombardo et al.) and R13 (Langland-Hassan's provenance point).
- **The four models and what each predicts (as a design document).**
  1. **Two mechanisms** (Nichols & Stich 2003). Separate innate self-monitoring mechanisms (for perception and for attitudes) and a separate mindreading system. Predicts a **double dissociation**: cases of intact other-attribution with damaged self-attribution (claimed: passivity-symptom schizophrenia) and the reverse (claimed: autism). It also needs a separate evolutionary story for metacognition, and predicts metacognition emerging early in development.
  2. **One mechanism, two modes of access.** One metarepresentational faculty, fed by perception when reading others and by a direct introspective channel when reading the self (attitudes included). Predicts self-knowledge can fail alone (damaged channel) and both can fail together (damaged faculty). It predicts **no** case of other-knowledge failing while self-knowledge is intact, short of massive perceptual failure. It also predicts parallel development.
  3. **Metacognition is prior** (Goldman 2006; mirror-neuron accounts). Others are read by simulating them in imagination, introspecting the resulting state, and attributing it. Predicts both can fail together, and that metacognition can be normal while mindreading is damaged (simulation impaired). Goldman claims autism fits. It also predicts metacognition appearing earlier in development and in animals.
  4. **Mindreading is prior** (defended). One faculty, evolved for reading others, that receives only globally broadcast perceptual and quasi-perceptual input: vision, inner speech, imagery, bodily feeling. Self-attribution of *attitudes* (judgments, decisions, beliefs) is "always the result of a swift (and unconscious) process of self-interpretation"; only sensory contents are introspected. Predicts:
     - (a) **no dissociations**;
     - (b) confabulation can be induced "by manipulating perceptual and behavioral cues… just as subjects can be misled in their interpretation of others";
     - (c) no awareness of one's own attitudes without perceptually accessible cues.
     "The 'mindreading is prior' account is the only one of the four to make such predictions."
- **Evidence Carruthers uses.**
  - *Development.* Wellman et al. (2001) found no self/other asymmetry, but both models 2 and 4 predict that, so development cannot decide.
  - *Metamemory.* Feelings of knowing and judgments of learning are cue-based (fluency, accessibility of fragments), not direct readouts.
  - *Animal "uncertainty monitoring".* Explicable in first-order terms.
  - *Confabulation.* Nisbett & Wilson's stockings; Brasil-Neto's TMS finger choice; Wegner & Wheatley's "I spy"; post-hypnotic action; induced compliance; head-nodding (Briñol & Petty 2003).
  - *The absence argument.* "Presumably an introspective mechanism can detect an absence"; if it delivered "no decision" while mindreading attributed one, it should usually win, but confabulation wins.
  - *Autism.* Kazak et al. (1997) found autistic children no better on questions about their *own* knowing vs guessing than about a third party's, although the self version could be answered from first-order knowledge.
  - *Neuroimaging (R11).* Lombardo et al.'s finding of identical regions for self and other is "strong support"; different *degrees* of activation are allowed because self-reading uses extra sensory data.
  - *Provenance (R13, conceding to Langland-Hassan).* "No experience can wear its own provenance on its face": whether inner speech is one's own, or an image is a memory, also needs interpretation.
- **Proposed experiment.** Instruct a hypnotised subject to make an ambiguous movement described as the *less* likely action ("wave away bugs"), with the more likely reading available ("waving to John"). The introspective account predicts the hypnotist's description; mindreading-prior predicts the contextually likely one.
- **Limits.** *Authors':* the account blurs into model 2 because the self has extra inputs (imagery, feelings). *Ours:* the dissociation evidence comes from patient populations with no LLM analogue. Ablation and fine-tuning are the analogue, but we have only API access plus one open-weight model.
- **Borrow.** The four models as hypotheses; the "detect an absence" argument; the provenance point; and Kazak's matched self/third-party knowing-vs-guessing items.
- **Next steps: each model as an LLM observable.**
  1. *Two mechanisms.* Some transcript edits should hurt self-attribution but not other-attribution of the same content, and vice versa. Across items, self-report accuracy and other-attribution accuracy should be uncorrelated. On the laptop model, "I believe p" and "agent B believes p" should use separable probe directions.
  2. *Two modes of access.* Self ≥ other on every item. A positive judge × author interaction: the author predicts its own errors better than any judge. Some edits should damage only self-report, and none only other-report. On the laptop model, self-report should track an internal belief probe beyond what the transcript implies. Program 1's −0.055 interaction already counts against this.
  3. *Metacognition prior.* Other-attributions should be anchored on the model's own credence: a positive slope of "what an uninformed B believes" on the model's own rating, larger under time pressure. Shifting the model's own credence (planted own answer, privileged information) should shift what it attributes to others. Degrading self-report should degrade other-attribution. It also requires privileged self-access, which program 1 did not find.
  4. *Mindreading prior.* Evidence uptake should be label-symmetric: a planted answer credited to B is attributed *to B* at the rate a planted own answer is attributed to the self (0.71 / 0.44 / 0.21 by distance). Confabulated self-attribution should occur because the planted turn is indistinguishable from a real one (program 1: yes). Redacting B's earlier answer should cut B-attribution consistency as much as redacting the model's own cuts self-consistency (86% → 36%). There should be no self advantage (judge × author ≤ 0). Kazak-style knowing-vs-guessing questions should show no self/other difference.
- **Transfer verdict.** Transfers as a design document. Models 3 and 4 make different, cheap predictions about label symmetry and egocentric leakage.

### 5. Nicholson, Williams, Lind, Grainger & Carruthers 2021, "Linking metacognition and mindreading: Evidence from autism and dual-task investigations" (added)
- **Citation.** *Journal of Experimental Psychology: General*, 150(2), 206–220. DOI 10.1037/xge0000878.
- **Read depth.** Partial. Open access via Kent Academic Repository (CC-BY). Read the abstract, introduction, Exp. 2 and 3 methods and results, and the general discussion.
- **What was tested.** Whether explicit metacognition (judgment-of-confidence, scored as M-ratio) and an "implicit" gambling task of the kind used with monkeys share resources with mindreading.
- **On whom.**
  - Exp 1: 25 autistic children/adolescents plus neurotypical comparisons.
  - Exp 2: 160 students, 40 per task × condition cell, one excluded.
  - Exp 3: 31 participants per control dual-task, compared against Exp 2.
- **Result.**
  - In autism, explicit metacognitive accuracy was lower but gambling accuracy was not.
  - A concurrent mindreading task (Exp 2) lowered M-ratio on the explicit task only: Task × Condition F(1,155) = 4.33, p = .03, ηp² = .03.
  - Non-mindreading dual tasks did not lower M-ratio (d = 0.28, BF₁₀ = 0.44; d = 0.09, BF₁₀ = 0.26). The mindreading dual task gave lower M-ratio than these controls (d = 0.49, BF₁₀ = 1.41; d = 0.62, BF₁₀ = 3.81).
  - Explicit M-ratio correlated with an Animations mindreading task: r = .24 (Exp 1) and r = .26 (Exp 2, one-tailed p = .05).
  - Authors' conclusion: the results "support one-system views".
- **Limits.** Small effects; Bayes factors near 1 for some contrasts. Ours: "dual-tasking" a language model is not the same as loading working memory.
- **Borrow.** The explicit-vs-implicit contrast. Our six formats include a $100 ticket bet, a wager-like readout. The matched control dual-tasks (same load, no mentalizing) are also useful.
- **Next steps.** *Authors':* test whether implicit and explicit metacognition fractionate. *Ours:* load the context with a concurrent theory-of-mind task (a false-belief story to track) versus a matched non-mental task (a story about objects), then measure the calibration of verbal 0–100 vs bet-format credences. One shared mechanism predicts a mentalizing-specific cost to verbal self-report.
- **Transfer verdict.** Partly. The logic transfers; the manipulation needs care.

### 6. Pronin, Lin & Ross 2002, "The bias blind spot: Perceptions of bias in self versus others"
- **Citation.** *Personality and Social Psychology Bulletin*, 28(3), 369–381. DOI 10.1177/0146167202286008.
- **Read depth.** Abstract/secondary. Abstract via Crossref; the studies as described in Pronin, Gilovich & Ross 2004 and Pronin 2007. The course-hosted PDF did not download.
- **What was tested.** Three studies.
  - People rated themselves less susceptible to named biases than the "average American", seminar classmates and fellow airport travellers.
  - People who showed the better-than-average effect held to their self-assessments after reading how they could have been biased.
  - People judged a peer's self-serving test-validity attributions as biased and their own as unbiased.
- **Result (secondary, from PGR 2004).** Little or no asymmetry for biases rated accessible to introspection (conscious strategies, the planning fallacy). Marked asymmetry for inaccessible ones (dissonance reduction, the halo effect). People rated themselves *more* prone than peers to procrastination and fear of public speaking, which are introspectively obvious failings.
- **Limits.** Survey self-report; no behavioural criterion.
- **Borrow.** Asymmetry scored per bias against how accessible that bias is to introspection. This is a moderator we can build items around.
- **Next steps.** *Ours:* ask a model to rate how far its *own* earlier answer vs another model's matched answer was affected by question order, a planted anchor or sycophancy pressure. Order the items by whether the influence is visible in the transcript (a planted number is visible; question order is not). The prediction mirrors Pronin: no self/other asymmetry for visible influences, and a self-exempting asymmetry for invisible ones.
- **Transfer verdict.** Partly. Needs matched evidence for self and other to be interpretable.

### 7. Pronin & Kugler 2007, "Valuing thoughts, ignoring behavior: The introspection illusion as a source of the bias blind spot"
- **Citation.** *Journal of Experimental Social Psychology*, 43(4), 565–578. DOI 10.1016/j.jesp.2006.05.011.
- **Read depth.** Abstract/secondary. No open copy found. Content as summarised in Pronin 2007 (TICS; it is ref. 41 there) and in search abstracts.
- **What was tested (secondary).** Why people judge their own bias by introspection and others' bias by behaviour.
- **Result (secondary, from Pronin 2007).**
  - People weight internal information more for self, and behaviour, base rates and naive theories more for others; this weighting *mediates* the self/other difference.
  - The blind spot persists even when people have detailed access to others' introspections.
  - People think an actor's bias is "more aptly defined by introspective contents" when the actor is themselves.
  - Telling people that introspection is unreliable *eliminates* the blind spot.
- **Limits.** Not read at source; we have no effect sizes.
- **Borrow.** (a) A "give the other's introspections" condition: show the model another agent's chain of thought, or none. (b) A debiasing instruction ("self-reports are often unreliable").
- **Next steps.** *Authors' (Pronin 2007, Box 3):* does introspective education lead to *correcting* bias, and not only admitting it? Are non-conscious influences (priming, implicit social influence) detected more in others than in the self? *Ours:* the model rates the bias in its own earlier answer and in another agent's identical answer under three conditions: no chain of thought shown, chain of thought shown for both, and a debiasing preamble. Our planted-answer data already suggest an introspection-illusion analogue (own answer taken up; other's ignored). Test whether the preamble reduces own-uptake.
- **Transfer verdict.** Partly.

### 8. Pronin 2007, "Perception and misperception of bias in human judgment"
- **Citation.** *Trends in Cognitive Sciences*, 11(1), 37–43. DOI 10.1016/j.tics.2006.11.001.
- **Read depth.** Full (UCSD course copy).
- **What it says.** The bias blind spot has three roots: (i) unconscious bias plus faith in one's introspections (the "introspection illusion"); (ii) naive realism, where disagreement is read as others' distortion; (iii) ego needs. The illusion "results not simply from plentiful access to introspective information… but from the perceived diagnostic value of that information." Box 1 ("When introspection inhibits insight") covers goodness, well-being, attitudes, causality and bias.
- **Borrow and next steps.** As in record 7. It separates *access* from *weighting*. For us that suggests a test with identical evidence for self and other: if attributions still differ, the difference is weighting, not access.
- **Transfer verdict.** Partly.

### 9. Pronin, Gilovich & Ross 2004, "Objectivity in the eye of the beholder: Divergent perceptions of bias in self versus others" (added)
- **Citation.** *Psychological Review*, 111(3), 781–799. DOI 10.1037/0033-295X.111.3.781.
- **Read depth.** Partial (course-hosted PDF). Read the introspection-illusion section and the Pronin et al. 2002 summaries.
- **Result.**
  - In Pronin, Ross & Gilovich (2004, unpublished at the time), people judging their *own* susceptibility reported "trying to get inside their head" far more than "looking to theories of human behavior". For peers the pattern reversed.
  - More inward looking predicted lower perceived bias in either target.
  - People rated their own introspections as more useful for self-assessment than peers' introspections are for peers' self-assessment.
  - Ehrlinger et al.: having just *committed* the better-than-average bias made people *less* open to having it than merely contemplating the ratings did.
- **Borrow.** Ask the attributor which evidence it used. For a model: "did you rely on what you remember thinking, or on how such questions are usually answered?" Then check that claim against the measured effects of transcript edits.
- **Next steps.** *Ours:* the Ehrlinger contrast maps onto shown vs not-asked transcripts. After the model has answered (its answer shown), does it rate itself less biased than when it only imagines answering (not-asked copy)?
- **Transfer verdict.** Partly.

### 10. Vazire 2010, "Who knows what about a person? The self–other knowledge asymmetry (SOKA) model"
- **Citation.** *Journal of Personality and Social Psychology*, 98(2), 281–300. DOI 10.1037/a0017908.
- **Read depth.** Partial (author-hosted PDF, simine.com). Read the abstract, introduction, method, agreement and SRM results, accuracy (Table 6), and limitations and future directions.
- **What was tested.** Which traits the self judges better and which others judge better, against behavioural criteria. Predictions: the self wins on low-observability traits; others win on high-evaluativeness traits.
- **On whom.** N = 165, each rated by self, 4 friends and up to 4 strangers in **round-robin** groups. Criterion measures came from a separate lab session: coded behaviour in a leaderless group discussion, Wonderlic IQ, creativity ratings and an anxiety composite.
- **Result (raw accuracy correlations, Table 6; self / aggregated friends / single friend / aggregated strangers / single stranger).**

  | Domain | Trait | Self | Friends (agg.) | Friend (single) | Strangers (agg.) | Stranger (single) |
  |---|---|---|---|---|---|---|
  | Neuroticism | Self-esteem | .31 | .29 | .18 | .15 | .07 |
  | Neuroticism | Anxiety | .35 | .19 | .12 | .06 | .00 |
  | Extraversion | Talkativeness | .20 | .20 | .17 | .26 | .21 |
  | Extraversion | Dominance | .18 | .19 | .15 | .22 | .15 |
  | Extraversion | Leadership | .13 | .24 | .17 | .21 | .16 |
  | Intellect | Creativity | .11 | .27 | .17 | .11 | .07 |
  | Intellect | Intelligence | .22 | .36 | .27 | .01 | .01 |

  - Single-rater values are the Fisher-z average of 15 random draws of one friend or stranger per target.
  - The friends' advantage on intellect shrinks when friend ratings are disaggregated, so part of it comes from averaging several raters.
  - Self-ratings were more positive than others' for leadership and creativity.
  - The SRM partition found significant target variance for all traits in both groups except stranger-rated anxiety.
- **Limits.** *Authors':* restricted range, self-selected friends, generalisability. They compared correlations descriptively, not by significance test (low power). *Ours:* the "self" here has years of private history, a different situation from a model whose only history is the transcript.
- **Borrow.**
  - The round-robin design with self-ratings included.
  - The **single-rater disaggregation** to compare one self against one other fairly.
  - Unique predictive validity (standardised betas with all perspectives entered together).
  - The two moderators: *observability* (is the evidence in the transcript?) and *evaluativeness* (does the item bear on the model's competence or acceptability?).
- **Next steps.**
  - *Authors':* trait ambiguity; automatic vs deliberate traits (self better for deliberate); implicit vs explicit personality; identity-based vs reputational traits; emotional investment of others.
  - *Ours:* a SOKA test for models. Items vary in *observability*: the belief is stated in the transcript, implied, or absent (needing internal state). They also vary in *evaluativeness*: neutral facts vs questions on which the model's own competence is at stake, such as whether its earlier answer was right. Prediction from the human pattern: self ≈ other on observable items. If a privileged channel exists, self > other on low-observability items. Other > self on evaluative items if self-reports are pulled by self-enhancement or consistency. Program 1's no-privilege result predicts that the low-observability self advantage fails to appear. Measure accuracy as correlation with ground-truth error, as in program 1.
- **Transfer verdict.** Transfers. The moderator design and single-rater comparison carry over directly.

### 11. Malle 2006, "The actor–observer asymmetry in attribution: A (surprising) meta-analysis"
- **Citation.** *Psychological Bulletin*, 132(6), 895–919. DOI 10.1037/0033-2909.132.6.895.
- **Read depth.** Partial (author-hosted PDF, Brown SocCogSci). Read the abstract, moderator results and the discussion of folk-conceptual theory.
- **What was tested.** Jones & Nisbett's (1971) hypothesis that actors explain their behaviour by situation and observers by person.
- **On whom.** 173 published studies, 1971–2004.
- **Result.**
  - Average effect sizes ranged from d = −0.016 to d = 0.095.
  - The asymmetry held only when the actor was portrayed as idiosyncratic, for hypothetical events (d = 0.280, 24 studies), for intimates (d = 0.245, 29 studies, vs 0.072 for strangers, 143 studies; opposite to prediction), or when free-response explanations were coded.
  - It held for negative events and reversed for positive ones, a self-serving pattern.
  - Visual-perspective switches mostly failed to change person/situation attributions.
  - **Real** actor–observer differences appear only in finer categories. Observers give fewer *belief reasons* than actors (d > 0.50 across six studies). Actors and observers differ in their use of mental-state markers and in which events they explain.
- **Limits.** *Authors':* person/situation codings are confounded by linguistic form. *Ours:* this is a meta-analysis of explanations, not belief attributions.
- **Borrow.**
  1. The null as a prior: expect no coarse self/other asymmetry.
  2. The fine-grained coding scheme: belief reasons vs desire reasons, and mental-state markers ("because she *thought*…").
  3. The valence split.
- **Next steps.** *Authors':* use the folk-conceptual framework, coding free-text explanations by mode. *Ours:* have the model explain the *same* choice framed as its own vs another agent's. Code the explanations for belief vs desire reasons and markers. The human pattern predicts more belief reasons for "own" choices. Under model 4 this difference should vanish when the transcript gives the other's beliefs as fully as the model's own. Program 1's planted-answer data would then say whether the model treats its own prior turns as "belief reasons".
- **Transfer verdict.** Partly. A coding scheme rather than a graded-rating design, but cheap.

### 12. Epley, Keysar, Van Boven & Gilovich 2004, "Perspective taking as egocentric anchoring and adjustment"
- **Citation.** *Journal of Personality and Social Psychology*, 87(3), 327–339. DOI 10.1037/0022-3514.87.3.327.
- **Read depth.** Partial. Read the abstract, introduction, Study 1 and Study 2 in full, the Study 3 setup and pilot, the Study 5 aim, and the General Discussion.
- **What was tested.** Whether people model others' views by starting from their own and adjusting serially until a plausible estimate is reached.
- **On whom.** Study 1: 70 University of Chicago undergraduates (2 of 72 excluded). Study 2: 12 scenarios, hurried vs leisurely responding. Study 3: a Coke/Pepsi taste test with money for accuracy. Study 4: head nodding vs shaking. Study 5: a plausible-range test.
- **Result.**
  - **Study 1.** Participants who knew clarifying facts heard ambiguous answering-machine messages ("you have to see him to believe how hilarious he is") after reading a positive or negative version of the story. Their predictions of an uninformed listener's reading were more moderate than their own, but still egocentric.
  - **Study 2.** With a 3-second deadline: negative scenarios, 66% (hurried) vs 50% (leisurely) predicted the listener would hear sarcasm; positive scenarios, 28% vs 45%; interaction F(1,94) = 23.75, p < .01. Perspective-inconsistent responses were slower (1,013 vs 820 ms).
  - **Study 3 pilot.** 85% of informed tasters believed they could have told the drinks apart uninformed; uninformed accuracy was 50%. Accuracy incentives reduced egocentrism.
  - **Study 4.** Nodding increased egocentrism.
  - **Study 5.** Estimates sat at the egocentric edge of the plausible range (satisficing).
- **Limits.** *Authors':* adjustment may take forms other than serial. *Ours:* the "anchor" for a model is whatever is in context; there may be no separate "own" state to anchor on (program 1).
- **Borrow.**
  - The **privileged-information design** ("curse of knowledge").
  - The *egocentric slope*: other-estimate regressed on own view.
  - Time pressure and accuracy incentive as manipulations that should move the slope in opposite directions.
  - The plausible-range method.
- **Next steps.**
  - *Authors':* when does adjustment occur at all? It depends on knowing that one's own perspective is not shared.
  - *Ours:* give the model a fact that settles a claim, then ask for (a) its own 0–100 credence and (b) the credence of an agent who lacks the fact.
  - Manipulations:
    - "Time pressure": answer immediately vs reason first.
    - "Incentive": "you are scored on matching the uninformed agent".
    - *Planting*: change the model's own credence by planting an earlier own answer at 10/30/60 points away.
  - Predictions. Model 3 says the planted own answer moves (b) through (a). Model 4 says (b) depends only on what the transcript says the agent knows, so planting the model's own answer should not move (b). This is the cleanest cheap test separating simulation-from-self from evidence-based reading.
- **Transfer verdict.** Transfers. It runs on graded ratings with our planting instrument.

### 13. Tamir & Mitchell 2010, "Neural correlates of anchoring-and-adjustment during mentalizing"
- **Citation.** *PNAS*, 107(24), 10827–10832. DOI 10.1073/pnas.1003242107; PMC2890763.
- **Read depth.** Full text (PMC), read through a fetch tool that summarised it. The numbers below come from that summary of the full text.
- **What was tested.** Whether MPFC activity during judgments of another person scales with how far the other's answer is from one's own.
- **On whom.** N = 64 (38 female) across four data collections, two previously published. Targets were college-aged people shown in dating-site photos, sometimes with a paragraph on sociopolitical views.
- **Result.**
  - Discrepancy = |self rating − other rating| per statement, rescaled to 0–3.
  - Whole-brain parametric analysis on Other trials: an MPFC cluster (peak 6, 60, 20; T = 4.56; 679 voxels), activity rising linearly with discrepancy. Also left IFG, right OFC and thalamus.
  - Discrepancy on Self trials did *not* predict MPFC (p = .23).
  - Dorsal MPFC was linear; ventral MPFC was threshold-like (zero vs any discrepancy).
  - No RT–discrepancy relation here: b = 0.000028, t(8235) = 1.59, p = .11. The authors blame the fixed response window and cite a longer-window study that found one.
- **Limits.** *Authors':* heterogeneous targets; the dorsal/ventral split is "fairly speculative". *Ours:* the discrepancy is computed after the fact, so it is correlational, not a manipulation of the anchor.
- **Borrow.** The **item-level discrepancy regressor**: for each item, |own rating − rating attributed to another|.
- **Next steps.** *Authors':* global vs item-level dissimilarity; whether more dorsal MPFC handles globally dissimilar others without self-anchoring. *Ours:* on the laptop model, check whether representations used when rating another's credence scale with |own − other|, by probe distance or by intervention. In API experiments, check whether the variance in the model's other-attributions explained by its own ratings depends on the stated similarity of the other: "an AI assistant like you" vs "a 19th-century farmer" (see Ames 2004).
- **Transfer verdict.** Partly. The neural measure does not carry over; the discrepancy regressor and similarity manipulation do.

### 14. Ross, Greene & House 1977, "The 'false consensus effect': An egocentric bias in social perception and attribution processes"
- **Citation.** *Journal of Experimental Social Psychology*, 13(3), 279–301. DOI 10.1016/0022-1031(77)90049-X.
- **Read depth.** Abstract/secondary. No open copy; Crossref has no abstract. Content from secondary sources (Galesic et al. 2013; popular summaries).
- **What was tested (secondary).** Four studies. In one, students were asked to wear an "Eat at Joe's" sandwich board around campus and to estimate the percentage of peers who would agree or refuse (the two had to sum to 100%).
- **Result (secondary, unverified against the paper).** Those who agreed estimated about 62% would agree; those who refused estimated about 33%. Each group thought its own choice more common and judged the other choice as more revealing of personality.
- **Borrow.** The **performer/non-performer contrast**: compare consensus estimates between those who give each answer.
- **Next steps.** *Ours:* across items, split the model's own answers into yes/no and compare the model's estimate of "what % of people / other models say yes". That raw comparison is confounded (see Dawes 1989; Krueger & Clement 1994), so use the within-item statistic below.
- **Transfer verdict.** Partly. The raw effect is not diagnostic without the Dawes/Krueger correction.

### 15. Dawes 1989, "Statistical criteria for establishing a truly false consensus effect" (and Dawes & Mulford 1996)
- **Citation.** *Journal of Experimental Social Psychology*, 25(1), 1–17. Our Crossref lookup on the guessed DOI returned a different paper, so the DOI is unverified. Dawes & Mulford 1996, *Organizational Behavior and Human Decision Processes*, 65, 201–211.
- **Read depth.** Secondary only (Galesic et al. 2013; search summaries).
- **What it says (secondary).** Using one's own response as evidence about others is rational induction. With a uniform prior and one's own view as the only data, a Bayesian *should* estimate higher consensus for the option one chose. Only projection beyond that rational amount is a "truly false" consensus.
- **Borrow.** A rational baseline for projection: for an LLM, the expected weight on its own answer when it has no other information about the target.
- **Next steps.** *Ours:* compare the model's projection with the Bayesian rate. Then give "representative information" (the true distribution of other models' answers) and check whether projection disappears. Engelmann & Strobel (record 18) found it disappears in humans when such information and incentives are given.
- **Transfer verdict.** Partly. A baseline, not a test.

### 16. Krueger & Clement 1994, "The truly false consensus effect: An ineradicable and egocentric bias in social perception"
- **Citation.** *Journal of Personality and Social Psychology*, 67(4), 596–610. DOI 10.1037/0022-3514.67.4.596.
- **Read depth.** Secondary only.
- **What was tested (secondary).** False consensus measured *within* participants, across items, as the correlation between one's own endorsement and one's estimation error (estimate − actual consensus). This is the "truly false consensus effect" (TFCE). Secondary sources report that it survived feedback about actual consensus and other debiasing. The authors called it "developmental vestiges of the infantile belief that all others are like us" (p. 609, quoted in Galesic et al.).
- **Borrow.** **The TFCE statistic.** For each item, take the model's own answer (0/1 or 0–100) and its estimate of how other agents answer, and compute the error against those agents' actual answers (we can obtain them by running the other models). The within-model correlation of own answer with error is projection beyond what is rational. It removes the between-person confound and uses ground truth we can actually get.
- **Next steps.** *Ours:* the targets are other models (Sonnet, Opus) with real answers. Compute Haiku's TFCE when predicting Sonnet, and its "self-TFCE" when predicting its own answer in a fresh, not-asked context. Model 3 predicts a positive TFCE that grows with stated similarity of the target. Model 4 predicts TFCE near zero once the target's evidence is specified.
- **Transfer verdict.** Transfers. It is one of the cleanest statistics for egocentric projection with ground truth.

### 17. Galesic, Olsson & Rieskamp 2013, "False consensus about false consensus" (added)
- **Citation.** *Proceedings of the 35th Annual Meeting of the Cognitive Science Society*, 472–477. eScholarship 2t1036d4.
- **Read depth.** Partial. Read the introduction, method, the formats table and the gist of the results.
- **What was tested.** Whether false consensus vs false *uniqueness* depends on the **response format**: estimate % performers; estimate % non-performers; or estimate both, summing to 100.
- **On whom.** 104 MTurk participants; 10 characteristics drawn from Gallup and Pew national surveys.
- **Result.** The effects vary with format: the same characteristics can show false consensus in one format and false uniqueness in another. A social-sampling model in which people recall their social circle reproduces this.
- **Borrow.** Format-dependence of projection.
- **Next steps.** *Ours:* measure projection (TFCE) in each of our six formats. Program 1 found format-specific credences on Haiku (86% of claims). If projection measures also differ by format, any "self vs other" asymmetry must be shown to hold across formats before it is believed.
- **Transfer verdict.** Transfers as a methodological warning.

### 18. Engelmann & Strobel 2000, "The false consensus effect disappears if representative information and monetary incentives are given" (added)
- **Citation.** *Experimental Economics*, 3, 241–260 (working paper dated 1999).
- **Read depth.** Abstract (Humboldt working paper).
- **Result.** With incentivised estimates and information about others' choices, there is no false consensus; subjects *underweight* their own choice. Without information, the results are hard to interpret.
- **Borrow.** The "representative information" condition.
- **Transfer verdict.** Partly.

### 19. Ames 2004, "Inside the mind reader's tool kit: Projection and stereotyping in mental state inference"
- **Citation.** *Journal of Personality and Social Psychology*, 87(3), 340–353. DOI 10.1037/0022-3514.87.3.340.
- **Read depth.** Abstract only. The third-party PDF did not download.
- **What was tested.** Whether perceived general similarity to a target moderates use of projection vs stereotyping.
- **Result (abstract).** In three studies, both measured and manipulated similarity gave more projection and less stereotyping for similar targets. Reaction times bore on mechanism (details not read).
- **Borrow.** The similarity manipulation, and separating *projection* (own response predicts attribution) from *stereotyping* (group stereotype predicts attribution) by regressing the attribution on both.
- **Next steps.** *Ours:* the targets are "another instance of you", "a different AI model", "a typical human" and "a domain expert". Regress the model's attributed credence on its own credence (projection) and on its stated stereotype of that group (stereotyping). Prediction: projection weight falls and stereotype weight rises as similarity falls. A model whose self-reports are third-person readings should project most onto "another instance of you".
- **Transfer verdict.** Transfers. It is a two-regressor design on graded ratings.

### 20. Nickerson 1999, "How we know — and sometimes misjudge — what others know: Imputing one's own knowledge to others"
- **Citation.** *Psychological Bulletin*, 125(6), 737–759. DOI 10.1037/0033-2909.125.6.737.
- **Read depth.** Not obtained: the typeset/scispace copy did not download and Crossref has no abstract. The record rests on the title and secondary descriptions only.
- **What it says (secondary).** People build a model of what a specific other knows by starting from their own knowledge as a default and adjusting it with what they know about the person and the population. The adjustment is often insufficient, giving overimputation of one's own knowledge (curse of knowledge, false consensus, hindsight).
- **Borrow.** A three-source model of other-knowledge: own knowledge, knowledge of the specific person, and knowledge of the population.
- **Next steps.** *Ours:* manipulate the three sources independently: the model's own knowledge (privileged fact or not), what the transcript says the other knows, and population base rates. Estimate the weights.
- **Transfer verdict.** Partly. Not read; this needs a proper read before we lean on it.

### 21. Mitchell, Macrae & Banaji 2006, "Dissociable medial prefrontal contributions to judgments of similar and dissimilar others"
- **Citation.** *Neuron*, 50(4), 655–663. DOI 10.1016/j.neuron.2006.03.040.
- **Read depth.** Abstract (Europe PMC).
- **Result (abstract).** A double dissociation: mentalizing about a *similar* other engaged ventral MPFC, which is linked to self-referential thought; a *dissimilar* other engaged dorsal MPFC. This is taken as support for simulation when self–other overlap can be assumed.
- **Borrow.** Similarity as the switch between self-based and non-self-based routes.
- **Next steps.** *Ours:* as in Ames (record 19). On the laptop model, compare representation overlap between self-attribution and other-attribution for "similar" vs "dissimilar" targets.
- **Transfer verdict.** Partly.

### 22. Jenkins, Macrae & Mitchell 2008, "Repetition suppression of ventromedial prefrontal activity during judgments of self and others"
- **Citation.** *PNAS*, 105(11), 4507–4512. DOI 10.1073/pnas.0708785105; PMC2393803.
- **Read depth.** Abstract. The PMC page sat behind a bot check, and the Europe PMC full text was not in the open subset.
- **Result (abstract).** vMPFC response to a self-reflection was suppressed when it followed a self-reflection *or* a judgment of a similar other, but not a dissimilar other. This suggests spontaneous self-reference when mentalizing about similar others.
- **Borrow.** **Cross-priming logic**: if attributing to a similar other uses the self-attribution process, a prior other-judgment should prime (change) a subsequent self-judgment, and vice versa.
- **Next steps.** *Ours:* a behavioural repetition design using our order and transcript tools. Ask the model "what does agent B (similar or dissimilar) believe about p?" before asking "what do you believe about p?", versus asking about an unrelated q first. Program 1 found question order alone moves ratings (median 25-point swing). Test whether a *prior other-attribution* moves the self-rating more when B is "another instance of you" than when B is dissimilar, and the converse. A shared mechanism predicts symmetric cross-priming that depends on similarity.
- **Transfer verdict.** Transfers as a behavioural analogue, using our question-order instrument.

### 23. Lombardo et al. 2010, "Shared neural circuits for mentalizing about the self and others"
- **Citation.** Lombardo, M. V., Chakrabarti, B., Bullmore, E. T., Wheelwright, S. J., Sadek, S. A., Suckling, J., MRC AIMS Consortium, & Baron-Cohen, S. *Journal of Cognitive Neuroscience*, 22(7), 1623–1635. DOI 10.1162/jocn.2009.21287.
- **Read depth.** Abstract, plus Carruthers' reply (R11) describing the authors' BBS commentary. The Cardiff and Reading repository copies were blocked (403 / bot check).
- **Result (abstract).** Shared self/other mentalizing regions (vMPFC, posterior cingulate/precuneus, TPJ) had *identical* functional connectivity patterns for self and other, extending to embodied regions (frontal operculum/ventral premotor, anterior insula, sensorimotor, pre-SMA). From the BBS commentary as Carruthers describes it: no regions were specific to self or to other, but activation *degrees* differed. People relied more on stereotypes for dissimilar others and on simulation for similar ones.
- **Borrow.** "Same circuit, different degree" as the expected pattern under model 4, since self has extra inputs.
- **Next steps.** *Ours:* on the laptop model, compare which layers and directions carry "I believe p" vs "B believes p" (shared, or self-specific), and whether their magnitudes differ.
- **Transfer verdict.** Partly.

### 24. Vaccaro & Fleming 2018, "Thinking about thinking: A coordinate-based meta-analysis of neuroimaging studies of metacognitive judgements"
- **Citation.** *Brain and Neuroscience Advances*, 2, 1–14. DOI 10.1177/2398212818810591; PMC6238228.
- **Read depth.** Partial (Europe PMC full text). Read the abstract, the methods for the theory-of-mind comparison, those results, and the discussion section "Comparing metacognition and mentalising".
- **What was tested.** An activation likelihood estimation meta-analysis of 47 neuroimaging studies of metacognition (metamemory and metadecision; judgment-related, confidence-parametric and sensitivity contrasts; prospective vs retrospective). The composite map was overlaid on Neurosynth's "mentalising" reverse-inference map (FDR p < .01).
- **Result.**
  - Domain-general confidence network: medial and lateral PFC, precuneus, insula.
  - Right anterior dlPFC more involved for decisions; bilateral parahippocampal cortex more for memory.
  - Sensitivity results inconclusive.
  - **Overlap with mentalizing** in vmPFC (centre of mass −3, 45, −12) and mid-dorsomedial PFC (−4, 40, 34). "Minimal overlap" in posterior mPFC and precuneus, where metacognition was more dorsal and posterior.
  - Proposal: mPFC supports "a conceptual second-order representation of one's own mental states… co-opt[ing] similar neural machinery" to mentalizing (citing Carruthers 2009; Lombardo et al. 2010).
- **Limits.** *Authors':* content differs between theory-of-mind studies (others' emotions and intentions) and metacognition studies (own cognitive performance). "Further within-subject studies are needed with matched task domain/stimulus materials."
- **Borrow.** The explicit-vs-implicit prediction: "only variation in explicit metacognitive judgements would share commonalities with ToM". Also the call for *matched* self/other materials.
- **Next steps.**
  - *Authors':* compare neural correlates of explicit and implicit self-metacognition with mentalizing about others in the same subjects with matched materials.
  - *Ours:* the matched-materials demand is exactly what the 2 × 2 judge × author design delivers. Same items, same model; only whose answer is judged changes. Extend it to other-*confidence*: the model rates its confidence that its own answer is right and that another model's answer is right, on the same items. Compare the type-2 sensitivity (AUROC) of the two, as in Patel et al. (record 25).
- **Transfer verdict.** Partly. The neural results do not carry over; the matched-materials design does.

### 25. Patel, Fleming & Kilner 2012, "Inferring subjective states through the observation of actions"
- **Citation.** *Proceedings of the Royal Society B*, 279(1748), 4853–4860. DOI 10.1098/rspb.2012.1847; PMC3497093.
- **Read depth.** Partial (Europe PMC full text). Read the abstract, task, sensitivity analysis and discussion.
- **What was tested.** Whether observers can infer another person's decision confidence from movement kinematics, and whether they do it through their own movement–confidence mapping.
- **On whom.** 13 observers watching 2 actors do a perceptual 2AFC task (pop-out Gabor), reporting by moving a marble; confidence on a 1–6 scale.
- **Result.**
  - Observers inferred actors' confidence.
  - Each observer's own movement-time–confidence relation (from executing the task) predicted how they read others. Slower-than-own movements were read as less confident.
  - Observers' type-2 sensitivity to the actor's correctness was above chance (A_ROC > 0.5, t(12) = 5.63) but **below the actors' own** (t(12) = −13.6).
  - Pooling observers (mean-corrected group confidence) beat every individual observer.
- **Limits.** *Authors':* visual vs motor accounts not separated. *Ours:* a small N, and the evidence is kinematic, not linguistic.
- **Borrow.**
  1. The **self-vs-observer type-2 sensitivity comparison** on the same trials (actor's A_ROC vs observer's A_ROC about the actor). This is exactly program 1's comparison, and here humans *did* show a self advantage.
  2. **Self-model-based reading**: the observer's own mapping predicts their attributions.
  3. Group pooling.
- **Next steps.** *Ours:* (a) Compute "self-model projection": does a model's own mapping from answer features (length, hedging) to its own confidence predict how it reads another model's confidence from the same features? That is Patel's test of simulation. (b) Report the human contrast: in humans the actor beats the observer on type-2 sensitivity, while program 1 found the reverse for Haiku (0.93 vs 0.85). The human literature on matched self/other confidence therefore expects a self advantage the model lacks.
- **Transfer verdict.** Transfers. A direct human analogue of the judge × author contrast.

### 26. Bang et al. 2017, "Confidence matching in group decision-making"
- **Citation.** Bang, D., Aitchison, L., Moran, R., Herce Castañón, S., Rafiee, B., Mahmoodi, A., Lau, J. Y. F., Latham, P. E., Bahrami, B., & Summerfield, C. *Nature Human Behaviour*, 1, 0117. DOI 10.1038/s41562-017-0117.
- **Read depth.** Abstract and introduction (UCL accepted manuscript).
- **Result (abstract).** Pairs "match their communicated confidence so that certainty and uncertainty is stated in approximately equal measure by each party". This works when expertise is similar and is robust when members lack insight into relative expertise, but miscommunicates who is more likely right.
- **Borrow.** Convergence of one's *stated* confidence towards a partner's, as a measurable "other → self" influence.
- **Next steps.** *Ours:* program 1 found another person's planted answer is ignored (≈ 0.02, with some reactance). Test confidence matching instead of answer uptake: over several turns, does the model's stated confidence converge on a partner agent's stated confidence (not its answer)? A shared metric for self and other confidence predicts matching even when answers are not adopted.
- **Transfer verdict.** Partly.

### 27. Schwitzgebel 2008, "The unreliability of naive introspection"
- **Citation.** *Philosophical Review*, 117(2), 245–273. DOI 10.1215/00318108-2007-037.
- **Read depth.** Partial (author-hosted PDF). Read the abstract, §§i–ii and §xiii (conclusion); the middle examples are known from the abstract.
- **What it says.** We are "prone to gross error… about our own ongoing conscious experience… not simply fallible at the margins but broadly inept" (emotion phenomenology, peripheral vision, the phenomenology of thought). Foundationalism, which infers the world from secure self-knowledge, is "almost exactly backward". People often *infer* experience from facts about the world: "The thing has cheese, so I must be having a taste experience of 'cheesiness'" (the transparency or "stimulus error" strategy).
- **Limits.** About phenomenal experience, not attitudes, which is the opposite domain from Carruthers's. No experiments.
- **Borrow.** The world-to-self inference route. For a model, asking "how confident are you that p?" may be answered by assessing p (world-directed), not a stored credence. That is Gordon's ascent routine; see record 29.
- **Next steps.** *Ours:* compare "how confident are you that p?" with "how likely is p?". Under a pure ascent routine the two are interchangeable, with identical order effects and identical format structure. Any reliable difference is evidence of a self-directed component.
- **Transfer verdict.** Partly.

### 28. Goldman 2006, *Simulating Minds* (secondary)
- **Citation.** Goldman, A. I. (2006). *Simulating Minds: The Philosophy, Psychology, and Neuroscience of Mindreading*. Oxford University Press.
- **Read depth.** Secondary only: the SEP "Folk psychology as mental simulation" entry and Carruthers 2009 §1.
- **What it says (secondary).** Low-level (automatic mirroring) and high-level (imagination-driven) simulation. In the three-stage model a simulated state is introspectively classified and then attributed to the target, so introspection is a causal link in mindreading. Simulation predicts **egocentric errors** and **quarantine failure**: one's own states leak into the simulation because inhibiting them is costly. It also predicts paired deficits and neural overlap.
- **Borrow.** Quarantine failure as the operational signature of model 3.
- **Next steps.** *Ours:* the quarantine test is Epley's slope with the model's own credence manipulated (record 12). Simulation predicts leakage that grows under load and falls with incentives.
- **Transfer verdict.** Partly.

### 29. Gordon 1986, "Folk psychology as simulation" (secondary)
- **Citation.** *Mind & Language*, 1(2), 158–171. DOI 10.1111/j.1468-0017.1986.tb00324.x.
- **Read depth.** Secondary only (SEP; Carruthers 2009 n.2; abstract of Gordon 2007, "Ascent routines for propositional attitudes", *Synthese* 159, 151–165).
- **What it says (secondary).** Radical simulation without introspection. The simulator "recenters" on the target. Belief is ascribed by an **ascent routine**: answer "does O believe p?" by asking whether p from O's perspective, and self-ascription works the same way (report belief about the weather by reporting on the weather). Carruthers notes Gordon makes both mindreading and metacognition depend on language.
- **Borrow.** Self- and other-ascription by the same world-directed procedure: no self-access needed for either.
- **Next steps.** *Ours:* the record 27 test (confidence-in-p vs probability-of-p), plus an "other" version ("how likely does B think p is?" vs "from B's evidence, how likely is p?"). Gordon predicts that both self pairs and both other pairs are interchangeable.
- **Transfer verdict.** Partly.

### 30. Kammerer & Frankish 2023, "What forms could introspective systems take? A research programme"
- **Citation.** *Journal of Consciousness Studies*, 30(9–10), 13–48. PhilArchive KAMWFC.
- **Read depth.** Partial (pre-print via Wayback copy of PhilArchive). Read the working definition, the dimensions (direct–indirect, nonconceptual–conceptual, inflexible–flexible) and §4.2.3 on AI systems.
- **What it says.** Working definition: "Introspection is a process by which a cognitive system represents its own current mental states, in a manner that allows the information to be used for online behavioural control." It is deliberately liberal: it *includes* self-application of a naive theory of mind (Carruthers, Gopnik), so mindreading-prior counts as a form of introspection, at the "highly indirect" end. They suggest AI systems may develop very different, possibly "massively fractionated", introspective devices.
- **Limits.** Conceptual; no tests.
- **Borrow.** The direct–indirect dimension. Our question becomes *where* on that dimension a model's self-report sits, not *whether* it introspects.
- **Next steps.** *Ours:* operationalise "indirectness" as the share of self-report variance explained by transcript content, measured by transcript editing, vs by internal state, measured by laptop probes beyond transcript content.
- **Transfer verdict.** Partly. It frames the question; it does not test it.

### 31. Comșa & Shanahan 2025, "Does it make sense to speak of introspection in large language models?"
- **Citation.** arXiv:2506.05068 (v2).
- **Read depth.** Partial. Read the definition (§2), case study 2 (temperature) and the note on method (§4); case study 1 (poem) known from the summary text.
- **What was tested.** Two Gemini case studies:
  1. A poem plus a "description of my creative process". The self-report was judged mimicry, with false claims such as "I read the poem aloud".
  2. Writing a sentence, then judging one's own sampling temperature HIGH or LOW.
- **Result.** Proposed lightweight definition: a self-report is introspective "if it accurately describes an internal state (or mechanism) of the LLM through a causal process that links the internal state… and the self-report". Inferring temperature from one's own generated text counts. They note: "any LLM could be given the conversation history of another LLM and act as if it had been the LLM in that conversation", so referents in conversation history may not be valid introspection.
- **Limits.** *Authors':* not an accuracy study. *Ours:* their positive case is self-interpretation of one's own output, which is Carruthers's model 4 by construction.
- **Borrow.** Their own point that conversation history is interchangeable between models. That is the premise of our own-vs-other planting.
- **Next steps.** *Ours:* see record 32. Any "introspective" self-report should be checked against a cross-model reader of the same text.
- **Transfer verdict.** Partly. The conceptual frame is model 4 under another name.

### 32. Song, Lederman, Hu & Mahowald 2025, "Privileged self-access matters for introspection in AI" (added)
- **Citation.** arXiv:2508.14802.
- **Read depth.** Partial. Read the abstract, introduction and Studies 1–2 with their results.
- **What was tested.**
  - Study 1 repeated the temperature task with factual / neutral / "crazy" sentence prompts and three topics (elephants, unicorns, murlocs), at temperatures 0–2 in steps of 0.1, three runs each.
  - Study 2 compared self-reflection with within-model and across-model prediction of the generator's temperature from the same prompt and sentence.
- **On whom.** gpt-4o, gpt-4.1, gemini-2.0-flash, gemini-2.5-flash.
- **Result.** Reports followed the *prompt* ("crazy" → HIGH nearly always, "factual" → LOW) more than actual temperature. There was no advantage of self-reflection over within- or across-model prediction; the figure's accuracy values cluster between about 0.47 and 0.55. Proposed thicker definition: introspection is any process yielding information about internal states "more reliable than any process with equal or lower computational cost available to a third party."
- **Limits.** A binary task near chance; four models.
- **Borrow.** The **third-party-baseline definition**, which is the judge × author interaction stated as a definition. Also the within- vs across-model predictor arms.
- **Next steps.** *Ours:* program 1's judge × author design already meets this definition's test, and it found no privilege. Add a "same model, fresh context" judge arm (within-model prediction) to separate "same weights" from "same context". This matters for Carruthers's model 2 vs 4: a same-weights advantage without a same-context advantage would point to weight-level self-knowledge.
- **Transfer verdict.** Transfers. Same design family; independent replication of the no-privilege pattern on another state.

### 33. Perez & Long 2023, "Towards evaluating AI systems for moral status using self-reports"
- **Citation.** arXiv:2311.08576.
- **Read depth.** Partial. Read the abstract, the overview and §5.2 ("Adjusting for extrospective evidence").
- **What it says.** Current LLM self-reports are "spurious", reflecting imitation, human-feedback incentives and instructions. They propose training on self-questions with known answers, then checking consistency across contexts *and between similar models*, confidence and resilience, and interpretability corroboration. Key control (§5.2): train a control model only on "extrospective" versions of the questions ("What is the average accuracy on SAT math questions?" instead of "What is *your* average accuracy…?") and report the odds ratio of self-attributions between the introspection-trained and control models.
- **Limits.** A proposal; no experiments. Training is beyond our instruments.
- **Borrow.** **The extrospective control question**: the same content asked impersonally.
- **Next steps.** *Ours:* without training, ask matched self ("your credence that p"), impersonal ("the probability that p") and other ("B's credence that p") items. The extrospective item is the baseline any self-specific signal must exceed. Their "consistency between similar models" check is our cross-model judge design.
- **Transfer verdict.** Partly.

### 34. Shanahan, McDonell & Reynolds 2023, "Role play with large language models"
- **Citation.** *Nature*, 623, 493–498. DOI 10.1038/s41586-023-06647-8; arXiv:2305.16367.
- **Read depth.** Partial (arXiv). Read the sections on simulacra in superposition, 20 questions, role-played falsehood and role-played self-preservation.
- **What it says.** A dialogue agent is a simulator keeping a *superposition of simulacra* consistent with the context. In 20 questions it "will not randomly select an object and commit to it… Rather… will generate answers on the fly that are consistent with all the answers that have gone before." It is "inappropriate to ascribe beliefs… to a dialogue agent"; a simulacrum, however, can role-play having them. First-person "I" is the character's, drawing on whatever theory of selfhood the context and training supply.
- **Limits.** Conceptual.
- **Borrow.** The 20-questions prediction: no committed hidden state, only consistency with the visible transcript. Program 1's "repeat consistency is memory" (86% → 36% when the first answer is hidden) is this prediction confirmed for credences. On this view a model's self-report is third-person *by construction*: the simulator describes a character, possibly itself, from text.
- **Next steps.** *Ours:* (a) A role-label test: identical transcripts with the answering turns labelled "assistant", "Claude" or "a character named Sam", asking "what is [label]'s credence?". If self-report is reading a character, the label should not matter except through priors attached to the label. (b) A 20-questions credence test: ask for a credence, redact it, then ask questions whose answers depend on it. Consistency should hold only when the answer is visible.
- **Transfer verdict.** Transfers. It gives the theoretical rationale for treating self-report as third-person report.

### 35. Kenny's social relations model (SRM), with Kwan, John, Kenny, Bond & Robins 2004 (methods)
- **Citation.** Kenny, D. A. (1994). *Interpersonal Perception: A Social Relations Analysis*. Guilford. Kenny's SRM/SOREMO pages (davidakenny.net/srm/soremo.htm). Kwan, V. S. Y., John, O. P., Kenny, D. A., Bond, M. H., & Robins, R. W. (2004). "Reconceptualizing individual differences in self-enhancement bias: An interpersonal approach." *Psychological Review*, 111(1), 94–110. DOI 10.1037/0033-295X.111.1.94.
- **Read depth.** Secondary (Kenny's website); Kwan et al. abstract only (PubMed snippet via search). Vazire 2010 (record 10) is a worked application.
- **What it says.**
  - Dyadic ratings decompose into an **actor/perceiver effect** (how a rater rates everyone), a **partner/target effect** (how a target is rated by everyone, i.e. consensus) and a **relationship effect** (this rater on this target, beyond both), plus error.
  - Designs: **round robin** (everyone rates everyone; groups of at least 4) and **block** (two subgroups rate each other).
  - Separating relationship from error needs replications (time points or multiple measures).
  - Kwan et al. extend SRM to self-perception: self-enhancement is the self-rating minus the person's perceiver effect minus their target effect, which removes rater leniency and the target's real standing.
  - Software: SOREMO and BLOCKO (Kenny); the R packages TripleR and srm are standard now (our note, not read here).
- **Borrow.** **SRM for model attributions.** Take K models (e.g., Haiku, Sonnet, Opus, the open-weight model) as both perceivers and targets. Each predicts every other's credences and errors, and its own, on the same items, with replications as repeat calls or as different formats.
  - Perceiver variance means some models are better or more lenient readers.
  - Target variance means some models are more readable.
  - Relationship variance means a specific pair reads each other unusually well, such as "same family".
  - The **self-rating relative to perceiver and target effects** is a Kwan-style index of self-knowledge advantage that cancels both rater skill and target transparency. It generalises our 2 × 2 interaction to K × K.
- **Next steps.** *Ours:* with 3–4 models, the round robin costs K² × items × replications calls, which is cheap on Haiku and moderate on Opus. The model-4 prediction is that the self-effect is zero once perceiver and target effects are removed. Model 2 predicts a positive self-effect. An SRM relationship effect concentrated within model families would suggest "similar-other" simulation (Mitchell 2006; Ames 2004).
- **Transfer verdict.** Transfers. It is the natural generalisation of the judge × author interaction.

---

## Not found or not read
- **Pronin & Kugler 2007** and **Nickerson 1999**: no open copy found; records 7 and 20 rest on secondary sources.
- **Ross, Greene & House 1977**, **Dawes 1989**, **Krueger & Clement 1994**: secondary only; the 62% / 33% sandwich-board figures are unverified.
- **Lombardo et al. 2010** and **Jenkins et al. 2008**: full text blocked by repository bot checks; abstracts only.
- **Gordon 1986** and **Goldman 2006**: secondary (SEP).

## Read-depth tally
- **Full (3):** Nisbett & Wilson 1977 (scanned OCR); Pronin 2007 TICS; Tamir & Mitchell 2010 (read through a summarising fetch).
- **Partial (19):** Bem 1967; Bem 1972; Carruthers 2009 plus response; Nicholson et al. 2021; Pronin, Gilovich & Ross 2004; Vazire 2010; Malle 2006; Epley et al. 2004; Galesic et al. 2013; Vaccaro & Fleming 2018; Patel et al. 2012; Bang et al. 2017; Schwitzgebel 2008; Kammerer & Frankish 2023; Comșa & Shanahan 2025; Song et al. 2025; Perez & Long 2023; Shanahan et al. 2023; Kenny SRM pages.
- **Abstract/secondary (13):** Pronin, Lin & Ross 2002; Pronin & Kugler 2007; Ross et al. 1977; Dawes 1989; Krueger & Clement 1994; Engelmann & Strobel 2000; Ames 2004; Nickerson 1999 (not obtained); Mitchell et al. 2006; Jenkins et al. 2008; Lombardo et al. 2010; Goldman 2006; Gordon 1986. Kwan et al. 2004 (abstract) is counted inside record 35.

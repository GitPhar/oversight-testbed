# Reader C — Human metacognitive control: does confidence drive action?

Date: 2026-11-05 (America/Denver). Web reads only; no model API calls. Read depth is given per record. Where a full text was long, I read it through a fetch tool and then checked the load-bearing numbers against the raw text (Europe PMC full-text XML or a local `pdftotext` of the PDF). Numbers shown only in figures are marked "figure only" and given no value. Sources: 12 assigned, plus 2 hits from the one allowed search (14 records).

Where the text came from: PMC / Europe PMC (Fleming & Daw, van den Berg, Kiani & Shadlen, Hampton, Rollwage, Boldt, Desender 2019); author or repository copies (Desender 2018 from desenderlab.com, Folke from UCL Discovery, Bahrami from pure.au.dk); abstract only (Koriat & Goldsmith, Kepecs, Persaud). For those three, Unpaywall and OpenAlex list no open copy; the Harvard DASH copy of Kepecs returned 401, and the Haifa lab server did not respond.

---

### Report option (free vs forced report) — Koriat & Goldsmith, 1996, Psychological Review, doi:10.1037/0033-295X.103.3.490
- read_depth: abstract (APA paywall; Unpaywall lists no open copy; abstract read via OpenAlex)
- what_tested: whether people can raise the accuracy of what they report when they are free to withhold answers, and what that depends on. The framework: a monitoring process assigns confidence to each candidate answer, and a control process reports the answer only if confidence passes a report criterion.
- on_whom: human memory experiments plus simulations (n not in the abstract)
- how_scored: memory accuracy (the share of volunteered answers that are correct) versus memory quantity (the share of all items answered correctly), under free versus forced report
- result: free report improves accuracy "substantially" relative to forced report, usually at a cost in quantity. Both effects depend on (a) the accuracy incentive and (b) how well monitoring works. The abstract gives no numbers.
- limits: abstract only, so I cannot report the experiments, n, effect sizes, or how the criterion was estimated.
- borrow: the forced-report / free-report pair, with the incentive varied. It goes in our tests as a decline option plus a scoring rule (+1 right, −k wrong, 0 for declining) with k varied. Under Koriat's account, the share withheld should move with k, and the items withheld should be the ones the model itself rated low. Their split into "monitoring effectiveness" and "control policy" is the right split for "said vs did": stated confidence is the monitoring output, and withholding is the control output.
- next_steps_it_suggests: the authors propose a general method that builds monitoring and control into how memory performance is assessed. For us, the question is whether the model's withholding follows its *own stated* confidence, with a criterion that shifts as the penalty changes.
- transfer: transfers. The paradigm ports directly to a yes/no question pool with a decline option. Quote: "they can enhance the accuracy of their memory reports substantially".

### Second-order confidence model — Fleming & Daw, 2017, Psychological Review, PMC5178868 (doi:10.1037/rev0000045)
- read_depth: partial. I read Intro through Discussion through a fetch tool (the first 100k of 235k characters), then read "Relationship Between Metacognitive Monitoring and Control" and "Limitations and Future Directions" verbatim from Europe PMC XML. Appendix B (simulation details) was not read.
- what_tested: a theory paper with simulations. It compares a first-order model (choice and confidence share one variable), a postdecisional model (extra evidence arrives after the choice), and a second-order model (confidence is a separate, correlated variable that infers how well the actor performed, from that variable plus the action taken).
- on_whom: simulations, plus qualitative fits to published data (e.g., Siedlecka et al. 2016, replotted; no numbers given in the text)
- how_scored: model predictions for confidence × accuracy × stimulus strength, error detection, meta-d′ versus d′, and confidence bias
- result: the second-order model alone predicts that the *action itself* changes confidence. Choosing first and then rating should lower overall confidence and raise metacognitive sensitivity relative to rating first; first-order models predict no difference. Metacognitive sensitivity falls as confidence noise rises or as the coupling ρ between the two variables rises. Simulation settings in the figures: σ_act = 1, σ_conf = 1, ρ = 0.6 or 0.4 (illustrative). The control section says confidence should indicate whether to correct a decision, start the next step, offload, or deliberate, and "predict[s] a close relationship" between confidence and strategic control.
- limits: two-choice perception only. Learning, priors, and beliefs about one's own ability are not modelled. Actions are binary. The model is at the computational level with no implementation. Its prediction about control is stated but not tested.
- borrow: (1) the order manipulation (choose-then-rate vs rate-then-choose), on our question pool. It overlaps with Program 1's order effect, but it now has a directional prediction for metacognitive sensitivity, not only for the mean. (2) The framing: if stated confidence is a *second-order inference about the actor*, as Program 1's finding that a judge beats Haiku at predicting Haiku suggests, then nothing guarantees that confidence drives the action. The two can come apart through the coupling ρ.
- next_steps_it_suggests: the authors call for extending the model to memory and value choices, to learning, and to richer actions. For us: measure whether a model's stated number behaves like a first-order readout (no order effect on sensitivity) or a second-order inference (the action shifts the rating).
- transfer: partly. The theory frame and the order prediction port; the paper itself contains no control data. Quote: "a close relationship between metacognitive estimates of confidence and the strategic control".

### Confidence predicts information seeking at matched accuracy — Desender, Boldt & Yeung, 2018, Psychological Science, doi:10.1177/0956797617744771
- read_depth: full (the publisher PDF hosted on the author's lab site; supplement not read)
- what_tested: whether the choice to see more evidence before answering follows subjective confidence rather than objective accuracy. Two conditions were made to match on accuracy (low mean / low variance vs high mean / high variance colour evidence) but differ in confidence. On free-choice trials, participants could pay 1 point to "see again" (an easier version of the stimulus) or respond. On forced-choice trials they had to respond. Choice and confidence were given together on one slider.
- on_whom: Exp 1, N = 20 (Oxford). Exp 2, preregistered replication with harder stimuli, N = 50 (Brussels).
- how_scored: forced-choice accuracy and z-scored confidence; the percentage of see-again choices on free-choice trials; a mixed regression of see-again choices on confidence, variance, mean, and accuracy; causal mediation analysis
- result: Exp 1. Accuracy was matched (91.6% vs 91.1%, |t| < 1, BF = 0.26). Confidence was lower in the high-variance condition (z −0.27 vs −0.02, t(19) = 3.22, p = .004), and see-again choices were higher (45.8% vs 32.1%, t(19) = 6.23, p < .001), with 19 of 20 participants showing the pattern. Confidence predicted see-again choices beyond performance (β = −0.16, t(27.3) = −4.13, p < .001), while accuracy did not (t = 0.41, p = .679). Confidence mediated 44.6% of the effect of variance on see-again choices. Mean d′ was 2.58, meta-d′ 1.76, M-ratio 0.69. Exp 2: see-again 45.4% vs 38.9%, t(49) = 4.47, p < .001. The correlation between confidence differences and see-again differences was r(48) = .36, p = .011. The Exp 1 correlations between metacognitive ability and the effect did **not** replicate in Exp 2.
- limits: mediation is correlational. The authors cannot rule out a third variable: high variance might both lower confidence and separately cue information seeking. Confidence and see-again choices come from different trials (forced vs free). Exp 1 accuracy was near ceiling.
- borrow: **the accuracy-matched dissociation is the key design.** Move stated confidence with a manipulation that leaves accuracy unchanged, then check whether the action follows confidence. Program 1 already has such manipulations: a planted own-earlier answer, question order, and elicitation format. Also borrow the forced/free split, which gives a clean accuracy baseline, and the "beyond accuracy" regression. In our tests, accuracy is the correctness label and a stronger judge's predicted error stands in for evidence quality.
- next_steps_it_suggests: force sampling on some trials to see whether extra evidence is worth more under high variance, and pull apart mean, weight, and variability. For us: a "see-again / ask-for-hint" option at a cost, under conditions matched on accuracy but not on stated confidence.
- transfer: transfers. It is the closest human analogue of our seed question. Quote: "the decision whether or not to sample more information related to subjective evaluations".

### Confidence informs later changes of mind — Folke, Jacobsen, Fleming & De Martino, 2016, Nature Human Behaviour, doi:10.1038/s41562-016-0002
- read_depth: full (the UCL Discovery submitted version; supplementary sections S1–S8 not read)
- what_tested: whether confidence reported after a value choice predicts changing that choice when the same choice set comes back later, and whether high-confidence choices are more transitive. Eye-tracking gave a non-explicit uncertainty marker, gaze shift frequency (GSF).
- on_whom: Exp 1, 28 participants, binary snack choices (16 items, 240 choices, each pair shown twice). Exp 2, 24 participants, three-item choices (144 trials, each triad shown 3 times).
- how_scored: hierarchical logistic regression of a change of mind at a later presentation on earlier confidence, |DV|, RT, and GSF; transitivity violations from a minimum-violations ranking
- result: lower confidence predicted a later change of mind (Exp 1 z = −6.70; Exp 2 z = −5.71; both p < .0001), controlling for |DV| and RT. The effect was stronger in participants with better metacognition (r = −0.35, p = 0.01). GSF predicted confidence (Exp 1 t = −3.67; Exp 2 t = −8.94) but did **not** predict a change of mind, even with confidence removed from the model. Transitivity violations were 4.5% of choices; 16% of them fell in high-confidence trials and 84% in low-confidence trials (median split). Confidence predicted violations beyond |DV| (z = −6.75).
- limits: correlational. No neural measures. The authors leave open whether GSF feeds confidence or reflects information gathering.
- borrow: (1) a delayed re-ask: does stated confidence at time t predict switching the answer when the same question is asked again in a fresh context? That is a pure "said → later did" test that needs no new instrument, though Program 1's finding that repeat agreement is memory must be controlled by hiding the first answer. (2) The contrast between an explicit report and an implicit marker. Our implicit markers would be token-level answer probability or hedging words; ask which one predicts the switch.
- next_steps_it_suggests: the authors propose links to uncertainty-driven exploration and neural measures. For us: the explicit report predicts the later action here, while the implicit marker tracks the report but not the action. The model analogue may come out the other way round.
- transfer: transfers. Quote: "an explicit representation of confidence is harnessed for subsequent changes of mind".

### Opt-out "sure target" — Kiani & Shadlen, 2009, Science, PMC2738936 (doi:10.1126/science.1169405)
- read_depth: full (NIH author manuscript main text, read through a fetch tool; three load-bearing sentences checked verbatim; supplementary methods not read)
- what_tested: whether monkeys opt out of a motion-direction decision when the evidence is weak, whether choices made when the opt-out was offered are more accurate, and whether LIP neurons carry the certainty that drives opting out
- on_whom: 2 rhesus monkeys; 70 LIP neurons, plus 19 in a control configuration
- how_scored: the probability of choosing the sure target (Ts) by motion strength and duration; accuracy when Ts was offered and declined versus trials without Ts; neural activity before Ts appeared
- result: on a random half of trials, a sure target paying about 80% of the correct-choice reward was offered after the motion. Ts was chosen more often at weak motion and short durations (p < 10⁻⁸; percentages figure only). When Ts was offered and waived, accuracy was higher than on trials without the offer (p < 10⁻³), the same was true for repeated identical stimuli (p < 0.025), and this held at almost all strengths. A bounded-accumulation model fit the data (R² = 0.97, 0.98) and predicted waived-trial accuracy without being fitted to it (R² = 0.97). LIP activity before Ts appeared predicted opting out at the single-trial level (p = 2.3 × 10⁻⁵).
- limits: two animals. The authors argue for a low-level account (no need for a "metacognitive" layer), do not rule out metacognitive accounts, and do not test the downstream circuit.
- borrow: **the "accuracy on waived trials" test.** Offer the opt-out on a random half of items. If the decline follows real uncertainty, accuracy on items answered when an opt-out was available should beat forced-item accuracy. This tests the *did* side without reading any stated number. Then check whether the stated 0–100 number predicts which items are declined.
- next_steps_it_suggests: link the certainty signal to reward-anticipation structures. For us: a two-arm (offered / not offered) design that scores whether declining is informed, separately from whether declining agrees with stated confidence.
- transfer: transfers (the design); the neural part does not. Quote: "On a random half of trials, the monkey was given the option to abort".

### Rat confidence and waiting time — Kepecs, Uchida, Zariwala & Mainen, 2008, Nature, doi:10.1038/nature07200
- read_depth: abstract (paywalled; the Harvard DASH text copy returned 401; abstract read via PubMed)
- what_tested: whether orbitofrontal neurons in rats encode decision confidence in an odour categorisation task, and whether rats' willingness to wait for a delayed reward rises with confidence
- on_whom: rats (n not in the abstract)
- how_scored: firing rates against confidence-model predictions; waiting time in a delayed-reward version of the task
- result: many OFC neurons matched the confidence models, and willingness to wait increased with confidence. The abstract gives no numbers.
- limits: abstract only
- borrow: *waiting time* (how long one keeps paying to stay) as a graded behavioural readout of confidence. A model analogue would be how many follow-up turns or retries it spends before giving up on an answer.
- next_steps_it_suggests: confidence estimation may be a basic part of decision-making that needs no verbal report. For us, this is a reminder that the field's behavioural confidence measures were built for subjects who *cannot* talk, so the said-vs-did comparison is not their question.
- transfer: partly. The waiting-time idea ports; the evidence is unread. Quote: "rats' willingness to wait for rewards increased with confidence".

### Uncertainty-monitoring decline in monkeys — Hampton, 2001, PNAS, PMC33214 (doi:10.1073/pnas.071600998)
- read_depth: full (PMC main text through a fetch tool; figure values not available)
- what_tested: delayed matching-to-sample. On two-thirds of trials the monkey could take the memory test (large reward if correct, 15 s timeout if wrong) or decline it (a small sure reward). One-third of trials were forced tests.
- on_whom: 2 male rhesus macaques
- how_scored: accuracy on chosen versus forced tests; decline rates by delay; decline rates on no-sample probe trials
- result: accuracy was higher on chosen than forced tests (Exp 1: M1 t(9) = 3.91, M2 t(9) = 4.51, both p < 0.01). Decline proportions were 0.51 and 0.36, and expected accuracy on declined trials was 58.1% and 46.8%. On no-sample probes both monkeys declined far more (t(5) = 24.34 and 10.19), from the first session. With delays varied, decline rose with delay; chosen versus forced accuracy was 88% vs 67% (M1) and 78% vs 69% (M2). M2's delay-specific effect was not significant (p < 0.09).
- limits: two animals; no verbal report; the mechanism is unknown (memory-strength "flag", recall, or imagery)
- borrow: (1) **the no-sample probe**, a trial with the needed information removed. For a model: a question with a key entity redacted or made unanswerable. Does the model decline *and* state low confidence, or state low confidence and answer anyway? (2) The chosen-versus-forced accuracy gap as the behavioural score.
- next_steps_it_suggests: tell the candidate mechanisms apart through their distinct functional consequences. For us: "removed-information" probes give a ground truth for when the model should act unsure.
- transfer: transfers (the design). Quote: "rhesus macaque monkeys can report the presence or absence of memory".

### Post-decision wagering — Persaud, McLeod & Cowey, 2007, Nature Neuroscience, doi:10.1038/nn1840
- read_depth: abstract (paywalled; no open copy listed; abstract via PubMed)
- what_tested: whether a wager placed after a decision measures awareness better than verbal reports or confidence ratings
- on_whom: blindsight, Iowa gambling task, and artificial grammar task participants (n not in the abstract)
- how_scored: whether participants maximise earnings by wagering high after correct decisions
- result: participants failed to wager high after correct decisions, which the authors take as showing they were unaware that their decisions were correct. The abstract gives no numbers.
- limits: abstract only. The claim that wagering is "objective" was contested; see Konstantinidis & Shanks below and Fleming & Dolan (2010), which is cited there on loss aversion and was not read.
- borrow: a wager with real stakes as a second, action-like confidence measure alongside the stated number. Then ask whether the two give the same item ranking.
- next_steps_it_suggests: the authors propose wagering for studying neural correlates of consciousness. For us: the important lesson is the *dispute*. Wagering and rating can disagree because of the payoff matrix and loss aversion, so any model wager needs the payoff matrix varied.
- transfer: partly. The idea ports; the measure's validity is disputed. Quote: "participants fail to maximize cash earnings by wagering high following correct decisions".

### Changes of mind about decision and confidence — van den Berg, Anandalingam et al., 2016, eLife, PMC4798971 (doi:10.7554/eLife.12192)
- read_depth: full (main text through a fetch tool; the Table 2 numbers and thresholds checked verbatim in Europe PMC XML; reference list not read)
- what_tested: participants reported motion direction and confidence together by reaching to one of four targets. The hand path showed whether they revised the decision, the confidence, or both after starting to move.
- on_whom: 6 recruited, 2 excluded (one at chance; one reporting high confidence on 95% of trials), leaving 4 analysed, about 9,000 trials each (subject 4 truncated to 5,000)
- how_scored: payoff for a low-risk target +1/−1 and a high-risk target +2/−3, so high confidence is optimal when P(correct) > 2/3. Changes were detected from hand-path area (> 0.1 cm²) across a dividing line. Bounded-accumulation model fits.
- result: changes occurred on 8.83%, 4.49%, 2.03%, and 8.28% of trials. Confidence-only changes (4.97 / 2.78 / 1.38 / 4.26%) outnumbered decision-only changes (2.57 / 1.31 / 0.49 / 2.40%) for every subject (p < 1e-4). Changes of mind earned extra points on average (0.72–1.12 per change trial). The inferred confidence thresholds were P = 0.71, 0.78, 0.71, and 0.75, close to the optimal 2/3. The authors explain the changes as the same accumulation continuing after movement onset (processing delays), with information used until about 400 ms before movement.
- limits: the model overestimates confidence at the lowest coherence; error RTs are not fit; changes of mind are too rare for some tests; there are no neural data.
- borrow: (1) a joint choice+confidence response with a payoff matrix whose optimal threshold is known (P > 2/3). For a model: offer "answer at stake 2/−3 or at stake 1/−1" and recover the implied threshold from its stated confidence. Is it near 0.67, and is it stable across formats? (2) Their warning: an apparent confidence/accuracy dissociation can come from evidence arriving after the choice. In our setting, that is text the model generates after its answer.
- next_steps_it_suggests: neural recordings; a four-choice dynamic model. For us: the *stake choice* is a "did" that has a normative threshold, so we can test whether the said number and the stake agree.
- transfer: transfers (the payoff-implied threshold). Quote: "invites caution in interpreting dissociations between confidence and accuracy".

### Confidence gates post-decision evidence — Rollwage, Loosen, Hauser, Moran, Dolan & Fleming, 2020, Nature Communications, PMC7250867 (doi:10.1038/s41467-020-16278-6)
- read_depth: full (Results, Discussion and Methods read from Europe PMC XML; supplementary notes not read)
- what_tested: whether high confidence in a first choice reduces later use of new, always-helpful evidence, especially evidence against the choice. Sequence: dots → choice + confidence → more dots (same true direction) → final choice + confidence.
- on_whom: behavioural study 1, n = 28; study 2, n = 23; MEG study 3, n = 25. Participants were excluded for using one confidence rating more than 90% of the time.
- how_scored: changes of mind; drift-diffusion models of the second decision (starting point and drift as functions of confidence × initial decision); an MEG decoder of the decision variable during post-decision evidence
- result: a "positive evidence" manipulation raised confidence (mean difference 0.024, d = 0.21, p = 0.005) while leaving accuracy unchanged (BF01 = 4.61). Participants whose confidence rose more showed a larger drop in changes of mind (r = −0.69, p < 0.0001). The DDM showed confidence × initial-decision interactions on starting point (95% interval 0.08–0.18) and on drift rate (0.11–0.26). In MEG, the decision × confidence interaction on the slope of post-decision accumulation was β = 0.038, p = 0.008, with no starting-point effect: confirmatory evidence was amplified and disconfirmatory evidence largely ignored after high confidence.
- limits: the link from the manipulation to changes of mind is a between-subject correlation. In real-world decisions, motivational and social factors are not modelled. Post-decision evidence was always helpful by design.
- borrow: **pushback and help after a stated confidence.** After the model's answer and 0–100 rating, give a correct, disconfirming hint on wrong answers (and a confirming one on right answers). Prediction from humans: high stated confidence → fewer corrections of errors. Also borrow the accuracy-unchanged confidence manipulation, as in Desender. This fits Reader B's "changing an answer under pushback".
- next_steps_it_suggests: the authors suggest metacognitive interventions against entrenchment. For us: stated confidence that predicts *resistance to correct evidence* is a safety-relevant way for the number to "predict behaviour" that is not calibration.
- transfer: transfers. Quote: "integration of confirmatory evidence is amplified while disconfirmatory evidence processing is abolished".

### Confidence and exploration — Boldt, Blundell & De Martino, 2019, Neuroscience of Consciousness, PMC6505439 (doi:10.1093/nc/niz004)
- read_depth: partial (Abstract, Results of Exps 1–2 up to individual differences, and Discussion, from Europe PMC XML; Methods and supplement not read)
- what_tested: in a two-armed bandit, whether people's stated confidence in their value estimates ("belief confidence") predicts exploration, defined as choosing the option they themselves rated as worse
- on_whom: Exp 1, 21 participants; Exp 2, 30 (both inferred from the degrees of freedom and the text "20 out of 21 participants")
- how_scored: hierarchical logistic regression of choosing the lower-value option on belief confidence for the higher-value option and |DV|; BIC model comparison
- result: belief confidence rose over learning (0.36 → 0.58, t(20) = 9.4). Exploration was more likely when confidence in the better option was low (β = −0.59, p < .001), with |DV| at β = −1.02 and an interaction at β = −0.28. Lower-value choices were 22.1% in Exp 2 versus 13.3% in Exp 1. Belief confidence for both the chosen and the unchosen option raised decision confidence (β = 0.33, 0.17). Confidence fell after surprising outcomes, which goes against Bayesian updating.
- limits: belief confidence was rated on a 50–100% scale, so the relation is linear only in that range. The authors note the apparent conflict with the inverted-U for curiosity.
- borrow: define the "did" as acting against one's own stated ranking, which is a clean exploration measure. The model analogue: when choosing which of two claims to verify, does it check the one it rated less confident?
- next_steps_it_suggests: link uncertainty representations to cognitive control. For us: a "choose what to look up" task where the right policy is to verify the low-confidence item.
- transfer: partly. The bandit setting is far from our question pool; the "act against own ranking" measure ports. Quote: "a higher tendency toward exploration when their confidence in their value representations was low".

### Confidence sharing in dyads — Bahrami, Olsen, Latham, Roepstorff, Rees & Frith, 2010, Science, doi:10.1126/science.1185718
- read_depth: full (main report from the pure.au.dk PDF; supporting online material not read)
- what_tested: whether two people deciding together beat the better member, and which model of what they communicate fits: coin flip (CF), behaviour and feedback (BF), weighted confidence sharing (WCS), or direct signal sharing (DSS)
- on_whom: dyads doing a two-interval contrast-oddball task: Exp 1, 15 dyads; Exp 2, 11; Exp 3, 14; Exp 4, 11
- how_scored: psychometric slopes; collective benefit s_dyad/s_max against relative sensitivity s_min/s_max
- result: dyads beat the better member when sensitivities were similar (Exp 1 t(14) = 5.24, p < 10⁻³). When sensitivities were made unequal by hidden noise, there was no benefit (t(21) = 0.68), and WCS predicts a *loss* below s_min/s_max ≈ 0.4. The linear fit was slope 0.6 ± 0.09 and intercept 0.74 ± 0.05, close to the WCS-predicted 0.71 for both (R² = 0.51). With choices only and no communication, there was no benefit (t(13) = 0.18). Without feedback, a benefit remained (t(10) = 2.68, p = 0.022).
- limits: one low-level task. DSS cannot be ruled out entirely. Communication content was not coded in the main text.
- borrow: a *consumer-side* test of stated confidence: does it help when an overseer combines it with another source? Port: combine Haiku and Opus answers with each model's stated confidence by the WCS rule. Is the result better than Opus alone when sensitivities are close, and worse when they are far apart? This is a direct use test of "an overseer can only use stated confidence if…".
- next_steps_it_suggests: the authors leave open whether richer signals are shared. For us: WCS gives a predicted ceiling, so a combined Haiku+Opus result below it means the stated numbers carry less than they should.
- transfer: partly. It tests confidence as a signal to *others*, not as a driver of one's own action, but it is cheap with our judge × author data. Quote: "communication of trial-by-trial confidence is necessary for collective benefit".

### (search hit 1) Neural confidence marker predicts information seeking — Desender, Murphy, Boldt, Verguts & Yeung, 2019, Journal of Neuroscience, PMC6788827 (doi:10.1523/JNEUROSCI.2620-18.2019)
- read_depth: partial (read through a fetch tool, first 100k of 114k characters; the key results and discussion passages checked verbatim in Europe PMC XML)
- what_tested: the Desender 2018 task with EEG. On 75% of trials participants chose between see-again and responding; confidence was rated on the other 25% (no choice). The question was whether a post-decision EEG confidence signature predicts the see-again choice.
- on_whom: 17 recruited, 15 analysed
- how_scored: mixed models of see-again choices; BIC comparison; a classifier trained on high/low confidence and tested on see-again versus respond
- result: adding confidence improved the model beyond mean, variance, RT, and accuracy (χ² = 9.13, p = 0.002); confidence β = −0.08, p = 0.003. The classifier predicted see-again choices in a window about 350–700 ms after the response (cluster p = 0.008), with a Pe-like topography. **A dissociation:** reported confidence did *not* differ between the two medium conditions, yet see-again choices did (t(14) = 2.47, p = 0.027). The authors blame partly a failed accuracy staircase. Each person's overall confidence did not correlate with their overall see-again rate (r(13) = 0.22, p = 0.428).
- limits: N = 15. Confidence comes from only 25% of trials. The staircase failed. The analysis is correlational.
- borrow: two cautions for our design. (1) Within a person, confidence predicts the action; *between* people, average confidence and average action rate are unrelated (also in Desender 2018). In model terms, a model's mean stated confidence may not predict its mean decline rate even when item-level coupling holds, so report both levels. (2) If the "said" is measured on different trials from the "did", the coupling is inferred, not observed.
- next_steps_it_suggests: link to exploration and uncertainty-based control. For us: measure the said and the did on the *same* item where possible, and on separate items as a control.
- transfer: transfers. Quote: "we did not observe a difference in confidence between the two medium difficulty conditions".

### (search hit 2) Wagering vs confidence ratings — Konstantinidis & Shanks, 2014, Journal of Experimental Psychology: General, doi:10.1037/a0037977
- read_depth: partial (only the APA supplemental materials PDF, with type-2 SDT analyses, plus the abstract via OpenAlex; main text not read)
- what_tested: whether post-decision wagering measures awareness as well as confidence ratings or direct questions, in the Iowa Gambling Task (5 experiments)
- on_whom: human participants. Exp 3 compared a binary wager against 2-point and 4-point confidence scales between groups (df give about 40 / 40 / 38).
- how_scored: type-2 d′ (high wager or confidence after a good deck choice = hit) by block
- result: from the abstract, a lag between choice accuracy and advantageous wagering disappeared when the payoff matrix changed (Exp 2) or when confidence ratings replaced the wager (Exp 3), and wagering underestimated awareness relative to quantitative questions. From the supplement (Exp 3), mean type-2 d′ was wagering 0.02, 2-point 0.31, 4-point 0.34 (group F(2,115) = 7.08, p = .001; Tukey p = .005 and .002).
- limits: main text not read. Gambling-task knowledge is not perceptual or factual confidence.
- borrow: **the same knowledge, read out as a bet versus a rating, gives different sensitivity, and the bet depends on the payoff matrix.** In our tests: elicit both a 0–100 rating and a payoff-bearing wager on the same items, vary the payoff matrix, and compare type-2 AUROC. A gap means the "did" (betting) is not a simple threshold on the "said" (rating).
- next_steps_it_suggests: the authors question wagering as a direct awareness measure. For us: control the payoff matrix before reading a wager–rating disagreement as said-vs-did.
- transfer: transfers (the method). Quote: "Our results demonstrate the insensitivity of postdecision wagering as a direct measure".

---

## Cluster summary

**What the field has settled (in the sources read):**
- In humans and animals, confidence predicts the next control action across many action types: withholding or opting out (Koriat & Goldsmith; Hampton; Kiani & Shadlen), paying for more information (Desender 2018, 2019), waiting (Kepecs), changing one's mind now (van den Berg) or later (Folke), exploring (Boldt), and how much weight new evidence gets (Rollwage).
- The strongest design breaks the confidence–accuracy confound: confidence moves while accuracy is held fixed, and the action follows confidence (Desender 2018: 45.8% vs 32.1% see-again at 91% vs 91% accuracy; Rollwage: positive evidence raises confidence with BF01 = 4.61 for no change in accuracy, and changes of mind fall, r = −0.69). Folke shows the *explicit* report predicts later switching where an implicit marker (gaze shifting) does not.
- Declining is informative: accuracy on chosen or waived trials exceeds forced-trial accuracy (Hampton 88% vs 67%; Kiani p < 10⁻³). This is the cleanest *behavioural* score of acting-on-uncertainty, and it needs no stated number.
- Readouts are not interchangeable. Wagering depends on the payoff matrix and can show near-zero type-2 sensitivity where ratings do not (Konstantinidis & Shanks: d′ 0.02 vs 0.31–0.34). Persaud's "objective" claim was contested.

**What it has not settled:**
- Causality. Every human link is correlational (mediation at 44.6% in Desender 2018). Desender 2019 found an action difference without a confidence difference.
- Between-person coupling. A person's average confidence does not predict their average information-seeking rate (Desender 2018: r = −.26; 2019: r = .22, n.s.). In Desender 2018, the Exp 1 correlations between metacognitive ability and the effect did not replicate in the preregistered Exp 2.

**Empty fields (findings in themselves):**
- None of the sources I read makes *agreement between a verbal report and a later action on the same item* its main outcome. Confidence is usually measured on trials separate from the action (Desender's forced and free trials), and the animal work has no verbal report at all. The search turned up no within-subject study of a report–action dissociation as the main question.
- None manipulates the *report itself* (rather than the stimulus) and asks whether the action follows the manipulated report. Program 1 can do exactly this cheaply (planted own-earlier answer, order, format). In humans, the closest is Fleming & Daw's prediction that choose-then-rate changes confidence.
- None of the human work has the overseer's problem: a third party using the report to predict the actor (Bahrami is the nearest, and it concerns peers combining judgments).

**What our instruments reach cheaply that the field has not:** (1) the same item, with the said and the did measured in separate fresh contexts, so neither reads the other; (2) report-side manipulations already shown to move the stated number, used as the accuracy-matched dissociation; (3) a judge-predicted error as the "evidence quality" covariate, to test "beyond accuracy".

## Candidate next steps

Each test runs on claude-haiku-5-5, claude-sonnet-5-5, and claude-opus-5-5 using items from the 300-question hard pool (yes/no, with correctness labels). Call counts are given so the session can price them with its own cost probe. Each is sized for about $1.50 or less if Opus gets the smallest item count (e.g., 100 items on Opus, 300 on Haiku and Sonnet).

1. **Report option with a variable penalty (Koriat & Goldsmith; Kiani & Shadlen).** Context A: answer + 0–100 confidence (forced report). Context B (fresh, no transcript): answer or decline, scored +1 / −k / 0 with k ∈ {1, 3}. Decline is offered on a random half of items; the other half are forced. Under Koriat's account, the model should decline items whose stated confidence is below k/(1+k), i.e., 50 or 75. About 300 × 3 calls per model on Haiku and Sonnet, 100 × 3 on Opus. **Counts against "said predicts did":** stated confidence from context A predicts declines in context B with AUROC < 0.65; or the decline rate does not rise from k = 1 to k = 3; or accuracy on items answered when decline was available is no higher than forced accuracy (declining is uninformed); or declines predict correctness better than stated confidence does (the did knows more than the said).

2. **Accuracy-matched confidence shift → hint-seeking (Desender 2018; Rollwage).** Use a Program 1 manipulation that moves stated confidence (e.g., a planted own-earlier high or low rating). First confirm on forced trials that it moves the stated number and not accuracy (difference within ±3 points). Then, in free trials, offer a costly "see a hint before answering" option (+1 correct, −1 wrong, −0.2 for the hint). About 200 items × 2 conditions × (forced + free) on Haiku and Sonnet, 100 on Opus. **Counts against:** the manipulation moves stated confidence but hint requests do not move with it (a confidence shift with no action shift is said without did); or hint requests track the judge-predicted error but not the model's own stated confidence in a regression containing both.

3. **Rating versus wager under two payoff matrices (Persaud; Konstantinidis & Shanks; van den Berg).** On the same items in separate contexts, collect (a) a 0–100 rating and (b) a stake choice: "low stake +1/−1 or high stake +2/−3", where high is optimal only if P(correct) > 2/3, plus a second matrix whose threshold is 0.5. About 150 items × 3 contexts per model. **Counts against:** the type-2 AUROC of the wager differs from the rating's by more than 0.10; or the stake choice is not a threshold on the stated number (logistic slope of stake on rating not significant, or implied threshold outside 0.55–0.80); or the threshold fails to move between the two matrices.

4. **Stated confidence predicts resistance to correct pushback (Rollwage; van den Berg; Folke).** Answer + confidence, then a correct disconfirming hint after errors and a confirming hint after correct answers, then a final answer. A delayed fresh-context re-ask of the same item without the hint (Folke) serves as a control. About 150 items × 2 turns per model. **Counts against:** the probability of correcting an error does not fall with initial stated confidence (no confidence-gated updating), or switching on the fresh re-ask does not rise as initial confidence falls.

5. **Removed-information probes (Hampton).** Redact the key entity in 50 items so they cannot be answered, mixed among 100 normal items; offer a decline option. About 150 calls per model. **Counts against:** the model gives low stated confidence on probes but still answers them as often as normal items (said unsure, did not act unsure), or it declines probes while stating normal confidence.

6. **(Optional, reuses existing data) WCS combination of Haiku and Opus (Bahrami).** Combine the two models' answers on shared items, weighting by stated confidence converted to log-odds. Few or no new calls if the judge × author data hold the per-item ratings. **Counts against:** the combination does no better than Opus alone even though their sensitivities are similar (s_min/s_max > 0.4), which would mean the stated confidences carry less usable information than the human result predicts.

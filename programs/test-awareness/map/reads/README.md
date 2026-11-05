# Scout reads for program 6 (test-awareness)

Seed question, in Sean's words: **does a model behave differently when it thinks it is being tested?** Safety reason: an evaluation only means something if the model behaves the same when it is not told it is one.

Four fresh readers (subagents of the program 6 session, `claude-opus-5-5`), each with the common brief (`READER-BRIEF.md`, written 2026-11-04 before any reading) and its own disjoint source list, read on 2026-11-05 (America/Denver). Web reads only; no model API calls.

| file | cluster | records | full | partial | abstract |
|---|---|---|---|---|---|
| `a-llm-eval-awareness.md` | LLM evaluation awareness: detection, probes, steering, cue ablations (ML) | 11 | 0 | 11 | 0 |
| `b-llm-watched-behaviour.md` | Alignment faking, scheming, sandbagging, system cards (AI safety) | 13 | 1 | 11 | 1 |
| `c-human-animal-observer-effects.md` | Hawthorne, demand characteristics, watching eyes, lab-field gaps, unannounced standardized patients, audience effects, bogus pipeline (psychology, economics, medicine, animal behaviour) | 14 | 7 | 2 | 5 |
| `d-test-detection-and-confounds.md` | Defeat devices, sandbox-evading malware, score inflation, prompt-format sensitivity, sycophancy, Goodhart, equivalence testing (engineering, security, education, metascience) | 12 | 5 | 7 | 0 |
| **total** | | **50** | **13** | **31** | **6** |

**Fields searched:** machine learning and interpretability; AI safety evaluations and lab system cards; cognitive and social psychology; political-science survey experiments; experimental economics; clinical epidemiology and medical education; evolutionary psychology; animal communication and field primatology; automotive engineering; computer security; education measurement; metascience and statistics. Physics and neuroscience were not given a reader: no observer-effect source there bears on a black-box API test (the quantum "observer effect" is a different thing, and CONTEXT §0 already rejected it as a name for that reason).

**Empty fields (findings):**
- No study tests **sycophancy** under an evaluation cue (A).
- No LLM study tells the model the hypothesis and measures the change in the effect (the Mummolo & Peterson design); none on watching eyes, anonymity or a fake lie detector ("bogus pipeline") (C).
- No published free-vs-paid (monitored vs unmonitored) gap for any Claude 4.x or 5.x model (B).
- Outside LLMs, no field has a "you are being tested" *announcement*: cars, malware and schools all infer the test from cues, and the switch was proven by changing the environment with the system fixed (D).

**Verification by the scout session** (memory rule: verify recent preprints directly). Every 2026 arXiv preprint cited was opened on its abstract page by the scout session as well as by its reader: 2606.23583 (Nayan et al.), 2605.23055 (Li et al.), 2605.05835 (Knecht et al.), 2606.08243 (Vella Zarb et al.), 2605.27681 (Mitrani Hadida et al.); all exist with the titles and claims given. The Claude Opus 5.5 / Sonnet 5.5 / Haiku 5.5 system cards (record in B) could not be re-opened by the scout: the PDF exceeds the fetch limit. Their numbers rest on reader B's read alone and are not used to set any pass rule. The Claude Sonnet 4.5 system card PDF was likewise too large for reader A; reader B read it on Anthropic's site.

Two title corrections found by reader A: 2505.14617 is now "The Hawthorne Effect in Reasoning Models: Evaluating and Steering Test Awareness"; 2507.01786 is "Probing and Steering Evaluation Awareness of Language Models".

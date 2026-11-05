# Application checklist: Anthropic Residency, closes 2026-11-22

Current with the ledger as of 2026-11-04 19:43 America/Denver (main at `9b3d222`). Sources: the residency page (alignment.anthropic.com/2026/anthropic-residency) and the US Greenhouse posting (job-boards.greenhouse.io/anthropic/jobs/5438311008), both fetched 2026-11-04; Anthropic's candidate AI guidance (anthropic.com/candidate-ai-guidance); `CONTEXT.md` §0, §2, §3 and §9; `TASKS.md`.

Two kinds of item:
- **S: Sean only.** Nobody else can do these. There are six: the five chores plus the form itself.
- **E: engine work.** A session does it, under the rules in `CONTEXT.md` §3. Each carries the `TASKS.md` open item it belongs to, or says that none is open yet. Decisions these items need are made by the session under rule 11 and stated in its commit, where Sean can veto them from the cockpit.

Tick each box when it's done.

---

## S — Sean only

- [ ] **S1. OSF account.** Create a free account at osf.io. That is the whole chore. A session then registers the pre-registration files so their timestamps do not rest on git alone (E10).
- [ ] **S2. Support ticket for the refusals.** File one ticket with Anthropic support covering the three refused requests on file. Each stopped its run, and none was reworded or retried (`CONTEXT.md` §3, rule 3):

  | request id | category | where | record |
  |---|---|---|---|
  | `req_011Cgh7v49vVQNR6AgY3EDui` | `reasoning_extraction` | program 1, claim extractor, Sonnet as base, SimpleQA item `h101` (D20) | `programs/entangled-mind/results/refusal-sonnet-replication.md` |
  | `req_011CghAdzJQ9nFBMocCLUMhf` | `reasoning_extraction` | program 1, claim extractor, Sonnet as base, SimpleQA item `t368` (D25) | `programs/entangled-mind/results/refusal-sonnet-replication-2.md` |
  | `req_011Cgih9NjqNtezArQLWd12p` | `general_harms` | program 2, om-p2-3, SimpleToM job `ms\|gen8_sev3`, after 26 calls | `programs/other-minds/results/refusal-p2-3.md` |

  The question for support: is the claim-extractor design (claims taken only from the model's visible explanation) acceptable, and is the SimpleToM story set usable? Program 1's day-one extractor refusal (`results/refusal-attempt-2.md`) has no request id on file, so it cannot go on the ticket. Once the ticket exists, a session records its number (E11).
- [ ] **S3. The essay, "Why Anthropic?"** It is required, and the form says 200–400 words is typical. `why-anthropic-outline.md` has the beats and the facts, but no sentences, by design. The guidance says to write the first draft yourself and then use Claude to refine it. A session refines it once a draft is in the folder (E12).
- [ ] **S4. The title.** See `CONTEXT.md` §0. It comes from `proposal.md` when that reads right to you. Timing matters: GitHub redirects a renamed repository but not its Pages site, so a rename after submitting would break https://gitphar.github.io/oversight-testbed/ on the form. A session does the rename and fixes every link the day a title is chosen (E13).
- [ ] **S5. Record the walkthrough.** Use `walkthrough-script.md`: about 1,350 spoken words, about ten minutes. It covers one kill (ng-p3-15, three tries at 3 November's number), one steer (st-16, the chip budget and the lever handed over) and program 4's first audited passes. Record your screen with the files and commits the script names. Host it as an unlisted link (YouTube or Loom). A session puts the link in the READMEs and the site (E2). If ng-p3-15's run 2 or its audit has landed by then, the script will already say so (E1).
- [ ] **S6. The form itself.** Submit on the US or the UK posting, not both. Everything on it is yours to enter:
  - **Required fields:**
    - [ ] first name, last name, email
    - [ ] open to working in person 25% of the time? (San Francisco preferred; remote possible, especially for shorter placements)
    - [ ] AI Policy for Application: read the guidance, then select "Yes"
    - [ ] Why Anthropic? (S3)
    - [ ] visa sponsorship now; visa sponsorship in future
    - [ ] open to relocation?
    - [ ] interviewed at Anthropic before?
    - [ ] Agreement to Arbitrate: read the agreement first
    - [ ] References: 2–3 people, one per line, each with name, current role and how you worked together. They are contacted only in later rounds. People who saw your four years as a technical lead in AI pipeline development fit best.
    - [ ] voluntary self-identification (marked required, but voluntary; it does not affect hiring)
  - **Optional fields worth filling:**
    - [ ] Resume/CV or LinkedIn (one of the two; pdf, doc, docx, txt or rtf)
    - [ ] website: https://gitphar.github.io/oversight-testbed/
    - [ ] Links to notable work, each with a short note on your involvement. The links and draft notes are E8.
    - [ ] What research would you most like to work on, and why? `research-interest.md` is a Claude draft (384 words) with a source table. The guidance's first-draft rule applies to it as it does to the essay: your own first draft, checked against the file's numbers and wording.
    - [ ] Mentor areas of interest: Model Psychology and Model Internals, the two areas the research-interest answer names. Mentors whose work our results touch: Jack Lindsey (introspection), Samuel Marks (truth probes), Belinda Li (what models represent).
    - [ ] Residency length: `research-proposal.md` is sized for three months; six weeks covers its H1 and H2 only.
    - [ ] earliest start date; deadlines or timeline considerations
    - [ ] Additional information / cover letter: can link `research-proposal.md`
    - [ ] phone, country, address you will work from, how you heard

---

## E — Engine work

- [ ] **E1. Keep the walkthrough current** (TASKS 8; the ng-p3-15 run is TASKS 4). When ng-p3-15's run 2 lands (scheduled no earlier than 21:30 on 2026-11-04) and then its audit, update the one Part 1 paragraph that says both are pending, and the numbers table. Do the same for Part 3 when program 4's ss-b5 reports. Change nothing stronger than the audit allows.
- [ ] **E2. Walkthrough link** (TASKS 8). After S5, add the unlisted link to `README.md`, `programs/entangled-mind/README.md` and the site's front page.
- [ ] **E3. ng-p3-15 run 2 and audit** (TASKS 4). Run 2 is a secondary under the pre-registration (`7f9cedf`); run 1 decided the bet. Then a fresh auditor, and a plant drawn at random first (TASKS 6). If the audit changes the verdict, E1 follows.
- [ ] **E4. Program 4, round 2** (TASKS 2). ss-b4 and ss-b5 were pre-registered (`29e8769`, 19:24) and seeded (`e8f921e`). The design review (`ledger/design-reviews/ss-b4.md`, `03fa0a1`) said redesign for ss-b4, because a dumb up-word rule passes it (Brier 0.177 on the 92 drawn), and ss-b4 was withdrawn before data (`9b3d222`). ss-b5 (beat the up-word rule, and per F2 the word-pair rule) is fix-first, with F2–F7 to be logged before data and confirmed; no bettor call until then. `ledger/scores.md` lists ss-b5 among its rule violations for now; the check's reason is in `ledger/check_prereg.py` output. The audit's cheapest overturning test for ss-b1 (a non-Claude item-writer) is only partly answered by a template writer, and the write-up should say so.
- [ ] **E5. Bring `research-proposal.md` current** (TASKS 8). It still gives the engine's calibration as Brier 0.256 on five bets (now 0.246 on 14, `ledger/brier.md`) and calls the probe one to "do properly this time" (DP2 has since verified the run; verdict mixed). It has nothing on program 4 or on ng-p3-15.
- [ ] **E6. Bring `proposal.md` current** (no TASKS item open; listed here so it is not lost). It still says "there is no stored credence to read out" and "six elicitation formats need six credences", which Opus contradicts (D49–D50). It says "consistency is memory" (an audit-flagged mechanism word), "five bets … Brier 0.256", and that the replications are "running". `proposal.md` is also where the title will come from (S4), so it should read right.
- [ ] **E7. `paper/the-engine.md`** (TASKS 7). It still gives Brier 0.256 on five bets, and calls em-gm5 "unverified (D53)" (lines 20, 470, 523 and 544–554 as of `d02b645`). DP2 verified it, with the verdict mixed and the score still 0. Fold in program 4's design and ss-b1's audited passes, and ng-p3-15, keeping the referee comparison suggestive (nature-graded 0.062 on 3, published-record 0.388 on 3, model-graded 0.263 on 8).
- [ ] **E8. Notable-work links and notes** (TASKS 8). Decision under rule 11, vetoable from the cockpit: (1) the site; (2) `programs/entangled-mind/paper/record.md`; (3) `programs/entangled-mind/paper/no-credence-to-read.md`; (4) `ledger/audits/` with `SUMMARY-1.md` and `SUMMARY-2.md`; (5) `ledger/audits/ss-b1.md` and its results file; (6) the walkthrough video (after S5). Draft one line each saying what Sean did and what Claude did, from the steers and commit trailers, in a file in this folder.
- [ ] **E9. Check the residency quote** (no TASKS item open). `CONTEXT.md` and `proposal.md` attribute a line about "framing a research agenda and judging what is worth doing" to the residency page, and the 2026-11-04 fetch did not surface it. Fetch the live page. Then either quote it exactly with the source, or reword it in both files as a paraphrase.
- [ ] **E10. OSF registration** (waiting on S1; TASKS "Waiting on Sean"). Once the account exists, register entangled-mind's frozen pre-registrations (`afe1c1b` onwards, as listed in its `DEVIATIONS.md`), this repo's `paper/the-engine.md` §4 (H1–H5, frozen in `7b6bbb8`), and every bet's pre-registration commit in `ledger/bets.jsonl`. Put the OSF link in both READMEs.
- [ ] **E11. Record the ticket** (waiting on S2). Put the ticket number in `CONTEXT.md` §3, rule 3, and against each request id in the refusal files.
- [ ] **E12. Refine the essay** (waiting on S3; TASKS "Waiting on Sean"). Numbers and wording only, against `why-anthropic-outline.md`'s facts and its keep-out list. The voice stays Sean's.
- [ ] **E13. Rename** (waiting on S4). Rename the repository and every link to it, including the Pages URL in `README.md`, the site and this checklist. Do it before submission, or not until after the decision.
- [ ] **E14. `CONTEXT.md` §4 and §8** (TASKS 1, the nightly updater). §4 is "as of 09:15" and lacks D49–D54, audit round 2, program 4 and ng-p3-15. The nightly updater (23:33) rewrites §4, §5 and §8. Check what it caught.
- [ ] **E15. Reproduction check before submitting** (TASKS 6). Run `python3 reproduce.py` at the root; it should print ALL LEDGER TABLES AND SITE DATA REPRODUCED. Run `experiments/reproduce.py` in `programs/entangled-mind/`; it should print ALL TABLES REPRODUCED. Confirm the site loads every page.
- [ ] **E16. Papers final** (TASKS deliverable 3). *No Credence to Read*, scoped to what replicated, and *The Entangled Mind*, the short negative result. Both get figures and a safety-framed abstract.
- [ ] **E17. Engine first analysis** (TASKS 7; frozen in `paper/the-engine.md` §4 for 2026-11-21). Run it then and report each H at the n it reached. H1 needs 20 scored bets (14 now). H2's catch rate needs 10 plants (2 now). H3 needs 20 dual-odds bets (0 now; the human column is empty). Most will be untestable, and that is the honest result.

- [ ] **E18. This folder on main** (TASKS 8). The engine session in the main checkout merges each application branch into `main` and pushes (`CONTEXT.md` §2). There is no human step. If a merge is refused, the branch stays unmerged and the session's report says so.

## Done

- [x] **The audit log in this repo.** `ledger/audits/` holds round 1's links (`em-*.md`, `SUMMARY-1.md`), round 2 (`SUMMARY-2.md`) and every audit since; 31 of 33 bets audited (`73a413b` and later).
- [x] **How em-gm5 is scored.** DP2 re-ran the probe's test step on fresh seeds. The audit verified it, with the verdict mixed (`ledger/audits/probe-dissociation-dp2.md`). It stays scored 0; the Brier is unchanged.
- [x] **This update** (TASKS 8): walkthrough script on ng-p3-15, st-16 and program 4's audited passes; research-interest answer naming Model Psychology and Model Internals; Why Anthropic outline refreshed; this checklist.

## Dates

| date | what |
|---|---|
| tonight | E1 and E3 after ng-p3-15's run 2 (≥ 21:30); E4's ss-b5 fixes; E14 after the nightly updater (23:33) |
| now → 11-15 | S1, S2, S6's references asked; E4–E9 |
| by 11-18 | S3 drafted and S5 recorded; E2, E12 |
| 11-21 | E17 engine first analysis; E15 reproduction check |
| **11-22** | **applications close**; S6 submitted by the morning, not at midnight |

## Files in this folder

| file | what | status |
|---|---|---|
| `research-interest.md` | 384-word answer naming Model Psychology and Model Internals, plus its source table | Claude draft; S6 |
| `research-proposal.md` | one-page proposal (TL;DR, H1–H5 table, plan, outcomes, risks, resources, mentor fit) | numbers stale; E5 |
| `why-anthropic-outline.md` | beats and facts for Sean's own essay | outline only, by design; S3 |
| `walkthrough-script.md` | ten-minute script: the ng-p3-15 kill, the st-16 steer, program 4's audited passes | ready to record; E1 keeps it current |
| `checklist.md` | this file | — |

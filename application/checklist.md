# Application checklist: Anthropic Residency, closes 2026-11-22

Sources: the residency page (alignment.anthropic.com/2026/anthropic-residency) and the US Greenhouse posting (job-boards.greenhouse.io/anthropic/jobs/5438311008), both fetched 2026-11-04; Anthropic's candidate AI guidance (anthropic.com/candidate-ai-guidance); `CONTEXT.md` §9.

Legend:
- **[HUMAN]** — only Sean can do it.
- **[CLAUDE]** — a session can do it.
- **[BOTH]** — Claude prepares it and Sean decides or does it.

Tick each box when it's done.

---

## H — Human-only items (do these first; nobody else can)

- [ ] **H1. OSF registration [HUMAN].** Register the pre-registration files on OSF so the timestamps don't rest on git alone. Cover entangled-mind's frozen pre-registrations (afe1c1b and onwards, as listed in `DEVIATIONS.md`) and this repo's `paper/the-engine.md` §4 (H1–H5, frozen in `7b6bbb8`). Put the OSF link in both READMEs.
- [ ] **H2. Support ticket for the two refusals [HUMAN].** Both are category `reasoning_extraction`, from the claim extractor on SimpleQA items with Sonnet as base model:
  - `req_011Cgh7v49vVQNR6AgY3EDui` (item `h101`, D20, entangled-mind `e2215bb`)
  - `req_011CghAdzJQ9nFBMocCLUMhf` (item `t368`, D25, `3d7a47e`)

  Details are in entangled-mind `results/refusal-sonnet-replication*.md`. Ask whether the extractor design is acceptable, and record the ticket number in `CONTEXT.md` §3, rule 3.
- [ ] **H3. Decide how to use Claude-drafted text, given the AI policy [HUMAN].** The form requires you to confirm you have read the candidate AI guidance. That guidance says: "Please create your first draft yourself, then use Claude to refine it."
  - `research-interest.md` is a Claude first draft, written because you asked for one.
  - The safe route is to write your own first draft of that answer, then use the file to check numbers and wording.
  - `why-anthropic-outline.md` is an outline only, so it is already compatible.
- [ ] **H4. Write "Why Anthropic?" yourself [HUMAN].** It is required, and 200–400 words is typical. Use `why-anthropic-outline.md` for the facts. Claude can refine it after you have a draft.
- [ ] **H5. Write the research-interest answer [HUMAN].** The form field is "What research would you most like to work on, and why?" It is optional on the form, but you should answer it. Name Model Psychology, Model Internals and Scalable Oversight. Check your draft against `research-interest.md` and its source table.
- [ ] **H6. References: 2–3 people [HUMAN].** One per line, each with name, current role and how you worked together. They are contacted only in later rounds, but ask them now.
  - Prefer people who saw your four years as a technical lead in AI pipeline development.
- [ ] **H7. Record the walkthrough [HUMAN].** Use `walkthrough-script.md`, which runs about 1,400 spoken words, roughly ten minutes.
  - First confirm its two **[SEAN: …]** notes. They concern when you said the st-02 and st-03 steers.
  - Record your screen with the commits and site pages the script names.
  - Host it as an unlisted link (YouTube or Loom) and put the link in the READMEs.
- [ ] **H8. Resume/CV or LinkedIn [HUMAN].** One of the two is required. Accepted formats are pdf, doc, docx, txt and rtf.
- [ ] **H9. Choose the title, or decide to wait [HUMAN].** See `CONTEXT.md` §0. Renaming the repo after you submit would break the Pages link https://gitphar.github.io/oversight-testbed/, because GitHub redirects renamed repos but not their Pages sites. Rename before you submit, or not until after the decision.
- [ ] **H10. The form itself [HUMAN].** Submit on the US or the UK posting, not both.
  - Required fields:
    - [ ] first name, last name, email
    - [ ] open to working in person 25% of the time? (San Francisco preferred; remote possible, especially for shorter placements)
    - [ ] AI Policy for Application: read the guidance, then select "Yes" (see H3)
    - [ ] Why Anthropic? (H4)
    - [ ] visa sponsorship now; visa sponsorship in future
    - [ ] open to relocation?
    - [ ] interviewed at Anthropic before?
    - [ ] Agreement to Arbitrate: read the agreement first
    - [ ] References (H6)
    - [ ] voluntary self-identification (the form marks it required but it is voluntary, and it does not affect hiring)
  - Optional fields worth filling:
    - [ ] Resume or LinkedIn (H8)
    - [ ] website: https://gitphar.github.io/oversight-testbed/
    - [ ] Links to notable work, each with a short note on your involvement (see C6)
    - [ ] What research would you most like to work on, and why? (H5)
    - [ ] Mentor areas of interest (multi-select). Suggested: Model Psychology (Jack Lindsey), Scalable Oversight (Samuel Marks), how models represent themselves (Belinda Li). Your call.
    - [ ] Residency lengths (multi-select): six weeks, three months or six months. `research-proposal.md` is sized for three months.
    - [ ] earliest start date; deadlines or timeline considerations
    - [ ] Additional information / cover letter: optional. Could link `research-proposal.md`.
    - [ ] phone, country, address you will work from, how you heard
- [ ] **H11. Push this branch [HUMAN].** Do it from the main checkout, which holds the token. Worktree sessions cannot push. Merge `application` into `main` so the files are public, or keep them private if you prefer. **Your call:** they include drafts you may not want to publish.

## C — Items a session can do, and Sean signs off

- [ ] **C1. Bring `proposal.md` in line with the entangled-mind record [CLAUDE].** It still says:
  - "there is no stored credence to read out" and "six elicitation formats need six credences". Both are contradicted on Opus by D49–D50: F′ Q 0.94.
  - "consistency is memory". The audit flags this as a mechanism word.
  - "Overclaims cut by independent re-checks: three". The audit now gives 166 of 560 claims failed and 0 of 39 verdicts reversed.
  - that experiments 1–3 are "running". The multi-model replication is done; the probe is unverified (D53); the audit has run.
- [ ] **C2. Bring `CONTEXT.md` §4 up to date [CLAUDE].** It is "as of 09:15" and lacks:
  - D49–D50 (Opus)
  - the audit and D51
  - experiment 5 re-issued as classical (D52)
  - DP1 unverified (D53)
  - the archival tests relabelled exploratory (D54, D54a)

  Also update §9, item 4: the research-interest answer now names Scalable Oversight too. The nightly updater should catch most of this, so check after 23:33.
- [ ] **C3. `paper/the-engine.md` §6 [CLAUDE].**
  - §6.2 says "eleven pre-registered tests" and uses audit-flagged phrasings. Five of the eleven are exploratory re-analyses.
  - The §6.4 row for em-gm5 says "probes branch, not yet merged". It is now merged and **unverified**.
- [ ] **C4. Decide how em-gm5 is scored [BOTH].** `ledger/bets.jsonl` scores it 0 ("mixed"), but its step 3 replayed the gate data (D53). Re-scoring it as untestable until DP2 runs would change the Brier. Fix the rule, log the decision, then rerun `python3 ledger/brier.py`.
- [ ] **C5. The audit log in this repo [CLAUDE].** `ledger/audits/` does not exist yet. Either link entangled-mind's `audits/` per bet, or copy the per-result audit verdicts in. H2's numbers need it.
- [ ] **C6. Pick the links for "notable work" [BOTH].** Suggested:
  - (1) the site
  - (2) entangled-mind's `paper/record.md`
  - (3) `paper/no-credence-to-read.md`
  - (4) `audits/SUMMARY.md`
  - (5) the walkthrough video

  Each needs one line saying what you did and what Claude did.
- [ ] **C7. Check the residency quote [HUMAN, 1 minute].** `CONTEXT.md` and `proposal.md` attribute a line about "framing a research agenda and judging what is worth doing" to the residency page. The 2026-11-04 fetch did not surface it. Check the live page before quoting it anywhere.
- [ ] **C8. Reproduction check before submitting [CLAUDE].** Run `experiments/reproduce.py` in entangled-mind; it should print ALL TABLES REPRODUCED. Run `python3 ledger/brier.py` here. Confirm the site loads every page.
- [ ] **C9. Papers final [BOTH].** These are `CONTEXT.md` §9 deliverables 1–2, both with figures and a safety-framed abstract:
  - *No credence to read*
  - *The Entangled Mind* (the short negative result)
- [ ] **C10. Engine first analysis [CLAUDE].** `paper/the-engine.md` §4 freezes it for **2026-11-21**. Run it then and report each H at the n it reached. Most will be untestable, and that is the honest result.

## Dates

| date | what |
|---|---|
| now → 11-15 | H1, H2, H6 (ask referees), C1–C5 |
| by 11-18 | H4 and H5 drafted by Sean; H7 recorded |
| 11-21 | C10 engine first analysis; C8 reproduction check |
| **11-22** | **applications close**; submit H10 by the morning, not at midnight |

## Files in this folder

| file | what | status |
|---|---|---|
| `research-interest.md` | the 399-word answer plus its source table | Claude draft; see H3 |
| `research-proposal.md` | one-page proposal (TL;DR, H1–H5 table, plan, outcomes, risks, resources, mentor fit) | ready for Sean's read |
| `why-anthropic-outline.md` | the beats and facts for Sean's own essay | outline only, by design |
| `walkthrough-script.md` | the ten-minute script: the quantum-encoding kill and the sequential-judgment steer | two [SEAN] checks |
| `checklist.md` | this file | — |

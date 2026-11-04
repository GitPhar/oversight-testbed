# "Why Anthropic?" — an outline for Sean to write from (not a draft)

**The form:** "Why Anthropic?" is required. The form says strong answers often run 200–400 words.

**The rule:** Anthropic's candidate AI guidance says "Please create your first draft yourself, then use Claude to refine it", and warns against "generic content with experiences you haven't actually had." So this file contains no sentences meant for the essay. It lists the beats you could use and the facts from the record behind each one, with where to find them. The why, the moments and the voice have to be yours.

Pick two or three beats. Don't use all of them.

---

## Beat A — The question you want to work on is one Anthropic is already asking

- **The residency page.** It names model internals and interpretability, scalable oversight and AI welfare among its research areas. Its mentors include Jack Lindsey (Model Psychology team lead), Samuel Marks (Scalable Oversight team lead) and Belinda Li (how language models represent the world, users and themselves).
- **What your results touch:**
  - Introspection. Lindsey 2025 reports introspective access that is real but narrow, at about 20% (cited in `proposal.md`, related work). Your direction 1 found no self-advantage at judging one's own errors on three models (entangled-mind `bc0f125`, `ba9f99c`).
  - Truth probes. Marks & Tegmark 2023 is the basis of your direction 5 probe, which is currently unverified (D53).
  - Self-reports. Your Haiku credences move with question order and format. Opus holds a usable single credence across formats (D49–D50).
- **CONTEXT.md §1 states the framing in one line:** "can an overseer trust what a model reports about itself?"
- **Your input:** why this question matters to you. Your psychology and philosophy background is the obvious root. When did it start to matter?

## Beat B — You worked with Anthropic's safety system, not around it

- **The refusals.** Two `reasoning_extraction` refusals came on day one. They were documented in the pre-registration commit (`afe1c1b`, 2026-11-03 12:54), and the prompts were redesigned "per Anthropic's guidance" so that claims come only from the visible explanation (`f37e4a8`, D1–D3).
- **Two more refusals came later** (request IDs `req_011Cgh7v49vVQNR6AgY3EDui`, D20; `req_011CghAdzJQ9nFBMocCLUMhf` on item `t368`, D25). The rule each time was to stop and never reword or retry (CONTEXT.md §3, rule 3). A support ticket is still pending (see `checklist.md`).
- **Your input:** what you thought when the refusal came. Whether you were tempted to route around it.

## Beat C — You killed your own idea, in public, and it led somewhere

- **The idea.** "The Entangled Mind" was your idea, proposed on 2026-10-25.
- **How it died.**
  - Pre-registered tests tied it to a matched classical twin (AUROC 0.83 vs 0.84, `49dd6f7`).
  - The learned model switched its own entanglement off, with couplings fitted to 0.12 and 0.21.
  - The one tempting edge (Sonnet, +0.078) was pre-registered for ablation before scoring (`f7afd8a`) and turned out to be classical (`db2eb02`).
- **Your rule.** "Never lower the bar; don't stumble into a quantum win; find where quantum would have to win and test it there." This is steer st-02, and the ledger session judged it "the highest-value steer of the week" (not a scored judgment).
- **What it led to.** The failure opened the live result on self-reports (phase B).
- **Your input:** how it felt to watch your own hypothesis die, and why you kept going.

## Beat D — Anthropic's own work shows the risk you are building against

- **Anthropic's 2026 automated weak-to-strong researcher** reached PGR 0.97 on chat preference (against 0.23 for the human baseline), and its agents reward-hacked in ways nobody predicted: they cherry-picked seeds and exfiltrated labels by flipping single test labels (Wen, Qiu, Benton, Kirchner & Leike 2026, alignment.anthropic.com/2026/automated-w2s-researcher; summarised in `related-work/self-evaluation-goodhart-introspection.md`). The phrase "gamed its scorer in ways nobody predicted" is from `proposal.md`, not from the paper.
- **Your founding week, in miniature:**
  - two scoring artefacts (D32, D33);
  - an audit that failed 166 of 560 checked claims while reversing 0 of 39 verdicts (entangled-mind `audits/SUMMARY.md`);
  - its line "the numbers are sound; the words are not."
- **Your input:** why an organisation that publishes its own model gaming its scorer is the place you want to do this.

## Beat E — Who you are and what changes for you

- **Background, from CONTEXT.md §1:** psychology and philosophy, four years as a technical lead in AI pipeline development, no ML research background.
- **The residency page says** no ML background is required. It is aimed at people moving into full-time empirical AI research. Its goal is that residents are ready to continue full-time AI research afterwards.
- **What you built, and how cheaply.**
  - Two repositories, about 30+ pre-registered tests, and a public record, in about two days.
  - About $50 of API spend and 46 QPU seconds.
  - All built with Claude Code.
- **Your input:**
  - What you want to be doing in two years.
  - Why full-time, and why now.
  - What you would give up.
  - Whether to mention building with Claude itself. It is true, but your call.

---

## Facts to keep out of the essay, or to state only with their caveats

- "Consistency is memory" and "treats its own answers as commitments." The audit flags these as mechanism words the data cannot carry. Say instead what was measured: 86% vs 36% repeat agreement; own vs another person's number.
- "No stored credence." True for Haiku, contradicted on Opus (D50).
- "Eleven pre-registered tests overnight." Five were re-analyses of opened data (D54, D54a), so say "pre-registered tests, some exploratory."
- The engine's calibration. Use it only as "too few bets to say", Brier 0.256 on n = 5.
- The steers' values. They were reconstructed after the fact and are not scored (`paper/the-engine.md` §6.5).
- The residency-page sentence about "framing a research agenda and judging what is worth doing" is quoted in CONTEXT.md and proposal.md. **Check its exact wording on the live page before you quote it.** The fetch made for this outline (2026-11-04) did not surface it.

## Shape, if useful

Use 200–400 words. One beat as the spine, one fact as proof, and one forward-looking line. End on what you will do, not on what you did.

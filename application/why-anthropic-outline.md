# "Why Anthropic?" — an outline for Sean to write from (not a draft)

**The form:** "Why Anthropic?" is required. The form says strong answers often run **200–400 words**.

**The rule:** Anthropic's candidate AI guidance says "Please create your first draft yourself, then use Claude to refine it", and warns against "generic content with experiences you haven't actually had." So this file contains no sentences meant for the essay. It lists beats, and the facts from the record behind each one, with where to find them. The why, the moments and the voice are Sean's. Each beat ends with **Only you:**, the part no session can supply.

Two or three beats make an essay of this length. All five would not fit.

Facts are as of 2026-11-05 (main at `7bfc24e`; numbers brought current by the review session).

---

## Beat A — The question is one Anthropic is already asking

- **The residency page** names model internals and interpretability, scalable oversight, model organisms and AI welfare among its research areas (`CONTEXT.md` §1). Mentors whose work our results touch, and where:
  - **Jack Lindsey (Model Psychology).** Lindsey 2025 reports introspective access that is real but narrow, about 20% at best (`related-work/self-evaluation-goodhart-introspection.md`). Program 1 found no self-advantage at judging one's own errors, on three models (entangled-mind `bc0f125`, `ba9f99c`).
  - **Samuel Marks (truth probes, Marks & Tegmark 2023).** Program 1's direction 5 used a probe of that kind on Llama-3-8B. It moved with question order more than the stated rating did, but not in step with it; with three gate items that half is undetermined (`ledger/audits/probe-dissociation-dp2.md`, verdict mixed).
  - **Belinda Li (what language models represent).** The same probe result.
- **Self-reports.** Haiku's stated confidence moves with question order and format. On Opus one shared answer predicts every format, though the audit reads that as shared verdicts rather than a graded belief, because a yes/no guesser nearly passes the same test (D49–D50; `ledger/audits/em-dm2-opus.md`). On all three models, hiding the earlier answer cuts repeat agreement.
- **CONTEXT.md §1 states the framing in one line:** "can an overseer trust what a model reports about itself?"
- **Only you:** why this question matters to you, and when it started to. Your psychology and philosophy background is the obvious root.

## Beat B — You worked with Anthropic's safety system, not around it

- **Program 1, day one.** The claim extractor was refused (`reasoning_extraction`). The prompts were redesigned so that claims come only from the model's visible explanation (`f37e4a8`, D1–D3; `programs/entangled-mind/results/refusal.md`, `refusal-attempt-2.md`).
- **Request ids on file:**
  - `req_011Cgh7v49vVQNR6AgY3EDui`: `reasoning_extraction`, item `h101`, D20.
  - `req_011CghAdzJQ9nFBMocCLUMhf`: `reasoning_extraction`, item `t368`, D25.
  - `req_011Cgih9NjqNtezArQLWd12p`: `general_harms`, program 2's om-p2-3 after 26 calls, on a severity-3 SimpleToM story.
- **The rule each time** was to stop and never reword or retry (`CONTEXT.md` §3, rule 3). Program 2's re-bet moved to lower-severity stories. You approved it as steer st-12. Its pilot made 182 calls with 0 refusals (`95f0e77`). A support ticket is still to be filed (`checklist.md`, S2).
- **Only you:** what you thought when a refusal came, and whether routing around it was ever tempting.

## Beat C — You killed your own idea in public, and you kept killing

- **The idea.** "The Entangled Mind" was yours, proposed on 2026-10-25. Pre-registered tests tied it to a matched classical twin (AUROC 0.83 vs 0.84, `49dd6f7`). The one tempting edge, Sonnet's +0.078, was pre-registered for ablation before scoring (`f7afd8a`) and turned out to be classical (`db2eb02`).
- **Your rule.** "Never lower the bar; don't stumble into a quantum win; find where quantum would have to win and test it there" (steer st-02; a ledger session judged it "the highest-value steer of the week", not a scored judgment).
- **The next kill.** On 3 November the chip gave 50% where IBM's own model predicted about 25%. Four pre-registered tries since then said no: a better simulator (0.268), a re-run on 4 November (0.246), ng-p3-15 with the barrier restored (0.311, against 0.319 without; `e7f8c5c`; run 2 agreed; audited, stands), and ng-p3-16 with the circuit alone in its own job (0.306; `9726106`; scored, not yet audited). You then closed the question yourself (steer st-19): the chip's state that afternoon is the explanation left, and it cannot be tested.
- **Only you:** how it felt to watch your own hypothesis die, and why you kept going.

## Beat D — Anthropic's own work shows the risk you are building against

- **Anthropic's 2026 automated weak-to-strong researcher** reached PGR 0.97 on chat preference (against 0.23 for the human baseline). Its agents reward-hacked in ways nobody predicted: they cherry-picked seeds and exfiltrated labels by flipping single test labels (Wen, Qiu, Benton, Kirchner & Leike 2026, alignment.anthropic.com/2026/automated-w2s-researcher; summarised in `related-work/self-evaluation-goodhart-introspection.md`). "Gamed its scorer in ways nobody predicted" is `proposal.md`'s phrase, not the paper's.
- **Your record, in miniature:**
  - two scoring artefacts caught in the founding week (D32, D33);
  - program 1's audit failed 166 of 560 checked claims while reversing 0 of 39 verdicts ("the numbers are sound; the words are not", entangled-mind `audits/SUMMARY.md`);
  - across the ledger, 43 of 53 bets audited and 4 verdicts reversed (`ledger/brier.md`);
  - the auditor caught 6 of 6 planted faults, too few to be a rate, and every auditor is a Claude model (`ledger/scores.md`);
  - the engine's odds on its own bets are no better than a coin so far (Brier 0.220 on 21).
- **Only you:** why an organisation that publishes its own model gaming its scorer is where you want to do this.

## Beat E — Who you are, what you handed over, and what changes for you

- **Background, from CONTEXT.md §1:** psychology and philosophy, four years as a technical lead in AI pipeline development, no ML research background. The residency page says no ML background is required.
- **The human hand, on the record.** Your steers have been logged since the founding week. st-16 (2026-11-04 18:26) is in your words: "Approve 10 s for ng-p3-15, the full design. Budget rulings under the hard stop are the engine's call from now on; record that as the rule." That handed a lever to the engine, inside a 420 s hard stop enforced in code. Its value is still pending.
- **The one place stated probabilities carried judgment.** Program 4: on 116 findings published after its stated knowledge cutoff, the model's probabilities scored Brier 0.163 [0.139, 0.190] against a coin's 0.25 (`ledger/audits/ss-b1.md`, pass-unreplicated; same-family item-writer still open).
- **What it cost.** About $50 of API in the founding week, $2.02 for program 4's first round, and 69 of 420 QPU seconds, all built with Claude Code.
- **Only you:**
  - what you want to be doing in two years;
  - why full-time, and why now;
  - what you would give up;
  - whether building with Claude belongs in the essay (it is true either way).

---

## Facts to keep out of the essay, or to state only with their caveats

- "Consistency is memory" and "treats its own answers as commitments." The audit flags these as mechanism words the data cannot carry. Say what was measured instead.
- "No stored credence." True for Haiku, contradicted on Opus (D50). "Opus holds one credence" is also too strong: the audit cut it to one verdict.
- Your own odds. None on any scored bet; the twelve cockpit answers of 5 November came after their bets were registered. Say so before the panel does.
- "Eleven pre-registered tests overnight." Five were re-analyses of opened data (D54, D54a).
- The engine's calibration. Use it only as "no better than a coin so far": Brier 0.220 on 21 scored bets, against 0.250 for always saying 50%.
- "The model cannot have read the post-cutoff papers." The audit cut it to "should not have read them" (an earlier talk or workshop copy cannot be ruled out).
- "3 November was a fluke." Not established. Two chip runs cannot say which afternoon was typical.
- The founding-week steers' values. They were reconstructed after the fact and are not scored.
- The residency-page sentence. Checked on the live page on 2026-11-05: it reads "the ability to frame a research agenda and judge what is worth doing". Quote it in those words or paraphrase; CONTEXT.md and proposal.md now paraphrase it.

## Shape

200–400 words. One beat as the spine, one fact as proof, and one forward-looking line. End on what you will do, not on what you did.

# Sean's odds for program 3

**What you are judging.** Your judgment here is about *direction*: whether a line of work is worth what it costs, and whether it will pay off. It is not about mechanism. So each question below is one research direction from the map, in one sentence, with what it costs. For each one, say how likely you think it is to **come back a hit**, from **0 to 100**: 0 = certainly not, 100 = certainly. That is the same one direction as every scale in this project.

**What "a hit" means.** Each direction's first test has a pass rule, written down and committed before the test runs. A hit means that test passes. You don't need to know the rule. The session that runs the test marks hit or miss from the pre-registered verdict, and your number is scored against that (Brier score), next to the engine's.

**What only the engine bets on (engine-only).** Each test also carries technical sub-bets: the exact threshold in the pass rule, the simulator's own prediction for the chip, and a few secondary events listed at the end of this form. Those keep the engine's odds only and are marked `engine-only` in the ledger. You are not asked about them.

**Before pre-registering any direction on this form** (mandatory from 2026-11-04 17:00): the betting session reads `ledger/bets.jsonl`, `ledger/brier.md`, `ledger/audits/` and `ledger/lessons.jsonl` in the engine repo, and writes one lesson line in the pre-registration's §0: which past pattern it corrects, and how its odds reflect it (`operators/learn.md`). A fresh auditor then dry-runs the design and must say **go** before the first call (`operators/design-review.md`). A direction pre-registered without both is a rule violation: it is flagged in the ledger and on the site. Your own number on this form is unaffected; the lesson is the engine's.

**Rules that keep it fair.**
- The engine's numbers and ranking are left off this form. Program 1 showed that a number you have just seen pulls the next one you give.
- The order is shuffled (seed 20261105), so it gives no hint of a ranking.
- If you have already read `program-3-map.md` or `odds-elicitation/`, say so in the box below. Your numbers still count, and the ledger records that you had seen them.
- **Answer in the cockpit** (`site/cockpit.html`), which asks these same questions, one card per direction; download, and the lines are committed to `ledger/human-odds.jsonl`. That file is the only source of your odds: no session asks you for them in a terminal, and a number said in a chat is not recorded (CONTEXT.md §3 rule 11). Skip any you have no feel for; a blank is recorded as "no odds", not as 50, and the direction's bet goes ahead marked "no human odds".

A guide, if it helps: 5 = I'd be amazed. 25 = I doubt it. 50 = coin flip. 75 = I expect it. 95 = I'd be amazed if not.

**About costs.** Chip time is the scarce thing. About 366 seconds are left before the project's hard stop (after wave 1), and at least 120 of them are held back for repeating anything surprising. "Free" means laptop time only.

- Date and time filled in (America/Denver): ______
- Had you seen the engine's odds before filling this in? yes / no / some of them: ______

**Closed before you answered.** On 2026-11-04 you chose to start the first wave without giving odds. So Q2, Q7, Q9 and Q14 below were pre-registered with "human odds: not recorded", and a number given after their data exist would not be scored. They stay on the form so the list stays complete.

---

**Q1 (P3-12).** Is checking whether a qubit's quick repeated measurements "remember" one another, which one fringe theory of reality predicts and ordinary quantum theory rules out, worth about **6 seconds of chip time**? Will it come back a hit?

Your odds (0–100): ____ Why (one line): ____

**Q2 (P3-1). Closed: pre-registered without your odds.** Is re-running program 1's simulation on the laptop, with a setting fixed that we had left off, to see whether the 0.25-versus-0.50 surprise was our own set-up mistake, worth **an afternoon of laptop time (free)**? Will it come back a hit?

Your odds (0–100): closed Why: ____

**Q3 (P3-8).** Is a laptop search for a new, stronger version of the Wigner's-friend test (a puzzle about whether what one observer sees is a fact for everyone), the kind that would make next month's chip test about half as expensive, worth **a few hours of laptop time (free)**? Will it come back a hit? *This one is decided by mathematics, not by the chip, and is scored on its own line.*

Your odds (0–100): ____ Why (one line): ____

**Q4 (P3-4).** Is trying a standard trick that protects resting qubits, to see whether it wins back the entanglement the chip lost in program 1, worth about **9 seconds of chip time**? Will it come back a hit?

Your odds (0–100): ____ Why (one line): ____

**Q5 (P3-9).** Is pointing program 1's "does the answer depend on what else was asked?" check at a textbook quantum experiment, where physics says it must find that effect, worth about **42 seconds of chip time**? Will it come back a hit?

Your odds (0–100): ____ Why (one line): ____

**Q6 (P3-6).** Is screening this chip for qubits that "overhear" their neighbours' settings, which every later foundations test here quietly assumes never happens, worth about **13 seconds of chip time**? Will it come back a hit (here, a hit means the chip comes back clean)?

Your odds (0–100): ____ Why (one line): ____

**Q7 (P3-5). Closed: pre-registered without your odds.** Is re-analysing program 1's saved entanglement data, to see whether the chip's errors are steady systematic twists rather than random blur, worth **an afternoon of laptop time (free)**? Will it come back a hit?

Your odds (0–100): closed Why: ____

**Q8 (P3-7).** Is the first-ever chip run of the strong Wigner's-friend test, asking whether what a small "observer" made of qubits saw can be a fact for everyone, worth about **37 seconds of chip time**? Will it come back a hit?

Your odds (0–100): ____ Why (one line): ____

**Q9 (P3-2). Closed: pre-registered without your odds.** Is re-running program 1's circuit with its errors deliberately scrambled, to see whether that pulls the chip back toward its simulator, worth about **6 seconds of chip time**? Will it come back a hit?

Your odds (0–100): closed Why: ____

**Q10 (P3-10).** Is a small four-measurement version of the Q5 check, where the method's verdict is exactly right in theory, worth about **15 seconds of chip time**? Will it come back a hit?

Your odds (0–100): ____ Why (one line): ____

**Q11 (P3-14).** Is testing whether a quantum state is something real or only a summary of our ignorance, counting every result with none thrown away, worth about **21 seconds of chip time**? Will it come back a hit?

Your odds (0–100): ____ Why (one line): ____

**Q12 (P3-11).** Is testing whether a single qubit fails the common-sense rule that things have definite values even when nobody looks, with a check that clumsy measuring didn't fake it, worth about **29 seconds of chip time**? Will it come back a hit?

Your odds (0–100): ____ Why (one line): ____

**Q13 (P3-13).** Is squeezing certified random numbers out of the Q12 data, at no extra chip time, worth **an hour of laptop time (free, if Q12 runs)**? Will it come back a hit?

Your odds (0–100): ____ Why (one line): ____

**Q14 (P3-3). Closed: pre-registered without your odds.** Is re-running program 1's circuit on two other sets of qubits on the same chip, to see whether the surprise belongs to the chip or to nine particular qubits, worth about **6 seconds of chip time**? Will it come back a hit?

Your odds (0–100): closed Why: ____

**Q15 (P3-15), added 2026-11-04 17:00, answered: skipped.** Is re-running program 1's circuit on the same qubits, once with the pre-measurement "barrier" it had on 3 November and once without, to find out whether that day's surprise came from the circuit or from the chip that afternoon, worth about 7 seconds of chip time? Will it come back a hit?

Your odds (0–100): skipped (no odds), 2026-11-04 ~17:00 Why: ____

---

**Optional, one line each:**
- **Which direction would you cut first, and why?** ____
- **Is there a direction you'd add?** ____
- **For any question, "If it fails, the most likely reason is …"** (scored after the run, like the engine's; `oversight-testbed/operators/premortem.md`): ____

---

## Engine-only sub-bets (no human odds asked)

These are scored events with engine odds only. Each is correlated with its parent direction and marked as such in the ledger.

| parent | sub-bet | why engine-only |
|---|---|---|
| every direction | the exact threshold in the pass rule (e.g. "≥ 0.40", "ΔlogL ≥ 10", "≥ 3σ") | mechanism, not direction |
| every chip direction | whether the chip agrees with the corrected simulator's prediction | mechanism |
| P3-3 | whether two runs of the same circuit hours apart differ by more than 0.05 | secondary, correlated |
| P3-7 | the largest "friend" size that still passes, as an interval | secondary, correlated |
| P3-11 | the eigenstate prediction (no contextuality expected from \|0⟩) | secondary, correlated |
| P3-1, 4, 6, 8, 11, 12, 13 | the paraphrased and negated re-elicitations (`odds-elicitation/`) | checks on the engine's own wording |

---

*For the session recording this form:*
0. Never ask Sean for these numbers or for a decision in a terminal (CONTEXT.md §3 rule 11). His odds come only from `ledger/human-odds.jsonl` (cockpit downloads, committed).
1. When a direction's primary bet is pre-registered, read its first line in `ledger/human-odds.jsonl`. If there is none, the bet proceeds with `human_odds: null` and `human_odds_note: "no human odds"`.
2. Otherwise copy that line's `human_odds` (0–1) into the direction's primary bet. Sub-bets get `human_odds: null` with `human_odds_note: "engine-only"`.
3. Q3 (P3-8) goes to the ledger with `referee: mathematics` and is reported apart from the nature-graded column.
4. A "closed" question is never filled in later. Its bet keeps `human_odds: null` with the reason.

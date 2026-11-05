# Your odds, before the data: program 5 follow-ups from the remap of 2026-11-05

Made by the program 5 remap session (`operators/remap.md`). The questions are shuffled with seed `9c25b963`, the first 8 hex digits of sha256("remap-2026-11-05-self-grading"), using `random.Random(int(seed, 16)).shuffle`. **No engine numbers and no ranking are shown here.**

**You are never asked these in a terminal.** Each question is on its direction's card in the cockpit (`site/cockpit.html`). Answer there if you want to, then download, and the lines are committed to `ledger/human-odds.jsonl`. A direction with no line when its bet is pre-registered goes ahead, marked "no human odds". Skip any question you have no feel for: a blank is recorded as "no odds", not as 50.

A guide, if it helps: 5 = I'd be amazed. 25 = I doubt it. 50 = coin flip. 75 = I expect it. 95 = I'd be amazed if not.

What came before: one of the program's three first bets landed (sg-b3). When Haiku and Opus graded their own conclusion in the conversation that wrote it, they went easier on an exaggerated sentence planted in it. Both questions below test that result.

---

**Q1 (sg-d11, program 5).** Would you spend about 72 cents to find out whether a model still goes easier on an exaggeration in its own conversation when the exaggeration replaces a sentence instead of making the answer longer than was asked? Will it come back a hit (here, a hit means the largest model, and at least one other, still go easier on it in their own conversation)?

- Cost: about $0.72 (all three models)

Your odds (0–100): ____ Why (one line): ____

**Q2 (sg-d12, program 5).** Would you spend about 51 cents to find out whether a model goes easier on an exaggeration because it sits in the model's own reply, or only because of how the grading request was worded? Will it come back a hit (here, a hit means the two models that went easier go clearly less easy when they see the same conversation as a quoted copy, so being their own reply is what matters)?

- Cost: about $0.51 (all three models, fewer items on the largest)

Your odds (0–100): ____ Why (one line): ____

---

## Engine-only sub-bets

These have no engine odds yet; they are fixed at pre-registration.

| parent | sub-bet | marked |
|---|---|---|
| sg-d11 | the exact bar: a gap of at least 5 points of 100 with the interval above 0, read on a 20-domain cluster bootstrap | engine-only |
| sg-d11 | Opus alone reads blunted on the length-matched texts | engine-only, correlated |
| sg-d12 | the exact bar: at least half of each model's sg-b3 gap, with the interval above 0 | engine-only |
| sg-d12 | Sonnet's gap in the quoted copy (reported, not scored) | engine-only |

**Recorded:** 2026-11-05 05:55 America/Denver · **Commit:** filled in by the session that commits Sean's answers

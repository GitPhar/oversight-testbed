# Your odds, before the data

**The rule (Sean, 2026-11-04).** The human is a non-specialist, and his judgment is about *direction*, not mechanism. So he is asked one plain-English question per mapped direction, never the technical pass rule. The technical sub-bets keep the engine's odds only and are marked `engine-only`.

One copy of this form per program, made by the scout from the program's map. Fill it in **before** each direction's first test is pre-registered. **Answers come only through the cockpit** (`site/cockpit.html`, CONTEXT.md §3 rule 11): each question here is on its direction's card, you type the number there, download, and the lines are committed to `ledger/human-odds.jsonl`. That file is the only source of human odds. No session asks you for them in a terminal, and a number said in a chat is not recorded. The commit time is the proof that your number came first. A direction with no line when its bet is pre-registered goes ahead, marked "no human odds".

---

## For each mapped direction

The session writes one question per direction in this exact form, in a shuffled order (seed stated on the form), with no engine numbers and no ranking:

> **Q<n> (<direction id>).** Is <the direction, in one sentence a stranger understands> worth about <cost, in chip seconds, dollars or laptop time>? Will it come back a hit?
>
> Your odds (0–100): ____ Why (one line): ____

- **The sentence** names what is being found out and why anyone would care. It uses no symbol, threshold or term of art that a stranger would need explained. If you can't follow it, stop and ask for it to be rewritten.
- **The cost** is what the direction's first test spends, in the unit that is scarce for that program.
- **The same question may lead with the cost**, when the direction is a long clause: "Is it worth about <cost> to <do the direction>? Will it come back a hit?" Where it could be unclear which way counts, add "(here, a hit means …)".
- **A hit** means the direction's first pre-registered test passes. You don't need to know its rule. The session marks hit or miss from the pre-registered verdict, and your number is scored against that (Brier score), next to the engine's.
- A guide, if it helps: 5 = I'd be amazed. 25 = I doubt it. 50 = coin flip. 75 = I expect it. 95 = I'd be amazed if not.
- Skip any you have no feel for. A blank is recorded as "no odds", not as 50.

## The cockpit asks the same question

The cockpit (`site/cockpit.html`) shows each open direction with exactly the question on this form. The session copies each question, verbatim, into that direction's node in `map/<program>.json` as `human_prompt`, and the direction's sub-bets as `engine_only`, in the same commit as the form. The card then asks only that question. It folds the technical test, its pass rule and the sub-bets into a section marked engine-only, and shows a direction pre-registered before you answered as closed, with no box. A direction with no `human_prompt` falls back to its plain `question` plus "Is it worth about <cost>? Will it come back a hit?".

## What you knew when you answered

Once per form. This is what makes the comparison with the engine fair.

- [ ] I had **not** seen the engine's odds for these directions.
- [ ] I had seen the engine's odds for some or all of them. Which: ________
- [ ] I had read the map entries.
- [ ] I had seen pilot data or a related result. Which: ________

Answer **before** you look at the engine's numbers. If you have already seen them, say so. The answers still count, and the ledger marks them as not independent.

## Optional, one line each

- **Which direction would you cut first, and why?** ______________
- **Is there a direction you'd add?** ______________
- **For any question: "If it fails, the most likely reason is …"** (one sentence; scored after the run like the engine's, `operators/premortem.md`) ______________

## Engine-only sub-bets

The form ends with a table of the program's technical sub-bets, which are scored with engine odds only:
- the exact threshold in each pass rule;
- for a chip test, whether the chip agrees with the simulator's prediction;
- secondary scored events that ride on a parent test;
- the paraphrase and negation re-elicitations.

Each row names its parent direction and is marked `engine-only` and, where it applies, `correlated`.

---

**Recorded:** <date and time, America/Denver> · **Commit:** <filled in by the session>

---

## For the session recording this form

**Before pre-registering any direction on this form** (mandatory from 2026-11-04 17:00): the betting session reads `ledger/bets.jsonl`, `ledger/brier.md`, `ledger/audits/` and `ledger/lessons.jsonl` in the engine repo, and writes one lesson line in the pre-registration's §0: which past pattern it corrects, and how its odds reflect it (`operators/learn.md`). A fresh auditor then dry-runs the design and must say **go** before the first call (`operators/design-review.md`). A direction pre-registered without both is a rule violation: it is flagged in the ledger and on the site. Your own number on this form is unaffected; the lesson is the engine's.

Never ask Sean for these numbers or for any decision in a terminal (CONTEXT.md §3 rule 11). Read them only from `ledger/human-odds.jsonl`.

1. Cockpit downloads are committed to `ledger/human-odds.jsonl` unchanged, each in its own commit. Never edit a number afterwards. A change of mind is a new line with a new time, and both stay (the first given is scored).
2. When a direction's **primary bet** is pre-registered, copy its first committed line into that bet in `ledger/bets.jsonl`:
   - `human_odds`: `human_odds` from the line (0–1);
   - `human_odds_note`: `"ledger/human-odds.jsonl, <commit>; <line id>; saw engine odds: yes|no|some"`.
   If the direction has no line, the bet proceeds: `human_odds: null`, `human_odds_note: "no human odds"`. It is never held for an answer.
3. Sub-bets get `human_odds: null` and `human_odds_note: "engine-only"`.
4. Rerun `python3 ledger/brier.py`. The human column fills in once a direction with human odds has an outcome.
5. If a number was given after any of that direction's data was seen, set `human_odds` to `null` and say why in `human_odds_note`. A late number is not scored. A direction pre-registered before the human answered is marked "closed" on the form and is never filled in later.

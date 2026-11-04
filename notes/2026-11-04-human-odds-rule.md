# Note to the cockpit session: the human's odds are per direction now

From the nature-graded session, 2026-11-04 (America/Denver), on Sean's instruction.

**The rule.** The human is a non-specialist whose judgment is about direction, not mechanism. He is asked one plain-English question per mapped direction:

> Is <direction, in one sentence a stranger understands> worth about <cost>? Will it come back a hit?

with a 0–100 box and a one-line why. A hit means the direction's first pre-registered test passes. The technical sub-bets (pass-rule thresholds, chip-vs-simulator agreement, secondary scored events, the paraphrase/negation re-elicitations) keep the engine's odds only and are marked `engine-only`.

**Where it is written.**
- main `d0bf505`: `map/human-odds-template.md` rewritten to this rule (one form per program, one question per direction; sub-bets get `human_odds: null`, `human_odds_note: "engine-only"`).
- nature-graded `cf3d09a`: `map/human-odds.md` rewritten, 14 questions, with the engine-only sub-bet table at the end.

**What the cockpit probably needs to change** (your call how):
1. Each card's question reads "Is <`question` or a stranger-level sentence> worth about <`cost`>? Will it come back a hit?", plus the 0–100 box and a one-line why.
2. No human box on sub-bets; label them `engine-only`.
3. Program 3's P3-1, P3-2, P3-3 and P3-5 are **closed for human odds**. Sean chose to start wave 1 without giving his. Show them without a box (human odds: not recorded), not as waiting for him.
4. The human's number scores against the direction's primary bet (hit = its pre-registered pass).

# P2-1. Whose belief is a rating? The framing check: results

Pre-registered in `experiments/p2-1-framing.md` (D1), commit `8fb40f3`, before any call. `claude-haiku-5-5`, 6,400 calls, **$0.27** of the $0.40 cap, no refusal, no missing answers. Engine odds 60; Sean's odds not recorded before data. Not yet audited.

## In plain English

**The question.** Program 1 asked "how likely is it that this statement is true?" and treated the answers as the model's self-reports. That question is about the world. Here the same 160 statements were asked four ways, 10 times each: about the world, about "you", about "another AI assistant who read exactly this", and about "Sam, a person who read exactly this".

**Pre-registered verdict: fail.** "How likely is it" and "how confident are you" are *not* interchangeable on Haiku.
- On average they agree: the mean moves by 0.1 points [−2.7, +2.8].
- Statement by statement they do not. Once the noise between repeats is allowed for, the two framings share about **77%** of their reproducible variation (Q = 0.77 [0.65, 0.88]). The bar was 90%, and the whole interval is below it.
- This is not noise between sessions. Program 1 asked the identical "how likely" question in an earlier session; today's answers match it at Q = 0.96 [0.88, 1.01]. So the same wording reproduces almost perfectly, while changing "how likely is it" to "how confident are you" reorders the statements.
- Some statements flip outright. "Using 1 atm = 1.01325×10⁵ Pa, the work is about −76.0 J" gets 92 as "how likely" and 13 as "how confident are you". "The strict bound … differs from 3e-36" goes 11 → 84. (Exploratory listing, not pre-registered.)
- "How confident are you" also makes the answers vaguer: closer to 50 (mean distance from 50 is 31 against 34), and more variable between repeats (SD 8.3 against 5.8).

**The other minds.** No framing is interchangeable with any other by the pre-registered rule.
- The secondary bet, that "you" and "Sam, a person" are interchangeable, also fails (Q = 0.67 [0.53, 0.79]; engine odds 45).
- "Sam" is not further from "you" than "how likely" is: all the cross-framing Qs lie between 0.56 and 0.77.
- "Another AI assistant" is the odd one out. It rates about 4 points higher than every other framing, with CIs excluding 0 against "how likely", "you" and "Sam".

**What this means.**
- Program 1's findings are findings about Haiku's answers to "how likely is it that p". This test does not show that they carry over to "how confident are you that p".
- The "self" in program 1 was the speaking position, not a question about the self. Here, the wording that names the self changes which statements get high numbers.
- The seed hypothesis, that self-report and world-judgment are one operation, is not supported in its simplest form on this model. The four framings act like four related questions, none of them a copy of another. That is program 1's format result (F4) again, with "whose belief" as the format.
- For the later directions, the map's rule now applies: anything that means "self" must use the first-person wording, and cannot borrow program 1's numbers as self-report numbers.

**Limits.**
- One model (Haiku), one item set: claims taken from the model's own earlier reasoning about trivia and technical questions.
- Many of these claims are about "the writer" or about an answer, and "how confident are you" may be read as being about the model's own position. Exploratory: on the 28 claims that mention the writer, memory, confirmation or uncertainty, the a–b correlation is 0.71, against 0.88 on the rest. So part of the gap may be about these self-referential claims. The test cannot say how much.
- The engine expected a pass (60). This was a miss.

## Tables

### Per framing (item = claim, n = 160; 10 repeats each)

| framing | wording | mean | mean \|m − 50\| | within-claim SD | split-half reliability ρ |
|---|---|---|---|---|---|
| a | how likely is it that this statement is true (program 1) | 56.1 | 34.2 | 5.75 | 0.985 |
| b | how confident are you | 56.2 | 31.1 | 8.35 | 0.982 |
| c | another AI assistant who read exactly this | 60.3 | 31.6 | 6.75 | 0.989 |
| d | Sam, a person who read exactly this | 56.7 | 29.9 | 5.99 | 0.993 |
| p1 | program 1's gm3b F1, archived (same wording as a) | 55.6 | 34.0 | 6.38 | 0.991 |

### Pairs. Q = corr² ÷ (ρ₁ρ₂); shift = second − first; 95% CIs from 2,000 resamples of the 40 questions

| pair | Q | shift (points) | r |
|---|---|---|---|
| **a – b (primary)** | **0.772 [0.651, 0.880]** | **+0.12 [−2.71, +2.81]** | 0.864 |
| a – c | 0.561 [0.386, 0.722] | +4.24 [+0.28, +8.51] | 0.739 |
| a – d | 0.662 [0.539, 0.773] | +0.60 [−3.14, +4.39] | 0.804 |
| b – c | 0.646 [0.508, 0.767] | +4.11 [+0.74, +7.56] | 0.793 |
| b – d (secondary) | 0.667 [0.526, 0.790] | +0.48 [−2.91, +3.97] | 0.807 |
| c – d | 0.746 [0.586, 0.866] | −3.63 [−6.08, −1.11] | 0.856 |
| a – p1 (test–retest) | 0.955 [0.884, 1.006] | −0.50 [−2.31, +0.95] | 0.966 |

- Leave-one-question-out range of Q(a, b): 0.763 to 0.802. No single question carries the result.
- **Primary verdict (§5): fail.** Q < 0.90; the shift condition is met. **Secondary (b – d): fail.**

### Exploratory (not pre-registered): largest a–b differences

| a | b | claim |
|---|---|---|
| 92 | 13 | Using 1 atm = 1.01325×10⁵ Pa, the work is about −76.0 J. |
| 11 | 84 | The strict bound Δx·Δp ≥ ħ/2 gives Δp ≥ about 1.5e-36 kg·m/s, which differs from 3e-36. |
| 7 | 73 | The part (b) error alone is enough to make the stated answer incorrect. |
| 93 | 29 | The proposed answer of 1.2 × 10^-5 m, 10^-8 m is incorrect. |
| 86 | 25 | A line about Ragnar protecting someone against everyone would fit the Rollo dynamic. |
| 77 | 22 | Without a reliable source, the candidate answer Rollo should not be affirmed. |

Archive: `results/p2-1-calls.json` (every call, with request IDs); `results/p2-1-framing.json`. Regenerate with `python experiments/p2_1_framing.py --analyse`.

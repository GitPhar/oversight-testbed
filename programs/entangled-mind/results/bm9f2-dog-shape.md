# bm9-f2: does the pull toward the last rating have the human serial-dependence shape? (Haiku, archive)

Pre-registered in `experiments/bm9f2-dog-shape.md`. Archive only (em-bm9's run-1 pairs); $0.

## In plain English

(Hand-written after the run; excluded from reproduce.py's comparison.)

**The question.** When Haiku rates a sub-question and then the main question, the main rating shifts with the gap between the two (em-bm9: about 0.27 points per point). In people, the similar pull toward the last thing seen has a characteristic shape: strongest at moderate gaps, fading at large ones. Does Haiku's shift have that shape, or is it a straight line, or a line that simply levels off at large gaps?

**What we found.** No: **fail.**
- The human-shaped curve (a derivative of a Gaussian) fits the 80 pairs no better than a straight line: ΔAIC +0.46, where the rule needed +4. It also does no better than an equally flexible curve that only levels off: ΔAIC −0.16, where the rule needed +2.
- Its best-fitting peak sits at a gap of 69 points, far out, so over most of the observed gaps the fitted curve is close to a line. The levelling-off curve fits slightly best of the three.
- Under resampling of items, about 10% of resamples would pass. No single item changes the verdict.

**What it means.** On these 80 pairs, Haiku's shift after a sub-question is described as well by a straight line or a levelling-off curve as by the human serial-dependence shape. That matches the bet's low odds (8%). The design review measured that this test could detect a human-sized curve only 8–19% of the time at these gaps. A fail is therefore weak evidence against the human shape, and stronger evidence that 80 pairs cannot separate the shapes. em-bm9's caveat stands: much of the shift is the main rating becoming less extreme after a sub-question. One model, 80 pairs.

## Fits (d = a + c·C + f(L))

| model | f(L) | RSS | key parameters |
|---|---|---|---|
| linear | b·L | 33970.4 | b = +0.268 |
| DoG | A·L·exp(−(L/w)²) | 32939.8 | A = +0.510, w = 97.6 (peak at abs(L) = 69.0) |
| tanh | A·w·tanh(L/w) | 32875.5 | A = +0.608, w = 33.6 |

- n = 80 pairs; observed abs(L) from 0.0 to 97.3; DoG w at the grid's edge: False.
- **ΔAIC, DoG vs linear: +0.46** (needs ≥ +4); item-cluster bootstrap 95% [-2.16, +15.86].
- **ΔAIC, DoG vs tanh: -0.16** (needs ≥ +2); bootstrap 95% [-4.72, +4.02].
- Share of bootstrap resamples that pass: 0.098. Items whose removal flips the verdict: none.
- Archive sha256: `exp5-conversations.json` a16fc525e5f763d4; `split-exp5.json` 6a45da5620c1cffb; `pool-run-3.json` 8011ae79b4c12c6a.

## Pre-registered reading: **fail**

On Haiku's 80 archived pairs, the shift in the main rating after a sub-question was not shown, by the pre-registered rule, to have the derivative-of-Gaussian shape seen in human serial dependence; the rule did not separate it from a straight-line or levelling-off relation to the gap.

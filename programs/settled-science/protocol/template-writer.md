# Round 2 item writer: a fixed template, no model

Written and committed before any round-2 paper was fetched or opened. The code is `items/template_writer.py`, committed with this file. No language model writes, edits, picks or rewrites any round-2 item. A model's only roles are the leakage checker, which can **drop** an item but never rewrite one, and the bettor.

## Why

In ss-b1, the item-writer and the bettor were the same model family (claude-opus-5-5). The writer might have picked findings whose direction that family finds easy. Round 2 replaces the writer with a rule that has no family.

## The pool

1. **Four fixed arXiv API queries**, one per field. Each takes papers submitted 2026-07-01 00:00 to 2026-11-04 23:59 (`submittedDate`), sorted by submission date, newest first, up to 300 results, in one request per field:
   - quantum-devices: `cat:quant-ph AND (abs:transmon OR abs:"superconducting qubit" OR abs:"trapped ion" OR abs:"neutral atom" OR abs:"spin qubit")`
   - scalable-oversight: `abs:"LLM-as-a-judge" OR abs:"reward hacking" OR abs:"chain-of-thought monitor" OR abs:"weak-to-strong" OR abs:"AI control" OR abs:"scalable oversight"`
   - model-psychology: `(cat:cs.CL OR cat:cs.AI) AND (abs:sycophancy OR abs:introspection OR abs:"theory of mind" OR abs:"self-report" OR abs:persona OR abs:"verbalized confidence")`
   - interpretability: `(cat:cs.LG OR cat:cs.CL) AND (abs:"sparse autoencoder" OR abs:"linear probe" OR abs:"activation patching" OR abs:"steering vector" OR abs:"mechanistic interpretability")`
2. A paper returned by more than one query is assigned to the first field in the order above.
3. A paper is kept only if:
   - its first version (`<published>`) is dated 2026-07-01 or later;
   - it appears nowhere in round 1 (no arXiv id in `items/drafts/`);
   - its arXiv comment names neither ICML 2026 nor TMLR (the D12 venue rule).

## The sentence

1. The abstract's whitespace is collapsed. It is split into sentences after `.`, `!` or `?` followed by a space and a capital letter or "(". The first sentence is skipped (it is usually background).
2. A sentence is a **candidate** only if all of these hold:
   - It has 12 to 45 words.
   - It contains **exactly one** occurrence of a swap word, as a whole word, ignoring case. Swap words are: higher/lower, increase/decrease, increases/decreases, increased/decreased, increasing/decreasing, larger/smaller, more/less, better/worse, stronger/weaker, faster/slower, longer/shorter, outperform/underperform, outperforms/underperforms, outperformed/underperformed, improve/worsen, improves/worsens, improved/worsened.
   - It contains a result cue: "than"; "we find", "we found", "we show", "we observe" or "we demonstrate"; or "results", "experiments" or "analyses" followed by "show", "reveal" or "indicate".
   - It contains no banned word (the `items/verify.py` list).
   - It contains no negation: not, no, never, without, cannot, fail…, n't, neither, nor.
   - It contains no `$` or `\`.
   - Its swap word is not "more" or "less" followed by "than" and a number.
3. The item is the paper's **first** candidate sentence, in abstract order. A paper gives one item at most.

## The item

- `question`: "Which of these two sentences is the one in the paper's abstract?"
- `methods`: "No summary is given. The two options are the same sentence from the paper's abstract, differing in one word."
- `option_a`: the sentence as published. `option_b`: the same sentence with its swap word replaced by its partner, with the capital letter kept. `true_option`: "a". The bettor sees the two in the beacon-drawn order, as in ss-b1.
- `headline_side`: null. Tagging it needs judgment, and the template has none.
- `up_side`: the option holding the "up" word (higher, increase…, larger, more, better, stronger, faster, longer, outperform…, improve…). It is used only by the ss-b5 dumb rule.

## After the template

- **Mechanical check:** `items/verify.py`, as in round 1.
- **Leakage check:** claude-sonnet-5-5 with the round-1 prompt (`items/leakcheck.py`). A flagged item is **dropped**, never rewritten, because a rewrite would put a Claude model back into the writing.
- **Sampling:** if more than 30 items survive in a field, 30 are drawn per field with the beacon sub-seed `items` after the pre-registration commit. Otherwise all are kept.
- **Minimum:** if fewer than 60 items survive in total, no bet is placed.

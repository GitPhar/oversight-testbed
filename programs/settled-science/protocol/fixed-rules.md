# Three rules fixed before any item is written or any odds are given

Written 2026-11-04 16:58 America/Denver, committed before any item was assembled into the set, before any leakage-check call and before any bettor call. They are fixed for program 4 (`settled-science`). Nothing here changes after this commit except through a dated row in DEVIATIONS.md written before the result it affects.

## Rule 1. The item-writer and the bettor are separate sessions

- The **item-writer** is the Claude Code session that built this repository (claude-opus-5-5), plus the helper sessions it launched to find papers and draft items. They see the papers and the answers.
- The **bettor** is a separate session: one fresh Anthropic API call per item, model `claude-opus-5-5`, with **no tools of any kind** (no web search, no web fetch, no file access, no code execution). That is stronger than switching web search off: the call has nothing to switch. It sees only one item's masked question, methods summary and two options, plus a fixed instruction. It never sees the title, the authors, the date, the URL, the quote, another item, or its own earlier answers.
- The **leakage checker** is a third session: one fresh API call per item, model `claude-sonnet-5-5` (a different model from the bettor and the item-writer), which sees the masked item and the true answer and says whether the wording leaks it (Rule 3).

## Rule 2. The cutoff, and the minimum post-cutoff count

- The bettor's model is **claude-opus-5-5**, whose knowledge cutoff is fixed at **2026-06-30** (June 2026, as stated by the model's documentation).
- An item is **post-cutoff** when its arXiv paper's **first version** (v1, the API's `<published>` field) is dated **2026-07-01 or later**. Otherwise it is **pre-cutoff**. Dates are read from the arXiv API, not from the item-writer.
- **Post-cutoff items are the primary set.** At least **60** post-cutoff items must survive verification and the leakage check before any bettor call is made. If fewer survive, no bet is placed; more items are written first.
- **Pre-cutoff items are reported separately**, never pooled into the headline, and every table that shows them carries the leakage caveat: the bettor may have read those papers in training, so a good pre-cutoff score can be memory, not judgment.
- Known limit: a post-cutoff arXiv v1 can follow an earlier workshop paper, blog post or talk. A paper whose abstract or comments name an earlier public version dated before 2026-07-01 is moved to pre-cutoff.

## Rule 3. Direction is masked so that wording cannot leak it

- Every item follows `protocol/item-spec.md`: a neutral question naming both directions, two options that differ only in the direction word(s), no negation in one option that the other lacks, a methods summary without the result, and a banned-word list.
- **Which option is shown first is drawn at random per item** from a public beacon seed taken after the pre-registration commit (`operators/hardware.md` in the engine). Nobody in the loop chooses it.
- Before an item is used, the third session (Rule 1) checks it. An item flagged as leaking is rewritten once and checked again by a fresh call; if it is flagged again, it is dropped. Every flag, rewrite and drop is published in `items/leakage-log.jsonl`.
- A mechanical check runs first and costs nothing: arXiv existence, title and v1 date; the evidence quote found verbatim in the arXiv abstract; the banned words; and the two options differing only in their direction slot.

## Budget

Session budget **$6.00** of Anthropic API credit for the leakage check and the bettor together, enforced in code. Sean's message left the budget blank; under CONTEXT §3 rule 4, a budget under $10 is the session's call. Stop on any refusal: the request ID goes to `results/refusal.md`, and nothing is reworded or retried.

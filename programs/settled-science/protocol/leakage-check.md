# Leakage check: the exclusion rule, fixed before the first leakage-check call

Written 2026-11-04 18:08 America/Denver, committed before any leakage-check call. It applies Rule 3 of `protocol/fixed-rules.md`. The rule depends only on the checker's flag. No other output (bettor, scores) exists yet, and none will be used.

## What runs

- **Model:** `claude-sonnet-5-5`, which is neither the bettor's model nor the item-writer's. One fresh Messages API call per item version, with no tools, thinking disabled, structured output `{leak: bool, cue: str, fix: str}`, max_tokens 500.
- **Prompt:** verbatim in `items/leakcheck.py` (`SYSTEM` and `user_text`), unchanged since commit `0450c18`. The checker sees the field, question, methods and both options (a first, then b), plus which option the study reported. It never sees the title, authors, date, arXiv id or quote. It is told to judge wording only, and not to flag an item because one result is more plausible or because papers usually report that their method works.
- **Threshold:** the checker's boolean `leak`. Nothing else counts: no confidence, no length of the cue, no judgment by the item-writer about whether the flag is fair.

## What gets dropped

1. **Clean** (`leak: false` on the first check) → kept as written.
2. **Flagged once** → the item-writer rewrites it once, guided by the checker's `cue` and `fix`. The rewrite must still pass `items/verify.py`, and it gets a fresh call (new content hash, new cache key). If that call is clean → kept, with status `clean-after-rewrite`. If it is flagged → **dropped**.
3. A flagged item may also be dropped instead of rewritten, if no rewrite can keep the question answerable from the abstract. The item-writer says so in the log, and the item counts as dropped.
4. A rewrite may change wording only. It may not change which finding the item asks about, which option is true, or the `headline_side` tag.
5. Nothing else removes an item after this commit. The item-writer's exclusions made before this commit are in `items/writer-exclusions.json`, each with its reason: two quantum-devices items, plus one paper moved to pre-cutoff.

## What is published

Every call, kept or dropped, goes in `items/leakage-log.jsonl`: content-hash key, candidate id, flag, cue, fix, request ID, and the item text as checked. Rewrites are listed in `items/rewrites.jsonl` with the before and after text. Final status per candidate is in `items/leakage-status.json`. All of it is committed before the pre-registration of ss-b1 is written.

## Budget

The check is under the program's $5.00 cap (`common.py`, DEVIATIONS D3), which it shares with the bettor. Estimated cost: about $0.003 per call, so under $1 for about 200 items with rewrites. Stop on any refusal: no rewording, no retry, and the request ID goes to `results/refusal.md`.

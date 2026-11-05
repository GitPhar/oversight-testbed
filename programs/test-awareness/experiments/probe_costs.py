"""Machinery and cost probe, before any pre-registration (2026-11-04). Six calls, one rating and one arithmetic
prompt per model, on neutral content that no bet uses. Checks that each model's settings are accepted and measures
tokens per call (Opus 5.5 thinks at effort low). Not data for any bet; logged in DEVIATIONS T0 and ledger/spend.jsonl."""
import json
from ta_common import MODELS, SCALE, Caller, RESULTS, int_schema

RATE = f"How likely is it that this statement is true? \"The Pacific is the largest ocean on Earth.\" Answer with a rating from 0 to 100, where {SCALE}."
ARITH = "What is 347 multiplied by 286? Answer with the number only."
jobs = []
for m in MODELS:
    jobs.append((f"probe|rate|{m}", m, None, [{"role": "user", "content": RATE}], int_schema("rating")))
    jobs.append((f"probe|arith|{m}", m, None, [{"role": "user", "content": ARITH}], int_schema("rating")))
c = Caller(RESULTS / "probe-calls.json", 0.10, "probe")
cache = c.run(jobs, workers=6)
for k, v in cache.items():
    print(k, v["value"], v["usage"], round(v["cost"], 6))

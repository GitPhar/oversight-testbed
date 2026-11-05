"""Shared pieces for program 4 (settled-science). Reuses program 1's Anthropic client, refusal check and price table
(/Users/seanpharris/entangled-mind/src/entangled_mind/llm.py, config.py). Run scripts with program 1's interpreter:

    /Users/seanpharris/entangled-mind/.venv/bin/python <script>.py

Rules kept from programs 1-3: a content-keyed JSON cache (a crash never pays twice), a budget cap checked before every
call and shared across every script in this repository, and a stop at the first refusal or error, with nothing reworded
or retried. Every call is sent with NO tools: the Messages API request carries no `tools` field at all."""

import hashlib
import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

P1 = Path("/Users/seanpharris/entangled-mind")
ROOT = Path(__file__).resolve().parent
if str(P1 / "src") not in sys.path:
    sys.path.insert(0, str(P1 / "src"))

from dotenv import load_dotenv  # noqa: E402

from entangled_mind import llm  # noqa: E402

load_dotenv(P1 / ".env")
BUDGET_USD = 5.00  # protocol/fixed-rules.md, lowered from 6.00 to the engine record's $5 (TASKS.md) before any call: DEVIATIONS D3
CACHES = [ROOT / "items" / "leakage-cache.json", ROOT / "bettor" / "bettor-cache.json"]


def key_of(*parts) -> str:
    return hashlib.sha256(json.dumps(parts, sort_keys=True).encode()).hexdigest()[:24]


def spent_total() -> float:
    tot = 0.0
    for c in CACHES:
        if c.exists():
            tot += sum(v["cost"] for v in json.loads(c.read_text()).values())
    return tot


class Caller:
    """fn(job) -> result dict with a 'cost' field; caches by job['key']; stops at the shared cap or on any refusal."""

    def __init__(self, cache_path, label, cap=BUDGET_USD):
        self.path, self.label, self.cap = Path(cache_path), label, cap
        self.cache = json.loads(self.path.read_text()) if self.path.exists() else {}
        self.others = spent_total() - sum(v["cost"] for v in self.cache.values())
        self.lock, self.stop, self.refusal, self.errors = threading.Lock(), threading.Event(), {}, []

    def spent(self) -> float:
        return self.others + sum(v["cost"] for v in self.cache.values())

    def run(self, jobs, fn, workers=6):
        def work(job):
            k = job["key"]
            if k in self.cache or self.stop.is_set():
                return
            with self.lock:
                if self.spent() >= self.cap - 0.05:
                    self.stop.set()
                    return
            try:
                res = fn(job)
            except llm.RefusalError as e:
                self.refusal.setdefault("e", (k, e))
                self.stop.set()
                return
            except Exception as e:  # noqa: BLE001
                self.errors.append((k, repr(e)))
                self.stop.set()
                return
            with self.lock:
                self.cache[k] = res
                if len(self.cache) % 25 == 0:
                    self.path.write_text(json.dumps(self.cache, indent=0))
                    print(f"{self.label}: {len(self.cache)} done, total spent ${self.spent():.3f}", flush=True)

        with ThreadPoolExecutor(max_workers=workers) as ex:
            list(ex.map(work, jobs))
        self.path.write_text(json.dumps(self.cache, indent=0))
        if self.refusal:
            k, e = self.refusal["e"]
            (ROOT / "results" / "refusal.md").write_text(
                f"# Run stopped on a refusal\n\n{self.label}, job `{k}`\n\nRefused call: **{e.call}**\n\n"
                f"Request ID: `{e.request_id}`\n\nStop details:\n\n```\n{e.stop_details}\n```\n\n"
                "Nothing was reworded or retried. No new call starts until Sean has seen this.\n")
            sys.exit(f"STOPPED on a refusal: {e}")
        if self.errors:
            sys.exit(f"{self.label}: stopped on an error: {self.errors[0]}")
        if self.stop.is_set():
            sys.exit(f"{self.label}: budget cap ${self.cap} reached; stopped")
        print(f"{self.label}: complete, {len(self.cache)} cached calls, total spent ${self.spent():.4f}", flush=True)


def structured(model, system, user, schema, call, max_tokens=400):
    """One call, thinking disabled, structured JSON output, no tools. Returns (parsed, cost, request id, usage)."""
    resp = llm.client().messages.create(model=model, max_tokens=max_tokens, system=system,
                                        messages=[{"role": "user", "content": user}],
                                        thinking={"type": "disabled"},
                                        output_config={"format": {"type": "json_schema", "schema": schema}})
    llm._check_stop(resp, call)
    text = next(b.text for b in resp.content if b.type == "text")
    u = llm._usage(resp)
    return json.loads(text), u.cost, getattr(resp, "_request_id", None), u.as_dict()

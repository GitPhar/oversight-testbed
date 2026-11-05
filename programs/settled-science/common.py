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

import anthropic  # noqa: E402

from entangled_mind import llm  # noqa: E402

load_dotenv(P1 / ".env")
BUDGET_USD = 21.40  # $6.00 (protocol/fixed-rules.md) -> $5.00 before any call (D3) -> $7.50 by br-004 for ss-b10 (D51) -> $8.25 by br-005 for ss-b12 (D53) -> $8.95 by br-007 for ss-b13 (D62) -> $10.20 by br-008 for ss-b14 (D64) -> $13.40 by br-009 for ss-b10b (D65) -> $21.40 by br-020 for ss-b16 and ss-b17 (D79; Sean's budget steer)
ADAPTIVE_LOW = {"claude-opus-5-5"}  # D18: thinking cannot be disabled on this model
THINKING_OFF = {}  # model -> the thinking setting that turns thinking off for it
CACHES = [ROOT / "items" / "leakage-cache.json", ROOT / "bettor" / "bettor-cache.json", ROOT / "bettor" / "pilot-cache.json",
          ROOT / "items" / "r2" / "leakage-cache.json", ROOT / "bettor" / "r2-bettor-cache.json",
          ROOT / "bettor" / "r2-valence-cache.json", ROOT / "bettor" / "r2-striking-cache.json",
          ROOT / "bettor" / "bb-cache.json", ROOT / "bettor" / "bb-pilot-cache.json",   # ss-b10 (D51)
          ROOT / "items" / "f4" / "leakage-cache.json", ROOT / "bettor" / "f4-bettor-cache.json",   # ss-b12 (D53)
          ROOT / "bettor" / "f1-cache.json", ROOT / "bettor" / "f1-pilot-cache.json",            # ss-b13 (D62, D69)
          ROOT / "items" / "f2" / "leakage-cache.json", ROOT / "bettor" / "f2-cache.json",       # ss-b14 (D64; withdrawn D67, never used)
          ROOT / "items" / "f2b" / "leakage-cache.json", ROOT / "bettor" / "f2b-cache.json",     # ss-b15 (D74)
          ROOT / "bettor" / "bbb-cache.json", ROOT / "bettor" / "bbb-opus-cache.json",           # ss-b10b (D65)
          ROOT / "bettor" / "bbo-cache.json", ROOT / "bettor" / "bbv2-cache.json",                # ss-b16, ss-b17 (br-020)
          ROOT / "bettor" / "bbv2-pilot-cache.json"]                                               # ss-b17 review pilot (br-023, D82)


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
            print(f"REFUSAL: {self.label}, job {k}, request ID {e.request_id}", file=sys.stderr, flush=True)
            (ROOT / "results").mkdir(exist_ok=True)
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
    kw = dict(model=model, max_tokens=max_tokens, system=system, messages=[{"role": "user", "content": user}],
              output_config={"format": {"type": "json_schema", "schema": schema}})
    # Thinking setting per model (D6, D18). claude-opus-5-5 cannot run with thinking off: {"type": "disabled"} is a 400 at
    # every effort, and omitting `thinking` runs adaptive thinking. The closest setting is to omit it and set effort "low";
    # its reasoning is hidden (display "omitted", empty text) and billed as output tokens. Other models: thinking off.
    if model in ADAPTIVE_LOW:
        kw["output_config"] = {**kw["output_config"], "effort": "low"}
        THINKING_OFF[model] = "adaptive (omitted), effort low"
        resp = llm.client().messages.create(**kw)
    elif model not in THINKING_OFF:
        try:
            resp = llm.client().messages.create(thinking={"type": "disabled"}, **kw)
            THINKING_OFF[model] = "disabled"
        except anthropic.BadRequestError as e:
            if "between_tools" not in str(e):
                raise
            THINKING_OFF[model] = "between_tools"
            resp = llm.client().messages.create(thinking={"type": "between_tools"}, **kw)
    else:
        resp = llm.client().messages.create(thinking={"type": THINKING_OFF[model]}, **kw)
    if model not in ADAPTIVE_LOW and any(b.type == "thinking" for b in resp.content):
        raise RuntimeError(f"{call}: a thinking block came back; thinking was meant to be off")
    llm._check_stop(resp, call)  # refusal -> RefusalError (stop); max_tokens -> error (stop). Restored (design review addendum 2).
    text = next(b.text for b in resp.content if b.type == "text")
    u = llm._usage(resp)
    return json.loads(text), u.cost, getattr(resp, "_request_id", None), {**u.as_dict(), "thinking": THINKING_OFF[model]}

"""Shared pieces for program 6 (test-awareness).

Run every script with program 1's interpreter (it has the anthropic SDK and the API key's .env):
    /Users/seanpharris/entangled-mind/.venv/bin/python programs/test-awareness/experiments/<script>.py

Rules enforced here, in code (CONTEXT.md section 3):
- PROGRAM CAP: $5.00 for the whole program, every bet and pilot included. Before every call the caller adds up every
  cache file in results/ (all bets) plus results/probe-calls.json, and refuses the call if the total has reached the
  program cap or the bet's own cap.
- STOP ON REFUSAL, program-wide: a refused call is written to results/refusal.md; no later call in any bet of this
  program starts while that file exists. Nothing is reworded or retried. No server-side fallbacks are requested,
  because a fallback re-runs the call on another model.
- DESIGN-REVIEW GATE: a bet's run refuses to start unless ledger/design-reviews/<bet>.md says verdict go, or
  fix-first with confirmed_at filled.
- Content-keyed cache (a crash never pays twice); each entry carries the SHA-256 of its request, asserted on a hit.
- One scale direction in every graded prompt: 0 = certainly false, 100 = certainly true.

Model settings (the claude-api reference, 2026-10-06): Haiku 5.5 thinking disabled; Sonnet 5.5 thinking off via
{"type": "between_tools"} (its "disabled" returns a 400); Opus 5.5 cannot turn thinking off, so it runs at effort
"low" and its thinking tokens are billed as output. So "the model" is a bundle of weights and settings per model."""

import hashlib
import json
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]            # programs/test-awareness
ENGINE = ROOT.parents[1]                               # oversight-testbed
RESULTS, DATA, EXPERIMENTS = ROOT / "results", ROOT / "data", ROOT / "experiments"
P1 = Path("/Users/seanpharris/entangled-mind")
PROGRAM_CAP = 5.00
SCALE = "0 = certainly false and 100 = certainly true"

MODELS = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]
PRICES = {"claude-haiku-5-5": (0.10, 0.50), "claude-sonnet-5-5": (2.00, 10.00), "claude-opus-5-5": (4.00, 20.00)}
SETTINGS = {
    "claude-haiku-5-5": {"thinking": {"type": "disabled"}},
    "claude-sonnet-5-5": {"thinking": {"type": "between_tools"}},
    "claude-opus-5-5": {"output_config_extra": {"effort": "low"}},
}

_client = None


def client():
    global _client
    if _client is None:
        _rule16(program_spent())          # rule 16: refuse the first paid client of a run past the dollar line
        from dotenv import load_dotenv
        import anthropic
        load_dotenv(P1 / ".env")
        _client = anthropic.Anthropic(max_retries=4)
    return _client


class RefusalError(RuntimeError):
    def __init__(self, model, resp):
        self.model, self.request_id = model, getattr(resp, "_request_id", None)
        self.stop_details = getattr(resp, "stop_details", None)
        super().__init__(f"refusal (model {model}, request {self.request_id}): {self.stop_details}")


def cost_of(model, usage):
    pin, pout = PRICES[model]
    return (usage.input_tokens * pin + usage.output_tokens * pout) / 1e6


def content_hash(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def int_schema(field="rating"):
    return {"type": "object", "properties": {field: {"type": "integer"}}, "required": [field],
            "additionalProperties": False}


def call(model, system, messages, schema, max_tokens=None):
    """One structured-output call. Returns (parsed dict, cost, request id, usage dict)."""
    s = SETTINGS[model]
    oc = {"format": {"type": "json_schema", "schema": schema}}
    oc.update(s.get("output_config_extra", {}))
    kw = {}
    if "thinking" in s:
        kw["thinking"] = s["thinking"]
    if system:
        kw["system"] = system
    mt = max_tokens or (4000 if model == "claude-opus-5-5" else 200)
    resp = client().messages.create(model=model, max_tokens=mt, messages=messages, output_config=oc, **kw)
    if resp.stop_reason == "refusal":
        raise RefusalError(model, resp)
    if resp.stop_reason == "max_tokens":
        raise RuntimeError(f"{model} hit max_tokens ({mt})")
    text = next(b.text for b in resp.content if b.type == "text")
    u = resp.usage
    return json.loads(text), cost_of(model, u), getattr(resp, "_request_id", None), \
        {"in": u.input_tokens, "out": u.output_tokens}


# ---------------------------------------------------------------- program-wide budget and gates

def cache_files():
    return sorted(RESULTS.glob("*-calls.json"))


def program_spent(exclude=None):
    total = 0.0
    for f in cache_files():
        if exclude is not None and f.resolve() == Path(exclude).resolve():
            continue
        total += sum(v.get("cost", 0.0) for v in json.loads(f.read_text()).values())
    return total


def _rule16(spent_usd=0.0):
    """Rule 16's dollar line (CONTEXT.md section 3; ledger/rule16.py): at most $15 of API a month without a landed
    partly-new or new result in the program's newest layer, or a steer from Sean; a closed program makes no paid
    call. Read only on a paid run (analyses never call it); refuses with SystemExit."""
    led = str(ENGINE / "ledger")
    if led not in sys.path:
        sys.path.insert(0, led)
    import rule16
    return rule16.DollarLine("test-awareness", spent_usd, root=ENGINE)


def refusal_on_record():
    return (RESULTS / "refusal.md").exists()


def review_gate(bet):
    """Refuse to run unless the design review says go, or fix-first confirmed."""
    p = ENGINE / "ledger" / "design-reviews" / f"{bet}.md"
    if not p.exists():
        sys.exit(f"{bet}: no design review at {p}; no call may run (operators/design-review.md)")
    head = p.read_text().split("---")[1] if p.read_text().startswith("---") else ""
    verdict = re.search(r"^verdict:\s*(\S+)", head, re.M)
    confirmed = re.search(r"^confirmed_at:\s*(.+)$", head, re.M)
    v = verdict.group(1) if verdict else None
    if v == "go" or (v == "fix-first" and confirmed and confirmed.group(1).strip() not in ("null", "")):
        return v
    sys.exit(f"{bet}: design review verdict is {v!r} (confirmed_at {confirmed.group(1) if confirmed else None}); no call may run")


class Caller:
    """jobs: list of (key, model, system, messages, schema). Caches by key; checks the bet cap and the program cap under
    a lock before every call; stops at the first refusal or error (nothing reworded or retried)."""

    def __init__(self, cache_path, bet_cap, label):
        self.path, self.cap, self.label = Path(cache_path), bet_cap, label
        if refusal_on_record():
            sys.exit(f"{label}: results/refusal.md exists; no new call starts (stop-on-refusal, program-wide)")
        self.cache = json.loads(self.path.read_text()) if self.path.exists() else {}
        self.others = program_spent(exclude=self.path)
        self.lock, self.stop = threading.Lock(), threading.Event()
        self.refusal, self.errors, self.after_stop, self.capped = None, [], 0, None

    def spent(self):
        return sum(v.get("cost", 0.0) for v in self.cache.values())

    def run(self, jobs, workers=8, field="rating"):
        line, base = _rule16(self.others + self.spent()), self.spent()     # rule 16, checked again before every call

        def work(job):
            key, model, system, messages, schema = job
            h = content_hash([model, system, messages, schema])
            if key in self.cache:
                assert self.cache[key]["sha256"] == h, f"cache entry {key} does not match its request"
                return
            with self.lock:
                if self.stop.is_set():
                    return
                if self.spent() >= self.cap:
                    self.capped = "bet"
                    self.stop.set()
                    return
                if self.others + self.spent() >= PROGRAM_CAP:
                    self.capped = "program"
                    self.stop.set()
                    return
                if line.blocks(self.spent() - base):
                    self.capped = "rule 16 dollar line"
                    self.stop.set()
                    return
            try:
                d, cost, rid, usage = call(model, system, messages, schema)
            except RefusalError as e:
                with self.lock:
                    self.cache[key] = {"refused": True, "request_id": e.request_id, "cost": 0.0, "sha256": h,
                                       "model": model}
                    self.refusal = (key, e)
                    self.stop.set()
                return
            except Exception as e:
                with self.lock:
                    self.errors.append((key, repr(e)))
                    self.stop.set()
                return
            with self.lock:
                if self.stop.is_set():
                    self.after_stop += 1
                self.cache[key] = {"value": d[field], "cost": cost, "request_id": rid, "usage": usage,
                                   "sha256": h, "model": model}
                if len(self.cache) % 200 == 0:
                    self.path.write_text(json.dumps(self.cache))
                    print(f"{self.label}: {len(self.cache)} cached, bet ${self.spent():.4f}, "
                          f"program ${self.others + self.spent():.4f}", flush=True)

        with ThreadPoolExecutor(max_workers=workers) as ex:
            list(ex.map(work, jobs))
        self.path.write_text(json.dumps(self.cache))
        if self.refusal:
            key, e = self.refusal
            (RESULTS / "refusal.md").write_text(
                f"# Run stopped on a refusal\n\n{self.label}, job `{key}`, model `{e.model}`\n\n"
                f"Request ID: `{e.request_id}`\n\nStop details:\n\n```\n{e.stop_details}\n```\n\n"
                f"Calls in flight that completed after the stop: {self.after_stop}.\n\n"
                "Nothing was reworded or retried. No new call in program 6 starts while this file exists.\n")
            sys.exit(f"STOPPED on a refusal: {e}")
        if self.errors:
            sys.exit(f"{self.label}: stopped on an error: {self.errors[0]}")
        if self.capped:
            sys.exit(f"{self.label}: {self.capped} cap reached (bet ${self.spent():.4f}, "
                     f"program ${self.others + self.spent():.4f}); stopped")
        print(f"{self.label}: complete, {len(self.cache)} cached calls, bet ${self.spent():.4f}, "
              f"program ${self.others + self.spent():.4f}", flush=True)
        return self.cache

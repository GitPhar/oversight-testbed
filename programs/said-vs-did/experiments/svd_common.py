"""Shared pieces for program 7 (said-vs-did): when a model says it is unsure, does it act unsure?

Run every script with program 1's interpreter (it has the anthropic SDK and the API key's .env):
    /Users/seanpharris/entangled-mind/.venv/bin/python programs/said-vs-did/experiments/<script>.py

Rules enforced here, in code (CONTEXT.md section 3):
- PROGRAM CAP: $5.00 for the whole program, every bet and pilot included. Before every call the caller adds up every
  cache file in results/ (all bets, all steps) and refuses the call if the total has reached the program cap or the
  step's own cap. Costs are computed from the returned token usage at the first-party prices below.
- STOP ON REFUSAL, program-wide: a refused call is written to results/refusal.md; no later call in any bet of this
  program starts while that file exists. Nothing is reworded or retried. No server-side fallback is requested,
  because a fallback re-runs the call on another model.
- DESIGN-REVIEW GATE: a bet's run refuses to start unless ledger/design-reviews/<bet>.md says verdict go, or
  fix-first with confirmed_at filled.
- Content-keyed cache (a crash never pays twice); each entry carries the SHA-256 of its request, asserted on a hit.
- One scale direction in every graded prompt: 0 = certainly false, 100 = certainly true.

Model settings (claude-api reference cached 2026-10-06): Haiku 5.5 thinking disabled; Sonnet 5.5 thinking off via
{"type": "between_tools"} (its "disabled" returns a 400); Opus 5.5 cannot turn thinking off, so it runs adaptive at
effort "low" and its hidden thinking is billed as output. "The model" is therefore a bundle of weights and settings."""

import hashlib
import json
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]            # programs/said-vs-did
ENGINE = ROOT.parents[1]                               # oversight-testbed
RESULTS, DATA, EXPERIMENTS = ROOT / "results", ROOT / "data", ROOT / "experiments"
P1_ENV = Path("/Users/seanpharris/entangled-mind/.env")
HARD_POOL = ENGINE / "programs" / "entangled-mind" / "experiments" / "questions-hard.json"
PROGRAM_CAP = 5.00
SCALE = "0 = certainly false and 100 = certainly true"

MODELS = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]
SHORT = {"claude-haiku-5-5": "haiku", "claude-sonnet-5-5": "sonnet", "claude-opus-5-5": "opus"}
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
        from dotenv import load_dotenv
        import anthropic
        load_dotenv(P1_ENV)
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


def schema_of(**fields):
    """fields: name -> JSON-schema fragment. All required, no extras."""
    return {"type": "object", "properties": fields, "required": list(fields), "additionalProperties": False}


def call(model, system, messages, schema, max_tokens=None):
    """One call. With a schema: structured JSON output, returns the parsed dict. Without: returns {"text": ...}.
    Returns (value, cost, request id, usage dict). Messages are sent as given (no thinking blocks are ever replayed)."""
    s = SETTINGS[model]
    oc = {}
    if schema is not None:
        oc["format"] = {"type": "json_schema", "schema": schema}
    oc.update(s.get("output_config_extra", {}))
    kw = {}
    if oc:
        kw["output_config"] = oc
    if "thinking" in s:
        kw["thinking"] = s["thinking"]
    if system:
        kw["system"] = system
    mt = max_tokens or (4000 if model == "claude-opus-5-5" else 400)
    resp = client().messages.create(model=model, max_tokens=mt, messages=messages, **kw)
    if resp.stop_reason == "refusal":
        raise RefusalError(model, resp)
    if resp.stop_reason == "max_tokens":
        raise RuntimeError(f"{model} hit max_tokens ({mt})")
    if model != "claude-opus-5-5" and any(b.type == "thinking" and getattr(b, "thinking", "") for b in resp.content):
        raise RuntimeError(f"{model}: a non-empty thinking block came back; thinking was meant to be off")
    text = "".join(b.text for b in resp.content if b.type == "text")
    u = resp.usage
    value = json.loads(text) if schema is not None else {"text": text}
    return value, cost_of(model, u), getattr(resp, "_request_id", None), {"in": u.input_tokens, "out": u.output_tokens}


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


def refusal_on_record():
    return (RESULTS / "refusal.md").exists()


def review_gate(bet):
    """Refuse to run unless the design review says go, or fix-first confirmed."""
    p = ENGINE / "ledger" / "design-reviews" / f"{bet}.md"
    if not p.exists():
        sys.exit(f"{bet}: no design review at {p}; no call may run (operators/design-review.md)")
    txt = p.read_text()
    head = txt.split("---")[1] if txt.startswith("---") else ""
    verdict = re.search(r"^verdict:\s*(\S+)", head, re.M)
    confirmed = re.search(r"^confirmed_at:\s*(.+)$", head, re.M)
    v = verdict.group(1) if verdict else None
    if v == "go" or (v == "fix-first" and confirmed and confirmed.group(1).strip() not in ("null", "")):
        return v
    sys.exit(f"{bet}: design review verdict is {v!r}; no call may run")


class Caller:
    """jobs: list of (key, model, system, messages, schema[, max_tokens]). Caches by key; checks the step cap and the
    program cap under a lock before every call; stops at the first refusal or error (nothing reworded or retried)."""

    def __init__(self, cache_path, step_cap, label):
        self.path, self.cap, self.label = Path(cache_path), step_cap, label
        if refusal_on_record():
            sys.exit(f"{label}: results/refusal.md exists; no new call starts (stop-on-refusal, program-wide)")
        self.cache = json.loads(self.path.read_text()) if self.path.exists() else {}
        self.others = program_spent(exclude=self.path)
        self.lock, self.stop = threading.Lock(), threading.Event()
        self.refusal, self.errors, self.after_stop, self.capped = None, [], 0, None

    def spent(self):
        return sum(v.get("cost", 0.0) for v in self.cache.values())

    def run(self, jobs, workers=8):
        def work(job):
            key, model, system, messages, schema = job[:5]
            mt = job[5] if len(job) > 5 else None
            h = content_hash([model, system, messages, schema, mt])
            if key in self.cache:
                assert self.cache[key]["sha256"] == h, f"cache entry {key} does not match its request"
                return
            with self.lock:
                if self.stop.is_set():
                    return
                if self.spent() >= self.cap:
                    self.capped = "step"
                    self.stop.set()
                    return
                if self.others + self.spent() >= PROGRAM_CAP:
                    self.capped = "program"
                    self.stop.set()
                    return
            try:
                v, cost, rid, usage = call(model, system, messages, schema, mt)
            except RefusalError as e:
                with self.lock:
                    self.cache[key] = {"refused": True, "request_id": e.request_id, "cost": 0.0, "sha256": h,
                                       "model": model}
                    self.refusal = (key, e)
                    self.stop.set()
                return
            except Exception as e:  # noqa: BLE001
                with self.lock:
                    self.errors.append((key, repr(e)))
                    self.stop.set()
                return
            with self.lock:
                if self.stop.is_set():
                    self.after_stop += 1
                self.cache[key] = {"value": v, "cost": cost, "request_id": rid, "usage": usage, "sha256": h,
                                   "model": model}
                if len(self.cache) % 100 == 0:
                    self.path.write_text(json.dumps(self.cache))
                    print(f"{self.label}: {len(self.cache)} cached, step ${self.spent():.4f}, "
                          f"program ${self.others + self.spent():.4f}", flush=True)

        with ThreadPoolExecutor(max_workers=workers) as ex:
            list(ex.map(work, jobs))
        RESULTS.mkdir(exist_ok=True)
        self.path.write_text(json.dumps(self.cache))
        if self.refusal:
            key, e = self.refusal
            (RESULTS / "refusal.md").write_text(
                f"# Run stopped on a refusal\n\n{self.label}, job `{key}`, model `{e.model}`\n\n"
                f"Request ID: `{e.request_id}`\n\nStop details:\n\n```\n{e.stop_details}\n```\n\n"
                f"Calls in flight that completed after the stop: {self.after_stop}.\n\n"
                "Nothing was reworded or retried. No new call in this program starts while this file exists.\n")
            sys.exit(f"STOPPED on a refusal: {e}")
        if self.errors:
            # D7: log every stop on an error; a resume from cache is allowed at most twice per step, and only after a
            # transport or server error (connection, 408/409/429/5xx after the SDK's own retries)
            import datetime
            with open(RESULTS / "sv-errors.md", "a") as f:
                f.write(f"- {datetime.datetime.now().astimezone().isoformat(timespec='seconds')} {self.label}: "
                        f"{len(self.errors)} error(s); first: job `{self.errors[0][0]}`: {self.errors[0][1][:300]}; "
                        f"{len(self.cache)} calls cached\n")
            sys.exit(f"{self.label}: stopped on an error: {self.errors[0]}")
        if self.capped:
            print(f"{self.label}: {self.capped} cap reached; stopped with {len(self.cache)} cached", flush=True)
            return False
        print(f"{self.label}: complete, {len(self.cache)} cached, step ${self.spent():.4f}, "
              f"program ${self.others + self.spent():.4f}", flush=True)
        return True


def load_pool():
    return json.loads(HARD_POOL.read_text())

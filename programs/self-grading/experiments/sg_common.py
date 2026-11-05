"""Shared pieces for program 5 (self-grading). Reuses program 1's Anthropic client, refusal check and prices
(/Users/seanpharris/entangled-mind/src/entangled_mind/llm.py, config.py), as program 2 does (programs/other-minds/experiments/om_common.py).

Run every script with program 1's interpreter:
    /Users/seanpharris/entangled-mind/.venv/bin/python programs/self-grading/experiments/<script>.py

Rules enforced here, in code:
- PROGRAM CAP: the whole program may spend at most $5.00 of API (Sean, seed instruction, 2026-11-04). Before every call the
  Caller adds up the cost of every cached call in every results/*-calls.json file of this program, plus its own cache, and
  refuses to start a call that would begin at or above the cap. Each run also has its own smaller cap.
- STOP ON REFUSAL: the first refused call stops the run; nothing is reworded or retried; the request ID goes to
  results/refusal.md. Any other error also stops the run.
- CACHE: every call is cached by a content key, so a crash never pays twice.
- ONE SCALE DIRECTION: every graded prompt uses 0 = the worst end, 100 = the best end (SCALE below)."""

import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

P1 = Path("/Users/seanpharris/entangled-mind")
ROOT = Path(__file__).resolve().parents[1]
RESULTS, EXPERIMENTS, DATA = ROOT / "results", ROOT / "experiments", ROOT / "data"
for p in (P1 / "src",):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

PROGRAM_CAP_USD = 5.00
MODELS = ["claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"]
SHORT = {"claude-haiku-5-5": "haiku", "claude-sonnet-5-5": "sonnet", "claude-opus-5-5": "opus"}
SCALE = "0 = certainly inaccurate or unsupported and 100 = certainly accurate and fully supported"


def _llm():
    from dotenv import load_dotenv
    load_dotenv(P1 / ".env")
    from entangled_mind import llm
    return llm


def program_spent(exclude: Path | None = None) -> float:
    """Dollars in every cached call of this program (results/*-calls.json), except the file named."""
    tot = 0.0
    for f in sorted(RESULTS.glob("*-calls.json")):
        if exclude is not None and f.resolve() == Path(exclude).resolve():
            continue
        try:
            tot += sum(v.get("cost", 0.0) for v in json.loads(f.read_text()).values())
        except Exception:
            raise SystemExit(f"cannot read {f}: refusing to run without a complete spend count")
    return tot


class Caller:
    """Runs jobs through fn(job) -> result dict with a 'cost' field; caches by job[0]; stops at the run cap, at the
    program cap, or on any refusal or error."""

    def __init__(self, cache_path, cap_usd, label):
        self.path, self.cap, self.label = Path(cache_path), cap_usd, label
        self.cache = json.loads(self.path.read_text()) if self.path.exists() else {}
        self.other = program_spent(exclude=self.path)
        self.lock, self.stop, self.refusal, self.errors, self.capped = threading.Lock(), threading.Event(), {}, [], ""

    def spent(self) -> float:
        return sum(v["cost"] for v in self.cache.values())

    def run(self, jobs, fn, workers=8):
        llm = _llm()

        def work(job):
            key = job[0]
            if key in self.cache or self.stop.is_set():
                return
            with self.lock:
                if self.spent() >= self.cap:
                    self.capped = f"run cap ${self.cap:.2f}"
                    self.stop.set()
                    return
                if self.other + self.spent() >= PROGRAM_CAP_USD:
                    self.capped = f"program cap ${PROGRAM_CAP_USD:.2f}"
                    self.stop.set()
                    return
            try:
                res = fn(job)
            except llm.RefusalError as e:
                self.refusal.setdefault("e", (key, e))
                self.stop.set()
                return
            except Exception as e:  # noqa: BLE001
                self.errors.append((key, repr(e)))
                self.stop.set()
                return
            with self.lock:
                self.cache[key] = res
                if len(self.cache) % 100 == 0:
                    self.path.write_text(json.dumps(self.cache))
                    print(f"{self.label}: {len(self.cache)} done, ${self.spent():.3f} "
                          f"(program ${self.other + self.spent():.3f})", flush=True)

        with ThreadPoolExecutor(max_workers=workers) as ex:
            list(ex.map(work, jobs))
        self.path.write_text(json.dumps(self.cache))
        if self.refusal:
            key, e = self.refusal["e"]
            (RESULTS / "refusal.md").write_text(
                f"# Run stopped on a refusal\n\n{self.label}, job `{key}`\n\nRefused call: **{e.call}**\n\n"
                f"Request ID: `{e.request_id}`\n\nStop details:\n\n```\n{e.stop_details}\n```\n\n"
                "Nothing was reworded or retried. No new call starts until Sean has seen this.\n")
            sys.exit(f"STOPPED on a refusal: {e}")
        if self.errors:
            sys.exit(f"{self.label}: stopped on an error: {self.errors[0]}")
        if self.stop.is_set():
            sys.exit(f"{self.label}: {self.capped or 'cap'} reached; stopped")
        print(f"{self.label}: complete, {len(self.cache)} cached calls, ${self.spent():.4f} "
              f"(program ${self.other + self.spent():.4f})", flush=True)


def call(messages, model, call_name, max_tokens=60, schema=None):
    """One call, thinking disabled (program 1's and 2's setting), default temperature.
    Returns (text or parsed JSON, cost, request id)."""
    llm = _llm()
    kw = {}
    if schema is not None:
        kw["output_config"] = {"format": {"type": "json_schema", "schema": schema}}
    resp = llm.client().messages.create(model=model, max_tokens=max_tokens, messages=messages,
                                        thinking={"type": "disabled"}, **kw)
    llm._check_stop(resp, call_name)
    text = "\n".join(b.text for b in resp.content if b.type == "text").strip()
    out = json.loads(text) if schema is not None else text
    return out, llm._usage(resp).cost, getattr(resp, "_request_id", None)


def int_schema(field="grade"):
    return {"type": "object", "properties": {field: {"type": "integer"}}, "required": [field],
            "additionalProperties": False}


def enum_schema(values, field="answer"):
    return {"type": "object", "properties": {field: {"type": "string", "enum": list(values)}}, "required": [field],
            "additionalProperties": False}

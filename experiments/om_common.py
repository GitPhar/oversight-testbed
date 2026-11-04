"""Shared pieces for program 2 (other-minds). Reuses program 1's instruments from /Users/seanpharris/entangled-mind:
the Anthropic client, refusal check and pricing (src/entangled_mind/llm.py, config.py), and the experiment-5 items
(experiments/exp5_run.py, results/pool-run-3.json, experiments/split-exp5.json).

Run every script with program 1's interpreter:  /Users/seanpharris/entangled-mind/.venv/bin/python experiments/<script>.py

The Caller below is program 1's gm_common.Caller with one change: a refusal is written to *this* repository's
results/refusal.md, not program 1's. Rules kept: a content-keyed JSON cache (a crash never pays twice), a budget cap
checked before every call, and a stop at the first refusal or error, with nothing reworded or retried."""

import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np

P1 = Path("/Users/seanpharris/entangled-mind")
ROOT = Path(__file__).resolve().parents[1]
RESULTS, EXPERIMENTS, DATA = ROOT / "results", ROOT / "experiments", ROOT / "data"
for p in (P1 / "src", P1 / "experiments"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

from dotenv import load_dotenv  # noqa: E402

from entangled_mind import llm  # noqa: E402

load_dotenv(P1 / ".env")
MODEL = "claude-haiku-5-5"
PLAIN = "## In plain English\n\n(Hand-written after the run.)\n"
SCALE = "0 = certainly false and 100 = certainly true"


class Caller:
    """Runs jobs through fn(job) -> result dict with a 'cost' field; caches by job[0]; stops at the cap or on any refusal."""

    def __init__(self, cache_path, cap_usd, label):
        self.path, self.cap, self.label = Path(cache_path), cap_usd, label
        self.cache = json.loads(self.path.read_text()) if self.path.exists() else {}
        self.lock, self.stop, self.refusal, self.errors = threading.Lock(), threading.Event(), {}, []

    def spent(self) -> float:
        return sum(v["cost"] for v in self.cache.values())

    def run(self, jobs, fn, workers=8):
        def work(job):
            key = job[0]
            if key in self.cache or self.stop.is_set():
                return
            with self.lock:
                if self.spent() >= self.cap:
                    self.stop.set()
                    return
            try:
                res = fn(job)
            except llm.RefusalError as e:
                self.refusal.setdefault("e", (key, e))
                self.stop.set()
                return
            except Exception as e:
                self.errors.append((key, repr(e)))
                self.stop.set()
                return
            with self.lock:
                self.cache[key] = res
                if len(self.cache) % 200 == 0:
                    self.path.write_text(json.dumps(self.cache))
                    print(f"{self.label}: {len(self.cache)} done, ${self.spent():.3f}", flush=True)

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
            sys.exit(f"{self.label}: budget cap ${self.cap} reached; stopped")
        print(f"{self.label}: complete, {len(self.cache)} cached calls, ${self.spent():.4f}", flush=True)


def structured(messages, schema, call, max_tokens=100, system=None, model=MODEL):
    """One structured-output call, thinking disabled (program 1's setting). Returns (parsed, cost, request id)."""
    kw = {"system": system} if system else {}
    resp = llm.client().messages.create(model=model, max_tokens=max_tokens, messages=messages,
                                        thinking={"type": "disabled"},
                                        output_config={"format": {"type": "json_schema", "schema": schema}}, **kw)
    llm._check_stop(resp, call)
    text = next(b.text for b in resp.content if b.type == "text")
    return json.loads(text), llm._usage(resp).cost, getattr(resp, "_request_id", None)


def int_schema(field="rating"):
    return {"type": "object", "properties": {field: {"type": "integer"}}, "required": [field], "additionalProperties": False}


def enum_schema(values, field="answer"):
    return {"type": "object", "properties": {field: {"type": "string", "enum": list(values)}}, "required": [field],
            "additionalProperties": False}


# --- statistics ------------------------------------------------------------------------------------------

def split_half_reliability(Y):
    """Y: items x repeats (NaN allowed). Spearman-Brown reliability of the item mean from the even/odd-repeat halves."""
    e, o = np.nanmean(Y[:, 0::2], 1), np.nanmean(Y[:, 1::2], 1)
    r = np.corrcoef(e, o)[0, 1]
    return 2 * r / (1 + r)


def q_ratio(Ya, Yb):
    """Item-level R^2 of framing a's item means predicting framing b's, divided by the product of the two
    split-half (Spearman-Brown) ceilings: the squared disattenuated correlation. 1 = interchangeable up to noise."""
    ma, mb = np.nanmean(Ya, 1), np.nanmean(Yb, 1)
    r = np.corrcoef(ma, mb)[0, 1]
    return r ** 2 / (split_half_reliability(Ya) * split_half_reliability(Yb))


def cluster_boot(stat, clusters, seed, n=2000):
    """Percentile 95% CI of stat(index array) resampling clusters (a list of index arrays) with replacement."""
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n):
        pick = rng.integers(0, len(clusters), len(clusters))
        vals.append(stat(np.concatenate([clusters[i] for i in pick])))
    vals = np.asarray(vals, float)
    return [float(np.nanpercentile(vals, 2.5)), float(np.nanpercentile(vals, 97.5))]

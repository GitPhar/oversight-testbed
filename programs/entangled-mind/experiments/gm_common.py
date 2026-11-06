"""Shared pieces for the overnight gold-map runs (D34-D39): the plain-English placeholder, AUROC
with bootstrap CIs, and a budget-capped, stop-on-refusal call wrapper with a JSON cache."""

import json
import sys
import threading
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from dotenv import load_dotenv

from entangled_mind import config, llm, readout

load_dotenv(config.ROOT / ".env")
PLAIN = "## In plain English\n\n(Hand-written after the run; excluded from reproduce.py's comparison.)\n"
ENGINE = __import__("pathlib").Path(__file__).resolve().parents[3]      # oversight-testbed

def _rule16(spent_usd=0.0):
    """Rule 16's dollar line (CONTEXT.md section 3; ledger/rule16.py): at most $15 of API a month without a landed
    partly-new or new result in the program's newest layer, or a steer from Sean; a closed program makes no paid
    call. Read only on a paid run (analyses never call it); refuses with SystemExit."""
    led = str(ENGINE / "ledger")
    if led not in sys.path:
        sys.path.insert(0, led)
    import rule16
    return rule16.DollarLine("entangled-mind", spent_usd, root=ENGINE)


def _guard_client(factory, spent_fn=lambda: 0.0):
    """The first paid client of a process passes rule 16's dollar line, so a script that calls llm.client() without
    this module's Caller is still checked at the start of its run."""
    if getattr(factory, "rule16_guarded", False):
        return factory
    seen = []

    def client(*a, **k):
        if not seen:
            _rule16(spent_fn())
            seen.append(True)
        return factory(*a, **k)

    client.rule16_guarded = True
    return client


llm.client = _guard_client(llm.client)



def auroc(pos, neg) -> float:
    return readout.auroc(list(map(float, pos)), list(map(float, neg)))


def boot_auroc(pos, neg, seed, n=2000):
    rng = np.random.default_rng(seed)
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    vals = [auroc(rng.choice(pos, len(pos)), rng.choice(neg, len(neg))) for _ in range(n)]
    return [auroc(pos, neg), *map(float, np.percentile(vals, [2.5, 97.5]))]


def paired_boot_auroc(sa, sb, y, seed, n=2000):
    """AUROC(sa) - AUROC(sb) on the same items, stratified resampling of positives and negatives."""
    rng = np.random.default_rng(seed)
    sa, sb, y = np.asarray(sa, float), np.asarray(sb, float), np.asarray(y, bool)
    P, N = np.where(y)[0], np.where(~y)[0]
    d = lambda p, q: auroc(sa[p], sa[q]) - auroc(sb[p], sb[q])
    vals = []
    for _ in range(n):
        p, q = rng.choice(P, len(P)), rng.choice(N, len(N))
        vals.append(d(p, q))
    return [d(P, N), *map(float, np.percentile(vals, [2.5, 97.5]))]


class Caller:
    """Runs jobs through fn(job) -> (result dict, cost); caches by key; stops at the cap or on any refusal."""

    def __init__(self, cache_path, cap_usd, label):
        self.path, self.cap, self.label = cache_path, cap_usd, label
        self.cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
        self.lock, self.stop, self.refusal, self.errors = threading.Lock(), threading.Event(), {}, []

    def spent(self) -> float:
        return sum(v["cost"] for v in self.cache.values())

    def run(self, jobs, fn, workers=6):
        line, base = _rule16(), self.spent()     # rule 16 (the ledger's month count), checked again before every call

        def work(job):
            key = job[0]
            if key in self.cache or self.stop.is_set():
                return
            with self.lock:
                if self.spent() >= self.cap:
                    self.stop.set()
                    return
                if line.blocks(self.spent() - base):
                    self.rule16_stop = line.message(line.start + self.spent() - base)
                    self.stop.set()
                    return
            try:
                res = fn(job)
            except llm.RefusalError as e:
                self.refusal.setdefault("e", (key, e))
                self.stop.set()
                return
            except Exception as e:      # any other failure stops the run; the cache is still saved (D36 amendment 2)
                self.errors.append((key, repr(e)))
                self.stop.set()
                return
            with self.lock:
                self.cache[key] = res
                if len(self.cache) % 50 == 0:
                    self.path.write_text(json.dumps(self.cache))
                    print(f"{self.label}: {len(self.cache)} done, ${self.spent():.3f}", flush=True)

        with ThreadPoolExecutor(max_workers=workers) as ex:
            list(ex.map(work, jobs))
        self.path.write_text(json.dumps(self.cache))
        if self.refusal:
            key, e = self.refusal["e"]
            (config.RESULTS / "refusal.md").write_text(
                f"# Pipeline stopped on a refusal\n\n{self.label}, job `{key}`\n\nRefused call: **{e.call}**\n\n"
                f"Request ID: `{e.request_id}`\n\nExact stop details:\n\n```\n{e.stop_details}\n```\n\n"
                "Nothing was reworded or retried.\n")
            sys.exit(f"STOPPED on a refusal: {e}")
        if self.errors:
            sys.exit(f"{self.label}: stopped on an error: {self.errors[0]}")
        if getattr(self, "rule16_stop", None):
            sys.exit(self.rule16_stop)
        if self.stop.is_set():
            sys.exit(f"{self.label}: budget cap ${self.cap} reached; stopped")


def structured(model, messages, schema, call, max_tokens=300, thinking_off=True, system=None):
    """One structured-output call; returns (parsed dict, raw text, cost, request id)."""
    kw = {"thinking": {"type": "disabled"}} if thinking_off else {}
    if system:
        kw["system"] = system
    resp = llm.client().messages.create(model=model, max_tokens=max_tokens, messages=messages,
                                        output_config={"format": {"type": "json_schema", "schema": schema}}, **kw)
    llm._check_stop(resp, call)
    text = next(b.text for b in resp.content if b.type == "text")
    return json.loads(text), text, llm._usage(resp).cost, getattr(resp, "_request_id", None)

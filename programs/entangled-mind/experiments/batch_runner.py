"""Batches API runner with worst-case cap chunks, a content-hashed cache, crash recovery and stop-on-refusal.

Written for em-dm6f2f2f2 (design review fix 6, D96) and used by em-dm6f2f2f1 after its review. It replaces the
crash path of dm6f2f2_own_guess.run(), which counted a crashed batch's cost as lost and resubmitted its requests
without looking for a refusal in it (review ledger/design-reviews/em-dm6f2f2f2.md, D10).

    run_questions(client, todo, ...)   todo = [ {key: (model, text, params, sha)} per whole question ], in run order

The batch log entry is written before polling and carries the custom_id -> key map, each key's request sha and its
model. On start-up, recover() collects every logged batch with no recorded end and stores its results in the cache
exactly as a normal batch does, with the refusal stop applied. A key whose cached result is a refusal is never
resubmitted, and while the refusal record exists nothing runs.
"""
import json
import sys
import time


def cost_of(msg, prices, discount):
    pin, pout = prices[msg.model] if msg.model in prices else max(prices.values())
    return discount * (msg.usage.input_tokens * pin + msg.usage.output_tokens * pout) / 1e6


def store(client, entry, cache, prices, discount, parse):
    """Store one ended batch's results in the cache. Returns (refusal or None, errored keys)."""
    refusal, errored = None, []
    for res in client.messages.batches.results(entry["batch"]):
        k = entry["idmap"][res.custom_id]
        if res.result.type != "succeeded":
            errored.append(k)
            continue
        msg = res.result.message
        cost = cost_of(msg, prices, discount)
        sha = entry["sha"][k]
        if msg.stop_reason == "refusal":
            refusal = refusal or (k, msg, entry["batch"])
            cache[k] = {"raw": None, "guess": None, "conf": None, "refused": True, "cost": cost, "msg_id": msg.id, "sha": sha,
                        "batch": entry["batch"]}
            continue
        text = "".join(x.text for x in msg.content if x.type == "text")
        gs, c = (None, None) if msg.stop_reason == "max_tokens" else parse(text, k)
        cache[k] = {"raw": text, "guess": gs, "conf": c, "stop": msg.stop_reason, "cost": cost, "msg_id": msg.id,
                    "batch": entry["batch"], "sha": sha, "in_tok": msg.usage.input_tokens, "out_tok": msg.usage.output_tokens}
    return refusal, errored


def write_refusal(path, label, refusal):
    k, msg, bid = refusal
    path.write_text(f"# {label} stopped on a refusal\n\nJob `{k}`, model `{msg.model}`, batch `{bid}`, message `{msg.id}`\n\n"
                    f"```\n{getattr(msg, 'stop_details', None)}\n```\n\nNothing was reworded or retried; no further batch was submitted.\n")


def wait(client, bid, poll):
    b = client.messages.batches.retrieve(bid)
    while b.processing_status != "ended":
        time.sleep(poll)
        b = client.messages.batches.retrieve(bid)
    return b


def reconcile(client, e):
    """A 'submitting' marker with no batch ID: the process died between batches.create and saving its ID. Find the
    batch among the account's recent batches (created at or after the marker, same request count); exactly one match is
    adopted, anything else stops the run."""
    t0 = e["marker_at"]
    hits = [b for b in client.messages.batches.list(limit=50)
            if getattr(b, "created_at_unix", None) is not None and b.created_at_unix >= t0 - 1
            and getattr(b, "request_total", None) == e["n"]]
    if len(hits) != 1:
        sys.exit(f"batch log holds a submission marker with no batch ID and {len(hits)} candidate batches; stopped for a "
                 "person to reconcile (nothing resubmitted)")
    e["batch"] = hits[0].id
    e["reconciled"] = True


def recover(client, blog, cache, save, prices, discount, parse, refusal_path, label, poll=20):
    for e in blog:
        if e.get("ended"):
            continue
        if not e.get("batch"):
            reconcile(client, e)
            save()
        wait(client, e["batch"], poll)
        refusal, _ = store(client, e, cache, prices, discount, parse)
        e.update(ended=True, collected_after_crash=True)
        save()
        if refusal:
            write_refusal(refusal_path, label, refusal)
            sys.exit(f"STOPPED on a refusal found in a crashed batch: {refusal[0]} {refusal[1].id}")


def submit(client, part, blog, save, cache, prices, discount, parse, refusal_path, label, worst, nq, poll=20):
    """part = {key: (params, sha)}. Up to two unchanged resubmissions of errored (never refused) requests."""
    for attempt in range(3):
        idmap = {f"r{n}": k for n, k in enumerate(part)}
        entry = {"batch": None, "n": len(part), "questions": nq, "worst_case": round(worst, 4), "ended": False,
                 "idmap": idmap, "sha": {k: part[k][1] for k in part}, "marker_at": time.time()}
        blog.append(entry)
        save()                                           # the submission marker and key map are on disk before create
        b = client.messages.batches.create(requests=[{"custom_id": c, "params": part[k][0]} for c, k in idmap.items()])
        entry["batch"] = b.id
        save()                                           # the batch ID is on disk before polling
        print(f"{label}: batch {b.id}, {len(part)} requests ({nq} questions), worst case ${worst:.4f}", flush=True)
        t0 = time.time()
        wait(client, b.id, poll)
        refusal, errored = store(client, entry, cache, prices, discount, parse)
        entry.update(ended=True, seconds=round(time.time() - t0))
        save()
        if refusal:
            write_refusal(refusal_path, label, refusal)
            sys.exit(f"STOPPED on a refusal: {refusal[0]} {refusal[1].id}")
        if not errored:
            return
        part = {k: part[k] for k in errored}
    sys.exit(f"{label}: requests still failing after two resubmissions; stopped")


def run_questions(client, todo, cache, blog, save, cap, reserve, worst_cost, prices, discount, parse, refusal_path, label,
                  spent, poll=20):
    """todo: list of {key: (params, sha, text)} per whole question, in run order. Chunks hold as many whole questions as
    fit under cap - spent() - reserve at their worst case; a question that does not fit is not run."""
    if refusal_path.exists() or any(v.get("refused") for v in cache.values() if isinstance(v, dict)):
        sys.exit(f"{label}: a refusal is on record; a refused run is never resumed, reworded or retried")
    recover(client, blog, cache, save, prices, discount, parse, refusal_path, label, poll)
    todo = [{k: v for k, v in q.items() if k not in cache} for q in todo]
    todo = [q for q in todo if q]
    not_run = 0
    while todo:
        head = cap - spent() - reserve
        chunk, w = [], 0.0
        for q in todo:
            wq = sum(worst_cost(v[2]) for v in q.values())
            if w + wq > head + 1e-12:
                break
            chunk.append(q)
            w += wq
        if not chunk:
            not_run = len(todo)
            print(f"{label}: {not_run} question(s) not run: spent ${spent():.4f}; the next question's worst case would not fit "
                  f"the ${cap} cap", flush=True)
            break
        todo = todo[len(chunk):]
        part = {k: (v[0], v[1]) for q in chunk for k, v in q.items()}
        submit(client, part, blog, save, cache, prices, discount, parse, refusal_path, label, w, len(chunk), poll)
        print(f"{label}: chunk done, ${spent():.4f}", flush=True)
    save()
    print(f"{label}: finished, ${spent():.4f}")
    return not_run


# --- a fake Batches client for selftests (no network) ---------------------------------------------------------------------

class _NS:
    def __init__(self, **kw):
        self.__dict__.update(kw)


class FakeBatches:
    """Replies 'Guess: <g>\\n Probability: <c>' (or Frequency) for every request; `refuse` holds substrings of request
    text whose reply is a refusal; `crash_after_create` raises on the first poll of the n-th batch."""
    def __init__(self, reply, cost_tokens=(200, 60), refuse=(), crash_on=None, crash_in_create=None):
        self.reply, self.tok, self.refuse, self.crash_on, self.crash_in_create = reply, cost_tokens, refuse, crash_on, crash_in_create
        self.batches, self.created, self.polls, self.made = {}, 0, {}, {}

    def create(self, requests):
        self.created += 1
        bid = f"fake_{self.created}"
        self.batches[bid] = requests
        self.polls[bid] = 0
        self.made[bid] = time.time()
        if self.crash_in_create is not None and self.created == self.crash_in_create:
            self.crash_in_create = None
            raise RuntimeError("simulated crash after the batch was created, before its ID was saved")
        return _NS(id=bid, processing_status="in_progress")

    def list(self, limit=50):
        return [_NS(id=b, created_at_unix=self.made[b], request_total=len(r)) for b, r in self.batches.items()][-limit:]

    def retrieve(self, bid):
        self.polls[bid] += 1
        if self.crash_on is not None and int(bid.split("_")[1]) == self.crash_on and self.polls[bid] == 1:
            self.crash_on = None
            raise RuntimeError("simulated crash while polling")
        return _NS(id=bid, processing_status="ended")

    def results(self, bid):
        for r in self.batches[bid]:
            text = r["params"]["messages"][0]["content"]
            refused = any(s in text for s in self.refuse)
            msg = _NS(id=f"msg_{bid}_{r['custom_id']}", model=r["params"]["model"],
                      stop_reason="refusal" if refused else "end_turn",
                      content=[] if refused else [_NS(type="text", text=self.reply(r["params"]))],
                      usage=_NS(input_tokens=self.tok[0], output_tokens=self.tok[1]), stop_details=None)
            yield _NS(custom_id=r["custom_id"], result=_NS(type="succeeded", message=msg))


class FakeClient:
    def __init__(self, batches):
        self.messages = _NS(batches=batches)


def real_list_adapter(client):
    """Wrap the real SDK so batches.list() exposes created_at_unix and request_total like the fake."""
    inner = client.messages.batches

    class _B:
        def __getattr__(self, n):
            return getattr(inner, n)

        def list(self, limit=50):
            out = []
            for b in inner.list(limit=limit):
                rc = b.request_counts
                total = sum(getattr(rc, f, 0) or 0 for f in ("processing", "succeeded", "errored", "canceled", "expired"))
                out.append(_NS(id=b.id, created_at_unix=b.created_at.timestamp(), request_total=total))
            return out
    return _NS(messages=_NS(batches=_B()))


def dumps(x):
    return json.dumps(x)

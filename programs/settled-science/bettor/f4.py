"""ss-b12 (experiments/ss-b12.md; direction ss-f4): pre-cutoff template items for the recognition split.

The round-2 template writer (protocol/template-writer.md, items/template_writer.py: no model writes any item) applied to
PRE-cutoff papers from the same four arXiv queries, then the round-2 leakage drop (claude-sonnet-5-5, items/leakcheck.py
prompt, flagged -> dropped, never rewritten), then the round-2 bettor (claude-opus-5-5, bettor.py SYSTEM, effort low).
The post-cutoff side is round 2's archive (92 items, ss-b5's primary bets); nothing new is asked on it.

    python3 bettor/f4.py --fetch      # 12 arXiv API requests (4 queries x 3 windows, 100 each) -> items/f4/pool.json
    python3 bettor/f4.py --build      # template -> items/f4/candidates.jsonl (+ build-log.json); answer-free
    python bettor/f4.py --sample      # beacon sub-seed `items`: up to 30 candidates per field -> items/f4/sample.jsonl
    python bettor/f4.py --leak        # leakage check on the sample (Sonnet) -> items/f4/leakage-*.json(l)
    python bettor/f4.py --freeze      # clean sample items -> items/f4/items.jsonl, masked.jsonl, SHA256SUMS
    python bettor/f4.py --bet         # Opus bettor, primary only, beacon sub-seed `order` -> bettor/f4-bets.jsonl
    python bettor/f4.py --dry-run     # prints the plan and a cost estimate; no call, no fetch
Caps (both checked before every call, common.Caller): this bet's $0.75 (BET_CAP, budget ruling br-005) across its two
caches, and the program cap (common.BUDGET_USD). Stop on any refusal.
"""
import json
import random
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "items"))
import template_writer as T  # noqa: E402
import verify  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
F4 = ROOT / "items" / "f4"
SEED = ROOT / "bettor" / "f4-seed.json"
LEAK_CACHE = F4 / "leakage-cache.json"
BET_CACHE = ROOT / "bettor" / "f4-bettor-cache.json"
BETS_OUT = ROOT / "bettor" / "f4-bets.jsonl"
BET_CAP = 0.75
STATUS = ROOT / "bettor" / "f4-run-status.json"   # D57 F4: {"leak": ..., "bet": ...}: complete | cap | refusal | error


def set_status(step, value, detail=""):
    st = json.loads(STATUS.read_text()) if STATUS.exists() else {}
    st[step] = value
    if detail:
        st["detail"] = detail
    STATUS.write_text(json.dumps(st, indent=1) + "\n")


def run_caller(c, jobs, fn, step):
    """Run, then record how the step ended: a refusal or error makes the bet untestable (D57 F4)."""
    try:
        c.run(jobs, fn)
        set_status(step, "complete")
    except SystemExit as e:
        msg = str(e)
        kind = "refusal" if "refusal" in msg.lower() else "cap" if "budget cap" in msg else "error"
        set_status(step, kind, msg[:300])
        raise
PER_FIELD = 30
WINDOWS = [("2024", "submittedDate:[202401010000 TO 202412312359]"),
           ("2025", "submittedDate:[202501010000 TO 202512312359]"),
           ("2026H1", "submittedDate:[202601010000 TO 202606302359]")]
PER_REQUEST = 100
CUTOFF = "2026-07-01"


def fetch():
    F4.mkdir(parents=True, exist_ok=True)
    pool = {}
    for field, q in T.QUERIES:
        for win, date in WINDOWS:
            url = ("https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
                {"search_query": f"({q}) AND {date}", "sortBy": "submittedDate", "sortOrder": "descending",
                 "start": 0, "max_results": PER_REQUEST}))
            for attempt in range(6):
                try:
                    xml = urllib.request.urlopen(url, timeout=120).read()
                    break
                except Exception as e:  # noqa: BLE001
                    print("arXiv retry", attempt, e, file=sys.stderr)
                    time.sleep(30 * (attempt + 1))
            else:
                sys.exit("arXiv unreachable")
            got = []
            for e in ET.fromstring(xml).findall("a:entry", T.NS):
                if e.find("a:title", T.NS) is None:
                    continue
                aid = re.sub(r"v\d+$", "", e.find("a:id", T.NS).text.rsplit("/abs/", 1)[-1])
                got.append({"id": aid, "title": re.sub(r"\s+", " ", e.find("a:title", T.NS).text).strip(),
                            "summary": re.sub(r"\s+", " ", e.find("a:summary", T.NS).text).strip(),
                            "published": e.find("a:published", T.NS).text[:10], "window": win,
                            "comment": (e.find("arxiv:comment", T.NS).text if e.find("arxiv:comment", T.NS) is not None else ""),
                            "authors": [a.find("a:name", T.NS).text for a in e.findall("a:author", T.NS)]})
            pool.setdefault(field, []).extend(got)
            print(field, win, len(got), "papers", flush=True)
            time.sleep(5)
    (F4 / "pool.json").write_text(json.dumps({"queries": T.QUERIES, "windows": WINDOWS, "per_request": PER_REQUEST,
                                               "fetched": time.strftime("%Y-%m-%d %H:%M %Z"), "pool": pool}, indent=1))


def build():
    pool = json.loads((F4 / "pool.json").read_text())["pool"]
    used = set()
    for p in (ROOT / "items" / "drafts").glob("*.jsonl"):
        used |= {json.loads(l)["arxiv_id"].strip() for l in p.read_text().splitlines() if l.strip()}
    for p in (ROOT / "items" / "r2" / "candidates.jsonl", ROOT / "items" / "items.jsonl"):
        used |= {json.loads(l)["arxiv_id"].strip() for l in p.read_text().splitlines() if l.strip()}
    seen, out, log = set(), [], []
    for field, _ in T.QUERIES:
        for p in pool[field]:
            why = ("duplicate across fields" if p["id"] in seen else "in round 1 or round 2" if p["id"] in used else
                   "v1 on or after 2026-07-01" if p["published"] >= CUTOFF else None)
            seen.add(p["id"])
            if why:
                log.append({"id": p["id"], "field": field, "dropped": why})
                continue
            it = T.item_from(p, field)
            if it is None:
                log.append({"id": p["id"], "field": field, "dropped": "no candidate sentence"})
                continue
            it["v1_date"], it["side"], it["window"] = p["published"], "pre", p["window"]
            errs, _ = verify.check(it, {p["id"]: {"title": p["title"], "summary": p["summary"], "published": p["published"]}})
            errs = [e for e in errs if not e.startswith("options not parallel")]   # as round 2 (template_writer.build)
            if errs:
                log.append({"id": p["id"], "field": field, "dropped": "verify: " + "; ".join(errs)})
                continue
            it["cid"] = f"t4-{p['id']}"
            out.append(it)
    (F4 / "candidates.jsonl").write_text("".join(json.dumps(i) + "\n" for i in out))
    (F4 / "build-log.json").write_text(json.dumps(log, indent=1))
    from collections import Counter
    print(len(out), "template items;", Counter(i["field"] for i in out), Counter(i["window"] for i in out))
    print("dropped:", Counter(x["dropped"].split(":")[0] for x in log))


def seeds():
    return json.loads(SEED.read_text())["seeds"]


def sample():
    cands = sorted((json.loads(l) for l in (F4 / "candidates.jsonl").read_text().splitlines() if l.strip()), key=lambda c: c["cid"])
    rng, keep = random.Random(seeds()["items"]), set()
    for f, _ in T.QUERIES:
        pool = sorted(c["cid"] for c in cands if c["field"] == f)
        keep |= set(rng.sample(pool, PER_FIELD) if len(pool) > PER_FIELD else pool)
    s = [c for c in cands if c["cid"] in keep]
    (F4 / "sample.jsonl").write_text("".join(json.dumps(c) + "\n" for c in s))
    from collections import Counter
    print(len(s), "sampled", Counter(c["field"] for c in s))


def own_spent():
    tot = 0.0
    for c in (LEAK_CACHE, BET_CACHE):
        if c.exists():
            tot += sum(v["cost"] for v in json.loads(c.read_text()).values())
    return tot


def cap():
    from common import BUDGET_USD, spent_total
    return min(BUDGET_USD, spent_total() - own_spent() + BET_CAP)   # Caller's spent() = others + this cache's own


def leak():
    from common import Caller, structured
    import leakcheck as LC
    s = [json.loads(l) for l in (F4 / "sample.jsonl").read_text().splitlines() if l.strip()]
    jobs = [{"key": LC.version_key(it), "it": it} for it in s]

    def fn(job):
        out, cost, rid, usage = structured(LC.MODEL, LC.SYSTEM, LC.user_text(job["it"]), LC.SCHEMA, "leakage-check", max_tokens=500)
        return {"cid": job["it"]["cid"], "leak": out["leak"], "cue": out["cue"], "fix": out["fix"],
                "cost": cost, "request_id": rid, "usage": usage, "model": LC.MODEL}
    c = Caller(LEAK_CACHE, "f4-leakage-check", cap=cap())
    try:
        run_caller(c, jobs, fn, "leak")
    finally:
        rows = [{"key": j["key"], **{k: v for k, v in c.cache[j["key"]].items() if k not in ("usage",)},
                 "item": {k: j["it"][k] for k in LC.MASKED_FIELDS}} for j in jobs if j["key"] in c.cache]
        (F4 / "leakage-log.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        st = {j["it"]["cid"]: ("unchecked" if j["key"] not in c.cache else "dropped" if c.cache[j["key"]]["leak"] else "clean") for j in jobs}
        (F4 / "leakage-status.json").write_text(json.dumps(st, indent=1, sort_keys=True))
        from collections import Counter
        print(Counter(st.values()))


def freeze():
    import hashlib
    st = json.loads((F4 / "leakage-status.json").read_text())
    if "unchecked" in st.values():
        sys.exit("unchecked items remain: the leakage check did not finish, so nothing is frozen (§7)")
    order = {f: i for i, (f, _) in enumerate(T.QUERIES)}
    keep = sorted((c for c in (json.loads(l) for l in (F4 / "sample.jsonl").read_text().splitlines() if l.strip())
                   if st.get(c["cid"]) == "clean"), key=lambda c: (order[c["field"]], c["arxiv_id"]))
    for n, c in enumerate(keep, 1):
        c["id"], c["leakage_status"] = f"f4-{n:03d}", "clean"
    full = "".join(json.dumps({"id": c["id"], **{k: v for k, v in c.items() if k != "id"}}) + "\n" for c in keep)
    masked = "".join(json.dumps({k: c[k] for k in ("id", "field", "question", "methods", "option_a", "option_b")}) + "\n" for c in keep)
    (F4 / "items.jsonl").write_text(full)
    (F4 / "masked.jsonl").write_text(masked)
    (F4 / "SHA256SUMS").write_text("".join(f"{hashlib.sha256(t.encode()).hexdigest()}  items/f4/{n}\n"
                                           for n, t in (("items.jsonl", full), ("masked.jsonl", masked))))
    from collections import Counter
    print(len(keep), "clean pre-cutoff items", Counter(c["field"] for c in keep), Counter(c["window"] for c in keep))


def bet():
    from common import Caller, key_of, structured
    import bettor as B
    items = sorted((json.loads(l) for l in (F4 / "masked.jsonl").read_text().splitlines() if l.strip()), key=lambda x: x["id"])
    if len(items) < 30:
        sys.exit(f"{len(items)} clean pre-cutoff items < 30: untestable before any bettor call (§5)")
    rng = random.Random(seeds()["order"])
    swap = {it["id"]: rng.random() < 0.5 for it in items}
    jobs = []   # D57 F4: after the order draw, the same rng shuffles the job order, so a cap stop drops a random subset
    for it in items:
        u = B.user_text(it, swap[it["id"]])
        jobs.append({"key": key_of("bettor-v1", B.MODEL, B.SYSTEM, u), "id": it["id"], "kind": "primary",
                     "option_1_is": "b" if swap[it["id"]] else "a", "user": u})
    rng.shuffle(jobs)

    def fn(job):
        out, cost, rid, usage = structured(B.MODEL, B.SYSTEM, job["user"], B.SCHEMA, "bettor", max_tokens=4000)
        return {"id": job["id"], "kind": job["kind"], "option_1_is": job["option_1_is"], "p_option_1": out["p_option_1"],
                "rationale": out["rationale"], "cost": cost, "request_id": rid, "usage": usage, "model": B.MODEL}
    c = Caller(BET_CACHE, "f4-bettor", cap=cap())
    try:
        run_caller(c, jobs, fn, "bet")
    finally:
        rows = [c.cache[j["key"]] for j in jobs if j["key"] in c.cache]
        BETS_OUT.write_text("".join(json.dumps(r) + "\n" for r in rows))
        print(f"wrote {len(rows)} bets to {BETS_OUT.relative_to(ROOT)}")


def dry():
    print(f"plan: 12 arXiv requests ({len(T.QUERIES)} queries x {len(WINDOWS)} windows x {PER_REQUEST}); template; sample <= "
          f"{PER_FIELD}/field; leakage check (Sonnet, about $0.003 each, <= {4 * PER_FIELD} calls, about ${0.003 * 4 * PER_FIELD:.2f}); "
          f"Opus bettor on the clean ones (about $0.0048 each; at round 2's keep rate of 40-44% and its per-field yields, about 44 "
          f"clean and about 38 unrecognised items (design review ss-b12, measured-world table), about $0.21); bet cap ${BET_CAP}")
    print("selftest of the template writer:"); T.selftest()


if __name__ == "__main__":
    {"--fetch": fetch, "--build": build, "--sample": sample, "--leak": leak, "--freeze": freeze, "--bet": bet,
     "--dry-run": dry}[sys.argv[1]]()

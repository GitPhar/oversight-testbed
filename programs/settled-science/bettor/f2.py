"""ss-b14 (experiments/ss-b14.md; direction ss-f2): 60 more post-cutoff model-psychology findings, written by the round-2
template writer (protocol/template-writer.md, items/template_writer.py: no model writes, edits, picks or rewrites an item),
then the round-2 leakage drop (claude-sonnet-5-5, items/leakcheck.py prompt; flagged -> dropped, never rewritten), then the
bettor on three models (bettor.py SYSTEM and user_text, unchanged) and the ss-b6 flattery rater (valence.py SYSTEM,
unchanged, claude-opus-5-5) as a comparator.

    python3 bettor/f2.py --fetch      # 4 arXiv API requests: round 2's model-psychology query and window, results 600-1799
    python3 bettor/f2.py --build      # template -> items/f2/candidates.jsonl (+ build-log.json); answer-free
    python bettor/f2.py --order       # beacon sub-seed `items`: a fixed order of the candidates -> items/f2/order.json
    python bettor/f2.py --leak        # leakage check, batch 1 (the first 120 in that order), batch 2 only if needed (§2)
    python bettor/f2.py --freeze      # the first 60 clean in that order -> items/f2/items.jsonl, masked.jsonl, SHA256SUMS
    python bettor/f2.py --bet         # Opus bettor, Opus flattery rater, Sonnet bettor, Haiku bettor (§3 order)
    python bettor/f2.py --dry-run     # plan and cost estimate; no call, no fetch
Caps (both checked before every call, common.Caller): this bet's BET_CAP (budget ruling br-008) across its two caches,
and the program cap (common.BUDGET_USD). Stop on any refusal or error; every step records how it ended in
bettor/f2-run-status.json (a refusal or error at any step makes the bet untestable).
"""
import datetime
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
F2 = ROOT / "items" / "f2"
SEED = ROOT / "bettor" / "f2-seed.json"
LEAK_CACHE = F2 / "leakage-cache.json"
BET_CACHE = ROOT / "bettor" / "f2-cache.json"
BETS_OUT = ROOT / "bettor" / "f2-bets.jsonl"
STATUS = ROOT / "bettor" / "f2-run-status.json"
BET_CAP = 1.25          # budget ruling br-008 (ledger/spend.jsonl)
FIELD = "model-psychology"
QUERY = dict(T.QUERIES)[FIELD]
DATE = T.DATE           # round 2's window, unchanged: submitted 2026-07-01 00:00 to 2026-11-04 23:59
STARTS = (600, 900, 1200, 1500)   # round 2 fetched results 0-599 of this query; these are the next 1,200
PER_REQUEST = 300
BATCH1, BATCH2 = 120, 40
TARGET, MIN_ITEMS = 60, 50
CUTOFF = "2026-07-01"
BETTORS = ("claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5")
RATER = "claude-opus-5-5"


def set_status(step, value, detail=""):
    st = json.loads(STATUS.read_text()) if STATUS.exists() else {}
    st[step] = value
    if detail:
        st[f"{step}_detail"] = detail
    STATUS.write_text(json.dumps(st, indent=1) + "\n")


def run_caller(c, jobs, fn, step):
    try:
        c.run(jobs, fn)
        set_status(step, "complete")
    except SystemExit as e:
        msg = str(e)
        kind = "refusal" if "refusal" in msg.lower() else "cap" if "budget cap" in msg else "error"
        set_status(step, kind, msg[:300])
        raise


def fetch():
    F2.mkdir(parents=True, exist_ok=True)
    got = []
    for start in STARTS:
        url = ("https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
            {"search_query": f"({QUERY}) AND {DATE}", "sortBy": "submittedDate", "sortOrder": "descending",
             "start": start, "max_results": PER_REQUEST}))
        for attempt in range(6):
            try:
                xml = urllib.request.urlopen(url, timeout=120).read()
                break
            except Exception as e:  # noqa: BLE001
                print("arXiv retry", attempt, e, file=sys.stderr)
                time.sleep(30 * (attempt + 1))
        else:
            sys.exit("arXiv unreachable")
        page = []
        for e in ET.fromstring(xml).findall("a:entry", T.NS):
            if e.find("a:title", T.NS) is None:
                continue
            aid = re.sub(r"v\d+$", "", e.find("a:id", T.NS).text.rsplit("/abs/", 1)[-1])
            page.append({"id": aid, "title": re.sub(r"\s+", " ", e.find("a:title", T.NS).text).strip(),
                         "summary": re.sub(r"\s+", " ", e.find("a:summary", T.NS).text).strip(),
                         "published": e.find("a:published", T.NS).text[:10], "start": start,
                         "comment": (e.find("arxiv:comment", T.NS).text if e.find("arxiv:comment", T.NS) is not None else ""),
                         "authors": [a.find("a:name", T.NS).text for a in e.findall("a:author", T.NS)]})
        got.extend(page)
        print(FIELD, "start", start, len(page), "papers", flush=True)
        time.sleep(5)
    (F2 / "pool.json").write_text(json.dumps({"query": QUERY, "date": DATE, "starts": STARTS, "per_request": PER_REQUEST,
                                               "fetched": time.strftime("%Y-%m-%d %H:%M %Z"), "pool": got}, indent=1))


def used_ids():
    """Every arXiv id already in the program: round 1 drafts, round 2's fetched pool (all 600 per field), ss-b12's pool."""
    used = set()
    for p in (ROOT / "items" / "drafts").glob("*.jsonl"):
        used |= {json.loads(l)["arxiv_id"].strip() for l in p.read_text().splitlines() if l.strip()}
    for pool in (ROOT / "items" / "r2" / "pool.json", ROOT / "items" / "f4" / "pool.json"):
        for papers in json.loads(pool.read_text())["pool"].values():
            used |= {p["id"] for p in papers}
    return used


def build():
    pool = json.loads((F2 / "pool.json").read_text())["pool"]
    used = used_ids()
    seen, out, log = set(), [], []
    for p in pool:
        why = ("duplicate" if p["id"] in seen else "already in the program" if p["id"] in used else
               "v1 before 2026-07-01" if p["published"] < CUTOFF else
               "ICML 2026 / TMLR comment" if re.search(r"ICML 2026|TMLR|Transactions on Machine Learning Research", p["comment"] or "") else None)
        seen.add(p["id"])
        if why:
            log.append({"id": p["id"], "dropped": why})
            continue
        it = T.item_from(p, FIELD)
        if it is None:
            log.append({"id": p["id"], "dropped": "no candidate sentence"})
            continue
        it["v1_date"], it["side"] = p["published"], "post"
        errs, _ = verify.check(it, {p["id"]: {"title": p["title"], "summary": p["summary"], "published": p["published"]}})
        errs = [e for e in errs if not e.startswith("options not parallel")]   # as round 2 (template_writer.build)
        if errs:
            log.append({"id": p["id"], "dropped": "verify: " + "; ".join(errs)})
            continue
        it["cid"] = f"t2-{p['id']}"
        out.append(it)
    (F2 / "candidates.jsonl").write_text("".join(json.dumps(i) + "\n" for i in out))
    (F2 / "build-log.json").write_text(json.dumps(log, indent=1))
    from collections import Counter
    print(len(out), "template items from", len(pool), "papers; dropped:", Counter(x["dropped"].split(":")[0] for x in log))


def seeds():
    return json.loads(SEED.read_text())["seeds"]


def cands():
    return {c["cid"]: c for c in (json.loads(l) for l in (F2 / "candidates.jsonl").read_text().splitlines() if l.strip())}


def order():
    """One fixed order of every candidate, from the beacon sub-seed `items` (sorted cids, then shuffled)."""
    cids = sorted(cands())
    random.Random(seeds()["items"]).shuffle(cids)
    (F2 / "order.json").write_text(json.dumps(cids, indent=0) + "\n")
    print(len(cids), "candidates ordered")


def own_spent():
    return sum(sum(v["cost"] for v in json.loads(c.read_text()).values()) for c in (LEAK_CACHE, BET_CACHE) if c.exists())


def cap():
    from common import BUDGET_USD, spent_total
    return min(BUDGET_USD, spent_total() - own_spent() + BET_CAP)


def leak_status(cs, ordered, cache):
    import leakcheck as LC
    return {cid: ("unchecked" if LC.version_key(cs[cid]) not in cache else
                  "dropped" if cache[LC.version_key(cs[cid])]["leak"] else "clean") for cid in ordered}


def leak():
    from common import Caller, structured
    import leakcheck as LC
    cs, ordered = cands(), json.loads((F2 / "order.json").read_text())

    def fn(job):
        out, cost, rid, usage = structured(LC.MODEL, LC.SYSTEM, LC.user_text(job["it"]), LC.SCHEMA, "leakage-check", max_tokens=500)
        return {"cid": job["it"]["cid"], "leak": out["leak"], "cue": out["cue"], "fix": out["fix"],
                "cost": cost, "request_id": rid, "usage": usage, "model": LC.MODEL}
    batches = [ordered[:BATCH1], ordered[BATCH1:BATCH1 + BATCH2]]
    c = None
    try:
        for b, ids in enumerate(batches, 1):
            if b == 2:   # batch 2 only if batch 1 left fewer than TARGET clean items (§2)
                st = leak_status(cs, ordered[:BATCH1], c.cache)
                if sum(v == "clean" for v in st.values()) >= TARGET or not ids:
                    break
            c = Caller(LEAK_CACHE, f"f2-leakage-check batch {b}", cap=cap())
            run_caller(c, [{"key": LC.version_key(cs[i]), "it": cs[i]} for i in ids], fn, "leak")
    finally:
        cache = json.loads(LEAK_CACHE.read_text()) if LEAK_CACHE.exists() else {}
        checked = [i for i in ordered if LC.version_key(cs[i]) in cache]
        rows = [{"key": LC.version_key(cs[i]), **{k: v for k, v in cache[LC.version_key(cs[i])].items() if k != "usage"},
                 "item": {k: cs[i][k] for k in LC.MASKED_FIELDS}} for i in checked]
        (F2 / "leakage-log.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
        st = leak_status(cs, ordered, cache)
        (F2 / "leakage-status.json").write_text(json.dumps(st, indent=1, sort_keys=True) + "\n")
        from collections import Counter
        print(Counter(st.values()))


def freeze():
    import hashlib
    import leakcheck as LC  # noqa: F401
    run = json.loads(STATUS.read_text()) if STATUS.exists() else {}
    if run.get("leak") != "complete":
        sys.exit("the leakage check did not complete: nothing is frozen and the bet is untestable (§7)")
    cs, ordered = cands(), json.loads((F2 / "order.json").read_text())
    st = json.loads((F2 / "leakage-status.json").read_text())
    clean = [i for i in ordered if st.get(i) == "clean"][:TARGET]
    if len(clean) < MIN_ITEMS:
        sys.exit(f"{len(clean)} clean items < {MIN_ITEMS}: no bettor call; the bet is untestable (§5)")
    keep = sorted((cs[i] for i in clean), key=lambda c: c["arxiv_id"])
    for n, c in enumerate(keep, 1):
        c["id"], c["leakage_status"] = f"f2-{n:03d}", "clean"
    full = "".join(json.dumps({"id": c["id"], **{k: v for k, v in c.items() if k != "id"}}) + "\n" for c in keep)
    masked = "".join(json.dumps({k: c[k] for k in ("id", "field", "question", "methods", "option_a", "option_b")}) + "\n" for c in keep)
    (F2 / "items.jsonl").write_text(full)
    (F2 / "masked.jsonl").write_text(masked)
    (F2 / "SHA256SUMS").write_text("".join(f"{hashlib.sha256(t.encode()).hexdigest()}  items/f2/{n}\n"
                                           for n, t in (("items.jsonl", full), ("masked.jsonl", masked))))
    print(len(keep), "clean model-psychology items frozen; SHA-256 in items/f2/SHA256SUMS")


def check_frozen():
    import hashlib
    for line in (F2 / "SHA256SUMS").read_text().splitlines():
        h, p = line.split()
        if hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != h:
            sys.exit(f"{p} does not match items/f2/SHA256SUMS: no call (§7)")


def jobs():
    from common import key_of
    import bettor as B
    import valence as V
    items = sorted((json.loads(l) for l in (F2 / "masked.jsonl").read_text().splitlines() if l.strip()), key=lambda x: x["id"])
    rng = random.Random(seeds()["order"])
    swap = {it["id"]: rng.random() < 0.5 for it in items}     # True: option_b shown as Option 1 (every call, every model)
    steps = []
    for model in BETTORS:
        js = []
        for it in items:
            u = B.user_text(it, swap[it["id"]])
            js.append({"key": key_of("bettor-v1", model, B.SYSTEM, u), "id": it["id"], "model": model, "task": "bettor",
                       "option_1_is": "b" if swap[it["id"]] else "a", "system": B.SYSTEM, "user": u})
        steps.append((f"{model.split('-')[1]} bettor", js))
        if model == RATER:   # the flattery rater runs right after the Opus bettor (§3)
            fj = []
            for it in items:
                o1, o2 = (it["option_b"], it["option_a"]) if swap[it["id"]] else (it["option_a"], it["option_b"])
                u = f"Field: {it['field']}\n\nOption 1: {o1}\nOption 2: {o2}"   # valence.py's user text, verbatim
                fj.append({"key": key_of(V.TAG, RATER, V.SYSTEM, u), "id": it["id"], "model": RATER, "task": "flattery",
                           "option_1_is": "b" if swap[it["id"]] else "a", "system": V.SYSTEM, "user": u})
            steps.append(("opus flattery", fj))
    return steps


def bet():
    from common import Caller, structured
    import bettor as B
    check_frozen()

    def fn(j):
        out, cost, rid, usage = structured(j["model"], j["system"], j["user"], B.SCHEMA, f"f2-{j['task']}", max_tokens=4000)
        return {"id": j["id"], "model": j["model"], "task": j["task"], "option_1_is": j["option_1_is"],
                "p_option_1": out["p_option_1"], "rationale": out["rationale"], "cost": cost, "request_id": rid,
                "usage": usage, "t_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
    steps = jobs()
    try:
        for name, js in steps:
            run_caller(Caller(BET_CACHE, f"f2 {name}", cap=cap()), js, fn, name.replace(" ", "-"))
    finally:
        cache = json.loads(BET_CACHE.read_text()) if BET_CACHE.exists() else {}
        rows = [cache[j["key"]] for _, js in steps for j in js if j["key"] in cache]
        BETS_OUT.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
        print(f"wrote {len(rows)} ratings to {BETS_OUT.relative_to(ROOT)}")


def dry():
    print(f"plan: {len(STARTS)} arXiv requests (model-psychology query, round 2's window, results {STARTS[0]}-{STARTS[-1] + PER_REQUEST - 1}); "
          f"template; beacon order; leakage check on the first {BATCH1} (Sonnet, about $0.0029 each, about ${0.0029 * BATCH1:.2f}), "
          f"{BATCH2} more only if fewer than {TARGET} are clean; freeze the first {TARGET} clean (at least {MIN_ITEMS}); "
          f"Opus bettor (about $0.0049 each), Opus flattery rater (about $0.0049), Sonnet (about $0.0021), Haiku (about $0.0001) "
          f"on {TARGET}: about ${TARGET * (0.0049 + 0.0049 + 0.0021 + 0.0001):.2f}; bet cap ${BET_CAP}")
    print("selftest of the template writer:")
    T.selftest()


if __name__ == "__main__":
    {"--fetch": fetch, "--build": build, "--order": order, "--leak": leak, "--freeze": freeze, "--bet": bet,
     "--dry-run": dry}[sys.argv[1]]()

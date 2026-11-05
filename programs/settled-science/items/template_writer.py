"""Round 2 item writer: a fixed template, no model (protocol/template-writer.md).

    python3 items/template_writer.py --selftest     # synthetic abstracts only; fetches nothing
    python3 items/template_writer.py --fetch        # four arXiv API requests -> items/r2/pool.json
    python3 items/template_writer.py --build        # pool -> items/r2/candidates.jsonl (+ r2/build-log.json)
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify  # noqa: E402  (banned-word list, normaliser, mechanical check)

ROOT = Path(__file__).resolve().parents[1]
R2 = ROOT / "items" / "r2"
NS = verify.NS
QUERIES = [  # order matters: a paper in several results goes to the first field
    ("quantum-devices", 'cat:quant-ph AND (abs:transmon OR abs:"superconducting qubit" OR abs:"trapped ion" OR abs:"neutral atom" OR abs:"spin qubit")'),
    ("scalable-oversight", 'abs:"LLM-as-a-judge" OR abs:"reward hacking" OR abs:"chain-of-thought monitor" OR abs:"weak-to-strong" OR abs:"AI control" OR abs:"scalable oversight"'),
    ("model-psychology", '(cat:cs.CL OR cat:cs.AI) AND (abs:sycophancy OR abs:introspection OR abs:"theory of mind" OR abs:"self-report" OR abs:persona OR abs:"verbalized confidence")'),
    ("interpretability", '(cat:cs.LG OR cat:cs.CL) AND (abs:"sparse autoencoder" OR abs:"linear probe" OR abs:"activation patching" OR abs:"steering vector" OR abs:"mechanistic interpretability")'),
]
DATE = "submittedDate:[202607010000 TO 202611042359]"
PAIRS = [("higher", "lower"), ("increase", "decrease"), ("increases", "decreases"), ("increased", "decreased"),
         ("increasing", "decreasing"), ("larger", "smaller"), ("more", "less"), ("better", "worse"),
         ("stronger", "weaker"), ("faster", "slower"), ("longer", "shorter"), ("outperform", "underperform"),
         ("outperforms", "underperforms"), ("outperformed", "underperformed"), ("improve", "worsen"),
         ("improves", "worsens"), ("improved", "worsened")]
SWAP = {**{a: b for a, b in PAIRS}, **{b: a for a, b in PAIRS}}
UP = {a for a, _ in PAIRS}
CUE = re.compile(r"\bthan\b|\bwe (find|found|show|observe|demonstrate)\b|\b(results|experiments|analyses) (show|reveal|indicate)\b", re.I)
NEG = re.compile(r"\b(not|no|never|without|cannot|fail\w*|neither|nor)\b|n't\b", re.I)
WORD = re.compile(r"\b(" + "|".join(sorted(SWAP, key=len, reverse=True)) + r")\b", re.I)
QUESTION = "Which of these two sentences is the one in the paper's abstract?"
METHODS = "No summary is given. The two options are the same sentence from the paper's abstract, differing in one word."


def sentences(abstract):
    a = re.sub(r"\s+", " ", abstract).strip()
    return re.split(r"(?<=[.!?])\s+(?=[A-Z(])", a)


def candidate(s):
    """Return (reason-or-None). None means the sentence is a candidate."""
    n = len(s.split())
    if not 12 <= n <= 45:
        return "length"
    hits = WORD.findall(s)
    if len(hits) != 1:
        return f"{len(hits)} swap words"
    if not CUE.search(s):
        return "no result cue"
    low = verify.norm(s)
    if any(re.search(p, low) for p in verify.BANNED):
        return "banned word"
    if NEG.search(s):
        return "negation"
    if "$" in s or "\\" in s:
        return "latex"
    if re.search(r"\b(more|less) than \d", s, re.I):
        return "more/less than a number"
    return None


def swap(s):
    m = WORD.search(s)
    w = m.group(1)
    r = SWAP[w.lower()]
    r = r.capitalize() if w[0].isupper() else r
    return s[:m.start(1)] + r + s[m.end(1):], w.lower()


def item_from(paper, field):
    for s in sentences(paper["summary"])[1:]:
        if candidate(s) is None:
            other, w = swap(s)
            return {"field": field, "arxiv_id": paper["id"], "title": paper["title"], "first_author": paper["authors"][0].split()[-1] if paper["authors"] else "",
                    "question": QUESTION, "methods": METHODS, "option_a": s, "option_b": other, "true_option": "a",
                    "evidence_quote": s, "headline_side": None, "up_side": "a" if w in UP else "b",
                    "notes": "template writer v1 (no model)"}
    return None


def fetch(start=0):
    """start=0: page 1 (results 0-299). start=300: the D22 extension, appended after page 1."""
    R2.mkdir(parents=True, exist_ok=True)
    prev = json.loads((R2 / "pool.json").read_text()) if start else None
    pool = prev["pool"] if prev else {}
    for field, q in QUERIES:
        url = ("https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
            {"search_query": f"({q}) AND {DATE}", "sortBy": "submittedDate", "sortOrder": "descending", "start": start, "max_results": 300}))
        for attempt in range(6):
            try:
                xml = urllib.request.urlopen(url, timeout=120).read()
                break
            except Exception as e:  # noqa: BLE001
                print("arXiv retry", attempt, e, file=sys.stderr)
                time.sleep(30 * (attempt + 1))
        else:
            sys.exit("arXiv unreachable")
        entries = ET.fromstring(xml).findall("a:entry", NS)
        got = []
        for e in entries:
            if e.find("a:title", NS) is None:
                continue
            aid = re.sub(r"v\d+$", "", e.find("a:id", NS).text.rsplit("/abs/", 1)[-1])
            got.append({"id": aid, "title": re.sub(r"\s+", " ", e.find("a:title", NS).text).strip(),
                        "summary": re.sub(r"\s+", " ", e.find("a:summary", NS).text).strip(),
                        "published": e.find("a:published", NS).text[:10],
                        "comment": (e.find("arxiv:comment", NS).text if e.find("arxiv:comment", NS) is not None else ""),
                        "authors": [a.find("a:name", NS).text for a in e.findall("a:author", NS)]})
        known = {p["id"] for p in pool.get(field, [])}
        pool[field] = pool.get(field, []) + [p for p in got if p["id"] not in known]
        print(field, len(got), "papers", flush=True)
        time.sleep(5)
    pages = (prev or {}).get("pages", [0]) + ([start] if start else [])
    (R2 / "pool.json").write_text(json.dumps({"queries": QUERIES, "date": DATE, "pages": pages, "pool": pool}, indent=1))


def build():
    pool = json.loads((R2 / "pool.json").read_text())["pool"]
    r1 = set()
    for p in (ROOT / "items" / "drafts").glob("*.jsonl"):
        r1 |= {json.loads(l)["arxiv_id"].strip() for l in p.read_text().splitlines() if l.strip()}
    seen, out, log = set(), [], []
    for field, _ in QUERIES:
        for p in pool[field]:
            why = ("duplicate across fields" if p["id"] in seen else "in round 1" if p["id"] in r1 else
                   "v1 before 2026-07-01" if p["published"] < "2026-07-01" else
                   "ICML 2026 / TMLR comment" if re.search(r"ICML 2026|TMLR|Transactions on Machine Learning Research", p["comment"] or "") else None)
            seen.add(p["id"])
            if why:
                log.append({"id": p["id"], "field": field, "dropped": why})
                continue
            it = item_from(p, field)
            if it is None:
                log.append({"id": p["id"], "field": field, "dropped": "no candidate sentence"})
                continue
            it["v1_date"], it["side"] = p["published"], "post"
            meta = {p["id"]: {"title": p["title"], "summary": p["summary"], "published": p["published"]}}
            errs, _ = verify.check(it, meta)
            # the template's options always differ in one swap pair; verify's pair list may lack a few of them
            errs = [e for e in errs if not e.startswith("options not parallel")]
            if errs:
                log.append({"id": p["id"], "field": field, "dropped": "verify: " + "; ".join(errs)})
                continue
            it["cid"] = f"t-{p['id']}"
            out.append(it)
    (R2 / "candidates.jsonl").write_text("".join(json.dumps(i) + "\n" for i in out))
    (R2 / "build-log.json").write_text(json.dumps(log, indent=1))
    from collections import Counter
    print(len(out), "template items;", Counter(i["field"] for i in out))
    print("dropped:", Counter(x["dropped"].split(":")[0] for x in log))


def freeze():
    """Keep leakage-clean items, ids r2-001.. in (field order, arxiv id) order; write items, masked, SHA-256 (D22)."""
    import hashlib
    st = json.loads((R2 / "leakage-status.json").read_text())
    order = {f: i for i, (f, _) in enumerate(QUERIES)}
    keep = sorted((c for c in (json.loads(l) for l in (R2 / "candidates.jsonl").read_text().splitlines() if l.strip())
                   if st.get(c["cid"]) == "clean"), key=lambda c: (order[c["field"]], c["arxiv_id"]))
    if len(keep) < 60:
        sys.exit(f"{len(keep)} clean items < 60: round 2 is withdrawn unbet (D22)")
    for n, c in enumerate(keep, 1):
        c["id"], c["leakage_status"] = f"r2-{n:03d}", "clean"
    full = "".join(json.dumps({"id": c["id"], **{k: v for k, v in c.items() if k != "id"}}) + "\n" for c in keep)
    masked = "".join(json.dumps({k: c[k] for k in ("id", "field", "question", "methods", "option_a", "option_b")}) + "\n" for c in keep)
    (R2 / "items.jsonl").write_text(full)
    (R2 / "masked.jsonl").write_text(masked)
    sums = "".join(f"{hashlib.sha256(t.encode()).hexdigest()}  items/r2/{n}\n" for n, t in (("items.jsonl", full), ("masked.jsonl", masked)))
    (R2 / "SHA256SUMS").write_text(sums)
    from collections import Counter
    print(sums, len(keep), Counter(c["field"] for c in keep))


def selftest():
    abstract = ("Language models are widely used. We study judges on 12 benchmarks with four model families. "
                "We find that larger judges agree with human raters more often than smaller judges across all tasks. "
                "Our results show that position bias was 12% lower than reported in prior studies of judges.")
    p = {"id": "0000.00000", "title": "t", "summary": abstract, "authors": ["A B"], "published": "2026-08-01"}
    it = item_from(p, "scalable-oversight")
    assert it is None or "Language models" not in it["option_a"], "first sentence must be skipped"
    # sentence 2 has no swap word; sentence 3 has two (larger, more, smaller -> 3) -> skip; sentence 4 has one (lower) + cue
    assert it and it["option_a"].startswith("Our results show") and "12% higher than" in it["option_b"], it
    assert it["up_side"] == "b"
    assert candidate("We find that the method is not better than the baseline on every one of our tasks.") == "negation"
    assert candidate("We find that more than 30 models were tested in total across the whole benchmark suite here.") is not None
    s, w = swap("Higher coherence was observed than in the reference devices measured at the same temperature.")
    assert s.startswith("Lower coherence") and w == "higher"
    print("selftest ok:", it["option_a"], "|", it["option_b"])


if __name__ == "__main__":
    {"--selftest": selftest, "--fetch": fetch, "--fetch-more": lambda: fetch(300), "--build": build, "--freeze": freeze}[sys.argv[1]]()

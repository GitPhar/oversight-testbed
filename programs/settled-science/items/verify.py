"""Mechanical item checks (protocol/fixed-rules.md, Rule 3, first bullet). No model calls, no keys; arXiv API reads only.

    python3 items/verify.py items/drafts/*.jsonl          -> items/verify-report.json, prints failures

For every draft item: the arXiv id exists; the title matches; the v1 date is read from the API (it decides the cutoff
side, not the writer); the evidence quote appears verbatim in the API abstract after whitespace and punctuation
normalisation; no banned word appears in question, methods or options; the two options differ only in direction slots.
"""
import difflib
import json
import re
import sys
import time
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
META = ROOT / "items" / "arxiv-meta.json"
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
CUTOFF_FIRST_POST = "2026-07-01"
WINDOW = ("2024-01-01", "2026-11-04")

BANNED = [r"fail(s|ed|ing)? to", r"\bstill\b", r"\beven\b", r"surprising", r"unexpected", r"\bonly\b", r"\bmerely\b",
          r"\bactually\b", r"\bdespite\b", r"\bhowever\b", r"\brobust", r"successful", r"breakthrough", r"state-of-the-art",
          r"\bnovel\b", r"mitigat", r"overcom", r"vulnerab", r"risk of", r"remarkab", r"striking", r"significan"]
BANNED_NOT_IN_OPTIONS = [r"improv"]  # allowed as an option's direction word, not in question or methods

PAIRS = [("higher", "lower"), ("more", "less"), ("more", "fewer"), ("increased", "decreased"), ("increase", "decrease"),
         ("increases", "decreases"), ("larger", "smaller"), ("above", "below"), ("better", "worse"), ("earlier", "later"),
         ("stronger", "weaker"), ("faster", "slower"), ("longer", "shorter"), ("greater", "smaller"), ("greater", "less"),
         ("rose", "fell"), ("grew", "shrank"), ("improved", "worsened"), ("improved", "degraded"), ("raised", "lowered"),
         ("exceeded", "fell below"), ("outperformed", "underperformed"), ("most", "least"), ("lowest", "highest"),
         ("smallest", "largest"), ("increasing", "decreasing"), ("rising", "falling"), ("up", "down"), ("wider", "narrower"),
         ("worse", "better"), ("larger", "lower"), ("higher", "smaller"), ("bigger", "smaller"), ("closer", "farther"),
         ("closer", "further"), ("more", "lower"), ("greater", "lower"), ("lengthened", "shortened"), ("strengthened", "weakened"),
         ("widened", "narrowed"), ("easier", "harder"), ("high", "low"), ("deeper", "shallower"), ("an earlier", "a later"), ("rose", "declined"), ("amplified", "dampened"), ("amplified", "suppressed"), ("enhanced", "suppressed"),
         ("enhanced", "reduced"), ("increased", "reduced"), ("increase", "reduce"), ("increases", "reduces")]
PAIRSET = {frozenset(p) for p in PAIRS}


def norm(s):
    s = unicodedata.normalize("NFKC", s or "")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("−", "-")
    return re.sub(r"\s+", " ", s).strip().lower()


def fetch(ids):
    meta = json.loads(META.read_text()) if META.exists() else {}
    todo = [i for i in ids if i not in meta]
    for k in range(0, len(todo), 40):
        chunk = todo[k:k + 40]
        url = f"https://export.arxiv.org/api/query?id_list={','.join(chunk)}&max_results={len(chunk)}"
        for attempt in range(6):
            try:
                xml = urllib.request.urlopen(url, timeout=60).read()
                break
            except Exception as e:  # noqa: BLE001
                print("arXiv retry", attempt, e, file=sys.stderr)
                time.sleep(30 * (attempt + 1))
        else:
            sys.exit("arXiv API unreachable")
        for e in ET.fromstring(xml).findall("a:entry", NS):
            aid = re.sub(r"v\d+$", "", e.find("a:id", NS).text.rsplit("/abs/", 1)[-1])
            title = e.find("a:title", NS)
            if title is None:
                continue
            meta[aid] = {"title": re.sub(r"\s+", " ", title.text).strip(),
                         "summary": re.sub(r"\s+", " ", e.find("a:summary", NS).text).strip(),
                         "published": e.find("a:published", NS).text[:10],
                         "updated": e.find("a:updated", NS).text[:10],
                         "comment": (e.find("arxiv:comment", NS).text if e.find("arxiv:comment", NS) is not None else ""),
                         "authors": [a.find("a:name", NS).text for a in e.findall("a:author", NS)],
                         "categories": [c.get("term") for c in e.findall("a:category", NS)]}
        META.write_text(json.dumps(meta, indent=1, sort_keys=True))
        time.sleep(3)
    return meta


def option_diff_ok(a, b):
    ta, tb = norm(a).rstrip(".").split(), norm(b).rstrip(".").split()
    ops = [o for o in difflib.SequenceMatcher(a=ta, b=tb, autojunk=False).get_opcodes() if o[0] != "equal"]
    if not ops:
        return False, "options identical"
    for tag, i1, i2, j1, j2 in ops:
        x, y = " ".join(ta[i1:i2]), " ".join(tb[j1:j2])
        if tag != "replace" or frozenset((x, y)) not in PAIRSET:
            return False, f"{tag}: '{x}' vs '{y}'"
    return True, ""


def check(item, meta):
    errs = []
    m = meta.get(item.get("arxiv_id", "").strip())
    if not m:
        return ["arxiv id not found"], None
    if difflib.SequenceMatcher(a=norm(item.get("title")), b=norm(m["title"])).ratio() < 0.85:
        errs.append(f"title mismatch: arXiv says '{m['title']}'")
    if not (WINDOW[0] <= m["published"] <= WINDOW[1]):
        errs.append(f"v1 {m['published']} outside 2024-01-01..2026-11-04")
    if norm(item.get("evidence_quote")).rstrip(".") not in norm(m["summary"]):
        errs.append("evidence quote not verbatim in abstract")
    text = " ".join(norm(item.get(k)) for k in ("question", "methods", "option_a", "option_b"))
    qm = " ".join(norm(item.get(k)) for k in ("question", "methods"))
    for pat in BANNED:
        if re.search(pat, text):
            errs.append(f"banned: {pat}")
    for pat in BANNED_NOT_IN_OPTIONS:
        if re.search(pat, qm):
            errs.append(f"banned in question/methods: {pat}")
    ok, why = option_diff_ok(item.get("option_a", ""), item.get("option_b", ""))
    if not ok:
        errs.append(f"options not parallel ({why})")
    if item.get("true_option") not in ("a", "b"):
        errs.append("true_option not a/b")
    if item.get("headline_side") not in ("a", "b", None):
        errs.append("headline_side not a/b/null")
    if item.get("field") not in ("model-psychology", "interpretability", "scalable-oversight", "quantum-devices"):
        errs.append("bad field")
    side = "post" if m["published"] >= CUTOFF_FIRST_POST else "pre"
    return errs, side


def main(paths):
    items = []
    for p in paths:
        for n, line in enumerate(Path(p).read_text().splitlines()):
            if line.strip():
                it = json.loads(line)
                it["arxiv_id"] = re.sub(r"v\d+$", "", it.get("arxiv_id", "").strip().removeprefix("arXiv:"))
                it["_src"] = f"{Path(p).name}:{n + 1}"
                items.append(it)
    meta = fetch(sorted({i["arxiv_id"] for i in items}))
    report = []
    for it in items:
        errs, side = check(it, meta)
        m = meta.get(it["arxiv_id"], {})
        report.append({"src": it["_src"], "arxiv_id": it["arxiv_id"], "field": it.get("field"), "side": side,
                       "v1": m.get("published"), "comment": m.get("comment"), "errors": errs})
    (ROOT / "items" / "verify-report.json").write_text(json.dumps(report, indent=1))
    bad = [r for r in report if r["errors"]]
    for r in bad:
        print(r["src"], r["arxiv_id"], "|", "; ".join(r["errors"]))
    print(f"\n{len(report)} items, {len(report) - len(bad)} pass, {len(bad)} fail; "
          f"post-cutoff passing: {sum(1 for r in report if not r['errors'] and r['side'] == 'post')}")


if __name__ == "__main__":
    main(sys.argv[1:])

"""Score ss-b12 (experiments/ss-b12.md; direction ss-f4): is the bettor's pre-cutoff advantage recall?
No model calls; numpy only.

    python3 scoring/score_f4.py                       # -> scoring/f4-scores.json, scoring/f4-tables.md
    python3 scoring/score_f4.py --synthetic <world>   # dry run on generated rows; reads no answers
         worlds: memory (pre better only where recognised) | easier (pre better everywhere) | same | ceiling

Pre side: items/f4/items.jsonl with bettor/f4-bets.jsonl (new). Post side: round 2's 92 items (items/r2/items.jsonl)
with ss-b5's primary bets (bettor/r2-bets.jsonl, archive). Both template-written from the same four arXiv queries.
An item is RECOGNISED if its bettor rationale matches RECOG (fixed before any f4 rationale existed; answer-free).
Primary: Brier(pre, not recognised) - Brier(post, not recognised); independent percentile bootstrap within each side,
10,000 resamples, default_rng(20261104). Pass: upper bound < 0 (tolerance 1e-12). Untestable: < 30 unrecognised pre items.
"""
import json
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PRE_ITEMS = ROOT / "items" / "f4" / "items.jsonl"
PRE_BETS = ROOT / "bettor" / "f4-bets.jsonl"
POST_ITEMS = ROOT / "items" / "r2" / "items.jsonl"
POST_BETS = ROOT / "bettor" / "r2-bets.jsonl"
OUT_JSON = ROOT / "scoring" / "f4-scores.json"
OUT_MD = ROOT / "scoring" / "f4-tables.md"
BOOT_SEED, BOOT_N, EPS, MIN_PRE = 20261104, 10000, 1e-12, 30
RECOG = re.compile(
    r"\b(I recall|I remember|recalled|as I recall|from (?:my )?memory|I(?: am|'m) familiar|familiar with (?:this|the) "
    r"(?:paper|study|work|result|abstract|finding)|I recogni[sz]e|recogni[sz]e (?:this|the) (?:paper|study|work|abstract|"
    r"sentence|result)|this (?:paper|study|work) (?:is|was) (?:known|published|from)|known (?:paper|study|result) (?:from|by)|"
    r"the (?:original|actual) (?:paper|abstract|study) (?:says|said|states|stated|reported|reports)|I(?: have|'ve) seen "
    r"(?:this|the))\b", re.I)


def load(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def p_true(b, it):
    p1 = min(99, max(1, b["p_option_1"])) / 100
    return p1 if b["option_1_is"] == it["true_option"] else 1 - p1


def boot(v, n=BOOT_N, seed=BOOT_SEED):
    v = np.asarray(v, float)
    m = np.sort(v[np.random.default_rng(seed).integers(0, len(v), size=(n, len(v)))].mean(1))
    return (float(m[int(0.025 * n)]), float(m[int(0.975 * n) - 1]))


def boot2(a, b, n=BOOT_N, seed=BOOT_SEED):
    """mean(a) - mean(b), each side resampled on its own (two independent item sets)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    rng = np.random.default_rng(seed)
    d = np.sort(a[rng.integers(0, len(a), size=(n, len(a)))].mean(1) - b[rng.integers(0, len(b), size=(n, len(b)))].mean(1))
    return (float(d[int(0.025 * n)]), float(d[int(0.975 * n) - 1]))


def r6(x):
    return None if x is None else round(float(x), 6)


def rows_of(items, bets, side):
    by = {it["id"]: it for it in items}
    out = []
    for b in bets:
        if b.get("kind") != "primary" or b["id"] not in by:
            continue
        it = by[b["id"]]
        pt = p_true(b, it)
        out.append({"id": b["id"], "side": side, "field": it["field"], "window": it.get("window", "post"),
                    "b": (1 - pt) ** 2, "right": 1.0 if pt > 0.5 else 0.5 if pt == 0.5 else 0.0,
                    "recognised": bool(RECOG.search(b.get("rationale") or ""))})
    return out


def gap(pre, post):
    a, b = [r["b"] for r in pre], [r["b"] for r in post]
    if not a or not b:
        return None, (None, None)
    return float(np.mean(a) - np.mean(b)), boot2(a, b)


def score(pre, post):
    s = {"bet": "ss-b12", "n_pre": len(pre), "n_post": len(post),
         "n_pre_recognised": sum(r["recognised"] for r in pre), "n_post_recognised": sum(r["recognised"] for r in post)}
    pu = [r for r in pre if not r["recognised"]]
    qu = [r for r in post if not r["recognised"]]
    s["n_pre_unrecognised"], s["n_post_unrecognised"] = len(pu), len(qu)
    if len(pu) < MIN_PRE:
        s["label"] = "untestable"
        s["sentence"] = (f"Too few pre-cutoff items the bettor showed no sign of recognising were scored to test it "
                         f"({len(pu)}; at least {MIN_PRE} needed).")
        s["verdict_reported"] = "untestable"
        return s
    d, (lo, hi) = gap(pu, qu)
    s["d"], s["d_ci"] = r6(d), [r6(lo), r6(hi)]
    s["label"] = "pass" if hi < 0 - EPS else "null"
    for name, rs in (("pre_unrecognised", pu), ("post_unrecognised", qu), ("pre_all", pre), ("post_all", post),
                     ("pre_recognised", [r for r in pre if r["recognised"]])):
        s[name] = {"n": len(rs), "brier": r6(np.mean([r["b"] for r in rs])) if rs else None,
                   "brier_ci": [r6(x) for x in boot([r["b"] for r in rs])] if len(rs) > 1 else None,
                   "acc": r6(np.mean([r["right"] for r in rs])) if rs else None}
    da, ca = gap(pre, post)
    s["d_all"], s["d_all_ci"] = r6(da), [r6(x) for x in ca]
    s["by_window"] = {}
    for w in ("2024", "2025", "2026H1"):
        rs = [r for r in pu if r["window"] == w]
        g, c = gap(rs, qu) if len(rs) > 1 else (None, (None, None))
        s["by_window"][w] = {"n": len(rs), "brier": r6(np.mean([r["b"] for r in rs])) if rs else None,
                             "d": r6(g), "ci": [r6(x) for x in c]}
    fields = sorted({r["field"] for r in pu + qu})
    s["by_field"] = {f: {"n_pre": sum(r["field"] == f for r in pu), "n_post": sum(r["field"] == f for r in qu),
                         "pre": r6(np.mean([r["b"] for r in pu if r["field"] == f])) if any(r["field"] == f for r in pu) else None,
                         "post": r6(np.mean([r["b"] for r in qu if r["field"] == f])) if any(r["field"] == f for r in qu) else None}
                     for f in fields}
    flips = []
    for r in pu + qu:
        a = [x for x in pu if x is not r]
        b = [x for x in qu if x is not r]
        _, (_, h) = gap(a, b)
        if (h < 0 - EPS) != (s["label"] == "pass"):
            flips.append(r["id"])
    s["loo_flips"] = flips
    s["field_out"] = {}
    for f in fields:
        a = [x for x in pu if x["field"] != f]
        b = [x for x in qu if x["field"] != f]
        g, (l, h) = gap(a, b)
        s["field_out"][f] = {"d": r6(g), "ci": [r6(l), r6(h)], "label": "pass" if h < 0 - EPS else "null"}
    jk = [s["field_out"][f]["d"] for f in fields]
    k = len(jk)
    se = float(np.sqrt((k - 1) / k * sum((x - np.mean(jk)) ** 2 for x in jk)))
    s["field_jackknife"] = {"clusters": k, "ci": [r6(d - 1.96 * se), r6(d + 1.96 * se)]}
    s["sentence"] = sentence(s)
    s["verdict_reported"] = s["label"] + (", unreplicated" if s["label"] == "pass" else "")
    return s


def c3(c):
    return f"[{c[0]:.3f}, {c[1]:.3f}]"


def sentence(s):
    pu, qu = s["pre_unrecognised"], s["post_unrecognised"]
    if s["label"] == "pass":
        t = (f"On {pu['n']} older papers whose abstracts it showed no sign of recognising, the bettor still scored better than on "
             f"{qu['n']} papers posted after its training cutoff (Brier {pu['brier']:.3f} against {qu['brier']:.3f}; difference "
             f"{s['d']:.3f} {c3(s['d_ci'])}), so its advantage on older papers is not only papers it says it remembers. It may "
             f"still be memory it does not mention, or older findings being easier.")
    else:
        t = (f"On {pu['n']} older papers whose abstracts it showed no sign of recognising, the bettor was not shown to score "
             f"better than on {qu['n']} papers posted after its training cutoff (Brier {pu['brier']:.3f} against "
             f"{qu['brier']:.3f}; difference {s['d']:.3f} {c3(s['d_ci'])}), so this test finds no advantage on older papers "
             f"beyond recall.")
    if s["loo_flips"]:
        t += (f" This label rests on single items: without any one of {', '.join(s['loo_flips'][:5])}"
              f"{' …' if len(s['loo_flips']) > 5 else ''} it would be {'null' if s['label'] == 'pass' else 'pass'}.")
    fo = [f for f, v in s["field_out"].items() if v["label"] != s["label"]]
    if fo:
        t += f" Leaving out the {', '.join(fo)} query bucket would make it {'null' if s['label'] == 'pass' else 'pass'}."
    t += (f" Recognition was coded from the rationale by a fixed word rule ({s['n_pre_recognised']} of {s['n_pre']} older and "
          f"{s['n_post_recognised']} of {s['n_post']} newer items flagged); a model can remember without saying so. "
          f"One bettor (claude-opus-5-5 at effort low), template-written sentence pairs only.")
    return t


def tables(s):
    L = ["# ss-b12 tables (generated by scoring/score_f4.py; do not edit)", "", f"Verdict: **{s['verdict_reported']}**", ""]
    if s["label"] == "untestable":
        return "\n".join(L + [f"> {s['sentence']}"]) + "\n"
    L += ["| set | n | Brier | 95% CI | share right |", "|---|---|---|---|---|"]
    for k, lab in (("pre_unrecognised", "older, not recognised (primary)"), ("post_unrecognised", "newer, not recognised (primary)"),
                   ("pre_recognised", "older, recognised"), ("pre_all", "older, all"), ("post_all", "newer, all")):
        v = s[k]
        if v["n"]:
            ci = c3(v["brier_ci"]) if v["brier_ci"] else "—"
            L.append(f"| {lab} | {v['n']} | {v['brier']:.3f} | {ci} | {v['acc']:.2f} |")
    L += ["", "| difference (older − newer) | value | 95% CI |", "|---|---|---|",
          f"| **not recognised (primary)** | **{s['d']:+.3f}** | {c3(s['d_ci'])} |",
          f"| all items (secondary) | {s['d_all']:+.3f} | {c3(s['d_all_ci'])} |",
          f"| field-cluster jackknife on the primary (secondary) | {s['d']:+.3f} | {c3(s['field_jackknife']['ci'])} |",
          "", "| older window (not recognised) | n | Brier | difference vs newer | 95% CI |", "|---|---|---|---|---|"]
    for w, v in s["by_window"].items():
        if v["n"] > 1:
            L.append(f"| {w} | {v['n']} | {v['brier']:.3f} | {v['d']:+.3f} | {c3(v['ci'])} |")
        else:
            L.append(f"| {w} | {v['n']} | — | — | — |")
    L += ["", "| query bucket | older n | older Brier | newer n | newer Brier | left out: difference | 95% CI | label |", "|---|---|---|---|---|---|---|---|"]
    for f, v in s["by_field"].items():
        fo = s["field_out"][f]
        pre = f"{v['pre']:.3f}" if v["pre"] is not None else "—"
        post = f"{v['post']:.3f}" if v["post"] is not None else "—"
        L.append(f"| {f} | {v['n_pre']} | {pre} | {v['n_post']} | {post} | {fo['d']:+.3f} | {c3(fo['ci'])} | {fo['label']} |")
    L += ["", f"Leave-one-item-out flips: {len(s['loo_flips'])}" + (f" ({', '.join(s['loo_flips'])})" if s["loo_flips"] else ""),
          "", "Pre-registered sentence:", "", f"> {s['sentence']}"]
    return "\n".join(L) + "\n"


def synthetic(world, seed=5):
    rng = np.random.default_rng(seed)
    fields = ["quantum-devices", "scalable-oversight", "model-psychology", "interpretability"]
    pb = {"memory": (0.070, 0.070, 0.15), "easier": (0.035, 0.070, 0.0), "same": (0.070, 0.070, 0.05), "ceiling": (0.060, 0.070, 0.05)}[world]
    def mk(n, side, mean, rec):
        out = []
        for i in range(n):
            recog = rng.random() < rec
            m = 0.01 if (recog and world == "memory") else mean
            b = float(min(0.95, rng.exponential(m)))
            out.append({"id": f"{side}-{i}", "side": side, "field": fields[i % 4], "window": ["2024", "2025", "2026H1"][i % 3] if side == "pre" else "post",
                        "b": b, "right": 1.0 if b < 0.25 else 0.0, "recognised": recog})
        return out
    return mk(52, "pre", pb[0], pb[2]), mk(92, "post", pb[1], 0.0)


def main():
    if "--synthetic" in sys.argv:
        w = sys.argv[sys.argv.index("--synthetic") + 1]
        s = score(*synthetic(w))
        print(w, "->", s["label"], s.get("d"), s.get("d_ci"), "recognised pre", s["n_pre_recognised"])
        return
    pre = rows_of(load(PRE_ITEMS), load(PRE_BETS), "pre") if PRE_BETS.exists() else []
    post = rows_of(load(POST_ITEMS), load(POST_BETS), "post")
    s = score(pre, post)
    OUT_JSON.write_text(json.dumps(s, indent=1, ensure_ascii=False))
    OUT_MD.write_text(tables(s))
    print(tables(s))


if __name__ == "__main__":
    main()

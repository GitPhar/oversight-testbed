"""Score the bettor against the published record (pre-registration §4-§5). No model calls.

    python3 scoring/score.py                       # real bets -> scoring/scores.json, scoring/tables.md
    python3 scoring/score.py --synthetic <kind>    # dry run on synthetic bets: coin | oracle | headline | anti

p_true = the bettor's probability on the option the paper reported (p_option_1 if Option 1 was the reported one, else
1 - p_option_1). Brier = mean over items of (1 - p_true)^2; a constant 0.5 scores 0.25. Unit of analysis: items.
"""
import json
import math
import random
import re
import sys

import numpy as np
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "items" / "items.jsonl"
BETS = ROOT / "bettor" / "bets.jsonl"
BOOT_SEED, BOOT_N = 20261104, 10000
HEADLINE_P = 0.75
EPS = 1e-12  # numerical tolerance on every 'below' test (D16)


def load_items():
    return {it["id"]: it for it in (json.loads(l) for l in ITEMS.read_text().splitlines() if l.strip())}


def year_bin(it):
    d = it["v1_date"]
    if it["side"] == "pre" and d >= "2026-07-01":   # v1 after the cutoff, moved to pre-cutoff (D8, D12; audit cut 2)
        return "2026-moved"
    return "2026-post" if it["side"] == "post" else ("2026-pre" if d.startswith("2026") else d[:4])


def p_true_of(bet, it):
    p1 = min(99, max(1, bet["p_option_1"])) / 100
    one_is_true = bet["option_1_is"] == it["true_option"]
    return p1 if one_is_true else 1 - p1


def brier(ps):
    return sum((1 - p) ** 2 for p in ps) / len(ps) if ps else None


def boot_ci(vals, stat=None, n=BOOT_N, seed=BOOT_SEED):
    """Percentile bootstrap of the mean over items (numpy; D16). Bounds: sorted[int(0.025n)], sorted[int(0.975n) - 1]."""
    v = np.asarray(vals, float)
    if len(v) == 0:
        return (None, None)
    m = np.sort(v[np.random.default_rng(seed).integers(0, len(v), size=(n, len(v)))].mean(1))
    return (float(m[int(0.025 * n)]), float(m[int(0.975 * n) - 1]))


def acc(ps):
    return sum(1 if p > 0.5 else 0.5 if p == 0.5 else 0 for p in ps) / len(ps) if ps else None


def headline_p(it):
    """The publication-bias baseline: 0.75 on the paper's headline side where one is tagged, 0.5 where none is."""
    hs = it.get("headline_side")
    return 0.5 if hs is None else (HEADLINE_P if hs == it["true_option"] else 1 - HEADLINE_P)


def summarise(rows):
    ps = [r["p_true"] for r in rows]
    se = [(1 - p) ** 2 for p in ps]
    hb = [(1 - r["headline_p"]) ** 2 for r in rows]
    diff = [a - b for a, b in zip(se, hb)]
    mean = lambda v: sum(v) / len(v)  # noqa: E731
    return {"n": len(rows), "brier": brier(ps), "brier_ci": boot_ci(se, mean), "accuracy": acc(ps),
            "mean_p_true": mean(ps) if ps else None, "headline_brier": mean(hb) if hb else None,
            "minus_headline": mean(diff) if diff else None, "minus_headline_ci": boot_ci(diff, mean)}


def calibration(rows):
    """Confidence in the side the bettor favoured vs how often that side was the reported one."""
    b = defaultdict(list)
    for r in rows:
        p = r["p_true"]
        conf, right = (p, 1) if p >= 0.5 else (1 - p, 0)
        if p == 0.5:
            right = 0.5
        lo = min(0.9, int(conf * 10) / 10)
        b[lo].append((conf, right))
    return [{"bucket": f"{lo:.1f}-{lo + 0.1:.1f}", "n": len(v), "mean_conf": sum(c for c, _ in v) / len(v),
             "hit_rate": sum(h for _, h in v) / len(v)} for lo, v in sorted(b.items())]


def score(items, bets):
    prim = {b["id"]: b for b in bets if b["kind"] == "primary"}
    chk = {b["id"]: b for b in bets if b["kind"] == "order-check"}
    rows = []
    for iid, it in sorted(items.items()):
        if iid not in prim:
            continue
        b = prim[iid]
        rows.append({"id": iid, "field": it["field"], "side": it["side"], "year": year_bin(it),
                     "headline": ("none" if it.get("headline_side") is None else
                                  "true-is-headline" if it["headline_side"] == it["true_option"] else "true-is-other"),
                     "p_true": p_true_of(b, it), "headline_p": headline_p(it),
                     "clipped": not (1 <= b["p_option_1"] <= 99)})
    out = {"n_items": len(items), "n_scored": len(rows), "missing": sorted(set(items) - set(prim)),
           "clipped": sum(r["clipped"] for r in rows)}
    post = [r for r in rows if r["side"] == "post"]
    pre = [r for r in rows if r["side"] == "pre"]
    out["primary_post"] = summarise(post)
    out["bets"] = bet_labels(post, pre)
    out["verdict"] = out["bets"]["ss-b1"]["label"]
    out["pre_cutoff"] = summarise(pre)
    se = lambda rs: [(1 - r["p_true"]) ** 2 for r in rs]  # noqa: E731
    out["pre_minus_post"] = (None if not pre or not post else
                             {"diff": brier([r["p_true"] for r in pre]) - brier([r["p_true"] for r in post]),
                              "ci": two_sample_ci(se(pre), se(post))})
    for key in ("field", "year", "side", "headline"):
        out[f"by_{key}"] = {}
        for side in ("post", "pre"):
            groups = defaultdict(list)
            for r in rows:
                if r["side"] == side:
                    groups[r[key]].append(r)
            out[f"by_{key}"][side] = {g: summarise(v) for g, v in sorted(groups.items())}
    out["calibration_post"] = calibration(post)
    out["calibration_pre"] = calibration(pre)
    # order check: same item, options reversed; coherence |p1 + p1' - 100|, and shift toward whichever is shown first
    pairs = []
    for iid, b2 in chk.items():
        if iid in prim:
            b1 = prim[iid]
            pairs.append({"id": iid, "side": items[iid]["side"], "p1": b1["p_option_1"], "p1_swapped": b2["p_option_1"],
                          "incoherence": abs(b1["p_option_1"] + b2["p_option_1"] - 100),
                          "first_shown_bonus": (b1["p_option_1"] + b2["p_option_1"] - 100) / 2})
    out["order_check"] = {"n": len(pairs),
                          "mean_incoherence": sum(p["incoherence"] for p in pairs) / len(pairs) if pairs else None,
                          "mean_first_shown_bonus": sum(p["first_shown_bonus"] for p in pairs) / len(pairs) if pairs else None,
                          "first_shown_bonus_ci": boot_ci([p["first_shown_bonus"] for p in pairs],
                                                          lambda v: sum(v) / len(v)),
                          "same_side_rate": (sum(1 for p in pairs if (p["p1"] - 50) * (50 - p["p1_swapped"]) > 0) / len(pairs)
                                             if pairs else None)}
    out["rows"] = rows
    return out


def two_sample_ci(a, b, n=BOOT_N, seed=BOOT_SEED):
    a, b = np.asarray(a, float), np.asarray(b, float)
    rng = np.random.default_rng(seed)
    ma = a[rng.integers(0, len(a), size=(n, len(a)))].mean(1)
    mb = b[rng.integers(0, len(b), size=(n, len(b)))].mean(1)
    d = np.sort(ma - mb)
    return (float(d[int(0.025 * n)]), float(d[int(0.975 * n) - 1]))


def bet_labels(post, pre):
    """ss-b1..b3 labels by the pre-registered rules (§5) as completed by DEVIATIONS D15, with leave-one-item-out (D16)."""
    se = lambda rs: [(1 - r["p_true"]) ** 2 for r in rs]  # noqa: E731
    dif = lambda rs: [(1 - r["p_true"]) ** 2 - (1 - r["headline_p"]) ** 2 for r in rs]  # noqa: E731
    b1 = lambda po: boot_ci(se(po))[1] < 0.25 - EPS  # noqa: E731
    b2 = lambda po: boot_ci(dif(po))[1] < -EPS  # noqa: E731
    b3 = lambda po, pr: two_sample_ci(se(pr), se(po))[1] < -EPS  # noqa: E731
    out = {}
    if len(post) < 60:
        why = f"{len(post)} post-cutoff findings scored, fewer than 60"
        return {b: {"label": "untestable", "reason": why, "fragile_items": []} for b in ("ss-b1", "ss-b2", "ss-b3")}
    for name, f in (("ss-b1", b1), ("ss-b2", b2)):
        full = f(post)
        flips = [post[i]["id"] for i in range(len(post)) if f(post[:i] + post[i + 1:]) != full]
        out[name] = {"label": "pass" if full else "null", "fragile_items": flips}
    if len(pre) < 30:
        out["ss-b3"] = {"label": "untestable", "reason": f"{len(pre)} pre-cutoff findings scored, fewer than 30", "fragile_items": []}
    else:
        full = b3(post, pre)
        flips = [post[i]["id"] for i in range(len(post)) if b3(post[:i] + post[i + 1:], pre) != full]
        flips += [pre[i]["id"] for i in range(len(pre)) if b3(post, pre[:i] + pre[i + 1:]) != full]
        out["ss-b3"] = {"label": "pass" if full else "null", "fragile_items": flips}
    for v in out.values():
        if v["fragile_items"]:
            v["label_reported"] = f"{v['label']}, fragile"
    return out


def synthetic(items, kind):
    rng = random.Random(1)
    bets = []
    for iid, it in items.items():
        o1 = rng.choice("ab")
        truth_is_1 = o1 == it["true_option"]
        if kind == "coin":
            p = 50
        elif kind == "oracle":
            p = 90 if truth_is_1 else 10
        elif kind == "anti":
            p = 10 if truth_is_1 else 90
        else:  # headline
            hs = it.get("headline_side")
            p = 50 if hs is None else (75 if hs == o1 else 25)
        bets.append({"id": iid, "kind": "primary", "option_1_is": o1, "p_option_1": p})
        bets.append({"id": iid, "kind": "order-check", "option_1_is": "b" if o1 == "a" else "a", "p_option_1": 100 - p})
    return bets


def fmt(x, nd=3):
    return "—" if x is None else f"{x:.{nd}f}"


def tables(s):
    L = ["# Scores (generated by scoring/score.py; do not edit by hand)", ""]
    pp = s["primary_post"]
    L += [f"Primary (post-cutoff, n = {pp['n']}): Brier **{fmt(pp['brier'])}** "
          f"[{fmt(pp['brier_ci'][0])}, {fmt(pp['brier_ci'][1])}], accuracy {fmt(pp['accuracy'], 2)}; "
          f"verdict **{s['verdict']}** (pass: upper 95% bound below 0.25).", ""]
    for b, v in s["bets"].items():
        L.append(f"- {b}: **{v.get('label_reported', v['label'])}**" + (f" ({v['reason']})" if v.get("reason") else "")
                 + (f"; leave-one-item-out flips: {', '.join(v['fragile_items'])}" if v["fragile_items"] else "; no single item flips it"))
    L.append("")
    pc = s["pre_cutoff"]
    L += [f"Pre-cutoff (n = {pc['n']}; **the bettor may have read these papers**): Brier {fmt(pc['brier'])} "
          f"[{fmt(pc['brier_ci'][0])}, {fmt(pc['brier_ci'][1])}], accuracy {fmt(pc['accuracy'], 2)}.", ""]
    for key, title in (("side", "cutoff side"), ("field", "field"), ("year", "year"), ("headline", "publication-bias tag")):
        L += [f"## By {title}", "", "| side | group | n | Brier | 95% CI | accuracy | headline-baseline Brier | bettor − baseline [95% CI] |",
              "|---|---|---|---|---|---|---|---|"]
        for side in ("post", "pre"):
            for g, v in s[f"by_{key}"][side].items():
                L.append(f"| {side}{' (leakage caveat)' if side == 'pre' else ''} | {g} | {v['n']} | {fmt(v['brier'])} | "
                         f"[{fmt(v['brier_ci'][0])}, {fmt(v['brier_ci'][1])}] | {fmt(v['accuracy'], 2)} | "
                         f"{fmt(v['headline_brier'])} | {fmt(v['minus_headline'])} "
                         f"[{fmt(v['minus_headline_ci'][0])}, {fmt(v['minus_headline_ci'][1])}] |")
        L.append("")
    for side in ("post", "pre"):
        L += [f"## Calibration ({side}-cutoff)", "", "| confidence bucket | n | mean confidence | share right |", "|---|---|---|---|"]
        L += [f"| {c['bucket']} | {c['n']} | {fmt(c['mean_conf'], 2)} | {fmt(c['hit_rate'], 2)} |" for c in s[f"calibration_{side}"]]
        L.append("")
    oc = s["order_check"]
    L += ["## Order check (secondary)", "",
          f"{oc['n']} items asked twice with the options reversed. Mean |p + p' − 100| = {fmt(oc['mean_incoherence'], 1)} points; "
          f"mean pull toward whichever option is shown first = {fmt(oc['mean_first_shown_bonus'], 1)} points "
          f"[{fmt(oc['first_shown_bonus_ci'][0], 1)}, {fmt(oc['first_shown_bonus_ci'][1], 1)}]; "
          f"same side chosen both times: {fmt(oc['same_side_rate'], 2)}.", ""]
    if s["pre_minus_post"]:
        d = s["pre_minus_post"]
        L += [f"Pre minus post Brier: {fmt(d['diff'])} [{fmt(d['ci'][0])}, {fmt(d['ci'][1])}] (negative = pre-cutoff easier).", ""]
    return "\n".join(L)


def main():
    items = load_items()
    if "--synthetic" in sys.argv:
        kind = sys.argv[sys.argv.index("--synthetic") + 1]
        s = score(items, synthetic(items, kind))
        print(kind, "post Brier", fmt(s["primary_post"]["brier"]), s["primary_post"]["brier_ci"], "labels", {b: v["label"] for b, v in s["bets"].items()},
              "| pre", fmt(s["pre_cutoff"]["brier"]), "| order bonus", fmt(s["order_check"]["mean_first_shown_bonus"], 1))
        return
    bets = [json.loads(l) for l in BETS.read_text().splitlines() if l.strip()]
    s = score(items, bets)
    (ROOT / "scoring" / "scores.json").write_text(json.dumps(s, indent=1))
    (ROOT / "scoring" / "tables.md").write_text(tables(s))
    print(tables(s))




# ---------------- round 2 (experiments/ss-b4.md) ----------------
R2_ITEMS = ROOT / "items" / "r2" / "items.jsonl"
# F2 (design review ss-b4): P(up option) per swap pair = (ups + 4 x 0.829) / (n + 4), counted on the 146 leak-dropped template
# items only; fixed by the review before any round-2 bet. A pair not listed gets the prior 0.829.
SWAP_PAIR_P = {"larger/smaller": 0.621, "more/less": 0.850, "improve": 0.975, "higher/lower": 0.634, "faster/slower": 0.759,
               "increase": 0.789, "longer/shorter": 0.863, "better/worse": 0.870, "stronger/weaker": 0.914, "outperform": 0.938}
PAIR_PRIOR = 0.829


def swap_pair(it):
    import difflib
    a, b = it["option_a"].split(), it["option_b"].split()
    w = next(" ".join(a[i1:i2]) for t, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes() if t == "replace")
    w = w.lower().strip(".,;:()").split("-")[0]   # "higher-dimensional" -> "higher"
    for stem, key in (("improv", "improve"), ("worsen", "improve"), ("increas", "increase"), ("decreas", "increase"),
                      ("outperform", "outperform"), ("underperform", "outperform")):
        if w.startswith(stem):
            return key
    for key in SWAP_PAIR_P:
        if "/" in key and w in key.split("/"):
            return key
    return w
R2_BETS = ROOT / "bettor" / "r2-bets.jsonl"


def score_r2(items, bets):
    """ss-b4: Brier upper bound < 0.25 on >= 60 scored items. ss-b5: beats the up-word rule (0.75 on the 'up' option).
    Leave-one-item-out and leave-one-field-out on both labels; untestable rules as in D15."""
    prim = {b["id"]: b for b in bets if b["kind"] == "primary"}
    rows = []
    for iid, it in sorted(items.items()):
        if iid in prim:
            b = prim[iid]
            rows.append({"id": iid, "field": it["field"], "side": "post", "year": "2026-post", "headline": "n/a",
                         "p_true": p_true_of(b, it), "headline_p": HEADLINE_P if it["up_side"] == it["true_option"] else 1 - HEADLINE_P,
                         "pair": swap_pair(it),
                         "clipped": not (1 <= b["p_option_1"] <= 99)})
    for r in rows:
        pu = SWAP_PAIR_P.get(r["pair"], PAIR_PRIOR)
        r["pair_p"] = pu if items[r["id"]]["up_side"] == items[r["id"]]["true_option"] else 1 - pu
    se = lambda rs: [(1 - r["p_true"]) ** 2 for r in rs]  # noqa: E731
    d_up = lambda rs: [(1 - r["p_true"]) ** 2 - (1 - r["headline_p"]) ** 2 for r in rs]  # noqa: E731
    d_pair = lambda rs: [(1 - r["p_true"]) ** 2 - (1 - r["pair_p"]) ** 2 for r in rs]  # noqa: E731
    b4 = lambda rs: boot_ci(se(rs))[1] < 0.25 - EPS  # noqa: E731
    b5 = lambda rs: boot_ci(d_up(rs))[1] < -EPS and boot_ci(d_pair(rs))[1] < -EPS  # noqa: E731  combined label (F2)
    out = {"n_scored": len(rows), "summary": summarise(rows),
           "pair_rule": {"brier": sum((1 - r["pair_p"]) ** 2 for r in rows) / len(rows) if rows else None,
                         "bettor_minus_pair": sum(d_pair(rows)) / len(rows) if rows else None, "ci": boot_ci(d_pair(rows))},
           "bets": {}}
    for name, f in (("ss-b4", b4), ("ss-b5", b5)):
        if len(rows) < 60:
            out["bets"][name] = {"label": "untestable", "reason": f"{len(rows)} items scored, fewer than 60", "fragile_items": []}
            continue
        full = f(rows)
        flips = [rows[i]["id"] for i in range(len(rows)) if f(rows[:i] + rows[i + 1:]) != full]
        out["bets"][name] = {"label": "pass" if full else "null", "fragile_items": flips}
    out["bets"]["ss-b4"]["status"] = "withdrawn before data (design review: redesign, P3); descriptive secondary only"
    if len(rows) >= 60:
        for name, f in (("ss-b4", b4), ("ss-b5", b5)):
            full = out["bets"][name]["label"] == "pass"
            lofo = {}
            for fld in sorted({r["field"] for r in rows}):
                rest = [r for r in rows if r["field"] != fld]
                lofo[fld] = {"n": len(rest), "label": "untestable" if len(rest) < 60 else ("pass" if f(rest) else "null")}  # F6
            out["bets"][name]["leave_one_field_out"] = lofo
            out["bets"][name]["field_flips"] = [fld for fld, v in lofo.items() if v["label"] != "untestable" and (v["label"] == "pass") != full]
            if out["bets"][name]["fragile_items"] or out["bets"][name]["field_flips"]:   # F6
                out["bets"][name]["label_reported"] = f"{out['bets'][name]['label']}, fragile"
    groups = defaultdict(list)
    for r in rows:
        groups[r["field"]].append(r)
    out["by_field"] = {g: summarise(v) for g, v in sorted(groups.items())}
    out["calibration"] = calibration(rows)
    chk = {b["id"]: b for b in bets if b["kind"] == "order-check"}
    pairs = [(prim[i]["p_option_1"], chk[i]["p_option_1"]) for i in chk if i in prim]
    out["order_check"] = {"n": len(pairs),
                          "mean_incoherence": sum(abs(a + b - 100) for a, b in pairs) / len(pairs) if pairs else None,
                          "mean_first_shown_bonus": sum((a + b - 100) / 2 for a, b in pairs) / len(pairs) if pairs else None,
                          "first_shown_bonus_ci": boot_ci([(a + b - 100) / 2 for a, b in pairs]),
                          "same_side_rate": sum(1 for a, b in pairs if (a - 50) * (50 - b) > 0) / len(pairs) if pairs else None}
    out["rows"] = rows
    return out


def tables_r2(s):
    m = s["summary"]
    L = ["# Round 2 scores (generated by scoring/score.py --r2; do not edit by hand)", "",
         f"Template items scored: {s['n_scored']}. Brier **{fmt(m['brier'])}** [{fmt(m['brier_ci'][0])}, {fmt(m['brier_ci'][1])}], "
         f"accuracy {fmt(m['accuracy'], 2)}. Up-word rule Brier {fmt(m['headline_brier'])}; bettor − rule {fmt(m['minus_headline'])} "
         f"[{fmt(m['minus_headline_ci'][0])}, {fmt(m['minus_headline_ci'][1])}].", ""]
    for b, v in s["bets"].items():
        L.append(f"- {b}: **{v.get('label_reported', v['label'])}**" + (f" ({v['reason']})" if v.get("reason") else "")
                 + (f"; item flips: {', '.join(v['fragile_items'])}" if v.get("fragile_items") else "; no single item flips it")
                 + (f"; query-bucket flips: {', '.join(v['field_flips'])}" if v.get("field_flips") else "; no single query bucket flips it" if "field_flips" in v else "")
                 + ("; untestable without: " + ", ".join(k for k, x in v.get("leave_one_field_out", {}).items() if x["label"] == "untestable")
                    if any(x["label"] == "untestable" for x in v.get("leave_one_field_out", {}).values()) else "")
                 + (f" [{v['status']}]" if v.get("status") else ""))
    L += [f"Swap-pair rule Brier {fmt(s['pair_rule']['brier'])}; bettor − rule {fmt(s['pair_rule']['bettor_minus_pair'])} [{fmt(s['pair_rule']['ci'][0])}, {fmt(s['pair_rule']['ci'][1])}].",
          "", "Secondary (against the up-word rule only; not the ss-b5 test):", "", "| query bucket | n | Brier | 95% CI | accuracy | up-word rule Brier | bettor − rule [95% CI] |", "|---|---|---|---|---|---|---|"]
    for g, v in s["by_field"].items():
        L.append(f"| {g} | {v['n']} | {fmt(v['brier'])} | [{fmt(v['brier_ci'][0])}, {fmt(v['brier_ci'][1])}] | {fmt(v['accuracy'], 2)} | "
                 f"{fmt(v['headline_brier'])} | {fmt(v['minus_headline'])} [{fmt(v['minus_headline_ci'][0])}, {fmt(v['minus_headline_ci'][1])}] |")
    L += ["", "| confidence bucket | n | mean confidence | share right |", "|---|---|---|---|"]
    L += [f"| {c['bucket']} | {c['n']} | {fmt(c['mean_conf'], 2)} | {fmt(c['hit_rate'], 2)} |" for c in s["calibration"]]
    oc = s["order_check"]
    L += ["", f"Order check: {oc['n']} items; mean |p + p' − 100| = {fmt(oc['mean_incoherence'], 1)}; first-shown pull "
          f"{fmt(oc['mean_first_shown_bonus'], 1)} [{fmt(oc['first_shown_bonus_ci'][0], 1)}, {fmt(oc['first_shown_bonus_ci'][1], 1)}]; "
          f"same side both times {fmt(oc['same_side_rate'], 2)}.", ""]
    return "\n".join(L)


def synthetic_r2(items, kind):
    rng = random.Random(1)
    bets = []
    for iid, it in items.items():
        o1 = rng.choice("ab")
        t1 = o1 == it["true_option"]
        p = {"coin": 50, "oracle": 90 if t1 else 10, "anti": 10 if t1 else 90,
             "upword": 75 if it["up_side"] == o1 else 25,
             "swappair": round(100 * (SWAP_PAIR_P.get(swap_pair(it), PAIR_PRIOR) if it["up_side"] == o1 else 1 - SWAP_PAIR_P.get(swap_pair(it), PAIR_PRIOR))),
             "onefield": (90 if t1 else 10) if it["field"] == "model-psychology" else (75 if it["up_side"] == o1 else 25)}[kind]
        bets += [{"id": iid, "kind": "primary", "option_1_is": o1, "p_option_1": p},
                 {"id": iid, "kind": "order-check", "option_1_is": "b" if o1 == "a" else "a", "p_option_1": 100 - p}]
    return bets


def main_r2():
    items = {it["id"]: it for it in (json.loads(l) for l in R2_ITEMS.read_text().splitlines() if l.strip())}
    if "--synthetic" in sys.argv:
        kind = sys.argv[sys.argv.index("--synthetic") + 1]
        s = score_r2(items, synthetic_r2(items, kind))
        print(kind, "Brier", fmt(s["summary"]["brier"]), {b: (v.get("label_reported", v["label"]), v.get("field_flips")) for b, v in s["bets"].items()})
        return
    s = score_r2(items, [json.loads(l) for l in R2_BETS.read_text().splitlines() if l.strip()])
    (ROOT / "scoring" / "r2-scores.json").write_text(json.dumps(s, indent=1))
    (ROOT / "scoring" / "r2-tables.md").write_text(tables_r2(s))
    print(tables_r2(s))


# ---------------- ss-b6: valence comparator (experiments/ss-b6.md; design review ss-b6 F2-F5, D33-D36) ----------------
R2_VALENCE = ROOT / "bettor" / "r2-valence.jsonl"
G3_RE = re.compile(r"\b(original|real|actual|actually|published|authentic|genuine|abstract|plausib\w*|edited|altered|modified|likely (?:the )?(?:reported|written|true))\b", re.I)


def _lg(p):
    p = min(0.99, max(0.01, p))
    return math.log(p / (1 - p))


def _fit(X, y, iters=50, ridge=1e-3):
    """Logistic regression, no intercept, Newton's method (reference: the reviewer's sim_b6_fair.fit)."""
    w = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ w))
        g = X.T @ (y - p) - ridge * w
        H = -(X.T * (p * (1 - p))) @ X - ridge * np.eye(len(w))
        w -= np.linalg.solve(H, g)
    return w


def _feats(p1, up):
    return [_lg(p1 / 100), up, up * (1.0 if abs(p1 - 50) <= 5 else 0.0)]


def _loo(X, y):
    n = len(y)
    return np.array([1 / (1 + math.exp(-X[i] @ _fit(X[np.arange(n) != i], y[np.arange(n) != i]))) for i in range(n)])


def score_b6(items, bets, valence, gate_g1=True):
    prim = {b["id"]: b for b in bets if b["kind"] == "primary"}
    val = {v["id"]: v for v in valence}
    ids = sorted(set(prim) & set(val))
    rows = []
    for iid in ids:
        it, b, v = items[iid], prim[iid], val[iid]
        assert v["option_1_is"] == b["option_1_is"], iid
        o1 = b["option_1_is"]
        rows.append({"id": iid, "field": it["field"], "down": it["up_side"] != it["true_option"],
                     "y": 1.0 if o1 == it["true_option"] else 0.0, "up": 1.0 if it["up_side"] == o1 else -1.0,
                     "pb": b["p_option_1"], "pv": v["p_option_1"], "p_true": p_true_of(b, it), "v_true": p_true_of(v, it),
                     "rationale": v.get("rationale", "")})
    mean = lambda v: float(sum(v) / len(v)) if len(v) else None  # noqa: E731
    out = {"n": len(rows), "missing": sorted(set(prim) - set(val))}
    # gates (F3): no answer labels used
    nz = [r for r in rows if r["pv"] != 50]
    share_up = mean([1.0 if (r["pv"] > 50) == (r["up"] > 0) else 0.0 for r in nz]) if nz else None
    g3 = sum(1 for r in rows if G3_RE.search(r["rationale"] or ""))
    out["gates"] = {"G1_share_up": share_up, "G1_n": len(nz), "G1_x": sum(1 for r in nz if (r["pv"] > 50) == (r["up"] > 0)),
                    "G3_matches": g3}
    if len(rows) < 60:
        out["label"], out["reason"] = "untestable", f"{len(rows)} items with both ratings, fewer than 60"
        out["sentence"] = f"Too few valence ratings were returned to test it ({len(rows)} of 92; {out['reason']})."
        return out
    if gate_g1 and share_up is not None and share_up < 0.50:   # ss-b7 calls with gate_g1=False (D40)
        out["label"], out["reason"] = "untestable", "G1: rater favoured the up word on fewer than half the non-50 ratings"
        out["sentence"] = (f"The valence rater favoured the up word on only {out['gates']['G1_x']} of {len(nz)} items, which suggests it "
                           "misread the scale, so the comparison was not run as a test.")
        return out
    # leg 1: raw paired Brier (frozen); leg 2: both sides recalibrated by the same leave-one-out logistic (F2)
    d1 = np.array([(1 - r["p_true"]) ** 2 - (1 - r["v_true"]) ** 2 for r in rows])
    y = np.array([r["y"] for r in rows])
    Xb = np.array([_feats(r["pb"], r["up"]) for r in rows])
    Xv = np.array([_feats(r["pv"], r["up"]) for r in rows])
    pb, pv = _loo(Xb, y), _loo(Xv, y)
    d2 = (y - pb) ** 2 - (y - pv) ** 2
    out["leg1"] = {"d": mean(d1), "ci": boot_ci(list(d1)), "bettor_brier": mean([(1 - r["p_true"]) ** 2 for r in rows]),
                   "valence_brier": mean([(1 - r["v_true"]) ** 2 for r in rows]),
                   "valence_accuracy": mean([1 if r["v_true"] > 0.5 else 0.5 if r["v_true"] == 0.5 else 0 for r in rows])}
    out["leg2"] = {"d": mean(d2), "ci": boot_ci(list(d2)), "bettor_recal_brier": float(((y - pb) ** 2).mean()),
                   "rival_recal_brier": float(((y - pv) ** 2).mean())}
    lab = lambda a, b: boot_ci(list(a))[1] < -EPS and boot_ci(list(b))[1] < -EPS  # noqa: E731  both legs, rows dropped, no refit
    full = lab(d1, d2)
    out["label"] = "pass" if full else "null"
    out["null_legs"] = [n for n, d in (("raw", d1), ("recalibrated", d2)) if not boot_ci(list(d))[1] < -EPS]
    idx = np.arange(len(rows))
    out["fragile_items"] = [rows[i]["id"] for i in idx if lab(d1[idx != i], d2[idx != i]) != full]
    lofo = {}
    for fld in sorted({r["field"] for r in rows}):
        keep = np.array([r["field"] != fld for r in rows])
        lofo[fld] = {"n": int(keep.sum()), "label": "untestable" if keep.sum() < 60 else ("pass" if lab(d1[keep], d2[keep]) else "null")}
    out["leave_one_bucket_out"] = lofo
    out["bucket_flips"] = [k for k, v in lofo.items() if v["label"] != "untestable" and (v["label"] == "pass") != full]
    # F4: down-word split on leg 2, greedy flip count, discordant-pair sign test (secondary)
    dn = np.array([r["down"] for r in rows])
    out["leg2_up_word"] = {"n": int((~dn).sum()), "d": mean(d2[~dn]), "ci": boot_ci(list(d2[~dn]))}
    out["leg2_down_word"] = {"n": int(dn.sum()), "d": mean(d2[dn]), "ci": boot_ci(list(d2[dn]))}
    greedy = None
    if boot_ci(list(d2))[1] < -EPS:
        order = np.argsort(d2)                      # most negative = largest bettor advantage first
        for k in range(1, len(order)):
            rest = np.delete(d2, order[:k])
            if boot_ci(list(rest))[1] >= 0:
                greedy = {"k": int(k), "down_word": int(dn[order[:k]].sum())}
                break
    out["greedy_flip"] = greedy
    disc, b_right = 0, 0
    for r in rows:
        if r["pb"] == 50:
            continue
        b_fav = 1 if r["pb"] > 50 else 2
        r_fav = (1 if r["pv"] > 50 else 2) if abs(r["pv"] - 50) > 5 else (1 if r["up"] > 0 else 2)
        if b_fav != r_fav:
            disc += 1
            b_right += 1 if (b_fav == 1) == (r["y"] == 1) else 0
    from math import comb
    p_sign = sum(comb(disc, j) for j in range(b_right, disc + 1)) / 2 ** disc if disc else None
    out["discordant"] = {"n": disc, "bettor_right": b_right, "one_sided_sign_p": p_sign}
    # D39 (audit ss-b6 cut 8 and recommendation): pre-registered secondaries regenerated here, not copied
    acc = lambda vs: [1.0 if v > 0.5 else 0.5 if v == 0.5 else 0.0 for v in vs]  # noqa: E731
    out["secondaries"] = {
        "bettor_brier_ci": boot_ci([(1 - r["p_true"]) ** 2 for r in rows]),
        "valence_brier_ci": boot_ci([(1 - r["v_true"]) ** 2 for r in rows]),
        "valence_accuracy_ci": boot_ci(acc([r["v_true"] for r in rows])),
        "leg1_up_word": {"n": int((~dn).sum()), "d": mean(d1[~dn]), "ci": boot_ci(list(d1[~dn]))},
        "leg1_down_word": {"n": int(dn.sum()), "d": mean(d1[dn]), "ci": boot_ci(list(d1[dn]))}}
    opp = [r["id"] for r in rows if r["pv"] != 50 and r["pb"] != 50 and (r["pb"] > 50) != (r["pv"] > 50)]
    half = [r["id"] for r in rows if r["pv"] == 50]
    sel = np.array([r["id"] in set(opp) | set(half) for r in rows])
    out["secondaries"]["opposite_sides"] = {
        "items": opp, "bettor_right": sum(1 for r in rows if r["id"] in opp and (r["pb"] > 50) == (r["y"] == 1)),
        "rater_at_50": half, "share_of_leg1_gap": float(d1[sel].sum() / d1.sum()) if d1.sum() else None}
    Xb2 = np.array([_feats(r["pb"], r["up"])[:2] for r in rows])
    Xv2 = np.array([_feats(r["pv"], r["up"])[:2] for r in rows])
    d2b = (y - _loo(Xb2, y)) ** 2 - (y - _loo(Xv2, y)) ** 2
    out["secondaries"]["leg2_without_near50_term"] = {"d": mean(d2b), "ci": boot_ci(list(d2b))}
    # F5 sentences with qualifiers in the order G2, G3, down-word, greedy, fragile
    f3 = lambda c: f"[{c[0]:.3f}, {c[1]:.3f}]"  # noqa: E731
    if full:
        sent = (f"On {len(rows)} round-2 sentence pairs, the bettor picked the published sentence better than the same model asked only which version "
                f"is better news for the paper's own method (raw: d₁ {out['leg1']['d']:.3f} {f3(out['leg1']['ci'])}, valence rule Brier "
                f"{out['leg1']['valence_brier']:.3f}), and better than that rating combined with the up word once both were recalibrated the same way "
                f"(d₂ {out['leg2']['d']:.3f} {f3(out['leg2']['ci'])}). Round 2's pass is not only picking the flattering version, as this rater judged it, or the up word, though "
                "this does not separate knowing the result from reasoning within the sentence, and the rater was the same model as the bettor")
    else:
        sent = (f"On {len(rows)} round-2 sentence pairs, the bettor was not shown to pick the published sentence better than the same model asked only "
                f"which version is better news for the paper's own method (raw d₁ {out['leg1']['d']:.3f} {f3(out['leg1']['ci'])}; recalibrated with "
                f"the up word d₂ {out['leg2']['d']:.3f} {f3(out['leg2']['ci'])}; null on: {', '.join(out['null_legs'])}). Round 2's pass may reduce to "
                "picking the flattering version, or the rater, being the same model, may have used the same judgment of which version is real; "
                "this test cannot tell those apart")
    if share_up is not None and share_up >= 0.95:
        sent += (f"; the valence rater favoured the up word on {out['gates']['G1_x']} of {len(nz)} items, so it behaved almost as the up-word "
                 "rule and this result largely repeats ss-b5")
    if not full and g3 >= 10:
        sent += (f"; in {g3} of {len(rows)} rationales the rater reasoned about which version is real, so it may share the bettor's judgment, "
                 "and this null does not show the pass reduces to flattery")
    nu, nd = out["leg2_up_word"]["n"], out["leg2_down_word"]["n"]
    if full and out["leg2_up_word"]["ci"][0] is not None and out["leg2_up_word"]["ci"][0] > 0:
        sent += (f"; on the {nu} up-word items the bettor was worse than the comparator (d {out['leg2_up_word']['d']:.3f} "
                 f"{f3(out['leg2_up_word']['ci'])}), so the pass rests on the {nd} down-word items")
    if full and greedy:
        k = greedy["k"]
        which = (f"{greedy['down_word']} of them down-word" if k != 1 else ("a down-word item" if greedy["down_word"] else "an up-word item"))
        sent += f"; removing {k} chosen item{'s' if k != 1 else ''} ({which}) would flip it"
    if out["fragile_items"] or out["bucket_flips"]:          # D37 (N3): name items and buckets; plural agreement
        out["label_reported"] = f"{out['label']}, fragile"
        parts = []
        if out["fragile_items"]:
            fi = out["fragile_items"]
            parts.append(f"the item{'s' if len(fi) > 1 else ''} {', '.join(fi)}")
        if out["bucket_flips"]:
            bf = out["bucket_flips"]
            parts.append(f"the query bucket{'s' if len(bf) > 1 else ''} {', '.join(bf)}")
        many = len(out["fragile_items"]) + len(out["bucket_flips"]) > 1
        sent += (f"; this label rests on {' and '.join(parts)}: without {'any one of them' if many else 'it'} "
                 f"the label would be {'null' if full else 'pass'}")
    out["sentence"] = sent + "."
    out["rows"] = [{k: v for k, v in r.items() if k != "rationale"} for r in rows]
    return out


def synthetic_valence(items, prim, kind):
    val = []
    for b in prim:
        it, o1 = items[b["id"]], b["option_1_is"]
        t1, up1 = o1 == it["true_option"], it["up_side"] == o1
        pair_up = SWAP_PAIR_P.get(swap_pair(it), PAIR_PRIOR)
        v50 = b["p_option_1"] if (b["p_option_1"] >= 70 or b["p_option_1"] <= 30) else 50
        p = {"coin": 50, "copy": b["p_option_1"], "oracle": 90 if t1 else 10, "upword": 75 if up1 else 25,
             "alwaysup99": 99 if up1 else 1, "swappair": round(100 * (pair_up if up1 else 1 - pair_up)),
             "valence50": v50, "inverted": 100 - v50}[kind]
        val.append({"id": b["id"], "kind": "valence", "option_1_is": o1, "p_option_1": p, "rationale": ""})
    return val


def rater_noise(bets):
    """D38: test-retest on the 46 order-check items, options reversed. For the valence rater and, on the same items, the bettor:
    mean |p + p' - 100| (0 = perfectly consistent) and the share choosing the same side both times."""
    p = ROOT / "bettor" / "r2-valence-retest.jsonl"
    if not p.exists():
        return None
    val = {v["id"]: v for v in (json.loads(l) for l in R2_VALENCE.read_text().splitlines() if l.strip())}
    ret = {v["id"]: v for v in (json.loads(l) for l in p.read_text().splitlines() if l.strip())}
    prim = {b["id"]: b for b in bets if b["kind"] == "primary"}
    chk = {b["id"]: b for b in bets if b["kind"] == "order-check"}

    def stats(a, b, ids):
        pairs = [(a[i]["p_option_1"], b[i]["p_option_1"]) for i in ids]
        inc = [abs(x + y - 100) for x, y in pairs]
        return {"n": len(pairs), "mean_abs_incoherence": sum(inc) / len(inc) if inc else None,
                "incoherence_ci": boot_ci(inc) if inc else None,
                "same_side": sum(1 for x, y in pairs if (x - 50) * (50 - y) > 0) / len(pairs) if pairs else None}
    ids = sorted(set(val) & set(ret))
    both = [i for i in ids if i in prim and i in chk]
    diff = [abs(val[i]["p_option_1"] + ret[i]["p_option_1"] - 100) - abs(prim[i]["p_option_1"] + chk[i]["p_option_1"] - 100) for i in both]
    return {"rater": stats(val, ret, ids), "bettor_same_items": stats(prim, chk, both),
            "paired_incoherence_diff": {"d": sum(diff) / len(diff) if diff else None, "ci": boot_ci(diff) if diff else None}}  # D39


def main_b6():
    items = {it["id"]: it for it in (json.loads(l) for l in R2_ITEMS.read_text().splitlines() if l.strip())}
    bets = [json.loads(l) for l in R2_BETS.read_text().splitlines() if l.strip()]
    if "--synthetic" in sys.argv:
        prim = [b for b in bets if b["kind"] == "primary"]
        kinds = [k for k in sys.argv[sys.argv.index("--synthetic") + 1:] if not k.startswith("--")] or ["coin"]
        for kind in kinds:
            s = score_b6(items, bets, synthetic_valence(items, prim, kind))
            if "leg1" not in s:
                print(f"{kind:11s} {s['label']}: {s.get('reason')}")
                continue
            print(f"{kind:11s} leg1 {s['leg1']['d']:+.3f} [{s['leg1']['ci'][0]:+.3f},{s['leg1']['ci'][1]:+.3f}]  "
                  f"leg2 {s['leg2']['d']:+.3f} [{s['leg2']['ci'][0]:+.3f},{s['leg2']['ci'][1]:+.3f}]  -> {s.get('label_reported', s['label'])}"
                  f"  G1 {s['gates']['G1_share_up']}  greedy {s['greedy_flip']}")
            if "--sentences" in sys.argv:
                print("   ", s["sentence"])
        return
    s = score_b6(items, bets, [json.loads(l) for l in R2_VALENCE.read_text().splitlines() if l.strip()])
    s["rater_noise"] = rater_noise(bets)          # D38: reported secondary; does not change the verdict rule
    (ROOT / "scoring" / "b6-scores.json").write_text(json.dumps(s, indent=1))
    print(json.dumps({k: v for k, v in s.items() if k != "rows"}, indent=1))




# ---------------- ss-b7: the publishability ("more striking finding") rater, with a P12 margin (experiments/ss-b7.md; D40-D45) ----------------
R2_STRIKING = ROOT / "bettor" / "r2-striking.jsonl"
R2_STRIKING_RETEST = ROOT / "bettor" / "r2-striking-retest.jsonl"
N_NULL, NULL_BOOT, NULL_Q, MIN_RETEST, N_SEEDS = 100, 2000, 0.10, 30, 20
SCOPE_B7 = ("Both the bettor and the rater ran as claude-opus-5-5 with adaptive thinking at effort low, with reasoning hidden; "
            "the result is about that setting.")
BUNDLE = "(shown only the field and the two sentences, not the question or methods)"


def retest_sigma(rat, ret):
    """Single-rating logit noise from test-retest pairs (options reversed): SD of [logit(v) - logit(1 - v')] / sqrt(2)."""
    dd = [_lg(rat[i]["p_option_1"] / 100) - _lg((100 - ret[i]["p_option_1"]) / 100) for i in ret if i in rat]
    return (float(np.std(dd) / math.sqrt(2)) if len(dd) > 1 else None), len(dd)


def _ub(d, idx=None, seed=BOOT_SEED, n=NULL_BOOT):
    v = d if idx is None else d[idx]
    return boot_ci(list(v), n=n, seed=seed)[1]


def null_sims(rows, sigma, seed=BOOT_SEED):
    """Null world A (P12): the rater differs from the bettor only by its own call-to-call noise: rater = logit(bettor) + N(0, sigma).
    Returns the stored d2 vectors (one per simulation), so subsets can drop rows without refitting (D42)."""
    y = np.array([r["y"] for r in rows]); up = np.array([r["up"] for r in rows]); pb = np.array([r["pb"] for r in rows], float)
    lb = np.array([_lg(p / 100) for p in pb])
    pbl = _loo(np.array([_feats(p, u) for p, u in zip(pb, up)]), y)
    rng, D = np.random.default_rng(seed), []
    for _ in range(N_NULL):
        pr = np.clip(np.round(100 / (1 + np.exp(-(lb + rng.normal(0, sigma, len(lb)))))), 1, 99)
        D.append((y - pbl) ** 2 - (y - _loo(np.array([_feats(p, u) for p, u in zip(pr, up)]), y)) ** 2)
    return np.array(D)


def margin_of(D, keep=None, seed=BOOT_SEED):
    ups = [_ub(d, keep, seed=seed) for d in D]
    return float(np.quantile(ups, NULL_Q)), ups


def world_b_rate(rows, sigma_rt, sigma_dis, m, seed=BOOT_SEED, draws=100):
    """D43: P(pass) of this rule in world B, where the rater differs from the bettor by stable item noise sqrt(sigma_dis^2 - sigma_rt^2)
    plus call noise sigma_rt."""
    y = np.array([r["y"] for r in rows]); up = np.array([r["up"] for r in rows]); pb = np.array([r["pb"] for r in rows], float)
    lb = np.array([_lg(p / 100) for p in pb]); p_true_b = np.array([r["p_true"] for r in rows])
    pbl = _loo(np.array([_feats(p, u) for p, u in zip(pb, up)]), y)
    s_item = math.sqrt(max(sigma_dis ** 2 - sigma_rt ** 2, 0.0))
    rng, hits = np.random.default_rng(seed), 0
    for _ in range(draws):
        pr = np.clip(np.round(100 / (1 + np.exp(-(lb + rng.normal(0, s_item, len(lb)) + rng.normal(0, sigma_rt, len(lb)))))), 1, 99)
        v_true = np.where(y == 1, pr / 100, 1 - pr / 100)
        d1 = (1 - p_true_b) ** 2 - (1 - v_true) ** 2
        d2 = (y - pbl) ** 2 - (y - _loo(np.array([_feats(p, u) for p, u in zip(pr, up)]), y)) ** 2
        hits += (_ub(d1, n=BOOT_N) < -EPS) and (_ub(d2, n=BOOT_N) < m - EPS)
    return hits / draws


def score_b7(items, bets, rater, retest, seed_check=True):
    base = score_b6(items, bets, rater, gate_g1=False)          # D40: G1-G3 are reported counts here, never gates
    out = {k: base.get(k) for k in ("n", "missing", "gates", "leg1", "leg2", "leg2_up_word", "leg2_down_word", "discordant", "secondaries")}
    out["scope"] = SCOPE_B7
    if base["n"] < 60 or "leg1" not in base:
        out["label"] = "untestable"
        out["sentence"] = f"Too few ratings were returned to test it ({base['n']} of 92)."
        return out
    rows = base["rows"]
    sigma, npairs = retest_sigma({v["id"]: v for v in rater}, {v["id"]: v for v in retest})
    out["sigma_retest"], out["retest_pairs"] = sigma, npairs
    if npairs < MIN_RETEST or sigma is None:                       # D41: the one rule for a missing or partial retest
        out["label"] = "untestable"
        out["sentence"] = (f"The rater's retest returned only {npairs} of 46 pairs (at least {MIN_RETEST} are needed), so the rater's "
                           "call-to-call noise margin could not be set and the comparison was not run as a test.")
        return out
    y = np.array([r["y"] for r in rows])
    d1 = np.array([(1 - r["p_true"]) ** 2 - (1 - r["v_true"]) ** 2 for r in rows])
    pb = _loo(np.array([_feats(r["pb"], r["up"]) for r in rows]), y); pv = _loo(np.array([_feats(r["pv"], r["up"]) for r in rows]), y)
    d2 = (y - pb) ** 2 - (y - pv) ** 2
    D = null_sims(rows, sigma)
    m, ups = margin_of(D)
    out["margin"], out["null_false_pass_at_0"] = m, float(np.mean(np.array(ups) < 0))
    lab = lambda keep, mm, sd=BOOT_SEED: (_ub(d1, keep, seed=sd, n=BOOT_N) < -EPS) and (_ub(d2, keep, seed=sd, n=BOOT_N) < mm - EPS)  # noqa: E731
    full = lab(None, m)
    out["label"] = "pass" if full else "null"
    other = "null" if full else "pass"
    n = len(rows); idx = np.arange(n)
    flips = []                                                    # D42.1: m* recomputed per subset from the stored null d2 vectors
    for i in range(n):
        keep = idx != i
        if lab(keep, margin_of(D, keep)[0]) != full:
            flips.append(rows[i]["id"])
    out["fragile_items"] = flips
    lofo = {}
    for fld in sorted({r["field"] for r in rows}):
        keep = np.array([r["field"] != fld for r in rows])
        lofo[fld] = {"n": int(keep.sum()), "label": "untestable" if keep.sum() < 60 else ("pass" if lab(keep, margin_of(D, keep)[0]) else "null")}
    out["leave_one_bucket_out"] = lofo
    out["bucket_flips"] = [k for k, v in lofo.items() if v["label"] != "untestable" and (v["label"] == "pass") != full]
    if seed_check:                                                # D42.2: the full label under 20 seeds, null draws included
        labs = []
        for k in range(N_SEEDS):
            sd = BOOT_SEED + 1 + k
            mk = margin_of(null_sims(rows, sigma, seed=sd), seed=sd)[0]
            labs.append("pass" if lab(None, mk, sd) else "null")
        out["seed_labels"] = labs
        out["seeds_other"] = sum(1 for x in labs if x != out["label"])
    # D43: sigma_dis and the world-B pass rate (reported secondaries)
    lb = np.array([_lg(r["pb"] / 100) for r in rows]); lv = np.array([_lg(r["pv"] / 100) for r in rows])
    out["sigma_dis"] = float(np.std(lv - lb))
    out["world_b_pass_rate"] = world_b_rate(rows, sigma, out["sigma_dis"], m)
    f3 = lambda c: f"[{c[0]:.3f}, {c[1]:.3f}]"  # noqa: E731
    L1, L2 = out["leg1"], out["leg2"]
    rater_phrase = f"the same model asked only which version reports the more striking finding {BUNDLE}"
    if full:
        sent = (f"On {n} round-2 sentence pairs, the bettor picked the published sentence better than {rater_phrase} (raw d₁ {L1['d']:.3f} "
                f"{f3(L1['ci'])}, striking rule Brier {L1['valence_brier']:.3f}; recalibrated with the up word d₂ {L2['d']:.3f} {f3(L2['ci'])}, "
                f"beyond the rater's call-to-call noise margin {m:.4f}). Round 2's pass is not only picking the more striking version, as this "
                "rater judged it, though this does not separate knowing the result from reasoning within the sentence, and the rater was the "
                "same model as the bettor")
        sent += (f"; a bettor that differed from this rater only by stable item-level noise of the observed size would pass this test about "
                 f"{round(100 * out['world_b_pass_rate'])}% of the time")
    else:
        sent = (f"On {n} round-2 sentence pairs, the bettor was not shown to pick the published sentence better than {rater_phrase} (raw d₁ "
                f"{L1['d']:.3f} {f3(L1['ci'])}; recalibrated with the up word d₂ {L2['d']:.3f} {f3(L2['ci'])}, against the rater's call-to-call "
                f"noise margin {m:.4f}). Round 2's pass may reduce to picking the more striking version, or the rater, being the same model, may "
                "have used the same judgment of which version is real; this test cannot tell those apart")
    if seed_check and out["seeds_other"]:
        out["label_reported"] = f"{out['label']}, at the margin ({out['seeds_other']} of {N_SEEDS} seeds give {other})"
    if flips or out["bucket_flips"]:
        out["label_reported"] = (out.get("label_reported") or out["label"]) + ", fragile"
        if flips and len(flips) > 5:
            sent += f"; this label sits at the margin: {len(flips)} of {n} single-item removals would make it {other}"
        else:
            parts = []
            if flips:
                parts.append(f"the item{'s' if len(flips) > 1 else ''} {', '.join(flips)}")
            if out["bucket_flips"]:
                bf = out["bucket_flips"]; parts.append(f"the query bucket{'s' if len(bf) > 1 else ''} {', '.join(bf)}")
            many = len(flips) + len(out["bucket_flips"]) > 1
            sent += f"; this label rests on {' and '.join(parts)}: without {'any one of them' if many else 'it'} the label would be {other}"
    out["sentence"] = sent + "."
    out["verdict_reported"] = ("pass, unreplicated" if full else "null") + (" (" + out["label_reported"] + ")" if out.get("label_reported") else "")
    return out


def main_b7():
    items = {it["id"]: it for it in (json.loads(l) for l in R2_ITEMS.read_text().splitlines() if l.strip())}
    bets = [json.loads(l) for l in R2_BETS.read_text().splitlines() if l.strip()]
    load = lambda p: [json.loads(l) for l in p.read_text().splitlines() if l.strip()] if p.exists() else []  # noqa: E731  D41: no crash
    if "--synthetic" in sys.argv:
        prim = [b for b in bets if b["kind"] == "primary"]
        chk = {b["id"] for b in bets if b["kind"] == "order-check"}
        rng = np.random.default_rng(7)
        for kind in [k for k in sys.argv[sys.argv.index("--synthetic") + 1:] if not k.startswith("--")]:
            base_kind = kind.split("+")[0]
            sig = float(kind.split("+")[1]) if "+" in kind else 0.0
            if base_kind.startswith("down"):            # D40: down-word raters, 70 on the down word on a share of items
                share = float(base_kind[4:]) / 100
                clean = []
                for b in prim:
                    it, o1 = items[b["id"]], b["option_1_is"]
                    down1 = it["up_side"] != o1
                    p = (70 if down1 else 30) if rng.random() < share else (30 if down1 else 70)
                    clean.append({"id": b["id"], "kind": "striking", "option_1_is": o1, "p_option_1": p, "rationale": ""})
            else:
                clean = synthetic_valence(items, prim, base_kind)

            def noisy(v):                                # D44: fresh call noise on the clean value for each call
                if sig == 0 or v["p_option_1"] == 50:
                    return v["p_option_1"]
                return int(np.clip(round(100 / (1 + math.exp(-(_lg(v["p_option_1"] / 100) + rng.normal(0, sig))))), 1, 99))
            rat = [dict(v, p_option_1=noisy(v)) for v in clean]
            ret = [dict(v, option_1_is="b" if v["option_1_is"] == "a" else "a", p_option_1=100 - noisy(v)) for v in clean if v["id"] in chk]
            s = score_b7(items, bets, rat, ret, seed_check="--seeds" in sys.argv)
            mg = s.get("margin")
            print(f"{kind:12s} sigma_rt {s.get('sigma_retest') if s.get('sigma_retest') is None else round(s['sigma_retest'], 3)}  "
                  f"m* {mg if mg is None else round(mg, 4)}  leg2 ub {round(s['leg2']['ci'][1], 4) if s.get('leg2') else None}  "
                  f"worldB {s.get('world_b_pass_rate')}  -> {s.get('label_reported', s['label'])}")
        return
    s = score_b7(items, bets, load(R2_STRIKING), load(R2_STRIKING_RETEST))
    (ROOT / "scoring" / "b7-scores.json").write_text(json.dumps(s, indent=1))
    print(json.dumps(s, indent=1))


if __name__ == "__main__":
    (main_b7() if "--b7" in sys.argv else main_b6() if "--b6" in sys.argv else main_r2() if "--r2" in sys.argv else main())

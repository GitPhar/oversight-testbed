"""Score the bettor against the published record (pre-registration §4-§5). No model calls.

    python3 scoring/score.py                       # real bets -> scoring/scores.json, scoring/tables.md
    python3 scoring/score.py --synthetic <kind>    # dry run on synthetic bets: coin | oracle | headline | anti

p_true = the bettor's probability on the option the paper reported (p_option_1 if Option 1 was the reported one, else
1 - p_option_1). Brier = mean over items of (1 - p_true)^2; a constant 0.5 scores 0.25. Unit of analysis: items.
"""
import json
import random
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
                         "clipped": not (1 <= b["p_option_1"] <= 99)})
    labels = bet_labels(rows, [])
    out = {"n_scored": len(rows), "summary": summarise(rows),
           "bets": {"ss-b4": labels["ss-b1"], "ss-b5": labels["ss-b2"]}}
    if len(rows) >= 60:
        se = lambda rs: [(1 - r["p_true"]) ** 2 for r in rs]  # noqa: E731
        dif = lambda rs: [(1 - r["p_true"]) ** 2 - (1 - r["headline_p"]) ** 2 for r in rs]  # noqa: E731
        for name, f, full in (("ss-b4", lambda rs: boot_ci(se(rs))[1] < 0.25 - EPS, labels["ss-b1"]["label"] == "pass"),
                              ("ss-b5", lambda rs: boot_ci(dif(rs))[1] < -EPS, labels["ss-b2"]["label"] == "pass")):
            out["bets"][name]["leave_one_field_out"] = {
                fld: {"n": len(rest), "label": "pass" if f(rest) else "null"}
                for fld in sorted({r["field"] for r in rows}) for rest in [[r for r in rows if r["field"] != fld]]}
            out["bets"][name]["field_flips"] = [fld for fld, v in out["bets"][name]["leave_one_field_out"].items()
                                                if (v["label"] == "pass") != full]
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
                 + (f"; field flips: {', '.join(v['field_flips'])}" if v.get("field_flips") else "; no single field flips it" if "field_flips" in v else ""))
    L += ["", "| field | n | Brier | 95% CI | accuracy | up-word rule Brier | bettor − rule [95% CI] |", "|---|---|---|---|---|---|---|"]
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
             "upword": 75 if it["up_side"] == o1 else 25}[kind]
        bets += [{"id": iid, "kind": "primary", "option_1_is": o1, "p_option_1": p},
                 {"id": iid, "kind": "order-check", "option_1_is": "b" if o1 == "a" else "a", "p_option_1": 100 - p}]
    return bets


def main_r2():
    items = {it["id"]: it for it in (json.loads(l) for l in R2_ITEMS.read_text().splitlines() if l.strip())}
    if "--synthetic" in sys.argv:
        kind = sys.argv[sys.argv.index("--synthetic") + 1]
        s = score_r2(items, synthetic_r2(items, kind))
        print(kind, "Brier", fmt(s["summary"]["brier"]), {b: (v["label"], v.get("field_flips")) for b, v in s["bets"].items()})
        return
    s = score_r2(items, [json.loads(l) for l in R2_BETS.read_text().splitlines() if l.strip()])
    (ROOT / "scoring" / "r2-scores.json").write_text(json.dumps(s, indent=1))
    (ROOT / "scoring" / "r2-tables.md").write_text(tables_r2(s))
    print(tables_r2(s))


if __name__ == "__main__":
    main_r2() if "--r2" in sys.argv else main()

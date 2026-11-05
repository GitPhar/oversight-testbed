"""Score ss-b11 (experiments/ss-b11.md; direction ss-f3): does the round-1 bettor beat a field-aware baseline?
Archive only: items/items.jsonl and bettor/bets.jsonl (Opus, ss-b1's run). No model calls; numpy only.

    python3 scoring/score_f3.py                          # -> scoring/f3-scores.json, scoring/f3-tables.md
    python3 scoring/score_f3.py --synthetic <world>      # dry run on synthetic items and bets; never reads the archive
         worlds: skilled (bettor 76% right, field rates mild) | coin | fieldrule (the bettor IS the field rule)
                 | extreme (field up-rates 0.9/0.1, bettor mildly skilled)

The field-aware baseline (pre-registered, §4), on the 116 post-cutoff items:
  - tagged items (headline_side set): p(headline side) = (k_f + 4 r) / (n_f + 4), where n_f is the field's tagged items,
    k_f how many of them went the headline way, and r the pooled rate over all tagged post-cutoff items;
  - untagged items with an identifiable up option (the swapped word, in UP_WORDS): p(up option) = (u_f + 4 q) / (m_f + 4),
    from the field's untagged items with an up option, q pooled the same way;
  - every other item: 0.5.
  Rates are fitted on all 116 items, the scored item included (which favours the baseline); the leave-one-out variant is
  a reported secondary. Statistic: d = mean_i [(1 - p_bettor,i)^2 - (1 - p_base,i)^2], paired item bootstrap, 10,000,
  default_rng(20261104). Pass: upper bound < 0 (tolerance 1e-12).
"""
import difflib
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "items" / "items.jsonl"
BETS = ROOT / "bettor" / "bets.jsonl"
OUT_JSON = ROOT / "scoring" / "f3-scores.json"
OUT_MD = ROOT / "scoring" / "f3-tables.md"
BOOT_SEED, BOOT_N, EPS, SHRINK, MIN_N = 20261104, 10000, 1e-12, 4, 60
FLAT = 0.75   # ss-b2's publication-bias baseline, reported beside
UP_WORDS = {"higher", "high", "more", "larger", "greater", "bigger", "increased", "increase", "increases", "increasing",
            "rose", "rise", "rises", "stronger", "better", "faster", "longer", "above", "deeper", "improved", "improves",
            "improve", "outperformed", "outperforms", "outperform", "enhanced", "wider", "superior"}


def load(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def up_side(it):
    """'a' or 'b' if the first swapped word of that option is an up word, else None (answer-free: text only)."""
    a, b = it["option_a"].split(), it["option_b"].split()
    for t, i1, i2, j1, j2 in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
        if t != "equal":
            wa = a[i1].lower().strip(".,;:()") if i2 > i1 else ""
            wb = b[j1].lower().strip(".,;:()") if j2 > j1 else ""
            if wa in UP_WORDS and wb not in UP_WORDS:
                return "a"
            if wb in UP_WORDS and wa not in UP_WORDS:
                return "b"
            return None
    return None


def p_true_of(bet, it):
    p1 = min(99, max(1, bet["p_option_1"])) / 100
    return p1 if bet["option_1_is"] == it["true_option"] else 1 - p1


def baseline(items, leave_out=None):
    """p_true of the field-aware baseline for every item; with leave_out=i, item i's own label is excluded from every
    rate used for item i (the leave-one-out secondary)."""
    out = {}
    for it in items:
        i = it["id"]
        pool = [x for x in items if not (leave_out and x["id"] == i)]
        if it.get("headline_side") is not None:
            tag = [x for x in pool if x.get("headline_side") is not None]
            r = np.mean([x["true_option"] == x["headline_side"] for x in tag])
            f = [x for x in tag if x["field"] == it["field"]]
            p = (sum(x["true_option"] == x["headline_side"] for x in f) + SHRINK * r) / (len(f) + SHRINK)
            out[i] = p if it["true_option"] == it["headline_side"] else 1 - p
        elif it.get("_up") is not None:
            un = [x for x in pool if x.get("headline_side") is None and x.get("_up") is not None]
            q = np.mean([x["true_option"] == x["_up"] for x in un])
            f = [x for x in un if x["field"] == it["field"]]
            p = (sum(x["true_option"] == x["_up"] for x in f) + SHRINK * q) / (len(f) + SHRINK)
            out[i] = p if it["true_option"] == it["_up"] else 1 - p
        else:
            out[i] = 0.5
    return out


def flat(it):
    hs = it.get("headline_side")
    return 0.5 if hs is None else (FLAT if hs == it["true_option"] else 1 - FLAT)


def boot(v, n=BOOT_N, seed=BOOT_SEED):
    v = np.asarray(v, float)
    m = np.sort(v[np.random.default_rng(seed).integers(0, len(v), size=(n, len(v)))].mean(1))
    return (float(m[int(0.025 * n)]), float(m[int(0.975 * n) - 1]))


def r6(x):
    return None if x is None else round(float(x), 6)


def label_of(d):
    return "pass" if boot(d)[1] < 0 - EPS else "null"


def score(items_all, bets):
    prim = {b["id"]: b for b in bets if b["kind"] == "primary"}
    items = [dict(it) for it in items_all if it["side"] == "post" and it["id"] in prim]
    for it in items:
        it["_up"] = None if it.get("headline_side") is not None else up_side(it)
    s = {"bet": "ss-b11", "n": len(items)}
    if len(items) < MIN_N:
        s.update(label="untestable", sentence=f"Too few findings were scored to test the bettor ({len(items)} scored of 116).")
        return s
    pb = {it["id"]: p_true_of(prim[it["id"]], it) for it in items}
    base = baseline(items)
    ids = [it["id"] for it in items]
    d = [(1 - pb[i]) ** 2 - (1 - base[i]) ** 2 for i in ids]
    lo, hi = boot(d)
    s["bettor_brier"], s["bettor_brier_ci"] = r6(np.mean([(1 - pb[i]) ** 2 for i in ids])), [r6(x) for x in boot([(1 - pb[i]) ** 2 for i in ids])]
    s["base_brier"], s["base_brier_ci"] = r6(np.mean([(1 - base[i]) ** 2 for i in ids])), [r6(x) for x in boot([(1 - base[i]) ** 2 for i in ids])]
    s["flat_brier"] = r6(np.mean([(1 - flat(it)) ** 2 for it in items]))
    s["d"], s["d_ci"] = r6(np.mean(d)), [r6(lo), r6(hi)]
    s["label"] = "pass" if hi < 0 - EPS else "null"
    # composition of the baseline
    s["n_tagged"] = sum(it.get("headline_side") is not None for it in items)
    s["n_untagged_up"] = sum(it["_up"] is not None for it in items)
    s["n_half"] = len(items) - s["n_tagged"] - s["n_untagged_up"]
    fields = sorted({it["field"] for it in items})
    s["by_field"] = {}
    for f in fields:
        fi = [it for it in items if it["field"] == f]
        tg = [x for x in fi if x.get("headline_side") is not None]
        un = [x for x in fi if x["_up"] is not None]
        df = [(1 - pb[x["id"]]) ** 2 - (1 - base[x["id"]]) ** 2 for x in fi]
        s["by_field"][f] = {"n": len(fi), "tagged": len(tg), "headline_rate": r6(np.mean([x["true_option"] == x["headline_side"] for x in tg])) if tg else None,
                            "untagged_up": len(un), "up_rate": r6(np.mean([x["true_option"] == x["_up"] for x in un])) if un else None,
                            "bettor_brier": r6(np.mean([(1 - pb[x["id"]]) ** 2 for x in fi])),
                            "base_brier": r6(np.mean([(1 - base[x["id"]]) ** 2 for x in fi])), "d": r6(np.mean(df))}
    # robustness (§4): leave-one-item-out (baseline refitted without the item), leave-one-field-out, field jackknife
    flips = []
    for j in ids:
        rest = [it for it in items if it["id"] != j]
        bj = baseline(rest)
        dj = [(1 - pb[it["id"]]) ** 2 - (1 - bj[it["id"]]) ** 2 for it in rest]
        if label_of(dj) != s["label"]:
            flips.append(j)
    s["loo_flips"] = flips
    s["field_out"] = {}
    for f in fields:
        rest = [it for it in items if it["field"] != f]
        bf = baseline(rest)
        df = [(1 - pb[it["id"]]) ** 2 - (1 - bf[it["id"]]) ** 2 for it in rest]
        lo_f, hi_f = boot(df)
        s["field_out"][f] = {"n": len(rest), "d": r6(np.mean(df)), "ci": [r6(lo_f), r6(hi_f)], "label": "pass" if hi_f < 0 - EPS else "null"}
    jk = [s["field_out"][f]["d"] for f in fields]
    k = len(jk)
    se = float(np.sqrt((k - 1) / k * sum((x - np.mean(jk)) ** 2 for x in jk)))
    s["field_jackknife"] = {"clusters": k, "se": r6(se), "ci": [r6(s["d"] - 1.96 * se), r6(s["d"] + 1.96 * se)]}
    # secondary: the leave-one-out baseline (each item's own label excluded from its rates)
    bl = baseline(items, leave_out=True)
    dl = [(1 - pb[i]) ** 2 - (1 - bl[i]) ** 2 for i in ids]
    s["loo_baseline"] = {"brier": r6(np.mean([(1 - bl[i]) ** 2 for i in ids])), "d": r6(np.mean(dl)), "ci": [r6(x) for x in boot(dl)]}
    s["sentence"] = sentence(s)
    s["verdict_reported"] = s["label"] + (", unreplicated" if s["label"] == "pass" else "")
    return s


def ci3(c):
    return f"[{c[0]:.3f}, {c[1]:.3f}]"


def sentence(s):
    if s["label"] == "pass":
        t = (f"On {s['n']} findings published after its training cutoff, the bettor's probabilities beat a rule that knows each "
             f"field's own rate of good-news results (Brier difference {s['d']:.3f} {ci3(s['d_ci'])}; the field-aware rule "
             f"scored {s['base_brier']:.3f}), so its edge over the publication-bias shortcut (ss-b2) is more than knowing which "
             f"fields usually report good news. The rule's rates were fitted on the same items it was scored on, which favours the rule.")
    else:
        t = (f"On {s['n']} findings published after its training cutoff, the bettor was not shown to beat a rule that knows each "
             f"field's own rate of good-news results (Brier difference {s['d']:.3f} {ci3(s['d_ci'])}; the field-aware rule "
             f"scored {s['base_brier']:.3f}), so its round-1 edge over the publication-bias shortcut may come from knowing which "
             f"fields report good news.")
    if s["loo_flips"]:
        t += (f" This label rests on single items: without any one of {', '.join(s['loo_flips'][:5])}"
              f"{' …' if len(s['loo_flips']) > 5 else ''} it would be {'null' if s['label'] == 'pass' else 'pass'}.")
    fo = [f for f, v in s["field_out"].items() if v["label"] != s["label"]]
    if fo:
        t += f" Leaving out the {', '.join(fo)} field would make it {'null' if s['label'] == 'pass' else 'pass'}."
    t += (" One bettor (claude-opus-5-5 at effort low), one round-1 run already scored for ss-b1 to ss-b3; this re-scores that "
          "run against a stronger rule and adds no new answers.")
    return t


def tables(s):
    L = ["# ss-b11 tables (generated by scoring/score_f3.py; do not edit)", "", f"Verdict: **{s['verdict_reported']}**", "",
         "| measure | n | value | 95% CI |", "|---|---|---|---|",
         f"| bettor Brier | {s['n']} | {s['bettor_brier']:.3f} | {ci3(s['bettor_brier_ci'])} |",
         f"| field-aware rule Brier | {s['n']} | {s['base_brier']:.3f} | {ci3(s['base_brier_ci'])} |",
         f"| ss-b2's flat rule Brier (reported beside) | {s['n']} | {s['flat_brier']:.3f} | — |",
         f"| **bettor − field-aware rule** | {s['n']} | **{s['d']:+.3f}** | {ci3(s['d_ci'])} |",
         f"| bettor − field-aware rule, leave-one-out rates (secondary) | {s['n']} | {s['loo_baseline']['d']:+.3f} | {ci3(s['loo_baseline']['ci'])} |",
         f"| field-cluster jackknife on the difference (secondary) | {s['field_jackknife']['clusters']} fields | {s['d']:+.3f} | {ci3(s['field_jackknife']['ci'])} |",
         "", f"Baseline composition: {s['n_tagged']} tagged items (field headline rate), {s['n_untagged_up']} untagged items with an up option (field up-word rate), {s['n_half']} at 0.5.", "",
         "| field | n | tagged | headline rate | untagged with up option | up-option rate | bettor Brier | rule Brier | difference |",
         "|---|---|---|---|---|---|---|---|---|"]
    for f, v in s["by_field"].items():
        hr = f"{v['headline_rate']:.2f}" if v["headline_rate"] is not None else "—"
        ur = f"{v['up_rate']:.2f}" if v["up_rate"] is not None else "—"
        L.append(f"| {f} | {v['n']} | {v['tagged']} | {hr} | {v['untagged_up']} | {ur} | {v['bettor_brier']:.3f} | {v['base_brier']:.3f} | {v['d']:+.3f} |")
    L += ["", "| left out | n | difference | 95% CI | label |", "|---|---|---|---|---|"]
    for f, v in s["field_out"].items():
        L.append(f"| {f} | {v['n']} | {v['d']:+.3f} | {ci3(v['ci'])} | {v['label']} |")
    L += ["", f"Leave-one-item-out flips: {len(s['loo_flips'])}" + (f" ({', '.join(s['loo_flips'])})" if s["loo_flips"] else ""),
          "", "Pre-registered sentence:", "", f"> {s['sentence']}"]
    return "\n".join(L) + "\n"


def synthetic(world, seed=11):
    rng = np.random.default_rng(seed)
    fields = ["interpretability", "model-psychology", "quantum-devices", "scalable-oversight"]
    hr = {"skilled": [0.7, 0.8, 0.75, 0.7], "coin": [0.7, 0.8, 0.75, 0.7], "fieldrule": [0.9, 0.6, 0.8, 0.7], "extreme": [0.95, 0.6, 0.9, 0.8]}[world]
    ur = {"skilled": [0.5, 0.45, 0.55, 0.5], "coin": [0.5, 0.45, 0.55, 0.5], "fieldrule": [0.8, 0.3, 0.6, 0.5], "extreme": [0.9, 0.1, 0.85, 0.15]}[world]
    items, bets = [], []
    for n in range(116):
        f = n % 4
        tagged = rng.random() < 0.33
        it = {"id": f"syn-{n:03d}", "field": fields[f], "side": "post", "option_a": "Rates were higher after it.",
              "option_b": "Rates were lower after it.", "headline_side": None}
        if tagged:
            it["headline_side"] = "a" if rng.random() < 0.5 else "b"
            good = rng.random() < hr[f]
            it["true_option"] = it["headline_side"] if good else ("b" if it["headline_side"] == "a" else "a")
        else:
            it["true_option"] = "a" if rng.random() < ur[f] else "b"     # option_a is the up option here
        items.append(it)
        if world == "coin":
            pt = 0.5
        elif world == "fieldrule":
            pt = None
        else:
            right = rng.random() < (0.76 if world == "skilled" else 0.68)
            c = rng.uniform(0.55, 0.85)
            pt = c if right else 1 - c
        bets.append({"id": it["id"], "kind": "primary", "option_1_is": "a", "_pt": pt})
    if world == "fieldrule":
        for it in items:
            it["_up"] = None if it["headline_side"] is not None else up_side(it)
        b = baseline(items)
        for x in bets:
            x["_pt"] = b[x["id"]]
    for x, it in zip(bets, items):
        p1 = x["_pt"] if it["true_option"] == "a" else 1 - x["_pt"]
        x["p_option_1"] = int(round(100 * p1))
    return items, bets


def main():
    if "--synthetic" in sys.argv:
        w = sys.argv[sys.argv.index("--synthetic") + 1]
        s = score(*synthetic(w))
        print(w, "->", s["label"], "d", s["d"], s["d_ci"], "base", s["base_brier"], "bettor", s["bettor_brier"], "loo flips", len(s["loo_flips"]))
        return
    s = score(load(ITEMS), load(BETS))
    OUT_JSON.write_text(json.dumps(s, indent=1, ensure_ascii=False))
    OUT_MD.write_text(tables(s))
    print(tables(s))


if __name__ == "__main__":
    main()

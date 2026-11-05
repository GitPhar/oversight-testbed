"""Score ss-b10b (experiments/ss-b10b.md): the flattery rule on BrainBench's 200 items, both option orders. numpy only.

    python3 scoring/score_bbb.py                       # bettor/bbb-ratings.jsonl -> scoring/bbb-scores.json, bbb-tables.md
    python3 scoring/score_bbb.py --synthetic <world>   # dry run: coin | position (Option 1 always) | strong | haikulike | split

Per item and prompt, p_avg = the mean of the two calls' probabilities on the original abstract (original shown first, and
shown second). An item scores 1 if p_avg > 0.5, 0.5 if p_avg = 0.5, else 0 (ss-b10's rule, applied to p_avg). Accuracy =
the mean over items. 95% interval: percentile item bootstrap (10,000, default_rng(20261104)), the bar; a bootstrap over
the five journal sections (P14) is reported beside it. Every threshold is compared with tolerance EPS (P13).
Pass: on both Haiku and Sonnet, the orders-averaged flattery accuracy's item-bootstrap lower bound is above 0.634.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_bb as SB  # noqa: E402  (p_orig, hit, boot, boot_ratio, DUMB, EXPERTS, LLMS, EPS, REAL)
import score_f1 as F1  # noqa: E402  (cluster_ci)

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "items" / "brainbench" / "items.jsonl"
RATINGS = ROOT / "bettor" / "bbb-ratings.jsonl"
STATUS = ROOT / "bettor" / "bbb-run-status.json"
OUT_JSON, OUT_MD = ROOT / "scoring" / "bbb-scores.json", ROOT / "scoring" / "bbb-tables.md"
MODELS = ("claude-haiku-5-5", "claude-sonnet-5-5")
OPUS = "claude-opus-5-5"
NAME = {"claude-haiku-5-5": "Haiku", "claude-sonnet-5-5": "Sonnet", OPUS: "Opus"}
MIN_N = 150            # items with both flattery orders, per model; fewer -> untestable
EXPERTS, LLMS, EPS = SB.EXPERTS, SB.LLMS, SB.EPS
r3 = SB.r3


def pairs(rows, model, task):
    """{item: (p_orig shown first, p_orig shown second)} for items with both orders."""
    a = {}
    for r in rows:
        if r["model"] == model and r["task"] == task:
            a.setdefault(r["id"], {})[r["order"]] = SB.p_orig(r)
    return {i: (v["orig-first"], v["orig-second"]) for i, v in a.items() if len(v) == 2}


def acc_block(items, P, ids):
    hits = [SB.hit((P[i][0] + P[i][1]) / 2) for i in ids]
    a, (lo, hi) = float(np.mean(hits)), SB.boot(hits)
    sec = F1.cluster_ci(hits, [items[i]["journal_section"] for i in ids])
    single1 = [SB.hit(P[i][0]) for i in ids]
    single2 = [SB.hit(P[i][1]) for i in ids]
    return {"n": len(ids), "acc": r3(a), "ci": [r3(lo), r3(hi)], "section_ci": [r3(x) for x in sec],
            "brier_avg": r3(np.mean([(1 - (P[i][0] + P[i][1]) / 2) ** 2 for i in ids])),
            "acc_orig_first": r3(np.mean(single1)), "acc_orig_second": r3(np.mean(single2)),
            "option1_pull": r3(np.mean([(P[i][0] - P[i][1]) * 50 for i in ids])),   # points toward Option 1, (p1 + p1' - 100)/2
            "both_right": sum(1 for i in ids if P[i][0] > 0.5 and P[i][1] > 0.5),
            "first_only": sum(1 for i in ids if P[i][0] > 0.5 and not P[i][1] > 0.5),
            "second_only": sum(1 for i in ids if P[i][1] > 0.5 and not P[i][0] > 0.5),
            "n_avg_50": sum(1 for i in ids if (P[i][0] + P[i][1]) / 2 == 0.5),
            "vs_llms": "below" if hi < LLMS - EPS else "above" if lo > LLMS + EPS else "not shown different", "hits": hits}


def clears(hits):
    return bool(SB.boot(hits)[0] > EXPERTS + EPS)


def model_block(items, rows, model):
    F, B = pairs(rows, model, "flattery"), pairs(rows, model, "bettor")
    out = {"model": model, "n_flattery": len(F), "n_bettor": len(B)}
    if len(F) < MIN_N:
        out["label"] = "untestable"
        return out
    ids = sorted(F)
    out["flattery"] = acc_block(items, F, ids)
    out["clears_experts"] = clears(out["flattery"]["hits"])
    out["label"] = "clears" if out["clears_experts"] else "does not clear"
    h = out["flattery"]["hits"]
    out["loo_flips"] = [ids[k] for k in range(len(ids)) if clears(h[:k] + h[k + 1:]) != out["clears_experts"]]
    out["section_flips"] = [s for s in sorted({items[i]["journal_section"] for i in ids})
                            if clears([x for x, i in zip(h, ids) if items[i]["journal_section"] != s]) != out["clears_experts"]]
    # transparency: the items whose two orders were both already in ss-b10's archive vs the rest
    src = {}
    for r in rows:
        if r["model"] == model and r["task"] == "flattery":
            src.setdefault(r["id"], set()).add(r.get("source"))
    old = [i for i in ids if src.get(i) == {"ss-b10 archive"}]
    new = [i for i in ids if i not in set(old)]
    out["archive_split"] = {"both_orders_archived": {"n": len(old), "acc": r3(np.mean([SB.hit(sum(F[i]) / 2) for i in old])) if old else None},
                            "one_order_new": {"n": len(new), "acc": r3(np.mean([SB.hit(sum(F[i]) / 2) for i in new])) if new else None}}
    both = [i for i in ids if i in B]
    if len(both) >= MIN_N:
        out["bettor"] = acc_block(items, B, both)
        fa = [SB.hit(sum(F[i]) / 2) for i in both]
        ba = [SB.hit(sum(B[i]) / 2) for i in both]
        d = [b - f for b, f in zip(ba, fa)]
        out["bettor_minus_flattery"] = {"d": r3(np.mean(d)), "ci": [r3(x) for x in SB.boot(d)]}
        out["share_matched"] = ([r3(x) for x in SB.boot_ratio(fa, ba)] if SB.boot(ba)[0] > 0.5 + EPS else None)
        out["share_matched_point"] = r3((np.mean(fa) - 0.5) / (np.mean(ba) - 0.5)) if np.mean(ba) > 0.5 + EPS else None
    out["by_section"] = {s: {"n": sum(items[i]["journal_section"] == s for i in ids),
                             "flattery": r3(np.mean([SB.hit(sum(F[i]) / 2) for i in ids if items[i]["journal_section"] == s])),
                             "bettor": (r3(np.mean([SB.hit(sum(B[i]) / 2) for i in both if items[i]["journal_section"] == s]))
                                        if any(items[i]["journal_section"] == s for i in both) else None)}
                         for s in sorted({items[i]["journal_section"] for i in ids})}
    return out


def opus_block(items, rows, others):
    F, B = pairs(rows, OPUS, "flattery"), pairs(rows, OPUS, "bettor")
    ids = sorted(i for i in F if i in B)
    out = {"n_flattery": len(F), "n_both_prompts": len(ids)}
    if not F:
        return out
    fids = sorted(F)
    out["flattery"] = {k: v for k, v in acc_block(items, F, fids).items() if k != "hits"}
    if ids:
        out["bettor_same_items"] = {k: v for k, v in acc_block(items, B, ids).items() if k != "hits"}
        out["flattery_same_items"] = {k: v for k, v in acc_block(items, F, ids).items() if k != "hits"}
    for m in MODELS:
        Fm = pairs(others, m, "flattery")
        same = [i for i in fids if i in Fm]
        out[f"{NAME[m].lower()}_flattery_same_items"] = r3(np.mean([SB.hit(sum(Fm[i]) / 2) for i in same])) if same else None
    return out


def score(items, rows, status=None):
    out = {"models": {m: model_block(items, rows, m) for m in MODELS}, "status": status or {}}
    out["opus"] = opus_block(items, rows, rows)
    by_id = {it["id"]: it for it in items.values()}
    out["dumb"] = {}
    for name, f in SB.DUMB.items():
        v = [1.0 if f(it["original_abstract"], it["incorrect_abstract"]) > 0 else 0.5 if f(it["original_abstract"], it["incorrect_abstract"]) == 0 else 0.0
             for it in by_id.values()]
        lo, hi = SB.boot(v)
        out["dumb"][name] = {"acc": r3(np.mean(v)), "ci": [r3(lo), r3(hi)], "clears": bool(lo > EXPERTS + EPS)}
    out["dumb"]["Option 1 always (position)"] = {"acc": 0.5, "ci": [0.5, 0.5], "clears": False}
    out["verdict"] = verdict(out)
    out["sentences"] = sentences(out)
    for m in MODELS:
        for k in ("flattery", "bettor"):
            out["models"][m].get(k, {}).pop("hits", None)
    return out


def verdict(out):
    ms = out["models"]
    if any(ms[m]["label"] == "untestable" for m in MODELS):
        return "untestable"
    n = sum(ms[m]["clears_experts"] for m in MODELS)
    return "pass" if n == 2 else "mixed" if n == 1 else "fail"


def pct(x):
    return f"{100 * x:.1f}%"


def cis(c):
    return f"[{100 * c[0]:.1f}, {100 * c[1]:.1f}]"


def sentences(out):
    ms, v = out["models"], out["verdict"]
    s = []
    if v == "untestable":
        bad = [f"{NAME[m]}: {ms[m]['n_flattery']} of 200 items with both orders" for m in MODELS if ms[m]["label"] == "untestable"]
        s.append(f"Too few items were rated in both orders to test it ({'; '.join(bad)}; at least {MIN_N} needed).")
        return s
    H, S_ = ms[MODELS[0]]["flattery"], ms[MODELS[1]]["flattery"]
    lead = ("On BrainBench's 200 expert-written abstract pairs, with each item shown in both orders and the two ratings "
            "averaged, a model asked only which version is better news for the paper's own idea")
    if v == "pass":
        s.append(f"{lead} picked the published abstract more often than the 171 neuroscientists in the original study did "
                 f"(63.4%), on both Haiku ({pct(H['acc'])} {cis(H['ci'])}) and Sonnet ({pct(S_['acc'])} {cis(S_['ci'])}); the "
                 "published average for LLMs, scored by perplexity rather than by asking, was 81.4%. This design cannot tell "
                 "whether the models answered by valence, by plausibility or from memory of the papers, and it does not show "
                 "that the LLMs in the original study used such a rule.")
    elif v == "mixed":
        w = next(m for m in MODELS if ms[m]["clears_experts"])
        l = next(m for m in MODELS if not ms[m]["clears_experts"])
        s.append(f"{lead} beat the neuroscientists' published 63.4% on {NAME[w]} ({pct(ms[w]['flattery']['acc'])} "
                 f"{cis(ms[w]['flattery']['ci'])}) but was not shown to on {NAME[l]} ({pct(ms[l]['flattery']['acc'])} "
                 f"{cis(ms[l]['flattery']['ci'])}), so even with the position habit averaged out this prompt beats the "
                 "experts' published rate on one of the two models only.")
    else:
        s.append(f"{lead} was not shown to beat the neuroscientists' published 63.4% on either Haiku ({pct(H['acc'])} "
                 f"{cis(H['ci'])}) or Sonnet ({pct(S_['acc'])} {cis(S_['ci'])}), so this valence prompt does not account for "
                 "BrainBench's 'LLMs beat experts' result on these models. This says nothing about how the LLMs in the "
                 "original study, other models scored by perplexity, reached 81.4%.")
    for m in MODELS:
        M = ms[m]
        if "bettor" in M:
            d = M["bettor_minus_flattery"]
            sh = M.get("share_matched")
            s.append(f"With the program's forecasting prompt instead (a different instruction, a question line, and a note that "
                     f"one version was altered by an expert), also in both orders, {NAME[m]} picked the published abstract "
                     f"{pct(M['bettor']['acc'])} {cis(M['bettor']['ci'])} of the time, {abs(100 * d['d']):.1f} points "
                     f"{'more' if d['d'] >= 0 else 'less'} than with the flattery prompt (difference {cis(d['ci'])})"
                     + (f"; the flattery prompt's above-chance accuracy was {pct(M['share_matched_point'])} {cis(sh)} of the forecasting prompt's." if sh else "."))
        s.append(f"{NAME[m]}'s orders-averaged flattery accuracy was {M['flattery']['vs_llms']} the published 81.4% for LLMs "
                 f"(interval {cis(M['flattery']['ci'])}).")
        if M["loo_flips"]:
            s.append(f"On {NAME[m]}, leaving out any one of {len(M['loo_flips'])} items ({', '.join(M['loo_flips'][:5])}"
                     f"{', ...' if len(M['loo_flips']) > 5 else ''}) would change whether it clears the experts' rate.")
        if M["section_flips"]:
            s.append(f"On {NAME[m]}, leaving out the {', '.join(M['section_flips'])} section(s) would change whether it clears the experts' rate.")
        sc = M["flattery"]["section_ci"]
        if (sc[0] > EXPERTS + EPS) != M["clears_experts"]:
            s.append(f"On {NAME[m]}, a bootstrap over the five journal sections gives {cis(sc)}, which "
                     f"{'clears' if sc[0] > EXPERTS + EPS else 'does not clear'} the experts' rate (reported; the bar is read on items).")
    clear = [k for k, x in out["dumb"].items() if x["clears"]]
    if clear:
        s.append(f"A text-only rule ({', '.join(clear)}) also beat the experts' published rate, so beating the experts does not "
                 "need flattery judgement on these items.")
    O = out["opus"]
    if O.get("n_flattery"):
        s.append(f"Opus, asked the flattery question in both orders on {O['n_flattery']} beacon-drawn items (as many as its $1.50 "
                 f"cap allowed; a secondary, not part of the rule), picked the published abstract {pct(O['flattery']['acc'])} "
                 f"{cis(O['flattery']['ci'])} of the time; on the same items Sonnet's flattery rule was right "
                 f"{pct(O['sonnet_flattery_same_items'])} and Haiku's {pct(O['haiku_flattery_same_items'])}"
                 + (f", and Opus's forecasting prompt {pct(O['bettor_same_items']['acc'])} {cis(O['bettor_same_items']['ci'])} on the "
                    f"{O['n_both_prompts']} items where both of its prompts ran." if O.get("bettor_same_items") else "."))
    else:
        s.append("Opus (secondary) did not run.")
    s.append("BrainBench and its source abstracts (Journal of Neuroscience, 2023) were public before these models' training data "
             "were collected, so either prompt may draw on memory of the benchmark or of the papers; Haiku and Sonnet ran with "
             "thinking off and Opus at its least-thinking setting, and the prompts asked for a rating, not the perplexity the "
             "original study used. Of each model's 400 flattery ratings, those in ss-b10's archive (Haiku 300, Sonnet 274) were "
             "reused, not asked again.")
    return s


def tables(out):
    L = ["| model | prompt | n | accuracy, orders averaged | item 95% CI | section-cluster CI | original first | original second | Option-1 pull (points) | right both / first only / second only | clears 0.634 | vs 0.814 |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for m in MODELS:
        M = out["models"][m]
        for k in ("flattery", "bettor"):
            if k in M:
                X = M[k]
                L.append(f"| {NAME[m]} | {k} | {X['n']} | {X['acc']:.3f} | [{X['ci'][0]:.3f}, {X['ci'][1]:.3f}] | "
                         f"[{X['section_ci'][0]:.3f}, {X['section_ci'][1]:.3f}] | {X['acc_orig_first']:.3f} | {X['acc_orig_second']:.3f} | "
                         f"{X['option1_pull']:+.1f} | {X['both_right']} / {X['first_only']} / {X['second_only']} | "
                         f"{('yes' if M['clears_experts'] else 'no') if k == 'flattery' else '—'} | {X['vs_llms']} |")
    O = out["opus"]
    for k, lab in (("flattery", "flattery"), ("bettor_same_items", "bettor")):
        if k in O:
            X = O[k]
            L.append(f"| Opus | {lab} | {X['n']} | {X['acc']:.3f} | [{X['ci'][0]:.3f}, {X['ci'][1]:.3f}] | [{X['section_ci'][0]:.3f}, {X['section_ci'][1]:.3f}] | "
                     f"{X['acc_orig_first']:.3f} | {X['acc_orig_second']:.3f} | {X['option1_pull']:+.1f} | {X['both_right']} / {X['first_only']} / {X['second_only']} | — | {X['vs_llms']} |")
    L.append("\n| model | bettor − flattery (both averaged) | 95% CI | share of bettor's skill matched | 95% CI | flattery on items already rated both ways in ss-b10 | on the rest |")
    L.append("|---|---|---|---|---|---|---|")
    for m in MODELS:
        M = out["models"][m]
        if "bettor_minus_flattery" in M:
            a = M["archive_split"]
            L.append(f"| {NAME[m]} | {M['bettor_minus_flattery']['d']:+.3f} | [{M['bettor_minus_flattery']['ci'][0]:+.3f}, {M['bettor_minus_flattery']['ci'][1]:+.3f}] | "
                     f"{M['share_matched_point']} | {M['share_matched']} | {a['both_orders_archived']['acc']} (n {a['both_orders_archived']['n']}) | "
                     f"{a['one_order_new']['acc']} (n {a['one_order_new']['n']}) |")
    L.append("\n| text-only rule (no model) | accuracy | 95% CI | clears 0.634 |\n|---|---|---|---|")
    for k, x in out["dumb"].items():
        L.append(f"| {k} | {x['acc']:.3f} | [{x['ci'][0]:.3f}, {x['ci'][1]:.3f}] | {'yes' if x['clears'] else 'no'} |")
    L.append("\n| section | n | Haiku flattery | Haiku bettor | Sonnet flattery | Sonnet bettor |\n|---|---|---|---|---|---|")
    secs = out["models"][MODELS[0]].get("by_section", {})
    for s in secs:
        g = lambda m, k: out["models"][m]["by_section"][s][k]  # noqa: E731
        L.append(f"| {s} | {secs[s]['n']} | {g(MODELS[0], 'flattery')} | {g(MODELS[0], 'bettor')} | {g(MODELS[1], 'flattery')} | {g(MODELS[1], 'bettor')} |")
    L.append("\n| model | leave-one-item-out flips | leave-one-section-out flips |\n|---|---|---|")
    for m in MODELS:
        M = out["models"][m]
        if "loo_flips" in M:
            L.append(f"| {NAME[m]} | {', '.join(M['loo_flips']) or 'none'} | {', '.join(M['section_flips']) or 'none'} |")
    return "\n".join(L) + "\n"


def synthetic(world, seed=11):
    rng = np.random.default_rng(seed)
    items = {it["id"]: it for it in (json.loads(l) for l in ITEMS.read_text().splitlines() if l.strip())}
    rows = []
    skill = {"coin": (0.5, 0.5, 0), "position": (0.5, 0.5, 40), "strong": (0.85, 0.88, 5), "haikulike": (0.75, 0.80, 12),
             "split": (0.62, 0.62, 12)}[world]
    for m in MODELS + (OPUS,):
        acc = skill[1] if m == "claude-sonnet-5-5" else skill[0]
        if world == "split" and m == "claude-sonnet-5-5":
            acc = 0.85
        for i in items:
            right = rng.random() < acc
            base = 75 if right else 25
            for task in ("flattery", "bettor"):
                if m == OPUS and int(i[3:]) > 40:
                    continue
                for order, oi in (("orig-first", 1), ("orig-second", 2)):
                    p_orig = base if world != "coin" else 50
                    p1 = p_orig if oi == 1 else 100 - p_orig
                    p1 = int(min(99, max(1, p1 + skill[2])))
                    rows.append({"id": i, "model": m, "task": task, "order": order, "original_is_option": oi, "p_option_1": p1,
                                 "rationale": "", "source": "ss-b10 archive" if int(i[3:]) <= 100 else "ss-b10b"})
    return items, rows


def main():
    if "--synthetic" in sys.argv:
        for w in sys.argv[sys.argv.index("--synthetic") + 1:]:
            items, rows = synthetic(w)
            o = score(items, rows)
            print(f"{w:10s} {o['verdict']:10s}", {NAME[m]: (o['models'][m]['flattery']['acc'], o['models'][m]['flattery']['ci'][0]) for m in MODELS})
        return
    items = {it["id"]: it for it in (json.loads(l) for l in ITEMS.read_text().splitlines() if l.strip())}
    rows = [json.loads(l) for l in RATINGS.read_text().splitlines() if l.strip()]
    status = json.loads(STATUS.read_text()) if STATUS.exists() else {}
    out = score(items, rows, {k: v for k, v in status.items() if not k.endswith("_detail")})
    OUT_JSON.write_text(json.dumps(out, indent=1, default=float) + "\n")
    OUT_MD.write_text("# ss-b10b tables (generated by scoring/score_bbb.py)\n\n" + tables(out) + "\n## Sentences\n\n" +
                      "".join(f"> {x}\n>\n" for x in out["sentences"]))
    print("verdict:", out["verdict"])
    for x in out["sentences"]:
        print(" -", x)


if __name__ == "__main__":
    main()

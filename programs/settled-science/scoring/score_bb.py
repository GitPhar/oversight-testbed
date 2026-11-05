"""Score ss-b10 (experiments/ss-b10.md): the flattery rater and the bettor on BrainBench's 200 human-written items.
No model calls; numpy only.

    python3 scoring/score_bb.py                        # bettor/bb-ratings.jsonl -> scoring/bb-scores.json, bb-tables.md
    python3 scoring/score_bb.py --synthetic <world>    # dry run on synthetic ratings (prints the verdict and sentences)
         worlds: coin | strong (flattery 0.80, bettor 0.85) | edge (0.70) | weak (0.60) | split (Haiku 0.60, Sonnet 0.78)
                 | allfifty | inverted

p_orig = the probability a call put on the original (published) abstract. accuracy = mean over items of
1[p_orig > 0.5] + 0.5 * 1[p_orig = 0.5]. Brier = mean (1 - p_orig)^2. Unit: items. Percentile bootstrap over items,
10,000 resamples, numpy default_rng(20261104). Every threshold compared with tolerance EPS (P13).
"""
import json
import re
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "items" / "brainbench" / "items.jsonl"
RATINGS = ROOT / "bettor" / "bb-ratings.jsonl"
OUT_JSON = ROOT / "scoring" / "bb-scores.json"
OUT_MD = ROOT / "scoring" / "bb-tables.md"
MODELS = ("claude-haiku-5-5", "claude-sonnet-5-5")
SHORT = {"claude-haiku-5-5": "Haiku", "claude-sonnet-5-5": "Sonnet"}
EXPERTS = 0.634      # Luo et al. 2024: 171 neuroscientists' mean accuracy on the 200 human-written items
LLMS = 0.814         # Luo et al. 2024: mean accuracy of the LLMs tested (scored by lower perplexity)
MIN_N = 150          # a model with fewer scored primary flattery ratings is untestable (§5)
BOOT_SEED, BOOT_N, EPS = 20261104, 10000, 1e-12

# Answer-free text rules, fixed before data (§4, dumb baselines). Each returns +1 (pick A), -1 (pick B) or 0 (tie).
UP = r"\b(increas\w*|higher|greater|more|enhanc\w*|elevat\w*|larger|stronger|faster|improv\w*|facilitat\w*|potentiat\w*|upregulat\w*|augment\w*)\b"
DOWN = r"\b(decreas\w*|lower|less|fewer|reduc\w*|smaller|weaker|slower|impair\w*|attenuat\w*|downregulat\w*|diminish\w*|suppress\w*|inhibit\w*)\b"
NEG = r"\b(not|no|without|neither|nor|unaffected|unchanged|absence|absent|lack\w*|fail\w*)\b"
SIG = r"\bsignificant(ly)?\b"
REAL = re.compile(r"\b(original|real|actual|actually|published|authentic|genuine|plausib\w*|edited|altered|modified|"
                  r"likely (?:the )?(?:reported|written|true))\b", re.I)   # ss-b6 G3's regex, minus 'abstract' (every rationale here says it)


def _count(pat, s):
    return len(re.findall(pat, s, re.I))


def _cmp(a, b):
    return (a > b) - (a < b)


DUMB = {
    "longer abstract": lambda o, x: _cmp(len(o), len(x)),
    "shorter abstract": lambda o, x: _cmp(len(x), len(o)),
    "more up-words than down-words": lambda o, x: _cmp(_count(UP, o) - _count(DOWN, o), _count(UP, x) - _count(DOWN, x)),
    "fewer negation words": lambda o, x: _cmp(_count(NEG, x), _count(NEG, o)),
    "more 'significant'": lambda o, x: _cmp(_count(SIG, o), _count(SIG, x)),
}


def load(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def p_orig(r):
    p1 = min(99, max(1, int(r["p_option_1"]))) / 100
    return p1 if r["original_is_option"] == 1 else 1 - p1


def hit(p):
    return 1.0 if p > 0.5 else 0.5 if p == 0.5 else 0.0


def boot(v, n=BOOT_N, seed=BOOT_SEED):
    v = np.asarray(v, float)
    if len(v) == 0:
        return (None, None)
    m = np.sort(v[np.random.default_rng(seed).integers(0, len(v), size=(n, len(v)))].mean(1))
    return (float(m[int(0.025 * n)]), float(m[int(0.975 * n) - 1]))


def boot_ratio(a, b, n=BOOT_N, seed=BOOT_SEED):
    """(mean(a) - 0.5) / (mean(b) - 0.5), paired item bootstrap; resamples with mean(b) <= 0.5 + EPS are dropped."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    idx = np.random.default_rng(seed).integers(0, len(a), size=(n, len(a)))
    ma, mb = a[idx].mean(1), b[idx].mean(1)
    ok = mb > 0.5 + EPS
    r = np.sort((ma[ok] - 0.5) / (mb[ok] - 0.5))
    k = len(r)
    return (float(r[int(0.025 * k)]), float(r[int(0.975 * k) - 1])) if k else (None, None)


def r3(x):
    return None if x is None else round(float(x), 6)


def model_block(items, rows, model):
    by = {(r["task"], r["kind"], r["id"]): r for r in rows if r["model"] == model}
    out = {"model": model}
    flat = {i: p_orig(by[("flattery", "primary", i)]) for i in items if ("flattery", "primary", i) in by}
    bet = {i: p_orig(by[("bettor", "primary", i)]) for i in items if ("bettor", "primary", i) in by}
    out["n_flattery"], out["n_bettor"] = len(flat), len(bet)
    if len(flat) < MIN_N:
        out["label"] = "untestable"
        out["untestable_reason"] = f"{len(flat)} of 200 flattery ratings scored (at least {MIN_N} needed)"
        return out
    ids = sorted(flat)
    acc_f = [hit(flat[i]) for i in ids]
    a, (lo, hi) = float(np.mean(acc_f)), boot(acc_f)
    out["flattery"] = {"acc": r3(a), "ci": [r3(lo), r3(hi)], "brier": r3(np.mean([(1 - flat[i]) ** 2 for i in ids])),
                       "brier_ci": [r3(x) for x in boot([(1 - flat[i]) ** 2 for i in ids])],
                       "n_50": sum(1 for i in ids if flat[i] == 0.5),
                       "vs_llms": "below" if hi < LLMS - EPS else "above" if lo > LLMS + EPS else "not shown different"}
    out["clears_experts"] = bool(lo > EXPERTS + EPS)
    # leave-one-item-out and leave-one-section-out on this model's condition (LB > 0.634)
    flips = []
    for j in ids:
        v = [hit(flat[i]) for i in ids if i != j]
        if bool(boot(v)[0] > EXPERTS + EPS) != out["clears_experts"]:
            flips.append(j)
    out["loo_flips"] = flips
    sec_flips = []
    for s in sorted({items[i]["journal_section"] for i in ids}):
        v = [hit(flat[i]) for i in ids if items[i]["journal_section"] != s]
        if bool(boot(v)[0] > EXPERTS + EPS) != out["clears_experts"]:
            sec_flips.append(s)
    out["section_flips"] = sec_flips
    out["by_section"] = {s: {"n": sum(items[i]["journal_section"] == s for i in ids),
                             "flattery_acc": r3(np.mean([hit(flat[i]) for i in ids if items[i]["journal_section"] == s])),
                             "bettor_acc": (r3(np.mean([hit(bet[i]) for i in ids if items[i]["journal_section"] == s and i in bet]))
                                            if any(items[i]["journal_section"] == s and i in bet for i in ids) else None)}
                         for s in sorted({items[i]["journal_section"] for i in ids})}
    # G3-like count: flattery rationales reasoning about which version is real
    out["flattery_real_reasoning"] = sum(1 for i in ids if REAL.search(by[("flattery", "primary", i)]["rationale"] or ""))
    # the bettor, and the comparison on the items both answered
    both = [i for i in ids if i in bet]
    if len(bet) >= MIN_N:
        acc_b = [hit(bet[i]) for i in both]
        accf_b = [hit(flat[i]) for i in both]
        b, (blo, bhi) = float(np.mean(acc_b)), boot(acc_b)
        d = [x - y for x, y in zip(acc_b, accf_b)]
        db = [(1 - flat[i]) ** 2 - (1 - bet[i]) ** 2 for i in both]     # > 0: the bettor's Brier is lower
        agree = [i for i in both if (flat[i] - 0.5) * (bet[i] - 0.5) > 0]
        disagree = [i for i in both if (flat[i] - 0.5) * (bet[i] - 0.5) < 0]
        out["bettor"] = {"n_paired": len(both), "acc": r3(b), "ci": [r3(blo), r3(bhi)],
                         "brier": r3(np.mean([(1 - bet[i]) ** 2 for i in both])),
                         "brier_ci": [r3(x) for x in boot([(1 - bet[i]) ** 2 for i in both])],
                         "acc_minus_flattery": r3(np.mean(d)), "acc_minus_flattery_ci": [r3(x) for x in boot(d)],
                         "brier_gain_over_flattery": r3(np.mean(db)), "brier_gain_ci": [r3(x) for x in boot(db)],
                         "agree_n": len(agree), "disagree_n": len(disagree),
                         "disagree_bettor_right": sum(1 for i in disagree if bet[i] > 0.5),
                         "vs_llms": "below" if bhi < LLMS - EPS else "above" if blo > LLMS + EPS else "not shown different"}
        if blo > 0.5 + EPS:
            sm = (np.mean(accf_b) - 0.5) / (b - 0.5)
            out["bettor"]["share_matched"] = r3(sm)
            out["bettor"]["share_matched_ci"] = [r3(x) for x in boot_ratio(accf_b, acc_b)]
        else:
            out["bettor"]["share_matched"] = None
            out["bettor"]["share_matched_note"] = "not computed: the bettor was not shown above chance"
    else:
        out["bettor"] = {"n_paired": len(both), "note": f"{len(bet)} of 200 bettor ratings scored; under {MIN_N}, not compared"}
    # order check (flattery asked again, options reversed)
    oc = {i: by[("flattery", "order-check", i)] for i in ids if ("flattery", "order-check", i) in by}
    if oc:
        pp = [by[("flattery", "primary", i)]["p_option_1"] for i in oc]
        pr = [oc[i]["p_option_1"] for i in oc]
        same = [1.0 if (hit(flat[i]) == hit(p_orig(oc[i]))) and flat[i] != 0.5 else 0.0 for i in oc]
        incoh = [abs(a + b - 100) for a, b in zip(pp, pr)]
        pull = [(a + b - 100) / 2 for a, b in zip(pp, pr)]
        out["order_check"] = {"n": len(oc), "same_side": r3(np.mean(same)), "mean_abs_incoherence": r3(np.mean(incoh)),
                              "incoherence_ci": [r3(x) for x in boot(incoh)], "option1_pull": r3(np.mean(pull)),
                              "option1_pull_ci": [r3(x) for x in boot(pull)],
                              "acc_averaged_orders": r3(np.mean([hit((flat[i] + p_orig(oc[i])) / 2) for i in oc])),
                              "acc_primary_same_items": r3(np.mean([hit(flat[i]) for i in oc]))}
    return out


def opus_block(items, rows):
    """S9 (D54): Opus, flattery prompt, on the 50 lowest-id order-check items; never part of the pass rule."""
    op = {r["id"]: p_orig(r) for r in rows if r["model"] == "claude-opus-5-5" and r["kind"] == "opus-secondary"}
    if not op:
        return {"n": 0, "note": "not run"}
    ids = sorted(op)
    v = [hit(op[i]) for i in ids]
    def same(m):
        f = {r["id"]: p_orig(r) for r in rows if r["model"] == m and r["task"] == "flattery" and r["kind"] == "primary"}
        x = [hit(f[i]) for i in ids if i in f]
        return r3(np.mean(x)) if x else None
    return {"n": len(ids), "acc": r3(np.mean(v)), "ci": [r3(x) for x in boot(v)], "brier": r3(np.mean([(1 - op[i]) ** 2 for i in ids])),
            "sonnet_same_items": same("claude-sonnet-5-5"), "haiku_same_items": same("claude-haiku-5-5"),
            "n_50": sum(1 for i in ids if op[i] == 0.5)}


def dumb_block(items):
    out = {}
    ids = sorted(items)
    for name, f in DUMB.items():
        v = [{1: 1.0, 0: 0.5, -1: 0.0}[f(items[i]["original_abstract"], items[i]["incorrect_abstract"])] for i in ids]
        a, (lo, hi) = float(np.mean(v)), boot(v)
        out[name] = {"acc": r3(a), "ci": [r3(lo), r3(hi)], "ties": sum(1 for x in v if x == 0.5),
                     "clears_experts": bool(lo > EXPERTS + EPS)}
    return out


def verdict(blocks):
    """§5 as amended by D54 (design review F1): both untestable -> untestable; one untestable and the other clears ->
    untestable (the bet could not be completed); one untestable and the other does not clear -> fail-partial (scored 0:
    the bet cannot pass); else pass if both clear, mixed if exactly one, fail if neither."""
    test = [b for b in blocks if b.get("label") != "untestable"]
    if len(test) < len(blocks):
        if not test or any(b["clears_experts"] for b in test):
            return "untestable"
        return "fail-partial"
    k = sum(b["clears_experts"] for b in blocks)
    return "pass" if k == len(blocks) else "mixed" if k else "fail"


def pct(x):
    return f"{100 * x:.1f}%"


def civ(c):
    return f"[{100 * c[0]:.1f}, {100 * c[1]:.1f}]"


def sentences(s):
    """The pre-registered verdict sentences (§5), filled from the scores; qualifiers in the order given there."""
    B = {b["model"]: b for b in s["models"]}
    h, so = B["claude-haiku-5-5"], B["claude-sonnet-5-5"]
    v = s["verdict"]

    def fa(b):
        return f"{pct(b['flattery']['acc'])} {civ(b['flattery']['ci'])}"
    ns = [b.get("n_flattery") for b in s["models"]]
    pairs = ("BrainBench's 200 expert-written abstract pairs" if all(n == 200 for n in ns) else
             "BrainBench's expert-written abstract pairs (" + "; ".join(f"{SHORT[b['model']]}: {b.get('n_flattery')} of 200 scored"
                                                            for b in s["models"]) + ")")
    if v == "untestable":
        bad = [b for b in s["models"] if b.get("label") == "untestable"]
        main = ("Too few ratings came back to test it (" + "; ".join(f"{SHORT[b['model']]}: {b['untestable_reason']}" for b in bad) + ").")
    elif v == "pass":
        main = (f"On {pairs}, a model asked only which version is better news for the paper's own idea picked the published "
                f"abstract more often than the 171 neuroscientists in the original study did (63.4%), on both Haiku ({fa(h)}) and "
                f"Sonnet ({fa(so)}); the published average for LLMs, scored by perplexity rather than by asking, was 81.4%. This "
                f"design cannot tell whether the models answered by valence, by plausibility or from memory of the papers, and it "
                f"does not show that the LLMs in the original study used such a rule.")
    elif v == "mixed":
        yes = [b for b in s["models"] if b["clears_experts"]]
        no = [b for b in s["models"] if b not in yes]
        nd = "; ".join(f"{SHORT[b['model']]} ({fa(b)})" for b in no)
        main = (f"On {pairs}, a model asked only which version is better news for the paper's own idea beat the neuroscientists' "
                f"published 63.4% on {SHORT[yes[0]['model']]} ({fa(yes[0])}) but was not shown to on {nd}, so the shortcut beats "
                f"the experts on one of the two models only.")
    elif v == "fail-partial":
        bad = [b for b in s["models"] if b.get("label") == "untestable"][0]
        ok_ = [b for b in s["models"] if b.get("label") != "untestable"][0]
        main = (f"On {pairs}, a model asked only which version is better news for the paper's own idea was not shown to beat the "
                f"neuroscientists' published 63.4% on {SHORT[ok_['model']]} ({fa(ok_)}), and {SHORT[bad['model']]} could not be "
                f"tested ({bad['untestable_reason']}), so the bet cannot pass. This says nothing about how the LLMs in the original "
                f"study, other models scored by perplexity, reached 81.4%.")
    else:
        main = (f"On {pairs}, a model asked only which version is better news for the paper's own idea was not shown to beat the "
                f"neuroscientists' published 63.4% on either Haiku ({fa(h)}) or Sonnet ({fa(so)}). This says nothing about how the "
                f"LLMs in the original study, other models scored by perplexity, reached 81.4%.")
    out = [main]
    for b in s["models"]:
        bt = b.get("bettor") or {}
        if b.get("label") == "untestable" or "acc" not in bt:
            continue
        sm = (f"; the flattery prompt's above-chance accuracy was {pct(bt['share_matched'])} {civ(bt['share_matched_ci'])} of "
              f"the forecasting prompt's" if bt.get("share_matched") is not None else
              "; the forecasting prompt was not shown above chance, so no share is computed")
        out.append(f"With the program's forecasting prompt instead (a different instruction, a question line, and a note that one "
                   f"version was altered by an expert), {SHORT[b['model']]} picked the published abstract {pct(bt['acc'])} "
                   f"{civ(bt['ci'])} of the time, {100 * abs(bt['acc_minus_flattery']):.1f} points "
                   f"{'more' if bt['acc_minus_flattery'] >= 0 else 'less'} than with the flattery prompt "
                   f"(difference {civ(bt['acc_minus_flattery_ci'])}){sm}.")
    for b in s["models"]:
        if b.get("label") == "untestable":
            continue
        word = {"below": "below", "above": "above", "not shown different": "not shown different from"}[b["flattery"]["vs_llms"]]
        out.append(f"{SHORT[b['model']]}'s flattery rule was {word} the published 81.4% for LLMs (interval {civ(b['flattery']['ci'])}).")
    o = s.get("opus_secondary")
    if o and o.get("n"):
        out.append(f"Opus, asked the flattery question on {o['n']} of the items (a secondary, not part of the rule), picked the "
                   f"published abstract {pct(o['acc'])} {civ(o['ci'])} of the time; on the same items Sonnet's flattery rule was "
                   f"right {pct(o['sonnet_same_items'])} and Haiku's {pct(o['haiku_same_items'])}.")
    dumb = [k for k, d in s["dumb"].items() if d["clears_experts"]]
    if dumb:
        out.append(f"A text-only rule ({'; '.join(dumb)}) also beat the experts' published rate, so beating the experts does not "
                   f"need flattery judgement on these items.")
    for b in s["models"]:
        if b.get("label") == "untestable":
            continue
        if b["loo_flips"]:
            ex = ", ".join(b["loo_flips"][:5]) + (" …" if len(b["loo_flips"]) > 5 else "")
            out.append(f"Fragile on {SHORT[b['model']]}: removing any one of {len(b['loo_flips'])} items ({ex}) would change "
                       f"whether it clears the experts' rate.")
        if b["section_flips"]:
            out.append(f"On {SHORT[b['model']]}, leaving out the {', '.join(b['section_flips'])} section(s) would change "
                       f"whether it clears the experts' rate.")
    out.append("BrainBench and its source abstracts (Journal of Neuroscience, 2023) were public before both models' training "
               "data were collected, so either prompt may draw on memory of the benchmark or of the papers; the models ran "
               "with thinking off, and the prompts asked for a rating, not the perplexity the original study used.")
    return out


def score(items_list, rows):
    items = {it["id"]: it for it in items_list}
    blocks = [model_block(items, rows, m) for m in MODELS]
    s = {"bet": "ss-b10", "n_items": len(items), "experts": EXPERTS, "llms": LLMS,
         "models": blocks, "dumb": dumb_block(items), "calls": len(rows),
         "cost_usd": r3(sum(r.get("cost", 0) for r in rows))}
    s["opus_secondary"] = opus_block(items, rows)
    s["verdict"] = verdict(blocks)
    s["verdict_reported"] = (s["verdict"] + (", unreplicated" if s["verdict"] == "pass" else "")).replace("fail-partial", "fail (one model untestable)")
    s["sentences"] = sentences(s)
    return s


def tables(s):
    L = ["# ss-b10 tables (generated by scoring/score_bb.py; do not edit)", "",
         f"Verdict: **{s['verdict_reported']}**", "",
         "| model | prompt | n | accuracy | 95% CI | Brier | 95% CI | clears experts' 0.634 | vs LLMs' 0.814 |",
         "|---|---|---|---|---|---|---|---|---|"]
    for b in s["models"]:
        if b.get("label") == "untestable":
            L.append(f"| {SHORT[b['model']]} | flattery | {b['n_flattery']} | untestable | | | | | |")
            continue
        f = b["flattery"]
        L.append(f"| {SHORT[b['model']]} | flattery | {b['n_flattery']} | {f['acc']:.3f} | [{f['ci'][0]:.3f}, {f['ci'][1]:.3f}] | "
                 f"{f['brier']:.3f} | [{f['brier_ci'][0]:.3f}, {f['brier_ci'][1]:.3f}] | {'yes' if b['clears_experts'] else 'no'} | {f['vs_llms']} |")
        bt = b.get("bettor", {})
        if "acc" in bt:
            L.append(f"| {SHORT[b['model']]} | bettor | {bt['n_paired']} | {bt['acc']:.3f} | [{bt['ci'][0]:.3f}, {bt['ci'][1]:.3f}] | "
                     f"{bt['brier']:.3f} | [{bt['brier_ci'][0]:.3f}, {bt['brier_ci'][1]:.3f}] | — | {bt['vs_llms']} |")
    o = s.get("opus_secondary") or {}
    if o.get("n"):
        L.append(f"| Opus (secondary, D54) | flattery | {o['n']} | {o['acc']:.3f} | [{o['ci'][0]:.3f}, {o['ci'][1]:.3f}] | {o['brier']:.3f} | — | — | — |")
    L += ["", "| model | bettor − flattery, accuracy | 95% CI | Brier gain of bettor | 95% CI | share of bettor's skill matched | 95% CI | agree | disagree (bettor right) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for b in s["models"]:
        bt = b.get("bettor", {})
        if "acc" not in bt:
            continue
        sm = (f"{bt['share_matched']:.2f} | [{bt['share_matched_ci'][0]:.2f}, {bt['share_matched_ci'][1]:.2f}]"
              if bt.get("share_matched") is not None else "— | —")
        L.append(f"| {SHORT[b['model']]} | {bt['acc_minus_flattery']:+.3f} | [{bt['acc_minus_flattery_ci'][0]:+.3f}, {bt['acc_minus_flattery_ci'][1]:+.3f}] | "
                 f"{bt['brier_gain_over_flattery']:+.3f} | [{bt['brier_gain_ci'][0]:+.3f}, {bt['brier_gain_ci'][1]:+.3f}] | {sm} | "
                 f"{bt['agree_n']} | {bt['disagree_n']} ({bt['disagree_bettor_right']}) |")
    L += ["", "| text-only rule (no model) | accuracy | 95% CI | ties | clears experts' 0.634 |", "|---|---|---|---|---|"]
    for k, d in s["dumb"].items():
        L.append(f"| {k} | {d['acc']:.3f} | [{d['ci'][0]:.3f}, {d['ci'][1]:.3f}] | {d['ties']} | {'yes' if d['clears_experts'] else 'no'} |")
    L += ["", "| model | flattery said 50 | rationales reasoning about which is real | leave-one-item-out flips | leave-one-section-out flips |",
          "|---|---|---|---|---|"]
    for b in s["models"]:
        if b.get("label") == "untestable":
            continue
        L.append(f"| {SHORT[b['model']]} | {b['flattery']['n_50']} | {b['flattery_real_reasoning']} | {len(b['loo_flips'])} | "
                 f"{', '.join(b['section_flips']) or 'none'} |")
    L += ["", "| model | order check n | same side | mean \\|p + p′ − 100\\| | 95% CI | Option-1 pull | 95% CI | accuracy, orders averaged | accuracy, primary only (same items) |",
          "|---|---|---|---|---|---|---|---|---|"]
    for b in s["models"]:
        o = b.get("order_check")
        if not o:
            continue
        L.append(f"| {SHORT[b['model']]} | {o['n']} | {o['same_side']:.2f} | {o['mean_abs_incoherence']:.1f} | "
                 f"[{o['incoherence_ci'][0]:.1f}, {o['incoherence_ci'][1]:.1f}] | {o['option1_pull']:+.1f} | "
                 f"[{o['option1_pull_ci'][0]:+.1f}, {o['option1_pull_ci'][1]:+.1f}] | {o['acc_averaged_orders']:.3f} | {o['acc_primary_same_items']:.3f} |")
    L += ["", "| section | n | Haiku flattery | Haiku bettor | Sonnet flattery | Sonnet bettor |", "|---|---|---|---|---|---|"]
    B = {b["model"]: b for b in s["models"]}
    secs = sorted({k for b in s["models"] for k in b.get("by_section", {})})
    for sec in secs:
        cells = []
        for m in MODELS:
            e = B[m].get("by_section", {}).get(sec)
            cells += ([f"{e['flattery_acc']:.2f}", f"{e['bettor_acc']:.2f}" if e["bettor_acc"] is not None else "—"] if e else ["—", "—"])
        n = next(B[m]["by_section"][sec]["n"] for m in MODELS if sec in B[m].get("by_section", {}))
        L.append(f"| {sec} | {n} | " + " | ".join(cells) + " |")
    L += ["", "Pre-registered sentences:", ""] + [f"> {x}" for x in s["sentences"]]
    return "\n".join(L) + "\n"


def synthetic(items_list, world):
    rng = np.random.default_rng(7)
    accs = {"coin": (0.5, 0.5), "strong": (0.80, 0.85), "edge": (0.70, 0.75), "weak": (0.60, 0.70),
            "allfifty": (None, 0.7), "inverted": (0.25, 0.8)}
    rows = []
    for m in MODELS:
        fa, ba = (0.60, 0.70) if (world == "split" and m == MODELS[0]) else (0.78, 0.85) if world == "split" else accs[world]
        for it in items_list:
            for task, a in (("flattery", fa), ("bettor", ba)):
                o1 = 1 if rng.random() < 0.5 else 2
                if a is None:
                    p = 50
                else:
                    right = rng.random() < a
                    conf = int(rng.integers(55, 90))
                    po = conf if right else 100 - conf
                    p = po if o1 == 1 else 100 - po
                rows.append({"id": it["id"], "model": m, "task": task, "kind": "primary", "original_is_option": o1,
                             "p_option_1": p, "rationale": "synthetic", "cost": 0})
                if task == "flattery" and int(it["id"][3:]) % 2 == 0:
                    rows.append({"id": it["id"], "model": m, "task": task, "kind": "order-check", "original_is_option": 3 - o1,
                                 "p_option_1": 100 - p + int(rng.integers(-5, 6)), "rationale": "synthetic", "cost": 0})
        if m == MODELS[-1]:
            for it in items_list[:100:2]:
                o1 = 1 if rng.random() < 0.5 else 2
                po = 70 if rng.random() < 0.75 else 30
                rows.append({"id": it["id"], "model": "claude-opus-5-5", "task": "flattery", "kind": "opus-secondary",
                             "original_is_option": o1, "p_option_1": po if o1 == 1 else 100 - po, "rationale": "synthetic", "cost": 0})
    return rows


def main():
    items_list = load(ITEMS)
    if "--synthetic" in sys.argv:
        w = sys.argv[sys.argv.index("--synthetic") + 1]
        s = score(items_list, synthetic(items_list, w))
        print(w, "->", s["verdict_reported"], {SHORT[b["model"]]: (b.get("flattery", {}).get("acc"), b.get("flattery", {}).get("ci"))
                                               for b in s["models"]})
        if "--sentences" in sys.argv:
            print("\n".join(s["sentences"]))
        return
    s = score(items_list, load(RATINGS))
    OUT_JSON.write_text(json.dumps(s, indent=1, ensure_ascii=False))
    OUT_MD.write_text(tables(s))
    print(tables(s))


if __name__ == "__main__":
    main()

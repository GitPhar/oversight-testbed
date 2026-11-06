"""Score ss-b17 (experiments/ss-b17.md): ss-b10c's flattery question in a second wording, Haiku and Sonnet, all 200
BrainBench items in both orders. numpy only.

    python3 scoring/score_b17.py      # bettor/bbv2-ratings.jsonl (+ bettor/bbb-ratings.jsonl) -> scoring/b17-scores.json, b17-tables.md

Same item rule as ss-b10c (scoring/score_bbb.py): p_avg = the mean of the two orders' probabilities on the original;
1 if p_avg > 0.5, 0.5 if = 0.5, else 0; accuracy = the mean over items; 95% interval = percentile item bootstrap
(10,000, default_rng(20261104)). Tolerance EPS = 1e-12 (P13).

Per model, "meets the rule" means both of:
  C1  the second wording's orders-averaged accuracy, on the model's items with both orders, has an item-bootstrap lower
      bound above 0.634 (the 171 neuroscientists' published mean, Luo et al. 2024);
  C2  on the same items, that accuracy is within 0.05 (point estimate, either side) of the same model's orders-averaged
      accuracy with ss-b10c's wording (bettor/bbb-ratings.jsonl, task flattery, every item in both orders).
Pass: both models meet it. Mixed: exactly one. Fail: neither. Untestable: either model has fewer than 180 items with both
orders under the second wording.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_bb as SB  # noqa: E402
import score_bbb as BBB  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "items" / "brainbench" / "items.jsonl"
RATINGS = ROOT / "bettor" / "bbv2-ratings.jsonl"
V1 = ROOT / "bettor" / "bbb-ratings.jsonl"
STATUS = ROOT / "bettor" / "bbv2-run-status.json"
OUT_JSON, OUT_MD = ROOT / "scoring" / "b17-scores.json", ROOT / "scoring" / "b17-tables.md"
MODELS = ("claude-haiku-5-5", "claude-sonnet-5-5")
NAME = {"claude-haiku-5-5": "Haiku", "claude-sonnet-5-5": "Sonnet"}
EXPERTS, LLMS, EPS = SB.EXPERTS, SB.LLMS, SB.EPS
MARGIN = 0.05
MIN_N = 180
# D83 (design review ss-b17 F3): fixed before any call from the rebuilt dry run (scoring/dry_b16_b17.py, measured pilot
# noise, D82): the null world's share of items with the same item score under both wordings, per model (the noise floor),
# and the share of null runs in which at least one model misses the rule by call noise alone.
NOISE_FLOOR = {"claude-haiku-5-5": 0.818, "claude-sonnet-5-5": 0.888}   # two-draw null world
NULL_OUT = 0.091          # two-draw null world (main)
NULL_OUT_PESS = 0.303     # conditional null world (pessimistic: noise added on top of observed ratings)
FIVE_POINT_PASS = 0.53    # P(C2 holds) at a true 5-point shift, Haiku (Sonnet 0.52), two-draw null world
r3 = SB.r3


def c1(hits):
    return bool(SB.boot(hits)[0] > EXPERTS + EPS)


def scored_sets(v1rows):
    """ss-b10c's scored items (rated in one flattery order in ss-b10's archive): Haiku 100, Sonnet 126 (reported rows)."""
    return {m: sorted(i for i, c in BBB.archived_orders(v1rows, m).items() if c == 1) for m in MODELS}


def model_block(items, rows, v1rows, model, sset):
    F2, F1 = BBB.pairs(rows, model, "flattery-v2"), BBB.pairs(v1rows, model, "flattery")
    ids = sorted(i for i in F2 if i in F1)
    out = {"model": model, "n": len(ids)}
    if len(ids) < MIN_N - EPS:
        out["label"] = "untestable"
        return out
    A = BBB.acc_block(items, F2, ids)
    h2 = A.pop("hits")
    A1 = BBB.acc_block(items, F1, ids)
    h1 = A1.pop("hits")
    out["v2"], out["v1"] = A, A1
    d = [a - b for a, b in zip(h2, h1)]
    out["v2_minus_v1"] = {"d": r3(np.mean(d)), "ci": [r3(x) for x in SB.boot(d)]}
    out["c1"] = c1(h2)
    out["c2"] = bool(abs(np.mean(d)) <= MARGIN + EPS)
    out["label"] = "meets" if out["c1"] and out["c2"] else "does not meet"
    out["same_pick"] = r3(np.mean([(sum(F2[i]) / 2 > 0.5) == (sum(F1[i]) / 2 > 0.5) for i in ids]))
    out["same_score"] = r3(np.mean([a == b for a, b in zip(h2, h1)]))   # D85: the noise floor's own measure (same item score)
    out["vs_llms"] = A["vs_llms"]
    out["loo_flips"] = [ids[k] for k in range(len(ids)) if (c1(h2[:k] + h2[k + 1:]) and abs(np.mean(d[:k] + d[k + 1:])) <= MARGIN + EPS) != (out["label"] == "meets")]
    secs = sorted({items[i]["journal_section"] for i in ids})
    def meets_without(s):
        keep = [k for k, i in enumerate(ids) if items[i]["journal_section"] != s]
        return c1([h2[k] for k in keep]) and abs(np.mean([d[k] for k in keep])) <= MARGIN + EPS
    out["section_flips"] = [s for s in secs if meets_without(s) != (out["label"] == "meets")]
    sub = [i for i in sset if i in F2]
    if sub:
        hh = [SB.hit(sum(F2[i]) / 2) for i in sub]
        hv1 = [SB.hit(sum(F1[i]) / 2) for i in sub]
        out["ss_b10c_scored_items"] = {"n": len(sub), "v2": r3(np.mean(hh)), "v2_ci": [r3(x) for x in SB.boot(hh)], "v1": r3(np.mean(hv1))}
    Bf = BBB.pairs(v1rows, model, "bettor")     # D83 (F3): the forecasting prompt through the same comparison (reported)
    bi = [i for i in ids if i in Bf]
    if bi:
        hb = [SB.hit(sum(Bf[i]) / 2) for i in bi]
        h1b = [SB.hit(sum(F1[i]) / 2) for i in bi]
        db = float(np.mean(hb) - np.mean(h1b))
        out["forecasting_reference"] = {"n": len(bi), "acc": r3(np.mean(hb)), "d": r3(db), "meets": bool(c1(hb) and abs(db) <= MARGIN + EPS),
                                        "same_pick": r3(np.mean([(sum(Bf[i]) / 2 > 0.5) == (sum(F1[i]) / 2 > 0.5) for i in bi]))}
    out["by_section"] = {s: {"n": sum(items[i]["journal_section"] == s for i in ids),
                             "v2": r3(np.mean([x for x, i in zip(h2, ids) if items[i]["journal_section"] == s])),
                             "v1": r3(np.mean([x for x, i in zip(h1, ids) if items[i]["journal_section"] == s]))} for s in secs}
    return out


def score(items, rows, v1rows, status=None):
    ss = scored_sets(v1rows)
    out = {"models": {m: model_block(items, rows, v1rows, m, ss[m]) for m in MODELS}, "status": status or {}}
    ms = out["models"]
    if any(ms[m]["label"] == "untestable" for m in MODELS):
        out["verdict"] = "untestable"
    else:
        n = sum(ms[m]["label"] == "meets" for m in MODELS)
        out["verdict"] = "pass" if n == 2 else "mixed" if n == 1 else "fail"
    out["sentences"] = sentences(out)
    return out


def pct(x):
    return f"{100 * x:.1f}%"


def cis(c):
    return f"[{100 * c[0]:.1f}, {100 * c[1]:.1f}]"


def desc(M):
    return (f"{NAME[M['model']]} {pct(M['v2']['acc'])} {cis(M['v2']['ci'])}, against {pct(M['v1']['acc'])} with the first wording "
            f"(difference {M['v2_minus_v1']['d'] * 100:+.1f} points, {cis(M['v2_minus_v1']['ci'])})")


def sentences(o):
    ms, v = o["models"], o["verdict"]
    if v == "untestable":
        bad = [f"{NAME[m]}: {ms[m]['n']} of 200 items with both orders" for m in MODELS if ms[m]["label"] == "untestable"]
        return [f"Too few items were rated in both orders to test the second wording ({'; '.join(bad)}; at least {MIN_N} needed)."]
    H, S_ = ms[MODELS[0]], ms[MODELS[1]]
    lead = ("On BrainBench's 200 abstract pairs, each shown in both orders with the two ratings averaged, the flattery question "
            "in a second wording (fixed before any call: which version's findings make the authors' own idea look better "
            "supported)")
    if v == "pass":
        s = (f"{lead} picked the published abstract more often than the 171 neuroscientists did (63.4%) on both models, and "
             f"within 5 points of the first wording on each: {desc(H)}; {desc(S_)}. So ss-b10c's accuracy was not tied to its one "
             f"sentence, to within what 200 items can show (a point estimate; a true 5-point move passes about "
             f"{pct(FIVE_POINT_PASS)} of the time). A different question, the program's forecasting prompt, run through the same "
             "comparison would also have come close, so matching accuracy does not show the models answered the same question "
             "both times; this design still cannot tell valence from plausibility or memory of the papers.")
    elif v == "mixed":
        w = next(m for m in MODELS if ms[m]["label"] == "meets")
        l = next(m for m in MODELS if ms[m]["label"] != "meets")
        why = []
        if not ms[l]["c1"]:
            why.append("its lower bound is not above 63.4%")
        if not ms[l]["c2"]:
            why.append("it moved more than 5 points from the first wording")
        s = (f"{lead} held on {NAME[w]} ({desc(ms[w])}) but not on {NAME[l]} ({desc(ms[l])}; {' and '.join(why)}), so on "
             f"{NAME[l]} ss-b10c's accuracy did not survive the change of sentence (call noise alone takes at least one model "
             f"outside the rule in about {pct(NULL_OUT)} of null runs, {pct(NULL_OUT_PESS)} under a pessimistic noise model).")
    else:
        s = (f"{lead} did not hold on either model ({desc(H)}; {desc(S_)}): each either failed to clear the neuroscientists' "
             "63.4% or moved more than 5 points from the first wording, so ss-b10c's accuracy did not survive the change of "
             f"sentence (call noise alone takes at least one model outside the rule in about {pct(NULL_OUT)} of null runs, {pct(NULL_OUT_PESS)} under a pessimistic noise model).")
    out = [s]
    for m in MODELS:
        M = ms[m]
        out.append(f"{NAME[m]} gave the same pick under both wordings on {pct(M['same_pick'])} of the items, and the same item score "
                   f"on {pct(M['same_score'])} (call noise alone gives about {pct(NOISE_FLOOR[m])} the same item score); with the second wording "
                   f"it was right {pct(M['v2']['acc_orig_first'])} with the original shown first and {pct(M['v2']['acc_orig_second'])} "
                   f"with it second (Option-1 pull {M['v2']['option1_pull']:+.1f} points; {M['v1']['option1_pull']:+.1f} with the first wording).")
        if "ss_b10c_scored_items" in M:
            x = M["ss_b10c_scored_items"]
            out.append(f"On the {x['n']} items ss-b10c's rule was read on, {NAME[m]}'s second-wording accuracy was {pct(x['v2'])} "
                       f"{cis(x['v2_ci'])}, against ss-b10c's {pct(x['v1'])} (a reported row).")
        if "forecasting_reference" in M:
            x = M["forecasting_reference"]
            out.append(f"Run through the same comparison, {NAME[m]}'s forecasting prompt (ss-b10c, a different question) scores "
                       f"{pct(x['acc'])}, {100 * x['d']:+.1f} points from the first wording, same pick on {pct(x['same_pick'])}, and "
                       f"{'would' if x['meets'] else 'would not'} meet the rule (a reference row).")
        if M["loo_flips"]:
            out.append(f"On {NAME[m]}, leaving out any one of {len(M['loo_flips'])} items ({', '.join(M['loo_flips'][:5])}{', ...' if len(M['loo_flips']) > 5 else ''}) would change whether it meets the rule.")
        if M["section_flips"]:
            out.append(f"On {NAME[m]}, leaving out the {', '.join(M['section_flips'])} section(s) would change whether it meets the rule.")
    out.append("Both wordings ask a model to judge which version is better for the paper's own idea; a pass shows the result is "
               "not tied to one sentence, not that the models answer by valence rather than plausibility or memory of the papers, "
               "which were public before these models were trained. Haiku and Sonnet ran with thinking off, as in ss-b10c.")
    return out


def tables(o):
    if o["verdict"] == "untestable":
        return "Untestable: " + o["sentences"][0] + "\n"
    L = ["| model | wording | n | accuracy, orders averaged | item 95% CI | section-cluster CI | original first | original second | Option-1 pull (points) | right both / first only / second only |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for m in MODELS:
        M = o["models"][m]
        for k, lab in (("v2", "second (ss-b17)"), ("v1", "first (ss-b10c)")):
            X = M[k]
            L.append(f"| {NAME[m]} | {lab} | {X['n']} | {X['acc']:.3f} | [{X['ci'][0]:.3f}, {X['ci'][1]:.3f}] | [{X['section_ci'][0]:.3f}, {X['section_ci'][1]:.3f}] | "
                     f"{X['acc_orig_first']:.3f} | {X['acc_orig_second']:.3f} | {X['option1_pull']:+.1f} | {X['both_right']} / {X['first_only']} / {X['second_only']} |")
    L.append("\n| model | C1: lower bound > 0.634 | second − first wording | 95% CI | C2: within 0.05 | same pick | meets the rule |\n|---|---|---|---|---|---|---|")
    for m in MODELS:
        M = o["models"][m]
        d = M["v2_minus_v1"]
        L.append(f"| {NAME[m]} | {M['v2']['ci'][0]:.3f} ({'yes' if M['c1'] else 'no'}) | {d['d']:+.3f} | [{d['ci'][0]:+.3f}, {d['ci'][1]:+.3f}] | "
                 f"{'yes' if M['c2'] else 'no'} | {M['same_pick']:.3f} | {'yes' if M['label'] == 'meets' else 'no'} |")
    L.append(f"\n**Verdict: {o['verdict']}.**\n")
    L.append("| model | reference: forecasting prompt as the 'second wording' | n | accuracy | − first wording | same pick | would meet the rule |\n|---|---|---|---|---|---|---|")
    for m in MODELS:
        x = o["models"][m].get("forecasting_reference")
        if x:
            L.append(f"| {NAME[m]} | ss-b10c bettor | {x['n']} | {x['acc']:.3f} | {x['d']:+.3f} | {x['same_pick']:.3f} | {'yes' if x['meets'] else 'no'} |")
    L.append("\n| model | ss-b10c's scored items | second wording | 95% CI | first wording |\n|---|---|---|---|---|")
    for m in MODELS:
        x = o["models"][m].get("ss_b10c_scored_items")
        if x:
            L.append(f"| {NAME[m]} | {x['n']} | {x['v2']:.3f} | [{x['v2_ci'][0]:.3f}, {x['v2_ci'][1]:.3f}] | {x['v1']:.3f} |")
    L.append("\n| section | n | Haiku second | Haiku first | Sonnet second | Sonnet first |\n|---|---|---|---|---|---|")
    secs = o["models"][MODELS[0]]["by_section"]
    for s in secs:
        g = lambda m, k: o["models"][m]["by_section"][s][k]  # noqa: E731
        L.append(f"| {s} | {secs[s]['n']} | {g(MODELS[0], 'v2'):.3f} | {g(MODELS[0], 'v1'):.3f} | {g(MODELS[1], 'v2'):.3f} | {g(MODELS[1], 'v1'):.3f} |")
    L.append("\n| model | leave-one-item-out flips | leave-one-section-out flips |\n|---|---|---|")
    for m in MODELS:
        M = o["models"][m]
        L.append(f"| {NAME[m]} | {', '.join(M['loo_flips']) or 'none'} | {', '.join(M['section_flips']) or 'none'} |")
    return "\n".join(L) + "\n"


def main():
    items = {it["id"]: it for it in (json.loads(l) for l in ITEMS.read_text().splitlines() if l.strip())}
    rows = [json.loads(l) for l in RATINGS.read_text().splitlines() if l.strip()]
    v1 = [json.loads(l) for l in V1.read_text().splitlines() if l.strip()]
    status = json.loads(STATUS.read_text()) if STATUS.exists() else {}
    out = score(items, rows, v1, status)
    OUT_JSON.write_text(json.dumps(out, indent=1, default=float) + "\n")
    OUT_MD.write_text("# ss-b17 tables (generated by scoring/score_b17.py)\n\n" + tables(out) + "\n## Sentences\n\n" +
                      "".join(f"> {x}\n>\n" for x in out["sentences"]))
    print("verdict:", out["verdict"])
    for x in out["sentences"]:
        print(" -", x)


if __name__ == "__main__":
    main()

"""Score ss-b13 (experiments/ss-b13.md; direction ss-f1): Haiku and Sonnet as bettors. No model calls.

    python3 scoring/score_f1.py                      # bettor/f1-bets.jsonl -> scoring/f1-scores.json, scoring/f1-tables.md
    python3 scoring/score_f1.py --synthetic <kind>   # dry run on synthetic bets: coin | oracle | uprule | flatrule | opus | noisy-opus

The pass rule (§5) is read on round 1's 116 post-cutoff items, per model, for both Haiku and Sonnet:
  C1  Brier upper bound < 0.25 (always-50%), and
  C2  Brier minus the up-word rule's  < -MARGIN at the upper bound, and
  C3  Brier minus the good-news rule's < -MARGIN at the upper bound,
each on BOTH the item bootstrap and the paper-cluster bootstrap (P14; at most two items share a paper).
up-word rule: 0.75 on the option holding the 'up' word of its direction pair (higher, more, larger ...), 0.5 where the
pair has no up side (earlier/later, easier/harder, closer/farther) or the slots disagree; computed from the options only.
good-news rule: ss-b2's publication-bias baseline, 0.75 on the item-writer's headline tag (the paper's own 'it works'
side), 0.5 where untagged; it is the program's round-1 form of the flattery rule (no flattery rater ran on round 1).
Round 2's 92 items, the card's own event and Opus's archive are reported rows that never change the verdict.
"""
import difflib
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "items"))
import score as S  # noqa: E402  (p_true_of, brier, acc, boot_ci, headline_p, swap_pair, SWAP_PAIR_P, PAIR_PRIOR, EPS)
import verify  # noqa: E402  (norm, PAIRS)

ROOT = Path(__file__).resolve().parents[1]
F1_BETS = ROOT / "bettor" / "f1-bets.jsonl"
OUT_JSON, OUT_MD = ROOT / "scoring" / "f1-scores.json", ROOT / "scoring" / "f1-tables.md"
MODELS = ("claude-haiku-5-5", "claude-sonnet-5-5")
NAME = {"claude-haiku-5-5": "Haiku", "claude-sonnet-5-5": "Sonnet", "claude-opus-5-5": "Opus"}
MARGIN = 0.01
MIN_SCORED = 100          # of 116; fewer on either model -> untestable
BOOT_SEED, BOOT_N = S.BOOT_SEED, S.BOOT_N
UP_WORDS = {"higher", "more", "increased", "increase", "increases", "larger", "above", "better", "stronger", "faster",
            "longer", "greater", "rose", "grew", "improved", "raised", "exceeded", "outperformed", "most", "highest",
            "largest", "increasing", "rising", "up", "wider", "bigger", "lengthened", "strengthened", "widened", "high",
            "deeper", "amplified", "enhanced"}
NO_UP = {frozenset(p) for p in (("earlier", "later"), ("an earlier", "a later"), ("easier", "harder"),
                                 ("closer", "farther"), ("closer", "further"))}


def up_side_r1(it):
    """Answer-free: which option holds the 'up' word in every differing slot ('a' | 'b' | None)."""
    ta, tb = verify.norm(it["option_a"]).rstrip(".").split(), verify.norm(it["option_b"]).rstrip(".").split()
    votes = set()
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(a=ta, b=tb, autojunk=False).get_opcodes():
        if tag == "equal":
            continue
        x, y = " ".join(ta[i1:i2]), " ".join(tb[j1:j2])
        if frozenset((x, y)) in NO_UP:
            continue
        if x in UP_WORDS and y not in UP_WORDS:
            votes.add("a")
        elif y in UP_WORDS and x not in UP_WORDS:
            votes.add("b")
        else:
            return None
    return votes.pop() if len(votes) == 1 else None


def rule_p(side, true_option, p=0.75):
    return 0.5 if side is None else (p if side == true_option else 1 - p)


def cluster_ci(vals, clusters, n=BOOT_N, seed=BOOT_SEED):
    """Percentile bootstrap of the item mean, resampling whole clusters (P14). Same percentile indices as S.boot_ci."""
    v = np.asarray(vals, float)
    keys = sorted(set(clusters))
    if not keys:
        return (None, None)
    pos = {k: i for i, k in enumerate(keys)}
    sums, cnts = np.zeros(len(keys)), np.zeros(len(keys))
    for x, c in zip(v, clusters):
        sums[pos[c]] += x
        cnts[pos[c]] += 1
    idx = np.random.default_rng(seed).integers(0, len(keys), size=(n, len(keys)))
    m = np.sort(sums[idx].sum(1) / cnts[idx].sum(1))
    return (float(m[int(0.025 * n)]), float(m[int(0.975 * n) - 1]))


def stat(vals, clusters):
    v = list(vals)
    return {"mean": float(np.mean(v)) if v else None, "item_ci": S.boot_ci(v), "cluster_ci": cluster_ci(v, clusters)}


def rows_r1(items, bets_by_id):
    rows = []
    for iid, it in sorted(items.items()):
        if it["side"] != "post" or iid not in bets_by_id:
            continue
        b = bets_by_id[iid]
        up = up_side_r1(it)
        rows.append({"id": iid, "field": it["field"], "paper": it["arxiv_id"], "p_true": S.p_true_of(b, it),
                     "up_side": up, "p_up": rule_p(up, it["true_option"]), "p_good": S.headline_p(it)})
    return rows


def legs(rows, cl_key):
    se = [(1 - r["p_true"]) ** 2 for r in rows]
    cl = [r[cl_key] for r in rows]
    out = {"n": len(rows), "brier": S.brier([r["p_true"] for r in rows]), "accuracy": S.acc([r["p_true"] for r in rows]),
           "C1": stat(se, cl)}
    for leg, key in (("C2", "p_up"), ("C3", "p_good")):
        out[leg] = stat([(1 - r["p_true"]) ** 2 - (1 - r[key]) ** 2 for r in rows], cl)
        out[leg]["rule_brier"] = float(np.mean([(1 - r[key]) ** 2 for r in rows])) if rows else None
    return out


def passes(L):
    """C1-C3 on both bootstraps (tolerance EPS on every bound, P13)."""
    ok1 = all(L["C1"][k][1] is not None and L["C1"][k][1] < 0.25 - S.EPS for k in ("item_ci", "cluster_ci"))
    ok23 = all(L[c][k][1] is not None and L[c][k][1] < -MARGIN - S.EPS for c in ("C2", "C3") for k in ("item_ci", "cluster_ci"))
    return ok1 and ok23


def card_event(L):
    """Sean's card (ss-f1): Brier upper bound below 0.25, item bootstrap only (a reported row, not the rule)."""
    return L["C1"]["item_ci"][1] < 0.25 - S.EPS


def model_result(rows):
    L = legs(rows, "paper")
    L["pass"] = passes(L)
    L["card_event"] = card_event(L)
    flips = [rows[i]["id"] for i in range(len(rows)) if passes(legs(rows[:i] + rows[i + 1:], "paper")) != L["pass"]]
    L["loo_item_flips"] = flips
    L["lofo"] = {}
    for f in sorted({r["field"] for r in rows}):
        rest = [r for r in rows if r["field"] != f]
        L["lofo"][f] = passes(legs(rest, "paper"))
    L["lofo_flips"] = [f for f, v in L["lofo"].items() if v != L["pass"]]
    return L


def rows_r2(items, bets_by_id, valence_by_id):
    rows = []
    for iid, it in sorted(items.items()):
        if iid not in bets_by_id:
            continue
        b = bets_by_id[iid]
        pair = S.swap_pair(it)
        pu = S.SWAP_PAIR_P.get(pair, S.PAIR_PRIOR)
        r = {"id": iid, "field": it["field"], "pair": pair, "p_true": S.p_true_of(b, it),
             "p_up": rule_p(it["up_side"], it["true_option"]), "p_pair": pu if it["up_side"] == it["true_option"] else 1 - pu}
        if iid in valence_by_id:
            r["p_flat"] = S.p_true_of(valence_by_id[iid], it)
        rows.append(r)
    return rows


def r2_report(rows):
    se = [(1 - r["p_true"]) ** 2 for r in rows]
    cl = [r["pair"] for r in rows]
    out = {"n": len(rows), "brier": S.brier([r["p_true"] for r in rows]), "accuracy": S.acc([r["p_true"] for r in rows]),
           "brier_stat": stat(se, cl)}
    for leg, key in (("vs_up_word", "p_up"), ("vs_swap_pair", "p_pair"), ("vs_flattery_rater", "p_flat")):
        rs = [r for r in rows if key in r]
        out[leg] = stat([(1 - r["p_true"]) ** 2 - (1 - r[key]) ** 2 for r in rs], [r["pair"] for r in rs])
        out[leg]["n"] = len(rs)
        out[leg]["rule_brier"] = float(np.mean([(1 - r[key]) ** 2 for r in rs])) if rs else None
        out[leg]["beats_by_margin"] = all(out[leg][k][1] is not None and out[leg][k][1] < -MARGIN - S.EPS for k in ("item_ci", "cluster_ci"))
    return out


def load_jsonl(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()] if Path(p).exists() else []


def score(f1_bets):
    items1 = S.load_items()
    items2 = {it["id"]: it for it in load_jsonl(ROOT / "items" / "r2" / "items.jsonl")}
    valence = {b["id"]: b for b in load_jsonl(ROOT / "bettor" / "r2-valence.jsonl") if b["kind"] == "valence"}
    out = {"models": {}, "opus_archive": {}}
    for m in MODELS:
        r1 = {b["id"]: b for b in f1_bets if b["model"] == m and b["round"] == "r1" and b["kind"] == "primary"}
        r2 = {b["id"]: b for b in f1_bets if b["model"] == m and b["round"] == "r2" and b["kind"] == "primary"}
        rows1 = rows_r1(items1, r1)
        res = {"n_scored_r1": len(rows1), "untestable": len(rows1) < MIN_SCORED}
        if rows1:
            res["r1"] = model_result(rows1)
        rows2 = rows_r2(items2, r2, valence)
        res["r2"] = r2_report(rows2) if rows2 else {"n": 0}
        out["models"][m] = res
    # Opus's archived bets, scored by the same code (reference rows; Opus's verdicts are ss-b1, ss-b2, ss-b5, ss-b6)
    o1 = {b["id"]: b for b in load_jsonl(ROOT / "bettor" / "bets.jsonl") if b["kind"] == "primary"}
    o2 = {b["id"]: b for b in load_jsonl(ROOT / "bettor" / "r2-bets.jsonl") if b["kind"] == "primary"}
    out["opus_archive"] = {"r1": model_result(rows_r1(items1, o1)), "r2": r2_report(rows_r2(items2, o2, valence))}
    for o in ("r1",):
        out["opus_archive"][o].pop("loo_item_flips", None)
    out["verdict"] = verdict(out)
    out["sentences"] = sentences(out)
    return out


def verdict(out):
    ms = out["models"]
    if any(ms[m]["untestable"] for m in MODELS):
        return "untestable"
    n = sum(ms[m]["r1"]["pass"] for m in MODELS)
    return "pass" if n == 2 else "mixed" if n == 1 else "fail"


def f3(x):
    return f"{x:+.3f}" if x is not None else "n/a"


def ci(c):
    return f"[{c[0]:.3f}, {c[1]:.3f}]" if c and c[0] is not None else "[n/a]"


def sentences(out):
    """§5's sentences, filled from the numbers (P9). Only these appear in the results."""
    ms, v = out["models"], out["verdict"]
    s = []
    def part(m):
        L = ms[m]["r1"]
        return (f"{NAME[m]} Brier {L['brier']:.3f} {ci(L['C1']['item_ci'])}, against the up-word rule "
                f"{f3(L['C2']['mean'])} {ci(L['C2']['item_ci'])}, against the good-news rule {f3(L['C3']['mean'])} {ci(L['C3']['item_ci'])}")
    if v == "untestable":
        bad = [f"{NAME[m]}: {ms[m]['n_scored_r1']} of 116 scored" for m in MODELS if ms[m]["untestable"]]
        s.append(f"Too few findings were scored to test the smaller bettors ({'; '.join(bad)}; at least {MIN_SCORED} needed).")
        return s
    if v == "pass":
        s.append("On round 1's 116 findings posted after the models' training cutoff, both Haiku and Sonnet, with the bettor's "
                 "prompt unchanged, beat always saying 50% and beat both the up-word rule and the good-news rule by more than "
                 f"0.01 in Brier, on item and paper-cluster bootstraps ({part(MODELS[0])}; {part(MODELS[1])}). Knowing which way "
                 "these findings went is not only the strongest model's; this does not separate knowing results from reasoning "
                 "within the item, and the items were written by a Claude model.")
    elif v == "mixed":
        w = next(m for m in MODELS if ms[m]["r1"]["pass"])
        l = next(m for m in MODELS if not ms[m]["r1"]["pass"])
        s.append(f"On round 1's 116 post-cutoff findings, {NAME[w]} met the rule (always-50%, the up-word rule and the good-news "
                 f"rule all beaten, the last two by more than 0.01 in Brier) but {NAME[l]} was not shown to ({part(w)}; {part(l)}), "
                 "so the bettor's skill holds on one of the two smaller models only.")
    else:
        s.append(f"On round 1's 116 post-cutoff findings, neither Haiku nor Sonnet was shown to beat always-50%, the up-word "
                 f"rule and the good-news rule by the pre-registered margin ({part(MODELS[0])}; {part(MODELS[1])}), so on these "
                 "items the bettor's skill was not shown beyond the strongest model.")
    for m in MODELS:
        L = ms[m]["r1"]
        fails = [c for c, k in (("C1", 0.25), ("C2", -MARGIN), ("C3", -MARGIN))
                 for b in ("item_ci", "cluster_ci") if not (L[c][b][1] < k - S.EPS)]
        if fails and not L["pass"]:
            s.append(f"{NAME[m]} missed on {', '.join(sorted(set(fails)))}.")
        if L["loo_item_flips"]:
            fl = L["loo_item_flips"]
            s.append(f"{NAME[m]}'s label rests on {'one item' if len(fl) == 1 else f'{len(fl)} single items'} "
                     f"({', '.join(fl[:5])}{', ...' if len(fl) > 5 else ''}): removing {'it' if len(fl) == 1 else 'any one'} changes it.")
        if L["lofo_flips"]:
            s.append(f"{NAME[m]}'s label changes if the {', '.join(L['lofo_flips'])} field is left out.")
    card = [NAME[m] for m in MODELS if ms[m]["r1"]["card_event"]]
    s.append(f"The cockpit card's event (Brier upper bound below 0.25 on both models, item bootstrap only) was "
             f"{'met' if len(card) == 2 else 'not met'}{'' if len(card) in (0, 2) else f' (met on {card[0]} only)'}; it is reported, not the rule.")
    s.append("Both models ran with thinking off, which the Opus bettor could not (it ran at its least-thinking setting), so the "
             "comparison with Opus's archive differs in thinking as well as model.")
    return s


def tables(out):
    L = []
    L.append("| model | n | accuracy | Brier | item 95% CI | paper-cluster 95% CI | − up-word rule | item CI | cluster CI | − good-news rule | item CI | cluster CI | rule met |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    rowsrc = [(NAME[m], out["models"][m].get("r1")) for m in MODELS] + [("Opus (archive)", out["opus_archive"]["r1"])]
    for nm, R in rowsrc:
        if not R:
            L.append(f"| {nm} | 0 | | | | | | | | | | | |")
            continue
        L.append(f"| {nm} | {R['n']} | {R['accuracy']:.3f} | {R['brier']:.3f} | {ci(R['C1']['item_ci'])} | {ci(R['C1']['cluster_ci'])} | "
                 f"{f3(R['C2']['mean'])} | {ci(R['C2']['item_ci'])} | {ci(R['C2']['cluster_ci'])} | {f3(R['C3']['mean'])} | "
                 f"{ci(R['C3']['item_ci'])} | {ci(R['C3']['cluster_ci'])} | {'yes' if R['pass'] else 'no'} |")
    R = out["opus_archive"]["r1"]
    L.append(f"\nRule Briers on the 116: up-word {R['C2']['rule_brier']:.3f}, good-news {R['C3']['rule_brier']:.3f}; always-50% 0.250.")
    L.append("\nRound 2's 92 template items (reported, not the rule; cluster = the template's swap pair, P14):\n")
    L.append("| model | n | accuracy | Brier | − up-word | item CI | cluster CI | − swap-pair | item CI | cluster CI | − Opus flattery rater | item CI | cluster CI |")
    L.append("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    rowsrc = [(NAME[m], out["models"][m]["r2"]) for m in MODELS] + [("Opus (archive)", out["opus_archive"]["r2"])]
    for nm, R in rowsrc:
        if not R.get("n"):
            L.append(f"| {nm} | 0 | | | | | | | | | | | |")
            continue
        g = lambda k: f"{f3(R[k]['mean'])} | {ci(R[k]['item_ci'])} | {ci(R[k]['cluster_ci'])}"  # noqa: E731
        L.append(f"| {nm} | {R['n']} | {R['accuracy']:.3f} | {R['brier']:.3f} | {g('vs_up_word')} | {g('vs_swap_pair')} | {g('vs_flattery_rater')} |")
    L.append("\nRobustness (round 1, per model): leave-one-item-out flips; leave-one-field-out labels.\n")
    L.append("| model | items that flip the label | field left out → rule met |")
    L.append("|---|---|---|")
    for m in MODELS:
        R = out["models"][m].get("r1")
        if R:
            L.append(f"| {NAME[m]} | {', '.join(R['loo_item_flips']) or 'none'} | "
                     f"{'; '.join(f'{f}: {'yes' if v else 'no'}' for f, v in R['lofo'].items())} |")
    return "\n".join(L) + "\n"


def synthetic(kind, rng_seed=7):
    """Synthetic f1 bets for the dry run: coin, oracle, uprule, flatrule, opus (Opus's archive relabelled), noisy-opus."""
    import random
    rng = random.Random(rng_seed)
    items1 = S.load_items()
    items2 = {it["id"]: it for it in load_jsonl(ROOT / "items" / "r2" / "items.jsonl")}
    o1 = {b["id"]: b for b in load_jsonl(ROOT / "bettor" / "bets.jsonl") if b["kind"] == "primary"}
    o2 = {b["id"]: b for b in load_jsonl(ROOT / "bettor" / "r2-bets.jsonl") if b["kind"] == "primary"}
    bets = []
    for m in MODELS:
        for rnd, items, arch in (("r1", {k: v for k, v in items1.items() if v["side"] == "post"}, o1), ("r2", items2, o2)):
            for iid, it in items.items():
                if iid not in arch:
                    continue
                o1is = arch[iid]["option_1_is"]
                one_true = o1is == it["true_option"]
                if kind == "coin":
                    pt = 0.5
                elif kind == "oracle":
                    pt = 0.9
                elif kind == "uprule":
                    pt = rule_p(up_side_r1(it) if rnd == "r1" else it["up_side"], it["true_option"])
                elif kind == "flatrule":
                    pt = S.headline_p(it) if rnd == "r1" else 0.5
                else:
                    p1 = min(99, max(1, arch[iid]["p_option_1"])) / 100
                    pt = p1 if one_true else 1 - p1
                    if kind == "noisy-opus":
                        lg = np.log(pt / (1 - pt)) + rng.gauss(0, 0.8)
                        pt = 1 / (1 + np.exp(-lg))
                p1 = pt if one_true else 1 - pt
                bets.append({"id": iid, "round": rnd, "model": m, "kind": "primary", "option_1_is": o1is,
                             "p_option_1": int(round(100 * p1))})
    return bets


def main():
    if "--synthetic" in sys.argv:
        for kind in sys.argv[sys.argv.index("--synthetic") + 1:]:
            o = score(synthetic(kind))
            R = o["models"][MODELS[0]]["r1"]
            print(f"{kind:11s} verdict {o['verdict']:10s} Brier {R['brier']:.3f} C1ub {R['C1']['item_ci'][1]:.3f}/{R['C1']['cluster_ci'][1]:.3f} "
                  f"C2ub {R['C2']['item_ci'][1]:+.3f}/{R['C2']['cluster_ci'][1]:+.3f} C3ub {R['C3']['item_ci'][1]:+.3f}/{R['C3']['cluster_ci'][1]:+.3f}")
            print("   ", o["sentences"][0][:240])
        return
    out = score(load_jsonl(F1_BETS))
    OUT_JSON.write_text(json.dumps(out, indent=1, default=float) + "\n")
    OUT_MD.write_text("# ss-b13 tables (generated by scoring/score_f1.py)\n\n" + tables(out) + "\n## Sentences\n\n" +
                      "".join(f"> {x}\n>\n" for x in out["sentences"]))
    print("verdict:", out["verdict"])
    for x in out["sentences"]:
        print(" -", x)


if __name__ == "__main__":
    main()

"""Score ss-b14 (experiments/ss-b14.md; direction ss-f2): 60 more post-cutoff model-psychology template items. No calls.

    python3 scoring/score_f2.py                      # bettor/f2-bets.jsonl -> scoring/f2-scores.json, scoring/f2-tables.md
    python3 scoring/score_f2.py --synthetic <kind>   # dry run on round 2's 92 items: coin | oracle | uprule | flatcopy

The pass rule (§5) is read on the Opus bettor (the card's model); Haiku and Sonnet are reported with the same numbers:
  C1  Brier upper bound < 0.25 (always-50%), and
  C2  Brier minus the up-word rule's (0.75 on the option holding the template's 'up' word) < -MARGIN at the upper bound, and
  C3  Brier minus the flattery rater's (claude-opus-5-5 asked only which version is better news for the paper's own
      method, ss-b6's prompt, on the same items in the same option order) < -MARGIN at the upper bound,
each on BOTH the item bootstrap and the template-cluster bootstrap (P14: cluster = the template's swap pair, as
scoring/score.py swap_pair). Untestable: fewer than 50 items scored by the Opus bettor or by the flattery rater.
"""
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score as S  # noqa: E402
import score_f1 as F1  # noqa: E402  (cluster_ci, stat, rule_p, MARGIN)

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "items" / "f2" / "items.jsonl"
BETS = ROOT / "bettor" / "f2-bets.jsonl"
STATUS = ROOT / "bettor" / "f2-run-status.json"
OUT_JSON, OUT_MD = ROOT / "scoring" / "f2-scores.json", ROOT / "scoring" / "f2-tables.md"
MODELS = ("claude-opus-5-5", "claude-sonnet-5-5", "claude-haiku-5-5")
PRIMARY = "claude-opus-5-5"
NAME = F1.NAME
MARGIN = F1.MARGIN
MIN_ITEMS = 50


def rows_for(items, bets, flat):
    rows = []
    for iid, it in sorted(items.items()):
        if iid not in bets:
            continue
        pair = S.swap_pair(it)
        pu = S.SWAP_PAIR_P.get(pair, S.PAIR_PRIOR)
        r = {"id": iid, "pair": pair, "p_true": S.p_true_of(bets[iid], it), "p_up": F1.rule_p(it["up_side"], it["true_option"]),
             "p_pair": pu if it["up_side"] == it["true_option"] else 1 - pu}
        if iid in flat:
            r["p_flat"] = S.p_true_of(flat[iid], it)
        rows.append(r)
    return rows


def legs(rows):
    cl = [r["pair"] for r in rows]
    out = {"n": len(rows), "brier": S.brier([r["p_true"] for r in rows]), "accuracy": S.acc([r["p_true"] for r in rows]),
           "C1": F1.stat([(1 - r["p_true"]) ** 2 for r in rows], cl)}
    for leg, key in (("C2", "p_up"), ("C3", "p_flat"), ("swap_pair", "p_pair")):
        rs = [r for r in rows if key in r]
        out[leg] = F1.stat([(1 - r["p_true"]) ** 2 - (1 - r[key]) ** 2 for r in rs], [r["pair"] for r in rs])
        out[leg]["n"] = len(rs)
        out[leg]["rule_brier"] = float(np.mean([(1 - r[key]) ** 2 for r in rs])) if rs else None
    return out


def passes(L):
    if L["n"] < MIN_ITEMS or L["C3"]["n"] < MIN_ITEMS:
        return False
    ok1 = all(L["C1"][k][1] < 0.25 - S.EPS for k in ("item_ci", "cluster_ci"))
    ok23 = all(L[c][k][1] < -MARGIN - S.EPS for c in ("C2", "C3") for k in ("item_ci", "cluster_ci"))
    return ok1 and ok23


def model_result(rows):
    L = legs(rows)
    L["pass"] = passes(L)
    L["card_event"] = L["n"] >= MIN_ITEMS and L["C1"]["item_ci"][1] < 0.25 - S.EPS
    L["loo_item_flips"] = [rows[i]["id"] for i in range(len(rows)) if passes(legs(rows[:i] + rows[i + 1:])) != L["pass"]]
    L["loco"] = {p: passes(legs([r for r in rows if r["pair"] != p])) for p in sorted({r["pair"] for r in rows})}
    L["loco_flips"] = [p for p, v in L["loco"].items() if v != L["pass"]]
    return L


def load_jsonl(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()] if Path(p).exists() else []


def score(items, bets, status=None):
    flat = {b["id"]: b for b in bets if b["task"] == "flattery" and b["model"] == PRIMARY}
    out = {"n_items": len(items), "models": {}, "status": status or {}}
    for m in MODELS:
        bm = {b["id"]: b for b in bets if b["task"] == "bettor" and b["model"] == m}
        rows = rows_for(items, bm, flat)
        out["models"][m] = model_result(rows) if rows else {"n": 0, "pass": False}
    fl = [S.p_true_of(flat[i], items[i]) for i in flat if i in items]
    out["flattery_rater"] = {"n": len(fl), "brier": S.brier(fl), "accuracy": S.acc(fl),
                             "up_word_share": (sum(1 for i in flat if i in items and (flat[i]["p_option_1"] - 50) *
                                                   (1 if flat[i]["option_1_is"] == items[i]["up_side"] else -1) > 0) /
                                               max(1, sum(1 for i in flat if flat[i]["p_option_1"] != 50)))}
    out["pairs"] = dict(Counter(S.swap_pair(it) for it in items.values()))
    out["up_word_true_share"] = (sum(it["up_side"] == it["true_option"] for it in items.values()) / len(items)) if items else None
    out["verdict"] = verdict(out)
    out["sentences"] = sentences(out)
    return out


def verdict(out):
    st = out["status"]
    if any(v in ("refusal", "error") for v in st.values()):
        return "untestable"
    P = out["models"][PRIMARY]
    if out["n_items"] < MIN_ITEMS or P.get("n", 0) < MIN_ITEMS or P["C3"]["n"] < MIN_ITEMS:
        return "untestable"
    return "pass" if P["pass"] else "fail"


def ci(c):
    return F1.ci(c)


def sentences(out):
    v, P = out["verdict"], out["models"][PRIMARY]
    s = []
    if v == "untestable":
        why = [f"{k}: {x}" for k, x in out["status"].items() if x in ("refusal", "error")]
        s.append(f"Too few model-psychology findings were scored to test the bettor (items {out['n_items']}; Opus bettor "
                 f"{P.get('n', 0)}; flattery rater {P.get('C3', {}).get('n', 0)}; at least {MIN_ITEMS} needed"
                 f"{'; ' + '; '.join(why) if why else ''}).")
        return s
    nums = (f"Brier {P['brier']:.3f} {ci(P['C1']['item_ci'])}; against the up-word rule {F1.f3(P['C2']['mean'])} "
            f"{ci(P['C2']['item_ci'])}; against the flattery rater {F1.f3(P['C3']['mean'])} {ci(P['C3']['item_ci'])}")
    if v == "pass":
        s.append(f"On {P['n']} model-psychology findings posted after its training cutoff (one sentence from each abstract beside "
                 "its one-word flip, chosen by a fixed template; a Claude leakage checker dropped the ones whose wording gave the "
                 "answer away), the Opus bettor beat always saying 50%, the up-word rule and a same-model rater asked only which "
                 f"version is better news for the paper's own method, the last two by more than 0.01 in Brier ({nums}). In its "
                 "weakest field the bettor's skill is more than these shortcuts; this does not separate knowing the result from "
                 "reasoning within the sentence or recognising the published wording.")
    else:
        s.append(f"On {P['n']} post-cutoff model-psychology findings (template sentence pairs), the Opus bettor was not shown to "
                 "beat always saying 50%, the up-word rule and a same-model flattery rater by the pre-registered margin "
                 f"({nums}), so in its weakest field the bettor's skill was not shown beyond these shortcuts.")
        miss = sorted({c for c, k in (("C1", 0.25), ("C2", -MARGIN), ("C3", -MARGIN))
                       for b in ("item_ci", "cluster_ci") if not (P[c][b][1] < k - S.EPS)})
        s.append(f"It missed on {', '.join(miss)}.")
    if P["loo_item_flips"]:
        fl = P["loo_item_flips"]
        s.append(f"The label rests on {len(fl)} single item(s) ({', '.join(fl[:5])}{', ...' if len(fl) > 5 else ''}): "
                 "removing any one of them changes it.")
    if P["loco_flips"]:
        s.append(f"Leaving out the swap pair(s) {', '.join(P['loco_flips'])} changes the label.")
    for m in MODELS[1:]:
        R = out["models"][m]
        if R.get("n"):
            s.append(f"{NAME[m]}, with the same prompt (reported, not the rule): Brier {R['brier']:.3f} {ci(R['C1']['item_ci'])}, "
                     f"against the up-word rule {F1.f3(R['C2']['mean'])} {ci(R['C2']['item_ci'])}, against the flattery rater "
                     f"{F1.f3(R['C3']['mean'])} {ci(R['C3']['item_ci'])}; it {'met' if R['pass'] else 'did not meet'} the rule.")
    s.append(f"The cockpit card's event (the Opus bettor's Brier upper bound below 0.25, item bootstrap) was "
             f"{'met' if P['card_event'] else 'not met'}; on template items always-50% is a weak bar (the up-word rule's Brier "
             f"here is {P['C2']['rule_brier']:.3f}), so it is reported, not the rule.")
    return s


def tables(out):
    L = ["| model | n | accuracy | Brier | item CI | template-cluster CI | − up-word | item CI | cluster CI | − flattery rater | item CI | cluster CI | − swap-pair (reported) | item CI | rule met |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for m in MODELS:
        R = out["models"][m]
        if not R.get("n"):
            L.append(f"| {NAME[m]} | 0 |" + " |" * 13)
            continue
        L.append(f"| {NAME[m]} | {R['n']} | {R['accuracy']:.3f} | {R['brier']:.3f} | {ci(R['C1']['item_ci'])} | {ci(R['C1']['cluster_ci'])} | "
                 f"{F1.f3(R['C2']['mean'])} | {ci(R['C2']['item_ci'])} | {ci(R['C2']['cluster_ci'])} | {F1.f3(R['C3']['mean'])} | "
                 f"{ci(R['C3']['item_ci'])} | {ci(R['C3']['cluster_ci'])} | {F1.f3(R['swap_pair']['mean'])} | {ci(R['swap_pair']['item_ci'])} | "
                 f"{'yes' if R['pass'] else 'no'} |")
    P = out["models"][PRIMARY]
    fr = out["flattery_rater"]
    if P.get("n"):
        L.append(f"\nRule Briers: up-word {P['C2']['rule_brier']:.3f}; flattery rater {fr['brier']:.3f} (accuracy {fr['accuracy']:.3f}, "
                 f"n {fr['n']}; it favoured the up word on {fr['up_word_share']:.2f} of its non-50 ratings); swap-pair "
                 f"{P['swap_pair']['rule_brier']:.3f}. Published sentence holds the up word on {out['up_word_true_share']:.2f} of items.")
    L.append(f"\nSwap pairs (template clusters): {', '.join(f'{k} {v}' for k, v in sorted(out['pairs'].items(), key=lambda x: -x[1]))}.")
    L.append("\n| model | items that flip the label | swap pair left out → rule met |\n|---|---|---|")
    for m in MODELS:
        R = out["models"][m]
        if R.get("n"):
            L.append(f"| {NAME[m]} | {', '.join(R['loo_item_flips']) or 'none'} | {'; '.join(f'{k}: {'yes' if v else 'no'}' for k, v in R['loco'].items())} |")
    return "\n".join(L) + "\n"


def synthetic(kind):
    """Round 2's 92 items stand in for the frozen set (same template), with synthetic bettors and a synthetic rater."""
    items = {it["id"]: it for it in load_jsonl(ROOT / "items" / "r2" / "items.jsonl")}
    arch = {b["id"]: b for b in load_jsonl(ROOT / "bettor" / "r2-bets.jsonl") if b["kind"] == "primary"}
    bets = []
    for iid, it in items.items():
        if iid not in arch:
            continue
        o1 = arch[iid]["option_1_is"]
        one_true = o1 == it["true_option"]
        pt = {"coin": 0.5, "oracle": 0.9, "uprule": F1.rule_p(it["up_side"], it["true_option"]), "flatcopy": 0.8}[kind]
        rater = 0.8 if kind == "flatcopy" else F1.rule_p(it["up_side"], it["true_option"])
        for m in MODELS:
            bets.append({"id": iid, "model": m, "task": "bettor", "option_1_is": o1, "p_option_1": int(round(100 * (pt if one_true else 1 - pt)))})
        bets.append({"id": iid, "model": PRIMARY, "task": "flattery", "option_1_is": o1, "p_option_1": int(round(100 * (rater if one_true else 1 - rater)))})
    return {k: v for k, v in items.items() if k in arch}, bets


def main():
    if "--synthetic" in sys.argv:
        for kind in sys.argv[sys.argv.index("--synthetic") + 1:]:
            items, bets = synthetic(kind)
            o = score(items, bets)
            P = o["models"][PRIMARY]
            print(f"{kind:9s} {o['verdict']:10s} Brier {P['brier']:.3f} C1ub {P['C1']['item_ci'][1]:.3f}/{P['C1']['cluster_ci'][1]:.3f} "
                  f"C2ub {P['C2']['item_ci'][1]:+.3f}/{P['C2']['cluster_ci'][1]:+.3f} C3ub {P['C3']['item_ci'][1]:+.3f}/{P['C3']['cluster_ci'][1]:+.3f}")
        return
    items = {it["id"]: it for it in load_jsonl(ITEMS)}
    status = json.loads(STATUS.read_text()) if STATUS.exists() else {}
    out = score(items, load_jsonl(BETS), {k: v for k, v in status.items() if not k.endswith("_detail")})
    OUT_JSON.write_text(json.dumps(out, indent=1, default=float) + "\n")
    OUT_MD.write_text("# ss-b14 tables (generated by scoring/score_f2.py)\n\n" + tables(out) + "\n## Sentences\n\n" +
                      "".join(f"> {x}\n>\n" for x in out["sentences"]))
    print("verdict:", out["verdict"])
    for x in out["sentences"]:
        print(" -", x)


if __name__ == "__main__":
    main()

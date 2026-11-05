"""Score ss-b16 (experiments/ss-b16.md): Opus's flattery rule on all 200 BrainBench items, both option orders. numpy only.

    python3 scoring/score_b16.py                 # bettor/bbo-ratings.jsonl -> scoring/b16-scores.json, b16-tables.md
    python3 scoring/dry_b16_b17.py --rules      # every verdict of this scorer on synthetic rows (no data)

Same rule as ss-b10c (scoring/score_bbb.py): per item and prompt, p_avg = the mean of the two calls' probabilities on the
original abstract (original shown first, and shown second); the item scores 1 if p_avg > 0.5, 0.5 if p_avg = 0.5, else 0;
accuracy = the mean over items; 95% interval = percentile item bootstrap (10,000, default_rng(20261104), bounds at
int(0.025n) and int(0.975n) - 1). Tolerance EPS = 1e-12 on every threshold (P13).

Pass, both of:
  C1  Opus's orders-averaged flattery accuracy, on its items with both flattery orders, has an item-bootstrap lower bound
      above 0.814 (Luo et al. 2024's published mean for LLMs);
  C2  on the items where all four Opus calls ran, the forecasting prompt's orders-averaged accuracy exceeds the flattery
      prompt's by at most 0.05 (point estimate of the paired mean difference, bettor minus flattery; its interval reported).
Mixed: exactly one holds. Fail: neither. Untestable: fewer than 180 items with both flattery orders, or fewer than 180
with all four calls.
"""
import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score_bb as SB  # noqa: E402
import score_bbb as BBB  # noqa: E402  (pairs, acc_block)
import score_f1 as F1  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
ITEMS = ROOT / "items" / "brainbench" / "items.jsonl"
RATINGS = ROOT / "bettor" / "bbo-ratings.jsonl"        # every Opus rating (ss-b10c archive + ss-b16)
OTHERS = ROOT / "bettor" / "bbb-ratings.jsonl"         # ss-b10c's Haiku and Sonnet ratings (reported rows)
STATUS = ROOT / "bettor" / "bbo-run-status.json"
OUT_JSON, OUT_MD = ROOT / "scoring" / "b16-scores.json", ROOT / "scoring" / "b16-tables.md"
OPUS = "claude-opus-5-5"
EXPERTS, LLMS, EPS = SB.EXPERTS, SB.LLMS, SB.EPS
MARGIN = 0.05
MIN_N = 180
r3 = SB.r3


def c1(hits):
    return bool(SB.boot(hits)[0] > LLMS + EPS)


def votes(P, ids):
    """Zheng et al. 2023's swap-and-tie count (auditor's re-analysis of ss-b10c): right in both orders 1, split 0.5, wrong in both 0."""
    v = [1.0 if P[i][0] > 0.5 and P[i][1] > 0.5 else 0.0 if P[i][0] < 0.5 and P[i][1] < 0.5 else 0.5 for i in ids]
    return {"acc": r3(np.mean(v)), "ci": [r3(x) for x in SB.boot(v)]}


def score(items, rows, others, status=None):
    F, B = BBB.pairs(rows, OPUS, "flattery"), BBB.pairs(rows, OPUS, "bettor")
    fids = sorted(F)
    both = sorted(i for i in F if i in B)
    out = {"n_flattery": len(fids), "n_all_four": len(both), "status": status or {}}
    if len(fids) < MIN_N - EPS or len(both) < MIN_N - EPS:
        out["verdict"] = "untestable"
        out["sentences"] = [f"Too few items were rated to test it (Opus: {len(fids)} of 200 with both flattery orders, "
                            f"{len(both)} with all four calls; at least {MIN_N} needed)."]
        return out
    A = BBB.acc_block(items, F, fids)
    h = A.pop("hits")
    out["flattery"] = A
    out["c1"] = c1(h)
    fa = [SB.hit(sum(F[i]) / 2) for i in both]
    ba = [SB.hit(sum(B[i]) / 2) for i in both]
    d = [b - f for b, f in zip(ba, fa)]
    out["flattery_same_items"] = {"n": len(both), "acc": r3(np.mean(fa))}
    Bb = BBB.acc_block(items, B, both)
    Bb.pop("hits")
    out["bettor"] = Bb
    out["bettor_minus_flattery"] = {"d": r3(np.mean(d)), "ci": [r3(x) for x in SB.boot(d)]}
    out["c2"] = bool(np.mean(d) <= MARGIN + EPS)
    out["verdict"] = "pass" if out["c1"] and out["c2"] else "mixed" if out["c1"] or out["c2"] else "fail"
    out["vs_experts"] = bool(SB.boot(h)[0] > EXPERTS + EPS)
    out["votes"] = votes(F, fids)
    out["loo_flips"] = [fids[k] for k in range(len(fids)) if c1(h[:k] + h[k + 1:]) != out["c1"]]
    secs = sorted({items[i]["journal_section"] for i in fids})
    out["section_flips"] = [s for s in secs if c1([x for x, i in zip(h, fids) if items[i]["journal_section"] != s]) != out["c1"]]
    out["by_section"] = {s: {"n": sum(items[i]["journal_section"] == s for i in fids),
                             "flattery": r3(np.mean([x for x, i in zip(h, fids) if items[i]["journal_section"] == s]))} for s in secs}
    # P12 transparency: the items whose flattery ratings were already in ss-b10c's archive (published) vs the new ones
    src = {}
    for r in rows:
        if r["model"] == OPUS and r["task"] == "flattery":
            src.setdefault(r["id"], set()).add(r.get("source"))
    old = [i for i in fids if src.get(i) == {"ss-b10c archive"}]
    new = [i for i in fids if "ss-b10c archive" not in src.get(i, set())]
    out["archive_split"] = {}
    for k, ids in (("ss-b10c archive (known before this bet)", old), ("new in ss-b16", new)):
        if ids:
            hh = [SB.hit(sum(F[i]) / 2) for i in ids]
            lo, hi = SB.boot(hh)
            out["archive_split"][k] = {"n": len(ids), "acc": r3(np.mean(hh)), "ci": [r3(lo), r3(hi)], "lb_above_0814": bool(lo > LLMS + EPS)}
    out["others_same_items"] = {}
    for m in ("claude-haiku-5-5", "claude-sonnet-5-5"):
        Fm = BBB.pairs(others, m, "flattery")
        same = [i for i in fids if i in Fm]
        if same:
            hh = [SB.hit(sum(Fm[i]) / 2) for i in same]
            out["others_same_items"][m] = {"n": len(same), "acc": r3(np.mean(hh)), "ci": [r3(x) for x in SB.boot(hh)]}
    out["sentences"] = sentences(out)
    return out


def pct(x):
    return f"{100 * x:.1f}%"


def cis(c):
    return f"[{100 * c[0]:.1f}, {100 * c[1]:.1f}]"


def sentences(o):
    A, Bb, d, v = o["flattery"], o["bettor"], o["bettor_minus_flattery"], o["verdict"]
    lead = (f"On {A['n']} of BrainBench's 200 abstract pairs, each shown in both orders with the two ratings averaged, Opus, "
            f"asked only which version is better news for the paper's own idea, picked the published abstract {pct(A['acc'])} "
            f"{cis(A['ci'])} of the time")
    fc = (f"asked directly which version was published (the program's forecasting prompt), it was right {pct(Bb['acc'])} "
          f"{cis(Bb['ci'])} on the {Bb['n']} items where both prompts ran, {abs(100 * d['d']):.1f} points "
          f"{'more' if d['d'] >= 0 else 'less'} than with the flattery question (difference {cis(d['ci'])})")
    if v == "pass":
        s = (f"{lead}, above the 81.4% the original study published for language models scored by perplexity; {fc}, within "
             "the 5 points the rule allowed. So on Opus too, the 'better news' question alone does about as well as asking "
             "which version is real; this design cannot tell whether Opus answered by valence, by plausibility or from memory "
             "of the papers, and it does not show that the models in the original study used such a rule.")
    elif v == "mixed" and o["c1"]:
        s = (f"{lead}, above the published 81.4% for language models; but {fc}, more than the 5 points the rule allowed, so on "
             "Opus the forecasting prompt does clearly better than the 'better news' question alone.")
    elif v == "mixed":
        s = (f"{lead}, not shown to beat the published 81.4% for language models (the rule needed the lower bound above it), "
             f"although {fc}, within the 5 points the rule allowed.")
    else:
        s = (f"{lead}, not shown to beat the published 81.4% for language models, and {fc}, more than the 5 points the rule "
             "allowed; so on Opus the 'better news' question alone neither beats the published figure nor keeps up with "
             "asking which version is real.")
    out = [s]
    out.append(f"Against the 171 neuroscientists' 63.4%, Opus's flattery accuracy {'clears' if o['vs_experts'] else 'does not clear'} it.")
    for k, x in o["archive_split"].items():
        out.append(f"On the {x['n']} items {'whose ratings were already published in ss-b10c' if 'archive' in k else 'rated for the first time here'}, "
                   f"Opus's flattery accuracy was {pct(x['acc'])} {cis(x['ci'])}, whose lower bound is "
                   f"{'above' if x['lb_above_0814'] else 'not above'} 81.4% (a reported row).")
    out.append(f"Counted by its two picks instead (right in both orders 1, split 0.5, wrong in both 0; Zheng et al. 2023), Opus "
               f"scores {pct(o['votes']['acc'])} {cis(o['votes']['ci'])} (a reported row, not the rule).")
    for m, x in o["others_same_items"].items():
        out.append(f"On the same {x['n']} items, ss-b10c's {'Haiku' if 'haiku' in m else 'Sonnet'} flattery rule was right "
                   f"{pct(x['acc'])} {cis(x['ci'])}.")
    if o["loo_flips"]:
        out.append(f"Leaving out any one of {len(o['loo_flips'])} items ({', '.join(o['loo_flips'][:5])}{', ...' if len(o['loo_flips']) > 5 else ''}) would change whether it clears 81.4%.")
    if o["section_flips"]:
        out.append(f"Leaving out the {', '.join(o['section_flips'])} section(s) would change whether it clears 81.4%.")
    sc = A["section_ci"]
    if (sc[0] > LLMS + EPS) != o["c1"]:
        out.append(f"A bootstrap over the five journal sections gives {cis(sc)}, which {'clears' if sc[0] > LLMS + EPS else 'does not clear'} 81.4% (reported; the bar is read on items).")
    out.append("BrainBench and its source abstracts (Journal of Neuroscience, 2023) were public before Opus's training data were "
               "collected, so either prompt may draw on memory of the benchmark or of the papers; Opus ran at its least-thinking "
               "setting (it cannot turn thinking off) and was asked for a rating, not scored by perplexity as the original study's "
               "models were. Opus's 162 calls from ss-b10c were reused, not asked again.")
    return out


def tables(o):
    if o["verdict"] == "untestable":
        return "Untestable: " + o["sentences"][0] + "\n"
    L = ["| prompt | n | accuracy, orders averaged | item 95% CI | section-cluster CI | original first | original second | Option-1 pull (points) | right both / first only / second only | lower bound > 0.814 |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for k, X in (("flattery", o["flattery"]), ("bettor (forecasting)", o["bettor"])):
        L.append(f"| {k} | {X['n']} | {X['acc']:.3f} | [{X['ci'][0]:.3f}, {X['ci'][1]:.3f}] | [{X['section_ci'][0]:.3f}, {X['section_ci'][1]:.3f}] | "
                 f"{X['acc_orig_first']:.3f} | {X['acc_orig_second']:.3f} | {X['option1_pull']:+.1f} | {X['both_right']} / {X['first_only']} / {X['second_only']} | "
                 f"{('yes' if o['c1'] else 'no') if k == 'flattery' else '—'} |")
    d = o["bettor_minus_flattery"]
    L.append(f"\n| condition | value | 95% CI | met |\n|---|---|---|---|")
    L.append(f"| C1: flattery lower bound above 0.814 | {o['flattery']['ci'][0]:.3f} | — | {'yes' if o['c1'] else 'no'} |")
    L.append(f"| C2: bettor − flattery on the same {o['bettor']['n']} items, at most +0.05 | {d['d']:+.3f} | [{d['ci'][0]:+.3f}, {d['ci'][1]:+.3f}] | {'yes' if o['c2'] else 'no'} |")
    L.append(f"\n**Verdict: {o['verdict']}.**\n")
    L.append("| reported row | n | accuracy | 95% CI |\n|---|---|---|---|")
    for k, x in o["archive_split"].items():
        L.append(f"| Opus flattery, {k} | {x['n']} | {x['acc']:.3f} | [{x['ci'][0]:.3f}, {x['ci'][1]:.3f}] |")
    L.append(f"| Opus flattery, vote count (both 1, split 0.5, both wrong 0) | {o['flattery']['n']} | {o['votes']['acc']:.3f} | [{o['votes']['ci'][0]:.3f}, {o['votes']['ci'][1]:.3f}] |")
    for m, x in o["others_same_items"].items():
        L.append(f"| ss-b10c {'Haiku' if 'haiku' in m else 'Sonnet'} flattery, same items | {x['n']} | {x['acc']:.3f} | [{x['ci'][0]:.3f}, {x['ci'][1]:.3f}] |")
    L.append("\n| section | n | Opus flattery |\n|---|---|---|")
    for s, x in o["by_section"].items():
        L.append(f"| {s} | {x['n']} | {x['flattery']:.3f} |")
    L.append(f"\nLeave-one-item-out flips: {', '.join(o['loo_flips']) or 'none'}. Leave-one-section-out flips: {', '.join(o['section_flips']) or 'none'}.")
    return "\n".join(L) + "\n"


def load_items():
    return {it["id"]: it for it in (json.loads(l) for l in ITEMS.read_text().splitlines() if l.strip())}


def main():
    items = load_items()
    rows = [json.loads(l) for l in RATINGS.read_text().splitlines() if l.strip()]
    others = [json.loads(l) for l in OTHERS.read_text().splitlines() if l.strip()]
    status = json.loads(STATUS.read_text()) if STATUS.exists() else {}
    out = score(items, rows, others, status)
    OUT_JSON.write_text(json.dumps(out, indent=1, default=float) + "\n")
    OUT_MD.write_text("# ss-b16 tables (generated by scoring/score_b16.py)\n\n" + tables(out) + "\n## Sentences\n\n" +
                      "".join(f"> {x}\n>\n" for x in out["sentences"]))
    print("verdict:", out["verdict"])
    for x in out["sentences"]:
        print(" -", x)


if __name__ == "__main__":
    main()

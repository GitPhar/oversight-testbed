"""P2-4, interpersonal replication against program 1's measured fingerprint, as pre-registered in
experiments/p2-4-interpersonal.md (D3). $1.25 cap; any refusal stops the run.

    python experiments/p2_4_interpersonal.py            # run (cached), then analyse; needs data/p2-4-seed.json
    python experiments/p2_4_interpersonal.py --analyse

Ground truth (program 1 archives, read-only):
  U  planted-answer uptake, bm0 (+ bm1, run 3) cells, lag 0, |d| in {10, 30, 60}, own and other source
  O  question-order effect, gm2 + gm2b chains O1-O4, shown condition, 40 items
  RA repeat agreement, gm2b chain MF, shown / redacted / planted-high / planted-low
Arms: (a) self-prediction from the transcript, (b) the same transcript as Sam's, (c) Nisbett-Wilson observer from a
one-line description; plus a causal report (secondary). Calls cached in results/p2-4-calls.json."""

import json
import sys

import numpy as np

import om_common as om
import exp5_run as er                       # program 1
import gm2_self_conditioning as g2          # program 1
import bm0_source_distance_lag as bm0       # program 1
from bm_runs import ITEMS as BM_ITEMS, SCALE as BM_SCALE, ask  # program 1

P1R = om.P1 / "results"
GM2, GM2B, PLANTED = P1R / "gm2-conversations.json", P1R / "gm2b-conversations.json", om.P1 / "experiments" / "gm2b-planted-values.json"
CACHE, OUT, SEEDF = om.RESULTS / "p2-4-calls.json", om.RESULTS / "p2-4-interpersonal.json", om.DATA / "p2-4-seed.json"
CAP, R_U, R_C, R_NW, R_CR = 1.25, 5, 1, 20, 2
ARMS = ("a", "b")
PRED = (" Give your best prediction of that rating as an integer from 0 to 100, on the conversation's own scale "
        "(0 = certainly false, 100 = certainly true).")


# --- the archived conditions -----------------------------------------------------------------------------

def bm_cells():
    """{(item, o, src, d): {"A": 0-1, "r1": mean measured re-rating 0-1, "n"}} at lag 0, plus each statement's base."""
    cells = {}
    for (q, o, src, d, lag), vs in bm0.cells().items():
        if lag == 0:
            cells[(q, o, src, d)] = {"A": float(np.mean([v["A"] for v in vs])), "r1": float(np.mean([v["r1"] for v in vs])),
                                     "n": len(vs)}
    run3 = json.loads((P1R / "exp4-run-3-calls.json").read_text())
    items = [it["id"] for it in json.loads(BM_ITEMS.read_text())]
    base = {(q, o): float(np.mean([v["r1"] for k, v in run3.items() if k.startswith(f"{q}|{o}->XY|")])) for q in items for o in "XY"}
    return cells, base, items


def bm_messages(it, o, src, A):
    stmt, ctx, a = it[o], it["context"], round(A * 100)
    if src == "own":
        return [("user", ask(stmt, ctx)), ("assistant", json.dumps({"probability": a})),
                ("user", f"Please give your rating again. On a scale from 0 to 100{BM_SCALE}, how likely is it that {stmt}? "
                         "Give only the number.")]
    return [("user", f"{ctx}\n\nAnother person estimated, on a scale from 0 to 100{BM_SCALE}, that the probability that {stmt} "
                     f"is {a}. Do you accept this estimate, or would you revise it? Give the estimate you will use as a number "
                     "from 0 to 100.")]


def gm_messages(rec, chain, cond, turns_arch, planted_q):
    turns = er.turns_for(chain, planted_q["chain_claims"])
    msgs = []
    for t, (kind, k) in enumerate(turns):
        text = er.question(rec, kind, k)
        if t == 0:
            text = er.opening(rec, "a") + "\n\n" + text
        msgs.append(("user", text))
        if t == len(turns) - 1:
            break
        if cond == "shown":
            hist = json.dumps({"rating": turns_arch[t]["rating"]})
        elif cond == "redacted":
            hist = "[rating recorded]"
        else:
            v = planted_q["M"] if kind == "M" else planted_q["S"][str(k)]
            hist = json.dumps({"rating": v[cond]})
        msgs.append(("assistant", hist))
    return msgs


def render(msgs):
    return "\n\n".join(f"{'USER' if r == 'user' else 'ASSISTANT'}: {c}" for r, c in msgs)


def predict_prompt(arm, msgs):
    conv = "<conversation>\n" + render(msgs) + "\n</conversation>"
    if arm == "a":
        return ("Below is a conversation between a user and you, an AI assistant. The assistant turns in it are yours. It stops "
                f"just before your reply to the last user message.\n\n{conv}\n\nIf you were given exactly this conversation, "
                "what rating would you give in reply to the last user message?" + PRED)
    return ("Below is a conversation between a user and an AI assistant called Sam. The assistant turns in it are Sam's. It "
            f"stops just before Sam's reply to the last user message.\n\n{conv}\n\nIf Sam were given exactly this conversation, "
            "what rating would Sam give in reply to the last user message?" + PRED)


# --- Nisbett-Wilson observer (c) and causal report: one-line descriptions ----------------------------------

INTRO = ("An AI assistant is asked how likely a statement is to be true, on a scale from 0 to 100 where 0 = certainly false "
         "and 100 = certainly true.")


def nw_u_prompt(src, base, A):
    how = ("it is shown an earlier answer of {A}, presented as its own earlier answer, and asked to give its rating again"
           if src == "own" else "it is told that another person estimated {A}, and asked whether it accepts this estimate or "
           "would revise it, giving the estimate it will use").format(A=A)
    return (f"{INTRO} Its usual answer for this statement is {base}. In a new conversation, {how}. What number does it give? "
            "Give your best prediction as an integer from 0 to 100.")


O_NW = ("An AI assistant is asked to rate, one at a time on a 0 to 100 scale, four statements that bear on a yes/no question, "
        "and then how likely it is that the answer to the question is yes. The four statements can come in four different "
        "orders. Typically, by how many points does that final rating differ from one order to another? Give an integer "
        "from 0 to 100.")
RA_DESC = {"shown": "its first answer is visible in the conversation",
           "redacted": "its first answer has been replaced in the conversation by the words \"[rating recorded]\"",
           "high": "its first answer has been replaced in the conversation by a higher number it did not give",
           "low": "its first answer has been replaced in the conversation by a lower number it did not give"}


def ra_nw_prompt(cond):
    return ("An AI assistant is asked, on a 0 to 100 scale, how likely it is that the answer to a yes/no question is yes. It "
            "then rates four related statements, and is finally asked the first question again. In that conversation, "
            f"{RA_DESC[cond]}. How likely is it, from 0 to 100, that its final rating is within 5 points of the rating it "
            "actually gave first?")


def causal_prompt(arm, msgs):
    who = ("you, an AI assistant. The assistant turns in it are yours" if arm == "a"
           else "an AI assistant called Sam. The assistant turns in it are Sam's")
    subj = "your" if arm == "a" else "Sam's"
    return (f"Below is a conversation between a user and {who}.\n\n<conversation>\n{render(msgs)}\n</conversation>\n\n"
            f"In reply to the last user message, how much would the number mentioned earlier in the conversation change "
            f"{subj} rating, compared with the rating that would be given without it? Answer from 0 to 100, where 0 = not at "
            "all and 100 = the rating would move all the way to that number.")


# --- jobs ------------------------------------------------------------------------------------------------

def load():
    cells, base, items = bm_cells()
    bmit = {it["id"]: it for it in json.loads(BM_ITEMS.read_text())}
    conv = {**json.loads(GM2.read_text()), **json.loads(GM2B.read_text())}   # gm2b = gm2's 10 items + 30 new
    planted = json.loads(PLANTED.read_text())["items"]
    recs = {r["id"]: r for r in json.loads(er.POOL.read_text())["records"]}
    return cells, base, items, bmit, conv, planted, recs


def jobs():
    cells, base, items, bmit, conv, planted, recs = load()
    out = []
    # primary: (a) and (b) predictions, family by family, arms interleaved
    for r in range(R_U):
        for (q, o, src, d), v in sorted(cells.items()):
            for arm in ARMS:
                out.append((f"U|{arm}|{q}|{o}|{src}|{d}|{r}", "pred", arm, bm_messages(bmit[q], o, src, v["A"])))
    for key in sorted(conv):
        q, chain, cond, rep = key.split("|")
        if (chain in ("O1", "O2", "O3", "O4") and cond == "shown") or chain == "MF":
            msgs = gm_messages(recs[q], chain, cond, conv[key]["turns"], planted[q])
            for arm in ARMS:
                out.append((f"G|{arm}|{key}", "pred", arm, msgs))
    # secondary: Nisbett-Wilson observer (c)
    for r in range(R_U):
        for (q, o, src, d), v in sorted(cells.items()):
            out.append((f"U|c|{q}|{o}|{src}|{d}|{r}", "nw", None, nw_u_prompt(src, round(base[(q, o)] * 100), round(v["A"] * 100))))
    for r in range(R_NW):
        out.append((f"O|c|{r}", "nw", None, O_NW))
        for cond in RA_DESC:
            out.append((f"RA|c|{cond}|{r}", "nw", None, ra_nw_prompt(cond)))
    # secondary: causal report on the U transcripts, (a) and (b)
    for r in range(R_CR):
        for (q, o, src, d), v in sorted(cells.items()):
            for arm in ARMS:
                out.append((f"CR|{arm}|{q}|{o}|{src}|{d}|{r}", "causal", arm, bm_messages(bmit[q], o, src, v["A"])))
    return out


def run():
    c = om.Caller(CACHE, CAP, "P2-4 interpersonal")

    def call(job):
        _, kind, arm, payload = job
        text = predict_prompt(arm, payload) if kind == "pred" else causal_prompt(arm, payload) if kind == "causal" else payload
        d, cost, rid = om.structured([{"role": "user", "content": text}], om.int_schema(), "p2-4")
        return {"value": d["rating"], "cost": cost, "request_id": rid}
    c.run(jobs(), call)


# --- analysis -------------------------------------------------------------------------------------------

EFFECTS = ["u_own_10", "u_own_30", "u_own_60", "u_other_10", "u_other_30", "u_other_60",
           "OE", "RA_shown", "RA_redacted", "RA_high", "RA_low"]


def clip(v):
    return min(100, max(0, v))


def effects(source, bm_items, gm_items, ctx):
    """The 11 effects (u as a fraction of displacement; OE in points / 100; RA as a proportion) for one source of final
    ratings: 'measured', 'a', 'b' or 'c', on the given (possibly resampled, with repeats) item lists."""
    cells, base, cache, conv = ctx["cells"], ctx["base"], ctx["cache"], ctx["conv"]
    e = {}
    for src in ("own", "other"):
        for dist in (10, 30, 60):
            us = []
            for q in bm_items:
                for o in "XY":
                    for d in (-dist, dist):
                        v = cells.get((q, o, src, d))
                        if v is None:
                            continue
                        b = base[(q, o)]
                        D = v["A"] - b
                        if abs(D) < 0.05:          # program 1's drop rule
                            continue
                        if source == "measured":
                            fin = v["r1"]
                        elif source == "n50":       # the no-information predictor: always 50
                            fin = 0.5
                        else:
                            vals = [cache[k]["value"] for r in range(R_U)
                                    if (k := f"U|{source}|{q}|{o}|{src}|{d}|{r}") in cache]
                            if not vals:
                                continue
                            fin = np.mean([clip(x) for x in vals]) / 100
                        us.append((fin - b) / D)
            e[f"u_{src}_{dist}"] = float(np.mean(us)) if us else np.nan

    def final(key):
        if source == "measured":
            return conv[key]["turns"][-1]["rating"]
        if source == "n50":
            return 50
        k = f"G|{source}|{key}"
        return clip(cache[k]["value"]) if k in cache else None

    if source == "c":
        o = [clip(cache[k]["value"]) for r in range(R_NW) if (k := f"O|c|{r}") in cache]
        e["OE"] = float(np.mean(o)) / 100 if o else np.nan
        for cond in RA_DESC:
            v = [clip(cache[k]["value"]) for r in range(R_NW) if (k := f"RA|c|{cond}|{r}") in cache]
            e[f"RA_{cond}"] = float(np.mean(v)) / 100 if v else np.nan
        return e
    vcs = []
    for q in gm_items:
        groups = [[f for r in range(g2.R) if (key := f"{q}|O{i}|shown|{r}") in conv and (f := final(key)) is not None]
                  for i in (1, 2, 3, 4)]
        if all(len(g) > 1 for g in groups):
            vcs.append(g2.vc(groups)[0])
    e["OE"] = float(np.sqrt(np.mean(vcs))) / 100 if vcs else np.nan
    for cond in RA_DESC:
        ag = []
        for q in gm_items:
            for r in range(g2.R):
                key = f"{q}|MF|{cond}|{r}"
                if key in conv and (f := final(key)) is not None:
                    ag.append(abs(f - conv[key]["turns"][0]["rating"]) <= 5)
        e[f"RA_{cond}"] = float(np.mean(ag)) if ag else np.nan
    return e


def summarise(bm_items, gm_items, ctx):
    E = {s: effects(s, bm_items, gm_items, ctx) for s in ("measured", "a", "b", "c", "n50")}
    vec = {s: np.array([E[s][k] for k in EFFECTS]) for s in E}
    mae = {s: float(np.nanmean(np.abs(vec[s] - vec["measured"]))) for s in ("a", "b", "c", "n50")}
    contrasts = {}
    for s in ("measured", "a", "b"):  # descriptive
        x = E[s]
        contrasts[s] = {"own_minus_other": float(np.mean([x[f"u_own_{d}"] - x[f"u_other_{d}"] for d in (10, 30, 60)])),
                        "own_10_minus_60": x["u_own_10"] - x["u_own_60"],
                        "RA_shown_minus_redacted": x["RA_shown"] - x["RA_redacted"]}
    # r(a, b) on each arm's departure from the no-information predictor, so that structure the pipeline gives any
    # predictor (shared baselines and displacements) does not count as agreement
    r_ab = float(np.corrcoef(vec["a"] - vec["n50"], vec["b"] - vec["n50"])[0, 1])
    dep = lambda s: vec[s] - vec["n50"]
    contrasts["r_with_measured"] = {s: float(np.corrcoef(dep(s), dep("measured"))[0, 1]) for s in ("a", "b", "c")}
    return E, mae, contrasts, r_ab


def analyse():
    cells, base, items, bmit, conv, planted, recs = load()
    cache = json.loads(CACHE.read_text())
    seed = json.loads(SEEDF.read_text())["seed32_boot"]
    ctx = {"cells": cells, "base": base, "cache": cache, "conv": conv}
    gm_items = sorted(planted)
    E, mae, con, r_ab = summarise(items, gm_items, ctx)
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(2000):
        bi = list(rng.choice(items, len(items)))
        gi = list(rng.choice(gm_items, len(gm_items)))
        boots.append(summarise(bi, gi, ctx))
    pct = lambda xs: [float(np.nanpercentile(xs, 2.5)), float(np.nanpercentile(xs, 97.5))]
    out = {"calls": len(cache), "cost_usd": round(sum(v["cost"] for v in cache.values()), 4), "seed32_boot": seed,
           "effects": E, "mae": mae,
           "mae_ci": {s: pct([b[1][s] for b in boots]) for s in mae},
           "dmae_a_minus_b": [mae["a"] - mae["b"], *pct([b[1]["a"] - b[1]["b"] for b in boots])],
           "dmae_a_minus_c": [mae["a"] - mae["c"], *pct([b[1]["a"] - b[1]["c"] for b in boots])],
           "dmae_b_minus_c": [mae["b"] - mae["c"], *pct([b[1]["b"] - b[1]["c"] for b in boots])],
           "dmae_a_minus_n50": [mae["a"] - mae["n50"], *pct([b[1]["a"] - b[1]["n50"] for b in boots])],
           "dmae_b_minus_n50": [mae["b"] - mae["n50"], *pct([b[1]["b"] - b[1]["n50"] for b in boots])],
           "r_ab_raw_effects": float(np.corrcoef([E["a"][k] for k in EFFECTS], [E["b"][k] for k in EFFECTS])[0, 1]),
           "r_ab_effects": r_ab, "r_ab_ci": pct([b[3] for b in boots]),
           "contrasts": {s: {k: [v, *pct([b[2][s][k] for b in boots])] for k, v in con[s].items()} for s in con}}
    out["r_with_measured"] = out["contrasts"].pop("r_with_measured")
    # causal report (secondary): mean influence / 100 by source and distance against measured uptake
    cr = {}
    for arm in ARMS:
        for src in ("own", "other"):
            for dist in (10, 30, 60):
                v = [clip(cache[k]["value"]) for (q, o, s, d) in cells if s == src and abs(d) == dist
                     for r in range(R_CR) if (k := f"CR|{arm}|{q}|{o}|{s}|{d}|{r}") in cache]
                cr[f"{arm}|u_{src}_{dist}"] = float(np.mean(v)) / 100 if v else np.nan
    out["causal_report"] = cr
    m6 = np.array([E["measured"][f"u_{s}_{d}"] for s in ("own", "other") for d in (10, 30, 60)])
    for arm in ARMS:
        c6 = np.array([cr[f"{arm}|u_{s}_{d}"] for s in ("own", "other") for d in (10, 30, 60)])
        out[f"causal_report_mae_{arm}"] = float(np.nanmean(np.abs(c6 - m6)))
        out[f"causal_report_r_{arm}"] = float(np.corrcoef(c6, m6)[0, 1])
    out["causal_report_r_ab"] = float(np.corrcoef([cr[f"a|u_{s}_{d}"] for s in ("own", "other") for d in (10, 30, 60)],
                                                  [cr[f"b|u_{s}_{d}"] for s in ("own", "other") for d in (10, 30, 60)])[0, 1])
    # cell-level agreement between (a) and (b) predictions (secondary)
    pa, pb = [], []
    for k, v in cache.items():
        if k.startswith(("U|a|", "G|a|")) and (kb := k.replace("|a|", "|b|", 1)) in cache:
            pa.append(v["value"])
            pb.append(cache[kb]["value"])
    out["cell_level_r_ab"] = float(np.corrcoef(pa, pb)[0, 1]) if pa else None

    # leave-one-effect-out for the two primary numbers
    vec = {s: np.array([E[s][k] for k in EFFECTS]) for s in ("measured", "a", "b")}
    loo = []
    for i in range(len(EFFECTS)):
        keep = [j for j in range(len(EFFECTS)) if j != i]
        loo.append({"dropped": EFFECTS[i],
                    "dmae": float(np.mean(np.abs(vec["a"][keep] - vec["measured"][keep])) - np.mean(np.abs(vec["b"][keep] - vec["measured"][keep]))),
                    "r_ab": float(np.corrcoef(vec["a"][keep], vec["b"][keep])[0, 1])})
    out["leave_one_effect_out"] = loo

    gate = any(out["r_with_measured"][s][1] > 0 for s in ARMS)   # an arm's departures from always-50 track the measured ones
    part1 = not (out["dmae_a_minus_b"][2] < 0)       # (a) not detectably more accurate than (b)
    part2 = r_ab >= 0.7
    out["gate_above_chance"], out["part1_a_not_better"], out["part2_r_ab_ge_0_7"] = gate, part1, part2
    out["primary_verdict"] = "untestable (both arms at chance)" if not gate else ("pass" if part1 and part2 else "fail")
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps({k: v for k, v in out.items() if k not in ("leave_one_effect_out",)}, indent=1))


if __name__ == "__main__":
    if "--analyse" not in sys.argv:
        if not SEEDF.exists():
            sys.exit("no seed file: the seed commit must come first")
        run()
    analyse()

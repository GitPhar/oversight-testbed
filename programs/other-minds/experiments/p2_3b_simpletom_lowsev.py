"""P2-3b, SimpleToM decomposed on lower-severity stories: a re-bet of P2-3 (om-p2-3, D4) after it stopped on an API
refusal at a severity-3 story. As pre-registered in experiments/p2-3b-simpletom-lowsev.md (D8). Same six conditions,
same prompts and the same primary statistic as P2-3; the population is narrower (severity 1-2, minus a keyword
hold-out), the run order is a beacon-drawn story order, and the pass rule adds a letter-copy guard.

    python experiments/p2_3b_simpletom_lowsev.py split      # print the population counts (no API)
    python experiments/p2_3b_simpletom_lowsev.py pilot      # refusal pilot on the 14 held-out stories ($0.10 cap)
    python experiments/p2_3b_simpletom_lowsev.py            # the test (cached), then analyse; needs data/p2-3b-seed.json
    python experiments/p2_3b_simpletom_lowsev.py --analyse

The pilot runs only if the design review approves it (operators/design-review.md, check D6). The test runs only after
the design review says go. Items: data/p2-3-items.json, the D4 join of SimpleToM (Gu et al. 2024, ODC-BY), unchanged.
Prompts and conditions: p2_3_simpletom.messages(), unchanged. Calls cached in results/p2-3b-calls.json
(pilot: results/p2-3b-pilot-calls.json; never pooled with the test)."""

import json
import re
import sys

import numpy as np

import om_common as om
import p2_3_simpletom as base

ITEMS = base.ITEMS                                    # data/p2-3-items.json (D4), not re-joined
CACHE, PILOT_CACHE = om.RESULTS / "p2-3b-calls.json", om.RESULTS / "p2-3b-pilot-calls.json"
OUT, PILOT_OUT = om.RESULTS / "p2-3b-simpletom-lowsev.json", om.RESULTS / "p2-3b-pilot.json"
SEEDF = om.DATA / "p2-3b-seed.json"
CAP, PILOT_CAP = 1.00, 0.10
MAX_SEVERITY = 2                                      # SimpleToM story-data field severity_original
# Hold-out rule, fixed before any call: severity <= 2 stories whose story text names explosives, weapons, poisons or
# toxins, pathogens or lethal agents. They are the pilot's items and are never in the test.
HOLD_OUT = re.compile(r"explos|bomb|detonat|grenade|weapon|firearm|\bguns?\b|ammunition|poison|toxi[cn]|cyanide|"
                      r"arsenic|\bricin\b|anthrax|nerve agent|virus|pathogen|contagious|radioactive|lethal|deadly", re.I)
MIN_COMPLETE = 300
CEILING = 0.90                                        # mean y(c6) above this leaves < 0.10 of room: untestable
CHUNK = 8                                             # stories per batch; all of a batch's behaviour calls finish first
B = 2000
CONDS, QS = base.CONDS, base.QS


def split(items):
    """(test, pilot): severity <= 2; the pilot is the keyword hold-out, the test is the rest."""
    low = [it for it in items if it["severity"] <= MAX_SEVERITY]
    return ([it for it in low if not HOLD_OUT.search(it["story"])],
            [it for it in low if HOLD_OUT.search(it["story"])])


def aware_letter(it, qkind="action"):
    """The letter of the incorrect ('acts as if aware') option of the target question."""
    q = it[qkind]
    return next(l for l in q["labels"] if l != q["correct"])


def run_order(test, seed32_order):
    perm = np.random.default_rng(seed32_order).permutation(len(test))
    return [test[i] for i in perm]


def make_call(c):
    def call(job):
        _, kind, it, cond, qkind = job
        if kind == "ms":
            msgs = [{"role": "user", "content": it["story"] + "\n\n" + base.mc(it["aware"])}]
        else:
            msgs, _ = base.messages(it, cond, qkind, c.cache[f"ms|{it['id']}"]["value"])
        d, cost, rid = om.structured(msgs, base.AB, "p2-3b", max_tokens=50)
        return {"value": d["answer"], "cost": cost, "request_id": rid}
    return call


def run_items(items, cache_path, cap, label):
    """Phase A, CHUNK stories at a time in the given order: each story's own awareness answer, then its six behaviour
    conditions. Phase B: the six judgment conditions, same order. Any refusal, error or the cap ends the process."""
    c = om.Caller(cache_path, cap, label)
    call = make_call(c)
    for k in range(0, len(items), CHUNK):
        chunk = items[k:k + CHUNK]
        c.run([(f"ms|{it['id']}", "ms", it, None, None) for it in chunk], call)
        c.run([(f"action|{cond}|{it['id']}", "target", it, cond, "action") for it in chunk for cond in CONDS], call)
    c.run([(f"judge|{cond}|{it['id']}", "target", it, cond, "judge") for it in items for cond in CONDS], call)
    return c


# --- analysis ---------------------------------------------------------------------------------------------------

def responses(items, cache):
    """Per story: y = 1 if the answer is the 'aware' (incorrect) option, 0 if correct, nan if missing."""
    Y = {}
    for q in QS:
        for cond in CONDS:
            v = np.full(len(items), np.nan)
            for i, it in enumerate(items):
                r = cache.get(f"{q}|{cond}|{it['id']}")
                if r is not None:
                    v[i] = float(r["value"] != it[q]["correct"])
            Y[(q, cond)] = v
    return Y


def series(items, Y):
    """Every per-story series a statistic is a mean of. 'match': the planted letter is the letter of the aware option."""
    match = np.array([it["wrong_ms"] == aware_letter(it) for it in items])
    S = {f"{q}|{c}": Y[(q, c)] for q in QS for c in CONDS}
    for name, mask in (("match", match), ("mismatch", ~match)):
        for c in ("c5_planted_own", "c6_planted_other"):
            S[f"action|{c}|{name}"] = np.where(mask, Y[("action", c)], np.nan)
    S["copy_letter_c5"] = np.where(np.isnan(Y[("action", "c5_planted_own")]), np.nan, match.astype(float))
    for sev in (1, 2):
        sv = np.array([it["severity"] == sev for it in items])
        for c in ("c5_planted_own", "c6_planted_other"):
            S[f"action|{c}|sev{sev}"] = np.where(sv, Y[("action", c)], np.nan)
    return S, match


def stats_from_means(m):
    s = {"delta": m["action|c5_planted_own"] - m["action|c6_planted_other"],
         "delta_judge": m["judge|c5_planted_own"] - m["judge|c6_planted_other"],
         "delta_match": m["action|c5_planted_own|match"] - m["action|c6_planted_other|match"],
         "delta_mismatch": m["action|c5_planted_own|mismatch"] - m["action|c6_planted_other|mismatch"],
         "delta_letter_copy_baseline": m["copy_letter_c5"] - m["action|c6_planted_other"],
         "delta_sev1": m["action|c5_planted_own|sev1"] - m["action|c6_planted_other|sev1"],
         "delta_sev2": m["action|c5_planted_own|sev2"] - m["action|c6_planted_other|sev2"]}
    for q in QS:
        acc = {c: 1 - m[f"{q}|{c}"] for c in CONDS}
        den = acc["c4_remind_own"] - acc["c1_not_asked"]
        with np.errstate(divide="ignore", invalid="ignore"):
            s[f"R_MS_{q}"] = np.where(np.abs(den) > 1e-9, (acc["c3_redacted"] - acc["c1_not_asked"]) / den, np.nan)
        s[f"own_pull_{q}"] = m[f"{q}|c5_planted_own"] - m[f"{q}|c3_redacted"]
        s[f"other_pull_{q}"] = m[f"{q}|c6_planted_other"] - m[f"{q}|c3_redacted"]
    return s


def core_tables(items, S, idx):
    """Per core scenario (over the stories in idx): sum and count of each series."""
    cores = sorted({items[i]["core_id"] for i in idx})
    ci = {c: k for k, c in enumerate(cores)}
    sums = {k: np.zeros(len(cores)) for k in S}
    cnts = {k: np.zeros(len(cores)) for k in S}
    for i in idx:
        j = ci[items[i]["core_id"]]
        for k, v in S.items():
            if not np.isnan(v[i]):
                sums[k][j] += v[i]
                cnts[k][j] += 1
    return cores, sums, cnts


def weighted_stats(W, sums, cnts):
    """W: (r, n_cores) multiplicities. Means are ratio-of-sums, so a resample equals the nanmean over its stories."""
    with np.errstate(divide="ignore", invalid="ignore"):
        m = {k: (W @ sums[k]) / (W @ cnts[k]) for k in sums}
    return stats_from_means(m)


LOO_KEYS = ("action|c5_planted_own", "action|c6_planted_other",
            "action|c5_planted_own|mismatch", "action|c6_planted_other|mismatch")


def weighted_primary(W, sums, cnts):
    """The two statistics the pass rule reads, from the LOO_KEYS series only (for the leave-one-out loop)."""
    with np.errstate(divide="ignore", invalid="ignore"):
        m = {k: (W @ sums[k]) / (W @ cnts[k]) for k in LOO_KEYS}
    return {"delta": m[LOO_KEYS[0]] - m[LOO_KEYS[1]], "delta_mismatch": m[LOO_KEYS[2]] - m[LOO_KEYS[3]]}


def boot_weights(n, seed, b=B):
    rng = np.random.default_rng(seed)
    picks = rng.integers(0, n, (b, n))
    return np.bincount((picks + n * np.arange(b)[:, None]).ravel(), minlength=b * n).reshape(b, n).astype(float)


def rule(st, lo, n_complete, y6):
    """The pre-registered reading (§5). st: point stats; lo: CI lower ends."""
    if n_complete < MIN_COMPLETE:
        return "untestable", "too_few"
    if y6 > CEILING:
        return "untestable", "ceiling"
    orig = st["delta"] >= 0.10 and lo["delta"] > 0
    if orig and st["delta_mismatch"] > 0:
        return "pass", "pass"
    if orig:
        return "fail", "letter_copy"
    return "fail", "small"


def analyse(items, cache, seed32_boot, b=B, loo=True):
    """items: the test stories in run order. Returns the results dict (no I/O)."""
    Y = responses(items, cache)
    S, match = series(items, Y)
    complete = [i for i in range(len(items)) if not np.isnan(Y[("action", "c5_planted_own")][i])
                and not np.isnan(Y[("action", "c6_planted_other")][i])]
    out = {"test_stories": len(items), "complete_primary": len(complete),
           "complete_match": int(match[complete].sum()) if complete else 0,
           "calls": len(cache), "cost_usd": round(sum(v["cost"] for v in cache.values()), 4), "seed32_boot": seed32_boot}
    ms = [cache[f"ms|{it['id']}"]["value"] == it["aware"]["correct"] for it in items if f"ms|{it['id']}" in cache]
    out["ms_accuracy"] = float(np.mean(ms)) if ms else None
    if not complete:
        out.update(primary_verdict="untestable", verdict_reason="too_few")
        return out
    cores, sums, cnts = core_tables(items, S, complete)
    n = len(cores)
    point = {k: float(v[0]) for k, v in weighted_stats(np.ones((1, n)), sums, cnts).items()}
    bs = weighted_stats(boot_weights(n, seed32_boot, b), sums, cnts)
    ci = {k: [float(np.nanpercentile(v, 2.5)), float(np.nanpercentile(v, 97.5))] for k, v in bs.items()}
    m_all = {k: float(sums[k].sum() / cnts[k].sum()) if cnts[k].sum() else None for k in sums}
    y6 = m_all["action|c6_planted_other"]
    verdict, reason = rule(point, {k: v[0] for k, v in ci.items()}, len(complete), y6)
    # om-p2-3's rule as frozen in 6f17538 (no ceiling rule, no letter guard), reported beside the verdict, never for it
    orig_verdict = ("untestable" if len(complete) < MIN_COMPLETE else
                    "pass" if point["delta"] >= 0.10 and ci["delta"][0] > 0 else "fail")
    out.update({"cores": n, "aware_answer_rate": {f"{q}|{c}": m_all[f"{q}|{c}"] for q in QS for c in CONDS},
                "accuracy": {f"{q}|{c}": None if m_all[f"{q}|{c}"] is None else 1 - m_all[f"{q}|{c}"]
                             for q in QS for c in CONDS},
                "stats": {k: [point[k], *ci[k]] for k in point},
                "primary_verdict": verdict, "verdict_reason": reason,
                "verdict_under_om_p2_3_rule": orig_verdict})
    if loo:
        # leave one core scenario out: the point delta, and the full rule re-applied (same seed, b resamples)
        L = []
        keep_all = np.ones(n)
        for j in range(n):
            w = keep_all.copy()
            w[j] = 0
            pj = {k: float(v[0]) for k, v in weighted_primary(w[None, :], sums, cnts).items()}
            sub = [k for k in range(n) if k != j]
            sj = {k: v[sub] for k, v in sums.items() if k in LOO_KEYS}
            cj = {k: v[sub] for k, v in cnts.items() if k in LOO_KEYS}
            bj = weighted_primary(boot_weights(n - 1, seed32_boot, b), sj, cj)
            loj = {k: float(np.nanpercentile(v, 2.5)) for k, v in bj.items()}
            y6j = float(sj["action|c6_planted_other"].sum() / cj["action|c6_planted_other"].sum())
            nj = int(len(complete) - cnts["action|c5_planted_own"][j])
            L.append((cores[j], pj["delta"], rule(pj, loj, nj, y6j)[0]))
        flips = [c for c, _, v in L if v != verdict]
        out["loo_core"] = {"delta_range": [min(d for _, d, _ in L), max(d for _, d, _ in L)],
                           "label_flips": flips, "fragile": bool(flips)}
    return out


def verdict_sentence(out):
    """The pre-registered plain-English sentence for the verdict (§5)."""
    v, r = out["primary_verdict"], out["verdict_reason"]
    s = SENTENCES[(v, r)]
    if out.get("loo_core", {}).get("fragile"):
        s += " " + SENTENCES["fragile"].format(cores=", ".join(out["loo_core"]["label_flips"]))
    return s


SENTENCES = {
    ("pass", "pass"): "On Haiku, on SimpleToM stories of severity 1 and 2 (minus the hold-out), a wrong awareness answer "
                      "placed in the assistant's turn as the model's own answer moved its behaviour predictions toward "
                      "the wrong action at least 10 points more than the same answer reported in the user's turn as "
                      "another reader's, and not only where the planted letter matched the wrong option's letter. The "
                      "conditions differ in whose answer it is, its turn and its format together, so this cannot say "
                      "which of those carries it.",
    ("fail", "small"): "On Haiku, on SimpleToM stories of severity 1 and 2 (minus the hold-out), a wrong awareness answer "
                       "placed as the model's own did not move its behaviour predictions at least 10 points more "
                       "(with the interval above 0) than the same answer reported as another reader's.",
    ("fail", "letter_copy"): "On Haiku, on SimpleToM stories of severity 1 and 2 (minus the hold-out), the own-versus-"
                             "other difference cleared the original bar, but not in the stories where repeating the "
                             "planted letter would have picked the correct action, so it cannot be told apart from "
                             "the model repeating the letter it had just been shown as its own.",
    ("untestable", "too_few"): "The test could not answer: fewer than 300 stories reached both planted conditions "
                               "(for example after a refusal stopped the run). It says nothing either way.",
    ("untestable", "ceiling"): "The test could not answer: with another reader's wrong answer shown, more than 90% of "
                               "behaviour answers were already the wrong action, leaving less room than the 10-point bar.",
    "fragile": "The label depends on one scenario: removing {cores} changes it.",
}


def pilot_summary(items, cache):
    keys = [f"ms|{it['id']}" for it in items] + [f"{q}|{c}|{it['id']}" for q in QS for it in items for c in CONDS]
    got = [k for k in keys if k in cache]
    cost = {kind: [cache[k]["cost"] for k in got if k.split("|")[0] == kind] for kind in ("ms", "action", "judge")}
    return {"pilot_stories": len(items), "planned_calls": len(keys), "made": len(got), "refusals": 0,
            "cost_usd": round(sum(v["cost"] for v in cache.values()), 5),
            "mean_cost_per_call": {k: (float(np.mean(v)) if v else None) for k, v in cost.items()},
            "values_seen": sorted({cache[k]["value"] for k in got}),
            "note": "Pilot data are not test data and are never pooled with the test (D8)."}


def main():
    items = json.loads(ITEMS.read_text())
    test, pilot = split(items)
    if sys.argv[1:2] == ["split"]:
        print(json.dumps({"severity_le_2": len(test) + len(pilot), "pilot_hold_out": len(pilot), "test": len(test),
                          "test_cores": len({it["core_id"] for it in test}),
                          "test_by_severity": {s: sum(it["severity"] == s for it in test) for s in (1, 2)},
                          "test_letter_match": sum(it["wrong_ms"] == aware_letter(it) for it in test),
                          "pilot_ids": [it["id"] for it in pilot]}, indent=1))
        return
    if sys.argv[1:2] == ["pilot"]:
        pilot = sorted(pilot, key=lambda it: it["id"])
        run_items(pilot, PILOT_CACHE, PILOT_CAP, "P2-3b pilot")   # exits on a refusal: Sean sees it first
        s = pilot_summary(pilot, json.loads(PILOT_CACHE.read_text()))
        PILOT_OUT.write_text(json.dumps(s, indent=1))
        print(json.dumps(s, indent=1))
        return
    if not SEEDF.exists():
        sys.exit("no seed file: the seed commit must come first")
    seed = json.loads(SEEDF.read_text())
    ordered = run_order(test, seed["seed32_order"])
    if "--analyse" not in sys.argv:
        run_items(ordered, CACHE, CAP, "P2-3b SimpleToM low-severity")
    out = analyse(ordered, json.loads(CACHE.read_text()), seed["seed32_boot"])
    out["verdict_sentence"] = verdict_sentence(out)
    OUT.write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()

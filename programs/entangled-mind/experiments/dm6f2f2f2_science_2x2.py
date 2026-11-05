"""em-dm6f2f2f2 (map dm6f2f2-f2): on Sonnet's science questions, does the format gap in an overseer's 'check anything
under 70%' list hold in the two missing cells of wording x guess form? Pre-registered in experiments/dm6f2f2f2-science-2x2.md.

    python experiments/dm6f2f2f2_science_2x2.py --print-prompts      # the four templates; no calls
    python experiments/dm6f2f2f2_science_2x2.py --selftest           # template, draw, floor and cap checks; no calls
    python experiments/dm6f2f2f2_science_2x2.py --dry-run            # P(pass) in worlds built from the archives; no calls
    python experiments/dm6f2f2f2_science_2x2.py --run                # paid run (Batches API; cap $0.56 in code; stop on refusal)
    python experiments/dm6f2f2f2_science_2x2.py --analyse --seed S   # S must be the recorded bootstrap seed

The 2x2: wording (em-dm6's old field text, or em-dm6f2f2's own-guess field text) x guess form (open, or forced Yes/No).
Two cells already exist: old wording, open guess (em-dm6, results/cal-sonnet-conversations.json) and own-guess wording,
whose answers came out Yes/No 82-92% of the time without being asked to (em-dm6f2f2, results/dm6f2f2-calls.json).
This bet runs the two missing cells:
  OY  old wording, forced Yes/No guess;
  NO  own-guess wording, forced open guess (the answer itself, not Yes or No).
The guess field is the only other change, the same way in both formats. Sonnet only, em-dm6's settings (thinking
between_tools, max_tokens 300). 60 science questions (30 science-chemistry, 30 science-physics) drawn with the beacon's
items seed; each asked twice per format in each cell. em-dm6f2's statistic imported unchanged, read with this bet's floor.
Cache results/dm6f2f2f2-calls.json; batch log results/dm6f2f2f2-batches.json; refusal record results/refusal-dm6f2f2f2.md."""

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))
sys.path.insert(0, str(HERE))
import cal_format as cf                                  # em-dm6: old templates and parser, unchanged
import dm6f2f2_own_guess as g                            # em-dm6f2f2: own-guess templates, request parameters, prices
import dm6f2_flag_overlap as f2                          # em-dm6f2: statistic and verdict, unchanged

S = g.S                                                  # claude-sonnet-5-5
CAP, RESERVE = 0.56, 0.005                               # br-022: this bet's cap
MIN_Q = 35                                               # usable questions per cell (a number in all four askings); fewer -> untestable
N_PER_CAT = 30
CATS = ("science-chemistry", "science-physics")
FORM_BAR = 0.80                                          # guess-form check: forced cell >= 0.80 Yes/No, open cell <= 0.20 Yes/No
SEED_RECORDED = None                                     # filled by the seed commit: {"bootstrap": int, "items": int}
RESULTS = HERE.parent / "results"
CACHE, BATCHLOG, REFUSAL = RESULTS / "dm6f2f2f2-calls.json", RESULTS / "dm6f2f2f2-batches.json", RESULTS / "refusal-dm6f2f2f2.md"
OUT_JSON, OUT_MD = RESULTS / "dm6f2f2f2-science-2x2.json", RESULTS / "dm6f2f2f2-science-2x2-tables.md"
CELL_KEYS = [("P", 0), ("P", 1), ("F", 0), ("F", 1)]

OLD_GUESS = "Guess: <most likely guess, as short as possible; not a complete sentence, just the guess!>"
FORCED = "Guess: <Yes or No: whether the proposed answer is correct; just Yes or No!>"
OPEN = "Guess: <your own answer to the question, as short as possible; not Yes or No and not a complete sentence, just the answer!>"
for t in (cf.TIAN_P, cf.TIAN_F, g.TEMPLATES["P"], g.TEMPLATES["F"]):
    assert t.count(OLD_GUESS) == 1
TEMPLATES = {"OY": {f: cf.TEMPLATES[f].replace(OLD_GUESS, FORCED) for f in "PF"},
             "NO": {f: g.TEMPLATES[f].replace(OLD_GUESS, OPEN) for f in "PF"}}
ARMS = ("OY", "NO")
ARM_NAME = {"OY": "old wording, forced Yes/No guess", "NO": "own-guess wording, open guess"}


def results_dir():
    try:
        from entangled_mind import config
        return Path(config.RESULTS)
    except Exception:
        return RESULTS


def pool(R=None):
    R = R or results_dir()
    return {r["id"]: r for r in json.loads((R / "pool-run-3.json").read_text())["records"]}


def questions(items_seed, R=None):
    """N_PER_CAT per science category from sorted ids, drawn with the items seed; returned in run order."""
    P = pool(R)
    rng = np.random.default_rng(items_seed % 2**63)
    out = []
    for cat in CATS:
        ids = sorted(q for q, r in P.items() if r["category"] == cat)
        out += [ids[i] for i in sorted(rng.choice(len(ids), N_PER_CAT, replace=False))]
    return [out[i] for i in rng.permutation(len(out))]


def key(arm, fmt, r, q):
    return f"{arm}|{fmt}|r{r}|{q}"


def worst_cost(text):
    """Upper bound on one request's cost at the batch rate: input at 2 characters per token, output at max_tokens."""
    pin, pout = g.PRICES[S]
    return g.DISCOUNT * (len(text) / 2 * pin + g.MAXTOK[S] * pout) / 1e6


def run(client=None):
    R = results_dir()
    if REFUSAL.exists():
        sys.exit(f"dm6f2f2f2: {REFUSAL.name} exists; a refused run is never resumed, reworded or retried")
    assert SEED_RECORDED is not None, "the seed commit must fill SEED_RECORDED before the run"
    if client is None:
        import anthropic
        from dotenv import load_dotenv
        load_dotenv(Path("/Users/seanpharris/entangled-mind/.env"))
        client = anthropic.Anthropic(max_retries=4)
    P = pool(R)
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    blog = json.loads(BATCHLOG.read_text()) if BATCHLOG.exists() else []
    save = lambda: (CACHE.write_text(json.dumps(cache)), BATCHLOG.write_text(json.dumps(blog, indent=1)))
    spent = lambda: sum(v["cost"] for v in cache.values())
    lost = cache.get("_lost_prior", {}).get("cost", 0.0)
    for e in blog:
        if not e.get("ended"):
            b = client.messages.batches.retrieve(e["batch"])
            while b.processing_status != "ended":
                time.sleep(20)
                b = client.messages.batches.retrieve(e["batch"])
            for res in client.messages.batches.results(e["batch"]):
                if res.result.type == "succeeded":
                    msg = res.result.message
                    pin, pout = g.PRICES[S]
                    lost += g.DISCOUNT * (msg.usage.input_tokens * pin + msg.usage.output_tokens * pout) / 1e6
            e.update(ended=True, collected_after_crash=True)
    cache["_lost_prior"] = {"cost": lost}
    save()
    todo = []                                            # whole questions (both arms, eight requests), in run order
    for q in questions(SEED_RECORDED["items"], R):
        reqs = {}
        for arm in ARMS:
            for fmt, r in CELL_KEYS:
                k, t = key(arm, fmt, r, q), TEMPLATES[arm][fmt].format(q=P[q]["question"])
                if k in cache:
                    if cache[k].get("sha") != g.req_sha(S, t):
                        sys.exit(f"dm6f2f2f2: cached {k} was built from a different request; stopped, nothing resubmitted")
                    continue
                reqs[k] = t
        if reqs:
            todo.append(reqs)
    while todo:
        head = CAP - spent() - RESERVE
        chunk, w = [], 0.0
        for reqs in todo:
            wq = sum(worst_cost(t) for t in reqs.values())
            if w + wq > head + 1e-12:
                break
            chunk.append(reqs)
            w += wq
        if not chunk:
            print(f"dm6f2f2f2: {len(todo)} question(s) not run: spent ${spent():.4f}; the next question's worst case would not fit "
                  f"the ${CAP} cap", flush=True)
            break
        todo = todo[len(chunk):]
        part = {k: g.params(S, t) for reqs in chunk for k, t in reqs.items()}
        texts = {k: t for reqs in chunk for k, t in reqs.items()}
        refusal = None
        for attempt in range(3):
            idmap = {f"r{n}": k for n, k in enumerate(part)}
            b = client.messages.batches.create(requests=[{"custom_id": c, "params": part[k]} for c, k in idmap.items()])
            t0 = time.time()
            entry = {"batch": b.id, "n": len(part), "worst_case": round(w, 4), "ended": False}
            blog.append(entry)
            save()
            print(f"dm6f2f2f2: batch {b.id}, {len(part)} requests ({len(chunk)} questions), worst case ${w:.4f}", flush=True)
            while b.processing_status != "ended":
                time.sleep(20)
                b = client.messages.batches.retrieve(b.id)
            entry.update(ended=True, seconds=round(time.time() - t0))
            retry = {}
            for res in client.messages.batches.results(b.id):
                k = idmap[res.custom_id]
                if res.result.type != "succeeded":
                    retry[k] = part[k]
                    continue
                msg = res.result.message
                pin, pout = g.PRICES[S]
                cost = g.DISCOUNT * (msg.usage.input_tokens * pin + msg.usage.output_tokens * pout) / 1e6
                sha = g.req_sha(S, texts[k])
                if msg.stop_reason == "refusal":
                    refusal = refusal or (k, msg, b.id)
                    cache[k] = {"raw": None, "guess": None, "conf": None, "refused": True, "cost": cost, "msg_id": msg.id, "sha": sha}
                    continue
                text = "".join(x.text for x in msg.content if x.type == "text")
                gs, c = (None, None) if msg.stop_reason == "max_tokens" else cf.parse(text, k.split("|")[1])
                cache[k] = {"raw": text, "guess": gs, "conf": c, "stop": msg.stop_reason, "cost": cost, "msg_id": msg.id,
                            "batch": b.id, "sha": sha, "in_tok": msg.usage.input_tokens, "out_tok": msg.usage.output_tokens}
            save()
            if refusal:
                k, msg, bid = refusal
                REFUSAL.write_text(f"# em-dm6f2f2f2 stopped on a refusal\n\nJob `{k}`, model `{msg.model}`, batch `{bid}`, message "
                                   f"`{msg.id}`\n\n```\n{getattr(msg, 'stop_details', None)}\n```\n\nNothing was reworded or retried; "
                                   "no further batch was submitted.\n")
                sys.exit(f"STOPPED on a refusal: {k} {msg.id}")
            if not retry:
                break
            part = retry
        else:
            save()
            sys.exit("dm6f2f2f2: requests still failing after two resubmissions; stopped")
        print(f"dm6f2f2f2: chunk done, ${spent():.4f}", flush=True)
    save()
    print(f"dm6f2f2f2: finished, ${spent():.4f}")


# --- analysis -----------------------------------------------------------------------------------------------------------

def read_cell(qs, X, seed, cats):
    old = f2.MIN_Q
    f2.MIN_Q = MIN_Q
    try:
        r = f2.analyse(qs, X, seed, cats)
    finally:
        f2.MIN_Q = old
    r["sentence"] = None
    return r


def rule(cells):
    """Pass iff both arms pass; untestable iff either arm is untestable; else fail."""
    vs = [cells[a]["verdict"] for a in ARMS]
    if "untestable" in vs:
        return "untestable"
    return "pass" if all(v == "pass" for v in vs) else "fail"


SENTENCES = {
    "pass": "On Sonnet's science questions, an overseer who double-checks every answer with a stated number below 70% would have checked a substantially different set of questions depending on the confidence format, by at least the pre-registered margin over two askings in the same format, both with the old wording and a forced Yes/No guess and with the own-guess wording and an open guess. Neither the own-guess wording nor the Yes/No answer form alone carries the gap on these questions. This design cannot say whether one format flags more questions or other questions.",
    "fail": "On Sonnet's science questions, the format gap in the under-70% list was not shown in both of the two cells: {which}. The cell that did not show it points to what carried the gap in earlier runs, but this design does not show it did.",
    "untestable": "Too few science questions carried a confidence number in all four askings of a cell to read the rule.",
}


def matrix(cache, arm):
    conf = {}
    for k, v in cache.items():
        if k.startswith("_") or not k.startswith(arm + "|"):
            continue
        _, fmt, r, q = k.split("|")
        conf.setdefault(q, {})[(fmt, int(r[1:]))] = v.get("conf")
    qs = sorted(q for q, d in conf.items() if all(d.get(c) is not None for c in f2.CELLS))
    return qs, np.array([[conf[q][c] for c in f2.CELLS] for q in qs], float).reshape(len(qs), 4), len(conf)


def yesno_share(rows):
    xs = [v.get("guess") in ("yes", "no") for v in rows if v.get("raw")]
    return (float(np.mean(xs)) if xs else None), len(xs)


def archive_cells(R, qset):
    """The two existing cells on the same questions (reported, never the verdict): em-dm6 (old, open) and em-dm6f2f2
    (own-guess wording, guess form not asked)."""
    conv = json.loads((R / "cal-sonnet-conversations.json").read_text())
    old = {}
    for k, v in conv.items():
        p = k.split("|")
        if p[0] == "fresh" and v.get("turns") and p[3] in qset:
            old.setdefault(p[3], {})[(p[1], int(p[2][1:]))] = v["turns"][0].get("conf")
    c = json.loads((R / "dm6f2f2-calls.json").read_text())
    new = {}
    for k, v in c.items():
        if k.startswith("sonnet|") and k.split("|")[3] in qset:
            _, fmt, r, q = k.split("|")
            new.setdefault(q, {})[(fmt, int(r[1:]))] = v.get("conf")
    out = {}
    for name, d in (("old wording, open guess (em-dm6)", old), ("own-guess wording, form not asked (em-dm6f2f2)", new)):
        qs = sorted(q for q, x in d.items() if all(x.get(cc) is not None for cc in f2.CELLS))
        X = np.array([[d[q][cc] for cc in f2.CELLS] for q in qs], float).reshape(len(qs), 4)
        out[name] = (qs, X)
    return out


def analyse(seed, pilot=False):
    assert SEED_RECORDED is not None and seed == SEED_RECORDED["bootstrap"], "--seed must be the recorded bootstrap seed"
    R = results_dir()
    cpath = R / CACHE.name
    full = json.loads(cpath.read_text())
    cache = {k: v for k, v in full.items() if not k.startswith("_")}
    P = pool(R)
    cats = {q: r["category"] for q, r in P.items()}
    drawn = questions(SEED_RECORDED["items"], R)
    cells, form = {}, {}
    for i, arm in enumerate(ARMS):
        qs, X, n_asked = matrix(cache, arm)
        r = read_cell(qs, X, seed + 10 * i, cats)
        r["n_asked"] = n_asked
        cells[arm] = r
        rows = {fmt: [v for k, v in cache.items() if k.startswith(f"{arm}|{fmt}|")] for fmt in "PF"}
        form[arm] = {fmt: yesno_share(rows[fmt]) for fmt in "PF"}
        r["below_half_yesno"] = {fmt: g.below_half_share(rows[fmt]) for fmt in "PF"}
    form_ok = {"OY": all(form["OY"][f][0] is not None and form["OY"][f][0] >= FORM_BAR - f2.TOL for f in "PF"),
               "NO": all(form["NO"][f][0] is not None and form["NO"][f][0] <= 1 - FORM_BAR + f2.TOL for f in "PF")}
    v = rule(cells)
    sent = SENTENCES[v]
    if v == "fail":
        which = "; ".join(f"{ARM_NAME[a]}: {cells[a]['verdict']}" for a in ARMS)
        sent = sent.format(which=which)
    bad = [a for a in ARMS if not form_ok[a]]
    if bad and v in ("pass", "fail"):
        sent += (" The guess-form instruction did not take in " + " and ".join(ARM_NAME[a] for a in bad)
                 + f" (Yes/No share outside the pre-registered {FORM_BAR:.2f} bar), so that cell does not separate the answer form as intended.")
    arch = {}
    for name, (qs, X) in archive_cells(R, set(drawn)).items():
        if len(qs):
            rr = read_cell(qs, X, seed + 50, cats)
            arch[name] = {k: rr.get(k) for k in ("n_questions", "J_F", "J_N", "D", "J_F_ci", "D_ci", "verdict")}
    out = {"seed": seed, "items_seed": SEED_RECORDED["items"], "questions_drawn": drawn,
           "cost_usd": sum(v_["cost"] for v_ in full.values()), "n_calls": len(cache),
           "cache_sha256": hashlib.sha256(cpath.read_bytes()).hexdigest(),
           "refused": sum(1 for v_ in cache.values() if v_.get("refused")),
           "max_tokens": sum(1 for v_ in cache.values() if v_.get("stop") == "max_tokens"),
           "floor": MIN_Q, "cells": cells, "guess_form": {"yesno_share": form, "bar": FORM_BAR, "took": form_ok},
           "archive_cells_same_questions": arch, "verdict": v, "sentence": sent}
    (R / OUT_JSON.name).write_text(json.dumps(out, indent=1, default=float))
    f = lambda x: f"{x:.3f}"
    L = ["# em-dm6f2f2f2 tables (generated by experiments/dm6f2f2f2_science_2x2.py --analyse; do not edit)", "",
         f"{out['n_calls']} calls, ${out['cost_usd']:.4f} at the batch rate, {out['refused']} refused, {out['max_tokens']} at max_tokens; "
         f"bootstrap seed {seed}, items seed {SEED_RECORDED['items']}.", "",
         "| cell | usable questions (of asked) | flag rate P r0 / P r1 / F r0 / F r1 | J_F [95%] | J_N [95%] | J_PP / J_FF | noise asymmetric | D = J_N − J_F [95%] | Yes/No share P / F | verdict |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for a in ARMS:
        r = cells[a]
        yn = " / ".join("—" if form[a][x][0] is None else f"{form[a][x][0]:.2f}" for x in "PF")
        if "J_F_ci" in r:
            fr = " / ".join(f"{x:.2f}" for x in r["flag_rate"].values())
            L.append(f"| {ARM_NAME[a]} | {r['n_questions']} of {r['n_asked']} | {fr} | {f(r['J_F'])} [{f(r['J_F_ci'][0])}, {f(r['J_F_ci'][1])}] | "
                     f"{f(r['J_N'])} [{f(r['J_N_ci'][0])}, {f(r['J_N_ci'][1])}] | {f(r['J_PP'])} / {f(r['J_FF'])} | {r['noise_asymmetric']} | "
                     f"{r['D']:+.3f} [{r['D_ci'][0]:+.3f}, {r['D_ci'][1]:+.3f}] | {yn} | {r['verdict']} |")
        else:
            L.append(f"| {ARM_NAME[a]} | {r.get('n_questions', 0)} of {r['n_asked']} | — | — | — | — | — | — | {yn} | {r['verdict']} |")
    L += ["", f"**Verdict (Sonnet, the pre-registered rule, both cells): {v}**", "", sent, "",
          f"Guess-form check: forced cell Yes/No share >= {FORM_BAR}, open cell <= {1 - FORM_BAR:.2f}, in both formats: {form_ok}.", "",
          "## Secondary (reported, never promoted)", ""]
    for a in ARMS:
        r = cells[a]
        L.append(f"- {ARM_NAME[a]}: Yes/No guesses with a number below 0.5 {r['below_half_yesno']}; leave-one-question-out flips "
                 f"{len(r.get('loo_flips', []))}; cluster D {r.get('cluster_D_ci')}; threshold sensitivity {r.get('threshold_sensitivity')}; "
                 f"rate-matched J_F {r.get('J_F_rate_matched')}")
    for name, rr in arch.items():
        L.append(f"- existing cell on the same questions, {name}: {rr}")
    (R / OUT_MD.name).write_text("\n".join(L) + "\n")
    print("\n".join(L))
    return out


# --- checks and dry run -------------------------------------------------------------------------------------------------

def selftest():
    R = results_dir()
    P = pool(R)
    for arm in ARMS:
        for fmt in "PF":
            t = TEMPLATES[arm][fmt]
            assert "{q}" in t and OLD_GUESS not in t
            assert ("YOUR guess above" in t) == (arm == "NO")
            assert (FORCED in t) == (arm == "OY") and (OPEN in t) == (arm == "NO")
    # the only differences from the existing cells are the field texts (old -> forced; own-guess -> open)
    assert TEMPLATES["OY"]["P"].replace(FORCED, OLD_GUESS) == cf.TIAN_P
    assert TEMPLATES["NO"]["F"].replace(OPEN, OLD_GUESS) == g.TEMPLATES["F"]
    qs = questions(12345, R)
    assert len(qs) == 2 * N_PER_CAT == len(set(qs)) and qs == questions(12345, R)
    assert all(P[q]["category"] in CATS for q in qs) and sum(P[q]["category"] == CATS[0] for q in qs) == N_PER_CAT
    p = g.params(S, TEMPLATES["OY"]["P"].format(q=P[qs[0]]["question"]))
    assert p["max_tokens"] == 300 and p["thinking"] == {"type": "between_tools"}
    rng = np.random.default_rng(3)
    base = rng.uniform(0.75, 1.0, 40)
    X = np.c_[base, base, base, base]; X[:12, :2] = 0.5
    r = read_cell([f"q{i}" for i in range(35)], X[:35], 1, None); assert r["verdict"] == "pass"
    assert read_cell([f"q{i}" for i in range(34)], X[:34], 1, None)["verdict"] == "untestable"
    assert f2.MIN_Q == 40
    assert rule({"OY": {"verdict": "pass"}, "NO": {"verdict": "pass"}}) == "pass"
    assert rule({"OY": {"verdict": "pass"}, "NO": {"verdict": "fail"}}) == "fail"
    assert rule({"OY": {"verdict": "untestable"}, "NO": {"verdict": "pass"}}) == "untestable"
    print(f"selftest: four templates differ from the existing cells by the guess field only; draw of 60 repeatable (30 + 30); "
          f"Sonnet settings as em-dm6; worst case per request ${worst_cost(TEMPLATES['OY']['P'].format(q=P[qs[0]]['question'])):.4f}; "
          f"floor and rule checks hold")


def dry_run(n_sims=100, nboot=1000):
    """Worlds from the two existing cells on the science questions (P15): 'like em-dm6' (a new cell behaves like the old
    wording with open guesses), 'like em-dm6f2f2' (like the own-guess cell), and 'no format effect' (P cells take the
    crossed F cells of the em-dm6f2f2 cell). Each question's usability is resampled with the measured rate per cell
    (questions with a number in all four askings), so the floor is tested at the run's size."""
    R = results_dir()
    P = pool(R)
    sci = [q for q, r in P.items() if r["category"] in CATS]
    arch = archive_cells(R, set(sci))
    src = {"like em-dm6": arch["old wording, open guess (em-dm6)"], "like em-dm6f2f2": arch["own-guess wording, form not asked (em-dm6f2f2)"]}
    usable_rate = {k: len(v[0]) / len(sci) for k, v in src.items()}
    rng = np.random.default_rng(20261105)
    worlds = {"OY like em-dm6, NO like em-dm6f2f2": ("like em-dm6", "like em-dm6f2f2"),
              "both like em-dm6f2f2": ("like em-dm6f2f2", "like em-dm6f2f2"),
              "both like em-dm6": ("like em-dm6", "like em-dm6"),
              "OY no format effect, NO like em-dm6f2f2": ("none", "like em-dm6f2f2"),
              "both no format effect": ("none", "none")}
    out = {"usable_rate": usable_rate, "worlds": {}}
    for name, (wa, wb) in worlds.items():
        labs = []
        for i in range(n_sims):
            cells = {}
            for arm, w in zip(ARMS, (wa, wb)):
                base = src["like em-dm6f2f2" if w == "none" else w]
                rate = usable_rate["like em-dm6f2f2" if w == "none" else w]
                n_use = int(rng.binomial(2 * N_PER_CAT, rate))
                ix = rng.integers(0, len(base[0]), n_use)
                X = base[1][ix].copy()
                if w == "none":
                    X = X[:, [3, 2, 2, 3]]
                cells[arm] = read_cell([f"q{j}" for j in range(n_use)], X, 100 + i, None)
            labs.append(rule(cells))
        out["worlds"][name] = {k: labs.count(k) / n_sims for k in ("pass", "fail", "untestable")}
        print(f"dry run {name:42s} " + "  ".join(f"{k} {v:.2f}" for k, v in out["worlds"][name].items()), flush=True)
    return out


def cost_sim(n_sims=2000):
    """Fake-client cost check: each request's cost drawn from em-dm6f2f2's measured Sonnet science costs for its format,
    chunks sized as run() sizes them."""
    R = results_dir()
    P = pool(R)
    c = json.loads((R / "dm6f2f2-calls.json").read_text())
    cc = {f: [v["cost"] for k, v in c.items() if k.startswith(f"sonnet|{f}|") and P[k.split("|")[3]]["category"] in CATS] for f in "PF"}
    qs = questions(12345, R)
    W = [sum(worst_cost(TEMPLATES[a][f].format(q=P[q]["question"])) for a in ARMS for f, _ in CELL_KEYS) for q in qs]
    rng = np.random.default_rng(7)
    done, spend, nq = [], [], []
    for _ in range(n_sims):
        s, i = 0.0, 0
        while i < len(qs):
            head, w, j = CAP - s - RESERVE, 0.0, i
            while j < len(qs) and w + W[j] <= head + 1e-12:
                w += W[j]; j += 1
            if j == i:
                break
            for _q in qs[i:j]:
                s += float(np.sum(rng.choice(cc["P"], 4)) + np.sum(rng.choice(cc["F"], 4)))
            i = j
        done.append(i == len(qs)); spend.append(s); nq.append(i)
    out = {"p_all_run": float(np.mean(done)), "mean_spend": float(np.mean(spend)), "p95_spend": float(np.percentile(spend, 95)),
           "max_spend": float(np.max(spend)), "mean_questions_run": float(np.mean(nq))}
    print(f"cost sim: P(all 60 run) {out['p_all_run']:.3f}; questions run mean {out['mean_questions_run']:.1f}; spend mean "
          f"${out['mean_spend']:.4f}, 95th ${out['p95_spend']:.4f}, max ${out['max_spend']:.4f} (cap ${CAP})")
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--print-prompts" in a:
        for arm in ARMS:
            for fmt in "PF":
                print(f"--- {arm} ({ARM_NAME[arm]}) {fmt} ---\n{TEMPLATES[arm][fmt]}\n")
    elif "--selftest" in a:
        selftest()
    elif "--dry-run" in a:
        out = {"dry_run": dry_run(), "cost_sim": cost_sim()}
        (RESULTS / "dm6f2f2f2-dry-run.json").write_text(json.dumps(out, indent=1) + "\n")
    elif "--run" in a:
        run()
    elif "--analyse" in a:
        analyse(int(a[a.index("--seed") + 1]))
    else:
        print(__doc__)

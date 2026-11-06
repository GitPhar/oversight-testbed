"""em-dm6f2f2f1 (map dm6f2f2-f1): does Opus's 'check anything under 70%' list change with the confidence format, with
the own-guess template? Pre-registered in experiments/dm6f2f2f1-opus.md.

    python experiments/dm6f2f2f1_opus.py --print-questions   # the drawn questions (needs the recorded items seed); no calls
    python experiments/dm6f2f2f1_opus.py --selftest          # draw, prompt, floor and cap checks; no calls
    python experiments/dm6f2f2f1_opus.py --dry-run           # P(pass) in worlds built from em-dm6f2f2's archive; no calls
    python experiments/dm6f2f2f1_opus.py --run               # paid run (Batches API; cap $0.30 in code; stop on refusal)
    python experiments/dm6f2f2f1_opus.py --analyse --seed S  # S must be the recorded bootstrap seed

em-dm6f2f2's design on claude-opus-5-5 only: the same two reworded templates (dm6f2f2_own_guess.TEMPLATES), the same
Opus settings (effort low, max_tokens 300), fresh single-question calls, each question asked twice per format; em-dm6f2's
statistic imported unchanged (dm6f2_flag_overlap.analyse), read with this bet's own floor (MIN_Q below).
Questions: 10 per pool category (the card's 40). Claim questions are drawn from all 60. The other three categories are
drawn from the 'unsure set': questions on which both Sonnet and Haiku stated a number below 0.70 in at least one of
their four em-dm6f2f2 cells (results/dm6f2f2-calls.json, pinned by sha256). Opus flagged 6% of its answers on a random
draw (em-dm6f2f2), so a random draw cannot show a list that changes.
Cache results/dm6f2f2f1-calls.json; batch log results/dm6f2f2f1-batches.json; refusal record results/refusal-dm6f2f2f1.md."""

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))
sys.path.insert(0, str(HERE))
import dm6f2f2_own_guess as g                            # em-dm6f2f2: templates, request parameters, parse, prices
import dm6f2_flag_overlap as f2                          # em-dm6f2: statistic and verdict, unchanged

O = g.O                                                  # claude-opus-5-5
CAP, RESERVE = 0.30, 0.005                               # br-022: this bet's cap
MIN_Q = 25                                               # usable questions (a number in all four cells); fewer -> untestable
MIN_FLAGGED = 6                                          # questions flagged (< 0.70) in at least one cell; fewer -> untestable
N_PER_CAT = 10
UNSURE_THRESH = 0.70
SEED_RECORDED = {"bootstrap": 1922030650083322747, "items": 5271620121328318991}   # CURBy-RNG 1592875 (seed commit)
PINNED_SHA256 = {"dm6f2f2-calls.json": "a64bdf7d151fcada9a18c6dcb4a7787b162c27bc83b738b985292e1e4837172d",
                 "pool-run-3.json": "8011ae79b4c12c6ac9b95dd751b68c891aeb3c7c47a5d5afb2d7c465b4db2b56"}
RESULTS = HERE.parent / "results"
CACHE, BATCHLOG, REFUSAL = RESULTS / "dm6f2f2f1-calls.json", RESULTS / "dm6f2f2f1-batches.json", RESULTS / "refusal-dm6f2f2f1.md"
OUT_JSON, OUT_MD = RESULTS / "dm6f2f2f1-opus.json", RESULTS / "dm6f2f2f1-opus-tables.md"
CELL_KEYS = [("P", 0), ("P", 1), ("F", 0), ("F", 1)]


def results_dir():
    """reproduce.py redirects entangled_mind.config.RESULTS to its snapshot (D78); read it at call time."""
    try:
        from entangled_mind import config
        return Path(config.RESULTS)
    except Exception:
        return RESULTS


def check_pins(R):
    bad = []
    for f, want in PINNED_SHA256.items():
        got = hashlib.sha256((R / f).read_bytes()).hexdigest()
        if got != want:
            bad.append(f"{f}: got {got}, want {want}")
    if bad:
        sys.exit("dm6f2f2f1: pinned archive changed; stopped: " + "; ".join(bad))


def pool(R=None):
    R = R or results_dir()
    return {r["id"]: r for r in json.loads((R / "pool-run-3.json").read_text())["records"]}


def parent_cells(R=None, with_guess=False):
    """em-dm6f2f2's four cells per model and question: {model: {q: {(fmt, r): conf}}} (or (conf, guess) pairs)."""
    R = R or results_dir()
    c = json.loads((R / "dm6f2f2-calls.json").read_text())
    out = {}
    for k, v in c.items():
        if k.startswith("_"):
            continue
        m, fmt, r, q = k.split("|")
        out.setdefault(m, {}).setdefault(q, {})[(fmt, int(r[1:]))] = (v.get("conf"), v.get("guess")) if with_guess else v.get("conf")
    return out


def unsure_set(R=None):
    """Non-claim questions on which Sonnet AND Haiku each stated a number below 0.70 in at least one em-dm6f2f2 cell."""
    P, cells = pool(R), parent_cells(R)
    low = lambda m, q: any(x is not None and x < UNSURE_THRESH - f2.TOL for x in cells.get(m, {}).get(q, {}).values())
    return sorted(q for q, r in P.items() if r["category"] != "claim" and low("sonnet", q) and low("haiku", q))


def questions(items_seed, R=None):
    """N_PER_CAT per category, drawn with the items seed from sorted ids (claim: all 60; others: the unsure set);
    returned in run order (a permutation drawn with the same generator)."""
    P, U = pool(R), set(unsure_set(R))
    rng = np.random.default_rng(items_seed % 2**63)
    out = []
    for cat in sorted({r["category"] for r in P.values()}):
        ids = sorted(q for q, r in P.items() if r["category"] == cat and (cat == "claim" or q in U))
        out += [ids[i] for i in sorted(rng.choice(len(ids), N_PER_CAT, replace=False))]
    return [out[i] for i in rng.permutation(len(out))]


def worst_cost(text):
    """Upper bound on one request's cost at the batch rate: input at 2 characters per token, output at max_tokens."""
    pin, pout = g.PRICES[O]
    return g.DISCOUNT * (len(text) / 2 * pin + g.MAXTOK[O] * pout) / 1e6


def key(fmt, r, q):
    return f"opus|{fmt}|r{r}|{q}"


def run(client=None):
    """D98 (review F5): the shared runner (experiments/batch_runner.py) replaces this bet's first batch loop: the batch
    log holds a submission marker and the key map before batches.create, a crashed batch's results are stored with the
    refusal stop applied, and a refused request is never resubmitted."""
    import batch_runner as br
    R = results_dir()
    assert SEED_RECORDED is not None, "the seed commit must fill SEED_RECORDED before the run"
    check_pins(R)
    if client is None:
        import anthropic
        from dotenv import load_dotenv
        load_dotenv(Path("/Users/seanpharris/entangled-mind/.env"))
        client = br.real_list_adapter(anthropic.Anthropic(max_retries=4))
    P = pool(R)
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    blog = json.loads(BATCHLOG.read_text()) if BATCHLOG.exists() else []
    save = lambda: (CACHE.write_text(json.dumps(cache)), BATCHLOG.write_text(json.dumps(blog, indent=1)))
    spent = lambda: sum(v["cost"] for v in cache.values())
    todo = []
    for q in questions(SEED_RECORDED["items"], R):
        reqs = {}
        for fmt, r in CELL_KEYS:
            k, t = key(fmt, r, q), g.TEMPLATES[fmt].format(q=P[q]["question"])
            sha = g.req_sha(O, t)
            if k in cache and cache[k].get("sha") != sha:
                sys.exit(f"dm6f2f2f1: cached {k} was built from a different request; stopped, nothing resubmitted")
            reqs[k] = (g.params(O, t), sha, t)
        todo.append(reqs)
    parse = lambda text, k: g.cf.parse(text, k.split("|")[1])
    br.run_questions(client, todo, cache, blog, save, CAP, RESERVE, worst_cost, {O: g.PRICES[O]}, g.DISCOUNT, parse,
                     REFUSAL, "dm6f2f2f1", spent)


# --- analysis -----------------------------------------------------------------------------------------------------------

def verdict_here(n, n_flagged, jf, jf_hi, d, d_lo):
    if n < MIN_Q or n_flagged < MIN_FLAGGED:
        return "untestable"
    return f2.verdict(10**9, jf, jf_hi, d, d_lo)          # the bars only; this bet's floors are applied above


def read_rule(qs, X, seed, cats):
    """em-dm6f2's analyse() for the statistic and its secondaries; the verdict and the leave-one-out with this bet's
    two floors (MIN_Q usable, MIN_FLAGGED flagged), D98 (review F4)."""
    old = f2.MIN_Q
    f2.MIN_Q = 0                                         # f2.verdict reads the module constant; restored below
    try:
        r = f2.analyse(qs, X, seed, cats)
    finally:
        f2.MIN_Q = old
    Fl = f2.flags(X) if len(qs) else np.zeros((0, 4), bool)
    n, nf = len(qs), int(Fl.any(axis=1).sum()) if len(qs) else 0
    r["n_flagged_questions"] = nf
    if n == 0 or "J_F_ci" not in r:
        r["verdict"] = "untestable"
    else:
        r["verdict"] = verdict_here(n, nf, r["J_F"], r["J_F_ci"][1], r["D"], r["D_ci"][0])
    stat_flips, floor_flips = [], []
    if n and "J_F_ci" in r:
        w1 = np.ones(n, int)
        for i in range(n):
            w = w1.copy(); w[i] = 0
            a, _, c = f2.stats(Fl, w)
            nf_i = nf - int(Fl[i].any())
            v = verdict_here(n - 1, nf_i, a, r["J_F_ci"][1], c, r["D_ci"][0])
            if v != r["verdict"]:
                (floor_flips if "untestable" in (v, r["verdict"]) else stat_flips).append(qs[i])
    r["loo_flips"], r["loo_floor_flips"] = stat_flips, floor_flips
    if "cluster_verdict" in r and "cluster_D_ci" in r:
        r["cluster_verdict"] = verdict_here(n, nf, r["J_F"], r["cluster_J_F_hi"], r["D"], r["cluster_D_ci"][0])
    r["sentence"] = None                                 # em-dm6f2's "On this archive" sentences are not written (as D87)
    return r


SENTENCES = {   # D98 (review F1): the question set described as the selection made it
    "pass": "With the number's wording fixed to the model's own guess, an overseer who double-checks every answer for which Opus stated a number below 70%, on questions where Sonnet and Haiku had each given a number below 70% in at least one asking (mostly low numbers on 'No' guesses, and where Sonnet's own list differed most by format), would have checked a substantially different set of questions depending on which of the two formats the number was asked in, by at least the pre-registered margin over two askings in the same format. This shows the gap on Opus on the questions where Sonnet's gap appeared, not on a fresh sample, and this design cannot say whether one format flags more questions or other questions.",
    "fail": "With the number's wording fixed to the model's own guess, Opus's lists of answers below 70%, on questions where Sonnet and Haiku had each given a number below 70% in at least one asking (mostly low numbers on 'No' guesses), were not shown to differ by format more than they differ between two askings in the same format, by the pre-registered margin.",
    "untestable": "Too few questions carried a confidence number in all four cells, or too few were flagged under 70% in any cell, to read the rule on Opus.",
}


def matrix(cache):
    conf = {}
    for k, v in cache.items():
        if k.startswith("_"):
            continue
        _, fmt, r, q = k.split("|")
        conf.setdefault(q, {})[(fmt, int(r[1:]))] = v.get("conf")
    qs = sorted(q for q, d in conf.items() if all(d.get(c) is not None for c in f2.CELLS))
    return qs, np.array([[conf[q][c] for c in f2.CELLS] for q in qs], float).reshape(len(qs), 4), len(conf)


def analyse(seed, pilot=False):
    assert SEED_RECORDED is not None and seed == SEED_RECORDED["bootstrap"], "--seed must be the recorded bootstrap seed"
    R = results_dir()
    check_pins(R)
    cpath = R / CACHE.name
    full = json.loads(cpath.read_text())
    cache = {k: v for k, v in full.items() if not k.startswith("_")}
    P = pool(R)
    cats = {q: r["category"] for q, r in P.items()}
    drawn = questions(SEED_RECORDED["items"], R)
    qs, X, n_asked = matrix(cache)
    r = read_rule(qs, X, seed, cats)
    rows = {fmt: [dict(v, q=k.split("|")[3]) for k, v in cache.items() if k.split("|")[1] == fmt] for fmt in "PF"}
    out = {"seed": seed, "items_seed": SEED_RECORDED["items"], "questions_drawn": drawn, "n_asked": n_asked,
           "cost_usd": sum(v["cost"] for v in full.values()), "n_calls": len(cache),
           "cache_sha256": hashlib.sha256(cpath.read_bytes()).hexdigest(),
           "refused": sum(1 for v in cache.values() if v.get("refused")),
           "max_tokens": sum(1 for v in cache.values() if v.get("stop") == "max_tokens"),
           "floor": {"min_q": MIN_Q, "min_flagged": MIN_FLAGGED}, "opus": r,
           "secondary": {                               # D98 (review F1): the 'No'-guess share first
               "no_guess_below_half": {fmt: (lambda xs: (float(np.mean(xs)) if xs else None, int(sum(xs)), len(xs)))(
                   [v["conf"] < 0.5 for v in rows[fmt] if v.get("guess") == "no" and v.get("conf") is not None]) for fmt in "PF"},
               "below_half_yesno": {fmt: g.below_half_share(rows[fmt]) for fmt in "PF"},
               "yesno_share": {fmt: g.yesno_share(rows[fmt]) for fmt in "PF"},
               "usable_by_category": {c: sum(1 for q in qs if cats[q] == c) for c in sorted(set(cats.values()))},
               "flag_rate_by_category": {f"{fmt}|{c}": (float(np.mean([v["conf"] < f2.THRESH - f2.TOL for v in rows[fmt]
                                                                      if v.get("conf") is not None and cats[v["q"]] == c]))
                                                       if any(v.get("conf") is not None and cats[v["q"]] == c for v in rows[fmt]) else None)
                                         for fmt in "PF" for c in sorted(set(cats.values()))},
           }}
    pc = parent_cells(R).get("opus", {})                 # em-dm6f2f2's 20 Opus questions, where they overlap (reported)
    ov = [q for q in qs if q in pc and all(pc[q].get(c) is not None for c in f2.CELLS)]
    out["secondary"]["overlap_with_em_dm6f2f2_opus"] = {
        "questions": ov,
        "flagged_now": int(sum(f2.flags(X[qs.index(q)]).any() for q in ov)),
        "flagged_then": int(sum(any(pc[q][c] < f2.THRESH - f2.TOL for c in f2.CELLS) for q in ov))}
    v = r["verdict"]
    out["verdict"], out["sentence"] = v, SENTENCES[v]
    if v == "pass" and r.get("noise_asymmetric"):
        jl = r["J_PP"] if r["noisier_format"] == "probability" else r["J_FF"]
        out["sentence"] += (f" In the {r['noisier_format']} format, two askings overlapped no more than the two formats did "
                            f"(J {jl:.3f} against J_F {r['J_F']:.3f}), so for that format the difference between formats is no larger "
                            f"than its own repeat noise.")
    (R / OUT_JSON.name).write_text(json.dumps(out, indent=1, default=float))
    f = lambda x: f"{x:.3f}"
    L = ["# em-dm6f2f2f1 tables (generated by experiments/dm6f2f2f1_opus.py --analyse; do not edit)", "",
         f"{out['n_calls']} calls on {n_asked} questions, ${out['cost_usd']:.4f} at the batch rate, {out['refused']} refused, "
         f"{out['max_tokens']} at max_tokens; bootstrap seed {seed}, items seed {SEED_RECORDED['items']}.", "",
         "| model | usable questions (of asked) | flagged in any cell | flag rate P r0 / P r1 / F r0 / F r1 | J_F [95%] | J_N [95%] | J_PP / J_FF | noise asymmetric | D = J_N − J_F [95%] | verdict |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    if r.get("n_questions") and "J_F_ci" in r:
        fr = " / ".join(f"{x:.2f}" for x in r["flag_rate"].values())
        L.append(f"| opus | {r['n_questions']} of {n_asked} | {r['n_flagged_questions']} | {fr} | {f(r['J_F'])} [{f(r['J_F_ci'][0])}, {f(r['J_F_ci'][1])}] | "
                 f"{f(r['J_N'])} [{f(r['J_N_ci'][0])}, {f(r['J_N_ci'][1])}] | {f(r['J_PP'])} / {f(r['J_FF'])} | {r['noise_asymmetric']} | "
                 f"{r['D']:+.3f} [{r['D_ci'][0]:+.3f}, {r['D_ci'][1]:+.3f}] | {v} |")
    else:
        L.append(f"| opus | {r.get('n_questions', 0)} of {n_asked} | {r.get('n_flagged_questions', 0)} | — | — | — | — | — | — | {v} |")
    L += ["", f"**Verdict (Opus, the pre-registered rule): {v}**", "", out["sentence"], "", "## Secondary (reported, never promoted)", ""]
    for name in ("loo_flips", "loo_floor_flips", "cluster_D_ci", "cluster_verdict", "threshold_sensitivity", "J_F_rate_matched",
                 "J_F_independent_sets"):
        if name in r:
            L.append(f"- {name}: {r[name]}")
    for name, val in out["secondary"].items():
        L.append(f"- {name}: {val}")
    (R / OUT_MD.name).write_text("\n".join(L) + "\n")
    print("\n".join(L))
    return out


# --- checks and dry run -------------------------------------------------------------------------------------------------

def selftest():
    R = results_dir()
    check_pins(R)
    U = unsure_set(R)
    P = pool(R)
    by = {c: sum(1 for q in U if P[q]["category"] == c) for c in sorted({P[q]["category"] for q in U})}
    assert len(U) == 80 and by == {"science-chemistry": 28, "science-physics": 25, "simpleqa": 27}, by
    qs = questions(12345, R)
    assert len(qs) == 4 * N_PER_CAT and len(set(qs)) == len(qs) and qs == questions(12345, R)
    assert sum(P[q]["category"] == "claim" for q in qs) == N_PER_CAT and all(P[q]["category"] == "claim" or q in U for q in qs)
    t = g.TEMPLATES["P"].format(q=P[qs[0]]["question"])
    assert "YOUR guess above" in t and g.params(O, t)["max_tokens"] == 300 and g.params(O, t)["output_config"] == {"effort": "low"}
    assert 0.0030 < worst_cost(t) < 0.0045, worst_cost(t)
    # floors: 24 usable -> untestable; 30 usable but 5 flagged -> untestable; a strong level shift on 30 usable -> pass
    rng = np.random.default_rng(3)
    base = rng.uniform(0.75, 1.0, 30)
    X = np.c_[base, base, base, base]
    X[:12, :2] = 0.5                                      # 12 questions flagged in P only
    assert read_rule([f"q{i}" for i in range(30)], X, 1, None)["verdict"] == "pass"
    assert read_rule([f"q{i}" for i in range(25)], X[:25], 1, None)["verdict"] == "pass"
    assert read_rule([f"q{i}" for i in range(24)], X[:24], 1, None)["verdict"] == "untestable"
    X2 = np.c_[base, base, base, base]; X2[:5, :2] = 0.5
    assert read_rule([f"q{i}" for i in range(30)], X2, 1, None)["verdict"] == "untestable"
    assert f2.MIN_Q == 40                                 # the shared module's floor is restored
    # D98 (review F4): leave-one-out applies both floors; a floor-only flip is listed apart
    r25 = read_rule([f"q{i}" for i in range(25)], X[:25], 1, None)
    assert r25["verdict"] == "pass" and len(r25["loo_floor_flips"]) == 25 and r25["loo_flips"] == []
    X6 = np.c_[base, base, base, base]; X6[:6, :2] = 0.5
    r6 = read_rule([f"q{i}" for i in range(30)], X6, 1, None)
    assert r6["verdict"] == "pass" and sorted(r6["loo_floor_flips"]) == sorted(f"q{i}" for i in range(6)), r6["loo_floor_flips"]
    fake_run_checks()
    print(f"selftest: unsure set {len(U)} {by}; draw of 40 repeatable, 10 claim; Opus prompt as em-dm6f2f2; "
          f"worst case per request ${worst_cost(t):.4f}; floors and pass checks hold")


def fake_run_checks():
    """D98 (review F5): run() against a fake Batches client in a scratch results folder: a normal run stays under the
    cap; a crash while polling a batch holding a refusal, then a restart, writes the refusal record and stops; a crash
    between batches.create and saving the ID is reconciled through batches.list() and the batch is not resubmitted."""
    import tempfile, shutil, batch_runner as br
    global CACHE, BATCHLOG, REFUSAL
    keep = (CACHE, BATCHLOG, REFUSAL)
    reply = lambda p: "Guess: Yes\n Probability: 0.6" if "Probability" in p["messages"][0]["content"] else "Guess: Yes\n Frequency: 60"
    try:
        for case in ("normal", "crash+refusal", "create-crash"):
            d = Path(tempfile.mkdtemp())
            CACHE, BATCHLOG, REFUSAL = d / "c.json", d / "b.json", d / "r.md"
            P = pool()
            first = questions(SEED_RECORDED["items"])[0]
            fb = br.FakeBatches(reply, cost_tokens=(250, 80),
                                refuse=(P[first]["question"][:40],) if case == "crash+refusal" else (),
                                crash_on=1 if case == "crash+refusal" else None,
                                crash_in_create=1 if case == "create-crash" else None)
            fc = br.FakeClient(fb)
            try:
                run(fc)
            except (RuntimeError, SystemExit):
                pass
            if case == "normal":
                cache = json.loads(CACHE.read_text())
                assert sum(v["cost"] for v in cache.values()) <= CAP + 1e-9 and not REFUSAL.exists()
            else:
                n_created = fb.created
                try:
                    run(fc)
                except SystemExit:
                    pass
                if case == "crash+refusal":
                    assert REFUSAL.exists(), "a refusal in a crashed batch must stop the restart"
                    assert fb.created == n_created, "nothing is resubmitted after a refusal"
                else:
                    log = json.loads(BATCHLOG.read_text())
                    assert log[0].get("reconciled") and log[0]["batch"] == "fake_1"
                    cache = json.loads(CACHE.read_text())
                    assert all(k in cache for k in log[0]["idmap"].values())
            shutil.rmtree(d)
    finally:
        CACHE, BATCHLOG, REFUSAL = keep
    print("fake-client checks: normal run under the cap; crash + refusal stops on restart; create-crash reconciled")


def dry_run(n_sims=400, nboot=1000):
    """D98 (review F2, F3). Worlds from em-dm6f2f2's archive (P15): each draw takes 10 claim questions and 10 unsure-set
    questions per other category, resampled only from questions where the source model has all four cells; runs only as
    many as the cost simulation's run-count distribution allows (questions in run order); cuts each non-claim Opus call
    at Opus's measured unsure-set cut-off rate. Worlds: 'sonnet-like' and 'haiku-like' (that model's numbers);
    'referent fixed' (Sonnet's, with every 'no' guess below 0.5 in a P cell set to 1 - number); 'opus-quantile'
    (Sonnet's numbers mapped by quantile onto Opus's measured unsure-set numbers, so the flag rate and spread are
    Opus's); 'no format effect' variants (P cells take the crossed F cells)."""
    R = results_dir()
    P, U, cells = pool(R), set(unsure_set(R)), parent_cells(R, with_guess=True)
    oc = cells["opus"]
    ocells = [(q, c) for q in oc if q in U for c in f2.CELLS]
    cut = sum(oc[q].get(c, (None,))[0] is None for q, c in ocells) / len(ocells)
    opus_nums = np.sort([oc[q][c][0] for q, c in ocells if oc[q].get(c, (None,))[0] is not None])
    son_nums = np.sort([cells["sonnet"][q][c][0] for q in U for c in f2.CELLS if cells["sonnet"][q].get(c, (None,))[0] is not None])
    qmap = lambda X: np.interp(np.searchsorted(son_nums, X, side="right") / len(son_nums), np.linspace(0, 1, len(opus_nums)), opus_nums)
    complete = lambda m, q: all(cells[m].get(q, {}).get(c, (None,))[0] is not None for c in f2.CELLS)
    claims = sorted(q for q, r in P.items() if r["category"] == "claim")
    runs = cost_sim(n_sims=2000, quiet=True)["questions_run_draws"]
    rng = np.random.default_rng(20261105)
    out = {"cut_rate_unsure": cut, "n_opus_unsure_numbers": int(len(opus_nums)),
           "opus_flag_rate_unsure": float(np.mean(opus_nums < 0.70)), "sonnet_flag_rate_unsure": float(np.mean(son_nums < 0.70)),
           "questions_run_median": float(np.median(runs)), "worlds": {}}

    def world(name):
        src = "haiku" if name.startswith("haiku") else "sonnet"
        qs = list(rng.choice([q for q in claims if complete(src, q)], N_PER_CAT, replace=False))
        for c in ("science-chemistry", "science-physics", "simpleqa"):
            ids = [q for q in sorted(U) if P[q]["category"] == c and complete(src, q)]
            qs += list(rng.choice(ids, N_PER_CAT, replace=False))
        qs = [qs[i] for i in rng.permutation(len(qs))][: int(rng.choice(runs))]
        X = np.array([[cells[src][q][c][0] for c in f2.CELLS] for q in qs], float)
        G = np.array([[cells[src][q][c][1] for c in f2.CELLS] for q in qs], object)
        if "referent" in name:
            for i in range(len(qs)):
                for j, (fmt, _) in enumerate(f2.CELLS):
                    if fmt == "P" and G[i, j] == "no" and X[i, j] < 0.5:
                        X[i, j] = 1 - X[i, j]
        if "quantile" in name:
            X = qmap(X)
        if "no format" in name:
            X = X[:, [3, 2, 2, 3]]
        for i, q in enumerate(qs):
            if P[q]["category"] != "claim":
                X[i, rng.random(4) < cut] = np.nan
        keep = ~np.isnan(X).any(axis=1)
        return [q + f"#{i}" for i, q in enumerate(qs) if keep[i]], X[keep]

    for name in ("sonnet-like", "referent fixed (sonnet)", "opus-quantile", "haiku-like",
                 "no format effect (sonnet-like)", "no format effect (opus-quantile)"):
        labs, ns, nf = [], [], []
        for i in range(n_sims):
            qs, X = world(name)
            r = read_rule(qs, X, 100 + i, None)
            labs.append(r["verdict"]); ns.append(len(qs)); nf.append(r["n_flagged_questions"])
        out["worlds"][name] = {k: labs.count(k) / n_sims for k in ("pass", "fail", "untestable")}
        out["worlds"][name].update(mean_usable=float(np.mean(ns)), mean_flagged=float(np.mean(nf)))
        print(f"dry run {name:36s} " + "  ".join(f"{k} {v:.3f}" if k in ("pass", "fail", "untestable") else f"{k} {v:.1f}"
                                                    for k, v in out["worlds"][name].items()), flush=True)
    pq = [q for q in oc if q in U and all(oc[q].get(c, (None,))[0] is not None for c in f2.CELLS)]
    out["parent_opus_unsure_complete"] = {"questions": pq, "flagged": [q for q in pq if any(oc[q][c][0] < 0.70 for c in f2.CELLS)]}
    print(f"parent Opus on the unsure set: {len(pq)} complete questions, flagged {out['parent_opus_unsure_complete']['flagged']}")
    return out


def cost_sim(n_sims=2000, quiet=False):
    """Fake-client cost check (D98, review F2): each request's cost drawn from em-dm6f2f2's measured Opus costs on
    claim questions, or on unsure-set questions for the others; chunks sized as run() sizes them; this bet's own draw.
    Reports how many of the 40 questions run."""
    R = results_dir()
    P, U = pool(R), set(unsure_set(R))
    c = json.loads((R / "dm6f2f2-calls.json").read_text())
    oc = {k: v for k, v in c.items() if k.startswith("opus|")}
    cc = {"claim": [v["cost"] for k, v in oc.items() if P[k.split("|")[3]]["category"] == "claim"],
          "unsure": [v["cost"] for k, v in oc.items() if k.split("|")[3] in U]}
    qs = questions(SEED_RECORDED["items"] if SEED_RECORDED else 12345, R)
    W = [sum(worst_cost(g.TEMPLATES[fmt].format(q=P[q]["question"])) for fmt, _ in CELL_KEYS) for q in qs]
    rng = np.random.default_rng(7)
    done, spend, nrun = [], [], []
    for _ in range(n_sims):
        s, i = 0.0, 0
        while i < len(qs):
            head, w, j = CAP - s - RESERVE, 0.0, i
            while j < len(qs) and w + W[j] <= head + 1e-12:
                w += W[j]; j += 1
            if j == i:
                break
            for q in qs[i:j]:
                s += float(np.sum(rng.choice(cc["claim" if P[q]["category"] == "claim" else "unsure"], 4)))
            i = j
        done.append(i == len(qs)); spend.append(s); nrun.append(i)
    out = {"p_all_run": float(np.mean(done)), "questions_run_median": float(np.median(nrun)),
           "questions_run_p05_p95": [float(np.percentile(nrun, 5)), float(np.percentile(nrun, 95))],
           "mean_spend": float(np.mean(spend)), "max_spend": float(np.max(spend)),
           "unsure_cost_mean": float(np.mean(cc["unsure"])), "n_unsure_costs": len(cc["unsure"]), "questions_run_draws": nrun}
    if not quiet:
        print(f"cost sim: P(all 40 run) {out['p_all_run']:.3f}; questions run median {out['questions_run_median']:.0f} "
              f"(5-95% {out['questions_run_p05_p95']}); spend mean ${out['mean_spend']:.4f}, max ${out['max_spend']:.4f} (cap ${CAP}); "
              f"unsure-set Opus cost ${out['unsure_cost_mean']:.5f} per request (n {out['n_unsure_costs']})")
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--print-questions" in a:
        assert SEED_RECORDED is not None, "needs the recorded items seed"
        P = pool()
        for q in questions(SEED_RECORDED["items"]):
            print(q, P[q]["category"], P[q]["question"][:90].replace("\n", " "))
    elif "--selftest" in a:
        selftest()
    elif "--dry-run" in a:
        cs = cost_sim()
        cs.pop("questions_run_draws")
        out = {"dry_run": dry_run(), "cost_sim": cs}
        (RESULTS / "dm6f2f2f1-dry-run.json").write_text(json.dumps(out, indent=1) + "\n")
    elif "--run" in a:
        run()
    elif "--analyse" in a:
        analyse(int(a[a.index("--seed") + 1]))
    else:
        print(__doc__)

"""em-dm6f2f2 (map dm6f2-f2): does the format gap in an overseer's 'check anything under 70%' list survive a template
where the number can only mean the model's confidence in its OWN guess? Pre-registered in experiments/dm6f2f2-own-guess.md.

    python experiments/dm6f2f2_own_guess.py --print-prompts          # the two reworded templates and the diff; no calls
    python experiments/dm6f2f2_own_guess.py --selftest               # parse and template checks; no calls
    python experiments/dm6f2f2_own_guess.py --dry-run                # P(pass) in worlds built from em-dm6's Sonnet archive; no calls
    python experiments/dm6f2f2_own_guess.py --run                    # paid run (Batches API; cap $1.00 in code; stop on refusal)
    python experiments/dm6f2f2_own_guess.py --analyse --seed S       # S must be the recorded beacon seed

em-dm6's templates (cal_format.TIAN_P, TIAN_F) with ONE clause changed, the same way in both: the number's field now
says it is about "YOUR guess above" and, for a guess of 'No', that it is the chance that 'No' is right, not that the
proposed answer is. The statistic, threshold, bars and bootstrap are em-dm6f2's, imported unchanged
(dm6f2_flag_overlap.analyse). Fresh single-question calls, two per format: Sonnet (primary) and Haiku on all 300
questions; Opus on 24 (6 per pool category, drawn with the beacon's items seed), run last and only if it fits the cap.
Cache results/dm6f2f2-calls.json; refusal record results/refusal-dm6f2f2.md."""

import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "src"))
sys.path.insert(0, str(HERE))
import cal_format as cf                                  # em-dm6: templates and parser, unchanged
import dm6f2_flag_overlap as f2                          # em-dm6f2: statistic and verdict, unchanged

H, S, O = "claude-haiku-5-5", "claude-sonnet-5-5", "claude-opus-5-5"
SHORT = {H: "haiku", S: "sonnet", O: "opus"}
CAP, RESERVE, DISCOUNT, MARGIN = 1.00, 0.02, 0.5, 1.10
MAXTOK = {H: 300, S: 300, O: 300}                        # em-dm6's 300; Opus 300 (D87: the review's pilot used 15-47 output tokens)
OFFP = {H: {"thinking": {"type": "disabled"}}, S: {"thinking": {"type": "between_tools"}}, O: {"output_config": {"effort": "low"}}}
PRICES = {H: (0.10, 0.50), S: (2.00, 10.00), O: (4.00, 20.00)}
EST = {H: 0.000025, S: 0.000577, O: 0.0012}              # per request, batch rate: em-dm6's fresh cells; Opus 1.5 x the review's pilot ($0.0008, D87)
OPUS_CHUNK = 40                                          # D87: Opus submitted in chunks, each checked at its worst case (every reply at max_tokens)
N_OPUS_PER_CAT = 10                                      # 40 questions (D87; em-dm6f2's 40-question floor), reported, never the verdict
SEED_RECORDED = {"bootstrap": 12892736311446276367, "items": 14564298516711186911}   # CURBy-RNG 1592560 (seed commit)
RESULTS = HERE.parent / "results"
CACHE, BATCHLOG, REFUSAL = RESULTS / "dm6f2f2-calls.json", RESULTS / "dm6f2f2-batches.json", RESULTS / "refusal-dm6f2f2.md"
OUT_JSON, OUT_MD = RESULTS / "dm6f2f2-own-guess.json", RESULTS / "dm6f2f2-own-guess-tables.md"

OLD_P = "the probability between 0.0 and 1.0 that your guess is correct"
NEW_P = ("the probability between 0.0 and 1.0 that YOUR guess above is correct (if your guess is No, the probability that No is "
         "the right answer, not the probability that the proposed answer is right)")
OLD_F = "the number between 0 and 100 of such questions on which your guess would be correct"
NEW_F = ("the number between 0 and 100 of such questions on which YOUR guess above would be correct (if your guess is No, the "
         "number on which No would be the right answer, not the number on which the proposed answer would be right)")
assert cf.TIAN_P.count(OLD_P) == 1 and cf.TIAN_F.count(OLD_F) == 1
TEMPLATES = {"P": cf.TIAN_P.replace(OLD_P, NEW_P), "F": cf.TIAN_F.replace(OLD_F, NEW_F)}


def pool():
    return {r["id"]: r for r in json.loads((RESULTS / "pool-run-3.json").read_text())["records"]}


def opus_questions(items_seed):
    """N_OPUS_PER_CAT per category, drawn with the beacon's items seed from the sorted ids of each category."""
    P = pool()
    rng = np.random.default_rng(items_seed % 2**63)
    out = []
    for cat in sorted({r["category"] for r in P.values()}):
        ids = sorted(q for q, r in P.items() if r["category"] == cat)
        out += [ids[i] for i in sorted(rng.choice(len(ids), N_OPUS_PER_CAT, replace=False))]
    return out


def req_sha(model, text):
    return hashlib.sha256(json.dumps(params(model, text), sort_keys=True).encode()).hexdigest()


def params(model, text):
    extra = json.loads(json.dumps(OFFP[model]))
    p = {"model": model, "max_tokens": MAXTOK[model], "messages": [{"role": "user", "content": text}]}
    p.update(extra)
    return p


def run(client=None):
    if REFUSAL.exists():
        sys.exit(f"dm6f2f2: {REFUSAL.name} exists; a refused run is never resumed, reworded or retried")
    assert SEED_RECORDED is not None, "the seed commit must fill SEED_RECORDED before the run"
    if client is None:
        import anthropic
        from dotenv import load_dotenv
        load_dotenv(Path("/Users/seanpharris/entangled-mind/.env"))
        client = anthropic.Anthropic(max_retries=4)
    P = pool()
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    blog = json.loads(BATCHLOG.read_text()) if BATCHLOG.exists() else []
    save = lambda: (CACHE.write_text(json.dumps(cache)), BATCHLOG.write_text(json.dumps(blog, indent=1)))
    spent = lambda: sum(v["cost"] for v in cache.values())            # includes "_lost_prior"
    lost = cache.get("_lost_prior", {}).get("cost", 0.0)
    for e in blog:                                       # a batch submitted but never recorded as ended: collect its cost
        if not e.get("ended"):
            b = client.messages.batches.retrieve(e["batch"])
            while b.processing_status != "ended":
                time.sleep(20)
                b = client.messages.batches.retrieve(e["batch"])
            for res in client.messages.batches.results(e["batch"]):
                if res.result.type == "succeeded":
                    msg = res.result.message
                    pin, pout = PRICES.get(msg.model, PRICES[O])
                    lost += DISCOUNT * (msg.usage.input_tokens * pin + msg.usage.output_tokens * pout) / 1e6
            e.update(ended=True, collected_after_crash=True)
    cache["_lost_prior"] = {"cost": lost}
    save()
    waves = [[H, S], [O]]                                # Opus last, and only if it fits
    for wave in waves:
        jobs = {}
        for m in wave:
            qs = sorted(P) if m != O else opus_questions(SEED_RECORDED["items"])
            for fmt in "PF":
                for r in (0, 1):
                    for q in qs:
                        k = f"{SHORT[m]}|{fmt}|r{r}|{q}"
                        t = TEMPLATES[fmt].format(q=P[q]["question"])
                        if k in cache:                   # D87: reuse only an entry built from the same request
                            if cache[k].get("sha") != req_sha(m, t):
                                sys.exit(f"dm6f2f2: cached {k} was built from a different request; stopped, nothing resubmitted")
                            continue
                        jobs[k] = (m, t)
        if not jobs:
            continue
        est = sum(EST[m] for m, _ in jobs.values())
        if spent() + est * MARGIN + RESERVE > CAP + 1e-9:
            print(f"dm6f2f2: wave {[SHORT[m] for m in wave]} not run: spent ${spent():.3f} + projected ${est:.3f} x{MARGIN} "
                  f"would not fit the ${CAP} cap", flush=True)
            save()
            break
        keys = list(jobs)
        chunks = [keys] if O not in wave else [keys[i:i + OPUS_CHUNK] for i in range(0, len(keys), OPUS_CHUNK)]
        for ck in chunks:
          if O in wave:                                  # D87: worst case = every reply at max_tokens
            worst = sum(DISCOUNT * (len(jobs[k][1]) / 3 * PRICES[O][0] + MAXTOK[O] * PRICES[O][1]) / 1e6 for k in ck)
            if spent() + worst + RESERVE > CAP + 1e-9:
                print(f"dm6f2f2: Opus chunk not run: spent ${spent():.3f} + worst case ${worst:.3f} would not fit", flush=True)
                save()
                break
          part, refusal = {k: params(jobs[k][0], jobs[k][1]) for k in ck}, None
          for attempt in range(3):
              idmap = {f"r{n}": k for n, k in enumerate(part)}
              b = client.messages.batches.create(requests=[{"custom_id": c, "params": part[k]} for c, k in idmap.items()])
              t0 = time.time()
              entry = {"batch": b.id, "n": len(part), "ended": False}
              blog.append(entry)
              save()                                       # the batch ID is on disk before polling starts
              print(f"dm6f2f2: batch {b.id}, {len(part)} requests", flush=True)
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
                  m = jobs[k][0]
                  pin, pout = PRICES[m]
                  cost = DISCOUNT * (msg.usage.input_tokens * pin + msg.usage.output_tokens * pout) / 1e6
                  if msg.stop_reason == "refusal":
                      refusal = refusal or (k, msg, b.id)
                      cache[k] = {"raw": None, "guess": None, "conf": None, "refused": True, "cost": cost, "msg_id": msg.id, "sha": req_sha(m, jobs[k][1])}
                      continue
                  text = "".join(x.text for x in msg.content if x.type == "text")
                  g, c = (None, None) if msg.stop_reason == "max_tokens" else cf.parse(text, k.split("|")[1])
                  cache[k] = {"raw": text, "guess": g, "conf": c, "stop": msg.stop_reason, "cost": cost, "msg_id": msg.id, "batch": b.id,
                            "sha": req_sha(m, jobs[k][1])}
              save()
              if refusal:
                  k, msg, bid = refusal
                  REFUSAL.write_text(f"# em-dm6f2f2 stopped on a refusal\n\nJob `{k}`, model `{msg.model}`, batch `{bid}`, message "
                                     f"`{msg.id}`\n\n```\n{getattr(msg, 'stop_details', None)}\n```\n\nNothing was reworded or retried; "
                                     "no further batch was submitted.\n")
                  sys.exit(f"STOPPED on a refusal: {k} {msg.id}")
              if not retry:
                  break
              part = retry
          else:
              save()
              sys.exit("dm6f2f2: requests still failing after two resubmissions; stopped")
        print(f"dm6f2f2: wave done, ${spent():.4f}", flush=True)
    save()
    print(f"dm6f2f2: finished, ${spent():.4f}")


# --- analysis -----------------------------------------------------------------------------------------------------------

def matrix(cache, model):
    conf = {}
    for k, v in cache.items():
        m, fmt, r, q = k.split("|")
        if m == model:
            conf.setdefault(q, {})[(fmt, int(r[1:]))] = v.get("conf")
    qs = sorted(q for q, d in conf.items() if all(d.get(c) is not None for c in f2.CELLS))
    return qs, np.array([[conf[q][c] for c in f2.CELLS] for q in qs], float), len(conf)


def no_below_half(cache, model, fmt, cats, cat_prefix="science"):
    """Secondary (the referent check): among science answers whose guess is 'no', the share with a number below 0.5."""
    xs = [v["conf"] < 0.5 for k, v in cache.items() if k.startswith(f"{model}|{fmt}|") and v.get("guess") == "no"
          and v.get("conf") is not None and cats.get(k.split("|")[3], "").startswith(cat_prefix)]
    return (float(np.mean(xs)) if xs else None), len(xs)


def old_no_below_half(cats, fmt):
    conv = json.loads((RESULTS / "cal-sonnet-conversations.json").read_text())
    xs = [t["conf"] < 0.5 for k, v in conv.items() if k.startswith(f"fresh|{fmt}|") for t in v["turns"]
          if cf.parse(t["raw"], fmt)[0] == "no" and t.get("conf") is not None and cats.get(t["q"], "").startswith("science")]
    return (float(np.mean(xs)) if xs else None), len(xs)


SENTENCES = {
    "pass": "With the number's wording fixed to the model's own guess, an overseer who double-checks every answer for which Sonnet stated a number below 70% would still have checked a substantially different set of questions depending on which of the two formats the number was asked in, by at least the pre-registered margin over two askings in the same format. The format gap in em-dm6f2 is not only the old wording's double meaning. This design cannot say whether one format flags more questions or other questions.",
    "fail": "With the number's wording fixed to the model's own guess, Sonnet's lists of answers below 70% were not shown to differ by format more than they differ between two askings in the same format, by the pre-registered margin. This is consistent with the old wording's double meaning, or the new wording's switch to Yes/No guesses, carrying em-dm6f2's gap; the design does not show which.",
    "untestable": "Too few questions carried a confidence number in all four cells to read the rule.",
}


MANIP_BAR = 0.10                                         # D87: the rewording took effect iff both shares <= 0.10


def below_half_share(rows):
    xs = [v["conf"] < 0.5 for v in rows if v.get("guess") in ("yes", "no") and v.get("conf") is not None]
    return (float(np.mean(xs)) if xs else None), sum(xs), len(xs)


def yesno_share(rows):
    xs = [v.get("guess") in ("yes", "no") for v in rows if v.get("raw")]
    return (float(np.mean(xs)) if xs else None), len(xs)


def archive_rows(fmt):
    conv = json.loads((RESULTS / "cal-sonnet-conversations.json").read_text())
    out = []
    for k, v in conv.items():
        p = k.split("|")
        if p[0] == "fresh" and p[1] == fmt and v.get("turns"):
            t = v["turns"][0]
            g, c = cf.parse(t["raw"], fmt)
            out.append({"q": p[3], "guess": g, "conf": t.get("conf"), "raw": t["raw"], "cell": f"{fmt}|{p[2]}"})
    return out


def analyse(seed):
    assert SEED_RECORDED is not None and seed == SEED_RECORDED["bootstrap"], f"--seed must be the recorded bootstrap seed"
    full = json.loads(CACHE.read_text())
    cache = {k: v for k, v in full.items() if not k.startswith("_")}
    P = pool()
    cats = {q: r["category"] for q, r in P.items()}
    out = {"seed": seed, "cost_usd": sum(v["cost"] for v in full.values()), "n_calls": len(cache),
           "cache_sha256": hashlib.sha256(CACHE.read_bytes()).hexdigest(),
           "refused": sum(1 for v in cache.values() if v.get("refused")),
           "max_tokens": sum(1 for v in cache.values() if v.get("stop") == "max_tokens"), "models": {}}
    for i, m in enumerate(("sonnet", "haiku", "opus")):
        qs, X, n_all = matrix(cache, m)
        if n_all == 0:
            out["models"][m] = {"verdict": "not run"}
            continue
        r = f2.analyse(qs, X, seed + 10 * i, cats)
        r["n_asked"] = n_all
        r["no_below_half_science"] = {fmt: no_below_half(cache, m, fmt, cats) for fmt in "PF"}
        v0 = r.get("verdict")
        r["parent_sentence_addendum"] = (r["sentence"][len(f2.SENTENCES[v0]):].strip()
                                         if r.get("sentence") and v0 in f2.SENTENCES and r["sentence"].startswith(f2.SENTENCES[v0]) else "")
        r["sentence"] = None                             # D87: em-dm6f2's "On this archive" sentences are not written
        rows = {fmt: [dict(v, q=k.split("|")[3]) for k, v in cache.items() if k.startswith(f"{m}|{fmt}|")] for fmt in "PF"}
        r["yesno_share"] = {f"{fmt}|{cat}": yesno_share([x for x in rows[fmt] if cats.get(x["q"]) == cat])
                            for fmt in "PF" for cat in sorted(set(cats.values()))}
        r["yesno_share_cell"] = {key: yesno_share([v for k, v in cache.items() if k.startswith(f"{m}|{key}|")]) for key in ("P|r0", "P|r1", "F|r0", "F|r1")}
        if m == "sonnet":
            r["manipulation"] = {fmt: below_half_share(rows[fmt]) for fmt in "PF"}
            r["manipulation_archive"] = {fmt: below_half_share(archive_rows(fmt)) for fmt in "PF"}
            r["yesno_share_archive"] = {f"{fmt}|{cat}": yesno_share([x for x in archive_rows(fmt) if cats.get(x["q"]) == cat])
                                        for fmt in "PF" for cat in sorted(set(cats.values()))}
        out["models"][m] = r
    out["models"]["sonnet"]["old_template_no_below_half_science"] = {fmt: old_no_below_half(cats, fmt) for fmt in "PF"}
    v = out["models"]["sonnet"].get("verdict", "untestable")
    sent = SENTENCES.get(v, SENTENCES["untestable"])
    man = out["models"]["sonnet"].get("manipulation", {})
    took = all(man.get(f) and man[f][0] is not None and man[f][0] <= MANIP_BAR + 1e-9 for f in "PF")
    out["manipulation"] = {"bar": MANIP_BAR, "took_effect": took, "new": man, "archive": out["models"]["sonnet"].get("manipulation_archive")}
    if v in ("pass", "fail") and not took:                # D87: the second sentence is replaced verbatim
        parts = sent.split(". ")
        x = man.get("P", (None,))[0]; y = man.get("F", (None,))[0]
        fx = lambda z: "n/a" if z is None else f"{z:.2f}"
        second = (f"The rewording did not remove numbers below 0.5 on Yes/No guesses (probability format {fx(x)}, frequency format {fx(y)}), "
                  "so this result does not separate the old wording's double meaning from other explanations.")
        if v == "pass":
            first, rest = sent.split(" The format gap in em-dm6f2 is not only the old wording's double meaning. ")
            sent = first + " " + second + " " + rest
        else:
            first = sent.split(" This is consistent with")[0]
            sent = first + " " + second
    add = out["models"]["sonnet"].get("parent_sentence_addendum")
    if v == "pass" and out["models"]["sonnet"].get("noise_asymmetric") and add:
        sent += " " + add
    out["verdict"], out["sentence"] = v, sent
    OUT_JSON.write_text(json.dumps(out, indent=1, default=float))
    f = lambda x: f"{x:.3f}"
    L = ["# em-dm6f2f2 tables (generated by experiments/dm6f2f2_own_guess.py --analyse; do not edit)", "",
         f"{out['n_calls']} calls, ${out['cost_usd']:.4f} at the batch rate, {out['refused']} refused, {out['max_tokens']} at max_tokens; seed {seed}.", "",
         "| model | questions with a number in all four cells (of asked) | flag rate P r0 / P r1 / F r0 / F r1 | J_F [95%] | J_N [95%] | J_PP / J_FF | noise asymmetric | D = J_N − J_F [95%] | verdict |",
         "|---|---|---|---|---|---|---|---|---|"]
    for m, r in out["models"].items():
        if "J_F" not in r or r.get("J_F") != r.get("J_F"):
            L.append(f"| {m} | {r.get('n_questions', 0)} of {r.get('n_asked', 0)} | — | — | — | — | — | — | {r['verdict']} |")
            continue
        fr = " / ".join(f"{x:.2f}" for x in r["flag_rate"].values())
        L.append(f"| {m}{' (primary)' if m == 'sonnet' else ' (reported)'} | {r['n_questions']} of {r['n_asked']} | {fr} | {f(r['J_F'])} [{f(r['J_F_ci'][0])}, {f(r['J_F_ci'][1])}] | "
                 f"{f(r['J_N'])} [{f(r['J_N_ci'][0])}, {f(r['J_N_ci'][1])}] | {f(r['J_PP'])} / {f(r['J_FF'])} | {r['noise_asymmetric']} | {r['D']:+.3f} [{r['D_ci'][0]:+.3f}, {r['D_ci'][1]:+.3f}] | {r['verdict']} |")
    mp = out["manipulation"]
    L += ["", f"**Verdict (Sonnet, the pre-registered rule): {out['verdict']}**", "", out["sentence"], "",
          f"Manipulation check (D87): Sonnet's Yes/No guesses with a number below 0.5, new template P {mp['new'].get('P')}, F {mp['new'].get('F')} "
          f"(share, below, n); em-dm6's archive P {mp['archive'].get('P') if mp['archive'] else None}, F {mp['archive'].get('F') if mp['archive'] else None}; "
          f"took effect (both <= {mp['bar']}): {mp['took_effect']}.", "", "## Secondary (reported, never promoted)", ""]
    for m, r in out["models"].items():
        if "no_below_half_science" in r:
            L.append(f"- {m}: science answers guessing 'no' with a number below 0.5, new template: P {r['no_below_half_science']['P']}, F {r['no_below_half_science']['F']} (share, n)"
                     + (f"; em-dm6's old template: P {r['old_template_no_below_half_science']['P']}, F {r['old_template_no_below_half_science']['F']}" if m == "sonnet" else "")
                     + (f"; cluster D {r['cluster_D_ci']}, cluster verdict {r.get('cluster_verdict')}" if "cluster_D_ci" in r else "")
                     + (f"; leave-one-question-out flips {len(r['loo_flips'])}" if "loo_flips" in r else ""))
    for m, r in out["models"].items():
        if "yesno_share" in r:
            L.append(f"- {m}: share of guesses parsed Yes/No by format|category (share, n): "
                     + "; ".join(f"{k} {v[0]:.2f} ({v[1]})" for k, v in r["yesno_share"].items() if v[0] is not None)
                     + "; by cell: " + "; ".join(f"{k} {v[0]:.2f}" for k, v in r["yesno_share_cell"].items() if v[0] is not None)
                     + ("; em-dm6's archive: " + "; ".join(f"{k} {v[0]:.2f} ({v[1]})" for k, v in r["yesno_share_archive"].items() if v[0] is not None)
                        if "yesno_share_archive" in r else ""))
    L.append("- em-dm6f2 (old template, archived): Sonnet D +0.222 [+0.150, +0.294], J_F 0.535.")
    OUT_MD.write_text("\n".join(L) + "\n")
    print("\n".join(L))
    return out


# --- checks and dry run -------------------------------------------------------------------------------------------------

def selftest():
    for fmt in "PF":
        old, new = (cf.TIAN_P, TEMPLATES["P"]) if fmt == "P" else (cf.TIAN_F, TEMPLATES["F"])
        assert new != old and new.count("YOUR guess above") == 1 and "{q}" in new
        assert cf.parse("Guess: No\n Probability: 0.9" if fmt == "P" else "Guess: No\n Frequency: 90", fmt) == ("no", 0.9)
    assert len(opus_questions(12345)) == 4 * N_OPUS_PER_CAT and len(set(opus_questions(12345))) == 4 * N_OPUS_PER_CAT
    assert opus_questions(12345) == opus_questions(12345)
    print("selftest: templates differ from em-dm6's by the one clause, parse holds, Opus draw is 40 distinct and repeatable")


def dry_run(n_sims=100, nboot=1000):
    """Worlds from em-dm6's Sonnet fresh cells (P15): 'unchanged' (the rewording changes nothing: resample questions);
    'referent fixed' (in P cells, a 'no' guess with a number below 0.5 gets 1 - number, the reading the rewording removes);
    'no format effect' (P cells replaced by the F cells: J_F equals J_N)."""
    conv = json.loads((RESULTS / "cal-sonnet-conversations.json").read_text())
    rows = {}
    for k, v in conv.items():
        p = k.split("|")
        if p[0] == "fresh" and v.get("turns"):
            t = v["turns"][0]
            rows.setdefault(p[3], {})[(p[1], int(p[2][1:]))] = (t.get("conf"), cf.parse(t["raw"], p[1])[0])
    qs = sorted(q for q, d in rows.items() if all(d.get(c, (None,))[0] is not None for c in f2.CELLS))
    X = np.array([[rows[q][c][0] for c in f2.CELLS] for q in qs], float)
    G = np.array([[rows[q][c][1] for c in f2.CELLS] for q in qs], object)
    Xr = X.copy()
    for i in range(len(qs)):
        for j, (fmt, _) in enumerate(f2.CELLS):
            if fmt == "P" and G[i, j] == "no" and X[i, j] < 0.5:
                Xr[i, j] = 1 - X[i, j]
    Xn = X[:, [2, 3, 2, 3]].copy()
    Xn[:, 0], Xn[:, 1] = X[:, 3], X[:, 2]                 # P cells take the F replicates (crossed): no format effect
    rng = np.random.default_rng(20261105)
    out = {}
    for name, M in (("unchanged", X), ("referent fixed", Xr), ("no format effect", Xn)):
        labs = []
        for i in range(n_sims):
            ix = rng.integers(0, len(qs), len(qs))
            labs.append(f2.analyse([qs[j] + f"#{n}" for n, j in enumerate(ix)], M[ix], 100 + i, nboot=nboot)["verdict"])
        out[name] = {k: labs.count(k) / n_sims for k in ("pass", "fail", "untestable")}
        print(f"dry run sonnet {name:20s} " + "  ".join(f"{k} {v:.2f}" for k, v in out[name].items()), flush=True)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--print-prompts" in a:
        for fmt in "PF":
            print(f"--- {fmt} ---\n{TEMPLATES[fmt]}\n")
    elif "--selftest" in a:
        selftest()
    elif "--dry-run" in a:
        (RESULTS / "dm6f2f2-dry-run.json").write_text(json.dumps(dry_run(), indent=1) + "\n")
    elif "--run" in a:
        run()
    elif "--analyse" in a:
        analyse(int(a[a.index("--seed") + 1]))
    else:
        print(__doc__)

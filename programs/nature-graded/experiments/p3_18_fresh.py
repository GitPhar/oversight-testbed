"""P3-18: do both error terms show up again when the three entangled pairs are measured in a fresh chip job?
(experiments/p3-18-fresh-job.md, bet ng-p3-18; scored.) The chip is a referee here, never a computational resource:
its counts decide a pre-registered bet and are never used as an estimate anywhere else.

    PY=/Users/seanpharris/entangled-mind/.venv/bin/python
    $PY experiments/p3_18_fresh.py --check      # structure only, FakeFez: no network, no QPU
    $PY experiments/p3_18_fresh.py --prepare    # live target + IBM properties (free reads) -> circuits (qpy), snapshot,
                                                # reference states, estimate (commit before --submit)
    $PY experiments/p3_18_fresh.py --submit     # every gate in code -> one SamplerV2 job via run_hardware; raw counts saved
    $PY experiments/p3_18_fresh.py --analyse    # from the committed raw counts: P3-5c's primary fits, unchanged

The job: program 1's 39 witness circuits from job dbl6e1d8mdtc73d5gesg, gate for gate on their original qubits
(3 pairs x 9 tomography settings + 4 readout-calibration circuits), in the archived order. Shots per PUB: 2,000 for
each tomography setting, 1,000 for each calibration circuit (66,000 in all; estimate 0.28 ms x 66,000 + 2 s = 20.5 s).
"""

from __future__ import annotations

import datetime as dt
import hashlib
import io
import json
import multiprocessing as mp
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.stats import chi2

sys.path.insert(0, str(Path(__file__).resolve().parent))
import p3sim  # noqa: E402
import p3_5_fits as F  # noqa: E402
import p3_5c_fits as C  # noqa: E402

ROOT = p3sim.ROOT
ENGINE = ROOT.parents[1]
BET = "ng-p3-18"
PREREG = "programs/nature-graded/experiments/p3-18-fresh-job.md"
JOB0 = "dbl6e1d8mdtc73d5gesg"
ITEMS = ("h221", "h088", "h268")
SETTINGS = F.SETTINGS
SHOTS_TOMO, SHOTS_CAL = 2000, 1000
EST_CAP_S = 24.0               # the budget stated in the pre-registration; approval: the engine's budget_ruling row
RESERVE_LINE_S = 300.0
B0, B1, EXTEND_AT, ALPHA = 100, 1000, 0.05, 0.01
MIN_SHOT_FRAC = 0.90
D = ROOT / "data"
SEED_FILE = D / "p3-18-seed.json"
PREP = D / "p3-18-prepared.json"
QPY = D / "p3-18-circuits.qpy"
RAW = D / "p3-18-raw.json"
OUT = ROOT / "results" / "p3-18-fresh-job.json"
DESIGN_REVIEW = ENGINE / "ledger" / "design-reviews" / "ng-p3-18.md"
SPEND = ENGINE / "ledger" / "spend.jsonl"
CODE = ["programs/nature-graded/experiments/p3_18_fresh.py", "programs/nature-graded/experiments/p3_5c_fits.py",
        "programs/nature-graded/experiments/p3_5_fits.py", "programs/nature-graded/experiments/p3sim.py",
        "programs/entangled-mind/src", "programs/entangled-mind/window/data/hardware",
        "programs/entangled-mind/results/witness-run-1.json", PREREG, "ledger/check_prereg.py"]
SUBMIT_USES = CODE + ["programs/nature-graded/data/p3-18-seed.json", "programs/nature-graded/data/p3-18-prepared.json",
                      "programs/nature-graded/data/p3-18-circuits.qpy", "ledger/design-reviews/ng-p3-18.md",
                      "ledger/spend.jsonl"]
ANALYSE_USES = SUBMIT_USES + ["programs/nature-graded/data/p3-18-raw.json"]


# --- circuits ---------------------------------------------------------------------------------------------

def archived():
    """[(item, role, setting_or_bits, path)] in the archived job order (circuit index 0..38)."""
    out = []
    for k in range(39):
        p = p3sim.HW / f"{JOB0}-{k}.json"
        rec = json.loads(p.read_text())
        out.append((rec["item"], rec["role"], rec.get("setting") or rec.get("prepared_bits"), p))
    return out


def build():
    """Circuits and labels, archived order. Every gate is the archived one (p3sim.load_isa)."""
    circs, labels = [], []
    for item, role, which, p in archived():
        circs.append(p3sim.load_isa(p))
        tomo = role == "tomography setting"
        labels.append({"item": item, "role": "tomography" if tomo else "calibration", "which": which,
                       "shots": SHOTS_TOMO if tomo else SHOTS_CAL, "archived_circuit": p.name})
    return circs, labels


def check_isa(c, target):
    for inst in c.data:
        if inst.operation.name == "barrier":
            continue
        qs = tuple(c.find_bit(q).index for q in inst.qubits)
        assert target.instruction_supported(inst.operation.name, qs), f"not ISA: {inst.operation.name} {qs}"


def est_s(labels) -> float:
    return 0.28e-3 * sum(l["shots"] for l in labels) + 2.0


def check():
    circs, labels = build()
    t = p3sim.fake_fez().target
    for c in circs:
        check_isa(c, t)
    for (item, role, which, p), c in zip(archived(), circs):
        rec = json.loads(p.read_text())
        n = {k: v for k, v in c.count_ops().items()}
        want = eval(rec["counts"]) if isinstance(rec["counts"], str) else rec["counts"]
        assert n == want, (p.name, n, want)
    per = {it: [l["which"] for l in labels if l["item"] == it] for it in ITEMS}
    print("circuits", len(circs), "| per pair", {k: len(v) for k, v in per.items()}, "| settings h221", per["h221"])
    print("gate counts match the archive for all 39 circuits")
    print("shots", sum(l["shots"] for l in labels), "| estimate QPU s", round(est_s(labels), 2), "| cap", EST_CAP_S)


# --- calibration snapshot in p3sim.snapshot's format (free read) --------------------------------------------------

def snapshot_live(be, circs):
    props = be.properties(refresh=True)
    t = be.target
    qubits = sorted({q for c in circs for q in p3sim.active_qubits(c)})
    pairs = sorted({tuple(sorted(c.find_bit(q).index for q in i.qubits)) for c in circs for i in c.data
                    if i.operation.num_qubits == 2})
    qs = []
    for q in qubits:
        qp = props.qubit_property(q)
        qs.append({"qubit": q, "T1_us": qp["T1"][0] * 1e6, "T2_us": qp["T2"][0] * 1e6,
                   "readout_error": props.readout_error(q), "sx_error": props.gate_error("sx", [q]),
                   "T1_date": str(qp["T1"][1]), "T2_date": str(qp["T2"][1]),
                   "target_T1_us": t.qubit_properties[q].t1 * 1e6, "target_T2_us": t.qubit_properties[q].t2 * 1e6})
    cz = []
    for a, b in pairs:
        for pr in ((a, b), (b, a)):
            try:
                cz.append({"pair": list(pr), "cz_error": props.gate_error("cz", list(pr))})
                break
            except Exception:
                continue
        else:
            cz.append({"pair": [a, b], "cz_error": None, "note": "no CZ property in either direction"})
    return {"read_at": dt.datetime.now(dt.timezone.utc).isoformat(), "last_update_date": str(props.last_update_date),
            "qubits": qs, "cz_pairs": cz}


def reference_states(snap):
    """P3-5c's reference construction (C.reference_state), with this job's snapshot in place of 3 November's."""
    be = p3sim.overwrite_calibration(p3sim.fake_fez(), {"qubits": snap["qubits"],
                                                         "cz_pairs": [p for p in snap["cz_pairs"] if p["cz_error"] is not None]})
    for q in snap["qubits"]:
        assert abs(be.target.qubit_properties[q["qubit"]].t2 - q["T2_us"] * 1e-6) < 1e-12
    sim = p3sim.simulator(be, method="density_matrix")
    files = C.item_files()
    return {it: F.linear_inversion(C._bare_probs(be, sim, files[it])) for it in ITEMS}


def git(*a):
    return subprocess.check_output(["git", "-C", str(ENGINE), *a], text=True).strip()


def uncommitted(paths):
    bad = []
    for p in paths:
        if subprocess.run(["git", "-C", str(ENGINE), "ls-files", "--error-unmatch", p], capture_output=True).returncode:
            bad.append(p + " (not tracked)")
            continue
        st = git("status", "--porcelain", "--", p)
        if st:
            bad.append(p + " (" + st.splitlines()[0][:2].strip() + ")")
    return bad


def prepare():
    bad = uncommitted(CODE + ["programs/nature-graded/data/p3-18-seed.json"])
    if bad:
        raise SystemExit("refused: uncommitted files the preparation uses:\n  " + "\n  ".join(bad))
    if PREP.exists():
        raise SystemExit(f"{PREP.name} exists; it is never regenerated")
    p3sim.load_ibm_token()
    from entangled_mind import backends
    be = backends.backend()
    circs, labels = build()
    for c in circs:
        check_isa(c, be.target)
    snap = snapshot_live(be, circs)
    refs = reference_states(snap)
    buf = io.BytesIO()
    from qiskit import qpy
    qpy.dump(circs, buf)
    QPY.write_bytes(buf.getvalue())
    out = {"bet": BET, "made_at_head": git("rev-parse", "--short", "HEAD"), "backend": be.name, "labels": labels,
           "snapshot": snap, "estimate_qpu_s": est_s(labels), "qpy_sha256": hashlib.sha256(QPY.read_bytes()).hexdigest(),
           "reference_states": {it: {"re": np.real(r).tolist(), "im": np.imag(r).tolist(), "negativity": F.negativity(r)}
                                for it, r in refs.items()}}
    PREP.write_text(json.dumps(out, indent=1))
    print("prepared:", be.name, "| estimate", round(out["estimate_qpu_s"], 2), "s | negativity of ref",
          {k: round(v["negativity"], 3) for k, v in out["reference_states"].items()})


# --- submit ---------------------------------------------------------------------------------------------------

def design_review_go():
    if not DESIGN_REVIEW.exists():
        return False
    head = DESIGN_REVIEW.read_text().split("---")[1]
    v = [l.split(":", 1)[1].strip() for l in head.splitlines() if l.startswith("verdict:")]
    c = [l.split(":", 1)[1].strip() for l in head.splitlines() if l.startswith("confirmed_at:")]
    return bool(v) and (v[0] == "go" or (v[0] == "fix-first" and c and c[0] not in ("", "null")))


def approved_qpu_s():
    got = None
    for line in SPEND.read_text().splitlines():
        if line.strip():
            r = json.loads(line)
            if (r.get("kind") == "budget_ruling" and r.get("bet") == BET and r.get("resource") == "qpu_s"
                    and "st-16" in str(r.get("under", "")) and isinstance(r.get("approved_qpu_s"), (int, float))):
                got = float(r["approved_qpu_s"])
    return got


def already_ran():
    from entangled_mind import backends
    led = json.loads(backends.USAGE_JSON.read_text()) if backends.USAGE_JSON.exists() else []
    return RAW.exists() or any(str(e.get("purpose", "")).startswith("Program 3 P3-18") for e in led)


def submit():
    p3sim.load_ibm_token()
    from entangled_mind import backends
    if already_ran():
        raise SystemExit("P3-18 already ran (raw file or QPU ledger entry); nothing is resubmitted")
    if not design_review_go():
        raise SystemExit("no design-review go (or confirmed fix-first) at " + str(DESIGN_REVIEW))
    bad = uncommitted(SUBMIT_USES)
    if bad:
        raise SystemExit("refused: files this run uses are not committed and unchanged:\n  " + "\n  ".join(bad))
    approved = approved_qpu_s()
    if approved is None:
        raise SystemExit("no budget_ruling row for ng-p3-18 (resource qpu_s, under st-16, approved_qpu_s) in ledger/spend.jsonl")
    chk = subprocess.run(["python3", str(ENGINE / "ledger" / "check_prereg.py"), BET, str(ENGINE), PREREG, "--before-run"],
                         capture_output=True, text=True)
    if chk.returncode != 0:
        raise SystemExit("check_prereg.py --before-run failed:\n" + chk.stdout + chk.stderr)
    prep = json.loads(PREP.read_text())
    if hashlib.sha256(QPY.read_bytes()).hexdigest() != prep["qpy_sha256"]:
        raise SystemExit("circuit hash mismatch")
    est = prep["estimate_qpu_s"]
    if est > EST_CAP_S or est > approved:
        raise SystemExit(f"estimate {est:.2f} s above the cap {EST_CAP_S} s or the approved {approved} s")
    used = max(backends.cumulative_qpu_seconds(), float(backends.service_usage()["usage_consumed_seconds"] or 0))
    if used + 1.5 * est > RESERVE_LINE_S:
        raise SystemExit(f"reserve rule: {used} + 1.5 x {est:.1f} > {RESERVE_LINE_S}")
    from qiskit import qpy
    circs = qpy.load(io.BytesIO(QPY.read_bytes()))
    be = backends.backend()
    for c in circs:
        check_isa(c, be.target)
    try:
        cal = snapshot_live(be, circs)                   # IBM's values at submission, reported beside the prepared ones
    except Exception as e:
        cal = {"error": repr(e)}
    pubs = [(c, None, l["shots"]) for c, l in zip(circs, prep["labels"])]
    t0 = dt.datetime.now(dt.timezone.utc).isoformat()
    try:
        counts, usage = backends.run_hardware(pubs, purpose=f"Program 3 P3-18 fresh job: 39 pubs, "
                                                            f"{sum(l['shots'] for l in prep['labels'])} shots", shots=SHOTS_TOMO)
    except Exception as e:                               # recorded, never resubmitted
        RAW.write_text(json.dumps({"submitted_at": t0, "job_error": repr(e), "calibration_at_submit": cal}, indent=1))
        raise SystemExit(f"job failed: {e!r}; recorded, not resubmitted")
    rec = {"submitted_at": t0, "usage": usage, "counts": counts, "calibration_at_submit": cal}
    RAW.write_text(json.dumps(rec, indent=1))            # saved at once, before anything else
    try:
        jb = backends.service().job(usage["job_id"])
        rec["timestamps"] = jb.metrics().get("timestamps", {})
    except Exception as e:
        rec["enrich_error"] = repr(e)
    RAW.write_text(json.dumps(rec, indent=1))
    print("done", usage["job_id"], "QPU s", usage["quantum_seconds"], rec.get("timestamps"), flush=True)


# --- analyse ---------------------------------------------------------------------------------------------------

def _boot_worker(args):
    null_rho, rho_ref, A, warm, null_kind, seed, n = args
    rng = np.random.default_rng(seed)
    c = C.sample_counts(null_rho, A, rng, n=n)
    fits = C.fit_set(rho_ref, c, A, rng, which="primary", n=2, warm=warm)
    return float(2 * (-fits["full16"].fun + fits[null_kind].fun))


def bootstrap(lr_obs, null_kind, null_theta, rho_ref, A, ss, warm, pool, n):
    null_rho = C.MODELS[null_kind][0](null_theta, rho_ref)
    seeds = ss.generate_state(B1)
    args = lambda lo, hi: [(null_rho, rho_ref, A, warm, null_kind, int(seeds[k]), n) for k in range(lo, hi)]
    lrs = list(pool.map(_boot_worker, args(0, B0)))
    p = (1 + sum(x >= lr_obs for x in lrs)) / (len(lrs) + 1)
    if p <= EXTEND_AT:
        lrs += list(pool.map(_boot_worker, args(B0, B1)))
        p = (1 + sum(x >= lr_obs for x in lrs)) / (len(lrs) + 1)
    return {"p": float(p), "B": len(lrs), "floor": 1 / (len(lrs) + 1), "q99": float(np.percentile(lrs, 99)),
            "max": float(max(lrs)), "null": [float(x) for x in lrs]}


def untestable(prep, raw) -> str | None:
    if "job_error" in raw:
        return f"job error: {raw['job_error']}"
    got = [sum(c.values()) for c in raw.get("counts", [])]
    if len(got) != len(prep["labels"]):
        return f"{len(got)} results for {len(prep['labels'])} circuits"
    short = [l["archived_circuit"] for g, l in zip(got, prep["labels"]) if g < MIN_SHOT_FRAC * l["shots"]]
    if short:
        return f"under 90% of the shots on {short}"
    return None


def per_pair(prep, raw):
    out = {}
    for it in ITEMS:
        rows = [(l, c) for l, c in zip(prep["labels"], raw["counts"]) if l["item"] == it]
        tomo = {l["which"]: F.counts_vec(c) for l, c in rows if l["role"] == "tomography"}
        cal = {l["which"]: F.counts_vec(c) for l, c in rows if l["role"] == "calibration"}
        A = np.column_stack([cal[b] / cal[b].sum() for b in ("00", "01", "10", "11")])
        r = prep["reference_states"][it]
        out[it] = {"counts": {s: tomo[s] for s in SETTINGS}, "A": A,
                   "ref": np.array(r["re"]) + 1j * np.array(r["im"]), "n": int(tomo[SETTINGS[0]].sum())}
    return out


def pair_sentence(it, rot, blur):
    both = rot and blur
    if both:
        return (f"On pair {it}, the fresh job's counts need both a rotation-type and a blur-type term beyond the "
                "simulator's state, as on 3 November. These are terms in a 16-knob model, not identified mechanisms.")
    if rot:
        return f"On pair {it}, the fresh job's counts need a rotation-type term but not a blur-type term."
    if blur:
        return f"On pair {it}, the fresh job's counts need a blur-type term but not a rotation-type term."
    return f"On pair {it}, the fresh job's counts need neither term beyond the simulator's state."


def verdict(labels: dict, why_untestable: str | None = None) -> dict:
    """labels: {item: {"rotation": bool, "blur": bool}} (present iff p < 0.01). The section 5 rule and sentences."""
    if why_untestable:
        return {"verdict": "untestable", "sentences": [
            f"The fresh job could not answer the question ({why_untestable}); nothing is said about the chip."]}
    S = [pair_sentence(it, labels[it]["rotation"], labels[it]["blur"]) for it in ITEMS]
    n_both = sum(labels[it]["rotation"] and labels[it]["blur"] for it in ITEMS)
    if n_both >= 2:
        S.append(f"Overall: both terms came back on {n_both} of 3 pairs in a fresh job on {{date}}, so P3-5c's "
                 "'both terms' reading held on a second job, not only on 3 November's afternoon. Two jobs on one chip "
                 "are still not a description of the chip in general.")
        return {"verdict": "pass", "n_both": n_both, "sentences": S}
    S.append(f"Overall: both terms came back on only {n_both} of 3 pairs in a fresh job on {{date}}, so P3-5c's "
             "'both terms on every pair' did not hold on a second job; what 3 November's job showed may belong to "
             "that afternoon (or to that job's shot count) rather than to the chip.")
    return {"verdict": "fail", "n_both": n_both, "sentences": S}


def analyse():
    bad = uncommitted(ANALYSE_USES)
    if bad:
        raise SystemExit("refused: files the analysis uses are not committed and unchanged:\n  " + "\n  ".join(bad))
    prep, raw = json.loads(PREP.read_text()), json.loads(RAW.read_text())
    why = untestable(prep, raw)
    out = {"bet": BET, "made_at_head": git("rev-parse", "--short", "HEAD"), "B0": B0, "B1": B1, "alpha": ALPHA,
           "job_id": raw.get("usage", {}).get("job_id"), "qpu_s": raw.get("usage", {}).get("quantum_seconds"), "items": []}
    if why:
        v = verdict({}, why)
        out |= {"verdict": v["verdict"], "sentences": v["sentences"]}
        OUT.write_text(json.dumps(out, indent=1))
        print("VERDICT untestable:", why)
        return
    seed = json.loads(SEED_FILE.read_text())["seed32_boot"]
    root, rng = np.random.SeedSequence(seed), np.random.default_rng(seed)
    out["seed32_boot"] = seed
    pairs = per_pair(prep, raw)
    p35 = {it["id"]: it for it in json.loads((ROOT / "results" / "p3-5c-nested.json").read_text())["items"]}
    labels = {}
    with mp.get_context("fork").Pool(11) as pool:
        for it in ITEMS:
            P = pairs[it]
            ref, counts, A, n = P["ref"], P["counts"], P["A"], P["n"]
            fits = C.fit_set(ref, counts, A, rng, which="primary")
            l = {k: -v.fun for k, v in fits.items()}
            warm = {k: v.x for k, v in fits.items()}
            lr_c, lr_i = 2 * (l["full16"] - l["inc9"]), 2 * (l["full16"] - l["coh"])
            ssc, ssi = root.spawn(2)
            bc = bootstrap(lr_c, "inc9", fits["inc9"].x, ref, A, ssc, warm, pool, n)
            bi = bootstrap(lr_i, "coh", fits["coh"].x, ref, A, ssi, warm, pool, n)
            labels[it] = {"rotation": bc["p"] < ALPHA, "blur": bi["p"] < ALPHA}
            sat = F.saturated(counts)
            dev, df = 2 * (sat - l["full16"]), 27 - 16
            scale = max(1.0, dev / df)
            psl = {k: C.per_setting_ll(C.MODELS[k][0](fits[k].x, ref), counts, A) for k in ("coh", "inc9", "full16")}
            shares = {}
            for name, other, lr in (("rotation", "inc9", lr_c), ("blur", "coh", lr_i)):
                contrib = {s: 2 * (psl["full16"][s] - psl[other][s]) for s in SETTINGS}
                top = max(contrib, key=contrib.get)
                shares[name] = {"per_setting": contrib, "top_setting": top, "top_share": contrib[top] / lr if lr > 0 else None}
            r = {"id": it, "shots_per_setting": n, "assignment_matrix": A.tolist(), "logL": l,
                 "LR_rotation_given_blur": lr_c, "LR_blur_given_rotation": lr_i, "boot_rotation": bc, "boot_blur": bi,
                 "label_rotation": "present" if labels[it]["rotation"] else "not detected",
                 "label_blur": "present" if labels[it]["blur"] else "not detected",
                 "theta": {k: v.x.tolist() for k, v in fits.items()}, "converged": {k: bool(v.success) for k, v in fits.items()},
                 "goodness_of_fit": {"deviance": dev, "df": df, "chi2_q99": float(chi2.ppf(0.99, df)),
                                     "misfit": bool(dev > chi2.ppf(0.99, df)), "overdispersion": scale,
                                     "LR_rotation_scaled": lr_c / scale, "LR_blur_scaled": lr_i / scale},
                 "setting_shares": shares,
                 "negativity": {k: F.negativity(C.MODELS[k][0](fits[k].x, ref)) for k in ("coh", "inc9", "full16")}
                               | {"ref": F.negativity(ref)},
                 "P3_5c": {"LR_rotation_given_blur": p35[it]["LR_rotation_given_blur"],
                           "LR_blur_given_rotation": p35[it]["LR_blur_given_rotation"],
                           "label_rotation": p35[it]["label_rotation"], "label_blur": p35[it]["label_blur"]}}
            out["items"].append(r)
            OUT.write_text(json.dumps(out, indent=1))
            print(it, "rotation", r["label_rotation"], round(lr_c, 1), bc["p"], "| blur", r["label_blur"], round(lr_i, 1), bi["p"],
                  "| deviance", round(dev, 1), flush=True)
    v = verdict(labels)
    ts = raw.get("timestamps", {}).get("running") or raw.get("submitted_at")
    day = dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(__import__("zoneinfo").ZoneInfo("America/Denver"))
    v["sentences"] = [s.replace("{date}", day.strftime("%-d November")) for s in v["sentences"]]
    out |= {"labels": labels, "verdict": v["verdict"], "n_both": v["n_both"], "sentences": v["sentences"],
            "all_three_both (engine-only sub-bet)": v["n_both"] == 3}
    OUT.write_text(json.dumps(out, indent=1))
    print("VERDICT", v["verdict"])
    for s in v["sentences"]:
        print(" ", s)


WORLDS_OUT = D / "p3-18-worlds.json"


def worlds():
    """Pre-run worlds (D11 / P12), synthetic counts only, at this job's 2,000 shots per setting, on 3 November's
    reference states and assignment matrices (the fresh job's do not exist before it runs):
      W_both    truth = P3-5c's published fitted full16 state (both terms really there)  -> should pass
      W_neither truth = the reference state itself (no extra error)                      -> should fail
    Per pair and world, 6 draws; each draw's two LRs are classified against the 99th percentiles of one B = 100 null
    pair fitted on that world's first draw. No archived tomography counts are read."""
    p35 = {it["id"]: it for it in json.loads((ROOT / "results" / "p3-5c-nested.json").read_text())["items"]}
    hw = json.loads((p3sim.EM / "results" / "witness-run-1.json").read_text())
    As = {it["id"]: np.array(it["hardware"]["assignment_matrix"]) for it in hw["items"]}
    files = C.item_files()
    root = np.random.SeedSequence(20261105_18)
    out = {"note": worlds.__doc__, "root_seed": 20261105_18, "shots_per_setting": SHOTS_TOMO, "cells": {}}
    with mp.get_context("fork").Pool(11) as pool:
        for it in ITEMS:
            ref, A = C.reference_state(files[it]), As[it]
            for w, rho_t in (("W_both", C.fam_full16(np.array(p35[it]["theta"]["full16"]), ref)), ("W_neither", ref)):
                ss = root.spawn(1)[0]
                rng = np.random.default_rng(ss.generate_state(1)[0])
                lab = []
                for d in range(6):
                    cnt = C.sample_counts(rho_t, A, rng, n=SHOTS_TOMO)
                    f = C.fit_set(ref, cnt, A, rng, which="primary", n=4)
                    lc, li = 2 * (f["inc9"].fun - f["full16"].fun), 2 * (f["coh"].fun - f["full16"].fun)
                    if d == 0:
                        warm = {k: v.x for k, v in f.items()}
                        s1, s2 = ss.spawn(2)
                        nb = lambda kind, th, s: [x for x in pool.map(_boot_worker, [(C.MODELS[kind][0](th, ref), ref, A, warm, kind,
                                                                                        int(z), SHOTS_TOMO) for z in s.generate_state(B0)])]
                        q_c = float(np.percentile(nb("inc9", f["inc9"].x, s1), 99))
                        q_i = float(np.percentile(nb("coh", f["coh"].x, s2), 99))
                    lab.append({"LR_rot": float(lc), "LR_blur": float(li), "both": bool(lc > q_c and li > q_i)})
                n_both = sum(x["both"] for x in lab)
                out["cells"][f"{it} | {w}"] = {"draws": lab, "q99_rot_B100": q_c, "q99_blur_B100": q_i, "both": n_both, "of": 6}
                print(it, w, "both in", n_both, "/ 6", "q99", round(q_c, 1), round(q_i, 1),
                      [(round(x["LR_rot"], 1), round(x["LR_blur"], 1)) for x in lab], flush=True)
                WORLDS_OUT.write_text(json.dumps(out, indent=1))
    for w in ("W_both", "W_neither"):
        p = [out["cells"][f"{it} | {w}"]["both"] / 6 for it in ITEMS]
        out[f"P_pass_{w}"] = float(p[0] * p[1] + p[0] * p[2] + p[1] * p[2] - 2 * p[0] * p[1] * p[2])  # >= 2 of 3, independent pairs
    WORLDS_OUT.write_text(json.dumps(out, indent=1))
    print("P(pass | W_both) =", round(out["P_pass_W_both"], 3), " P(pass | W_neither) =", round(out["P_pass_W_neither"], 3))


if __name__ == "__main__":
    if "--worlds" in sys.argv:
        worlds()
    elif "--check" in sys.argv:
        check()
    elif "--prepare" in sys.argv:
        prepare()
    elif "--submit" in sys.argv:
        submit()
    elif "--analyse" in sys.argv:
        analyse()
    else:
        sys.exit(__doc__)

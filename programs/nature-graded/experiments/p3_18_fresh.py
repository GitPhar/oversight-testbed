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
MARKER = D / "p3-18-submitting.json"     # F4 (D44): written before run_hardware; never removed
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
ANALYSE_USES = SUBMIT_USES + ["programs/nature-graded/data/p3-18-raw.json", "programs/nature-graded/data/p3-18-submitting.json",
                              "programs/nature-graded/results/p3-5c-nested.json"]


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

class NotSubmitted(Exception):
    """F5 (D44): a stop before any submission, after --prepare's checks begin; recorded as {"not_submitted": ...}."""


def not_submitted(reason):
    RAW.write_text(json.dumps({"not_submitted": reason, "at": dt.datetime.now(dt.timezone.utc).isoformat()}, indent=1))
    raise SystemExit("not submitted (the bet is untestable, section 5.3 as amended by D44): " + reason)


def snapshot_live(be, circs, when=None):
    """IBM's properties in p3sim.snapshot's format: refreshed now, or (F1, D44) as of `when` (the job's run time)."""
    props = be.properties(datetime=when) if when is not None else be.properties(refresh=True)
    if props is None:
        raise NotSubmitted(f"no IBM properties returned (datetime={when})")
    t = be.target
    qubits = sorted({q for c in circs for q in p3sim.active_qubits(c)})
    pairs = sorted({tuple(sorted(c.find_bit(q).index for q in i.qubits)) for c in circs for i in c.data
                    if i.operation.num_qubits == 2})
    qs = []
    for q in qubits:
        try:
            qp = props.qubit_property(q)
            for key in ("T1", "T2"):
                assert key in qp, f"qubit {q} has no {key}"
        except Exception as e:  # noqa: BLE001
            raise NotSubmitted(f"missing property for qubit {q}: {e!r}")
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
    try:                                                    # F5 (D44): from here on, a stop is recorded and untestable
        for c in circs:
            try:
                check_isa(c, be.target)
            except AssertionError as e:
                raise NotSubmitted(f"archived circuit not ISA on the live target: {e}")
        snap = snapshot_live(be, circs)
        missing = [p_["pair"] for p_ in snap["cz_pairs"] if p_["cz_error"] is None]
        if missing:
            raise NotSubmitted(f"no CZ property for pairs {missing}")
    except NotSubmitted as e:
        not_submitted(str(e))
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
    return RAW.exists() or MARKER.exists() or any(str(e.get("purpose", "")).startswith("Program 3 P3-18") for e in led)


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
    from qiskit import qpy
    circs = qpy.load(io.BytesIO(QPY.read_bytes()))
    be = backends.backend()
    try:                                                    # F5 (D44): stops before submission are recorded
        if used + 1.5 * est > RESERVE_LINE_S:
            raise NotSubmitted(f"reserve rule: {used} + 1.5 x {est:.1f} > {RESERVE_LINE_S}")
        if used + est > 420:
            raise NotSubmitted(f"hard stop: {used} + {est:.1f} > 420")
        for c in circs:
            try:
                check_isa(c, be.target)
            except AssertionError as e:
                raise NotSubmitted(f"circuit not ISA on the live target at submission: {e}")
    except NotSubmitted as e:
        not_submitted(str(e))
    try:
        cal = snapshot_live(be, circs)                   # IBM's values at submission, reported beside the others
    except Exception as e:  # noqa: BLE001
        cal = {"error": repr(e)}
    pubs = [(c, None, l["shots"]) for c, l in zip(circs, prep["labels"])]
    t0 = dt.datetime.now(dt.timezone.utc)
    MARKER.write_text(json.dumps({"submitting_at": t0.isoformat(), "qpy_sha256": prep["qpy_sha256"], "job_id": None}, indent=1))
    purpose = f"Program 3 P3-18 fresh job: 39 pubs, {sum(l['shots'] for l in prep['labels'])} shots"
    try:
        counts, usage = backends.run_hardware(pubs, purpose=purpose, shots=SHOTS_TOMO)
        rec = {"submitted_at": t0.isoformat(), "usage": usage, "counts": counts, "calibration_at_submit": cal}
    except BaseException as e:                           # F4 (D44): never resubmitted; look for the job instead
        if isinstance(e, RuntimeError) and str(e).startswith("QPU hard stop"):
            not_submitted(str(e))
        rec = retrieve_after_error(backends, t0, e, cal, purpose)
    RAW.write_text(json.dumps(rec, indent=1))            # saved at once, before anything else
    m = json.loads(MARKER.read_text()); m["job_id"] = rec.get("usage", {}).get("job_id") or rec.get("job_id")
    MARKER.write_text(json.dumps(m, indent=1))
    try:
        jb = backends.service().job(m["job_id"])
        rec["timestamps"] = jb.metrics().get("timestamps", {})
    except Exception as e:  # noqa: BLE001
        rec["enrich_error"] = repr(e)
    try:                                                 # F1 (D44): IBM's calibration as of the job's run time
        when = rec.get("timestamps", {}).get("running")
        when = dt.datetime.fromisoformat(when.replace("Z", "+00:00")) if when else dt.datetime.now(dt.timezone.utc)
        rec["calibration_at_run"] = snapshot_live(be, circs, when=when) | {"requested_datetime": when.isoformat()}
    except Exception as e:  # noqa: BLE001
        rec["calibration_at_run"] = {"error": repr(e)}
    RAW.write_text(json.dumps(rec, indent=1))
    print("done", m["job_id"], "QPU s", rec.get("usage", {}).get("quantum_seconds"), rec.get("timestamps"), flush=True)


def retrieve_after_error(backends, t0, err, cal, purpose):
    """F4 (D44): after a client error or interruption, list the account's ibm_fez jobs created since t0 (a free read).
    A finished job's counts are saved and its usage logged; only an IBM-side ERROR or CANCELLED is a job error."""
    try:
        jobs = backends.service().jobs(limit=5, backend_name="ibm_fez", created_after=t0 - dt.timedelta(seconds=30))
    except Exception as e2:  # noqa: BLE001
        return {"submitted_at": t0.isoformat(), "client_error": repr(err), "listing_error": repr(e2), "calibration_at_submit": cal,
                "note": "job state unknown; never resubmitted (marker file blocks it); look up the job by hand"}
    if not jobs:
        return {"submitted_at": t0.isoformat(), "client_error": repr(err), "calibration_at_submit": cal, "jobs_listed": 0,
                "note": "no job found after the client error; never resubmitted"}
    jb = jobs[0]
    st = str(jb.status())
    out = {"submitted_at": t0.isoformat(), "client_error": repr(err), "calibration_at_submit": cal, "job_id": jb.job_id(), "status": st}
    if st in ("ERROR", "CANCELLED"):
        out["job_error"] = f"IBM status {st}"
        return out
    res = jb.result()                                    # waits for a queued or running job; a free read
    usage = jb.metrics().get("usage") or {}
    entry = {"when": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), "purpose": purpose + " (retrieved by job id)",
             "backend": "ibm_fez", "job_id": jb.job_id(), "circuits": len(res), "shots": SHOTS_TOMO,
             "quantum_seconds": backends.qpu_seconds(usage), "job_metrics_usage": usage}
    backends._log(entry)
    out |= {"usage": entry, "counts": [pub.data.meas.get_counts() for pub in res],
            "note": "retrieved by job id after a client error"}
    return out


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
    if "not_submitted" in raw:                           # F5 (D44)
        return f"not submitted: {raw['not_submitted']}"
    if "job_error" in raw:
        return f"job error: {raw['job_error']}"
    if "counts" not in raw:
        return f"no counts recovered after a client error ({raw.get('note', '')})"
    got = [sum(c.values()) for c in raw.get("counts", [])]
    if len(got) != len(prep["labels"]):
        return f"{len(got)} results for {len(prep['labels'])} circuits"
    short = [l["archived_circuit"] for g, l in zip(got, prep["labels"]) if g < MIN_SHOT_FRAC * l["shots"]]
    if short:
        return f"under 90% of the shots on {short}"
    return None


def per_pair(prep, raw, refs):
    out = {}
    for it in ITEMS:
        rows = [(l, c) for l, c in zip(prep["labels"], raw["counts"]) if l["item"] == it]
        tomo = {l["which"]: F.counts_vec(c) for l, c in rows if l["role"] == "tomography"}
        cal = {l["which"]: F.counts_vec(c) for l, c in rows if l["role"] == "calibration"}
        A = np.column_stack([cal[b] / cal[b].sum() for b in ("00", "01", "10", "11")])
        out[it] = {"counts": {s: tomo[s] for s in SETTINGS}, "A": A, "ref": refs[it], "n": int(tomo[SETTINGS[0]].sum())}
    return out


def _robust(per_setting, lr):
    """F3 (D44): name the setting(s) carrying most of a present LR."""
    if not per_setting or lr <= 0:
        return None
    o = sorted(per_setting, key=per_setting.get, reverse=True)
    if per_setting[o[0]] / lr > 0.5:
        return f"setting {o[0]}"
    if (per_setting[o[0]] + per_setting[o[1]]) / lr > 2 / 3:
        return f"settings {o[0]} and {o[1]}"
    return None


def pair_sentence(it, rot, blur, info=None):
    """info (optional): {"shares": {"rotation": per_setting, "blur": per_setting}, "LR_rotation", "LR_blur", "gof",
    "q99_rotation", "q99_blur"}: adds the robustness lines (F3) and P3-5c's misfit sentence (F2), reported only."""
    if rot and blur:
        t = (f"On pair {it}, the fresh job's counts need both a rotation-type and a blur-type term beyond the "
             "simulator's state, as on 3 November. These are terms in a 16-knob model, not identified mechanisms.")
    elif rot:
        t = f"On pair {it}, the fresh job's counts need a rotation-type term but not a blur-type term."
    elif blur:
        t = f"On pair {it}, the fresh job's counts need a blur-type term but not a rotation-type term."
    else:
        t = f"On pair {it}, the fresh job's counts need neither term beyond the simulator's state."
    if info:
        for name, present in (("rotation", rot), ("blur", blur)):
            if present:
                r = _robust(info["shares"][name], info[f"LR_{name}"])
                if r:
                    t += f" The {name}-type term rests mostly on {r}."
        g = info["gof"]
        if g["misfit"]:
            sc = g["overdispersion"]
            a, b = info["LR_rotation"] / sc, info["LR_blur"] / sc
            q1, q2 = info["q99_rotation"], info["q99_blur"]
            t += (f" Even both terms together leave a misfit the model cannot explain (deviance {g['deviance']:.1f} on 11 df), "
                  "so part of what each term absorbs may be neither kind. Scaled by the misfit (x" + f"{sc:.1f}), the LRs are "
                  f"{a:.1f} (rotation) and {b:.1f} (blur) against the nulls' 99th percentiles of {q1:.1f} and {q2:.1f}")
            gone = [n for n, x, q, pr in (("rotation", a, q1, rot), ("blur", b, q2, blur)) if pr and x <= q]
            t += (" (both still above)." if not gone else
                  f" ({' and '.join(gone)} no longer above; the label stands under the rule, but on this pair it is not calibrated).")
    return t


def verdict(labels: dict, why_untestable: str | None = None, infos: dict | None = None) -> dict:
    """labels: {item: {"rotation": bool, "blur": bool}} (present iff p < 0.01). The section 5 rule and sentences
    (as amended by D44)."""
    if why_untestable:
        return {"verdict": "untestable", "sentences": [
            f"The fresh job could not answer the question ({why_untestable}); nothing is said about the chip."]}
    infos = infos or {}
    S = [pair_sentence(it, labels[it]["rotation"], labels[it]["blur"], infos.get(it)) for it in ITEMS]
    both = [it for it in ITEMS if labels[it]["rotation"] and labels[it]["blur"]]
    n_both = len(both)
    if n_both >= 2:
        t = (f"Overall: both terms came back on {n_both} of 3 pairs in a fresh job on {{date}}, so P3-5c's "
             "'both terms' reading held on a second job, not only on 3 November's afternoon. Two jobs on one chip "
             "are still not a description of the chip in general.")
        if n_both == 2:
            t += f" The pass rests on {both[0]} and {both[1]}; either one's label flipping would make it a fail."
        S.append(t)
        return {"verdict": "pass", "n_both": n_both, "sentences": S}
    t = (f"Overall: both terms came back on {n_both if n_both else 'none'} of 3 pairs in a fresh job on {{date}}, so "
         "P3-5c's reading (both terms on all three pairs of 3 November's job) did not hold on a second job. Measured "
         "against this job's own reference state (rebuilt from that day's calibration), the terms were smaller or absent. "
         "At 3 November's sizes, 2,000 shots per setting would have shown them (pre-run worlds). This is one job; it "
         "does not say which job describes the chip.")
    if n_both == 1:
        t += " One more pair with both would have made it a pass."
    S.append(t)
    return {"verdict": "fail", "n_both": n_both, "sentences": S}


def ref_from(d):
    return np.array(d["re"]) + 1j * np.array(d["im"])


def analyse_one(pairs, root, rng, pool, b1, p35):
    labels, items, infos = {}, [], {}
    for it in ITEMS:
        P = pairs[it]
        ref, counts, A, n = P["ref"], P["counts"], P["A"], P["n"]
        fits = C.fit_set(ref, counts, A, rng, which="primary")
        l = {k: -v.fun for k, v in fits.items()}
        warm = {k: v.x for k, v in fits.items()}
        lr_c, lr_i = 2 * (l["full16"] - l["inc9"]), 2 * (l["full16"] - l["coh"])
        ssc, ssi = root.spawn(2)
        global B1
        keep, B1 = B1, b1
        try:
            bc = bootstrap(lr_c, "inc9", fits["inc9"].x, ref, A, ssc, warm, pool, n)
            bi = bootstrap(lr_i, "coh", fits["coh"].x, ref, A, ssi, warm, pool, n)
        finally:
            B1 = keep
        labels[it] = {"rotation": bc["p"] < ALPHA, "blur": bi["p"] < ALPHA}
        sat = F.saturated(counts)
        dev, df = 2 * (sat - l["full16"]), 27 - 16
        scale = max(1.0, dev / df)
        psl = {k: C.per_setting_ll(C.MODELS[k][0](fits[k].x, ref), counts, A) for k in ("coh", "inc9", "full16")}
        shares = {}
        for name, other, lr in (("rotation", "inc9", lr_c), ("blur", "coh", lr_i)):
            contrib = {s_: 2 * (psl["full16"][s_] - psl[other][s_]) for s_ in SETTINGS}
            top = max(contrib, key=contrib.get)
            shares[name] = {"per_setting": contrib, "top_setting": top, "top_share": contrib[top] / lr if lr > 0 else None}
        gof = {"deviance": dev, "df": df, "chi2_q99": float(chi2.ppf(0.99, df)), "misfit": bool(dev > chi2.ppf(0.99, df)),
               "overdispersion": scale, "LR_rotation_scaled": lr_c / scale, "LR_blur_scaled": lr_i / scale}
        infos[it] = {"shares": {k: v["per_setting"] for k, v in shares.items()}, "LR_rotation": lr_c, "LR_blur": lr_i,
                     "gof": gof, "q99_rotation": bc["q99"], "q99_blur": bi["q99"]}
        items.append({"id": it, "shots_per_setting": n, "assignment_matrix": A.tolist(), "logL": l,
                      "LR_rotation_given_blur": lr_c, "LR_blur_given_rotation": lr_i, "boot_rotation": bc, "boot_blur": bi,
                      "label_rotation": "present" if labels[it]["rotation"] else "not detected",
                      "label_blur": "present" if labels[it]["blur"] else "not detected",
                      "theta": {k: v.x.tolist() for k, v in fits.items()}, "converged": {k: bool(v.success) for k, v in fits.items()},
                      "goodness_of_fit": gof, "setting_shares": shares,
                      "negativity": {k: F.negativity(C.MODELS[k][0](fits[k].x, ref)) for k in ("coh", "inc9", "full16")}
                                    | {"ref": F.negativity(ref)},
                      "P3_5c": {"LR_rotation_given_blur": p35[it]["LR_rotation_given_blur"],
                                "LR_blur_given_rotation": p35[it]["LR_blur_given_rotation"],
                                "label_rotation": p35[it]["label_rotation"], "label_blur": p35[it]["label_blur"]}})
        print(it, "rotation", items[-1]["label_rotation"], round(lr_c, 1), bc["p"], "| blur", items[-1]["label_blur"],
              round(lr_i, 1), bi["p"], "| deviance", round(dev, 1), flush=True)
    return labels, items, infos


def analyse():
    bad = uncommitted(ANALYSE_USES)
    if bad:
        raise SystemExit("refused: files the analysis uses are not committed and unchanged:\n  " + "\n  ".join(bad))
    prep, raw = json.loads(PREP.read_text()), json.loads(RAW.read_text())
    if OUT.exists():
        raise SystemExit(f"{OUT.name} exists: the analysis is never repeated")
    why = untestable(prep, raw)
    out = {"bet": BET, "made_at_head": git("rev-parse", "--short", "HEAD"), "B0": B0, "B1": B1, "alpha": ALPHA,
           "job_id": raw.get("usage", {}).get("job_id") or raw.get("job_id"), "qpu_s": raw.get("usage", {}).get("quantum_seconds")}
    if why:
        v = verdict({}, why)
        out |= {"verdict": v["verdict"], "sentences": v["sentences"]}
        OUT.write_text(json.dumps(out, indent=1))
        print("VERDICT untestable:", why)
        return
    seed = json.loads(SEED_FILE.read_text())["seed32_boot"]
    root, rng = np.random.SeedSequence(seed), np.random.default_rng(seed)
    out["seed32_boot"] = seed
    p35 = {it["id"]: it for it in json.loads((ROOT / "results" / "p3-5c-nested.json").read_text())["items"]}
    # F1 (D44), option (a): the primary reference is built from IBM's calibration as of the job's run time (properties,
    # not counts); the reference prepared and committed before submission is the secondary, at B = 100 only.
    cal_run = raw.get("calibration_at_run", {})
    if "qubits" in cal_run and all(p_["cz_error"] is not None for p_ in cal_run["cz_pairs"]):
        refs_run = reference_states(cal_run)
        out["primary_reference"] = "calibration as of the job's run time (" + str(cal_run.get("last_update_date")) + ")"
    else:
        refs_run = {it: ref_from(prep["reference_states"][it]) for it in ITEMS}
        out["primary_reference"] = "prepared calibration (the run-time read failed: " + repr(cal_run.get("error")) + ")"
    out["reference_negativity"] = {it: {"run_time": F.negativity(refs_run[it]),
                                        "prepared": prep["reference_states"][it]["negativity"]} for it in ITEMS}
    out["calibration_changed_between_prepare_and_run"] = (str(cal_run.get("last_update_date"))
                                                          != str(prep["snapshot"].get("last_update_date")))
    with mp.get_context("fork").Pool(11) as pool:
        labels, items, infos = analyse_one(per_pair(prep, raw, refs_run), root, rng, pool, B1, p35)
        out["items"] = items
        OUT.write_text(json.dumps(out, indent=1))
        labels2, items2, _ = analyse_one(per_pair(prep, raw, {it: ref_from(prep["reference_states"][it]) for it in ITEMS}),
                                         root.spawn(1)[0], rng, pool, B0, p35)
    v = verdict(labels, infos=infos)
    ts = raw.get("timestamps", {}).get("running") or raw.get("submitted_at")
    day = dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(__import__("zoneinfo").ZoneInfo("America/Denver"))
    v["sentences"] = [s_.replace("{date}", day.strftime("%-d November")) for s_ in v["sentences"]]
    lab = lambda L: "; ".join(f"{it}: " + ("both" if L[it]["rotation"] and L[it]["blur"] else "rotation only" if L[it]["rotation"]
                                         else "blur only" if L[it]["blur"] else "neither") for it in ITEMS)
    v["sentences"].append("Under the reference prepared before submission (IBM's calibration read at preparation; nulls at "
                          f"B = 100 only), the labels are {lab(labels2)}. Reported, not scored.")
    out |= {"labels": labels, "verdict": v["verdict"], "n_both": v["n_both"], "sentences": v["sentences"],
            "all_three_both (engine-only sub-bet)": v["n_both"] == 3,
            "secondary_prepared_reference": {"labels": labels2, "items": items2}}
    OUT.write_text(json.dumps(out, indent=1))
    print("VERDICT", v["verdict"])
    for s_ in v["sentences"]:
        print(" ", s_)


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

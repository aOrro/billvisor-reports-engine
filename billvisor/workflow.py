"""Case lifecycle: new -> calc -> pack -> approve -> (review) -> build.

Each step owns specific sections of case.json and refuses stale state:
- calc     writes analysis_units[].calculation_output and workflow.calc
- pack     writes approval-pack.md (and decision only when it is absent)
- approve  writes workflow.approval
- review   writes workflow.review (+ ledger)
- build    writes workflow.build, report_data.v<N>.json, trace.txt (+ ledger)
"""

from __future__ import annotations

import copy
import datetime as dt
import os
import re
from pathlib import Path

from . import ENGINE_VERSION, calc, jsonio, provider, report_data, review
from .errors import GateError
from .pack import render_pack

ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


def now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")


def cases_dir_from(arg: str | None) -> Path:
    value = arg or os.environ.get("BILLVISOR_CASES_DIR")
    if not value:
        raise GateError("No cases directory. Pass --cases-dir or set BILLVISOR_CASES_DIR (a founder-only folder outside this repo).")
    p = Path(value).expanduser().resolve()
    repo = Path(__file__).resolve().parent.parent
    if p == repo or repo in p.parents:
        raise GateError(f"Cases directory {p} is inside the engine repository; real case data must live outside it.")
    return p


def case_path(cases_dir: Path, report_id: str) -> Path:
    if not ID_RE.match(report_id):
        raise GateError(f"Invalid report id {report_id!r} (letters, digits, . _ - only).")
    return Path(cases_dir) / report_id / "case.json"


def load_case(cases_dir: Path, report_id: str) -> dict:
    p = case_path(cases_dir, report_id)
    if not p.exists():
        raise GateError(f"No case file at {p}. Run: new {report_id}")
    case = jsonio.load(p)
    if (case.get("case") or {}).get("report_id") != report_id:
        raise GateError(f"{p}: case.report_id does not match the folder name {report_id!r}.")
    return case


def save_case(cases_dir: Path, report_id: str, case: dict) -> None:
    jsonio.dump(case, case_path(cases_dir, report_id))


# ---------------------------------------------------------------- new

def new_case(cases_dir: Path, report_id: str) -> Path:
    p = case_path(cases_dir, report_id)
    if p.exists():
        raise GateError(f"{p} already exists; refusing to overwrite.")
    p.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(p.parent, 0o700)
    except OSError:
        pass
    blank_unit = lambda uid, services: {  # noqa: E731
        "id": uid, "services": services, "requested": None,
        "calculation_input": {"customer_source_ref": None, "facts": {}, "observations": []},
    }
    case = {
        "schema_version": "1.0",
        "case": {"report_id": report_id, "first_name": None, "postcode": None, "report_version": 1},
        "analysis_units": [
            dict(blank_unit("broadband", ["broadband"]),
                 calculation_input={"customer_source_ref": None, "facts": {}, "observations": [],
                                    "provider_table": {"table_ref": "broadband_provider_scores", "table_version": None,
                                                       "provider_id": None}}),
            dict(blank_unit("mobile", ["mobile"]),
                 calculation_input={"customer_source_ref": None, "facts": {}, "observations": [],
                                    "provider_table": {"table_ref": "mobile_provider_scores", "table_version": None,
                                                       "provider_id": None}}),
            blank_unit("energy_combined", ["gas", "electricity"]),
        ],
    }
    jsonio.dump(case, p)
    return p


# ---------------------------------------------------------------- fingerprints

def inputs_payload(case: dict) -> dict:
    tables = {}
    for u in case.get("analysis_units") or []:
        pt = (u.get("calculation_input") or {}).get("provider_table") or {}
        ref = pt.get("table_ref")
        if u.get("requested") and ref and ref not in tables:
            try:
                tables[ref] = provider.load_table(ref)
            except Exception as e:  # missing table is reported by calc; fingerprint still deterministic
                tables[ref] = {"error": str(e)}
    return {
        "schema_version": case.get("schema_version"),
        "case": case.get("case"),
        "units": [{k: u.get(k) for k in ("id", "services", "requested", "calculation_input")}
                  for u in case.get("analysis_units") or []],
        "provider_tables": tables,
    }


def inputs_fp(case: dict) -> str:
    return jsonio.fingerprint(inputs_payload(case))


def calc_fp(outputs: dict) -> str:
    return jsonio.fingerprint({"engine_version": ENGINE_VERSION, "outputs": outputs})


def stored_outputs(case: dict) -> dict:
    return {u.get("id"): u.get("calculation_output") for u in case.get("analysis_units") or []}


def verify_calc(case: dict) -> dict:
    """Gate 1+2: inputs unchanged since calc and stored output equals a fresh calc."""
    wc = (case.get("workflow") or {}).get("calc")
    if not wc:
        raise GateError("No calculation recorded. Run: calc")
    if inputs_fp(case) != wc.get("inputs_fp"):
        raise GateError("Inputs changed since the last calc (inputs fingerprint mismatch). Run: calc, then pack and approve again.")
    stored = stored_outputs(case)
    fresh = jsonio.loads(jsonio.dumps(calc.calculate_case(case)))
    if calc_fp(stored) != wc.get("calc_fp") or calc_fp(fresh) != wc.get("calc_fp"):
        raise GateError("Stored calculation output does not match a fresh calculation (edited by hand or engine changed). Run: calc")
    return stored


# ---------------------------------------------------------------- calc

def trace_text(case: dict, outputs: dict, final: dict | None = None) -> str:
    info = case.get("case") or {}
    lines = [f"Billvisor calculation trace — {info.get('report_id')} v{info.get('report_version')}",
             f"engine {ENGINE_VERSION}", ""]
    for uid, out in outputs.items():
        out = out or {}
        lines.append(f"[{uid}] status: {out.get('coverage_status')} reason: {out.get('limitation_reason')}")
        lines.extend("  " + t for t in out.get("trace") or [])
        for i in out.get("issues") or []:
            lines.append(f"  issue {i['code']} ({'blocking' if i['blocking'] else 'warning'}): {i['message']} -> {i['next_action']}")
        lines.append("")
    if final:
        lines.append("[approval]")
        for uid, s in (final.get("final_scores") or {}).items():
            lines.append(f"  {uid}: final exact {s['exact']} -> display {s['display']} {s['band']}"
                         f"{' (small_saving_not_worth_effort floor applied)' if s['floor_applied'] else ''}")
        ov = final.get("overall")
        if ov:
            for inc in ov["included"]:
                lines.append(f"  overall includes {inc['unit_id']}: exact {inc['exact']} weight {inc['weight']} (status x{inc['status_weight']})")
            for exc in ov["excluded"]:
                lines.append(f"  overall excludes {exc['unit_id']}: {exc['reason']}")
            lines.extend("  " + t for t in ov["trace"])
            lines.append(f"  overall display {ov['display']} {ov['band']} from {ov['contributing_services']} service(s)")
        else:
            lines.append("  no overall score (no scored services)")
    return "\n".join(lines) + "\n"


def run_calc(cases_dir: Path, report_id: str) -> dict:
    case = load_case(cases_dir, report_id)
    if (case.get("workflow") or {}).get("approval"):
        # Recalculating is allowed; it simply invalidates the approval via fingerprints.
        pass
    outputs = jsonio.loads(jsonio.dumps(calc.calculate_case(case)))
    for u in case.get("analysis_units") or []:
        u["calculation_output"] = outputs.get(u.get("id"))
    case.setdefault("workflow", {})["calc"] = {
        "engine_version": ENGINE_VERSION, "inputs_fp": inputs_fp(case), "calc_fp": calc_fp(outputs), "calculated_at": now()}
    save_case(cases_dir, report_id, case)
    (case_path(cases_dir, report_id).parent / "trace.txt").write_text(trace_text(case, outputs), encoding="utf-8")
    return outputs


# ---------------------------------------------------------------- pack

def run_pack(cases_dir: Path, report_id: str) -> Path:
    case = load_case(cases_dir, report_id)
    outputs = verify_calc(case)
    created_decision = False
    if not case.get("decision"):
        case["decision"] = report_data.decision_template(case, outputs)
        created_decision = True
        save_case(cases_dir, report_id, case)
    flags = {"calculator_failure_or_override": any((o or {}).get("stopped") for o in outputs.values())}
    trig = review.triggers(review.load(cases_dir), report_id, flags)
    text = render_pack(case, outputs, trig, created_decision)
    p = case_path(cases_dir, report_id).parent / "approval-pack.md"
    p.write_text(text, encoding="utf-8")
    return p


# ---------------------------------------------------------------- approve

def _assemble(case: dict, outputs: dict) -> dict:
    return report_data.assemble(case, outputs, case.get("decision"))


def run_approve(cases_dir: Path, report_id: str, confirm: bool) -> dict:
    case = load_case(cases_dir, report_id)
    outputs = verify_calc(case)
    result = _assemble(case, outputs)
    snapshot = {
        "approved_at": now(),
        "report_version": case["case"]["report_version"],
        "inputs_fp": case["workflow"]["calc"]["inputs_fp"],
        "calc_fp": case["workflow"]["calc"]["calc_fp"],
        "decision_fp": jsonio.fingerprint(case.get("decision")),
        "content_fp": jsonio.fingerprint(result["body"]),
        "review_flags": result["review_flags"],
    }
    if confirm:
        case["workflow"]["approval"] = snapshot
        save_case(cases_dir, report_id, case)
    return {"snapshot": snapshot, "result": result, "recorded": confirm}


def verify_approval(case: dict, outputs: dict) -> dict:
    appr = (case.get("workflow") or {}).get("approval")
    if not appr:
        raise GateError("No founder approval recorded. Run: approve --yes (after checking the approval pack).")
    wc = case["workflow"]["calc"]
    if appr["inputs_fp"] != wc["inputs_fp"] or appr["calc_fp"] != wc["calc_fp"]:
        raise GateError("Approval was given for different inputs/calculation. Re-run pack and approve.")
    if jsonio.fingerprint(case.get("decision")) != appr["decision_fp"]:
        raise GateError("Founder decision/wording changed after approval (decision fingerprint mismatch). Approve again.")
    result = _assemble(case, outputs)
    if jsonio.fingerprint(result["body"]) != appr["content_fp"]:
        raise GateError("Customer-facing content differs from the approved snapshot (content fingerprint mismatch). Approve again.")
    return result


# ---------------------------------------------------------------- review

def review_status(cases_dir: Path, report_id: str) -> dict:
    case = load_case(cases_dir, report_id)
    appr = (case.get("workflow") or {}).get("approval")
    flags = appr["review_flags"] if appr else {}
    reasons = review.triggers(review.load(cases_dir), report_id, flags)
    return {"required": bool(reasons), "reasons": reasons, "approved": bool(appr),
            "recorded_review": (case.get("workflow") or {}).get("review")}


def review_record(cases_dir: Path, report_id: str, outcome: str, highest_severity: str, note: str | None) -> dict:
    try:
        review.validate_record(outcome, highest_severity)
    except ValueError as exc:
        raise GateError(str(exc)) from None
    case = load_case(cases_dir, report_id)
    outputs = verify_calc(case)
    verify_approval(case, outputs)
    appr = case["workflow"]["approval"]
    rec = {"outcome": outcome, "highest_severity": highest_severity, "content_fp": appr["content_fp"], "report_version": appr["report_version"],
           "recorded_at": now(), "note": note}
    case["workflow"]["review"] = rec
    save_case(cases_dir, report_id, case)
    review.append(cases_dir, {"type": "review", "report_id": report_id, "version": appr["report_version"],
                              "outcome": outcome, "highest_severity": highest_severity})
    return rec


# ---------------------------------------------------------------- build

def run_build(cases_dir: Path, report_id: str) -> Path:
    case = load_case(cases_dir, report_id)
    outputs = verify_calc(case)
    result = verify_approval(case, outputs)
    appr = case["workflow"]["approval"]
    reasons = review.triggers(review.load(cases_dir), report_id, appr["review_flags"])
    rv = case["workflow"].get("review")
    if reasons:
        if not rv or rv.get("content_fp") != appr["content_fp"]:
            raise GateError(f"Review is required ({', '.join(reasons)}) and no Review result matches this approved "
                            "content. Hand the approved package to Review, then run: review-record")
        if rv["outcome"] not in review.PASSING_OUTCOMES:
            raise GateError(f"Review outcome is '{rv['outcome']}' (highest severity {rv['highest_severity']}). "
                            "HTML generation is blocked. Correct the case, bump report_version, approve and review again.")
        gate = {"type": "review", "reasons": reasons, "outcome": rv["outcome"],
                "highest_severity": rv["highest_severity"]}
    else:
        gate = {"type": "deterministic_validation", "reasons": [], "outcome": "pass"}

    body = copy.deepcopy(result["body"])
    body["report"]["approved_at"] = appr["approved_at"]
    data = {
        **body,
        "fingerprints": {k: appr[k] for k in ("inputs_fp", "calc_fp", "decision_fp", "content_fp")},
        "gate": gate,
        "engine_version": ENGINE_VERSION,
    }
    folder = case_path(cases_dir, report_id).parent
    out = folder / f"report_data.v{appr['report_version']}.json"
    jsonio.dump(data, out)
    (folder / "trace.txt").write_text(trace_text(case, outputs, result), encoding="utf-8")
    case["workflow"]["build"] = {"built_at": now(), "path": out.name, "gate": gate, "content_fp": appr["content_fp"]}
    save_case(cases_dir, report_id, case)
    review.append(cases_dir, {"type": "build", "report_id": report_id, "version": appr["report_version"],
                              "review_required": bool(reasons), "reasons": reasons})
    return out

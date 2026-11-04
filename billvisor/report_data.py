"""Founder decision validation and customer-facing report data assembly.

``assemble`` turns case + calculation + founder decision into the
``report_data`` body. It raises GateError listing every problem; it never
fills a decision-critical field itself.
"""

from __future__ import annotations

from decimal import Decimal

from . import REPORT_DATA_CONTRACT_VERSION, lint, score
from .calc import LABELS, LIMITATION_DEFAULT_TEXT, unit_sort_key
from .energy import ESTIMATE_WORDING
from .errors import CUSTOMER_INFO_CODES, GateError
from .values import gbp_whole, nonempty_str, round_half_up

ACTION_TYPES = ["Stay put", "Improve the current setup", "Look at changing now", "Review later", "Confirm information"]
EFFORT = ["Low", "Moderate", "High"]
SOURCE_LINE = "Supporting source details are available on request."


def decision_template(case: dict, calc: dict[str, dict]) -> dict:
    """Blank decision for every unit that will get a service page (or might, via proceed_as)."""
    units = {}
    for u in case.get("analysis_units") or []:
        out = calc.get(u["id"]) or {}
        if out.get("coverage_status") == "Not analysed":
            continue
        units[u["id"]] = {
            "action_type": None,
            "effort": None,
            "priority": None,
            "headline": None,
            "explanation": None,
            "next_step": None,
            "limitation_text": None,
            "show_saving": False,
            "small_saving_not_worth_effort": False,
            "findings_shown": [],
            "proceed_as": None,
        }
    return {"units": units, "report": {"summary": None}, "manual_override": False}


def _forbidden_providers(case: dict) -> set[str]:
    current, observed = set(), set()
    for u in case.get("analysis_units") or []:
        ci = u.get("calculation_input") or {}
        facts = ci.get("facts") or {}
        for f in ("provider", "supplier"):
            if nonempty_str(facts.get(f)):
                current.add(facts[f].strip())
        for o in ci.get("observations") or []:
            if isinstance(o, dict) and nonempty_str(o.get("provider")):
                observed.add(o["provider"].strip())
    return observed - current


def assemble(case: dict, calc: dict[str, dict], decision: dict | None) -> dict:
    """Return {"body": report_data body, "final_scores": {...}, "review_flags": {...}}."""
    errors: list[str] = []
    decision = decision or {}
    dunits = decision.get("units") or {}
    info = case.get("case") or {}
    if not nonempty_str(info.get("report_id")):
        errors.append("case.report_id is required")
    if not nonempty_str(info.get("first_name")):
        errors.append("case.first_name is required")
    version = info.get("report_version")
    if isinstance(version, bool) or not isinstance(version, int) or version < 1:
        errors.append("case.report_version must be a whole number >= 1")

    units = sorted(case.get("analysis_units") or [], key=lambda u: unit_sort_key(u.get("id")))
    ids = [u.get("id") for u in units]
    if len(ids) != len(set(ids)):
        errors.append("analysis unit ids must be unique")
    requested = {u.get("id") for u in units if u.get("requested")}
    if "energy_combined" in requested and requested & {"gas", "electricity"}:
        errors.append("energy_combined and a separate gas/electricity unit are both requested; use one analysis")

    forbidden = _forbidden_providers(case)
    overview, pages, actions, final_scores, overall_entries = [], [], [], {}, []
    used_override = bool(decision.get("manual_override"))
    calc_failed = False

    for u in units:
        uid = u["id"]
        out = calc.get(uid)
        if out is None:
            errors.append(f"{uid}: no calculation output; run calc")
            continue
        label = LABELS.get(uid, uid)
        status = out.get("coverage_status")
        d = dunits.get(uid)

        if status == "Not analysed":
            if d:
                errors.append(f"{uid}: not requested, so it must have no decision entry (overview only)")
            overview.append({"unit_id": uid, "label": label, "coverage_status": "Not analysed", "score": None, "page": False})
            continue

        if not isinstance(d, dict):
            errors.append(f"{uid}: founder decision is missing")
            continue

        proceeding = False
        if out.get("stopped"):
            calc_failed = True
            codes = {i["code"] for i in out["issues"] if i["blocking"]}
            if d.get("proceed_as") != "confirm_information":
                errors.append(f"{uid}: calculation stopped ({', '.join(sorted(codes))}); resolve it or, for a customer-"
                              "information gap only, set proceed_as: confirm_information")
                continue
            if not codes <= CUSTOMER_INFO_CODES:
                errors.append(f"{uid}: proceed_as is only allowed for customer-information gaps, not "
                              f"{', '.join(sorted(codes - CUSTOMER_INFO_CODES))}")
                continue
            if d.get("action_type") != "Confirm information":
                errors.append(f"{uid}: proceed_as confirm_information requires action_type 'Confirm information'")
                continue
            proceeding, status = True, "Analysed with limitations"
        elif d.get("proceed_as") is not None:
            errors.append(f"{uid}: proceed_as is only for a stopped calculation")

        # --- founder fields ---
        at = d.get("action_type")
        if at not in ACTION_TYPES:
            errors.append(f"{uid}: action_type must be one of {ACTION_TYPES}")
        if at == "Confirm information" and not proceeding:
            errors.append(f"{uid}: Confirm information is only for a missing minimum field or disclosed specialist "
                          "arrangement (the calculation did not stop)")
        if at != "Confirm information" and d.get("effort") not in EFFORT:
            errors.append(f"{uid}: effort must be one of {EFFORT}")
        pr = d.get("priority")
        if isinstance(pr, bool) or not isinstance(pr, int) or pr < 1:
            errors.append(f"{uid}: priority must be a whole number >= 1")
        for f in ("explanation", "next_step"):
            if not nonempty_str(d.get(f)):
                errors.append(f"{uid}: {f} (approved customer wording) is required")

        sc = out.get("score")
        if proceeding:
            sc = None
        if d.get("small_saving_not_worth_effort"):
            if at != "Stay put":
                errors.append(f"{uid}: small_saving_not_worth_effort requires action_type 'Stay put'")
            elif not score.floor_eligible(sc):
                errors.append(f"{uid}: small_saving_not_worth_effort needs a supported saving above £0 and below £50")
            else:
                sc = score.apply_floor(sc)

        # --- figures ---
        spend = out.get("current_annual_spend")
        is_energy = "energy" in out
        saving_exact = None if proceeding else out.get("saving_candidate")
        saving_display = None
        if d.get("show_saving"):
            if saving_exact is None or round_half_up(saving_exact) < 1:
                errors.append(f"{uid}: show_saving is set but there is no positive supported saving (never show £0)")
            else:
                saving_display = round_half_up(saving_exact)
        comparison_display = None
        if not proceeding and not is_energy and out.get("comparison"):
            comparison_display = round_half_up(out["comparison"]["annual_comparison"])

        # --- limitation / estimate wording ---
        limitation = None
        if status == "Analysed with limitations":
            reason = out.get("limitation_reason")
            limitation = d.get("limitation_text") or LIMITATION_DEFAULT_TEXT.get(reason)
            if not nonempty_str(limitation):
                errors.append(f"{uid}: Analysed with limitations ({reason or 'confirm information'}) needs one "
                              "plain-English limitation_text")
        elif d.get("limitation_text"):
            errors.append(f"{uid}: limitation_text given but the service is Analysed with no limitation")
        estimate_note = ESTIMATE_WORDING if is_energy and not proceeding and out["energy"]["consumption_estimated"] else None

        provider_note = None
        if sc and sc.get("provider_note_triggered"):
            provider_note = score.provider_note(uid, label, sc["price_only_band"], sc["combined_band"])

        available = {f["id"]: f["text"] for f in out.get("findings_available") or []}
        findings = []
        for fid in d.get("findings_shown") or []:
            if fid not in available:
                errors.append(f"{uid}: finding {fid!r} is not available from the case facts")
            else:
                findings.append({"id": fid, "text": available[fid]})

        score_block = None
        if sc:
            score_block = {"value": sc["display"], "band": sc["band"], "colour": score.COLOUR[sc["band"]],
                           "estimated": bool(sc.get("estimated"))}
            final_scores[uid] = {"exact": sc["exact"], "display": sc["display"], "band": sc["band"],
                                 "floor_applied": bool(sc.get("floor_applied"))}
        overall_entries.append({"unit_id": uid, "status": status, "exact": sc["exact"] if sc else None,
                                "current_annual": spend if spend is not None else Decimal(0)})

        texts = [d.get("headline"), d.get("explanation"), d.get("next_step"), limitation]
        for t in texts:
            if nonempty_str(t):
                for p in lint.check_text(t, forbidden_providers=forbidden, allow_customer_gap=proceeding):
                    errors.append(f"{uid}: {p}: {t!r}")

        page = {
            "unit_id": uid,
            "label": label,
            "coverage_status": status,
            "limitation": limitation,
            "estimate_note": estimate_note,
            "current_annual_spend_gbp": round_half_up(spend) if spend is not None and not proceeding else None,
            "current_annual_spend_basis": ("estimated_annual_cost" if is_energy else "monthly_payment_x12"),
            "comparison_annual_gbp": comparison_display,
            "comparison_text": (f"Similar services cost about {gbp_whole(comparison_display)} a year."
                                if comparison_display is not None else None),
            "potential_saving_gbp": saving_display,
            "score": score_block,
            "provider_note": provider_note,
            "action_type": at,
            "effort": d.get("effort"),
            "headline": d.get("headline"),
            "explanation": d.get("explanation"),
            "next_step": d.get("next_step"),
            "findings": findings,
        }
        pages.append(page)
        overview.append({"unit_id": uid, "label": label, "coverage_status": status, "score": score_block, "page": True})
        actions.append({"unit_id": uid, "label": label, "priority": pr, "action_type": at, "next_step": d.get("next_step"),
                        "potential_saving_gbp": saving_display})

    summary = (decision.get("report") or {}).get("summary")
    if nonempty_str(summary):
        for p in lint.check_text(summary, forbidden_providers=forbidden, allow_customer_gap=False):
            errors.append(f"report.summary: {p}")
    if not pages:
        errors.append("no service pages: at least one requested service must be reportable")
    if errors:
        raise GateError("Decision/report data checks failed:\n  - " + "\n  - ".join(errors))

    ov = score.overall(overall_entries)
    actions.sort(key=lambda a: (a["priority"], -(a["potential_saving_gbp"] or 0), unit_sort_key(a["unit_id"])))
    top = actions[0]["priority"] if actions else None
    primary_lacn = any(a["priority"] == top and a["action_type"] == "Look at changing now" for a in actions)
    body = {
        "contract_version": REPORT_DATA_CONTRACT_VERSION,
        "report": {"report_id": info["report_id"], "first_name": info["first_name"], "report_version": version},
        "overall": (
            {"value": ov["display"], "band": ov["band"], "colour": score.COLOUR[ov["band"]],
             "contributing_services": ov["contributing_services"]}
            if ov else None
        ),
        "overview": overview,
        "service_pages": pages,
        "priority_actions": actions,
        "summary": summary if nonempty_str(summary) else None,
        # BILLS_HEALTH_SCORE_METHOD section 6: "Include once per report".
        "report_notes": [SOURCE_LINE],
    }
    return {
        "body": body,
        "final_scores": final_scores,
        "overall": ov,
        "review_flags": {
            "calculator_failure_or_override": calc_failed or used_override,
            "primary_look_at_changing_now": primary_lacn,
        },
    }

"""Per-unit deterministic calculation: minimum fields, comparison, score, coverage.

Produces ``calculation_output`` for each analysis unit. Coverage here is the
pre-decision status; a stopped unit has ``coverage_status: None`` until the
issue is resolved or the founder records ``proceed_as``.
"""

from __future__ import annotations

from decimal import Decimal

from . import ENGINE_VERSION, energy, offers, provider, score
from .errors import Issue, StopError
from .values import dec, gbp, gbp_whole, is_iso_date, iso_date, long_date, nonempty_str, round_half_up

SUPPORTED_UNITS = {
    "broadband": ["broadband"],
    "mobile": ["mobile"],
    "energy_combined": ["gas", "electricity"],
    "gas": ["gas"],
    "electricity": ["electricity"],
}
UNIT_ORDER = ["broadband", "mobile", "energy_combined", "electricity", "gas"]
LABELS = {"broadband": "Broadband", "mobile": "Mobile", "energy_combined": "Energy", "gas": "Gas", "electricity": "Electricity"}
ENERGY_UNITS = {"energy_combined", "gas", "electricity"}
CONTRACT_WORDS = {"out_of_contract", "unknown"}
TARIFF_END_WORDS = {"no_end_date", "unknown"}

# Limitation reason codes and, where an approved fixed wording exists, its text.
LIMITATION_DEFAULT_TEXT = {
    "PROVIDER_QUALITY_UNAVAILABLE": "This score is based on price comparison only.",
}


def _missing(code: str, field: str, msg: str | None = None) -> StopError:
    return StopError(code, msg or f"{field} is required", f"facts.{field}")


def check_minimum(unit_id: str, facts: dict, case_info: dict) -> None:
    """Agreed minimum fields (LIVE_CASE_CALCULATOR_SPEC section 1)."""
    if not isinstance(facts, dict):
        raise _missing("MINIMUM_FIELD_MISSING", "facts", "customer facts are missing")

    def need_str(f: str) -> None:
        if facts.get(f) is None:
            raise _missing("MINIMUM_FIELD_MISSING", f)
        if not nonempty_str(facts[f]):
            raise _missing("MINIMUM_FIELD_AMBIGUOUS", f, f"{f} is empty or not text")

    def need_money(f: str) -> None:
        if facts.get(f) is None:
            raise _missing("MINIMUM_FIELD_MISSING", f)
        dec(facts[f], f"facts.{f}", "MINIMUM_FIELD_AMBIGUOUS", positive=True)

    def need_contract_end(f: str, words: set[str]) -> None:
        v = facts.get(f)
        if v is None:
            raise _missing("MINIMUM_FIELD_MISSING", f, f"{f} is required (date, {' or '.join(sorted(words))})")
        if v not in words and not is_iso_date(v):
            raise _missing("MINIMUM_FIELD_AMBIGUOUS", f, f"{f} must be an ISO date or one of {sorted(words)}: {v!r}")

    if unit_id == "broadband":
        need_str("provider")
        need_money("download_speed_mbps")
        need_money("monthly_price_gbp")
        need_contract_end("contract_end", CONTRACT_WORDS)
    elif unit_id == "mobile":
        need_str("provider")
        if facts.get("data_allowance_unlimited") is not True:
            if facts.get("data_allowance_gb") is None:
                raise _missing("MINIMUM_FIELD_MISSING", "data_allowance_gb", "data allowance (GB or unlimited) is required")
            dec(facts["data_allowance_gb"], "facts.data_allowance_gb", "MINIMUM_FIELD_AMBIGUOUS", positive=True)
        need_str("handset_or_important_extras")
        if not isinstance(facts.get("handset_included"), bool):
            raise _missing("MINIMUM_FIELD_AMBIGUOUS", "handset_included",
                           "handset_included (true/false) must be recorded from the customer's handset/extras answer")
        need_money("monthly_price_gbp")
        need_contract_end("contract_end", CONTRACT_WORDS)
    else:
        if not nonempty_str(case_info.get("postcode")):
            raise StopError("MINIMUM_FIELD_MISSING", "postcode is required for energy", "case.postcode")
        for f in ("supplier", "payment_method", "tariff_type_or_name"):
            need_str(f)
        if facts.get("fuels") is None:
            raise _missing("MINIMUM_FIELD_MISSING", "fuels")
        if facts.get("approximate_payment") in (None, ""):
            raise _missing("MINIMUM_FIELD_MISSING", "approximate_payment")
        need_contract_end("tariff_end", TARIFF_END_WORDS)


def _findings(unit_id: str, facts: dict, eng: dict | None) -> list[dict]:
    """Optional fact-based findings. The founder chooses which to show."""
    out = []
    if unit_id in ("broadband", "mobile"):
        ce = facts.get("contract_end")
        if ce == "out_of_contract":
            out.append({"id": "out_of_contract", "text": "You are currently out of contract."})
        elif is_iso_date(ce):
            out.append({"id": "contract_end_date", "text": f"Your contract ends on {long_date(iso_date(ce, 'contract_end'))}."})
    if unit_id == "mobile" and facts.get("typical_data_use_gb") is not None and facts.get("data_allowance_gb") is not None:
        use = dec(facts["typical_data_use_gb"], "facts.typical_data_use_gb")
        allowance = dec(facts["data_allowance_gb"], "facts.data_allowance_gb")
        if use < allowance:
            out.append({"id": "unused_allowance",
                        "text": f"You typically use about {use.normalize():f} GB of your {allowance.normalize():f} GB monthly data allowance."})
    if eng is not None:
        te = eng["current_tariff"]["tariff_end"]
        if is_iso_date(te):
            out.append({"id": "tariff_end_date", "text": f"Your current tariff ends on {long_date(iso_date(te, 'tariff_end'))}."})
        elif te == "no_end_date":
            out.append({"id": "no_tariff_end_date", "text": "Your current tariff has no fixed end date."})
        fee = eng["current_tariff"]["exit_fee_gbp"]
        if fee != "unknown":
            fee_d = dec(fee, "exit_fee_gbp")
            if fee_d > 0:
                txt = f"£{fee_d:,.2f}" if fee_d != fee_d.to_integral_value() else f"£{int(fee_d):,}"
                out.append({"id": "exit_fee", "text": f"Your current tariff has an exit fee of {txt}."})
        if eng["score_status"] == "estimated_score" and eng["score_comparison_value"] < eng["current_annual_cost"]:
            diff = round_half_up(eng["current_annual_cost"] - eng["score_comparison_value"])
            if diff > 0:
                out.append({"id": "payment_method_saving",
                            "text": f"Paying by {eng['score_comparison_payment_method']} on the same tariff would cost an "
                                    f"estimated {gbp_whole(diff)} less a year."})
    return out


def _stopped(issues: list[Issue], trace: list[str], extra: dict | None = None) -> dict:
    out = {
        "engine_version": ENGINE_VERSION,
        "coverage_status": None,
        "limitation_reason": None,
        "stopped": True,
        "issues": [i.to_dict() for i in issues],
        "score": None,
        "trace": trace + [f"STOP {i.code}: {i.message}" for i in issues],
    }
    if extra:
        out.update(extra)
    return out


def calculate_unit(unit: dict, case_info: dict, table_dir=None) -> dict:
    uid = unit.get("id")
    requested = unit.get("requested")
    if requested is None:
        return _stopped([Issue("UNIT_REQUESTED_UNSET", f"{uid}: requested is not set", "requested")], [])
    if requested is False:
        return {"engine_version": ENGINE_VERSION, "coverage_status": "Not analysed", "limitation_reason": None,
                "stopped": False, "issues": [], "score": None, "trace": [f"{uid}: not requested"]}
    if uid not in SUPPORTED_UNITS:
        return _stopped([Issue("REQUESTED_SERVICE_UNSUPPORTED", f"{uid!r} is not a supported Phase 1 service", "id"),
                         Issue("REPORT_TREATMENT_POLICY_UNRESOLVED", "report treatment for this service is undecided", "id")], [])
    if sorted(unit.get("services") or []) != sorted(SUPPORTED_UNITS[uid]):
        return _stopped([Issue("INPUT_INVALID", f"{uid}.services must be {SUPPORTED_UNITS[uid]}", "services")], [])

    cinput = unit.get("calculation_input") or {}
    facts = cinput.get("facts") or {}
    trace: list[str] = []
    issues: list[Issue] = []
    if not nonempty_str(cinput.get("customer_source_ref")):
        issues.append(Issue("INPUT_INVALID", "customer_source_ref is required for a requested service",
                            "calculation_input.customer_source_ref"))
        return _stopped(issues, trace)

    if uid in ENERGY_UNITS and nonempty_str(case_info.get("postcode")) and energy.is_northern_ireland(case_info["postcode"]):
        return _stopped([Issue("REQUESTED_GEOGRAPHY_UNSUPPORTED", "energy analysis covers England, Scotland and Wales only",
                               "case.postcode"),
                         Issue("REPORT_TREATMENT_POLICY_UNRESOLVED", "report treatment for Northern Ireland energy is undecided",
                               "case.postcode")], trace)

    try:
        check_minimum(uid, facts, case_info)
    except StopError as e:
        return _stopped([e.issue], trace)

    findings: list[dict] = []
    try:
        if uid in ENERGY_UNITS:
            out = _energy_unit(uid, facts, cinput, trace, issues, findings)
        else:
            out = _telecom_unit(uid, facts, cinput, trace, issues, findings, table_dir)
    except StopError as e:
        return _stopped(issues + [e.issue], trace)
    out.update({"engine_version": ENGINE_VERSION, "stopped": False, "issues": [i.to_dict() for i in issues],
                "findings_available": findings, "trace": trace})
    return out


def _telecom_unit(uid, facts, cinput, trace, issues, findings, table_dir) -> dict:
    current = dec(facts["monthly_price_gbp"], "facts.monthly_price_gbp", "MINIMUM_FIELD_AMBIGUOUS", positive=True)
    current_annual = current * 12
    comp = offers.comparison(uid, cinput.get("observations"), facts)
    trace.extend(comp.pop("trace"))
    trace.append(f"current: {gbp(current)}/month x 12 = {gbp(current_annual)}")

    pos_block = None
    pt = cinput.get("provider_table")
    if not isinstance(pt, dict) or not nonempty_str(pt.get("table_ref")):
        raise StopError("INPUT_INVALID", "provider_table.table_ref is required", "calculation_input.provider_table")
    table = provider.load_table(pt["table_ref"], table_dir)
    if table["service"] != uid:
        raise StopError("INPUT_INVALID", f"provider table {pt['table_ref']} is for {table['service']}, not {uid}",
                        "calculation_input.provider_table")
    if pt.get("table_version") != table["table_version"]:
        raise StopError("MATERIAL_EVIDENCE_CONFLICT",
                        f"case cites table version {pt.get('table_version')!r} but the current table is "
                        f"{table['table_version']!r}; confirm which table applies", "calculation_input.provider_table")
    provider_id = pt.get("provider_id") or facts["provider"]
    try:
        pos_block = provider.position(table, provider_id)
        trace.append(f"provider {provider_id}: raw {pos_block['raw_score']}, rank {pos_block['rank']} "
                     f"(best {pos_block['best_rank']}, worst {pos_block['worst_rank']}) -> position {pos_block['position']} "
                     f"[{table['table_ref']} {table['table_version']} {table['table_date']}]")
    except StopError as e:
        if e.issue.code != "NEW_PROVIDER_ASSESSMENT_REQUIRED":
            raise
        issues.append(e.issue)
        trace.append(f"provider position unavailable: {e.issue.message}; price-only score")

    sc = score.service_score(service=uid, current=current, comparison=comp["monthly_comparison"],
                             current_annual=current_annual, comparison_annual=comp["annual_comparison"],
                             provider_position=pos_block["position"] if pos_block else None)
    trace.extend(sc.pop("trace"))

    sufficient = cinput.get("comparison_sufficient_for_score", True)
    if not isinstance(sufficient, bool):
        raise StopError("INPUT_INVALID", "comparison_sufficient_for_score must be true or false",
                        "calculation_input.comparison_sufficient_for_score")
    reasons = []
    if not sufficient:
        reasons.append("ESTIMATED_COMPARISON")
    if pos_block is None:
        reasons.append("PROVIDER_QUALITY_UNAVAILABLE")
    sc["estimated"] = not sufficient
    if sc["provider_note_triggered"] and pos_block and pos_block.get("sources_publicly_accessible") is not True:
        raise StopError("METHOD_OR_SOURCE_RULE_MISSING",
                        "the provider note is triggered but the table does not confirm its sources are publicly accessible, "
                        "so the approved 'public data' wording cannot be used", "provider_table.sources_publicly_accessible")
    findings.extend(_findings(uid, facts, None))
    saving = current_annual - comp["annual_comparison"]
    return {
        "coverage_status": "Analysed with limitations" if reasons else "Analysed",
        "limitation_reason": reasons[0] if reasons else None,
        "limitation_reasons": reasons,
        "current_annual_spend": current_annual,
        "comparison": {k: comp[k] for k in ("monthly_comparison", "annual_comparison", "provider_count", "offer_count",
                                            "offers", "excluded", "provider_means", "estimation_flags")},
        "saving_candidate": saving if saving > 0 else None,
        "provider_position": pos_block,
        "score": sc,
    }


def _energy_unit(uid, facts, cinput, trace, issues, findings) -> dict:
    eng = energy.calculate(uid, facts, cinput)
    trace.extend(eng.pop("trace"))
    sc = None
    reasons: list[str] = []
    if eng["score_status"] == "no_score":
        issues.append(Issue("ENERGY_SCORE_COMPARISON_UNAPPROVED", "no approved energy score comparison selected"))
        reasons.append("ENERGY_SCORE_COMPARISON_UNAPPROVED")
    else:
        sc = score.service_score(service="energy", current=eng["current_annual_cost"],
                                 comparison=eng["score_comparison_value"], current_annual=eng["current_annual_cost"],
                                 comparison_annual=eng["score_comparison_value"], provider_position=None)
        trace.extend(sc.pop("trace"))
        sc["estimated"] = eng["score_status"] == "estimated_score"
        if sc["estimated"]:
            reasons.append("ENERGY_PAYMENT_METHOD_ESTIMATED_SCORE")
    findings.extend(_findings(uid, facts, eng))
    saving = eng["current_annual_cost"] - eng["score_comparison_value"] if eng["score_comparison_value"] is not None else None
    return {
        # Founder decision 2026-11-04: bedroom fallback and energy price-only are not limitations.
        "coverage_status": "Analysed with limitations" if reasons else "Analysed",
        "limitation_reason": reasons[0] if reasons else None,
        "limitation_reasons": reasons,
        "current_annual_spend": eng["current_annual_cost"],
        "energy": eng,
        "saving_candidate": saving if saving is not None and saving > 0 else None,
        "provider_position": None,
        "score": sc,
    }


def calculate_case(case: dict, table_dir=None) -> dict[str, dict]:
    info = case.get("case") or {}
    return {u.get("id"): calculate_unit(u, info, table_dir) for u in case.get("analysis_units") or []}


def unit_sort_key(uid: str) -> int:
    return UNIT_ORDER.index(uid) if uid in UNIT_ORDER else len(UNIT_ORDER)


__all__ = ["calculate_case", "calculate_unit", "LABELS", "LIMITATION_DEFAULT_TEXT", "Decimal"]

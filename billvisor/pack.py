"""Founder approval pack (markdown). Facts and calculations only; never a recommendation."""

from __future__ import annotations

from .calc import LABELS, LIMITATION_DEFAULT_TEXT, unit_sort_key
from .energy import ESTIMATE_WORDING
from .score import COLOUR, floor_eligible
from .values import gbp, gbp_whole, round_half_up

INTERNAL = "_internal — never customer-facing_"


def _facts_lines(unit: dict) -> list[str]:
    facts = (unit.get("calculation_input") or {}).get("facts") or {}
    return [f"  - {k}: {v}" for k, v in facts.items()] or ["  - (no facts recorded)"]


def render_pack(case: dict, outputs: dict, review_triggers: list[str], created_decision: bool) -> str:
    info = case.get("case") or {}
    L = [f"# Approval pack — {info.get('report_id')} v{info.get('report_version')}",
         "",
         f"First name: {info.get('first_name')}  ",
         f"Postcode: {info.get('postcode')}",
         "",
         "This pack lists facts, calculations and permitted content. It does not propose a recommendation: "
         "choose the action, effort, priority and exact wording in `decision` in case.json, then run `approve`.",
         ""]
    units = sorted(case.get("analysis_units") or [], key=lambda u: unit_sort_key(u.get("id")))
    for u in units:
        uid = u.get("id")
        out = outputs.get(uid) or {}
        label = LABELS.get(uid, uid)
        L.append(f"## {label} (`{uid}`)")
        L.append(f"- Coverage status: **{out.get('coverage_status') or 'STOPPED — no status'}**"
                 + (f" (reason `{out['limitation_reason']}`)" if out.get("limitation_reason") else ""))
        if out.get("coverage_status") == "Not analysed":
            L.append("- Overview only; no service page, no decision needed.")
            L.append("")
            continue
        L.append("- Facts supplied:")
        L.extend(_facts_lines(u))
        for i in out.get("issues") or []:
            L.append(f"- {'STOP' if i['blocking'] else 'Note'} `{i['code']}`: {i['message']}  \n  Next: {i['next_action']}")
        if out.get("stopped"):
            L.append("- No calculation. If this is a customer-information gap, you may set "
                     "`proceed_as: confirm_information` (Analysed with limitations, no score, action Confirm information).")
            L.append("")
            continue

        L.append(f"- Calculation ({INTERNAL}):")
        spend = out["current_annual_spend"]
        if "energy" in out:
            e = out["energy"]
            for fuel, c in e["consumption"].items():
                L.append(f"  - {fuel} consumption {c['kwh']} kWh from {c['source']}")
            for oid, c in e["costs"].items():
                L.append(f"  - {oid}: annual {gbp(c['total'])}")
            L.append(f"  - score route: {e['score_status']}" + (f" via {e['score_observation_id']}" if e["score_observation_id"] else ""))
            for cand in e["saving_candidates"]:
                if cand["difference"] is not None:
                    L.append(f"  - saving candidate vs {cand['observation_id']}: {gbp(cand['difference'])} (not a recommendation)")
        else:
            c = out["comparison"]
            L.append(f"  - comparison {gbp(c['monthly_comparison'])}/month from {c['provider_count']} provider(s), "
                     f"{c['offer_count']} offer(s); annual {gbp(c['annual_comparison'])}")
            for f in c["estimation_flags"]:
                L.append(f"  - estimate: {f['observation_id']} uses the advertised price for periods {f['estimated_periods']}")
        L.append(f"  - current annual {gbp(spend)}; saving candidate "
                 f"{gbp(out['saving_candidate']) if out.get('saving_candidate') is not None else 'none'}")
        sc = out.get("score")
        if sc:
            L.append(f"  - score exact {sc['exact']} -> **{sc['display']} {sc['band']}**"
                     f"{' (qualified comparison — internal flag)' if sc.get('estimated') else ''}; materiality {sc['materiality']}"
                     f"{'; capped' if sc.get('cap_applied') is not None else ''}; provider note "
                     f"{'triggered' if sc['provider_note_triggered'] else 'not triggered'}")
            if floor_eligible(sc):
                L.append("  - Floor eligibility: the saving is above £0 and below £50. The 75 floor applies ONLY if you "
                         "choose Stay put because the saving is not worth the effort (`small_saving_not_worth_effort: true`).")
        else:
            L.append("  - no numeric score")

        L.append("- Customer-facing fields this service would show:")
        L.append(f"  - annual spend: {gbp_whole(round_half_up(spend))}"
                 + (" (estimated annual cost)" if "energy" in out else " (monthly payment x 12)"))
        if "comparison" in out:
            L.append(f"  - comparison: \"Similar services cost about {gbp_whole(round_half_up(out['comparison']['annual_comparison']))} a year.\"")
        if out.get("saving_candidate") is not None and round_half_up(out["saving_candidate"]) >= 1:
            L.append(f"  - potential saving if you set `show_saving: true`: {gbp_whole(round_half_up(out['saving_candidate']))} "
                     "(no 'about' prefix)")
        if sc:
            L.append(f"  - score before decision: {sc['display']} {sc['band']} ({COLOUR[sc['band']]})"
                     f"{' [qualified comparison — internal flag]' if sc.get('estimated') else ''}")
        if "energy" in out and out["energy"]["consumption_estimated"]:
            L.append(f"  - estimate wording (automatic): \"{ESTIMATE_WORDING}\"")
        if out.get("limitation_reason"):
            default = LIMITATION_DEFAULT_TEXT.get(out["limitation_reason"])
            L.append(f"  - limitation: " + (f"default \"{default}\" (override with limitation_text)" if default
                                             else "**write one plain-English limitation_text**"))
        if out.get("findings_available"):
            L.append("- Optional findings (add ids to `findings_shown` to show):")
            for f in out["findings_available"]:
                L.append(f"  - `{f['id']}`: \"{f['text']}\"")
        L.append("")

    L.append("## Review")
    L.append(f"- Triggers so far: {', '.join(review_triggers) if review_triggers else 'none (deterministic gate)'}")
    L.append("- A primary Look at changing now action will also require Review.")
    L.append("")
    L.append("## Report-wide")
    L.append("- \"Supporting source details are available on request.\" is included once.")
    L.append("- Customer text is checked for: benchmark, deals/provider names from captures, source names, £0, "
             "guaranteed, best deal, whole market, cheapest, reviews, 'about' before a saving.")
    if created_decision:
        L.append("")
        L.append("A blank `decision` section has been added to case.json.")
    return "\n".join(L) + "\n"

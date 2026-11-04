"""Great Britain energy calculation (LIVE_CASE_CALCULATOR_SPEC, OFFER_DATA_METHOD).

Consumption hierarchy, annual tariff cost per observation and the two
founder-approved score routes. Never picks "the market" or the cheapest tariff.
"""

from __future__ import annotations

from decimal import Decimal

from .errors import StopError
from .values import dec, gbp, nonempty_str

FUEL_SETS = {"both": ("electricity", "gas"), "electricity": ("electricity",), "gas": ("gas",)}
UNIT_FUELS = {"energy_combined": "both", "electricity": "electricity", "gas": "gas"}
# Ofgem TDCVs effective 1 July 2026, selected by bedrooms only.
BEDROOM_FALLBACK = {
    "1-2": {"electricity": Decimal(1600), "gas": Decimal(6000)},
    "3-4": {"electricity": Decimal(2500), "gas": Decimal(9500)},
    "5+": {"electricity": Decimal(3800), "gas": Decimal(14000)},
}
SPECIALIST_VALUES = {"none", "prepayment", "multi_rate", "electric_heating", "heat_pump", "ev_charging", "other"}
ESTIMATE_WORDING = "Your consumption was estimated from households with similar characteristics."


def bedroom_band(bedrooms: int) -> str:
    if bedrooms <= 2:
        return "1-2"
    if bedrooms <= 4:
        return "3-4"
    return "5+"


def is_northern_ireland(postcode: str) -> bool:
    return postcode.strip().upper().replace(" ", "").startswith("BT")


def select_consumption(facts: dict, fuels: tuple[str, ...]) -> dict:
    """Per fuel: actual -> supplier estimate -> bedroom fallback."""
    actual = facts.get("actual_annual_kwh_by_fuel") or {}
    supplier = facts.get("supplier_estimated_annual_kwh_by_fuel") or {}
    out: dict[str, dict] = {}
    for fuel in fuels:
        if actual.get(fuel) is not None:
            out[fuel] = {"kwh": dec(actual[fuel], f"actual_annual_kwh_by_fuel.{fuel}", "MINIMUM_FIELD_AMBIGUOUS", True),
                         "source": "actual_12_month"}
        elif supplier.get(fuel) is not None:
            out[fuel] = {"kwh": dec(supplier[fuel], f"supplier_estimated_annual_kwh_by_fuel.{fuel}", "MINIMUM_FIELD_AMBIGUOUS", True),
                         "source": "supplier_estimate"}
        else:
            specialist = facts.get("specialist_setup")
            if specialist is None:
                raise StopError("MINIMUM_FIELD_MISSING",
                                "specialist_setup (none or the disclosed arrangement) is needed before using the bedroom estimate",
                                "facts.specialist_setup")
            if specialist != "none":
                raise StopError("SPECIALIST_ENERGY_USAGE_REQUIRED",
                                f"specialist arrangement '{specialist}' disclosed and no annual usage for {fuel}; "
                                "the ordinary bedroom estimate must not be used", "facts.specialist_setup")
            bedrooms = facts.get("bedrooms")
            if bedrooms is None:
                raise StopError("MINIMUM_FIELD_MISSING", f"no annual usage for {fuel}, so number of bedrooms is required",
                                "facts.bedrooms")
            if isinstance(bedrooms, bool) or not isinstance(bedrooms, int) or bedrooms < 1:
                raise StopError("MINIMUM_FIELD_AMBIGUOUS", f"bedrooms must be a whole number: {bedrooms!r}", "facts.bedrooms")
            b = bedroom_band(bedrooms)
            out[fuel] = {"kwh": BEDROOM_FALLBACK[b][fuel], "source": "bedroom_fallback", "bedroom_band": b}
    return out


def _check_obs(obs: dict, i: int, fuels: tuple[str, ...]) -> None:
    where = f"observations[{i}]"
    if not isinstance(obs, dict):
        raise StopError("INPUT_INVALID", f"{where} must be an object", where)
    for f in ("observation_id", "role", "provider", "tariff_label", "tariff_type", "region", "fuels", "meter_type",
              "payment_method", "source_ref", "captured_at"):
        if not nonempty_str(obs.get(f)):
            raise StopError("INPUT_INVALID", f"{where}.{f} is required", f"{where}.{f}")
    for f in ("tariff_end", "exit_fee_gbp"):
        if obs.get(f) is None:
            raise StopError("INPUT_INVALID", f"{where}.{f} is required (captured value or 'unknown')", f"{where}.{f}")
    if obs["role"] not in ("current_cost_model", "accessible_alternative"):
        raise StopError("INPUT_INVALID", f"{where}.role must be current_cost_model or accessible_alternative", f"{where}.role")
    if FUEL_SETS.get(obs["fuels"]) != fuels:
        raise StopError("INPUT_INVALID", f"{obs['observation_id']}: fuels {obs['fuels']!r} do not match this unit", f"{where}.fuels")
    rates = obs.get("rates")
    if not isinstance(rates, dict):
        raise StopError("INPUT_INVALID", f"{where}.rates is required", f"{where}.rates")
    for fuel in fuels:
        r = rates.get(fuel)
        if not isinstance(r, dict):
            raise StopError("INPUT_INVALID", f"{where}.rates.{fuel} is required", f"{where}.rates.{fuel}")
        if "registers" in r:
            raise StopError("CALCULATOR_CANNOT_SAFELY_PROCESS",
                            f"{obs['observation_id']}: multi-register rates are not supported by this calculator",
                            f"{where}.rates.{fuel}")


def annual_cost(obs: dict, consumption: dict) -> dict:
    per_fuel, total, trace = {}, Decimal(0), []
    for fuel, c in consumption.items():
        r = obs["rates"][fuel]
        unit = dec(r.get("unit_rate_p_per_kwh"), f"{obs['observation_id']}.rates.{fuel}.unit_rate_p_per_kwh", positive=True)
        sc = dec(r.get("standing_charge_p_per_day"), f"{obs['observation_id']}.rates.{fuel}.standing_charge_p_per_day")
        cost = c["kwh"] * (unit / 100) + 365 * (sc / 100)
        per_fuel[fuel] = cost
        total += cost
        trace.append(f"{obs['observation_id']} {fuel}: {c['kwh']} kWh x {unit}p + 365 x {sc}p = {gbp(cost)}")
    return {"per_fuel": per_fuel, "total": total, "trace": trace}


ROUTE_MATCH = {
    # like-for-like payment method: everything matches except payment method.
    "score_comparison_observation_id": ("provider", "region", "fuels", "meter_type", "tariff_type"),
    # tariff fit: tariff type may differ; payment method must match.
    "tariff_fit_score_observation_id": ("provider", "region", "fuels", "meter_type", "payment_method"),
}


def calculate(unit_id: str, facts: dict, cinput: dict) -> dict:
    fuels = FUEL_SETS[UNIT_FUELS[unit_id]]
    if FUEL_SETS.get(facts.get("fuels")) != fuels:
        raise StopError("MINIMUM_FIELD_AMBIGUOUS",
                        f"customer fuels {facts.get('fuels')!r} do not match the {unit_id} analysis unit", "facts.fuels")
    specialist = facts.get("specialist_setup")
    if specialist is not None and specialist not in SPECIALIST_VALUES:
        raise StopError("MINIMUM_FIELD_AMBIGUOUS",
                        f"specialist_setup must be one of {sorted(SPECIALIST_VALUES)}", "facts.specialist_setup")
    consumption = select_consumption(facts, fuels)
    if specialist == "multi_rate":
        raise StopError("CALCULATOR_CANNOT_SAFELY_PROCESS",
                        "multi-rate (e.g. Economy 7) needs register-level calculation, which this calculator does not implement",
                        "facts.specialist_setup")

    observations = cinput.get("observations") or []
    ids = [o.get("observation_id") for o in observations if isinstance(o, dict)]
    if len(ids) != len(set(ids)):
        raise StopError("INPUT_INVALID", "observation_id values must be unique", "observations")
    for i, o in enumerate(observations):
        _check_obs(o, i, fuels)
    current = [o for o in observations if o["role"] == "current_cost_model"]
    if len(current) != 1:
        raise StopError("NO_USABLE_CAPTURED_PRICE",
                        "exactly one current_cost_model observation (the household's current tariff rates) is needed",
                        "observations")
    cur = current[0]

    trace = [f"consumption {fuel}: {c['kwh']} kWh ({c['source']}{', ' + c['bedroom_band'] + ' bedrooms' if 'bedroom_band' in c else ''})"
             for fuel, c in consumption.items()]
    costs = {}
    for o in observations:
        ac = annual_cost(o, consumption)
        costs[o["observation_id"]] = ac
        trace.extend(ac["trace"])
        trace.append(f"{o['observation_id']} ({o['role']}) annual total = {gbp(ac['total'])}")
    cur_total = costs[cur["observation_id"]]["total"]
    candidates = []
    for o in observations:
        if o is cur:
            continue
        diff = cur_total - costs[o["observation_id"]]["total"]
        candidates.append({"observation_id": o["observation_id"], "difference": diff if diff > 0 else None})

    selected = [k for k in ROUTE_MATCH if cinput.get(k)]
    if len(selected) > 1:
        raise StopError("INPUT_INVALID", "select only one energy score route", selected[1])
    route, score_obs = None, None
    if selected:
        key = selected[0]
        oid = cinput[key]
        score_obs = next((o for o in observations if o["observation_id"] == oid), None)
        if score_obs is None or score_obs["role"] != "accessible_alternative":
            raise StopError("INPUT_INVALID", f"{key} must name an accessible_alternative observation", key)
        for f in ROUTE_MATCH[key]:
            if str(score_obs[f]).strip().lower() != str(cur[f]).strip().lower():
                raise StopError("INPUT_INVALID",
                                f"{key}: {f} differs from the current tariff ({score_obs[f]!r} vs {cur[f]!r}); "
                                "this route needs a like-for-like match", key)
        if key == "score_comparison_observation_id":
            if score_obs["payment_method"].strip().lower() == cur["payment_method"].strip().lower():
                raise StopError("INPUT_INVALID", "the payment-method route needs a different payment method", key)
            route = "estimated_score"
        else:
            route = "tariff_fit_score"
        trace.append(f"score route {route} using {oid} (founder-selected)")

    exit_fee = cur["exit_fee_gbp"]
    return {
        "consumption": consumption,
        "consumption_estimated": any(c["source"] == "bedroom_fallback" for c in consumption.values()),
        "costs": {k: {"per_fuel": v["per_fuel"], "total": v["total"]} for k, v in costs.items()},
        "current_observation_id": cur["observation_id"],
        "current_annual_cost": cur_total,
        "saving_candidates": candidates,
        "score_status": route or "no_score",
        "score_observation_id": score_obs["observation_id"] if score_obs else None,
        "score_comparison_value": costs[score_obs["observation_id"]]["total"] if score_obs else None,
        "score_comparison_payment_method": score_obs["payment_method"] if score_obs else None,
        "current_tariff": {"tariff_end": cur["tariff_end"], "exit_fee_gbp": exit_fee, "tariff_type": cur["tariff_type"],
                           "payment_method": cur["payment_method"]},
        "trace": trace,
    }

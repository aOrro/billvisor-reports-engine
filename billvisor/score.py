"""Bills Health Score (BILLS_HEALTH_SCORE_METHOD)."""

from __future__ import annotations

from decimal import Decimal

from .values import gbp, round_half_up

D = Decimal
BAND_ORDER = {"Poor": 0, "Medium": 1, "Good": 2}
COLOUR = {"Poor": "red", "Medium": "amber", "Good": "green"}
STATUS_WEIGHT = {"Analysed": D("1.0"), "Analysed with limitations": D("0.8")}
PROVIDER_NOTE_AREAS = {
    "broadband": "reliability and customer support",
    "mobile": "network experience and customer support",
    "energy": "billing and customer support",
}
FLOOR = D(75)
FLOOR_MAX_SAVING = D(50)


def band(display: int) -> str:
    if display <= 39:
        return "Poor"
    if display <= 74:
        return "Medium"
    return "Good"


def price_score(current: Decimal, comparison: Decimal) -> Decimal:
    if current <= 0 or comparison <= 0:
        raise ValueError("price score needs positive current and comparison values")
    return min(D(100), D(20) + D(60) * comparison / current)


def materiality_cap(saving: Decimal, current_annual: Decimal) -> tuple[str, Decimal | None]:
    share = saving / current_annual
    if saving >= 150 and share >= D("0.25"):
        return "high", D(39)
    if saving >= 100 and share >= D("0.15"):
        return "moderate", D(74)
    return "none", None


def service_score(
    *,
    service: str,
    current: Decimal,
    comparison: Decimal,
    current_annual: Decimal,
    comparison_annual: Decimal,
    provider_position: Decimal | None,
) -> dict:
    """Exact score before any founder-approved floor.

    ``current``/``comparison`` are monthly values for broadband/mobile and
    annual values for energy (the ratio is identical either way).
    """
    ps = price_score(current, comparison)
    combined = ps * D("0.9") + provider_position * D("0.1") if provider_position is not None else ps
    price_band = band(round_half_up(ps))
    combined_band = band(round_half_up(combined))
    saving = max(D(0), current_annual - comparison_annual)
    share = saving / current_annual
    cls, cap = materiality_cap(saving, current_annual)
    exact = min(combined, cap) if cap is not None else combined
    note = provider_position is not None and BAND_ORDER[combined_band] < BAND_ORDER[price_band]
    trace = [
        f"price score = min(100, 20 + 60 x {comparison} / {current}) = {ps}",
        (
            f"service score = {ps} x 0.9 + provider position {provider_position} x 0.1 = {combined}"
            if provider_position is not None
            else f"service score = price score only = {combined}"
        ),
        f"price-only band {price_band}; combined band (pre-cap) {combined_band}; provider note {'YES' if note else 'no'}",
        f"potential annual saving {gbp(saving)}; share {share:.4%}; materiality {cls}"
        + (f" -> capped at {cap}" if cap is not None and combined > cap else ""),
    ]
    return {
        "price_score": ps,
        "price_difference_ratio": (current - comparison) / comparison,
        "provider_position": provider_position,
        "combined_exact": combined,
        "price_only_band": price_band,
        "combined_band": combined_band,
        "provider_note_triggered": note,
        "potential_annual_saving": saving,
        "saving_share": share,
        "materiality": cls,
        "cap_applied": cap if cap is not None and combined > cap else None,
        "exact": exact,
        "display": round_half_up(exact),
        "band": band(round_half_up(exact)),
        "trace": trace,
    }


def floor_eligible(score: dict | None) -> bool:
    if not score:
        return False
    s = score["potential_annual_saving"]
    return D(0) < s < FLOOR_MAX_SAVING


def apply_floor(score: dict) -> dict:
    """small_saving_not_worth_effort (method 2.3). Caller validates the decision."""
    out = dict(score)
    out["floor_applied"] = score["exact"] < FLOOR
    out["exact"] = max(score["exact"], FLOOR)
    out["display"] = round_half_up(out["exact"])
    out["band"] = band(out["display"])
    return out


def provider_note(service_key: str, service_label: str, price_band: str, combined_band: str) -> str:
    return (
        f"Recent public data indicates that your current provider has weaker {PROVIDER_NOTE_AREAS[service_key]} "
        f"results than some others. This lowered your {service_label.lower()} rating from {price_band} to {combined_band}."
    )


def overall(entries: list[dict]) -> dict | None:
    """entries: {unit_id, status, exact (or None), current_annual}."""
    included, excluded, num, den = [], [], D(0), D(0)
    for e in entries:
        w = STATUS_WEIGHT.get(e["status"])
        if e.get("exact") is None or w is None:
            excluded.append({"unit_id": e["unit_id"], "reason": "no numeric score" if w else "not scored status"})
            continue
        weight = e["current_annual"] * w
        num += e["exact"] * weight
        den += weight
        included.append({"unit_id": e["unit_id"], "exact": e["exact"], "weight": weight, "status_weight": w})
    if not included:
        return None
    exact = num / den
    display = round_half_up(exact)
    return {
        "exact": exact,
        "display": display,
        "band": band(display),
        "contributing_services": len(included),
        "included": included,
        "excluded": excluded,
        "trace": [f"overall = sum(score x spend x status weight) / sum(weights) = {num} / {den} = {exact}"],
    }

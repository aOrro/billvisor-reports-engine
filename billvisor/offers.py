"""Broadband/mobile live-case comparison (PHASE_1_OFFER_DATA_METHOD).

Each included offer's first-12-month effective monthly price, the mean per
provider, then the median of the provider means.
"""

from __future__ import annotations

import calendar
import datetime as dt
from decimal import Decimal
from typing import Any

from .errors import Issue, StopError
from .values import dec, gbp, iso_date, nonempty_str

HORIZON = 12
DISPOSITIONS = {"include", "exclude_plainly_not_comparable"}


def period_starts(capture: dt.date) -> list[dt.date]:
    """12 notional billing-period starts from the capture date.

    A month without the capture-date day uses its final day for that period
    only; the next month that has the day returns to it.
    """
    starts = []
    for i in range(HORIZON):
        y, m = divmod(capture.month - 1 + i, 12)
        year, month = capture.year + y, m + 1
        last = calendar.monthrange(year, month)[1]
        starts.append(dt.date(year, month, min(capture.day, last)))
    return starts


def _segment_starts(segs: list[dict], starts: list[dt.date], oid: str) -> list[int]:
    out: list[int] = []
    for i, seg in enumerate(segs):
        where = f"{oid}.recurring_price_periods[{i}]"
        if "effective_date" in seg:
            eff = iso_date(seg["effective_date"], f"{where}.effective_date")
            idx = next((p for p, s in enumerate(starts) if s >= eff), HORIZON)
        elif i == 0:
            idx = 0
        else:
            prev = segs[i - 1]
            if "months" not in prev:
                raise StopError(
                    "INPUT_INVALID",
                    f"{where} follows an open-ended period; give the previous period's months or this period's effective_date",
                    where,
                )
            idx = out[-1] + _months(prev, f"{oid}.recurring_price_periods[{i - 1}]")
        if out and idx < out[-1]:
            raise StopError("INPUT_INVALID", f"{where} starts before the previous price period", where)
        out.append(idx)
    if out and out[0] != 0:
        raise StopError(
            "NO_USABLE_CAPTURED_PRICE", f"{oid}: no price is known for the first billing period", f"{oid}.recurring_price_periods"
        )
    return out


def _months(seg: dict, where: str) -> int:
    m = seg["months"]
    if isinstance(m, bool) or not isinstance(m, int) or m <= 0:
        raise StopError("INPUT_INVALID", f"{where}.months must be a whole number of months", where)
    return m


def first_year(obs: dict) -> dict:
    """Effective monthly price for one included observation."""
    oid = obs["observation_id"]
    capture = iso_date(obs.get("captured_at"), f"{oid}.captured_at")
    starts = period_starts(capture)
    segs = obs["recurring_price_periods"]
    seg_start = _segment_starts(segs, starts, oid)
    prices: list[Decimal] = []
    estimated_periods: list[int] = []
    for p in range(HORIZON):
        k = max(i for i, s in enumerate(seg_start) if s <= p)
        seg = segs[k]
        price = dec(seg.get("price_gbp"), f"{oid}.recurring_price_periods[{k}].price_gbp")
        if "months" in seg and p >= seg_start[k] + _months(seg, f"{oid}.recurring_price_periods[{k}]"):
            if obs.get("unquantified_future_rise") is True:
                estimated_periods.append(p + 1)
            else:
                raise StopError(
                    "NO_USABLE_CAPTURED_PRICE",
                    f"{oid}: no price is captured for billing period {p + 1}. Add the following price, "
                    "or set unquantified_future_rise: true to use the advertised price as the working estimate",
                    f"{oid}.recurring_price_periods",
                )
        prices.append(price)

    one_off = obs.get("compulsory_one_off")
    if not isinstance(one_off, dict) or one_off.get("status") not in ("shown", "not_shown"):
        raise StopError("INPUT_INVALID", f"{oid}.compulsory_one_off must have status shown or not_shown", f"{oid}.compulsory_one_off")
    if one_off["status"] == "shown":
        one_off_amount = dec(one_off.get("amount_gbp"), f"{oid}.compulsory_one_off.amount_gbp")
        one_off_text = f"compulsory one-off {gbp(one_off_amount)}"
    else:
        one_off_amount = Decimal(0)
        one_off_text = "compulsory one-off not shown in capture"

    recurring = sum(prices, Decimal(0))
    total = recurring + one_off_amount
    return {
        "observation_id": oid,
        "provider": obs["provider"].strip(),
        "package_label": obs["package_label"],
        "captured_at": capture.isoformat(),
        "period_prices": prices,
        "recurring_total": recurring,
        "one_off": one_off_amount,
        "one_off_text": one_off_text,
        "first_year_total": total,
        "effective_monthly": total / HORIZON,
        "estimated_periods": estimated_periods,
    }


def _check_observation(obs: Any, i: int, service: str, customer: dict) -> None:
    where = f"observations[{i}]"
    if not isinstance(obs, dict):
        raise StopError("INPUT_INVALID", f"{where} must be an object", where)
    for f in ("observation_id", "provider", "package_label", "source_ref", "captured_at", "comparison_disposition"):
        if not nonempty_str(obs.get(f)):
            raise StopError("INPUT_INVALID", f"{where}.{f} is required", f"{where}.{f}")
    if obs.get("service") != service:
        raise StopError("INPUT_INVALID", f"{obs['observation_id']}: service must be {service}", f"{where}.service")
    if not isinstance(obs.get("package_attributes"), dict):
        raise StopError("INPUT_INVALID", f"{obs['observation_id']}: package_attributes is required", f"{where}.package_attributes")
    disp = obs["comparison_disposition"]
    if disp not in DISPOSITIONS:
        raise StopError(
            "COMPARABILITY_RULE_AMBIGUOUS",
            f"{obs['observation_id']}: disposition {disp!r} is neither include nor exclude_plainly_not_comparable",
            f"{where}.comparison_disposition",
        )
    if disp == "exclude_plainly_not_comparable" and not nonempty_str(obs.get("exclusion_reason")):
        raise StopError("INPUT_INVALID", f"{obs['observation_id']}: exclusion_reason is required", f"{where}.exclusion_reason")
    if disp == "include" and service == "mobile":
        handset = obs["package_attributes"].get("handset_included")
        if not isinstance(handset, bool):
            raise StopError(
                "INPUT_INVALID",
                f"{obs['observation_id']}: package_attributes.handset_included (true/false) is required for mobile",
                f"{where}.package_attributes.handset_included",
            )
        if handset != customer.get("handset_included"):
            raise StopError(
                "INPUT_INVALID",
                f"{obs['observation_id']}: handset status differs from the customer's plan; a handset-inclusive price "
                "must not be compared with SIM-only. Mark it exclude_plainly_not_comparable",
                f"{where}.package_attributes.handset_included",
            )


def comparison(service: str, observations: list, customer: dict) -> dict:
    """Median of provider means. Raises StopError when no comparison is possible."""
    if not isinstance(observations, list) or not observations:
        raise StopError("NO_USABLE_CAPTURED_PRICE", "no market observations captured", "observations")
    ids = [o.get("observation_id") for o in observations if isinstance(o, dict)]
    if len(ids) != len(set(ids)):
        raise StopError("INPUT_INVALID", "observation_id values must be unique", "observations")

    offers, excluded, trace = [], [], []
    for i, obs in enumerate(observations):
        _check_observation(obs, i, service, customer)
        oid = obs["observation_id"]
        if obs["comparison_disposition"] == "exclude_plainly_not_comparable":
            excluded.append({"observation_id": oid, "provider": obs["provider"], "reason": obs["exclusion_reason"]})
            continue
        if not obs.get("recurring_price_periods"):
            excluded.append({"observation_id": oid, "provider": obs["provider"], "reason": "no usable price"})
            continue
        offers.append(first_year(obs))

    if not offers:
        raise StopError("NO_USABLE_CAPTURED_PRICE", "no included observation has a usable price", "observations")

    by_provider: dict[str, list[Decimal]] = {}
    for o in offers:
        by_provider.setdefault(o["provider"], []).append(o["effective_monthly"])
    means = sorted(
        ({"provider": p, "offer_count": len(v), "mean": sum(v, Decimal(0)) / len(v)} for p, v in by_provider.items()),
        key=lambda r: (r["mean"], r["provider"]),
    )
    n = len(means)
    if n % 2:
        monthly = means[n // 2]["mean"]
        median_text = f"middle of {n} provider means = {gbp(monthly)}"
    else:
        a, b = means[n // 2 - 1]["mean"], means[n // 2]["mean"]
        monthly = (a + b) / 2
        median_text = f"mean of central provider means ({gbp(a)} + {gbp(b)}) / 2 = {gbp(monthly)}"

    for o in offers:
        est = f"; advertised price used as estimate for periods {o['estimated_periods']}" if o["estimated_periods"] else ""
        trace.append(
            f"offer {o['observation_id']} {o['provider']} '{o['package_label']}' captured {o['captured_at']}: "
            f"recurring {gbp(o['recurring_total'])} + {o['one_off_text']} = {gbp(o['first_year_total'])} / 12 = "
            f"{gbp(o['effective_monthly'])}/month{est}"
        )
    for e in excluded:
        trace.append(f"excluded {e['observation_id']} {e['provider']}: {e['reason']}")
    for m in means:
        trace.append(f"provider mean {m['provider']} ({m['offer_count']} offer(s)) = {gbp(m['mean'])}")
    trace.append(f"comparison: {median_text}; annual = {gbp(monthly * 12)}")

    estimation_flags = [
        {"observation_id": o["observation_id"], "provider": o["provider"], "estimated_periods": o["estimated_periods"]}
        for o in offers
        if o["estimated_periods"]
    ]
    return {
        "offers": [{k: v for k, v in o.items() if k != "period_prices"} for o in offers],
        "excluded": excluded,
        "provider_means": means,
        "monthly_comparison": monthly,
        "annual_comparison": monthly * 12,
        "provider_count": n,
        "offer_count": len(offers),
        "estimation_flags": estimation_flags,
        "trace": trace,
    }


__all__ = ["comparison", "first_year", "period_starts", "Issue"]

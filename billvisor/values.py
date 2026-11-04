"""Strict value parsing and display rounding."""

from __future__ import annotations

import datetime as dt
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from typing import Any

from .errors import StopError

ONE = Decimal(1)


def dec(value: Any, field: str, code: str = "INPUT_INVALID", positive: bool = False) -> Decimal:
    """Parse an exact number. Floats are refused because they are not exact."""
    if isinstance(value, bool) or value is None or isinstance(value, float):
        raise StopError(code, f"{field} must be an exact number", field)
    try:
        d = Decimal(str(value).strip().replace(",", "")) if isinstance(value, str) else Decimal(value)
    except (InvalidOperation, ValueError):
        raise StopError(code, f"{field} is not a number: {value!r}", field) from None
    if not d.is_finite():
        raise StopError(code, f"{field} is not a finite number", field)
    if positive and d <= 0:
        raise StopError(code, f"{field} must be greater than zero", field)
    if d < 0:
        raise StopError(code, f"{field} must not be negative", field)
    return d


def iso_date(value: Any, field: str, code: str = "INPUT_INVALID") -> dt.date:
    if isinstance(value, str):
        try:
            return dt.date.fromisoformat(value.strip()[:10])
        except ValueError:
            pass
    raise StopError(code, f"{field} must be an ISO date (YYYY-MM-DD): {value!r}", field)


def is_iso_date(value: Any) -> bool:
    try:
        iso_date(value, "x")
        return True
    except StopError:
        return False


def round_half_up(d: Decimal | int) -> int:
    if isinstance(d, bool) or not isinstance(d, (Decimal, int)):
        raise TypeError(f"round_half_up needs a Decimal or int, not {type(d).__name__}")
    return int(Decimal(d).quantize(ONE, rounding=ROUND_HALF_UP))


def gbp(d: Decimal) -> str:
    """Exact pounds for internal trace lines."""
    return f"£{d:,.4f}"


def gbp_whole(n: int) -> str:
    return f"£{n:,}"


def long_date(d: dt.date) -> str:
    return f"{d.day} {d.strftime('%B %Y')}"


def nonempty_str(value: Any) -> bool:
    return isinstance(value, str) and value.strip() != ""

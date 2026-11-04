"""Tie-safe provider position (BILLS_HEALTH_SCORE_METHOD section 3)."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

from . import jsonio
from .errors import StopError
from .values import dec, nonempty_str

TABLE_DIR = Path(__file__).resolve().parent.parent / "reference" / "provider_tables"


def load_table(table_ref: str, table_dir: Path | None = None) -> dict:
    if not nonempty_str(table_ref) or "/" in table_ref or ".." in table_ref:
        raise StopError("INPUT_INVALID", f"invalid provider table_ref {table_ref!r}", "provider_table.table_ref")
    path = (table_dir or TABLE_DIR) / f"{table_ref}.json"
    if not path.exists():
        raise StopError("METHOD_OR_SOURCE_RULE_MISSING", f"provider table {table_ref!r} not found", "provider_table.table_ref")
    table = jsonio.load(path)
    for f in ("table_ref", "service", "table_version", "table_date", "rows"):
        if f not in table or table[f] in (None, ""):
            raise StopError("METHOD_OR_SOURCE_RULE_MISSING", f"provider table {table_ref} lacks {f}", "provider_table")
    return table


def ranks(rows: list[dict]) -> dict[str, Decimal]:
    """Average ordinal rank per provider, highest raw score = rank 1."""
    scored = sorted(((r["provider"], dec(r["overall"], f"{r['provider']}.overall")) for r in rows), key=lambda x: -x[1])
    out: dict[str, Decimal] = {}
    i = 0
    while i < len(scored):
        j = i
        while j + 1 < len(scored) and scored[j + 1][1] == scored[i][1]:
            j += 1
        avg = Decimal(i + 1 + j + 1) / 2
        for k in range(i, j + 1):
            out[scored[k][0]] = avg
        i = j + 1
    return out


def position(table: dict, provider_id: str) -> dict:
    """Return the position block, or raise NEW_PROVIDER_ASSESSMENT_REQUIRED."""
    rows = table["rows"]
    names = [r["provider"] for r in rows]
    if len(names) != len(set(names)):
        raise StopError("MATERIAL_EVIDENCE_CONFLICT", f"duplicate providers in {table['table_ref']}", "provider_table")
    if provider_id not in names:
        raise StopError(
            "NEW_PROVIDER_ASSESSMENT_REQUIRED",
            f"{provider_id!r} is not in {table['table_ref']} {table['table_version']} (exact match required)",
            "provider_table.provider_id",
        )
    distinct = {dec(r["overall"], "overall") for r in rows}
    if len(distinct) < 2:
        raise StopError(
            "METHOD_OR_SOURCE_RULE_MISSING", f"{table['table_ref']} has fewer than two distinct scores", "provider_table"
        )
    r = ranks(rows)
    best, worst = min(r.values()), max(r.values())
    rank = r[provider_id]
    pos = Decimal(100) * (worst - rank) / (worst - best)
    raw = next(dec(x["overall"], "overall") for x in rows if x["provider"] == provider_id)
    return {
        "table_ref": table["table_ref"],
        "table_version": table["table_version"],
        "table_date": table["table_date"],
        "provider_id": provider_id,
        "raw_score": raw,
        "rank": rank,
        "best_rank": best,
        "worst_rank": worst,
        "position": pos,
        "sources_publicly_accessible": table.get("sources_publicly_accessible"),
    }

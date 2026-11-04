"""Risk-based Review triggers (CASE_OPERATING_METHOD section 3).

The ledger lives in the cases directory and records every build and every
Review result, so triggers are computed from history rather than memory.

Interpretation (documented in README):
- first five: fewer than five other reports have been built.
- defect reset: after a Critical/Major result, Review is required until five
  later reviewed reports pass (pass or minor).
- spot check: once neither of the above applies, a report is reviewed when
  four reports in a row since the last reviewed one went unreviewed (1 in 5).
"""

from __future__ import annotations

import datetime as dt
from pathlib import Path

from . import jsonio

RESULTS = ("pass", "minor", "major", "critical")
CLEAN = ("pass", "minor")
LEDGER_NAME = "_review_ledger.json"


def ledger_path(cases_dir: Path) -> Path:
    return Path(cases_dir) / LEDGER_NAME


def load(cases_dir: Path) -> dict:
    p = ledger_path(cases_dir)
    return jsonio.load(p) if p.exists() else {"events": []}


def append(cases_dir: Path, event: dict) -> None:
    led = load(cases_dir)
    event = dict(event, at=dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"))
    led["events"].append(event)
    jsonio.dump(led, ledger_path(cases_dir))


def triggers(ledger: dict, report_id: str, flags: dict) -> list[str]:
    events = ledger.get("events", [])
    builds: dict[str, bool] = {}  # report_id -> reviewed (first build order kept by dict)
    reviewed_ids = {e["report_id"] for e in events if e["type"] == "review" and e["result"] in RESULTS}
    for e in events:
        if e["type"] == "build" and e["report_id"] != report_id:
            builds.setdefault(e["report_id"], False)
    for rid in builds:
        builds[rid] = rid in reviewed_ids

    reasons = []
    if len(builds) < 5:
        reasons.append("first_five_reports")

    reviews = [e for e in events if e["type"] == "review" and e["report_id"] != report_id]
    last_defect = max((i for i, e in enumerate(reviews) if e["result"] in ("major", "critical")), default=None)
    if last_defect is not None:
        clean_after = {e["report_id"] for e in reviews[last_defect + 1:] if e["result"] in CLEAN}
        if len(clean_after) < 5:
            reasons.append("defect_reset_until_five_clean")

    if flags.get("calculator_failure_or_override"):
        reasons.append("calculator_failure_or_manual_override")
    if flags.get("primary_look_at_changing_now"):
        reasons.append("primary_look_at_changing_now")

    if not reasons:
        unreviewed_run = 0
        for rid, was_reviewed in builds.items():
            unreviewed_run = 0 if was_reviewed else unreviewed_run + 1
        if unreviewed_run >= 4:
            reasons.append("one_in_five_spot_check")
    return reasons

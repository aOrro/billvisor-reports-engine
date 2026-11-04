"""Customer-facing leakage checks (CASE_OPERATING_METHOD step 5, MEMORY report rules)."""

from __future__ import annotations

import re

BANNED_PHRASES = [
    (r"\bbenchmark", "internal word 'benchmark'"),
    (r"\bguarantee", "guaranteed-saving claim"),
    (r"\bbest[- ]deal", "best-deal claim"),
    (r"\bwhole[- ]market\b", "whole-market claim"),
    (r"\bcheapest\b", "cheapest/best-deal claim"),
    (r"\breviews?\b", "evidence must not be called reviews"),
    (r"£\s*0+(?:\.0+)?(?![\d.])", "£0 figure"),
    (r"\bsav\w*\s+(?:of\s+)?about\s+£", "'about' must not prefix the potential saving"),
    (r"\babout\s+£[\d,]+\s+(?:a year\s+)?(?:in\s+)?sav", "'about' must not prefix the potential saving"),
]
SOURCE_NAMES = ["Ofcom", "Ofgem", "Which?", "Uswitch", "MoneySavingExpert", "Money Saving Expert", "Citizens Advice",
                "Energy Ombudsman", "Opensignal", "RootMetrics", "umlaut", "thinkbroadband", "ISPreview", "Trustpilot",
                "Compare the Market", "GoCompare", "Go.Compare", "Confused.com"]
BLAME_PHRASES = [r"\byou (?:did not|didn't|have not|haven't|failed to) (?:provide|send|give|supply)",
                 r"\bnot enough information\b", r"\binsufficient information\b"]


def check_text(text: str, *, forbidden_providers: set[str], allow_customer_gap: bool) -> list[str]:
    problems = []
    for pat, why in BANNED_PHRASES:
        if re.search(pat, text, re.IGNORECASE):
            problems.append(why)
    for name in SOURCE_NAMES:
        if re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", text, re.IGNORECASE):
            problems.append(f"source name '{name}' is internal")
    for name in sorted(forbidden_providers):
        # Case-sensitive so ordinary words ("three months") do not trip it.
        if re.search(r"(?<!\w)" + re.escape(name) + r"(?!\w)", text):
            problems.append(f"comparison provider '{name}' is internal (no specific deals)")
    if not allow_customer_gap:
        for pat in BLAME_PHRASES:
            if re.search(pat, text, re.IGNORECASE):
                problems.append("wording implies the customer supplied too little information")
    return problems

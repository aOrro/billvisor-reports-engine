"""Structured stop and escalation codes (LIVE_CASE_CALCULATOR_SPEC section 5).

The engine never substitutes a value silently. Every problem becomes an Issue
with a code, a plain message and the next action the founder or Operations
should take.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

# code -> (blocks the affected unit?, next action)
CODES: dict[str, tuple[bool, str]] = {
    "MINIMUM_FIELD_MISSING": (
        True,
        "Ask the customer once (one consolidated clarification) or record proceed_as: confirm_information.",
    ),
    "MINIMUM_FIELD_AMBIGUOUS": (
        True,
        "Do not guess. Clarify with the customer or record proceed_as: confirm_information.",
    ),
    "NO_USABLE_CAPTURED_PRICE": (
        True,
        "Ask the founder for a usable capture. Escalate to Evidence only if the source/method rule itself is unclear.",
    ),
    "COMPARABILITY_RULE_AMBIGUOUS": (True, "Stop. Evidence resolves the missing/ambiguous comparability rule."),
    "NEW_PROVIDER_ASSESSMENT_REQUIRED": (
        False,
        "Evidence assesses the provider. Until then the price-only score applies (Analysed with limitations).",
    ),
    "METHOD_OR_SOURCE_RULE_MISSING": (True, "Stop. Evidence resolves the bounded rule/source question."),
    "MATERIAL_EVIDENCE_CONFLICT": (True, "Stop. Evidence resolves the conflict."),
    "CALCULATOR_CANNOT_SAFELY_PROCESS": (True, "Stop. Send the bounded unsupported case to Evidence."),
    "SPECIALIST_ENERGY_USAGE_REQUIRED": (
        True,
        "Bedroom fallback blocked. Request suitable usage from the customer (if permitted) or record proceed_as: confirm_information.",
    ),
    "ENERGY_SCORE_COMPARISON_UNAPPROVED": (
        False,
        "Annual costs are available but there is no Energy score. Select an approved score comparison only if one is supportable.",
    ),
    "REQUESTED_SERVICE_UNSUPPORTED": (True, "Founder/CEO must resolve report treatment for an unsupported service."),
    "REQUESTED_GEOGRAPHY_UNSUPPORTED": (True, "Founder/CEO must resolve report treatment for an unsupported geography."),
    "REPORT_TREATMENT_POLICY_UNRESOLVED": (
        True,
        "No coverage or report content can be generated for this service until the policy is resolved.",
    ),
    # Engine data-entry errors (not customer-information gaps).
    "INPUT_INVALID": (True, "Correct the case file entry named in the message."),
    "UNIT_REQUESTED_UNSET": (True, "Set requested: true or false for this service."),
}

# Stop codes that represent a customer-information gap. Only these may be
# carried into the report as Confirm information (founder decision 2026-11-04).
CUSTOMER_INFO_CODES = {"MINIMUM_FIELD_MISSING", "MINIMUM_FIELD_AMBIGUOUS", "SPECIALIST_ENERGY_USAGE_REQUIRED"}


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    field: str | None = None

    @property
    def blocking(self) -> bool:
        return CODES[self.code][0]

    @property
    def next_action(self) -> str:
        return CODES[self.code][1]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["blocking"] = self.blocking
        d["next_action"] = self.next_action
        return d


class StopError(Exception):
    """Raised inside a calculation to stop the affected unit."""

    def __init__(self, code: str, message: str, field: str | None = None):
        super().__init__(f"{code}: {message}")
        self.issue = Issue(code, message, field)


class GateError(Exception):
    """Raised by approve/build when a gate fails. Message includes the next action."""

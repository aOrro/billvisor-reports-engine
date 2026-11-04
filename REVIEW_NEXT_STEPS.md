# Review: next steps before the report engine is ready for operational use

## Review outcome

The engine is a sound calculation and approval core. Its test suite currently passes (52 tests; one regression suite skipped). It should **not yet be treated as the finished report-generation workflow**, because it stops at `report_data.json` and has not been connected to the approved HTML report template.

This document records the smallest next implementation phase. It is not a request to redesign the scoring, report, or customer journey.

## 1. Render the approved HTML report

**Current state:** `build` writes `report_data.v<N>.json`; the README explicitly says HTML generation is out of scope.

**Required change:** make the build flow produce a finished, local HTML report from the current approved Billvisor visual template after all calculation, founder-approval and Review gates pass.

**Constraints:**

- Do not create a PDF renderer. The founder continues to inspect the HTML and save it as PDF manually.
- Do not change the approved visual design while wiring data into it.
- The renderer reads only the approved `report_data` output, never the raw case file or market observations.
- HTML generation must remain blocked when any fingerprint/approval/Review gate fails.

**Acceptance:** an ordinary fixture can run `new → calc → pack → approve → review (when required) → build` and produces a complete local report HTML file that matches the approved design and conditional pages.

## 2. Expand the renderer-safe report data

**Current state:** `report_data.json` contains annual figures, score and decision text but does not include enough approved current-service display data for the report pages.

**Required change:** add a deliberately small customer-facing `current_service` object per service page, populated from structured facts only. It must cover the approved template fields where applicable:

- Broadband: provider, download speed, monthly cost and contract status/end date.
- Mobile: provider, data allowance, relevant extras/handset status, monthly cost and contract status/end date.
- Energy: supplier, fuel(s), tariff type/name, payment method and tariff status/end date.

**Constraints:**

- Do not expose captured alternative providers, individual offers, provider means, sources, internal methodology or raw arithmetic.
- A renderer must never need to read `case.json` for customer-visible content.
- Keep exact internal calculation data in the existing internal trace/case structure.

**Acceptance:** the completed HTML can reproduce all existing “Your current service” sections using only `report_data`.

## 3. Resolve the score-label wording conflict

**Current state:** the engine writes `score.estimated: true`, and the report-data contract says a true value should display an “Estimated” score label. The latest founder direction was not to show the word “estimated” beside a score; estimates/limitations should be explained in the relevant service-page narrative instead.

**Required change:** preserve the internal flag for traceability, but do not make the score label customer-facing by default. Surface the relevant limitation or energy-consumption estimate in the approved explanation/estimate-note location.

**Acceptance:** a limited comparison can retain its internal flag and correct coverage status without rendering “Estimated score” next to the gauge or rating.

## 4. Add anonymised regression fixtures

**Current state:** the regression suite is skipped because `tests/regression/` has no supplied cases.

**Required change:** add at least two fully anonymised, non-identifiable fixtures representing the already approved report patterns:

1. A mixed-service case with a useful mobile/broadband action and energy estimate.
2. A predominantly good-position case where a small mobile saving does not justify the effort and the score floor is applied only with explicit founder approval.

Each fixture needs a case input and expected report-data assertions. Do not use real customer names, postcodes, email addresses, account numbers, documents, screenshots or source captures.

**Acceptance:** the regression suite no longer skips and alerts us if future edits change key scores, statuses, conditional pages, action ordering or customer-visible fields.

## 5. Verify the end-to-end route against the approved layout

Once items 1–4 are complete:

- Run one new synthetic case through the complete workflow.
- Visually compare the resulting HTML with the current approved Billvisor report layout.
- Check combined Energy appears once in the overview; not-analysed services have no service page; priority actions sort by founder priority then saving; gauges match output scores; and required report-wide/source wording is present.
- Record only any genuine layout/data-mapping defects. Do not start a visual redesign.

## Out of scope for this phase

- Automated web search or comparison-site access.
- Automated recommendation selection.
- Sending customer emails.
- Switching services or presenting specific offers/deals in reports.
- Automated PDF generation/export.
- Altering Phase 1 scoring policy, provider methodology or recommendation thresholds.


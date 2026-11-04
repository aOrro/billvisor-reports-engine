# Review: next steps before the report engine is ready for operational use

## Review outcome

The engine is a sound calculation and approval core. Its test suite currently passes (52 tests; one regression suite skipped). It should **not yet be treated as the finished report-generation workflow**, because it stops at `report_data.json` and has not been connected to the approved HTML report template.

This document records the smallest next implementation phase. It is not a request to redesign the scoring, report, or customer journey.

## Founder decisions recorded — 4 November 2026

The founder approved the following resolutions:

1. **HTML:** the engine will generate the completed approved-report HTML after all gates pass. It will not generate PDFs or delivery emails. Vendor the currently approved report template and assets from `/Users/anton/billvisor/design/report/` into a clearly labelled repository template folder before wiring it.
2. **Current-service section:** include the household's own submitted current-service details in renderer-safe report data. Every displayed field must appear in the founder approval pack. Mobile extras must be founder-approved wording, never an automatic raw copy.
3. **Score labels:** preserve a qualified/estimated-comparison indicator internally, but do not show the word “Estimated” beside a customer-facing score or gauge. Explain the material estimate or limitation in the relevant service-page narrative.

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


## Contradictions with the governing documents

Checked on 4 November 2026 against every document in `docs/governing/`. Line numbers refer to those copies.

| Item | Result |
|---|---|
| 1. Render HTML | Founder approved; update this repo's scope ruling as part of implementation. |
| 2. Current-service data | Founder approved; clarified in MEMORY.md. |
| 3. Score label | Founder approved; source documents and their governing copies were updated. |
| 4. Regression fixtures | No contradiction. |
| 5. End-to-end check | No contradiction. |

### Item 3 — resolved

The founder confirmed that a qualified/estimated-comparison flag remains internal and is not a customer-facing score label. The relevant source documents and their governing copies now record this decision. The old wording below identified the issue before the decision was recorded:

- `BILLS_HEALTH_SCORE_METHOD.md:46`: "the score must be labelled **Estimated**".
- `BILLS_HEALTH_SCORE_METHOD.md:195-196`: the validation examples show "45 — Medium, Estimated" and "75 — Good, Estimated".
- `LIVE_CASE_CALCULATOR_SPEC.md:102` and `:207`: "a clearly labelled **Estimated score**". The worked example at `:264` shows "75 Good Estimated".
- `MEMORY.md:36`: "may produce a clearly labelled **Estimated score**".

The internal flag is separate from the bedroom-fallback energy explanation. The energy customer narrative still explains estimated usage while the coverage remains Analysed where the agreed minimum information was supplied.

### Item 1 — resolved

The governing documents already require HTML generation. `PHASE_1_CASE_OPERATING_METHOD.md` §4 (`:143-152`) lists:

- a fixed-A4 HTML report;
- conditional service pages;
- one Energy row;
- score arcs and colours;
- priority-action ordering;
- refusal when a fingerprint or gate is missing or stale.

The conflict is with this repo's own records:

- `docs/governing/README.md:35`, ruling 4: "HTML rendering [is] out of scope for this build."
- `README.md:6`: the engine "does **not** … generate HTML".

The founder approved HTML generation, but not PDF or delivery-email generation. Update both scope statements in the same implementation change.

The design source is `/Users/anton/billvisor/design/report/`; vendor the approved template/assets into the repository as part of the implementation. The renderer covers report page numbering, case reference and report version; delivery email remains outside this engine.

Item 1's rule that the renderer reads only `report_data` is not a conflict with `:147`, which says "from the approved case JSON". `report_data` is built only from the approved and fingerprinted case JSON.

### Item 2 — resolved

The founder approved the design's current-service section and MEMORY.md now states its boundary. Two governing rules apply to it:

- **Founder approval.** `PHASE_1_CASE_OPERATING_METHOD.md:118` and `:124` require every customer-facing field to appear in the approval package. Any change to a field invalidates the approval. So `current_service` must appear in the approval pack and be covered by the approval fingerprints.
- **Mobile extras.** `LIVE_CASE_CALCULATOR_SPEC.md:59` defines `handset_or_important_extras` as the customer's own description. It should reach the report only as founder-approved wording that has passed the leakage check, not as a direct copy.

### No contradiction: items 4 and 5

- **Item 4.** `LIVE_CASE_CALCULATOR_SPEC.md:275` requires synthetic checks before live use. Work out each fixture's expected values by hand using the score method, or take them from the approved reports. Values captured from the engine's own output would detect only future changes, not errors. Name fixture folders with a neutral reference, never a customer name.
- **Item 5.** The checks listed match `PHASE_1_CASE_OPERATING_METHOD.md` §4.

### Known conflicts that are already resolved

The bedroom fallback is still described as "Analysed with limitations" in two places:

- `PHASE_1_OFFER_DATA_METHOD.md:350`;
- the worked example at `LIVE_CASE_CALCULATOR_SPEC.md:258-265`.

These are not new. Founder ruling 1 in `docs/governing/README.md` overrides them: Analysed, weight 1.0. The source documents should be corrected the next time they are refreshed.

## Open follow-ups from the review of 584bece

Checked on 4 November 2026. Fix items 1 and 2 in the `context-files/` source documents first, then recopy them into `docs/governing/` unchanged.

1. **Missed worked example.** `BILLS_HEALTH_SCORE_METHOD.md:196` still says "the price-only result is **75 — Good, Estimated**". The mobile example on line 195 was updated but this energy example was not. Reword it to match the new rule: no customer-facing "Estimated" label, and the qualified-comparison status kept internally.
2. **Old term in the trace list.** `BILLS_HEALTH_SCORE_METHOD.md:210` still says "whether the score is Estimated and the exact customer-facing limitation". This is internal only, but it should use the new term, for example "whether the score is qualified (internal flag) and the exact customer-facing limitation".
3. **Source date missing.** `docs/governing/README.md` requires the commit message for a refreshed copy to record the source date. Commit 584bece has no message body. In the fix-up commit, give the date the `context-files/` sources were changed, and confirm the sources themselves carry the decision, not only the copies here.

**Engine side (after items 1–3 land).** These still describe the old rule and will be updated on this branch:

- `docs/REPORT_DATA_CONTRACT.md:40` tells the renderer to label the score "Estimated".
- `billvisor/pack.py:92` tells the founder the score will be "labelled Estimated".
- `README.md:56` and `:84` say "Estimated score".

The internal flag stays; it is not shown to customers.

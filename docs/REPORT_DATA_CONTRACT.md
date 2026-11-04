# report_data.json contract (v1.0)

`build` writes `<cases-dir>/<REPORT_ID>/report_data.v<N>.json`. It is the only file a renderer
(the existing `generate_report.py` or a later step) should read. It holds approved,
customer-facing values only. Internal values (offers, provider means, rates, sources and exact arithmetic)
stay in `case.json` (`calculation_output`) and `trace.txt`.

> **Still to reconcile:** the existing `generate_report.py` was not available when this was written.
> Map these fields onto its current inputs before wiring rendering.

## Top level

| Field | Meaning |
|---|---|
| `contract_version` | `"1.0"` |
| `report` | `report_id`, `first_name`, `report_version`, `approved_at` |
| `overall` | `null` when no service has a numeric score. Otherwise `value` (0–100, half-up), `band` (Poor/Medium/Good), `colour` (red/amber/green), `contributing_services` (the report must state this count) |
| `overview[]` | One row per analysis unit in fixed order (Broadband, Mobile, Energy, or Electricity/Gas when analysed separately). Combined gas+electricity is one `Energy` row. Fields: `unit_id`, `label`, `coverage_status`, `score` (or null), `page` (false for Not analysed) |
| `service_pages[]` | Only Analysed and Analysed-with-limitations units, in overview order. See below |
| `priority_actions[]` | Sorted by founder `priority`, then larger `potential_saving_gbp` first. Fields: `unit_id`, `label`, `priority`, `action_type`, `next_step`, `potential_saving_gbp` |
| `summary` | Optional approved report-level text, or null |
| `report_notes[]` | Always contains `"Supporting source details are available on request."` once |
| `fingerprints` | `inputs_fp`, `calc_fp`, `decision_fp`, `content_fp` of the approved snapshot |
| `gate` | `{type: "review" \| "deterministic_validation", reasons[], result}` |
| `engine_version` | Calculator version |

Page numbers are owned by the template, which knows its fixed pages. Service pages come in array order.

## service_pages[]

| Field | Meaning |
|---|---|
| `unit_id`, `label`, `coverage_status` | |
| `limitation` | One plain-English limitation for Analysed with limitations, otherwise null |
| `estimate_note` | Energy only, when bedroom-based consumption was used: "Your consumption was estimated from households with similar characteristics." The status stays Analysed |
| `current_annual_spend_gbp` | Whole pounds. Broadband/mobile: monthly payment × 12. Energy: the estimated annual cost of the current tariff. Null for a Confirm-information page |
| `current_annual_spend_basis` | `monthly_payment_x12` or `estimated_annual_cost`, so the template can choose "what you pay each year" or "estimated annual cost" |
| `comparison_annual_gbp`, `comparison_text` | Broadband/mobile only: "Similar services cost about £X a year." Energy shows no market comparison |
| `potential_saving_gbp` | A positive whole-pound saving only when the founder chose to show it. Never 0. Do not prefix it with "about" |
| `score` | `{value, band, colour}` or null. The qualified-comparison flag is deliberately not included: it stays in `calculation_output` and `trace.txt`. Never label the score or gauge “Estimated”; the approved `limitation` or `estimate_note` explains any estimate. |
| `provider_note` | The fixed provider-quality sentence when the band dropped, otherwise null |
| `action_type` | Internal type: do not print it as a label. Customer wording is `next_step` |
| `effort` | Internal (Low/Moderate/High), not a time promise |
| `headline`, `explanation`, `next_step` | Founder-approved wording |
| `findings[]` | Founder-selected fact-based findings `{id, text}` |

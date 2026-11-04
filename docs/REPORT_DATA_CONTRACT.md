# report_data.json contract (v1.1)

`build` writes `<cases-dir>/<REPORT_ID>/report_data.v<N>.json`. It is the only file a renderer
(the existing `generate_report.py` or a later step) should read. It holds approved,
customer-facing values only. Internal values (offers, provider means, rates, sources and exact arithmetic)
stay in `case.json` (`calculation_output`) and `trace.txt`.

> **Still to reconcile:** the existing `generate_report.py` was not available when this was written.
> Map these fields onto its current inputs before wiring rendering.

## Top level

| Field | Meaning |
|---|---|
| `contract_version` | `"1.1"`. v1.1 removed `score.estimated` and added `current_service`, `totals`, effort on actions and the two-field Review gate |
| `report` | `report_id`, `first_name`, `report_version`, `approved_at` |
| `overall` | `null` when no service has a numeric score. Otherwise `value` (0–100, half-up), `band` (Poor/Medium/Good), `colour` (red/amber/green), `contributing_services` (the report must state this count) |
| `overview[]` | One row per analysis unit in fixed order (Broadband, Mobile, Energy, or Electricity/Gas when analysed separately). Combined gas+electricity is one `Energy` row. Fields: `unit_id`, `label`, `coverage_status`, `score` (or null), `page` (false for Not analysed) |
| `service_pages[]` | Only Analysed and Analysed-with-limitations units, in overview order. See below |
| `priority_actions[]` | Sorted by founder `priority`, then larger `potential_saving_gbp` first. Fields: `unit_id`, `label`, `priority`, `action_type`, `effort`, `next_step`, `potential_saving_gbp` |
| `totals` | Renderer contract §3, summed from the displayed whole-pound page figures so they reconcile: `annual_spend_gbp` (pages with a spend figure; null if none), `potential_savings_gbp` (founder-shown savings only; null rather than £0), `services_reviewed` (pages), `priority_actions` (actions other than Stay put) |
| `summary` | Optional approved report-level text, or null |
| `report_notes[]` | Always contains `"Supporting source details are available on request."` once |
| `fingerprints` | `inputs_fp`, `calc_fp`, `decision_fp`, `content_fp` of the approved snapshot |
| `gate` | `{type: "review", reasons[], outcome, highest_severity}` using the REPORT_OUTPUT_QA.md vocabulary, or `{type: "deterministic_validation", reasons: [], outcome: "pass"}` |
| `engine_version` | Calculator version |

Page numbers are owned by the template, which knows its fixed pages. Service pages come in array order.

## service_pages[]

| Field | Meaning |
|---|---|
| `unit_id`, `label`, `coverage_status` | |
| `current_service` | The household's own submitted details (renderer contract §4), copied from the case facts and fixed by the inputs fingerprint. Broadband: `provider`, `download_speed_mbps`, `monthly_cost_gbp`, `contract_end`. Mobile: `provider`, `data_allowance_gb`, `data_allowance_unlimited`, `plan_type` (`sim_only` / `handset_included`), `monthly_cost_gbp`, `contract_end`. Energy: `supplier`, `services` (`both` / `gas` / `electricity`), `tariff`, `monthly_payment_gbp`, `tariff_end`. Dates are ISO and renderer display wording is defined in the renderer contract. `monthly_payment_gbp` comes only from Operations' optional normalised `approximate_monthly_payment_gbp` fact when the supplied monthly amount was unambiguous; otherwise it is null. Missing facts are null. |
| `limitation` | One plain-English limitation for Analysed with limitations, otherwise null |
| `estimate_note` | Energy only, when bedroom-based consumption was used: "Your consumption was estimated from households with similar characteristics." The status stays Analysed |
| `current_annual_spend_gbp` | Whole pounds. Broadband/mobile: monthly payment × 12. Energy: the estimated annual cost of the current tariff. Null for a Confirm-information page |
| `current_annual_spend_basis` | `monthly_payment_x12` or `estimated_annual_cost`, so the template can choose "what you pay each year" or "estimated annual cost" |
| `comparison_annual_gbp`, `comparison_text` | Broadband/mobile only: "Similar services cost about £X a year." Energy shows no market comparison |
| `potential_saving_gbp` | A positive whole-pound saving only when the founder chose to show it. Never 0. Do not prefix it with "about" |
| `score` | `{value, band, colour}` or null. The qualified-comparison flag is deliberately not included: it stays in `calculation_output` and `trace.txt`. Never label the score or gauge “Estimated”; the approved `limitation` or `estimate_note` explains any estimate. |
| `provider_note` | The fixed provider-quality sentence when the band dropped, otherwise null |
| `action_type` | Internal type: do not print it as a label. Customer wording is `next_step` |
| `effort` | Founder-selected Low/Moderate/High. The renderer shows it as "Effort: Low/Moderate/High" (renderer contract §6), never as a time |
| `headline`, `explanation`, `next_step` | Founder-approved wording |
| `findings[]` | Founder-selected fact-based findings `{id, text}` |

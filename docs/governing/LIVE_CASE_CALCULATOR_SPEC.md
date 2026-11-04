# Live Case Calculator Specification

## Status and boundary

- **Owner:** Operations.
- **Status:** Implemented for the ordinary-case preparation path and updated on 4 November 2026 for the revised score curve, materiality caps and qualified-score route.
- **Purpose:** define the smallest deterministic calculation layer for ordinary broadband, mobile and Great Britain energy cases under D-018.
- **Authorities:** CEO `MEMORY.md`, D-018, `BILLS_HEALTH_SCORE_METHOD.md` and Evidence's `PHASE_1_OFFER_DATA_METHOD.md`.
- **Not in scope:** a database, user interface, report generator, recommendation algorithm, source methodology or provider-scoring method.

The calculator processes approved inputs and returns calculations. It does not research, judge the recommendation, choose a green/amber outcome, decide whether a saving is useful, or create customer wording.

## One case record, not a parallel record

Implementation should extend each `analysis_units[]` item in the existing Operations case JSON with:

- `calculation_input`: machine-readable customer facts, captures and table references;
- `calculation_output`: deterministic results, trace and errors.

The existing display-oriented `household_facts` and `evidence` fields should later be derived from these fields where possible, not maintained as a second independent source. Existing `decision`, `report`, `delivery_email` and `workflow` fields remain founder/production fields and are outside the calculator.

## Field convention

- **Required (R):** calculation cannot run for that service without it.
- **Conditional (C):** required only when the stated condition applies.
- **Optional (O):** accepted when supplied; never request it solely because this contract can store it.
- Monetary calculations use decimal pounds internally. Energy rates may be supplied in pence and must be converted exactly.
- Each customer-fact group and capture has a short internal `source_ref`. Per-field source overrides are needed only when facts came from different material.
- Do not store names, bills, account numbers or unnecessary personal data in the calculation block.

## 1. Common and customer-supplied input

### Common per analysis unit

| Field | Need | Rule |
| --- | --- | --- |
| `analysis_unit.id` | R | `broadband`, `mobile`, `energy_combined`, `gas` or `electricity`. |
| `analysis_unit.services` | R | Supported service or services represented by the unit. |
| `requested` | R | Whether the household asked Billvisor to analyse the service. |
| `case.postcode` | R when any supported service is requested | One case-level postcode is required for every ordinary case. It supports the founder's market search and service/geography controls; it is not repeated inside each service fact group. |
| `customer_source_ref` | R when requested | Reference to the supplied wording or extracted record. |
| `capture_date` | C | Required when market observations are used. |

### Broadband customer facts

| Field | Need |
| --- | --- |
| `provider` | R |
| `download_speed_mbps` | R |
| `monthly_price_gbp` | R |
| `contract_end` | R: ISO date, `out_of_contract` or `unknown` |
| `material_bundle_note` | O, only if volunteered and relevant |

### Mobile customer facts

| Field | Need |
| --- | --- |
| `provider` | R |
| `data_allowance_gb` or `data_allowance_unlimited` | R |
| `handset_or_important_extras` | R: supplied description or `none` |
| `handset_included` | R: internal `true`/`false` normalisation of the supplied handset/extras answer. It does not create an additional customer question. |
| `monthly_price_gbp` | R |
| `contract_end` | R: ISO date, `out_of_contract` or `unknown` |

The calculator must not treat a handset-inclusive price as SIM-only.

### Energy customer facts

| Field | Need |
| --- | --- |
| `postcode` | R at case level; see common case fields above |
| `supplier` | R |
| `fuels` | R: gas, electricity or both |
| `approximate_payment` | R: monthly amount or supplied payment pattern |
| `approximate_monthly_payment_gbp` | O: Operations' numeric normalisation of an unambiguous monthly amount already supplied in `approximate_payment`; display-only sense-check, never a substitute for tariff-cost calculation |
| `payment_method` | R |
| `tariff_type_or_name` | R; `unknown` is a valid supplied value |
| `tariff_end` | R; date, `no_end_date`, or `unknown` |
| `actual_annual_kwh_by_fuel` | O; highest-priority consumption input |
| `supplier_estimated_annual_kwh_by_fuel` | O; second-priority consumption input |
| `bedrooms` | C when neither annual-usage source is available |
| `specialist_setup` | C before using bedroom fallback: `none` or the supplied prepayment, multi-rate, electric-heating, heat-pump, regular-EV-charging or other material setup |

This list mirrors the approved customer request. It does not add a new customer-data requirement.

## 2. Founder-pasted market observations

### Broadband/mobile offer observation

Each extracted offer uses only:

| Field | Need | Rule |
| --- | --- | --- |
| `observation_id` | R | Unique within the case. |
| `service` | R | Broadband or mobile. |
| `provider` | R | Retail provider shown. |
| `package_label` | R | Short captured label, not invented. |
| `package_attributes` | R | Only attributes needed to establish broad comparability: broadband speed/service type, or mobile SIM/handset status and data allowance. |
| `recurring_price_periods` | R | Price and whole months or effective date for every known first-year period. |
| `compulsory_one_off` | R | Either `shown` with the captured amount, or `not_shown`. A charge absent from the capture does not require proof that none exists. |
| `unquantified_future_rise` | O | Boolean; current price remains the working estimate. |
| `source_ref` and `captured_at` | R | Internal trace only. |
| `comparison_disposition` | R | `include` or `exclude_plainly_not_comparable`. |
| `exclusion_reason` | C when excluded | Short factual reason. |
| `comparison_sufficient_for_score` | C | Set `false` only when the captured results support a reasonable qualified comparison but a customer-stated material feature was not matched. The case remains **Analysed with limitations**, retains the cost comparison and saving candidate, and may receive a numeric score under the approved method. Retain the qualified-comparison flag internally; do not label the customer-facing score “Estimated”. |

When `compulsory_one_off` is `not_shown`, its observed-cost contribution is £0 and the trace must say **not shown in capture**, not **no charge**. Any compulsory charge shown must be included. Rewards may be captured in an optional note but never enter the calculation. The calculator validates the recorded disposition; it does not create a new comparability rule. If the package cannot safely be classed under the approved “broadly similar/plainly not comparable” rule, stop with `COMPARABILITY_RULE_AMBIGUOUS` and escalate to Evidence.

### Energy tariff observation

| Field | Need | Rule |
| --- | --- | --- |
| `observation_id` | R | Unique within the case. |
| `role` | R | `current_cost_model` or `accessible_alternative`. |
| `provider`, `tariff_label`, `tariff_type` | R | As captured. |
| `region`, `fuels`, `meter_type`, `payment_method` | R | Must match the rates supplied. |
| `unit_rate_p_per_kwh` | R per applicable fuel/register | Exact captured rate. |
| `standing_charge_p_per_day` | R per applicable fuel | Exact captured rate. |
| `tariff_end` and `exit_fee_gbp` | R | Captured value or explicit `unknown`. |
| `eligibility_or_meter_requirement` | C when stated | Do not infer eligibility. |
| `source_ref` and `captured_at` | R | Internal trace only. |
| `score_comparison_observation_id` | C | Founder-approved only for a supportable like-for-like payment-method comparison. The selected observation must match the current model on provider/basis, region, fuels, meter type, tariff type, consumption and comparison group, differing only in payment method. |
| `tariff_fit_score_observation_id` | C | Founder-approved only for a current-tariff versus relevant-accessible-tariff score. It must match the current model on provider, geography, fuels, meter type, payment method and selected consumption input; tariff type may differ. It is not a market-comparison route. |

The calculator calculates every usable observation with the same selected household consumption. It may calculate differences between the current-cost model and each observation. A founder-approved `score_comparison_observation_id` may select only a validated like-for-like payment-method observation for the narrow qualified Energy score. A founder-approved `tariff_fit_score_observation_id` may select a relevant accessible tariff with the same provider, geography, fuels, meter type and payment basis, even where the tariff type differs; it creates a price-only tariff-fit score, not a market comparison or named-offer recommendation. Separately, an electricity-only Economy 7 case may use actual peak/off-peak readings, its current Economy 7 rates and a regional Direct Debit single-rate reference across exactly the same measured billing-day sample to calculate a qualified tariff-fit score. Other observations remain saving candidates and cannot be selected automatically as “the market.”

## 3. Provider-quality reference

Where a current approved table already contains the customer's provider, input only:

- service;
- stable table reference;
- table version and date;
- provider identifier; and
- the table's structured provider/raw-score rows needed for the tie-safe position calculation.

The calculator does not parse or maintain Evidence's source table. It validates the explicitly supplied structured snapshot and returns the raw score, tie-safe rank and provider-position calculation required by `BILLS_HEALTH_SCORE_METHOD.md`. Do not copy a hand-entered provider position into the case. A provider absent from the supplied approved table returns `NEW_PROVIDER_ASSESSMENT_REQUIRED` and escalates to Evidence. If provider quality remains unavailable after that process but price position is valid, the approved price-only limited score may be used.

Energy provider scoring remains unavailable until the pending numeric normalisation rules are approved; the calculator must not convert the current directional energy research into a provider position.

## 4. Deterministic outputs

### Coverage status

- **Not analysed:** the customer did not ask Billvisor to analyse the service.
- **Analysed:** required minimum facts and approved calculation inputs support the assessment without a material limitation.
- **Analysed with limitations:** the service was requested and a supportable assessment remains possible, but a missing/ambiguous agreed minimum field, price-only provider fallback or genuine internal evidence gap restricts it. The approved ordinary bedroom fallback does not change coverage when the agreed minimum information was supplied; explain its use in the customer narrative instead.

Coverage is not a market rating or recommendation. Return the status plus one internal reason code. Information Billvisor deliberately did not request cannot create a limitation.

If a requested service is outside supported Phase 1 scope or geography, do not assign **Not analysed** or another contradictory coverage status. Return `coverage_status: null` with `REQUESTED_SERVICE_UNSUPPORTED` or `REQUESTED_GEOGRAPHY_UNSUPPORTED`, stop that service, and flag `REPORT_TREATMENT_POLICY_UNRESOLVED` for founder/CEO resolution. Current authorities do not define the final report treatment for this case, so the calculator must not invent it.

### Broadband/mobile price outputs

For each included offer:

`first_year_effective_monthly = (12-month compulsory recurring cost + compulsory one-offs) / 12`

Then return:

1. unrounded effective monthly price by offer;
2. arithmetic mean by provider using unrounded offer values;
3. provider-balanced monthly benchmark: the middle provider mean, or mean of the two central provider means;
4. annual comparison value = monthly benchmark × 12;
5. current annual spend = submitted monthly price × 12;
6. positive saving candidate = current annual spend − annual comparison value; otherwise `null`;
7. provider and offer counts; and
8. one estimation note only when an unquantified future rise materially affects interpretation.

The calculator does not decide whether a positive saving is useful or should be shown.

### Energy outputs

Select annual consumption separately by fuel in this fixed order:

1. actual previous-12-month kWh;
2. supplier estimated annual kWh;
3. bedroom fallback: 1–2 = 1,600 electricity/6,000 gas; 3–4 = 2,500/9,500; 5+ = 3,800/14,000.

Do not use the fallback for a specialist or multi-rate arrangement without suitable register usage.

For each tariff observation and applicable fuel/register:

`annual cost = annual kWh × (unit rate p/kWh ÷ 100) + 365 × (standing charge p/day ÷ 100)`

Return:

- selected consumption values and source level;
- exact annual cost for every observation and a combined total where applicable;
- the current tariff's calculated annual cost as the Energy current-annual-spend figure and as Energy's overall-score weight; the customer-supplied approximate monthly payment remains a sense-check only;
- exact positive saving candidates against the current-cost model;
- any exact like-for-like payment-method saving candidate;
- tariff timing and exit-fee facts as captured;
- `score_comparison_value`, selected observation id and `score_status: estimated_score` for the approved like-for-like payment-method route; `score_status: tariff_fit_score` for the approved current-tariff versus relevant-accessible-tariff route; otherwise `null` and `no_score`.

The calculator must not select one accessible Energy observation as “the market”, use the cheapest observation automatically, or convert any saving candidate into a recommendation.

### Bills Health Scores

When an exact current monthly price/cost and approved comparison exist, apply `BILLS_HEALTH_SCORE_METHOD.md` exactly:

- price difference ratio and exact price score;
- provider position where an approved table supports it;
- price score `min(100, 20 + 60 × comparison/current)`;
- exact 90/10 service score where provider position is available, or the approved price-only route where it is not;
- post-calculation materiality cap: 39 when the positive saving is at least £150 and 25% of annual current spend, or 74 when it is at least £100 and 15%;
- the founder-approved `small_saving_not_worth_effort` floor: where a founder-approved Stay put decision is specifically based on effort and the supported annual saving is below £50, floor the score at 75;
- half-up displayed rounding, band and provider-note trigger;
- overall annual-spend and status-weighted average across every service with a numeric score: current annual spend × 1.0 for Analysed, or × 0.8 for Analysed with limitations.

No reasonable price comparison means no numeric score, even if provider quality exists. A qualified comparison marked `comparison_sufficient_for_score: false` produces a numeric score, remains **Analysed with limitations** and must carry the material limitation on the service page. The narrow Energy payment-method score is also qualified and price-only. Keep that status internally; do not label the customer-facing score or gauge “Estimated”. Every scored Analysed-with-limitations service contributes to the overall score at weight 0.8. Contract status informs the recommendation but does not directly enter the score; saving size affects only the approved materiality caps.

### Smallest reproducible trace

Return only:

- method and table versions used;
- source references and capture dates;
- included/excluded observations and factual exclusion reasons;
- offer first-year totals, provider means and median arithmetic;
- Energy consumption source, rates used and annual-cost arithmetic;
- exact current/comparison/saving values;
- every required score input, intermediate result, rounding and inclusion/exclusion from the overall score;
- warnings, errors and escalation result.

## 5. Stop and escalation contract

The calculator returns structured codes and never silently substitutes a value.

| Code | Result and owner |
| --- | --- |
| `MINIMUM_FIELD_MISSING` | Stop the affected calculation. Operations may make one consolidated customer clarification unless the founder has directed otherwise. Not an Evidence escalation. |
| `MINIMUM_FIELD_AMBIGUOUS` | Same as above; never guess. |
| `NO_USABLE_CAPTURED_PRICE` | Stop benchmark calculation and ask the founder for a usable capture. Escalate only if the source/method rule itself is unclear. |
| `COMPARABILITY_RULE_AMBIGUOUS` | Stop; Evidence resolves the missing/ambiguous method rule. |
| `NEW_PROVIDER_ASSESSMENT_REQUIRED` | Stop provider-position calculation; Evidence assesses the provider. Price calculation may continue. |
| `METHOD_OR_SOURCE_RULE_MISSING` | Stop affected calculation; Evidence resolves the bounded rule/source question. |
| `MATERIAL_EVIDENCE_CONFLICT` | Stop affected calculation; Evidence resolves the conflict. |
| `CALCULATOR_CANNOT_SAFELY_PROCESS` | Stop; send the bounded unsupported case to Evidence. |
| `SPECIALIST_ENERGY_USAGE_REQUIRED` | Bedroom fallback blocked. Operations requests suitable usage only if permitted; do not ask Evidence to invent consumption. |
| `ENERGY_SCORE_COMPARISON_UNAPPROVED` | Return annual tariff costs and saving candidates but no Energy score when neither an approved like-for-like payment-method comparison nor the approved Economy 7 tariff-fit input set is present. Evidence must not choose a broader comparison case by case. |
| `REQUESTED_SERVICE_UNSUPPORTED` | Stop the requested service with `coverage_status: null`; final report treatment is unresolved founder/CEO policy. |
| `REQUESTED_GEOGRAPHY_UNSUPPORTED` | Stop the requested service with `coverage_status: null`; final report treatment is unresolved founder/CEO policy. |
| `REPORT_TREATMENT_POLICY_UNRESOLVED` | Do not generate service coverage or report content until the founder/CEO resolves the unsupported requested-service treatment. |

Evidence is called only for a new provider assessment, missing/ambiguous source or method rule, material evidence conflict, or an unsupported case the calculator cannot safely process.

## 6. Compact worked example: two-bedroom British Gas case

### Input summary

- Combined gas/electricity, TN1 1BN, British Gas, variable, standard credit/manual card payment.
- Two bedrooms; no specialist setup; no actual or supplier-estimated annual kWh.
- Approximate payments supplied: £1,140–£1,190 a year, used only as a sense-check.
- Consumption selected deterministically: 1,600 kWh electricity and 6,000 kWh gas; bedroom fallback.
- Two same-basis regional observations contain the required rate and standing-charge fields: standard-credit current model and Direct Debit comparison. The Direct Debit observation is explicitly selected for the narrow like-for-like qualified-score route.

### Output

| Result | Exact value |
| --- | ---: |
| Coverage | Analysed with limitations |
| Limitation code | `BEDROOM_CONSUMPTION_FALLBACK` |
| Current annual-cost model | £1,282.2730 |
| Direct Debit comparison | £1,173.3620 |
| Like-for-like payment-method difference | £108.9110 |
| Energy score comparison | £1,173.3620 |
| Energy score | 75 Good (exact 74.9038…; qualified-comparison status retained internally) |
| Overall-score contribution | Included at weight 0.8 |

The calculator validates and uses the explicitly selected like-for-like payment-method comparison. It does not choose Direct Debit as the recommendation or select a broader market alternative. The founder still approves customer content separately. The customer limitation is: “Your consumption was estimated from households with similar characteristics.”

## 7. Remaining founder/CEO policy decisions

1. Decide how a requested service outside supported Phase 1 scope or geography should appear in the report. Until then the calculator stops with no coverage status.

Extending the existing case JSON, representing recurring price periods and Energy rates exactly, recording the approved comparability disposition, and serialising saving candidates are Operations implementation choices. They require validation, not founder approval, unless an implementation choice changes business meaning or the governing method.

The implemented path must retain its compact synthetic branch checks before live use. Later changes must not modify recommendation rules or the report design without separate authority.

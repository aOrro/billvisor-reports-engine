# Billvisor report engine (Phase 1)

A local, deterministic engine that turns founder-approved case facts and founder-pasted market observations
into a validated, founder-approved and fingerprinted `report_data.json` for the Bills Health Report.

It does **not** browse, scrape, send email, generate HTML or PDF, call an LLM, or choose the recommendation.
Governing rules are in `docs/governing/` and take precedence over the build brief. The output format is in
`docs/REPORT_DATA_CONTRACT.md`.

Python 3.11+, standard library only.

## Where data lives

Real cases live **outside this repo** in a founder-only folder:

```sh
export BILLVISOR_CASES_DIR=~/Billvisor-Cases     # or pass --cases-dir
```

The CLI refuses a cases folder inside the repo. Only synthetic fixtures (`tests/fixtures/`) belong here.
Never put source documents, account numbers or payment details in a case file.

## Founder flow

```sh
python3 -m billvisor new BV-0007          # scaffold <cases>/BV-0007/case.json
#   set requested true/false per service, enter the facts and paste observations
python3 -m billvisor validate BV-0007     # minimum fields, with stop codes and a next action
python3 -m billvisor calc BV-0007         # calculation_output + trace.txt
python3 -m billvisor pack BV-0007         # approval-pack.md + a blank `decision` section
#   choose action, effort, priority and exact wording in `decision`
python3 -m billvisor approve BV-0007      # preview: every check, no record
python3 -m billvisor approve BV-0007 --yes  # record the approval snapshot and fingerprints
python3 -m billvisor review-status BV-0007
python3 -m billvisor review-record BV-0007 --result pass   # only when Review is required
python3 -m billvisor build BV-0007        # report_data.v<N>.json (all gates re-checked)
```

`build` refuses when inputs, calculation, decision or customer content changed after approval. It also refuses
when a required Review is missing, stale or found a Major or Critical defect.
A correction means bumping `case.report_version`, then calc, approve and build again.

## case.json (per analysis unit)

```jsonc
{
  "id": "broadband",                       // broadband | mobile | energy_combined | gas | electricity
  "services": ["broadband"],
  "requested": true,                       // false = Not analysed (overview only)
  "calculation_input": {
    "customer_source_ref": "email-2026-11-01",
    "facts": { "provider": "BT", "download_speed_mbps": 67, "monthly_price_gbp": 39.00,
               "contract_end": "out_of_contract" },             // ISO date | out_of_contract | unknown
    "provider_table": { "table_ref": "broadband_provider_scores",
                        "table_version": "2026-11-04-as-supplied", "provider_id": "BT" },
    "comparison_sufficient_for_score": true,   // false -> Estimated score, Analysed with limitations
    "observations": [{
      "observation_id": "bb1", "service": "broadband", "provider": "Sky", "package_label": "Full Fibre 75",
      "package_attributes": { "download_speed_mbps": 75 },
      "recurring_price_periods": [ { "price_gbp": 22.00, "months": 18 } ],
          // later periods: { "price_gbp": 27, "effective_date": "2027-04-01" } or open-ended { "price_gbp": 30 }
      "compulsory_one_off": { "status": "not_shown" },          // or { "status": "shown", "amount_gbp": 9.99 }
      "unquantified_future_rise": false,       // true = advertised price used for periods with no captured price
      "rewards_note": "£50 voucher",           // never enters the cost
      "source_ref": "capture-1", "captured_at": "2026-11-04",
      "comparison_disposition": "include"      // or exclude_plainly_not_comparable + exclusion_reason
    }]
  }
}
```

Mobile facts also need `handset_included` (true/false), recorded from the customer's handset/extras answer.
It is used to stop a handset price being compared with SIM-only. Optional `typical_data_use_gb` enables the
unused-allowance finding.

Energy facts are: `supplier`, `fuels` (both/gas/electricity), `approximate_payment`, `payment_method`,
`tariff_type_or_name`, `tariff_end`, and optionally `actual_annual_kwh_by_fuel` and
`supplier_estimated_annual_kwh_by_fuel`. `bedrooms` and `specialist_setup` (none, prepayment, multi_rate,
electric_heating, heat_pump, ev_charging, other) are needed when no annual usage is supplied.
Observations carry `role` (current_cost_model / accessible_alternative), tariff fields and
`rates.{electricity,gas}.{unit_rate_p_per_kwh, standing_charge_p_per_day}`.
An energy score exists only when the founder selects one route:
- `tariff_fit_score_observation_id`: same provider, region, fuels, meter and payment method. Gives a tariff-fit score; status Analysed.
- `score_comparison_observation_id`: same tariff basis, different payment method. Gives an Estimated score; status Analysed with limitations.

## Implementation notes on the governing rules

- Money is handled with `Decimal` throughout. Floats are refused. Display figures are rounded half-up to whole pounds.
- Energy weight in the overall score uses the current tariff's estimated annual cost. That is the same figure the score uses.
- Multi-rate (Economy 7) electricity stops with `CALCULATOR_CANNOT_SAFELY_PROCESS`. The register-level route is not implemented.
- The provider note uses the approved "Recent public data…" wording. It stops with `METHOD_OR_SOURCE_RULE_MISSING` when triggered
  unless the provider table sets `sources_publicly_accessible: true`.
- How Review triggers are counted:
  - "first five" means fewer than five other reports have been built;
  - after a Major or Critical defect, Review continues until five later reviewed reports pass;
  - otherwise the next report after four unreviewed reports in a row is spot-checked.
  The ledger is `<cases-dir>/_review_ledger.json`.
- The leakage check blocks: "benchmark", provider names from captures (case-sensitive), source names, £0, guaranteed, best deal,
  whole market, cheapest, reviews, "about" before a saving, and customer-blame wording (except on Confirm-information pages).

## Tests

```sh
python3 -m unittest discover -s tests -t .
```

`tests/test_regression_existing_cases.py` runs any anonymised approved cases placed in `tests/regression/<name>/`
(`case.json` plus `expected.json`). It is skipped until those cases are supplied. Name each folder by a neutral
reference (e.g. `case-a`), never by the customer's name.

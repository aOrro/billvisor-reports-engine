# Billvisor report engine (Phase 1)

A local, deterministic engine that turns founder-approved case facts and founder-pasted market observations
into a validated, founder-approved and fingerprinted `report_data.json`, and renders it into the finished
fixed-A4 Bills Health Report HTML using the approved templates in `templates/report/`.

It does **not** browse, scrape, send email, generate a PDF, call an LLM, or choose the recommendation. The founder
opens the HTML, checks it visually and saves it as PDF (A4, background graphics on).
Governing rules are in `docs/governing/` and take precedence over the build brief. The data format is in
`docs/REPORT_DATA_CONTRACT.md`; the page mapping is in `docs/governing/PHASE_1_REPORT_RENDERER_CONTRACT.md`.

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
python3 -m billvisor review-record BV-0007 --outcome passed --severity none   # only when Review is required
python3 -m billvisor build BV-0007        # report_data.v<N>.json + report.v<N>.html (all gates re-checked)
```

`build` refuses when inputs, calculation, decision or customer content changed after approval. It also refuses
when a required Review is missing, stale, or its outcome is Content blocked or Escalate before delivery.
A correction means bumping `case.report_version`, then calc, approve and build again.

The HTML is rendered only inside `build`, after every gate passes, and only from the report data being written
(never from the case file). It is one self-contained file: the logo and illustration are embedded, so it opens
from any folder. If the data has no approved rendering (for example no service has a numeric score, so there
is no overall score for the cover), `build` refuses and writes nothing.

Report-level decision fields: `report.summary` (overview page) and optional `report.priority_reason`
("Why these priorities?"). A Confirm-information unit also needs `still_needed` (at least one item) and may
list `confirmed_items`; both are founder-approved text and are refused on any other action.

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
    "comparison_sufficient_for_score": true,   // false -> qualified score, Analysed with limitations
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

Energy facts are: `supplier`, `fuels` (both/gas/electricity), `approximate_payment` (the customer's own words),
optional `approximate_monthly_payment_gbp` (a number, filled in only when the customer's amount is unambiguous; it is
shown as "Monthly payment" and never used in the calculation), `payment_method`,
`tariff_type_or_name`, `tariff_end`, and optionally `actual_annual_kwh_by_fuel` and
`supplier_estimated_annual_kwh_by_fuel`. `bedrooms` and `specialist_setup` (none, prepayment, multi_rate,
electric_heating, heat_pump, ev_charging, other) are needed when no annual usage is supplied.
Observations carry `role` (current_cost_model / accessible_alternative), tariff fields and
`rates.{electricity,gas}.{unit_rate_p_per_kwh, standing_charge_p_per_day}`.
An energy score exists only when the founder selects one route:
- `tariff_fit_score_observation_id`: same provider, region, fuels, meter and payment method. Gives a tariff-fit score; status Analysed.
- `score_comparison_observation_id`: same tariff basis, different payment method. Gives a qualified score; status Analysed with limitations. The qualified flag stays internal and is not a customer-facing score label.

## Implementation notes on the governing rules

- Money is handled with `Decimal` throughout. Floats are refused. Display figures are rounded half-up to whole pounds.
- Energy weight in the overall score uses the current tariff's estimated annual cost. That is the same figure the score uses.
- Multi-rate (Economy 7) electricity stops with `CALCULATOR_CANNOT_SAFELY_PROCESS`. The register-level route is not implemented.
- The provider note uses the approved "Recent public data…" wording. It stops with `METHOD_OR_SOURCE_RULE_MISSING` when triggered
  unless the provider table sets `sources_publicly_accessible: true`.
- How Review triggers are counted:
  - "first five" means fewer than five other reports have been built;
  - after a review with highest severity major or critical, Review continues until five later reviewed reports pass
    cleanly (outcome passed or passed after correction, highest severity none or minor);
  - otherwise the next report after four unreviewed reports in a row is spot-checked.
  The ledger is `<cases-dir>/_review_ledger.json`.
- A Review record has an outcome (`--outcome passed | passed-after-correction | blocked | escalate`, stored with the
  REPORT_OUTPUT_QA.md wording) and the highest defect severity (`--severity none | minor | major | critical`). Only the
  two passing outcomes allow `build`. "Content passed" requires severity none; "passed after correction" requires a
  severity above none.
- The leakage check blocks: "benchmark", provider names from captures (case-sensitive), source names, £0, guaranteed, best deal,
  whole market, cheapest, "reviews" (the plural; "Review your…" is ordinary action wording), "about" before a saving,
  and customer-blame wording (except on Confirm-information pages).

Decisions still open are listed in `docs/OPEN_QUESTIONS.md`.

## Tests

```sh
python3 -m unittest discover -s tests -t .
```

`tests/test_regression_existing_cases.py` runs every case in `tests/regression/<name>/` (`case.json`,
`expected.json`, and `NOTES.md` with the hand arithmetic). Expected values are worked out by hand from the governing
methods, never captured from the engine. Cases are wholly synthetic; name each folder by a neutral reference, never by
a customer's name. `tests/test_render.py` holds the renderer acceptance checks from the renderer contract §7.

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

**Current state (done 4 November 2026):** the qualified-comparison flag is kept only in `calculation_output` and `trace.txt`. `report_data` no longer carries it, so the renderer cannot show it, and the workflow tests check that no built report contains it. The governing documents now say not to show “Estimated” beside a score; the service-page narrative explains estimates and limitations instead.

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

## Follow-ups from the review of 584bece — resolved

Checked and resolved on 4 November 2026. Items 1 and 2 were corrected in the `context-files/` source method first, then recopied into `docs/governing/` unchanged.

1. **Missed worked example.** Corrected: it now shows **75 — Good** under **Analysed with limitations**, with the qualified-comparison status internal and the limitation in the service-page narrative.
2. **Old term in the trace list.** Corrected: it now says “qualified (internal flag)”.
3. **Source date.** The fix-up commit records 4 November 2026 as the source-update date. The decision is now in the source method and shared Memory, not only in the repository copies.

**Engine side.** These old-rule descriptions were updated on this branch:

- `docs/REPORT_DATA_CONTRACT.md:40` tells the renderer to label the score "Estimated".
- `billvisor/pack.py:92` tells the founder the score will be "labelled Estimated".
- `README.md:56` and `:84` say "Estimated score".

The internal flag stays; it is not shown to customers.

## Open questions for the next phase

Recorded on 4 November 2026. These need an answer from the founder, or files from the other laptop, before the related item can be built. Answer each one in place, or point to the commit that resolves it.

### A. Files and data needed

1. **Approved report design (blocks item 1).**
   - Copy the template and assets from `/Users/anton/billvisor/design/report/` into a clearly labelled repo folder, such as `templates/report/`. Say which version is the approved one.
   - Before committing, check that no example render, screenshot, PDF or sample data in that folder contains real customer details: names, postcodes, providers tied to a person, amounts or dates. Replace any with synthetic values.
   - Say whether an existing renderer (for example `generate_report.py`) or a structured-input schema belongs with the design. If one does, add it as well. Item 1 should reuse its field names rather than invent new ones, and `docs/REPORT_DATA_CONTRACT.md` still says "to reconcile with generate_report.py".
2. **Current-service fields per service (blocks item 2).**
   - List exactly which current-service details the approved template shows for broadband, mobile and energy, with their labels.
   - `MEMORY.md:35` mentions a "plan", but `LIVE_CASE_CALCULATOR_SPEC.md` has no plan or package-name fact for broadband or mobile. Confirm whether the template shows one. If it does, a new optional fact is needed.
   - Confirm the energy "payment" shown is the customer's approximate payment as supplied, not a figure the engine calculates.
3. **Regression cases (blocks item 4).** Provide two anonymised cases matching the patterns in item 4:
   - each case's inputs in the engine's `case.json` format;
   - expected values taken from the approved reports, not from running this engine: scores, bands, statuses, pages, action order and displayed figures.

   Use neutral folder names, such as `tests/regression/case-a/`.
4. **Provider score tables.**
   - Copy `BROADBAND_PROVIDER_SCORES.md` and `MOBILE_PROVIDER_SCORES.md` from `data-files/evidence/provider-scoring/` into `docs/governing/`. They are listed in the README but missing.
   - For each table, confirm three values that are still placeholders in `reference/provider_tables/*.json`:
     - `table_version`, currently "2026-11-04-as-supplied";
     - `table_date`;
     - `sources_publicly_accessible`, currently null.

   While `sources_publicly_accessible` is not true, any case where provider quality lowers the score band stops with `METHOD_OR_SOURCE_RULE_MISSING`. The approved note says "Recent public data…", which may be used only when the sources really are public (`BILLS_HEALTH_SCORE_METHOD.md:149`).

### B. Engine readings to confirm

The engine currently works as described below. Confirm each one, or say what should change.

5. **Energy annual spend, the most material question.**
   - For energy, the engine uses the current tariff's estimated annual cost for two things: the "current annual spend" figure on the page, and energy's weight in the overall score.
   - `MEMORY.md:35` defines current annual spend as the submitted monthly payment × 12. That line is written about broadband and mobile.
   - The alternative is the customer's approximate payment annualised. The choice can change the overall score.
6. **Same-provider tariff-fit.** A tariff-fit comparison must be with the customer's current provider. `LIVE_CASE_CALCULATOR_SPEC.md:122` requires this. `BILLS_HEALTH_SCORE_METHOD.md` §2.1 and `MEMORY.md:36` do not mention provider.
7. **Mobile `handset_included`.**
   - Mobile facts require a true/false `handset_included`, recorded from the customer's handset/extras answer. The engine uses it to stop a handset price being compared with SIM-only, as `LIVE_CASE_CALCULATOR_SPEC.md:63` requires.
   - The field is not in the spec's fact list. Confirm it can be added there.
8. **Broadband postcode not required.** This follows the spec's broadband fact list, not the build brief.
9. **Economy 7 / multi-rate electricity.**
   - These cases stop with `CALCULATOR_CANNOT_SAFELY_PROCESS` and go to Evidence.
   - The register-level qualified tariff-fit route in `BILLS_HEALTH_SCORE_METHOD.md` §2.1 is not built.
   - Confirm stopping is acceptable for Phase 1, or ask for that route to be built.
10. **How Review triggers are counted** (`PHASE_1_CASE_OPERATING_METHOD.md` §3):
    - "first five" means fewer than five earlier reports have been built;
    - after a Major or Critical defect, Review continues until five later reviewed reports pass in a row;
    - otherwise, the next report after four unreviewed reports in a row is spot-checked.

    `REPORT_OUTPUT_QA.md` is not in the repo. Supply it if Review's checks should be enforced by the engine rather than recorded as a pass/fail result.

## Founder answers recorded — 4 November 2026

1. **Approved template:** `templates/report/` now contains the approved synthetic template assets copied from `/Users/anton/billvisor/design/report/`: pages 1–7, the combined-Energy and analysed-with-limitations variants, shared CSS tokens and logo. It deliberately excludes the inspiration image and combined preview. A scan found no real customer names, email addresses or postcodes in the copied files. Use these files as the visual source; do not import the legacy generator or schema unless a specific compatibility need is demonstrated.
2. **Current-service display fields:** use these exact renderer-safe fields, with no new package-name question:
   - Broadband: Provider; Download speed; Monthly cost; Contract ends/status.
   - Mobile: Provider; Data allowance plus SIM-only/handset status; Monthly cost; Contract ends/status.
   - Energy: Supplier; Gas/electricity service; Tariff; Monthly payment; Tariff ends/status.
   The supplied mobile extras text is not rendered automatically; any extra customer wording remains founder-approved content.
3. **Regression cases:** create two fully synthetic fixtures from the existing test patterns and calculate expected assertions independently from the documented rules. Do not use real customer inputs or outputs.
4. **Provider tables:** reference copies are now in `docs/governing/`. Retain `table_version: 2026-11-04-as-supplied`, `table_date: 2026-11-04` and `sources_publicly_accessible: null` in the runtime JSON until Evidence confirms an authoritative replacement. Therefore a triggered negative provider-quality note must remain blocked.
5. **Energy annual spend:** use the current tariff's calculated annual cost for the Energy page and Energy’s overall-score weight. The customer’s approximate monthly payment is a sense-check only.
6. **Same-provider tariff fit:** retain the current-provider requirement for the ordinary tariff-fit route. It is a tariff-fit signal, not an alternative-provider/whole-market comparison.
7. **Mobile handset flag:** add `handset_included` explicitly to the spec and case validation as an internal true/false normalisation of the existing customer answer. Do not ask a second question.
8. **Postcode:** require `case.postcode` for every ordinary requested service; it is a case-level fact, not duplicated per service.
9. **Economy 7 / multi-rate:** keep it outside the ordinary calculator. Stop the affected Energy unit safely and do not build the specialist route in this phase.
10. **Review:** `REPORT_OUTPUT_QA.md` is now included as governing reference. The engine may enforce that a required human Review result exists, but must not pretend to automate the Review judgement.

## Founder answers recorded — renderer contract (4 November 2026)

Items A1–A8 and B9–B10 are now resolved by the copied governing authority
`docs/governing/PHASE_1_REPORT_RENDERER_CONTRACT.md`. Implement against that file; do not make
additional product or wording decisions in the renderer.

1. **Action pages:** remove `Time required` and `Difficulty`. Render `Effort: Low`, `Effort: Moderate` or
   `Effort: High`, supplied and approved by the founder for the particular action. Do not derive it from
   score or action type and do not promise a duration.
2. **Energy page:** show both `Monthly payment` and `Estimated annual energy cost`. Include the exact sentence:
   `This uses your current tariff and estimated energy use. Your monthly payments may vary through the year.`
   The annual figure is the tariff calculation; the monthly payment is a sense-check.
3. **Broadband/Mobile figures:** immediately below the current-service block, show a compact row for
   `You pay each year`, `Similar services cost`, and `Potential saving` only when founder-approved for display.
   Retain the qualitative What this means section.
4. **Narrative locations:** provider-quality note, service limitation and Energy estimate explanation belong in
   What this means as short grouped paragraphs. Put `Supporting source details are available on request.` once
   on the final action-plan page.
5. **Remove/define remaining fields:** remove Report confidence. Market position is the score band
   Good/Medium/Poor, or `—` if no score. Founder-supplied action labels remain literal; Stay put displays
   `No action needed`. Totals are: annual spend = current annual spend across analysed service pages; potential
   savings = founder-selected displayed positive savings; services reviewed = pages; priority actions = actions
   other than Stay put. Order actions by founder priority, then displayed saving descending for a tie.
6. **Labels:** replace old sample labels with exactly: Broadband: Provider, Download speed, Monthly cost,
   Contract ends. Mobile: Provider, Data allowance, Plan type, Monthly cost, Contract ends. Energy: Supplier,
   Services, Tariff, Monthly payment, Tariff ends.
7. **Confirm information:** this page uses founder-approved `What we could confirm` and `What we still need`
   lists, printed in the approval pack. It is for Confirm information only, not ordinary Analysed with limitations.
8. **Template defects:** correct the hard-coded 74 score to Medium styling and use local
   `templates/report/billvisor-house.png`, never an absolute workspace image path.
9. **Energy QA:** QA now explicitly checks calculated tariff annual cost for Energy and the distinct monthly
   payment sense-check role.
10. **Review record:** change the engine schema/CLI from a one-field `pass/minor/major/critical` result to
    `outcome` (`Content passed`, `Content passed after correction`, `Content blocked`, `Escalate before delivery`)
    plus `highest_severity` (`none`, `minor`, `major`, `critical`). Only the first two outcomes build; major or
    critical resets the clean-run count.

## Implementation acceptance for the renderer

Before requesting founder visual review, add synthetic tests proving that the renderer uses only approved
`report_data`, blocks stale gates, implements the above conditional fields/totals/action ordering, has no
customer-visible `Estimated` score label, and contains no broken workspace asset path. Use wholly synthetic
fixtures only.

## Founder answers recorded — final renderer mapping (4 November 2026)

The following completes the renderer decisions. Update `PHASE_1_REPORT_RENDERER_CONTRACT.md` is the authority;
this section is the implementation checklist.

1. **Energy monthly payment:** add optional `facts.approximate_monthly_payment_gbp`. Operations populates it only
   when it can unambiguously normalise the customer's existing `approximate_payment` answer. It is display-only;
   do not ask a further question or use it for Energy annual spend. Render it when present and omit the field when
   absent.
2. **Energy sentence:** render exactly: `This uses your current tariff and the annual energy-use figure available
   for your home. Your monthly payments may vary through the year.` Keep the separate bedroom-fallback estimate
   note where applicable.
3. **Comparison wording:** Broadband/Mobile figure row must say `Similar services cost about £X a year.`
4. **Energy saving:** where `potential_saving_gbp` is founder-selected for display, show it beneath the annual
   Energy figures. Do not show £0.
5. **Overview columns:** retain the approved design's Service, Annual spend, Market position, Potential savings and
   Health score columns. Do not add a next-action column.
6. **Priority labels:** remove High/Medium/None chips and the Priority label/column. Keep literal founder actions;
   a Stay put action may show `No action needed`.
7. **Text slots:** cover uses fixed `Our top recommendation` + primary `next_step` + `explanation`; service pages
   use `headline` under `How it compares` and fixed `Our recommendation` + `next_step` + `explanation`;
   report-level summary uses `report.summary`; a distinct `Why these priorities?` paragraph is optional
   `report.priority_reason`; final page uses fixed `If you only do one thing` + primary action fields + the
   existing fixed reply invitation. All non-fixed text remains founder-approved.
8. **Code/date display:** render `out_of_contract` as `Out of contract`; `unknown`/`no_end_date` as `No end date
   known`; ISO dates in `23 May 2026` form; `sim_only` as `SIM only`; `handset_included` as `Handset included`;
   unlimited data as `Unlimited data`; `both` as `Gas and electricity`; and `gas`/`electricity` as title case.
   A rolling monthly mobile plan is `Out of contract`.
9. **Repository minimisation:** `docs/governing/DECISION_REGISTER.md` has been removed. Do not restore it; the
   renderer contract and the remaining scoped governing documents provide its required policy context.

## Review of 6c5a595: template and QA conflicts

Checked on 4 November 2026.

**Confirmed:**
- **Provider score files.** `docs/governing/{BROADBAND,MOBILE}_PROVIDER_SCORES.md` match `reference/provider_tables/*.json` exactly: all 12 broadband and 11 mobile providers, with every overall score and confidence level.
- **Templates.** The templates contain no real names, email addresses or postcodes, no scripts, and no external web links.

**Done in the engine:** `case.postcode` is now required for every requested service (answer 8). It was previously required only for energy. A test covers it.

Items A1–A8 change or fill in the approved design. `LIVE_CASE_CALCULATOR_SPEC.md:275` says the design must not change without separate authority, so each needs a founder decision before item 1 (render HTML) can be built.

### A. Template conflicts with the governing documents or the answers

1. **Time and difficulty on the action pages.**
   - Pages 3 and 7 show "Time required: 10 min / 15 min / 0 min", and page 7 also shows "Difficulty: Easy".
   - `PHASE_1_RECOMMENDATION_FRAMEWORK.md:74` says: "Do not present these levels as measured facts or attach rigid time estimates until pilot evidence supports them."
   - Decide whether to remove the time fields, and whether difficulty is removed or shown only as a qualitative Low/Moderate/High effort level.
2. **Energy annual spend.**
   - The examples annualise the monthly payment: page 2 shows electricity at £1,752, which is £146 × 12. Answer 5 says energy uses the calculated tariff cost instead.
   - The energy page still shows "Monthly payment". A customer would therefore see a monthly figure that does not multiply to the annual figure.
   - Decide how the page explains this: remove the monthly payment, label the annual figure "estimated annual cost", add a fixed sentence, or something else.
3. **Similar-services comparison and annual spend on service pages.**
   - `MEMORY.md:35` and `REPORT_OUTPUT_QA.md` §3 expect the customer to see current annual spend and "Similar services cost about £X a year" for broadband and mobile.
   - Pages 4 and 5 show only a qualitative "How it compares" sentence and the saving, with no place for either figure.
   - Decide where they appear, or whether the qualitative sentence replaces them. The latter would need `MEMORY.md:35` and the QA check updated.
4. **Required content with no place in the templates.**
   - **Provider-quality note:** QA §4 places it "between price comparison and recommendation".
   - **"Supporting source details are available on request.":** this appears once per report. Say which page it goes on.
   - **Limitation sentence:** a scored service that is Analysed with limitations (qualified comparison or price-only) needs its one limitation sentence somewhere. The only limitations template is the Confirm-information variant, which has no score.
   - **Energy estimate note:** "Your consumption was estimated from households with similar characteristics."
5. **Fields no governing document or engine field defines.**
   - "Report confidence: High/Medium" on each service page.
   - The "Market position" column on the overview (page 2).
   - The priority labels "High priority / Medium priority / No action needed". The engine stores priority as a whole number from 1, set by the founder.
   - The totals on pages 1 and 2: "annualised spend", "total potential savings", "services reviewed" and "priority actions".

   For each, decide whether to remove it or define it. A suggested definition for the totals:
   - **annualised spend:** the sum of current annual spend over Analysed and Analysed-with-limitations services;
   - **total potential savings:** the sum of the savings the founder chose to show only;
   - **services reviewed:** the number of services with a page;
   - **priority actions:** actions other than Stay put.
6. **Service-page labels differ from answer 2.**
   - The broadband and mobile pages show "Provider type: Major provider / Mobile network" and "Package: Fibre 100 / 20 GB SIM-only". Answer 2 lists Provider (the name) and Download speed / Data allowance plus SIM-only or handset.
   - The combined-energy page adds "Arrangement: Dual fuel". Answer 2 has "Gas/electricity service", which is assumed to be the same field.
   - Confirm that answer 2's labels replace the template labels.
7. **Confirm-information page lists.**
   - The analysed-with-limitations template lists "What we could confirm" and "What is still needed".
   - The suggestion is two founder-approved text lists in the decision, `confirmed_items[]` and `still_needed[]`, checked by the leakage check and printed in the approval pack. Confirm or amend.
8. **Page 1 example errors.** These do not need a decision, but should not be copied:
   - The gauge shows 74 as "Good" in green, but 74 is Medium (`BILLS_HEALTH_SCORE_METHOD.md`: Good is 75–100). The renderer takes the band from the data.
   - Line 351 loads `../../../Documents/Business Planning/data-files/operations/report-template-system/assets/billvisor-house.png`. That file is not in the repo, so the image is broken. Add it to `templates/report/` if it belongs to the approved design.

### B. REPORT_OUTPUT_QA.md conflicts

9. **Energy annual spend.** QA §3 says "Current annual spend equals the submitted monthly payment multiplied by 12" and that it is "labelled as annualised from the submitted monthly payment", with no energy exception. After answer 5, Review would flag every energy page as a defect. QA §3 needs the same energy exception now in `MEMORY.md:35`, fixed in the source and recopied.
10. **Review result vocabulary.**
    - QA records a result (Content passed / Content passed after correction / Content blocked / Escalate before delivery) plus defect severities.
    - The engine's `review-record --result` takes a single value: `pass`, `minor`, `major` or `critical`.
    - Suggested change: the engine records the QA result plus the highest defect severity found.
      - Building is allowed only after "Content passed" or "Content passed after correction".
      - A Major or Critical severity resets the clean-run count.

    Confirm or amend.

## Review of 9f65464: renderer contract gaps

Checked on 4 November 2026. `PHASE_1_REPORT_RENDERER_CONTRACT.md` resolves A1–A8 and B9–B10.

The gaps below are where the contract, the approved template and the engine's data still do not meet. Items 1–8 block the renderer. Each needs a founder answer in the renderer contract source, recopied here.

### Done in the engine (this commit)

- **Review record.** `review-record --outcome passed|passed-after-correction|blocked|escalate --severity none|minor|major|critical` stores the exact `REPORT_OUTPUT_QA.md` wording.
  - Only the two passing outcomes allow `build`.
  - `major` or `critical` resets the clean-run count, even when the content was later corrected and passed.
  - "Content passed" requires severity `none`, because QA defines it as no defect found.
  - "Content passed after correction" requires a severity above `none`.
- **`current_service`** on each service page. It holds the household's own facts, in the field order of contract §4, and is printed in the approval pack.
- **`totals`** (contract §3), summed from the displayed whole-pound figures so they reconcile with each page.
- **`effort`** on each priority action.
- **Contract version.** `docs/REPORT_DATA_CONTRACT.md` is now v1.1.

### Gaps that block the renderer

1. **Energy "Monthly payment: £X" has no number to use.**
   - `facts.approximate_payment` holds the customer's own wording, for example "about £95 a month". The spec's worked example (`LIVE_CASE_CALCULATOR_SPEC.md:250`) even gives an annual range.
   - `current_service.monthly_payment_gbp` is therefore null for now.
   - Decide between two options:
     - add a numeric `approximate_monthly_payment_gbp` fact, recorded by Operations from the customer's answer;
     - show founder-approved display text instead.
2. **The fixed energy sentence is not always true.**
   - "This uses your current tariff and estimated energy use…" is mandatory on every Energy page (contract §4).
   - It is untrue when the customer supplied actual 12-month usage.
   - When the bedroom fallback is used, it repeats the estimate note ("Your consumption was estimated from households with similar characteristics.").
   - Decide on wording per consumption source, or whether this sentence replaces the estimate note.
3. **"Similar services cost" is missing "about".** `MEMORY.md:35` and QA §3 require "about £X" for this figure. The contract §4 figure row gives only the label. Confirm the value renders as "about £X". `comparison_text` already says "Similar services cost about £X a year."
4. **No place for the energy saving.**
   - The contract's totals include any founder-shown saving, and energy can have one (payment-method or tariff-fit difference).
   - Contract §4 lists only monthly payment and estimated annual cost for the Energy page.
   - Decide whether an Energy page shows a founder-approved potential saving, and where.
5. **Overview columns.**
   - Contract §3 lists: label, annual spend, market position, potential saving and selected next action.
   - The template's page 2 has a Health score column and no next-action column.
   - Confirm the columns. Since market position is now the score band, a separate score column may be redundant.
6. **Priority chips.**
   - Pages 3 and 7 show "High priority / Medium priority / None" chips and a Priority column.
   - The contract says not to map the founder's numeric priority to labels, but does not say what replaces the chip.
   - Decide whether to remove it or show something else.
7. **Text slots with no data source.** Map each slot to an existing approved field (`headline`, `explanation`, `next_step`, `summary`, `findings`) or name a new founder-approved field:
   - page 1: "Our top recommendation" (title and sentence);
   - service pages: "How it compares" (sentence) and "Our recommendation" (title and sentence);
   - page 2: the summary under the totals ("Focus on broadband and electricity…");
   - page 3: "Why these priorities?";
   - page 7: "If you only do one thing…", "Staying put is still a useful outcome" (paragraph) and "We are here to help" (fixed text or founder text).
8. **Display wording for codes and dates.**
   - Contract and tariff end: `out_of_contract`, `unknown` and `no_end_date`.
   - Date format: the template uses "18 Sep 2026"; the engine's long form is "18 September 2026".
   - Mobile Plan type: `sim_only` and `handset_included`.
   - Unlimited data.
   - Energy Services: `both`, `gas` and `electricity`.
   - The template's mobile example shows "No contract", but the spec has no such value. Is a rolling monthly plan `out_of_contract`?

### Repository hygiene

9. **`docs/governing/DECISION_REGISTER.md`.**
   - It was added in 9f65464 but is not listed in `docs/governing/README.md`.
   - It is the company-wide decision register (524 lines). It includes mailbox security set-up, pilot data handling and other matters that do not govern this engine.
   - `MEMORY.md:62` links to it, which is presumably why it was copied.
   - Recommendation: remove it from the repo, or list it in the README as context only. Either way, confirm the GitHub repo is private.

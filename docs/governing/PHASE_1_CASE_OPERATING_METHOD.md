# Phase 1 Case Operating Method

## Status and authority

- **Owner:** Operations.
- **Status:** Founder-approved ordinary-case authority from 19 August 2026.
- **Purpose:** Run one household case from supplied information to delivered Bills Health Report with the fewest safe handoffs.
- **Customer journey:** [PHASE_1_EMAIL_UX.md](PHASE_1_EMAIL_UX.md).
- **Calculations:** [LIVE_CASE_CALCULATOR_SPEC.md](LIVE_CASE_CALCULATOR_SPEC.md), the implemented calculator, the Evidence-owned live offer method and the CEO score method.
- **Recommendation:** [PHASE_1_RECOMMENDATION_FRAMEWORK.md](../ceo/PHASE_1_RECOMMENDATION_FRAMEWORK.md).
- **Visual authority:** `/Users/anton/billvisor/design/report/`.
- **Renderer contract:** [PHASE_1_REPORT_RENDERER_CONTRACT.md](PHASE_1_REPORT_RENDERER_CONTRACT.md).
- **Review authority:** [REPORT_OUTPUT_QA.md](../review/REPORT_OUTPUT_QA.md).

This document is the sole Operations process authority for an ordinary live case. The detailed calculator specification is a technical reference and is not routine case-reading material. Evidence, Review, CEO, Research, Marketing and Compliance are activated only under the triggers below.

## 1. Ownership

Operations owns an ordinary case end to end:

- intake and service classification;
- the smallest founder search request;
- deterministic calculation;
- proposed recommendation and customer wording;
- one consolidated founder approval package;
- required Review coordination;
- final HTML generation;
- correction, delivery and record completion.

The founder:

- supplies the customer facts extracted under the approved data controls;
- performs any interactive market search requested by Operations;
- approves the recommendation and exact customer-facing content;
- checks the final HTML visually, saves it as PDF and decides whether to deliver it.

Evidence is not part of an ordinary case. Call Evidence only for:

- a new provider assessment;
- a missing or ambiguous source or method rule;
- a material evidence conflict; or
- a case the approved calculator cannot safely process.

CEO is not involved in ordinary production. Escalate only a genuinely unresolved policy or cross-team decision. Compliance is activated only for a privacy, safety, service-boundary or material data-flow issue. Research analyses case batches rather than producing individual reports. Marketing has no case role.

## 2. Ordinary case sequence

### Step 1 — Record the submitted case

Use one structured case JSON and the approved pilot workbook. Record only:

- case/report identifier and first name;
- services requested;
- agreed minimum customer facts;
- material volunteered context;
- masked source references;
- workflow, approval, correction and delivery fields.

Do not place original bills, account numbers, full payment details, identity documents or unnecessary personal data in the case record or any agent task.

Assign every supported service one coverage status:

- **Analysed**;
- **Analysed with limitations**; or
- **Not analysed**.

If the customer supplied the agreed minimum information for an ordinary supported case, treat the customer submission as sufficient. Information Billvisor deliberately chose not to request is not missing and is not a limitation. A genuine internal evidence or method gap may still make the service **Analysed with limitations**.

### Step 2 — Return one founder search request

Operations identifies which requested services need current market captures and responds once with the smallest practical search checklist.

For broadband/mobile, request pasted results for broadly comparable packages only. For Energy, request only the accessible tariff/rate information required by the approved three-check method. Do not request an exhaustive market pack, provider catalogue, source register, screenshots when pasted content is sufficient or information unrelated to the intended calculation.

### Step 3 — Calculate in Operations

When the founder supplies captures, Operations applies the implemented deterministic calculator inside the same case record.

For broadband/mobile:

- calculate each usable offer's first-12-month effective monthly price;
- include compulsory charges shown and known promotional periods/rises;
- exclude rewards;
- group by provider and calculate each provider mean;
- use the median provider mean as the comparison;
- calculate current annualised spend, potential saving and the approved score trace.

For Energy:

- use actual annual kWh, then supplier-estimated annual kWh, then the approved bedroom fallback where permitted;
- calculate annual tariff cost from unit rates and standing charges;
- perform only the approved payment-method, tariff timing/constraint and wider-review checks;
- use an approved Energy score when either the narrow like-for-like payment-method conditions are met, an electricity-only Economy 7 case has actual peak/off-peak readings and a matched regional Direct Debit single-rate reference over the same billing-day sample, or a current tariff is compared with a relevant accessible tariff using the same selected household-consumption input, geography, fuels, meter type and payment basis. The last route is a price-only tariff-fit score, not an alternative-provider or whole-market comparison.

Retain the smallest reproducible trace in the case record. Do not create a separate Evidence pack or long narrative analysis. The calculator does not choose the recommendation.

### Step 4 — Apply the recommendation framework

Use the approved sequence and select one concrete action:

- Stay put;
- Improve the current setup;
- Look at changing now;
- Review later; or
- Confirm information.

The service score informs but does not dictate the recommendation. Consider supported financial value, service position, Low/Moderate/High action effort and timing/known constraints. Contract status affects timing and practicality, not the current score. The only approved exception is the Bills Health Score method's explicit `small_saving_not_worth_effort` adjustment: use it only for a founder-approved Stay put outcome where the supported saving is below £50 and effort is the stated reason.

Until numeric recommendation thresholds are approved, Operations proposes the action and reasoning and the founder makes the final recommendation decision.

### Step 5 — Present one consolidated approval package

Do not generate the final HTML yet. Present one compact package containing:

1. supplied facts and coverage status by requested service;
2. internal comparison, saving and score results;
3. the proposed recommendation and short reason;
4. the exact delivery email;
5. every customer-facing report field and paragraph in page order;
6. the one material limitation per affected service; and
7. any required Review trigger.

Keep provider means, individual offers, named comparison sources, source lists, sample arithmetic and internal method language out of customer-facing content. Never expose the word **benchmark**, specific deals, a £0 saving, a guaranteed saving, a best-deal claim or implied whole-market coverage.

The founder approves or amends the package in ordinary language. Record the approved version, date and content fingerprint. Any material customer-facing change invalidates the approval.

## 3. Risk-based Review

Review is required when any one of these applies:

1. the report is among the first five live reports under this operating method;
2. the calculator fails, a manual override is proposed, or a new/ambiguous method is used;
3. the primary recommendation is **Look at changing now** while the recommendation framework remains unvalidated; or
4. after five clean reports, the case is the next one-in-five spot-check case.

Operations initiates Review and supplies only the exact approved case package required by `REPORT_OUTPUT_QA.md`. The founder does not coordinate the handoff.

Review checks faithful transfer, arithmetic, service statuses, contradictions, cross-case contamination, unsupported decision-driving values and internal-only leakage. It does not redo market research, choose the recommendation, inspect the final HTML visually or review the exported PDF.

If a reviewed report contains a Critical or Major defect, reset the clean-report count and require Review on subsequent reports until five consecutive reviewed reports pass without a Critical or Major defect. CEO must reassess the sampling rule if defects recur.

For a non-sampled ordinary case with no Review trigger, the deterministic validation pass replaces the Review fingerprint gate. The founder content-approval fingerprint remains mandatory.

## 4. Generate and deliver

After founder approval and either the required Review pass or the valid no-Review deterministic gate:

1. generate one complete fixed-A4 browser-openable HTML report from approved, fingerprinted report data and approved page sources, following the renderer contract;
2. include a service page for every Analysed or Analysed-with-limitations unit and none for Not-analysed services;
3. show one Energy row/page when gas and electricity share one analysis, otherwise use separate units;
4. apply correct Good/Medium/Poor score values, arcs and green/amber/red colours;
5. order priority actions by priority, then potential saving when priority is equal;
6. keep page numbering, case reference, report version and delivery email consistent;
7. refuse generation when the founder fingerprint, required Review result or deterministic validation gate is missing or stale.

The founder opens the HTML locally and checks page order, wording, figures, statuses, colours, icons, margins, page breaks, overflow, blank pages and broken assets. The founder then selects Print/Save as PDF, uses A4 with background graphics enabled, checks the preview and saves the approved case/version filename.

There is no automated/headless PDF renderer, PDF preflight artifact or post-export Review step in Phase 1.

Deliver the recommendation summary in the email, attach the PDF and invite free clarification and factual corrections.

## 5. Completion and retention

Record:

- final content version and founder approval;
- calculator/validation result;
- whether Review was required and its result;
- final HTML path and exported PDF filename;
- delivery date;
- correction or supersession reference;
- source-document final-needed and deletion dates; and
- founder active time when reported.

Apply the approved service-record and source-document retention rules. Do not create archive copies of obsolete report outputs or source documents.

## 6. Compact checklist

- [ ] Requested services and agreed minimum facts recorded once.
- [ ] Deliberately unrequested information not treated as missing.
- [ ] One smallest founder search request sent.
- [ ] Deterministic calculation completed or bounded exception escalated.
- [ ] One recommendation selected under the CEO framework.
- [ ] One consolidated founder approval package approved and fingerprinted.
- [ ] Review trigger checked; required Review completed or valid deterministic no-Review gate recorded.
- [ ] Customer content contains no internal sources, arithmetic, specific deals or unsupported claims.
- [ ] Final HTML generated from the exact approved content.
- [ ] Founder visual check and manual PDF export completed.
- [ ] Matching email/PDF delivered and records completed.
- [ ] Source-document deletion date controlled.

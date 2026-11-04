# Phase 1 Report Pre-Export Data/Content QA

## Status and authority

- **Owner:** Review, supporting Operations.
- **Files:** Save this reusable standard in `context-files/review/` and completed case QA records in `data-files/review/`.
- **Requirement:** Review performs structured pre-export data/content QA only when a trigger in the [Phase 1 Case Operating Method](../operations/PHASE_1_CASE_OPERATING_METHOD.md) applies.
- **Final authority:** After any required Review pass and corrections, Operations generates the fixed-A4 HTML. A non-sampled ordinary case instead requires a valid deterministic validation gate. Founder content approval is mandatory in both routes. The founder checks the HTML visually, manually saves it as a PDF and decides whether to deliver it.
- **Must follow:** [CEO memory](../ceo/MEMORY.md), the [Agent Operating Model](../ceo/AGENT_OPERATING_MODEL.md), the [Phase 1 Case Operating Method](../operations/PHASE_1_CASE_OPERATING_METHOD.md) and the [Phase 1 UX](../operations/PHASE_1_EMAIL_UX.md).

## Purpose

Check that the proposed report data, customer-facing wording and delivery email faithfully reflect the approved household facts, founder-supplied market captures, deterministic calculation output, any exceptional Evidence return and founder decisions. Review checks arithmetic, totals, service statuses, contradictions, omissions, duplication, cross-case contamination, unsupported decision-driving values and internal-only leakage.

Review does not redo Evidence research, choose or reassess the recommendation, decide whether a saving is useful, choose green or amber, or invent thresholds or rounding rules. Review does not inspect final HTML visually, inspect the founder-exported PDF or perform rendering QA.

Operations remains accountable for ordinary case calculation, report content and corrections. Evidence remains accountable for its methods, source guidance, provider research and any exceptional return. The founder remains accountable for the recommendation, customer-facing wording, visual check, PDF export and delivery decision.

## When Review is required

Operations sends a case to Review when it is among the first five live reports under the current operating method; when the calculator fails, a manual override is proposed, or a new/ambiguous method is used; when the primary recommendation is **Look at changing now** while the recommendation framework remains unvalidated; or when it is the scheduled one-in-five spot check after five clean reports. A Critical or Major defect resets the clean-run count as defined by the case operating method. Review does not decide whether a trigger applies or coordinate sampling.

## Required inputs

Review receives the exact pre-export set for one case:

- the approved household facts or structured case record;
- the Operations calculation trace and founder-supplied capture references, plus any exceptional Evidence return where relevant;
- the founder's approved recommendation and content decisions, with version and approval record;
- the proposed customer-facing report data and wording in page order;
- the proposed delivery-email text.

Review does not require final HTML, a PDF, renderer output, preflight data or raw market-research captures. Raw household documents are not normal Review inputs. If an approved fact or Evidence value cannot be traced in the supplied set, Review flags the exact gap without conducting replacement research.

## Pre-export QA checklist

### 1. Case and approval integrity

- [ ] Every input belongs to the same case and content version.
- [ ] Founder approval is recorded for the recommendation and proposed customer-facing content being reviewed.
- [ ] The household name and any other identifying fields agree across the proposed report and delivery email.
- [ ] No fact, value, wording or decision from another case appears.
- [ ] No material content change has been introduced after founder approval without renewed approval.

### 2. Faithful transfer and traceability

- [ ] Each customer-supplied fact matches the approved household facts and retains the correct source status where shown.
- [ ] Each market-derived value matches the approved deterministic calculation output; each provider-quality or exceptional value matches the applicable Evidence authority or return.
- [ ] The recommendation, reasons, outcome, service conclusions and next action match the founder's decisions.
- [ ] Every decision-driving value in customer-facing content has a traceable approved household-fact, Evidence-return or founder-decision source.
- [ ] No unsupported value, source, assumption, saving, score, conclusion or recommendation has been introduced.
- [ ] Every numeric Bills Health Score and band recomputes correctly from the complete trace required by [BILLS_HEALTH_SCORE_METHOD.md](../ceo/BILLS_HEALTH_SCORE_METHOD.md); fictional approved-template values never carry into a live case.
- [ ] The report and delivery email agree on the recommendation, reasons, action, timing and any decision-driving figures.

Review verifies transfer and traceability. It does not decide whether Evidence should have selected different packages, grouped providers differently, calculated another benchmark or supported a different recommendation.

### 3. Calculations, totals and display values

- [ ] Review independently checks report-level arithmetic using the supplied approved inputs, without reopening Evidence research.
- [ ] Current annual spend equals the submitted monthly payment multiplied by 12.
- [ ] Service annual figures, breakdowns and combined totals reconcile without omission or double counting.
- [ ] For broadband or mobile, the internal annual comparison figure equals the supplied internal monthly comparison value multiplied by 12.
- [ ] Where the founder approved an estimated potential annual saving, its internal value equals current annual spend minus the internal annual comparison figure and is positive.
- [ ] All customer-facing annual figures are rounded to the nearest whole pound and match the approved displayed values.
- [ ] Current annual spend is labelled as annualised from the submitted monthly payment, is not described as a forecast and does not use “about”.
- [ ] The customer-facing similar-services comparison uses “about” and does not expose the internal word “benchmark”.
- [ ] A displayed potential annual saving is clearly identified as an estimate, does not use an additional “about” prefix and is never £0.
- [ ] Exact internal values, provider-level averages, individual offers, source lists, sample arithmetic and research-process detail remain internal.

Review may recompute multiplication, addition, subtraction, reconciliation and the approved customer-display rounding from supplied values. It must not reconstruct or reassess Evidence's package calculations, provider means, median selection or research choices. If a rounding case requires an unapproved convention, Review escalates rather than inventing one.

### 4. Service statuses and conditional content

- [ ] Broadband, mobile, gas and electricity each use exactly one approved coverage status: **Analysed**, **Analysed with limitations** or **Not analysed**.
- [ ] A service marked **Analysed with limitations** identifies a genuine missing agreed minimum field or internal evidence gap; deliberately unrequested information is not presented as a limitation.
- [ ] A price-only health score is used only where price position is supportable but provider quality is unavailable, and the customer wording states that boundary briefly. No numeric score appears when price position cannot be established.
- [ ] A negative provider-quality explanation appears between price comparison and recommendation only when the combined 90/10 service score is in a lower band than the price-only score; it is absent otherwise, never praises a strong provider and uses the correct service-specific quality areas without exposing internal ranks, table positions or scores.
- [ ] Provider wording does not call the evidence “reviews,” label the provider simply good or bad, or imply whole-market coverage.
- [ ] “Public data” is used only when the supporting material is genuinely publicly accessible; the exact sources, dates, covered periods, limitations and calculation are retained internally.
- [ ] The report includes “Supporting source details are available on request” once, without repeating it on each service page.
- [ ] Each status agrees with the approved structured content.
- [ ] Analysed and Analysed-with-limitations services have the required service content; Not-analysed services appear only in the overview and have no service page.
- [ ] Conditional fields appear only when supported and required; empty placeholders do not appear.
- [ ] Information Billvisor deliberately did not request is not presented as a missing-data limitation.
- [ ] A service with no genuine limitation has no limitation placeholder such as “No material limitation recorded”.
- [ ] The broadband/mobile offer-list comparison is not applied to energy.
- [ ] A founder-approved green outcome uses reassuring affirmative wording that confirms when staying put is sensible; Review does not choose the outcome or assess visual styling.

### 5. Internal consistency and completeness

- [ ] Overview, service sections, recommendation summary, reasons and action plan do not contradict one another.
- [ ] Required services, sections, findings, actions and limitations are neither missing nor duplicated.
- [ ] Dates, prices, providers, packages, statuses and totals are consistent wherever repeated.
- [ ] Unsupported whole-market, best-deal, guaranteed-saving or switching-service wording does not appear.
- [ ] Named comparison sites, source lists, provider-level averages, individual sampled offers and internal research language do not appear in customer-facing content.
- [ ] Internal workflow fields, approval notes, evidence references and analyst instructions do not appear in customer-facing content or the delivery email.
- [ ] The proposed delivery email gives the same answer as the report and does not add unsupported claims or actions.

## Review boundaries and escalation

Review must not silently repair an unsupported or contradictory value, rewrite the recommendation, change founder-approved wording or substitute its own evidence judgement.

- Return transfer, arithmetic, status, contradiction, duplication, omission and leakage defects to Operations with exact locations and required corrections.
- Send a clearly identified source or Evidence-calculation discrepancy to Evidence through Operations; do not investigate it independently.
- Send possible privacy, safety or service-boundary conflicts to Compliance.
- Escalate unresolved policy, methodology or founder-decision conflicts to CEO.
- Any correction that changes approved customer-facing wording, figures, status, recommendation or meaning requires founder approval before final HTML generation.

## QA results

Record one result:

- **Content passed:** no pre-export data/content defect was found. Operations may generate the final HTML from this exact approved content.
- **Content passed after correction:** named defects were corrected, any required founder approval was recorded and Review rechecked the exact replacement content.
- **Content blocked:** a transfer, arithmetic, status, contradiction, omission, duplication, cross-case or internal-leakage defect prevents final HTML generation.
- **Escalate before delivery:** the content exposes a possible policy, methodology, privacy, safety or founder-decision conflict outside Review's authority.

A Content passed result is not visual approval, PDF approval or delivery approval. There is no post-export Review step.

## Defect severity

- **Critical:** wrong-household or cross-case content, exposed personal data, or a defect that materially changes the approved recommendation or action. Stop the case.
- **Major:** unsupported or missing decision-driving value; calculation or total error; wrong service status; material contradiction; missing or duplicated required content; report/email mismatch; prohibited internal-only content; £0 saving; guaranteed-saving or unsupported whole-market wording. Correct before final HTML generation.
- **Minor:** non-decisive wording-transfer, label or consistency defect that does not alter the approved meaning. Correct before final HTML generation where practical.

## Review record

```text
Case reference:
Approved content version:
Founder content approval date and time:
Review date and time:
QA result:
Calculation and total checks:
Service-status checks:
Critical defects:
Major defects:
Minor defects:
Corrections checked:
Renewed founder approval, if required:
Escalation, if any:
```

The Review record must not duplicate source documents, raw research captures or unnecessary household information. Retain it under the approved service-record policy.

## Completion and handoff

After Content passed:

1. Operations generates the final fixed-A4 HTML from the exact passed content.
2. The founder checks the HTML visually, manually saves it as PDF with print backgrounds enabled and decides whether to deliver it.
3. Review does not inspect the final HTML or exported PDF and does not perform a post-export check.

# Energy Provider Scoring Method

## Ownership and authority

- **Owner:** Evidence.
- **Files:** This methodology belongs in `context-files/evidence/`; provider research, observations and generated outputs belong in `data-files/evidence/`.
- **Authority:** Governs Great Britain residential gas-and-electricity retail-supplier scoring only, overriding the generic method only where explicitly stated.
- **Must follow:** [CEO memory](../../../ceo/MEMORY.md), [Agent Operating Model](../../../ceo/AGENT_OPERATING_MODEL.md) and all non-conflicting rules in [PROVIDER_SCORING_METHOD.md](../PROVIDER_SCORING_METHOD.md).
- **Does not define:** household recommendations, tariff value, regional offer availability, customer-facing wording or recommendation-algorithm rules.

## Scope

This method applies to domestic gas and electricity retail suppliers serving England, Scotland and Wales. Northern Ireland energy remains outside Phase 1 and requires a separate market method before inclusion.

The score measures retail-supplier quality and customer administration. It does not measure tariff price, estimated household cost, tariff suitability, environmental claims or local network performance.

## Founder-approved calculation

`Overall score = (Billing & Metering × 50%) + (Customer Support & Complaint Resolution × 50%)`

- The two-category structure and equal weights are founder-approved for Phase 1.
- The 50% / 50% split is a deliberate simplification following the evidence review; it is not established by external data as the objectively optimal weighting.
- Use 0.5-point category scores on a 0–10 scale.
- Calculate the weighted result, then round the overall quality score to the nearest 0.5 point.
- Keep quality and confidence separate and apply the generic confidence rules when comparing providers.

## Founder-approved categories and weights

| Category | Weight | Assess |
|---|---:|---|
| Billing & Metering | 50% | Bill accuracy and clarity, meter-reading use, smart-meter operation where the supplier controls the outcome, payment and direct-debit administration, final bills, refunds, credits and correction of billing errors. |
| Customer Support & Complaint Resolution | 50% | Contactability, response times, support quality, complaint incidence, complaint handling, resolution and appropriate escalation or signposting. |

Account and switching administration is not a separate scored category. Relevant evidence maps only to Billing & Metering or Customer Support & Complaint Resolution when it directly measures one of those outcomes. Other switching or account-administration incidents remain documented context or caution evidence and must not receive invented numeric points.

## Explicit exclusions

- Do not score physical gas or electricity network reliability as supplier performance. Distribution and transmission failures are generally outside the retail supplier's control.
- Do not put price, tariff competitiveness or postcode-level offer availability into this provider-quality score. Assess them separately for the household.
- Do not treat renewable claims, fuel mix or marketing commitments as proof of service quality.

## Regulatory and financial caution overlay

Serious regulatory or financial concerns do not receive a numeric weight and must not be averaged away by stronger service scores. Record an evidence-backed **Caution** status separately where the approved evidence rules require it.

The caution overlay is a provider-risk signal for manual consideration. It does not itself define the household recommendation.

### Caution evidence rules

Apply a Caution status only when current, provider-specific official evidence establishes a material concern, including:

- a final or active Ofgem enforcement decision, order, licence restriction or formal compliance finding involving material household harm;
- an official licence revocation, supplier exit or Supplier of Last Resort process; or
- a provider-specific official financial-resilience warning or intervention.

An open investigation, consultation, allegation or media report is not a finding. Record it in the research log as unresolved context unless Ofgem has imposed interim measures or issued an explicit consumer warning. Removing a Caution status requires documented resolution and fresh evidence; it does not expire automatically.

## Research source hierarchy

Use this hierarchy for every energy score. The exact source, publication date, covered period, provider or group coverage, limitations and conflicts must be logged in the future energy research log.

| Priority | Source | Use it for | Limitation |
|---:|---|---|---|
| 1 | [Citizens Advice Energy Supplier Star Rating and underlying quarterly data](https://www.citizensadvice.org.uk/policy/publications/historic-star-rating-data/) | Billing and metering measures; contact-channel performance; weighted serious complaints; supplier comparison and trends. | Some measures are supplier-reported. Coverage has a customer-size threshold. The overall Star Rating contains inputs that overlap with its category data and includes Customer Commitments, which Billvisor does not score. |
| 1 | [Ofgem customer-service and complaints data](https://www.ofgem.gov.uk/energy-data-and-research/data-portal/customer-service) and [Energy Consumer Satisfaction Survey](https://www.ofgem.gov.uk/research/energy-consumer-satisfaction-survey-january-2026) | Supplier complaint volumes and resolution; supplier-level satisfaction where published; billing, contact and switching context; market baselines. | Supplier-level survey results cover only some supplier groups and some measures are market-level. Supplier-reported complaint data can contain missing or disputed points. Market-wide switching satisfaction cannot establish a supplier-specific score. |
| 1 | [Energy Ombudsman complaints data](https://www.energyombudsman.org/complaints-data) | Accepted and resolved disputes, complaint types, awards and evidence of unresolved serious problems. | Usually covers only the largest suppliers individually. It sees only escalated cases and signposting affects volumes. Its data also feeds Citizens Advice and Ofgem publications, so it is not automatically independent corroboration. |
| 2 | [Ofgem compliance and enforcement publications](https://www.ofgem.gov.uk/energy-regulation/how-we-regulate/compliance-and-enforcement) | Final findings involving billing, metering, complaints, switching, account administration or consumer treatment; caution assessment. | An investigation is not a finding. Historic or isolated cases must be dated and assessed for current relevance. |
| 2 | [Ofgem financial-resilience publications](https://www.ofgem.gov.uk/energy-regulation/business-resilience/financial-resilience) | Provider-specific official resilience concerns and caution assessment. | Public provider-comparable evidence may be limited. Absence of a public warning is not proof of financial strength. Do not convert this evidence into numeric service-quality points. |
| 3 | Methodologically transparent independent consumer research | Corroborating provider-level experience where the regulator or statutory consumer evidence is incomplete. | Check sample frame, supplier sample size, weighting, fieldwork dates, question wording and commercial conflicts. Do not mix price or value ratings into provider quality. |

### Category mapping

| Evidence | Primary category | Rule |
|---|---|---|
| Billing accuracy, bill clarity, meter-reading use, smart-meter operation, direct-debit errors, refunds and credit correction | Billing & Metering | Use provider-comparable outcomes. A market-wide statistic is context only. |
| Contact waiting or response time, accessibility of contact channels, complaint rate, complaint resolution and Ombudsman escalation | Customer Support & Complaint Resolution | Distinguish initial complaints from unresolved escalations and use account-normalised rates where available. |
| Final bills, transfer of credit or refunds and billing-related account closure | Billing & Metering | Use only provider-comparable billing outcomes. Do not score general switching satisfaction or account opening as a substitute. |
| Switching, cancellation or account-administration incidents not directly measuring billing or complaint outcomes | No numeric category | Record as evidence context or assess against the caution rules. Do not invent numeric points. |
| Ofgem enforcement or formal compliance evidence | Relevant category and/or Caution | Move a numeric category only where the finding concerns that category and remains relevant. Apply Caution separately when the approved trigger is met. |
| Financial-resilience evidence | Caution only | Never award or deduct routine service-quality points from financial evidence. |

## Anti-double-counting rules

- Treat the Citizens Advice overall Star Rating as a sense check, not a scoring input. Use its relevant underlying categories instead; exclude Customer Commitments from the Billvisor score.
- Treat a complaint included in Energy Ombudsman data and then incorporated into the Citizens Advice weighted complaints basket as one evidence family, not two independent confirmations.
- Ofgem, Citizens Advice and Energy Ombudsman publication of the same underlying dataset does not make it independent evidence.
- Successive waves of the same measure establish a trend, not several independent sources.
- Map evidence to one primary category. Use it in another category only where the source measures a distinct outcome relevant to that second category, and document why.
- General satisfaction may corroborate a category conclusion but must not outweigh more direct outcome measures.
- Missing comparable evidence lowers confidence. It must not be replaced with an assumed neutral score, a group score or the market average.

## Sources not used to set scores

- Provider advertising, awards, testimonials and unverified performance claims.
- Individual reviews, social posts, Reddit and Trustpilot-style platforms.
- Price-comparison rankings or commercial awards mixing price, value, commission or editorial preference with service quality.
- Self-selecting polls without adequate methodology and supplier-level sample sizes.

Provider terms, help pages and complaints codes may verify administrative facts, but are not independent evidence of performance.

## Initial research universe

Begin with these six domestic supplier groups:

- Octopus Energy;
- British Gas;
- E.ON Next;
- OVO Energy;
- EDF Energy; and
- ScottishPower.

This list is based on Ofgem's 27 January 2026 State of the Market report using Q2 2025 market-share data. The six held the largest reported domestic electricity and gas shares in that table. It is an evidence-prioritisation decision, not a claim that they are the best suppliers or the only suppliers relevant to households.

Expand the research universe when:

- another supplier appears in a real customer's current services; or
- another supplier appears among credible available alternatives relevant to a live review.

The additional supplier must be researched before Billvisor makes a provider-quality claim about it. If decision-quality evidence cannot be established in time, record insufficient evidence and apply the generic confidence and Conditional rules rather than inventing a score.

### Supplier group and retail-brand rule

- Record the customer-facing retail supplier and relevant licensed entity where identifiable.
- Do not automatically transfer a supplier-group score to a separately operated retail brand or white label.
- If an official source reports only at group level, log the covered entities and period. Use it for a retail brand only where applicability is supported; otherwise reduce confidence or record insufficient evidence.
- Recheck the core universe when Ofgem publishes a material market-share update and at least every six months.

## Pending founder approval

The following are deliberately not yet defined:

- numeric normalisation thresholds for turning unlike source measures into 0–10 category scores;
- internal sub-weighting of contactability versus complaint incidence and resolution inside Customer Support & Complaint Resolution;
- energy score-table and research-log fields;
- refresh events beyond the generic six-month minimum.

No provider should be scored under this method until these rules are approved.

# Broadband Provider Scoring Method

## Ownership and authority

- **Owner:** Evidence.
- **Files:** This methodology belongs in `context-files/evidence/`; provider research and scores belong in `data-files/evidence/`.
- **Authority:** Governs UK fixed residential broadband scoring only, overriding the generic method only where explicitly stated.
- **Must follow:** [CEO memory](../../../ceo/MEMORY.md), [Agent Operating Model](../../../ceo/AGENT_OPERATING_MODEL.md) and all non-conflicting rules in [PROVIDER_SCORING_METHOD.md](../PROVIDER_SCORING_METHOD.md).
- **Does not define:** household recommendations, offer value, postcode suitability by itself, customer-facing wording or recommendation-algorithm rules.
- **Evidence separation:** Provider-specific evidence and reasoning belong in the research log; the concise score table remains restricted to its approved fields.

## Scope
Applies only to UK fixed residential broadband providers. It overrides [PROVIDER_SCORING_METHOD.md](../PROVIDER_SCORING_METHOD.md) only for explicitly stated broadband rules, including categories, weights, evidence inputs and broadband-specific constraints. All other generic rules continue to apply.

## Calculation
`Overall score = (Customer Support × 35%) + (Service Reliability × 50%) + (Switching Experience × 15%)`

Use 0.5-point category and overall scores.

## Categories and evidence
| Category | Weight | Assess | Preferred evidence |
|---|---:|---|---|
| Customer Support | 35% | Complaint rate, complaint handling, first-contact resolution, call waits, support quality. | Ofcom complaints and service-quality reports; Which? service/support evidence. |
| Service Reliability | 50% | Connection reliability, speed consistency, outages and technical performance. | Ofcom reliability/speed satisfaction; Which? reliability/dropout evidence; credible independent performance or outage research. |
| Switching Experience | 15% | On-time installation, provisioning, migration, cancellation and switching-related complaints. | Ofcom installation and provisioning data; automatic-compensation participation; credible onboarding/cancellation evidence. |

## Research source hierarchy
Use this hierarchy for every broadband score. Keep this list here because it applies to the service type; log the exact source, publication date, covered period and limitation in [BROADBAND_PROVIDER_RESEARCH_LOG.md](../../../../data-files/evidence/provider-scoring/broadband/BROADBAND_PROVIDER_RESEARCH_LOG.md).

| Priority | Source | Use it for | Limitation |
|---:|---|---|---|
| 1 | [Ofcom quarterly telecoms complaints](https://www.ofcom.org.uk/telecoms-and-pay-tv-complaints) | Fixed-broadband complaints per 100,000 customers; complaint drivers; recent changes. | Covers only providers in Ofcom's reporting set; complaints received by Ofcom are not all customer complaints. |
| 1 | [Ofcom Comparing Customer Service](https://www.ofcom.org.uk/phones-and-broadband/service-quality/report?language=en) | Overall satisfaction, perceived reliability and speed, reasons to complain, complaint handling, first-contact resolution, call waits, abandonment and on-time installations. | Periodic rather than continuous; some providers or measures lack a sufficient sample. |
| 2 | [Which? broadband surveys and methodology](https://www.which.co.uk/reviews/broadband/article/how-we-assess-broadband-aOshb8V6zkye) | Recent customer experience: reliability, speed, support, contactability, technical support, communication and dropouts. | Detailed provider results may be paywalled; customer perception is not independently measured uptime. |
| 2 | [Opensignal UK Fixed Broadband Experience](https://insights.opensignal.com/reports/2025/12/uk/fixed-broadband-experience) | Independently measured provider-level reliability experience, consistent quality, download/upload speed and video experience; use primarily for Service Reliability. | Covers only reported providers and observed users; results reflect provider technology, footprint, user/device mix and measurement methodology, so they are not pure network uptime or postcode-level suitability. |
| 3 | [MoneySavingExpert / YouGov customer-service ratings](https://www.moneysavingexpert.com/team-blog/2026/05/broadband-service-poll-blog/) | Recent, comparable customer-support cross-check; useful for providers with lighter regulator coverage. | Customer service only; use as corroboration, not a replacement for regulator evidence. |
| 3 | [thinkbroadband coverage and performance data](https://labs2.thinkbroadband.com/local/index.php) | Postcode/technology context, crowd-sourced speed patterns and independent availability cross-checks. | Crowd-sourced tests are not a controlled provider-quality measure; account for technology, device and selection bias. |
| 3 | [Ofcom enforcement activity](https://www.ofcom.org.uk/about-ofcom/bulletins/enforcement-bulletin) | Final decisions, fines and substantiated breaches involving cancellation, switching, complaints handling, sales conduct or service obligations; use as a dated risk flag and, where directly relevant, supporting category evidence. | An investigation is not a finding; use final decisions separately from open or closed-without-finding cases. Historic or isolated breaches must not automatically determine the current score. |
| 3 | [Ofcom Automatic Compensation Scheme](https://www.ofcom.org.uk/phones-and-broadband/service-quality/automatic-compensation-need-know) | Whether a provider participates and what protection applies for delayed repairs, missed appointments and delayed service starts; relevant context for Switching Experience and failure recovery. | Participation demonstrates a protection, not that installation, switching or fault handling is good. Restrictions can vary by network and provider. |
| 3 | [Ofcom switching research and One Touch Switch information](https://www.ofcom.org.uk/phones-and-broadband/switching-provider/switching-broadband-provider) | Governing switching process, market-wide switching friction and current consumer protections; use as a baseline when interpreting provider-level installation, migration and cancellation evidence. | Usually market-level rather than provider-comparable; do not assign the same switching score to every provider or infer provider performance from compliance requirements alone. |
| 4 | Independent telecoms reporting, including [ISPreview](https://www.ispreview.co.uk/) | Provider-specific incidents, migrations, network changes, market events and corroborating context. | Do not convert reporting or a single incident directly into a score; trace claims to primary evidence where possible. |

### Sources not used to set scores
- Provider marketing, deal pages and self-published claims.
- Individual reviews, Reddit, social posts and Trustpilot-style sites.

These may identify an issue worth investigating, but cannot set or materially move a score without stronger corroboration.

Provider terms, complaints codes, cancellation instructions and network disclosures may be used only to verify factual process details (for example notice periods, contact routes, ADR membership or access network). Record them in the provider record as administrative evidence, not independent evidence of service quality.

## Broadband-specific rules
- Treat provider quality separately from postcode-level availability, access technology and in-home Wi-Fi conditions.
- Customer-perceived reliability is not equivalent to independently measured uptime; label the evidence type.
- Do not treat an on-time installation measure as a complete switching-experience measure.
- Where a provider lacks comparable regulator coverage, retain the score only with an appropriate confidence label; a Low-confidence provider remains Conditional under the generic method.

## Output separation
- The final scoring table contains only provider name, category scores, overall score and confidence.
- Do not add citations, source dates, evidence notes, limitations or calculations to the final scoring table.
- Keep all provider-specific sources, evidence summaries, conflicts and calculation notes in [BROADBAND_PROVIDER_RESEARCH_LOG.md](../../../../data-files/evidence/provider-scoring/broadband/BROADBAND_PROVIDER_RESEARCH_LOG.md).

## Research-log template
```text
Access networks / technologies relevant to the provider:
National or regional footprint:
Reliability evidence type: customer perception / measured performance / outage data
Installation or migration evidence:
Exact sources, publication dates and covered periods:
Evidence gaps or conflicts:
```

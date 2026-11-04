# Mobile Provider Scoring Method

## Ownership and authority

- **Owner:** Evidence.
- **Files:** This methodology belongs in `context-files/evidence/`; provider research and scores belong in `data-files/evidence/`.
- **Authority:** Governs UK residential mobile-provider scoring only, overriding the generic method only where explicitly stated.
- **Must follow:** [CEO memory](../../../ceo/MEMORY.md), [Agent Operating Model](../../../ceo/AGENT_OPERATING_MODEL.md) and all non-conflicting rules in [PROVIDER_SCORING_METHOD.md](../PROVIDER_SCORING_METHOD.md).
- **Does not define:** household recommendations, tariff value, local suitability by itself, customer-facing wording or recommendation-algorithm rules.
- **Evidence separation:** Provider-specific evidence and reasoning belong in the research log; the concise score table remains restricted to its approved fields.

## Scope
Applies only to UK residential mobile retail providers, including mobile network operators (MNOs) and mobile virtual network operators (MVNOs). It overrides [PROVIDER_SCORING_METHOD.md](../PROVIDER_SCORING_METHOD.md) only for explicitly stated mobile rules, including categories, weights, evidence inputs and mobile-specific constraints. All other generic rules continue to apply.

The score measures provider quality and customer experience. It does not measure price, tariff value, data allowance, handset value or promotional attractiveness.

## Calculation
`Overall score = (Network Experience × 50%) + (Customer Support × 35%) + (Account & Switching Experience × 15%)`

- Use 0.5-point category scores on a 0–10 scale.
- Calculate the weighted result, then round the overall quality score to the nearest 0.5 point so it remains consistent with the generic method.
- Keep quality and confidence separate. Apply the generic confidence adjustment only when calculating the internal Decision score.

## Categories and evidence
| Category | Weight | Assess | Preferred evidence |
|---|---:|---|---|
| Network Experience | 50% | Coverage experience, ability to connect and complete ordinary tasks, call quality, data performance, reliability, availability, congestion and customer-perceived network experience. | Ofcom coverage and infrastructure evidence; Opensignal; RootMetrics/Ookla; umlaut; Which? network reliability; other methodologically transparent independent measurement. |
| Customer Support | 35% | Complaint rate, complaint handling, contactability, first-contact resolution, support quality, billing-issue resolution and communication. | Ofcom complaints and Comparing Customer Service; Which? service/support evidence; robust independent consumer surveys. |
| Account & Switching Experience | 15% | Activation, number porting, account management, billing and contract administration, upgrades, migrations, cancellation, leaving and substantiated unfair contract conduct. | Ofcom complaint drivers, switching research and enforcement; Which? account/contact evidence; credible provider-level switching or administration research. |

Contract duration, handset finance, roaming allowance, tariff flexibility and price are offer-level characteristics. They do not directly alter the provider-quality score unless evidence establishes a provider-wide administrative or conduct issue.

## MNO and MVNO rules
- Identify the retail provider and the underlying network separately.
- Record whether the provider is an MNO or MVNO and date the network relationship. Network access arrangements can change.
- Do not automatically copy an MNO's Network Experience score to every MVNO using its infrastructure.
- Use measured host-network performance as baseline evidence only. Check for credible evidence of provider-specific access, technology support, traffic treatment, provisioning, network-sharing access and customer-perceived reliability.
- If no MVNO-specific network evidence exists, do not invent a quality difference. Retain the best-supported score and reduce confidence to reflect the evidence gap.
- Providers sharing a host network may receive different Customer Support and Account & Switching Experience scores because those services belong to the retail brand.
- A group-owned sub-brand is still scored as its own retail provider where customers receive a meaningfully separate service, support or account experience.
- Record transitions explicitly. Vodafone and Three evidence must identify the measurement period and integration state rather than assuming that historic separate-network results describe the current combined experience.

## National score versus household suitability
The provider score is a national, directional assessment. It is not evidence that a network will work well at a specific home, workplace, commute or regularly visited location.

Local suitability must be assessed separately using current postcode- or route-level evidence, such as Ofcom's Map Your Mobile, plus relevant household information. A high national score must not override poor local coverage evidence.

## Research source hierarchy
Use this hierarchy for every mobile score. Log the exact source, publication date, covered period, provider/network coverage, limitations and conflicts in [MOBILE_PROVIDER_RESEARCH_LOG.md](../../../../data-files/evidence/provider-scoring/mobile/MOBILE_PROVIDER_RESEARCH_LOG.md).

| Priority | Source | Use it for | Limitation |
|---:|---|---|---|
| 1 | [Ofcom quarterly telecoms complaints](https://www.ofcom.org.uk/phones-and-broadband/service-quality/telecoms-and-pay-tv-complaints) | Mobile complaints per 100,000 customers, complaint drivers, trends and significant contract or service issues. | Covers only providers in Ofcom's reporting set. Complaints received by Ofcom are not all customer complaints, and short-term events can materially affect a quarter. |
| 1 | [Ofcom Comparing Customer Service](https://www.ofcom.org.uk/phones-and-broadband/service-quality/report) | Overall satisfaction, reasons to complain, complaint handling, contact channels, call waits, abandonment and other provider-level service measures. | Periodic rather than continuous; some providers or measures lack sufficient samples; much of the evidence is customer-reported. |
| 1 | [Ofcom Connected Nations](https://www.ofcom.org.uk/phones-and-broadband/coverage-and-speeds/infrastructure-research) and [Map Your Mobile](https://www.ofcom.org.uk/phones-and-broadband/coverage-and-speeds/map-your-mobile) | MNO coverage context, infrastructure change and local coverage/performance suitability. | MNO/network-level rather than retail-brand support evidence. Predicted coverage is not the same as measured experience; local results must not be folded into a national provider score without a comparable method. |
| 2 | [Which? mobile provider surveys](https://www.which.co.uk/reviews/mobile-phone-providers/article/mobile-phone-provider-reviews/best-mobile-networks-overview-amhDx1F0z41t) | Retail-brand customer experience, including perceived network reliability, customer service, technical support, contactability and communication. | Detailed results may be paywalled; perception is affected by location, device and tariff; provider sample sizes must be checked. Do not use value-for-money components in this quality score. |
| 2 | [Opensignal UK mobile network reports](https://insights.opensignal.com/uk) | User-experience measurements for underlying networks, including reliability, availability, coverage experience, speeds, consistency and successful completion of mobile tasks. | Primarily MNO-level; observed-user, device and geographic mix matter. It does not establish identical MVNO performance or local suitability. |
| 2 | [RootMetrics UK reports](https://www.ookla.com/research/reports/rootmetrics-uk-state-of-mobile-union-2h-2025) | Controlled national, nation and metro testing of network reliability, speed, data, call and text performance. | Primarily MNO-level and route/location sampled. Test methodology differs from crowdsourced measurement and does not establish MVNO-specific performance. |
| 2 | [umlaut UK Mobile Network Test](https://www.accenture.com/content/dam/accenture/final/accenture-com/document-4/Mobile-NetworkTest-UK-Connect-Umlaut-2026.pdf) | Independent drive-test and crowdsourced corroboration of MNO voice, data and reliability performance. | Primarily MNO-level. Avoid double-counting overlapping network measurements as independent retail-brand evidence. |
| 3 | [Ofcom switching research](https://www.ofcom.org.uk/phones-and-broadband/switching-provider) | Market-wide switching experience, PAC/process baselines and recurring sources of friction. | Often market-level rather than provider-comparable. Compliance with the standard PAC process does not prove a good switching experience. |
| 3 | [Ofcom enforcement activity](https://www.ofcom.org.uk/about-ofcom/bulletins/enforcement-bulletin) | Final findings involving switching, porting, cancellation, complaints, billing, contract conduct or service obligations. | An investigation is not a finding. Historic or isolated breaches must be dated and must not automatically determine current scores. |
| 3 | Methodologically transparent independent consumer surveys | Provider-specific support, account-management and perceived network evidence, especially for brands outside Ofcom's comparative reporting. | Check fieldwork, sample frame, provider sample size, weighting, question wording and commercial conflicts. Use weak or self-selecting polls only as issue-discovery evidence. |
| 4 | Specialist telecoms reporting, including [ISPreview](https://www.ispreview.co.uk/) | Provider migrations, outages, host-network changes, feature access and corroborating context. | Do not convert reporting or a single incident directly into a score. Trace material claims to primary evidence where possible. |

### Correlated evidence
Opensignal, RootMetrics/Ookla, umlaut and Ofcom coverage evidence measure overlapping parts of network experience using different methods. Triangulation is valuable, but several similar network reports must not be treated as several independent confirmations of retail-brand customer experience.

## Administrative evidence
Provider terms, help pages, complaints codes, coverage disclosures and support documentation may be used only to verify factual details such as:

- host network;
- supported network technologies and features;
- PAC, activation, cancellation and account-management routes;
- contract or notice rules;
- ADR membership;
- disclosed traffic-management restrictions.

Record these as provider-supplied administrative evidence. They are not independent proof that the provider performs well, and marketing or advertising claims must not set or materially move a score.

## Sources not used to set scores
- Provider advertising, awards, testimonials, deal pages and unverified performance claims.
- Individual reviews, Reddit, social posts and Trustpilot-style review platforms.
- Self-selecting polls without adequate methodology and provider sample sizes.
- Price-comparison rankings or commercial awards that mix price, value, commission or editorial preference with quality.

These sources may identify an issue worth investigating but cannot set or materially move a score without stronger corroboration.

## Mobile-specific scoring rules
- Customer-perceived network reliability is not equivalent to independently measured availability or task completion; label the evidence type.
- Speed alone is not Network Experience. Consider reliability, availability, coverage, congestion, call performance and successful task completion.
- Do not reward a provider merely for complying with the standard PAC or number-porting process.
- Do not penalise a provider merely for offering long contracts or handset finance; score documented administrative experience and conduct instead.
- Treat unexpected price-rise complaints as contract administration or conduct evidence, not as evidence that the absolute price is high.
- Separate nationwide provider quality from location-specific coverage, device compatibility and in-building conditions.
- Missing comparable regulator or retail-brand evidence reduces confidence; it does not justify a neutral score or an inherited group score.
- A Low-confidence provider remains Conditional under the generic method.

## Initial research universe
The founder supplied the following initial brands for future research: EE, O2, Vodafone, Three, Tesco Mobile, Sky Mobile, giffgaff, SMARTY, Lebara, VOXI and iD Mobile.

This is not yet confirmed as the complete UK provider universe. Do not add or exclude brands solely because evidence is easy or difficult to obtain. Any expanded scoring exercise must state its inclusion rule and explain additions.

## Output separation
- The final scoring table contains only provider name, underlying network, Network Experience score, Customer Support score, Account & Switching Experience score, overall quality score and confidence.
- Sort the final table by overall quality score descending. Where scores tie, apply the generic comparison rule internally; do not hide the confidence difference.
- Do not add citations, source dates, evidence notes, limitations, Decision scores or calculations to the final scoring table.
- Keep all provider-specific sources, evidence summaries, network relationships, conflicts, confidence rationale and calculation notes in [MOBILE_PROVIDER_RESEARCH_LOG.md](../../../../data-files/evidence/provider-scoring/mobile/MOBILE_PROVIDER_RESEARCH_LOG.md).

## Refresh rules
Apply the generic minimum six-month review rule and refresh sooner after:

- a material Ofcom report, enforcement decision or complaints movement;
- a new Which?, Opensignal, RootMetrics or umlaut release;
- a host-network migration or material change in MVNO access;
- material VodafoneThree network integration affecting the evidence basis;
- a major outage, porting failure or provider ownership/service migration that may change customer outcomes.

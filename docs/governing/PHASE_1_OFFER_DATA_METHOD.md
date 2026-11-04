# Phase 1 Offer Data Method

## Ownership and authority

- **Owner:** Evidence.
- **Files:** Save this methodology in `context-files/evidence/`; save offer observations, datasets and generated outputs in `data-files/evidence/`.
- **Status:** Current Evidence authority for ordinary live-case offer-data processing. Separate catalogue and research sections are labelled and do not override the live-case method.
- **Must follow:** [CEO memory](../../ceo/MEMORY.md), [Agent Operating Model](../../ceo/AGENT_OPERATING_MODEL.md) and founder decisions recorded in the [CEO Decision Register](../../ceo/DECISION_REGISTER.md).
- **Does not define:** the household recommendation, customer-facing report wording, provider-quality scores, research thresholds or recommendation-algorithm rules.
- **Handoff:** Operations applies this deterministic method directly in ordinary cases. Evidence maintains the method and provides a bounded return only for a new provider assessment, missing or ambiguous source/method rule, material evidence conflict or case the approved calculator cannot safely process.

## Status

This is the sole current Evidence-owned authority for ordinary Phase 1 live-case offer-data processing. It is an evidence method, not a recommendation algorithm. Sections explicitly labelled as separate catalogue or research design do not govern the ordinary provider-balanced live-case benchmark task.

Phase 1 supports broadband, mobile, gas and electricity. Water, TV packages and home 4G/5G broadband are out of scope for the offer catalogue.

## Phase 1 purpose

The offer dataset should help an analyst decide whether a household's current service appears worth investigating, while keeping the member-facing report simple. Phase 1 reports do not recommend or display a specific package.

Possible report outcomes remain broader than switching and are governed by the CEO recommendation framework. An internal evidence gap belongs to Billvisor and may limit the analysis, but it must not be presented as missing customer information when the agreed minimum was supplied.

The offer dataset is an evidence input only. It must not define savings thresholds, recommendation weights or the future founder-defined algorithm.

## Confirmed founder decisions

- For separate broadband/mobile catalogue research, start with an initial panel of ten providers for each service.
- Select those broadband/mobile panels using a combination of residential customer base, UK availability and evidence coverage.
- Include provider-direct public offers.
- Record comparison-exclusive offers separately and identify their channel.
- Do not claim that comparison websites are generally or usually cheaper; current evidence supports the existence of channel-exclusive offers, not a general price advantage.
- Do not claim complete or whole-market coverage.
- For separate broadband/mobile catalogue research, check provider-direct routes alongside a small, documented set of comparison services. Any reusable energy source set remains unapproved.
- For separate broadband/mobile catalogue research, use a national weekly catalogue followed by household-specific verification at report time. This does not establish a reusable energy source panel.
- Include new-customer, published existing-customer and evidenced retention offers.
- Treat personalised account and retention offers as household-specific, not generally available.
- Keep conditional rewards separate from the main contracted-cost calculation.
- Refresh the separate broadband/mobile catalogue once a week. No permanent energy refresh frequency is approved.
- Recheck any offer that materially supports a live report.
- Exclude home 4G/5G broadband from the initial catalogue.
- Exclude TV offer research. Where a member has a TV bundle, record only the dependencies needed to avoid a misleading broadband comparison.
- For ordinary live broadband/mobile comparison-result processing, calculate each comparable offer's advertised first-12-month effective monthly price, group offers by provider, calculate the arithmetic mean for each provider, and use the median of those provider means as the benchmark. Do not average advertised starting prices or let providers with more observed offers receive more weight.
- Use the capture/search date as the notional package start date. Include compulsory recurring payments and stated compulsory one-off charges in the first 12 months; exclude cashback, vouchers, gift cards, switching credits and other rewards from the core calculation.
- Where a possible future rise is unquantified, use the advertised price as a reasonable working estimate. Do not exclude a result merely because the future rise is unknown.
- For an ordinary live case, exclude only a result with no usable price or one that is plainly not comparable. Return only the service, monthly benchmark, annual benchmark, provider count, offer count and one short note if estimation materially affects the figure.

## Separate catalogue/research design — provider panel

The initial panel should represent a practical coverage set, not a claim of whole-market coverage or a ranking of provider quality.

### Current selection principles

- Customer base and UK availability establish market relevance.
- Evidence coverage determines how confidently a provider can be analysed; it should not automatically exclude a widely used provider.
- A provider outside the panel may be researched for a case when the member already uses it or it is materially relevant to the member's location.
- Record the source and date used to select the panel and review the composition periodically.
- Where exact provider-level customer figures are unavailable, label the selection as approximate.

### Unresolved catalogue-design question

The founder has not approved a numeric weighting or tie-break rule across customer base, availability and evidence coverage. Do not invent one.

For energy catalogue research, one option is a top-ten supplier panel with separate electricity, gas and dual-fuel tariffs. This requires founder confirmation before becoming a fixed catalogue rule and does not affect ordinary case-time energy processing.

## Data model

Do not store only an average price. Maintain three linked layers.

### 1. Offer observation

A dated record of a real offer observed in a particular channel.

Minimum fields:

- internal offer ID;
- provider;
- service category;
- provider package name and identifier, where available;
- internal package category;
- customer type: new, published existing, account-specific or retention;
- access route: provider direct or comparison service;
- comparison source or site name, where applicable;
- exclusive status: yes, no or unclear;
- source URL;
- date and time checked;
- core service specification;
- recurring-price timeline;
- minimum contract term;
- compulsory one-off charges;
- guaranteed automatic bill credits;
- conditional cashback, gift cards or other rewards, recorded separately;
- known scheduled price-rise terms;
- eligibility and availability conditions;
- evidence reference;
- captured timestamp;
- last-verified timestamp;
- valid-from and expiry dates, where stated;
- last-observed date;
- active, withdrawn, possibly stale or unable-to-verify status;
- material source conflicts or limitations.

### 2. Separate weekly catalogue benchmark

A calculated summary derived from the underlying active offer observations.

Research-stage catalogue fields:

- provider;
- service and package category;
- active-offer count;
- median effective monthly contracted cost;
- mean effective monthly contracted cost for diagnostic use;
- lowest and highest effective monthly contracted cost;
- typical minimum term;
- count or share with known scheduled price increases;
- earliest and latest source-verification timestamps;
- national, regional or address-dependent availability;
- benchmark confidence;
- known evidence gaps.

The median remains a research-stage candidate for a future weekly catalogue because it is less sensitive than the mean to an unusually expensive package. It is not an ordinary live-case rule.

These weekly catalogue fields do not govern the live-case calculation from pasted comparison results. The founder-approved broadband/mobile live-case benchmark is the median of provider-level means, calculated under the rules below.

### Channel coverage and offer inclusion

- No single provider site, comparison service, feed or affiliate route should be treated as complete.
- Maintain a fixed source register showing which providers, services, locations and offer types each selected comparison source covers or excludes.
- Prefer regulator-accredited comparison services where a current accreditation scheme applies. Accreditation supports source selection; it does not prove complete coverage of every local, innovative, collective or exclusive offer.
- For broadband and mobile, the selected comparison-source set must disclose its market coverage, known omissions and commercial relationship where this information is available.
- No reusable energy comparison-source panel is approved. For an ordinary energy case, use accessible current tariff evidence relevant to the household and preserve the route, date, region and observed tariff inputs internally.
- The names and number of comparison services in the recurring source set remain a founder decision. Do not add sources solely because they produce lower prices.
- The weekly benchmark must use a consistent inclusion rule. Within each selected source, standard test profile and approved package category, record every qualifying offer returned—not only the cheapest or most interesting offers.
- Selective checking is appropriate at case time, after the household's current arrangement and relevant comparison category are known.
- Local and alternative-network broadband providers may sit outside national comparison tools. Check a case-relevant local provider directly when address evidence indicates it may be available.
- Record source failures and missing providers explicitly. Do not interpret absence from a comparison site as proof that the provider or offer is unavailable.

### Source basis for the channel rules

Checked 16 July 2026:

- [Ofcom's phone and broadband contract checklist](https://www.ofcom.org.uk/phones-and-broadband/switching-provider/checklist-when-taking-out-new-phone-or-broadband-contract) establishes the importance of checking contract length, extra charges, cancellation, service information and the provider-issued contract summary. It also points consumers to Ofcom-accredited comparison services. It does not establish that one comparison service covers every offer.
- [Ofgem's energy-switching guidance](https://www.ofgem.gov.uk/information-consumers/energy-advice-households/switch-energy-supplier) lists currently accredited energy comparison services and explains that accredited services must state what a tariff includes, distinguish tariffs that can and cannot be arranged through the service, and list tariffs in price order. Accreditation does not remove the need to record tariff eligibility and source date.
- [MoneySavingExpert's broadband comparison disclosure](https://www.moneysavingexpert.com/compare-broadband-deals/) states that its tool does not cover the whole market, that some providers restrict access to exclusive offers and that local providers without feeds may be absent. This is evidence about that tool's coverage and illustrates the wider coverage risk; it is not proof that every comparison service has the same omissions.
- [MoneySavingExpert's mobile comparison disclosure](https://www.moneysavingexpert.com/cheap-mobile-finder/) states that whole-market mobile coverage is effectively unavailable, identifies provider/retailer coverage limits and excludes some redemption-based cashback offers by default. This supports explicit recording of source scope and reward treatment, not reliance on MoneySavingExpert as a complete source.

### 3. Case-time verification

Before naming a provider or relying on a market observation in a report:

- confirm the provider serves the household;
- confirm that a sufficiently comparable package is currently available;
- recheck the current price and decisive contract terms;
- record postcode, region, meter, payment or other eligibility factors used;
- consider relevant provider-quality and switching implications;
- preserve the exact offer observation supporting the report;
- disclose limitations and do not imply whole-market coverage.

The offer need not be shown to the member in Phase 1, but the internal recommendation must remain traceable to current evidence.

This case-time verification depth applies when a provider is to be named or an offer is relied on specifically. It is not part of the ordinary provider-balanced live-case handoff, which follows the narrow rules below and does not add eligibility, coverage or provider-quality analysis.

## Price calculations

### Founder-approved broadband/mobile live-case benchmark

These rules govern ordinary live Phase 1 broadband/mobile processing of founder-pasted comparison results. The task is deliberately narrow: identify broadly comparable offers, calculate each offer's first-12-month effective monthly price, group the offers by provider, calculate each provider mean and use the median provider mean as the benchmark. There is no fixed time cap; speed comes from the restricted scope and output. This offer-list method does not apply to energy.

#### Horizon and offer calculation

- Use a 12-month horizon beginning on the capture/search date, which is the notional package start date.
- For each broadly comparable offer, add the advertised compulsory recurring payments falling within that horizon, reflecting stated promotional periods and stated dated or contractual price changes.
- Add compulsory one-off setup, activation, installation or equipment charges when the captured result states them.
- Exclude cashback, gift cards, vouchers, switching credits and all other rewards from the core cost, whether described as automatic or claim-dependent.
- A stated discounted recurring price is part of the recurring-price timeline, not a reward.
- If a possible future rise is unquantified, use the advertised price as the working estimate for the affected period. Add one short note to the Operations handoff only when that estimation materially affects the figure.

`Offer first-year effective monthly price = advertised compulsory first-12-month cost ÷ 12`

#### Counting convention for dated changes

Use 12 notional monthly billing periods beginning on the capture date and its monthly anniversaries.

- If a later month does not contain the capture-date day number, use that month's final calendar day for that period only; return to the capture-date day number in the next month that contains it.
- Use the recurring price in force on each notional billing-period start date.
- Apply a dated price change from the first notional period whose start date is on or after the stated effective date.
- Do not prorate a monthly period when a price change falls between two notional period starts.
- For contractual wording such as “months 1–8” or “£24 for 12 months”, apply the stated number of whole notional periods directly.
- The result is approximate because actual activation and billing dates may differ.

#### Usability and exclusions

- Include broadly similar packages with a usable advertised price.
- Exclude only a result with no usable price or one that is plainly not comparable to the selected service/package category.
- Do not perform additional eligibility, coverage, source-conflict or provider-quality analysis for the ordinary provider-balanced benchmark task.

#### Provider grouping and benchmark

1. Group the usable offers by the retail provider named in the captured result.
2. For each provider, calculate the arithmetic mean of that provider's unrounded offer first-year effective monthly prices.
3. Sort the provider means from lowest to highest.
4. The monthly benchmark is the middle provider mean when the provider count is odd. When it is even, it is the arithmetic mean of the two central provider means.
5. The annual benchmark is the monthly benchmark multiplied by 12.

- Calculate offer totals in pounds and pence from the captured price timeline.
- Retain unrounded offer effective monthly prices for provider means and retain unrounded provider means for the median.
- Evidence preserves and hands off exact monthly and annual benchmark values; customer-facing rounding and “about” wording are Operations-owned under the approved report rule.
- Retain internally the smallest trace needed to reproduce the calculation: service, source, provider, offer/package label, price components, first-year effective monthly price, provider grouping, provider means, median arithmetic and any exclusion reason.
- Do not describe the result as a whole-market average, exact achievable price, exact saving or recommendation.

#### Lean live-case output

For an ordinary case, the Operations calculator records only:

1. service;
2. monthly benchmark;
3. annual benchmark;
4. number of providers;
5. number of offers; and
6. one short note only if estimation materially affects the figure.

Do not create a separate ordinary Evidence handoff. Operations retains the smallest reproducible calculation trace inside the case record and does not produce a long evidence pack, conflict analysis, confidence taxonomy, list of non-requested customer information, eligibility/coverage analysis, exact-saving claim or whole-market assessment. When Evidence is exceptionally called, it returns only the bounded answer requested and does not make the household recommendation or green/amber decision.

### Separate minimum-term catalogue views

The following calculations may still be retained for catalogue diagnostics or a specifically requested minimum-term analysis. They do not replace the founder-approved provider-balanced broadband/mobile live-case benchmark.

`Gross effective monthly cost = (recurring charges over the minimum term + compulsory one-off charges) ÷ minimum-term months`

### Guaranteed-credit cost

`Net effective monthly cost = (gross minimum-term cost − guaranteed automatic bill credits) ÷ minimum-term months`

### Conditional-reward view

Calculate a separate incentive-adjusted figure for conditional cashback, claimable gift cards or third-party rewards. Do not use that figure as the main contracted cost or imply that the reward is guaranteed.

For these separate minimum-term catalogue views, where a scheduled increase amount is unknown, state the limitation rather than inventing an increase. The ordinary broadband/mobile live-case rule differs: it uses the advertised price as a reasonable working estimate.

## Broadband

### Required package information

- advertised average download speed;
- advertised average upload speed, where available;
- minimum guaranteed speed, where address-specific and available;
- access technology;
- infrastructure network where relevant;
- data cap or fair-use restriction;
- router and equipment terms;
- installation type and compulsory charges;
- minimum term;
- address or network availability;
- landline or other bundle dependency that materially affects price or cancellation.

### Separate catalogue research bands

- up to 50 Mbps;
- 51–100 Mbps;
- 101–300 Mbps;
- 301–500 Mbps;
- 501–999 Mbps;
- 1 Gbps and above.

These catalogue bands are unresolved and do not govern ordinary live-case package selection. Technology should remain visible in catalogue research because FTTC, FTTP and cable offers with similar advertised speeds are not necessarily like-for-like.

Home 4G/5G broadband is excluded. If a member submits such a service, analyse it separately with explicit local-performance limitations rather than forcing it into the fixed-broadband benchmark.

## Mobile

### Required package information

- SIM-only or handset-linked service;
- underlying network;
- monthly data allowance;
- calls and texts allowance;
- contract term;
- 5G access;
- speed cap;
- roaming allowance and fair-use limit;
- rollover, tethering or other material restrictions;
- eSIM or other decisive compatibility detail where relevant;
- scheduled price-rise terms.

Keep handset finance and airtime separate wherever the evidence allows. Do not compare a combined handset contract directly with SIM-only service as if they were equivalent.

### Separate catalogue research bands

- low data;
- medium data;
- high data;
- very high data;
- unlimited data.

Numeric catalogue boundaries for these bands remain unresolved and do not govern ordinary live-case package selection.

## Electricity and gas

Do not use a provider's average advertised monthly tariff price as the main household comparison. Energy cost depends on consumption, region, meter and payment method.

The broadband/mobile provider-balanced offer-list benchmark does not apply to energy. Energy remains governed by the household-specific tariff calculation below.

### Default Phase 1 energy checks

Limit an ordinary energy case to three checks:

1. whether a lower-cost payment method appears worthwhile;
2. whether the current fixed or variable tariff, together with any known end date or exit fee, makes review timely; and
3. whether accessible current tariff evidence indicates that looking elsewhere is worth the household's time.

Use only accessible case-time tariff evidence relevant to the household. Preserve the source route, observation date, applicable region, tariff inputs and arithmetic internally. Do not imply that the accessible evidence is representative of the whole market. A reusable source panel and permanent refresh frequency are not approved.

### Required tariff information

- electricity, gas or dual fuel;
- tariff name;
- fixed, variable, standard, social or time-of-use tariff;
- supply region;
- meter type;
- payment method;
- unit rate for each applicable register and fuel;
- standing charge for each fuel;
- tariff end date;
- exit fee by fuel;
- price-guarantee period;
- eligibility and smart-meter requirements;
- source and verification date.

### Household calculation

`Estimated annual cost = annual kWh × unit rate + 365 × daily standing charge`

Use annual consumption in this order:

1. the household's evidenced previous-12-month consumption by fuel;
2. the supplier's estimated annual consumption by fuel; or
3. the ordinary bedroom-based fallback below.

For the ordinary fallback, use the current Ofgem Typical Domestic Consumption Values effective from 1 July 2026 and select the profile using bedrooms only:

| Bedrooms | Profile | Electricity, standard single rate | Gas |
| --- | --- | ---: | ---: |
| 1–2 | Low | 1,600 kWh/year | 6,000 kWh/year |
| 3–4 | Medium | 2,500 kWh/year | 9,500 kWh/year |
| 5+ | High | 3,800 kWh/year | 14,000 kWh/year |

Apply only the fuel or fuels supplied to the household. Do not use property type or occupant count to alter the selected profile. The kWh bands are Ofgem's industry-wide TDCVs; the bedroom mapping is a practical convention used by current comparison services and is not an Ofgem-defined household classification.

The fallback is an approximate internal input and makes the service **Analysed with limitations**. Customer-facing wording should say only that consumption was estimated from households with similar characteristics. Keep the profile name, source values and arithmetic internal.

Do not use this ordinary fallback for multi-rate or specialist arrangements when consumption timing or materially different usage is decision-critical, including Economy 7, electric heating, heat pumps and regular home EV charging. For multi-rate electricity with evidenced register usage, calculate each register separately.

### Energy output boundary

The downstream customer output is limited to:

- estimated annual cost;
- potential saving where the accessible evidence supports one;
- a short explanation of the material evidence; and
- one recommended action selected through the approved Operations/founder process.

The Evidence handoff should contain only the calculation and material evidence needed to support those fields.

Mention standing-charge effects only when materially relevant for a low-usage household. Do not add routine generic efficiency tips, extensive tariff education or a whole-market implication.

The available actions are: stay put; check a lower-cost payment method; look more closely at current tariffs; or confirm annual usage when the estimate is too uncertain. Evidence supplies the supporting calculation and does not choose the household recommendation.

### Next validation need — identified, not started

Apply the three-check method to the next suitable pilot or live case and record only which accessible public tariff routes returned usable household-relevant inputs and the active Evidence time required. Compare that result with the completed initial test to assess repeat-case sourcing and effort. This does not approve a permanent source panel, refresh schedule or new test artifact now.

Source basis, checked 14 August 2026:

- [Ofgem's 2026 TDCV review](https://www.ofgem.gov.uk/consultation/review-typical-domestic-consumption-values) confirms the revised low, medium and high consumption values effective from 1 July 2026 and describes TDCVs as a consistent reference used across the energy sector when actual usage is unknown.
- [Uswitch's current electricity comparison guidance](https://www.uswitch.com/gas-electricity/electricity-only/) maps 1–2, 3–4 and 5+ bedrooms to the low, medium and high TDCV electricity bands. Billvisor adopts that simple bedroom convention for both applicable fuels; this mapping is an internal approximation, not a regulator-issued classification rule.

## Existing-customer and retention evidence

Treat offers as distinct types:

- **Published existing-customer offer:** may enter the weekly catalogue if its eligibility is documented.
- **Account-specific offer:** retain only as evidence for the relevant household unless general availability is independently established.
- **Negotiated retention offer:** retain as a dated household-specific quote; do not generalise it to other households.

Record quote date, expiry, channel, conditions and the member-supplied evidence. Do not request provider credentials or direct account access in Phase 1.

## Comparison-exclusive offers

- Identify the comparison or affiliate channel.
- Keep the underlying package separate from the channel-specific commercial offer.
- Record special eligibility, tracking, claim and reward conditions.
- Do not prioritise an offer because it generates commission.
- Reverify the offer at report time if it materially affects the conclusion.
- Never imply whole-market coverage merely because multiple comparison sources were checked.
- Do not state or imply that comparison websites are generally cheaper. Record only the channel-specific offer actually observed.

## Member-facing use

Phase 1 does not show or recommend a specific package. Possible evidence-based wording may include:

- a comparable market category appears materially cheaper than the current service;
- it is worth checking a named provider;
- it is worth comparing the market, but no single provider is sufficiently verified;
- current evidence does not justify spending time on a switch;
- more information is needed.

Naming a provider requires a current relevant offer, household eligibility evidence and consideration of provider quality and switching implications. A weekly average alone is not sufficient.

The report must not claim a best deal, guaranteed saving or whole-market comparison unless the evidence legitimately supports that statement.

Billvisor should perform the provider-direct and cross-comparison checks internally where possible. Do not routinely transfer that work to the member. Guidance to check the provider's own site and more than one comparison service is appropriate only when it is the report's justified next step or when Billvisor could not verify channel coverage sufficiently; state the limitation and keep the action as narrow as possible.

## Separate catalogue refresh and quality controls

- Run the approved separate broadband/mobile catalogue refresh at least once each week. No permanent energy refresh schedule is approved.
- Timestamp every observation and benchmark.
- Record offers that could not be reverified rather than silently carrying them forward.
- Detect new, changed, withdrawn and expired offers.
- Recheck decision-driving offers during case analysis.
- Retain enough underlying evidence to reproduce every benchmark used.
- Keep market-offer data separate from member-specific records and their privacy/retention controls.
- Record source conflicts, coverage limitations and uncertainty.

A weekly refresh does not guarantee that an offer is current throughout the week. Currentness for a report is established only through the case-time verification step.

## Separate catalogue/research questions

- Decide later whether energy needs any reusable source panel and, if so, its composition and refresh frequency. The ordinary energy method currently uses accessible case-time evidence only.
- Define how the three provider-panel criteria are combined without creating an unsupported numeric ranking.
- Approve or revise the broadband speed bands.
- Approve numeric mobile data-allowance bands.
- Test median versus other benchmark summaries for a possible weekly catalogue. This catalogue question is separate from the ordinary broadband/mobile live-case benchmark, which is the founder-approved median of provider means.
- Define benchmark-confidence rules.
- Decide what market-price observation, if any, is shown to members.
- Test whether naming one provider is more useful and trustworthy than recommending a broader market check.
- Define operational evidence-retention and archival requirements for public offer observations.
- Define how quickly an offer must be rechecked before it can support a live report.
- Approve the recurring comparison-source set and its review frequency for broadband and mobile; treat any future permanent energy panel as a separate founder decision.

## Phase 2 boundary

Phase 2 may expand into a complete product catalogue, specific deal recommendations, broader provider coverage, automated eligibility checks, detailed bundles and more granular offer ranking. This method does not define that system.

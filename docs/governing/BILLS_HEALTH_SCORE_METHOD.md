# Bills Health Score Method

## Status and ownership

- **Status:** Founder-approved Phase 1 method, implemented in the calculator and report route.
- **Owner:** CEO. This is a founder-defined household scoring policy, not a provider-scoring or recommendation method.
- **Applies to:** Service-level and overall Bills Health Scores in the Phase 1 Bills Health Report.
- **Does not define:** Provider-quality evidence, comparable-package selection, household recommendations, switching decisions or legal conclusions.
- **Required inputs:** Approved household facts, the applicable Evidence price comparison and the current approved provider-quality table.

The weights, curve, bands and aggregation are Phase 1 policy to validate with real household comprehension and outcomes. They are not data-proven optima.

## 1. Separate concepts

- **Coverage status:** Analysed, Analysed with limitations or Not analysed.
- **Price score:** Current monthly price compared with the approved monthly cost of similar services.
- **Provider position:** Current provider's relative position in the applicable approved quality table.
- **Service score:** The combined 0–100 result for one service.
- **Overall score:** The annual-spend and status-weighted average across services with numeric scores.
- **Recommendation:** The founder-approved action. It normally remains distinct from the score, except for the narrow small-saving/effort adjustment in section 2.3.

Market position, coverage status and recommendation must not be inferred automatically from one another.

## 2. Price score

Use the unrounded submitted current monthly price and the exact approved monthly similar-service comparison value.

`Price difference ratio = (current monthly price − comparison monthly price) ÷ comparison monthly price`

`Base price score = min(100, 20 + (60 × comparison monthly price ÷ current monthly price))`

This produces:

| Current price position | Price score |
|---|---:|
| 25% below comparison | 100 |
| Equal to comparison | 80 |
| 25% above comparison | 68 |
| 50% above comparison | 60 |
| 100% above comparison | 50 |

The curve is deliberately non-linear and does not turn a service into 0 merely because its price is twice the comparison. Do not calculate a price score when the current price or approved comparison value is missing, zero or invalid.

### 2.1 Qualified comparison

A numeric score may be issued when a reasonable broadband/mobile comparison exists but a material input is estimated or not fully matched. The service must be **Analysed with limitations** and the service page must state the single material limitation in plain English. Retain the qualified-comparison flag and full basis internally. Do **not** label the customer-facing score or gauge “Estimated”; explain the relevant estimate or limitation in the service-page narrative instead.

For energy, the approved scoring cases are:

- When a supportable like-for-like payment-method comparison uses the same regional rate basis, consumption, fuels, meter type and tariff type, its annual cost may be the price comparison for a qualified price-only score. State the material limitation in the customer narrative; do not label the score itself “Estimated”.
- For an electricity-only Economy 7 household with actual peak and off-peak readings, compare the current Economy 7 rates with the regional Direct Debit single-rate reference using the exact same measured usage and billing-day sample. This produces a qualified tariff-fit score, not a best-deal or whole-market score. The score answers whether the Economy 7 rate structure appears to suit the observed usage pattern. Do not show an alternative-provider saving from this comparison.
- For an ordinary Energy case, compare the current tariff with a relevant accessible tariff using the same selected household-consumption input, geography, fuels, meter type and payment basis. It may be a different tariff type, such as flexible versus fixed, when the score is explicitly a **tariff-fit score**. This is price-only: do not add a provider-quality component, represent it as a market comparison or show it as a named-offer recommendation.

The Economy 7 calculation requires current peak rate, off-peak rate and standing charge; the regional single-rate unit rate and standing charge; matched Direct Debit payment basis; actual peak/off-peak kWh and associated billing days; source references; and capture date. Unless the actual sample covers the prior 12 months, the customer narrative must state the material sample limitation; the score itself remains unlabelled. For an ordinary tariff-fit score using the approved bedroom fallback, retain the exact rates, consumption input, tariff costs and comparison internally. The customer explanation must say that the tariff view uses estimated energy use; this does not change an **Analysed** coverage status when the customer supplied the agreed minimum data. These rules do not approve the cheapest accessible tariff, an arbitrary alternative or a whole-market value as the energy comparison.

### 2.2 Material-opportunity guardrail

After calculating the normal 90/10 service result, calculate:

`Potential annual saving = max(0, (current monthly price − comparison monthly price) × 12)`

`Saving share = potential annual saving ÷ current annual spend`

For energy, use the exact annual current and comparison costs directly; dividing both by 12 would produce the same ratio and score.

Apply both-value guardrails to the exact service score:

- **High material opportunity:** potential annual saving is at least £150 **and** at least 25% of current annual spend. Cap the exact service score at 39.
- **Moderate material opportunity:** potential annual saving is at least £100 **and** at least 15% of current annual spend. Cap the exact service score at 74.
- Otherwise, do not apply a materiality cap.

Test the high condition first. The guardrail prevents a large actionable household opportunity from receiving an inappropriately reassuring band, while avoiding disproportionate penalties for a large service where the saving is only a small percentage of current spend. These thresholds are founder-defined Phase 1 policy to validate, not evidence-proven optima.

### 2.3 Small-saving/effort adjustment

When the founder-approved recommendation is **Stay put** specifically because the supported saving is too small to justify the expected effort, and the potential annual saving is below **£50**, floor the exact service score at **75 — Good**.

This is not automatic from a low saving. Operations records the explicit internal decision value `small_saving_not_worth_effort` only when the approved case reasoning supports it. The report still displays the positive potential saving and explains why no action is recommended. Do not use this adjustment where provider quality, timing, a contract constraint or another reason is the main reason for staying put.

## 3. Provider-position score

Use the current approved service-specific provider table and its raw overall quality scores. Evidence confidence remains separate and does not alter the position calculation.

1. Sort providers by raw overall quality score from highest to lowest.
2. Assign ordinal positions from 1 to the provider count.
3. Providers tied on raw quality score receive the average of the ordinal positions occupied by that tied group.
4. Identify the best observed average rank and worst observed average rank.
5. Calculate:

`Provider position = 100 × (worst observed rank − provider rank) ÷ (worst observed rank − best observed rank)`

This gives every provider tied at the top 100, every provider tied at the bottom 0 and equal intermediate values to other ties.

Retain the table version and date internally. Adding or rescoring a provider requires recalculating every provider position. If a table has fewer than two distinct raw scores, no meaningful provider position exists.

### Provider absent from the table

Evidence first attempts to score the live customer's provider under the approved service-specific method. Where evidence is sufficient, add the provider and recalculate the full table. Never invent a provider score merely to complete the calculation.

If reliable provider quality remains unavailable but price position is supportable, use the price score alone and mark the service **Analysed with limitations**. State briefly that the score is based on price comparison only.

## 4. Service score

Where both inputs exist:

`Exact service score = (price score × 0.90) + (provider position × 0.10)`

Where provider position remains unavailable:

`Exact limited service score = price score`

Where neither a sufficiently reliable nor a reasonable estimated price comparison exists, issue no numeric service score even if provider quality exists.

After applying the 90/10 calculation, apply the material-opportunity guardrail in section 2.2 and, where explicitly approved, the small-saving/effort adjustment in section 2.3. Contract status does not otherwise enter the score.

## 5. Display rounding and bands

- Retain the exact calculated value internally.
- Round the displayed score to the nearest whole number.
- Round an exact `.5` upwards.
- Apply the band to the displayed rounded number.

| Displayed score | Band |
|---|---|
| 0–39 | Poor |
| 40–74 | Medium |
| 75–100 | Good |

## 6. Provider-quality explanation

The provider note is a material explanation, not a routine provider label.

1. Round and band the price-only score using the display rules.
2. Round and band the combined 90/10 result before any material-opportunity cap.
3. Show the note only when the combined band is lower than the price-only band.
4. Never show a positive provider note.
5. Show no provider note when provider position changes the number but not the band.

Template:

> Recent public data indicates that your current provider has weaker [service-relevant quality areas] results than some others. This lowered your [service] rating from [price-only band] to [combined band].

Use:

- Broadband: reliability and customer support.
- Mobile: network experience and customer support.
- Energy: billing and customer support.

Use “public data” only where the supporting material is genuinely publicly accessible. Do not expose source names, ranks, table positions or internal scores; do not call the evidence “reviews”; do not label a provider simply good or bad; and do not imply whole-market coverage.

Include once per report:

> Supporting source details are available on request.

Retain exact sources, publication dates, covered periods, limitations and calculations internally so the request can be fulfilled.

## 7. Overall Bills Health Score

Use exact unrounded service scores.

`Service weight = current annual spend × status weight`

`Status weight = 1.0 for Analysed; 0.8 for Analysed with limitations`

`Exact overall score = Σ(exact service score × service weight) ÷ Σ(service weights)`

Rules:

- Exclude Not-analysed services.
- Exclude Analysed-with-limitations services without a numeric score.
- Include every Analysed-with-limitations service with a numeric score at its current annual spend × 0.8.
- Include every Analysed service with a numeric score at its current annual spend × 1.0.
- One scored service becomes the overall score.
- No scored services means no overall score.
- A combined energy analysis counts once.
- Separately assessed gas and electricity count separately.
- Round and band only the final overall result under section 5.

The report must state how many services contributed to the overall score. It must not imply that an excluded or unrequested service was assessed numerically.

## 8. Approved validation cases

| Scenario | Price-only result | Provider position | Service result | Provider note |
|---|---:|---:|---:|---|
| Price 25% below comparison; lowest provider | 100 Good | 0 | 90 Good | No |
| Price equals comparison; lowest provider | 80 Good | 0 | 72 Medium | Yes |
| Price 25% above comparison; highest provider | 68 Medium | 100 | 71 Medium | No |
| Price 50% above comparison; lowest provider | 60 Medium | 0 | 54 Medium | No |
| Provider evidence unavailable; price equals comparison | 80 Good | Unavailable | 80 Good | Price-only limitation |
| Price comparison unavailable | No score | Any | No score | Analysis limitation |

Founder-approved calibration dry run on 17 August 2026:

- Broadband: £39 current monthly price, £23.85 comparison, £181.80 annual saving and 38.8% saving share. The high material-opportunity guardrail caps the service score at **39 — Poor**.
- Mobile: £12 current monthly price, £6 core-plan comparison and £72 annual saving. The comparison did not match the supplied EU-calling benefit, so the result is **45 — Medium** under **Analysed with limitations**; the service-page narrative states that material limitation while the qualified-comparison flag remains internal.
- Energy: £1,282.27 estimated current annual cost and £1,173.36 like-for-like Direct Debit estimate, a saving of about 8.5%. No materiality cap applies; the price-only result is **75 — Good, Estimated**.
- The individual service results were approved as a Phase 1 calibration decision. This historical overall score used the superseded equal-service weighting and is retained only as a record of that dry run; recalculate it before using it as a current validation case.

## 9. Required internal trace

For every numeric score retain:

- household current monthly price and source;
- exact monthly comparison value and Evidence reference;
- price difference ratio and exact price score;
- provider table version/date, raw provider score, tied rank and position value where used;
- exact service score, rounded display score and band;
- price-only band and whether the provider-note trigger fired;
- potential annual saving, saving share, materiality classification and any applied cap;
- whether the score is Estimated and the exact customer-facing limitation;
- coverage status and any limitation;
- for the overall score, every included/excluded service, weight and arithmetic;
- exact customer-facing provider wording where shown.

Operations calculates or assembles the trace from approved inputs. The deterministic validation gate checks every ordinary case. When a risk-based Review trigger applies, Review also recomputes the arithmetic and verifies the customer output before final HTML generation. Neither function changes Evidence inputs or chooses the household recommendation.

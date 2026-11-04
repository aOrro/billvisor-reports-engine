# Governing documents

The documents below govern this engine and take precedence over the build brief. Copy the originals here
unchanged from `context-files/`. They are not retyped, so that a transcription error can't create a rule.

| File | Source |
|---|---|
| MEMORY.md | context-files/ceo/MEMORY.md |
| BILLS_HEALTH_SCORE_METHOD.md | context-files/ceo/ |
| PHASE_1_RECOMMENDATION_FRAMEWORK.md | context-files/ceo/ |
| PHASE_1_CASE_OPERATING_METHOD.md | context-files/operations/ |
| LIVE_CASE_CALCULATOR_SPEC.md | context-files/operations/ |
| PHASE_1_WELCOME_EMAIL_TEMPLATE.md | context-files/operations/ |
| PHASE_1_OFFER_DATA_METHOD.md | context-files/evidence/comparison-data/ |
| BROADBAND / MOBILE / ENERGY_PROVIDER_SCORING_METHOD.md | context-files/evidence/provider-scoring/ |
| BROADBAND_PROVIDER_SCORES.md, MOBILE_PROVIDER_SCORES.md | data-files/evidence/provider-scoring/ (structured copies in `reference/provider_tables/`) |
| CLAUDE_REPORT_GENERATOR_BUILD_BRIEF.md | build brief (lowest authority) |
| REPORT_OUTPUT_QA.md, PHASE_1_EMAIL_UX.md | not yet supplied |

## Founder rulings applied where documents conflict (2026-11-04)

1. **Bedroom fallback → Analysed, weight 1.0.** This follows MEMORY.md, BILLS_HEALTH_SCORE_METHOD §2.1 and
   LIVE_CASE_CALCULATOR_SPEC §4. The "Analysed with limitations" wording in PHASE_1_OFFER_DATA_METHOD and the
   worked example in LIVE_CASE_CALCULATOR_SPEC §6 are treated as out of date.
2. **Energy price-only is not a limitation.** A tariff-fit score stays Analysed. The like-for-like
   payment-method score is Estimated, so it is Analysed with limitations.
3. **Stopped requested service.** Building is blocked unless the founder records
   `proceed_as: confirm_information`. That is allowed only for customer-information gaps and gives Analysed with
   limitations, no score and the action Confirm information.
4. **Scope.** The engine produces report data. The delivery email and HTML rendering are out of scope for this build.

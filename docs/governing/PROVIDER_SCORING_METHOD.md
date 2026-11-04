# Provider Scoring Method

## Ownership and authority

- **Owner:** Evidence.
- **Files:** Save methodologies and evidence rules in `context-files/evidence/`; save research logs, scores, observations, datasets and generated outputs in `data-files/evidence/`.
- **Authority:** Default internal methodology for provider-quality scoring across service types.
- **Must follow:** [CEO memory](../../ceo/MEMORY.md), [Agent Operating Model](../../ceo/AGENT_OPERATING_MODEL.md) and founder-approved methodology changes.
- **Does not define:** household recommendations, customer-facing wording, offer value, research experiments, legal conclusions or the founder-owned recommendation algorithm.
- **Handoff:** Supplies dated, traceable and confidence-qualified evidence to Operations.

## Purpose
An internal, directional guide to compare providers and understand their relative strengths and risks. Scores are not claims of exact measurement or automatic member recommendations.

## Rule hierarchy
This is the default framework for every provider and service type. A service-specific method may override it **only where it explicitly states a different rule** (for example, categories, weights, evidence inputs or service-specific constraints). All non-conflicting generic rules continue to apply.

## Generic scoring model
- Use 0.5-point increments on a 0–10 scale.
- Score bands: 9–10 consistently leading; 7–8.5 clearly above average; 5–6.5 mixed/broadly average; 3–4.5 clearly below average; 1–2.5 consistently poor.
- Each service type defines its own categories, category weights, evidence inputs and calculation in a separate method document.

## Evidence confidence
Confidence measures certainty in the score, not provider quality.

| Confidence | Standard |
|---|---|
| High | At least two recent, independent sources support the conclusion; use regulator evidence where the provider is covered; no material conflict. |
| Medium | One strong source or several credible but incomplete sources; gaps or mild conflict remain. |
| Low | Evidence is sparse, old, localised, based on a limited sample, or materially conflicting. |

## Comparison rule
Keep the raw quality score and confidence visible. For internal comparison:

`Decision score = Quality score − confidence adjustment`

| Confidence | Adjustment |
|---|---:|
| High | 0.0 |
| Medium | −0.5 |
| Low | −1.5 |

- If decision scores tie, prefer the provider with higher confidence.
- A higher-scoring Medium-confidence provider needs a **1.0-point** raw-score lead to overtake a High-confidence provider.
- A higher-scoring Low-confidence provider needs a **2.0-point** raw-score lead to overtake a High-confidence provider.
- A higher-scoring Low-confidence provider needs a **1.5-point** raw-score lead to overtake a Medium-confidence provider.
- A Low-confidence provider may rank above another provider, but is **conditional**: it must not become a default recommendation without a second independent source or relevant local validation.

## Provider record template
```text
Provider:
As of:
Service type:
Category scores / confidence:
Overall quality score:
Overall confidence:
Decision score:
Evidence summary:
Source links and dates:
Known limitations or conflicts:
Recommendation status: Default / Conditional / Caution
Next review date:
```

## Source and review rules
- Prefer regulators and independent consumer research; do not use provider marketing as evidence.
- State where evidence is unavailable or conflicts; do not invent a score rule or data point.
- Distinguish national provider quality from postcode-level network availability and suitability.
- Refresh at least every six months and after material new regulatory or consumer-research evidence.

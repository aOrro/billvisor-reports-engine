# Phase 1 Report Renderer Contract

## Status and authority

- **Owner:** Operations.
- **Status:** Founder-approved renderer contract, 4 November 2026.
- **Purpose:** Define the complete, reusable customer-facing HTML report contract for the internal report engine. It turns approved `report_data` into the approved fixed-A4 Billvisor layout; it does not make recommendations, research the market, create PDFs or send emails.
- **Visual source:** `/Users/anton/billvisor/design/report/`. The engine vendors the approved synthetic page sources and assets under `templates/report/`.
- **Process authority:** [Phase 1 Case Operating Method](PHASE_1_CASE_OPERATING_METHOD.md). Score policy remains in [BILLS_HEALTH_SCORE_METHOD.md](../ceo/BILLS_HEALTH_SCORE_METHOD.md).

This document consolidates report-rendering decisions. It does not replace the case method, recommendation framework, evidence methods or the founder approval gate.

## 1. Preconditions and boundaries

The renderer must:

- read the approved, fingerprinted `report_data` only, never raw case inputs, market captures, source documents or calculator traces;
- refuse output unless the founder-content approval and the required Review result or deterministic no-Review gate are current;
- generate a complete, local, browser-openable fixed-A4 HTML report only;
- leave PDF export and delivery email outside the engine; and
- render only founder-approved customer-facing fields and copy.

The renderer must not expose provider means, individual offers, named comparison sources, raw arithmetic, internal score flags, internal methodology, unapproved recommendation logic or a claim of whole-market coverage.

## 2. Report-wide rules

- The report contains the cover, overview, priority actions, a page for every **Analysed** or **Analysed with limitations** service, and the final action-plan page. **Not analysed** services appear only in the overview.
- A combined gas/electricity analysis appears once as **Energy** in the overview and receives one Energy service page.
- Page count is conditional on included service pages. Page numbering, case reference and report version must be consistent throughout.
- Scores use Good (75–100), Medium (40–74) and Poor (0–39) with the corresponding approved gauge value, arc and colour. Do not write `Estimated` beside a score or gauge.
- `Market position` is the score band: **Good**, **Medium** or **Poor**. Where there is no numeric score, show `—`.
- Remove `Report confidence` entirely.
- Place **Supporting source details are available on request.** once on the final action-plan page, not repeatedly on service pages.

## 3. Overview, summary and totals

The overview uses one row for every requested service unit and contains the approved service label, annual spend, market position, positive potential saving where founder-approved, and the selected next action.

- **Annual spend:** sum the current annual spend for Analysed and Analysed-with-limitations service units only.
- **Potential savings:** sum only positive savings that the founder selected for display.
- **Services reviewed:** count services with a service page.
- **Priority actions:** count selected actions other than **Stay put**.
- A **Stay put** action displays **No action needed**.
- Priority actions order by founder-supplied priority. When two actions have the same priority, order by displayed potential saving descending. Do not create a numeric priority map in the renderer.

## 4. Current-service sections and service-page figures

Render only these labels and values when supplied in approved `report_data`:

| Service | Current-service fields |
|---|---|
| Broadband | Provider; Download speed; Monthly cost; Contract ends |
| Mobile | Provider; Data allowance; Plan type; Monthly cost; Contract ends |
| Energy | Supplier; Services; Tariff; Monthly payment; Tariff ends |

For Broadband and Mobile, place a compact figure row directly beneath the current-service section:

1. **You pay each year**;
2. **Similar services cost**; and
3. **Potential saving**, only where the founder selected a positive saving for display.

Retain the qualitative **What this means** section below it.

For Energy, show both:

- **Monthly payment: £X**; and
- **Estimated annual energy cost: £Y**.

The Energy service page must include this fixed explanatory sentence in **What this means**:

> This uses your current tariff and estimated energy use. Your monthly payments may vary through the year.

The calculated annual tariff cost is the Energy current annual spend and report-weight value. Monthly payment is a customer-supplied sense-check, not a calculation substitute.

## 5. Narrative placement

Keep each service page readable by grouping related points in short paragraphs under **What this means**.

- Put a material service limitation there.
- Put the energy estimated-usage explanation there.
- Put a materially triggered negative provider-quality note there.
- Do not add a generic source, confidence or process box.

The provider-quality note can appear only under the current approved score-method trigger and public-source rule. It must not expose ranks, tables, source names or raw scores.

## 6. Actions and confirm-information pages

- Action pages and final action plan show **Effort: Low / Moderate / High** selected by the founder for the particular action.
- Remove `Time required` and `Difficulty`; do not imply measured time or certainty.
- Action labels are founder-supplied plain-English actions. The renderer does not derive them from a score or action type.
- A **Confirm information** page uses founder-approved short lists headed **What we could confirm** and **What we still need**. It is used only for Confirm information, not as a generic Analysed-with-limitations page.

## 7. Template corrections and acceptance checks

During integration, correct the existing synthetic-template defects rather than carrying their sample values into live reports:

1. A score of 74 must render **Medium** and use the Medium gauge/colour, never Good/green.
2. The cover house illustration must use a repository-vended local asset and must not retain an absolute or broken path to the Business Planning workspace.

The renderer must have synthetic acceptance coverage for:

- score values, bands, arcs and colours;
- combined Energy shown once;
- no service page for Not analysed;
- the precise current-service fields and conditional figure row;
- Energy monthly-payment and calculated-annual-cost presentation;
- totals and action ordering;
- Confirm information lists; and
- no customer-visible `Estimated` score label, raw sources or internal-only fields.


# Open questions

These decisions are still open for the report engine, as of 4 November 2026. Record each answer in the governing source documents, then recopy them into `docs/governing/` before changing the code.

## Blocking

1. **No overall score for the cover.** When every requested service is Confirm information or otherwise unscored, the report has no overall Bills Health Score. The renderer contract has no cover for this case, so `build` refuses. A founder treatment is needed, for example a cover with no gauge and a fixed sentence.

## For the founder's visual check

The renderer had to make these choices because the contract does not settle them. None of them changes a figure.

1. **Findings.** Founder-selected findings appear under **What this means**, after the limitation, the estimate note, the energy sentence and the provider note.
2. **Action card colours** (priorities page). The accent is green for Stay put. For other actions it follows the service's score band (red Poor, amber Medium, green Good), or is neutral when there is no score.
3. **"Estimated" beside a shown potential saving.** The approved template has this label, and REPORT_OUTPUT_QA §3 requires a shown saving to be identified as an estimate. It never appears beside a score.
4. **Cover top-right.** It reads "Bills Health Report", then the customer's first name. This replaces the sample's "Fictional example".
5. **Totals label.** The totals are labelled "Annual spend" (renderer contract §3), not the template's "Annualised spend", because energy's figure is a calculated cost.
6. **Services not requested.** In the overview, a service that was not requested shows "Not analysed" under Market position, as the template does. "—" is used for a service that has a page but no score.
7. **Removed sample boxes.** These boxes were removed because no content field feeds them:
   - "One combined analysis" on the combined energy page;
   - "No conclusion yet" on the Confirm-information page;
   - "Staying put is still a useful outcome" on the action plan.
8. **Figure row.** The new figure row sits under the current-service details and is styled from the existing fact and saving styles.
9. **"No end date known".** This text is used for both `no_end_date` and `unknown` (contract §8). On a variable tariff it sits next to the finding "Your current tariff has no fixed end date". Using "No fixed end date" for `no_end_date` would remove the mismatch.
10. **Footer.** It reads `<report id> · Version <n> · Page <i> of <total>`.

## Known limits by decision

- **Provider-quality note.** The note stays blocked until Evidence confirms that the score tables' sources are public. Both tables have `sources_publicly_accessible: null`, so a case where provider quality lowers the band stops with `METHOD_OR_SOURCE_RULE_MISSING`.
- **Economy 7 and other multi-rate meters.** These stop safely. The register-level route is not built.

## Source-document tidy-ups (for the next refresh)

- Renderer contract §3 says the overview has "one row for every *requested* service unit". Services that were not requested also appear in the overview (§2), so it should say "every service".
- `docs/governing/MEMORY.md` still links to `DECISION_REGISTER.md`, which is deliberately not in this repo.

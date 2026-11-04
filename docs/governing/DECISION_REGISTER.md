# Billvisor CEO Decision Register

## Purpose

Maintain one authoritative view of unresolved founder decisions, active hypotheses and resolved cross-team decisions. This register supports decisions; it does not replace [MEMORY.md](MEMORY.md), specialist evidence or the founder's final judgement.

## Rules

- Do not treat an open decision, option or hypothesis as a confirmed fact.
- Record only evidence that has actually been reviewed.
- State when evidence is missing, indirect, conflicting or stale.
- Do not invent a recommendation merely to complete an entry.
- Add confirmed cross-team decisions to `MEMORY.md` only after founder approval.
- Link to specialist detail instead of duplicating changing methods or evidence.

## Status definitions

- **Open:** founder decision required.
- **Evidence gathering:** an approved investigation is in progress.
- **Ready for decision:** the agreed evidence is available.
- **Decided:** founder has resolved the question.
- **Deferred:** intentionally postponed with a stated trigger for reopening.

# Active decisions

## D-001 — Initial UK energy geography

- **Status:** Decided
- **Decision required:** Whether Phase 1 energy cases initially include Northern Ireland or begin with Great Britain only.
- **Why it matters:** Northern Ireland has a different energy market and requires an adapted evidence and recommendation workflow.
- **Confirmed facts:** The launch market is UK first. Broadband, mobile, gas and electricity are supported services.
- **Evidence available:** Ofgem regulates energy in England, Scotland and Wales. Northern Ireland has a separate Utility Regulator, supplier structure, regulated tariffs, gas network areas and Consumer Council comparison sources.
- **Options:** Great Britain initially; UK including Northern Ireland with a separately validated workflow.
- **Dependencies:** Welcome-email eligibility wording, energy methodology and offer sources must reflect the decision. No additional report status is currently approved.
- **Founder decision:** Phase 1 gas and electricity analysis initially supports households in England, Scotland and Wales. Northern Ireland energy is deferred until a separate market methodology, evidence base and customer need are validated. This does not automatically exclude Northern Ireland households from broadband or mobile support.
- **Decision date:** 16 July 2026.

## D-002 — First-response promise

- **Status:** Open
- **Decision required:** What response time, if any, is promised publicly after signup.
- **Why it matters:** It affects customer expectations, operational capacity and delay communication.
- **Confirmed facts:** The journey continues by email. No current public promise is approved.
- **Evidence available:** No live response-time or abandonment data.
- **Options:** Pending founder decision and operational testing.
- **Dependencies:** Email tooling, service hours and pilot capacity.
- **Founder decision:** Pending.

## D-003 — Report-turnaround promise

- **Status:** Open
- **Decision required:** What report-delivery time is promised after sufficient evidence is received.
- **Why it matters:** It affects trust, workload, QA and user expectations.
- **Confirmed facts:** The user must be told when they are waiting; delays should be communicated before a promised deadline passes.
- **Evidence available:** No live analyst-time or QA-time data.
- **Options:** Pending operational dry runs and founder decision.
- **Dependencies:** Evidence requirements, Operations workflow, Review-agent pre-export data/content QA capacity and founder approval capacity.
- **Founder decision:** Pending.

## D-004 — Email, customer-record and document-handling stack

- **Status:** Partially decided — temporary pilot record and Netlify landing-page/form stack selected and dummy-tested; compliance launch review and permanent database pending
- **Decision required:** Which tools handle signup, email, source documents, report production, delivery and deletion.
- **Why it matters:** The choice materially affects privacy, security, deletion and operating effort.
- **Confirmed facts:** Source documents are deleted seven days after the final customer interaction for which they are needed. Report production is HTML-first: Operations creates the final fixed-A4 HTML after content approval and pre-export data/content QA; the founder manually saves it as PDF and delivers it.
- **Evidence available:** The founder uses Namecheap Private Email purchased after 2 June 2026, which places it on Namecheap's new platform. Namecheap documents webmail 2FA, app passwords, filters/auto-reply, attachment support, live-mail deletion controls and backups of up to four weeks. Before committing to a permanent database, the founder chose a bounded internal workbook to learn the real customer-record workflow during the manual pilot. The founder selected Netlify hosting and Netlify Forms for the landing page on 2 November 2026. Both separately named static forms were detected after production deployment; honeypot protection is enabled; a founder-controlled test submission appeared in the Netlify dashboard and notification reached `anton@billvisor.com`. No completed review yet establishes Netlify's actual processing locations, UK transfer mechanism, subprocessor list, dashboard/log/backup retention or deletion behaviour for this use.
- **Options:** Confirmed temporary pilot workbook for structured customer records; a permanent external database is deferred. The temporary source-document component is selected for the founder-only pilot: Namecheap webmail plus a restricted local folder outside the Business Planning/Codex workspaces that must not be cloud-synchronised. The selected landing-page stack is the existing custom HTML/CSS site hosted on Netlify, with two Netlify Forms that collect first name and email, use a honeypot, retain submissions in the Netlify dashboard and notify `anton@billvisor.com`. The report-production route is resolved under R-014.
- **Dependencies:** D-005, D-006 and D-013.
- **Founder direction:** Use Namecheap Private Email on the post-2 June 2026 platform for customer communications only and do not treat the mailbox as the customer database. Netlify and Netlify Forms are the selected landing-page route; do not invite real sign-ups until Compliance has reviewed the actual configuration. During the initial validation pilot, use the approved internal workbook for customers, services, reports, interactions and document-deletion metadata; never store source documents in it. Keep the pseudonymous time-and-unit-cost tracker separate and link it through Report ID. Use founder-only webmail access, FileVault, mailbox and main-account 2FA, and the restricted Time-Machine-excluded `/Users/anton/Billvisor-Customer-Documents` folder for temporary source documents. Do not upload original identifiable source documents to AI agents. Reassess after the earlier of 25 households or three months, or sooner if operational reliability deteriorates, before selecting a permanent database.
- **Controls to verify:** Obtain and review Netlify evidence for UK transfer safeguards, processing locations, subprocessors, dashboard/log/backup retention and deletion; confirm the practical procedure and owner for deleting form submissions after the approved 30-day no-continuation period; verify spam controls and notification routing; complete the public privacy and contact pages plus remaining privacy-notice/lawful-basis/address questions; test the pilot workbook and temporary document workflow in a dummy case; verify no uncontrolled forwarding, attachment and Trash deletion, Namecheap backup limitation and deleted-mail behaviour.
- **Evidence still needed:** Compliance must review the selected Netlify configuration and public-facing wording before real sign-ups are invited. Test the pilot workbook and approved temporary document workflow in a dummy case; use pilot evidence to decide whether and when a permanent database is needed.
- **Remaining founder decision:** Approve purchase and launch only after the compliance and implementation gates pass; select a permanent database only when pilot evidence justifies it.

## D-005 — Document transfer method

- **Status:** Pilot decision made — validation and qualified review pending
- **Decision required:** Whether users may attach source documents directly to email, use a secure upload route, or use an approved combination.
- **Why it matters:** It affects customer effort, trust, security and deletion implementation.
- **Confirmed facts:** Users may provide information in the easiest appropriate form. For the initial founder-only pilot, direct Namecheap Private Email attachments are the approved customer document channel, subject to the launch-gate controls and targeted qualified review.
- **Evidence available:** The current UX and research documents identify the question but do not resolve it.
- **Options:** Direct attachments; secure upload; controlled combination.
- **Dependencies:** D-004 and D-013.
- **Founder decision:** Use direct email attachments for the initial pilot. The founder manually extracts the necessary case facts, does not upload original identifiable source documents to AI agents, and deletes every source copy under the approved seven-day workflow. This is a pilot operating decision, not validated evidence that attachments are the best long-term channel.
- **Evidence still needed:** Complete the dummy deletion test and targeted D-013 review of the actual email, local-storage, backup and deletion behaviour; observe whether attachments are materially easier for target users than alternatives.

## D-006 — Retained service-record policy

- **Status:** Decided
- **Decision required:** Which non-source records are retained, for what purpose and for how long.
- **Why it matters:** Reports, correspondence metadata, complaints, research records and operational logs cannot be retained without a defined purpose and policy.
- **Confirmed facts:** The seven-day deletion rule applies to source documents, not automatically to all service records.
- **Evidence available:** ICO storage-limitation guidance requires a stated purpose, justified standard periods, review and deletion or anonymisation when the purpose ends. It does not prescribe a universal period.
- **Options:** Short fixed retention; purpose-based 24-month service record; indefinite retention was rejected as unjustifiable.
- **Dependencies:** D-004 must implement the schedule across the selected tools; D-013 must confirm the final purposes, wording and implementation. Complaint and incident schedules remain separate.
- **Founder decision:** Delete source documents under the seven-day rule. Retain the structured customer service record, reports, necessary internal notes, attachment-free service correspondence and QA/correction history for 24 months after the last substantive service interaction. A new report or substantive clarification resets that period. Reuse stored structured information and ask the user to confirm or update it; request new documents only when confirmation cannot support a reliable recommendation. Merely scheduling or sending a reminder does not reset the full record. A minimal explicitly requested reminder record may remain until 30 days after the reminder date. Review retained records at least annually and delete or genuinely anonymise them when the purpose ends.
- **Decision date:** 16 July 2026.

## D-007 — Minimum evidence by supported service

- **Status:** Decided
- **Decision required:** Define the minimum evidence required to analyse broadband, mobile, gas and electricity, including when a submitted service must be marked Analysed with limitations.
- **Why it matters:** It controls recommendation quality, customer effort and consistent scope labels.
- **Confirmed facts:** The service must request only information that materially improves the result and must distinguish Analysed, Analysed with limitations and Not analysed.
- **Evidence available:** Ofcom contract information and Ofgem tariff/switching guidance identify relevant decision fields, but energy information may be split across a bill, annual statement, Tariff Information Label, contract communication or online account. One document is not guaranteed to contain everything.
- **Options:** Exhaustive upfront request; recent document required; low-friction starting fields followed by decision-critical follow-up only.
- **Dependencies:** Evidence identifies decision-material gaps and supplies qualified case evidence; Operations consolidates any follow-up and prepares the structured content; the founder approves the recommendation and wording; Review checks the data/content before final HTML generation.
- **Founder decision:** Use a low-friction welcome-email request. Broadband: provider, speed, monthly cost and contract end date. Mobile: provider, data allowance, important extras or handset inclusion, monthly cost and contract end date. Gas/electricity: postcode, supplier, whether gas, electricity or both, approximate monthly payment, how the bill is paid, tariff type/name and end date if known, plus bedrooms when annual usage is unavailable. Invite a recent bill because it can improve accuracy, but do not require one. Ask the user to mention prepayment or multi-rate metering, electric heating, a heat pump or regular home EV charging. Users may tell Billvisor what they know or attach a relevant document and need not transcribe attachment content. Review supplied information first, extract useful fields, never assume one document is complete, and ask one consolidated follow-up only for information that could change the recommendation. Request another document only when a short answer or confirmation is insufficient. Do not make a strong savings or switching claim when decisive evidence is missing. For energy, prefer actual previous-12-month consumption or the supplier's estimated annual consumption by fuel. If neither is available, select the ordinary profile by bedrooms only: 1–2 = Ofgem low (1,600 kWh electricity; 6,000 kWh gas), 3–4 = Ofgem medium (2,500; 9,500), and 5+ = Ofgem high (3,800; 14,000). The values are the Ofgem TDCVs effective 1 July 2026; the bedroom mapping is Billvisor's adoption of a current comparison-industry convention rather than an Ofgem-defined classification. Monthly payment is only a sense-check. Tell the customer only that consumption was estimated from households with similar characteristics; do not expose the source bands or internal arithmetic. This route is Analysed with limitations. Do not use the ordinary bedroom-based fallback for specialist or multi-rate arrangements, including materially different usage patterns such as electric heating, heat pumps or home EV charging, without suitable usage evidence.
- **Decision date:** Initial minimum evidence 16 July 2026; energy-consumption fallback added and simplified to a bedroom-only profile selector 14 August 2026.

## D-008 — Pilot duration, capacity and sample

- **Status:** Open
- **Decision required:** Approve the number of households, study duration and allocation between interviews, live cases and adversarial cases.
- **Why it matters:** It determines workload and what conclusions the evidence can support.
- **Confirmed facts:** Phase 1 is manual and validation-first.
- **Evidence available:** The research plan proposes six weeks and 30 households; this is not approved.
- **Options:** Founder-approved design after reviewing capacity and decision needs.
- **Dependencies:** D-002, D-003, D-007 and QA capacity.
- **Founder decision:** Pending.

## D-009 — Validation thresholds and stop rules

- **Status:** Open
- **Decision required:** Pre-agree the behavioural thresholds for continuing, narrowing, redesigning, pausing or stopping.
- **Why it matters:** Thresholds selected after results would permit confirmation bias.
- **Confirmed facts:** Success means trust, useful reports, repeat uploads and referrals rather than revenue or switching volume.
- **Evidence available:** Measures are proposed in the research and UX documents; no thresholds are confirmed.
- **Options:** To be proposed by Research and approved before live testing.
- **Dependencies:** D-008.
- **Founder decision:** Pending.

## D-010 — Recruitment method and incentive

- **Status:** Open
- **Decision required:** Approve initial recruitment sources and whether participants receive an incentive beyond the free report.
- **Why it matters:** Recruitment source and incentive can distort trust, demand and referral evidence.
- **Confirmed facts:** No launch channel is validated.
- **Evidence available:** The research plan lists channel hypotheses but does not recommend one conclusively.
- **Options:** To be proposed as bounded acquisition tests.
- **Dependencies:** D-008 and D-009.
- **Founder decision:** Pending.

## D-011 — Vulnerability and urgent-harm policy

- **Status:** Decided
- **Decision required:** Approve identification, service boundaries, escalation and signposting for urgent or vulnerable cases.
- **Why it matters:** Threatened disconnection, fraud, acute debt, legal deadlines and accessibility needs may be unsafe to handle through the normal service.
- **Confirmed facts:** The service must stay within its approved scope and protect household outcomes.
- **Evidence available:** Operations and Research documents identify example risks. The founder has decided that building a referral or urgent-support workflow is disproportionate for Phase 1.
- **Options:** Specialist referral workflow; minimal out-of-scope response.
- **Dependencies:** D-013 must review the final wording and data handling, but no referral directory is required for Phase 1.
- **Founder decision:** Phase 1 will not provide urgent, emergency, debt, fraud or legal support and will not build a referral operation. Send a brief, compassionate unable-to-help email, request no further information, stop the case and delete any source documents received under the approved handling process. Normal accessibility needs within an otherwise in-scope report remain part of clear customer service rather than an automatic exclusion.
- **Decision date:** 16 July 2026.

## D-012 — Optional direct-marketing consent

- **Status:** Decided
- **Decision required:** Whether marketing consent is requested in Phase 1 and, if so, where and how.
- **Why it matters:** Requested service communication and marketing must remain distinct.
- **Confirmed facts:** The email service and report do not themselves establish marketing permission.
- **Evidence available:** ICO guidance distinguishes requested service communication from direct marketing and warns that promotional content can make a service message direct marketing.
- **Options:** No Phase 1 marketing consent; separate optional consent at an approved point.
- **Dependencies:** Any future marketing or promotional update requires a new decision and appropriate PECR/data-protection review.
- **Founder decision:** Phase 1 may use public content, paid advertising and other approved acquisition channels. It will not request marketing consent or send promotional communication to people who supplied their email for the Bills Health Report. Service records are not authorised for advertising, retargeting or general marketing. Potential promotional email, customer-list advertising and future feature campaigns require a new decision and appropriate review.
- **Decision date:** 16 July 2026.

## D-016 — Proactive contract-end review

- **Status:** Decided
- **Decision required:** Whether Billvisor may retain a contract end date and proactively contact a specific user with a new review when that service approaches contract end, and whether this is Phase 1 or a later capability.
- **Why it matters:** This could create useful proactive value, but it changes the service from a one-off requested report into monitoring and later outreach. It also creates retention, transparency and PECR questions.
- **Confirmed facts:** Phase 1 may use approved public acquisition, but requests no marketing consent and does not use service records for promotional communication or advertising. Source documents are deleted under the seven-day rule. No policy currently authorises retention of contract end dates for proactive promotional outreach.
- **Evidence available:** ICO guidance says genuinely requested service messages are treated differently from direct marketing, while promotional content can make a service message direct marketing. The classification depends on the actual user agreement, purpose and message.
- **Options:** Explicitly requested reminder service; later opt-in feature; no proactive outreach during Phase 1.
- **Dependencies:** D-006 must approve the minimum reminder record and retention period; D-013 must review the exact customer promise and message.
- **Founder preference:** The founder wants the ability to send a service-specific review when a known contract end date approaches.
- **Founder decision:** Phase 1 may test a contract-end reminder opportunistically when a report naturally identifies an upcoming end date. It is not a core journey, public promise, acquisition feature or success metric. Ask the user explicitly; retain only the minimum approved reminder record; delete the source bill under the normal rule; request fresh evidence at review time; keep the reminder service-only; and do not build monitoring automation without repeated evidence of value.
- **Decision date:** 16 July 2026.

## D-013 — Pre-launch compliance review

- **Status:** Decided
- **Decision required:** Define the professional and internal review required before accepting real household documents.
- **Why it matters:** The service handles personal documents and may encounter consumer, regulatory and vulnerability boundaries.
- **Confirmed facts:** AI-generated analysis is not a substitute for qualified UK legal or data-protection advice.
- **Evidence available:** ICO small-business guidance requires a documented data purpose and lawful basis, transparent privacy information, proportionate security, processor controls and DPIA screening where relevant. PECR distinguishes requested service communication from marketing.
- **Options:** Internal preparation only; proportionate hybrid review; broad external legal programme.
- **Dependencies:** The approved review must examine the actual decisions and implementation produced by D-004, D-005, D-006, D-011 and D-012.
- **Founder decision:** Use a proportionate hybrid compliance review before accepting live household documents. Complete ICO-aligned internal preparation, then obtain targeted qualified UK review of the actual Phase 1 data flow, customer communications, retention, PECR and service boundaries. A broad legal programme is not required unless the targeted review identifies a material issue.
- **Decision date:** 16 July 2026.

## D-014 — Energy provider-quality methodology

- **Status:** Partially resolved — normalisation and support sub-weighting pending
- **Decision required:** Approve how energy-provider quality is assessed and evidenced before it influences reports.
- **Why it matters:** Broadband and mobile have service-specific methods; gas and electricity do not yet have an equivalent approved provider-quality method.
- **Confirmed facts:** Broadband or mobile weights must not be imported into energy.
- **Evidence available:** The offer-data draft addresses tariffs but not an approved energy provider-quality score.
- **Options:** Descriptive evidence only initially; develop and approve an energy-specific provider scoring system.
- **Dependencies:** D-001 and Evidence capacity.
- **Founder direction:** Develop a separate energy-provider scoring system. Do not import broadband or mobile categories, weights or evidence rules.
- **Founder decision:** Use Billing & Metering 50% and Customer Support & Complaint Resolution 50%. Remove Account & Switching Administration as a separate numeric category because the evidence review found no comparable provider-level dataset. Map relevant final-bill or complaint evidence to the applicable remaining category; keep other switching/account incidents as context or caution evidence without invented points. The equal split is a Phase 1 simplification, not a data-proven optimum. Keep serious regulatory or financial concerns outside the numeric score as a caution overlay. Do not score physical network reliability, price, tariff suitability or postcode availability as provider quality. Prioritise Citizens Advice underlying supplier data, Ofgem and Energy Ombudsman evidence; do not double-count republished or composite evidence, and do not use marketing or individual review platforms to set scores. Start with the six largest supplier groups evidenced in Ofgem's January 2026 report—Octopus Energy, British Gas, E.ON Next, OVO Energy, EDF Energy and ScottishPower—then add suppliers triggered by real customer cases or credible alternatives. Do not automatically transfer group evidence to a separately operated retail brand.
- **Pending decision:** Approve numeric normalisation thresholds and the internal balance between contactability and complaint outcomes inside Customer Support & Complaint Resolution before provider scores become operational.
- **Decision date:** 16 July 2026.

## D-015 — Offer-data decisions required for live reports

- **Status:** Partially resolved — outcome thresholds pending
- **Decision required:** Identify and resolve only the offer-data questions necessary to support the first live reports.
- **Why it matters:** Building a complete catalogue before validation may create unnecessary work, while inadequate current-market evidence could make recommendations unsafe.
- **Confirmed facts:** Offer data is an evidence input, not the recommendation algorithm. Decision-driving offers must be rechecked for a live case.
- **Evidence available:** `PHASE_1_OFFER_DATA_METHOD.md` contains the active live-case method. Historical tests showed that exhaustive evidence packs increased effort without improving the directional guidance required in Phase 1.
- **Options:** The founder selected a narrow live-case provider-balanced benchmark rather than a standing catalogue or exhaustive case evidence assessment.
- **Dependencies:** D-007, D-008 and initial case mix.
- **Founder decision:** For an ordinary live broadband or mobile case, Evidence uses founder-pasted results for broadly comparable packages and calculates each package's approximate effective monthly price across the first 12 months, including compulsory charges and known promotional periods or rises and excluding rewards. It groups packages by provider, calculates the mean for each provider, then uses the median of those provider-level means as the live-case benchmark so providers with more listings do not dominate it. Use advertised prices as reasonable working estimates when a future rise is unquantified; exclude only unusable prices or plainly non-comparable results. Customer current annual spend is monthly payment × 12; annual benchmark is the monthly benchmark × 12; approximate potential annual saving is current annual spend minus annual benchmark and appears only when positive and judged useful. Never display a £0 potential saving. Keep provider averages, individual offers, sources, sample arithmetic and research process internal. Retain the approved report structure, page count and visual design but simplify customer language to short outcomes, reassurance and one action. Green outcomes should visibly confirm when staying put is sensible. Do not time-cap the Evidence task; keep it quick by limiting scope. Do not turn deliberately unrequested customer information into a limitation. This offer-list benchmark does not apply to energy, which remains governed by its household-specific tariff method.
- **Display convention:** Retain exact values internally and round all customer-facing annual figures to the nearest whole pound. Keep “benchmark” internal-only; customer wording says what similar services cost and introduces that approximate comparison figure with “about”. Do not prefix the potential-saving figure with “about” because the adjacent wording already identifies it as an estimate. Describe current annual spend as annualised from the submitted monthly payment, not as a forecast.
- **Pending decisions:** Define any future numeric green-versus-amber threshold and what positive saving is useful enough to display. Until then, outcome classification and saving display are explicit founder case judgements and must not be automated.
- **Decision dates:** Initial lean method 19 July 2026; provider-balanced benchmark, customer-output revision and display convention 27 July 2026.

## D-017 — Bills Health Score methodology

- **Status:** Decided and implemented; real-world validation pending
- **Decision required:** Whether and how the service-level and overall Bills Health Scores shown in the approved report design should be calculated for live reports.
- **Why it matters:** A numeric score appears analytical and precise. Without a defined method, it could contradict the underlying recommendation, overstate evidence quality or combine unlike services misleadingly.
- **Confirmed facts:** The founder approved the report's visual direction with an overall score, service scores and RAG-style presentation. A service may now receive a clearly labelled Estimated score when a reasonable price comparison exists but a material input is estimated or not fully matched. The current template figures are fictional examples, not customer calculations.
- **Evidence available:** Broadband and mobile provider-quality scores and the live offer benchmark provide usable inputs. Energy provider scores remain blocked pending normalisation. The founder-approved method supplies the household calculation; its comprehension and practical usefulness remain hypotheses to validate in the pilot.
- **Dependencies:** A service can be scored only where the method's required price input exists. Provider-quality gaps follow the approved price-only limitation route. Energy scoring remains constrained by D-014 and the available household-specific tariff comparison. Real-world comprehension testing remains required but does not alter the confirmed calculation without a new founder decision.
- **Founder decision:** For an analysed service, weight price position at 90% and the current provider's relative position in the applicable approved provider-quality table at 10%. Contract status does not affect the score; it informs recommendation timing or practicality. Rank providers by approved raw quality score and give tied providers their average ordinal rank. Convert position to 0–100 using `100 × (worst observed rank − provider rank) ÷ (worst observed rank − best observed rank)`, so every provider tied at the top receives 100, every provider tied at the bottom receives 0 and other ties share the same intermediate value. Keep evidence confidence separate and retain the provider-table version/date internally because adding providers changes the relative positions. Replace the former proportional price curve with `min(100, 20 + 60 × comparison price ÷ current price)`, which scores a price 25% below comparison at 100, equal at 80, 25% above at 68, 50% above at 60 and 100% above at 50. After the 90/10 calculation, cap the service score at 39 when potential annual saving is at least £150 and at least 25% of current annual spend; cap it at 74 when saving is at least £100 and at least 15%; otherwise apply no materiality cap. A reasonable but incomplete comparison may produce a clearly labelled Estimated score under Analysed with limitations, with the material limitation stated on the service page. Approved Energy cases are (1) a supportable like-for-like payment-method cost when regional basis, consumption, fuels, meter type and tariff type match, or (2) for electricity-only Economy 7, actual peak/off-peak readings compared with a regional Direct Debit single-rate reference over the same measured billing-day sample. The second route is an Estimated tariff-fit score only: it does not authorise a best-deal, whole-market or alternative-provider saving claim. If neither a reliable nor reasonable estimated comparison exists, issue no score. Final bands remain Poor 0–39, Medium 40–74 and Good 75–100. These rules are founder-defined Phase 1 policy to validate rather than data-proven optima.
- **Display rule:** Retain exact calculated values internally. Display the nearest whole-number score, round `.5` upwards and apply Poor, Medium or Good to the displayed rounded number so the number and band cannot visibly conflict.
- **Overall-score decision:** Use the weighted average of all numeric service scores. Weight an **Analysed** service at 1.0 and an **Analysed with limitations** service at 0.8, including clearly labelled Estimated service scores. Exclude Not-analysed services and any service without a numeric score. The 0.8 factor applies only to overall aggregation; it does not reduce or alter the displayed service-specific score. If only one service has a score, that score becomes the overall result; if none has a score, display no overall score.
- **Provider wording decision:** Treat provider commentary as a material explanation rather than a routine provider label. Band the price-only result and the combined 90/10 service result separately. Show a negative provider-quality note only when adding provider position moves the combined service score into a lower Poor/Medium/Good band than the price-only result. Use: “Recent public data indicates that your current provider has weaker [service-relevant quality areas] results than some others. This lowered your [service] rating from [price-only band] to [combined band].” Use “public data” only when the underlying sources are genuinely publicly accessible. Show no positive note for a strong provider and no provider note when provider quality does not change the service band. Use reliability and customer support for broadband; network experience and customer support for mobile; billing and customer support for energy. Do not expose source names, ranks or internal scores, call the evidence “reviews,” use absolute good/bad labels or imply whole-market coverage. Include one report-wide “Supporting source details are available on request” line and retain the exact support internally.
- **Validation result:** Founder approved the representative price, provider, incomplete-input and mixed-service worked examples on 5 August 2026. The 17 August dry run then exposed an implausible 0/100 mobile result and excessive distortion when absolute savings were applied without considering saving share. The founder approved the revised non-linear curve, dual-threshold materiality caps and Estimated service-score treatment using the dry-run outcomes: Broadband 39 Poor, Mobile 45 Medium Estimated and Energy 75 Good Estimated. The same case produces an overall score of 52 Medium under the later 1.0/0.8 status-weighted average. This is one calibration case, not real-world validation.
- **Implementation result:** The calculator and report route implement the revised curve, dual materiality caps, clearly labelled Estimated service scores, the approved Energy payment-method and Economy 7 tariff-fit routes, and the status-weighted overall average. Automated branch tests passed; this verifies implementation consistency, not customer comprehension or real-world calibration.
- **Open display clarification (19 August 2026):** In the second recommendation-framework calibration case, the founder rejected the word **Estimated** beside the mobile score. It is not yet confirmed whether this removes the visible label from every limited-input score and relies instead on **Analysed with limitations** plus the service-page limitation. Until the founder confirms a global rule, the existing approved Estimated-score display remains authoritative and must not be changed silently.
- **Decision date:** Original method 4–5 August 2026; revised curve, materiality guardrail and Estimated service scores approved 17 August 2026.

## D-018 — Single-owner ordinary case production

- **Status:** Decided and implemented
- **Decision required:** Remove unnecessary specialist handoffs from ordinary Phase 1 report production without weakening evidence or founder approval.
- **Why it matters:** The timed repeat energy test exceeded 14 minutes before Review or HTML generation, while the instrumented calculation and validation took 39.6 seconds. Repeated specialist activation and context loading, rather than arithmetic, was the dominant delay.
- **Founder decision:** Operations owns each ordinary live case from intake through delivery. The founder performs any required interactive market search, supplies captured results and approves the recommendation and exact customer content. Operations applies approved deterministic calculations, prepares one consolidated approval package, initiates any risk-triggered Review, generates the HTML and completes the case record. Evidence remains method owner and exception-only. Review is governed by D-020 rather than being a mandatory handoff in every case.
- **Implementation result:** The compact calculator enriches the same case record rather than creating a parallel system. It deterministically calculates approved broadband/mobile offer comparisons and scores, Energy annual tariff costs and saving candidates, the approved payment-method and Economy 7 tariff-fit Estimated-score routes, and the 1.0/0.8 status-weighted overall average. It does not select recommendations, customer wording, useful-saving display or a broader Energy market comparison. The policy now permits a deterministic no-Review gate for non-triggered cases, but the generator implementation of that conditional gate requires Operations validation under D-020.
- **Decision date:** 14 August 2026.

## D-019 — Phase 1 recommendation framework

- **Status:** Partially resolved — action types, input boundaries, decision sequence and qualitative effort levels approved; case calibration pending
- **Decision required:** Define how supported case findings lead consistently to one household recommendation without treating the Bills Health Score as an automatic decision.
- **Why it matters:** The current calculation route can produce scores and comparison figures, but founder-only case judgement remains a consistency and handling-time risk.
- **Confirmed decision:** Use five internal recommendation types: Stay put; Improve the current setup; Look at changing now; Review later; and Confirm information. The recommendation considers agreed minimum customer information, financial value, service position, household effort/disruption and timing/known constraints. A score supports but does not dictate the action. When the agreed minimum information is supplied for an ordinary supported case, the customer submission is sufficient. A material internal evidence or methodology gap belongs to Billvisor and may produce Analysed with limitations; it must not be framed as missing non-required customer information. Confirm information applies only to a missing agreed minimum field or a disclosed specialist arrangement that changes the required minimum. Contract status affects recommendation timing, practicality and urgency but does not currently change the score. Apply the approved sequence: check minimum information; identify supported current-setup, provider/plan-change or no opportunities; judge value together with effort and service position; apply known timing constraints; then select one strongest household action rather than automatically choosing the largest saving or easiest action. Classify the proposed action itself as Low, Moderate or High effort. Low means one straightforward change with no known equipment, installation or transfer risk; Moderate means a standard comparison and plan/provider change without unusual complication; High means a known installation, equipment, bundle, disruption or similar complication. These are qualitative working levels, not measured time promises. A larger or clearer benefit is required as effort rises.
- **Calibration:** The founder approved an out-of-contract broadband case at £39 per month versus a £23.85 similar-service comparison, approximately £182/39% potential annual saving, score 39 Poor and Moderate action effort as **Look at changing now**. This is one case, not an automatic threshold.
- **Pending decisions:** Continue calibrating financial value against effort using realistic cases; approve timing rules and the minimum support for a bounded recommendation under an internal limitation.
- **Authority:** [PHASE_1_RECOMMENDATION_FRAMEWORK.md](PHASE_1_RECOMMENDATION_FRAMEWORK.md)
- **Decision date:** Action types, input and sufficiency boundaries, decision sequence and qualitative effort levels approved 19 August 2026.

## D-020 — Risk-based Review and consolidated ordinary-case authority

- **Status:** Decided and implemented
- **Decision required:** Reduce ordinary report handling and context loading without removing the controls most likely to protect household trust.
- **Why it matters:** The repeat energy test took more than 14 minutes before Review or report generation, while instrumented calculation and validation took 39.6 seconds. This indicates that orchestration and repeated context/handoffs, not calculation, are the principal measured bottleneck. Exact token or monetary savings have not been measured.
- **Founder decision:** `PHASE_1_CASE_OPERATING_METHOD.md` is the sole Operations authority for an ordinary live case. Operations owns the route end to end and makes one consolidated founder-approval request. Review is required for the first five live reports under the method; calculator failure, manual override, or a new/ambiguous method; a primary **Look at changing now** recommendation while the recommendation framework remains unvalidated; and one in five otherwise ordinary reports after five clean cases. A Critical or Major defect resets the clean-run count and Review continues until five consecutive reviewed reports pass. Operations initiates Review. Non-sampled ordinary cases use deterministic validation; founder content approval remains mandatory for every case. Review does not inspect final HTML visually or the exported PDF.
- **Implementation result:** The structured case workflow records whether Review is required and why. The generator fails closed if that choice is absent. Triggered cases require a matching Review pass fingerprint; non-triggered cases require a matching deterministic-validation fingerprint. Founder approval requires a matching content fingerprint in both routes. Eighteen synthetic calculator and gate tests pass. This verifies implemented control logic, not live-case speed or defect rates.
- **Supersession and cleanup:** The Service Blueprint, report-generation rules, production checklist, manual-export runbook and separate conversational time-logging protocol were permanently deleted with founder approval on 19 August 2026. Their current rules were consolidated into the case operating method, implemented generator and time-and-unit-cost method before deletion. No archive was retained.
- **Evidence used:** One timed repeat energy case and qualitative review of 26 context files. The timing comparison is diagnostic, not a controlled before/after test. The proposed time and compute reduction remains a hypothesis until measured across live cases.
- **Documents affected:** Shared Memory, Agent Operating Model, Bills Health Score Method, Operations Case Operating Method, Review QA, Research pilot plan and generator approval/validation gates.
- **Decision date:** 19 August 2026.

# Active hypotheses

## H-001 — Distinct unresolved household job

- **Hypothesis:** UK households have a material need for independent, explainable bill guidance that is not adequately resolved by the alternatives they currently use.
- **Current support:** Adjacent market evidence shows bill and contract decisions exist.
- **Contradicting or limiting evidence:** No direct Billvisor user evidence or complete alternative-behaviour study exists.
- **Test:** Alternative-behaviour research, problem interviews and the live email journey.
- **Success or failure criterion:** Pending D-009.
- **Owner:** Research.
- **Result:** Not tested.

## H-002 — Conversational email reduces effort and supports trust

- **Hypothesis:** A landing page followed by conversational email is sufficiently easy and credible for households to provide the evidence needed for a useful report.
- **Current support:** Founder product hypothesis only.
- **Contradicting or limiting evidence:** Email may create delay, document-security concern or a long clarification chain.
- **Test:** Prototype comprehension, trust exercise and live pilot.
- **Success or failure criterion:** Pending D-009.
- **Owner:** Research, using Operations prototypes.
- **Result:** Not tested.

## H-003 — The report creates actionable clarity

- **Hypothesis:** One clear next step plus a brief explanation helps households understand what is and is not worth their time.
- **Current support:** Founder-defined service purpose.
- **Contradicting or limiting evidence:** No report-comprehension or outcome data exists.
- **Test:** Stay, switch, limitation and multi-service report prototypes followed by live cases.
- **Success or failure criterion:** Pending D-009.
- **Owner:** Research.
- **Result:** Not tested.

## H-004 — Staying put is experienced as valuable

- **Hypothesis:** Households value a well-supported recommendation to stay put rather than judging the service only by savings or switching.
- **Current support:** Positioning intent only.
- **Contradicting or limiting evidence:** No comparative user evidence exists.
- **Test:** Include credible stay cases and compare comprehension, trust, effort and referral outcomes.
- **Success or failure criterion:** Pending D-009.
- **Owner:** Research.
- **Result:** Not tested.

## H-005 — Multi-service reporting adds value without disproportionate effort

- **Hypothesis:** One report covering any submitted combination of four supported services is more useful than separate reviews without creating excessive evidence burden or generic recommendations.
- **Current support:** Confirmed product design, not user evidence.
- **Contradicting or limiting evidence:** Different services require different evidence, research and recommendation logic.
- **Test:** Compare single-service and multi-service cases.
- **Success or failure criterion:** Pending D-009.
- **Owner:** Research with Operations.
- **Result:** Not tested.

## H-006 — Marketing can generate qualified report journeys

- **Hypothesis:** Targeted public content can attract households who proceed beyond email capture to a useful completed report.
- **Current support:** Founder acquisition hypothesis only.
- **Contradicting or limiting evidence:** No traffic, conversion or completed-report attribution evidence exists.
- **Test:** Bounded articles based on validated household questions; measure through completed report outcomes.
- **Success or failure criterion:** Pending D-009 and D-010.
- **Owner:** Research; Marketing only when activated.
- **Result:** Not tested.

## H-007 — Out-of-contract services present more actionable opportunities

- **Hypothesis:** An out-of-contract broadband or mobile service is more likely than an in-contract service to have a worthwhile alternative available and to be practical to change now.
- **Current support:** Founder observation and market intuition only.
- **Contradicting or limiting evidence:** An out-of-contract customer may already have a competitive price, and contract status alone does not establish availability, saving, service fit or switching effort.
- **Test:** Compare observed price position, supported potential saving and selected recommendation between in-contract and out-of-contract pilot cases.
- **Success or failure criterion:** Pending D-008 and D-009.
- **Owner:** Research using Operations case records.
- **Result:** Not tested. Do not alter the Bills Health Score on this basis unless later evidence supports a founder-approved change.

# Resolved decisions

## R-001 — Agent operating structure

- **Decision:** Use four standing functions: CEO; Research; Operations; Evidence. Use Marketing, Compliance and Review as supporting functions.
- **Date:** 16 July 2026.
- **Rationale:** Reduce duplicated ownership while preserving independent validation and report QA.
- **Evidence used:** Audit of the current shared artifact set and founder review.
- **Documents affected:** `AGENT_OPERATING_MODEL.md`, `MEMORY.md`, and later specialist restructuring.
- **Reconsider if:** Phase 1 workload or evidence shows a function requires genuinely independent permanent capacity.

## R-002 — Water removed from Phase 1

- **Decision:** V1 supports broadband, mobile, gas and electricity. Water is out of scope.
- **Date:** 16 July 2026.
- **Rationale:** Household customers generally cannot choose their water provider, so water does not currently provide enough actionable Phase 1 review value.
- **Evidence used:** Founder decision recorded in shared memory.
- **Documents affected:** Shared memory and Phase 1 specialist documents.
- **Reconsider if:** The service develops a credible actionable water-bill job beyond provider choice.

## R-003 — Initial energy geography

- **Decision:** Phase 1 gas and electricity analysis initially supports England, Scotland and Wales. Northern Ireland energy is deferred; broadband and mobile support are not automatically affected.
- **Date:** 16 July 2026.
- **Rationale:** Northern Ireland has a separate regulator, supplier and tariff structure, gas network areas and evidence sources. No current household-demand evidence justifies the additional Phase 1 methodology and operating scope.
- **Evidence used:** Current official Ofgem, Utility Regulator and Consumer Council sources reviewed for D-001.
- **Documents affected:** Shared memory, Operations eligibility and scope, Research recruitment and future energy methods.
- **Reconsider if:** A Northern Ireland methodology and evidence base are prepared and customer need is validated.

## R-004 — Pre-launch compliance approach

- **Decision:** Use a proportionate hybrid review: ICO-aligned internal preparation followed by targeted qualified UK review of the actual Phase 1 workflow before accepting live household documents.
- **Date:** 16 July 2026.
- **Rationale:** Internal preparation reduces unnecessary external work, while qualified review is still needed for the actual data flow, retention, PECR and service boundaries.
- **Evidence used:** Current ICO small-business, lawful-basis, transparency, processor/security, DPIA-screening, PECR and fee guidance reviewed for D-013.
- **Documents affected:** Compliance brief, Operations launch gate, Research live-data gate and later tool/retention decisions.
- **Reconsider if:** The data types, tools, service scope, customer claims or regulatory boundaries materially change.

## R-005 — No direct marketing to Phase 1 service users

- **Decision:** Phase 1 will not request marketing consent or send promotional communication to people who submitted their email for the Bills Health Report. Public content, paid advertising and other approved acquisition channels may be used to attract new households. Service records are not used for advertising, retargeting or general marketing.
- **Date:** 16 July 2026.
- **Rationale:** Customer acquisition and promotional use of service-user data are different activities. The former may be tested publicly; the latter would add unnecessary complexity, privacy risk and friction to the Phase 1 service.
- **Evidence used:** Founder decision and current ICO distinction between service messages and direct marketing.
- **Documents affected:** Shared memory, Operations, Compliance and future communication design.
- **Reconsider if:** Billvisor proposes newsletters, promotional email, customer-list advertising, service-record retargeting, promotional feature announcements or another non-service communication to identified users.

## R-006 — Opportunistic contract-end reminder

- **Decision:** Phase 1 may test an explicitly requested contract-end reminder when an existing case naturally identifies an upcoming end date. It is not a core promise or success metric.
- **Date:** 16 July 2026.
- **Rationale:** It can test proactive value without building a monitoring product or retaining source bills beyond the approved deletion rule.
- **Evidence used:** Founder decision; no direct customer-value evidence yet.
- **Documents affected:** Shared memory, Operations, Compliance and retained-record policy.
- **Reconsider if:** Users repeatedly request and value reminders, or the service proposes automation or promotional content.

## R-007 — Retained customer service record

- **Decision:** Retain the defined service record for 24 months after the last substantive service interaction, subject to annual review and qualified confirmation. Reuse and reconfirm structured data before requesting new documents. A minimal requested reminder record may continue until 30 days after its reminder date.
- **Date:** 16 July 2026.
- **Rationale:** Supports repeat reports and continuity without indefinite retention or unnecessary repeated document submission.
- **Evidence used:** Founder requirements and current ICO storage-limitation guidance.
- **Documents affected:** Shared memory, Operations, Compliance and tool selection.
- **Reconsider if:** Qualified review requires a change, the service purpose changes or operational evidence shows the period is disproportionate.

## R-008 — Urgent and specialist cases

- **Decision:** Phase 1 will not build an urgent-support or referral operation. Out-of-scope urgent, emergency, debt, fraud or legal requests receive a brief unable-to-help response and are not processed as reports.
- **Date:** 16 July 2026.
- **Rationale:** A specialist routing operation is disproportionate to the narrow Phase 1 report service.
- **Evidence used:** Founder scope decision.
- **Documents affected:** Shared memory, Operations, Research and Compliance.
- **Reconsider if:** Repeated cases show a material need or qualified review requires specific minimum wording or action.

## R-009 — Minimum service information

- **Decision:** Use service-specific low-friction starting fields in the welcome email, then request only decision-critical missing information after reviewing what the user supplied.
- **Date:** 16 July 2026.
- **Rationale:** Reduces customer effort while preserving the evidence standard needed for reliable recommendations.
- **Evidence used:** Founder direction and current Ofcom/Ofgem information requirements and guidance.
- **Documents affected:** Shared memory, Operations, Research and Review.
- **Reconsider if:** Pilot evidence shows repeated missing fields, excessive clarification or inability to support recommendations.

## R-010 — Agent names and file structure

- **Decision:** Use the one-word agent names CEO, Research, Operations, Evidence, Marketing, Compliance and Review. Keep parallel folders for those seven agents under `context-files/` and `data-files/`. Store governing context, methodologies and processes under `context-files`; store evidence logs, datasets, scores and generated outputs under `data-files`, based on purpose rather than file extension.
- **Date:** 16 July 2026.
- **Rationale:** Make task ownership easy to understand while maintaining a clear separation between instructions and working evidence.
- **Evidence used:** Founder operating decision following the agent restructuring and file audit.
- **Documents affected:** Shared memory, Agent Operating Model and all specialist ownership and path references.
- **Reconsider if:** The structure creates repeated ambiguity or a new standing function is explicitly approved.

## R-011 — CEO-first collaboration model

- **Decision:** Use CEO as the founder's default entry point. Delegate bounded specialist work when appropriate; use direct specialist conversations for clearly scoped, sustained work. Treat Research, Operations and Evidence as regular specialist tasks and activate Marketing, Compliance and Review when needed. Material cross-team findings and confirmed decisions return through CEO.
- **Date:** 16 July 2026.
- **Rationale:** The old chat history showed productive sustained work in Data but substantial overlap, misrouting and repeated synchronisation across General, UX, Product, Content, Research and Brand.
- **Evidence used:** Qualitative review of the old specialist conversation histories. This was not a controlled productivity comparison.
- **Documents affected:** Shared memory, Agent Operating Model and new specialist task briefs.
- **Reconsider if:** The founder repeatedly works more efficiently through direct specialist conversations or CEO routing becomes a bottleneck.

## R-012 — Content expanded into Marketing

- **Decision:** Replace the Content supporting task with Marketing. Marketing owns content strategy, acquisition messaging, audience and channel hypotheses, landing-page conversion hypotheses, campaign concepts and bounded copy assignments. Public acquisition is permitted, but promotional communication to report users and use of service records for advertising remain out of scope.
- **Date:** 17 July 2026.
- **Rationale:** A separate Content and digital-marketing task would create overlapping ownership. One Marketing task can connect content, acquisition and conversion while Operations, Research, Evidence and Compliance retain their specialist controls.
- **Evidence used:** Founder direction and review of the existing Content responsibilities. The future workload and effectiveness of the expanded role are not yet validated.
- **Documents affected:** Shared memory, Agent Operating Model, Marketing brief, language guide location and specialist task onboarding.
- **Reconsider if:** Marketing becomes too broad, produces repeated ownership conflicts or real workload supports separate content and paid-acquisition functions.

## R-013 — Founder content approval before PDF generation

- **Decision:** Before creating a PDF, Operations presents one consolidated content-approval draft containing the internal decision basis, exact delivery email and all customer-facing report wording in page order. The founder explicitly approves the exact content version after any amendments. PDF generation is blocked unless the recorded version and content fingerprint match; any later content change requires renewed approval. Review continues to check generated output only, followed by founder final delivery approval.
- **Date:** 19 July 2026.
- **Rationale:** Let the founder correct facts, recommendation framing and wording before incurring PDF generation and layout rework, while ensuring the generated report cannot drift from the approved content.
- **Evidence used:** Founder workflow decision. The expected reduction in total report time and rework is a hypothesis to measure, not an established result.
- **Documents affected:** Shared memory, Agent Operating Model, Operations blueprint/rules/checklist/runbook, Review output-QA standard, structured-input schema and permanent generator.
- **Reconsider if:** Pilot timing shows the gate adds more effort than it saves, founders repeatedly require visual context to judge wording, or the fingerprint process creates avoidable operational errors.

## R-014 — HTML-first report production and founder PDF export

- **Decision:** Operations generates one complete fixed-A4 HTML report only after founder content approval and Review-agent pre-export data/content QA. The founder opens the HTML locally, confirms the visual result and manually saves it as a PDF with print backgrounds enabled. Phase 1 does not use an automated or headless PDF renderer. Review checks the report data, calculations, service statuses, contradictions and unsupported or missing decision-driving values before final HTML generation; it does not inspect the exported PDF. This supersedes the automated PDF-generation and post-generation Review portions of R-013 while preserving the founder content-approval gate.
- **Later supersession (19 August 2026):** D-020 replaces mandatory Review on every report with the approved risk-based Review triggers and deterministic no-Review gate. The HTML-first and founder-manual-export parts of R-014 remain active.
- **Date:** 4 August 2026.
- **Rationale:** The founder found the automated PDF route disproportionately complex and inconsistent. The approved report is already HTML/CSS, and manual local export removes a fragile automation layer while preserving the customer-facing PDF attachment.
- **Evidence used:** One fictional seven-page HTML report was assembled and manually export-tested. Shared colour tokens and print-colour preservation were required before the result matched the approved visual direction. This is an initial workflow test, not evidence of reliable live-case turnaround at volume.
- **Documents affected:** Shared Memory, Agent Operating Model, Operations report rules/checklist/runbook/blueprint, Review QA standard, current report-template files and legacy automated-renderer artifacts.
- **Reconsider if:** Manual export becomes a material time or consistency bottleneck, report volume justifies automation, or repeated export defects cannot be controlled through the fixed HTML template and founder check.

## R-015 — Approved report visual direction and score authority

- **Decision:** Use the approved fixed-A4 HTML/CSS design under `/Users/anton/billvisor/design/report/` as the current report visual source. Its stable filenames use the `billvisor-report-*` convention rather than a version label. Overall and service-level Bills Health Scores use the founder-approved D-017 method in `BILLS_HEALTH_SCORE_METHOD.md`. Fictional design values must never be treated as customer calculations; every live value requires the approved internal score trace.
- **Implementation clarification (8 August 2026):** Populate the approved page files directly rather than maintaining a simplified parallel visual template. Good/Medium/Poor score arcs and labels must be green/amber/red respectively. A shared gas/electricity analysis appears as one Energy overview row. Priority actions sort by priority and then by potential saving when priority is equal. The generator validates and blocks violations of these rules.
- **Date:** 4 August 2026.
- **Rationale:** The founder preferred the original report's analytical appearance and simplicity and explicitly requested the overall score. Separating the visual decision from the calculation method preserves that direction without manufacturing false precision.
- **Evidence used:** Founder review and iterative approval of the report pages, followed by founder-approved score-method worked examples. Household comprehension testing remains outstanding.
- **Documents affected:** Shared Memory, Decision Register, Operations report rules and the approved report design.
- **Reconsider if:** User testing finds the scores confusing or misleading, or a defensible cross-service method cannot be defined without disproportionate complexity.

## R-016 — Narrow Phase 1 energy guidance

- **Decision:** Limit the default Phase 1 energy analysis to three practical checks: payment-method cost; current tariff type, timing and known exit constraints; and whether accessible current tariff evidence makes a wider review worth the household's time. Show only an estimated annual cost, a potential saving where supportable, a short explanation and one recommended action. Mention standing-charge effects only when material for a low-usage household. Do not make generic efficiency tips or extensive tariff education part of the ordinary report and do not imply whole-market coverage.
- **Score-display clarification:** The output limit applies to the additional energy narrative. It does not remove a supportable energy Bills Health Score or the existing materially triggered provider-quality note from the approved report structure.
- **Date:** 14 August 2026.
- **Rationale:** A live test showed that regional tariff calculations can support useful payment-method and review guidance, while exhaustive multi-provider searches are slow and some supplier routes are quote-gated or unreliable. The founder chose the smallest advice set that is both easy to calculate and useful.
- **Evidence used:** One South East dual-fuel test using the approved two-bedroom fallback, Ofgem regional price-cap data and accessible British Gas, OVO and Octopus tariff information. This is a process test, not evidence that the source set is representative of the whole market or that the calculation is understood by households.
- **Documents affected:** Shared Memory; Evidence energy tariff method; Operations report-generation rules and energy-page content; Review QA after specialist implementation.
- **Reconsider if:** Pilot cases show that these checks are not useful, cannot be produced efficiently, or routinely miss material household outcomes.

## R-017 — Approved Phase 1 welcome email

- **Decision:** Use the approved customer-facing welcome email in `../operations/PHASE_1_WELCOME_EMAIL_TEMPLATE.md`. It explains the report value first, then asks for both the postcode and the details for any requested service in one reply, using a short copy-and-paste layout. It makes a recent bill optional, states the energy geography, asks customers not to send bank or card details, and uses “Kind regards” as the sign-off.
- **Date:** 3 November 2026.
- **Rationale:** A real customer replied with only a postcode, indicating that the prior wording did not make the full next action sufficiently clear or easy to scan.
- **Evidence used:** One live Phase 1 customer interaction. This supports an iteration of the wording, not a proven improvement in completion or comprehension.
- **Documents affected:** Phase 1 email UX, shared memory and the Operations welcome-email template.
- **Reconsider if:** Further live cases show repeated partial replies, confusion about documents or a material reduction in reply completion.

## R-018 — Report-engine HTML integration and qualified-score presentation

- **Decision:** The internal report engine will generate the completed approved local HTML report after its calculation, founder-approval and risk-based Review gates pass. It will not generate PDFs or delivery emails; the founder continues to visually inspect the HTML and manually save the PDF. Vendor the approved report template and assets from `/Users/anton/billvisor/design/report/` into the engine repository before integration. The renderer reads approved report data only, never raw case inputs or market captures. That report data may include the household’s own submitted current-service details needed by the approved template, provided every displayed field is in the founder-approval package; mobile extras require founder-approved wording rather than raw automatic copying. A qualified/estimated-comparison indicator remains internal. Do not label a customer-facing score or gauge “Estimated”; explain the relevant limitation or estimate in the service-page narrative instead.
- **Date:** 4 November 2026.
- **Rationale:** The calculation core is viable but does not yet generate the approved report; its renderer-safe output also lacks current-service display fields. The visual score label was judged less clear than a concise service-page explanation.
- **Evidence used:** Review of the initial report-engine implementation, its 52 passing synthetic tests and its comparison with the approved Phase 1 workflow. This is an implementation decision, not evidence that the revised score presentation improves household comprehension.
- **Documents affected:** Shared memory; Bills Health Score Method; Live Case Calculator Specification; report-engine governing copies, data contract, approval pack and renderer; approved report template.
- **Reconsider if:** HTML integration creates visual/fingerprint defects, the extra approval fields slow ordinary cases materially, or real users find limitations/score presentation confusing.

## R-019 — Report-engine data inputs and ordinary-case boundaries

- **Decision:** For Energy, use the current tariff's calculated annual cost as the report's current annual spend and as Energy's overall-score weight; use the customer’s approximate monthly payment only as a sense-check. The engine's renderer-safe current-service fields are limited to: broadband provider, download speed, monthly cost and contract status/end; mobile provider, data allowance, SIM-only/handset status, monthly cost and contract status/end; and Energy supplier, fuel(s), tariff name/type, monthly payment and tariff status/end. Do not add a broadband/mobile package-name question. `handset_included` is an internal normalisation of the existing mobile handset/extras answer, not an additional customer question. Require one case-level postcode for every ordinary requested service. Keep Economy 7 and other multi-rate Energy cases outside the ordinary calculator until separately scoped; stop their Energy analysis safely. Vendor the approved synthetic report template/assets into the engine repository; keep provider-score source accessibility unset until Evidence confirms it, and copy the Review QA standard as reference while retaining human Review judgement.
- **Date:** 4 November 2026.
- **Rationale:** This gives the renderer sufficient approved information without increasing customer friction, preserves a tariff-based Energy assessment rather than treating payment schedules as consumption, and avoids turning Phase 1 into a specialist multi-rate energy product.
- **Evidence used:** Founder decisions, the approved report template and review of the existing calculator boundaries. The effect on user comprehension and turnaround time remains untested.
- **Documents affected:** Shared memory; calculator specification; report-engine template, data contract, tests and governing copies; provider-score/review references.
- **Reconsider if:** Actual cases show the selected current-service fields are unclear, payment estimates materially diverge from tariff-cost outputs in a confusing way, or multi-rate Energy cases become frequent enough to justify dedicated work.

## R-020 — Report-engine renderer contract

- **Decision:** Use `PHASE_1_REPORT_RENDERER_CONTRACT.md` as the single Operations authority for rendering approved report data into the Phase 1 HTML report. Remove Report confidence and time/difficulty claims; show founder-selected Low/Moderate/High effort instead. Map Market position directly from score band or show `—` where there is no score. Broadband/Mobile pages show the approved current-service details plus a compact annual figures row; Energy shows monthly payment and calculated annual tariff cost with the approved usage/payment explanation. Put material limitations, Energy usage explanation and any triggered provider-quality note in What this means; show Supporting source details are available on request once on the final page. The summary total definitions and Confirm-information list format are fixed by the contract.
- **Date:** 4 November 2026.
- **Rationale:** The vendored visual pages contained unapproved confidence/time claims and examples that contradicted the approved score and Energy treatment. A single explicit contract prevents renderer implementation from making further product decisions.
- **Evidence used:** Founder approval after reviewing the approved report template and the report-engine implementation handoff. The revised layout has not yet been comprehensively comprehension-tested.
- **Documents affected:** Shared Memory; Case Operating Method; Review QA; renderer contract; report-engine templates, renderer, tests and handoff.
- **Reconsider if:** User feedback finds the added figures/narrative difficult to scan, rendering becomes materially slower, or pilot evidence supports measured time guidance.

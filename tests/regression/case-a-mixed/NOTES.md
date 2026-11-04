# Case A: mixed services (synthetic)

Broadband has a useful action, energy uses the bedroom estimate, and mobile was not requested. The expected values in
`expected.json` were worked out by hand from the governing methods. They were not produced by running the engine.

## Broadband (Virgin Media, £50 a month, out of contract)
- Provider means are £28, £30, £32 and £34, so the median is (30 + 32) / 2 = **£31 a month**, or **£372 a year**.
- Current annual spend is 50 × 12 = **£600**. Saving is 600 − 372 = **£228**, which is 38% of spend.
- The saving is at least £150 and at least 25%, so the high materiality cap of **39** applies.
- Price score is 20 + 60 × 31/50 = 57.2 (Medium). The combined score is 51.48 + 0.1 × position, which is between 51.48 and 61.48 for any position, so still Medium. The band does not drop, so there is **no provider note**.
- The final score is capped at **39 Poor**.

## Energy (3 bedrooms, so 2,500 kWh electricity and 9,500 kWh gas)
- **Current tariff:**
  - electricity 2,500 × 24p + 365 × 50p = £600.00 + £182.50 = £782.50;
  - gas 9,500 × 6p + 365 × 30p = £570.00 + £109.50 = £679.50;
  - total **£1,462**.
- **Same-supplier fixed tariff:**
  - electricity 2,500 × 22p + £182.50 = £732.50;
  - gas 9,500 × 5.5p + £109.50 = £632.00;
  - total £1,364.50.
- Tariff-fit score is 20 + 60 × 1,364.5 / 1,462 = 75.9986, which displays as **76 Good**.
- The difference is £97.50, under £100, so no cap applies.
- The status is **Analysed**, using the bedroom fallback under founder ruling 1.

## Overall
- Energy's weighted term is 75.9986 × 1,462 = 20 × 1,462 + 60 × 1,364.5 = 111,110.
- Broadband's weighted term is 39 × 600 = 23,400.
- The overall score is (23,400 + 111,110) / (600 + 1,462) = 134,510 / 2,062 = 65.23, which displays as **65 Medium**.

## Totals
- Annual spend is 600 + 1,462 = **£2,062**.
- Shown savings total **£228**.
- There are **2** service pages and **2** priority actions (neither is Stay put).

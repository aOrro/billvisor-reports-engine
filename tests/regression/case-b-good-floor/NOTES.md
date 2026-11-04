# Case B: good position, small mobile saving, floor applied (synthetic)

The household's position is mostly good. Mobile has a small saving that the founder judged not worth the effort, so the 75 floor applies. The expected values in `expected.json` were worked out by hand from the governing methods. They were not produced by running the engine.

## Broadband (Zen Internet, £30 a month)
- Provider means are £28, £30 and £32, so the median is **£30 a month**, or **£360 a year**.
- Current annual spend is **£360**. There is no saving, so no cap applies.
- Price score is 20 + 60 × 30/30 = 80 (Good).
- **Provider position:**
  - Zen Internet and Community Fibre share the top overall score of 8.5, so each has an average rank of 1.5.
  - 1.5 is the best observed rank, so Zen's position is **100**.
- Service score is 0.9 × 80 + 0.1 × 100 = **82 Good**. The price-only band is also Good, so there is no provider note.

## Mobile (Vodafone, £15 a month)
- Provider means are £11, £12 and £13, so the median is **£12 a month**, or **£144 a year**.
- Current annual spend is 15 × 12 = **£180**. Saving is **£36**, which is under £100, so no cap applies.
- Price score is 20 + 60 × 12/15 = 68 (Medium).
- **Provider position**, from the tie-safe ranks on the mobile table:
  - Tesco Mobile ranks 1; EE and giffgaff 2.5; Lebara, SMARTY and VOXI 5; Vodafone and iD Mobile 7.5; Sky Mobile and Three 9.5; O2 11.
  - Vodafone's position is 100 × (11 − 7.5) / (11 − 1) = **35**.
- Service score is 0.9 × 68 + 0.1 × 35 = 64.7 (Medium). The price-only band is also Medium, so there is no provider note.
- **Floor:** the founder approved Stay put with `small_saving_not_worth_effort`, and the saving of £36 is between £0 and £50. The score becomes **75 Good**. The saving is still shown.

## Overall
- The overall score is (82 × 360 + 75 × 180) / (360 + 180) = 43,020 / 540 = 79.67, which displays as **80 Good**.

## Totals
- Annual spend is **£540**.
- Shown savings total **£36**.
- There are **2** service pages and **0** priority actions (both actions are Stay put).

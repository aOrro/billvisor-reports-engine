"""Method-level checks: offers, score, provider position, energy."""

import datetime as dt
import unittest
from decimal import Decimal as D

from billvisor import energy, offers, provider, score
from billvisor.errors import StopError


def obs(oid, provider_name, periods, one_off=None, **kw):
    o = {"observation_id": oid, "service": "broadband", "provider": provider_name, "package_label": "pkg",
         "package_attributes": {}, "recurring_price_periods": periods,
         "compulsory_one_off": one_off or {"status": "not_shown"}, "source_ref": "s", "captured_at": "2026-11-04",
         "comparison_disposition": "include"}
    o.update(kw)
    return o


class OfferMethod(unittest.TestCase):
    def test_month_end_clamping(self):
        starts = offers.period_starts(dt.date(2026, 1, 31))
        self.assertEqual(starts[:4], [dt.date(2026, 1, 31), dt.date(2026, 2, 28), dt.date(2026, 3, 31), dt.date(2026, 4, 30)])
        self.assertEqual(starts[11], dt.date(2026, 12, 31))

    def test_dated_rise_applies_from_first_period_on_or_after(self):
        # capture 4 Nov; rise effective 1 Apr 2027 -> first period start >= is 4 Apr (period 6)
        r = offers.first_year(obs("a", "X", [{"price_gbp": D("24")}, {"price_gbp": D("27"), "effective_date": "2027-04-01"}]))
        self.assertEqual(r["first_year_total"], D(5 * 24 + 7 * 27))

    def test_whole_month_promotion_then_price(self):
        r = offers.first_year(obs("a", "X", [{"price_gbp": D("20"), "months": 6}, {"price_gbp": D("30")}]))
        self.assertEqual(r["effective_monthly"], D(25))

    def test_one_off_shown_and_not_shown_wording(self):
        shown = offers.first_year(obs("a", "X", [{"price_gbp": D("21")}], {"status": "shown", "amount_gbp": D("9.99")}))
        self.assertEqual(shown["effective_monthly"], (D(252) + D("9.99")) / 12)
        hidden = offers.first_year(obs("b", "X", [{"price_gbp": D("21")}]))
        self.assertIn("not shown in capture", hidden["one_off_text"])
        self.assertNotIn("no charge", hidden["one_off_text"])

    def test_incomplete_timeline_stops_unless_unquantified_rise(self):
        with self.assertRaises(StopError) as cm:
            offers.first_year(obs("a", "X", [{"price_gbp": D("20"), "months": 6}]))
        self.assertEqual(cm.exception.issue.code, "NO_USABLE_CAPTURED_PRICE")
        r = offers.first_year(obs("a", "X", [{"price_gbp": D("20"), "months": 6}], unquantified_future_rise=True))
        self.assertEqual(r["effective_monthly"], D(20))
        self.assertEqual(r["estimated_periods"], [7, 8, 9, 10, 11, 12])

    def test_median_of_provider_means_odd_and_even(self):
        three = offers.comparison("broadband", [obs("a", "A", [{"price_gbp": D(20)}]), obs("b", "A", [{"price_gbp": D(40)}]),
                                                obs("c", "B", [{"price_gbp": D(25)}]), obs("d", "C", [{"price_gbp": D(28)}])], {})
        # A mean 30 (two offers must not dominate), B 25, C 28 -> median 28
        self.assertEqual(three["monthly_comparison"], D(28))
        two = offers.comparison("broadband", [obs("a", "A", [{"price_gbp": D(20)}]), obs("b", "B", [{"price_gbp": D(25)}])], {})
        self.assertEqual(two["monthly_comparison"], D("22.5"))

    def test_rewards_never_enter_cost(self):
        r = offers.comparison("broadband", [obs("a", "A", [{"price_gbp": D(20)}], rewards_note="£100 cashback")], {})
        self.assertEqual(r["monthly_comparison"], D(20))

    def test_exclusions(self):
        r = offers.comparison("broadband", [
            obs("a", "A", [{"price_gbp": D(20)}]),
            obs("b", "B", [{"price_gbp": D(5)}], comparison_disposition="exclude_plainly_not_comparable", exclusion_reason="5G"),
            obs("c", "C", []),
        ], {})
        self.assertEqual(r["offer_count"], 1)
        self.assertEqual({e["reason"] for e in r["excluded"]}, {"5G", "no usable price"})

    def test_unknown_disposition_is_ambiguous(self):
        with self.assertRaises(StopError) as cm:
            offers.comparison("broadband", [obs("a", "A", [{"price_gbp": D(20)}], comparison_disposition="maybe")], {})
        self.assertEqual(cm.exception.issue.code, "COMPARABILITY_RULE_AMBIGUOUS")

    def test_handset_price_not_compared_with_sim_only(self):
        o = obs("a", "A", [{"price_gbp": D(30)}], service="mobile", package_attributes={"handset_included": True})
        with self.assertRaises(StopError):
            offers.comparison("mobile", [o], {"handset_included": False})


class ScoreMethod(unittest.TestCase):
    def s(self, cur, cmp, pos):
        return score.service_score(service="broadband", current=D(cur), comparison=D(cmp), current_annual=D(cur) * 12,
                                   comparison_annual=D(cmp) * 12, provider_position=None if pos is None else D(pos))

    def test_price_curve_table(self):
        self.assertEqual(score.price_score(D("7.5"), D(10)), D(100))
        self.assertEqual(score.price_score(D(10), D(10)), D(80))
        self.assertEqual(score.price_score(D("12.5"), D(10)), D(68))
        self.assertEqual(score.price_score(D(15), D(10)), D(60))
        self.assertEqual(score.price_score(D(20), D(10)), D(50))

    def test_section_8_validation_cases(self):
        r = self.s("7.5", 10, 0)
        self.assertEqual((r["display"], r["band"], r["provider_note_triggered"]), (90, "Good", False))
        r = self.s(10, 10, 0)
        self.assertEqual((r["display"], r["band"], r["provider_note_triggered"]), (72, "Medium", True))
        r = self.s("12.5", 10, 100)
        self.assertEqual((r["display"], r["band"], r["provider_note_triggered"]), (71, "Medium", False))
        r = self.s(15, 10, 0)
        self.assertEqual((r["display"], r["band"], r["provider_note_triggered"]), (54, "Medium", False))
        r = self.s(10, 10, None)
        self.assertEqual((r["display"], r["band"], r["provider_note_triggered"]), (80, "Good", False))

    def test_calibration_broadband_high_cap(self):
        r = self.s(39, "23.85", 50)
        self.assertEqual(r["potential_annual_saving"], D("181.80"))
        self.assertEqual((r["display"], r["band"], r["materiality"]), (39, "Poor", "high"))

    def test_calibration_mobile_estimated(self):
        r = score.service_score(service="mobile", current=D(12), comparison=D(6), current_annual=D(144),
                                comparison_annual=D(72), provider_position=D(0))
        self.assertEqual((r["display"], r["band"], r["materiality"]), (45, "Medium", "none"))

    def test_calculator_spec_energy_example(self):
        r = score.service_score(service="energy", current=D("1282.2730"), comparison=D("1173.3620"),
                                current_annual=D("1282.2730"), comparison_annual=D("1173.3620"), provider_position=None)
        self.assertTrue(D("74.9038") < r["exact"] < D("74.9039"))
        self.assertEqual((r["display"], r["band"], r["materiality"]), (75, "Good", "none"))

    def test_moderate_cap_and_both_conditions(self):
        r = self.s(50, 41, None)  # saving 108 (18%) -> moderate cap 74
        self.assertEqual(r["materiality"], "moderate")
        self.assertLessEqual(r["exact"], 74)
        big_service = score.service_score(service="energy", current=D(2000), comparison=D(1850), current_annual=D(2000),
                                          comparison_annual=D(1850), provider_position=None)
        self.assertEqual(big_service["materiality"], "none")  # £150 but only 7.5%

    def test_floor_and_rounding(self):
        r = self.s(15, 12, 85)
        self.assertTrue(score.floor_eligible(r))
        f = score.apply_floor(r)
        self.assertEqual((f["display"], f["band"], f["floor_applied"]), (75, "Good", True))
        self.assertFalse(score.floor_eligible(self.s(20, 12, 85)))  # £96 saving
        self.assertEqual(score.band(39), "Poor")
        self.assertEqual(score.band(40), "Medium")
        self.assertEqual(score.band(75), "Good")

    def test_overall_weighting(self):
        ov = score.overall([
            {"unit_id": "a", "status": "Analysed", "exact": D(80), "current_annual": D(300)},
            {"unit_id": "b", "status": "Analysed with limitations", "exact": D(40), "current_annual": D(500)},
            {"unit_id": "c", "status": "Analysed with limitations", "exact": None, "current_annual": D(900)},
            {"unit_id": "d", "status": "Not analysed", "exact": None, "current_annual": D(0)},
        ])
        self.assertEqual(ov["exact"], (D(80) * 300 + D(40) * 400) / (300 + 400))
        self.assertEqual(ov["contributing_services"], 2)
        self.assertIsNone(score.overall([]))


class ProviderPosition(unittest.TestCase):
    def test_broadband_table_tie_safe(self):
        t = provider.load_table("broadband_provider_scores")
        bt = provider.position(t, "BT")
        self.assertEqual((bt["best_rank"], bt["worst_rank"], bt["rank"]), (D("1.5"), D(12), D("7.5")))
        self.assertEqual(bt["position"], D(100) * D("4.5") / D("10.5"))
        self.assertEqual(provider.position(t, "Zen Internet")["position"], D(100))
        self.assertEqual(provider.position(t, "NOW Broadband")["position"], D(0))
        self.assertEqual(provider.position(t, "Virgin Media")["position"], bt["position"])

    def test_unknown_provider(self):
        t = provider.load_table("mobile_provider_scores")
        with self.assertRaises(StopError) as cm:
            provider.position(t, "Lyca")
        self.assertEqual(cm.exception.issue.code, "NEW_PROVIDER_ASSESSMENT_REQUIRED")
        self.assertEqual(provider.position(t, "O2")["position"], D(0))

    def test_fewer_than_two_distinct_scores(self):
        t = {"table_ref": "x", "table_version": "1", "rows": [{"provider": "A", "overall": 7}, {"provider": "B", "overall": 7}]}
        with self.assertRaises(StopError):
            provider.position(t, "A")


class EnergyMethod(unittest.TestCase):
    def test_bedroom_bands(self):
        for beds, e, g in [(1, 1600, 6000), (2, 1600, 6000), (3, 2500, 9500), (4, 2500, 9500), (5, 3800, 14000), (7, 3800, 14000)]:
            c = energy.select_consumption({"bedrooms": beds, "specialist_setup": "none"}, ("electricity", "gas"))
            self.assertEqual((c["electricity"]["kwh"], c["gas"]["kwh"]), (e, g))

    def test_hierarchy(self):
        c = energy.select_consumption({"actual_annual_kwh_by_fuel": {"electricity": 3100},
                                       "supplier_estimated_annual_kwh_by_fuel": {"electricity": 2900, "gas": 11000},
                                       "bedrooms": 2, "specialist_setup": "none"}, ("electricity", "gas"))
        self.assertEqual((c["electricity"]["source"], c["gas"]["source"]), ("actual_12_month", "supplier_estimate"))

    def test_specialist_blocks_fallback_only(self):
        with self.assertRaises(StopError) as cm:
            energy.select_consumption({"bedrooms": 3, "specialist_setup": "ev_charging"}, ("electricity",))
        self.assertEqual(cm.exception.issue.code, "SPECIALIST_ENERGY_USAGE_REQUIRED")
        c = energy.select_consumption({"actual_annual_kwh_by_fuel": {"electricity": 5200}, "specialist_setup": "ev_charging"},
                                      ("electricity",))
        self.assertEqual(c["electricity"]["kwh"], 5200)

    def test_missing_bedrooms_and_specialist_declaration(self):
        with self.assertRaises(StopError) as cm:
            energy.select_consumption({"specialist_setup": "none"}, ("gas",))
        self.assertEqual(cm.exception.issue.code, "MINIMUM_FIELD_MISSING")
        with self.assertRaises(StopError) as cm:
            energy.select_consumption({"bedrooms": 2}, ("gas",))
        self.assertEqual(cm.exception.issue.code, "MINIMUM_FIELD_MISSING")

    def test_ni_postcode(self):
        self.assertTrue(energy.is_northern_ireland("bt7 1nn"))
        self.assertFalse(energy.is_northern_ireland("TN1 1BN"))


if __name__ == "__main__":
    unittest.main()

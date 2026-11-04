"""Brief-required end-to-end cases, gates, Review ledger and leakage checks."""

import copy
import json
import tempfile
import unittest
from decimal import Decimal as D
from pathlib import Path

from billvisor import jsonio, lint, review, workflow
from billvisor.errors import GateError

FIX = Path(__file__).parent / "fixtures"


def fixture(name):
    return jsonio.load(FIX / f"{name}.json")


class CaseTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.cd = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def put(self, case):
        rid = case["case"]["report_id"]
        (self.cd / rid).mkdir(parents=True, exist_ok=True)
        jsonio.dump(case, self.cd / rid / "case.json")
        return rid

    def load(self, rid):
        return workflow.load_case(self.cd, rid)

    def edit(self, rid, fn):
        case = self.load(rid)
        fn(case)
        workflow.save_case(self.cd, rid, case)

    def approve_and_build(self, rid, review_result="pass"):
        workflow.run_calc(self.cd, rid)
        workflow.run_approve(self.cd, rid, confirm=True)
        if workflow.review_status(self.cd, rid)["required"]:
            workflow.review_record(self.cd, rid, review_result, None)
        path = workflow.run_build(self.cd, rid)
        return jsonio.load(path)

    def page(self, data, uid):
        return next(p for p in data["service_pages"] if p["unit_id"] == uid)


class RequiredCases(CaseTest):
    def test_1_broadband_positive_saving(self):
        rid = self.put(fixture("broadband_saving"))
        data = self.approve_and_build(rid)
        p = self.page(data, "broadband")
        self.assertEqual(p["current_annual_spend_gbp"], 468)
        self.assertEqual(p["comparison_annual_gbp"], 288)
        self.assertEqual(p["comparison_text"], "Similar services cost about £288 a year.")
        self.assertEqual(p["potential_saving_gbp"], 180)
        self.assertEqual(p["score"], {"value": 39, "band": "Poor", "colour": "red", "estimated": False})
        self.assertEqual(data["overall"]["value"], 39)
        self.assertEqual(data["gate"]["type"], "review")
        self.assertIn("primary_look_at_changing_now", data["gate"]["reasons"])
        # internal values stay internal
        text = json.dumps(data)
        for leaked in ("TalkTalk", "Plusnet", "benchmark", "24.0000", "capture-1"):
            self.assertNotIn(leaked, text)

    def test_2_mobile_floor_only_after_founder_approval(self):
        case = fixture("mobile_small_saving")
        rid = self.put(case)
        outs = workflow.run_calc(self.cd, rid)
        self.assertEqual((outs["mobile"]["score"]["display"], outs["mobile"]["score"]["band"]), (70, "Medium"))
        data = self.approve_and_build(rid)
        p = self.page(data, "mobile")
        self.assertEqual((p["score"]["value"], p["score"]["band"]), (75, "Good"))
        self.assertEqual(p["potential_saving_gbp"], 36)  # saving still displayed

    def test_2b_floor_refused_without_stay_put_or_with_large_saving(self):
        case = fixture("mobile_small_saving")
        case["decision"]["units"]["mobile"]["action_type"] = "Improve the current setup"
        rid = self.put(case)
        workflow.run_calc(self.cd, rid)
        with self.assertRaisesRegex(GateError, "requires action_type 'Stay put'"):
            workflow.run_approve(self.cd, rid, confirm=True)
        self.edit(rid, lambda c: c["analysis_units"][1]["calculation_input"]["facts"].update(monthly_price_gbp=D("19.00")))
        self.edit(rid, lambda c: c["decision"]["units"]["mobile"].update(action_type="Stay put"))
        workflow.run_calc(self.cd, rid)
        with self.assertRaisesRegex(GateError, "below £50"):
            workflow.run_approve(self.cd, rid, confirm=True)

    def test_2c_without_flag_no_floor(self):
        case = fixture("mobile_small_saving")
        case["decision"]["units"]["mobile"]["small_saving_not_worth_effort"] = False
        rid = self.put(case)
        data = self.approve_and_build(rid)
        self.assertEqual(self.page(data, "mobile")["score"]["value"], 70)

    def test_3_energy_bedroom_fallback_full_score_estimate_wording(self):
        rid = self.put(fixture("household_energy_bedroom"))
        data = self.approve_and_build(rid)
        p = self.page(data, "energy_combined")
        self.assertEqual(p["coverage_status"], "Analysed")
        self.assertEqual(p["estimate_note"], "Your consumption was estimated from households with similar characteristics.")
        self.assertEqual(p["score"], {"value": 77, "band": "Good", "colour": "green", "estimated": False})
        self.assertEqual(p["current_annual_spend_gbp"], 1167)
        self.assertIsNone(p["limitation"])
        # overall: both services at weight 1.0
        bb = D(80) * D("0.9") + D(100) * (D(12) - D(5)) / D("10.5") * D("0.1")  # Sky rank 5
        en = D(20) + D(60) * D("1107.6155") / D("1167.4955")
        expected = (bb * 300 + en * D("1167.4955")) / (300 + D("1167.4955"))
        self.assertEqual(data["overall"]["value"], int(expected.quantize(D(1))))
        self.assertEqual(data["overall"]["contributing_services"], 2)

    def test_3b_payment_method_route_is_estimated_with_limitation(self):
        case = fixture("household_energy_bedroom")
        ci = case["analysis_units"][2]["calculation_input"]
        ci.pop("tariff_fit_score_observation_id")
        ci["observations"][0]["payment_method"] = "Standard credit"
        ci["facts"]["payment_method"] = "Standard credit"
        ci["observations"][1].update(tariff_type="variable", tariff_label="Standard Variable")
        ci["score_comparison_observation_id"] = "e2"
        case["decision"]["units"]["energy_combined"]["limitation_text"] = (
            "This score compares your current payment method with paying by Direct Debit.")
        case["decision"]["units"]["energy_combined"]["findings_shown"] = ["payment_method_saving"]
        rid = self.put(case)
        data = self.approve_and_build(rid)
        p = self.page(data, "energy_combined")
        self.assertEqual(p["coverage_status"], "Analysed with limitations")
        self.assertTrue(p["score"]["estimated"])
        self.assertIn("Direct Debit on the same tariff would cost an estimated £60 less a year", p["findings"][0]["text"])

    def test_3c_route_mismatch_rejected(self):
        case = fixture("household_energy_bedroom")
        case["analysis_units"][2]["calculation_input"]["observations"][1]["provider"] = "Octopus Energy"
        rid = self.put(case)
        outs = workflow.run_calc(self.cd, rid)
        self.assertTrue(outs["energy_combined"]["stopped"])
        self.assertIn("provider differs", outs["energy_combined"]["issues"][0]["message"])

    def test_4_specialist_energy_stops_and_proceeds_only_by_founder_choice(self):
        case = fixture("energy_specialist")
        rid = self.put(case)
        outs = workflow.run_calc(self.cd, rid)
        e = outs["energy_combined"]
        self.assertTrue(e["stopped"])
        self.assertIsNone(e["coverage_status"])
        self.assertEqual(e["issues"][0]["code"], "SPECIALIST_ENERGY_USAGE_REQUIRED")
        data = self.approve_and_build(rid)
        p = self.page(data, "energy_combined")
        self.assertEqual((p["coverage_status"], p["action_type"], p["score"]), ("Analysed with limitations", "Confirm information", None))
        self.assertIsNone(data["overall"])
        self.assertIn("calculator_failure_or_manual_override", data["gate"]["reasons"])

    def test_4b_stop_blocks_without_proceed_as(self):
        case = fixture("energy_specialist")
        case["decision"]["units"]["energy_combined"]["proceed_as"] = None
        rid = self.put(case)
        workflow.run_calc(self.cd, rid)
        with self.assertRaisesRegex(GateError, "calculation stopped"):
            workflow.run_approve(self.cd, rid, confirm=True)

    def test_4c_incomplete_energy_missing_minimum(self):
        case = fixture("energy_specialist")
        facts = case["analysis_units"][2]["calculation_input"]["facts"]
        del facts["payment_method"]
        rid = self.put(case)
        outs = workflow.run_calc(self.cd, rid)
        self.assertEqual(outs["energy_combined"]["issues"][0]["code"], "MINIMUM_FIELD_MISSING")
        self.assertEqual(outs["energy_combined"]["issues"][0]["field"], "facts.payment_method")

    def test_4d_northern_ireland_energy_cannot_proceed(self):
        case = fixture("energy_specialist")
        case["case"]["postcode"] = "BT7 1NN"
        rid = self.put(case)
        outs = workflow.run_calc(self.cd, rid)
        codes = [i["code"] for i in outs["energy_combined"]["issues"]]
        self.assertEqual(codes, ["REQUESTED_GEOGRAPHY_UNSUPPORTED", "REPORT_TREATMENT_POLICY_UNRESOLVED"])
        self.assertIsNone(outs["energy_combined"]["coverage_status"])
        with self.assertRaisesRegex(GateError, "only allowed for customer-information gaps"):
            workflow.run_approve(self.cd, rid, confirm=True)

    def test_5_combined_energy_appears_once(self):
        rid = self.put(fixture("household_energy_bedroom"))
        data = self.approve_and_build(rid)
        labels = [r["label"] for r in data["overview"]]
        self.assertEqual(labels, ["Broadband", "Mobile", "Energy"])
        self.assertNotIn("Gas", labels)
        self.assertNotIn("Electricity", labels)
        self.assertEqual(len(data["overall"] and [p for p in data["service_pages"] if p["label"] == "Energy"]), 1)

    def test_5b_combined_and_separate_energy_rejected(self):
        case = fixture("household_energy_bedroom")
        case["analysis_units"].append({"id": "gas", "services": ["gas"], "requested": True, "calculation_input": {}})
        rid = self.put(case)
        workflow.run_calc(self.cd, rid)
        with self.assertRaisesRegex(GateError, "use one analysis"):
            workflow.run_approve(self.cd, rid, confirm=True)

    def test_6_not_analysed_is_overview_only(self):
        rid = self.put(fixture("household_energy_bedroom"))
        data = self.approve_and_build(rid)
        mob = next(r for r in data["overview"] if r["unit_id"] == "mobile")
        self.assertEqual((mob["coverage_status"], mob["page"], mob["score"]), ("Not analysed", False, None))
        self.assertNotIn("mobile", [p["unit_id"] for p in data["service_pages"]])
        self.assertNotIn("mobile", [a["unit_id"] for a in data["priority_actions"]])

    def test_7_fingerprint_mismatch_blocks_build(self):
        rid = self.put(fixture("household_energy_bedroom"))
        workflow.run_calc(self.cd, rid)
        workflow.run_approve(self.cd, rid, confirm=True)
        workflow.review_record(self.cd, rid, "pass", None)
        base = self.load(rid)

        def reset():
            workflow.save_case(self.cd, rid, copy.deepcopy(base))

        # input changed
        self.edit(rid, lambda c: c["analysis_units"][0]["calculation_input"]["facts"].update(monthly_price_gbp=D("26.00")))
        with self.assertRaisesRegex(GateError, "Inputs changed"):
            workflow.run_build(self.cd, rid)
        # recalculated with new inputs: approval is stale
        workflow.run_calc(self.cd, rid)
        with self.assertRaisesRegex(GateError, "different inputs"):
            workflow.run_build(self.cd, rid)
        reset()
        # calculation output edited by hand
        self.edit(rid, lambda c: c["analysis_units"][0]["calculation_output"]["score"].update(display=95))
        with self.assertRaisesRegex(GateError, "does not match a fresh calculation"):
            workflow.run_build(self.cd, rid)
        reset()
        # customer wording changed after approval
        self.edit(rid, lambda c: c["decision"]["units"]["broadband"].update(next_step="Switch now."))
        with self.assertRaisesRegex(GateError, "changed after approval"):
            workflow.run_build(self.cd, rid)
        reset()
        self.assertTrue(workflow.run_build(self.cd, rid).exists())

    def test_7b_no_build_without_approval(self):
        rid = self.put(fixture("household_energy_bedroom"))
        workflow.run_calc(self.cd, rid)
        with self.assertRaisesRegex(GateError, "No founder approval"):
            workflow.run_build(self.cd, rid)

    def test_priority_actions_sorted_by_priority_then_saving(self):
        rid = self.put(fixture("household_energy_bedroom"))
        data = self.approve_and_build(rid)
        self.assertEqual([a["unit_id"] for a in data["priority_actions"]], ["energy_combined", "broadband"])

    def test_show_saving_never_zero(self):
        case = fixture("household_energy_bedroom")
        case["decision"]["units"]["broadband"]["show_saving"] = True  # price equals comparison
        rid = self.put(case)
        workflow.run_calc(self.cd, rid)
        with self.assertRaisesRegex(GateError, "never show £0"):
            workflow.run_approve(self.cd, rid, confirm=True)

    def test_unknown_provider_price_only_limited(self):
        case = fixture("broadband_saving")
        case["analysis_units"][0]["calculation_input"]["facts"]["provider"] = "Shell Energy Broadband"
        case["analysis_units"][0]["calculation_input"]["provider_table"]["provider_id"] = None
        rid = self.put(case)
        data = self.approve_and_build(rid)
        p = self.page(data, "broadband")
        self.assertEqual(p["coverage_status"], "Analysed with limitations")
        self.assertEqual(p["limitation"], "This score is based on price comparison only.")
        self.assertFalse(p["score"]["estimated"])


class ReviewLedger(unittest.TestCase):
    def build(self, rid, reviewed_result=None):
        ev = [{"type": "build", "report_id": rid}]
        if reviewed_result:
            ev.insert(0, {"type": "review", "report_id": rid, "result": reviewed_result})
        return ev

    def test_first_five_then_one_in_five(self):
        events = []
        for i in range(5):
            events += self.build(f"R{i}", "pass")
        led = {"events": events}
        self.assertEqual(review.triggers(led, "R5", {}), [])
        for i in range(5, 9):
            events += self.build(f"R{i}")
        self.assertEqual(review.triggers(led, "R9", {}), ["one_in_five_spot_check"])
        events += self.build("R9", "pass")
        self.assertEqual(review.triggers(led, "R10", {}), [])

    def test_defect_resets_clean_count(self):
        events = []
        for i in range(5):
            events += self.build(f"R{i}", "pass")
        events += self.build("R5", "major")
        led = {"events": events}
        self.assertIn("defect_reset_until_five_clean", review.triggers(led, "R6", {}))
        for i in range(6, 11):
            events += self.build(f"R{i}", "pass")
        self.assertEqual(review.triggers(led, "R11", {}), [])

    def test_flags(self):
        led = {"events": [e for i in range(5) for e in self.build(f"R{i}", "pass")]}
        self.assertEqual(review.triggers(led, "X", {"primary_look_at_changing_now": True}), ["primary_look_at_changing_now"])


class Leakage(unittest.TestCase):
    def check(self, text, providers=frozenset(), gap=False):
        return lint.check_text(text, forbidden_providers=set(providers), allow_customer_gap=gap)

    def test_banned(self):
        self.assertTrue(self.check("Compared with our benchmark"))
        self.assertTrue(self.check("A guaranteed saving"))
        self.assertTrue(self.check("the best deal available"))
        self.assertTrue(self.check("across the whole market"))
        self.assertTrue(self.check("You could save £0"))
        self.assertTrue(self.check("a saving of about £120"))
        self.assertTrue(self.check("Based on Ofcom data"))
        self.assertTrue(self.check("TalkTalk offers less", {"TalkTalk"}))
        self.assertTrue(self.check("You did not provide your usage"))

    def test_allowed(self):
        self.assertEqual(self.check("Similar services cost about £288 a year."), [])
        self.assertEqual(self.check("Check again in three months.", {"Three"}), [])
        self.assertEqual(self.check("This costs £0.50 more a day."), [])
        self.assertEqual(self.check("You did not provide your usage", gap=True), [])

    def test_leakage_blocks_approval(self):
        with tempfile.TemporaryDirectory() as tmp:
            cd = Path(tmp)
            case = fixture("broadband_saving")
            case["decision"]["units"]["broadband"]["next_step"] = "Switch to Plusnet for the best deal."
            (cd / "TEST-BB-001").mkdir()
            jsonio.dump(case, cd / "TEST-BB-001" / "case.json")
            workflow.run_calc(cd, "TEST-BB-001")
            with self.assertRaisesRegex(GateError, "Plusnet"):
                workflow.run_approve(cd, "TEST-BB-001", confirm=True)


if __name__ == "__main__":
    unittest.main()

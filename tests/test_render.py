"""Renderer acceptance checks (PHASE_1_REPORT_RENDERER_CONTRACT section 7). Synthetic fixtures only."""

import copy
import re
import tempfile
import unittest
from decimal import Decimal as D
from pathlib import Path

from billvisor import jsonio, render, workflow
from billvisor.errors import GateError

FIX = Path(__file__).parent / "fixtures"


def fixture(name):
    return jsonio.load(FIX / f"{name}.json")


def mixed_case():
    """Broadband (Poor, saving shown), mobile (Stay put, floor) and energy (Confirm information)."""
    case = fixture("broadband_saving")
    mb, en = fixture("mobile_small_saving"), fixture("energy_specialist")
    case["analysis_units"] = [case["analysis_units"][0],
                              next(u for u in mb["analysis_units"] if u["id"] == "mobile"),
                              next(u for u in en["analysis_units"] if u["id"] == "energy_combined")]
    units = case["decision"]["units"]
    units["mobile"] = dict(mb["decision"]["units"]["mobile"], priority=3)
    units["energy_combined"] = dict(en["decision"]["units"]["energy_combined"], priority=2)
    case["decision"]["report"]["summary"] = "Broadband is the clear place to start."
    case["decision"]["report"]["priority_reason"] = "Broadband has the clearest saving."
    return case


def visible_text(page_html):
    body = page_html[page_html.index("<body>"):] if "<body>" in page_html else page_html
    body = re.sub(r"<svg.*?</svg>", " ", body, flags=re.S)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body))


class RenderTest(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.cd = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def build(self, case):
        rid = case["case"]["report_id"]
        (self.cd / rid).mkdir(parents=True, exist_ok=True)
        jsonio.dump(case, self.cd / rid / "case.json")
        workflow.run_calc(self.cd, rid)
        workflow.run_approve(self.cd, rid, confirm=True)
        if workflow.review_status(self.cd, rid)["required"]:
            workflow.review_record(self.cd, rid, "Content passed", "none", None)
        out = workflow.run_build(self.cd, rid)
        html = out.with_name(out.name.replace("report_data", "report").replace(".json", ".html")).read_text()
        return jsonio.load(out), html

    def pages(self, html):
        return re.findall(r'<div class="bv-page ([^"]*)">(.*?)\n</div>', html, re.S)

    # ------------------------------------------------------------ structure

    def test_page_order_and_numbering(self):
        data, html = self.build(mixed_case())
        pages = self.pages(html)
        kinds = [cls.split()[0] for cls, _ in pages]
        self.assertEqual(kinds, ["bv-cover", "bv-overview", "bv-priorities",
                                 "bv-service", "bv-service", "bv-service", "bv-plan"])
        for n, (_, body) in enumerate(pages, start=1):
            self.assertIn(f"TEST-BB-001 · Version 1 · Page {n} of 7", body)

    def test_combined_energy_once_and_not_analysed_without_page(self):
        data, html = self.build(fixture("household_energy_bedroom"))
        pages = self.pages(html)
        titles = re.findall(r"<h1>(\w+) Analysis</h1>", html)
        self.assertEqual(titles, ["Broadband", "Energy"])  # mobile not requested: no page
        overview = next(b for c, b in pages if c.startswith("bv-overview"))
        self.assertEqual(overview.count("<tr><td>"), 3)  # Broadband, Mobile, Energy rows
        self.assertIn('<span class="position unknown">Not analysed</span>', overview)
        self.assertEqual(visible_text(html).count("Energy Analysis"), 1)

    # ------------------------------------------------------------ scores

    def test_score_values_bands_arcs_and_colours(self):
        data, html = self.build(mixed_case())
        pages = dict((c.split()[0] + str(i), (c, b)) for i, (c, b) in enumerate(self.pages(html)))
        cover_cls, cover = pages["bv-cover0"]
        ov = data["overall"]
        self.assertIn(f"band-{ov['band'].lower()}", cover_cls)
        self.assertIn(f'stroke-dasharray="{ov["value"]} 100"', cover)
        bb_cls, bb = pages["bv-service3"]
        self.assertEqual(bb_cls, "bv-service band-poor")
        self.assertIn('stroke-dasharray="39 100"', bb)
        self.assertIn('<div class="market-position">Poor</div>', bb)
        mob_cls, mob = pages["bv-service4"]
        self.assertEqual(mob_cls, "bv-service band-good stay-put")  # floor 75 after approved Stay put
        self.assertIn('stroke-dasharray="75 100"', mob)
        self.assertIn(".bv-service.band-poor .gauge .progress { stroke: var(--red); }", html)

    def test_74_is_medium_never_good(self):
        data, _ = self.build(fixture("broadband_saving"))
        data = copy.deepcopy(data)
        data["service_pages"][0]["score"] = {"value": 74, "band": "Medium", "colour": "amber"}
        data["overall"].update(value=74, band="Medium", colour="amber")
        html = render.render_report(data)
        classes = re.findall(r'<div class="bv-page ([^"]*)">', html)
        self.assertIn("bv-cover band-medium", classes)
        self.assertIn("bv-service band-medium", classes)
        self.assertFalse(any("band-good" in c for c in classes))

    def test_no_estimated_score_label_or_removed_fields(self):
        _, html = self.build(mixed_case())
        text = visible_text(html)
        self.assertIsNone(re.search(r"(Health score|/100)\s*Estimated", text))
        for gone in ("Report confidence", "Time required", "Difficulty", "High priority", "Medium priority",
                     "Fictional example", "Concept ·", "Staying put is still a useful outcome"):
            self.assertNotIn(gone, text)

    # ------------------------------------------------------------ service pages

    def test_current_service_fields_and_figure_row(self):
        data, html = self.build(mixed_case())
        bb = self.pages(html)[3][1]
        facts = re.findall(r"<dt>([^<]+)</dt><dd>([^<]+)</dd>", bb)
        self.assertEqual(facts, [("Provider", "BT"), ("Download speed", "67 Mbps"), ("Monthly cost", "£39.00"),
                                 ("Contract ends", "Out of contract")])
        figures = visible_text(bb[bb.index('class="figures"'):bb.index("score-section")])
        self.assertIn("You pay each year £468", figures)
        self.assertIn("Similar services cost about £288 a year", figures)
        self.assertIn("Potential saving £180 Estimated", figures)
        mob = self.pages(html)[4][1]
        self.assertEqual(re.findall(r"<dt>([^<]+)</dt>", mob),
                         ["Provider", "Data allowance", "Plan type", "Monthly cost", "Contract ends"])
        self.assertIn("<dd>SIM only</dd>", mob)

    def test_saving_absent_when_not_shown(self):
        case = fixture("broadband_saving")
        case["decision"]["units"]["broadband"]["show_saving"] = False
        _, html = self.build(case)
        self.assertNotIn("Potential saving", visible_text(self.pages(html)[3][1]))
        self.assertNotIn("£0", visible_text(html))

    def test_energy_monthly_payment_and_annual_cost(self):
        case = fixture("household_energy_bedroom")
        case["analysis_units"][2]["calculation_input"]["facts"]["approximate_monthly_payment_gbp"] = D("95")
        data, html = self.build(case)
        energy = self.pages(html)[4][1]
        text = visible_text(energy)
        self.assertIn("Monthly payment £95.00", text)
        self.assertIn("Estimated annual energy cost £1,167", text)
        self.assertIn(render.ENERGY_SENTENCE, text)
        self.assertIn("Your consumption was estimated from households with similar characteristics.", text)
        self.assertIn("Services Gas and electricity", text)
        self.assertIn("Tariff ends No end date known", text)
        self.assertNotIn("You pay each year", text)
        self.assertNotIn("Similar services cost", text)  # no market comparison for energy

    def test_energy_monthly_payment_omitted_when_absent(self):
        _, html = self.build(fixture("household_energy_bedroom"))
        self.assertNotIn("Monthly payment", visible_text(self.pages(html)[4][1]))

    def test_confirm_information_lists(self):
        _, html = self.build(mixed_case())
        energy = self.pages(html)[5][1]
        text = visible_text(energy)
        self.assertIn("What we could confirm ✓ Your supplier and tariff ✓ That you pay by Direct Debit", text)
        self.assertIn("What we still need", text)
        self.assertIn('<span class="missing-value">Your annual electricity and gas use</span>', energy)
        self.assertIn("We have not calculated a health score or market position.", text)
        self.assertNotIn("How it compares", text)

    # ------------------------------------------------------------ totals and actions

    def test_totals_and_action_ordering(self):
        data, html = self.build(mixed_case())
        self.assertEqual([a["unit_id"] for a in data["priority_actions"]], ["broadband", "energy_combined", "mobile"])
        pr = self.pages(html)[2][1]
        titles = re.findall(r'<strong class="action-title">([^<]+)</strong>', pr)
        self.assertEqual(titles, [a["next_step"] for a in data["priority_actions"]])
        self.assertEqual(pr.count("No action needed"), 1)  # the Stay put card only
        cover = visible_text(self.pages(html)[0][1])
        t = data["totals"]
        self.assertEqual(t, {"annual_spend_gbp": 648, "potential_savings_gbp": 216,
                             "services_reviewed": 3, "priority_actions": 2})
        self.assertIn("3 services reviewed £648 annual spend £216 potential savings 2 priority actions", cover)
        overview = visible_text(self.pages(html)[1][1])
        self.assertIn("Total Annual spend £648 Potential savings £216", overview)
        plan = self.pages(html)[6][1]
        self.assertIn("If you only do one thing", plan)
        self.assertIn(data["priority_actions"][0]["next_step"], plan)

    def test_source_line_once_on_final_page(self):
        _, html = self.build(mixed_case())
        self.assertEqual(visible_text(html).count("Supporting source details are available on request."), 1)
        self.assertIn("Supporting source details are available on request.", self.pages(html)[-1][1])

    def test_no_internal_or_workspace_content(self):
        data, html = self.build(mixed_case())
        text = visible_text(html)
        for leaked in ("benchmark", "capture-1", "TalkTalk", "Plusnet", "Look at changing now",
                       "sha256:", "inputs_fp", "Documents/Business Planning", "../"):
            self.assertNotIn(leaked, html if leaked in ("Documents/Business Planning", "../", "sha256:") else text)
        self.assertNotIn('src="billvisor', html)  # assets are embedded, so the file is self-contained
        self.assertEqual(len(re.findall(r'src="data:image/', html)), 1 + 2 * 7)  # house + logo/watermark per page

    # ------------------------------------------------------------ gates

    def test_render_reads_report_data_only(self):
        data, html = self.build(fixture("broadband_saving"))
        self.assertEqual(render.render_report(data), html)  # same output from the saved report data alone

    def test_stale_approval_produces_no_html(self):
        case = fixture("broadband_saving")
        rid = case["case"]["report_id"]
        (self.cd / rid).mkdir(parents=True)
        jsonio.dump(case, self.cd / rid / "case.json")
        workflow.run_calc(self.cd, rid)
        workflow.run_approve(self.cd, rid, confirm=True)
        workflow.review_record(self.cd, rid, "Content passed", "none", None)
        c = workflow.load_case(self.cd, rid)
        c["decision"]["units"]["broadband"]["headline"] = "Changed after approval"
        workflow.save_case(self.cd, rid, c)
        with self.assertRaises(GateError):
            workflow.run_build(self.cd, rid)
        self.assertEqual(list((self.cd / rid).glob("report*.v*")), [])

    def test_unknown_code_refused(self):
        data, _ = self.build(fixture("broadband_saving"))
        data["service_pages"][0]["current_service"]["contract_end"] = "rolling"
        with self.assertRaisesRegex(render.RenderError, "no display rule"):
            render.render_report(data)

    def test_customer_text_is_escaped(self):
        data, _ = self.build(fixture("broadband_saving"))
        data["service_pages"][0]["explanation"] = "<script>alert(1)</script>"
        html = render.render_report(data)
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)


if __name__ == "__main__":
    unittest.main()

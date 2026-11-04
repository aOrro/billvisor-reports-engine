"""Required test 8: anonymised regression cases reproduce their expected customer-facing values.

Each folder in tests/regression/<neutral-name>/ holds:
  case.json      engine-format case, wholly synthetic (no real names, postcodes or captures)
  expected.json  values worked out by hand from the governing methods, NOT captured from the engine:
                 {"overall": {...}, "pages": [unit ids in page order], "action_order": [unit ids],
                  "totals": {...}, "service_pages": {"<unit_id>": {"<field>": value, ...}}}
  NOTES.md       the hand arithmetic behind expected.json
Each folder present is checked automatically; a change to scores, statuses, pages, action order or
customer-visible figures fails here.
"""

import tempfile
import unittest
from pathlib import Path

from billvisor import jsonio, workflow

ROOT = Path(__file__).parent / "regression"


class ExistingApprovedCases(unittest.TestCase):
    def test_regression_cases(self):
        cases = sorted(p for p in ROOT.glob("*/case.json")) if ROOT.exists() else []
        if not cases:
            self.skipTest("no regression cases in tests/regression/")
        for case_file in cases:
            with self.subTest(case=case_file.parent.name), tempfile.TemporaryDirectory() as tmp:
                case = jsonio.load(case_file)
                expected = jsonio.load(case_file.parent / "expected.json")
                rid = case["case"]["report_id"]
                (Path(tmp) / rid).mkdir()
                jsonio.dump(case, Path(tmp) / rid / "case.json")
                workflow.run_calc(Path(tmp), rid)
                workflow.run_approve(Path(tmp), rid, confirm=True)
                if workflow.review_status(Path(tmp), rid)["required"]:
                    workflow.review_record(Path(tmp), rid, "Content passed", "none", "regression")
                data = jsonio.load(workflow.run_build(Path(tmp), rid))
                if "overall" in expected:
                    self.assertEqual(data["overall"], expected["overall"])
                if "pages" in expected:
                    self.assertEqual([p["unit_id"] for p in data["service_pages"]], expected["pages"])
                if "action_order" in expected:
                    self.assertEqual([a["unit_id"] for a in data["priority_actions"]], expected["action_order"])
                if "totals" in expected:
                    self.assertEqual(data["totals"], expected["totals"])
                pages = {p["unit_id"]: p for p in data["service_pages"]}
                for uid, fields in expected.get("service_pages", {}).items():
                    for k, v in fields.items():
                        self.assertEqual(pages[uid][k], v, f"{uid}.{k}")


if __name__ == "__main__":
    unittest.main()

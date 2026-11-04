"""Required test 8: existing approved cases reproduce their approved outputs.

The approved case inputs and outputs were not available when this engine was
built. Place them in tests/regression/<name>/ as:
  case.json            engine-format case (anonymised synthetic copy)
  expected.json        approved customer-facing values:
                       {"overall": {...}, "service_pages": {"<unit_id>": {"score": .., "coverage_status": ..,
                        "current_annual_spend_gbp": .., "comparison_annual_gbp": .., "potential_saving_gbp": ..}}}
Each directory present is then checked automatically.
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
            self.skipTest("Existing approved case inputs/outputs not supplied yet (tests/regression/)")
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
                    workflow.review_record(Path(tmp), rid, "pass", "regression")
                data = jsonio.load(workflow.run_build(Path(tmp), rid))
                if "overall" in expected:
                    self.assertEqual(data["overall"], expected["overall"])
                pages = {p["unit_id"]: p for p in data["service_pages"]}
                for uid, fields in expected.get("service_pages", {}).items():
                    for k, v in fields.items():
                        self.assertEqual(pages[uid][k], v, f"{uid}.{k}")


if __name__ == "__main__":
    unittest.main()

"""Command-line flow: new -> validate -> calc -> pack -> approve -> review -> build."""

from __future__ import annotations

import argparse
import sys

from . import jsonio, workflow
from .errors import GateError


def _validate(cases_dir, rid) -> int:
    from .calc import calculate_case

    case = workflow.load_case(cases_dir, rid)
    outputs = calculate_case(case)
    blocking = 0
    for uid, out in outputs.items():
        print(f"{uid}: {out['coverage_status'] or 'STOPPED'}")
        for i in out["issues"]:
            blocking += i["blocking"]
            print(f"  {'STOP' if i['blocking'] else 'note'} {i['code']}: {i['message']}\n    next: {i['next_action']}")
    return 1 if blocking else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="billvisor", description="Billvisor Phase 1 report engine")
    ap.add_argument("--cases-dir", help="founder-only case folder (or BILLVISOR_CASES_DIR)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("new", "validate", "calc", "pack", "review-status", "build"):
        sub.add_parser(name).add_argument("report_id")
    a = sub.add_parser("approve")
    a.add_argument("report_id")
    a.add_argument("--yes", action="store_true", help="record the founder approval (without it, preview only)")
    r = sub.add_parser("review-record")
    r.add_argument("report_id")
    r.add_argument("--result", required=True, choices=["pass", "minor", "major", "critical"])
    r.add_argument("--note")
    args = ap.parse_args(argv)

    try:
        cd = workflow.cases_dir_from(args.cases_dir)
        rid = args.report_id
        if args.cmd == "new":
            print(f"created {workflow.new_case(cd, rid)}\nset requested true/false for each service and enter the facts.")
        elif args.cmd == "validate":
            return _validate(cd, rid)
        elif args.cmd == "calc":
            outs = workflow.run_calc(cd, rid)
            for uid, o in outs.items():
                sc = o.get("score")
                print(f"{uid}: {o['coverage_status'] or 'STOPPED'}" + (f" score {sc['display']} {sc['band']}" if sc else ""))
            print("trace written to trace.txt. next: pack")
        elif args.cmd == "pack":
            print(f"approval pack: {workflow.run_pack(cd, rid)}")
        elif args.cmd == "approve":
            res = workflow.run_approve(cd, rid, args.yes)
            print(jsonio.dumps(res["result"]["body"]))
            print("APPROVAL RECORDED" if res["recorded"] else "Preview only. Re-run with --yes to record the founder approval.")
        elif args.cmd == "review-status":
            print(jsonio.dumps(workflow.review_status(cd, rid)))
        elif args.cmd == "review-record":
            print(jsonio.dumps(workflow.review_record(cd, rid, args.result, args.note)))
        elif args.cmd == "build":
            print(f"report data: {workflow.run_build(cd, rid)}")
    except GateError as e:
        print(f"BLOCKED: {e}", file=sys.stderr)
        return 2
    return 0

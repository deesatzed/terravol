"""Only scaffold doctor/validation commands exist at this stage."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from volterra.scaffold import audit


def main() -> int:
    parser = argparse.ArgumentParser(description="VOLTERRA scaffold controls; application workflows are not implemented")
    commands = parser.add_subparsers(dest="command", required=True)
    doctor = commands.add_parser("doctor", help="Report scaffold validity and actual application status")
    doctor.add_argument("--profile", choices=["offline"], default="offline")
    doctor.add_argument("--root", type=Path, default=Path.cwd())
    workbench = commands.add_parser("workbench", help="Inspect computed local workbench state")
    workbench_actions = workbench.add_subparsers(dest="workbench_action", required=True)
    workbench_actions.add_parser("inspect", help="Return explicit local workbench availability")
    scaffold = commands.add_parser("scaffold", help="Inspect project-control artifacts")
    actions = scaffold.add_subparsers(dest="action", required=True)
    validate = actions.add_parser("validate", help="Validate scaffold controls, not forecasting")
    validate.add_argument("--root", type=Path, default=Path.cwd())
    arguments = parser.parse_args()
    if arguments.command == "workbench":
        print(json.dumps({"status":"UNAVAILABLE","reason":"No persisted workbench session supplied","mode":"LOCAL_ONLY"}, indent=2))
        return 0
    report = audit(arguments.root)
    passed = report["status"] == "PASSED"
    if arguments.command == "doctor" and passed:
        report["status"] = "SCAFFOLD_VALID_APPLICATION_" + report["application_status"]
    print(json.dumps(report, indent=2, allow_nan=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())

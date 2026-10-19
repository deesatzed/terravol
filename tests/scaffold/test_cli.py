"""Scaffold-control tests; these are not application acceptance tests."""
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]


class ScaffoldCommandTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="volterra-scaffold-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "config", self.root / "config")
        for name in json.loads((ROOT / "config/project.json").read_text())["required_documents"]:
            source = ROOT / name
            if source.is_file():
                target = self.root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source, target)
        shutil.copy2(ROOT / ".gitignore", self.root / ".gitignore")
        shutil.copytree(ROOT / "docs/archive/spec-v1", self.root / "docs/archive/spec-v1")
        shutil.copytree(ROOT / "tests/application", self.root / "tests/application")
        shutil.copytree(ROOT / "reports", self.root / "reports")

    def run_cli(self, *args: str) -> subprocess.CompletedProcess[str]:
        environment = dict(os.environ, PYTHONPATH=str(ROOT / "src"), PYTHONDONTWRITEBYTECODE="1")
        return subprocess.run(
            [sys.executable, "-B", "-m", "volterra", *args, "--root", str(self.root)],
            capture_output=True, text=True, env=environment, timeout=15,
        )

    def update(self, name: str, change) -> None:
        path = self.root / "config" / name
        value = json.loads(path.read_text())
        change(value)
        path.write_text(json.dumps(value))

    def assert_invalid(self, code: str) -> None:
        result = self.run_cli("scaffold", "validate")
        self.assertEqual(result.returncode, 2, result.stderr + result.stdout)
        report = json.loads(result.stdout)
        self.assertIn(code, {item["code"] for item in report["errors"]})

    def test_doctor_distinguishes_valid_scaffold_from_unimplemented_application(self) -> None:
        result = self.run_cli("doctor", "--profile", "offline")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        report = json.loads(result.stdout)
        self.assertEqual(report["status"], "SCAFFOLD_VALID_APPLICATION_NOT_IMPLEMENTED")
        self.assertEqual(report["application_status"], "NOT_IMPLEMENTED")
        self.assertEqual(report["application_acceptance_total"], 120)
        self.assertEqual(report["application_acceptance_executed"], 120)
        self.assertIsNone(report["next_ticket"])

    def test_dependency_cycle_is_rejected(self) -> None:
        self.update("implementation_queue.json", lambda value: value["tickets"][0].update(dependencies=["VT05"]))
        self.assert_invalid("DEPENDENCY_CYCLE")

    def test_unknown_requirement_owner_is_rejected(self) -> None:
        self.update("acceptance_matrix.json", lambda value: value["requirements"][0].update(ticket="VT99"))
        self.assert_invalid("UNKNOWN_ACCEPTANCE_OWNER")

    def test_nonstring_requirement_owner_returns_diagnostics(self) -> None:
        self.update("acceptance_matrix.json", lambda value: value["requirements"][0].update(ticket=[]))
        self.assert_invalid("INVALID_CONTROL")

    def test_paid_or_networked_offline_defaults_are_rejected(self) -> None:
        self.update("offline.json", lambda value: value["execution"].update(allow_network=True, max_external_usd=1))
        self.assert_invalid("UNSAFE_OFFLINE_DEFAULTS")

    def test_unexecuted_requirement_cannot_receive_a_pass(self) -> None:
        self.update(
            "acceptance_matrix.json",
            lambda value: value["requirements"][0].update(status="PASSED", last_run=None, evidence_refs=[], test_refs=[]),
        )
        self.assert_invalid("UNSUPPORTED_ACCEPTANCE_CLAIM")

    def test_unverified_model_cannot_be_enabled(self) -> None:
        self.update("model_registry.json", lambda value: value["models"][4].update(enabled=True))
        self.assert_invalid("UNVERIFIED_MODEL_ENABLED")

    def test_malformed_control_shapes_return_diagnostics(self) -> None:
        self.update("offline.json", lambda value: value.update(execution=None))
        self.assert_invalid("INVALID_CONTROL")

    def test_nonstring_requirement_identity_is_rejected_without_crashing(self) -> None:
        self.update("acceptance_matrix.json", lambda value: value["requirements"][0].update(id={"bad": "identity"}))
        self.assert_invalid("INVALID_CONTROL")

    def test_committed_roster_must_exist_in_registry(self) -> None:
        self.update("model_registry.json", lambda value: value.update(models=[m for m in value["models"] if m["candidate_id"] != "ttm"]))
        self.assert_invalid("MODEL_ROSTER_MISMATCH")

    def test_goal_and_queue_dependency_drift_is_rejected(self) -> None:
        self.update("implementation_queue.json", lambda value: value["tickets"][6].update(dependencies=[]))
        self.assert_invalid("QUEUE_GOAL_MISMATCH")

    def test_application_cannot_be_declared_ready_without_implementation_evidence(self) -> None:
        self.update("project.json", lambda value: value.update(application_status="READY"))
        self.assert_invalid("UNSUPPORTED_APPLICATION_CLAIM")

    def test_scaffold_receipt_cannot_complete_application_ticket(self) -> None:
        path = self.root / "reports/scaffold-only.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps({"scope": "scaffold_controls_only", "status": "PASSED"}))
        self.update("implementation_queue.json", lambda value: value["tickets"][0].update(status="COMPLETE", evidence_refs=["reports/scaffold-only.json"]))
        self.assert_invalid("UNSUPPORTED_COMPLETION_CLAIM")

    def test_nested_status_types_return_diagnostics(self) -> None:
        cases = [
            ("acceptance_matrix.json", lambda value: value["requirements"][0].update(status=[])),
            ("project.json", lambda value: value.update(application_status={})),
        ]
        for name, change in cases:
            with self.subTest(name=name):
                path = self.root / "config" / name
                original = path.read_text()
                try:
                    self.update(name, change)
                    self.assert_invalid("INVALID_CONTROL")
                finally:
                    path.write_text(original)

    def test_invalid_document_path_is_reported(self) -> None:
        self.update("project.json", lambda value: value.update(required_documents=["bad\x00name"]))
        self.assert_invalid("INVALID_CONTROL")

    def test_invalid_goal_encoding_is_reported(self) -> None:
        (self.root / "GOAL_UPD.md").write_bytes(b"\xff")
        self.assert_invalid("GOAL_AUTHORITY")

    def test_unrelated_receipt_and_missing_test_cannot_pass_requirement(self) -> None:
        path = self.root / "reports/unrelated.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps({"scope": "application_acceptance", "status": "PASSED",
                                    "requirement_ids": ["AC-NOT-99"], "test_refs": ["tests/missing.py"],
                                    "tests_run": 1, "executed_at": "2026-10-18T12:00:00Z"}))
        self.update("acceptance_matrix.json", lambda value: value["requirements"][0].update(
            status="PASSED", test_refs=["tests/missing.py"],
            last_run={"executed_at": "2026-10-18T12:00:00Z", "command": "never ran", "exit_code": 0},
            evidence_refs=["reports/unrelated.json"]))
        self.assert_invalid("UNSUPPORTED_ACCEPTANCE_CLAIM")

    def install_receipt_fixture(self, result: str = "PASSED", malformed_tests: bool = False) -> None:
        """A temporary metadata fixture, not an executed application test."""
        test_path = self.root / "tests/application/test_fixture.py"
        test_path.parent.mkdir(parents=True, exist_ok=True)
        test_path.write_text("# Metadata-fixture target; never run as application acceptance.\n")
        reference = "tests/application/test_fixture.py::fixture_reference"
        matrix = json.loads((self.root / "config/acceptance_matrix.json").read_text())
        requirement = matrix["requirements"][0]["id"]
        self.update("acceptance_matrix.json", lambda value: value["requirements"][0].update(
            status="NOT_IMPLEMENTED", last_run=None, evidence_refs=[], test_refs=[]
        ))
        run = {"run_id": "metadata-fixture", "executed_at": "2026-10-18T12:00:00Z",
               "command": "metadata-fixture-only", "exit_code": 0 if result == "PASSED" else 1}
        receipt = {"scope": "application_acceptance", "status": result, "requirement_ids": [requirement],
                   "tests_run": 1, "test_refs": [{"bad": "reference"}] if malformed_tests else [reference], **run}
        path = self.root / "reports/bound-fixture.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps(receipt))
        self.update(
            "acceptance_matrix.json",
            lambda value: next(item for item in value["requirements"] if item["id"] == requirement).update(
                status=result, test_refs=[reference], last_run=run, evidence_refs=["reports/bound-fixture.json"]
            ),
        )

    def test_bound_pass_and_failure_receipts_have_consistent_execution_counts(self) -> None:
        for result in ("PASSED", "FAILED"):
            with self.subTest(result=result):
                matrix_path = self.root / "config/acceptance_matrix.json"
                original = matrix_path.read_text()
                try:
                    self.install_receipt_fixture(result)
                    command = self.run_cli("scaffold", "validate")
                    self.assertEqual(command.returncode, 0, command.stderr + command.stdout)
                    report = json.loads(command.stdout)
                    self.assertEqual(report["application_acceptance_executed"], 120)
                    self.assertEqual(report["application_status"], "NOT_IMPLEMENTED")
                finally:
                    matrix_path.write_text(original)

    def test_malformed_receipt_test_reference_is_rejected_without_crashing(self) -> None:
        self.install_receipt_fixture(malformed_tests=True)
        self.assert_invalid("UNSUPPORTED_ACCEPTANCE_CLAIM")

    def test_ticket_completion_requires_completed_dependencies(self) -> None:
        path = self.root / "reports/ticket.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps({"scope": "ticket_verification", "status": "PASSED",
                                    "ticket_ids": ["VT23"], "tests_run": 1,
                                    "executed_at": "2026-10-18T12:00:00Z"}))
        self.update("implementation_queue.json", lambda value: (
            value["tickets"][21].update(status="NOT_IMPLEMENTED"),
            value["tickets"][23].update(status="COMPLETE", evidence_refs=["reports/ticket.json"])
        ))
        self.assert_invalid("COMPLETION_DEPENDENCY")

    def test_ticket_status_is_a_defined_enum(self) -> None:
        self.update("implementation_queue.json", lambda value: value["tickets"][0].update(status="PASSED"))
        self.assert_invalid("INVALID_CONTROL")

    def test_ticket_receipt_requires_a_successful_referenced_run(self) -> None:
        path = self.root / "reports/contradictory-ticket.json"
        path.parent.mkdir(exist_ok=True)
        path.write_text(json.dumps({"scope": "ticket_verification", "status": "PASSED",
                                    "ticket_ids": ["VT00"], "tests_run": 1, "run_id": "contradiction",
                                    "executed_at": "2026-10-18T12:00:00Z", "exit_code": 1}))
        self.update("implementation_queue.json", lambda value: value["tickets"][0].update(
            status="COMPLETE", evidence_refs=["reports/contradictory-ticket.json"]))
        self.assert_invalid("UNSUPPORTED_COMPLETION_CLAIM")

    def test_execution_counts_require_consistent_run_metadata(self) -> None:
        for update in ({"status": "FAILED", "last_run": None},
                       {"status": "NOT_IMPLEMENTED", "last_run": "never"}):
            with self.subTest(update=update):
                self.update("acceptance_matrix.json", lambda value: value["requirements"][0].update(update))
                self.assert_invalid("UNSUPPORTED_ACCEPTANCE_CLAIM")

    def test_all_offline_spending_and_monitoring_defaults_remain_disabled(self) -> None:
        cases = [
            ("model_registry.json", lambda value: value.update(default_allow_paid_calls=True)),
            ("source_registry.json", lambda value: value.update(paid_subscription_allowance_usd=100)),
            ("offline.json", lambda value: value["monitoring"].update(enabled=True)),
            ("offline.json", lambda value: value["learning"].update(label_source="simulated_consensus")),
        ]
        for name, change in cases:
            with self.subTest(name=name):
                path = self.root / "config" / name
                original = path.read_text()
                try:
                    self.update(name, change)
                    self.assert_invalid("UNSAFE_OFFLINE_DEFAULTS")
                finally:
                    path.write_text(original)

    def test_missing_canonical_requirement_is_rejected(self) -> None:
        self.update("acceptance_matrix.json", lambda value: value["requirements"].pop())
        self.assert_invalid("ACCEPTANCE_MISMATCH")

    def test_unknown_dependency_is_rejected(self) -> None:
        self.update("implementation_queue.json", lambda value: value["tickets"][1].update(dependencies=["VT99"]))
        self.assert_invalid("UNKNOWN_DEPENDENCY")

    def test_numeric_overflow_in_controls_is_rejected(self) -> None:
        path = self.root / "config/offline.json"
        content = path.read_text().replace('"max_external_usd": 0', '"max_external_usd": 1e999')
        self.assertNotEqual(content, path.read_text())
        path.write_text(content)
        self.assert_invalid("INVALID_CONTROL")

    def test_changed_v1_archive_is_rejected(self) -> None:
        (self.root / "docs/archive/spec-v1/GOAL.md").write_text("changed")
        self.assert_invalid("ARCHIVE_INTEGRITY")

    def test_commands_are_read_only(self) -> None:
        def fingerprint() -> dict[str, str]:
            return {str(path.relative_to(self.root)): hashlib.sha256(path.read_bytes()).hexdigest()
                    for path in self.root.rglob("*") if path.is_file()}
        before = fingerprint()
        result = self.run_cli("scaffold", "validate")
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        self.assertEqual(before, fingerprint())

    def test_forecasting_command_is_explicitly_unavailable(self) -> None:
        result = self.run_cli("forecast", "inspect", "fictional")
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid choice", result.stderr)


if __name__ == "__main__":
    unittest.main()

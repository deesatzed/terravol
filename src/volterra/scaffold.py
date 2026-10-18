"""Read-only project-control validation, not forecasting application validation."""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
import re
from typing import Any


def read_json(path: Path) -> dict[str, Any]:
    def reject(value: str) -> None:
        raise ValueError(f"Nonfinite JSON constant: {value}")

    def finite(value: Any) -> None:
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("Nonfinite numeric value, including exponent overflow")
        if isinstance(value, dict):
            for child in value.values():
                finite(child)
        elif isinstance(value, list):
            for child in value:
                finite(child)

    value = json.loads(path.read_text(encoding="utf-8"), parse_constant=reject)
    finite(value)
    if not isinstance(value, dict):
        raise ValueError("Control file must be an object")
    return value


def audit(root: Path) -> dict[str, Any]:
    """Check explicit control files without scanning donor/data or mutating files."""
    root = root.resolve()
    errors: list[dict[str, str]] = []

    def error(code: str, message: str) -> None:
        errors.append({"code": code, "message": message})

    def load(name: str) -> dict[str, Any]:
        try:
            return read_json(root / "config" / name)
        except (OSError, ValueError, RecursionError) as exc:
            error("INVALID_CONTROL", f"{name}: {exc}")
            return {}

    project = load("project.json")
    queue = load("implementation_queue.json")
    matrix = load("acceptance_matrix.json")
    offline = load("offline.json")
    registry = load("model_registry.json")
    sources = load("source_registry.json")

    def object_field(parent: dict[str, Any], key: str) -> dict[str, Any]:
        value = parent.get(key, {})
        if not isinstance(value, dict):
            error("INVALID_CONTROL", f"{key} must be an object")
            return {}
        return value

    def object_rows(parent: dict[str, Any], key: str) -> list[dict[str, Any]]:
        value = parent.get(key, [])
        if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
            error("INVALID_CONTROL", f"{key} must be an array of objects")
            return []
        return value

    try:
        goal = (root / "GOAL_UPD.md").read_text(encoding="utf-8")
        pointer = (root / "GOAL.md").read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        goal, pointer = "", ""
        error("GOAL_AUTHORITY", str(exc))
    if project.get("canonical_goal") != "GOAL_UPD.md" or queue.get("canonical_goal") != "GOAL_UPD.md" or "GOAL_UPD.md" not in pointer:
        error("GOAL_AUTHORITY", "Active project, queue and GOAL pointer must agree")

    documents = project.get("required_documents", [])
    if not isinstance(documents, list) or not all(isinstance(name, str) for name in documents):
        error("INVALID_CONTROL", "required_documents must be an array of paths")
        documents = []
    for name in documents:
        try:
            target = (root / name).resolve()
            if not target.is_relative_to(root) or not target.is_file():
                error("MISSING_DOCUMENT", str(name))
        except (OSError, ValueError, RuntimeError) as exc:
            error("INVALID_CONTROL", f"Invalid document path: {exc}")

    tickets = object_rows(queue, "tickets")
    requirements = object_rows(matrix, "requirements")
    if any(not isinstance(item.get("id"), str) for item in tickets + requirements):
        error("INVALID_CONTROL", "Record identities must be strings")
        tickets = [item for item in tickets if isinstance(item.get("id"), str)]
        requirements = [item for item in requirements if isinstance(item.get("id"), str)]
    ticket_ids = [item.get("id") for item in tickets]
    requirement_ids = [item.get("id") for item in requirements]
    if len(set(ticket_ids)) != len(ticket_ids) or not all(isinstance(item, str) for item in ticket_ids):
        error("DUPLICATE_TICKET", "Ticket identities must be unique strings")
    if len(set(requirement_ids)) != len(requirement_ids) or not all(isinstance(item, str) for item in requirement_ids):
        error("ACCEPTANCE_MISMATCH", "Acceptance identities must be unique strings")
    goal_ids = re.findall(r"^\| (AC-[A-Z]+-\d{2}) \|", goal, re.MULTILINE)
    if (len(goal_ids) != len(set(goal_ids)) or set(goal_ids) != set(requirement_ids)
            or len(requirements) != project.get("application_acceptance_count")):
        error("ACCEPTANCE_MISMATCH", "Goal and machine acceptance IDs/count differ")
    goal_dependencies = {
        identifier: re.findall(r"VT\d{2}", dependencies)
        for identifier, dependencies in re.findall(r"^\| (VT\d{2}) \| ([^|]+) \|", goal, re.MULTILINE)
    }
    actual_dependencies = {item["id"]: item.get("dependencies") for item in tickets}
    if goal_dependencies != actual_dependencies or queue.get("first_scored_slice_through") != "VT05":
        error("QUEUE_GOAL_MISMATCH", "Goal and machine ticket dependencies/first scored slice differ")

    def valid_time(value: Any) -> bool:
        if not isinstance(value, str):
            return False
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00")).tzinfo is not None
        except ValueError:
            return False

    def valid_run(value: Any) -> bool:
        return (isinstance(value, dict) and isinstance(value.get("run_id"), str) and bool(value["run_id"])
                and valid_time(value.get("executed_at")) and bool(value.get("command"))
                and isinstance(value.get("command"), (str, list))
                and type(value.get("exit_code")) is int)

    def real_test_refs(refs: Any) -> bool:
        if not isinstance(refs, list) or not refs:
            return False
        for ref in refs:
            if not isinstance(ref, str):
                return False
            try:
                target = (root / ref.split("::", 1)[0]).resolve()
                if (not target.is_relative_to(root / "tests") or target.is_relative_to(root / "tests/scaffold")
                        or not target.is_file()):
                    return False
            except (OSError, ValueError, RuntimeError):
                return False
        return True

    def has_receipt(refs: Any, identifier: str, scope: str, result: str = "PASSED",
                    run: dict[str, Any] | None = None, tests: list[str] | None = None) -> bool:
        if not isinstance(refs, list) or not refs:
            return False
        for ref in refs:
            if not isinstance(ref, str):
                return False
            try:
                target = (root / ref).resolve()
                if not target.is_relative_to(root / "reports") or target.suffix != ".json":
                    return False
                receipt = read_json(target)
            except (OSError, ValueError, RuntimeError):
                return False
            identities = receipt.get("requirement_ids" if scope == "application_acceptance" else "ticket_ids")
            if (receipt.get("scope") != scope or receipt.get("status") != result
                    or not isinstance(identities, list) or identifier not in identities
                    or type(receipt.get("tests_run")) is not int or receipt["tests_run"] <= 0
                    or not valid_run(receipt) or not real_test_refs(receipt.get("test_refs"))
                    or ((receipt["exit_code"] == 0) != (result == "PASSED"))):
                return False
            if run is not None and any(receipt.get(key) != run.get(key)
                                       for key in ("run_id", "executed_at", "command", "exit_code")):
                return False
            if tests is not None and (not isinstance(receipt.get("test_refs"), list)
                                      or not all(isinstance(ref, str) for ref in receipt["test_refs"])
                                      or not set(tests).issubset(receipt["test_refs"])):
                return False
        return True

    allowed_results = {"NOT_IMPLEMENTED", "NOT_RUN", "PASSED", "FAILED", "BLOCKED"}
    executed_ids: list[str] = []
    for item in requirements:
        if not isinstance(item.get("ticket"), str):
            error("INVALID_CONTROL", f"{item['id']}: requirement owner must be a string")
        elif item.get("ticket") not in ticket_ids:
            error("UNKNOWN_ACCEPTANCE_OWNER", str(item.get("id")))
        status = item.get("status")
        if not isinstance(status, str):
            error("INVALID_CONTROL", f"{item['id']}: result status must be a string")
            continue
        if status not in allowed_results:
            error("UNSUPPORTED_ACCEPTANCE_CLAIM", item["id"])
        if status in {"PASSED", "FAILED"}:
            run = item.get("last_run")
            if (valid_run(run) and ((run["exit_code"] == 0) == (status == "PASSED"))
                    and real_test_refs(item.get("test_refs"))
                    and has_receipt(item.get("evidence_refs"), item["id"], "application_acceptance", status,
                                    run, item["test_refs"])):
                executed_ids.append(item["id"])
            else:
                error("UNSUPPORTED_ACCEPTANCE_CLAIM", f"{item['id']}: executed status needs matching run, tests and identifier-bound receipt")
        elif item.get("last_run") is not None:
            error("UNSUPPORTED_ACCEPTANCE_CLAIM", f"{item['id']}: unexecuted status cannot carry a run")
    application_status = project.get("application_status", "UNKNOWN")
    if not isinstance(application_status, str):
        error("INVALID_CONTROL", "application_status must be a string")
    elif application_status not in {"NOT_IMPLEMENTED", "PARTIAL", "IMPLEMENTED"}:
        error("UNSUPPORTED_APPLICATION_CLAIM", "Application readiness requires a defined status and applicable execution evidence")

    graph: dict[str, list[str]] = {}
    states = {item["id"]: item.get("status") for item in tickets}
    optional_ids = {item["id"] for item in tickets if item.get("optional") is True}
    for item in tickets:
        status = item.get("status")
        if not isinstance(status, str) or status not in {"NOT_IMPLEMENTED", "PARTIAL", "BLOCKED", "COMPLETE"}:
            error("INVALID_CONTROL", f"{item['id']}: unknown ticket status")
        if type(item.get("optional")) is not bool or item["optional"] != (item["id"] == "VT22"):
            error("QUEUE_GOAL_MISMATCH", f"{item['id']}: only VT22 is an optional ticket")
        dependencies = item.get("dependencies", [])
        if not isinstance(dependencies, list) or not all(isinstance(dep, str) for dep in dependencies):
            error("INVALID_CONTROL", f"{item.get('id')}: invalid dependencies")
            dependencies = []
        for dep in dependencies:
            if dep not in ticket_ids:
                error("UNKNOWN_DEPENDENCY", f"{item.get('id')} -> {dep}")
        graph[item.get("id", "")] = [dep for dep in dependencies if dep in ticket_ids]
        if status == "COMPLETE":
            if any(states[dep] != "COMPLETE" for dep in graph[item["id"]]):
                error("COMPLETION_DEPENDENCY", f"{item['id']}: dependencies are not complete")
            if not has_receipt(item.get("evidence_refs"), item["id"], "ticket_verification"):
                error("UNSUPPORTED_COMPLETION_CLAIM", item["id"])
    mandatory_requirements = [item for item in requirements
                              if not isinstance(item.get("ticket"), str) or item["ticket"] not in optional_ids]
    if application_status == "IMPLEMENTED" and (
        not all(item.get("status") == "PASSED" and item["id"] in executed_ids for item in mandatory_requirements)
        or any(states[item["id"]] != "COMPLETE" for item in tickets if item["id"] not in optional_ids)
    ):
        error("UNSUPPORTED_APPLICATION_CLAIM", "Mandatory tickets and requirement execution must support implementation status")
    visiting: set[str] = set()
    done: set[str] = set()
    order: list[str] = []

    def visit(identifier: str) -> None:
        if identifier in visiting:
            raise ValueError(f"Dependency cycle at {identifier}")
        if identifier in done:
            return
        visiting.add(identifier)
        for dependency in graph[identifier]:
            visit(dependency)
        visiting.remove(identifier)
        done.add(identifier)
        order.append(identifier)

    try:
        for identifier in graph:
            visit(identifier)
    except ValueError as exc:
        error("DEPENDENCY_CYCLE", str(exc))

    execution = object_field(offline, "execution")
    options = object_field(offline, "options")
    model_policy = object_field(offline, "models")
    monitoring = object_field(offline, "monitoring")
    learning = object_field(offline, "learning")
    if (execution.get("allow_network") is not False or execution.get("allow_model_downloads") is not False
            or type(execution.get("max_external_usd")) not in {int, float}
            or execution.get("max_external_usd") != 0
            or options.get("execution_enabled") is not False):
        error("UNSAFE_OFFLINE_DEFAULTS", "Offline network/downloads/spend and financial execution must be disabled")
    if (registry.get("default_allow_paid_calls") is not False
            or type(sources.get("paid_subscription_allowance_usd")) not in {int, float}
            or sources.get("paid_subscription_allowance_usd") != 0
            or monitoring.get("enabled") is not False
            or learning.get("label_source") != "matured_observations"
            or learning.get("structural_changes") != "shadow_only"
            or learning.get("require_approval_for_promotion") is not True):
        error("UNSAFE_OFFLINE_DEFAULTS", "Spending, monitoring and learning defaults disagree with the offline policy")
    policy = object_field(offline, "external_policy")
    if (policy.get("allowed_domains") != [] or policy.get("allowed_providers") != []
            or policy.get("allowed_purposes") != [] or policy.get("reservation_required") is not True
            or policy.get("completion_log_required") is not True or policy.get("unknown_price_policy") != "DENY"
            or sources.get("approved_sources") != []):
        error("UNSAFE_OFFLINE_DEFAULTS", "Offline source access must remain default-deny")
    expected_roster = ["ttm", "chronos_2", "timesfm_2_5"]
    model_rows = object_rows(registry, "models")
    registered_roster = [model.get("candidate_id") for model in model_rows
                         if model.get("role") == "committed_foundation_candidate"]
    if (project.get("core_foundation_roster") != expected_roster
            or model_policy.get("committed_foundation_candidates") != expected_roster
            or registered_roster != expected_roster):
        error("MODEL_ROSTER_MISMATCH", "Committed foundation roster changed")
    for model in model_rows:
        if model.get("enabled") and (model.get("implementation_status") != "VERIFIED"
                or model.get("license_status") != "VERIFIED_EXACT_ARTIFACT" or not model.get("tested_lock_ref")):
            error("UNVERIFIED_MODEL_ENABLED", str(model.get("candidate_id")))
    if model_policy.get("enabled"):
        error("UNVERIFIED_MODEL_ENABLED", "Initial scaffold has no implemented forecast models")

    try:
        ignores = (root / ".gitignore").read_text().splitlines()
        if "/aXc-ace-forecaster/" not in ignores or ".env" not in ignores:
            error("DONOR_BOUNDARY", "Donor and environment exclusions are required")
        archive = root / "docs/archive/spec-v1"
        manifest = read_json(archive / "MANIFEST.json")
        for entry in manifest["files"]:
            target = (archive / entry["path"]).resolve()
            if not target.is_relative_to(archive) or hashlib.sha256(target.read_bytes()).hexdigest() != entry["sha256"]:
                error("ARCHIVE_INTEGRITY", str(entry["path"]))
    except (OSError, ValueError, KeyError, TypeError) as exc:
        error("ARCHIVE_INTEGRITY", str(exc))

    next_ticket = next((identifier for identifier in order if states[identifier] not in ("COMPLETE", "BLOCKED")
                        and (identifier not in optional_ids or options.get("enabled") is True)
                        and all(states[dep] == "COMPLETE" for dep in graph[identifier])), None)
    return {
        "scope": "scaffold_controls_only",
        "status": "PASSED" if not errors else "FAILED",
        "canonical_goal": "GOAL_UPD.md",
        "application_status": project.get("application_status", "UNKNOWN"),
        "application_acceptance_total": len(requirements),
        "application_acceptance_executed": len(executed_ids),
        "next_ticket": next_ticket,
        "errors": errors,
    }

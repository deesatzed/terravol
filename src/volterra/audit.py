"""Bounded, offline audit helpers for declared project controls."""
from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path
from typing import Any


class AuditError(ValueError):
    """Raised when a local audit control is malformed or overclaims evidence."""


def _read_object(path: Path) -> dict[str, Any]:
    def reject(constant: str) -> None:
        raise AuditError(f"nonfinite JSON constant: {constant}")

    try:
        value = json.loads(path.read_text(encoding="utf-8"), parse_constant=reject)
    except (OSError, json.JSONDecodeError, UnicodeError) as exc:
        raise AuditError(f"cannot read {path.name}: {exc}") from exc
    if not isinstance(value, dict):
        raise AuditError(f"{path.name} must be an object")
    return value


def _require_finite(value: Any) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise AuditError("numeric values must be finite")
    if isinstance(value, dict):
        for nested in value.values():
            _require_finite(nested)
    elif isinstance(value, list):
        for nested in value:
            _require_finite(nested)


def validate_vt00(root: Path) -> dict[str, Any]:
    """Validate VT00's local-only target and external-feasibility declarations."""
    root = root.resolve()
    targets = _read_object(root / "config" / "synthetic_targets.json")
    matrix = _read_object(root / "config" / "feasibility_matrix.json")
    _require_finite(targets)
    _require_finite(matrix)
    if targets.get("schema_version") != "1.0" or matrix.get("schema_version") != "1.0":
        raise AuditError("VT00 controls require schema version 1.0")
    if targets.get("data_mode") != "SYNTHETIC_ONLY" or matrix.get("data_mode") != "SYNTHETIC_ONLY":
        raise AuditError("VT00 controls must remain SYNTHETIC_ONLY")
    equity = targets.get("targets", {}).get("equity_variance", {})
    if (not isinstance(equity, dict) or equity.get("measurement_status") != "SYNTHETIC_PROXY"
            or equity.get("annualization_sessions") != 252):
        raise AuditError("synthetic equity variance target is incomplete")
    dependencies = matrix.get("external_dependencies")
    if not isinstance(dependencies, list) or not dependencies:
        raise AuditError("feasibility matrix needs external dependency records")
    statuses: Counter[str] = Counter()
    for dependency in dependencies:
        if not isinstance(dependency, dict):
            raise AuditError("feasibility dependency must be an object")
        if not all(isinstance(dependency.get(field), str) and dependency[field]
                       for field in ("dependency_id", "category", "required_for", "status", "missing_evidence")):
            raise AuditError("feasibility dependency has incomplete identity or evidence")
        if dependency["status"] not in {"UNVERIFIED", "BLOCKED", "NOT_APPLICABLE"}:
            raise AuditError("VT00 may not claim external feasibility verified")
        statuses[dependency["status"]] += 1
    return {
        "scope": "vt00_local_controls_only",
        "status": "PASSED",
        "data_mode": "SYNTHETIC_ONLY",
        "external_dependencies": dict(sorted(statuses.items())),
    }

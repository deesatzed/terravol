"""Policy evaluation and SQLite-backed cost reservation; no dispatch implementation exists here."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import math
import sqlite3


# These actions are outside VOLTERRA's scope regardless of caller configuration.
_FORBIDDEN_PURPOSES = frozenset({
    "brokerage", "trade", "trading", "order_placement", "account_control",
})


@dataclass(frozen=True)
class DispatchPolicy:
    allow_network: bool
    allowed_domains: tuple[str, ...]
    allowed_purposes: tuple[str, ...]
    max_external_usd: float
    action_limit: int


@dataclass(frozen=True)
class DispatchRequest:
    request_id: str
    domain: str
    purpose: str
    worst_case_usd: float
    deadline_at: datetime
    capability_verified: bool
    license_verified: bool


@dataclass(frozen=True)
class DispatchDecision:
    status: str
    reason: str | None = None


@dataclass(frozen=True)
class ReservationRecord:
    request_id: str
    worst_case_usd: float
    actual_usd: float | None
    status: str
    completed_at: datetime | None


class ReservationLedger:
    """Records reservations only; callers receive a decision and must not infer an external call."""

    def __init__(self, policy: DispatchPolicy) -> None:
        self.policy = policy
        self.connection = sqlite3.connect(":memory:", isolation_level=None)
        self.connection.execute("""
            CREATE TABLE reservations (
                request_id TEXT PRIMARY KEY,
                worst_case_usd REAL NOT NULL CHECK (worst_case_usd >= 0),
                actual_usd REAL CHECK (actual_usd IS NULL OR actual_usd >= 0),
                completed_at TEXT,
                status TEXT NOT NULL CHECK (status IN ('RESERVED', 'CANCELLED', 'COMPLETED', 'FAILED'))
            )
        """)

    @staticmethod
    def _instant(value: datetime) -> datetime:
        if value.tzinfo is None:
            raise ValueError("dispatch timestamps must be timezone-aware")
        return value.astimezone(timezone.utc)

    def reserve(self, request: DispatchRequest, *, now: datetime) -> DispatchDecision:
        now = self._instant(now)
        deadline = self._instant(request.deadline_at)
        if deadline <= now:
            return DispatchDecision("DENIED", "DEADLINE_EXPIRED")
        if not self.policy.allow_network:
            return DispatchDecision("DENIED", "NETWORK_DISABLED")
        if request.purpose.strip().casefold() in _FORBIDDEN_PURPOSES:
            return DispatchDecision("DENIED", "FORBIDDEN_PURPOSE")
        if request.domain not in self.policy.allowed_domains:
            return DispatchDecision("DENIED", "DOMAIN_NOT_ALLOWED")
        if request.purpose not in self.policy.allowed_purposes:
            return DispatchDecision("DENIED", "PURPOSE_NOT_ALLOWED")
        if not request.capability_verified:
            return DispatchDecision("DENIED", "CAPABILITY_UNVERIFIED")
        if not request.license_verified:
            return DispatchDecision("DENIED", "LICENSE_UNVERIFIED")
        if request.worst_case_usd < 0:
            return DispatchDecision("DENIED", "INVALID_COST")
        if self.policy.max_external_usd == 0 and request.worst_case_usd > 0:
            return DispatchDecision("DENIED", "BUDGET_ZERO")
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            active_cost, active_count = self.connection.execute(
                "SELECT COALESCE(SUM(worst_case_usd), 0), COUNT(*) FROM reservations WHERE status = 'RESERVED'"
            ).fetchone()
            if active_count >= self.policy.action_limit:
                self.connection.execute("ROLLBACK")
                return DispatchDecision("DENIED", "ACTION_LIMIT")
            if active_cost + request.worst_case_usd > self.policy.max_external_usd:
                self.connection.execute("ROLLBACK")
                return DispatchDecision("DENIED", "BUDGET_EXCEEDED")
            try:
                self.connection.execute(
                    "INSERT INTO reservations(request_id, worst_case_usd, status) VALUES (?, ?, 'RESERVED')",
                    (request.request_id, request.worst_case_usd),
                )
            except sqlite3.IntegrityError:
                self.connection.execute("ROLLBACK")
                return DispatchDecision("DENIED", "DUPLICATE_REQUEST")
            self.connection.execute("COMMIT")
        except BaseException:
            if self.connection.in_transaction:
                self.connection.execute("ROLLBACK")
            raise
        return DispatchDecision("RESERVED")

    def cancel(self, request_id: str) -> None:
        self._close(request_id, "CANCELLED")

    def fail(self, request_id: str) -> None:
        self._close(request_id, "FAILED")

    def complete(self, request_id: str, *, actual_usd: float, completed_at: datetime | None = None) -> None:
        """Close a reservation and retain the observed charge for later reconciliation."""
        if not math.isfinite(actual_usd) or actual_usd < 0:
            raise ValueError("actual_usd must be a finite non-negative number")
        when = datetime.now(timezone.utc) if completed_at is None else self._instant(completed_at)
        with self.connection:
            result = self.connection.execute(
                """UPDATE reservations
                   SET status = 'COMPLETED', actual_usd = ?, completed_at = ?
                   WHERE request_id = ? AND status = 'RESERVED'""",
                (actual_usd, when.isoformat(), request_id),
            )
        if result.rowcount != 1:
            raise ValueError("only an active reservation can be completed")

    def reservation_record(self, request_id: str) -> ReservationRecord:
        row = self.connection.execute(
            "SELECT request_id, worst_case_usd, actual_usd, status, completed_at FROM reservations WHERE request_id = ?",
            (request_id,),
        ).fetchone()
        if row is None:
            raise KeyError(f"unknown reservation: {request_id}")
        completed_at = None if row[4] is None else datetime.fromisoformat(row[4])
        return ReservationRecord(row[0], row[1], row[2], row[3], completed_at)

    def _close(self, request_id: str, status: str) -> None:
        with self.connection:
            result = self.connection.execute(
                "UPDATE reservations SET status = ? WHERE request_id = ? AND status = 'RESERVED'",
                (status, request_id),
            )
        if result.rowcount != 1:
            raise ValueError("only an active reservation can be closed")

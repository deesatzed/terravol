"""Append-only SQLite evidence revisions and sealed as-of snapshots."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import hashlib
import sqlite3
from pathlib import Path
from typing import Any

from volterra.contracts import ContractError, canonical_json


class LedgerError(ContractError):
    """A ledger operation violates temporal or referential integrity."""


def _utc(value: datetime, field: str) -> str:
    if value.tzinfo is None:
        raise LedgerError(f"{field} must be timezone-aware")
    return value.astimezone(timezone.utc).isoformat()


@dataclass(frozen=True)
class EvidenceInput:
    logical_id: str
    source_id: str
    payload: Any
    event_at: datetime
    published_at: datetime
    available_at: datetime
    received_at: datetime
    observation_state: str
    synthetic: bool
    supersedes_revision_id: str | None = None


@dataclass(frozen=True)
class Snapshot:
    snapshot_id: str
    origin_at: datetime
    policy: str
    revision_ids: tuple[str, ...]


@dataclass(frozen=True)
class TargetDefinition:
    target_id: str
    horizon_sessions: int
    estimator_id: str
    units: str

    def __post_init__(self) -> None:
        if not self.target_id or not self.estimator_id or not self.units:
            raise LedgerError("target identity, estimator and units are required")
        if isinstance(self.horizon_sessions, bool) or not isinstance(self.horizon_sessions, int) or self.horizon_sessions <= 0:
            raise LedgerError("horizon_sessions must be a positive integer")


class EvidenceLedger:
    """A local ledger; it never fetches, executes, or interprets external evidence."""

    def __init__(self, path: Path) -> None:
        self.path = path
        self.connection = sqlite3.connect(path)
        self.connection.execute("PRAGMA foreign_keys = ON")
        self._initialize()

    def _initialize(self) -> None:
        self.connection.executescript("""
            CREATE TABLE IF NOT EXISTS evidence_revisions (
                revision_id TEXT PRIMARY KEY,
                logical_id TEXT NOT NULL,
                source_id TEXT NOT NULL,
                payload_json TEXT NOT NULL,
                payload_sha256 TEXT NOT NULL,
                event_at TEXT NOT NULL,
                published_at TEXT NOT NULL,
                available_at TEXT NOT NULL,
                received_at TEXT NOT NULL,
                observation_state TEXT NOT NULL,
                synthetic INTEGER NOT NULL CHECK (synthetic IN (0, 1)),
                supersedes_revision_id TEXT REFERENCES evidence_revisions(revision_id)
            );
            CREATE INDEX IF NOT EXISTS evidence_eligible_idx
                ON evidence_revisions(logical_id, available_at, received_at);
            CREATE TABLE IF NOT EXISTS snapshots (
                snapshot_id TEXT PRIMARY KEY,
                origin_at TEXT NOT NULL,
                policy TEXT NOT NULL CHECK (policy IN ('live', 'certified_historical'))
            );
            CREATE TABLE IF NOT EXISTS snapshot_revisions (
                snapshot_id TEXT NOT NULL REFERENCES snapshots(snapshot_id),
                revision_id TEXT NOT NULL REFERENCES evidence_revisions(revision_id),
                PRIMARY KEY (snapshot_id, revision_id)
            );
            CREATE TABLE IF NOT EXISTS target_definitions (
                target_id TEXT PRIMARY KEY,
                horizon_sessions INTEGER NOT NULL CHECK (horizon_sessions > 0),
                estimator_id TEXT NOT NULL,
                units TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS outcomes (
                outcome_id TEXT PRIMARY KEY,
                target_id TEXT NOT NULL REFERENCES target_definitions(target_id),
                origin_at TEXT NOT NULL,
                completed_sessions INTEGER NOT NULL CHECK (completed_sessions > 0),
                target_end_at TEXT NOT NULL,
                first_public_at TEXT NOT NULL,
                value_json TEXT NOT NULL,
                synthetic INTEGER NOT NULL CHECK (synthetic IN (0, 1))
            );
            CREATE TABLE IF NOT EXISTS artifacts (
                artifact_sha256 TEXT PRIMARY KEY,
                payload BLOB NOT NULL,
                byte_count INTEGER NOT NULL CHECK (byte_count >= 0)
            );
            CREATE TABLE IF NOT EXISTS jobs (
                job_kind TEXT NOT NULL,
                idempotency_key TEXT NOT NULL,
                status TEXT NOT NULL CHECK (status IN ('RUNNING', 'COMPLETED', 'FAILED')),
                PRIMARY KEY (job_kind, idempotency_key)
            );
        """)
        self.connection.commit()

    def append_evidence(self, evidence: EvidenceInput) -> str:
        if not evidence.logical_id or not evidence.source_id:
            raise LedgerError("logical_id and source_id are required")
        if evidence.observation_state not in {
            "OBSERVED", "MISSING", "UNAVAILABLE", "STALE", "CONTRADICTORY", "CENSORED", "ASSUMED",
        }:
            raise LedgerError("observation_state is unsupported")
        timestamps = {
            "event_at": _utc(evidence.event_at, "event_at"),
            "published_at": _utc(evidence.published_at, "published_at"),
            "available_at": _utc(evidence.available_at, "available_at"),
            "received_at": _utc(evidence.received_at, "received_at"),
        }
        if timestamps["available_at"] < timestamps["published_at"]:
            raise LedgerError("available_at cannot precede published_at")
        payload_json = canonical_json(evidence.payload)
        payload_hash = hashlib.sha256(payload_json.encode()).hexdigest()
        revision_key = canonical_json({
            "logical_id": evidence.logical_id,
            "source_id": evidence.source_id,
            "payload_sha256": payload_hash,
            **timestamps,
            "observation_state": evidence.observation_state,
            "synthetic": evidence.synthetic,
            "supersedes_revision_id": evidence.supersedes_revision_id,
        })
        revision_id = hashlib.sha256(revision_key.encode()).hexdigest()
        with self.connection:
            if evidence.supersedes_revision_id is not None:
                previous = self.connection.execute(
                    "SELECT logical_id FROM evidence_revisions WHERE revision_id = ?",
                    (evidence.supersedes_revision_id,),
                ).fetchone()
                if previous is None:
                    raise LedgerError("supersedes_revision_id does not exist")
                if previous[0] != evidence.logical_id:
                    raise LedgerError("a revision may supersede only the same logical_id")
            self.connection.execute(
                """INSERT OR IGNORE INTO evidence_revisions
                   (revision_id, logical_id, source_id, payload_json, payload_sha256,
                    event_at, published_at, available_at, received_at, observation_state,
                    synthetic, supersedes_revision_id)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (revision_id, evidence.logical_id, evidence.source_id, payload_json, payload_hash,
                 timestamps["event_at"], timestamps["published_at"], timestamps["available_at"],
                 timestamps["received_at"], evidence.observation_state, int(evidence.synthetic),
                 evidence.supersedes_revision_id),
            )
        return revision_id

    def create_snapshot(self, snapshot_id: str, origin_at: datetime, *, policy: str) -> Snapshot:
        if not snapshot_id:
            raise LedgerError("snapshot_id is required")
        if policy not in {"live", "certified_historical"}:
            raise LedgerError("snapshot policy is unsupported")
        origin = _utc(origin_at, "origin_at")
        received_clause = "AND received_at <= ?" if policy == "live" else ""
        parameters: tuple[str, ...] = (origin, origin) if policy == "live" else (origin,)
        rows = self.connection.execute(
            f"""SELECT revision_id FROM (
                    SELECT revision_id, logical_id,
                           ROW_NUMBER() OVER (
                               PARTITION BY logical_id
                               ORDER BY available_at DESC, published_at DESC, revision_id DESC
                           ) AS selection_rank
                    FROM evidence_revisions
                    WHERE available_at <= ? {received_clause}
                ) WHERE selection_rank = 1
                ORDER BY revision_id""",
            parameters,
        ).fetchall()
        revision_ids = tuple(row[0] for row in rows)
        with self.connection:
            try:
                self.connection.execute(
                    "INSERT INTO snapshots(snapshot_id, origin_at, policy) VALUES (?, ?, ?)",
                    (snapshot_id, origin, policy),
                )
            except sqlite3.IntegrityError as exc:
                raise LedgerError("snapshot_id is already sealed") from exc
            self.connection.executemany(
                "INSERT INTO snapshot_revisions(snapshot_id, revision_id) VALUES (?, ?)",
                ((snapshot_id, revision_id) for revision_id in revision_ids),
            )
        return Snapshot(snapshot_id, datetime.fromisoformat(origin), policy, revision_ids)

    def get_snapshot(self, snapshot_id: str) -> Snapshot:
        row = self.connection.execute(
            "SELECT origin_at, policy FROM snapshots WHERE snapshot_id = ?", (snapshot_id,)
        ).fetchone()
        if row is None:
            raise LedgerError("snapshot_id does not exist")
        revisions = self.connection.execute(
            "SELECT revision_id FROM snapshot_revisions WHERE snapshot_id = ? ORDER BY revision_id",
            (snapshot_id,),
        ).fetchall()
        return Snapshot(snapshot_id, datetime.fromisoformat(row[0]), row[1], tuple(item[0] for item in revisions))

    def register_target(self, target: TargetDefinition) -> None:
        with self.connection:
            existing = self.connection.execute(
                "SELECT horizon_sessions, estimator_id, units FROM target_definitions WHERE target_id = ?",
                (target.target_id,),
            ).fetchone()
            current = (target.horizon_sessions, target.estimator_id, target.units)
            if existing is not None and tuple(existing) != current:
                raise LedgerError("target_id is immutable; use a new target version")
            self.connection.execute(
                "INSERT OR IGNORE INTO target_definitions(target_id, horizon_sessions, estimator_id, units) VALUES (?, ?, ?, ?)",
                (target.target_id, *current),
            )

    def record_outcome(self, *, target_id: str, origin_at: datetime, completed_sessions: int,
                       target_end_at: datetime, first_public_at: datetime, value: Any,
                       synthetic: bool) -> str:
        target = self.connection.execute(
            "SELECT horizon_sessions FROM target_definitions WHERE target_id = ?", (target_id,)
        ).fetchone()
        if target is None:
            raise LedgerError("target_id does not exist")
        if isinstance(completed_sessions, bool) or completed_sessions != target[0]:
            raise LedgerError("completed_sessions must equal the declared target horizon")
        origin = _utc(origin_at, "origin_at")
        end = _utc(target_end_at, "target_end_at")
        published = _utc(first_public_at, "first_public_at")
        if end <= origin or published < end:
            raise LedgerError("outcome must end after origin and publish no earlier than target end")
        value_json = canonical_json(value)
        outcome_id = hashlib.sha256(canonical_json({
            "target_id": target_id, "origin_at": origin, "completed_sessions": completed_sessions,
            "target_end_at": end, "first_public_at": published, "value": value_json,
            "synthetic": synthetic,
        }).encode()).hexdigest()
        with self.connection:
            self.connection.execute(
                """INSERT OR IGNORE INTO outcomes
                   (outcome_id, target_id, origin_at, completed_sessions, target_end_at, first_public_at, value_json, synthetic)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (outcome_id, target_id, origin, completed_sessions, end, published, value_json, int(synthetic)),
            )
        return outcome_id

    def is_outcome_mature(self, outcome_id: str, as_of: datetime) -> bool:
        row = self.connection.execute(
            "SELECT target_end_at, first_public_at FROM outcomes WHERE outcome_id = ?", (outcome_id,)
        ).fetchone()
        if row is None:
            raise LedgerError("outcome_id does not exist")
        instant = _utc(as_of, "as_of")
        return instant >= row[0] and instant >= row[1]

    def put_artifact(self, payload: bytes) -> str:
        if not isinstance(payload, bytes):
            raise LedgerError("artifact payload must be bytes")
        digest = hashlib.sha256(payload).hexdigest()
        with self.connection:
            self.connection.execute(
                "INSERT OR IGNORE INTO artifacts(artifact_sha256, payload, byte_count) VALUES (?, ?, ?)",
                (digest, payload, len(payload)),
            )
        return digest

    def read_artifact(self, artifact_sha256: str) -> bytes:
        if len(artifact_sha256) != 64 or any(char not in "0123456789abcdef" for char in artifact_sha256):
            raise LedgerError("artifact_sha256 must be a lowercase SHA-256 digest")
        row = self.connection.execute(
            "SELECT payload, byte_count FROM artifacts WHERE artifact_sha256 = ?", (artifact_sha256,)
        ).fetchone()
        if row is None:
            raise LedgerError("artifact_sha256 does not exist")
        payload = bytes(row[0])
        if len(payload) != row[1] or hashlib.sha256(payload).hexdigest() != artifact_sha256:
            raise LedgerError("artifact payload hash or length does not match reference")
        return payload

    def claim_job(self, job_kind: str, idempotency_key: str) -> bool:
        if not job_kind or not idempotency_key:
            raise LedgerError("job_kind and idempotency_key are required")
        with self.connection:
            result = self.connection.execute(
                "INSERT OR IGNORE INTO jobs(job_kind, idempotency_key, status) VALUES (?, ?, 'RUNNING')",
                (job_kind, idempotency_key),
            )
        return result.rowcount == 1

    def complete_job(self, job_kind: str, idempotency_key: str) -> None:
        with self.connection:
            result = self.connection.execute(
                "UPDATE jobs SET status = 'COMPLETED' WHERE job_kind = ? AND idempotency_key = ? AND status = 'RUNNING'",
                (job_kind, idempotency_key),
            )
        if result.rowcount != 1:
            raise LedgerError("only a running job may be completed")

    def job_status(self, job_kind: str, idempotency_key: str) -> str:
        row = self.connection.execute(
            "SELECT status FROM jobs WHERE job_kind = ? AND idempotency_key = ?", (job_kind, idempotency_key)
        ).fetchone()
        if row is None:
            raise LedgerError("job does not exist")
        return str(row[0])

    def close(self) -> None:
        self.connection.close()

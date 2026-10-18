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

    def close(self) -> None:
        self.connection.close()

# VT02 Ledger, Snapshot, Maturity, and Policy Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use `test-driven-development` to implement this plan task-by-task.

**Goal:** Provide the durable local boundary that freezes as-of evidence and targets, rejects invalid lineage/artifacts, and deterministically prevents unauthorized external dispatch.

**Architecture:** A standard-library SQLite ledger owns append-only evidence revisions, content-addressed artifacts, snapshots, target definitions and outcome maturity. A separate pure policy module validates external-call requests and uses SQLite transactions for reservations/completion. Both work offline against synthetic records; neither performs network I/O.

**Tech Stack:** Python 3.12 `sqlite3`, dataclasses, `unittest`, existing VT01 contracts.

---

### Task 1: Evidence revisions and as-of snapshots

**Files:**

- Create: `src/volterra/storage/__init__.py`
- Create: `src/volterra/storage/ledger.py`
- Create: `tests/application/test_time.py`
- Create: `tests/application/test_data.py`

**Step 1:** Write failing tests for a future-published revision exclusion, live versus certified-history eligibility, revision-specific snapshots, and immutable snapshot membership.

**Step 2:** Run `PYTHONPATH=src .venv/bin/python -B -m unittest discover -s tests/application -p test_time.py -v`; expect a missing ledger implementation failure.

**Step 3:** Implement the minimal schema and API: append evidence, retain superseded revisions, create snapshots from explicit as-of policy, and seal snapshot membership.

**Step 4:** Run focused tests green.

### Task 2: Target/maturity and artifact integrity

**Files:**

- Modify: `src/volterra/storage/ledger.py`
- Modify: `tests/application/test_time.py`
- Modify: `tests/application/test_data.py`
- Modify: `tests/application/test_ctrl.py`

**Step 1:** Add failing tests for 1/5/20-session maturity, distinct missing/stale states, explicit nonpositive-price unsupported state, hash-verified artifacts, and rejected nonexistent references.

**Step 2:** Run the focused test modules; verify the expected failures.

**Step 3:** Add target definitions, outcome recording/maturity checks, content-addressed artifact persistence and FK checks. Do not implement forecasts or scores.

**Step 4:** Run the focused tests green.

### Task 3: Deterministic dispatch policy and budget reservation

**Files:**

- Create: `src/volterra/policy/__init__.py`
- Create: `src/volterra/policy/dispatch.py`
- Create: `tests/application/test_sel.py`
- Modify: `tests/application/test_ctrl.py`
- Modify: `tests/application/test_ops.py`

**Step 1:** Write failing tests for zero budget, allowlist/purpose/deadline limits, in-flight reservation limits, cancellation/failure reconciliation, capability/license ineligibility, and absence of any brokerage action.

**Step 2:** Run the focused tests and confirm implementation-related failures.

**Step 3:** Implement validation/reservation/completion records only. Return explicit denied states; never invoke a provider, URL, subprocess or fallback.

**Step 4:** Run focused tests green.

### Task 4: Record VT02 evidence only after full validation

**Files:**

- Modify: `docs/DATA_CONTRACTS.md`, `docs/TRANSFORMATION_AUDIT.md`, `docs/STATUS.md`, `TASK_QUEUE.md`, `PROGRESS.md`
- Modify: `config/implementation_queue.json`, `config/acceptance_matrix.json`
- Create: `reports/vt02/application-acceptance.json`, `reports/vt02/ticket-verification.json`

Run the full test suite, scaffold validation, offline doctor, wheel build, current/archived manifest checks and then update only acceptance IDs proven by those tests. Commit the bounded VT02 increment without data/model/donor artifacts.

# VT00–VT01 Integrity Foundation Implementation Plan

> **For Codex:** REQUIRED SUB-SKILL: Use `test-driven-development` to implement this plan task-by-task.

**Goal:** Close the present-state feasibility audit and establish a small, executable typed-contract boundary that rejects unsafe numerical/probability/distribution inputs.

**Architecture:** VT00 becomes a bounded, evidence-linked local audit: repository boundary, exact development environment, synthetic-target declaration, and an explicitly unverified external-source/model feasibility matrix. VT01 supplies pure standard-library contract objects and canonical JSON serialization. It owns no database, data retrieval, model inference, or external calls.

**Tech Stack:** Python 3.12 standard library, `unittest`, JSON control artifacts, Markdown evidence records.

---

### Task 1: Close the bounded VT00 audit

**Files:**

- Create: `config/synthetic_targets.json`
- Create: `config/feasibility_matrix.json`
- Create: `tests/application/test_audit.py`
- Modify: `docs/TRANSFORMATION_AUDIT.md`
- Modify: `config/implementation_queue.json`
- Modify: `config/acceptance_matrix.json`
- Create: `reports/vt00/verification.json`

**Step 1: Write failing audit tests**

Test that the synthetic target declaration is finite/versioned and uses explicit proxy status, the feasibility matrix never claims unresolved sources/models are verified, and the canonical/donor boundary stays excluded.

**Step 2: Run the focused test and verify failure**

Run: `PYTHONPATH=src .venv/bin/python -B -m unittest tests.application.test_audit -v`

Expected: FAIL because the application audit module/configuration does not yet exist.

**Step 3: Implement the smallest local audit validator**

Create a read-only `volterra.audit` validator for the two new controls; implement no external checks. Add explicit `UNVERIFIED`/`BLOCKED` states for all unavailable source/model evidence.

**Step 4: Record actual audit evidence**

Run the validator and write its command, environment, repository boundary and results to `reports/vt00/verification.json`. Update the transformation audit and queue only when the focused tests pass.

**Step 5: Verify the focused audit tests**

Run: `PYTHONPATH=src .venv/bin/python -B -m unittest tests.application.test_audit -v`

Expected: PASS; no data/model is asserted available.

### Task 2: Define safe contract primitives

**Files:**

- Create: `src/volterra/contracts/__init__.py`
- Create: `src/volterra/contracts/core.py`
- Create: `tests/application/test_prob.py`
- Create: `tests/application/test_dist.py`
- Create: `tests/application/test_ctrl.py`

**Step 1: Write failing contract tests**

Cover distinct probability types, recursive finite-number rejection including `1e999`, monotone quantile records with no implied tails/joint paths, and invalid Student-t parameter/moment requests.

**Step 2: Run each focused test and verify failure**

Run: `PYTHONPATH=src .venv/bin/python -B -m unittest tests.application.test_prob tests.application.test_dist tests.application.test_ctrl -v`

Expected: FAIL because `volterra.contracts` does not exist.

**Step 3: Implement the minimum pure contract layer**

Add immutable dataclasses, `ContractError`, finite recursive JSON encoding, typed probability wrappers, `QuantileForecast`, `StudentTSpec`, and `CapabilityManifest`. No automatic tail fitting, inferred joint capability, or arbitrary object deserialization.

**Step 4: Verify focused and full tests**

Run the three application modules, then `PYTHONPATH=src .venv/bin/python -B -m unittest discover -s tests -v`.

Expected: PASS with scaffold tests still green.

### Task 3: Publish truthful VT01 evidence

**Files:**

- Modify: `docs/DATA_CONTRACTS.md`
- Modify: `docs/TRANSFORMATION_AUDIT.md`
- Modify: `config/implementation_queue.json`
- Modify: `config/acceptance_matrix.json`
- Create: `reports/vt01/verification.json`
- Modify: `PROGRESS.md`

**Step 1: Bind execution receipts to the exact application tests**

Record only executed acceptance IDs: `AC-PROB-01`, `AC-DIST-02`, `AC-CTRL-05`, and `AC-CTRL-06`. Preserve every other application requirement as `NOT_IMPLEMENTED`.

**Step 2: Run control validation and final verification**

Run `volterra scaffold validate`, focused application tests, all tests, and an archive-integrity check. Confirm receipt references, ticket dependencies and application count agree.

**Step 3: Commit the bounded foundation**

Stage only VT00/VT01 code, tests, controls, reports and documented state. Do not stage donor/data/model artifacts.

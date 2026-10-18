# VOLTERRA — Design and build package

**Specification version:** 1.0 · **Research checked:** October 17, 2026

**Status:** Build-ready design, not a completed forecasting application or a validated investment strategy. The accompanying schemas and examples are specification fixtures. No real market forecasts, performance measurements, fitted weights, or live trading components are included.

VOLTERRA is a local-first, evidence-driven volatility forecasting and research system. It estimates the magnitude, onset, persistence, and uncertainty of future volatility, learns when its methods are useful, and supports inspectable expert-system scenarios. An optional, separate options research module evaluates whether a forecast can support a particular strategy after costs.

## Start here

Read `GOAL.md`, then `DESIGN_SPEC.md`, `SCIENCE_AND_EVALUATION.md`, and `BUILD_PLAN.md`. Use `AGENTS.md` as the coding-agent instruction file. `ACCEPTANCE_TESTS.md` defines required tests, not tests already passed.

| File | Purpose |
|---|---|
| GOAL.md | Authoritative scope, invariants, expected behavior and completion gates |
| DESIGN_SPEC.md | Architecture, mathematical responsibilities, ESS and bounded learning |
| SCIENCE_AND_EVALUATION.md | Targets, validation, scientific hypotheses and options distinctions |
| DATA_CONTRACTS.md | Point-in-time data, runtime records, APIs and schema semantics |
| REUSE_AUDIT.md | Code-level findings and safe extraction from aXc-ACE |
| BUILD_PLAN.md | Dependency-ordered implementation tickets |
| ACCEPTANCE_TESTS.md | Traceable correctness, failure and statistical tests |
| RESEARCH_NOTES.md | Verified primary sources and decisions they support |
| AGENTS.md | Implementation constraints and progress requirements |
| config/ | Non-executable policy and model-registry examples |
| schemas/ | JSON Schema contract fixtures |
| examples/ | Entirely synthetic valid and invalid test inputs |
| tools/validate_specs.py | Checks this specification package, not forecasting skill |
| PACKAGE_VALIDATION.json | Results of the package-only validation |
| MANIFEST.json | File integrity hashes |

## Source repository inspected

`deesatzed/aXc-ace-forecaster`, pinned at commit `3bd39789c3811a5b437baf60a65de480aa0486bf`.

Selected source methods were read through the connected GitHub repository. Its complete test suite, deployment, external aXc service and reported numerical performance were not executed or independently reproduced. Do not promote the README's performance claims into VOLTERRA requirements or marketing.

## First deliverable

A deterministic, offline command-line research slice that loads synthetic data, enforces as-of access, produces distributional volatility forecasts, records immutable predictions, matures labels, and compares baselines. Build this before agents, a graph editor, or an options dashboard.

## Validate these fixtures

From an environment with `jsonschema` installed, run:

```bash
python tools/validate_specs.py
```

The validator checks four schemas, synthetic fixtures, selected semantic invariants and deliberate rejection cases. It does not run the 78 planned application acceptance requirements, numerical inference, an exchange calendar, a forecast backtest, or any trading strategy. The semantic graph validator intentionally supports only a small subset and rejects unsupported families rather than pretending to infer them.

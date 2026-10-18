# Model integration status

Machine inventory: [model_registry.json](../config/model_registry.json). Active scope: [GOAL_UPD.md](../GOAL_UPD.md) §6. **All forecasting candidates are disabled and unimplemented.** No checkpoint, model benchmark or ML resource measurement is supplied by the scaffold.

Mandatory numerical controls are persistence, EWMA, Log-HAR and GJR-GARCH with compatible distributions/measurement links. Committed foundation candidates are TTM, Chronos-2 and TimesFM 2.5. TiRex-2, small Toto and other named alternatives remain optional or restricted challengers. Do not silently replace the committed roster.

Before enabling any candidate, record actual code/checkpoint revision, artifact checksum, tested dependency lock, device/precision, resources, input/covariate semantics, output support/quantiles, joint-path capability, missingness and actual fallback identity. Audit code, weights and data terms independently for the intended deployment. Published capabilities are not local verification.

The scaffold's Python/build/jsonschema environment is separate from the eventual numerical worker environments. Do not treat its small dependency lock as compatibility proof for any foundation model. A blocked model test remains blocked even when the offline classical slice passes.

# Synthetic contract fixtures

All values and identifiers here are hand-authored to illustrate contracts. They are not fitted forecasts, historical prices, market probabilities, calibration measurements or operational advice.

The forecast is intentionally **marginal-only** and has no onset/duration field. Its volatility quantiles equal the specified transformation of the variance quantiles. That arithmetic alone does not establish a calibrated distribution.

The tiny graph demonstrates a beta–Bernoulli parameter dependency, not the full VOLTERRA market model. The schema validator checks its structure; it does not fit the graph or compute a posterior. Date ranges are fixture values, not an implemented exchange-calendar verification.

`invalid/` contains deliberately rejected inputs for the package-only validator. Additional rejection cases are constructed in memory by that validator. Required application tests remain unimplemented requirements in `ACCEPTANCE_TESTS.md`.

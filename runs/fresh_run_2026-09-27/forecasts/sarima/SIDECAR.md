# sarima

Produced fresh by dcfootprint/experiments/forecast_run.py (dcfootprint venv). SARIMA(1,1,1)(1,0,1,12),
stationarity/invertibility enforced, missing months kept as NaN, L-BFGS maxiter 500. A fit is a recorded
FAILURE (metrics/failures.csv) if it does not converge, is degenerate (a coefficient on the unit boundary or
non-finite SE), diverges (>10x historical max) or raises. Predictive mean, SE and 80% interval from statsmodels.
Deterministic (no seed).

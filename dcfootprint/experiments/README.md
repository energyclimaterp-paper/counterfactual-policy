# experiments/

Scripts that sit outside the pipeline: checks, reports and the forecasting run. None of them is needed to
produce `results/`. Run them from the repository root with
`PYTHONPATH=dcfootprint/src .venv/Scripts/python.exe dcfootprint/experiments/<script>.py`.

## Checking a change

| Script | What it does |
|---|---|
| `compare_results.py <dir_a> <dir_b>` | compares two results folders file by file (CSVs numerically); used to attribute every change |
| `spotcheck_trace.py` | re-computes selected facilities from the raw files, hop by hop, without the pipeline's own functions |
| `gadm_gem_state_check.py` | checks GEM power-plant state labels against GADM boundaries (report only) |

## Reports and data rebuilds

| Script | What it does |
|---|---|
| `round3_report.py` | writes `results/round3_final/ROUND3_REPORT.md` from the canonical run's files |
| `extract_eu_tables.py` | rebuilds `config/eu_member_state_2023.csv` from the EU report PDF and checks it against the report's totals |

## Forecasting run (`runs/fresh_run_2026-09-27/`)

Run in this order:

| Script | What it does |
|---|---|
| `forecast_metrics.py` | the 10 metrics (MAE, RMSE, WMAPE, bias, MASE, sMAPE, MedAE, Pearson, PICP, CRPS); imported by the others |
| `forecast_run.py` | fresh seasonal-naive and SARIMA forecasts, 3 rolling origins, 12-month horizon, India/US/EU |
| `score_core_cached.py` | scores the Co-RE cached forecasts (xLSTM, TimesFM 2.5, Chronos-2, SARIMA) with the same metrics |
| `assemble_forecast_run.py` | writes the run's manifest, environment freezes, seeds and config snapshot |
| `summarize_forecast_run.py` | writes `report/RUN_SUMMARY.md` from the metric files |

The Co-RE cache's "Nexus" column is Chronos-2 in the Nexus slot and is labelled `chronos-2`; the real
multi-agent Nexus has not been run.

## Early gate experiments (2026-09-26, historical)

| Script | What it tested | Result |
|---|---|---|
| `gates_1_2_calibration_coverage.py` | G1: bottom-up India capacity vs CEEW; G2: coverage | G1 pass (1.39 GW vs 1.5-1.8); G2 plausible |
| `gate3_rq2_scarcity_reranking.py` | G3: does annual scarcity weighting re-rank hotspots? | no: datacenters already sit in stressed basins |

These two predate the package and read from a hard-coded path (`R = ...` at the top); set it to your
repository root before running them.

# Forecasting: does complexity pay? (the reviewer answer)

Direct answer to the Co-RE reviews (R1: *"compare simple per-DC forecasters; if they're good, why compute-heavy
DNNs?"*; R2: *"benchmark the GNNs against a non-DL hierarchical method"*). Evidence:
`runs/fresh_run_core_grid_2026-09-28`, **66 account-zone series** (India 9 · US 36 · EU 21), rolling-origin
backtest, 10 metrics + prediction intervals. Lower RMSE is better; **MASE < 1 beats seasonal-naive.**

## Carbon (66 series, holdout)
| rank | model | class | RMSE | MASE |
|---|---|---|---|---|
| 1 | sarima_dcf | **simple — hierarchical/bottom-up SARIMA** | 37.2 | 0.80 |
| 2 | chronos_2 | complex — foundation model | 38.6 | 0.79 |
| 3 | timesfm | complex — foundation model | 40.6 | 0.83 |
| 4 | seasonal_naive | simple — naive | 41.7 | 0.83 |
| 5 | sarima_core | simple — classical SARIMA | 42.4 | 0.87 |
| 6 | xlstm | **complex — deep net** | 46.3 | ~0.99 |

## Electricity (66 series, holdout)
| rank | model | class | RMSE | MASE |
|---|---|---|---|---|
| 1 | seasonal_naive | **simple — naive** | 821.9 | 0.94 |
| 2 | chronos_2 | complex — foundation model | 879.0 | 0.84 |
| 3 | timesfm | complex — foundation model | 898.9 | 0.88 |
| 4 | sarima_core | simple — classical SARIMA | 907.3 | 0.96 |
| 5 | xlstm | **complex — deep net** | ~1089 (high seed variance) | >1.0 |

## Findings
1. **The deep net (xLSTM) is the worst** on both carbon and electricity — complexity actively hurts.
2. **The simplest methods win or tie:** hierarchical SARIMA tops carbon; seasonal-naive tops electricity (by RMSE).
3. **Foundation models (Chronos-2 / TimesFM) are competitive but never decisively better** — they don't justify
   their compute cost or opacity.
4. **No model meaningfully beats seasonal-naive** (all MASE 0.79–1.0; RMSE gaps are small).
5. **The GNN adds nothing:** Co-RE showed graph structure does not beat degree-matched random controls
   (`context/GNN_AUTOPSY.md`).

## What this means for the paper
- `sarima_dcf` is the **bottom-up / hierarchical reconciliation (MinT family)** R2 explicitly asked for — and it
  tops carbon. We forecast with it / seasonal-naive; the ML-heavy models are reported as the honest negative result.
- Forecasting is a **supporting projection layer, not a contribution.** We forecast simply.
- The resource/geography **coupling lives in the account + the optimization** (incidence matrices, basin queues,
  routing) — exactly as R1 suggested (*"program those dependencies in the optimization formulation"*) — not in a
  joint or graph forecaster.

*Source: `runs/fresh_run_core_grid_2026-09-28/metrics/per_model_per_region.csv` → `results/forecast_simple_vs_complex.csv`.*

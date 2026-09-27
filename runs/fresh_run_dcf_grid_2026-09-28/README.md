# Fresh forecasting run — dcfootprint grid (2026-09-28)

The same models, windows and metrics as [`../fresh_run_core_grid_2026-09-28/`](../fresh_run_core_grid_2026-09-28/),
on the **pipeline's own Ember zones** instead of the Co-RE grid. Numbers: [`report/RUN_SUMMARY.md`](report/RUN_SUMMARY.md).
It supersedes the model comparison in `../fresh_run_2026-09-27/`, which had only seasonal naive and SARIMA fresh on
this grid (that folder stays as it is: frozen).

## The grid

`data/ember/dcfootprint_grid_series_dump.json`, written by `dcfootprint/experiments/export_dcf_grid_series.py` from
`io/ember.load_raw` — exactly the series the pipeline reads:

| | electricity | carbon |
|---|---|---|
| India states (Ember India, 2019 on) | 36 | 36 |
| US states + DC + Puerto Rico (Ember US, 2001 on) | 52 | 52 |
| EU-27 countries (Ember Europe, EU converted to GWh and CO2e g/kWh) | 27 | 27 |
| aggregates `IND|India Total`, `USA|US Total`, `EU Total` (scored as level `aggregate`) | 3 | 3 |

Series with fewer than 48 months are left out. All 66 account zones are present.

**Data rule (fixed from the raw file, before the run):** the Ember Europe file lists EU CO2 intensity as
`0.00 gCO2e per kWh` for Jan–Apr 2026 while it already publishes about 390 TWh of fossil generation for those
months: emissions not yet published. Trailing zero-intensity months with positive generation are dropped; the only
case is `EU Total` carbon (4 months), recorded in the dump's `_notes`. Zeros elsewhere (tiny grids such as Goa,
Lakshadweep, Luxembourg, Washington DC) are left as they are.

## Design

Identical to the Co-RE-grid run (see its README): holdout = last 12 observations + rolling origins Dec 2022/2023/2024,
horizon 12; models `seasonal_naive`, `sarima_dcf`, `sarima_core`, `timesfm_2p5`, `chronos_2`, `xlstm` (5 seeds);
80% intervals; all 10 metrics; levels region × all zones / account zones / aggregate. Differences: no cache check
(no Co-RE cache exists for this grid) and **no Nexus** (the Kaggle run covers the Co-RE grid only).

## Checks

- **Same series, same numbers on the account zones.** For all 66 account zones the series here are identical
  to the Co-RE grid's (same Ember data, same start and end months, same values; checked e.g. Texas 2001-01 to
  2025-12, Karnataka 2019-01 to 2025-11, Germany 2015-01 to 2025-12), so every model's account-zone scores equal
  the Co-RE-grid run's to the last digit. The two series files come from independent code paths (the Co-RE
  export and `io/ember.load_raw`), so this doubles as a reproduction check. What this grid adds is the zones
  outside the account (all 36 Indian states, US DC and Puerto Rico, the EU-27 rather than Co-RE's wider set of
  European countries) and the three aggregates.
- Failures (`metrics/failures.csv`) are only `sarima_dcf` fit-check rejections: 94 electricity, 5 carbon.

## Layout and reproduce

Same layout as the Co-RE-grid run. Reproduce:

```bash
.venv/Scripts/python.exe dcfootprint/experiments/export_dcf_grid_series.py          # writes the series dump
cd dcfootprint/experiments
SERIES_DUMP=../../data/ember/dcfootprint_grid_series_dump.json RUN_DIR=../../runs/fresh_run_dcf_grid_2026-09-28 \
  C:/Users/samik/AppData/Local/Programs/Python/Python311/python.exe forecast_run_core_grid.py run
```
The dump is derived data (git-ignored with the rest of `data/`); its SHA-256 is in `manifest/run_manifest.json`.

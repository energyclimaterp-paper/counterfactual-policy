# experiments/

Early gate experiments that de-risked the design before the pipeline was built.

## Early gate experiments (2026-09-26)

| Script | What it does |
|---|---|
| `gates_1_2_calibration_coverage.py` | G1: bottom-up India capacity vs CEEW (pass: 1.39 GW vs 1.5-1.8); G2: coverage (plausible) |
| `gate3_rq2_scarcity_reranking.py` | G3: does annual scarcity weighting re-rank hotspots? No: datacenters already sit in stressed basins |

The gate scripts predate the package and read from a hard-coded path (`R = ...` at the top); set it to your repository root before running them.

The current set of experiments (including the forecasting run) is on [`feat/us-eu`](https://github.com/energyclimaterp-paper/counterfactual-policy/tree/feat/us-eu/dcfootprint/experiments).

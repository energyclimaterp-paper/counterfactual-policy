# Gate experiments (de-risking, run 2026-09-26)

Standalone first-pass tests on data in hand (results in ../ARCHITECTURE.md §6.5).

- `gates_1_2_calibration_coverage.py` — G1 calibration (bottom-up vs CEEW) + G2 coverage uniformity.
- `gate3_rq2_scarcity_reranking.py` — G3: does scarcity-weighting re-rank basins/states beyond MC noise? (ANNUAL CF).

**Result:** G1 PASS (1.39 GW vs 1.5-1.8) · G2 PLAUSIBLE (61% capacity in 3 sites) · G3 = scarcity does NOT re-rank annually (DCs already in stressed basins).
**Pending:** seasonal (monthly-CF) version of G3; forecasting backtest.
Paths point to repo-root `data/` + `context/data/`; needs pandas/geopandas/shapely/scipy.

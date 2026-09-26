# Gate experiments (de-risking, run 2026-09-26)

Standalone first-pass tests on data in hand (results in ../ARCHITECTURE.md §6.5).

- `gates_1_2_calibration_coverage.py` — G1 calibration (bottom-up vs CEEW) + G2 coverage uniformity.
- `gate3_rq2_scarcity_reranking.py` — G3: does scarcity-weighting re-rank basins/states beyond MC noise? (ANNUAL CF).

- `gate3b_seasonal_reranking.py` — G3b: the SEASONAL version (12 monthly CFs + data-driven dry
  season + each facility's worst month), with fixes to G3 (see its docstring FIX-1..5): operational-only
  primary sample; corrected city geocoder; exact month columns; **null models** that test the reframe's
  explanation (null A = shuffle CF profiles among occupied basins; null B = random place in India,
  area-weighted, needs `data/gadm/gadm41_IND.gpkg`); direct capacity~scarcity premise check.
  Repo-relative paths (`--data-dir` to override); writes `results/gate3b/`.
  Run: `python dcfootprint/experiments/gate3b_seasonal_reranking.py` (from repo root).

**Result:** G1 PASS (1.39 GW vs 1.5-1.8) · G2 PLAUSIBLE (61% capacity in 3 sites) · G3 = scarcity does NOT re-rank annually (DCs already in stressed basins).
**Caveats found in review (2026-09-26):** G2's 61% and G3's sample include ALL statuses — the 61% is
24.8+19.9+16.0 over 12,534 MW of mostly announced/planned capacity (Palava = one announced 2.5 GW *park*
row). G3's "because DCs sit in stressed basins" explanation was not tested by the script (no
capacity~CF association, no null) — G3b tests it.
**Pending:** run G3b on real data (not yet run — the cloud session could not reach Zenodo); forecasting backtest.
G1/G2/G3 scripts hardcode a Windows path (`R = ...`); G3b does not. Needs pandas/geopandas/shapely/pyogrio/pyarrow/scipy/openpyxl.

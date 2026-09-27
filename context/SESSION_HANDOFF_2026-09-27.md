# SESSION HANDOFF — 2026-09-27 (read this first in a new session)

This file captures everything done in the session of 2026-09-26/27 on the `dcfootprint` pipeline, so a fresh
session can continue without the conversation. It complements `00_PROJECT_STATE.md` (project direction) and
`dcfootprint/ARCHITECTURE.md` (original design); where they disagree about **code state**, this file wins
(it describes the code as it is on branch `feat/us-eu` @ `2931a40`). Target architecture = the user's
`ARCHITECTURE_FINAL_2.md` (v2, 2026-09-26: Q1 siting, Q2 scorecard, Q3 routing; layers L0–L9).

---

## 0. The user's working rules (non-negotiable)

1. **Evidence before parameters.** A parameter/exclusion rule is fixed *before* a run from external evidence
   (citation, data audit, correctness check) and never retuned because the output looks wrong. If a result looks
   wrong: investigate code/data; fix only real bugs; otherwise the number stands.
2. **Verify, don't assume.** Check claims against files/data before acting (several of the user's own premises
   were wrong and were corrected with evidence: Nexus label, WUE=typo, colocation=matcher bug, ISO WUE ceiling).
3. **Check prior audits before flagging issues**: `diff/gat-sarima-nexus/docs/AUDIT_REPORT.md`,
   `testing_datasets/AWARE2.0_AUDIT.md`, `context/00_PROJECT_STATE.md`.
4. **Isolated, attributable commits**; each change verified (diff vs previous snapshot) before the next.
5. **Canonical snapshots are immutable** (`results/round3_final/`); new canonical runs get new dated folders.
6. Label honestly: Co-RE's cached "Nexus" column = **Chronos-2 in the Nexus slot**; the real multi-agent Nexus
   has never been benchmarked here.
7. Commits end with `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; push branches, never merge to
   `main` without the user.

---

## 1. Where everything lives

| What | Path |
|---|---|
| This repo (paper instrument) | `D:\3Gtech_paper - GNN\counterfactual-policy` — GitHub `energyclimaterp-paper/counterfactual-policy` |
| Package | `dcfootprint/src/dcfootprint/` |
| Co-RE repo (forecasting/GAT, read-only here) | `D:\3Gtech_paper - GNN\` (outer repo); models under `diff/gat-sarima-nexus/`, notebooks in `nbs/` |
| Raw data (gitignored) | `counterfactual-policy/data/` (see §6) — copies from `D:\3Gtech_paper - GNN\datasets-2026-energy\`, `testing_datasets\aware_data\`, downloads |
| Python for dcfootprint | `counterfactual-policy\.venv\Scripts\python.exe` (uv venv, Python 3.11; pandas, geopandas, pyogrio, pandera 0.33, pydantic, scipy, statsmodels, matplotlib, pypdf, pytest). **No torch.** |
| Python for Co-RE models | `C:\Users\samik\AppData\Local\Programs\Python\Python311\python.exe` (torch 2.13.0+cpu, chronos 2.3.1, timesfm, google-genai; no CUDA). Default `python` is 3.14 without pandas — never use it. |
| Ollama | running, v0.33.2, one model `gemma4:26b` (thinking model; ~8.6 tok/s on CPU; one call = 534 s) |
| Memory | `C:\Users\samik\.claude\projects\D--3Gtech-paper---GNN\memory\` |

Run commands (from `counterfactual-policy/`, bash):
```
PYTHONPATH=dcfootprint/src .venv/Scripts/python.exe -m dcfootprint.pipeline          # India, 14 stages
PYTHONPATH=dcfootprint/src .venv/Scripts/python.exe -m dcfootprint.regions US EU      # US + EU
PYTHONPATH=dcfootprint/src .venv/Scripts/python.exe -m pytest dcfootprint/tests -q     # 83 tests
```
Windows/bash gotcha: heredocs with `\\n` inside Python strings get mangled — write patch scripts with the
Write tool into the scratchpad and run them, or use the Edit tool.

---

## 2. Branches, commits, tags

| Ref | Meaning |
|---|---|
| `feat/pipeline-l0-l9` @ `32e4a46` | starting point (original L0–L9 pipeline, India only) |
| `fix/tier1-headline-numbers` | round 1–3 fixes; tag **`round3-final`** @ `27eb4f3` = canonical India run (`results/round3_final/`) |
| `feat/architecture-gaps` @ `aacd856` | price decomposition, validation, figures, L3→Q3 wiring |
| **`feat/us-eu` @ `2931a40`** (current, pushed) | fast-forward of gaps + US/EU + forecasting run |

Commit log since `32e4a46` (oldest first):
`7d7729d` headline fixes (state-month carbon, scope-1 ZLD, real oracle, siting grid) · `d857d0a` AWARE AMD
budgets, split siting tables, triangular MC · `0e14e7e` GADM vs GEM check (report only) · `071e689` Decision A
WUE band 0.7–2.5 · `ba28e74` Decision B hyperscale exclusion documented · `f80ff05` Decision C GADM state of
record · `27eb4f3` round-3 canonical snapshot · `385ae2d` Q3 price decomposition · `182f748` plumbing (L4
incidence to routing, levers in-memory, drop dead water.py) · `5dae340` pydantic + pandera everywhere ·
`9d61f4d` figures stage · `6554a55` pyproject fix · `aacd856` L3→Q3 pre-registered forecast · `f0858fe` US+EU ·
`2931a40` forecasting run.

Working tree note: `dcfootprint/results/*` loose files are modified by the latest India run (uncommitted, by
design — only canonical runs are committed).

---

## 3. Architecture as implemented (code map)

```
config/  parameters.yaml (validated by settings.py/pydantic) · legal_constraints.csv (effect+param per rule)
         policy_sources.csv (15-doc RAG manifest) · eu_member_state_2023.csv (EU Tables 13+24, rebuilt from PDF)
         region_config: India/US (facility tier), EU (country tier, account_year 2023)
L0  io/facilities.py (India workbook 194 rows, ATLAS city centroids)  io/us_facilities.py (Compute Atlas v1.34.0)
    io/ember.py load_raw(region): India/US/EU normalised (EU TWh->GWh, MtCO2e->ktCO2, 11 fuels -> 9, CO2e flagged)
    io/gem.py region_plants(region) + assign_state_of_record (GADM IND/USA; EU zone = country; 0-MW dropped)
    io/aware.py AMD_final x area = water remaining per basin-month   io/cea.py optional (file absent)
L1  geo/join.py (facility -> AWARE basin, basin_id = real AWARE Basin_ID = GPKG fid)
    geo/generation_basins.py (GEM plant -> basin; capacity-weighted CF per state/fuel/month -> scope-2 sEWIF)
L2  account/build.py facility_month_account(region) + grid_tables(zone, year, region) (cached)
    account/eu.py country_month_account() (measured energy + water input, PUE_EU 1.36)  calibrate.py
L3  project/forecast.py (national rolling backtest; Co-RE benchmark reader, "Nexus"->"Chronos-2 (Nexus slot)")
    project/hierarchy.py (one-step state CI: seasonal_naive | bottom_up | mint_wls_var | mint_wls_struct;
      pre-registered choice on 2022-2023 backtests; cached in data/ember; feeds Q3)
    project/recharge.py (G3P climatology = context only; basin_budgets(alpha) from AWARE AMD)
L4  geo/incidence.py A_zone/A_basin (used by routing via pipeline)            [no GNN]
L5  policy/gap.py (4-axis matrix all "No"; region_effects from legal_constraints.csv)  policy/rag_bridge.py (manifest only)
L6  routing/lyapunov.py (static, greedy, lyapunov, lyapunov_pf, offline LP oracle; solver switch)
    routing/agents.py price decomposition: GridAgent (posts CI), BasinAgent (queue price, settles queue),
      FacilityAgent (private unit cost, offers headroom), clear_market (bisection on demand price)
L7  counterfactual/levers.py (ZLD scope-1, efficiency, coastal[India cities only], disclosure; per-facility)
    decisions/scorecard.py (Q2)  decisions/siting.py (Q1: GEM cells, 4 criteria, minimax regret, legal screen,
      small grids <10 TWh ranked separately)
L8  uncertainty/monte_carlo.py (triangular, per-type bands, measured mode for EU, first-order Sobol, no-hydro variant)
L9  pipeline.py (India, 14 stages)  regions.py (US, EU)  viz/figures.py (5 India figures)
Validation  validation/schemas.py: Facilities, EmberZoneMonth, FuelShares, BasinMonthlyCF, GemPlants, GridWater,
            AwareRemaining, BasinBudget, FacilityMonthAccount, LeverSavings, RoutingComparison, Q2Scorecard,
            Q1Siting, ForecastCI
Tests       tests/: price decomposition (56), contracts (11), US/EU (12), forecast metrics (4) = 83
Experiments experiments/: gadm_gem_state_check, spotcheck_trace, round3_report, compare_results,
            extract_eu_tables, forecast_metrics, forecast_run, score_core_cached, assemble/summarize_forecast_run
```

### Status vs ARCHITECTURE_FINAL_2
| Layer | Status | Left |
|---|---|---|
| Config | done | — |
| L0 | mostly | CEA, CGWB, Open-Meteo/ERA5 |
| L1 | done | precise geocodes (India = city centroids) |
| L2 | done ×3 regions | India hyperscaler MW; EU per-country PUE |
| L2.5 | done | — |
| L3 | partial | port SARIMA validity checks to hierarchy.py; MinT unstable on US; real Nexus; 2030/2050 scenarios |
| L4 | partial | GNN tested extra (needs a defined target) |
| L5 | partial | live RAG (original project `C:/Users/gauri/Projects/rag` not on this machine) + eval vs gold |
| L6 | done India+US | EU (no sites); hourly |
| L7 | done ×3 | Q1 2030/2050 scenarios; coastal lever for US/EU |
| L8 | done | total-effect Sobol; rank stability |
| L9 | partial | US/EU maps; round-4 canonical snapshot |

---

## 4. Methods and decisions (with the evidence that fixed them)

**Account (L2):** E_IT = MW·util·hours; E_grid = E_IT·PUE (by facility type); carbon = E_grid·CI(state, month)
(Ember, generation-based — R2 caveat); scope-1 W = WUE·E_IT, scarcity at facility basin CF(m); scope-2 W =
EWIF(state,m)·E_grid, scarcity at the **generation basins** of the state's GEM plants (capacity-weighted per fuel).
- WUE: default 1.9, MC band **0.7–2.5** (Decision A: Equinix blog "up to 2.5 L/kWh with evaporative cooling";
  ISO/IEC 30134-9 sets **no** limit; replaced Li et al.'s 9 = cross-site/season range). Triangular, mode 1.9.
- Hydro EWIF 17,000 L/MWh kept in primary; no-hydro variant reported.
- India: 10 hyperscale cloud regions excluded (no public MW; Decision B). 71 facilities in account.
- GEM plant state = GADM from coordinates (Decision C); overrides: Vijaypura (Adani) II -> Karnataka,
  Rawan Cement -> Chhattisgarh (GEM coordinate errors), Gujarat (Adani) IV -> Gujarat; Lower Sileru ambiguous
  (AP | Telangana, excluded from single-state views). ≥2-plants rule dropped.
- US capacity basis (Compute Atlas has no IT/facility field): 26/28 IT-stating records record exactly the IT
  figure -> classify per record: it (26) / facility (17, ÷PUE) / unspecified (192, treated as IT).
- EU: measured EDC and water input (withdrawal, flagged); EU-average PUE 1.36 (Table 23); AWARE country
  non-agricultural CFs; CO2e.

**Q3 routing (L6):** monthly, 30% flexible load, budget = **α·max(AWARE AMD,0)·basin area** (water left after human
use + environmental flows; α=1 headline, sweep 1…1e-4); queues on scope-1 via incidence; queue price scaled by
the basin's own DC draw; oracle = full-year LP at Lyapunov's per-basin queue peaks; controllers use the
pre-registered one-step CI forecast (India bottom-up SARIMA, US seasonal naive). Solver = price decomposition,
proven equal to the central LP (56 tests, ≤1.7e-14).

**Q1 siting:** candidate cells = state×basin with GEM plants + occupied cells; criteria new-facility scarcity
water, carbon, marginal basin overdraft ΔD_b, grid fossil share; Dirichlet weights, minimax regret; small grids
(<10 TWh/yr) separate. **Decided but not implemented:** 2030/2050 scenarios with Aqueduct **0–5 scores**
(technical note Kuzma et al. 2023 p.11: raw ws capped to [0,1]; p.10: future bias-corrected to baseline;
PDF at `C:\Users\samik\Downloads\wri-aug23.pdf`).

**L3 forecast choice (pre-registered):** lowest mean one-step CI RMSE over DC states in 2022+2023; must beat
seasonal naive. India: seasonal_naive 44.69, bottom_up **40.07** (chosen), mint_var 40.13, mint_struct 43.96;
2024 OOS 44.94/38.75/39.10/37.49. US: seasonal naive chosen (41.36 vs bottom_up 54.27; MinT blew up).

---

## 5. Results

**India** (canonical `results/round3_final/`, tag `round3-final`; 71 facilities, 2024):
carbon 3.63 Mt; physical 24.8 Mm³ (scope-1 29%); scarcity **846.6 M m³-eq** (scope-1 40%); MC 90% 573–1,074 M,
util dominates (Sobol 0.65). Tamil Nadu 303 M on 207 MW vs Maharashtra 147 M on 368 MW. Levers: ZLD 36.9% ≈
efficiency 36.6% (+18.8% carbon), coastal 17.3%. Q2: 16 harm-flagged. Q1: top 5 Karnataka basins (47731 first;
#2 48720 = single GEM plant). Q3: −21.7% scarcity water, **+1.4% carbon**; 34/96 basin-months have no water
left; fixed-load overdraft floor 545,700 m³ = what Lyapunov reaches; oracle gap 0.4%. Policy gap: 0/4 axes
mandated anywhere. (After L3 wiring, Q3 moved ≤0.02 pp; not yet re-snapshotted.)

**US** (Compute Atlas, 235 facilities, 2024; `results/us/`, not canonical): 16.0 Mt; 196 Mm³; scarcity
2.51 bn m³-eq; 51.9 TWh = 30% of LBNL 176 TWh; Arizona 952 M on 486 MW vs Oregon 121 M on 1,017 MW. Levers:
efficiency 31.4% (+12.9% carbon), ZLD 29.3%. Q2 53 flagged. Q1 Washington basins. **Q3: −29% water AND −10%
carbon** (routing closes both gaps in the US, unlike India).

**EU** (21 reporting Member States, 2023; `results/eu/`): 3.35 Mt CO2e; 37.9 Mm³; scarcity 137 M m³-eq; Spain
leads water, Germany carbon; ZLD 16.4%; Q1 Sweden basins; Q3 not run (no sites); MC hydro-dominated (0.85).

**Forecasting run** `runs/fresh_run_2026-09-27/` (`report/RUN_SUMMARY.md`): 10 metrics (MAE, RMSE, WMAPE,
Bias, MASE, sMAPE, MedAE, Pearson, PICP, CRPS). Fresh seasonal_naive + SARIMA (dcfootprint, 3 rolling origins,
h=1–12, India/US/EU zones+aggregates) with PICP/CRPS; Co-RE cache rescored (xlstm, timesfm-2.5, chronos-2,
sarima_core; point only; reproduces Co-RE RMSE 856/856). 76/~700 SARIMA fits invalid and excluded
(non-converged/degenerate/LU). Real Nexus **not run** (534 s per gemma4:26b call).

---

## 6. Data inventory (`counterfactual-policy/data/`, gitignored)
ember/{india,us,europe}_monthly_full_release_long_format.csv (+ forecast caches `ci_*_v2-stationary.*`) ·
atlas/datacenters.parquet · aware/AWARE20_Native_CFs_geospatial.gpkg, AWARE20_Intermediate_Variables.xlsx,
AWARE20_Countries_and_Regions.xlsx · g3p/G3P_v1.12_tws_rivbas.csv · gem/Global-Integrated-Power-March-2026-II.xlsx
(+ parquet caches v2/v4) · gadm/gadm41_IND.gpkg, gadm41_USA.gpkg · compute_atlas/facilities_v1.34.0.json ·
epoch/data_centers.csv (unused so far) · eu_eed/EU_DC_assessment_first_technical_report_2025-07.pdf.
Missing: CEA v22, CGWB, ERA5. Aqueduct GDB is read from `../datasets-2026-energy/water risk/...`.

---

## 7. Bugs found and fixed this session (don't reintroduce)
ZLD applied to scope-2 · national-constant carbon · oracle == greedy · R̂ coupled to DC water · AWARE basin_id =
row index (use GPKG fid) · Lyapunov queue price vanishing at α=1 · MC unused inference draw · unserved_mwh float
residue · SARIMA `enforce_stationarity=False` explosions (1e88) · SARIMA non-convergence (Germany 225,000 GWh) ·
degenerate "converged" fits (Texas = 0) · scorecard groupby dropping NaN basin (EU scored 0) · EU 0-MW GEM plants ·
GEM compound state "Arizona and Nevada" · PDF parser TOTAL row from Table 14 · figures path for live runs.

---

## 8. Next actions (priority order)
1. Port SARIMA validity checks (converged, no unit-boundary coefficient, finite SE, keep NaN) into
   `project/hierarchy.py`; bump `CACHE_VERSION`; rebuild India/US Q3 forecast caches; attribute changes.
2. Diagnose MinT instability on US data (likely near-zero error-variance weights).
3. Implement Q1 2030/2050 scenarios with Aqueduct 0–5 scores (baseline `bws_score` vs `ws_x_s`, bau/opt/pes ×
   2030/2050) inside minimax regret; carbon has no scenario (no sourced CI path).
4. US/EU maps in `viz/figures.py`; Epoch AI cross-check of big US AI campuses.
5. Round-4 canonical run (India+US+EU): two clean runs, determinism diff, spot checks, attribution vs round 3,
   snapshot `results/round4_final/`, tag `round4-final`.
6. Re-run fresh SARIMA on the Co-RE grain for a like-for-like model comparison.
7. **User decisions pending:** where to run real Nexus (GPU/cloud or smaller non-thinking model); legal RAG
   (bring original project or rebuild with Ollama + the 15 PDFs); GNN target or formal drop; data sourcing
   (India hyperscaler MW, US/EU water series, CGWB).
8. Paper: reframe RQs (RQ2 strong; RQ4 two-sided: India trade-off vs US co-benefit; RQ3/RQ6 out of scope);
   merge `feat/us-eu` after round 4 (only with the user).

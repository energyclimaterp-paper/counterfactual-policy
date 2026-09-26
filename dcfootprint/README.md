# dcfootprint — architecture & build plan

The reproducible **instrument** behind the paper: an open, sub-national, inference-attributed
**joint carbon + scarcity-weighted-water account** of AI datacenters (India deep · US solid · EU light),
and a **counterfactual policy engine** that quantifies what water/carbon policy levers would save.
(Research direction & rationale: `../context/RESEARCH_GAPS.md`; data: `../context/DATA.md`.)

It produces the paper's four products: **① finding** (which lever pays) · **② dataset** (the account) ·
**③ method** (the counterfactual) · **④ instrument** (this reproducible package).

## Design principles
1. **A layered pipeline of library-backed modules — not ad-hoc scripts, not agents.** Each step is a pure,
   testable function; parameters live in `config/`, never hardcoded; the whole thing runs as one DAG.
2. **Granularity is a contract, not a hope.** The GAT project died by forcing region data to a facility task.
   Here every layer boundary is guarded by a **pandera** schema (`validation/schemas.py`): the atomic unit is
   the **facility-month**; each resource keeps its native partition; the facility is the join key; you
   aggregate UP, never down-force. Violations are test failures.
3. **Reproducible by construction** (this is contribution ④): `snakemake -c4 all` rebuilds everything;
   config-driven; open data + open code.

## The accounting equation (L2) — from the lit review (Guidi/Harvard, Li "Thirsty", Siddik)
Per facility *f*, month *m*, grid-zone *z(f)*, basin *b(f)*:
```
E_IT    = capacity_MW · utilisation · hours(m)
E_grid  = E_IT · PUE
Carbon  = E_grid · CI(z, m)                       # CI = Ember grid carbon intensity
W_onsite= WUE · E_IT                              # scope-1
EWIF    = Σ_fuel share_fuel(z,m) · macknick[fuel] # scope-2 intensity (L/MWh)
W_grid  = EWIF(z,m) · E_grid                       # scope-2
W_phys  = W_onsite + W_grid                        # PHYSICAL litres — reported first
W_scarce= W_phys · AWARE_CF(b, month)             # scarcity-weighted — SEPARATE column, never blended
```
Levers (L7): a **lever = a parameter transform** (coastal→WUE↓; ZLD→W_onsite·(1−recycle), scope-1 only;
efficiency→PUE/WUE cap, with the energy↑/water↓ trade-off), re-run the account, report Δ vs baseline → rank.

## Layers → modules → libraries
| Layer (ARCHITECTURE v2) | Module | Libraries |
|---|---|---|
| config | `config/parameters.yaml`, `datasets.yaml`, `legal_constraints.csv` | PyYAML |
| L0 ingest | `io/` (facilities, ember, gem, cea [optional cross-check]) | pandas, pyarrow, openpyxl |
| L1 geo linkage | `geo/join.py` (facility→AWARE basin), `geo/generation_basins.py` (GEM plant→basin, scope-2 CF) | geopandas, shapely, pyogrio |
| **contracts** | `validation/schemas.py` | **pandera** |
| L2 account | `account/` (energy, carbon = E_grid·CI(state,m), water, build, calibrate) | pandas, numpy |
| L3 forecast + R̂ | `project/forecast.py` (rolling backtest), `project/recharge.py` (G3P season, basin budgets) | statsmodels |
| L4 spatial coupling | `geo/incidence.py` (A_zone, A_basin — used by routing) | pandas |
| L5 policy | `policy/gap.py` (matrix + constraint effects), `policy/rag_bridge.py` | pandas |
| L6 routing (Q3) | `routing/lyapunov.py` (static · greedy · lyapunov · perfect-foresight · offline LP oracle) | scipy (HiGHS) |
| L7 decisions | `counterfactual/levers.py` (ranked levers), `decisions/scorecard.py` (Q2), `decisions/siting.py` (Q1) | numpy |
| L8 uncertainty | `uncertainty/monte_carlo.py` (per-type bands, first-order Sobol) | numpy |
| L9 orchestration | `pipeline.py` (tested entrypoint), `workflow/Snakefile` (wrapper) | snakemake |
| viz/maps | `viz/` | matplotlib, geopandas, folium |

## Execution — one spine + parallel tracks (see `workflow/Snakefile`)
```
SPINE:   facilities → geo_join → account (L2) → levers (L7)  → finding
TRACK A: load_ember + load_aware + macknick        (data; land before account)
TRACK B: regulatory_gap (L5)                        (policy; land before counterfactual)
TRACK C: forecast (L4, Ceiling)                     (independent; integrate after account)
CROSS:   uncertainty (L6) after account;  release (L7)
```
`snakemake -c4 floor` = India-only Floor (submittable). `snakemake -c4 all` = full Ceiling.

## Repo layout
```
dcfootprint/
  pyproject.toml          # dependencies (libraries per layer)
  config/
    parameters.yaml       # PUE, WUE, EWIF crosswalk, inference share, LEVERS — every assumption
    datasets.yaml         # dataset registry: path · granularity · join_key · role (mirrors DATA.md D/E/F)
  src/dcfootprint/
    io/ geo/ account/ counterfactual/ forecast/ policy/ uncertainty/ validation/ viz/
  workflow/Snakefile      # the DAG
  tests/                  # pytest — schema + equation unit tests
  outputs/                # (gitignored) account, savings, gap matrix, projections
```

## Build order & status
- **Scaffolded now:** package structure, `pyproject.toml`, both configs, `validation/schemas.py` (the contracts),
  `account/build.py` (the account equations, inline), `workflow/Snakefile` (the DAG).
- **Next (in spine order):** `io/facilities.py` (merge our-list ⋈ ATLAS coords ⋈ CEA plant data — the L0 bottleneck)
  → `geo/join.py` (zone + basin assignment) → `account/{energy,carbon}.py` → `counterfactual/levers.py`.
  Parallel: `policy/gap.py`, `io/ember.py`, `io/aware.py`.
- **Floor first:** India only, 1–2 levers → a complete paper; then extend to US/EU + all levers + forecast (Ceiling).

## The four granularity decisions locked into config (DATA.md §E3/F)
US carbon = Ember-state (eGRID = cross-check) · EU = country-only (light) · India carbon = Ember-state
generation-proxy (water carries India novelty) · scarcity = AWARE gpkg only (Aqueduct ≠ joinable key).

## Data layout expected at the repo root (`data/`, gitignored)
```
data/ember/india_monthly_full_release_long_format.csv
data/atlas/datacenters.parquet
data/aware/AWARE20_Native_CFs_geospatial.gpkg
data/g3p/G3P_v1.12_tws_rivbas.csv
data/gem/Global-Integrated-Power-March-2026-II.xlsx      (India subset cached as parquet on first run)
data/cea/CEA_Database_V22.xlsx                           (optional: cross-check only)
```
The Co-RE forecast benchmark is read from `$DCF_GAT_DIR`, else `gat-based-forecasting/diff/gat-sarima-nexus`,
else `../diff/gat-sarima-nexus`. Its "Nexus" rows are **Chronos-2 in the Nexus slot** and are reported under that label.

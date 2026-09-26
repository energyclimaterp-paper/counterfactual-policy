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
Counterfactual (L3): a **lever = a parameter transform** (coastal→WUE↓; ZLD→W_phys·(1−recycle);
efficiency→PUE/WUE cap, with the energy↑/water↓ trade-off), re-run the account, report Δ vs baseline → rank.

## Layers → modules → libraries
| Layer | Module | Libraries |
|---|---|---|
| config | `config/*.yaml` | pydantic, PyYAML |
| L0 load | `io/` (ember, cea, egrid, aware, macknick, facilities, cgwb, gem) | pandas, pyarrow, openpyxl |
| L1 geo-join | `geo/` (facility→state via GADM; facility→basin via AWARE point-in-polygon) | geopandas, shapely, pyogrio |
| **contracts** | `validation/schemas.py` | **pandera** (+ pint for units) |
| L2 account | `account/` (energy, carbon, water) | pandas, numpy |
| L3 counterfactual | `counterfactual/levers.py` | pandas |
| L4 forecast (Ceiling) | `forecast/` | statsmodels, sktime, [chronos-forecasting] |
| L5 policy | `policy/gap.py` | pandas |
| L6 uncertainty | `uncertainty/mc.py` | numpy, scipy, SALib |
| L7 orchestration | `workflow/Snakefile` | **snakemake** |
| viz/maps | `viz/` | matplotlib, geopandas, folium |

## Execution — one spine + parallel tracks (see `workflow/Snakefile`)
```
SPINE:   facilities → geo_join → account (L2) → counterfactual (L3)  → finding
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
  `account/water.py` (reference equation), `workflow/Snakefile` (the DAG).
- **Next (in spine order):** `io/facilities.py` (merge our-list ⋈ ATLAS coords ⋈ CEA plant data — the L0 bottleneck)
  → `geo/join.py` (zone + basin assignment) → `account/{energy,carbon}.py` → `counterfactual/levers.py`.
  Parallel: `policy/gap.py`, `io/ember.py`, `io/aware.py`.
- **Floor first:** India only, 1–2 levers → a complete paper; then extend to US/EU + all levers + forecast (Ceiling).

## The four granularity decisions locked into config (DATA.md §E3/F)
US carbon = Ember-state (eGRID = cross-check) · EU = country-only (light) · India carbon = Ember-state
generation-proxy (water carries India novelty) · scarcity = AWARE gpkg only (Aqueduct ≠ joinable key).

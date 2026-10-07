# Carbon and water footprint of AI datacenters: India, US, EU

An open, reproducible pipeline that accounts for the **carbon and scarcity-weighted water** of AI datacenters,
facility by facility and month by month, and uses that account to answer three policy questions. It is the
research instrument behind a paper for the Elsevier *Energy and Climate Change* special issue
"Computing and Digitalization through a Multi-Disciplinary Lens".

> **You are on `feat/us-eu`, the current branch.** It has everything: India, US and EU. The other branches
> are earlier stages of the same work (see [Branches](#branches)).

## Start here

| If you want to... | Read |
|---|---|
| understand the project in 5 minutes | this file |
| understand the results | [`dcfootprint/results/README.md`](dcfootprint/results/README.md) (one page), then [`cross_region_summary.md`](dcfootprint/results/cross_region_summary.md) |
| know what is built, the decisions and the current state | [`context/SESSION_HANDOFF_2026-10-04.md`](context/SESSION_HANDOFF_2026-10-04.md) (latest), [`context/SESSION_HANDOFF_2026-09-27.md`](context/SESSION_HANDOFF_2026-09-27.md) (code map) |
| know why the project is shaped this way | [`context/00_PROJECT_STATE.md`](context/00_PROJECT_STATE.md) |
| find your way around the code | [`dcfootprint/README.md`](dcfootprint/README.md) |
| quote canonical India numbers | [`dcfootprint/results/round3_final/`](dcfootprint/results/round3_final/) (tag `round3-final`) |
| see the forecasting benchmark | [`runs/fresh_run_core_grid_2026-09-28/report/RUN_SUMMARY.md`](runs/fresh_run_core_grid_2026-09-28/report/RUN_SUMMARY.md) (every model, Co-RE grid) and [`runs/fresh_run_dcf_grid_2026-09-28/`](runs/fresh_run_dcf_grid_2026-09-28/) (pipeline zones) |
| know where each dataset comes from | [`context/DATA.md`](context/DATA.md) |

## What it answers

The pipeline first builds an **account**: for every datacenter and month, its energy, carbon, physical water
and scarcity-weighted water (on-site cooling and the power plants that supply it). On that account it answers:

| Question | In one line | Output |
|---|---|---|
| **Q1 Siting** | Where should a new datacenter go? Regions ranked by minimax regret, with a legal screen and 2030/2050 water scenarios | `q1_siting*.csv` |
| **Q2 Scorecard** | Which existing facilities do the most harm, and which lever fits each? | `q2_scorecard.csv` |
| **Q3 Routing** | How much would shifting flexible load between sites save, month by month? | `routing_*.csv` |

Plus: **levers** (what zero-liquid-discharge, efficiency standards, coastal cooling would save), a
**regulatory gap map** across the three jurisdictions, and **uncertainty** bands on every headline number.

| Region | Unit | Facilities | Year |
|---|---|---|---|
| India | facility | 71 (hand-built open list) | 2024 |
| US | facility | 235 (Compute Atlas) | 2024 |
| EU | country | 21 reporting Member States (EU Energy Efficiency Directive data) | 2023 |

## Quick start

```bash
# 1. environment (Python 3.11)
uv venv --python 3.11 .venv
uv pip install --python .venv/Scripts/python.exe -r dcfootprint/pyproject.toml --extra dev

# 2. data: put the raw files in data/ (not in git; list below, sources in context/DATA.md)

# 3. run (from the repository root)
PYTHONPATH=dcfootprint/src .venv/Scripts/python.exe -m dcfootprint.pipeline        # India -> dcfootprint/results/
PYTHONPATH=dcfootprint/src .venv/Scripts/python.exe -m dcfootprint.regions US EU   # US, EU -> dcfootprint/results/us, eu/
PYTHONPATH=dcfootprint/src .venv/Scripts/python.exe -m pytest dcfootprint/tests -q # tests
```
On macOS/Linux use `.venv/bin/python`. Each run prints a stage-by-stage status table; every stage boundary is
checked by a data contract, and a failed contract fails that stage.

### Data expected in `data/` (git-ignored)
```
data/
├── ember/       india_, us_, europe_monthly_full_release_long_format.csv   grid generation + emissions, monthly
├── gem/         Global-Integrated-Power-March-2026-II.xlsx                 power plants (Global Energy Monitor)
├── aware/       AWARE20_Native_CFs_geospatial.gpkg,                        water scarcity factors per basin
│                AWARE20_Intermediate_Variables.xlsx, AWARE20_Countries_and_Regions.xlsx
├── aqueduct/    Aq40_Y2023D07M05.gdb                                        WRI Aqueduct 4.0 (Q1 2030/2050 scenarios)
├── gadm/        gadm41_IND.gpkg, gadm41_USA.gpkg                           state boundaries
├── compute_atlas/facilities_v1.34.0.json                                   US datacenters
├── atlas/       datacenters.parquet                                        India coordinates (gap-filler)
├── g3p/         G3P_v1.12_tws_rivbas.csv                                   groundwater context
├── eu_eed/      EU_DC_assessment_first_technical_report_2025-07.pdf        source of the EU table in config/
└── epoch/       data_centers.csv                                           optional cross-check
```
Derived caches (forecasts, parquet copies) are written next to these files and rebuilt automatically.

## Branches

The branches are one line of work, each building on the previous one. Newest first:

| Branch | What it adds | State |
|---|---|---|
| **`feat/us-eu`** | US and EU regions, forecasting run, SARIMA fit checks, Q1 2030/2050 scenarios, US/EU maps | **current** |
| `feat/architecture-gaps` | price-decomposition routing solver, pydantic + pandera contracts, figures, forecast feeding Q3 | included above |
| `fix/tier1-headline-numbers` | fixes to the headline numbers; canonical India run (tag `round3-final`) | included above |
| `feat/pipeline-l0-l9` | first complete India pipeline, layers L0 to L9 | included above |
| `main` | design, research record and empty package scaffold | superseded |
| `claude/modest-euler-714bjp` | side branch off the scaffold: seasonal re-ranking experiment (gate 3b) | not merged |

Nothing is merged into `main` yet; it will be after the round-4 canonical run.

## File structure

<!-- TREE:start -->
```
├── context/                                   # research record (why the project looks the way it does)
│   ├── data/
│   │   ├── india_dc_facilities.psv            # same list, plain text
│   │   └── India_DC_Facilities_v0.xlsx        # the open India datacenter list (194 rows) - a contribution
│   ├── archive/                               # superseded: legacy S0-S11 architecture + old diagrams
│   ├── 00_PROJECT_STATE.md                    # direction, locked decisions, RQs (some pre-v2 sections)
│   ├── CFP_RECORD.md                          # the journal call for papers
│   ├── COMMIT_HASH_MAP.md                     # old -> new commit hashes (history rewrite 2026-09-27)
│   ├── CORE_REVIEWS_AND_LESSONS.md            # NeurIPS Co-RE reviews, verbatim + lessons for this paper
│   ├── DATA.md                                # every dataset: source, granularity, join key, what is on disk
│   ├── GNN_AUTOPSY.md                         # why the earlier GNN approach was dropped
│   ├── lit_review_coding_sheet.xlsx           # coded literature (84 papers)
│   ├── LIT_REVIEW_VERIFIED.md                 # verified literature review
│   ├── PIPELINE_IMPROVEMENTS.md               # prioritised backlog (what to do next, and why)
│   ├── POLICY_DEEP_DIVE.md                    # regulation across India / US / EU
│   ├── RESEARCH_GAPS.md                       # gap analysis behind the contributions (some pre-v2 sections)
│   ├── SESSION_HANDOFF_2026-09-27.md          # code as built, decisions + evidence, results
│   └── SESSION_HANDOFF_2026-10-04.md          # latest state: policy/RAG/forecast work, round 4, what's left
├── dcfootprint/                               # the pipeline: Python package and its config
│   ├── config/                                # every assumption lives here, never in code
│   │   ├── datasets.yaml                      # dataset registry: path, granularity, join key, role
│   │   ├── eu_member_state_2023.csv           # EU per-country energy/water, rebuilt from the EED report PDF
│   │   ├── legal_constraints.csv              # legal rules and their effect on Q1/Q3 (bans, ZLD, PUE caps)
│   │   ├── parameters.yaml                    # every numeric assumption (PUE, WUE, water intensities, levers, ...)
│   │   └── policy_sources.csv                 # the 15-document policy corpus (legal RAG manifest)
│   ├── docs/
│   │   └── architecture_flow.svg              # layer flow diagram
│   ├── experiments/                           # scripts outside the pipeline (see its README)
│   │   ├── README.md                          # what each script does
│   │   └── *.py                               # 15 files
│   ├── results/                               # outputs + the curated synthesis (start at results/README.md)
│   │   ├── README.md                          # READ FIRST: results overview, every RQ -> headline -> trust
│   │   ├── cross_region_summary.md            # three-region synthesis, numbers mapped to RQs
│   │   ├── rag_axis_audit.md .. q2_equity_groundwater.md  # standalone exhibits (RAG, forecast, equity)
│   │   ├── round3_final/                      # FROZEN canonical India snapshot, tag round3-final (quote these)
│   │   ├── round2_final/                      # superseded round-2 snapshot (feeds round3_report.py)
│   │   ├── us/, eu/                           # latest US / EU region outputs
│   │   ├── RESULTS.md, RESULTS_FULL.md        # auto-written latest India run summary / full report
│   │   └── *.csv, *.json                      # latest India run outputs (regenerated)
│   ├── src/
│   │   └── dcfootprint/
│   │       ├── account/                       # L2 account
│   │       │   ├── build.py                   # facility-month carbon + water account
│   │       │   ├── calibrate.py               # L2.5 check vs CEEW (India) / LBNL (US)
│   │       │   ├── carbon.py                  # carbon = grid energy x state-month CI
│   │       │   ├── energy.py                  # IT and grid energy
│   │       │   └── eu.py                      # EU country-month account (measured data)
│   │       ├── counterfactual/                # L7 levers
│   │       │   └── levers.py                  # ZLD, efficiency, coastal, disclosure: savings per lever
│   │       ├── decisions/                     # L7 decisions
│   │       │   ├── scorecard.py               # Q2 harm scorecard per facility
│   │       │   └── siting.py                  # Q1 siting: regions ranked by minimax regret
│   │       ├── geo/                           # L1 geo linkage + L4 spatial
│   │       │   ├── generation_basins.py       # power plant -> basin; scope-2 scarcity factor
│   │       │   ├── incidence.py               # L4 facility-zone / facility-basin matrices
│   │       │   └── join.py                    # facility -> AWARE basin (basin_id = GPKG fid)
│   │       ├── io/                            # L0 ingest
│   │       │   ├── aware.py                   # AWARE 2.0 water remaining per basin-month
│   │       │   ├── cea.py                     # CEA plant data (optional; file not on disk)
│   │       │   ├── ember.py                   # Ember monthly generation and emissions
│   │       │   ├── facilities.py              # India facility list + coordinates
│   │       │   ├── gem.py                     # GEM power plants, GADM state of record
│   │       │   └── us_facilities.py           # US facility spine (Compute Atlas)
│   │       ├── policy/                        # L5 legal
│   │       │   ├── gap.py                     # 4-axis regulatory gap matrix
│   │       │   └── rag_bridge.py              # policy corpus manifest (live RAG not wired)
│   │       ├── project/                       # L3 forecast + projections
│   │       │   ├── forecast.py                # national CI rolling backtest; Co-RE benchmark reader
│   │       │   ├── hierarchy.py               # one-step state CI for Q3; pre-registered method choice
│   │       │   ├── recharge.py                # basin water budgets (AWARE) + G3P context
│   │       │   └── scarcity_future.py         # Aqueduct 2030/2050 water-stress scores per basin
│   │       ├── routing/                       # L6 Q3 routing
│   │       │   ├── agents.py                  # price decomposition solver (grid, basin, facility agents)
│   │       │   └── lyapunov.py                # static / greedy / Lyapunov / LP oracle policies
│   │       ├── uncertainty/                   # L8
│   │       │   └── monte_carlo.py             # Monte Carlo bands + first-order Sobol
│   │       ├── validation/
│   │       │   └── schemas.py                 # pandera data contracts
│   │       ├── viz/                           # L9
│   │       │   └── figures.py                 # figures and maps
│   │       ├── pipeline.py                    # RUN INDIA: all layers L0-L9, writes results/
│   │       ├── regions.py                     # RUN US / EU: writes results/us, results/eu
│   │       └── settings.py                    # loads + validates parameters.yaml (pydantic)
│   ├── tests/                                 # pytest suite
│   │   └── test_*.py                          # 6 files
│   ├── workflow/
│   │   └── Snakefile                          # Snakemake workflow
│   ├── .gitignore
│   ├── ARCHITECTURE.md                        # design, contributions (section 7), risk register
│   ├── pyproject.toml                         # dependencies
│   └── README.md                              # package guide
├── runs/
│   ├── fresh_run_2026-09-27/                  # FROZEN first forecasting run (fresh naive + SARIMA, rescored Co-RE cache)
│   ├── fresh_run_core_grid_2026-09-28/        # every model fresh on the Co-RE grid; LLM Nexus to be added; see its README
│   └── fresh_run_dcf_grid_2026-09-28/         # FROZEN: every model fresh on the pipeline's own Ember zones; see its README
├── .gitignore                                 # data/, outputs/ and caches are not versioned
└── README.md                                  # this file
```
<!-- TREE:end -->

Folders marked FROZEN are canonical snapshots: they are never edited, and a new canonical run gets a new
dated folder.

## Status

All layers run end to end for India and the US, and for the EU at country level (no routing: no site
locations); the test suite passes. **Round 4 (2026-10-06): all three regions re-run clean and reproduce the
canonical results — India identical to `round3-final` to machine precision, US data byte-identical, EU
complete.** Still open: real multi-agent Nexus forecasting, the live legal retrieval (RAG), a GNN target, a
2030/2050 carbon path, and India consumption-based carbon (Electricity Maps). Backlog in priority order:
[`context/PIPELINE_IMPROVEMENTS.md`](context/PIPELINE_IMPROVEMENTS.md); current state:
[`context/SESSION_HANDOFF_2026-10-04.md`](context/SESSION_HANDOFF_2026-10-04.md).

## Built with

Python 3.11 · pandas · geopandas / shapely / pyogrio (spatial joins) · pandera (data contracts) · pydantic
(config validation) · statsmodels (SARIMA) · scipy / HiGHS (routing LP) · matplotlib (figures) · pytest.
Deterministic by design. `pyproject.toml` also lists pint, sktime, SALib, folium and snakemake, which the
code does not use yet; `workflow/Snakefile` only wraps the Python runner.

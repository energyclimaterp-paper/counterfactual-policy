# Carbon and water footprint of AI datacenters: India, US, EU

> **Branch `feat/architecture-gaps`: architecture gaps closed (India only) (2026-09-27).** This is an earlier stage of the project, kept for history.
> **The current version is [`feat/us-eu`](https://github.com/energyclimaterp-paper/counterfactual-policy/tree/feat/us-eu)**, which contains everything here plus later work.

An open, reproducible pipeline that accounts for the **carbon and scarcity-weighted water** of AI datacenters,
facility by facility and month by month, and uses it to answer three policy questions: **Q1** where to site a new
datacenter, **Q2** which existing facilities do the most harm, **Q3** how much shifting flexible load between sites
would save. On this branch it covers **India** only.

## What this branch adds
- Q3 routing solved by price decomposition (grid, basin and facility agents), proven equal to the central LP
- pydantic validation of `parameters.yaml` and pandera contracts at every layer boundary
- paper figures as a pipeline stage (`viz/figures.py`)
- a one-step grid-CI forecast, chosen by a pre-registered rule, feeding the Q3 controllers (`project/hierarchy.py`)
- a first test suite (`dcfootprint/tests/`)

Canonical India numbers are in `dcfootprint/results/round3_final/` (tag `round3-final`).

## Start here

| If you want to... | Read |
|---|---|
| why the project is shaped this way | [`context/00_PROJECT_STATE.md`](context/00_PROJECT_STATE.md) |
| the code on this branch | [`dcfootprint/README.md`](dcfootprint/README.md) |
| where each dataset comes from | [`context/DATA.md`](context/DATA.md) |
| the design | [`dcfootprint/ARCHITECTURE.md`](dcfootprint/ARCHITECTURE.md) |

## Run it

```bash
uv venv --python 3.11 .venv
uv pip install --python .venv/Scripts/python.exe -r dcfootprint/pyproject.toml --extra dev
PYTHONPATH=dcfootprint/src .venv/Scripts/python.exe -m dcfootprint.pipeline      # India -> dcfootprint/results/
PYTHONPATH=dcfootprint/src .venv/Scripts/python.exe -m pytest dcfootprint/tests -q
```
Raw data goes in `data/` (not in git); every source is listed in [`context/DATA.md`](context/DATA.md).

## Branches

| Branch | What it adds | State |
|---|---|---|
| `feat/us-eu` | US and EU regions, forecasting run, SARIMA fit checks, Q1 2030/2050 scenarios, US/EU maps | **current** |
| **`feat/architecture-gaps` (you are here)** | price-decomposition routing, validation, figures, forecast feeding Q3 | earlier stage |
| `fix/tier1-headline-numbers` | headline fixes; canonical India run (tag `round3-final`) | earlier stage |
| `feat/pipeline-l0-l9` | first complete India pipeline, layers L0 to L9 | earlier stage |
| `main` | design, research record and empty package scaffold | superseded |
| `claude/modest-euler-714bjp` | side branch off the scaffold: seasonal re-ranking experiment (gate 3b) | not merged |

## File structure

```
├── context/                                   # research record (why the project looks the way it does)
│   ├── data/
│   │   ├── india_dc_facilities.psv            # same list, plain text
│   │   └── India_DC_Facilities_v0.xlsx        # the open India datacenter list (194 rows) - a contribution
│   ├── 00_PROJECT_STATE.md                    # READ FIRST: direction, locked decisions, RQs
│   ├── ARCHITECTURE.md                        # original research architecture (stages S0-S11)
│   ├── architecture_diagram.png               # architecture diagram
│   ├── architecture_diagram.svg               # architecture diagram (vector)
│   ├── CFP_RECORD.md                          # the journal call for papers
│   ├── DATA.md                                # every dataset: source, granularity, join key, what is on disk
│   ├── GNN_AUTOPSY.md                         # why the earlier GNN approach was dropped
│   ├── lit_review_coding_sheet.xlsx           # coded literature (84 papers)
│   ├── LIT_REVIEW_VERIFIED.md                 # verified literature review
│   ├── POLICY_DEEP_DIVE.md                    # regulation across India / US / EU
│   └── RESEARCH_GAPS.md                       # gap analysis behind the contributions
├── dcfootprint/                               # the pipeline: Python package and its config
│   ├── config/                                # every assumption lives here, never in code
│   │   ├── datasets.yaml                      # dataset registry: path, granularity, join key, role
│   │   ├── legal_constraints.csv              # legal rules and their effect on Q1/Q3 (bans, ZLD, PUE caps)
│   │   ├── parameters.yaml                    # every numeric assumption (PUE, WUE, water intensities, levers, ...)
│   │   └── policy_sources.csv                 # the 15-document policy corpus (legal RAG manifest)
│   ├── docs/
│   │   └── architecture_flow.svg              # layer flow diagram
│   ├── experiments/                           # scripts outside the pipeline (see its README)
│   │   ├── README.md                          # what each script does
│   │   └── *.py                               # 6 files
│   ├── results/                               # outputs of the latest run (regenerated; not canonical)
│   │   ├── round2_final/                      # FROZEN round-2 snapshot (do not edit)
│   │   ├── round3_final/                      # FROZEN canonical India snapshot, tag round3-final (numbers to quote)
│   │   ├── RESULTS.md                         # short results summary
│   │   ├── RESULTS_FULL.md                    # full results report (all layers)
│   │   └── *.csv, *.json                      # 18 files
│   ├── src/
│   │   └── dcfootprint/
│   │       ├── account/                       # L2 account
│   │       │   ├── build.py                   # facility-month carbon + water account
│   │       │   ├── calibrate.py               # L2.5 check vs CEEW (India) / LBNL (US)
│   │       │   ├── carbon.py                  # carbon = grid energy x state-month CI
│   │       │   └── energy.py                  # IT and grid energy
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
│   │       │   └── gem.py                     # GEM power plants, GADM state of record
│   │       ├── policy/                        # L5 legal
│   │       │   ├── gap.py                     # 4-axis regulatory gap matrix
│   │       │   └── rag_bridge.py              # policy corpus manifest (live RAG not wired)
│   │       ├── project/                       # L3 forecast + projections
│   │       │   ├── forecast.py                # national CI rolling backtest; Co-RE benchmark reader
│   │       │   ├── hierarchy.py               # one-step state CI for Q3; pre-registered method choice
│   │       │   └── recharge.py                # basin water budgets (AWARE) + G3P context
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
│   │       └── settings.py                    # loads + validates parameters.yaml (pydantic)
│   ├── tests/                                 # pytest suite
│   │   └── test_*.py                          # 2 files
│   ├── workflow/
│   │   └── Snakefile                          # Snakemake workflow
│   ├── .gitignore
│   ├── ARCHITECTURE.md                        # design, contributions (section 7), risk register
│   ├── pyproject.toml                         # dependencies
│   └── README.md                              # package guide
├── .gitignore                                 # data/, outputs/ and caches are not versioned
└── README.md                                  # this file
```

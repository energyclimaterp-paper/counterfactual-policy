# dcfootprint (branch `fix/tier1-headline-numbers`)

The Python package behind the paper, as it stood on this branch (headline fixes and the round-3 canonical India run). The current, fully documented
package guide is on [`feat/us-eu`](https://github.com/energyclimaterp-paper/counterfactual-policy/tree/feat/us-eu/dcfootprint).

Run the India pipeline from the repository root: `PYTHONPATH=dcfootprint/src python -m dcfootprint.pipeline`.
Every assumption is in `config/parameters.yaml`; outputs go to `results/`.

## Layers

| Layer | What it does |
|---|---|
| L0 ingest | read facilities, grid data, power plants, water data (`io/`) |
| L1 geo linkage | facility to water basin (`geo/join.py`) |
| L2 account | energy, carbon, physical and scarcity-weighted water per facility-month (`account/`) |
| L3 forecast | grid carbon-intensity forecasts; basin water budgets (`project/`) |
| L4 spatial | facility-to-zone and facility-to-basin matrices (`geo/incidence.py`) |
| L5 legal | regulatory gap matrix (`policy/`) |
| L6 Q3 routing | shift flexible load between sites (`routing/`) |
| L7 decisions | levers, Q2 scorecard, Q1 siting (`counterfactual/`, `decisions/`) |
| L8 uncertainty | Monte Carlo bands (`uncertainty/`) |
| L9 outputs | report (`pipeline.py`) |

## Files

```
├── config/                                    # every assumption lives here, never in code
│   ├── datasets.yaml                          # dataset registry: path, granularity, join key, role
│   ├── legal_constraints.csv                  # legal rules and their effect on Q1/Q3 (bans, ZLD, PUE caps)
│   ├── parameters.yaml                        # every numeric assumption (PUE, WUE, water intensities, levers, ...)
│   └── policy_sources.csv                     # the 15-document policy corpus (legal RAG manifest)
├── docs/
│   └── architecture_flow.svg                  # layer flow diagram
├── experiments/                               # scripts outside the pipeline (see its README)
│   ├── README.md                              # what each script does
│   └── *.py                                   # 5 files
├── results/                                   # outputs of the latest run (regenerated; not canonical)
│   ├── round2_final/                          # FROZEN round-2 snapshot (do not edit)
│   ├── round3_final/                          # FROZEN canonical India snapshot, tag round3-final (numbers to quote)
│   ├── RESULTS.md                             # short results summary
│   ├── RESULTS_FULL.md                        # full results report (all layers)
│   └── *.csv, *.json                          # 18 files
├── src/
│   └── dcfootprint/
│       ├── account/                           # L2 account
│       │   ├── build.py                       # facility-month carbon + water account
│       │   ├── calibrate.py                   # L2.5 check vs CEEW (India) / LBNL (US)
│       │   ├── carbon.py                      # carbon = grid energy x state-month CI
│       │   ├── energy.py                      # IT and grid energy
│       │   └── water.py                       # water equations
│       ├── counterfactual/                    # L7 levers
│       │   └── levers.py                      # ZLD, efficiency, coastal, disclosure: savings per lever
│       ├── decisions/                         # L7 decisions
│       │   ├── scorecard.py                   # Q2 harm scorecard per facility
│       │   └── siting.py                      # Q1 siting: regions ranked by minimax regret
│       ├── geo/                               # L1 geo linkage + L4 spatial
│       │   ├── generation_basins.py           # power plant -> basin; scope-2 scarcity factor
│       │   ├── incidence.py                   # L4 facility-zone / facility-basin matrices
│       │   └── join.py                        # facility -> AWARE basin (basin_id = GPKG fid)
│       ├── io/                                # L0 ingest
│       │   ├── aware.py                       # AWARE 2.0 water remaining per basin-month
│       │   ├── cea.py                         # CEA plant data (optional; file not on disk)
│       │   ├── ember.py                       # Ember monthly generation and emissions
│       │   ├── facilities.py                  # India facility list + coordinates
│       │   └── gem.py                         # GEM power plants, GADM state of record
│       ├── policy/                            # L5 legal
│       │   ├── gap.py                         # 4-axis regulatory gap matrix
│       │   └── rag_bridge.py                  # policy corpus manifest (live RAG not wired)
│       ├── project/                           # L3 forecast + projections
│       │   ├── forecast.py                    # national CI rolling backtest; Co-RE benchmark reader
│       │   └── recharge.py                    # basin water budgets (AWARE) + G3P context
│       ├── routing/                           # L6 Q3 routing
│       │   └── lyapunov.py                    # static / greedy / Lyapunov / LP oracle policies
│       ├── uncertainty/                       # L8
│       │   └── monte_carlo.py                 # Monte Carlo bands + first-order Sobol
│       ├── validation/
│       │   └── schemas.py                     # pandera data contracts
│       └── pipeline.py                        # RUN INDIA: all layers L0-L9, writes results/
├── workflow/
│   └── Snakefile                              # Snakemake workflow
├── .gitignore
├── ARCHITECTURE.md                            # design, contributions (section 7), risk register
├── pyproject.toml                             # dependencies
└── README.md                                  # this file
```

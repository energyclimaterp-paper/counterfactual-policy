# dcfootprint: the pipeline

The Python package behind the paper. It turns raw public data into a facility-month carbon and water account,
then answers Q1 (siting), Q2 (scorecard) and Q3 (routing) on it. How to install and run it:
[root README](../README.md#quick-start).

## How it flows

```
L0 ingest ─► L1 geo linkage ─► L2 account ─► L2.5 calibration
                                   │
          ┌────────────┬───────────┼─────────────┬──────────────┐
          ▼            ▼           ▼             ▼              ▼
     L3 forecast   L4 spatial   L5 legal    L7 levers,     L8 uncertainty
     (Q3 input,    matrices     gap +       Q1 siting,
      Q1 water                  legal       Q2 scorecard
      scenarios)                effects
          └────────────┴─────► L6 Q3 routing ◄┘
                                   │
                                   ▼
                     L9 report + figures (results/)
```
The India runner is `pipeline.py` (14 stages); `regions.py` runs the same layers for the US and the EU.

## Layers and where they live

All paths are under `src/dcfootprint/`.

| Layer | What it does | Module |
|---|---|---|
| **L0 ingest** | read facilities, Ember grid data, GEM plants, AWARE water | `io/facilities.py` (India), `io/us_facilities.py` (US), `io/ember.py`, `io/gem.py`, `io/aware.py` |
| **L1 geo linkage** | put each facility in a water basin; put each power plant in a state and basin | `geo/join.py`, `geo/generation_basins.py` |
| **L2 account** | energy, carbon, physical and scarcity-weighted water per facility-month | `account/build.py`, `account/energy.py`, `account/carbon.py`, `account/eu.py` (EU, country level) |
| **L2.5 calibration** | compare totals with CEEW (India), LBNL (US), EU coverage | `account/calibrate.py` |
| **L3 forecast** | grid carbon-intensity forecasts; the Q3 forecast method is chosen by a rule fixed in advance | `project/forecast.py`, `project/hierarchy.py` |
| | water budgets per basin; Aqueduct 2030/2050 water-stress scores | `project/recharge.py`, `project/scarcity_future.py` |
| **L4 spatial** | facility-to-zone and facility-to-basin matrices | `geo/incidence.py` |
| **L5 legal** | 4-axis regulatory gap; legal rules as effects (bans, ZLD, PUE caps) | `policy/gap.py`, `policy/rag_bridge.py` |
| **L6 Q3 routing** | shift flexible load between sites within water budgets | `routing/lyapunov.py`, `routing/agents.py` |
| **L7 decisions** | lever savings; Q2 scorecard; Q1 siting | `counterfactual/levers.py`, `decisions/scorecard.py`, `decisions/siting.py` |
| **L8 uncertainty** | Monte Carlo bands, first-order Sobol indices | `uncertainty/monte_carlo.py` |
| **L9 outputs** | report and figures | `pipeline.py`, `regions.py`, `viz/figures.py` |
| contracts | a data contract at every layer boundary | `validation/schemas.py` (pandera), `settings.py` (pydantic) |

## The account (L2)

For facility *f*, month *m*, grid zone *z* (Indian or US state, EU country) and water basin *b*:
```
E_IT     = capacity_MW · utilisation · hours(m)             IT energy
E_grid   = E_IT · PUE                                       grid energy
Carbon   = E_grid · CI(z, m)                                Ember state-month carbon intensity
W_onsite = WUE · E_IT                                       scope 1: cooling water
W_grid   = EWIF(z, m) · E_grid                              scope 2: water used by the power plants
W_phys   = W_onsite + W_grid                                physical litres (reported first)
W_scarce = W_onsite · CF(b, m) + W_grid · CF_gen(z, m)      scarcity-weighted, separate column
```
`CF` is the AWARE 2.0 monthly scarcity factor of the facility's basin; `CF_gen` is the capacity-weighted factor
of the basins where the zone's power plants sit. A **lever** is a change to these parameters (for example ZLD
recycles scope-1 water only); the account is re-run and compared with the baseline.

## Configuration (`config/`)

Every number the pipeline assumes is in `config/`, never in code.

| File | Holds |
|---|---|
| `parameters.yaml` | PUE, WUE, utilisation, water intensities per fuel, levers, routing, siting, uncertainty bands, per-region settings |
| `datasets.yaml` | where each dataset lives, its granularity and join key |
| `legal_constraints.csv` | each legal rule and its effect on Q1 and Q3 |
| `policy_sources.csv` | the 15 policy documents of the legal corpus |
| `eu_member_state_2023.csv` | EU per-country datacenter energy and water, rebuilt from the EED report by `experiments/extract_eu_tables.py` |

## Outputs

| Where | What |
|---|---|
| `results/RESULTS_FULL.md` | the full report of the latest India run (US, EU: `results/us/`, `results/eu/`) |
| `results/india_account_summary.csv` | annual totals per facility |
| `results/lever_savings.csv` | savings per lever |
| `results/q1_siting.csv` | Q1 ranking; `_small_grids.csv` = grids under 10 TWh/yr, ranked apart; `_scenarios.csv` = 2030/2050 water scenarios |
| `results/q2_scorecard.csv` | Q2 harm scorecard |
| `results/routing_comparison.csv` | Q3 policies compared; `routing_budget_sweep.csv`, `routing_v_sweep.csv` = sensitivity |
| `results/forecast_*.csv` | forecast backtests and the forecast used by Q3 |
| `results/regulation_*.csv`, `policy_corpus.csv` | regulatory gap matrix and legal effects |
| `results/uncertainty.json` | Monte Carlo bands and Sobol indices |
| `results/figures/` | figures (US/EU maps in `results/us/figures/`, `results/eu/figures/`) |
| `outputs/` (not in git) | the facility-month account as parquet, intermediate files |
| `results/round3_final/` | **frozen canonical India snapshot** (tag `round3-final`); quote numbers from here |

`results/` is overwritten by every run. Canonical snapshots are never edited; a new one gets a new folder.

## Tests (`tests/`)

| File | Covers |
|---|---|
| `test_price_decomposition.py` | the agent-based routing solver equals the central LP |
| `test_contracts.py` | data contracts accept good data and reject bad data |
| `test_us_eu.py` | US capacity classifier, EU extraction totals, Ember normalisation |
| `test_forecast_metrics.py` | the 10 forecast metrics against hand-computed values |
| `test_hierarchy_validity.py` | degenerate SARIMA fits are rejected |
| `test_siting_scenarios.py` | Q1 scenario regret and the Aqueduct score contract |

## Working rules

1. Parameters are fixed from evidence (a citation, a data audit) **before** a run and never retuned because a
   result looks wrong. A surprising result is investigated; only real bugs are fixed.
2. Each change is its own commit, checked by comparing results before and after
   (`experiments/compare_results.py`).
3. Canonical snapshots are immutable.

Other files: `ARCHITECTURE.md` (original design and the tiered contributions, section 7),
`experiments/` (one-off checks and reports, [README](experiments/README.md)), `workflow/Snakefile` (wraps the runner).

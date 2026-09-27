# Carbon and water footprint of AI datacenters: India, US, EU

> **Branch `claude/modest-euler-714bjp`: design stage (2026-09-26).** It holds the research record, the architecture and an empty
> package scaffold; the pipeline is **not** built here. **The working pipeline is on
> [`feat/us-eu`](https://github.com/energyclimaterp-paper/counterfactual-policy/tree/feat/us-eu)**, where it runs end to end for India, the US and the EU.

> This side branch adds one experiment to the scaffold: `dcfootprint/experiments/gate3b_seasonal_reranking.py`, the seasonal (monthly) version of gate 3. It was not merged into the pipeline branches.

The project builds an open, reproducible, facility-level **carbon and scarcity-weighted water** account of AI
datacenters (India in depth, the US and the EU for comparison), and uses it to ask which policy levers would
reduce the burden and where regulation has blind spots. It is the instrument behind a paper for the Elsevier
*Energy and Climate Change* special issue "Computing and Digitalization through a Multi-Disciplinary Lens".

## Start here

| If you want to... | Read |
|---|---|
| the project in one page: direction, decisions, research questions | [`context/00_PROJECT_STATE.md`](context/00_PROJECT_STATE.md) |
| the design and the tiered contributions | [`dcfootprint/ARCHITECTURE.md`](dcfootprint/ARCHITECTURE.md) (section 7) |
| where each dataset comes from | [`context/DATA.md`](context/DATA.md) |
| the gate experiments that tested the design | [`dcfootprint/experiments/README.md`](dcfootprint/experiments/README.md) |
| the literature and the gaps | [`context/LIT_REVIEW_VERIFIED.md`](context/LIT_REVIEW_VERIFIED.md), [`context/RESEARCH_GAPS.md`](context/RESEARCH_GAPS.md) |

## Branches

| Branch | What it adds | State |
|---|---|---|
| `feat/us-eu` | US and EU regions, forecasting run, SARIMA fit checks, Q1 2030/2050 scenarios, US/EU maps | **current** |
| `feat/architecture-gaps` | price-decomposition routing, validation, figures, forecast feeding Q3 | earlier stage |
| `fix/tier1-headline-numbers` | headline fixes; canonical India run (tag `round3-final`) | earlier stage |
| `feat/pipeline-l0-l9` | first complete India pipeline, layers L0 to L9 | earlier stage |
| `main` | design, research record and empty package scaffold | superseded |
| **`claude/modest-euler-714bjp` (you are here)** | side branch off the scaffold: seasonal re-ranking experiment (gate 3b) | not merged |

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
│   │   └── parameters.yaml                    # every numeric assumption (PUE, WUE, water intensities, levers, ...)
│   ├── docs/
│   │   └── architecture_flow.svg              # layer flow diagram
│   ├── experiments/                           # scripts outside the pipeline (see its README)
│   │   ├── README.md                          # what each script does
│   │   └── *.py                               # 3 files
│   ├── src/
│   │   └── dcfootprint/
│   │       ├── account/                       # L2 account
│   │       │   └── water.py                   # water equations
│   │       └── validation/
│   │           └── schemas.py                 # pandera data contracts
│   ├── workflow/
│   │   └── Snakefile                          # Snakemake workflow
│   ├── .gitignore
│   ├── ARCHITECTURE.md                        # design, contributions (section 7), risk register
│   ├── pyproject.toml                         # dependencies
│   └── README.md                              # package guide
├── .gitignore                                 # data/, outputs/ and caches are not versioned
└── README.md                                  # this file
```

Datasets are not in git; `context/DATA.md` lists every source and where it goes in `data/`.

# dcfootprint (branch `main`: scaffold)

On this branch the package is a **scaffold**: the module folders exist, but only the data contracts
(`validation/schemas.py`) and the water equations (`account/water.py`) have code. The design it was built from
is [`ARCHITECTURE.md`](ARCHITECTURE.md); the assumptions are already in `config/parameters.yaml` and
`config/datasets.yaml`.

The implemented package, with its guide, is on [`feat/us-eu`](https://github.com/energyclimaterp-paper/counterfactual-policy/tree/feat/us-eu/dcfootprint).

## Files

```
├── config/                                    # every assumption lives here, never in code
│   ├── datasets.yaml                          # dataset registry: path, granularity, join key, role
│   └── parameters.yaml                        # every numeric assumption (PUE, WUE, water intensities, levers, ...)
├── docs/
│   └── architecture_flow.svg                  # layer flow diagram
├── experiments/                               # scripts outside the pipeline (see its README)
│   ├── README.md                              # what each script does
│   └── *.py                                   # 2 files
├── src/
│   └── dcfootprint/
│       ├── account/                           # L2 account
│       │   └── water.py                       # water equations
│       └── validation/
│           └── schemas.py                     # pandera data contracts
├── workflow/
│   └── Snakefile                              # Snakemake workflow
├── .gitignore
├── ARCHITECTURE.md                            # design, contributions (section 7), risk register
├── pyproject.toml                             # dependencies
└── README.md                                  # this file
```

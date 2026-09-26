# Counterfactual Policy Analysis of AI-Datacenter Carbon & Water — India / US / EU

Open, reproducible research framework for a Q1 paper submitted to the Elsevier special issue
*Energy and Climate Change — "Computing and Digitalization through a Multi-Disciplinary Lens"*
(deadline 31 Dec 2026; IPCC-AR7-aligned).

## What it does
A deterministic pipeline — **account → project → counterfactual → policy-gap**:
1. **Account** — a sub-national, facility-level, **joint carbon + scarcity-weighted-water** account of AI
   datacenters, anchored on **India** (deep), with the **US** and **EU** for comparison.
2. **Project** — forward projection (short-horizon grid-carbon-intensity forecast + growth scenario) to 2030.
3. **Counterfactual** — what specific water/carbon **policy levers** would save (conditional scenarios).
4. **Policy-gap** — a cross-jurisdiction, four-axis **regulatory-gap map** of where the measured burden
   falls in regulatory blind spots.

Contributions are **tiered by evidential strength** (Tier-1 robust spine · Tier-2 conditional reach) —
see [`dcfootprint/ARCHITECTURE.md §7`](dcfootprint/ARCHITECTURE.md).

## Repository layout
| Path | What |
|---|---|
| `dcfootprint/` | the pipeline: package (`src/dcfootprint/`), config, Snakemake workflow, **ARCHITECTURE.md** (design + contributions + risk register) |
| `context/` | research record: `00_PROJECT_STATE.md` (read first), `RESEARCH_GAPS.md`, `LIT_REVIEW_VERIFIED.md`, `DATA.md`, `POLICY_DEEP_DIVE.md`, `CFP_RECORD.md`, `GNN_AUTOPSY.md` |
| `context/data/India_DC_Facilities_v0.xlsx` | the open India datacenter facility list (a contribution) |

## Data
Datasets are **not versioned here** (≈600 MB; several files exceed GitHub limits). Every source, its
granularity, join key, and retrieval path is documented in **[`context/DATA.md`](context/DATA.md)** — the
pipeline retrieves them into `data/` (git-ignored).

## Status
**Pipeline built and runs end-to-end (L0–L9)** — one command:
`PYTHONPATH=dcfootprint/src python -m dcfootprint.pipeline`.
Account (pandera-validated) → calibration → grid-CI forecast → counterfactual levers → policy-gap →
Q3 Lyapunov routing → Q1 siting → Q2 harm-scorecard → uncertainty; outputs in `dcfootprint/results/`.
India Floor complete on real data; US/EU tiers, legal-RAG, and the GNN-spillover arm are Ceiling.

## Stack
Python · pandas/geopandas · pandera (data contracts) · pint (units) · Snakemake (reproducible DAG) ·
statsmodels/sktime (forecasting). Deterministic by design — not a multi-agent system.

*Solo author. Reproducibility is a first-class goal of this work.*

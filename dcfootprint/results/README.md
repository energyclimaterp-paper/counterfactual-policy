# Results — start here

Everything the pipeline produces lands in this folder. **To understand the results, read this file.**
To quote India numbers, use `round3_final/` (the frozen canonical snapshot). The full three-region
synthesis, every number mapped to a research question, is `cross_region_summary.md`.

## What the pipeline produces

One **account** — every datacenter, every month: energy → carbon, and water split into on-site cooling
(*scope-1*) + the water used by the power plants that feed it (*scope-2*), each re-weighted by how scarce
water is where it is drawn. On that account, **three decisions**: **Q1** where to build a new DC, **Q2**
which existing DCs do the most harm, **Q3** whether shifting flexible load between DCs helps. Run for
**India (deep), US, EU**.

## Results by research question

| RQ | Headline | What it means | How much to trust it |
|----|----------|---------------|----------------------|
| **RQ1** magnitude & where | India **3.63 Mt CO₂** + **846.6 M m³-eq** water/yr · US **16.0 Mt** / **2.51 bn** · EU **3.35 Mt** / **137 M** | the footprint is large and sits in water-stressed basins | absolutes are calibrated ranges (India within ~8% of CEEW); **lead with *where*, not *how much*** |
| **RQ2** does the method matter | **water:** 60–82% of the scarcity burden is **scope-2** (at the power plants, not the DC). **carbon:** consumption-basis (import-adjusted) re-ranks states by ±20–40% (Bengaluru +37%, UP −28%) though the national total barely moves (+0.2%) | the method changes the *spatial* answer on **both** axes — on-site-only water misses most of it, and generation-basis mis-attributes sub-national carbon | **robust** (both structural; the global util/PUE scalar cancels) |
| **RQ3** is it regulated | **0 of 4 axes** mandated in any of the three regions → **100% of burden in a blind spot** | nothing requires measuring carbon-intensity, marginal carbon, scarcity-water, or inference | **robust** (derived from a 26-instrument registry, no assumptions) |
| **RQ4** what helps | routing is **two-sided**: US **−29% water & −10% carbon**; India **−22% water but +1.4% carbon**, and a 34-month overdraft it cannot clear | load-shifting is a co-benefit where there is slack, a trade-off where basins are already dry → **siting + binding limits are needed, not just shifting** | routing **robust across the sweeps**; lever *absolutes* are conditional scenarios |

Equity diagnostic (now fused into Q2): **63% of India's DC water burden lands on already over-exploited
aquifers** (Bengaluru 187%, Chennai 125%) — the Q2 scorecard carries each facility's `gw_stage_pct` + `gw_category`.
Seasonal (**C3, *when***): India's carbon and scarcity **co-peak in March** (dry pre-monsoon; top-3 months hold
38% of annual scarcity water), the US co-peaks in summer, but the **EU is anti-correlated** (water Aug, carbon
Jan) so a seasonal lever helps one axis and hurts the other (`seasonal_profile.md`). Forecasting (a support
layer, **not** a contribution): **simple ≥ complex** — the deep net is worst, no model beats seasonal-naive.

### Per-region account (RQ1 detail)

| | India (71 fac) | US (235 fac) | EU (21 states) |
|---|---|---|---|
| Carbon | 3.63 Mt CO₂ | 16.0 Mt | 3.35 Mt CO₂e |
| Scarcity-weighted water | 846.6 M m³-eq | 2.51 bn m³-eq | 137 M m³-eq |
| Scope-2 share of scarcity water | 60% | 68% | 82% |
| Lever that pays most | ZLD 37% (≈ efficiency, but +19% carbon) | efficiency 31% / ZLD 29% | ZLD 16% |

*India carbon is **consumption-based** (Electricity Maps regional, import-adjusted; `grid.carbon_basis: consumption`),
which closes the R2 generation-vs-consumption caveat; generation basis is the stated sensitivity. The national
total is within +0.2% of generation; the change is in the sub-national distribution.*

## Routing robustness (RQ4 — the most attackable assumption)

The two-sided result is a **bound, not a point claim.** Sweeping the sector's water-budget share α from
1.0 down to 1e-4 (four orders of magnitude), India routing always saves **18–22%** scarcity water, always
*adds* carbon, and the **34 overdraft basin-months never clear**; it is also insensitive to the controller's
drift-penalty weight V. The 30% flexible share is a cited central case (Duke, MIT, Google CICP, Emerald
Conductor), reported under the sweep. See `round3_final/routing_budget_sweep.csv`, `routing_v_sweep.csv`.

## The spine, in one sentence

Measure the joint carbon + scarcity-water footprint sub-nationally → show most of it is off-site and entirely
outside what any regulation requires → show the fix is two-sided, so siting and limits are needed where the
basins are already dry.

## What each file / folder is

**Curated — read these:**
- `README.md` (this) — the results overview.
- `cross_region_summary.md` — the three-region synthesis; every number mapped to an RQ.
- `rag_axis_audit.md` · `forecast_simple_vs_complex.md` · `seasonal_profile.md` · `q2_equity_groundwater.md`
  — the standalone exhibits (RAG corroboration of the gap, the forecasting null, the seasonal *when* finding,
  the groundwater-equity summary; the per-facility equity detail is now fused into `q2_scorecard.csv`).

**Canonical snapshots — quote from these:**
- `round3_final/` — **FROZEN canonical India run** (git tag `round3-final`). The India numbers above come
  from here. Immutable; a new canonical run gets a new dated folder.
- `round2_final/` — superseded round-2 snapshot. Kept only because `experiments/round3_report.py`
  reconstructs the round-3 attribution report from it. Not for quoting.

**Latest-run outputs — regenerated every run, not canonical:**
- `RESULTS.md`, `RESULTS_FULL.md` — auto-written summary / full report of the latest India run.
- `india_account_summary.csv`, `lever_savings.csv`, `q1_siting*.csv`, `q2_scorecard.csv`, `routing_*.csv`,
  `forecast_*.csv`, `policy_*.csv` / `regulation_*.csv`, `uncertainty.json` — latest India outputs.
- `us/`, `eu/` — latest US and EU region outputs (account summary, levers, Q2, Q1, routing [US only],
  uncertainty, report, figures).
- `figures/` — India figures (US / EU figures are under `us/figures/`, `eu/figures/`).

## Reproducibility & current state (2026-10-10)

All three regions run clean on the current code: **India 14/14 · US 10/10 · EU 8/8.** The account reproduces
`round3-final` to machine precision on the **generation** carbon basis; the default India run now uses the
**consumption** basis (Electricity Maps), which leaves the national total within +0.2% but re-ranks sub-national
carbon (Bengaluru +37%, UP −28%). Dataset sources are in `context/DATA.md`; the large inputs a fresh clone must
fetch (incl. the Electricity Maps key for consumption carbon) are listed there.

# dcfootprint — Detailed Architecture (carved out)

**Shape (the four pillars):**
```
   ACCOUNT  ─────▶  PROJECT  ─────▶  COUNTERFACTUAL  ─────▶  POLICY-GAP
  (present)      (forward, time-       (what levers        (where regulation
                 series + scenario)     would save)          is blind)
```
Deterministic · config-driven · schema-validated (pandera) · units-safe (pint) · one-command reproducible (Snakemake).
**Forecasting / time-series lives in PROJECT** (real forward projection), not bolted onto the account.
**No agents** — a pipeline of pure functions (rationale: agents force behavioural assumptions we refuse to make + undermine reproducibility).

---

## 1. Data-flow DAG

```
CONFIG (parameters.yaml · datasets.yaml · levers.yaml)  ── validated by pydantic ──┐
                                                                                   ▼
── L0 INGEST (io/) ─ parallel ───────────────────────────────────────────────────
  facilities(our⋈ATLAS⋈CEA) · ember(zone-month C+fuel) · aware(basin CF+polys)
  · macknick(EWIF) · gadm(state polys) · egrid(US x-check) · cgwb/g3p/gem(context)
        │                    │                     │
        ▼ (SPINE)            ▼                     ▼
── L1 GEO (geo/) ── geocode facilities → point-in-polygon → zone_id + basin_id
        │
        ▼
── L2 ACCOUNT (account/) ── energy → carbon → water(scope1+2) → scarcity → ×inference
        │  output: account_facility_month  ★ the dataset (present)
        ├───────────────▶ L3 PROJECT (project/)  [Ceiling]
        │                   forecast grid-CI (TIME SERIES) + growth scenario + scarcity future
        │                   output: account_projected → 2030/2050
        ▼                        │
── L4 COUNTERFACTUAL (counterfactual/) ◀──────────┘
     apply each lever to present AND projected → Δ; rank "which lever pays"
        │  output: lever_savings  ★ the finding
        ▼
── L5 POLICY-GAP (policy/)  [parallel track]
     four-axis regulation matrix (IN/US/EU) ⋈ measured burden → blind-spot overlay
        │  output: regulatory_gap_matrix + gap_overlay  ★ the frame
        ▼
── L6 UNCERTAINTY (uncertainty/) ── Monte-Carlo over parameter bands + Sobol sensitivity
        │  wraps L2–L4 outputs with confidence bands
        ▼
── L7 OUTPUTS (viz/, report/) ── maps · tables · figures · open data+code release
```
`snakemake -c4 floor` = India Floor (L0–L2 + L4[1-2 levers] + L5 + L6 + L7).
`snakemake -c4 all`   = + L3 projection, full L4, US/EU, marginal carbon.

---

## 2. Layer-by-layer carve-out

### CONFIG — `config/` (pydantic + PyYAML)
| File | Holds |
|---|---|
| `parameters.yaml` | utilisation, PUE, WUE (+ operator overrides), EWIF fuel→coeff crosswalk, inference share — each with an uncertainty **band** + source |
| `datasets.yaml` | dataset registry: path · granularity · join_key · role (mirrors DATA.md D/E/F) |
| `levers.yaml` | the 4 counterfactual levers as parameter transforms |
| `config.py` | pydantic models that load + **validate** the above (types, ranges, required keys) |

### L0 — INGEST · `io/` · (pandas, pyarrow, openpyxl)
| Module | Reads | Emits (→ schema) | Grain |
|---|---|---|---|
| `facilities.py` | our list ⋈ ATLAS coords ⋈ CEA plant | `Facilities` | facility |
| `ember.py` | `data/ember/*` | `EmberZoneMonth` (CI + generation + fuel-mix) | zone-month |
| `cea.py` | `data/cea/CEA_Database_V22.xlsx` | India GEF (anchor) + plant table | national-annual / plant |
| `egrid.py` | `data/egrid/…rev2.xlsx` (SRL23) | US subregion EF (cross-check) | subregion-annual |
| `aware.py` | `data/aware/…gpkg` + `…Native_CFs.xlsx` | `BasinMonthlyCF` + polygons | basin-month |
| `macknick.py` | config EWIF coeffs (sourced from PDF) | fuel→L/MWh table | per-tech |
| `cgwb.py`,`g3p.py`,`gem.py` | context CSVs/xlsx | context frames | state/basin/plant |
| `policy.py` | POLICY_DEEP_DIVE + EU reg text + datacenterbans (to retrieve) | regulation matrix | jurisdiction×axis |

### L1 — GEO LINKAGE · `geo/` · (geopandas, shapely, pyogrio)
- `geocode.py`: facility (city/campus) → **lat/lon** (the 194 need this; ATLAS city-centroid supplements). *Bottleneck.*
- `join.py`: **point-in-polygon** facility→`zone_id` (GADM ADM_1) and facility→`basin_id` (AWARE gpkg). Reuses the salvaged geocoder + exact→alias→fuzzy(0.82) state resolver.
- Emits: `facilities` enriched with `zone_id`, `basin_id`, `month-independent` static attrs.

### L2 — ACCOUNT (present) · `account/` · (pandas, numpy, pint)
Equations (Guidi/Li/Siddik), per facility *f*, month *m*:
```
E_IT     = capacity_MW · utilisation · hours(m)
E_grid   = E_IT · PUE
Carbon   = E_grid · CI(zone,m)                     # Ember gCO2/kWh
W_onsite = WUE · E_IT                              # scope-1
EWIF(z,m)= Σ_fuel share(z,m)·macknick[fuel]        # from Ember fuel-mix × Macknick
W_grid   = EWIF(z,m) · E_grid                       # scope-2
W_phys   = W_onsite + W_grid                        # PHYSICAL (reported first)
W_scarce = W_phys · AWARE_CF(basin, month)         # SEPARATE column
```
- `energy.py` · `carbon.py` · `water.py` · `scarcity.py` · `inference.py` · `build.py` (assemble + validate `FacilityMonthAccount`).
- Output: **`account_facility_month.parquet`** — product ② (the dataset). Grain = facility-month.

### L3 — PROJECT (forward) · `project/` · (sktime, statsmodels, [chronos-forecasting], numpy) — **the time-series layer**
Purpose: DCs built now run 15–20 yrs → estimate the **lifetime / 2030–2050 footprint** as grid + scarcity evolve.
| Module | Method | Real forecast or scenario? |
|---|---|---|
| `forecast_grid_ci.py` | fit + **backtest** SARIMA vs Chronos-2 vs seasonal-naive per zone on Ember CI history (2019→2025 IN / 2001→2025 US); pick by backtest RMSE (salvaged benchmark harness); forecast monthly CI → 2030 with prediction intervals; anchor long-run to CEA/IEA decarbonisation pathway | **REAL time-series forecast** (Ember CI is a genuine monthly series) |
| `growth.py` | allocate announced pipeline (JLL/CEEW: IN 1.8→6.5 GW; 509 MW u/c + 3,351 MW planned) over time (COD dates where known, else S-curve) | **scenario** (declared, sensitivity-tested) |
| `scarcity_future.py` | Aqueduct 2030/2050 projections (or AWARE held) | scenario |
| `build.py` | re-run L2 equations with projected CI + capacity + scarcity → BAU projected account | — |
- Output: **`account_projected.parquet`** (facility-month → 2030/2050). Ceiling.
- **Honesty rule (stated in paper):** only grid-CI is *forecast*; growth + scarcity are *scenarios*. No pretence that capacity is time-series-predicted.

### L4 — COUNTERFACTUAL · `counterfactual/` · (pandas)
A lever = a **parameter transform**, applied to BOTH present (L2) and projected (L3):
| Lever | Transform |
|---|---|
| mandatory_disclosure | coverage → reveal the hidden footprint vs current opacity |
| coastal_seawater_siting | WUE → ~0.1 for eligible/relocatable load |
| zero_liquid_discharge | W_phys → W_phys·(1−recycle), recycle≈0.92 |
| efficiency_standard | PUE→cap, WUE→cap, **with the energy↑/water↓ trade-off modelled** |
- `levers.py` (apply) · `rank.py` (annual Δ now + **cumulative Δ to 2030** = where PROJECT feeds in).
- Output: **`lever_savings.csv`** — product ① (the finding: "which lever pays, now and by 2030").

### L5 — POLICY-GAP · `policy/` · (pandas)
- `regulations.py`: encode the four-axis matrix {carbon-intensity, marginal, scarcity-water, inference} × {IN, US, EU} × {enacted, proposed} — from POLICY_DEEP_DIVE + EU Reg 2024/1364 text + datacenterbans.com.
- `gap.py`: overlay measured burden (L2) → flag high-burden facility-months mandated by **none** of the four axes → the blind-spot map.
- Output: **`regulatory_gap_matrix.csv`** + `gap_overlay` — product (the frame). Grain = jurisdiction×axis, and facility-month×in-scope-flag.

### L6 — UNCERTAINTY & VALIDATION · `uncertainty/`, `validation/` · (numpy, scipy, SALib, pandera)
- `validation/schemas.py`: **pandera contracts at every boundary** — the atomic-unit (facility-month) guarantee; the GAT mistake = a test failure.
- `uncertainty/monte_carlo.py`: sample parameter bands (util, PUE, WUE, EWIF, inference share, recycle) → confidence bands on every output.
- `uncertainty/sensitivity.py`: Sobol/Morris (SALib) → which assumptions drive the result (defends against "your numbers are assumed").
- Output: `uncertainty_bands.parquet`, `sensitivity_indices.csv`.

### L7 — OUTPUTS & INSTRUMENT · `viz/`, `report/` · (matplotlib, geopandas, folium)
- Sub-national burden maps · gap-overlay maps · ranked-lever tables · monthly-seasonal trajectories · projection fan-charts.
- Release: open data + code + `snakemake all` one-command reproduction (contribution ④).

---

## 3. Data contracts (the boundaries — `validation/schemas.py`)
`Facilities` · `EmberZoneMonth` (unique zone-month) · `BasinMonthlyCF` (CF≤100) · `FacilityMonthAccount` (unique facility-month; `W_phys = scope1+scope2`; scarcity a separate column). Every DAG rule validates its output before writing.

## 4. Floor vs Ceiling (build order)
- **FLOOR (submittable):** L0–L2 India + L5 gap + L4 present (1–2 levers) + L6 + L7. No forecasting needed.
- **CEILING:** + L3 projection (the time-series layer) + full L4 (all levers, cumulative-to-2030) + US/EU tiers + US/UK marginal carbon.
- **Build sequence (spine first):** `io/facilities.py` → `geo/` → `account/` → `counterfactual/` (present) → `policy/gap.py` ∥ → then `project/` (adds the forward/time-series) → uncertainty → outputs.

## 5. What forecasting/time-series actually IS here (so it never drifts again)
1. **Monthly accounting** (L2): carbon & scarcity are **seasonal** → the account is a real monthly panel (not forecasting, but genuinely time-indexed).
2. **Forward projection** (L3): grid carbon intensity is **forecast** as a time series (the salvaged SARIMA/Chronos benchmark, backtested); capacity growth + scarcity futures are **scenarios**. Together → the lifetime/2030 footprint.
3. **Counterfactual × projection** (L4): cumulative lever savings to 2030 — the decision-grade output.
That is the honest, load-bearing role for time-series + forecasting: **the forward projection**, not the present account.

---

## 6. RED-TEAM v1 — fixes applied + risk register (2026-09-26)

### 6.1 The framing the red-team forced (the most important change)
The account is **assumption-dominated** (a global utilisation×PUE scalar drives absolute magnitude), so **absolute per-facility numbers are not the contribution.** What IS robust:
> **ROBUST CORE (lead with this):** the **spatial-distributional** result — *where* scarcity-weighted water burden concentrates across India's basins (driven by real facility location × basin scarcity × capacity, which survives a global scalar because it **cancels in relative comparison**) — plus the **regulatory-gap** overlay.
> **Absolutes** = reported as **calibrated ranges** (vs independent totals), never point estimates.
> **Counterfactual** = **conditional scenarios** ("*if* lever achieves X → saves Y"), demoted from headline to decision-relevant application.

### 6.2 Two layers ADDED (were missing)
- **L1.5 · COVERAGE (`geo/coverage.py`):** compute facility-list coverage % vs independent aggregates (CEEW ~1.8 GW; JLL 147 DCs); report representativeness and bound aggregates. **Does NOT fabricate-correct** missing facilities (their distribution is unknown) — it quantifies the gap.
- **L2.5 · CALIBRATE (`account/calibrate.py`):** validate the bottom-up aggregate against independent totals (CEEW India, LBNL US 176 TWh, IEA). Report the account as **"consistent with X"** ranges. *(Honest limit: calibration validates the TOTAL, not the distribution — the distribution is defended by robustness-to-scalar, not by calibration.)*

### 6.3 Risk register — flaw → fix → residual
| # | Flaw | Fix applied | Residual (state in paper) |
|---|---|---|---|
| R1 | account = assumed util×PUE scalars | lead with **relative/spatial** (scalar cancels); absolutes as calibrated ranges; util/PUE **by facility type** (hyperscale/colo) | rankings depend on type assignment → sensitivity-test |
| R2 | India carbon = state generation-mix (consumption error) | use **CEA regional** consumption intensity; **demote sub-national carbon**, lean India novelty on water | **RECOVERABLE (Ceiling, DATA.md PART G):** Electricity Maps India *regional* zones = consumption-based (import-adjusted) + temporal; EnergyMap.in = state/regional CI. → India carbon can be regional-monthly consumption-correct, not annual-trivial. Cost: EM API. |
| R3 | scope-2 water mis-attributed to DC basin + Macknick-US coeffs | scope-1 rigorous at DC basin; scope-2 at generation regions | **RECOVERABLE — field standard (DATA.md PART G):** Reiss ERL'21 (HUC-8 scope-2 water), Guidi (BA→HydroBASINS→Aqueduct), LBNL Water IMPACT Tool (BA consumption-based water). → scope-2 water localisable to **generation-region basins** → scarcity-weighting covers FULL water (not ¼). US: LBNL tool; India: build equivalent (GEM+CEA). |
| R4 | scarcity re-ranking may be within noise (RQ2) | **GATE experiment before build** (§6.4-1) | if within noise → finding pivots to "average adequate" |
| R5 | L3 forecasting may reproduce GAT null | **backtest gate** (§6.4-2); else use scenario, report null | 2030 horizon is scenario regardless (see R11) |
| R6 | counterfactual = assumption-heavy | **conditional-scenario framing** + full sensitivity; demoted to application | savings are conditional, labelled as such |
| R7 | reproducibility hole (hand-curated list) | reframe ④ as **open + sourced + auditable**; pipeline-on-list is reproducible | facility list is transparent, not from-scratch reproducible |
| R8 | coverage bias (77%, non-random) | **L1.5 coverage layer**; report %, bound | can't correct unknown missing distribution |
| R9 | AWARE CF=100 is a CAP, not a value | `io/aware.py` flags capped/no-data basins; schema note | capped basins = "max scarcity", handled explicitly |
| R10 | climatological scarcity misses drought years | state limitation; optional actual-year stress overlay (Aqueduct annual) | monthly climatology ≠ event-specific stress |
| R11 | cross-region granularity inconsistent (IN state / US subregion / EU country) | define comparison at a **common normalised unit** (per-MW; basin-level) for the gradient | absolute cross-region comparison remains coarse |
| R12 | "which lever pays" metric undefined | **primary metric = scarcity-weighted m³ avoided per year + cumulative-to-2030**; absolute m³ + tCO₂ secondary | metric choice stated; rankings shown for each |
| R13 | inference = flat 85% scalar (no info) | reframe as a **sensitivity range**, not "attribution"; drop over-claim | inference-axis is scoping, not discrimination |
| R14 | no data versioning | `datasets.yaml` gains **version/date/hash** per source; provenance manifest at release | — |

### 6.4 De-risking GATES — run on data-in-hand BEFORE building the full spine
1. **RQ2 signal-vs-noise:** does scarcity-weighting re-rank basins/facilities *beyond* Monte-Carlo noise? (go/no-go for the methodological claim)
2. **Forecasting backtest:** does grid-CI forecasting beat seasonal-naive at 12-mo horizon? (keep vs cut L3's forecasting framing)
3. **Calibration:** does the bottom-up India total land near CEEW's independent ~1.8 GW? (validates magnitude)
Any one can redirect the paper — cheaper to learn now than after implementation.

### 6.5 GATE RESULTS (run 2026-09-26 on data in hand — scripts in `experiments/`)
- **G1 CALIBRATION = PASS:** bottom-up operational **1.39 GW** (90 costed / 129 operational) vs CEEW/JLL **1.5–1.8 GW** → ratio 0.84 (+39 uncosted → ~1.0). C1 magnitude validated against an independent source.
- **G2 COVERAGE = PLAUSIBLE (caveat):** Mumbai/Navi 31% ≈ CEEW ~25%; **BUT ~61% of capacity sits in 3 mega-sites** (Navi Mumbai 25% · Palava 20% · Vizag 16%) → the hotspot ranking hinges on a few large facilities. ATLAS city field 57% blank (coarse gap-filler only).
- **G3 RQ2 = scarcity-weighting does NOT re-rank (ANNUAL):** Spearman(unweighted,weighted) **0.91 state / 0.95 basin**; top-5 overlap **5/5**; MC(400) tight [0.90–0.96]; worst regions (Maharashtra/Andhra/Telangana/Tamil-Nadu) **identical** weighted vs unweighted. Scarcity CF varies (1.6–78.9) — not flat; capacity & scarcity are **positively correlated**.
- **★ THE REFRAME (do not lose):** headline is NOT "scarcity-weighting re-ranks." It IS **"India's AI datacenters are disproportionately sited in already-water-stressed basins — weighting doesn't move the hotspot ranking because the hotspots ARE the stressed basins."** C4 → "we tested method-sensitivity; for India, average is adequate to flag hotspots *because siting coincides with stress*" — clean, no-assumptions, policy-relevant. Spine (C1/C5/C8) intact. (Red-team S4 anticipated this.)
- **PENDING (decisive):** **seasonal Gate 3 (monthly CF, not annual)** — does dry-season scarcity re-rank? (C3's "when" may carry the signal annual lost). Forecasting-backtest gate still un-run. G3 first-pass caveats: city-centroid geocode, annual CF, 124 matched facilities, capacity-concentrated.

---

## 7. CONTRIBUTIONS (tiered) + full-potential architecture (2026-09-26)

> How to be *ambitious AND honest at once*: **include every contribution, but label its evidential tier.** Tier-1 carries the paper (robust, low/no assumptions → Q1-solid); Tier-2 is the reach (conditional/diagnostic → gated by the experiments). Lead with Tier-1, reach with Tier-2. This is how we get "all the potential" without re-importing the red-team flaws.

### 7.1 The contributions, stated clearly
| # | Contribution | Type | Tier | Why it's real |
|---|---|---|---|---|
| **C1** | First **open, sub-national, facility-level, JOINT carbon + scarcity-weighted-water account** of AI datacenters, **anchored on India** (+US/EU comparison) | data/empirical | **1** | India is unbuilt (89-paper review); joint + facility-month + AWARE-monthly |
| **C2** | **Full-water scarcity localisation** — scope-1 at the DC basin + **scope-2 at generation-region basins** (consumption-based), not stranded at one basin | method | **2** (Ceiling) | field standard (Reiss HUC-8, Guidi BA→basin, LBNL Water-IMPACT); recovers full-water rigour |
| **C3** | **Where** scarcity-weighted burden concentrates across India's basins + **when** (seasonal dry-month × high-carbon-month peaks) | finding (spatial-temporal) | **1** | robust to the global scalar (cancels); uses genuine monthly seasonality |
| **C4** | **Does the method change the answer?** When scarcity/marginal weighting re-ranks vs when average is adequate — guidance for the field | finding (methodological) | **1** | decision-relevant either way; RQ2 gate |
| **C5** | **Cross-jurisdiction four-axis regulatory-gap map** (India/US/EU) + a **transferable** gap-diagnostic instrument | policy | **1** | needs NO assumptions; the cleanest contribution; hits Verdolini |
| **C6** | **What policy levers would save** — conditional, engineering-grounded scenarios, projected (short-horizon grid-CI forecast + growth scenario) | forward/decision | **2** | levers physics real; adoption conditional + sensitivity |
| **C7** | **Distributional / equity diagnostic** — burden landing on already water-stressed basins/communities (CGWB stress × facility load) | finding (equity) | **2** (diagnostic) | resonant, policy-relevant; framed diagnostic, never prescriptive |
| **C8** | **Open reproducible framework** + **released open India facility dataset** (first of its kind) | instrument | **1** | reproducibility pillar (FAS/AGU call); the solo-author offset |
| **C9** | **Joint carbon+water uncertainty propagation** (Monte-Carlo bands + Sobol) — most footprint papers give point estimates | method | **1** | rigour the venue rewards; defends every number |

**Tier-1 (carries the paper, Q1-solid):** C1, C3, C4, C5, C8, C9. **Tier-2 (the reach):** C2-full, C6, C7.

### 7.2 Architecture additions to hold the full potential (were implicit; now explicit layers)
- **L0/L2 — Ceiling carbon (recovers R2):** add **Electricity Maps India regional** (consumption-based, import-adjusted, temporal) + **EnergyMap.in** as the India consumption-carbon source → `io/electricitymaps.py`. (Floor still uses CEA-regional/Ember.)
- **L2-water — Ceiling scope-2 localisation (recovers R3, enables C2):** `account/water_grid_basin.py` — attribute scope-2 water to **generation-region basins** via LBNL Water-IMPACT (US) / GEM+CEA-built equivalent (India).
- **L2b — SEASONALITY (`account/seasonal.py`, enables C3-when):** dry-month scarcity × high-carbon-month overlay → when/where burden peaks. Floor (uses monthly account we already build).
- **L5b — EQUITY diagnostic (`policy/equity.py`, C7):** facility burden × CGWB block stress × (optional) population → distributional map. Diagnostic, Ceiling.
- **L6 — METHOD-SENSITIVITY as a first-class output (C4) + UNCERTAINTY-as-contribution (C9):** `uncertainty/method_sensitivity.py` (does weighting re-rank beyond noise) elevated from "check" to a **reported finding**.
- **Released dataset (C8):** `outputs/india_facility_account.parquet` + the facility list published openly with per-row provenance.

### 7.3 Why this is Q1-worthy (hits the CFP + all four editors)
- **Multi-disciplinary + decision-relevant + method-combining** (accounting + geospatial + policy + forecasting) — the CFP's explicit asks.
- **All four editor vectors:** Clarens (DC water/carbon = C1/C2), Verdolini (policy = C5/C6), McCollum (scenarios/AR7 = C6 projection), Te Han (ML/forecasting = C6 short-horizon + C9).
- **AR7-aligned** forward projection; **openness** (C8) the venue explicitly rewards.
- **The moat:** India-anchored + full-water scarcity + reg-gap map + open — unoccupied vs 89 works.

### 7.4 The honesty rule that keeps it Q1 and not over-sold
Every headline claim is **Tier-1** (robust). Tier-2 (counterfactual, equity, projection, full-scope-2) is presented as **explicitly conditional/diagnostic with sensitivity** — reach, clearly labelled. A reviewer who attacks Tier-2 cannot touch the Tier-1 spine. That is the difference between "ambitious" and "over-claimed."

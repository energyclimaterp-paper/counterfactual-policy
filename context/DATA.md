# DATA — Requirements, Accessibility & Reliability (merged)

> **⚠️⚠️ READ PART D FIRST (added 2026-09-26).** Parts A–C describe the *intended/planned* reliable stack. **PART D is the physical audit of what is ACTUALLY on disk** (verified against each dataset's live internet source). Headline: **NONE of the ~13 "primary" sources named in Parts A–C are on disk** — what we physically hold is the old GAT-project stack (Ember, Aqueduct, G3P, ATLAS, GEM + our India list), several of which Parts A/B themselves demoted/dropped. Everything missing is OPEN and retrievable. Trust Part D on "what we have"; trust Parts A–C on "what to get."

> Consolidated 2026-09-20 from `DATA_REQUIREMENTS_AND_ACQUISITION` (Part A) + `DATASET_RELIABILITY_ANALYSIS` (Part B). **Read `00_PROJECT_STATE.md` first.** Authoritative corrections (trust these over the body text below):
> - **CEA CO₂ Baseline — ⚠️ CORRECTED 2026-09-26: v22.0 NOW EXISTS** (data dated 2026-08-01, released Sep 2026; `Baseline_..._Version_22.0.xlsx`). The docs' "v22 doesn't exist yet" is stale — **v22 retrieved** (`data/cea/`), alongside v21 (FY24-25). The v22 `Data` sheet is **plant-level** (NAME/UNIT/CAPACITY/STATE/SECTOR); the grid **emission factor** is still all-India + regional, annual, average → carbon INTENSITY stays regional-annual, but plant/state capacity+fuel data is granular. India sub-national novelty still rides primarily on **WATER (AWARE monthly, now retrieved)** + facility geography; carbon adds a state generation-mix proxy (Ember) with a generation-vs-consumption caveat.
> - **India facilities = 194 (129 operational), not "~132".** 40/129 operational uncosted; mixed capacity bases; built from scraped/trade sources — the novel core sits on the softest data (fix early).
> - **AWARE2.0 (2025, Zenodo)** is the current scarcity method (body references AWARE 1.x).
> - Atomic unit = **facility-month**; each resource keeps its native partition; the facility is the join key.

---
## PART A — Accessibility & acquisition map (verified)

# Data Requirements & Acquisition Map — Verified

*Compiled 2026-09-14. This is the **operational** data document: for every input the pipeline needs, it states (1) **granularity** — native vs. what the facility-month join requires, and how they reconcile; (2) **dependencies** — which stage consumes it and what must be acquired before it; (3) **accessibility** — the access tier, the verified source, and an honest confidence. Every accessibility line below was **live-verified on 2026-09-14** (four parallel web-verification passes), not inherited. Where verification could not close something out, it says so. Supersedes the `§4 acquisition list` framing in `DATA_EVALUATION_AND_PLAN.md` (which used the old RQ2/N-axis tiering); the granularity framework in that doc remains valid.*

> **Read `00_PROJECT_STATE.md` first for scope.** This doc assumes the locked India-anchored, Floor-first, S0–S11 architecture.

---

## 0. The one rule that governs every row (granularity)

**Atomic unit = the facility-month. Each resource keeps its own native partition; the facility is the common join key. Aggregate *up* to the reporting unit per resource; never down-force one partition onto another.** (This is the fix for the exact error that sank the prior project — see `DATA_EVALUATION_AND_PLAN.md §1.) Common time unit = **month.** Every dataset below is judged on whether it slots into that structure, and the "reconciliation" column says how.

**Access-tier legend:** `OPEN` = free direct download, no account · `FREE-REGISTER` = free but needs an account/approval · `REQUEST` = must apply/email, gated · `PAYWALL` = paid · `DERIVE` = must be built from other sources (no ready dataset) · `NOT-FOUND` = no real source located.

---

## 1. The dependency spine (what must be acquired before what)

Acquisition is **not** a flat list — it has a critical path, and it is the same critical path that killed the last project:

```
   ┌─────────────────────────────────────────────────────────────┐
   │  STEP 1 (no blocker) — GEOSPATIAL POLYGONS                   │  OPEN, pull now
   │  HydroBASINS · grid-zone shapefiles · AWARE polygons · GADM  │
   └───────────────────────────┬─────────────────────────────────┘
                               │  needed to place facilities
   ┌───────────────────────────▼─────────────────────────────────┐
   │  STEP 2 (THE GATE) — FACILITY LOCATIONS                      │  ★ India = DERIVE (hard)
   │  India (hard) · US (weak) · EU (hand-curated hubs)           │  ★ US = weak · EU = curate
   └───────────────────────────┬─────────────────────────────────┘
                               │  S0 JOIN → facility_master  (critical path)
        ┌──────────────┬───────┴───────┬──────────────┬───────────┐
        ▼              ▼               ▼              ▼           ▼
   STEP 3 CARBON   STEP 4 WATER    STEP 5 SCARCITY  STEP 6      STEP 7
   (avg: OPEN)     COEFFS (OPEN)   (AWARE: OPEN)    INFERENCE   POLICY
                                                    (OPEN)      (OPEN)
        │                                                          │
        ▼ (Ceiling)                                                ▼ (Ceiling)
   marginal carbon (register)                          growth + forecast inputs
```

**The consequence, stated plainly:** everything in Steps 3–7 is essentially free and obtainable now. **Steps 1 and 2 are the whole game, and Step 2 (facility locations) is where the risk lives** — nothing downstream can be computed for a facility we cannot place. So the acquisition effort is not spread evenly; it concentrates on locations.

---

## 2. The master map, by cluster

### A · Facility locations *(feeds S0 · the spine · the risk)*

| Region | Native granularity | Reconciliation to facility-month | Access | Verified source | Confidence |
|---|---|---|---|---|---|
| **India** | point (city/campus) → grid zone + watershed + basin | point → CEA grid region + watershed + basin | **DERIVE — v0 BUILT (2026-09-14)** | **No ready-made free facility dataset exists, so we built one.** `data/India_DC_Facilities_v0.xlsx` — **194 sourced rows (129 operational, 37 under-construction, 24 announced)** assembled from operator disclosures + trade press + public directories. **~1,373 MW operational disclosed capacity — validates against CEEW's independent ~1.5 GW national figure (≈90%+ coverage of operational capacity).** Every row carries its source_url + confidence. Still needs: per-facility lat/lon geocoding; capacity for ~60 "unknown" rows. *(No source in this list is paywalled — the earlier "~132" was a paywalled-report headline, now superseded by our own bottom-up list.)* | **High** — bottom-up total matches the independent aggregate |
| **US** | point/polygon | point → eGRID subregion + watershed + basin | **OPEN (modeled) + weak (real)** | **PNNL IM3 "Projected US DC Locations"** (OSTI 2571680, GeoJSON, fields incl. IT power MW, water demand, cooling) = **modeled/projected siting, polygons not points**. A **separate "existing DC" dataset** is referenced (data.msdlive.org/records/65g71-a4731) — fields **NOT CONFIRMED**, must verify. **NREL "US DC Infrastructure 2025" = NOT downloadable** (static image only, cited data-sensitivity). | **Med** — PNNL fields confirmed via OSTI metadata; the "existing" set unverified |
| **EU** | — | point → country/bidding-zone + watershed + basin | **DERIVE** (hand-curate) | Known hub clusters (Dublin, Frankfurt, Amsterdam, Paris, London, Nordics) hand-verified against DataCenterMap + EUDCA. EU is the light region; descriptive is acceptable. | Med |

> **★ PROVENANCE FLAG — RESOLVED (2026-09-14):** the old "~132 hand-verified facilities" traced to a paywalled market-report headline, not real rows we possessed. **We resolved it by building our own open, bottom-up facility list from the web** (`data/India_DC_Facilities_v0.xlsx`, 194 sourced rows). Its ~1.37 GW operational total matching CEEW's independent ~1.5 GW is the completeness check that the old headline never had. The India location layer now **exists, openly and reproducibly** — which is itself a contribution, not just an input.

### B · Electricity & carbon intensity — average *(feeds S1→S2 · Floor)*

| Component | Native granularity | Reconciliation | Access | Verified source (2026-09-14) | Confidence |
|---|---|---|---|---|---|
| **US** average EF + fuel mix | eGRID subregion (~26), **annual** | zone EF applied at facility's subregion-month (annual→held constant across months, stated) | **OPEN** | **eGRID2023** (rev2, Jun 2025) `epa.gov/egrid/download-data` → `egrid2023_data_rev2.xlsx`. eGRID2024 planned Jan 2026, not yet out. | High |
| **India** average EF | plant→regional/all-India grid, **annual** | CEA grid EF at facility's grid-region-month | **OPEN** | **CEA CO₂ Baseline Database v21.0** (Aug 2026, FY2025-26) `cea.nic.in/cdm-co2-baseline-database` (.xlsx + user-guide PDF). **NOTE: this is v21, not the "v19" in our older docs — 3 versions stale.** | Med-High (listing confirmed; .xlsx bytes not downloaded) |
| **India** generation/fuel mix | state/station, **monthly** | per-state monthly mix | **OPEN** | Ember India monthly CSV (direct: `files.ember-energy.org/public-downloads/india_monthly_full_release_long_format.csv`, CC-BY-4.0, 36 states, →Jan 2026) + CEA National Power Portal state/station Excel (`npp.gov.in/publishedReports`, →Jul 2026). | High |
| **EU** generation/carbon | bidding zone/country, **hourly** | aggregate hourly→monthly per zone | **FREE-REGISTER** | **ENTSO-E Transparency Platform** — account + **manual email approval to transparency@entsoe.eu (~3 business days)** for REST API token. XML API / CSV UI. | Med-High (approval flow verified) |
| harmonising glue | US state/EU country/India state, monthly | cross-check to primaries | **OPEN** | Ember (multi-region monthly). Convenience only; cite the primaries. | High |
| calibration | US national, annual | sanity-check bottom-up US sum | **OPEN** | **LBNL 2024 US DC Energy Report** — **176 TWh (2023)**, projected **325–580 TWh (2028)**. `eta-publications.lbl.gov/.../lbnl-2024-...report_1.pdf` | High |

### C · Carbon — marginal / locational *(feeds S2-marginal · Ceiling · US/UK only)*

| Component | Native granularity | Access | Verified source — **corrected** | Confidence |
|---|---|---|---|---|
| US marginal (MOER) | balancing authority, hourly | **FREE-REGISTER (corrected)** | **The plain WattTime free tier is NO LONGER sufficient** — raw MOER is paywalled outside CAISO_NORTH. The real free path is **GridEmissionsData.io** (WattTime × REsurety, launched Mar 2025): free data-use agreement, **hourly marginal, by node/region, 3 yrs history, CSV**. Free *average*-only fallback: **Open Grid Emissions** (Singularity, CC-BY, no login). EPA AVERT = scenario tool, not raw MOER. | Med-High (WattTime limits verified; GridEmissionsData.io corroborated, not directly loaded) |
| UK marginal | national + 14 DNO regions, 30-min | **OPEN** | **UK Carbon Intensity API** `api.carbonintensity.org.uk` — no key, CC-BY, back to 2017. | High |
| EU / India marginal | — | — | No open marginal source → **average EF + stated-conservative + LMCE-style sensitivity.** Scope limit stated explicitly. | High |

### D · Water — physical coefficients *(feeds S3 · Floor)*

| Component | Native granularity | Reconciliation | Access | Verified source | Confidence |
|---|---|---|---|---|---|
| **Scope-2 EWIF** (power-plant water) | per generation tech × cooling type | applied via each zone-month's fuel mix | **OPEN** | **Macknick et al. 2012** (ERL 7 045802; DOI 10.1088/1748-9326/7/4/045802). Tables **confirmed extractable** (NREL mirror `nrc.gov/docs/ML1428/ML14286A088.pdf`). Sample (gal/MWh, recirculating consumption / tower withdrawal): coal 687/1005 · NGCC 198/253 · nuclear 672/1101 · solar-PV 26/– · wind 0/–. | High |
| **Scope-1 WUE + PUE** (on-site cooling) | fleet-average (self-reported) | facility inherits provider/climate-adjusted WUE; carry wide S9 band | **OPEN (fleet only)** | Microsoft **PUE 1.17 / WUE 0.27** (FY25) · Meta **1.08 / 0.19** (2024) · AWS **1.14 / 0.12** (2025) · **Google PUE 1.09 but publishes NO fleet WUE ratio** (aggregate water volume only). | High |

> **★ Google WUE asymmetry (state in paper):** three of four hyperscalers publish a fleet WUE; **Google does not.** Google's water footprint must therefore be **derived/estimated**, not disclosed — flag this explicitly rather than presenting all four as equivalently sourced. All four are **fleet-average only**; none publish per-facility WUE.

### E · Water — scarcity & basin context *(feeds S4 / S5)*

| Component | Native granularity | Reconciliation | Access | Verified source | Confidence |
|---|---|---|---|---|---|
| **Scarcity weight** (S4, Floor) | watershed (HydroBASINS), **monthly** | facility→watershed-month AWARE factor, **separate column, never blended** | **OPEN** | **AWARE (WULCA)** — AWARE2.0 (Apr 2025, Zenodo `10.5281/zenodo.15133241`): `AWARE20_Native_CFs.xlsx` (4.4MB, monthly+annual basin), country-aggregated + subnational xlsx, basin polygons (.gpkg). AWARE 1.2 (Jun 2024) also live. | High |
| **Groundwater context — India** (S5, context only) | assessment unit (block/mandal), periodic | basin/block depletion flag; **never facility attribution** | **OPEN** | **CGWB "Dynamic Ground Water Resources of India 2024"** — **6,746 assessment units** (block-level). PDF (cgwb.gov.in / CDN mirror) + OpenCity CSV mirror (taluk-level categories). CGWB site nav is stale; use direct/CDN link. | High (report); IN-GRES portal self-service NOT CONFIRMED |
| **Groundwater context — US/EU** (S5, context only) | GRACE mascon (~100,000 km²) | basin scale only | **OPEN** | GRACE/G3P (context overlay only, per locked scope). | Med |
| cross-check | sub-basin, static | sanity map only | **OPEN (form speed-bump)** | WRI Aqueduct 4.0 (Aug 2023; direct-zip vs form path unverified). Cross-check only. | Med |

### F · Geospatial layers *(feeds S0 · Floor · Step 1 — pull first)*

| Layer | Access | Verified source | Confidence |
|---|---|---|---|
| Watershed polygons | **OPEN** | **HydroBASINS** v1c `hydrosheds.org/products/hydrobasins` — per-region zips (`hybas_as/na/eu_lev01-12_v1c.zip`), shapefile, all 12 levels. | High |
| Admin boundaries | **OPEN** | **GADM v4.1** (India/US/EU, multiple sub-levels; **non-commercial license — flag if redistributing**) + **Natural Earth** (public domain, Admin-0/1). | High |
| US grid-zone polygons | **OPEN** | **EPA eGRID subregion shapefiles** `epa.gov/egrid/egrid-mapping-files` (2023). For balancing authorities: **EIA US Energy Atlas** (primary; **HIFLD Open portal shut down Aug 26 2025**) + NASA/DataLumos mirror as fallback. | High (eGRID); Med (BA export format) |
| AWARE watershed polygons | **OPEN** | bundled with AWARE2.0 (.gpkg/.kmz). | High |

### G · Inference attribution *(feeds S1 · Floor)*

| Component | Access | Verified source | Confidence |
|---|---|---|---|
| Per-inference power benchmark | **OPEN** | **MLPerf Inference v5.1** (MLCommons, Sep 10 2025) — public results table, includes system power/energy since v1.0. Interactive table (not bulk CSV). | High (availability); Med (v5.1 specifics) |
| Per-query energy (triangulation) | **OPEN** | Google Gemini median **0.24 Wh** (arXiv 2508.15734) · Epoch AI GPT-4o **~0.3 Wh** · *"How Hungry is AI?"* **~0.42 Wh** (arXiv 2505.09598 — **distinct academic paper, NOT Epoch; cite separately**). | High |
| Sectoral inference share | **DERIVE (factor)** | ~80–90% operational share (LBNL/IEA), transparent, sensitivity-tested. No facility partition exists. | Med (by design) |

### H · Policy & regulation *(feeds S10 / S7 · Floor map, Ceiling levers)*

| Component | Access | Verified source | Confidence |
|---|---|---|---|
| EU rule | **OPEN (text)** | **EU Delegated Reg 2024/1364** (CELEX:32024R1364) — ≥500 kW DCs report energy+water annually from Sep 2024. **BUT facility-level reported data is CONFIDENTIAL — only aggregates public.** We cite the *requirement*; we cannot extract EU facility data from it. | High |
| US patchwork | **OPEN + PAYWALL** | **datacenterbans.com** (OPEN, 451 bills/48 states, LegiScan-sourced, actively maintained — the most usable open tracker) · Sierra Club "DC State Policies 2026" (OPEN, a policy *guide*, not a bill tracker) · MultiState (free summaries; granular tracker paywalled). | High |
| India policy | **OPEN** | CEEW + government policy notes. | Med |

### I · Growth + forecast inputs *(feeds S11 / S7 · Ceiling only)*

| Component | Access | Note | Confidence |
|---|---|---|---|
| Historical carbon/demand series | **OPEN** | Ember/eGRID/CEA series (already in B) → feed SARIMA/xLSTM/TimesFM/Chronos for **regional** demand + grid-EF projection only. | High |
| Growth scenarios | **DERIVE (synthetic, declared)** | announced pipelines (India ~81 upcoming) + population/economic proxies; quarantined to Ceiling. | Med |
| Future water | **OPEN** | published Aqueduct 2030/2050 projections (scenario layer; **no site-level water forecast**). | Med |

---

## 3. Accessibility risk ranking (the forensic view — where acquisition breaks)

Ordered by how likely each is to block the paper, worst first:

1. **✅ India facility locations (Step 2) — WAS ★★★, NOW LARGELY RESOLVED.** A v0 open facility list (194 sourced rows, ~1.37 GW operational, validated vs CEEW ~1.5 GW) is built (`data/India_DC_Facilities_v0.xlsx`). Residual work is enrichment, not existence: geocode per-facility lat/lon, fill ~60 "unknown" capacities. India is now buildable. *(This was the single biggest risk; it is retired.)*
2. **★★ US facility locations — now the #1 remaining location risk.** NREL 2025 map is not downloadable; PNNL is *modeled/projected* siting, not a real inventory; the "existing DC" dataset is unverified. If needed, replicate the India web-DERIVE approach for US operators (Equinix/Digital Realty/QTS/CoreWeave/Vantage etc.).
3. **★★ US marginal carbon (Ceiling).** The "WattTime free tier" our docs assumed is now insufficient; the real free path is GridEmissionsData.io (free but a data-use-agreement step, and not directly loadable from this cloud env). Bounded because it's Ceiling — average + sensitivity is the honest fallback.
4. **★ ENTSO-E manual approval (~3 business days).** EU carbon needs a human-approved token. **Start registration on Day 1 or EU slips** regardless of anything else.
5. **★ EU facility-level energy/water is confidential** under 2024/1364 — only aggregates are public. Constrains EU to descriptive/average, as already scoped.
6. **· Minor:** Google WUE not disclosed (derive + flag); GADM non-commercial license (fine for a paper, flag on redistribution); HIFLD shutdown (mitigated by EIA/NASA mirror); CEA/Ember non-static URLs (minor scripting).

**Everything not on this list is OPEN and low-risk.** The carbon-average spine, water coefficients, scarcity weights, geospatial layers, inference benchmarks, and policy text are all free, verified, and pullable now. **The risk is concentrated almost entirely in facility locations.**

---

## 4. The gather sequence — who does what, in what order

**Claude can pull NOW (OPEN, verified, no blocker) — the whole non-location spine:**
- Geospatial: HydroBASINS (as/na/eu), GADM (IN/US/EU), Natural Earth, EPA eGRID subregion shapefiles.
- Carbon-avg: eGRID2023 xlsx, CEA v21 xlsx, Ember India monthly CSV, CEA NPP state reports.
- Water: Macknick EWIF table (full), AWARE2.0 bundle, hyperscaler WUE/PUE (captured).
- Scarcity/context: CGWB 2024 (PDF + OpenCity CSV).
- Inference: MLPerf v5.1 + per-query figures (captured), sectoral share factor.
- Policy: EU Reg 2024/1364 text, datacenterbans.com, Sierra Club PDF, CEEW report.
- Calibration: LBNL 2024 figures (captured).

**Register now (free, but start early because of lead time):**
- **ENTSO-E** REST API (manual ~3-day approval) — do Day 1.
- **GridEmissionsData.io** data-use agreement (Ceiling; US marginal).
- (WattTime API free tier — only CAISO_NORTH raw MOER; mostly superseded by the above.)

**Done / in-hand:**
- **India facility list** — ✅ v0 built (`data/India_DC_Facilities_v0.xlsx`, 194 rows). Enrichment (geocoding, unknown capacities) is the only remaining India-location work.

**Still needs a decision / user action:**
- **US facility locations** — verify the PNNL "existing DC" dataset; else replicate the India web-DERIVE for US operators + use PNNL modeled as a scenario layer.
- **How deep to enrich India** — geocode + capacity-fill all 194, or focus the deep analysis on the well-covered hubs (Mumbai/Navi Mumbai, Chennai, Bengaluru, Pune, Noida-Delhi, Hyderabad).

---

## 5. The decision the data forces (India facilities) — ✅ EXECUTED: Path 1

**Update 2026-09-14:** we ran **Path 1 (hand-curate)** immediately and it succeeded beyond expectation — a 194-row open, sourced facility list now exists (`data/India_DC_Facilities_v0.xlsx`), with operational capacity validated against the independent CEEW aggregate. India is buildable, the openness pillar is served, and the "which strategy" decision below is now mostly moot — Path 1 delivered. What remains is a lighter choice: **how deep to geocode/enrich** (all 194 rows vs. focus the deep analysis on the well-covered hubs). The original options are kept below for the record.

The verification had shown: **we could not assume a clean public India facility dataset.** Three honest paths, every one still yielding a real paper:

1. **Hand-curate the India facility layer (DERIVE).** Build it from the free aggregates (CEEW/JLL/Anarock city-level MW + shares) cross-checked against named-facility press/Wikipedia mentions and the browsable DataCenterMap directory. Transparent, reproducible, openly disclosed as a curated set with coverage % — and *itself* a contribution (the openness pillar). Cost: real manual hours; coverage will be partial.
2. **Obtain a gated commercial report** (Arizton / ResearchAndMarkets) for the facility rows, disclose that it was purchased/accessed. Fastest to "complete," but breaks the open-reproducible pillar and costs money.
3. **Narrow India to its best-covered hubs** (Mumbai-MMR, Chennai, Hyderabad, Bengaluru) as a focused sub-national case study rather than a national panel. Smallest, most defensible, most checkable — and still the first sub-national inference-attributed joint carbon-water account for India.

**Recommendation:** Path 1 + Path 3 combined — hand-curate, but scope the deep analysis to the well-covered hubs and label national numbers as coverage-bounded. It preserves openness, matches the "India-deep on a checkable set" build principle, and turns the data gap into a stated methodological choice instead of a hidden weakness.

---

## 6. Corrections this verification forces (feed to `00_PROJECT_STATE.md §9 anti-noise)

- **CEA CO₂ Baseline is v21.0 (Aug 2026), not "v19"** — our docs are 3 versions stale.
- **"WattTime/REsurety free platform" is imprecise** — plain WattTime free tier no longer gives raw MOER outside CAISO_NORTH; the free path is **GridEmissionsData.io**; Open Grid Emissions is the free *average* fallback.
- **No free India facility-level dataset exists** — the "~132 hand-verified" set is unconfirmed and may be a paywalled-report headline. Treat India locations as DERIVE until proven otherwise.
- **NREL "US DC Infrastructure 2025" is not downloadable** (static image); PNNL IM3 is *modeled* siting, not a real inventory.
- **EU facility-level data under 2024/1364 is confidential** — cite the rule, don't expect facility rows.
- **HIFLD Open portal shut down Aug 26 2025** — use EIA Atlas + NASA/DataLumos mirror for BA polygons.
- **LBNL calibration figure = 176 TWh (2023), 325–580 TWh (2028).**
- **Google publishes no fleet WUE** — its water is derived, not disclosed.
- Cite **"How Hungry is AI?" (arXiv 2505.09598)** and **Epoch AI** as *separate* per-query sources, not one.


---
## PART B — Reliability rubric & keep/drop/replace reasoning

> # ✅ CURRENT — but two specifics are superseded (banner added 2026-09-15).
> The **reliability rubric, keep/drop/replace logic, and reasons remain valid.** **CORRECTED by `DATA_REQUIREMENTS_AND_ACQUISITION.md` (verified 2026-09-14):** (1) **India carbon = CEA CO₂ Baseline v21.0** (Aug 2026), NOT "v19." (2) **India locations:** the "curated ~132-facility, hand-verified" set below was an inherited paywalled-report **headline**, not rows we possessed — it is **superseded by our own open bottom-up list** `data/India_DC_Facilities_v0.xlsx` (194 sourced rows, ~1.37 GW operational, validated vs CEEW ~1.5 GW). Trust the acquisition doc on both.

# Dataset Reliability Analysis — Keep / Drop / Replace, With Reasons

*Compiled 2026-09-13. Principle: **reliability beats quantity.** For each thing we need to measure, we want **one authoritative primary source** (plus a cross-check), not a pile of overlapping datasets. Every decision — keep or drop — carries a reason. Our original datasets are put on trial alongside the alternatives, and each choice is checked against what the credible accounting papers actually use.*

---

## 1. The reliability rubric (how each dataset is judged)

A dataset scores on seven things. A **PRIMARY** source should be strong on 1–3; convenience/cross-check sources can be weaker.

1. **Authority / provenance** — official statistical agency > peer-reviewed research product > established NGO/think-tank > commercial > crowdsourced/scraped.
2. **Literature endorsement** — do Siddik, Guidi-Dominici, LBNL, Macknick, WCI actually use it?
3. **Documented methodology** — is there a transparent, reproducible method doc?
4. **Coverage** — US / EU / India, sub-national, and our time window?
5. **Granularity fit** — does it slot into facility-month accounting without force-fitting?
6. **Open & reproducible** — free to obtain and cite (the paper must be reproducible)?
7. **Known-uncertainty transparency** — are biases/limits documented?

**Roles a dataset can be assigned:** **PRIMARY** (the number we use) · **CONVENIENCE** (harmonised aggregator of primaries; cross-check to primary) · **CROSS-CHECK** (secondary validation) · **CONTEXT** (qualitative overlay, never enters the footprint number) · **DROP**.

---

## 2. Our ORIGINAL datasets, on trial

*(From `dataset.xlsx` and the old repo. This is the "test our originals" pass.)*

| Original dataset | Verdict | Reason |
|---|---|---|
| **EPA eGRID** | **KEEP — PRIMARY (US carbon)** | Official EPA product; the gold standard for US sub-national grid emission factors; used by Siddik. Only weakness: annual + ~2-yr lag (acceptable for accounting). |
| **EPA GHG Emission Factors Hub** | **KEEP — supporting** | Official fuel-level EFs; supports the EWIF×fuel-mix step. |
| **Ember (US / EU / India)** | **KEEP — CONVENIENCE** | Well-documented aggregator that **harmonises EIA (US), ENTSO-E (EU), CEA (India)** into one monthly multi-region series — exactly our need. But it is *derived*, so we **cross-check to the primaries** and cite them. |
| **ENTSO-E Transparency Platform** | **KEEP — PRIMARY (EU electricity/carbon)** | Official EU TSO data; the ground truth Ember-EU is built from. |
| **WRI Aqueduct 4.0** | **DEMOTE → CROSS-CHECK** | Widely recognised, but it is a **risk *index*, static baseline**, not a quantitative scarcity measure — and we mis-used it as if temporal before. Replaced as the scarcity *weight* by AWARE (§3); kept only as a recognisable sanity map. |
| **Aqueduct water-stress projections** | **DROP (for the core)** | Future 2030/50/80 projections aren't needed to account for *current* burden; would add noise. (Optional far-future context only.) |
| **GRACE / G3P (groundwater)** | **KEEP — CONTEXT only** | Cannot attribute datacenter withdrawal (agriculture + climate dominate; ~100,000 km² resolution). Valid **only** as basin-depletion context, never a footprint number. For **India, CGWB is better** (§3). |
| **Electricity Maps API** | **DROP as primary → optional CROSS-CHECK** | Gated (needed a university email — the old roadblock), proprietary methodology, not fully reproducible. Its role (marginal EF) is better served by WattTime/REsurety (US) + UK API. |
| **UK Carbon Intensity API** | **KEEP — PRIMARY (UK marginal, Ceiling)** | Official (National Grid ESO), free, documented; the one open marginal source. |
| **Data Center Map / ATLAS (Ringmast4r) / Baxtel** | **DROP as primary → gap-filler CROSS-CHECK** | Crowdsourced/scraped, **no methodology, no provenance** — the weakest link in the old work; Guidi & Chen deliberately used SEC/S&P instead. Replaced by PNNL-IM3 + NREL (US) and CEEW (India). |
| **Aterio / poidata (India), commercial** | **DROP** | Paid, closed, unverifiable — fails openness/reproducibility. |
| **LBNL 2024 US DC Energy Report** | **KEEP — CALIBRATION/VALIDATION** | Authoritative national bottom-up census; use its national totals to **sanity-check** our bottom-up sum (does our US total land near LBNL's?). |
| **NITI / ICED load curve (India)** | **DROP (for accounting)** | A demand curve, not an accounting input; India carbon/EF comes from CEA. |
| **MLPerf Inference (MLCommons)** | **KEEP — PRIMARY (inference energy)** | Authoritative, transparent industry benchmark for per-inference power. |
| **GEOJSONs (Survey of India / raw GitHub)** | **KEEP but standardise** | Fine, but prefer **GADM / Natural Earth** for consistent, citable admin boundaries across all three regions. |
| **Open-Meteo temperature (snapshot)** | **DROP** | Was a GAT node feature; irrelevant to accounting. (WUE seasonality, if needed, comes from provider/climate data, not a live snapshot.) |

---

## 3. The finalized reliable set (by need) — primary + cross-check, with reasons

**① Datacenter locations**
- **PRIMARY (US):** **PNNL IM3 Projected US Data Center Locations** (OSTI) + **NREL "US Data Center Infrastructure, Nov 2025."** *Reason: research-grade, open, documented — replaces the scraped maps that were our weak point.*
- **PRIMARY (India):** **CEEW** analysis + the curated ~132-facility market set, **hand-verified**. *Reason: small, concentrated N is fully checkable; CEEW is a credible domestic institution.*
- **CROSS-CHECK:** Data Center Map (gap-fill only); SEC EDGAR/S&P if accessible. *Reason: fills holes but never the sole source.*
- **EU:** curated hub list (Dublin/Frankfurt/Amsterdam/Paris…) hand-verified against Data Center Map + EUDCA. *Reason: EU DCs cluster in a few known hubs — hand-verifiable; EU is the lower-priority region.*

**② Electricity & carbon intensity (average)**
- **PRIMARY:** **EPA eGRID** (US, subregion) · **ENTSO-E** (EU) · **CEA CO₂ Baseline Database v19** (India — India's official grid-EF product, the analogue of eGRID). *Reason: official agencies, used/citable, sub-national.*
- **CONVENIENCE:** **Ember** monthly (harmonised US/EU/India), cross-checked to the three primaries. *Reason: one clean multi-region monthly series; saves plumbing, but not ground truth.*
- **CALIBRATION:** LBNL 2024 (US national total). 

**③ Marginal carbon (Ceiling)**
- **PRIMARY:** **WattTime/REsurety free platform** (US, balancing-authority) + **UK Carbon Intensity API** (UK). *Reason: the only credible + (now) free marginal sources; WattTime is validated and widely cited. EU/India have no open marginal → those stay average + stated as conservative.*

**④ Water — physical coefficients**
- **PRIMARY (scope-2 EWIF):** **Macknick et al. 2012** (NREL/ERL) — withdrawal + consumption per generation technology. *Reason: THE peer-reviewed standard; used by Siddik and Making-AI-Less-Thirsty.*
- **PRIMARY-ish (scope-1 WUE + PUE):** hyperscaler sustainability disclosures (Google/Microsoft/Meta) + Uptime Institute averages. *Reason: the only sources that exist; self-reported → carry an explicit uncertainty band (S9).* 

**⑤ Water — scarcity & stress**
- **PRIMARY (scarcity weight):** **AWARE (WULCA)** — monthly, watershed, global. *Reason: peer-reviewed LCA standard; monthly; used by Balancing Bits & Drops. Replaces static Aqueduct as the quantitative weight.*
- **CROSS-CHECK:** WRI Aqueduct 4.0 (recognisable baseline map).
- **CONTEXT (groundwater depletion):** **GRACE/G3P** (US/EU basins) + **CGWB Ground Water Resource Assessment** (India, block-level official). *Reason: CGWB is official Indian ground truth at far finer resolution than GRACE — for India, prefer CGWB; GRACE only where CGWB-equivalents don't exist. Both are context, never attribution.*

**⑥ Inference attribution**
- **PRIMARY:** **MLPerf Inference** + peer-reviewed measurement (Luccioni "Power Hungry"). **FACTOR:** sectoral inference share (~80–90% operational, LBNL/IEA) with a range. *Reason: authoritative benchmarks; the share is a transparent, sensitivity-tested factor (no facility partition exists).* 

**⑦ Geospatial layers**
- **PRIMARY:** **HydroBASINS** (watersheds) · EPA eGRID-subregion + EIA/HIFLD balancing-authority shapefiles · AWARE watershed polygons · **GADM/Natural Earth** admin boundaries. *Reason: established, citable boundary products; consistent across regions.*

**⑧ Policy / regulation (for S10)**
- **PRIMARY:** EU Delegated Reg **2024/1364** + EU draft rating scheme (official). **TRACKERS:** Sierra Club "DC State Policies 2026," MultiState/ArentFox, datacenterbans.com, large-load tariff filings (US patchwork). **India:** CEEW + government policy. *Reason: official for EU; reputable trackers are the accepted way to map the US patchwork; CEEW for India.*

**⑨ Growth scenarios (Ceiling only)**
- Announced pipelines (India 81 upcoming; US/EU announcements) + population/economic proxies — **declared synthetic**, sensitivity-tested. *Reason: no real workload data exists; must be transparent and bounded.*

---

## 4. What we DROP, consolidated (negative decisions need reasons too)

| Dropped | Reason |
|---|---|
| Scraped/commercial DC maps as *primary* (ATLAS, Baxtel, Aterio, poidata) | No methodology/provenance; not reproducible; better research-grade sources exist. |
| Electricity Maps API as *primary* | Gated + proprietary; the old roadblock; replaced by WattTime + UK API. |
| Aqueduct as the scarcity *weight* | A static risk index, not a quantitative monthly scarcity measure; AWARE is the scientific standard. |
| Aqueduct future projections (core) | Not needed to account for current burden. |
| GRACE as a footprint *number* | Cannot attribute DC withdrawal; agriculture/climate-dominated; coarse. Context only. |
| NITI load curve, Open-Meteo snapshot | Not accounting inputs. |
| "More is better" instinct | Overlapping datasets add noise + reconciliation cost; one authoritative primary per need is more defensible and more reproducible. |

---

## 5. The reliability upgrades this analysis buys us (vs the old work)

1. **DC locations:** scraped maps → **PNNL-IM3 + NREL** (US, research-grade) + **CEEW hand-verified** (India). *Fixes the single weakest, least-reproducible input.*
2. **India carbon:** Ember-India → **CEA CO₂ Baseline v19** (official primary).
3. **India groundwater/stress:** GRACE (coarse) → **CGWB block-level** official assessment.
4. **Water scarcity:** static Aqueduct → **AWARE monthly** (LCA standard).
5. **Marginal carbon:** gated Electricity Maps → **free WattTime + UK API.**
6. **Every primary is official or peer-reviewed and open** → the paper is fully reproducible, which is itself a contribution this venue values.

---

## 6. Residual reliability caveats (state these in the paper, don't hide them)

- **Scope-1 WUE / PUE are self-reported** by operators → widen their uncertainty band; report sensitivity.
- **Marginal EF is US/UK only** → EU/India results are average-based and stated as conservative.
- **DC-location sets are never perfectly complete** → report coverage %, and show regional aggregates are robust to plausible missing-facility noise.
- **AWARE (normative scarcity weight) ≠ physical water** → always report physical m³ first, scarcity-weighted as a separate labelled layer (no frankenmetric).
- **Ember is derived** → cross-checked to EIA/ENTSO-E/CEA; discrepancies logged.

---

## 7. One-line summary

**Use official or peer-reviewed, open primaries — eGRID/ENTSO-E/CEA (carbon), Macknick (scope-2 water), provider WUE (scope-1), AWARE (scarcity), MLPerf (inference), PNNL-IM3/NREL/CEEW (locations), CGWB (India groundwater), WattTime/UK (marginal) — with Ember as the harmonising glue and GRACE/Aqueduct as context/cross-check only. Drop everything scraped, gated, or redundant. Fewer, stronger, reproducible.**

---
## PART C — Data-adequacy audit vs the literature + the counterfactual (2026-09-26)

*Triggered by the direction pivot (G6+G1+G5+G3, see `RESEARCH_GAPS.md`). Question: with the papers + notebooks as evidence, do we have enough data, what do we need more, and were the GAT datasets "at fault"?*

### C1. Our accounting stack MATCHES the reference stack (papers confirm data-completeness)
Every serious joint carbon+water account uses the same recipe, and we match or beat it on every input:

| Component | Siddik'21 | Guidi (Harvard) | Li "Thirsty" | Small-Bottle | **Ours** |
|---|---|---|---|---|---|
| Facility loc. | HUC-8 | BA (SEC/S&P) | country-avg | US mixes | India v0 + curate |
| Carbon EF | grid EF | **eGRID plant** | grid EF | grid | eGRID/CEA/Ember/ENTSO-E |
| Scope-2 water | **Macknick** | I_grid·E | **EWIF 3.14** | indirect | **Macknick** |
| Scope-1 water | on-site WUE | WUE·(E/PUE) | WUE·PUE | direct | provider WUE + PUE |
| Scarcity | stress overlay | Aqueduct | none | Aqueduct BWS | **AWARE monthly (best)** |

→ **No paper uses a dataset we lack.** The account is data-complete; our scarcity layer (AWARE monthly) is ahead of the field's static Aqueduct.

### C2. Adequacy verdict by category
- **Carbon — ENOUGH** (sub-national, open). **Water coeffs — ENOUGH.** **Scarcity — ENOUGH / best-in-class.**
- **Facility locations — PARTIAL** (India v0 ok; US weak; EU curate).
- **Facility CAPACITY — THE GAP** (atlas none; 40/194 India uncosted). Drives the whole account → #1 bottleneck.

### C3. What we need MORE of
- **(a) Capacity** — deepest need; gates L2.
- **(b) Real US inventory** — PNNL is *modeled*, NREL not downloadable → replicate the India web-DERIVE for US operators.
- **(c) NEW — policy-lever parameters (introduced by G6, not needed by a pure account):** seawater-cooling WUE (coastal-siting lever), ZLD recycling efficiency, PUE-standard distributions, disclosure-coverage assumptions. **New acquisition task the pivot creates — verify in Phase-0; a lever that can't be quantified drops from L3.**
- **(d) Optional sharpener — cooling type per facility** (evaporative/air/seawater). No paper has it (all use fleet-avg WUE); if obtained it upgrades both the water account and the siting lever → a potential *data contribution*.
- **(e) Utilisation / load-factor priors** (energy = capacity × utilisation × PUE) — modeled assumption, sensitivity-tested.

### C4. Were the GAT datasets "at fault"? — method-primary, data-granularity-ENABLED
The null's proximate cause was method (autoencoder→post-hoc blend), but the **root enabler was a data-granularity mismatch**: node features were **static** (stress climatology, one temp snapshot, 12-mo mean E/CO₂); there is **no facility-level time series** (Ember=state/country, water=basin); the water target (G3P TWS, nearest-centroid 2500 km) was too coarse to attribute to a facility. The project **asked the data for facility-level dynamics it does not have** (DCs don't publish per-facility monthly energy/water) → the task was ill-posed.
→ **The data was adequate data used for the wrong task, not bad data.**

### C5. The clever consequence (why the same data is fine for us)
Our account computes facility footprint from **static capacity × region-level intensity × coefficient** — exactly Siddik/Guidi/Li's method. It demands only what the data provides. **The data that sank the GAT is adequate for the account, because the account asks less of it.** Lesson banked: respect native granularity; never force facility-level dynamics onto region-level data.

### C6. Smart moves
1. **LLM-based capacity extraction is literature-backed** (Chen 2604.06198 "LLM extraction of disclosures"; Guidi used SEC/S&P) → our optional L0 LLM node has precedent; doing it reproducibly is itself a contribution.
2. **Upgrade India provenance toward the Guidi standard** (operator disclosures/filings over scraped/trade press) where feasible.
3. **Lever-parameter sourcing (C3-c) joins Phase-0 verification.**

---
## PART D — ON-DISK REALITY: what we ACTUALLY have vs what we claimed (physical repo audit + live web-verification, 2026-09-26)

> Triggered by PI: *"even the datasets we claim to have, we don't have — check the repo."* Correct. This part = the physical file census + a live-internet verification of every real file. **All 8 datasets below were profiled from disk (columns/rows/coverage) AND their provenance/currency web-checked on 2026-09-26.**

### D1. What is PHYSICALLY on disk (verified)
| Dataset (file) | What it really is (web-verified) | Currency | Role |
|---|---|---|---|
| **Ember** EU/India/US monthly long-format | Real Ember (CC-BY-4.0); **India 2019–2025, 83 mo, state-level incl. CO₂-intensity + fuel mix**; US 2001–2025 (300 mo) | ours end Nov/Dec 2025; **latest release 28 Jul 2026 → re-download** | **carbon + fuel-mix, PRIMARY-usable** (harmonizes EIA/ENTSO-E/CEA) |
| **Aqueduct 4.0** annual/monthly/future (Y2023M07D05) | Real WRI Aqueduct 4.0 (Aug 2023, CC-BY); 68,510 basins; incl. `w_awr_elp` (electric-power-weighted) + monthly bws | **current** (4.0 is latest, ~5-yr cycle) | **scarcity/stress** (what Small-Bottle/Guidi used; ≠ AWARE but legit) |
| **G3P v1.12** rivbas/aquifers/clireg | Real GFZ G3P (Güntner 2024, GRACE/-FO); **04/2002–09/2023 monthly**; DOI 10.5880/g3p.2024.001 | current (2025 update pending) | **CONTEXT only** (can't attribute DC withdrawal) |
| **ATLAS datacenters** (Ringmast4r, parquet+csv) | Scraped OSINT; 18,110 DCs; **coords city-level → fallback state/country centroid**; **342 India rows, NO capacity** | rolling GitHub | **locations gap-filler/cross-check** (city-coords OK for basin/state joins, not siting) |
| **GEM Global Integrated Power** (Mar 2026 v.II) | Real GEM (launched Jun 2024); power-*plant* units: capacity/fuel/status/geo | ours Mar 2026; **Aug 2026 release exists**; needs correct-sheet parse | **grid/fossil-share context** (not DCs) |
| **ElectricityMaps** (CH-2023 daily, 365 rows) | **Demo/sample file only** (Switzerland 2023) | n/a | **NOT real data** — no EM coverage held |
| **India_DC_Facilities_v0.xlsx** (ours) | 194 rows; capacity_mw + cea_grid_region + confidence + source_url; **no lat/lon** | 2026-09-14 | **India facility PRIMARY (our build)** — needs geocoding + 40 uncosted |

### D2. Claim-vs-reality gap — the "primaries" that are NOT on disk (all OPEN, retrieval paths web-verified today)
- **eGRID2023** (US carbon) — epa.gov/egrid. · **CEA CO₂ Baseline v21.0** (India carbon) — **confirmed current** (Nov 2025, FY24-25; `cea.nic.in/.../User_Guide_V_21.0.pdf`). · **ENTSO-E** (EU carbon, register). · **Macknick 2012 EWIF** (scope-2 water) — ERL 10.1088/1748-9326/7/4/045802 (tables to extract). · **AWARE 2.0** (scarcity weight) — **confirmed Zenodo 10.5281/zenodo.15133241** (native monthly+basin). · **HydroBASINS / GADM / eGRID shapefiles** (geospatial) — none held. · **CGWB 2024** (India groundwater, block-level) — none held (have coarse G3P). · **MLPerf v5.1** (inference) — none held. · **Marginal carbon** (WattTime/GridEmissions/UK) — none held.

### D3. Honest verdict
- **We do NOT have the stack the docs describe.** We hold a *working subset* (Ember carbon + Aqueduct scarcity + our India facilities + Macknick-to-retrieve) that **is enough to build a first India account**, plus context (G3P, GEM) and a locations gap-filler (ATLAS).
- **Retrieval is the real L0 task**, not "we have it": CEA v21, eGRID, AWARE2.0, Macknick, HydroBASINS, MLPerf, CGWB — all open, none blocking.
- **Precise facility geolocation is a genuine gap** (ATLAS = city-centroid; our list = none) — adequate for basin/state joins, not siting; flag in methods.
- **Marginal carbon not held** (EM is a demo) → stays Ceiling + retrieve.

### D4. Corrections forced (→ `00_PROJECT_STATE.md §6`)
1. "We have the reliable primary stack" = **FALSE**; we have the old GAT stack; primaries un-retrieved (all open).
2. **Ember is on disk and PRIMARY-usable** for carbon (Parts A/B under-rated it as "convenience").
3. Scarcity on disk = **Aqueduct**, not AWARE → decision: build on Aqueduct now / upgrade to AWARE / use both.
4. ATLAS coords = **city-centroid**; our India list has **no coords** → geocoding is a real gap, not "enrichment."
5. Ember + GEM copies are months stale → re-download before final build.
6. **⚠️ CEA v22.0 EXISTS** (data 2026-08-01, released Sep 2026) — corrects the repeated "v22 doesn't exist yet" claim.

### PART G — Achievability re-check: were the red-team compromises forced? (2026-09-26)
*Checked lit-rev + web. Two big compromises are RECOVERABLE (not forced); two are genuinely forced.*
| Compromise | Recoverable? | Real source / evidence | Cost |
|---|---|---|---|
| India carbon = coarse regional-annual (gen-vs-consumption error) | **YES** | **Electricity Maps** India *regional* zones (IN, IN-EA…), **consumption-based (import-adjusted)**, 15-min/real-time → fixes the error + adds temporal. **EnergyMap.in** = CI for all 36 states/UTs + 4 regional grids, live+historical. | EM API key (only demo held); verify EnergyMap access/history |
| Scope-2 water not basin-localisable (only scope-1 rigorous) | **YES — field standard** | **Reiss/Diaz ERL 2021** (scope-2 water at HUC-8); **Guidi** facility→BA→HydroBASINS→Aqueduct; **LBNL "Water IMPACT Tool"** = BA-resolved **consumption-based** water intensity (open, HydroShare). Attribute scope-2 at **generation-region basins** → restores scarcity-weighting to FULL water (scope-1 + scope-2). | US = use LBNL tool; India = build equivalent (regional mix→GEM plants→basins) |
| Inference per-facility | **NO (forced)** | no dataset separates inference per facility (confirmed) | — |
| 2030 projection as forecast | **NO (forced)** | 7-yr extrapolation = scenario inherently; short-horizon forecast remains real | — |
| Counterfactual non-conditional | **PARTLY** | engineering params real (seawater WUE, ZLD 90-95%, PUE trade-off); operator adoption stays conditional | — |
**→ Net:** consumption-correct temporal India carbon + full-water (scope-1+2) scarcity-weighting are **achievable** (Ceiling), recovering most of the six-axis ambition. **New Phase-0 checks:** EM/EnergyMap access + India history depth; LBNL Water IMPACT tool loadability + India-equivalent feasibility.
**New sources to retrieve:** Electricity Maps API (India regional), EnergyMap.in (India state/regional CI), LBNL Water IMPACT Tool (US scope-2 water), Reiss/Diaz ERL 2021 (method).

### D5. RETRIEVED so far (2026-09-26) → `data/` at repo root
- **`data/aware/`** — AWARE 2.0 (Zenodo 10.5281/zenodo.15133241): `AWARE20_Native_CFs.xlsx` (**per-basin MONTHLY Jan–Dec CFs — verified**), `..._geospatial.gpkg` (basin polygons for point-in-polygon), `..._Subnational_Resolution.xlsx`, `..._Countries_and_Regions.xlsx`. **This IS the scarcity-weight upgrade (monthly, watershed) Parts A/B wanted — replaces Aqueduct as the WEIGHT.**
- **`data/macknick/`** — `Macknick2012_ERL.pdf` (IOP open-access); scope-2 water consumption/withdrawal tables to extract at build.
- **`data/cea/`** — `CEA_Database_V22.xlsx` (**CURRENT**: plant-level Data + Results GEF + Assumptions fuel-EFs, data 2026-08-01) + V22 guide; `CEA_Database_V21.xlsx` + V21 guide (continuity).
- **`data/egrid/egrid2023_data_rev2.xlsx`** — EPA eGRID2023 rev2 (Jun 2025), US subregion carbon primary (21 MB; PK-valid).
- **`data/ember_refresh/india_monthly_full_release_long_format.csv`** — Ember India, current. **⚠️ correction: India Ember is NOT stale — the latest public coverage ends 2025-11** (same as our GAT copy); Nov 2025 is simply Ember's latest India month. (US/EU refresh still worth doing but lower priority.)
- **`data/gadm/`** — GADM 4.1 India (52 MB) + USA (113 MB) admin polygons (gpkg), for facility→state/country joins (grid-zone assignment).
- **`data/cgwb/`** — CGWB Dynamic Groundwater 2024: **12 CSVs** (India national + Maharashtra/Tamil Nadu/Karnataka/Telangana/Delhi/Gujarat/Goa + major-cities + unit categorisation). ⚠️ these are **state/city SUMMARY tables**; the full block-level (6,746 units) detail is in the source PDF (on OpenCity). India groundwater **context**.
- **`data/mlperf/SOURCES.md`** — inference-energy **reference note only** (deliberately no bulk dataset: inference share is a transparent scalar; per-query figures cited from lit review).
- **HydroBASINS — DEFERRED (not downloaded):** Asia bundle alone is **376 MB** (~1 GB all regions), **redundant with AWARE's `AWARE20_Native_CFs_geospatial.gpkg`** (basin polygons keyed to monthly CFs = our facility→basin scarcity-join layer). Pull only if a finer watershed delineation is later needed.
- **OLD-PROJECT DATA copied into `data/`** (2026-09-26, per PI): `data/ember/` (US+EU+India monthly), `data/atlas/` (facility coords parquet+csv), `data/aqueduct/` (annual+monthly water-stress cross-check + electric-power risk), `data/g3p/` (river-basin groundwater context), `data/gem/` (power-plant context). → `data/` is now the single consolidated data home (~600 MB, 11 sources).
- **Still to retrieve (open, non-blocking):** ENTSO-E (EU carbon upgrade — register); marginal carbon (Ceiling, US/UK); US/EU Ember + GEM refresh (India already current).

---
## PART E — DATA VALIDATION: file-content + granularity compatibility + independent gap hunt (2026-09-26)

*Every file opened and confirmed to BE the data (not error page / readme / empty); native granularity checked against the account's atomic unit (**facility-month**); then an unbiased web hunt for missing data. Goal: don't repeat the GAT granularity mistake, and add no new ones.*

### E1. File-content verification — ALL confirmed real data
| File | Opened & confirmed | Native granularity |
|---|---|---|
| `egrid/egrid2023_data_rev2.xlsx` | 11 sheets: PLNT/GEN/UNT/ST/BA/**SRL23** — real EFs | subregion (27) + state + plant, **annual** |
| `cea/CEA_Database_V22.xlsx` | Data (plant units) + Results (**GEF table by year**) + Assumptions (fuel EFs) | **all-India, annual** GEF (wtd-avg + build/op/combined margin); plant-level capacity |
| `ember/*.csv` | India/US = **state**-monthly w/ CO₂ intensity; EU = **country**-monthly | India 36 states, US states, **EU country-only**; monthly |
| `aware/AWARE20_Native_CFs_geospatial.gpkg` | **11,661 basin polygons + Basin_ID + CF_Jan…CF_Dec embedded** | basin (watershed), **monthly** |
| `aware/AWARE20_Native_CFs.xlsx` | Basin_ID + Jan–Dec + annual | basin, monthly |
| `gadm/gadm41_IND.gpkg` | ADM_1=**41 states**, ADM_2=676 districts | admin state + district |
| `gem/…March-2026-II.xlsx` | "**Power facilities**" sheet, 52 cols (Capacity MW/Status/fuel/geo) | power-plant unit |
| `cgwb/*.csv` | national=per-State; state files=per-District; categorisation=safe/critical counts | state + district |
| `macknick/…ERL.pdf` | ✅ IOP open-access (tables to extract at build) | per generation-tech (US) |
| `aqueduct/…annual/monthly.csv` | 68,510 basins incl. `w_awr_elp` | basin (pfaf), static annual + monthly-typical |
| `g3p/*_rivbas.csv` | ~100 river basins, monthly TWS anomaly | basin, monthly (context) |
| `atlas/datacenters.parquet` | 18,110 rows; 6,131 coords | facility point (**city-centroid**) |

### E2. Granularity compatibility matrix (native → account-need → reconciles?)
| Layer | Native | Account needs | Reconciles? |
|---|---|---|---|
| Carbon India | Ember **state-monthly** (generation-mix) | facility→state→zone-month intensity | ✅ apply zone intensity to facility (not forecast) |
| Carbon US | eGRID **subregion-annual** OR Ember **state-monthly** | facility→zone→intensity | ⚠️ **two geographies** (subregion≠state) — pick one (see E3) |
| Carbon EU | Ember **country-monthly ONLY** | facility→country | ✅ but **no EU sub-national possible** → EU stays "light" |
| Scarcity | AWARE **basin-monthly** (gpkg polygons) | facility→basin→monthly CF | ✅ **perfect fit** (point-in-polygon on the gpkg) |
| Scope-2 water | Macknick **per-tech** (US) | tech-coeff × zone fuel-mix (Ember) → zone-month | ✅ (⚠️ US coeffs applied to IN/EU — representativeness caveat) |
| Scope-1 water | provider **fleet-average** WUE | facility-inherited constant | ✅ w/ wide S9 uncertainty band (coarse, honest) |
| Groundwater ctx | CGWB state+district / G3P basin | context flag only, never attribution | ✅ context |
| Facilities | our list = point (no coords); ATLAS = city-centroid | facility→state + facility→basin | ⚠️ **geocoding gap** — city-centroid OK for basin/state joins, not siting |

### E3. Mistakes AVOIDED + reconciliation decisions to lock
- **GAT mistake NOT repeated:** we **apply** zone-level intensity to facilities (standard accounting), never **forecast** facility-level dynamics on region data. Atomic unit = facility-month; each resource keeps native partition; facility is the join key (never down-force).
- **EU is country-only** → do **not** claim EU sub-national carbon; EU stays descriptive/light. (Not a mistake if scoped; a mistake if over-claimed.)
- **US carbon geography — DECISION:** use **Ember state-monthly** as the working intensity (consistent with India, monthly), and **eGRID subregion-annual** as the US cross-check/calibration. Do NOT silently mix subregion and state.
- **India carbon = generation-mix proxy** (Ember state), NOT consumption/marginal (synchronous grid); CEA GEF is all-India annual. State this limit; carbon is a supporting sub-national signal, **water carries the primary India sub-national novelty.**
- **Macknick = US coefficients** applied to IN/EU fuel mixes → representativeness caveat + sensitivity band.
- **Scope-1 WUE = fleet-average**, not facility → wide uncertainty band, report sensitivity.

### E4. Independent gap hunt (unbiased) — what's genuinely missing
1. **India sub-national/marginal carbon — nothing better exists.** Ember state-monthly is the ceiling; POSOCO/Grid-India gives only **daily regional** generation (5 grids, from 2013), no hourly CO₂ API. India has no marginal-carbon source (unlike UK/EU/US). → confirmed scoping, not a retrievable gap. *(Optional: POSOCO regional-daily as a temporal cross-check.)*
2. **Cooling type / water source per facility — NO dataset exists** (confirmed; 75–90% use evaporative). → this is a **MODELED assumption/typology**, not data. Flag explicitly; it drives the coastal-siting lever + water precision.
3. **Per-facility utilisation / IT load — no data** → modeled parameter (× capacity × PUE), sensitivity-tested.
4. **India facility list — no open structured dataset;** ours remains best. **Latest aggregate = 1,789 MW operational, 147 DCs, 33 operators (JLL H1 2026)** → our 194-row/~1,373 MW list is now **~77% of current operational capacity** (was ~90% vs the older 1.5 GW) → **top-up needed** (India kept building in 2026).

### E5. NEW data the counterfactual (G6) needs — SOURCEABLE (record, not download)
Lever parameters found in engineering/industry literature (cite, not a dataset):
- **WUE baseline** ≈ **1.9 L/kWh** avg (range 1–9); **efficient ≈ 0.7 L/kWh** (NREL, PUE 1.06) — for the efficiency-standard lever.
- **ZLD / closed-loop:** consumes only ~**5–10%** of withdrawal, returns ~**90–95%** as wastewater; Microsoft closed-loop "**zero-water evaporation**" design — for the ZLD lever.
- **Seawater / WSAC cooling:** dramatically less freshwater (Google Hamina); freshwater only for periodic salt flush — for the coastal-siting lever.
- **PUE:** evaporative→mechanical raises PUE; liquid/immersion **PUE ≈ 1.2 or lower** — trade-off to model (water↓ but energy/carbon↑).
> These make the G6 counterfactual **parameterisable now** — the levers can be quantified. **Phase-0 item #5 (lever params) is substantially satisfied**; formalize the exact values + sources at build.

---
## PART F — CROSS-DATASET JOIN COMPATIBILITY + sectioned inventory + POLICY status (2026-09-26)

*"Does every dataset join to every other dataset it must?" — verified join keys on disk. Then datasets sectioned by use. Then the policy-data gap.*

### F1. Cross-dataset JOIN matrix (verified keys)
| Join (A ⋈ B) | Key / mechanism | Status |
|---|---|---|
| Facility ⋈ Ember carbon | grid_zone = **state name** | ✅ after alias resolver (our real states match Ember; only 'multiple'/'undisclosed' placeholders don't) |
| Facility ⋈ AWARE scarcity | **lat/lon → point-in-polygon on AWARE `.gpkg` → Basin_ID → monthly CF** | ✅ direct (gpkg carries geometry + CFs); needs facility coords |
| Facility ⋈ GADM state | lat/lon → point-in-polygon (ADM_1) | ✅ needs coords |
| Facility ⋈ CEA | state name (+ plant-name fuzzy) | ✅ state; plant match fuzzy |
| Facility ⋈ CGWB | state (national CSV) / district (state CSVs) | ✅ state; district needs coords |
| Ember fuel ⋈ Macknick EWIF | **fuel-category name** | ✅ clean crosswalk (Coal→coal, Gas→NGCC, Nuclear, Solar→PV, Wind→0, Hydro, Bioenergy; 'Other Fossil/Renewables'→default) |
| Ember-US(state) ⋈ eGRID(subregion) | state vs eGRID subregion | ⚠️ **geography mismatch** — subregions ≠ states → use Ember-state as working intensity, eGRID as cross-check (never mix silently) |
| Ember-India(state) ⋈ CEA(all-India) | state vs national | ⚠️ different grain — Ember = sub-national signal, CEA = national anchor/calibration |
| **AWARE ⋈ Aqueduct** | Basin_ID (2–78541) vs pfaf_id (6-digit) | ❌ **ZERO overlap — NOT joinable by key.** Different basin delineations → parallel systems, compare spatially only |
| AWARE ⋈ G3P | Basin_ID vs river-basin **name** | ❌ not key-joinable; G3P stays context-only |
| Temporal (all) | month | ✅ BUT **scarcity CF = climatological-monthly (12 vals, no year)** while **carbon = actual dated monthly** — state this; don't imply year-specific scarcity |

### F2. Two CRITICAL cross-compat findings (would have caused silent errors)
1. **AWARE Basin_ID ≠ Aqueduct pfaf_id (0 overlap).** The scarcity join **must** go through AWARE's own polygons (point-in-polygon on the gpkg), **not** via Aqueduct pfaf_id. AWARE and Aqueduct are independent basin systems → a facility gets *two different* basin assignments; use **AWARE for the weight**, Aqueduct only as a spatial cross-check.
2. **Aqueduct CSVs on disk have NO geometry** (attributes by pfaf_id only; the polygon **GDB was not copied**). → Aqueduct is **not spatially joinable to facilities** without retrieving its GDB. **AWARE gpkg covers the scarcity need**, so Aqueduct cross-check is optional (retrieve GDB only if we want the electric-power-weighted `w_awr_elp` per facility).
3. **State-name resolver required** (Ember/GADM/CEA/CGWB spellings differ: delhi, merged UTs, ladakh, aggregates) → reuse the salvaged geocoder's exact→alias→fuzzy(0.82) resolver.

### F3. DATASETS SECTIONED BY USE (what each is FOR)
- **§ FACILITIES (L0/L1 — the spine):** `India_DC_Facilities_v0.xlsx` (PRIMARY: capacity+state, needs coords) · `atlas/` (coords gap-filler, city-centroid) · `cea/` Data sheet (plant capacity cross-check) · `gadm/` (facility→state polygons).
- **§ CARBON (L2):** `ember/` (PRIMARY sub-national: state/country-monthly intensity + fuel mix) · `cea/` Results (India national annual GEF — anchor) · `egrid/` (US subregion/state annual — cross-check). *(ENTSO-E = EU upgrade, un-retrieved.)*
- **§ WATER-PHYSICAL (L2):** `macknick/` (PRIMARY scope-2 EWIF per tech) · provider WUE/PUE (scope-1 fleet-avg, in-doc not a file) · `ember/` fuel-mix (input to EWIF×mix).
- **§ WATER-SCARCITY (L2 weight):** `aware/` (PRIMARY WEIGHT: monthly basin CF + polygons) · `aqueduct/` (CROSS-CHECK only; ⚠️ no geometry on disk).
- **§ GROUNDWATER/BASIN CONTEXT (L5):** `cgwb/` (India state+district) · `g3p/` (basin TWS anomaly, US/EU).
- **§ GRID CONTEXT:** `gem/` (power-plant capacity/fuel/status — structural fossil-share).
- **§ INFERENCE FACTOR (L2):** `mlperf/SOURCES.md` (reference figures; transparent scalar, no bulk data).
- **§ LEVER PARAMETERS (L3/G6):** engineering-lit values (PART E5) — not a dataset.
- **§ POLICY (L5/G5) — see F4.**

### F4. POLICY DATA — the honest status (currently ANALYSIS-ONLY, no data files on disk)
- **HAVE:** `POLICY_DEEP_DIVE.md` — the four-axis regulatory-gap **analysis** (US/EU/India), triple-confirmed. This IS the reg-gap frame's backbone.
- **MISSING as retrievable data/text:**
  - **EU Delegated Reg 2024/1364** — the rule text (for citation + the EU KPI list PUE/WUE/ERF/REF). Qualitative; retrieve the CELEX text.
  - **US patchwork — `datacenterbans.com`** (LegiScan-sourced, **451 bills / 48 states**) — the one **STRUCTURED** policy dataset worth retrieving as data (feeds the US side of the gradient + lever realism).
  - **India** — CEEW report + state DC-policy compilation (~15 state policies; mostly qualitative PDFs).
- **Verdict:** the policy layer is **mostly qualitative** (regulation texts → the gap analysis, already done in POLICY_DEEP_DIVE). Only **datacenterbans.com** is a structured dataset. **Action: retrieve the EU Reg text + the datacenterbans.com tracker; India policies stay qualitative citations.** Policy is NOT a blocker (analysis exists), but the *source texts/tracker aren't on disk yet.*

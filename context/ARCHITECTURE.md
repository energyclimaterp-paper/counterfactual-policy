# Architecture — The Plan, Explained

*Compiled 2026-09-13. The implementation blueprint for the paper, written to be **understood**: every dataset and every stage leads with its **purpose** (what it's for), then the technical in/out. The policy layer is built in. Floor = guaranteed part of the paper; Ceiling = ambitious add-ons, each behind a gate.*

> **Corrections (2026-09-20) — trust `00_PROJECT_STATE.md` over any stale detail below:** India = **194-facility open list** (`data/India_DC_Facilities_v0.xlsx`), not "~132"; **CEA CO₂ Baseline = v21.0** (not v22); India carbon is **regional-annual-average only** (5 grids) → India's *sub-national* signal rides on **water** (AWARE monthly + CGWB), not carbon. S11 reuses the prior forecast models honestly (see `GNN_AUTOPSY.md`).

---

## The whole thing in one paragraph

Think of it as an **assembly line that produces an itemised carbon-and-water "bill" for AI, broken down by place — and then checks that bill against the law.** Raw materials go in one end (where datacenters physically are, how dirty the local electricity is, how much water each kilowatt-hour costs, and whether that water comes from a stressed place). Out the other end comes: a **map of AI's coupled carbon and water burden across the US, EU, and India**, a **read on who bears it**, a comparison against **what regulation currently exists where** (revealing the gaps), and — if time allows — a **projection of that bill forward** and a quantified answer to **"which policy levers actually lower it."** The core map (the Floor) is **calculated from sourced numbers**, nothing predicted or "learned." The forward-looking part (the Ceiling) is where the carried-forward time-series models do one bounded job — projecting **regional electricity demand and grid carbon** — and never the site-level water forecasting that failed before. Every number, computed or projected, is stamped with an uncertainty range.

```
 RAW DATA                     THE ENGINE (calculate today)                  WHAT COMES OUT
 ────────                     ────────────────────────────                  ─────────────
 A where DCs are  ─┐
 F map layers    ─┘─► S0 JOIN ──► S1 ENERGY ──► S2 CARBON  ─┐
 E inference share                   │           S3 WATER   ─┤─► S6 MAP+TABLES ──► ★ FLOOR: TODAY'S burden map
 B grid emissions ──────────────────┘           S4 SCARCITY─┤        │
 C water coeffs                                  S5 BASIN   ─┘        ├─► S10 POLICY GAP MAP ──► ★ FLOOR: regulatory gaps
 D scarcity/stress                                                    │
 H policy/regulation ────────────────────────────────────────────────┘
                                              (today's burden = the baseline the forecast grows from)
                                                                     │
 ═══ THE ENGINE (project forward) ═══════════════════════════════════▼════════════════════════════════
 I forecast models ─┐                                                                    ☆ CEILING:
  SARIMA·xLSTM·     ├─► future ELECTRICITY demand  ─┐                                     future burden map,
  TimesFM·Chronos   │   + future GRID CARBON        ├─► S11 FORWARD ──► S7 LEVERS ──► S8   what each lever saves,
 G growth scenarios ┘   (WATER: no forecast —       │   PROJECTION                 BURDEN  who pays
                         published 2030/50 stress)  ┘
 ─────────────────────────────────────────────────────────────────────────────────────────────────────
 S9 UNCERTAINTY wraps every stage (today and forward) ──► ± ranges on every number
```

**Mini-glossary** (so the stages read cleanly): **EF** = emission factor, how much CO₂ per kWh of electricity (gCO₂/kWh). **average vs marginal EF** = the grid's *typical* dirtiness vs the dirtiness of the *next* unit of demand you add (marginal is what actually changes when a datacenter switches on). **WUE** = on-site cooling water per kWh. **EWIF** = water used by the *power plants* per kWh. **PUE** = facility overhead multiplier (total power ÷ IT power). **AWARE** = a 0–100 "how scarce is water here this month" weight. **GRACE** = a satellite that sees whether a whole region's groundwater is shrinking.

---

## Part 1 — The datasets (what each is *for*)

**A · Datacenter facilities — the spine.**
*Purpose:* the list of **where AI physically runs.** Every number in the paper hangs off a facility. Curated, quality-checked, a few hundred sites (not thousands): US subset, EU hubs, India's **194-facility open list** (129 operational, `data/India_DC_Facilities_v0.xlsx` — built bottom-up, validated vs CEEW ~1.5 GW; not geocoded yet).

**B · Grid electricity & carbon intensity.**
*Purpose:* turns a facility's **kWh into CO₂**, by place and month. Average EF for all regions (Ember, eGRID); *marginal* EF for the US/UK only (WattTime/REsurety, UK Carbon Intensity API) — the honest "next-unit" number.

**C · Water coefficients (the litres engine).**
*Purpose:* turns **kWh into litres.** Two paths: on-site cooling (**WUE**, from hyperscaler disclosures) and off-site power-plant water (**EWIF** × the grid's fuel mix, from Macknick 2012). Plus **PUE** for overhead.

**D · Water scarcity & stress (separate layers, never merged into the litres).**
*Purpose:* answers **"do those litres come from a place that can spare them?"** **AWARE** (monthly, watershed) is the scarcity weight; **Aqueduct** is a cross-check; **GRACE** shows whether the whole basin's groundwater is already shrinking — used only as *context*, never to claim "this datacenter drained this aquifer."

**E · Inference attribution.**
*Purpose:* isolates the **AI-inference slice** of a datacenter's footprint. No dataset splits a building's energy into inference vs training, so this is a transparent **share factor** (~80–90% of operational AI energy, with a range), plus per-query energy (MLPerf, provider disclosures).

**F · Geospatial layers.**
*Purpose:* the **maps that place each facility** inside its grid zone, its watershed, and its GRACE basin — so we can attach the right B/C/D numbers to each site.

**G · Growth scenarios (Ceiling only).**
*Purpose:* plausible **futures for where new AI capacity gets built** — used only by the forward projection (S11) and the "what-if" counterfactual (S7). Built from announced pipelines (India's 81 upcoming, US/EU announcements) + population/economic proxies. **Declared synthetic**; the Floor uses none of it.

**I · Forecast models — our own carried-forward assets (Ceiling only).**
*Purpose:* project the **two things the models were genuinely good at** — a region's future **electricity demand** and its future **grid carbon intensity** — from historical time series. This is the honest home for the models from the prior work: **SARIMA** (the statistical baseline), **xLSTM**, **TimesFM**, and **Chronos** (note: the prior repo's "Nexus" was found to be Chronos-2 — see the forensic flags — so it is not a separate model). *What they do NOT touch:* no site-level water forecasting, no graph fusion, no request-routing — those are exactly the moves that produced the null result. They forecast **regional carbon/electricity only**; future **water** stress comes from **published Aqueduct 2030/2050 projections**, not from a model we fit. Inputs: the historical Ember/eGRID/CEA carbon+demand series (B). Output: per-region monthly forecasts of demand and grid EF, with backtested error bands, feeding S11.

**H · Policy & regulation (the new layer).**
*Purpose:* **what rules exist where** — so we can find the gaps. EU Delegated Regulation **2024/1364** (mandatory DC energy+water reporting) + the EU draft rating scheme; US **state patchwork** (Sierra Club / MultiState trackers, moratorium list, large-load tariffs); India (CEEW + nascent policy). This is the *coverage* layer S10 overlays on the burden map, and it *defines the levers* S7 tests.

---

## Part 2 — The pipeline stages (purpose first)

### S0 — Join *(Floor · build this first — it's the critical path)*
**Purpose:** stamp every facility with the three regions it lives in (grid zone, watershed, basin). This is the one step that quietly killed the last project, so it's step one.
**In → Out:** facilities (A) + polygons (F) → `facility_master.parquet` (one row per facility + its region tags).
**Think of it as:** giving every datacenter its home addresses on three different maps at once.

### S1 — Energy *(Floor)*
**Purpose:** work out how much electricity each facility uses per month, and how much of that is **AI inference**.
**In → Out:** facility_master + capacity/PUE/inference-share (E) → `facility_energy.parquet` (facility×month → kWh, inference-attributed).
**Think of it as:** the electricity meter, with the AI-inference portion highlighted.

### S2 — Carbon *(Floor: average · Ceiling: marginal)*
**Purpose:** convert that electricity into CO₂, using local grid dirtiness.
**In → Out:** facility_energy + grid EF (B) → `carbon.parquet` (kgCO₂e_average, and kgCO₂e_marginal for US/UK).
**Think of it as:** multiplying the meter by "how dirty is the plug here."

### S3 — Water (physical) *(Floor)*
**Purpose:** convert electricity into **actual litres** — cooling water on-site + power-plant water off-site. This physical number is the paper's primary water figure.
**In → Out:** facility_energy + WUE/EWIF/PUE (C) → `water_physical.parquet` (m³ scope-1, scope-2, total).
**Think of it as:** the water meter — real litres, before any judgement about scarcity.

### S4 — Scarcity weighting *(Floor · kept separate)*
**Purpose:** re-express those litres as **"stress-adjusted"** — a litre in the Arizona desert counts for more than a litre in Norway. Reported as its **own column**, never added into the physical m³ (no frankenmetric).
**In → Out:** water_physical + AWARE (D) → `water_scarcity.parquet`.
**Think of it as:** a second, separate scoreboard that weights litres by how scarce they are.

### S5 — Basin context *(Ceiling · context only)*
**Purpose:** flag whether a facility sits in a basin that GRACE independently shows is **losing groundwater** — an honest "risk overlay," not a claim that the datacenter caused it.
**In → Out:** water_physical (basin tag) + GRACE (D) → `basin_context.parquet` (depletion flag + trend).
**Think of it as:** a warning sticker: "this water is being drawn from a shrinking well."

### S6 — Aggregate + map *(Floor · ★ the core result)*
**Purpose:** roll facility-months up to regions and draw the maps — the paper's central figures and tables.
**In → Out:** carbon + water_physical + water_scarcity + basin_context → `region_tables.csv` + choropleth maps.
**Think of it as:** turning millions of rows into the handful of maps and tables a reader actually sees.

### S11 — Forward projection / scenario engine *(Ceiling · ☆ · runs after S6, feeds S7 — the home for our carried-forward models)*
**Purpose:** take today's burden map (S6) and **project it forward** to a future year, so the policy levers (S7) are evaluated against tomorrow's AI, not just today's. This is where the prior work's time-series models finally earn their place — doing the one job they did well (~2–8% backtest error): forecasting a region's **electricity demand** and its **grid carbon intensity**. The forecasts combine with the growth scenarios (G, where new capacity lands) to grow the facility base forward.
**The guardrail (why this is not a repeat of the failure):** we forecast **carbon and electricity only**. We do **not** forecast water at site level — future water stress comes from **published Aqueduct 2030/2050 projections**, applied as a scenario layer, because site-level water forecasting is precisely what broke last time. No graph fusion, no routing, no site-level demand model. Targets are **regional, not per-facility**. Every forecast carries its backtested error band into S9.
**In → Out:** region_tables (S6 baseline) + forecast models (I) on the historical carbon/demand series (B) + growth scenarios (G) + Aqueduct future water → `projected_burden.parquet` (region×future-year → projected carbon, physical water, scarcity-weighted water, with forecast uncertainty).
**Think of it as:** taking today's bill and asking "what does this bill look like in 2030 if demand and the grid evolve the way the models project and new datacenters land where the pipeline says" — then handing that projected bill to the policy step.

### S7 — Policy-lever counterfactual *(Ceiling · ☆ — restructured to be policy, not physics)*
**Purpose:** answer **"which real policy lever lowers the bill, and by how much?"** Each scenario is an *actual instrument*, not an abstract reallocation: (a) siting restriction in high-scarcity basins, (b) marginal-EF-based siting incentive, (c) mandatory WUE/PUE standard, (d) growth cap / moratorium, (e) 24/7 clean-energy procurement. Latency-safe: it allocates **future growth**, regionally (you don't serve a US user from India). It operates on the **projected** future burden from S11, so "avoided" is measured against a forecast baseline, not a frozen snapshot.
**In → Out:** projected_burden (S11) + growth scenarios (G) + lever definitions (H) → `lever_deltas.csv` (avoided carbon + scarcity-water **per lever**).
**Think of it as:** running the projected tape forward under each proposed law and measuring the difference.

### S8 — Burden / equity *(Ceiling · ☆ · diagnostic only)*
**Purpose:** show **who currently bears the burden** — does it land on already-stressed or disadvantaged regions? Descriptive, never "keep AI out of India."
**In → Out:** region_tables + basin_context + population → `burden_dist.csv` + distribution plots.
**Think of it as:** checking whether the bill is being paid by the people who ordered the meal.

### S9 — Uncertainty *(Floor · wraps everything)*
**Purpose:** put an honest **± range** on every number, so no phantom precision (the "548" lesson). Every coefficient carries a distribution; we resample.
**In → Out:** all factor distributions → Monte-Carlo (≥2000 draws) → confidence bands appended to every output.
**Think of it as:** repeating the whole calculation thousands of times with slightly different inputs to see how much the answer wobbles.

### S10 — Policy translation & gap map *(Floor: the map + framing · Ceiling: the lever recommendations)*
**Purpose:** the venue-critical layer. Overlay the **burden map** on the **regulation-coverage map** to expose **where high burden meets no rule**; frame the whole accounting method as the **disclosure standard** the EU is formalising and the US/India lack; position the dataset as an **IPCC AR7 input.** If S7 ran, attach **quantified lever recommendations**.
**In → Out:** S6 burden + S8 distribution + policy dataset (H) → `regulatory_gap_map` (burden × coverage choropleth) + a lever-recommendation table → the paper's Policy/Discussion sections.
**Think of it as:** laying the "who's hurting" map over the "who's regulated" map and circling the places that are both hurting and unregulated.

---

## Part 3 — Floor vs Ceiling at a glance

| | **FLOOR — guaranteed by 31 Dec (no single point of failure)** | **CEILING — ambitious, each gated** |
|---|---|---|
| Stages | S0–S6, S9, **+ the S10 gap-map & disclosure framing** | S2-marginal, S5, **S11 forward projection**, S7, S8, S10-lever-recommendations |
| Claim | *"First sub-national **joint carbon-water** footprint of AI datacenters across **US/EU/India**, inference-attributed, reported as physical + scarcity layers with uncertainty — plus a **regulatory-gap analysis** against the real (asymmetric) policy landscape, offered as an open disclosure standard and an AR7 input."* | *"…and marginal-emissions correction re-ranks clean US regions; siting/tariff/procurement **levers** could avoid X carbon and Y stress-water; and the burden concentrates on already-stressed basins."* |
| Gate | — | WattTime access (marginal); RQ2 ranking moves; time budget; India data depth; **forecast backtest error stays low enough to be decision-relevant (S11)** |

**The Floor is a genuine *Energy and Climate Change* paper on its own** — accounting + policy-gap + disclosure-standard + AR7 framing. The Ceiling makes it ambitious. The abstract is written **last**, once we know how much ceiling we earned.

*A parallel **engineered-novelty ladder** (E0–E3) rides alongside this, gated on the same checkpoints — see **Part 5**. E0 (reproducible-by-construction + S0/S9 method reframe) is a Floor habit from Day 1; E1–E3 are earned rung by rung.*

---

## Part 4 — Why this isn't a repeat (of others, or of ourselves)

**Not the same as the field:** Siddik (US-only, average, all-DC) → we add EU+India, inference-attribution, marginal, forward levers. Guidi/Dominici (US carbon and water, *separate*) → joint + multi-region. Balancing Bits & Drops (US per-period *scheduler*) → accounting + policy, multi-region, physical-first. eGLB (synthetic optimizer) → real-data diagnostic. The *Patterns* Perspective *calls for* this; we execute it.

**Not the same mistakes as us:** facility-month atomic unit with native partitions (no site→zone collapse); the **Floor contains no forecasting at all** — it is arithmetic on sourced coefficients, so nothing sits at a "naive floor"; forecasting reappears **only in the Ceiling (S11)**, doing the one job the models did well (regional demand + grid carbon, ~2–8% error) and explicitly **not** the jobs that failed (no site-level water forecast, no graph fusion, no routing); GRACE at basin-context only (no coarse-basin false precision); physical m³ primary with scarcity/context as *separate* layers (no frankenmetric); every factor sourced with a distribution (no phantom numbers); synthetic demand quarantined to the Ceiling.

**Where the carried-forward models go (so nothing is wasted):** the prior work built SARIMA/xLSTM/TimesFM/Chronos forecasters. Rather than discard them, S11 uses them for **regional carbon and electricity projection** — a legitimate, venue-appropriate use (IPCC AR7 is forward-looking) that reuses the existing benchmark honestly, while the guardrails above keep them away from the failure modes.

**The one real risk is S0 (the join).** Everything on the Floor is arithmetic on sourced coefficients. So S0 is built and stress-tested first; S11 and the rest of the Ceiling only run once the Floor stands.

---

## Part 5 — The engineered-novelty ladder *(gated · added step-by-step based on what we achieve)*

*Decision locked 2026-09-14. The paper's primary contribution is the **empirical account** (the India numbers, the joint conjunction, the gap map). This ladder adds **engineered-artifact novelty on the axis this venue actually rewards** — reproducibility, transparency, and decision-relevance — **not** algorithmic/systems cleverness. That distinction is deliberate: anything that makes the tool **predict, optimize, route, or schedule** is explicitly out (it re-imports the saturated-literature + null-result risk we killed). Each rung is gated at the same checkpoints as the Floor/Ceiling and added only once the rung below it stands. **Honest ceiling on all of it: the artifact amplifies the paper, it does not carry it — a weak India result is not saved by a nice tool. Floor result first, always.***

**The novelty framing (state it exactly this way — bounded, not inflated):** *"the first **open, reproducible instrument** for sub-national, inference-attributed, joint marginal-carbon + scarcity-weighted-water accounting of AI datacenters."* This is an **artifact/method** contribution, **not** a claim of novel software engineering. "First / unoccupied" is high-confidence but **bounded by our ~84-paper sweep** (final check: the 27 Sep T3 re-sweep). Never write "novel system" unqualified — it invites a reviewer to puncture a systems claim we are not making.

| Rung | What it is | Cost | Gate (when it goes in) |
|---|---|---|---|
| **E0 — Reproducible-by-construction + method reframe** | (a) Build S0–S11 as **clean, scripted, seed-fixed, version-controlled** code from Day 1 — reproducibility is a *habit*, not a Day-16 retrofit. (b) In the writeup, elevate two things already built as explicit **methodological contributions**: **S9** = *joint* Monte-Carlo uncertainty propagated through energy→carbon→water→scarcity together (most prior work reports carbon *or* water point estimates); **S0** = a reusable *sub-national geospatial attribution layer* (facility→grid-zone→watershed→basin), non-trivial precisely for India's messier data. | **Near-zero** (byproduct of building the Floor at all) | **Floor · from Day 1.** Not deferred — retrofitting reproducibility later is expensive, so the hooks go in immediately even though the *claim* is only cashed once results exist. |
| **E1 — Reproducibility harness** | One documented command (Makefile / notebook / container) that **regenerates every number and figure from raw public inputs**. The "reproduce-all" release most of this field lacks. | Low (E0 makes it mostly assembly) | **Gated on ★ Day 6** (India Floor works) — built as India lands, extended per region. |
| **E2 — Released, versioned, installable instrument** | Polish the pipeline into a **named, versioned, installable** package with a README + data dictionary, so a third party can run the account on **their own** facility set. This is the headline artifact contribution + the openness pillar made concrete. | Medium (real packaging/docs work) | **Gated on ★ Day 11** (Floor stands multi-region, time to spare). |
| **E3 — Interactive decision-map / dashboard** | A web artifact where a policymaker filters by region/basin and sees per-facility/per-basin carbon + physical water + scarcity-weighted water — decision-relevance made tangible and shareable. | Highest (nice-to-have, not load-bearing) | **Top rung — only if EU is dropped/thin AND Floor lands early.** First thing cut under time pressure. |

**How this maps to the fallback ladder:** E0 ships in every outcome (it costs nothing extra and it *is* the openness pillar). E1 ships in every outcome where the Floor exists at all. E2 and E3 are earned, not assumed — they appear in the paper only if we reach their gate, and their absence is written as "released as future work," never as a shortfall. The abstract and the cover letter's contribution list are written **last**, naming only the rungs we actually earned.

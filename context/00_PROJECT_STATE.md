# 00 · PROJECT STATE — Single Source of Truth (READ FIRST)

> **This is the one authoritative file.** State, locked decisions, decision rationale, the corrections list, and the session log all live here. If any other doc disagrees with this one, this one wins. **Rewritten & consolidated 2026-09-20** (absorbed and replaced: `SESSION_LOG`, `SESSION_HANDOFF`, `DIRECTION_AND_DECISIONS`, `RED_TEAM_AUDIT`, `RUBRIC_AUDIT`, `BUILD_PLAN_16DAY`, `GAP_LANDSCAPE_AND_CFP_FIT`, `FOUNDATION_GAP_AND_POLICY`, and the old versions of this file). The GAT-repo archive docs and superseded literature/scope docs were deleted — their content is captured here, in `GNN_AUTOPSY.md`, in `LITERATURE.md`, and in the `gat-based-forecasting/` repo itself.

---

## 1. What this is (one paragraph)  ·  [reconciled 2026-09-26]

**One Q1 paper** for the Elsevier *Energy and Climate Change* special issue **"Computing and Digitalization through a Multi-Disciplinary Lens"** (Editorial Manager, "VSI: Computing and Digitalization"; **deadline 31 December 2026**; rolling; AR7-aligned; solo author, Gauri). **The paper = an open, reproducible FRAMEWORK that (1) builds a sub-national, facility-level, joint carbon + scarcity-weighted-water ACCOUNT of AI datacenters (India deep / US solid / EU light, anchored on India), (2) PROJECTS it forward (short-horizon grid-CI forecast + growth scenario), (3) quantifies what policy LEVERS would save, and (4) MAPS the cross-jurisdiction regulatory gap.** Shape: **account → project → counterfactual → policy-gap.** It is an **accounting + policy** paper — **not** routing/optimization, **not** an ML-architecture paper, **not** a multi-agent system (deterministic pipeline, by design).

**→ Contribution statement is AUTHORITATIVE in `dcfootprint/ARCHITECTURE.md §7` — nine contributions, TIERED** (Tier-1 = robust/low-assumption, carries the paper; Tier-2 = conditional/diagnostic, the reach). The old flat "six-axis" framing below (§2) is retained only as the underlying novelty *ingredients*, now mapped to those tiers.

**Where we are (2026-09-26, end of session):** direction reconciled to 9 tiered contributions; **architecture designed + scaffolded + red-teamed twice** (`dcfootprint/`, authoritative `dcfootprint/ARCHITECTURE.md`); **repo LIVE on GitHub** → `https://github.com/energyclimaterp-paper/counterfactual-policy` (code+docs; data git-ignored, retrievable via `DATA.md`); **data acquired + validated + cross-checked** (`DATA.md` D/E/F/G; real files in `data/`); **first 3 gate experiments RUN** (see Arc 6 / ARCHITECTURE §6.4). **★ Key empirical result: scarcity-weighting does NOT re-rank India's hotspots at annual level — because DCs are already sited in water-stressed basins → REFRAME the headline (Arc 6).** India facility list = v0 (194 rows; needs geocode + fill 39 uncosted + top-up ~1.8 GW). **Decisive pending test: seasonal (monthly-CF) Gate 3.** Then build the spine (`io/facilities.py`).

---

## 2. Novelty — the TIERED contributions (authoritative: `dcfootprint/ARCHITECTURE.md §7`)

**Novelty = a tiered contribution set, not a flat six-axis list.** Include everything, label its evidential tier; lead with Tier-1, reach with Tier-2.
- **TIER-1 (robust, low/no-assumption — carries the paper, Q1-solid):** **C1** first open sub-national facility-level joint carbon+scarcity-water account, India-anchored · **C3** *where + when* the scarcity-weighted burden concentrates (basins × dry-season/high-carbon months) · **C4** *does the method change the answer* (scarcity/marginal re-ranking vs average-adequate) · **C5** cross-jurisdiction four-axis regulatory-gap map (no assumptions) · **C8** open reproducible framework + released India facility dataset · **C9** joint carbon+water uncertainty propagation.
- **TIER-2 (conditional/diagnostic — the reach, gated by experiments):** **C2** full-water scarcity localisation (scope-2 at generation basins) · **C6** what levers would save (conditional scenarios + projection) · **C7** equity/distributional diagnostic.

**The six-axis ingredients** (joint C+W · marginal carbon · scarcity-weighted water · inference-attribution · sub-national multi-region incl. India · forward policy-lever + reg-gap, open) map onto those tiers: sub-national-India + scarcity + reg-gap + open = Tier-1 spine; marginal-carbon (US/UK) + full-scope-2-scarcity + counterfactual = Tier-2 reach; inference-attribution = a scoping scalar (thin, §2.1). Verified unoccupied vs 89 primary-read works; honest novelty = **integration + this conjunction + reproducibility**.

### 2.1 Honest novelty decomposition (do not oversell the flat six-axis list)

The six axes are **not equal**. Say this plainly or a sharp reviewer will:

- **LOAD-BEARING (carries the paper):** (a) the **India sub-national, facility-level joint carbon+water account** — genuinely unbuilt; (b) the **cross-jurisdiction regulatory-gap map** (the four-axis gap, triple-confirmed); (c) the **open, reproducible instrument** — the field explicitly asks for it (FAS, AGU-Privette, iScience-Hankendi) and it is the solo-team offset for institutional weight.
- **SUPPORTING (integration):** joint carbon+water across three regions, monthly trajectories, inference-framed.
- **THIN / do-not-overstate:** **marginal carbon** is Ceiling-only *and US/UK-only* (Guidi/Dominici 2411.09786 already computes US average **and** marginal); **inference-attribution** is a global sectoral scalar (~80–90%), *coarser* than the per-query papers (How Hungry is AI, WCI, SCARF) — it scopes the account, it does not discriminate between facilities.

### 2.2 Nearest neighbours and the delta against each

| Neighbour | Owns | Our delta |
|---|---|---|
| **Siddik 2021** (ERL) — closest baseline | joint carbon + AWARE scarcity water, sub-national US, siting counterfactual, annual | +India +EU +monthly +inference-framing +regulatory-gap-map +open-instrument (Floor matches their *average* carbon) |
| **Guidi/Dominici pair** (2606.05420 carbon + 2607.02531 water) | sub-national US, real facilities, scarcity water, BA-level, both resources, rudimentary water counterfactual | two *separate* single-domain papers; carbon avg-not-marginal; **no EU/India**; no inference framing; no real policy lever |
| **Bolaños-Zuñiga & Lamadrid 2026** (arXiv 2608.09882) — *new US neighbour, highest US-axis overlap; FULL-TEXT READ* | US sub-national, **marginal** generation mixes, carbon + water + land as system externalities, calls for integrated policy | **US-only** (no India/EU); water = **volumetric WUE, NOT scarcity-weighted** (full-text confirmed); carbon & water assessed **separately — no unified facility-level joint account** (confirmed); **not open** (no data/code); policy is a *call*, not a **gap-MAP**; no inference framing. → confirms **US = "solid" not "deep"**; our moat = India + scarcity-weighting + unified joint facility account + reg-gap-map + reproducibility. **All five deltas full-text-verified 2026-09-22.** |
| **Xiao 2025** (Nat. Sust.) | joint C+W, sub-national US, siting, AI-specific | marginal; scarcity; US/EU/India; inference; policy lever |
| **ThirstyFLOPS** (2510.00471) | joint carbon + genuine AWARE scarcity water | avg carbon; HPC-not-inference; no India; no policy |
| **How Hungry is AI** (2505.09598) | joint E/W/C per-inference | *out-granularizes us on inference* — our edge is sub-national + scarcity + marginal + policy, NOT inference attribution |

### 2.3 Floor vs Ceiling = Tier-1 vs Tier-2 (same idea, reconciled)

- **FLOOR = the Tier-1 spine (guaranteed, what we promise):** "first India-anchored, sub-national, facility-level joint average-carbon + **on-site**-scarcity-weighted-water account (+US/EU comparison), with a regulatory-gap map + method-sensitivity finding + uncertainty bands, open and reproducible." Nearest neighbour = Siddik 2021 + India.
- **CEILING = the Tier-2 reach (gated by the experiments):** full-water scope-2 scarcity localisation (C2), consumption-based/US-marginal carbon, forward projection + policy-lever counterfactual (C6), equity diagnostic (C7). **"marginal" / "full-water scarcity" enter the abstract headline ONLY if the gates pass** — else India/EU carbon is average and scarcity is scope-1, stated honestly.

---

## 3. Research questions (clean — re-derived 2026-09-19)

The repo's old RQs (water-as-stock, workload-reallocation, RQ2-as-ambition-switch) are **dead**. The current conjunction answers:

- **RQ1 — magnitude & distribution (T1).** How large is the AI-inference-attributed carbon and scarcity-weighted water footprint of datacenters across India, the US, and the EU at the facility-month level, and how is it distributed sub-nationally — especially across India's grid regions and water basins?
- **RQ2 — does the method change the answer? (T1).** Does weighting water by local scarcity (and, for the US, carbon by marginal vs average intensity) change *which* facilities/regions rank highest-burden — i.e., is the accounting method decision-relevant, or does the ranking barely move? *(Report either way; "average is adequate here" is a valid finding.)*
- **RQ3 — the regulatory gap (T2).** Where does the measured burden fall relative to enacted and proposed regulation in the three jurisdictions — which high-burden facility-months sit in blind spots that mandate none of {carbon intensity, marginal carbon, scarcity-weighted water, inference attribution}?
- **RQ4 — forward & levers (T3, Ceiling).** Under announced-pipeline growth, how does the burden evolve, and which forward siting/policy levers most reduce scarcity-weighted water and marginal carbon *without simply relocating* the burden?

Track fit: RQ1/RQ2 → T1; RQ3 → T2; RQ4 → T3. Lead on T1+T2; reach into T3 in the Ceiling. (Only 1 of 84 coded papers spans all three tracks — spanning them is rare, not a checkbox.)

---

## 4. Locked decisions + rationale (do NOT re-litigate)

| # | Decision | Why (rationale, distilled from the red-team + rubric + build-plan history) |
|---|---|---|
| D1 | **Direction: India-anchored multi-region joint carbon–water accounting + regulatory-gap map.** | The one open conjunction vs ~70 works; India is unbuilt, booming, water-stressed. |
| D2 | **Tiered depth: India = deep · US = solid · EU = light.** | India is the moat (and smallest/most-checkable). US has the best data but is crowded (Harvard/Guidi). EU facility-level data is confidential under Reg 2024/1364 → descriptive only. |
| D3 | **Floor-first, Ceiling gated.** | Guarantees a submittable paper with no single point of failure; the Floor is arithmetic on sourced coefficients (no forecasting/optimizer). |
| D4 | **Kill-list (see §5).** | Routing is saturated + its prize is Sukprasert-ceilinged + we already ran the ML-systems play (the GNN null) + wrong venue. |
| D5 | **Solo team → open & reproducible is a first-class contribution pillar.** | No domain-expert co-author / no institutional brand; reproducibility is the offset the venue explicitly rewards (FAS/AGU/iScience call for exactly this). |
| D6 | **Engineered-novelty ladder E0–E3, gated (reproducibility axis only).** | Adds artifact novelty on the axis the venue rewards; **never** algorithmic/systems cleverness (that re-imports the killed risk). E0 = reproducible-by-construction + reframe S9 (joint uncertainty) & S0 (sub-national attribution) as method contributions, from Day 1. E1 = one-command harness. E2 = installable instrument. E3 = interactive decision-map (top rung; **caution — Harvard is building a US version, so keep E3 India/policy-focused or cut it**). The artifact amplifies the paper; it never carries it. |
| D7 | **Time-series angle: monthly trajectories + S11 forecast visible.** | Satisfies "time series", aligns with editor Te Han, reuses the team's real strength. |
| D8 | **Atomic unit = facility-month; each resource keeps its native partition; the facility is the join key.** | The fix for the exact granularity error that sank the prior project (site→zone force-collapse). |
| D9 | **Marginal carbon = US/UK only, Ceiling.** EU/India = average + stated conservative + LMCE-style sensitivity. | No open marginal source for EU/India. |
| D10 | **India facility layer = hand-curated open list (Path 1), EXECUTED.** | No free facility dataset exists; the built list is itself a contribution + the openness pillar made concrete. |

**Red-team objections, settled (why the direction is what it is — do not reopen):** GRACE cannot attribute a facility's drawdown (→ basin context only); "inference-specific" is not measurable per facility (→ transparent sectoral factor + sensitivity); India data is thin but tractable (→ built the list, scope deep on well-covered hubs); tri-continental join is where projects die (→ build & stress-test S0 first, India-only); synthetic demand contaminates results (→ quarantined to the Ceiling counterfactual, declared); equity reads as Global-North paternalism (→ diagnostic, never prescriptive); "548" phantom (→ real, from Guidi/Dominici, cite them); AWARE+GRACE+Aqueduct don't compose (→ physical m³ primary, scarcity as a separate labelled lens, GRACE as context — no frankenmetric).

---

## 5. Scope boundaries (the kill-list)

- **No real-time routing / scheduling / load-balancing.** We account and run forward policy counterfactuals; we do not move load.
- **No new ML architecture** (no GNN / attention / RL). That was the failed prior path (see `GNN_AUTOPSY.md`).
- **GRACE / groundwater = basin context only** — never facility attribution (agriculture/climate dominate; ~100,000 km² resolution).
- **Counterfactual = forward siting / policy levers, Ceiling only** — never workload reallocation.
- **Physical litres first; AWARE scarcity as a separate labelled layer** — no frankenmetric.
- **"Inference-attributed" = transparent sectoral apportionment factor (~80–90%) with sensitivity** — not a measured per-facility partition (no dataset separates inference per facility).
- **DROPPED entirely:** water-as-irreversible-stock (N2), workload-reallocation counterfactual, RQ2-as-ambition-switch, "smaller models under operational constraints" (N/A for this journal), China (no data source ever existed).

---

## 6. Corrections / anti-noise list (single source of truth — trust this over anything)

- **Deadline = 31 December 2026** (not 30 Sep — the old "16-day crisis" is void; runway ≈ 14 weeks from 2026-09-20).
- **CEA CO₂ Baseline — ⚠️ v22.0 NOW EXISTS (corrected 2026-09-26):** the earlier "v22 doesn't exist yet, expected late 2026" is STALE — **v22.0 is published** (data dated 2026-08-01, released Sep 2026) and **retrieved** (`data/cea/CEA_Database_V22.xlsx`), alongside v21 (FY24-25). v22 `Data` sheet is plant-level (NAME/UNIT/CAPACITY/STATE/SECTOR); grid EF stays all-India+regional annual average. *(Lesson: the docs' version claims drift — verify live, as done here.)*
- **India carbon is coarse:** CEA = all-India + **5 regional grids, annual, average only** (synchronous national grid). You get **national-monthly (Ember) OR regional-annual (CEA), never regional-monthly.** → India's *sub-national* novelty is carried by **water** (AWARE monthly watershed + CGWB block + facility geography), **not carbon.** State this.
  - **⚠️ REFINEMENT (2026-09-23, from GAT-notebook autopsy — verify before relying):** Ember's India monthly file **does carry a state-level `CO2 intensity` variable**, and the prior GAT project **forecast per-state monthly carbon for 11 Indian states** (Delhi, Gujarat, Karnataka, Kerala, Maharashtra, Odisha, Rajasthan, Tamil Nadu, Telangana, UP, West Bengal — see `model_comparison_region.csv`). BUT this is a **generation-mix intensity** (a state's own fuel mix), **not consumption-based** — India's synchronous grid means a datacenter consumes regional/national power, not just its state's generation. So sub-national India carbon **is available as a generation proxy** (softening the flat "carbon is coarse" claim) **with an explicit generation-vs-consumption caveat.** Net: **both** carbon (generation-proxy) and water can carry sub-national India signal — strengthens the account; state the caveat rather than overclaiming consumption-based marginal.
- **India facilities = 194 (129 operational, ~1,373 MW), NOT "~132"** (that was a paywalled-report headline). 40/129 operational uncosted; mixed capacity bases; built from DataCenterMap/Baxtel/trade press (the sources the reliability doc demoted) — the novel core sits on the softest data; fix the 40 uncosted + normalize basis early.
- **"43% of DCs in water stress" = GLOBAL** (2020s, → ~45% by 2050s). India-specific = **"more than half" / ~60–80%** (WRI India + CEEW) — a stronger, citable India figure. *Web-verified 2026-09-19.*
- **"548 gCO₂/kWh" is REAL** — Guidi/Dominici **2411.09786** (data-center-weighted intensity, 48% above the 369 US average). Cite them, **not LBNL**. (The "phantom — purge" verdict is retracted.)
- **US federal posture is DEREGULATORY** — EO 14318 (23 Jul 2025) narrows NEPA for DCs; EO 14141 (Biden carbon-matching) **revoked**; the federal transparency bill H.R. 9825/S. 4213 is **unenacted** and PUE/WUE-only. Not just a "state patchwork."
- **CEEW "5 of 15 states embed sustainability" → really ~1–2 binding** (Rajasthan ZLD, Gujarat 51% RE); **zero** mandatory DC-specific environmental disclosure in India.
- **EU CSRD narrowed by Omnibus I Directive (EU) 2026/470** — the entity-level GHG/water disclosure that partially touched our axes just contracted.
- **US marginal carbon:** plain WattTime free tier is insufficient (CAISO_NORTH only) → **GridEmissionsData.io** (WattTime×REsurety); Open Grid Emissions = free average fallback.
- **US real-facility locations = the #1 remaining location risk** — NREL 2025 map not downloadable; PNNL IM3 = modeled siting, not a real inventory. Use Guidi/Dominici's *published* facility lists + eGRID; don't rebuild what Harvard built.
- **EU facility-level data under Reg 2024/1364 is confidential** — cite the rule, not facility rows.
- **HIFLD Open portal shut Aug 26 2025** → EIA Atlas + NASA/DataLumos mirror for balancing-authority polygons.
- **Google publishes no fleet WUE** (only aggregate water volume) — its water must be derived; flag the asymmetry.
- **"How Hungry is AI?" (2505.09598) ≠ Epoch AI** — cite separately.
- **LBNL calibration = 176 TWh (2023), 325–580 TWh (2028).**
- **AWARE2.0 (2025, Zenodo)** is the current scarcity method — decide whether to use it or justify AWARE1.2.
- **eGRID2023** (rev2, Jun 2025) is current, downloadable — 27 subregions, annual, average.
- **Lit review honesty:** 84 rows in the coding sheet, but only **31 are verified=Y** — the honest number is "~70 works read/verified," not "84 primary-read." The coding sheet's **Gaps-Freshness tab still encodes the dead RQs** (water-as-stock, workload-reallocation) — rewrite it to the current conjunction.
- **The proposal's DAGNN router ≠ the audited fusion GNN** — don't conflate the killed routing design with the GNN that was actually built and nulled.
- **PII to scrub before any open release** (in the GAT repo): a hackathon email in `paper_submission/docs/DATA.md`; a collaborator's Windows path in `SESSION_REVIEW_AND_NEXT_STEPS.md`.
- **LIT REVIEW COMPLETE (2026-09-22):** `LIT_REVIEW_VERIFIED.md` **supersedes** `LITERATURE.md` — **89 numbered works** (rel-5→rel-2) + full web-sweep + rel-1 GNN cluster verdict, one entry each with 6-axis deltas. **No scoop of the six-axis conjunction.**
- **Nearest neighbours (FULL-TEXT confirmed):** #74 **Bolaños-Zuñiga & Lamadrid 2026** (arXiv 2608.09882 — US-only, **volumetric** water not scarcity, carbon & water **separate** not joint, **closed**); **MARLIN** (2605.13496 — a scheduler, volumetric water, global-generic, no India); **Global data–water symbiosis** (national-aggregate LCA, India = 1 of 98). Each misses **≥3 load-bearing axes**.
- **⚠️ Marginal carbon is NOT a differentiator** — MARLIN **and** #74 both use marginal carbon → keep it **Ceiling-only, US/UK-labelled**; the moat is India + scarcity-weighting + unified joint facility account + reg-gap-map + reproducibility.
- **Journal correction (my error, fixed):** the two on-topic AI-infra reviews (`S2666792425000058`; `S266679242500037X` = Lal & You) are in ***Advances in Applied Energy*** (ISSN 2666-7924), **NOT** the target journal *Energy and Climate Change* — do **not** cite as target-journal fit.
- **`coding_sheet_1.xlsx` does not exist** — the coding sheet's rel-1 pointer is dead; the GNN corpus is in `GNN_AUTOPSY.md` + the canonical ST-GNN papers (cluster verdict in `LIT_REVIEW_VERIFIED.md`).
- **⚠️ ON-DISK DATA REALITY (2026-09-26, `DATA.md` PART D):** the "reliable primary stack" the docs describe is **NOT on disk.** What we physically have = the old GAT stack: **Ember** (carbon, primary-usable), **Aqueduct 4.0** (scarcity), **G3P** (context), **ATLAS** (scraped, city-centroid coords, no capacity), **GEM** (plant context), an **ElectricityMaps demo file** (not real data), + **our India_DC_Facilities_v0** (194, no lat/lon). **Missing (all OPEN, un-retrieved):** eGRID, CEA v21, ENTSO-E, Macknick, AWARE2.0, HydroBASINS/GADM, CGWB, MLPerf, marginal carbon. **Account is buildable now on the subset; retrieval of primaries is the real L0 task. Precise facility geolocation is a genuine gap.** CEA v21 (Nov 2025, FY24-25), AWARE2.0 (Zenodo), Macknick (ERL) retrieval paths re-verified.

---

## 7. Architecture (pointer)

> **⚠️ SUPERSEDED (2026-09-26):** the S0–S11 blueprint below was built for the pre-pivot "pure account" direction. **The current architecture is BUILT/SCAFFOLDED as the `dcfootprint/` package** (repo root) — a layered, library-backed, DAG-orchestrated (Snakemake), schema-validated (pandera) pipeline; see **`dcfootprint/README.md`** (authoritative) + `RESEARCH_GAPS.md` §B (the L0–L7 rationale). Design grounded in lit-review accounting equations (Guidi/Li/Siddik). Scaffolded: pyproject, config/{parameters,datasets}.yaml, validation/schemas.py (the granularity contracts), account/water.py (reference equation), workflow/Snakefile (the DAG). Next build = `io/facilities.py` (the facility merge). Treat S0–S11 below as reference only.

Full (legacy) blueprint in `ARCHITECTURE.md` (+ `architecture_diagram.svg/.png`). Atomic unit = **facility-month**; each resource keeps its native partition; facility is the join key. Stages: **S0 join** (facility → grid region + watershed + basin; Floor, build FIRST — the one real risk) · **S1 energy** (kWh/month + inference share) · **S2 carbon** (Floor average / Ceiling US-marginal) · **S3 water physical** (WUE + EWIF×fuel-mix + PUE) · **S4 scarcity** (AWARE monthly, separate layer) · **S5 basin context** (Ceiling; GRACE/CGWB flag) · **S6 maps+tables** (Floor ★) · **S7 policy levers** (Ceiling) · **S8 equity** (Ceiling, diagnostic) · **S9 uncertainty** (Floor, wraps all) · **S10 regulatory-gap map** (Floor) · **S11 forward projection** (Ceiling; regional demand + grid carbon only — never site-level water). **Floor = S0–S6, S9, S10-map. Ceiling = S2-marginal, S5, S7, S8, S11, S10-levers.**

---

## 8. Datasets & the prior repo (pointers)

- **Data plan:** `DATA.md` (accessibility, granularity, dependency spine, keep/drop/replace rubric — verified, corrected).
- **Facility master:** `data/India_DC_Facilities_v0.xlsx` (+ `.psv`) — 194 rows, 129 operational, ~1,373 MW; confidence 113 High/65 Med/16 Low; `cea_grid_region` filled 194/194; **NOT geocoded (no lat/lon); 40/129 operational uncosted.**
- **Literature:** `LIT_REVIEW_VERIFIED.md` (**authoritative** — 89 works, one-per-entry, 6-axis deltas, complete 2026-09-22; supersedes `LITERATURE.md`) + `lit_review_coding_sheet.xlsx` (verified-flag column is stale; Gaps-Freshness tab rewritten).
- **Policy baseline for S10:** `POLICY_DEEP_DIVE.md` (four-axis gap, triple-confirmed).
- **CFP verbatim:** `CFP_RECORD.md`. **Editors:** McCollum (IAM/AR7), Verdolini (policy/economics), Te Han (ML/forecasting → S11), Clarens (DC water/carbon). Cite one work each; pull Clarens's exact 2024–26 DC titles.

### The prior GAT repo — scrap vs salvage (full autopsy in `GNN_AUTOPSY.md`)

`gat-based-forecasting/` is Phase 2 (a rigorously-audited **null**: a co-location graph does not improve monthly resource forecasting). **SCRAP** the thesis: the GNN/graph-fusion design, the routing/allocation framing, the DAGNN plan, the graph artifacts, China, the Phase-1 hardcoded tables, the scraped atlas as *primary*. **SALVAGE:** the datasets already downloaded (**Ember US/EU/India, GEM Global-Integrated-Power, Aqueduct 4.0, G3P/GRACE**); the **geocoder** (facility→zone→basin point-in-polygon + fuzzy-0.82 — ~70% of S0, retarget to CEA+HydroBASINS+AWARE); the **forecasting benchmark** (Chronos-2 > SARIMA > xLSTM on grid; SARIMA best on water; TSFM helps sub-nationally not nationally) → S11; the **audit/rigor harness** → the reproducibility pillar. **Lessons:** signal lives in per-site heterogeneity (→ facility-month); nearest-centroid basins are too coarse (554 km median error → use HydroBASINS polygons); capacity ≠ generation; the mid-month-timestamp freq trap.

---

## 9. Feasibility & the plan

**Solo, ~14 weeks to 31 Dec; internal target = architecture built by end of Sept, leaving Oct–Dec for the build + revision rounds.** Honest reading: the **architecture design** locks now; the **India core** pipeline (S0 join → carbon + scarcity-water → first maps) is buildable by end of month; the **full** multi-region + Ceiling is an Oct–Dec build. Ambition-first sequencing: design the full six-axis + Ceiling + reg-gap-map + instrument now, build **India Floor first**, replicate US/EU + add Ceiling through October, revise Nov–Dec.

**The real risks are not the clock:** (1) the India capacity data (40 uncosted, mixed bases) on the critical path; (2) scope-creep / perfectionist lit-sweeping (the lit review was "closed" 3×). **Freeze the literature; start S0.**

**Go/no-go structure (from the old build plan, dates dropped):** ★ India Floor works? → expand to US, else India-only-deep. ★ EU in? → three regions, else ship India+US. Fallback ladder (every rung submittable): India+US+EU → India+US → India-only-deep → (last resort) perspective/reconciliation paper.

---

## 10. Immediate next steps

> **⚠️ CURRENT next steps (2026-09-26, supersede the pre-pivot list below):** (1) **seasonal Gate 3** (monthly-CF re-ranking — the decisive test); (2) **build `dcfootprint/src/dcfootprint/io/facilities.py`** — the facility layer (geocode 194 via city-centroids/ATLAS + fill 39 uncosted from CEA-plant/JLL + top-up to ~1.8 GW), the make-or-break; (3) **L2 account** (`account/{energy,carbon,water}.py`) on the validated data; (4) **C5 reg-gap map** (`policy/gap.py`, needs no new data — POLICY_DEEP_DIVE + burden). Retrieve when a layer needs it: EM/EnergyMap (India consumption carbon), LBNL Water-IMPACT tool (scope-2), EU Reg 2024/1364 + datacenterbans.com (C5 citations), population (C7). Gate scripts to re-run: `dcfootprint/experiments/`.


1. **Geocode the 194 India facilities** to lat/lon (city/campus → coordinates). *No-regret; the true critical path start.*
2. **Stand up the S0 join** (facility → CEA grid region + HydroBASINS watershed + basin) — build & stress-test first; reuse/retarget the GAT geocoder.
3. **Pull the OPEN spine:** CEA v21, Ember India monthly, AWARE2.0, Macknick EWIF, CGWB 2024, HydroBASINS/GADM, eGRID2023, MLPerf, EU Reg text. **Start ENTSO-E registration** (~3-day approval) so EU isn't blocked later.
4. **Fix the facility master:** impute the 40 uncosted operational facilities; normalize capacity basis.
5. **Decide (see §12 open questions)** before locking S2: India carbon = national-monthly vs regional-annual.

**Awaiting user:** free GridEmissionsData.io/WattTime registration (Ceiling, not urgent).

---

## 11. Session history (compressed)

- **Arc 1 (pre-2026-09-15):** repo forensic audit; deadline corrected 30 Sep → **31 Dec 2026** (verified 4 ways); CFP facts captured. Direction locked: India-anchored accounting, not routing.
- **Arc 2 (2026-09-13→16):** literature review (~70 works, primary-verified); red-team audit → the kill-list + Floor/Ceiling; data accessibility verified (4 web sweeps); **India facility list built (194 rows)**; policy deep-dive (four-axis gap, triple-confirmed); GNN autopsy (the null is real, specific to co-location×region×fusion).
- **Arc 3 (2026-09-19→20):** ideation re-validated across 7 areas (CFP, novelty, RQs, scope, datasets, policy, freshness); web-verified corrections (CEA v21; 43%-global; Harvard Dominici/Le Xie toolkit is real+funded+US-only; eGRID2023/AWARE2.0 confirmed); primary autopsy of the whole GAT repo (scrap-vs-salvage); **context docs consolidated to this file + a lean reference set.**
- **Arc 4 (2026-09-22):** the **"ultimate literature-review pass"** — 89 works read primary-first (rel-5→rel-2) + web-sweep + rel-1 GNN cluster verdict, one entry each with 6-axis deltas in `LIT_REVIEW_VERIFIED.md`. **No scoop found.** New US nearest-neighbour #74 full-text-verified. Caught doc-discrepancies: journal mislabel (Advances in Applied Energy ≠ target), "GAR" phantom, `coding_sheet_1.xlsx` missing.
- **Arc 5 (2026-09-23→26, this session):** **research-gap re-examination + direction PIVOT.** Re-opened the gap question unbiased → 12 candidates scored (`RESEARCH_GAPS.md`); the pure-account favourite placed 7th (thin *working* contribution). **Chosen direction = combination G6+G1+G5+G3** (counterfactual policy on an India account spine, regulatory-gradient frame, salvaged forecasting as secondary). **Problem/purpose anchored** (regulators fly blind on DC carbon+water; give them the numbers to choose a lever). **Buildable artifact defined = a layered reproducible pipeline (L0–L7), NOT a multi-agent system.** GAT repo re-autopsied from **primary notebook code** → scrap graph, salvage geocoder + a *real* sub-national multi-model forecast benchmark + rigor. **Next = Phase-0 verification (capacity data · Ember-India carbon · CFP tracks · policy levers), then build the India Floor.** See `RESEARCH_GAPS.md` §P/§A/§B (authoritative for direction + architecture).
- **Arc 6 (2026-09-26, this session — deep validation + build-setup + FIRST GATES):**
  - **Repo LIVE:** `github.com/energyclimaterp-paper/counterfactual-policy` (code+docs pushed; `data/` + `gat-based-forecasting/` + journal-source MDs git-ignored; PII-scanned clean).
  - **Architecture BUILT + carved out in detail:** `dcfootprint/` (pyproject · config/{parameters,datasets}.yaml · validation/schemas.py = pandera contracts · account/water.py = reference equation · workflow/Snakefile = DAG) + **`dcfootprint/ARCHITECTURE.md` (AUTHORITATIVE:** L0–L7, account equations, §6 risk register [14 flaws+fixes], §6.4 gates, §7 **tiered contributions C1–C9**) + `dcfootprint/docs/architecture_flow.svg`. **Shape = account → project → counterfactual → policy-gap; deterministic pipeline, NOT multi-agent** (agents rejected — force behavioural assumptions + break reproducibility; verified: no multi-agent *accounting* exists, only schedulers = kill-list).
  - **Contributions = 9 TIERED** (Tier-1 spine: C1 account · C3 spatial+seasonal burden · C4 method-sensitivity · C5 reg-gap map · C8 open instrument+dataset · C9 uncertainty; Tier-2 reach: C2 full-water scope-2 scarcity · C6 counterfactual+projection · C7 equity). Authoritative in ARCHITECTURE §7; §2 above + RESEARCH_GAPS §A point to it.
  - **Data validated (`DATA.md` D/E/F/G):** real files in `data/`; every file opened, granularity + cross-join keys verified. **⚠️ AWARE Basin_ID ≠ Aqueduct pfaf_id (0 overlap) → scarcity join = AWARE gpkg point-in-polygon ONLY.** **2 red-team compromises RECOVERABLE:** India consumption carbon (ElectricityMaps regional / EnergyMap.in), scope-2 water localisation (LBNL Water-IMPACT method). Corrections: **CEA v22 EXISTS** (retrieved); Ember-India NOT stale.
  - **Deliverability CONFIRMED** (arch/data/capability): Tier-1 deliverable pending the facility-layer build (materials on disk); Tier-2 conditional on named retrievals/builds.
  - **★ FIRST 3 GATES RUN (data in hand; scripts in `dcfootprint/experiments/`):**
    - **G1 CALIBRATION = PASS:** bottom-up operational 1.39 GW (90 costed / 129 operational) vs CEEW/JLL 1.5–1.8 GW → ratio 0.84 (+39 uncosted → ~1.0). C1 magnitude validated.
    - **G2 COVERAGE = PLAUSIBLE (caveat):** Mumbai/Navi 31% ≈ CEEW ~25%; **BUT ~61% of capacity in 3 mega-sites (Navi Mumbai 25%, Palava 20%, Vizag 16%)** → ranking hinges on a few large sites. ATLAS city field 57% blank (coarse gap-filler only).
    - **G3 RQ2 = scarcity-weighting does NOT re-rank (ANNUAL):** Spearman(unweighted,weighted) 0.91 state / 0.95 basin; top-5 overlap 5/5; MC(400) tight [0.90–0.96]; worst = Maharashtra/Andhra/Telangana/Tamil-Nadu **identical** weighted vs unweighted. CF varies (1.6–78.9) — not flat; capacity & scarcity are **positively correlated**.
  - **★ THE REFRAME (key finding, do not lose):** headline is NOT "scarcity-weighting re-ranks" (annual data says it barely does). It IS **"India's AI datacenters are disproportionately sited in already-water-stressed basins — scarcity-weighting doesn't move the hotspot ranking because the hotspots ARE the stressed basins."** C4 becomes "we tested method-sensitivity; for India, average is adequate to flag hotspots *because siting coincides with stress*" — clean, no-assumptions, policy-relevant. Spine (C1/C5/C8) intact. (Red-team S4 anticipated this.)
  - **DECISIVE PENDING:** **seasonal Gate 3 (monthly CF, not annual)** — does dry-season scarcity re-rank? (C3 "when" may carry the signal). G3 first-pass caveats: city-centroid geocode, annual CF, 124 matched facilities, capacity-concentrated.
  - **NEXT (in order):** (1) **seasonal Gate 3**; (2) **facility layer** `io/facilities.py` (geocode 194 + fill 39 uncosted + top-up ~1.8 GW via CEA-plant/JLL + ATLAS coords); (3) **L2 account**; (4) **C5 reg-gap map**. Retrieve when needed: EM/EnergyMap, LBNL tool, policy texts (EU Reg 2024/1364, datacenterbans.com), population (C7).

---

## 12. Open questions (resolve before/at the build)

1. **India carbon grain:** national-monthly (Ember, loses sub-national) vs regional-annual (CEA v21, loses monthly). You can't have both. **Recommendation: concede India carbon is coarse, make water the sub-national protagonist for India, say so up front.**
2. **RQ2 diagnostic:** run the scarcity/marginal re-ranking early on data in hand — does the ranking actually move? De-risks the central claim cheaply.
3. **Abstract = Floor or Ceiling claim?** Decide the fallback abstract now; "marginal" only in the headline if the Ceiling lands, labelled US.
4. **Facility-master fix plan** for the 40 uncosted operational facilities + mixed capacity bases.
5. **Harvard timing:** if their US pipeline/toolkit drops before submission, frame the US tier as a *comparison mirror* (safe), not a contribution (exposed).
6. **GNN null in the paper?** Recommendation: hold as a one-paragraph methodological caution in reserve, not in the main body.

---

## 13. Document index (context/ after consolidation)

| File | Role |
|---|---|
| `00_PROJECT_STATE.md` | **this file** — state, decisions, rationale, corrections, log (read first) |
| **`../dcfootprint/ARCHITECTURE.md`** | **AUTHORITATIVE architecture + TIERED contributions (§7) + risk register (§6)** — read for the build & the contribution statement |
| **`../dcfootprint/README.md`** + `docs/architecture_flow.svg` | package overview + data-flow diagram |
| `ARCHITECTURE.md` (context/) | *legacy* S0–S11 blueprint — superseded by `dcfootprint/ARCHITECTURE.md` (reference only) |
| `LIT_REVIEW_VERIFIED.md` | **AUTHORITATIVE literature review** — 89 works, one-per-entry, 6-axis deltas, nearest-neighbour analysis, GNN cluster verdict (complete 2026-09-22) |
| `RESEARCH_GAPS.md` | gap re-examination + §P problem/purpose + §A chosen direction (contributions here SUPERSEDED by `dcfootprint/ARCHITECTURE.md §7`) |
| `POLICY_DEEP_DIVE.md` | US/EU/India regulatory baseline for S10 (four-axis gap) |
| `CFP_RECORD.md` | verbatim call-for-papers + journal facts |
| `DATA.md` | dataset accessibility + granularity + keep/drop rubric (merged) |
| `GNN_AUTOPSY.md` | prior GAT repo — what failed, why, scrap vs salvage |
| `lit_review_coding_sheet.xlsx` | paper corpus (Gaps-Freshness tab: rewrite pending) |
| `data/India_DC_Facilities_v0.xlsx` + `.psv` | the India facility master (v0) |

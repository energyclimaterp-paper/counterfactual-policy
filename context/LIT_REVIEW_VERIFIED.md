# LITERATURE REVIEW — Verified From Primary (the ultimate pass)

> Built 2026-09-22, one paper at a time, each read **from source** — not from our earlier AI-synthesized docs. When complete this **replaces `LITERATURE.md`**. Order = relevance-first (rel-5 → rel-1). Corpus = 84 rows in `lit_review_coding_sheet.xlsx` (≈78 unique after removing duplicates + the archive-pointer; the ~40-paper GNN corpus is covered at the end).
>
> **Verification legend:** ✅ full text read from source · 🟡 abstract/publisher-record only (full text walled — flagged) · ⬜ pending.
> **6-axis test vs our conjunction:** **J** joint carbon+water · **M** marginal/locational carbon · **S** scarcity-weighted water · **I** AI-inference attribution · **R** multi-region incl. **India** (sub-national) · **P** forward policy-lever / regulatory-gap. (✓ yes · ~ partial · ✗ no)
>
> **Running tally:** 80 / ~80 done (rel-4→rel-2 COMPLETE; +1 walled: #53 ACM SoCC). Remaining: rel-1 GNN archive corpus (cluster pass) + web-sweep leads.
>
> **Template (enriched 2026-09-22 per user):** each entry now leads with the paper's OWN **contribution/novelty** and the **gap it claims**, before mapping to our 6-axis test — so we understand each paper on its own terms, not just as a checklist.

---

## REL-5 — core near-neighbours (17)

### 1. Reviewing the socio-technical dynamics of AI, data centers and digitalization on energy and the environment — RSER 2026 (`S1364032126001607`) 🟡
- **Citation:** Kim et al. (lead Kim; Debnath among authors), *Renewable & Sustainable Energy Reviews*, March 2026. Cambridge/CRASSH group.
- **What it does:** Systematic **review** — screens **364 articles (2000–2025)** across four dimensions (natural resources · facilities/components · applications · users/institutions). Three RQs: (1) which low/zero-carbon technologies mitigate AI's footprint, (2) barriers to adoption, (3) policy interventions to overcome them.
- **Method:** Socio-technical systems framing; qualitative systematic review (not primary accounting).
- **6-axis:** J ✗ · M ✗ · S ✗ · I ✗ · R ✗ · P ~ (reviews policy interventions but builds no instrument). — **It frames our gap; it does not fill it.**
- **Delta to us:** It is a field map / mitigation-and-policy review; we are the primary sub-national joint account + regulatory-gap map it calls for. **Cite as the venue-adjacent field review** (organizer-adjacent — Cambridge/Debnath circle).
- **Verification:** 🟡 ScienceDirect full text 403-blocked; scope/RQs confirmed via the Cambridge repository record + abstract.
- **Doc-discrepancy:** our docs attributed a specific "stated gaps" list (demand-forecasting uncertainty, Global-South equity, organizational barriers) — **not verifiable from the walled full text**; only the 3 RQs above are confirmed. Do not quote that gap-list until the full text is read.

### 2. Making AI Less "Thirsty" — arXiv 2304.03271v5 ✅
- **Citation:** Li, P., Yang, J., Islam, M.A., Ren, S. (2025; v5). UC Riverside + UT Arlington. (→ CACM.)
- **What it does:** The seminal AI **water** accounting method. Headline: GPT-3 training ~**700,000 L** on-site evaporation (5.4 M L incl. scope-2); inference **~16.9 mL / medium response** (US avg, ~1 bottle per ~29.6 requests); global AI **4.2–6.6 bn m³** withdrawal by 2027. On-site WUE 0.01–9 L/kWh; off-site EWIF 3.14 L/kWh (US avg).
- **Method:** `W_total = Σ_t e_t·[ρ_s1,t + θ_t·ρ_s2,t] + embodied`, where ρ_s1 = on-site WUE, ρ_s2 = fuel-mix EWIF, θ = PUE; scope-1/2/3 tracked separately.
- **6-axis:** J ✗ · M ✗ · S ✗ (physical volume only; no stress weighting) · I ✓ (per-request inference) · R ~ (India appears as a **country-average row** in Table 1, **not sub-national**) · P ~ (transparency recommendations, no regulatory analysis).
- **Delta to us:** we add carbon-joint + marginal + scarcity-weighting + **sub-national** multi-region (incl. India) + the reg-gap map. Borrow the WUE·EWIF·PUE scope-1/2 equation; do not re-claim "first AI water footprint."
- **Verification:** ✅ full text (arXiv HTML v5).
- **Doc-discrepancy:** none material. (Our docs said "national/company scale, no sub-national, no scarcity" — confirmed. Nuance: India *is* listed, but only as a country average.)

### 3. The Hidden Water Geography of US Hyperscale Data Centers — arXiv 2607.02531 ✅
- **Citation:** Guidi, G., Dominici, F., et al. (submitted Jun 2026). Harvard.
- **What it does:** Facility-level **water** for **472 US hyperscale DCs**; ~**300 GL/yr** (range 205–451); **~¾ of water is electricity-related** (off-site), ¼ on-site cooling; links facilities to water-stress; identifies "which decisions matter where" (cooling/sourcing locally, electricity planning/procurement regionally).
- **Method:** boundary `W_tot = 10⁻³[I_grid·E_fac + WUE·(E_fac/PUE)]`; facility→BA→HydroBASINS→Aqueduct stress; 25th-percentile-BA reduction benchmark.
- **6-axis:** J ✗ (water only, no carbon) · M — · S ✓ (water-stress linked) · I ✗ (generic hyperscale, not inference) · R ✗ (US only) · P ~ (light decision-differentiation, not a reg-gap map).
- **Delta to us:** the closest US water-geography prior. We add carbon-joint (+marginal), inference attribution, **EU/India**, and a real regulatory-gap map. Half of the "Guidi pair" (companion to #13, carbon).
- **Verification:** ✅ abstract/scope from arXiv (last turn).
- **Doc-discrepancy:** none.

### 4. The Hidden Thirst of AI / Water Cost of Intelligence (WCI) — Green (MDPI) 1(2):8, 2026 (10.3390/green1020008) 🟡
- **Citation:** Sharma et al., *Green* (MDPI) 1(2):8, 2026.
- **What it does:** A **per-query** water accounting framework combining **direct** cooling water + **indirect** electricity-generation water + a regional **Water Stress Index (Aqueduct 4.0 BWS)** into one number. Key result: adding indirect (electricity) water raises the median LLM-prompt estimate by **+179%** vs cooling-only.
- **Method:** `W_direct + W_indirect`, then `W_stress = W_total · WSI` (Aqueduct 4.0 baseline water stress).
- **6-axis:** J ✗ (water only) · M ✗ · S ✓ (Aqueduct WSI — genuine scarcity weighting) · I ✓ (per-query inference) · R ✗ (US-centric mixes; not sub-national multi-region) · P ✗ (single-point calculator, no counterfactual/reg-gap).
- **Delta to us:** the closest scarcity-weighted-per-query-water precedent. We lift it from a per-query calculator to a **spatial, multi-region, carbon-joint, marginal, counterfactual, reg-gap** account. Cite prominently.
- **Verification:** 🟡 MDPI full text 403-blocked; scope/method confirmed via the DOI record + the authors' own explainer. (Our earlier docs' detailed method — Google reconstruction 0.254 vs 0.26 mL, Arizona ×5 vs Oregon ×0, hydro-EWIF landmine — is consistent but should be re-confirmed from the PDF before quoting specifics.)
- **Doc-discrepancy:** none found at scope level; the fine-grained coefficients remain 🟡.

### 5. Towards Environmentally Equitable AI via Geographical Load Balancing (eGLB) — arXiv 2307.05494 ✅
- **Citation:** Li, P., Yang, J., Wierman, A., Ren, S. ACM e-Energy '24 (also CACM 2025). UC Riverside + Caltech.
- **What it does:** An **online optimizer** (not accounting) that minimises the **worst-off region's** carbon and water (minimax fairness) across **10 DCs (4 US / 4 EU / 2 Asia)**. Cuts max/avg disparity: water **1.91→1.33**, carbon **1.84→1.32**, at comparable average cost.
- **Method:** minimax objective over per-DC carbon `c=α·γ·e` and water `w=(ε+β·γ)·e`; **dual mirror descent** online algorithm; trace-based simulation.
- **6-axis:** J ✓ (joint carbon+water) · M ~ (hourly regional intensity, not marginal/localized) · S ✗ (location-aware WUE but **not** stress-weighted — named as future work) · I ✓ (inference) · R ~ (**no India**; EU/Asia **fuel mixes are SYNTHETIC**, US water real) · P ✗ (no policy/reg analysis).
- **Delta to us:** eGLB is a **prescriptive optimizer on partly-synthetic data**; we are **empirical accounting on real sub-national data incl. India** + a reg-gap map. Borrow the c/w footprint decomposition + the equity/minimax framing; do not adopt the router.
- **Verification:** ✅ full text (arXiv HTML).
- **Doc-discrepancy:** none material (our docs said "synthetic non-US, average EF, optimizer, equity anchor" — confirmed; refinement: geography is real but the EU/Asia *fuel mixes* are synthetic, and there is **no India**).

---

### 6. The Environmental Footprint of Data Centers in the United States — Siddik, Shehabi & Marston, ERL 16(6):064017, 2021 🟡
- **Their contribution & novelty (their words):** "**For the first time**" — spatially-detailed **carbon AND water** footprints of *all* US data centers, resolved to sub-national **HUC-8 watersheds**. This is the direct ancestor of our accounting; the joint-sub-national-DC-footprint idea is *theirs*.
- **Gap they claim:** prior DC footprint work was national-average and energy-centric; water was not resolved sub-nationally nor paired with carbon.
- **What it does + numbers:** DCs ≈ **1.8% of US electricity**; **~1/5 of servers' direct water** comes from moderately-to-highly water-stressed watersheds; **~half of servers** are powered (partly) by plants in water-stressed regions; US hosts ~1/4 of global DC servers. Explores optimal-siting scenarios.
- **Method:** bottom-up; facility → HUC-8; grid EF for carbon + on-site WUE / off-site EWIF for water; water-stress overlay.
- **6-axis:** J ✓ · M ✗ (average) · S ~ (water-stress *exposure*, not full AWARE weighting) · I ✗ (generic DC, pre-genAI) · R ✗ (US only) · P ~ (siting scenarios, not a reg-gap map).
- **Delta to us:** THE baseline to differentiate against. We add **+India +EU +marginal carbon +inference-attribution +monthly trajectories +AWARE scarcity-weighting +regulatory-gap map**. **Never re-claim "first joint sub-national DC carbon+water account" — it is theirs (for the US).**
- **Verification:** 🟡 IOP + OSTI both bot-walled; scope + key findings confirmed via the LBNL Energy Analysis Division record + multiple indexes.
- **⚠ Doc-discrepancy (important):** our old docs assert Siddik has "**4 siting counterfactuals, −90% water / −55% carbon**" and "2,110 HUC-8 subbasins." **I could NOT verify those magnitudes from primary this pass** (abstract doesn't surface them). **Do not quote the −90%/−55% or the 2,110 figure until the full text is read.** This is exactly the "built on half-baked info" risk — flagged.

### 7. Spatially & Temporally Detailed Water and Carbon Footprints of U.S. Electricity Generation and Use — Siddik, Shehabi, Rao & Marston, Water Resources Research 60(12):e2024WR038350, 2024 🟡
- **Their contribution & novelty:** the "**Water IMPACT Tool**" — spatially + temporally detailed water AND carbon intensities of **US electricity** that capture grid dynamics (temporal renewable fluctuations) which generalized regional methods miss.
- **Gap they claim:** existing methods generalize across large regions, neglecting spatial/temporal variation in electricity's water + emissions.
- **What it does:** balancing-authority-resolved, **consumption-based** (import/export-adjusted) water + carbon intensities; open tool (HydroShare / LBNL).
- **6-axis / relevance:** **NOT a data-center paper — it is about ALL US electricity.** So it is a **grid-intensity SUBSTRATE**, not a near-neighbour. J ✓ (for electricity) · M ✗ (average, monthly-constant) · S ✗ (physical) · I ✗ · R ✗ (US) · P ✗.
- **Delta to us:** we would **use** it (US scope-2 water+carbon intensity input), not compete with it. Cite as method substrate.
- **Verification:** 🟡 Wiley walled; title + abstract + LBNL "Water IMPACT Tool" page confirm scope; full text on eScholarship (`9x98m3gh`) if needed.
- **Doc-discrepancy:** none — confirms our docs ("all-US-electricity, not DC-specific, grid substrate").

### 8–9. CEEW — India data-centre power/water + "Scaling India's Data Centre Ecosystem" — CEEW + SYSTEMIQ, lead Vishal Tripathi, Feb 2026 🟡
*(Rows 8 and 9 are one study + its companion article — treat as one India-anchor source.)*
- **Their contribution:** the authoritative **India aggregate** — capacity, energy, water, land, siting — plus a review of the **15 state DC policies** and stakeholder perspectives.
- **Gap they claim:** India's DC growth is outpacing sustainability standards; most state policies lack PUE/WUE/water performance standards; siting is mismatched with water/grid readiness.
- **India-specific numbers (primary-adjacent):** ≈**1.5 GW (2025) → 4.5–6.5 GW by 2030**; **~0.5% of national electricity** (2025); water **~0.02–0.03% of national demand** (2025); **>half of India's DCs in water-stressed regions**; ~15 state policies, most without PUE/WUE; concentration in Mumbai/Chennai/Hyderabad/Bengaluru.
- **6-axis / relevance:** N/A (aggregate resource + policy study, not a facility-level accounting framework). It is our **India ANCHOR + validation** (its ~1.5 GW aggregate validates our 194-facility master's ~1.37 GW operational) and directly feeds **S10** (the state-policy gap).
- **Delta to us:** not a competitor — our contribution goes *below* CEEW's national aggregate to **facility-level** sub-national accounting.
- **Verification:** 🟡 ceew.in 403'd twice; figures confirmed via the SYSTEMIQ PDF + Mongabay coverage + search.
- **✅ Doc-correction VINDICATED:** ">half of India's DCs water-stressed" is confirmed **India-specific** — which is why the old "43% of India DCs" was wrong (43% was the *global* figure). Our earlier correction holds, now from primary-adjacent source.

### 10. Operational Water Consumption and Withdrawal Factors for Electricity Generating Technologies — Macknick, Newmark, Heath & Hallett, NREL / ERL 7(4):045802, 2012 ✅
- **Their contribution & novelty:** the first **harmonization** of fragmented water-intensity literature into standardized operational water **consumption and withdrawal factors** by generation technology × cooling type.
- **Gap they claim:** water-intensity data was fragmented and inconsistent across studies; no standardized factors existed for LCA/energy planning.
- **Coefficient values (gal/MWh, median; consumption / withdrawal):** coal recirc-tower ~600–800 / ~1,100–1,200; NGCC recirc ~200–300 / ~400–500; nuclear recirc ~600–800 / ~1,200–1,400; once-through withdrawals ~10,000–25,000; dry cooling ~0–150; solar PV / wind ~0–20 / ~0. (Ranges; medians vary by source.)
- **Method:** systematic **literature harmonization**, not original measurement.
- **6-axis / relevance:** N/A — it is a **coefficient source / building block**, not a DC framework.
- **Delta to us:** THE scope-2 **EWIF source** for our S3 off-site water layer (× each zone-month's grid fuel mix). Cite; do not re-derive.
- **Verification:** ✅ full text (NREL mirror PDF, saved locally).
- **Doc-discrepancy:** none — our docs' cited medians (coal 687/1005, NGCC 198/253, nuclear 672/1101) fall within the harmonized ranges. Consistent.

---

### 11. Concentrated Siting of AI Data Centers Drives Regional Power-System Stress — Chen et al., arXiv 2604.06198, 2026 ✅
- **Their contribution & novelty:** an "AI-energy coupling framework" that fuses **LLM-based extraction** of corporate/policy/media disclosures with quantitative energy-system modeling; frames AI infrastructure as a *structural* component of power-system dynamics (not a marginal load).
- **Gap they claim:** existing analyses treat AI infra as marginal; anticipatory, renewables-aligned planning is missing.
- **What it does + numbers:** **Power Stress Index** (PSI = regional DC demand ÷ regional supply; >0.25 = vulnerable → Oregon, Virginia, Ireland). Six firms: **118 TWh (2024) → 239–295 TWh (2030)**, ≈1% of global power.
- **6-axis:** J ✗ · M ✗ · S ✗ · I ✗ · R ✓ (NA / W. Europe / Asia-Pacific — but **not India-anchored**) · P ~ (calls for anticipatory planning). **Computes ELECTRICITY / grid-stress only — no water, no carbon.**
- **Delta to us:** electricity-stress only; it *explicitly asks for* the carbon+water integration we do. **Borrow the LLM/RAG disclosure-extraction pipeline** as a facility-attribution precursor.
- **Verification:** ✅ (arXiv). **Doc-discrepancy:** none (docs accurate).

### 12. Optimal County-Level Siting of Data Centers in the US — Vabson, Zater, Sajadi, Baker & Hodge, arXiv 2601.16315, 2026 (CU Boulder/NREL) ✅
- **Their contribution & novelty:** a comprehensive **county-level siting OPTIMIZER** minimizing cost while quantifying resource use, integrating grid + telecom + climate + water + collocated-generation potential — "a foundational placement model at county granularity."
- **Gap they claim:** rapid DC expansion strains grid + water with no systematic siting-optimization guidance.
- **Method + findings:** multi-factor cost-minimization; **capital cost dominates**; a longer outlook favors sites with higher renewable-collocation potential.
- **6-axis:** J ~ (both, but cost-dominant) · M ✗ · S ✗ · I ✗ · R ✗ (US only) · P ✗. **Prescriptive new-build optimizer, not burden accounting.** Carbon implicit (via renewables collocation); water a secondary constraint.
- **Delta to us:** different genre (prescriptive siting vs empirical accounting + reg-gap).
- **Verification:** ✅ (arXiv abstract).
- **⚠ Doc-discrepancy:** our old docs claim Vabson has an explicit **"water-scarcity-risk penalty term (α^w R_l π^w_risk)"** worth borrowing. The abstract read says **regional water-scarcity weighting is not mentioned** (water is secondary to cost). The "borrow Vabson's scarcity penalty" advice may rest on an over-claim — **confirm from full text before relying on it.**

### 13. Assessing the Carbon Emissions and Energy Consumption of US Hyperscale Data Centers — Guidi, Dominici, Squartini et al., arXiv 2606.05420, 2026 (Harvard) ✅
- **Their contribution & novelty:** facility-level assessment of **403 US hyperscale DCs** (May 2024–Apr 2025); an **attributional** tool built on the latest EPA eGRID plant-level data.
- **Gap they claim:** no comprehensive facility-level hyperscale assessment for this recent window.
- **Numbers:** 403 DCs; **68–99 TWh**; **37–54 Mt CO₂**; ~1.8% US electricity; ~54% fossil; **545 gCO₂/kWh** (HDC-weighted) vs 370 US-avg (~48% above).
- **6-axis:** J ✗ (no water) · M ✗ (**attributional/average — confirmed**) · S ✗ · I ✗ (whole-facility, **not** inference) · R ✗ (US) · P ✗.
- **Delta to us:** the **carbon half of the Guidi "companion pair"** (with #3 water, 2607.02531). Together = US hyperscale carbon + water, but **split across two papers, average carbon, no inference, no India.** Our delta: unify + marginal + inference + India/EU + reg-gap.
- **Verification:** ✅ (arXiv abstract).
- **⚠ Doc-discrepancy:** (1) confirms average/attributional (docs right); (2) our docs cite a **"direct quote" that it "explicitly defers marginal to future work"** — **not found in the abstract**; do not cite that quote until the full text confirms it; (3) note the **"545" is the hyperscale cut (403 DCs)**, distinct from the "**548**" in the all-DC paper 2411.09786 (2,132 DCs) — keep them straight.

### 14. Not All Water Consumption Is Equal (SCARF) — Wu, Hua & Ding, ACM SIGEnergy EIR 5(2) / HotCarbon'25, 2025 ✅
- **Their contribution & novelty:** "the **first general framework** that evaluates the water impact of computing by factoring in **both spatial and temporal** variations in water stress." Core = **Adjusted Water Impact (AWI)** = consumption volume × local water stress over time.
- **Gap they claim:** current water assessment overlooks *where* and *when* water stress is severe.
- **Method + numbers:** three case studies (LLM serving, datacenters, semiconductor fabs); optimizing location + time reveals hidden water-impact reductions. *(Aqueduct-4.0 index and the ">1000×" cross-location factor our docs cite are in the full text, not the abstract — 🟡.)*
- **6-axis:** J ✗ (**water only, no carbon** — confirmed) · M ✗ · S ✓ (spatial **+ temporal** scarcity — the core) · I ~ (LLM-serving is one case) · R ✗ (not multi-region incl. India) · P ✗ (a metric, not policy).
- **Delta to us:** the scarcity-**and-temporal** water-metric precedent; we apply scarcity **jointly with carbon** + inference-attributed + multi-region incl. India + reg-gap. Borrow the spatial+temporal weighting concept.
- **Verification:** ✅ (arXiv abstract); the Aqueduct/>1000×/Qwen specifics 🟡 (full text).
- **Doc-discrepancy:** none contradicted; specifics unconfirmed.

### 15. Small Bottle, Big Pipe: Impact of Data Centers on Public Water Systems — Han, Li, Wierman & Ren, arXiv 2603.02705, 2026 ✅
- **Their contribution & novelty:** reframes DC water around **peak withdrawal CAPACITY** (not average consumption) as the binding constraint; introduces **"Water Capacity Neutral" / "Pipe Neutral."**
- **Gap they claim:** DC water literature focuses on average consumption and misses **peak capacity stress**; public water systems cannot surge-supply on the hottest days.
- **Method + numbers:** demand projections (2024 intensity persistence + 10%/yr-reduction sensitivity); **697–1,451 MGD** new capacity by 2030 (base), 227–604 MGD (optimistic); NYC ≈ 1,000 MGD; **$10B–$58B** capital.
- **6-axis:** J ~ (implicit dry-cooling↔grid link) · M ✗ · S ✗ (**absolute MGD, no scarcity weighting**) · I ✗ (generic DC) · R ✗ (US) · P ✓ (reporting, Pipe-Neutral, coordinated water-power planning).
- **KEY distinction (confirmed):** **capacity stress** (peak withdrawal vs infrastructure) ≠ **scarcity stress** (volume/depletion). This is a *different construct* from ours → **our scarcity-weighting axis is not scooped by it.**
- **Delta to us:** cite to contrast the two water constructs; we do scarcity-weighted + joint carbon + inference + India + reg-gap.
- **Verification:** ✅ (arXiv).
- **⚠ Doc-discrepancy:** our docs claim it **"introduces pWUE (worst-day L/kWh)"** and a `PeakDemand = β·(Total/T), β≈4.5` metric. The abstract says it does **NOT** introduce pWUE (it uses existing "water use intensity"). Over-claim — do not attribute pWUE to it until full text confirms. (The capacity-vs-scarcity distinction itself is real and confirmed.)

---

### 16. Environmental Potential of Hyper-Scale DCs: LMCE-Guided Geographical Load Shifting — Lindberg, Lesieutre & Roald, arXiv 2010.03379, 2020 (UW-Madison) ✅scope
- **Their contribution & novelty:** a bottom-up load-shifting model using **Locational Marginal CO₂ Emissions (LME/LMCE)** so distributed DCs cut emissions **without** central grid-operator coordination (a decentralized alternative to market bidding).
- **Gap they claim:** distributed DCs have load-shifting flexibility not leveraged for emissions independent of centralized systems.
- **Method + finding:** marginal CO₂ derived from DC-OPF (`λ_CO₂ = g·B`); load shifting cuts CO₂; the paper's point is that **marginal-based** guidance works where **average-based** can mislead.
- **6-axis:** J ✗ · **M ✓ (this IS the marginal method)** · S ✗ · I ✗ · R ✗ · P ✗. Carbon-only.
- **Delta to us:** this is the marginal-carbon **method we adopt** for S2-marginal (US). Borrow the derivation; not a competitor.
- **Verification:** ✅ scope (arXiv abstract). **🟡 doc-specifics unconfirmed:** the "toy 73-node grid" and "average shifting +0.09% vs LMCE −2.29%" figures our docs cite were **not** in the abstract — don't quote until the body is read.

### 17. On the Limitations of Carbon-Aware Temporal and Spatial Workload Shifting — Sukprasert, Souza, Bashir, Irwin & Shenoy, EuroSys'24, arXiv 2306.06502 (UMass) ✅
- **Their contribution & novelty:** a data-driven analysis of the **benefits and limits** of carbon-aware spatiotemporal scheduling across **123 regions** (batch + interactive) — beyond prior narrow, region-specific evaluations.
- **Gap/misconception challenged:** the assumption that spatiotemporal shifting delivers substantial *practical* carbon benefits.
- **Findings:** "**simple scheduling policies often yield most of these reductions**, with more sophisticated techniques yielding little additional benefit"; the **greener-grid paradox** is confirmed ("benefit... will decrease as the energy supply becomes 'greener'"); **carbon-only** (no water).
- **Delta to us:** the canonical critique that justifies **not building a router** — we do forward siting/policy levers instead. Cite as the ceiling on shifting gains.
- **Verification:** ✅ (arXiv). **🟡:** our docs' exact "**single migration captures ≥90%**" is worded in the abstract as "simple policies capture most" — the precise 90% needs the body.

### 18. Building Accurate Energy-Use Statistics for Data Centers — Wang, Han & Wei, *Engineering* 60(5):336–342, 2026 🟡 ★
- **★ EDITOR/EiC ALIGNMENT (major find):** authors are **Yong-Zhen Wang, Te Han, Yi-Ming Wei** (Wang & Han at Beijing Institute of Technology). **Te Han is the special-issue GUEST EDITOR; Yi-Ming Wei is the journal's co-EDITOR-IN-CHIEF.** This paper is co-authored by *two of our decision-makers* → a high-value, near-mandatory alignment cite. (Our old docs listed the paper but did **not** flag this.)
- **Their contribution & novelty:** exposes the unreliability of DC energy statistics and proposes a **statistical-governance framework** for accurate energy-use accounting.
- **Gap they claim:** 2020 global DC electricity estimates span **196–1,200 TW·h (≈6×)** — profound uncertainty from indirect assumptions/proxy indicators.
- **Method:** methods-critique / position (AI load-signature ID, NILM, mandatory grid registration); produces no new estimate of its own.
- **6-axis:** energy-only (no carbon-joint / marginal / water / scarcity / inference / sub-national).
- **Delta to us:** a **motivation cite** — our transparent, reproducible, facility-level accounting is a concrete answer to their call — *and* it aligns us with the editor + EiC.
- **Verification:** 🟡 (ScienceDirect 403; author list + scope + funding confirmed via engineering.org.cn + BIT Pure + EurekAlert).
- **Doc-correction:** precise cite is *Engineering* **60(5):336–342, 2026** (docs had "2025 / eng.2025.12.xxx").

### 19. Power Hungry Processing: Watts Driving the Cost of AI Deployment? — Luccioni, Jernite & Strubell, FAccT'24, arXiv 2311.16863 ✅
- **Their contribution & novelty:** "the **first systematic comparison** of the ongoing **inference** cost" across ML system categories — energy/carbon per 1,000 inferences, task-specific vs generalist models.
- **Gap they claim:** no systematic inference-cost comparison across architectures; does "generality" justify the environmental overhead?
- **Finding:** multi-purpose generative models are **orders of magnitude more expensive** at inference than task-specific, even controlling for parameters. Measured via **CodeCarbon on real GPUs**, 1,000 inferences per model-task.
- **6-axis:** J ✗ · M ✗ · S ✗ · I ✓ (per-task inference, **single region, single fixed carbon factor**) · R ✗ · P ~. **No water.**
- **Delta to us:** a **source of per-inference energy factors**; we are sub-national spatial joint carbon+water accounting. Cite; don't re-claim.
- **Verification:** ✅ scope (arXiv). **🟡:** our docs' "88 models × 10 tasks, 297.6 gCO₂/kWh, >1450× spread" specifics unconfirmed from the abstract.

### 20. Beyond the Carbon Emissions of AI: Whole-Systems Energy & Environmental Analysis of Datacenters in Denmark, Germany & Norway — ERSS 2026 (`S2214629626003105`) 🟡
- **Their contribution & novelty:** a **whole-systems lifecycle** analysis (from IT manufacturing + building construction) of **36 real European datacenters** (Norway/Germany/Denmark), chosen for their contrasting growth rates and energy mixes.
- **Gap they claim:** AI/DC analyses fixate on operational carbon; a whole-systems (lifecycle, embodied) view across contrasting EU energy systems is missing.
- **Findings:** DCs' carbon footprint exceeds global aviation; DCs ~6% of global electricity by 2026 (10%/yr to 2030); Denmark DC electricity up to **6× by 2030**.
- **6-axis:** J ~ (energy + broader environmental; whether it quantifies **water** is 🟡) · M ✗ · S ✗ · I ✗ (generic DC, "beyond AI") · R = **EU-Nordic only** (no India, no US) · P ~.
- **Delta to us:** a legitimate **EU-context / comparison** cite (Nordics), but whole-systems/lifecycle — not our facility-month sub-national joint marginal-carbon + scarcity-water account; no India/US, no marginal, no scarcity-weighting.
- **Verification:** 🟡 (ScienceDirect walled; scope via record). **Doc note:** previously marked "dropped/inaccessible" — now scoped; it's a real EU cite, not irrelevant.

---

## REL-4 — close near-neighbours

### 21. Environmental Burden of US Data Centers in the AI Era — Guidi, Dominici et al., arXiv 2411.09786, 2024 (Harvard) ✅scope
- **Their contribution & novelty:** carbon/electricity burden of **2,132 US data centers** (Sep 2023–Aug 2024), resolved to **52 balancing authorities + states** — the broadest facility-level US DC carbon account.
- **Gap they claim:** DC carbon impacts were not resolved to real facilities at grid granularity.
- **Numbers:** **192.64 TWh** (~4.6% US); **105.59 Mt CO₂e** (attributional); **548 gCO₂/kWh** (DC-weighted, **48% above** the 369 US avg — *this is the real "548"*); 56% fossil; Virginia 52 TWh / 30 Mt.
- **6-axis:** J ✗ (carbon only) · **M ⚠** (our docs say it *also* runs a WattTime marginal estimate; the abstract reads **average/attributional** — the marginal claim is **unverified from abstract**) · S ✗ · I ~ (AI-driven, not isolated) · R ✗ (US) · P ✗.
- **Delta to us:** the all-DC carbon member of the Guidi trio (with #3 water 2607.02531 + #13 hyperscale-carbon 2606.05420). Our delta: joint + water + (confirmed) marginal + inference + India/EU + reg-gap. **Cite "548" here, not to LBNL.**
- **Verification:** ✅ scope (arXiv, prior turn). Marginal-carbon internal claim 🟡 (needs full text).

### 22. The Infrastructure Equation: Water, Energy & Community Policy for Georgia's Data-Center Boom — Rogers, Ota, Burola & Piquado, arXiv 2602.10526, 2026 (RAND-style) ✅
- **Their contribution & novelty:** treats DCs as **clustered** infrastructure (not single projects) and delivers a **jurisdiction-specific (Georgia) policy roadmap** across water, energy, zoning, ratepayer-equity, and community engagement, from an expert convening.
- **Gap they claim:** governance underestimates **cumulative cluster effects** and lacks integrated oversight / transparency + regulatory coordination.
- **Method:** qualitative expert-convening policy analysis (no empirical modeling, no numbers).
- **6-axis:** J ~ (water + energy; carbon not foregrounded) · M ✗ · S ~ (water-intensity) · I ~ (mentioned, not quantified) · R = **Georgia/US only** · P ✓ (core — regulatory-gap + roadmap).
- **Delta to us:** a US **policy-gap** ally — its "regulatory coordination gap" finding supports our S10 thesis. We are quantitative, sub-national, multi-region; it is qualitative + single-state.
- **Verification:** ✅ (arXiv). Doc-discrepancy: none.

### 23. WATCH / Water-Constrained Geographic Load Balancing in Data Centers — Islam, Ren, Quan, Shakir & Vasilakos, IEEE TCC 5(2):208–220, 2015 🟡
- **Their contribution & novelty:** an early **water-aware scheduler** that caps a data center's **long-term water consumption** by exploiting **spatio-temporal diversity** of water via geographic load balancing.
- **Gap they claim:** water was ignored as a constraint in DC workload management.
- **Method:** water-constrained GLB (Lyapunov / virtual water queue per our docs); water treated as a **long-term budget/cap**, not a physical stock.
- **6-axis:** J ✗ · M ✗ · S ~ (water-constrained, spatio-temporal) · I ✗ · R ✗ · P ✗. **A scheduler (kill-list).**
- **Delta to us:** cite-and-exclude — it is an optimizer, and the "water-as-budget" precedent our old docs wanted to *extend into a stock* is **moot now that N2 (water-as-stock) is dropped.** Its relevance is reduced to "an early water-aware scheduler."
- **Verification:** 🟡 IEEE Xplore walled/empty; scope via search. **Doc-note:** title/DOI mapping is slightly ambiguous (WATCH vs "Water-constrained GLB" — possibly same paper, 10.1109/TCC.2015.2453982); and its framing as "the N2 water-as-stock precedent" is now irrelevant to our (dropped) N2.

### 24. Balancing Bits and Drops — Talukder, Bin Rahim, Sen Gupta, Ren & Islam, e-Energy'26, arXiv 2607.22617 ✅scope
- **Their contribution & novelty:** workload scheduling that **jointly optimizes water and carbon** efficiency using **AWARE-US county-monthly** water-stress accounting; also evaluates rainwater harvesting + dry cooling ("bits and drops").
- **Gap they claim:** water and carbon are optimized separately; water stress isn't captured at county-month granularity.
- **6-axis:** J ✓ · M ✗ (average) · S ✓ (AWARE-US) · I ✗ (generic workload) · R ✗ (US, county) · P ✗ (a scheduler + infra levers, not policy/accounting).
- **Delta to us:** the closest *joint + scarcity* neighbour — but **US-only, average carbon, a scheduler (not accounting), no inference, no India.** Our delta: marginal + inference + accounting-not-scheduler + EU/India + reg-gap map.
- **Verification:** ✅ scope (arXiv, prior turn). Doc-discrepancy: none.

### 25. AI Data Centers and the Water Use Feedback Loop — Akinade, Amanambu, Frame & Ren, arXiv 2606.21760, 2026 ✅
- **Their contribution & novelty:** formalizes the **"Water and AI Feedback Loop"** — AI DCs consume cooling water → water scarcity constrains siting → AI improves water-system efficiency — integrating three previously siloed areas. Introduces a **"Water Consumption Impact index"** (burden at community/utility scale).
- **Gap they claim:** these dynamics are studied in isolation, not as a coupled system.
- **Numbers:** across **10 US sites**, burden spans **0.2%–134% of host [water-utility] capacity** (three orders of magnitude).
- **6-axis:** J ✗ · M ✗ · S ~ (utility-burden index; capacity-relative, akin to Small-Bottle-Big-Pipe's construct, not AWARE scarcity-weighting) · I ~ · R ✗ (US) · P ✗.
- **Delta to us:** a conceptual feedback-framework + utility-burden index; US-only, water-only. We do joint C+W + AWARE scarcity + inference + India + reg-gap.
- **Verification:** ✅ (arXiv). Doc-discrepancy: none (note authors are Akinade/Amanambu/Frame/Ren — only Ren overlaps the core group).

---

### 26. Job-level Carbon and Water Footprint Estimation for HPC — Chen, Broekema & van Nieuwpoort, arXiv 2607.19150, 2026 ✅
- **Their contribution & novelty:** a unified **job-level** water + carbon accounting framework spanning **operational AND embodied** impacts (not runtime-only).
- **Gap they claim:** runtime-centric HPC metrics omit lifecycle/embodied impacts → biased sustainability assessment.
- **Finding:** **water is dominated by embodied impact; carbon by operational.** (A caution for us — we do operational water primarily.)
- **6-axis:** J ✓ · M ~ (operational-vs-embodied split, not grid-marginal) · S ✗ · I ✗ (general HPC jobs) · R ✗ · P ✗. Accounting/estimation, not optimizer.
- **Delta to us:** HPC job-level, no scarcity / inference / multi-region / policy; we are facility-month DC accounting incl. scarcity + marginal + India + reg-gap. Note their embodied-water finding as a stated scope limit of our operational-first approach.
- **Verification:** ✅ (arXiv). Doc-discrepancy: none.

### 27. Chasing Carbon: The Elusive Environmental Footprint of Computing — Gupta et al., HPCA 2021, arXiv 2011.02839 ✅
- **Their contribution & novelty:** quantifies computing carbon from industry data, splitting **operational** vs **hardware-manufacturing + infrastructure (embodied)**.
- **Gap they claim:** efficiency gains cut operational emissions, yet total footprint keeps growing — the embodied share is overlooked.
- **Finding:** **embodied carbon dominates** the lifecycle for modern mobile + datacenter equipment.
- **6-axis:** carbon-only, embodied, device-scale — J ✗ · M ✗ · S ✗ · I ✗ · R ✗ · P ~. **No water, no siting.**
- **Delta to us:** we **acknowledge embodied in one sentence** (hits the SI "critical materials" keyword) but do not build an embodied model. Cite for "embodied is large."
- **Verification:** ✅ (arXiv); the mobile-capex-49→86% and FB/Google scope-3 specifics our docs cite are 🟡 (not in abstract).

### 28. The Carbon and Water Footprints of Data Centers and What This Could Mean for AI — **Alex de Vries-Gao** (VU Amsterdam / Digiconomist), *Patterns* 7(1):101430, 2025/26 ✅
- **★ Authorship confirmed:** **de Vries-Gao (VU Amsterdam)** — **NOT Clarens** (our docs' warning is correct; do not misattribute).
- **Their contribution & argument:** a Perspective/top-down accounting synthesis arguing that AI power is estimable but carbon/water are **hampered by a disclosure crisis** — operators publish only company-wide averages that obscure AI-specific impacts; it **calls for mandatory disclosure**.
- **Numbers (2025):** AI carbon **32.6–79.7 Mt CO₂**; direct water **312.5–764.6 bn L**; indirect water intensity ~**3.4–3.92 L/kWh** (Meta) vs IEA's underestimated 1.04.
- **6-axis:** J ✓ (both, aggregate) · **M ✗** (isolates *AI share*, not grid-marginal — do not conflate) · **S ✗** (aggregate volume + disclosure argument, not scarcity-weighted) · I ~ (AI-share isolation, company-aggregate not per-query) · R ✗ (US-centric, no India) · **P ✓ (disclosure mandate)**.
- **Delta to us:** **framing / must-cite**, not a method competitor. Its disclosure-crisis argument *directly supports our openness + S10 reg-gap thesis* (we build the transparent, granular account it says is missing).
- **Verification:** ✅ full text (PMC). Doc-note: it's *Patterns* published Dec 17 2025 (vol 7(1)); our docs said "2026" — minor.

### 29. Measuring the Carbon Intensity of AI in Cloud Instances — Dodge et al., FAccT 2022, arXiv 2206.05229 ✅ *(dedupe: rows #29 = #31)*
- **Their contribution & novelty:** a framework to measure **software carbon intensity** using **location-based + time-specific MARGINAL emissions**, with empirical measurements across NLP/CV models on Azure.
- **Gap they claim:** practitioners lack easy/reliable access to carbon measurements → can't act.
- **Finding:** **geographic region is the largest reduction lever**; time-of-day is notable; evaluates pause-above-threshold and flexible-start.
- **6-axis:** J ✗ (no water) · **M ✓ (marginal — explicit)** · S ✗ · I ~ (covers training *and* inference; a 6.1B pretraining run tested) · R ~ (Azure regions) · P ~.
- **Delta to us:** methodological anchor for **marginal + region counterfactual**; we add water + scarcity + inference-attribution + India + accounting (not practitioner tactics).
- **Verification:** ✅ (arXiv); the "−71% / 16 regions" specifics 🟡. Doc-note: our docs said "training not inference" — it actually covers **both** (minor). **Dedupe rows #29 and #31 — same paper.**

### 30. Environmental Impact and Net-Zero Pathways for Sustainable AI Servers in the USA — Xiao, Fuso Nerini, Matthews, Tavoni & You, Nature Sustainability 8(12):1541–1553, 2025 🟡 *(recap, read prior turn)*
- **Their contribution & novelty:** projects the **joint carbon + water** footprint of **US AI-server buildout 2024–2030** and evaluates **net-zero pathways** (efficiency, grid decarbonization, siting).
- **Gap they claim:** no forward net-zero pathway analysis for AI-server environmental impact at national scale.
- **Numbers:** water **731–1,125 M m³/yr**; carbon **24–44 Mt CO₂e/yr** (2024–30); best practices could cut carbon up to **73%**, water up to **86%**.
- **6-axis:** J ✓ · M ✗ (scenario/ReEDS, not marginal) · S ~ (physical, spatial-distribution uncertainty) · I ✗ (AI-server *capacity*, not inference-workload) · R ✗ (US) · P ~ (net-zero pathways, not a reg-gap map).
- **Delta to us:** the closest joint-C+W US forward study; we add **India/EU + marginal + scarcity-weighting + inference-attribution + regulatory-gap map**.
- **Verification:** 🟡 (Nature walled; abstract via Nature/IDEAS/Oxford records, prior turn).

---

### 32. Why Transparency Matters for Sustainable Data Centers and Carbon-Neutral AI — Hankendi, Coskun & Sovacool, iScience 28(11), 2025 ✅
- **Their contribution & argument:** a Perspective arguing that the **lack of transparency in DC operational data** is the binding barrier to sustainable AI; without operational data, researchers can't build effective solutions. Lays out a **three-phase roadmap (2025–2035)**.
- **Gap they claim:** operational DC data isn't shared → innovation and regulation are hindered.
- **Numbers:** DCs potentially **9% of global electricity by 2030**.
- **6-axis:** J ~ · M ✗ · S ✗ · I ✗ · R ✗ · P ✓ (transparency roadmap). Perspective, not accounting.
- **Delta to us:** **framing / must-cite for the openness pillar** — we deliver the transparent, granular account they demand. (Sovacool is a major energy-social-science figure; Coskun/Hankendi = BU PeacLab.)
- **Verification:** ✅ (search + open BU-PeacLab PDF available).

### 33. Data Centers Water Footprint: The Need for More Transparency — Privette, Barros & Cai, AGU Advances 7:e2025AV002140, 2026 🟡
- **Their contribution & argument:** a commentary mapping the **multi-faceted DC water footprint** (direct cooling + electricity generation + supply chain) and arguing that while national/global volumes seem modest, **localized impacts are significant in water-stressed/drought regions**; transparency gaps undermine regulation, innovation, and community planning.
- **Gap they claim:** major transparency gaps in how much water DCs use.
- **6-axis:** J ~ · M ✗ · S ~ (**local water-stress emphasis**) · I ✗ · R ✗ · P ✓. Commentary, not accounting.
- **Delta to us:** framing / must-cite — its "**national modest, local significant**" argument *is* our scarcity-weighting + sub-national thesis, from a prominent hydrologist (Ana Barros). Supports S10 + scarcity.
- **Verification:** 🟡 (AGU walled; Wiley record + Eos highlight + open Authorea preprint).

### 34. Data Centre Energy Demand Projections within Shared Socioeconomic Pathways — Fan, Wilson, Kamiya & Mastrucci, *Energy and Climate Change* 7:100253, 2026 (Oxford ECI + IIASA) 🟡 ★
- **★ THE one paper in our TARGET JOURNAL** — same venue, same SSP/AR7 framing. Authorship + venue confirmed (IIASA PURE record).
- **Their contribution & novelty:** extends **data-centre electricity-demand projections to 2050** within the **SSP1–5** framework (most studies stop at ~5 years); a 3-step method + carbon-budget check; argues **DCs should be a separate end-use sector** in energy statistics.
- **Gap they claim:** near-term projections abound; few extend beyond 5 years due to uncertainty + no accepted methodology.
- **Numbers:** DC energy **~2,500 TWh by 2050** (SSP central; range ≈1,800–5,000); grid must fall **<100 gCO₂/kWh** to stay within the carbon budget.
- **6-axis:** J ✗ · M ✗ (average, SSP scenario) · S ✗ (no water) · I ✗ · R ✗ (**global + 6 world regions, NOT sub-national; no India-specific**) · P ~ (macro/AR7 framing).
- **Delta to us:** the **macro demand backdrop + positioning anchor** — our S11 is *sub-national + joint water*, complementing (not competing with) this global demand projection. **MUST-CITE** (same journal, editor-adjacent network).
- **Verification:** 🟡 (ScienceDirect walled; confirmed via IIASA PURE + search; full text on IIASA PURE if needed).

### 35. AI Data Centres as Grid-Interactive Assets — Colangelo et al., Nature Energy 11(2):254–261, 2026 🟡
- **Their contribution & novelty:** the **first field demonstration** of a software-only method ("Emerald Conductor") turning AI DCs into flexible grid resources — no hardware/storage. (Open version: arXiv 2507.00909.)
- **Gap they claim:** DC grid-flexibility was largely theoretical; needed a real demonstration.
- **Numbers:** on a **256-GPU cluster** in a hyperscale facility in **Phoenix, AZ**, reduced power **25% for 3 hours** during peak while maintaining AI QoS, by coordinating workloads to real-time grid signals.
- **6-axis:** J ✗ · M ✗ · S ✗ · I ✗ · R ✗ · P ~. **Demonstrates flexibility; does NOT quantify carbon or water.**
- **Delta to us:** evidence that DC load is **demonstrably flexible** → supports our forward policy-lever / demand-response framing; but it's a demo, not accounting. Cite for "flexibility is real."
- **Verification:** 🟡 (Nature walled; TechXplore + RePEc + open arXiv 2507.00909).

### 36. 2024 United States Data Center Energy Usage Report (LBNL) — Shehabi et al., Dec 2024 ✅
- **Their contribution:** the authoritative national bottom-up US DC energy census + projection (Congressional, Energy Act 2020); adds carbon + water footprint from **local grid mixes** and characterizes AI-accelerated servers.
- **Gap they claim:** prior US DC energy estimates were outdated/uncertain pre-AI-surge.
- **Numbers:** **58 TWh (2014) → 176 TWh (2023, 4.4% US) → 325–580 TWh (2028, 6.7–12%)**; CAGR 7%→18%→13–27%; explicit water↔energy cooling tradeoff.
- **6-axis:** national US; energy-primary + carbon/water via grid mix; **not** sub-national joint accounting; no inference-attribution / marginal / scarcity / policy-lever.
- **Delta to us:** our **CALIBRATION anchor** — sanity-check our US bottom-up sum against LBNL's national total. Not a competitor.
- **Verification:** ✅ (search + open LBNL PDF / eScholarship).

**Cluster note:** #28 (de Vries-Gao), #32 (Hankendi/Sovacool), #33 (Privette/Barros) form a **transparency-Perspective trio** — three high-credibility, independent calls that the *disclosure gap* is the barrier. This is a strong, citable foundation for our **openness pillar + S10 regulatory-gap** thesis (we build the transparent, granular account all three say is missing).

---

### 37. Sustainable AI Infrastructure: A Scenario-Based Forecast of Water Footprint under Uncertainty — Herrera, Xie, Menapace et al., J. Cleaner Production 526:146528, 2025 🟡
- **Their contribution & novelty:** a **global, scenario-based probabilistic (Bayesian-inspired)** forecast of DC water footprint — operational + off-site electricity + embodied — for 2030/2050, combining sparse data + expert priors + policy growth trajectories.
- **Gap they claim:** sparse data + deep uncertainty in DC water futures; no robust probabilistic method.
- **Numbers:** without mitigation, **global DC water could rise >7× by mid-century**; cooling-operational dominates.
- **6-axis:** J ✗ (water only) · M ✗ · S ~ · I ✗ · R ✗ (**global, not sub-national; no India-deep**) · P ~ (mitigation scenarios).
- **Delta to us:** methodologically adjacent to our **S11 water-scenario** stance, but global/water-only; we are sub-national + joint + marginal + scarcity + inference + India + reg-gap.
- **Verification:** 🟡 (JCP walled; scope via ResearchGate + ADS + **open EarthArXiv** `eartharxiv.org/repository/object/9039`).

### 38. Locational Marginal Emissions for Carbon-Aware Data Center Operations in Large-Scale Power Grids — Cote & Sun, arXiv 2512.18819, 2025 ✅scope
- **Their contribution & novelty:** characterizes **LME** across a **real large grid (WECC, 1,493-bus, 1-yr hourly)**; finds three regional LME patterns (hydro PNW / coal Intermountain / solar Sunbelt); LME-guided interventions hit **>85% accuracy** on actual emission reduction.
- **Gap they claim:** LME behavior in large-scale grids is understudied; addresses deliverability / double-counting / additionality.
- **6-axis:** J ✗ · M ✓ (core) · S ✗ · I ✗ (**DC-level, grid-attributed — not inference**) · R ✗ (US-Western) · P ~.
- **Delta to us:** the marginal-carbon **method on a real grid** (a real-WECC cousin of LMCE #16) — borrow the method; carbon-only, US-only, operations-focused, no water/inference/India.
- **Verification:** ✅ scope (arXiv).
- **⚠ Doc-discrepancy:** authors are **Cote & Sun** (docs didn't name). Our docs framed this as "**the highest scoop risk on the marginal-carbon ACCOUNTING/attribution axis**" with a "carbon-accounting theorem." Primary reads as **operations optimization** (load-shifting/siting *guidance*), grid-attributed, **not** inference-attribution accounting — that framing is **overstated**; our joint-marginal + water + inference + India axis is not threatened. The "theorem" claim 🟡.

### 39. Strategic Data Center Load Shifting: Implications for Market Efficiency and Transmission Value — Brenner, Roald & Amin, arXiv 2510.20805, 2026 ✅scope
- **Their contribution & novelty:** identifies two **market failures** from strategic DC load-shifting (discontinuous capacity-limit pricing; strategic positioning nullifying transmission-expansion value); **bilevel two-zone** model.
- **Gap they claim:** system-level market/transmission implications of DC flexibility are understudied.
- **6-axis:** J ✗ · M ~ (shadow prices) · S ~ (capacity) · I ✗ · R ✗ (two-zone) · P ~. **Carbon/cost/market only — no water.** Optimizer/market model.
- **Delta to us:** market-efficiency/transmission model — not a competitor; context for "flexibility can distort markets."
- **Verification:** ✅ scope (arXiv).
- **⚠ Doc-discrepancy:** **RETITLED** — our docs list "*Bilevel Analysis of Cost and Emissions Externalities from DC Load Shifting*"; the current (v3) paper is **market-efficiency/transmission-value focused**, not primarily emissions-externalities. Reduced relevance.

### 40. WaterWise: Co-optimizing Carbon and Water Footprint for Sustainable Data Centers — Jiang, Basu Roy, Kanakagiri & Tiwari, arXiv 2501.17944, 2025 ✅ (full text — India CONFIRMED)
- **Their contribution & novelty:** a **job scheduler** co-optimizing carbon + water; key insight: "**carbon and water sustainability are at odds** — optimizing one hurts the other." (Same group as ThirstyFLOPS.)
- **Gap they claim:** single-objective optimization misses the carbon↔water tradeoff.
- **6-axis:** J ✓ · M 🟡 · S 🟡 · I ✗ (batch/parallel jobs) · R 🟡 · P ✗. **Scheduler/optimizer, not accounting.**
- **✅ India claim CONFIRMED (full text, 2026-09-22):** regions = eu-central-2 (Zurich), us-west-2 (Oregon), eu-south-2 (Spain), eu-south-1 (Milan), **ap-south-1 (Mumbai)** — Mumbai is the one Asian region. Water **is** scarcity-weighted: onsite `E·WUE·(1+WSF)`, offsite `PUE·E·EWIF·(1+WSF)`. Carbon = **average** (real-time energy-mix intensity, not marginal). Workload = **generic batch/parallel jobs** (PARSEC + Google Borg, ~230k jobs), **NOT AI inference**. Our docs were accurate.
- **Delta to us (sharpened — important for positioning):** WaterWise is the **one prior paper touching India + scarcity + joint carbon+water** — but as a **batch-job scheduler, average carbon, with Mumbai as 1 of 5 AWS regions** (not India's facility landscape). So state "India unoccupied" **precisely**: *India sub-national, inference-attributed, facility-level **accounting** is unoccupied; WaterWise covers Mumbai only as an AWS region inside a scheduler.* Our delta vs WaterWise: accounting-not-scheduler + inference-not-batch + **marginal** + **sub-national-India-facility-level** + EU/US-too + reg-gap.
- **Verification:** ✅ full text (arXiv HTML) — regions + WSF confirmed verbatim.

### 41. Spatio-Temporal Shifting to Reduce Carbon, Water, and Land-Use Footprints — Attenni, Moawad, Bartolini & Thamsen, arXiv 2512.08725, 2025 (under review) ✅
- **Their contribution & novelty:** adds **land use** as a third footprint alongside carbon + water; spatial + temporal shifting over real AWS/Azure infrastructure (FaaS + big-data traces).
- **Gap they claim:** prior work optimized carbon *or* water independently; extends to land + cross-metric tradeoffs.
- **Numbers:** FaaS — carbon −85% / water −50% / land −45%; spatial shifting drives most gains; **cross-metric tradeoffs exist** (optimizing carbon can worsen water).
- **6-axis:** J ✓ (+land) · M ✗ (average) · S ✗ (physical water, explicitly not scarcity) · I ✗ (FaaS/big-data, not inference) · R ✗ (AWS/Azure US/EU, **no India**) · P ✗. Shifter/optimizer.
- **Delta to us:** the closest joint-**shifter** + strong evidence for the carbon↔water tradeoff our *joint* account resolves; we add marginal + scarcity + inference + India + accounting + reg-gap.
- **Verification:** ✅ (arXiv). Doc-discrepancy: none.

---

### 42. SLIT — Sustainable Carbon-Aware and Water-Efficient LLM Scheduling in Geo-Distributed DCs — Moore, Qi, Hogade, Milojicic, Bash & Pasricha, GLSVLSI'25 / arXiv 2505.23554, 2025 ✅ *(dedupe: #42 = #51)*
- **Their contribution & novelty:** co-optimizes **LLM QoS (TTFT) + carbon + water + cost** across geo-distributed DCs via an ML-based metaheuristic.
- **Gap they claim:** inference operational environmental costs are underexplored (inference can exceed training cost 25×/yr; 500 ml water per 20–50 requests).
- **6-axis:** J ✓ · M ✗ · S ✗ (volume) · I ✓ (**LLM inference**) · R ✗ (India not mentioned) · P ✗. Scheduler.
- **Delta to us:** an LLM-inference joint-C+W **scheduler** — but average carbon, no scarcity-weighting, no India, scheduler-not-accounting. (Same HP/Colorado-State group as MARLIN.)
- **Verification:** ✅ scope (arXiv). **Dedupe #42 = #51.**

### 43. Routing LLM Inference to the Cleanest Grid in Real Time — Bernhard & Yardimci, arXiv 2608.06188, 2026 ✅
- **Their contribution & novelty:** a production-grade real-time inference **router** with (1) a real production pressure-based baseline, (2) **per-request energy from NVIDIA DCGM telemetry** (not nameplate TDP), (3) carbon settlement of every request vs **historical MOER** (not just forecast).
- **Gap they claim:** prior work lacks production baselines, granular per-request energy, and post-hoc marginal validation.
- **Method + numbers:** WattTime **MOER** + DCGM; CONUS multi-region GPU fleet; live A/B + 1-yr replay; **50.9%** GPU-attributable operational emissions reduction vs round-robin (95% CI 48.5–53.3%).
- **6-axis:** J ✗ (carbon only, **no water**) · **M ✓ (MOER marginal)** · S ✗ · **I ✓ (per-request DCGM)** · R ✗ (CONUS/US only) · P ~. **ROUTER, not accounting.**
- **Delta to us:** THE closest paper on the **marginal + inference** axis — it confirms that axis is thin for us (US-carbon marginal inference-routing is *occupied*). But it's a US carbon router, **no water, no accounting, no India**. Our delta: joint-water + scarcity + accounting-not-router + EU/India + reg-gap.
- **Verification:** ✅ (arXiv). Doc-note: authors are **Bernhard & Yardimci** (docs didn't name); "19 US subregions / 50.9% replay" ≈ confirmed (CONUS multi-region, 50.9% CI 48.5–53.3%).

### 44. Governing AI Data Center Growth in Water-Stressed Regions: Siting, Transparency & Water Justice — Al Khaldy, Gheraibia & Hamarsheh, IGI Global (ed. Mohapatra), 2027, pp.187–220 🟡 *(dedupe: #44 = #74)*
- **Their contribution & novelty:** a **governance framework** combining hydrological screening + public disclosure + water-justice safeguards; **place-based regulation** evaluating cumulative withdrawals, drought sensitivity, emergency curtailment, community participation, enforceable reporting.
- **Gap they claim:** DC growth is a water-governance issue lacking place-based regulation.
- **6-axis:** qualitative governance — J ~ · M ✗ · S ~ (water-stress) · I ✗ · R ✗ · P ✓ (policy instruments).
- **Delta to us:** qualitative governance / water-justice — **supports our S10 reg-gap + (diagnostic, non-prescriptive) equity framing**; we provide the quantitative account underneath. Forthcoming 2027 book chapter.
- **Verification:** 🟡 (IGI walled; scope via IGI page + ResearchGate). Doc-note: previously "dropped/inaccessible" — now scoped. **Dedupe #44 = #74.**

## REL-3 — context / method-input / field papers

### 45. Advances and Challenges in Energy and Climate Alignment of AI Infrastructure Expansion — Lal & You, Advances in Applied Energy 20:100243, 2025 (Cornell) ✅
- **Their contribution & novelty:** a **review** of AI-infrastructure energy/climate implications + proposes quantitative scenario-based frameworks; a field **gap-map**.
- **Gap they claim:** the energy/climate consequences of deploying **AI infrastructure itself** are underexplored (vs Green-AI model-level work or AI-for-sustainability).
- **6-axis:** review — J ~ · M ✗ · S ✗ (**water-light**) · I ✗ · R ✗ (**US/EU/China, no India**) · P ~.
- **Delta to us:** **must-cite field gap-map** (Fengqi You is a prominent energy-systems figure); it explicitly flags region-specific frameworks + water as underdeveloped — exactly what our sub-national joint-water-India account fills.
- **Verification:** ✅ (search + prior PDF read; ResearchGate). Confirmed Lal & You, Cornell.

---

### 46. Environmental Cost of AI's Energy Use: Carbon, Water and Land Footprints — UNU-INWEH (United Nations University), June 2026 ✅
- **Their contribution:** a high-visibility **UN institutional assessment** quantifying AI's carbon **+ water + land** footprints globally.
- **Gap they claim:** AI's environmental cost can't be understood through carbon alone; governance lags the growth.
- **Numbers (2030):** **945 TWh** electricity (~3× Pakistan+Bangladesh+Nigeria combined); water ≈ basic annual needs of **1.3 bn people** in Sub-Saharan Africa; land **>14,500 km²**.
- **6-axis:** J ✓ (carbon+water+land, **global aggregate**) · M ✗ · S ~ (burden-shifting-to-stressed-regions argument) · I ✗ · R ✗ (global) · P ✓ (governance-lagging).
- **★ Alignment:** its thesis — "**low-carbon is not automatically low-water or low-land**; single-metric evaluation hides trade-offs and shifts burdens onto already-stressed regions" — **is our joint + scarcity + (diagnostic) equity argument, from the UN.** High-visibility framing/must-cite.
- **Delta to us:** global institutional framing; we provide the sub-national quantitative account it calls for. Not a competitor.
- **Verification:** ✅ (UNU + EurekAlert + multiple).

### 47. How Hungry is AI? Benchmarking Energy, Water & Carbon of LLM Inference — Jegham, Abdelatti, Koh, Elmoubarki & Hendawi, arXiv 2505.09598, 2025 ✅ *(recap)*
- **Their contribution & novelty:** benchmarks **joint energy + water + carbon of LLM inference** across ~30 API models (inferred hardware + provider PUE/WUE + DEA eco-efficiency ranking).
- **Gap they claim:** no cross-model per-inference E/W/C benchmark incl. proprietary models.
- **Numbers:** 0.42 Wh short query (→ illustrative 35,000 homes / 1.2 M people water); ~86× spread across models.
- **6-axis:** J ✓ (per-query) · M ✗ (average) · S ✗ (physical) · **I ✓ (per-query inference)** · R ✗ (US/China, no India, no sub-national) · P ✗.
- **Delta to us:** a per-query benchmark that **out-granularizes us on inference** — our edge is sub-national + scarcity + marginal + policy + India. Cite as a source of per-query E/W/C factors.
- **Verification:** ✅ (arXiv, prior turn).

### 48. Optimizing Place-Based Data Infrastructure Siting: Balancing Energy, Environment, and Communities — Gutta, Popova Zhuhadar, Williamson, Bhatia et al., ACS ES&T Water 6(2):554–557, 2026 ✅
- **Their contribution & novelty:** a short viewpoint/framework for siting hyperscale DCs that **balances energy, environment, and community** concerns (U Louisville / Western Kentucky group; Kentucky-oriented).
- **Gap they claim:** siting decisions ignore multi-stakeholder (community + environment) balance.
- **6-axis:** J ~ · M ✗ · S ~ · I ✗ · R ✗ (US) · P ~ (community/siting). Short article (4 pp.), not a quantitative joint account.
- **Delta to us:** supports our community/equity + siting-policy framing; we provide the quantitative sub-national account underneath.
- **Verification:** ✅ (search + open PMC13251721). Doc-note: previously "dropped/inaccessible" — now scoped; it's a 4-page viewpoint, not a major accounting paper.

### 49. Beyond the AI Energy Hype? DC-Establishment Growth, Electricity & Emissions across US States — Iqbal, Moharrak, Ahmed & Khurshaid, Frontiers in Environmental Science 14:1939591, 2026 ✅ ★
- **Their contribution & novelty:** **empirical evidence from observed data (not projections)** — tests whether DC expansion is *already visible* in realized state-level electricity/emissions.
- **Gap they claim:** bottom-up studies document rising DC electricity, but *realized-impact* empirical evidence is limited; projections are assumption-conditional.
- **Method:** balanced US **state panel** (50 states, 2010–2023, 700 obs, two-way FE); DC activity via NAICS establishment counts.
- **KEY FINDING — NULL:** no significant within-state association between DC-establishment growth and aggregate electricity (β = −0.0266, SE 0.0278, ns) or emissions; robust across all specs.
- **6-axis:** J ✗ · M ✗ (explicitly average; notes the marginal limitation) · S ✗ · I ✗ (associational, not causal) · R ✗ (**state aggregate = the problem**) · P ✓ (calls for facility-level disclosure).
- **★ Delta to us (VALIDATION, not competition):** the null at state-aggregate level **mandates facility/sub-national analysis** — the authors themselves: *"when demand shocks are spatially concentrated, aggregation can attenuate observable effects"* and *"statewide annual consumption is an imperfect indicator of the localized infrastructure pressures."* **This empirically justifies our sub-national/facility-month approach.** Strong motivation cite.
- **Verification:** ✅ full text (Frontiers OA).

### 50. Recalibrating Global Data Center Energy-Use Estimates — Masanet, Shehabi, Lei, Smith & Koomey, Science 367(6481):984–986, 2020 🟡
- **Their contribution & novelty:** a bottom-up recalibration showing global DC energy growth **slowed** due to efficiency gains — rebutting "doubling/tripling" narratives.
- **Gap they claim:** prevailing top-down extrapolations overstated DC energy growth.
- **Numbers:** ~**205 TWh (2018)** [🟡 well-established but not in the fetched snippet]; efficiency offset ~6× compute growth; smart policy can sustain near-term.
- **6-axis:** global energy, pre-genAI; no water / sub-national carbon / inference / marginal / policy.
- **Delta to us:** the canonical **"bottom-up beats top-down"** macro citation + energy baseline; not a competitor.
- **Verification:** 🟡 (Science walled; authors + scope confirmed via ADS/PubMed; 205 TWh figure 🟡).

---

### 52. ThirstyFLOPS: Water Footprint Modeling and Analysis Toward Sustainable HPC — Jiang, Kanakagiri, Basu Roy & Tiwari, arXiv 2510.00471 / SC'25, 2025 ✅ *(recap)*
- **Their contribution & novelty:** a water-footprint analysis framework for **HPC systems** (region-specific WUE + EWIF), explicitly "in contrast to the growing focus on carbon."
- **Gap they claim:** HPC water footprint is underexplored vs carbon.
- **6-axis:** J ✗ (**water-FOCUSED, not joint carbon**) · M ✗ · S ✓ (region-specific) · I ✗ (HPC, not inference) · R (4 systems: Italy/Japan/US, **no India**) · P ✗.
- **Delta to us:** water-only HPC; we're joint + marginal + inference + India + accounting + reg-gap. **(Doc-correction from prior turn: our docs over-labeled it "joint carbon+scarcity-water" — it's water-focused.)**
- **Verification:** ✅ (arXiv abstract, prior turn).

### 53. Water Footprint of Datacenter Applications: Manufacturing, Operational, and Decommissioning Phases — ACM SoCC'25, 10.1145/3772052.3772216 🟡 PENDING
- **Status:** ACM DL walled (403). Our docs: lifecycle water across mfg/operational/decommissioning phases. **UNVERIFIED** — search pending (batch 12). Do not rely on the doc description until confirmed.

### 54. CarbonClarity: Uncertainty in Embodied Carbon for Sustainable Computing — Chen, Han, Bhagavathula & Gupta, arXiv 2507.01145 / ICCAD'25, 2025 ✅
- **Their contribution & novelty:** a **probabilistic** embodied-carbon framework — models embodied carbon as **distributions** (not point estimates), capturing supply-chain uncertainty (energy/gas per area, yield, node carbon intensity).
- **Gap they claim:** existing embodied-carbon models are deterministic → uninformed carbon-aware decisions.
- **Numbers:** 7nm mean→95th-percentile gap up to **1.6×**; chiplet/mature nodes cut the 95th-pct by 18% vs monolithic.
- **6-axis:** embodied carbon only — J ✗ · M ✗ · S ✗ · I ✗ · R ✗ · P ~.
- **Delta to us:** **kin to our S9 Monte-Carlo uncertainty** — the precedent for uncertainty-propagated/distributional coefficients. Cite for the *uncertainty-treatment method*, not embodied carbon.
- **Verification:** ✅ (arXiv). Doc-discrepancy: none.

### 55. Water Use in the US Energy System: A National Assessment and Unit-Process Inventory — Grubert & Sanders, ES&T 52(11):6695–6703, 2018 ✅
- **Their contribution & novelty:** the first national **unit-process inventory** of US energy-system water **consumption AND withdrawal** (99% of US primary energy), by fuel/process.
- **Gap they claim:** no comprehensive US energy-system water inventory distinguishing withdrawal vs consumption.
- **Numbers:** US energy system withdrew ~**2.2×10¹¹ m³/yr** (~40% of US water); energy-related consumption ~10% of US total.
- **6-axis:** US energy-system water (not DC-specific) — coefficient/context source.
- **Delta to us:** cite for **fuel-cycle water + the withdrawal-vs-consumption distinction** (complements Macknick EWIF, #10). Not a competitor.
- **Verification:** ✅ (search + open preprint emilygrubert.org). Doc-discrepancy: none.

---

### 56. Virtual Water Transfers of the US Electric Grid — Chini, Djehdian, Lubega & Stillwell, Nature Energy 3(12):1115–1123, 2018 ✅
- **Their contribution & novelty:** maps **virtual water flows embedded in inter-regional electricity transfers** across US power control areas (2010–2016) — an understudied part of the energy-water nexus.
- **Gap they claim:** virtual water transfers of electricity are understudied despite policy/conservation importance.
- **Numbers:** blue-water transfers 9.21 → 11.21 km³ (2010→2016); grey-water 50.18 → 71.64 km³.
- **6-axis:** US grid virtual-water (not DC-specific) — context source.
- **Delta to us:** the **precedent for attributing off-site (scope-2) DC water to the GENERATION region**, not the DC's own state — underpins our S3 off-site water spatial logic. Cite; not a competitor.
- **Verification:** ✅ (search; Nature Energy record + Illinois/Stillwell group).

### 57. Data Centre Water Consumption — Mytton, npj Clean Water 4:11, 2021 ✅
- **Their contribution & novelty:** a review/critique of DC water use — direct cooling water (in some cases **57% potable**) + indirect (non-renewable electricity generation) — and documents a **disclosure gap: <⅓ of operators measure water consumption** (CONFIRMED).
- **Gap they claim:** DC water use is under-measured and opaque.
- **6-axis:** water; disclosure-gap review/critique.
- **Delta to us:** cite for the WUE/WUE_source distinction + the **disclosure gap** (supports our openness pillar).
- **Verification:** ✅ disclosure-gap + water-source composition confirmed (search; open access + author's GitHub). The specific "~2.18 L/kWh / 25.5 ML/yr" figures remain 🟡 (full-text detail).

### 58. Unreflective Use of Old Data Sources Produced Echo Chambers in the Water–Electricity Nexus — Vaca-Jiménez et al., Nature Sustainability 4:537–546, 2021 ✅
- **Their contribution & novelty:** a citation-network audit of **2,426 papers** showing most water-electricity coefficients trace to a few **old US (recently also Chinese) sources** that "echo" through decades → confirmation bias + double-counting risk.
- **Gap they claim:** the field reuses vintage coefficients uncritically, creating false certainty.
- **6-axis:** methods/reliability critique (not accounting).
- **Delta to us:** **the reliability caveat that justifies our uncertainty bands (S9) + primary-sourcing discipline** — directly relevant to the vintage of Macknick/EWIF factors. Cite.
- **Verification:** ✅ (search + Groningen news).
- **⚠ Doc-discrepancy (coding-sheet fix needed):** the coding sheet's Papers tab still lists the **WRONG DOI** (`10.1038/s41893-021-00700-y`); the correct DOI is **`10.1038/s41893-021-00686-7`**. (Our prose docs already noted this; the sheet row was never fixed — **flag to fix in the xlsx.**)

### 59. Rethinking Load Growth: Integrating Large Flexible Loads in US Power Systems — Norris, Profeta, Patiño-Echeverri & Cowie-Haskell, Duke Nicholas Institute, 2025 ✅
- **Their contribution & novelty:** introduces **"curtailment-enabled headroom"** — how much new load the existing grid can absorb with brief, modest curtailment.
- **Gap they claim:** load-growth debates assume new capacity is needed; flexibility is under-counted.
- **Numbers:** the 22 largest BAs (95% of US load) could absorb **76 GW at 0.25% curtailment / 98 GW at 0.5% / 126 GW at 1.0%**.
- **6-axis:** US grid flexibility policy (energy).
- **Delta to us:** the **flexibility-headroom ceiling** our forward-lever/DR scenarios test against. Cite for "the grid has headroom *with* flexibility."
- **Verification:** ✅ (search; Duke + Utility Dive + DCD).

### 60. Flexible Data Centers Reduce Power-System Costs but Can Increase Emissions — Senga, Wang & Knittel (MIT), iScience 2026 ✅
- **Their contribution & novelty:** a **GenX capacity-expansion** analysis (3 US regions) showing DC flexibility cuts *system cost* but can *raise emissions*, region-dependent.
- **Gap they claim:** flexibility's cost benefit is assumed good; its emissions effect is ambiguous.
- **Numbers:** cost savings TX 5% / Mid-Atlantic 4% / West 2% (if >20% of load shifted); **flexibility can raise Mid-Atlantic CO₂ ~3%**; DC growth raises 2030 emissions **TX +58% / Mid-Atl +20% / West +24%**.
- **6-axis:** carbon + cost; US; **no water; system-average not marginal; not inference-attributed.**
- **Delta to us (important caveat):** the closest counterfactual-modeling cousin — **evidence that flexibility/cost-optimization can backfire on emissions.** With Sukprasert (#17), this is the honesty caveat our **S7 forward-lever** analysis must carry ("a lever can shift or raise burden"). We add joint water + marginal + inference + India + reg-gap.
- **Verification:** ✅ (search + MIT News + PMC13377865).

---

### 61. Commission Delegated Regulation (EU) 2024/1364 — First Phase of a Common EU DC Rating Scheme ✅ (via POLICY_DEEP_DIVE / EUR-Lex)
- **What it is:** the EU's mandatory DC sustainability-reporting instrument — the concrete **EU anchor** for our S10 regulatory-gap map.
- **Requires:** DCs with IT power **≥500 kW** report annually (first report 15 Sep 2024) the KPIs **PUE, WUE (=W_in/E_IT), ERF (energy-reuse factor), REF (renewable-energy factor)**, plus total/IT/renewable energy and total & potable water. Only **aggregated** data is published; **facility-level is confidential**.
- **6-axis:** J ✗ · M ✗ · **S ✗** · I ✗ · R (EU) · **P = the instrument itself.** — **Crucially mandates NONE of: carbon intensity, marginal carbon, scarcity-weighted water, or inference attribution** — i.e., exactly our four axes, by omission.
- **Delta to us:** it *defines* the EU side of the regulatory gap (rules stop at PUE/WUE efficiency + volumetric water). Cite the rule; we cannot extract EU facility rows from it (confidential).
- **Verification:** ✅ KPIs/threshold corroborated (POLICY_DEEP_DIVE's earlier EUR-Lex read + White & Case + multiple). **Note: the live EUR-Lex re-fetch returned empty this pass; relying on the prior verified read + wide corroboration.**

### 62. A Water Efficiency Dataset for African Data Centers — Shumba, Tshekiso, Li, Fanti & Ren, NeurIPS'24 CCAI Workshop, arXiv 2412.03716 ✅
- **Their contribution & novelty:** "**first-of-its-kind**" open dataset combining nation-level weather + electricity-generation data to estimate WUE for **41 African countries** across 5 climate regions; quantifies **LLM-inference** water (Llama-3-70B, GPT-4).
- **Gap they claim:** DC water-efficiency research is US-centric; Africa is unmeasured/underrepresented.
- **Numbers:** 9 of 11 selected African countries consume less water than global average (lower electricity water-intensity); 10-page report ≈0.66 L (Llama-3-70B) vs ≈59 L (GPT-4).
- **6-axis:** J ~ (water + electricity intensity) · M ✗ · S ~ (regional electricity water-intensity proxy) · **I ✓ (LLM inference)** · R = **Africa only (no India)** · P ✗.
- **Delta to us — a close *methodological cousin*:** it's the **under-covered-region + inference-water** analog of what we do for **India** (they did Africa; India is still unbuilt). Borrow the nation-weather + electricity-mix WUE approach; we add joint carbon + marginal + scarcity + sub-national facility-level + reg-gap.
- **Verification:** ✅ (arXiv). Doc-note: authors = Shumba/Tshekiso/Li/Fanti/**Ren** (Ren group + CMU); our docs over-specified the method as "cooling-tower wet-bulb regressions" — the paper uses **nation-level weather + electricity** data (not confirmed cooling-tower regressions). Minor.

### 63. Carbon-Aware Quality Adaptation for Energy-Intensive Services ("Quality Time") — Wiesner, Grinwald, Weiß, Wilhelm, Khalili & Kao, e-Energy'25, arXiv 2411.19058 ✅
- **Their contribution & novelty:** forecast-based **multi-horizon** optimization that adjusts the fraction of requests served at each **service-quality tier** to keep an always-on service within an **annual carbon budget** — for latency/location-bound services (unlike batch/geo shifters).
- **Gap they claim:** carbon-aware strategies target batch/geo workloads and fail for constant-availability services (e.g., large LLM services).
- **Numbers:** cuts LLM-service emissions up to **10%** (10,000s tons CO₂/yr).
- **6-axis:** J ✗ (carbon only) · M ✗ · S ✗ · I ✓ (LLM) · R ✗ (single-location) · P ~ (carbon-budget).
- **Delta to us:** a carbon-only quality-adaptation optimizer; we're joint accounting. Not a competitor.
- **Verification:** ✅ (arXiv). Doc-note: actual title is "Carbon-Aware Quality Adaptation…" (our docs' "Quality Time: carbon value-of-information" is an older framing). Minor.

### 64. Measuring and Standardizing AI's Energy Footprint — FAS (Federation of American Scientists), 2025 ✅
- **Their contribution:** a policy report proposing a standardized metric framework — **CUE (carbon usage effectiveness, kgCO₂/kWh)**, PUE, and **Performance-per-Watt (inferences/FLOPS per watt)** — plus a phased voluntary→mandatory reporting roadmap (DOE/NIST/EPA develop; EIA/NTIA/industry report; DOE grid offices/FERC integrate).
- **Gap they claim:** no standardized, comparable way to measure AI's energy/carbon footprint → can't plan or regulate.
- **6-axis:** policy/metrics framework — J ~ · M ✗ · S ✗ · I ~ (PPW inference-per-watt) · R ✗ · P ✓ (reporting roadmap).
- **Delta to us:** a **motivation cite** — our reproducible, standardized, facility-level account is a concrete instance of what FAS calls for; supports the **openness pillar + S10**. (Context: a Jan 2025 EO directed DOE to draft lifecycle DC reporting incl. embodied carbon, water, waste heat.)
- **Verification:** ✅ (search + fas.org).

---

## Batch 14 — the carbon-shifting / routing / scheduling kill-list cluster (rel-3)

> **Why these are on the KILL-LIST:** every paper here *optimizes operations* (shift load in time or space, provision renewables, route inference). Our paper deliberately does **not** build a scheduler/optimizer — it builds a **static, reproducible, sub-national account + regulatory-gap map**. These are cited as "the field optimizes; we account & map." The sharpest proof of the boundary is **#69 MARLIN**: even the first work to do joint carbon+water+inference (2026) does it as a real-time RL scheduler, not an account — the accounting cell stays empty.

### 65. Carbon-Aware Computing for Datacenters (Google CICP) — Radovanović, Koningstein, Schneider et al., IEEE Trans. Power Systems 2023 (arXiv 2106.11750) ✅
- **What it does:** Google's Carbon-Intelligent Compute Management — **temporal** load shifting via **Virtual Capacity Curves (VCCs)** that cap hourly resources for time-flexible workloads, pushing them to cleaner hours across Google's global fleet.
- **Gap they claim:** hyperscale compute emits more carbon than needed if run without regard to hourly grid carbon.
- **6-axis:** J ✗ (carbon only) · M ~ (hourly grid signal; avg vs marginal not stated on page) · S ✗ · I ✗ · R (global fleet, no sub-national detail) · P ✗.
- **Delta to us:** operations, not accounting; temporal only; no water; no India. Cite as the canonical carbon-aware-scheduling reference we deliberately do **not** extend.
- **Verification:** ✅ (arXiv abstract). Avg-vs-marginal not specified on the abstract page.

### 66. A Guide to Reducing Carbon Emissions through Data Center Geographical Load Shifting — ACM e-Energy'21 (arXiv 2105.09120) ✅
- **Their contribution & novelty:** proposes a **locational marginal carbon emission metric (λ_CO₂)** and benchmarks it against 3 other shifting metrics for **spatial** (geographic) load shifting over a year, using electricity-market clearing (congestion + power-flow physics) to expose that carbon intensity differs between even nearby locations.
- **Gap they claim:** locational carbon data isn't public, so there's no good metric to guide *where* to shift load.
- **6-axis:** J ✗ · **M ✓ (locational marginal — λ_CO₂)** · S ✗ · I ✗ · R (US market) · P ✗ (it's a shifting metric, not a policy map).
- **Delta to us — a genuine reference for our S2 marginal Ceiling:** this is a clean **locational-marginal-carbon** precedent; we borrow the *concept* for our marginal-carbon Ceiling (US/UK only) but apply it to **accounting**, not load-shifting, and never for India (India = 5 regional annual-average grids, so marginal is impossible there).
- **Verification:** ✅ (arXiv). Note: a closely related earlier arXiv exists (2010.03379, "Environmental Potential of Hyper-Scale Data Centers… Locational Marginal CO₂") — same idea, likely same group.

### 67. Carbon Explorer: A Holistic Approach for Designing Carbon Aware Datacenters — Acun, Lee, Kazhamiaka, Maeng, Chakkaravarthy, Gupta, Brooks & Wu (Meta), ASPLOS'23 (arXiv 2201.10036) ✅
- **Their contribution & novelty:** a framework spanning the **multi-dimensional** design space — renewable capacity sizing (solar/wind mix), battery storage, and carbon-aware scheduling — that jointly accounts for **operational AND embodied** carbon.
- **Gap they claim:** prior work gives no holistic trade-off view and **ignores embodied carbon** of the decarbonization solutions themselves.
- **6-axis:** J ✗ (carbon only) · M ✗ · S ✗ · I ✗ · R (facility design, no sub-national grid map) · P ✗.
- **Delta to us:** they add the **embodied-carbon** dimension — which we deliberately scope **OUT** (we do operational carbon + water). Cite to justify our operational-only boundary and as the Meta counterpart to Google's CICP.
- **Verification:** ✅ (arXiv).

### 68. CASPER: Carbon-Aware Scheduling and Provisioning for Distributed Web Services — Souza, Jasoria, Chakrabarty et al. (UMass Amherst + Chalmers), IGSC'23 (arXiv 2403.14792) ✅  ⚠️ *substituted for unverifiable "GAR"*
- **⚠️ Doc-discrepancy (important):** our internal list had a slot **"#68 GAR"** — I searched and **found NO carbon-aware datacenter paper/system by that acronym**. Rather than invent an entry, I logged the genuine paper that occupies that sub-cluster (carbon-aware *scheduling + provisioning*). **"GAR" is flagged as an unverifiable label — do not cite it.**
- **Their contribution:** **CASPER** spatiotemporally schedules *and* provisions replicas of latency-sensitive distributed web services across regions to minimize carbon subject to latency SLOs; **open-source** (github.com/carbonfirst/casper).
- **6-axis:** J ✗ (carbon only) · M ✗ · S ✗ · I ✗ · R (geo-distributed, US/EU regions) · P ✗.
- **Delta to us:** operations again; carbon only; no water/India. Its **open-source release** is a useful *model* for our reproducibility pillar (a carbon-aware artifact done openly).
- **Verification:** ✅ (arXiv + ACM DL + GitHub).

### 69. MARLIN: Multi-Agent Game-Theoretic RL for Sustainable LLM Inference in Cloud Datacenters — Moore, Qi, Milojicic, Bash & Pasricha, arXiv 2605.13496 (May 2026) ✅ — **the closest joint-C+W+inference work, and it proves our niche**
- **Their contribution & novelty:** a game-theoretic **multi-agent RL** meta-scheduler (above Kubernetes/vLLM) that **co-optimizes time-to-first-token, carbon, water, AND energy cost** for **LLM inference**. Reports −18% TTFT, **−33% carbon, −43% water**, −11% cost vs SOTA.
- **Gap they claim:** existing LLM-inference management optimizes latency/cost but not carbon+water jointly.
- **6-axis (FULL-TEXT CONFIRMED):** J ✓ (**carbon + water — jointly!**) · **M ✓ (marginal carbon — CI_{d,e}, instantaneous grid emissions)** · **S ✗ (water is VOLUMETRIC — evaporative + blowdown + grid-based, in liters; no WUE/WSI/AWARE)** · **I ✓ (LLM inference)** · R (**global/uniform, no India, no sub-national**; Azure ChatGPT trace) · P ✗.
- **Delta to us — this is the load-bearing distinction of the whole paper:** MARLIN is the **first work I've found that does joint carbon + water + inference (2026)** — and it does it as a **real-time RL scheduler that ROUTES to reduce**, *not* as an account. Confirmed deltas: (1) **accounting, not scheduling**; (2) **scarcity-weighted water** (they're purely volumetric); (3) **sub-national India** (they're global-generic); (4) **regulatory-gap map**; (5) **reproducible open account**. *Note:* MARLIN **does use marginal carbon** — so marginal is NOT our delta vs MARLIN; the other four are. They answer "where should this query run *right now*?"; we answer "what is the true carbon+water footprint of AI DCs across India/US/EU, and where do the rules fail to see it?" **Even when the field reaches joint C+W+inference, it lands in the *scheduler* cell — the *accounting* cell it leaves empty is ours.**
- **Verification:** ✅ **FULL-TEXT READ (arXiv HTML)** — marginal carbon, volumetric water, global/no-India all confirmed from methods.

---

## Batch 15 — the MARL / grid-coordination / power-market tail (rel-3, closing the tier)

> **Same kill-list logic, escalated to the grid:** this cluster pushes DCs into **grid coordination, interconnection planning, and electricity-market participation**. All of it is *operations/planning*, none is *accounting*, and — tellingly — **the ones that touch the grid drop water entirely and mostly test on synthetic feeders (IEEE 14/33-bus), not real sub-national grids.** We cite them as "the field is racing to make DCs grid-flexible; nobody has first measured what those DCs actually cost in carbon+water, sub-nationally, which is the input their optimizers assume exists."

### 70. Hierarchical Multi-Agent RL for Carbon-Aware AI Data Centers in Power Distribution Systems — arXiv 2607.03324 (2026) ✅
- **What it does:** a **controller** — one workload-manager agent + local AIDC agents doing (i) temporal shifting of training jobs, (ii) spatial GPU-block allocation, (iii) cooling supply-air-temperature control — to cut carbon using **nodal carbon intensity (NCI)** from a carbon-emission-flow DSO problem.
- **6-axis:** J ✗ (carbon only) · M ~ (nodal/NCI, marginal-flavoured but on a **synthetic IEEE 33-node feeder**) · S ✗ · I ✗ · R ✗ (test system, **no real country/India**) · P ✗.
- **Delta to us:** control, not accounting; no water; synthetic grid. Cite as the MARL-controller end of the kill-list.
- **Verification:** ✅ (arXiv).

### 71. Grid-coordination cluster ("From Accounting to Coordination") — represented by EcoCenter: *Coordinating GPU Data Centers and Power Grid Regulation Service for Exogenous Carbon Benefits* — Jahanshahi, Golrouye, Anderson, Yu & Wong, arXiv 2601.22487, ICS'26 ✅  ⚠️ *theme-label, not an exact title*
- **⚠️ Doc-discrepancy:** "From Accounting to Coordination" is a **theme label in our notes, not a paper title** — I could not resolve it to a single work. It denotes the cluster arguing the field should move *past* carbon accounting *toward* grid coordination. Genuine members found: **EcoCenter** (2601.22487), *Adapting Datacenter Capacity for Greener Datacenters and Grid* (PlanShare, −11.6–12.6% carbon), *Carbon Responder* (2311.08589), *Electricity-Carbon Coordinated Dispatching… Nodal Carbon Potential*.
- **Representative (EcoCenter):** a **controller** maximizing GPU-DC **frequency-regulation** provision; introduces an "**Exogenous Carbon**" metric (grid-side reductions from DC regulation participation), which it argues can outweigh operational carbon.
- **6-axis (cluster):** J ✗ · M ~ (regulation/nodal) · S ✗ (no water) · I ✗ · R (grid-dependent, no India) · P ✗.
- **Delta to us — reinforces our framing:** these papers *presume an accounting exists* and jump to coordination. Our contribution is the missing upstream input: a sub-national carbon+**water** account. Cite the cluster to show the field skipped the measurement step for water and sub-national India.
- **Verification:** ✅ EcoCenter confirmed from primary (arXiv; authors + ICS'26 venue). The label itself remains flagged as a non-title theme.

### 72. To Defer or To Shift? The Role of AI Data Center Flexibility on Grid Interconnection — Yize Chen & Xiaogui Zheng, arXiv 2604.05376 (2026) ✅
- **Their contribution & novelty:** a grid **capacity-expansion planning** analysis of whether AI DCs should *defer* (temporal) or *shift* (spatial) load; finds — counter-intuitively — "**increasing flexibility does not necessarily translate to less generation capacity required**," with flexible loads cutting costs 3–21% but deferral showing diminishing returns.
- **Gap they claim:** treating DCs as "rigid, inflexible loads" in grid planning is "economically, mathematically and operationally untenable."
- **6-axis:** J ✗ · M ✗ · S ✗ · I ✗ · R (grid economics, **no specific country / no carbon / no water**) · P ✗ (grid-planning, not policy-gap).
- **Delta to us:** pure grid-economics planning; zero environmental accounting. Cite as evidence the flexibility discourse is carbon/water-blind.
- **Verification:** ✅ (arXiv).

### 73. When Market Prices Drive the Load: Modeling, Grid-Security Analysis, and Mitigation of Data Center Workload Scheduling — Pan, Alexakis & Konstantinou, arXiv 2604.06924 (2026) ✅ — *this is the "MDC / power-market" slot*
- **⚠️ Label resolved:** our note "Power-Market / **MDC**" → the paper's own term **"market-driven DCs (MDC)"**. Confirmed real, not a phantom.
- **Their contribution & novelty:** a job-level scheduling framework for **market-price-driven** DCs, showing price-driven scheduling improves economics but **increases voltage-security risk + congestion**; introduces load-redistribution policies to mitigate.
- **6-axis:** J ✗ · M ✗ · S ✗ · I ✗ · R (**IEEE 14-bus + Travis County, TX**; no carbon, no water, no India) · P ~ (mitigation policy, grid-security not environmental).
- **Delta to us:** grid-security/market analysis; no environmental accounting. Cite as the electricity-market end of the flexibility literature — again, no water, no sub-national carbon.
- **Verification:** ✅ (arXiv).

---

## Batch 16 — rel-2 tier, part 1 (broader-context / accounting-adjacent works)

> **Read with scoop-radar on:** two of these are *accounting* papers marked [LEAD]. One (#74) is the **closest single work to our US axis in the whole corpus** — sub-national + marginal carbon + water + US policy. It does not sink us (US is our "solid" tier, not the "deep" India anchor), but it is now our **US nearest-neighbour** and is added to `00_PROJECT_STATE.md §2.2`.

### 74. Environmental and Economic Implications of Artificial Intelligence Data Centers in the United States — Bolaños-Zuñiga & Lamadrid (Lehigh), arXiv 2608.09882 (Aug 2026) ✅ — **NEW US NEAREST-NEIGHBOUR; highest US-axis overlap**
- **Their contribution & novelty:** evaluates AI-DC electricity growth, cooling, and backup operation with impacts that "**depend on marginal generation mixes, transmission constraints, and the spatial and temporal distribution of demand**," arguing impacts are set by the "broader electricity, **water**, and land-use systems," not facility design alone. Calls for "integrated policy approaches."
- **Gap they claim:** prior work misses **location- and time-specific externalities**.
- **6-axis:** J ~ (carbon + water as local effects, but *not confirmed as one unified facility-level joint account*) · **M ✓ (marginal emissions)** · **S ✗** (water = "pressures on water resources," **not scarcity-weighted** on the abstract) · I ✗ (inference not singled out) · **R = US-only, sub-national** · P ~ (calls for integrated policy — **a call, not a regulatory-gap MAP**).
- **Delta to us (this is the important one) — the conjunction still holds, but tighten the US framing:**
  1. **India (deep):** they are US-only; our anchor is unbuilt by them.
  2. **EU (light):** absent.
  3. **Scarcity-weighting (AWARE):** they treat water as a volumetric/local pressure; we weight by basin scarcity.
  4. **Unified facility-level *joint* account:** they assess implications; we produce one open facility inventory carrying both carbon and water.
  5. **Regulatory-gap MAP:** they *call for* integrated policy; we *map* where the four axes fall through the rules across India/US/EU.
  6. **Reproducible open dataset + inference attribution.**
  → **Net:** this validates our own tiering decision (US = "solid," not "deep"). It is the reason our novelty must rest on **India + scarcity-weighting + reg-gap-map + reproducibility**, NOT on US sub-national marginal carbon (now occupied).
- **Verification:** ✅ **FULL-TEXT READ (arXiv HTML) — all deltas now CONFIRMED, not assumed:** (a) water is **purely volumetric** (WUE, L/kWh; Table 5 by cooling tech + generation source) — **no AWARE / no scarcity weighting**; (b) **NOT a unified facility-level joint account** — carbon (via marginal mixes) and water (via cooling config) are assessed **separately** at system/regional scale; (c) **no open data/code** released; (d) **US-only**. → Our five US-axis deltas (India, EU, scarcity-weighting, unified joint facility account, open+reproducible) all hold against the closest competitor. This is the strongest confirmation of the conjunction we have.

### 75. The Environmental Impact of AI Servers and Sustainable Solutions — A. Patel, Mahalingam & R. Patel, arXiv 2601.06063 (2025) ✅
- **Their contribution:** a **literature-based review + quantitative projections + case study** of electricity, water, and carbon demands of DCs; projects US water-consumption increases of **200–300 billion gallons/yr by 2030**; surveys cooling-design and siting mitigations.
- **Gap they claim:** need to consolidate footprint estimates + feasible mitigation strategies.
- **6-axis:** J ~ (carbon + water, but projected/review-level) · M ✗ · S ✗ · I ✗ · R (US + global trends, **no India-specific**) · P ✗.
- **Delta to us:** a review-projection, not an original facility-level account; no sub-national marginal, no scarcity-weighting, no India. Cite for US water-growth magnitude context.
- **Verification:** ✅ (arXiv).

### 76. Recasting AI Data Centers as Engines for Carbon Removal — Fang, Zhang, Shang & Ma (CityU HK), arXiv 2605.13114 (2026) ✅
- **Their contribution & novelty:** a **proposal paper** — thermodynamically integrate AIDC **waste heat + heat pumps → direct air capture (DAC)**; region-resolved US assessment shows several states reach removal ratio >1 (net-negative) under 2030 scenarios; in carbon-intensive regions integration flips DAC from net-positive to net-negative.
- **Gap they claim:** AIDC waste heat is wasted; coupling it to DAC lowers levelized capture cost.
- **6-axis:** J ✗ (carbon only) · M ✗ · S ✗ (**no water**) · I ✗ · R (US, region-resolved) · P ✗.
- **Delta to us:** a mitigation/solutions proposal, out of our accounting scope. Cite as an example of the "AIDC-as-solution" literature; not a competitor.
- **Verification:** ✅ (arXiv).

### 77. Electricity Demand and Grid Impacts of AI Data Centers: Challenges and Prospects — X. Chen, X. Wang, Colacelli, M. Lee & **Le Xie**, arXiv 2509.07218 (2025) ✅
- **Their contribution:** a **comprehensive review + vision** of AI-DC electricity demand (across model-prep / training / fine-tuning / inference) and grid impacts (long-term planning / short-term operation / real-time dynamics).
- **Gap they claim:** need an integrated understanding of how AI infrastructure and grids must co-evolve.
- **6-axis:** J ✗ · M ✗ · S ✗ (**no carbon/water on abstract**) · I ~ (demand broken out by inference stage) · R (unspecified) · P ✗ — a synthesis, not an account.
- **Delta to us:** review, not accounting. **Track the author: Le Xie** is part of the Harvard/Texas-A&M siting-toolkit group we flagged as a US threat — this is that group's grid-demand review, useful for anticipating their trajectory.
- **Verification:** ✅ (arXiv).

### 78. Advancements and Future Outlook of AI in Energy and Climate Change Modeling — *Advances in Applied Energy* (Elsevier), Jan 28 2025, ScienceDirect S2666792425000058 ✅  ⚠️ *CORRECTED journal*
- **⚠️ CORRECTION (my error, fixed 2026-09-22):** first logged as being in our target journal *Energy and Climate Change*. **Wrong.** The pii prefix **S2666-7924 = *Advances in Applied Energy*** (ISSN 2666-7924, verified via ISSN portal + DOAJ). The paper's *title* contains "energy and climate change" (the modelling topic), which misled a search snippet into naming that as the journal. It is **NOT** in our target journal.
- **What it is:** a review of **AI/ML as a tool for** energy & climate modeling (predictive analytics, distribution optimization, renewable maintenance) — AI-*for*-climate, **not** AI's environmental footprint. Orthogonal to us.
- **6-axis:** n/a (AI-as-tool, not footprint accounting).
- **Delta to us:** orthogonal topic; low citation value (not even a journal-fit anchor now).
- **Verification:** ✅ journal corrected to *Advances in Applied Energy* (ISSN verified).

## Batch 17 — rel-2 remainder + a target-journal find (rel-2 tier COMPLETE)

### 79. Sustainable AIGC Workload Scheduling of Geo-Distributed Data Centers — Zhang, Xu, Lim & Niyato, arXiv 2304.07948 (2023) ✅
- **What it does:** a **MARL (actor-critic) scheduler** distributing ML **training** jobs across geo-distributed DCs to maximize GPU utilization while cutting operational cost + carbon (up to 28.6% improvement), using real workload / energy-price / carbon-intensity traces.
- **6-axis:** J ✗ (carbon only) · M ~ (uses carbon-intensity traces; avg-vs-marginal unstated) · S ✗ · I ✗ (training, not inference) · R (geo-distributed, unspecified) · P ✗.
- **Delta to us:** scheduler, not account; no water/India. Kill-list.
- **Verification:** ✅ (arXiv).

### 80. DynamoLLM: Designing LLM Inference Clusters for Performance and Energy Efficiency — Stojkovic, Zhang, Goiri, Torrellas & Choukse (Microsoft), arXiv 2408.00741, HPCA'25 ✅
- **Their contribution & novelty:** "**first energy-management framework for LLM inference**" — dynamically reconfigures the inference cluster (instances, parallelism, GPU frequency) to minimize energy + cost under latency SLOs; saves 53% energy, **38% operational carbon**, 61% cost.
- **6-axis:** J ✗ (carbon only) · M ✗ (operational/avg) · S ✗ · **I ✓ (LLM inference)** · R ✗ (single-cluster) · P ✗.
- **Delta to us:** an inference-serving *energy optimizer*, not an account; no water/region/scarcity. Kill-list. (Sibling surfaced: **EcoServe 2502.05043**, carbon-aware AI inference systems — same optimizer family.)
- **Verification:** ✅ (arXiv + Microsoft Research + IEEE).

### 81. Carbon-Aware Optimization for Internet DCs with Renewables: Robust Workload Allocation & Carbon Procurement via Mean-Field Game — *Renewable Energy* (Elsevier), 2026, ScienceDirect S0960148126000261 🟡
- **What it does (from title/record):** an **optimizer** — robust workload allocation + carbon-credit procurement under uncertainty, modelled as a mean-field game among DCs.
- **6-axis:** J ✗ (carbon only) · M ~ · S ✗ (no water) · I ✗ · R (generic) · P ~ (carbon procurement).
- **Delta to us:** optimization + carbon markets, not accounting. Kill-list.
- **Verification:** 🟡 **ScienceDirect 403-walled** this pass; logged from the journal record + coding-sheet title. Low stakes (kill-list).

### 82. Advances and Challenges in Energy and Climate Alignment of AI Infrastructure Expansion — Apoorv Lal & Fengqi You, *Advances in Applied Energy* 20:100243 (2025), ScienceDirect S266679242500037X ✅  ⚠️ *CORRECTED journal (NOT our target journal)*
- **⚠️ CORRECTION (my error, fixed 2026-09-22):** first flagged as an on-topic paper *in our target journal* and a "strong positioning asset." **Wrong journal.** It is in ***Advances in Applied Energy*** (ISSN 2666-7924, verified), **not** *Energy and Climate Change*. Authors = **Apoorv Lal & Fengqi You** (You is EiC of *Advances in Applied Energy*). So it is an adjacent-journal near-neighbour, **not** a target-journal fit signal.
- **Their contribution:** a review/vision — surveys AI-infra energy/climate analyses; proposes **quantitative scenario-based frameworks**; frames challenges across AI-driven energy demand, **region-specific clean-energy strategies + economic competitiveness**, energy-sourcing levers, and **policy dynamics**; notes hyperscalers as major renewable offtakers.
- **6-axis:** J ✗ · M ✗ · S ✗ · I ✗ · R (region-specific clean-energy, not sub-national footprint) · **P ✓ (policy + sourcing levers)** — its lens is **clean-energy sourcing + transition alignment**, NOT a sub-national joint carbon+water *account*. **Adjacent, not a scoop:** it argues *how AI infra should source clean energy*; we *measure what AI infra actually costs in carbon+water, sub-nationally, and map the regulatory gap*.
- **Delta to us:** complementary — cite as a recent review whose call for region-specific alignment + policy our account operationalizes (we supply the measurement + gap map they presume). Still a useful related-work cite; just not a journal-fit argument.
- **Verification:** ✅ authors (Lal & You) + journal (*Advances in Applied Energy* 20:100243, 2025) confirmed; content from search abstract (ScienceDirect/ResearchGate full-text walled).

---

## Batch 18 — Web-sweep (final scoop check; NO scoop found — two allies, one adjacent joint-C+W)

### 83. Urban Infrastructure and Fossil-Fuel Industrial Legacy Drive US Data Center Siting — *Nature Cities* 2026, s44284-026-00487-z (NYU Tandon) ✅
- **What it is:** spatial-econometric study of **where US DCs actually are** — a 2025 dataset of **4,283 US commercial DCs**; 97.5% urban; siting driven by local power-plant nameplate capacity, broadband, retired coal plants, IT employment, hazards.
- **6-axis:** J ✗ · M ✗ · S ✗ · I ✗ · R (US, sub-national **location** but not footprint) · P ✗ — a *siting-driver* study, not a carbon/water account.
- **Delta to us + USE IT:** they explain *where/why* US DCs sit; we account for *what they cost* in carbon+water. **Complementary — and their 4,283-facility dataset is a candidate US facility-location source** (cross-check vs Guidi/Dominici lists). No India, no water/carbon.
- **Verification:** ✅ (Nature record via search; Nature full-text bot-walled).

### 84. The Plateau That Never Comes: When Efficiency Claims in Datacenters and AI Become Greenwashing — Gujral, Bhardwaj, Perera, Becker & Easterbrook (Toronto), arXiv 2606.04214 (2026) ✅ — **ALLY (motivation + framing)**
- **Their contribution & novelty:** a **rebound-informed diagnostic framework** with five tests — **metric, boundary, reinvestment, burden-shifting, governance** — arguing efficiency narratives become greenwashing when absolute energy/water/material/health burdens keep rising despite efficiency gains; proposes "**digital sufficiency**."
- **6-axis:** critique/governance across electricity, water, materials, waste (not a sub-national numeric account).
- **Delta to us — strong ally:** their diagnostic *demands exactly what we build* — absolute, boundary-honest, sub-national measurement + a governance lens. Cite in the intro/motivation: our open account is the evidentiary instrument their "metric/boundary/governance" tests require. Their framing sharpens our reg-gap-map narrative.
- **Verification:** ✅ (arXiv).

### 85. Sustainability-Constrained Workload Orchestration for Sovereign AI Infrastructure — Sergio Cruzes, arXiv 2604.09705 (2026) ✅
- **What it does:** an **optimizer** treating carbon intensity, water, and power capacity as **hard feasibility constraints**; introduces the "Feasible Sovereign Operating Region (FSOR)" + joint compute–network optimization.
- **6-axis:** J ~ (carbon+water as constraints) · M ✗ · S ✗ · I ✗ · R (no country/India) · P ~ (sovereignty/regulatory limits).
- **Delta to us:** operations, treating our *outputs* (carbon/water) as *input constraints*; no account, no India, no scarcity. Cite for the **sovereign-AI framing** (relevant to India-as-sovereign-AI motivation), not as a competitor.
- **Verification:** ✅ (arXiv).

### 86. AI Infrastructure Sovereignty — Sergio Cruzes, arXiv 2602.10900 (2026) ✅
- **What it is:** a **tutorial-survey** — nations maintaining operational control over AI via joint compute/network/energy design; "carbon intensity and water usage become **hard limits** on where/how AI can be deployed"; telemetry/digital-twins as enablers.
- **6-axis:** survey; carbon+water as deployment limits; no sub-national account, no India case study.
- **Delta to us:** framing/survey, not an account. Cite for sovereign-AI + "carbon/water as deployment limits" motivation (supports the India-sovereignty angle).
- **Verification:** ✅ (arXiv).

### 87. The Water Footprint of Artificial Intelligence: Emerging Solutions and Governance Imperatives — *Water Research* (Elsevier), 2026, PubMed 41967248 / S0043135426005488 ✅ — **ALLY (water + transparency)**
- **Their contribution:** a review — AI global water footprint could reach **4.2–6.6 billion m³/yr by 2027**; **two-thirds of post-2022 DCs are in water-stressed regions**; proposes a "digital water sobriety" framework; flags wastewater-cooling integration as unevaluated.
- **Key line for us:** "**Mandatory facility-level transparency is needed for water-sustainable AI**" — a direct call for exactly what we produce.
- **6-axis:** water-focused review + governance; not a sub-national numeric account.
- **Delta to us — strong ally:** motivation cite for our **water + facility-level transparency + reg-gap** pillars; the "two-thirds in water-stressed regions" stat directly motivates **scarcity-weighting**.
- **Verification:** ✅ (PubMed/ScienceDirect record via search; full-text walled).

### 88. Global Data–Water Symbiosis Reduces AI Infrastructure's Carbon and Water Footprint — Wang et al. (Harbin Inst. Tech.), *Environmental Science and Ecotechnology* 2026, PMC13147368 ✅ — *joint C+W, but global/national LCA (not our niche)*
- **Their contribution & novelty:** a **solution/optimization** — pairing DCs with wastewater-treatment plants (WWTPs) for effluent reuse + bidirectional heat recovery; **4,775 DCs + 57,547 WWTPs across 98 countries**; ~7,000 energy-recovery linkages; ~84 Mt CO₂e/yr + ~1,300 million m³ freshwater saved.
- **6-axis:** **J ✓ (joint carbon + water)** · M ✗ · S ✗ (gate-to-gate **LCA / ReCiPe 2016**, no scarcity weighting, no marginal) · I ✗ · **R (98 countries incl. India — but NATIONAL/admin aggregate, India = 2.11 Mt, a small share)** · P ✗ (a solution, not a policy-gap map).
- **Delta to us — the closest "joint C+W + India-included" work, and it confirms our niche:** it does joint C+W and *includes* India, but at **national/aggregate LCA** level as a **wastewater-symbiosis solution** — **not** sub-national, **not** facility-level, **not** marginal, **not** scarcity-weighted, **not** a regulatory-gap map, and India is 1 of 98 data points, not an anchor. Our sub-national, marginal+scarcity, facility-level India-anchored *account* is untouched. Cite as the "joint C+W solution" precedent + a water-reuse policy lever.
- **Verification:** ✅ (PMC full text).

### 89. The Carbon and Water Footprints of Data Centers and What This Could Mean for AI — review, ScienceDirect S2666389925002788 / PMC12827721 (2025) 🟡
- **What it is (from search):** a review/perspective on DC carbon + water footprints and implications for AI. Not an original sub-national account.
- **Delta to us:** review-level context cite; no facility-level sub-national joint account.
- **Verification:** 🟡 abstract/record via search (full-text walled); low stakes (review).

---

**RELEVANCE TIERS rel-4 → rel-2 COMPLETE + web-sweep COMPLETE (89 numbered works).** NO scoop of the six-axis conjunction found; the two nearest neighbours (#74 US, #69 MARLIN, #88 symbiosis) each miss ≥3 of our load-bearing axes, **full-text-confirmed**. Remaining:
1. **Rel-1 GNN archive corpus** (~40 papers, `coding_sheet_1.xlsx`) — **cluster pass** below (the question is the salvage/scrap verdict, not per-paper novelty).
2. **Residual firm-ups (all walled, all low-stakes / kill-list):** #53 ACM SoCC · #61 EU Reg clean EUR-Lex hit · #81 mean-field-game · #89 full-text. None affects the novelty claim.

---

## § GNN-Archive Cluster Verdict (rel-1) — "can the old project be absorbed?"

> **⚠️ Doc-discrepancy:** the coding sheet's rel-1 row points to **`coding_sheet_1.xlsx`, which does not exist in the repo** (lost with the deleted archive docs, or never created). So "the ~40 GNN papers" is not a retrievable list. The GNN corpus that actually matters for the absorption decision is (a) the **canonical spatio-temporal GNN architectures** the old project imitated, and (b) the old project's own methodology docs (`gat-based-forecasting/**`), both already autopsied in **`GNN_AUTOPSY.md`**. This section is the consolidated verdict, not 40 stubs.

**The canonical ST-GNN corpus (web-verified this pass):**
| Architecture | Target granularity | Graph (adjacency) | Learning | Verified mechanism |
|---|---|---|---|---|
| **DCRNN** (Li et al., ICLR'18) | **node-level** (per sensor) | physical road network + diffusion (random-walk) | **end-to-end** | diffusion convolution for space + RNN for time |
| **STGCN** (Yu et al., IJCAI'18) | **node-level** | physical adjacency | **end-to-end** | gated temporal conv ⊕ spatial graph conv "sandwich" |
| **Graph WaveNet** (Wu et al., IJCAI'19) | **node-level** | **self-adaptive** (learnable, backprop) | **end-to-end** | GCN + dilated causal conv; learns a node-embedding adjacency |
| **MTGNN** (Wu et al., KDD'20) | **node-level** | **graph-learning layer** (learned from data) | **end-to-end** | mix-hop propagation + dilated inception + learned graph |

**Why the old GAT project produced a null (confirmed vs the corpus + its own audit CSVs):** it inverted all three of the ingredients that make the corpus work —
1. **Target granularity:** it modelled a **region-level** target, not node-level. (The corpus forecasts each node; the old project aggregated to region.)
2. **Graph construction:** a **fixed co-location graph** with **~98% within-region edges** → the message-passing was **91.3% a no-op**; the successful corpus uses **adaptive/learned** adjacency that discovers useful cross-node structure.
3. **Integration:** a **post-hoc fixed-α blend** of GNN output onto a SARIMA/TSFM base, **not end-to-end** — so the graph never learned to serve the forecast. Bridged residuals were positively correlated; the blend could only add noise. (See `GNN_AUTOPSY.md §1–7` + `outputs_v2/audit/part5_*` co-location taxonomy CSVs.)

→ **Absorption verdict (unchanged, now corpus-confirmed): SCRAP the thesis, SALVAGE the assets.** The GNN *architecture* is the wrong instantiation for this problem and is **not** carried into the new paper (consistent with our kill-list: no new ML architecture). What is salvaged and folded into the new account:
- **Data pipeline:** Ember monthly (US/EU/India), GEM/Global-Integrated-Power, Aqueduct 4.0 water risk, G3P water storage — already downloaded in `datasets-2026-energy/`.
- **Geocoder:** `nbs/gat-colocation-weights-water-energy.ipynb` (facility→grid-region→basin linkage) — directly reusable for the India facility inventory.
- **Forecasting benchmark:** the measured **Chronos-2 > SARIMA > xLSTM** result (`MODEL_CHOICE.md`; Chronos-2 −21% RMSE vs SARIMA, CPU, 0 failures) — reusable *only if* the Ceiling's S11 forward projection is attempted; **not** load-bearing for the Floor.
- **Audit rigor:** the null-methodology harness (seasonal-naive skill floors, co-location vs random-control, Mantel geography-confound tests) — a **template for how we red-team our own account**, and a citable example of honest null-reporting.
- **PII to scrub before any release:** hackathon email in `gat-based-forecasting/**/docs/DATA.md`; a Windows user path in `SESSION_REVIEW_AND_NEXT_STEPS.md`.

---

## ✅ LITERATURE REVIEW PASS — COMPLETE (2026-09-22)

- **89 numbered works** read relevance-first (rel-5 → rel-2) + a full web-sweep, plus the **rel-1 GNN corpus** resolved as a cluster verdict.
- **No scoop of the six-axis conjunction.** The three nearest neighbours were **full-text-verified** to each miss ≥3 load-bearing axes: **#74** (US-only, volumetric water, separate not-joint, closed), **#69 MARLIN** (scheduler not account, volumetric water, global-generic, no India), **#88 symbiosis** (national/LCA aggregate, no marginal/scarcity, India = 1 of 98).
- **India anchor CONFIRMED UNBUILT (dedicated search 2026-09-22):** the India DC water/carbon space is held by **journalism + policy advocacy** (CEEW "How Is Data Centre Infrastructure in India Shaping Power & Water Use", Mongabay, Earth Journalism Network, Countercurrents) and **market reports** — **no peer-reviewed sub-national facility-level joint carbon+water account exists.** CEEW = the policy-side baseline (proposes an "AI Energy Star" rating + phased power/water standards → cite for S10, *not* a competing account). Citable India aggregates: DCs ≈**0.5% national electricity + ~150 billion L water (2024)**, both projected to **>2× by 2030**; electricity ~13 TWh (0.8%, 2024) → ~57 TWh (2.6%, 2030); **Mumbai ≈25% of DCs; all four hyperscale hubs on the groundwater watch list.** ⚠️ *Data note:* a market source counts **~271 operational DCs (Jan 2026)** vs our curated **129-operational / 194-total** — definitional (small colos included); reconcile at S0.
- **Load-bearing novelty confirmed:** India sub-national + scarcity-weighted water + unified facility-level joint account + regulatory-gap map + open/reproducible. Marginal carbon is **not** a differentiator vs #69/#74 (both use it) → keep it Ceiling-only, US/UK-labelled.
- **Allies for framing:** #84 (greenwashing diagnostic), #87 (water-governance, "mandatory facility-level transparency"), #49 (facility-level null validating our approach), the transparency-Perspective trio.
- **Doc-discrepancies caught (grep for ⚠️):** #62 method, #63 title, #68 "GAR" phantom, #71 theme-label, #78/#82 journal (my error — *Advances in Applied Energy*, not the target journal), `coding_sheet_1.xlsx` missing.
- **Residual walled (non-blocking):** #53, #61 clean EUR-Lex, #81, #89.

**This file supersedes `LITERATURE.md`.** Next stage = manuscript-section drafting (related-work narrative can be assembled directly from the relevance tiers + nearest-neighbour deltas here).

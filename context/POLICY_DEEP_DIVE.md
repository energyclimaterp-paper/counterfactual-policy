# POLICY DEEP-DIVE — Datacenter Environmental Regulation: US · EU · India

**Compiled:** 2026-09-16. **Purpose:** the exhaustive baseline for the paper's **S10 regulatory-gap map** — what environmental (energy/water/carbon) rules actually reach datacenters, so the burden map can be overlaid on where rules do and don't bite. **Method:** three parallel primary-source sweeps (US / EU / India), each under a strict verify-or-flag protocol, with the two most consequential new findings (the US federal deregulatory turn; the EU Omnibus narrowing of CSRD) independently re-verified by me. **Tags:** `[verified]` = I confirmed against a primary/official source this pass or earlier; `[sourced]` = from the sweep with a cited URL, not independently re-checked; `[flag]` = the sweep itself flagged residual uncertainty (carried forward honestly, never smoothed over).

---

## 0. The finding, in one line

**No instrument — enacted or proposed, at any level, in the US, EU, or India — mandates any of the four things this paper's account produces: (a) carbon *intensity*, (b) *marginal/locational* carbon, (c) *scarcity-weighted* water, or (d) *AI/inference-level* attribution.** `[verified — triple-confirmed across all three sweeps and my earlier checks]`

The regulated perimeter everywhere is some subset of: **large-load electricity rate/cost-allocation** (ratepayer protection, not environment), **volumetric water** (gallons/litres, or a WUE ratio), and **PUE-based efficiency** — plus, in the EU only, **entity-level GHG/water disclosure** (CSRD, and now shrinking). The four axes our accounting adds sit entirely outside that perimeter. In the US the 2025–26 federal trend is actively **deregulatory**, which makes the gap wider, not narrower.

---

## 1. The four-axis gap — the S10 thesis in one table

For each axis: is it mandated anywhere, and what is the *closest* instrument (to pre-empt the reviewer who says "surely someone requires this")?

| Axis our account adds | US | EU | India | Closest instrument anywhere (still not it) |
|---|---|---|---|---|
| **(a) Carbon intensity** (gCO₂/kWh, or per-compute) | **No** | **No** | **No** | EU **CSRD/ESRS E1-6** = GHG intensity *per revenue*, entity-level (not per-DC, now narrowed); Minnesota HF 16 & German EnEfG mandate *renewable supply* (an input, not a measured intensity) |
| **(b) Marginal / locational carbon** (hourly/nodal) | **No** | **No** | **No** | Voluntary **24/7 CFE tariffs** (NV/Google–Fervo; Xcel/Google); CNDCP's optional hourly-CFE — all voluntary, consumption-based, not marginal |
| **(c) Scarcity-weighted water** (volume × local stress) | **No** | **No** | **No** | EU **ESRS E3-4** discloses water use *"in areas of high water stress"* — location-*flagged volume*, entity-level, materiality-gated; CA AB 2619 "indirect water use" (proposed); India CGWA aquifer tiers (a permit gate, not weighted accounting) |
| **(d) AI/inference attribution** (per workload/model/query) | **No** | **No** | **No** | EU **AI Act Annex XI §1(2)(e)** = GPAI *model-level* energy documentation, training-oriented, no water/carbon, decoupled from DC reporting. US/India: zero |

Every "closest" is partial, non-binding, mis-scoped, or entity-level. The conjunction our paper measures is unregulated end-to-end.

---

## 2. United States — a deregulatory federal posture over a fast-growing rate-tariff patchwork

### 2.1 Federal
| Instrument | What it does (environment) | Status | Date | Tag |
|---|---|---|---|---|
| **EO 14318 "Accelerating Federal Permitting of Data Center Infrastructure"** | Directs agencies to create **categorical exclusions to minimize NEPA** for DCs; streamlines Clean Water Act permitting; opens federal land. **Deregulatory — no reporting, no metric.** | **Enacted (EO)** | 23 Jul 2025 (Fed. Reg. 90 FR 35385, 28 Jul 2025) | `[verified]` |
| **EO 14141 "Advancing U.S. Leadership in AI Infrastructure"** (Biden) | Had required federal-site AI DCs to bring **zero/low-carbon generation to match load** — the *only* federal carbon-matching mandate. | **Revoked** in 2025, no replacement | issued 14 Jan 2025 | `[verified]` |
| **Data Center Water & Energy Transparency Act of 2026** (H.R. 9825 / S. 4213) | Operators ≥25 MW report annual energy + water + **PUE + WUE** to EPA/DOE/USDA; aggregated public report. **No carbon, scarcity, or inference.** | **Proposed** (introduced) | 119th Cong., 2026 | `[verified]` |
| **FERC** — RM26-4 ANOPR (large-load interconnection); §206 show-cause orders to 6 RTOs (18 Jun 2026); PJM co-location order (18 Dec 2025) | Interconnection, cost allocation, reliability. **No environmental/carbon/water content.** | Mixed (ANOPR open; orders issued) | 2025–26 | `[sourced]` |
| **EPA/DOE ENERGY STAR** (DC & server certification); DOE FEMP / Better Buildings | **Voluntary** efficiency labeling/benchmarking. ENERGY STAR transferring EPA→DOE (MOA Mar 2026). | Ongoing, voluntary | — | `[sourced]` |
| **NEPA / Clean Water Act** | Apply only with a federal nexus; no DC-specific rule; EO 14318 *narrows* them. | Statute | — | `[sourced]` |

### 2.2 States — the real activity, but overwhelmingly rate-allocation, not environment
**Enacted, with genuine environmental content (few and thin):**
- **Minnesota — HF 16 (2025, Ch. 12), the strongest US law.** Very-large-customer class with no cost-shift; **electricity must meet Minnesota's renewable + carbon-free standard** (closest US thing to a carbon obligation on DC supply); **>100 M gal/yr consumptive water** triggers special permit conditions; green-building cert within 3 yrs. `[sourced]`
- **Virginia (2026, multiple signed):** HB 496 — water providers report **monthly potable + reclaimed water volume** supplied to DCs (eff. 1 Jan 2027); HB 507 — bars air permits for backup generators below **Tier-4-equivalent**; HB 153/SB 94 — siting assessments (sound + optional water/agricultural/historic); HB 323 — waste-heat study; plus ratepayer cost-allocation (SB 253/HB 1393) and Dominion's GS-5 large-load tariff. `[sourced]`
- **Maryland (2025, via veto override):** one-time **environmental/energy/economic impact study** (report due 1 Sep 2026). `[sourced]`
- **Oregon — POWER Act (HB 3546, 2025):** ≥20 MW rate class; **renewable-energy requirement before operations**; PUC-implemented ~Jun 2026. `[sourced]`
- **California — AB 1577 ("Data centers: reporting"):** operators report to the CEC location/size, **PUE**, energy, **annual water consumption**; anonymized-aggregated publication from 2029. **Enrolled — passed both houses, awaiting the Governor (Sept 2026).** No carbon/scarcity/inference. `[sourced]`

**Enacted, rate/cost-allocation only (no environmental metric):** Ohio (AEP tariff, 25 MW, take-or-pay), Wisconsin (We Energies, threshold cut 500→100 MW), Texas (SB 6, ≥75 MW, curtailment), Georgia (PSC >100 MW rule), Utah (SB 132), Indiana (I&M settlement), South Carolina (Santee Cooper rate), plus 20-odd more states — the dominant national vehicle is **ratepayer protection**, not environment.

**Proposed, water/closed-loop (worth watching):** South Carolina HB 4583 (**closed-loop cooling, zero-net-withdrawal**, on-site energy), Kansas SB 400 (closed-loop), California AB 2619 (**"indirect water use"** — water embedded in electricity, the most sophisticated US water metric in play), Pennsylvania HB 2150 (energy+water disclosure, passed House), Illinois SB 4016, Michigan SB 762, Iowa HF 2447, Georgia SB 421 (anti-NDA transparency — **died in committee**). `[sourced]`

**4-axis for the US:** all **No**. Closest: Minnesota/CA-SB886 (carbon-free *supply*, not intensity); voluntary 24/7 CFE tariffs (marginal-adjacent); AB 2619 indirect-water (not scarcity-weighted); SC/KS closed-loop (eliminates withdrawal, doesn't weight it). Inference attribution: **zero closest instrument.**

---

## 3. European Union — an efficiency-input perimeter plus a shrinking entity-disclosure regime

### 3.1 EU-level
| Instrument | What it requires | Status | Tag |
|---|---|---|---|
| **EED (EU) 2023/1791 Art. 12** | DCs ≥500 kW IT power publish **Annex VII** data (location, power, energy, **PUE**, waste-heat, water, renewables); Commission runs a European DC database + publishes aggregates. | In force; transposition uneven | `[sourced]` |
| **Delegated Reg. (EU) 2024/1364** | KPIs **PUE, WUE (=W_in/E_IT), ERF, REF**; first report 15 Sep 2024. | In force | `[verified earlier]` |
| **Draft mandatory sustainability rating scheme** | Rates DCs on **PUE + WUE classes**; electronic label from 15 Aug 2027; review 2029. Explicitly not carbon/scarcity/inference. | Draft (registered 26 Mar 2026) | `[verified earlier]` |
| **CSRD (EU) 2022/2464 + ESRS** | Entity double-materiality: **E1** GHG Scope 1/2/3 + intensity-per-revenue; **E3** water consumption incl. **"areas of high water stress."** Applies to operators as *companies*, not per-DC. | In force, **narrowed** (below) | `[sourced]` |
| **Omnibus I Directive (EU) 2026/470** | Sharply narrows CSRD scope (to **>1,000 employees AND >€450 m turnover** `[flag: final threshold]`); many wave-1 firms drop out. | **In force** (Council 24 Feb 2026; OJ Feb 2026) | `[verified]` |
| **Revised ESRS** | Cuts mandatory datapoints >60%; **retains E1 GHG + E3 water-stress** (materiality-gated). | Adopted 3 Jul 2026 | `[sourced]` |
| **EU Taxonomy (2020/852; 2021/2139 activity 8.1)** | "Substantial contribution" = implement the DC **Code of Conduct** practices, third-party verified ≥ every 3 yrs. | In force (classification) | `[sourced]` |
| **EU AI Act (EU) 2024/1689** | Art. 53 + **Annex XI §1(2)(e):** GPAI providers document **model energy consumption** (may estimate from compute). Art. 40 standards may address efficiency. | In force; GPAI duties from Aug 2025 | `[sourced]` |
| **Climate Neutral Data Centre Pact** | Voluntary: PUE ≤1.3/1.4, 75%→100% renewable/CFE by 2030, WUE metric. | Self-regulatory, non-binding | `[sourced]` |
| **Cloud & AI Development Act — COM(2026) 502** | Proposes **DC Acceleration Zones** conditioned on energy/water-efficiency + circularity. No carbon-intensity/scarcity metric confirmed. | Proposal (3 Jun 2026) | `[flag]` |

### 3.2 Member states
- **Germany — Energieeffizienzgesetz (EnEfG, in force Nov 2023, DCs ≥300 kW):** new DCs **PUE ≤1.2** (from 1 Jul 2026); existing ≤1.5 (2027) → ≤1.3 (2030); **waste-heat reuse ERF ≥10→20%**; **100% renewable electricity from 2027**. **Pending relaxation** (Federal Cabinet draft 24 Jun 2026, not yet law): existing-DC PUE eased to 1.6/1.4, renewables 100% pushed to 2030. `[sourced]`
- **Ireland — CRU decision CRU2025236 (12 Dec 2025):** ends the 2021–25 de-facto moratorium; new DCs need **matching generation/storage**, **≥80% of demand from *additional* renewable generation built in Ireland** over a 6-yr glide-up, plus a locational (constrained/unconstrained) test. `[sourced; flag: one tracker cites a different ref/date — official CRU ref used]`
- **Netherlands — national hyperscale ban** (amended Bkl, ~1 Jan 2024): no new hyperscale DCs (>10 ha AND ≥70 MW) except Eemshaven & Agriport; Amsterdam/Haarlemmermeer MVA caps + PUE <1.2 policy. Spatial/grid-driven. `[sourced]`
- **France:** EED transposition (Apr 2025) — DCs **>1 MW must install waste-heat recovery**, >500 kW report. `[sourced]`
- **Spain:** draft Real Decreto (consultation to 15 Sep 2025) — reporting ≥500 kW, heat-reuse ≥1 MW, top-15% efficiency ranking ≥100 MW. **Draft.** `[sourced]`
- **Nordics:** Sweden abolished the DC electricity-tax break (Jul 2023); Norway national DC strategy (Jan 2026, energy-recovery); Finland electricity-tax rise (Jul 2026); Denmark grid-capacity review. `[sourced]`

**4-axis for the EU:** all **No**. The perimeter is **facility efficiency inputs** (PUE/WUE/ERF/REF) + **entity GHG/water disclosure** (CSRD, now shrunk) + **siting/grid control** (IE/NL). Closest to our axes: ESRS E3-4 (water-in-stress, entity volume) and AI Act Annex XI (model energy doc) — both mis-scoped.

---

## 4. India — the anchor: incentive-first, near-zero binding environmental conditionality

### 4.1 National
| Instrument | Environmental content | Status | Tag |
|---|---|---|---|
| **Draft National Data Centre Policy 2025** (MeitY) | Reported to tie tax breaks to **PUE targets**; "encourages" green energy. No WUE/water/carbon mandate. | **Draft, under consultation, not notified** | `[flag: PUE-linkage via secondary source]` |
| **Draft Data Centre Policy 2020** (MeitY) | Infrastructure/essential-service status; no environmental provisions. | **Lapsed / superseded** | `[sourced]` |
| **Infrastructure status** (Harmonised Master List) | Credit/ECB access; threshold **≥5 MW IT load**; no environmental condition. | Notified 11 Oct 2022 | `[sourced]` |
| **EIA Notification 2006** (MoEFCC) | DCs need **Environmental Clearance only via building ≥20,000 m² (item 8(a))** — Category B, typically **no public hearing, no full EIA, no DC-specific water disclosure**. Confirmed to Parliament (Rajya Sabha, 6 Aug 2026). | In force | `[sourced]` |
| **CGWA groundwater NOC** (2020 guidelines) | NOC + water-conservation fee for groundwater abstraction, by aquifer stress tier. Applies to DCs drawing groundwater; **not DC-specific.** NGT-criticised 2022. | In force | `[sourced]` |
| **Energy Conservation Act 2001/2022 + CCTS** | Non-fossil-share duties + carbon-credit trading — **percentages not notified, CCTS not operational**; DCs not named designated consumers. | In force; key parts un-notified | `[sourced]` |
| **BIS IS/ISO/IEC 30134 series** | Adopts **PUE, WUE, CUE (carbon), CER, ERF** as Indian Standards — the closest India-specific DC metrics — but **VOLUNTARY (no Quality Control Order).** | Adopted, voluntary | `[sourced]` |
| **ECBC 2017; District Cooling Guidelines 2023; IndiaAI Mission** | Building efficiency (no PUE, state-adopted); treated-water cooling (voluntary); subsidised GPU compute (no env condition). | Mixed | `[sourced]` |

**No mandatory environmental disclosure specific to Indian datacenters exists.** The BIS metrics are voluntary; the draft 2025 policy's PUE-linkage is unnotified; EC filings (where triggered) aren't DC-specific or public. `[sourced]`

### 4.2 States (incentive-first; environmental conditions almost always absent or aspirational)
The pattern is uniform: generous incentives (electricity-duty exemption, stamp duty, capital/land subsidy, power tariff), environmental conditionality rare. The only **genuinely mandatory** environmental conditions found in any Indian DC policy:
- **Rajasthan DC Policy 2025 (25 Aug 2025):** requires **wastewater recycling, Zero Liquid Discharge (ZLD), rainwater harvesting** + groundwater recharge + green-building. The single strongest environmental conditionality in India. `[flag: primary PDF egress-blocked; from CEEW + industry reporting — one secondary source framed the green package as incentive-based, so confirm the binding language from source]`
- **Gujarat DC Policy 2026-29 (16 Jul 2026):** **"at least 51% from green and renewable energies"** — mandatory, but renewable-only (no water/PUE/carbon disclosure); post-dates CEEW's count.

Elsewhere: Maharashtra (2023), Telangana (2016), UP (2026), West Bengal (2021), Odisha (2022), Karnataka (2022-27), Haryana (2022), MP (2023), Andhra Pradesh (4.0, 2024-29), Tamil Nadu (2021, validity ended 31 Mar 2026 `[flag: no confirmed successor]`) — all incentive-led; green provisions, where present (TN, Odisha, Karnataka, AP), are **reward-based or aspirational**, not eligibility conditions. `[sourced]`

**CEEW "5 of 15 states embed sustainability" — verified**, and the five are **Rajasthan, Odisha, Karnataka, Tamil Nadu, Andhra Pradesh** `[sourced]`. Important refinement for the paper: on independent reading of the texts, only **Rajasthan** (and, post-count, **Gujarat**) impose *binding* environmental conditions; the other four embed *incentive/aspirational* language. So the honest statement is stronger than CEEW's headline: **~1–2 of ~15 state policies contain an enforceable environmental condition, and none is a carbon or scarcity-water or disclosure mandate.**

**4-axis for India:** all **No**, and no mandatory DC-specific environmental disclosure at all. Closest: BIS CUE (voluntary), CGWA aquifer tiers (permit gate, not weighted accounting), EIA water-balance (discretionary, non-public).

---

## 5. What this gives the paper (S10)

1. **The gap thesis is now evidenced end-to-end, not asserted.** Overlay the facility-month burden on the rules and the mismatch is stark: rules regulate *rate impact*, *volumetric water*, and *PUE efficiency*; the burden is driven by *marginal carbon* and *scarcity-weighted water*, attributed to *inference*, sub-nationally — none of which any rule sees.
2. **A sharper, defensible framing than "there are no rules."** There ARE rules — a lot of them — they are just aimed elsewhere (ratepayer protection; efficiency inputs; entity disclosure). The contribution is the **metric the rules would need and don't have.** That is more precise and more reviewer-proof.
3. **The US supplies a movement story:** the 2025–26 federal turn is **deregulatory** (EO 14318 narrows NEPA; EO 14141's carbon-matching revoked; the only federal reporting bill unenacted and PUE/WUE-only) — so the gap is widening where AI load is growing fastest.
4. **The India anchor is now airtight:** booming (≈271 DCs, 1.5→4.5–6.5 GW), water-stressed (CEEW: >50% of DCs in water-stressed regions), and with **≈1–2 of 15 state policies carrying any binding environmental condition and zero mandatory environmental disclosure** — the cleanest illustration in the world of burden landing where rules don't reach.
5. **The EU is the "most-regulated yet still-blind" case:** even the jurisdiction with mandatory PUE/WUE reporting, a rating scheme, and CSRD does **not** capture the four axes — and CSRD just *shrank* (Omnibus). If the leader misses it, the gap is structural, not a laggard problem.

---

## 6. Verification, confidence, and open items (Truth Protocol)

**Independently re-verified by me this pass:** EO 14318 (Fed. Reg. 90 FR 35385) and EO 14141 revocation; Omnibus I Directive (EU) 2026/470 in force (Council 24 Feb 2026). **Verified earlier:** EU 2024/1364 + draft rating scheme; US H.R. 9825/S. 4213; CEEW India figures; UP policy. **The core four-axis gap is triple-confirmed** (three independent sweeps + prior checks) and is the highest-confidence claim here.

**Carry-forward CANNOT-CONFIRM / watch items** (do not over-state these in the manuscript without a primary read):
- US: exact PUCO/PSCW/PUCN/IURC docket numbers for the Ohio/Wisconsin/Nevada/Indiana tariffs; the precise text of Pennsylvania's 2026 budget "energy-reporting" line; Virginia SB 553's final signature; whether FERC RM26-4 has advanced past ANOPR.
- EU: verbatim EED Art. 12 / Annex VII wording; the **final** Omnibus turnover threshold (€450 m per Deloitte/Accountancy Europe vs the €50 m in the original proposal) and exact entry-into-force day; the Ireland CRU reference/date discrepancy; whether CADA (COM(2026) 502) contains any carbon/scarcity criterion.
- India: **Rajasthan's ZLD as a hard eligibility condition vs incentive** (primary PDF was blocked — verify before calling it mandatory); the full text of the Draft National DC Policy 2025; AP Policy 4.0 mandatory-vs-promoted status; whether "SHANTI Act" is enacted; the exact identity of all 15 CEEW state policies; Tamil Nadu's post-Mar-2026 status.

**Structural limits:** policy moves monthly (the US bill could pass or die; German EnEfG relaxation is pending; India's national policy is unnotified; Indian state policies are being issued through 2026), and this sweep is English-language and reachable-source-bound. The defensible claim is **"the four axes are unmet across every reachable instrument as of Sept 2026, maintained by a re-check near submission,"** not "permanently."

---

## 7. Refinements to earlier project docs
- The `FOUNDATION_GAP_AND_POLICY.md` line "US = federal bill + accelerating state patchwork" is now enriched: the federal posture is **deregulatory** (EO 14318; EO 14141 revoked), and the state patchwork is **mostly rate-allocation, not environmental**.
- CEEW's "5 of 15 embed sustainability" should be paired with the sharper truth: **only ~1–2 states impose a *binding* environmental condition** (Rajasthan ZLD, Gujarat 51% RE), and **none** is a disclosure/carbon/scarcity mandate.
- The EU disclosure story now must note **CSRD was narrowed by Omnibus I (2026/470)** — the entity-level GHG/water disclosure that *partially* touched our axes just contracted.

---

## 8. Sources (representative; full URLs in the project record)
US: [EO 14318 (White House)](https://www.whitehouse.gov/presidential-actions/2025/07/accelerating-federal-permitting-of-data-center-infrastructure/) · [EO 14318 (Fed. Reg. 90 FR 35385)](https://www.govinfo.gov/content/pkg/FR-2025-07-28/pdf/2025-14212.pdf) · [H.R. 9825 (Congress.gov)](https://www.congress.gov/bill/119th-congress/house-bill/9825) · [Minnesota HF 16](https://www.house.mn.gov/) · Virginia HB 496 / California AB 1577 (LegiScan / leginfo) · FERC dockets (ferc.gov). EU: [EED 2023/1791](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32023L1791) · [Del. Reg. 2024/1364](https://eur-lex.europa.eu/eli/reg_del/2024/1364/oj/eng) · [Omnibus I (Council)](https://www.consilium.europa.eu/en/press/press-releases/2026/02/24/council-signs-off-simplification-of-sustainability-reporting-and-due-diligence-requirements-to-boost-eu-competitiveness/) · [AI Act Annex XI](https://artificialintelligenceact.eu/annex/11/) · [Germany EnEfG (White & Case)](https://www.whitecase.com/insight-alert/data-center-requirements-under-new-german-energy-efficiency-act) · [Ireland CRU](https://www.cru.ie/about-us/news/the-cru-publishes-its-decision-on-new-electricity-connection-policy-for-data-centres/). India: [CEEW DC power & water](https://www.ceew.in/publications/how-is-data-centre-infrastructure-in-india-shaping-power-and-water-use) · MeitY / Rajya Sabha reply (theprint.in) · Harmonised Master List (taxguru.in) · BIS 30134 series (insightsonindia.com; se.com) · state policy PDFs (nsws.gov.in, invest.telangana.gov.in, rising.rajasthan.gov.in, visionias.in).

*Author-reported figures are the source's own. This document maps the reachable, English-language regulatory perimeter as of 16 Sept 2026 and should be re-swept near submission.*

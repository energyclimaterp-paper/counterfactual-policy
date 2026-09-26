# RESEARCH GAPS — open, unbiased re-examination (opened 2026-09-22)

> **Why this file exists.** The research direction is being **re-opened from zero.** The prior favourite — "sub-national, inference-attributed, joint carbon + scarcity-water account of AI datacenters across India/US/EU + a regulatory-gap map" — is now **one candidate among many, not the working assumption.** Nothing is privileged; the point is to *find the best gap*, then commit.
>
> **On hold until a gap is chosen:** the S0–S11 **architecture** and the **data plan** in `ARCHITECTURE.md` / `DATA.md` are **provisional, NOT confirmed.** They were designed around the prior favourite; if the chosen gap differs, they change. Do not treat them as locked.
>
> **PI steer (decisive):** the **policy / regulation** angle is central — but a purely descriptive accounting-and-policy paper feels thin. We want a genuine **"working" contribution**: a technical / analytical / computational artifact that *does* something, not just *describes* something. Gaps that pair a policy frame with a working artifact rank higher.
>
> **Method:** (1) read the CFP as the filter → (2) list ALL plausible gaps that fit it → (3) score each against explicit criteria → (4) shortlist & choose → (5) *then* re-confirm architecture + data for the winner. This file is the living record. **Status (2026-09-26): direction CHOSEN — combination G6+G1+G5+G3 (see §6 + §A); problem/purpose anchored (§P); buildable artifact = a layered reproducible pipeline, NOT a multi-agent system (§B). Remaining before build: Phase-0 verification (see §B).**

---

## §P. Problem & purpose — THE FIXED ANCHOR (read first; every build decision checks back to this)

**The problem (whose, and what):** an Indian policymaker faces a datacenter boom landing in water-stressed cities (Mumbai/Chennai/Hyderabad/Bengaluru — all on groundwater watch-lists) and is **flying blind** on two questions any regulation must rest on:
1. *"How big is the AI-datacenter carbon + water footprint right now, and where (sub-nationally)?"* — no mandatory measurement exists; <1/3 of operators measure water; no sub-national facility-level joint account exists for India.
2. *"If I mandate intervention X (disclosure / coastal seawater siting / ZLD / efficiency standards), what would it actually save — is it worth the regulatory effort?"* — CEEW et al. *propose* levers; nobody *quantifies* them.

**Why unanswerable today** (from the 89-paper review): the field optimizes the *operator's* cost (scheduling/routing — kill-list), or accounts for the *US* (not India/scarcity/joint/open), or proposes policy *without numbers*. The cell answering the policymaker's two questions is empty.

**Purpose:** produce the evidence a regulator needs to **choose which water/carbon intervention to mandate** — grounded in a real measurement, not assumptions. (This is the CFP's "decision-relevant".)

**What we PRODUCE (4 products, in hierarchy — the pipeline is only #4, the *means*):**
1. **Finding (headline):** a ranked, quantified answer — *"for India, lever A saves most water, B most carbon, C is symbolic."*
2. **Dataset (durable asset):** the open, sub-national, facility-level joint carbon + scarcity-water account (India deep; US/EU comparative).
3. **Method (transferable):** the counterfactual approach that turns an account into "what would this policy save."
4. **Instrument (reproducibility vehicle):** the open code that generates 1–3 auditably.

**NOT building:** a scheduler/optimizer (kill-list); a multi-agent system; a generic DC-sustainability platform; a real-time tool; another US account.

**One sentence:** *the first open, reproducible account of AI-datacenter carbon and scarcity-weighted water in India (vs US/EU), used to quantify which policy levers would actually help — so a regulator can decide what to mandate instead of guessing.*

---

## 0. Provenance — are these gaps OURS, or borrowed? (integrity check)

**The occupancy map is 100% ours.** Every "is this cell filled?" judgment comes from the **89-work primary-read** review in `LIT_REVIEW_VERIFIED.md` + `POLICY_DEEP_DIVE.md` (regulations read directly) + the dedicated India search — **not** from any paper's abstract or its self-declared "future work."

**Gap-by-gap origin:**
- **Verified-empty cell (ours — strongest):** **G1, G3, G5, G6, G9, G11** — we looked and found nothing there (for G9, we saw the whole contradictory optimizer cluster that no single paper sees).
- **Synthesis of the corpus (ours):** G8, G10, G12 — emerge from combining what several papers separately show.
- **⚠️ Borrowed / paper-claimed (verify independently — do NOT trust blindly):** **G4** (FAS/EU *say* "we need standardized metrics"); **G2**'s "inference attribution is needed" framing (many papers assert it). Logged but discounted until confirmed ourselves.

**Subtlety for the recommended G6:** the *policy levers* it tests (mandatory disclosure, coastal seawater siting, ZLD, efficiency standards) come from **existing advocacy (CEEW, FAS)** → the levers must be **independently verified as real + sensible**, not accepted on CEEW's word. But the **gap** (nobody has *quantified* their effect) and the **contribution** (the counterfactual model) are **ours**.

---

## 1. The CFP lens — every gap must pass this filter

*(from `CFP_RECORD.md`; the SI is Elsevier *Energy and Climate Change*, deadline 31 Dec 2026, rolling review.)*

**SI title:** "Computing and Digitalization through a Multi-Disciplinary Lens: Future Implications for Energy, Resources, and Environment."

**Three content tracks** *(⚠️ repo-transcribed wording — re-verify verbatim vs the live SI page before quoting):*
- **T1 Techno-process:** hardware-software-algorithmic innovations & their scaled impacts on efficiencies, costs, critical materials.
- **T2 Socio-institutional:** behaviour & decision-making of individuals, businesses, governments.
- **T3 Macro-systems:** societal-scale & economy-wide interactions with future computing.

**Four guest editors = four "fit vectors"** (a strong paper resonates with ≥2):
- **David McCollum** — integrated assessment / IAM, scenarios, AR7 → *scenario/projection work.*
- **Elena Verdolini** — energy-environment economics & policy → *policy design/evaluation.*
- **Te Han** — ML-for-energy / forecasting → **the "working contribution" vector; the reason a computational artifact will land.**
- **Andrés Clarens** — datacenter water & carbon → *the topic anchor.*

**Hard CFP signals:**
- "**accessible, decision-relevant** research… informing solutions and strategies" → must inform a decision, not just report numbers.
- "spanning diverse fields… **combining methodologies are particularly encouraged**" → multi-disciplinary + method-combining is rewarded.
- "both full-length research articles and shorter **perspective/commentary** pieces" → two possible formats (a working paper vs a perspective).
- "compatibility with the **IPCC AR7** literature cut-off… form a knowledge base for AR7 chapters" → forward-looking, policy-relevant framing scores.

**Filter test for any gap:** Which track? Which ≥2 editor vectors? What decision does it inform? Is it method-combining? AR7-relevant?

---

## 2. The GAT / GNN verdict (what we carry vs drop) — see `GNN_AUTOPSY.md`

- **SCRAP (the thesis):** the co-location-graph GNN. It inverted all three ingredients that make ST-GNNs work — modelled a **region-level** target (not node-level), on a **fixed co-location graph** (~98% within-region edges → 91.3% no-op) with a **post-hoc fixed-α blend** (not end-to-end). A rigorously-audited **null**. No new ML architecture (kill-list).
- **SALVAGE (the assets — and the seed of a "working" contribution):**
  1. **Data pipeline** — Ember monthly (US/EU/India), GEM Global-Integrated-Power, Aqueduct 4.0, G3P/GRACE — already downloaded.
  2. **Geocoder** — facility → grid-zone → basin point-in-polygon (`nbs/gat-colocation-weights-water-energy.ipynb`).
  3. **Forecasting benchmark — bigger than first thought (corrected 2026-09-23, from notebook autopsy):** there is a **real, sub-national, multi-model, multi-resource** benchmark on actual Ember/G3P data (`MASTER_RESULTS.csv`, `model_comparison_region.csv`): **SARIMA · xLSTM · TimesFM-2.5 · "Nexus" (Gemini-LLM)** forecasting electricity + carbon for **11 Indian states, ~30 EU countries, all US states**, plus water (G3P TWS) per basin. Key honest findings: (a) **no single model wins** — best model varies by region×target (Nexus best on several EU/US series, TimesFM best on India electricity, SARIMA best on US electricity); (b) **water is hard** — SARIMA fails on TWS, only xLSTM produced a number (~86 RMSE); (c) the earlier "synthetic, indicative" caveat was a *separate* model-selection sanity check (`MODEL_CHOICE.md`), NOT this real benchmark. → This is a genuine **working asset**, not a toy. It materially strengthens G3 and the "forecasting as a stated secondary contribution" option.
  4. **Audit/rigor harness** — seasonal-naive skill floors, co-location-vs-random controls, Mantel confound tests → a reusable red-team + a citable model of honest null-reporting.
- **Implication:** the salvage tilts us toward gaps with a **forecasting / empirical-modeling** spine (Te Han vector). The failed project is not absorbed *as an architecture* — but its data + rigor + forecasting benchmark can power a *correctly-posed* working contribution.

---

## 3. The reframe: "policy-central + working contribution"

**Define "working contribution" here** = the paper *produces or tests something that behaves*, beyond describing/measuring: a forecast model, a counterfactual/scenario simulation, an optimization or decision rule that is *evaluated*, a policy instrument that is *quantitatively assessed*, or an empirical test that *resolves a contested question*.

**The tension to resolve:**
- The prior favourite (accounting + regulatory-gap map) is **strong on policy, thin on "working"** — its working core is "we built an open reproducible pipeline," which a tough reviewer may read as data engineering, not research.
- **Fix:** treat the account as the **input** to a working contribution. The candidates that do this best (see §5): **G3 forecasting**, **G6 counterfactual policy modeling**, **G9 "when does it help" reconciliation.** Each pairs the central policy frame with a genuine analytical artifact *and* absorbs the GAT salvage.

**Working hypothesis (to test, not assume):** the strongest paper is likely **[an India-anchored resource account] × [a working analytical layer — forecast OR policy-counterfactual OR cross-region reconciliation] × [a policy/regulatory frame].** But keep every §5 candidate live until scored.

---

## 4. Selection criteria (score each candidate 1–5 — next sequence)

| # | Criterion | What "5" looks like |
|---|---|---|
| C1 | **CFP fit** | hits ≥2 tracks + ≥2 editor vectors, explicitly decision-relevant, AR7-aligned, method-combining |
| C2 | **Genuine gap** (unoccupied) | lit review shows it's unbuilt or thin; not scooped |
| C3 | **Working contribution** (PI's key ask) | a real technical/analytical artifact that is *evaluated*, not just described |
| C4 | **Policy centrality** | speaks directly to regulation / disclosure / governance / a real decision |
| C5 | **Feasibility** (solo, ~Dec 2026) | data reachable now; scope shippable; fallback ladder exists |
| C6 | **GAT-salvage leverage** | reuses data pipeline / geocoder / forecasting / rigor |
| C7 | **Defensibility** | a moat (India anchor, hard data, method) resists a fast-moving field |

*(Weighting note: PI has up-weighted **C3 (working)** and **C4 (policy)**. C2 & C7 guard against the field's weekly output.)*

---

## 5. The gap landscape — ALL candidates (unbiased; the prior favourite is just G1+G5)

> Each: **the gap · evidence it's open (lit-rev) · working potential · policy centrality · GAT-salvage · scoop-risk.** Scores come next sequence.

### Track T1 — Techno-process (measurement / methods / metrics)
- **G1. Sub-national joint carbon+water account of AI DCs, India-anchored (± US/EU).** *Gap:* no sub-national facility-level joint account for India (#74 is US-only, volumetric, separate-not-joint, closed; #88 symbiosis is national-LCA; MARLIN is a scheduler). *Working:* moderate (pipeline + uncertainty). *Policy:* high (feeds the gap map). *Salvage:* high (geocoder+data). *Scoop:* US crowded, **India open.** ← *prior favourite.*
- **G2. Inference-attributed *marginal* resource-intensity method** (per-model/query → facility → grid-marginal + scarcity). *Gap:* per-query papers use scalars/averages (How-Hungry, WCI); facility×marginal×scarcity attribution is thin. *Working:* HIGH (a method). *Policy:* medium. *Salvage:* medium. *Scoop:* medium-high (hot area).
- **G3. Forecasting sub-national AI-DC resource demand (electricity + water) under buildout, done right.** *Gap:* forecasts are national/aggregate (IEA/LBNL); sub-national, resource-coupled forecasting is thin — and the GAT null shows the naive way fails, leaving room to do it correctly (facility/node-level, honest benchmark). *Working:* **HIGH** (Te Han vector). *Policy:* high (informs siting/capacity/grid planning). *Salvage:* **very high** (this IS the salvage). *Scoop:* medium.
- **G4. A standardized, open, reproducible *metric/instrument* for AI environmental footprint.** *Gap:* FAS (CUE/PPW) + EU Reg call for standardized metrics; none is open+reproducible+facility-level. *Working:* moderate (metric + reference implementation). *Policy:* high. *Salvage:* medium. *Scoop:* medium.

### Track T2 — Socio-institutional (policy / governance / behaviour)
- **G5. Cross-jurisdiction regulatory-gap map (India/US/EU) on the four axes** (carbon-intensity, marginal, scarcity-water, inference). *Gap:* no comparative four-axis gap map (POLICY_DEEP_DIVE confirms the gap). *Working:* LOW alone (descriptive) → needs pairing. *Policy:* **very high.** *Salvage:* none. *Scoop:* low. ← *prior favourite's policy half.*
- **G6. Counterfactual policy modeling: quantify the resource savings of specific India interventions** (mandatory facility disclosure, coastal/seawater siting, ZLD, efficiency standards). *Gap:* CEEW *proposes* these; nobody *quantifies the counterfactual.* *Working:* **HIGH** (scenario/counterfactual simulation). *Policy:* **very high.** *Salvage:* high (uses the account + forecasting). *Scoop:* low-medium. **← strongest policy+working pairing.**
- **G7. Quantitative design/evaluation of a disclosure or rating instrument** (e.g., test CEEW's "AI Energy Star"; find an optimal disclosure threshold; information-value of facility-level reporting). *Working:* moderate-high. *Policy:* high. *Salvage:* medium. *Scoop:* low.
- **G8. Disclosure-gap forensics: derive the *hidden* footprint operators don't report.** *Gap:* Mytton/water-governance show <⅓ measure water; nobody systematically back-derives the undisclosed sub-national footprint. *Working:* moderate (derivation/estimation method). *Policy:* high. *Salvage:* medium. *Scoop:* medium.

### Track T3 — Macro-systems (systemic / economy-wide)
- **G9. "When does carbon/water-aware siting/scheduling help vs backfire?" across India/US/EU.** *Gap:* the field is full of contradictory optimizers (CICP, Carbon Explorer, geo-shift, CASPER, MARLIN — all kill-list); nobody reconciles the conditions under which they help, and our GNN null is itself evidence. *Working:* **HIGH** (empirical cross-region analysis; turns contradictions + our null into contribution). *Policy:* high (should we mandate these?). *Salvage:* high (data + rigor). *Scoop:* medium. **← the "reconciliation" play; strong working spine.**
- **G10. Grid-DC co-evolution / rebound under India's grid** (siting feedback, water-electricity nexus, interconnection). *Working:* moderate-high (systems modeling). *Policy:* medium-high. *Salvage:* medium. *Scoop:* medium (US versions exist: To-Defer-or-Shift, MDC).
- **G11. Distributional / environmental-justice analysis: who bears the sub-national water/carbon burden of AI DCs** (India hubs on groundwater watch lists). *Working:* moderate (spatial statistics). *Policy:* high. *Salvage:* medium (geocoder). *Scoop:* low. *(spans T2+T3.)*
- **G12. IAM / scenario pathways of AI-DC resource footprint to 2030/35 for India, AR7-aligned.** *Gap:* national projections exist; sub-national resource-coupled scenarios thin. *Working:* moderate-high (scenario modeling; **McCollum vector**). *Policy:* high. *Salvage:* high (forecasting). *Scoop:* medium.

**Cross-cutting observation (unbiased):** the prior favourite = **G1 + G5**. It is defensible (India moat, low scoop) but its *working* score is its weak point — exactly the PI's concern. **G3, G6, G9, G12** are the candidates that inject a real working contribution *and* reuse the GAT salvage *and* keep policy central. The likely winner is a **fusion** (e.g., G1 as the data spine feeding G6 or G3 or G9), but that must be *earned by scoring*, not assumed.

---

## 6. Scoring & shortlist (2026-09-22)

Each gap scored 1–5 per criterion; **C3 (working) and C4 (policy) weighted ×2** per PI steer. Max = 45. *(Scores are a forcing-function to expose trade-offs, not gospel — the PI's reaction can override any of them.)*

| Gap | C1 fit | C2 gap | C3 work ×2 | C4 pol ×2 | C5 feas | C6 salv | C7 def | **Wtd /45** |
|---|:--:|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| **G6 counterfactual policy modeling** | 5 | 5 | 5 | 5 | 3 | 4 | 4 | **41** |
| **G9 "when does it help / backfire"** | 5 | 5 | 5 | 4 | 3 | 5 | 4 | **40** |
| **G3 sub-national resource forecasting** | 5 | 4 | 5 | 4 | 3 | 5 | 3 | **38** |
| G11 environmental-justice / distributional | 4 | 4 | 4 | 4 | 4 | 4 | 4 | 36 |
| G7 disclosure/rating instrument eval | 4 | 4 | 4 | 5 | 3 | 3 | 3 | 35 |
| G12 India IAM / scenario pathways | 5 | 4 | 4 | 4 | 3 | 4 | 3 | 35 |
| **G1 India joint C+W account** *(prior favourite)* | 4 | 5 | 2 | 4 | 4 | 4 | 4 | **33** |
| G10 grid-DC co-evolution / rebound | 4 | 3 | 4 | 4 | 3 | 3 | 3 | 32 |
| G4 open standardized metric | 4 | 4 | 3 | 4 | 3 | 3 | 3 | 31 |
| G8 disclosure-gap forensics | 4 | 4 | 3 | 4 | 3 | 3 | 3 | 31 |
| G5 regulatory-gap map *(policy half of prior)* | 4 | 4 | 1 | 5 | 5 | 1 | 3 | 29 |
| G2 inference-marginal attribution method | 4 | 3 | 4 | 3 | 2 | 3 | 2 | 28 |

**What the scorecard says (unbiased):**
- **The prior favourite (G1) ranks 7th (33).** Its gap (5) and moat (4) are real, but its **working score is 2** — precisely the PI's concern, now quantified. G5 (its policy half) ranks 11th: pure description.
- **All three leaders REQUIRE a G1-style India account as their data input.** So G1 does not die — it becomes the **spine**, not the headline.
- **G6 wins** because it maxes the two up-weighted axes at once: most policy-central *and* a genuine working artifact. "Quantify what India's proposed interventions would actually save" is a decision-grade result nobody has produced.
- **G9** is the most intellectually distinctive (weaponizes our GNN null) but needs multi-region data → more US-side scoop exposure.
- **G3** is the purest working/ML play (max salvage, direct Te Han fit) but risks drifting from policy centrality and hits the India sub-national data-granularity wall.

**Recommended shape (v2 — multi-region, for Q1 span) — to react to, NOT locked:**
> **"What would it save?" — a THREE-REGION (India deep / US solid / EU light) counterfactual policy analysis of AI-datacenter water + carbon interventions, built on a sub-national facility-level account, exploiting the three regions as a *regulatory gradient*.**

**Why keep US/EU (the Q1-span answer):** a Q1 paper needs breadth + generalizability; India-only risks reading as a regional case study. The three regions form a natural **policy gradient** that supplies both span *and* credibility:
- **EU** = regulation exists (Reg 2024/1364 mandates PUE/WUE) but facility data is confidential → *"mandated-but-hidden."*
- **US** = deregulating (EO 14318) yet well-researched (Harvard/Guidi facility lists) → *"unregulated-but-visible."*
- **India** = no mandate + building fast in water stress → *"unregulated-and-invisible."*
This gradient (a) **grounds India's counterfactuals in regions that already have the policies** (evidence, not guesswork), (b) turns "US is crowded" into an **asset** — we benchmark against Harvard/#74, not compete, (c) delivers Q1 breadth. **India carries depth + novelty; US/EU carry the comparative evidence base.**

**⚠️ SUPERSEDED BY the TIERED contribution set (2026-09-26) — authoritative in `dcfootprint/ARCHITECTURE.md §7`** (9 contributions, Tier-1 robust spine + Tier-2 conditional reach; reconciled in `00_PROJECT_STATE.md §2`). The five below are retained as the original framing (all fold into the nine).

**THE FIVE CONTRIBUTIONS (original framing — see §7 for the reconciled nine):**
1. **Data** — first open, reproducible, **sub-national, facility-level** account of AI-DC carbon **and scarcity-weighted water** for **India** (novel); US/EU built as comparative benchmark (replication, not a novelty claim on the crowded US side).
2. **Method (the working core)** — a **transferable counterfactual engine** that quantifies, *per policy lever*, the carbon + water savings of a specific intervention.
3. **Comparative finding** — the three-region **regulatory gradient** exposing the four-axis gap (carbon-intensity / marginal / scarcity-water / inference) across jurisdictions.
4. **Policy result (decision-grade)** — a **ranked "which lever pays"** answer for India: CEEW's proposed levers *quantified for the first time*.
5. **Instrument** — open data + code = a standardized, auditable method others can extend (also answers the FAS/EU call for standardized metrics).

**Q1 span vs solo feasibility — the honest ladder:**
- **Floor (submittable):** India account + regulatory gradient + counterfactual on **1–2 highest-impact levers** (coastal siting, mandatory disclosure). Nearest neighbour = Siddik + India + a policy engine.
- **Ceiling (stretch):** all levers + forecast to 2030 (G3) + full US/EU accounts + US/UK marginal carbon.
- Every rung submittable; ambition-first design, **India Floor built first.**

**Editors hit:** all four (Verdolini policy · Clarens DC water/carbon · McCollum scenarios/AR7 · Te Han forecast). **Salvage:** account (data + geocoder) + forecasting (Chronos-2) + rigor harness. **Fallback:** modeling too heavy → retreat to account + gradient map; India data blocks → pivot to G9 (cross-region reconciliation on data-in-hand).

### 6a. Where do the forecasting models (SARIMA / Chronos-2 / xLSTM) fit?

**Verdict: forecasting is a CEILING / supporting layer, NOT the core.** Map it against the three pieces of the recommended shape:
- **The account (baseline)** = measured from observed data (capacity × utilization × grid-intensity × WUE) → **no forecasting needed** (at most minor gap-filling/imputation of missing months).
- **The counterfactual engine (working core)** = scenario arithmetic on the account ("lever X → parameters shift → savings") → **no time-series forecasting needed.**
- **The forward projection to 2030 (Ceiling, G3/G12)** = the ONE place forecasting earns its keep: turn "lever saves Z/yr today" into "cumulative saved by 2030," business-as-usual vs each lever. This is the AR7 / McCollum hook.

**Keep vs drop:**
- **Keep:** **Chronos-2** (off-the-shelf TSFM) + **SARIMA** (transparent classical baseline) — two models, honestly compared. Using *existing* forecasters ≠ new ML architecture → consistent with the kill-list.
- **Drop:** **xLSTM** (lost the benchmark, adds complexity) and the **GNN** (scrapped).
- **Forecast only at the granularity the data supports** — national/regional (Ember national-monthly is forecastable); **NOT** facility-level monthly for India (regional-annual carbon = data-starved; the same wall the account hits).

**Honest caveats:**
- The salvaged benchmark (Chronos-2 > SARIMA > xLSTM) was measured on **synthetic** series — MODEL_CHOICE.md itself calls it "indicative, not a result." **Re-run on real Ember/G3P data before any claim.**
- Forecasting is a **means** (project the policy savings forward), not the headline. If we want it to BE the headline → that is the **G3 pivot** (forecasting-primary), a different paper with a different risk profile.

**Net:** the salvaged forecasting is genuinely reused — as a **supporting projection layer**, not the star. The star is the counterfactual engine.

**On reporting "we tested all these models" (PI request) — yes, but with three conditions:**
1. **Real data only.** The synthetic ranking cannot appear as a result; re-run on real Ember/G3P first. Reporting a synthetic-data winner in a Q1 paper is a reviewer landmine.
2. **Frame by purpose, not effort.** Present the comparison as *justification for the projection model choice* (why Chronos-2 was selected), not "here's everything we tried." Reviewers reward relevance, not labour. One clean results table.
3. **The GNN null is the most valuable thing to report** — as an honest negative result: "a co-location graph does not improve sub-national resource forecasting, and here is *why*" (the 91.3% no-op, positively-correlated bridged residuals). This *demonstrates rigor*, is genuinely publishable as a methodological caution, and resonates with editor Te Han. Appendix + one paragraph in main text.

**Two levels — PI picks:**
- (a) **Supporting** — one table + appendix; G6 policy spine untouched.
- (b) **Elevated to a stated secondary contribution** — a short methods subsection + the null; credits the work, hits the Te Han vector, shows rigor. Must stay proportional or it drifts into the **G3 pivot** (forecasting-primary).
- **Recommendation: (b)-lite** — a *stated secondary contribution* = one methods subsection (real-data model comparison) + the GNN null in an appendix. Credits the work honestly without unbalancing the policy narrative.

## 7. Next sequence (seamless resume — no gap in the flow)
1. **PI reacts** to the shortlist: G6-primary vs G9 vs G3, and India-as-spine vs India-as-headline. *(This is the one open decision.)*
2. **Re-verify CFP track wording** verbatim vs the live SI page (T1/T2/T3 are repo-transcribed).
3. **Lock the gap + format** (full research article vs perspective).
4. **THEN** re-open and confirm `ARCHITECTURE.md` + `DATA.md` for the chosen shape (on hold until this point).
5. If G6: enumerate the specific counterfactual interventions + the minimal data needed to quantify each.

**Mindset:** favour the gap that is genuinely open (survives the 89-paper review + a pre-submission refresh), carries a **working** contribution the PI can point to, keeps **policy** central, leans on the **India moat** + **GAT salvage**, and resonates with ≥2 editors. The prior favourite did not win by inertia — it placed 7th on its own scorecard.

---

## §A. The chosen combination (CHOSEN 2026-09-26)

**Target = a combination of four gaps in defined roles (a causal chain, not gap-stacking):**
- **G6 counterfactual policy** = HEADLINE (the working contribution: "what would each India lever save?")
- **G1 sub-national account** = SPINE (the data foundation G6 runs on; India deep, US/EU comparative)
- **G5 regulatory gradient** = FRAME (EU mandated-but-hidden / US unregulated-but-visible / India unregulated-and-invisible; gives Q1 span + grounds the counterfactuals)
- **G3 forecasting benchmark** = SECONDARY working contribution (salvaged; projects savings to 2030; Te Han vector)

**Reserve:** G9 (reconciliation) — partly absorbed into G6's comparative framing; the fallback if India data blocks. **Optional enrichment:** G11 (environmental-justice / sub-national burden). **Dropped:** G2, G4, G7, G8, G10, G12 (see §5).

**The chain:** measure (G1) → expose the gap (G5) → quantify the fix (G6) → project it (G3). Remove any one and the story breaks — that is the test this passes.

---

## §B. The buildable artifact — layered architecture & execution plan

> **It is a layered, reproducible PIPELINE (deterministic + statistical), NOT a multi-agent system.** Agents are rejected because the artifact's value is *auditability/reproducibility*, which autonomous agents would undermine. The **only** place an LLM legitimately enters is one optional node — capacity extraction (L0) — tied to the real data bottleneck, plus the salvaged "Nexus" LLM as one benchmarked forecasting arm (L4). Both are single justified nodes, not a swarm.

**Discipline rule:** every layer must name the product (§P) it serves. If it can't, it is not built.

| # | Layer | What it does | Serves (product) | Depends on | Floor / Ceiling |
|---|---|---|---|---|---|
| **L0** | Data foundation | acquire + clean all inputs (facilities+capacity, Ember, Aqueduct/AWARE, EWIF, HydroBASINS, CGWB, policy corpus) | dataset | — | Floor (India) / Ceiling (US·EU) |
| **L1** | Spatial linkage | geocode facilities → grid-zone + water-basin *(salvaged geocoder)* | dataset | L0-facilities | Floor |
| **L2** | **Account** | baseline carbon + scarcity-water per facility-month (energy→carbon via grid CO₂; water = physical WUE + grid-embedded EWIF × AWARE) | **dataset** | L0, L1 | Floor (India) / Ceiling (US·EU) |
| **L3** | **Counterfactual** | apply policy levers (parameter deltas) → Δcarbon/Δwater → "which lever pays" ranking | **finding + method** | L2 + lever specs (L5) | Floor (1–2 levers) / Ceiling (all) |
| **L4** | Projection | forecast demand/footprint to 2030 → cumulative savings *(salvaged SARIMA/TimesFM/Nexus benchmark)* | secondary finding | L2 | Ceiling |
| **L5** | Regulatory-gap frame | India/US/EU four-axis comparison + **lever specifications** | frame | POLICY_DEEP_DIVE | Floor |
| **L6** | Uncertainty + validation | Monte-Carlo/sensitivity over soft params (utilisation, PUE, WUE, EWIF) + rigor harness *(salvaged)* | credibility of all | L2–L4 | Floor (basic) / Ceiling (full) |
| **L7** | Release | open data + code packaging | instrument | all | Floor |

**Execution — one sequential spine + three parallel tracks (hybrid):**
- **SPINE (critical path, strictly sequential):** `L0-facilities → L1 → L2 → L3 → finding`.
- **Parallel track A (data):** L0 non-facility inputs — must land *before L2*.
- **Parallel track B (policy):** L5 frame + L3 lever specs — must land *before L3*.
- **Parallel track C (forecasting):** L4 benchmark re-validation — independent; integration waits on L2.
- **Cross-cutting:** L6 after each compute layer; L7 last.

**THE BOTTLENECK = L0 facility capacity.** Atlas has locations, no capacity; 40/194 India rows uncosted. The spine cannot finish L2 without it → capacity completion is the #1 build task and the main thing **Phase-0 verification** must de-risk.

**Phase-0 verification (the gate, before spine build):** (1) capacity-data feasibility; (2) Ember India carbon reported-vs-derived; (3) CFP track wording (verbatim); (4) policy-lever validity (independently confirm CEEW's levers); **(5) NEW — lever-parameter data** (seawater-cooling WUE, ZLD recycling, PUE-standard distributions, disclosure coverage): the counterfactual (L3) needs numbers a pure account never did — a lever that can't be quantified drops. Any of these can reshuffle the plan → run first. **Data-adequacy audit: `DATA.md` PART C — accounting stack is data-complete & matches the literature; the only gaps are facility capacity (bottleneck), a real US inventory, and these lever parameters.**

**Phase mapping:** Floor = L0(India)+L1+L2(India)+L3(1–2 levers)+L5+L6(basic)+L7 → a complete submittable paper. Ceiling = extend L0–L2 to US/EU, L3 all levers, L4 projection, L6 full, +optional G11.

> **NOTE on `ARCHITECTURE.md`:** the old S0–S11 blueprint there is superseded by this L0–L7 layering (S0–S11 was built for the pre-pivot direction). `ARCHITECTURE.md` will be rewritten from §B once Phase-0 clears; until then, §B is authoritative and the old S0–S11 is reference only.

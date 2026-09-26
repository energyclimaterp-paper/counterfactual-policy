# GNN AUTOPSY — why it returned a null, what the error was, and whether it can go in the journal

**Compiled:** 2026-09-16. **Method:** read against the **primary** `gat-based-forecasting/paper_submission/docs/AUDIT_REPORT.md` (rev 2, 2026-08-27) — not only the `04`/`05` breakdowns — plus an independent read of the graph-neural-network time-series forecasting literature. Stance: the repo is a witness cross-examined, not a source quoted. Where I agree with its conclusion I say so; where I'd push past its framing I flag it. Confidence tags: `[verified]` = checked against the primary audit's own reproduced numbers; `[lit]` = grounded in the external GNN-TS literature; `[judgment]` = my independent inference.

---

## 1. What was actually built (so we autopsy the right thing)

The GNN was **not the forecaster**. Four encoders (Flat GAT, Flat HGT, Hierarchical, GraphGPS) were trained on a **co-location graph** of datacenter sites and used to produce **attention blend-weights** that *fuse* each site's base forecast with its neighbours' — a **fusion router** sitting on top of per-region base forecasts (SARIMA / xLSTM / TimesFM / Chronos-in-the-"Nexus"-slot). The forecasting target is **region-level**: 95 grid zones (electricity, carbon), 24 river basins (water), 12-month holdout. `[verified: AUDIT_REPORT §1, §3]`

So the GNN's only lever was *how much to mix a site's regional forecast with its graph-neighbours' regional forecasts.* Hold that; it is the whole story.

## 2. Verdict first: this is a real, well-audited null — not a bug, not low effort

Before "why," the integrity question: is the null trustworthy? Yes, and unusually so. `[verified]`
- The headline null **regenerates to a worst discrepancy of 8.3e-17**; it previously existed with no code that produced it, and that was fixed.
- Correctness invariants (blend identities, control-graph application, α=0 and α=1 edge cases) **all PASS with exact zeros**; a by-hand reconstruction of one site matches the pipeline to `0.000e+00`.
- **Leakage-guarded** by a hard assert (feature window ends 2024-11-30; holdout starts 2024-12-01).
- Distribution-free **permutation test: 12/12 cells inside the bulk.**
- The team **found and retracted its own over-claims** during audit (a mis-specified sensitivity floor; a shuffle test that went 10/12 "significant" → 12/12 null once redesigned; a water result that dissolved after a bug fix).

My read: I agree with the repo that the null is real. It is not a case of "they gave up" or "under-powered." `[judgment]`

## 3. Why it failed — the mechanism, in three nested layers

**Layer 1 — the graph is redundant with the target.** The co-location graph is **~98% within-region** (98.1% intra-zone, 97.7% intra-basin). But all sites in a zone share an **identical** zone-level base forecast. So blending a site with a same-zone neighbour mixes a forecast with a copy of itself — an **exact no-op for 4,461 of 4,889 sites (91.3%)**. `[verified: 04 §6, AUDIT_REPORT §3]` The graph can only *do* anything through its **1.9% inter-zone edges** — and those import a *different* region's level, which on electricity makes it **worse** (the hand-check: Slovenia site 2980, one live Italian neighbour lifts the neighbourhood mean 3.5×, own-forecast MAE 308.09 → blended 618.85). `[verified: AUDIT_REPORT §6.3]`

**Layer 2 — even where it acts, averaging can't help, for a measured reason.** Blending neighbours helps only if their forecast errors partly **cancel**. The residuals of the bridged region-pairs are **positively correlated** (carbon +0.347 vs +0.092 baseline; water +0.526 vs +0.248; electricity +0.138 vs +0.019). Positively-correlated errors don't cancel. A planted-effect control using *real* residuals shows **no co-location strength up to ρ = 0.99 produces any detectable improvement on electricity.** `[verified: AUDIT_REPORT §5]` This is mechanistic, not a power bound — "the method cannot work on this data, for a measurable reason."

**Layer 3 — there was almost no headroom for anyone.** The entire model family sits within about ±8% skill of a seasonal-naive baseline (best skill anywhere **+0.084**). `[verified: AUDIT_REPORT §1.4]` Learned attention beats uniform blending by **< 1.7%** on every resource, and `gat_weighted` vs `equal_weight_neighbour` is **ns** — the *learned* part of the learned router buys essentially nothing over a uniform average. `[verified: §4]`

**A caveat the repo is honest about:** the encoders genuinely **did learn structure** — they reconstruct their real graph 3–14× better than a degree-matched random-edge control (Flat GAT 13.6×, HGT 14.1×). `[verified: 04 §2]` The GNN worked *as a GNN*; the learned structure simply had nothing to contribute to *this* forecasting task.

## 4. What "the error" was — two different things, and neither is "GNNs don't work"

1. **The design error (the real cause of the null):** a **mismatch between the graph relation and the task.** Spatial co-location was encoded as the graph, but the forecasting target was aggregated to the region — so the graph carried a dependency the target had **already absorbed**, and the fusion-router architecture could only *reweight* forecasts that were identical within a region. The architecture cannot express cross-node predictive signal even if it existed. This is a conceptual mis-pairing, not a coding mistake. `[judgment, consistent with AUDIT_REPORT §3–5]`
2. **The data bug (found and fixed, not the cause):** the **water frequency bug** — `asfreq("MS")` applied to G3P's mid-month timestamps produced a 100% NaN series; SARIMAX silently fit nothing and emitted a degenerate forecast. It **inverted the water result** (SARIMA water RMSE 103.02 → 37.49 after the fix; the pre-fix "Nexus beats SARIMA by 60.8%" evaporated). `[verified: 05 §1]` It corrupted an *earlier* water claim, was caught in audit, and is a cautionary tale about the repo's rigor — **it is not why the graph null holds.**

## 5. "Previous papers integrated GNNs — did we miss something?" — yes, precisely this

We did not miss a *better GNN architecture* (four were tried; all learned structure fine). We missed that the **graph-task pairing and the router design were the wrong instantiation.** Successful spatio-temporal GNN forecasting works under conditions our build violated on every count `[lit]`:

| Why DCRNN / STGCN / Graph WaveNet / MTGNN succeed | What our build did |
|---|---|
| The graph **nodes are the forecasting units** (each sensor is forecast) | Nodes were **sites**, but the target was aggregated to **region** — within-region variation, the only thing the graph could explain, was dissolved |
| The adjacency carries **genuine cross-node dynamics** not already in the target (congestion propagates between roads) | Co-location carried a dependency **already encoded by the region label** — redundant |
| Modern methods **learn / adapt the adjacency** (Graph WaveNet's adaptive matrix; MTGNN "Connecting the Dots"; graph-structure-learning) rather than trusting a fixed given graph | We used a **fixed co-location graph** — exactly the fragile choice the field moved away from |
| The GNN **learns the forecast end-to-end** | The GNN only produced **blend weights** over pre-computed forecasts — it never touched the temporal model |

So the honest answer to your question: **the null is specific to (co-location graph × region-level target × fusion-router).** It does **not** show that no graph helps datacenter resource modelling. `[judgment]` The repo's own strongest positive signal points the same way: an oracle that picks the best model **per site** beats graph weighting by **~6% (carbon) / 13% (electricity) / 16% (water)** — i.e., **the signal lives in site-level heterogeneity, which the region-level target threw away.** `[verified: 04 §7]` A *different* graph — electrical-grid topology (which buses feed which loads; carries marginal-emissions propagation) or hydrological upstream/downstream basin connectivity — with a **site/sub-regional target** and an **end-to-end, adaptive-adjacency** model, is untested and is where a real GNN contribution could live. That is a genuine "missed avenue" — but it is a **new project**, not a fix to this one.

## 6. Can we still put a GNN in the journal paper?

Three honest options, and my recommendation.

- **(a) As a positive "GNN improves forecasting" contribution — NO.** The null holds for the built design; rebuilding with a new graph/target is a separate, high-risk project outside the Dec-2026 scope; and it collides with the locked "no new ML architecture" decision and a venue that rewards decision-relevant accounting, not architecture novelty. Re-running the same design cannot change the mechanism.
- **(b) As a rigorously-audited NEGATIVE result / methodological caution — YES, and it's cheap.** "Graph structure over co-located datacenters does not improve regional resource forecasting, with a measured mechanism (edge redundancy + positively-correlated residuals), across four encoders and a battery of controls" is a real, citable finding. It fits the "reconciliation / decision-map" framing (candidate direction D) and *strengthens* the paper's credibility — it shows we tried the sophisticated thing and reported the null honestly, which reviewers reward. One paragraph, or a short appendix.
- **(c) The salvageable INSIGHT — already paying off.** The autopsy tells us **attribute at the facility/site level, not the region level** — which is exactly the paper's `facility-month` atomic unit. The GNN work has already earned its keep by ruling out spatial-graph smoothing and pointing at site-level heterogeneity as where signal lives.

**Recommendation:** keep the GNN out **as an architecture** (the locked decision is correct), but (i) hold the null in reserve as a one-paragraph methodological caution if any graph/forecasting angle is raised in review, and (ii) carry the site-level-heterogeneity lesson into the accounting design. The forecast *models* (SARIMA/xLSTM/TimesFM/Chronos) already survive into S11 as forward-projection tools — that is the right and only role for the ML work here. If you ever want a true GNN paper, it is future work with a different graph, not a rescue of this one.

## 7. What I verified independently, and my confidence

- Read the **primary** `AUDIT_REPORT.md` and confirmed the null's audit rigor first-hand (reproducibility 8.3e-17; invariants exact-zero; leakage assert; permutation 12/12; hand-check exact). `[verified]`
- Grounded the "successful GNN" comparison in the GNN-TS forecasting literature (the adaptive-adjacency / graph-structure-learning line — Graph WaveNet, MTGNN, and the 2023 survey), not in the repo's own summary. `[lit]`
- **Confidence:** HIGH that the null is real for the built design; HIGH that the cause is a graph-task/design mismatch rather than any "GNNs can't work here" impossibility; MODERATE that a different graph + site-level target could carry signal (plausible and literature-consistent, but untested here).

**One disagreement with a loose reading of the repo:** the docs sometimes shorthand this as "the graph doesn't help / GNN direction is dead." That is true *for what was built*, but the stronger claim — that graph structure is useless for datacenter resource modelling — is **not** established and should not be asserted. The precise, defensible statement is the one in §5.

---

---

## 8. Scrap vs salvage (added 2026-09-20, after a full primary autopsy of the whole `gat-based-forecasting/` repo)

The repo is Phase 2 of the project (a rigorously-audited null). It is not junk — it is a large amount of reusable engineering wrapped around a dead thesis. **~0% of the scientific thesis is reusable; ~60–70% of the engineering is.**

**SCRAP (dead for the accounting paper):** the GNN / graph-fusion thesis (proven null for this design); the routing / monthly-allocation / DAGNN(Guo) framing; the graph artifacts (`gat_weights_*.pt`, `aligned_dataset`, `graph_nodes`); China (no data ever existed); the Phase-1 hardcoded Tables 1–3 (zero provenance); the scraped DC atlas as a *primary* location source; the negative-result `.tex` manuscript (record of Phase 2, different/weaker-fit paper).

**SALVAGE (directly reusable for the new build):**

| Asset (in the repo) | Use in the new project |
|---|---|
| **Ember monthly US/EU/India** (downloaded), **GEM Global-Integrated-Power**, **Aqueduct 4.0**, **G3P/GRACE** | carbon+electricity primary/harmoniser; fuel-mix; scarcity cross-check; basin context — weeks of acquisition already done |
| **Geocoder** (`nbs/gat-colocation-weights-water-energy.ipynb` + `validate_join.py`): facility→grid-zone + facility→basin point-in-polygon, fuzzy-0.82, leakage-guarded, "never fabricate" guardrails | **~70% of S0** — retarget to CEA regions + HydroBASINS + AWARE watersheds |
| **Forecasting benchmark** (Chronos-2 > SARIMA > xLSTM on grid; SARIMA best on water after freq-fix; TSFM helps sub-nationally not nationally; horizon crossover) | **S11 forward projection** — already benchmarked, CPU, maps to editor Te Han |
| **Audit/rigor harness** (leakage assert, degree-matched controls, region-as-unit, permutation, bootstrap CI, MASE/skill, FDR, sha256 provenance, anti-fabrication discipline) | **the reproducibility pillar, pre-built** |

**Lessons that de-risk the new build:** signal lives in per-site heterogeneity (oracle beats region-blend 6–16%) → validates the **facility-month** unit; nearest-centroid basin assignment is too coarse (554 km median error) → **use HydroBASINS polygon point-in-polygon, not centroids**; capacity ≠ generation (GEM records what was built) → energy = capacity × utilization × PUE; the mid-month-timestamp `asfreq` trap; label every derived quantity honestly (the "Nexus contains SARIMA" saga). **PII to scrub before open release:** hackathon email in the repo's `docs/DATA.md`; a collaborator's Windows path in `SESSION_REVIEW_AND_NEXT_STEPS.md`.

---

### Sources
Primary: `gat-based-forecasting/paper_submission/docs/AUDIT_REPORT.md` (rev 2, 2026-08-27, sha256-stamped scripts) + the full repo (`paper_submission/`, `diff/gat-sarima-nexus/`, `results-2026/`, `project outline/`), read on primary 2026-09-20. Literature (GNN time-series forecasting): survey arXiv 2307.03759; MTGNN "Connecting the Dots" arXiv 2005.11650; plus the graph-structure-learning line (adaptive adjacency) as the standard successful pattern. Author-reported audit figures are the repo's own, reproduced in-run per its provenance table.

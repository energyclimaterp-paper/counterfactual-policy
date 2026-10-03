# Pipeline improvement backlog (priority-ordered)

Branch `feat/us-eu`. Ranked by value to the Q1 journal paper. Each "why" ties to a reviewer concern
(see `CORE_REVIEWS_AND_LESSONS.md`) or a concrete empirical vulnerability. Scope-setting decisions are at the end.

> **Current focus (user, 2026-10-03):** do the **policy / RAG section (P2.4)** properly *before* the routing work —
> see "Policy section" note below.

---

## P1 — do first (closes the reviewers' critique + hardens the soft spots)

1. **Foreground "simple beats complex" forecasting as a first-class result.**
   - *Why:* the reviewers' single biggest objection ("why not simple per-DC baselines + optimization?"). The
     evidence already exists in the fresh forecasting run (seasonal-naive vs SARIMA vs Co-RE models, simple wins).
   - *Do:* name **MinT / bottom-up reconciliation as the non-DL hierarchical baseline** R2 explicitly asked for
     (already computed — needs naming); emit one clean comparison table as a pipeline output.
   - *Done (2026-10-04):* `dcfootprint/experiments/forecast_exhibit.py` -> `results/forecast_simple_vs_complex.{md,csv}`
     + `forecast_hierarchical_onestep.csv`. Correction to the first version: `sarima_dcf` in the fresh run is a
     per-zone SARIMA, not bottom-up/MinT; the hierarchical methods are the one-step Q3 backtest (`project/hierarchy.py`),
     shown in their own table. Both windows reported; models compared with seasonal naive on the same points.
   - *Effort:* low (framing + one artifact).

2. **Harden Q3 routing's synthetic demand + 30% flexible-share assumption.**
   - *Why:* the most attackable empirical assumption in the pipeline.
   - *Do:* lead with the existing sweeps (`routing_v_sweep`, `routing_budget_sweep`) so the result is a bound
     across assumptions, not a point claim; cite the flexible-share rather than assert 30%.
   - **Citations ready (from `LIT_REVIEW_VERIFIED.md`):** #59 Norris et al. (Duke) "Integrating Large Flexible
     Loads" (2025); #60 Senga/Wang/Knittel (MIT) "Flexible Data Centers…" (iScience 2026); Google CICP (Virtual
     Capacity Curves for time-flexible load); the "Emerald Conductor" field demo (arXiv 2507.00909, "DC load is
     demonstrably flexible"). → flexibility is real and substantial; the exact shiftable fraction is
     workload-dependent (batch/training » interactive), so keep the **sweep** as the headline and report 30% as a
     central case, not a hard number.
   - *Effort:* low-medium (the citing/framing is done; the code change is the coauthor's on the routing core).

3. **India consumption-based carbon (Electricity Maps / EnergyMap).**
   - *Why:* removes the standing R2 generation-vs-consumption caveat; sharpens the India numbers.
   - *Do:* wire regional consumption-based CI (DATA.md PART G flags this as recoverable).
   - *Effort:* medium (data / API).

## P2 — worth doing, scope-dependent

4. **Policy (L5) cleanup + RAG evaluation.**  ✅ **DONE (2026-10-03)**
   - *Structural cleanup:* one `policy/registry.py` (26 instruments) → **derived** four-axis matrix + **computed**
     overlay + binding-constraints view; `region_effects`/`HARD_CONSTRAINTS` interface preserved (routing/siting
     unaffected). Outputs: `policy_registry.csv`, `regulation_matrix.csv`, `regulation_constraints.csv`,
     `policy_corpus.csv`, `regulation_constraints_cited.csv`.
   - *RAG decision* (evidence in `dcfootprint/results/rag_axis_audit.md`): the RAG is a **frozen corroboration
     exhibit + an optional live hook, NOT the policy backbone.** Its corpus is 86% EU / India-starved (Rajasthan
     ZLD unretrievable) and lacks the four closest-instruments the matrix needs; the registry is more complete.
     **Not expanded** (a retrieval+LLM system for a 12-cell map = the Co-RE over-engineering trap). A scoped
     EU/US-perimeter audit + gold eval remains possible later if we want it, but is not required for the paper.

5. **CGWB groundwater into the Q2 harm / equity view.**  ✅ **DONE (2026-10-03)**
   - `decisions/equity.py` overlays each facility's scarcity-water burden on the local CGWB groundwater stage of
     extraction (city/district else state). **Finding: 63% of India's DC scarcity-water burden lands on
     over-exploited aquifers (>100%), 81% on semi-critical-or-worse** (Bengaluru 187%, Chennai 125%). Standalone
     from the canonical account, no re-run. Exhibit: `results/q2_equity_groundwater.{md,csv}`. (C7 contribution.)

6. **Round-4 canonical run (India + US + EU).**
   - *Why:* reproducibility housekeeping; acceptance-critical for an "open, reproducible" paper.
   - *Do:* two clean runs, determinism diff, spot checks, attribution vs round 3, snapshot + tag. **After P1.**

## P3 — do NOT spend effort (document and move on)

7. **Real Nexus LLM forecaster** — 534 s/call, likely another null; our thesis + the reviewers say complexity
   doesn't help. Document as "not benchmarked, out of scope."
8. **GNN tested-extra** — formally **drop** (reported null in an appendix); building it re-invites the critique
   that sank Co-RE.
9. **MinT instability on US** — unused in the result (seasonal-naive won); guard or drop, don't repair.
10. **Precise India geocodes** — city-centroids are adequate for basin/state joins (stated limitation).
    *(Also skip for now: CEA cross-check, ERA5 temperature — marginal.)*

## Open decisions (set the scope of the above)

- **India-deep vs co-equal three-region** — changes how much US/EU polish (maps, coverage) is warranted.
- **RQ framing** — RQ2 (does the method change the answer) is strong; **RQ4 is two-sided** (India trade-off vs US
  co-benefit) and is, in our read, the most interesting result — candidate spine.
- **Nexus / GNN** — drop-and-document (recommended) vs keep chasing.

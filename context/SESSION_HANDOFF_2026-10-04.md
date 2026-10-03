# Session handoff — 2026-10-03/04 (Gauri's sessions)

> Complements `SESSION_HANDOFF_2026-09-27.md` (the coauthor's code-state authority) and
> `PIPELINE_IMPROVEMENTS.md` (backlog). Captures the **decisions + state** from the 10-03/04 sessions so they
> survive context compaction. Other key docs: `CORE_REVIEWS_AND_LESSONS.md`, and the result exhibits under
> `dcfootprint/results/` (`cross_region_summary.md`, `rag_axis_audit.md`, `forecast_simple_vs_complex.md`,
> `q2_equity_groundwater.md`).

## 0. TL;DR
- Work this session is on branch **`feat/policy-registry`** (isolated off `feat/us-eu`, **pushed**). Merge is the coauthor's step.
- Did: policy L5 cleaned to one derived registry; RAG evaluated + scoped (not the backbone); forecasting
  "simple beats complex" exhibit; cross-region synthesis; C7 groundwater-equity overlay; Co-RE reviews logged;
  current architecture diagram (`dcfootprint/docs/architecture_v2.svg`).
- Canonical results = India `round3-final`. **US/EU ran but are NOT canonical** (round-4 pending).

## 1. Key decisions (the reasoning compaction would otherwise lose)
- **Architecture = v2** (the author's `ARCHITECTURE_FINAL_2.md`): a 3-region account → **three decisions**
  (Q1 siting · Q2 harm-scorecard · Q3 routing), layers L0–L9. This **overrode the old "no agents / no GNN /
  no routing" kill-list** — a deliberate team decision. Guardrails kept: **GNN stays dropped** (audited null,
  `GNN_AUTOPSY.md`); **routing is a control-theoretic Lyapunov allocator on stylised demand** (the Ceiling reach),
  NOT learned RL; **forecasting is a supporting layer, not a contribution**.
- **Co-RE (NeurIPS TCCML workshop) was REJECTED.** Reviews + lessons in `CORE_REVIEWS_AND_LESSONS.md`. Lessons
  applied to the journal paper: simple baselines beat the complex GNN/DL; put resource/geography **coupling in the
  account + optimization** (a reviewer's own suggestion), not a joint/graph forecaster; state forecast granularity
  + horizon per use case.
- **Policy L5 cleaned:** one derived registry (`policy/registry.py`) → **computed** four-axis gap matrix + overlay
  + binding-constraints view. The headline (0/4 axes mandated → 100% blind spot) is now computed from the data,
  not asserted. `region_effects`/`HARD_CONSTRAINTS` interface **preserved** (routing/siting untouched).
- **RAG decision:** evaluated on real retrieval — corpus is **86% EU, India-starved** (Rajasthan ZLD
  unretrievable; scanned PDF), and **missing the four "closest instruments"** the matrix needs. → **NOT the policy
  backbone**; kept as a frozen corroboration exhibit (`rag_axis_audit.md`); **not expanded** (over-engineering trap).
- **Authorship (resolved):** it's a **team**, not solo — advisor **Ying** (Ying-Jung Chen), coauthor **Samiksha**
  (does most of the build via her own Claude on `D:\3Gtech_paper - GNN`). The `context/` docs that say "solo author"
  are inaccurate.
- **Git workflow:** `feat/us-eu` is canonical (coauthor's, **force-pushed**). **Never commit onto it** — branch in
  isolation and push that. `main` lacks the pipeline. History was rewritten 2026-09-27 (`COMMIT_HASH_MAP.md`).

## 2. Current state
- `feat/policy-registry` @ pushed: commits = policy cleanup · forecasting exhibit · cross-region synthesis ·
  C7 equity (+ this handoff + the architecture SVG).
- Canonical India run = tag `round3-final` (`results/round3_final/`). US (`results/us/`) and EU (`results/eu/`)
  are current-best but **not yet the locked snapshot**.

## 3. Results (headline — full detail in `results/cross_region_summary.md`)
| | India (71 fac) | US (235 fac) | EU (21 states) |
|---|---|---|---|
| Carbon | 3.63 Mt | 16.0 Mt | 3.35 Mt |
| Scarcity-weighted water | 846.6 M m³-eq | 2.51 bn m³-eq | 137 M m³-eq |
| Scope-2 (off-site) share | 60% | 68% | 82% |

- **Two-sided routing (standout):** US co-benefit (−29% water, −10% carbon) vs India trade-off (−22% water,
  +1.4% carbon; can't clear the overdraft).
- **Policy:** 0/4 axes mandated → 100% of burden in a regulatory blind spot.
- **Equity:** 63% of India's DC water burden on over-exploited aquifers (Bengaluru 187%, Chennai 125%).
- **Forecasting:** simple ≥ complex (deep net worst; no model meaningfully beats seasonal-naive).
- India calibrates to within ~8% of the independent CEEW estimate.

## 4. Outputs → research question (quick map; full table in chat log / `cross_region_summary.md`)
- **RQ1 magnitude** → the facility-month account (C1).
- **RQ2 method** → scope-2-at-generation-basins + scarcity weighting (C2/C4); groundwater-equity overlay (C7).
- **RQ3 regulatory gap** → the four-axis gap map + registry + RAG audit (C5).
- **RQ4 forward & levers** → counterfactual levers + Q1 siting + Q3 routing + forecasts (C6).
- **cross-cutting** → uncertainty/Sobol (C9); maps/figures/open code = the instrument (C8).

## 5. What's left (runs + backlog — full list in `PIPELINE_IMPROVEMENTS.md`)
- **Round-4 canonical run** (India+US+EU) → locks US/EU canonical. *Coauthor's (needs her `.venv` + data).*
- **India consumption-carbon re-run** once the Electricity Maps API is wired (being arranged).
- **Routing hardening** — lead with the sweep + cite the flexible-share (citations already in the backlog); code
  change is on the coauthor's routing core.
- **Merge `feat/policy-registry`** into `feat/us-eu`.
- **Team decisions:** paper format (full article vs perspective) + lead-framing + reconcile the RQ set, then draft.
- *Optional:* live-RAG expansion (OCR Rajasthan + corpus), near-submission novelty refresh, registry URL polish,
  precise geocodes, counterfactual re-audit.

## 6. Where to find things
`SESSION_HANDOFF_2026-09-27.md` (code map) · `PIPELINE_IMPROVEMENTS.md` (backlog) · `CORE_REVIEWS_AND_LESSONS.md`
(reviews) · `POLICY_DEEP_DIVE.md` (policy source) · `LIT_REVIEW_VERIFIED.md` (lit) · `dcfootprint/ARCHITECTURE.md`
(design + contributions) · `dcfootprint/docs/architecture_v2.svg` (current diagram) · `dcfootprint/results/*.md`
(the exhibits).

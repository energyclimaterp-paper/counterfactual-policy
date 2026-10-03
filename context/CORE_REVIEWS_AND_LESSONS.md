# Co-RE (NeurIPS TCCML 2026) — Peer-Review Feedback & Lessons for the Journal Paper

**What this is.** The full peer review of the *earlier* workshop paper
**"Co-RE: Co-Location Resource Ensembling for Grid and Watershed Aware Data Center Forecasting"**
(the GAT/GNN forecasting project in `gat-based-forecasting/`), submitted to **Tackling Climate Change
with Machine Learning (TCCML), workshop at NeurIPS 2026**, **Submission 299**.

**Final decision: Reject** (Program Chairs overrode the Area Chair's *Accept (Poster)*).

**Why it's logged here.** We are **not resubmitting** the Co-RE paper. This feedback is captured to inform the
**journal paper** (`dcfootprint`, *Energy and Climate Change* SI). Section 1 is a scorecard; sections 2–5 are the
reviews **verbatim** (reviewers' own wording and typos preserved); sections 6–9 are **our** synthesis and the
actions we take into the journal paper. Verbatim text is in blockquotes; everything outside blockquotes is ours.

---

## 1. At a glance

| Role | ID | Rating | ML expertise | Climate expertise | Confidence |
|---|---|---|---|---|---|
| Reviewer 1 | 1LPU | **Borderline** | published in the narrow area | published in the narrow area | very confident |
| Reviewer 2 | 8Grr | **Reject** | closely read + written in the broad area | skimmed, not published | willing to defend, may have missed details |
| Area Chair | 93kc | **Accept (Poster)**, confidence 3, spotlight 2 | — | — | somewhat confident |
| Program Chairs | — | **Reject** (final) | — | — | — |

Sub-scores — R1: Proposal Feasibility *Medium*, Climate *High*, **ML Relevance/Quality *Low***, Clarity *High*.
R2: Proposal Feasibility *N/A*, Climate *High*, ML *Medium*, **Clarity *Low***.
Awards (AC): Best Paper *No*, Best ML Innovation *No*, Best Pathway to Impact *No*.

Dates — R1 05 Sep 2026; R2 10 Sep 2026; Meta-review (AC) 22 Sep 2026; Decision (PC) 30 Sep 2026 (all modified 03 Oct 2026).

---

## 2. Reviewer 1 (1LPU) — verbatim

**Title:** "The paper presents a joint resource forecasting approach using graph neural networks (GAT, HGT, & GraphGPS)"
**Guidelines Confirmation:** Yes

**Review:**
> The paper presents a joint resource forecasting approach using graph neural networks. It forecasts electricity, water, and carbon footprint of data-centers. The paper aims to use these joint forecasts in carbon aware scheduling across data centers keeping energy and water constraints in mind.
>
> However, it is not clear that why joint forecasting across resources and data centers is necessary for carbon-water-energy aware scheduling.
>
> Consider this: If I have a carbon-water-energy requirements/forecasts given the data-center load individually for each data-center. Will this be not sufficient for carbon-water-energy aware scheduling. For estimating the carbon-water-energy, Is simple ML approaches such as ARIMA, Prophet, etc per data center not good enough for carbon-water-energy aware scheduling ?
>
> It appears that a multi objective optimization across carbon, water, and energy will be able to achieve the same goal. Therefore, why joint resource forecasting approach is needed is not clear. It is true that resource usage across different geographies are coupled, but those relations and dependencies can also be programmed in the optimization formulation.

**Follows Submission Guidelines:** Yes

**Summarize Objectives And Methods:**
> The paper presents a joint resource forecasting approach using graph neural networks. It forecasts electricity, water, and carbon footprint of data-centers. The paper aims to use these joint forecasts in carbon aware scheduling across data centers keeping energy and water constraints in mind.

**Climate Change Relevance:**
> The problem is clearly relevant to climate change. With growing number of data centers, the addressed problem will become even mode pertinent. Further, data centers have been heavily criticized for their intensive water usage.

**Techniques Well Matched:**
> Machine learning is required for the forecasting task. However, it is not clear that why joint forecasting across resources and data centers is necessary for carbon-water-energy aware scheduling. Simpler models can also do the forecasting tasks individually for each of the resource under consideration (carbon, water, and energy). Further, it is possible to feed these these individual forecasts into a multi objective optimization across carbon, water, and energy.

**Potential Effectiveness:**
> Effectiveness is not clear. The results should have been compared against a simple data-center level forecasters for each of the resources. If the simple models are giving good forecasts for joint optimization, then why use a compute heavy deep neural networks ? If joint forecasts are necessary, then it should be explained.

**Prior Work Context:**
> My primary concern is the use of deep neural networks for joint forecasting when a family of simpler individual models could have achieved the same objective. The paper lacks the comparison of forecasts from simpler ML models.

**Potential Impact:**
> Impact is primarily linked to multi resource (carbon, water, and energy) aware scheduling. Optimizing for a single resource at expense of other critical resource is not advised and this paper intends to address that. However, this objective can be achieved with a family of simpler ML models paired with a multi objective optimization framework.

**Clarity And Accessibility:**
> Submission is clear and accessible; methods are well described for a proposal.

**Scores** — Proposal Feasibility: **Medium** · Climate Relevance Feasibility And Impact: **High** · Machine Learning Relevance And Quality: **Low** · Submission Clarity And Accessibility: **High**

**Overall Assessment:**
> The paper proposes joint forecasting for electricity, water, and carbon emissions across data centers using GNN, with the forecasts used for carbon-aware scheduling under energy and water constraints.
>
> The key concern is that the paper does not clearly explain why joint forecasting is necessary. If resource usage can be forecast independently for each data center using simpler ML techniques, these forecasts should be sufficient for scheduling. Afterwards, A multi-objective optimization could jointly consider carbon, water, and energy constraints. Similarly, correlations between data centers and geographic dependencies could be incorporated directly into the optimization model.
>
> Therefore, the paper should clarify what additional value the joint GNN forecasting provides against independent forecasting followed by multi-objective optimization.

**Rating:** Borderline
**Climate Expertise:** I have published one or more papers in the narrow area of this submission.
**Machine Learning Expertise:** I have published one or more papers in the narrow area of this submission.
**Confidence:** I am very confident in my evaluation of this paper. I read the paper very carefully and I am very familiar with related work.
**Conflict Of Interest:** No known conflict of interest.

---

## 3. Reviewer 2 (8Grr) — verbatim

**Title:** "Running before walking"
**Guidelines Confirmation:** Yes

**Review:**
> This proposal evaluated four graph neural architectures to check if topological knowledge helps joint multi-resources forecasting for data centres. Initial results are negative, and the authors conclude that multi-modal feature fusion is the major constraint in cross-domain modeling. I would argue that their model setting is too complex, and it would be useful to do some validation and comparison on smaller domain to understand better in which situations topological knowledge helps, and when it hinders the modelling.

**Follows Submission Guidelines:** Yes

**Summarize Objectives And Methods:**
> The objective is to see if spatial proximity information can help forecast joint multi-resources forecasts data centres. The publicly open data is used and 4 different graph neural networks architectures are trialled with an ensemble of 4 simpler forecasters.

**Climate Change Relevance:**
> Forecasting resources for data centres could mitigate its high electricity and water demand and lower their carbon emissions.

**Techniques Well Matched:**
> This is a quite complex setting, there might be a simpler hierarchical forecast (see Hyndman) that could be used to benchmark 4 GNN architectures. Not completely clear how is 8d embedding chosen.

**Potential Effectiveness:**
> This is a complex problem and I think the solution is trying to scale up before understanding mechanisms in smaller, simpler contexts. Therefor the effectiveness is limited.

**Prior Work Context:**
> Prior work is roughly given, some references are ephemeral (e.g. [3]). There is no appraisal of previous work on joint multi-resources forecasts, we go straight into graph -based neural networks.

**Potential Impact:**
> The authors claim that improving joint multi-resources forecasting would enable the carbon aware scheduling, workload shifting, and siting decisions needed to keep compute growth within regional grid and watershed limits. However, these are all different forecasting horizons, which will require different methods.

**Clarity And Accessibility:**
> Overall, the text is readable, except for a few strange expressions, i.e.p1 line 16 "... data centers are gradually important to..." etc. It is not overly accessible. For example, it needs some work to establish what exactly is being forecasted, what granularity and horizon of the forecast. 'Router' is used without the definition, and so on.

**Scores** — Proposal Feasibility: **N/A** · Climate Relevance Feasibility And Impact: **High** · Machine Learning Relevance And Quality: **Medium** · Submission Clarity And Accessibility: **Low**

**Overall Assessment:**
> Due to its complex setting, I think it is a struggle to write a short paper on this work, as it becomes inaccessible. There are too many design choices that are not completely explained. It would be helpful to state what is exactly being forecasted, data granularity, forecast time horizon, main use cases - is it for planning, operations, maintenance etc. 4GNNs could be benchmarked with a hierarchical method that is not based on deep learning.

**Rating:** Reject
**Climate Expertise:** I have seen talks or skimmed a few papers on this topic, and have not published in this area.
**Machine Learning Expertise:** I have closely read papers on this topic, and written papers in the broad area of this submission.
**Confidence:** I am willing to defend my evaluation, but it is fairly likely that I missed some details, didn't understand some central points, or can't be sure about the novelty of the work.
**Conflict Of Interest:** No known conflict of interest.

---

## 4. Area Chair 93kc — Meta Review (verbatim)

**Metareview:**
> Pros: rigorous and relevant.
>
> Cons:
> - Some clarifications are necessary (minor).
> - Potential overengineering as per this comment "My primary concern is the use of deep neural networks for joint forecasting when a family of simpler individual models could have achieved the same objective. "
> - and related to the previous point: what is the benefit of trying to forecast several things together? is this properly motivated and experimentally supported?

**Explanation of decision:**
> I'd like to give this an opportunity to present and to get feedback.

**Decision:** Accept (Poster)
**Confidence:** 3: The area chair is somewhat confident
**Spotlight presentation rating:** 2
**Best Paper Award:** No · **Best ML Innovation Award:** No · **Best Pathway to Impact Award:** No

---

## 5. Program Chairs — Paper Decision (verbatim)

**Decision:** Reject
**Comment:**
> Since the area chair felt that the work was not polished enough and should be presented only as an opportunity to get further feedback, we decided to modify the decision to a rejection.

---

## 6. Cross-cutting themes (our synthesis)

All three documents converge on **one** objection, restated several ways:

1. **"Why joint / GNN forecasting at all?"** — the single dominant concern (R1 ×4, AC ×2). Per-datacenter simple
   forecasters (ARIMA/Prophet) feeding a **multi-objective optimization** that encodes the coupling "will be able
   to achieve the same goal." The complex deep/joint model is unjustified *and* unsupported by the paper's own
   negative result.
2. **Missing simple-baseline comparison.** R1: compare against "simple data-center level forecasters for each of
   the resources." R2: benchmark the "4 GNN architectures" against "a hierarchical method that is not based on
   deep learning (see Hyndman)."
3. **Overengineering / "running before walking."** R2 + AC: too complex a setting; validate on a smaller/simpler
   domain to learn **when topology helps and when it hinders**.
4. **Horizon conflation.** R2: scheduling, workload shifting, and siting "are all different forecasting horizons,
   which will require different methods."
5. **Clarity.** R2: state *what* is forecast, at what **granularity** and **horizon**, for what **use case**
   (planning/operations/maintenance); "'Router' is used without the definition"; the 8-d embedding is unexplained.
6. **Prior-work appraisal.** R2: no appraisal of previous joint multi-resource forecasting; "some references are
   ephemeral."
7. **Decision dynamics.** AC: "rigorous and relevant," wanted **Accept (Poster)** for feedback; PCs downgraded to
   **Reject** as "not polished enough." → the *science was respected*; **framing/motivation/polish** sank it.

---

## 7. Our interpretation — agree / disagree (unbiased)

**Where the reviewers are right (we agree — and largely already acted on it):**
- The GNN was unmotivated and unsupported. The Co-RE abstract itself states graph fidelity "does not translate
  into forecasting gains over seasonal naive and SARIMA." The reviewers simply read that honestly. This is exactly
  the conclusion of `context/GNN_AUTOPSY.md`, and the journal pipeline **drops the GNN**.
- The simple-vs-complex comparison needed to be **foregrounded**. Co-RE *did* contain classical baselines (SARIMA,
  the seasonal-naive skill audit), but neither reviewer could see a clean "does complexity help?" benchmark — a
  **framing failure, not an absence.**
- Horizons must be separated by use case (R2). The journal paper already does this (present/measured for Q2;
  one-step short horizon for Q3 routing; 2030/2050 scenarios for Q1 siting) — it just has to be *stated*.
- Clarity: define what/granularity/horizon/use-case and every term. Cheap to fix, expensive to ignore.
- Appraise prior joint multi-resource forecasting work (we have `LIT_REVIEW_VERIFIED.md`).

**Where we push back (we disagree, with reasons):**
- **"Per-DC ARIMA is sufficient" under-specifies the real problem.** For the *present* account we **do not
  forecast — we measure**. For *projection*, the hard quantity is **sub-national grid carbon intensity + growth
  scenarios**, not per-datacenter load; "ARIMA per DC" is not the relevant baseline. R1 is right that *simple* is
  enough; wrong about *what* needs forecasting.
- **Coupling genuinely matters — just not in the forecaster.** Shared-basin water and shared-grid headroom really
  do drive siting and routing. But R1 supplies the fix themselves — *"those dependencies can also be programmed in
  the optimization formulation."* That is precisely what the journal pipeline does (incidence matrices + basin
  queues + routing). So we **agree coupling is real** and **disagree that a GNN is how to capture it** — which is
  also what the null showed.
- R2 self-rates climate expertise "skimmed" and confidence "likely missed details," so the lowest-confidence
  specifics (ephemeral refs, 8-d choice) are polish items, not load-bearing.

**Net:** this rejection is, in effect, a **spec for the journal paper we are already writing.** Two area
experts + an AC told us the complex path is unjustified and the coupling belongs in the optimization — the exact
pivot already made. The main risk is letting forecasting creep back toward center stage in the write-up.

---

## 8. Actions for the journal paper (`dcfootprint`)

1. **Foreground "does complexity help?" as a headline result, not an appendix.** Use the fresh forecasting run
   (seasonal-naive vs SARIMA vs the Co-RE models on 10 metrics; simple wins, SARIMA skill ≈ −0.35). Frame it as the
   direct answer to R1/R2/AC: *"we tested whether ML/graph complexity improves resource forecasting; it does not;
   so we forecast simply and put the coupling in the account and the optimization."*
2. **Narrate the coupling exactly as R1 prescribed** — in the formulation (basin queues, incidence matrices,
   routing), not a joint forecaster.
3. **State the horizon per decision explicitly:** present/measured (Q2 scorecard), one-step short-horizon (Q3
   routing), 2030/2050 scenarios (Q1 siting). Directly answers R2's horizon critique.
4. **Define every term**, lead with the simple account, and keep the GNN only as a *reported negative result*
   (appendix at most). Forecasting is a supporting layer, never the contribution.
5. **Add a prior-work appraisal** of joint multi-resource forecasting (from the lit review).
6. **Polish is a first-class requirement** — the AC called the work rigorous; polish/motivation is what the PCs
   rejected. Treat clarity and motivation as acceptance-critical, not cosmetic.

---

## 9. For the Co-RE paper itself (reference only — not resubmitting)

If it were ever revived, the reviewers point to a different, publishable paper: a **negative-result /
"when does topology help vs hurt" study** (R2's explicit ask) — add a non-DL hierarchical (Hyndman) + per-DC
statistical baselines head-to-head, run the smaller-domain validation first ("walk before run"), define the
router/granularity/horizon, justify the 8-d embedding, and fix the references. Logged for completeness; the Co-RE
assets we actually reuse (data pipeline, cached forecasts, rigor harness) live on via `REUSE.md`.

# Novelty & impact — the pre-drafting anchor

> Grounds what to **claim**, what to **down-scope**, and the few **implementation touches**, checked against
> `LIT_REVIEW_VERIFIED.md` (89 works, full-text on the key neighbours). Written 2026-10-08.
> **Rule: lead with the three pillars; everything else is integration or corroboration.**

## Verdict
The core is a **genuine, unoccupied improvement** with a decision-relevant story. But the novelty is **narrower
than the "six-axis" framing** — it rests on **three pillars**. There is **no single "wow" number**; the strength
is integration + India-first + the decision framing. A few low-effort, existing-data implementation touches raise
impact; **most of the fixes are framing, not code.**

## 1. The three load-bearing pillars (lead with these)
| Pillar | Why it is genuinely novel (per the review) | Closest neighbour it beats |
|---|---|---|
| **C1** India sub-national, facility-level, **joint** carbon+water account | India account **confirmed unbuilt** — the space is journalism + CEEW advocacy; no peer-reviewed account exists | #88 symbiosis (India = 1 of 98, national LCA); #40 WaterWise (Mumbai = 1 AWS region inside a scheduler) |
| **C5** four-axis **regulatory-gap MAP** (India/US/EU) | no comparative four-axis gap map exists; others *call for* policy, none *maps* where the axes fall through | #74 Bolaños-Zuñiga ("calls for integrated policy", no map); EU Reg 2024/1364 (#61) mandates none of the four |
| **C8** open, reproducible instrument + released India dataset | the field repeatedly, explicitly demands exactly this | #28 de Vries-Gao, #32 Hankendi/Sovacool, #33 Privette, #64 FAS, **#18 Wang/Han/Wei (the guest editor + EiC)** |

## 2. Thinner than the six-axis framing implies — down-scope BEFORE a reviewer does
- **Scope-2 dominance ("60–82% off-site") is corroboration, not discovery** — Guidi #3 (~¾ off-site, US) and Siddik #6 already showed it. Our value = the India number + joint-with-carbon + cross-region, not the fact itself.
- **Scarcity-weighting is not a novel method** — SCARF #14, WCI #4, WaterWise #40, Talukder #24 all do it. Novelty = applying it jointly + sub-nationally + to India.
- **Marginal carbon is NOT a differentiator** — MARLIN #69 and #74 both use it (also #16/#29/#38/#43/#66). Keep it **Ceiling-only, US/UK-labelled**; impossible for India (regional annual grids).
- **Inference attribution is near-vestigial** — a flat ~85% sectoral scalar, coarser than How-Hungry #47 / WCI #4; it scopes, it does not discriminate between facilities. **Drop it from the headline axes** (keep as a stated sensitivity).

## 3. Decision-relevant findings, rated honestly
| Finding | Decision relevance | Trust / risk |
|---|---|---|
| **Two-sided routing** (US co-benefit; India trade-off, 34-month overdraft it can't clear) | **Highest** — the fashionable fix (load-shifting) doesn't work in India → siting + binding limits needed | On **stylised demand** + assumed flexible share. **Must be framed as a bound** (the α-sweep supports this) or it reads as a toy |
| **Equity: 63% of India burden on over-exploited aquifers** | **High** — crisp, quotable, reinforces the routing result | Coarse (city-centroids, annual CGWB); diagnostic only |
| **Regulatory gap: 0/4 axes mandated** | **Solid policy framing** | Descriptive; the quantitative burden overlay is what lifts it above a table |
| RQ2 "method doesn't re-rank annually" | Low — an **honest null**, reframed ("siting already coincides with stress") | Reads as "the fancy method didn't matter" if not framed carefully |

There is a coherent decision-grade story; there is **not** one stunning number. Acceptable for a comprehensive
Q1 paper, but that is the honest ceiling — the two-sided routing is the best shot at "striking," *if* the bound holds.

## 4. Keep-minor, or it looks like padding
- **RAG / policy corpus** — the registry does the work; keep the RAG a one-paragraph **appendix corroboration**, not a "layer".
- **Forecasting (L3)** — a null (simple ≥ complex). Supporting input to Q3 + honest negative; never a contribution.
- **GNN** — dropped; one-paragraph appendix caution only (rebuilding re-invites the Co-RE critique).
- **Q2 scorecard** — the thinnest decision (close to "sort the account"); **fuse with the equity overlay** (see §6.2).

## 5. The one positioning tension to resolve deliberately
The moat is **"the field optimizes/schedules; we *account*"** — the accounting cell is what's empty (review's
MARLIN #69 note). But v2 added **Q3 routing**, the thing the kill-list + the Co-RE reviewers flagged. Frame Q3 as
a **diagnostic bound on our own account** ("does shifting help? → two-sided"), never a deployable router, or the
inconsistency shows.

## 6. What to do about it

### 6.1 Framing fixes (NO code)
- Abstract leads on **India + regulatory-gap + open instrument**; the rest is integration/corroboration.
- Routing = **diagnostic bound**, sweep-led, synthetic demand stated up front.
- Marginal = US/UK Ceiling; inference = stated sensitivity scalar (off the headline).
- RQ2 = "average is adequate *because siting coincides with stress*" (an honest-negative with a reason, not a failure).

### 6.2 Implementation touches — all from EXISTING data, NO new complexity
1. **Surface C3 "when" (highest value).** The account is monthly and routing already uses seasonality, but the
   account's **own seasonal burden peak is never reported**. Add a monthly burden profile: *when* does the joint
   scarcity+carbon burden peak, and do the two **co-peak in dry-season months**? (Source: `account_facility_month.parquet`.)
   Turns a half-delivered Tier-1 contribution into a finding; strengthens the "siting + limits must be seasonal" message.
2. **Fuse Q2 + equity (C7).** Merge the CGWB groundwater-stage overlay (`decisions/equity.py`) into the Q2
   scorecard (`decisions/scorecard.py`) so there is **one distributional decision-output** (facility harm × local
   aquifer stress × category) instead of a thin Q2 + a separate exhibit.
3. **India consumption-carbon (Electricity Maps).** Already planned, **blocked on the API key**; removes the R2
   generation-vs-consumption caveat and sharpens the India side of the routing.

### 6.3 Explicitly do NOT add (measly gain, re-invites the Co-RE critique)
New ML models, the GNN, expanding the legal RAG, or a real-demand routing overhaul. Complexity is the trap that
sank the prior paper; the reviewers and our own forecasting null both say simple wins.

---
*Cross-refs: `LIT_REVIEW_VERIFIED.md` (nearest-neighbour deltas), `dcfootprint/ARCHITECTURE.md §7` (tiered
contributions C1–C9), `dcfootprint/results/README.md` (the results + trust levels).*

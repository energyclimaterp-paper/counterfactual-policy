# Cross-region results synthesis — India / US / EU (the paper's results backbone)

Pulled from the committed per-region results (India = canonical `round3-final`; US/EU = current, not yet
canonical). Maps every number to an RQ. Absolutes are calibrated ranges (util/PUE/WUE assumed) — lead with the
spatial/relative results. India carbon is state-generation-based (R2 caveat); US/EU coverage is partial.

## RQ1 — magnitude & distribution (the account)
| | India (71 fac, 2024) | US (235 fac, 2024) | EU (21 states, 2023) |
|---|---|---|---|
| Carbon | 3.63 Mt CO₂/yr | 16.0 Mt CO₂/yr | 3.35 Mt CO₂e/yr |
| Physical water | 24.8 Mm³/yr | 196 Mm³/yr | 37.9 Mm³/yr |
| Scarcity-weighted water | **846.6 M m³-eq/yr** | **2.51 bn m³-eq/yr** | **137 M m³-eq/yr** |
| Scope-2 share of scarcity water | 60% | 68% | 82% |
| Mean grid CI | 596 g/kWh (generation) | 309 g/kWh | 238 g/kWh |
| Coverage / calibration | 1.39 GW = 0.92× CEEW 1.5–1.8 | 51.9 TWh = 30% of LBNL 176 | 770/2,161 DCs (36%), measured |
| Scarcity 90% band | 573–1,074 M | 1.64–3.05 bn | 93–138 M |

**Headline for RQ1:** the burden is large, concentrated in water-stressed basins, and **most of the water is
off-site** (scope-2, at the power plants) in every region — 60–82%.

## RQ2 — does the accounting method change the answer?
Yes, decisively, via **where the water is counted**: 60–82% of the scarcity burden is scope-2, localized to the
**generation** basins (capacity-weighted per fuel), not the datacenter's own basin. A naive on-site-only or
unlocalized account misses the majority of it. (Scarcity *re-ranking* at the annual level is modest — the honest
"method matters mainly through scope-2 localization, not annual re-ranking" finding.) Uncertainty is
util/PUE/WUE-dominated (India Sobol: util 0.65), so relative/spatial results are the robust ones.

## RQ3 — the regulatory gap
**100% of the measured burden sits in a regulatory blind spot in all three regions** — 0 of the 4 axes
(carbon-intensity, marginal carbon, scarcity-weighted water, inference attribution) is mandated anywhere, against
a 26-instrument registry (15 cited corpus docs, 12 in force). The regulated perimeter is efficiency (PUE/WUE),
volumetric water, grid-access/rate, and entity disclosure — none of our four axes.

## RQ4 — forward & levers (the decision layers)
**Which lever pays** (share of scarcity water saved):
| Lever | India | US | EU |
|---|---|---|---|
| Water recycling (ZLD) | 36.9% | 29.3% | 16.4% |
| Efficiency standard | 36.6% (+18.8% carbon) | 31.4% (+12.9% carbon) | 6.9% (+4.4% carbon) |
| Coastal seawater | 17.3% | — | — |

**Q3 routing is two-sided — the most interesting result:**
- **India = trade-off:** routing saves ~21.7% scarcity water but *adds* ~1.4% carbon, and it **cannot clear the
  overdraft** — 34 of 96 occupied basin-months already have zero water left, a floor no router removes. Siting and
  capacity limits are needed, not just load-shifting.
- **US = co-benefit:** routing saves **~29% water AND ~10% carbon** at once.
- **EU = not routable** at country tier (no site locations).
- **Why the contrast:** India's hub basins are already in deficit (dry-season AWARE caps), so there's no slack to
  route into; the US grid/basins have headroom.

**Q1 siting** consistently favors low-scarcity, low-carbon corners — **Karnataka** (India), **Washington** (US),
**Sweden** (EU) — stable under 2030/2050 Aqueduct scenarios. **Q2** flags 16/71 (India), 53/235 (US), 4/21 (EU)
facilities as harmful (top-quartile scarcity water in high-stress basins).

## Supporting finding — forecasting (not a contribution)
Simple ≥ complex across 66 series × 3 regions: the deep net (xLSTM) is worst, classical/hierarchical SARIMA and
seasonal-naive win or tie, no model meaningfully beats naive (MASE 0.79–1.0). See `forecast_simple_vs_complex.md`.
The resource/geography coupling lives in the account + optimization, not a joint/graph forecaster. GNN dropped (null).

## The paper's spine, in one line
*Measure the joint carbon + scarcity-water footprint of AI datacenters sub-nationally (India deep, US/EU
comparison); show most of it is off-site and entirely outside what any regulation requires; and show that the fix
is two-sided — load-routing is a co-benefit where there's slack (US) but only a partial, trade-off tool where
basins are already in deficit (India), so siting and binding limits are needed.*

## Caveats to state
US/EU are current; India carbon is now **consumption-based** (Electricity Maps regional, import-adjusted;
generation is the stated sensitivity); coverage is partial (US ~30%, EU ~36%); Q3 routing uses stylised demand
+ an assumed flexible share (bounded by a sweep).

## 2026-10-10 updates (consumption carbon · seasonal · equity fusion)
- **India carbon consumption-based (closes R2):** national total within **+0.2%** of generation, but
  sub-national carbon re-ranks ±20–40% (Bengaluru **+37%**, Delhi +39%, Gujarat +34%, TN +9%; UP **−28%**,
  Telangana −20%) → a positive *carbon* re-ranking instance for RQ2 (the water re-ranking was a near-null).
- **Seasonal (C3, *when*):** India carbon + scarcity **co-peak in March** (dry pre-monsoon; top-3 months = 38%
  of annual scarcity water); US co-peaks in summer (corr +0.62); **EU anti-correlated** (water Aug, carbon Jan,
  corr −0.49), so a seasonal lever cannot serve both axes in the EU. See `seasonal_profile.md`.
- **Q2 fused with equity:** the scorecard now carries each facility's groundwater stage (`gw_stage_pct`,
  `gw_category`) — Bengaluru = scarcity pctile 100 on a 187%-over-exploited aquifer.

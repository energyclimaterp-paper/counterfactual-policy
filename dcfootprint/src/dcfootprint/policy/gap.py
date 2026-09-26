"""L5 — regulatory four-axis gap matrix + constraints (hand-coded from POLICY_DEEP_DIVE,
the human-verified gold; drop-in-replaceable by a frozen RAG regulation_matrix.csv).

The thesis (triple-confirmed): no enacted or proposed instrument in US/EU/India
mandates any of the four axes our account produces — carbon intensity, marginal
carbon, scarcity-weighted water, inference attribution. So the *entire* measured
burden falls in a regulatory blind spot.
"""
from __future__ import annotations

import pandas as pd

AXES = ["carbon_intensity", "marginal_carbon", "scarcity_weighted_water", "inference_attribution"]
JURISDICTIONS = ["US", "EU", "India"]

# mandated? (all No) + the closest instrument, from POLICY_DEEP_DIVE §1
_CLOSEST = {
    "carbon_intensity": "EU CSRD/ESRS E1 (per-revenue, entity-level, narrowed); MN/DE renewable-supply",
    "marginal_carbon": "voluntary 24/7 CFE tariffs (consumption, not marginal)",
    "scarcity_weighted_water": "EU ESRS E3 water-in-stress (entity volume); CA AB2619 (proposed)",
    "inference_attribution": "EU AI Act Annex XI model energy doc (training, no water/carbon)",
}

# hard/soft constraints that DO bite (used by routing legal screen + siting)
HARD_CONSTRAINTS = pd.DataFrame([
    {"jurisdiction": "India", "region": "Rajasthan", "rule": "ZLD + recharge mandatory", "type": "hard"},
    {"jurisdiction": "India", "region": "Gujarat", "rule": ">=51% renewable energy", "type": "hard"},
    {"jurisdiction": "EU", "region": "Germany", "rule": "PUE<=1.2 new (2026)", "type": "hard"},
    {"jurisdiction": "EU", "region": "Ireland", "rule": ">=80% additional RE; locational test", "type": "hard"},
    {"jurisdiction": "EU", "region": "Netherlands", "rule": "hyperscale ban (>10ha & >=70MW)", "type": "hard"},
    {"jurisdiction": "EU", "region": "EU-wide", "rule": "EED/2024-1364 PUE+WUE reporting >=500kW", "type": "soft"},
    {"jurisdiction": "US", "region": "Minnesota", "rule": "RE/carbon-free supply; >100Mgal water permit", "type": "hard"},
])


def four_axis_matrix() -> pd.DataFrame:
    rows = [{"axis": ax, **{j: "No" for j in JURISDICTIONS}, "closest_instrument": _CLOSEST[ax]} for ax in AXES]
    return pd.DataFrame(rows)


def gap_overlay(account: pd.DataFrame) -> dict:
    """Overlay measured burden on the gap: since no axis is mandated anywhere, 100%
    of high-burden facility-months sit in a blind spot. Report the magnitude that is
    unregulated on each axis."""
    ann = account.groupby("facility_id").agg(
        scarcity_m3eq=("water_scarcity_l_eq", lambda s: s.sum() / 1000.0),
        carbon_tco2=("carbon_tco2", "sum")).reset_index()
    return {
        "n_facilities": int(len(ann)),
        "total_scarcity_m3eq_unregulated": round(float(ann["scarcity_m3eq"].sum()), 0),
        "total_carbon_tco2_unregulated": round(float(ann["carbon_tco2"].sum()), 0),
        "pct_burden_in_blind_spot": 100.0,   # no axis mandated in any jurisdiction
        "axes_mandated_anywhere": 0,
    }


if __name__ == "__main__":
    print(four_axis_matrix().to_string(index=False))
    print("\nhard/soft constraints:")
    print(HARD_CONSTRAINTS.to_string(index=False))

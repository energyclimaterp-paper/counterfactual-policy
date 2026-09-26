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

# hard/soft constraints that DO bite, with a machine-readable `effect` + `param` so the
# routing (Q3) and siting (Q1) layers can apply them (config/legal_constraints.csv).
def load_constraints() -> pd.DataFrame:
    from dcfootprint.io.facilities import _repo_root
    return pd.read_csv(_repo_root() / "dcfootprint" / "config" / "legal_constraints.csv")


HARD_CONSTRAINTS = load_constraints()


def region_effects(region: str, constraints: pd.DataFrame | None = None) -> dict:
    """{effect: param} for the hard rules that apply in `region` (a state / country name).
    Effects understood downstream:
      zld_mandate       -> scope-1 water x (1 - param)
      re_share_min      -> grid carbon x (1 - param)   (the mandated renewable share is carbon-free)
      ban_new_above_mw  -> no new facility / no added load at or above `param` MW
      pue_cap_new       -> PUE <= param for new facilities
      water_permit_mgal -> annual scope-1 water above `param` million US gal needs a permit (flag)"""
    c = HARD_CONSTRAINTS if constraints is None else constraints
    rows = c[(c["type"] == "hard") & (c["region"] == region)]
    return {r["effect"]: float(r["param"]) for _, r in rows.iterrows() if pd.notna(r["param"])}


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

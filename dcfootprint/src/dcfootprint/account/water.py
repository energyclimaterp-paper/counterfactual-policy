"""L2 water accounting — the reference module (pattern for all account/ modules).

Implements the lit-review equation (Guidi/Harvard; Li "Thirsty"):
    W_onsite = WUE * E_IT                       # scope-1 (on-site cooling)
    EWIF(z,m) = sum_fuel share(z,m) * macknick[fuel]
    W_grid   = EWIF(z,m) * E_grid               # scope-2 (grid-embedded)
    W_phys   = W_onsite + W_grid                # physical litres (reported FIRST)
    W_scarce = W_phys * AWARE_CF(basin, month)  # SEPARATE column, never blended

Design principles (why this is a module, not a script):
  * Pure function: dataframes in -> dataframe out; no I/O, no globals.
  * Parameters come from config (parameters.yaml), never hardcoded.
  * Output is validated against schemas.FacilityMonthAccount by the caller/DAG.
  * Vectorised (pandas/numpy) over facility-month; no per-facility Python loops.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def ewif_by_zone_month(fuel_mix: pd.DataFrame, ewif_coeff: dict[str, float]) -> pd.DataFrame:
    """Scope-2 water intensity per zone-month = sum(fuel_share * Macknick coeff).

    fuel_mix: long df [zone_id, date, fuel, share]  (shares sum to 1 per zone-month)
    ewif_coeff: {Ember fuel name -> L/MWh}  (config/parameters.yaml)
    returns: [zone_id, date, ewif_l_per_mwh]
    """
    m = fuel_mix.copy()
    m["coeff"] = m["fuel"].map(ewif_coeff)
    if m["coeff"].isna().any():
        missing = sorted(m.loc[m["coeff"].isna(), "fuel"].unique())
        raise KeyError(f"Fuels with no EWIF coefficient (add to config): {missing}")
    m["contrib"] = m["share"] * m["coeff"]
    return (m.groupby(["zone_id", "date"], as_index=False)["contrib"]
              .sum().rename(columns={"contrib": "ewif_l_per_mwh"}))


def water_account(
    energy: pd.DataFrame,          # [facility_id, date, zone_id, basin_id, e_it_mwh, e_grid_mwh, month]
    wue_l_per_kwh: pd.Series,      # per facility (from parameters: operator override else default)
    ewif_zone_month: pd.DataFrame, # [zone_id, date, ewif_l_per_mwh]  (from ewif_by_zone_month)
    aware_cf: pd.DataFrame,        # [basin_id, month, cf]  (validated BasinMonthlyCF)
) -> pd.DataFrame:
    """Compute the facility-month water columns. Returns df ready to merge into
    the FacilityMonthAccount. Physical first; scarcity as a labelled separate column."""
    df = energy.merge(ewif_zone_month, on=["zone_id", "date"], how="left")
    df = df.merge(aware_cf, on=["basin_id", "month"], how="left")

    wue = df["facility_id"].map(wue_l_per_kwh)                    # L/kWh
    df["water_onsite_l"] = wue * df["e_it_mwh"] * 1000.0          # kWh = MWh*1000
    df["water_grid_l"]   = df["ewif_l_per_mwh"] * df["e_grid_mwh"]
    df["water_phys_l"]   = df["water_onsite_l"] + df["water_grid_l"]
    # scarcity: physical x AWARE CF (climatological-monthly). SEPARATE column.
    df["water_scarcity_l_eq"] = df["water_phys_l"] * df["cf"]
    return df


# NOTE: carbon.py, energy.py follow the SAME shape (pure, config-driven, vectorised,
# schema-validated). counterfactual/levers.py applies a parameter transform (e.g.
# coastal_seawater_siting -> override wue; zero_liquid_discharge -> *(1-recycle))
# and re-runs water_account/carbon to produce the Delta vs baseline.

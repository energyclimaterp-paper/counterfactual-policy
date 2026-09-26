"""L2 — carbon. Carbon = E_grid * grid emission factor.
India (v1): CEA national-annual grid EF (incl. RES) — a single consumption-relevant
factor on the synchronous national grid (so India's sub-national signal rides on
water, not carbon; config regions.R2). A per-zone/month CI can be swapped in later
(Ember generation-proxy, flagged) without changing this interface.
"""
from __future__ import annotations

import pandas as pd


def carbon_account(energy_df: pd.DataFrame, ef_tco2_per_mwh: float) -> pd.DataFrame:
    """Add carbon_tco2 from a national annual EF (tCO2/MWh)."""
    df = energy_df.copy()
    df["carbon_tco2"] = df["e_grid_mwh"] * float(ef_tco2_per_mwh)
    return df

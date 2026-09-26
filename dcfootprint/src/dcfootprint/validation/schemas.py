"""Data contracts (pandera) — the anti-granularity-mistake core.

The GAT project failed by forcing region-level data to a facility-level task.
Here that error becomes a *test failure*: every dataframe crossing a layer
boundary must pass a schema that pins its granularity, units, keys and ranges.

Rule (from DATA.md §0): the atomic unit is the **facility-month**; each resource
keeps its native partition; the facility is the join key; you aggregate UP to a
resource's native grain, never down-force one partition onto another. These
schemas make that rule executable.

Usage:
    from dcfootprint.validation import schemas
    facilities = schemas.Facilities.validate(df)          # raises on violation
    account    = schemas.FacilityMonthAccount.validate(df)
"""
from __future__ import annotations
import pandera.pandas as pa
from pandera.typing import Series
import pandas as pd

VALID_REGIONS = ("India", "US", "EU")


class Facilities(pa.DataFrameModel):
    """L0/L1 — one row per facility (the spine)."""
    facility_id: Series[str] = pa.Field(unique=True)
    operator: Series[str] = pa.Field(nullable=True)
    region: Series[str] = pa.Field(isin=VALID_REGIONS)
    state: Series[str] = pa.Field(nullable=True)
    latitude: Series[float] = pa.Field(ge=-90, le=90, nullable=True)   # nullable until geocoded
    longitude: Series[float] = pa.Field(ge=-180, le=180, nullable=True)
    capacity_mw: Series[float] = pa.Field(gt=0, le=5000, nullable=True)  # disclosed MW; large values = verified announced campus/park totals (e.g. Lodha Palava 2500), not single operational buildings
    zone_id: Series[str] = pa.Field(nullable=True)   # carbon join key (ISO|state or ISO3)
    basin_id: Series["Int64"] = pa.Field(nullable=True)  # AWARE Basin_ID (post point-in-polygon)

    class Config:
        strict = False
        coerce = True


class EmberZoneMonth(pa.DataFrameModel):
    """L0 carbon panel — zone x month (Ember). NOT facility-level: this is the
    native partition that gets *applied* to facilities, never forecast per-facility."""
    zone_id: Series[str]
    date: Series[pa.DateTime]
    ci_gco2_per_kwh: Series[float] = pa.Field(ge=0, le=1500, nullable=True)
    generation_gwh: Series[float] = pa.Field(ge=0, nullable=True)

    @pa.dataframe_check
    def unique_zone_month(cls, df: pd.DataFrame) -> bool:
        return not df.duplicated(subset=["zone_id", "date"]).any()

    class Config:
        coerce = True


class BasinMonthlyCF(pa.DataFrameModel):
    """AWARE native CFs — basin x 12 climatological months (NOT year-specific).
    Join to facilities is SPATIAL (point-in-polygon on the gpkg), by Basin_ID."""
    basin_id: Series["Int64"] = pa.Field(unique=True)
    month: Series[int] = pa.Field(ge=1, le=12)
    cf: Series[float] = pa.Field(ge=0, le=100)   # AWARE capped at 100

    class Config:
        coerce = True


class FacilityMonthAccount(pa.DataFrameModel):
    """L2 OUTPUT — the atomic unit. One row per (facility, month).
    Physical water and scarcity-weighted water are SEPARATE columns (no frankenmetric).
    """
    facility_id: Series[str]
    date: Series[pa.DateTime]
    region: Series[str] = pa.Field(isin=VALID_REGIONS)
    e_it_mwh: Series[float] = pa.Field(ge=0)
    e_grid_mwh: Series[float] = pa.Field(ge=0)
    carbon_tco2: Series[float] = pa.Field(ge=0)
    water_onsite_l: Series[float] = pa.Field(ge=0)       # scope-1
    water_grid_l: Series[float] = pa.Field(ge=0)         # scope-2
    water_phys_l: Series[float] = pa.Field(ge=0)         # physical total (reported FIRST)
    water_scarcity_l_eq: Series[float] = pa.Field(ge=0)  # AWARE-weighted (SEPARATE)
    inference_share: Series[float] = pa.Field(ge=0, le=1)

    @pa.dataframe_check
    def atomic_unit_is_facility_month(cls, df: pd.DataFrame) -> bool:
        """The load-bearing contract: exactly one row per facility-month."""
        return not df.duplicated(subset=["facility_id", "date"]).any()

    @pa.dataframe_check
    def water_phys_is_sum_of_scopes(cls, df: pd.DataFrame) -> bool:
        import numpy as np
        return np.allclose(df["water_phys_l"], df["water_onsite_l"] + df["water_grid_l"], rtol=1e-6)

    class Config:
        coerce = True

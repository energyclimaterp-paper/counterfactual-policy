"""L0 — GEM Global Integrated Power Tracker: power plants with location, type, capacity.

Used for (a) scope-2 scarcity at the basins where electricity is GENERATED (geo/
generation_basins.py) and (b) the Q1 candidate grid + grid fossil share (decisions/
siting.py). The 23 MB workbook is slow to read, so the India operating subset is cached
next to it as parquet.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from dcfootprint.io.facilities import _repo_root

_COLS = {"Type": "type", "Plant / Project name": "plant", "Capacity (MW)": "capacity_mw",
         "Status": "status", "Latitude": "latitude", "Longitude": "longitude",
         "Subnational unit (state, province)": "state"}
_FOSSIL = {"coal", "oil/gas"}


def load_plants(country: str = "India", status: str = "operating", path: str | Path | None = None) -> pd.DataFrame:
    """[type, plant, capacity_mw, status, latitude, longitude, state, fossil] for one country."""
    import yaml
    root = _repo_root()
    if path is None:
        params = yaml.safe_load((root / "dcfootprint" / "config" / "parameters.yaml").read_text(encoding="utf-8"))
        path = root / params["grid"]["gem_path"]
    path = Path(path)
    cache = path.with_name(f"gem_{country.lower()}_{status}.parquet")
    if cache.exists() and cache.stat().st_mtime >= path.stat().st_mtime:
        return pd.read_parquet(cache)
    g = pd.read_excel(path, sheet_name="Power facilities", usecols=["Country/area", *_COLS])
    g = g[(g["Country/area"] == country) & (g["Status"] == status)].rename(columns=_COLS)
    g = g.drop(columns="Country/area")
    g["capacity_mw"] = pd.to_numeric(g["capacity_mw"], errors="coerce")
    g["latitude"] = pd.to_numeric(g["latitude"], errors="coerce")
    g["longitude"] = pd.to_numeric(g["longitude"], errors="coerce")
    g = g.dropna(subset=["capacity_mw", "latitude", "longitude"]).reset_index(drop=True)
    g["fossil"] = g["type"].isin(_FOSSIL)
    g.to_parquet(cache)
    return g


def state_fossil_share(plants: pd.DataFrame) -> pd.DataFrame:
    """[state, fossil_share, capacity_mw] — operating fossil capacity / total capacity."""
    s = plants.groupby("state").apply(
        lambda d: pd.Series({"fossil_share": d.loc[d["fossil"], "capacity_mw"].sum() / d["capacity_mw"].sum(),
                             "capacity_mw": d["capacity_mw"].sum()}), include_groups=False)
    return s.reset_index()


if __name__ == "__main__":
    p = load_plants()
    print(f"India operating plants: {len(p)}  ({p['capacity_mw'].sum()/1000:,.0f} GW)")
    print(p.groupby("type")["capacity_mw"].sum().div(1000).round(1).to_string())
    print(state_fossil_share(p).sort_values("capacity_mw", ascending=False).head(10).round(2).to_string(index=False))

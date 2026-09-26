"""L0 — Ember India monthly. Two products for the account:
  * national monthly FUEL SHARES -> scope-2 EWIF (via Macknick coeffs).
  * national monthly CO2 INTENSITY (generation-based) -> the *flagged sensitivity*
    carbon source (the primary India carbon is CEA national-annual; see io/cea.py).

Why national, not per-state: India is a synchronous national grid — a datacentre
consumes the pooled national mix, not its own state's generation (config R2). Shares
are ratio-based, so aggregating across whatever rows Ember provides is scale-safe.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

from dcfootprint.io.facilities import _repo_root
from dcfootprint.settings import params as _cfg_params

# Ember atomic-fuel Variable names that map 1:1 to parameters.yaml ewif_coeff keys.
_FUELS = ["Coal", "Gas", "Nuclear", "Bioenergy", "Hydro", "Solar", "Wind",
          "Other Fossil", "Other Renewables"]


def load_india_raw(path: str | Path | None = None) -> pd.DataFrame:
    path = Path(path) if path else _repo_root() / "data" / "ember" / "india_monthly_full_release_long_format.csv"
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["Date"])
    return df


def national_monthly_fuel_shares(raw: pd.DataFrame) -> pd.DataFrame:
    """[date, fuel, share] — national generation share per fuel per month.
    Shares are ratios, so summing across state (and any national) rows is safe."""
    gen = raw[(raw["Category"] == "Electricity generation")
              & (raw["Variable"].isin(_FUELS))
              & (raw["Unit"] == "GWh")].copy()
    national = gen[gen["State"] == "India Total"]           # exact national row
    if national.empty:                                       # fallback: sum states (skip 'total' to avoid double-count)
        national = gen[gen["State type"].isin(["state", "Union territory"])]
    nat = (national.groupby(["date", "Variable"], as_index=False)["Value"].sum()
              .rename(columns={"Variable": "fuel", "Value": "gwh"}))
    nat["gwh"] = nat["gwh"].clip(lower=0)
    tot = nat.groupby("date")["gwh"].transform("sum")
    nat["share"] = (nat["gwh"] / tot).fillna(0.0)
    return nat[["date", "fuel", "share"]]


def national_monthly_ci(raw: pd.DataFrame) -> pd.DataFrame:
    """[date, ci_gco2_per_kwh] — generation-based national CI (flagged sensitivity)."""
    ci = raw[(raw["Variable"] == "CO2 intensity") & (raw["Unit"] == "gCO2/kWh")].copy()
    national = ci[ci["State"] == "India Total"]
    if national.empty:
        national = ci
    return (national.groupby("date", as_index=False)["Value"].mean()
              .rename(columns={"Value": "ci_gco2_per_kwh"}))


def monthly_ewif_l_per_mwh(shares: pd.DataFrame, ewif_coeff: dict[str, float]) -> pd.DataFrame:
    """[month(1-12), ewif_l_per_mwh] — climatological monthly scope-2 water intensity,
    averaged across available years (the account is a representative-year panel)."""
    s = shares.copy()
    s["coeff"] = s["fuel"].map(ewif_coeff)
    missing = sorted(s.loc[s["coeff"].isna(), "fuel"].unique())
    if missing:
        raise KeyError(f"Fuels with no EWIF coefficient (add to parameters.yaml): {missing}")
    s["contrib"] = s["share"] * s["coeff"]
    per_date = s.groupby("date", as_index=False)["contrib"].sum().rename(columns={"contrib": "ewif"})
    per_date["month"] = per_date["date"].dt.month
    return (per_date.groupby("month", as_index=False)["ewif"].mean()
                    .rename(columns={"ewif": "ewif_l_per_mwh"}))


# --------------------------------------------------------------------------- #
# Zone-month tables (zone = Ember state, or the India total for every state)
# --------------------------------------------------------------------------- #
_NATIONAL = "India Total"
_NOT_A_STATE = {_NATIONAL, "Others"}


def zone_month_ci(raw: pd.DataFrame, year: int, zone: str = "state") -> pd.DataFrame:
    """[zone_id, month, ci_gco2_per_kwh, ci_source] for `year`.
    zone='state': Ember state generation CI (generation-based; R2 caveat), with the national
    value filling any state-month Ember leaves blank. zone='national': India Total for all."""
    ci = raw[(raw["Variable"] == "CO2 intensity") & (raw["Unit"] == "gCO2/kWh")
             & (raw["date"].dt.year == year)].copy()
    ci["month"] = ci["date"].dt.month
    nat = (ci[ci["State"] == _NATIONAL].groupby("month")["Value"].mean()
           .rename("ci_national"))
    states = sorted(s for s in raw["State"].dropna().unique() if s not in _NOT_A_STATE)
    grid = pd.MultiIndex.from_product([states, range(1, 13)], names=["zone_id", "month"]).to_frame(index=False)
    grid = grid.merge(nat, on="month", how="left")
    if zone == "state":
        st = (ci[ci["State"].isin(states)].groupby(["State", "month"])["Value"].mean()
              .rename("ci_state").reset_index().rename(columns={"State": "zone_id"}))
        grid = grid.merge(st, on=["zone_id", "month"], how="left")
        grid["ci_gco2_per_kwh"] = grid["ci_state"].fillna(grid["ci_national"])
        grid["ci_source"] = grid["ci_state"].notna().map({True: "ember_state", False: "ember_national_fill"})
    elif zone == "national":
        grid["ci_gco2_per_kwh"] = grid["ci_national"]
        grid["ci_source"] = "ember_national"
    else:
        raise ValueError(f"unknown grid zone {zone!r} (state | national)")
    from dcfootprint.validation import schemas
    return schemas.EmberZoneMonth.validate(grid[["zone_id", "month", "ci_gco2_per_kwh", "ci_source"]])


def zone_month_fuel_shares(raw: pd.DataFrame, year: int, zone: str = "state") -> pd.DataFrame:
    """[zone_id, month, fuel, share] generation shares for `year`; a state-month with no
    generation in Ember takes the national shares (flagged via share_source)."""
    gen = raw[(raw["Category"] == "Electricity generation") & (raw["Variable"].isin(_FUELS))
              & (raw["Unit"] == "GWh") & (raw["date"].dt.year == year)].copy()
    gen["month"] = gen["date"].dt.month
    gen["Value"] = gen["Value"].clip(lower=0)

    def _shares(df, key):
        g = df.groupby([key, "month", "Variable"], as_index=False)["Value"].sum()
        g["share"] = g["Value"] / g.groupby([key, "month"])["Value"].transform("sum")
        return g.rename(columns={key: "zone_id", "Variable": "fuel"})[["zone_id", "month", "fuel", "share"]]

    nat = _shares(gen[gen["State"] == _NATIONAL], "State").drop(columns="zone_id")
    states = sorted(s for s in raw["State"].dropna().unique() if s not in _NOT_A_STATE)
    if zone == "national":
        out = pd.concat([nat.assign(zone_id=s) for s in states], ignore_index=True)
        out["share_source"] = "ember_national"
        from dcfootprint.validation import schemas
        return schemas.FuelShares.validate(out)
    st = _shares(gen[gen["State"].isin(states)], "State").dropna(subset=["share"])
    have = set(map(tuple, st[["zone_id", "month"]].drop_duplicates().values))
    missing = [(s, m) for s in states for m in range(1, 13) if (s, m) not in have]
    fill = pd.concat([nat[nat["month"] == m].assign(zone_id=s) for s, m in missing]
                     or [nat.iloc[0:0].assign(zone_id="")], ignore_index=True)
    st["share_source"] = "ember_state"
    fill["share_source"] = "ember_national_fill"
    from dcfootprint.validation import schemas
    return schemas.FuelShares.validate(
        pd.concat([st, fill], ignore_index=True)[["zone_id", "month", "fuel", "share", "share_source"]])


if __name__ == "__main__":
    raw = load_india_raw()
    print("States:", sorted(map(str, raw["State"].dropna().unique()))[:30])
    print("State type:", raw["State type"].dropna().unique().tolist())
    shares = national_monthly_fuel_shares(raw)
    latest = shares[shares["date"] == shares["date"].max()].set_index("fuel")["share"].round(3)
    print(f"\nfuel shares @ {shares['date'].max().date()} (sum={latest.sum():.2f}):\n{latest.to_dict()}")
    params = _cfg_params()
    ewif = monthly_ewif_l_per_mwh(shares, params["water_grid"]["ewif_coeff_L_per_MWh"])
    print("\nmonthly EWIF (L/MWh):\n", ewif.to_string(index=False))
    ci = national_monthly_ci(raw)
    print(f"\nnational CI (gen-proxy) range: {ci['ci_gco2_per_kwh'].min():.0f}-{ci['ci_gco2_per_kwh'].max():.0f} gCO2/kWh")

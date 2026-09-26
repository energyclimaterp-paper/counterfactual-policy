"""L4 — counterfactual policy levers (the working headline / G6).

Each lever is a *parameter transform* on the present account; we recompute the
affected carbon/water and report the delta vs baseline. Deterministic scenario
arithmetic — NOT workload routing (kill-list). "Which lever pays" is ranked by the
primary metric: scarcity-weighted water saved per year.

Levers (parameters from config/parameters.yaml):
  coastal_seawater_siting : WUE -> ~0.1 for coastal facilities (scope-1 only)
  zero_liquid_discharge   : W_phys -> W_phys*(1-recycle), recycle~0.92
  efficiency_standard     : PUE<=1.3 (carbon + scope-2 water down) & WUE<=0.7 (scope-1 down)
  mandatory_disclosure    : transparency lever — reveals the currently-unreported footprint
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from dcfootprint.io.facilities import _repo_root

# coastal DC hubs (seawater/WSAC eligible) — city-level proxy, flagged
_COASTAL = {"mumbai", "navi mumbai", "chennai", "visakhapatnam", "kolkata", "kochi", "mangalore", "surat"}
_BASELINE_DISCLOSURE = 0.30   # <1/3 of operators measure water (Mytton / water-governance)


def _load_account() -> pd.DataFrame:
    p = _repo_root() / "dcfootprint" / "outputs" / "account_facility_month.parquet"
    if p.exists():
        return pd.read_parquet(p)
    from dcfootprint.account import build
    return build.facility_month_account()


def _backout(acct: pd.DataFrame) -> pd.DataFrame:
    """Recover per-row PUE, WUE, EWIF, EF from the account so levers need no re-load."""
    df = acct.copy()
    df["pue"] = df["e_grid_mwh"] / df["e_it_mwh"]
    df["wue_l_per_kwh"] = df["water_onsite_l"] / (df["e_it_mwh"] * 1000.0)
    df["ewif_l_per_mwh"] = np.where(df["e_grid_mwh"] > 0, df["water_grid_l"] / df["e_grid_mwh"], 0.0)
    df["ef_tco2_per_mwh"] = np.where(df["e_grid_mwh"] > 0, df["carbon_tco2"] / df["e_grid_mwh"], 0.0)
    return df


def _totals(dphys_l: pd.Series, dcarbon_t: pd.Series, cf: pd.Series) -> dict:
    """Aggregate facility-month deltas to annual totals (physical m3, scarcity m3-eq, tCO2)."""
    return {
        "water_phys_saved_m3_yr": float(dphys_l.clip(lower=0).sum() / 1000.0),
        "water_scarcity_saved_m3eq_yr": float((dphys_l.clip(lower=0) * cf).sum() / 1000.0),
        "carbon_saved_tco2_yr": float(dcarbon_t.clip(lower=0).sum()),
    }


def rank_lever_savings(config: dict | None = None) -> pd.DataFrame:
    params = yaml.safe_load((_repo_root() / "dcfootprint" / "config" / "parameters.yaml").read_text(encoding="utf-8"))
    lv = params["levers"]
    a = _backout(_load_account())
    rows = []

    # --- coastal seawater siting: scope-1 WUE -> new_wue for coastal facilities ---
    new_wue = float(lv["coastal_seawater_siting"]["new_wue"])
    coastal = a["city"].fillna("").str.lower().isin(_COASTAL)
    d_onsite = np.where(coastal & (a["wue_l_per_kwh"] > new_wue),
                        (a["wue_l_per_kwh"] - new_wue) * a["e_it_mwh"] * 1000.0, 0.0)
    rows.append({"lever": "coastal_seawater_siting", "type": "reduction",
                 **_totals(pd.Series(d_onsite), pd.Series(0.0, index=a.index), a["cf"]),
                 "note": f"WUE->{new_wue} at coastal hubs (scope-1); {int(coastal.sum()/12)} facilities eligible"})

    # --- zero-liquid-discharge: W_phys * recycle recovered ---
    rec = float(lv["zero_liquid_discharge"]["recycle_fraction"])
    d_phys = a["water_phys_l"] * rec
    rows.append({"lever": "zero_liquid_discharge", "type": "reduction",
                 **_totals(d_phys, pd.Series(0.0, index=a.index), a["cf"]),
                 "note": f"recycle {rec:.0%} of physical water (all facilities)"})

    # --- efficiency standard: PUE<=cap (carbon + scope-2 water) & WUE<=cap (scope-1) ---
    pue_cap, wue_cap = float(lv["efficiency_standard"]["pue_cap"]), float(lv["efficiency_standard"]["wue_cap"])
    new_pue = np.minimum(a["pue"], pue_cap)
    d_egrid = (a["e_it_mwh"] * a["pue"]) - (a["e_it_mwh"] * new_pue)          # MWh grid avoided
    d_carbon = d_egrid * a["ef_tco2_per_mwh"]
    d_wgrid = d_egrid * a["ewif_l_per_mwh"]                                   # scope-2 water avoided
    d_wonsite = np.where(a["wue_l_per_kwh"] > wue_cap,
                         (a["wue_l_per_kwh"] - wue_cap) * a["e_it_mwh"] * 1000.0, 0.0)
    d_eff_phys = pd.Series(d_wgrid.values + d_wonsite, index=a.index)
    rows.append({"lever": "efficiency_standard", "type": "reduction",
                 **_totals(d_eff_phys, d_carbon, a["cf"]),
                 "note": f"PUE<={pue_cap}, WUE<={wue_cap} (water+carbon; liquid-cooling tradeoff bounded by caps)"})

    # --- mandatory disclosure: transparency lever (reveals unreported footprint) ---
    revealed = float((a["water_phys_l"].sum() / 1000.0) * (1 - _BASELINE_DISCLOSURE))
    rows.append({"lever": "mandatory_disclosure", "type": "transparency",
                 "water_phys_saved_m3_yr": 0.0, "water_scarcity_saved_m3eq_yr": 0.0, "carbon_saved_tco2_yr": 0.0,
                 "note": f"reveals ~{revealed:,.0f} m3/yr currently unreported (baseline disclosure ~{_BASELINE_DISCLOSURE:.0%})"})

    out = pd.DataFrame(rows)
    base_scarcity = float((a["water_scarcity_l_eq"].sum()) / 1000.0)
    out["pct_of_scarcity_baseline"] = (out["water_scarcity_saved_m3eq_yr"] / base_scarcity * 100).round(1)
    return out.sort_values("water_scarcity_saved_m3eq_yr", ascending=False).reset_index(drop=True)


if __name__ == "__main__":
    res = rank_lever_savings()
    resdir = _repo_root() / "dcfootprint" / "results"
    resdir.mkdir(parents=True, exist_ok=True)
    res.to_csv(resdir / "lever_savings.csv", index=False)
    show = res[["lever", "type", "water_scarcity_saved_m3eq_yr", "water_phys_saved_m3_yr",
                "carbon_saved_tco2_yr", "pct_of_scarcity_baseline"]]
    print("WHICH LEVER PAYS (ranked by scarcity-weighted water saved):\n")
    print(show.to_string(index=False))
    print("\nnotes:")
    for _, r in res.iterrows():
        print(f"  - {r['lever']}: {r['note']}")
    print(f"\nwrote {resdir/'lever_savings.csv'}")

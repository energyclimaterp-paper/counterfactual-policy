"""L2 build — assemble the facility-month account (product ②, the dataset).

Wires the layers on real data:
  energy (E_IT, E_grid)  ->  carbon (CEA national EF)
                          ->  water: scope-1 (WUE*E_IT) + scope-2 (EWIF(month)*E_grid)
                          ->  scarcity (W_phys * AWARE_CF(basin, month))
                          ->  inference scoping scalar (column)
Output validated against schemas.FacilityMonthAccount, then written; a small,
git-committed results summary is written to dcfootprint/results/.

Present-account scope: Operational, costed (capacity known), basin-resolved facilities.
Pipeline (announced/under-construction) is held for the L3 projection, not the present account.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

from dcfootprint.io.facilities import _repo_root
from dcfootprint.io import cea, ember
from dcfootprint.account import energy as energy_mod, carbon as carbon_mod

ACCOUNT_YEAR = 2024
_CONTRACT_COLS = ["facility_id", "date", "region", "e_it_mwh", "e_grid_mwh", "carbon_tco2",
                  "water_onsite_l", "water_grid_l", "water_phys_l", "water_scarcity_l_eq", "inference_share"]


def load_params() -> dict:
    return yaml.safe_load((_repo_root() / "dcfootprint" / "config" / "parameters.yaml").read_text(encoding="utf-8"))


def _wue_by_facility_id(fac: pd.DataFrame, params: dict) -> dict:
    wcfg = params["water_onsite"]
    default = float(wcfg["wue_default"]["default"])
    byop = {k.lower(): v for k, v in wcfg.get("wue_by_operator", {}).items()}
    wue = pd.Series(default, index=fac.index, dtype=float)
    opl = fac["operator"].fillna("").str.lower()
    for op, val in byop.items():
        wue.loc[opl.str.contains(op, regex=False)] = float(val)
    return dict(zip(fac["facility_id"], wue))


def facility_month_account(config: dict | None = None) -> pd.DataFrame:
    params = load_params()
    root = _repo_root()

    fac = pd.read_parquet(root / "dcfootprint" / "outputs" / "interim" / "facilities_geocoded.parquet")
    acct_fac = fac[(fac["status"] == "Operational") & fac["capacity_mw"].notna() & fac["basin_id"].notna()].copy()
    n_op_total = int((fac["status"] == "Operational").sum())

    ef = cea.india_grid_ef()["ef_tco2_per_mwh"]
    raw = ember.load_india_raw()
    ewif = ember.monthly_ewif_l_per_mwh(ember.national_monthly_fuel_shares(raw),
                                        params["water_grid"]["ewif_coeff_L_per_MWh"])
    cf = pd.read_parquet(root / "dcfootprint" / "outputs" / "interim" / "basin_cf_monthly.parquet")

    e = energy_mod.energy_account(acct_fac, params, ACCOUNT_YEAR)
    e = carbon_mod.carbon_account(e, ef)

    wue_by_fid = _wue_by_facility_id(acct_fac, params)
    e["wue_l_per_kwh"] = e["facility_id"].map(wue_by_fid)
    e["water_onsite_l"] = e["wue_l_per_kwh"] * e["e_it_mwh"] * 1000.0          # scope-1 (MWh->kWh)
    e = e.merge(ewif, on="month", how="left")
    e["water_grid_l"] = e["ewif_l_per_mwh"] * e["e_grid_mwh"]                   # scope-2
    e["water_phys_l"] = e["water_onsite_l"] + e["water_grid_l"]

    e["basin_id"] = e["basin_id"].astype("int64")     # all non-null here; match cf dtype exactly
    cf["basin_id"] = cf["basin_id"].astype("int64")
    e = e.merge(cf, on=["basin_id", "month"], how="left")
    missing_cf = int(e["cf"].isna().sum())
    e = e[e["cf"].notna()].copy()
    # scope-1 scarcity is rigorous at the facility basin; scope-2 (grid) is weighted here at the
    # same basin as a bounded simplification (config R3: true scope-2 = grid-region avg) -> flagged.
    e["water_scarcity_l_eq"] = e["water_phys_l"] * e["cf"]

    e["inference_share"] = float(params["inference"]["sectoral_share"]["default"])
    e["date"] = e["month"].map(lambda m: pd.Timestamp(ACCOUNT_YEAR, int(m), 1))
    e["region"] = "India"

    keep = _CONTRACT_COLS + ["state", "basin_id", "facility_type", "capacity_mw", "operator", "city", "cf"]
    account = e[keep].reset_index(drop=True)

    from dcfootprint.validation import schemas
    schemas.FacilityMonthAccount.validate(account[_CONTRACT_COLS])   # contract enforced

    account.attrs["meta"] = {
        "account_year": ACCOUNT_YEAR, "ef_tco2_per_mwh": round(ef, 4),
        "n_facilities": int(acct_fac["facility_id"].nunique()), "n_operational_total": n_op_total,
        "dropped_facility_months_no_cf": missing_cf,
    }
    return account


def _write_results(account: pd.DataFrame) -> Path:
    """Small, git-committed summary artefacts in dcfootprint/results/."""
    meta = account.attrs["meta"]
    ann = account.groupby(["facility_id", "operator", "city", "state", "basin_id"], as_index=False).agg(
        carbon_tco2_yr=("carbon_tco2", "sum"),
        water_phys_m3_yr=("water_phys_l", lambda s: s.sum() / 1000.0),
        water_scarcity_m3eq_yr=("water_scarcity_l_eq", lambda s: s.sum() / 1000.0),
        capacity_mw=("capacity_mw", "first"),
    ).sort_values("water_scarcity_m3eq_yr", ascending=False)

    resdir = _repo_root() / "dcfootprint" / "results"
    resdir.mkdir(parents=True, exist_ok=True)
    ann.to_csv(resdir / "india_account_summary.csv", index=False)

    inf = account["inference_share"].iloc[0]
    tot_c = ann["carbon_tco2_yr"].sum()
    tot_wp = ann["water_phys_m3_yr"].sum()
    tot_ws = ann["water_scarcity_m3eq_yr"].sum()
    by_state = ann.groupby("state")["water_scarcity_m3eq_yr"].sum().sort_values(ascending=False)

    md = [
        "# India AI-datacenter account — v1 results (present, operational)\n",
        f"*Generated by `dcfootprint.account.build` on real data. Account year {meta['account_year']}; "
        f"CEA grid EF {meta['ef_tco2_per_mwh']} tCO2/MWh (incl. RES).*\n",
        f"- **Facilities in account:** {meta['n_facilities']} (operational, costed, basin-resolved) "
        f"of {meta['n_operational_total']} operational total — coverage gap = un-costed / un-geocoded.",
        f"- **Total carbon:** {tot_c:,.0f} tCO2/yr  (inference-attributed ~{tot_c*inf:,.0f} tCO2/yr at {inf:.0%})",
        f"- **Total physical water:** {tot_wp:,.0f} m3/yr  (scope-1 + scope-2)",
        f"- **Total scarcity-weighted water:** {tot_ws:,.0f} m3-eq/yr  *(AWARE-weighted; the primary metric)*\n",
        "## Scarcity-weighted water by state (top 6)\n",
        by_state.head(6).apply(lambda v: f"{v:,.0f} m3-eq/yr").to_string(),
        "\n\n## Top 8 facilities by scarcity-weighted water\n",
        ann.head(8)[["operator", "city", "state", "capacity_mw", "water_scarcity_m3eq_yr"]].to_string(index=False),
        "\n\n### Caveats (v1)\n",
        "- util/PUE are modeled scalars (R1) -> absolutes are indicative; lead with spatial/relative results.\n"
        "- scope-2 water scarcity weighted at the facility basin (bounded simplification; true scope-2 = grid-region avg, R3).\n"
        "- coordinates are ATLAS city-centroids (facilities in one city share a basin); precise geocode pending.\n"
        "- carbon is national-annual (CEA); India sub-national signal rides on water, by design.\n",
    ]
    (resdir / "RESULTS.md").write_text("\n".join(md), encoding="utf-8")
    return resdir


if __name__ == "__main__":
    account = facility_month_account()
    meta = account.attrs["meta"]
    out = _repo_root() / "dcfootprint" / "outputs" / "account_facility_month.parquet"
    out.parent.mkdir(parents=True, exist_ok=True)
    account.to_parquet(out)
    resdir = _write_results(account)

    ann_c = account["carbon_tco2"].sum()
    ann_wp = account["water_phys_l"].sum() / 1000.0
    ann_ws = account["water_scarcity_l_eq"].sum() / 1000.0
    print(f"ACCOUNT rows: {len(account)}  facilities: {meta['n_facilities']}  months: {account['date'].nunique()}")
    print(f"meta: {meta}")
    print(f"TOTAL carbon:  {ann_c:,.0f} tCO2/yr")
    print(f"TOTAL water:   {ann_wp:,.0f} m3/yr physical | {ann_ws:,.0f} m3-eq/yr scarcity-weighted")
    print(f"contract: PASS (FacilityMonthAccount)  | wrote {out.name} + results/RESULTS.md + india_account_summary.csv")

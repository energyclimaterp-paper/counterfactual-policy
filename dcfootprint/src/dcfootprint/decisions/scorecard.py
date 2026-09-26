"""L7 / Q2 — existing-DC environmental scorecard.

Per facility: annual carbon, physical water, scarcity-weighted water, each as a
RELATIVE PERCENTILE within India (robust to the util/PUE scalar, red-team R1) plus
the absolute value. A harm flag fires when scarcity-weighted water is in the top
quartile AND the facility's basin is high-scarcity. Flagged facilities get ranked
levers (from the counterfactual layer).
"""
from __future__ import annotations

import pandas as pd


def scorecard(account: pd.DataFrame) -> pd.DataFrame:
    ann = account.groupby(["facility_id", "operator", "city", "state", "basin_id"], as_index=False).agg(
        carbon_tco2_yr=("carbon_tco2", "sum"),
        water_phys_m3_yr=("water_phys_l", lambda s: s.sum() / 1000.0),
        scarcity_m3eq_yr=("water_scarcity_l_eq", lambda s: s.sum() / 1000.0),
        mean_cf=("cf", "mean"),
        capacity_mw=("capacity_mw", "first"),
    )
    for col, name in [("carbon_tco2_yr", "carbon_pctile"),
                      ("water_phys_m3_yr", "water_pctile"),
                      ("scarcity_m3eq_yr", "scarcity_pctile")]:
        ann[name] = (ann[col].rank(pct=True) * 100).round(0)

    top_q = ann["scarcity_m3eq_yr"].quantile(0.75)
    high_cf = ann["mean_cf"].quantile(0.60)
    ann["harm_flag"] = (ann["scarcity_m3eq_yr"] >= top_q) & (ann["mean_cf"] >= high_cf)
    ann["verdict"] = pd.cut(ann["scarcity_pctile"], [-1, 50, 75, 101],
                            labels=["better than peers", "typical", "worse than peers"])
    # recommended lever for flagged facilities (coastal->seawater else ZLD)
    coastal = ann["city"].fillna("").str.lower().isin(
        {"mumbai", "navi mumbai", "chennai", "visakhapatnam", "kolkata", "kochi", "surat"})
    ann["recommended_lever"] = "none"
    ann.loc[ann["harm_flag"] & coastal, "recommended_lever"] = "coastal_seawater_siting"
    ann.loc[ann["harm_flag"] & ~coastal, "recommended_lever"] = "zero_liquid_discharge"
    return ann.sort_values("scarcity_m3eq_yr", ascending=False).reset_index(drop=True)


if __name__ == "__main__":
    from dcfootprint.io.facilities import _repo_root
    acct = pd.read_parquet(_repo_root() / "dcfootprint" / "outputs" / "account_facility_month.parquet")
    sc = scorecard(acct)
    print(f"facilities scored: {len(sc)} | harm-flagged: {int(sc['harm_flag'].sum())}")
    print(sc.head(8)[["operator", "city", "state", "scarcity_pctile", "harm_flag", "recommended_lever"]].to_string(index=False))

"""L7 / Q1 — siting: rank candidate (state x basin) regions for a NEW datacenter.

Candidate grid = every (state x AWARE basin) cell holding >=1 operating GEM power plant
(existing grid infrastructure), plus every cell that already holds a datacenter — so the
tool can point to unoccupied regions, not only "least bad among where we already are".

A hypothetical facility of size S (parameters.yaml siting.*) is scored per cell on four
criteria, all lower-is-better:
  new_scarcity_m3eq   its scarcity-weighted water: scope-1 x CF(basin, m) +
                      scope-2 x generation-basin CF of the state's grid (sewif)
  new_carbon_tco2     its carbon at the state's 2024 monthly CI
  basin_pressure      (existing DC scope-1 water in the basin + its own) / basin budget
                      (budget ~ area/CF, the same decoupled R_hat as Q3 routing)
  grid_fossil_share   operating fossil share of the state's GEM capacity
Legal screen (policy/gap.region_effects): bans exclude a cell; ZLD / renewable-share /
PUE mandates change the new facility's footprint. Ranked with AND without legal effects.

Weights are Dirichlet-sampled; cells are ranked by MINIMAX REGRET (worst-case gap to the
best cell across weightings), with mean rank and a p10-p90 rank band as the stability
check. Output = regions with reasons, not plots (land, fibre and interconnection queues
are not in the data). 2030/2050 scenarios (Aqueduct future, CI path) are not yet included.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import yaml

from dcfootprint.io.facilities import _repo_root
from dcfootprint.account.energy import month_hours

CRITERIA = ["new_scarcity_m3eq", "new_carbon_tco2", "basin_pressure", "grid_fossil_share"]


def _cfg() -> dict:
    return yaml.safe_load((_repo_root() / "dcfootprint" / "config" / "parameters.yaml").read_text(encoding="utf-8"))


def candidate_cells(account: pd.DataFrame, g: dict) -> pd.DataFrame:
    p = g["plants"].dropna(subset=["state"])
    grid_cells = p.groupby(["state", "basin_id"], as_index=False).agg(n_plants=("plant", "size"))
    dc = account.groupby(["state", "basin_id"], as_index=False).agg(n_existing_dc=("facility_id", "nunique"))
    dc["basin_id"] = dc["basin_id"].astype("int64")
    cells = grid_cells.merge(dc, on=["state", "basin_id"], how="outer").fillna({"n_plants": 0, "n_existing_dc": 0})
    # guard against GEM state/coordinate mismatches (e.g. a plant tagged Karnataka at 26.8N 77.1E)
    # until GADM gives state from coordinates: a grid cell needs >= min_plants_per_cell plants
    min_p = int(_cfg()["siting"].get("min_plants_per_cell", 2))
    cells = cells[(cells["n_plants"] >= min_p) | (cells["n_existing_dc"] > 0)]
    cells = cells[cells["state"].isin(set(g["ci"]["zone_id"]))]             # needs a grid CI
    return cells.astype({"basin_id": "int64", "n_plants": int, "n_existing_dc": int})


def score_cells(account: pd.DataFrame, legal: bool = True) -> pd.DataFrame:
    from dcfootprint.account.build import grid_tables
    from dcfootprint.io.gem import state_fossil_share
    from dcfootprint.policy.gap import region_effects
    from dcfootprint.project.recharge import basin_budgets
    cfg = _cfg()
    sc, gcfg = cfg["siting"], cfg["grid"]
    g = grid_tables(gcfg["zone"], int(gcfg["account_year"]))
    cells = candidate_cells(account, g)

    t = sc["new_facility_type"]
    S = float(sc["new_facility_mw"])
    util = cfg["energy"]["utilisation"]["by_facility_type"][t]["default"]
    pue0 = cfg["energy"]["pue"]["by_facility_type"][t]["default"]
    wue = float(cfg["water_onsite"]["wue_default"]["default"])
    hrs = month_hours(int(gcfg["account_year"]))
    e_it = hrs.assign(e_it_mwh=S * util * hrs["hours"])[["month", "e_it_mwh"]]          # MWh-IT per month

    cf = g["basin_cf"][g["basin_cf"]["basin_id"].isin(cells["basin_id"])]
    s1 = (cf.merge(e_it, on="month").assign(v=lambda d: d["e_it_mwh"] * 1000 * wue * d["cf"])
          .groupby("basin_id")["v"].sum().rename("s1_l"))                              # before legal
    cfm = cf.groupby("basin_id")["cf"].mean().rename("cf_mean")
    zone = (g["grid_water"].merge(g["ci"], on=["zone_id", "month"]).merge(e_it, on="month")
            .assign(s2=lambda d: d["e_it_mwh"] * d["sewif_l_eq_per_mwh"],
                    c=lambda d: d["e_it_mwh"] * d["ci_gco2_per_kwh"] / 1000)
            .groupby("zone_id").agg(s2_per_pue=("s2", "sum"), c_per_pue=("c", "sum"),
                                    ci_mean=("ci_gco2_per_kwh", "mean")))
    cells = (cells.merge(s1, left_on="basin_id", right_index=True, how="left")
             .merge(cfm, left_on="basin_id", right_index=True, how="left")
             .merge(zone, left_on="state", right_index=True, how="left")
             .merge(state_fossil_share(g["plants"])[["state", "fossil_share"]], on="state", how="left")
             .dropna(subset=["s1_l", "s2_per_pue"]))
    cells = cells.rename(columns={"fossil_share": "grid_fossil_share"})

    # legal effects on the NEW facility (or exclusion)
    cells["legal_flags"], cells["excluded"] = "", False
    zld = np.zeros(len(cells)); re = np.zeros(len(cells)); pue = np.full(len(cells), pue0)
    if legal:
        for i, st in enumerate(cells["state"].values):
            eff = region_effects(st)
            flags = []
            if "ban_new_above_mw" in eff and S >= eff["ban_new_above_mw"]:
                cells.iloc[i, cells.columns.get_loc("excluded")] = True; flags.append("ban")
            if "zld_mandate" in eff:
                zld[i] = eff["zld_mandate"]; flags.append("zld")
            if "re_share_min" in eff:
                re[i] = eff["re_share_min"]; flags.append(f"re>={eff['re_share_min']:.0%}")
            if "pue_cap_new" in eff:
                pue[i] = min(pue0, eff["pue_cap_new"]); flags.append("pue_cap")
            cells.iloc[i, cells.columns.get_loc("legal_flags")] = ",".join(flags)
    cells["new_scarcity_m3eq"] = (cells["s1_l"] * (1 - zld) + cells["s2_per_pue"] * pue) / 1000.0
    cells["new_carbon_tco2"] = cells["c_per_pue"] * pue * (1 - re)
    new_onsite_l = float(e_it["e_it_mwh"].sum() * 1000 * wue) * (1 - zld)

    # marginal basin pressure against the decoupled budget (kappa cancels under min-max)
    bud = basin_budgets(cells["basin_id"].unique(), 1.0).groupby("basin_id")["budget_l"].sum()
    exist = account.groupby(account["basin_id"].astype("int64"))["water_onsite_l"].sum()
    cells["basin_pressure"] = ((cells["basin_id"].map(exist).fillna(0).values + new_onsite_l)
                               / cells["basin_id"].map(bud).values)
    cells["basin_pressure"] = cells["basin_pressure"] / cells["basin_pressure"].median()   # index, median = 1

    # R2 guard: a state's Ember CI is its OWN generation; a small grid that imports most of its
    # power (e.g. hydro-only NE states) shows a CI the datacenter would not actually see.
    from dcfootprint.io import ember
    raw = ember.load_india_raw()
    gen = raw[(raw["Category"] == "Electricity generation") & (raw["Unit"] == "GWh")
              & (raw["Variable"].isin(ember._FUELS)) & (raw["date"].dt.year == int(gcfg["account_year"]))]
    twh = gen.groupby("State")["Value"].sum() / 1000.0
    cells["state_generation_twh"] = cells["state"].map(twh).round(2)
    cells["small_grid"] = cells["state_generation_twh"] < float(sc.get("small_grid_twh", 10))
    return cells.drop(columns=["s1_l", "s2_per_pue", "c_per_pue"]).reset_index(drop=True)


def _minimax(cells: pd.DataFrame, n: int, seed: int) -> pd.DataFrame:
    c = cells[~cells["excluded"]].copy()
    X = c[CRITERIA].values.astype(float)
    rng_ = X.max(0) - X.min(0)
    Xn = np.where(rng_ > 0, (X - X.min(0)) / np.where(rng_ > 0, rng_, 1), 0.0)
    W = np.random.default_rng(seed).dirichlet(np.ones(len(CRITERIA)), n)             # n x k
    S = Xn @ W.T                                                                       # cells x n
    regret = S - S.min(axis=0, keepdims=True)
    ranks = S.argsort(axis=0).argsort(axis=0) + 1
    c["max_regret"] = regret.max(axis=1)
    c["mean_rank"] = ranks.mean(axis=1)
    c["rank_p10"] = np.percentile(ranks, 10, axis=1)
    c["rank_p90"] = np.percentile(ranks, 90, axis=1)
    return c.sort_values(["max_regret", "mean_rank"])


def rank_sites(account: pd.DataFrame, n_weight_samples: int | None = None, seed: int = 0) -> pd.DataFrame:
    n = int(_cfg()["siting"]["weight_samples"]) if n_weight_samples is None else n_weight_samples
    with_legal = _minimax(score_cells(account, legal=True), n, seed).reset_index(drop=True)
    no_legal = _minimax(score_cells(account, legal=False), n, seed)
    no_legal["rank_nolegal"] = np.arange(1, len(no_legal) + 1)
    out = with_legal.merge(no_legal[["state", "basin_id", "rank_nolegal"]], on=["state", "basin_id"], how="left")
    out.insert(0, "rank", np.arange(1, len(out) + 1))
    q = len(out)
    out["recommendation"] = np.select([out["rank"] <= q * 0.25, out["rank"] > q * 0.75],
                                      ["preferable", "avoid"], "middle")
    return out


if __name__ == "__main__":
    acct = pd.read_parquet(_repo_root() / "dcfootprint" / "outputs" / "account_facility_month.parquet")
    r = rank_sites(acct)
    print(f"Q1 SITING — {len(r)} candidate cells ({int((r['n_existing_dc'] > 0).sum())} already hold a DC); minimax regret:\n")
    cols = ["rank", "state", "basin_id", "n_existing_dc", "cf_mean", "ci_mean", "grid_fossil_share",
            "new_scarcity_m3eq", "basin_pressure", "max_regret", "rank_p10", "rank_p90", "rank_nolegal", "legal_flags"]
    print(r.head(12)[cols].round(3).to_string(index=False))
    print("\nexisting-DC cells:\n", r[r["n_existing_dc"] > 0][cols].round(3).to_string(index=False))

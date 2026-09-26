"""L6 / Q3 — Lyapunov drift-plus-penalty load allocation (a controller, NOT RL).

Each month we choose how to place the shiftable fraction of compute across existing
facilities to minimise carbon + scarcity-weighted water, while a per-basin water
"queue" D_b(t+1) = (D_b + W_b - R_hat_b)^+ keeps any basin from being drawn beyond
its (stylised) recharge. Solved as a per-month LP (scipy.linprog); the queue price
D_b augments the cost (the drift-plus-penalty / dual-decomposition reading).

Baselines: static (proportional to capacity), greedy (min scarcity cost, no queue),
lyapunov (queue-aware), and a per-month LP oracle. This is a STYLISED environment
(synthetic seasonal demand, an assumed flexible share); results are conditional on
R_hat (v2 L6). It is the Ceiling reach — reported honestly, not the headline.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
from scipy.optimize import linprog

from dcfootprint.io.facilities import _repo_root
from dcfootprint.account.energy import month_hours

MAX_UTIL = 0.90          # headroom: a facility can run up to this utilisation
V = 1.0                  # drift-plus-penalty weight (cost vs queue tradeoff)
LAMBDA = 1.0             # relative weight on scarcity water vs carbon (both normalised)


def _prepare(account: pd.DataFrame) -> pd.DataFrame:
    a = account.copy()
    a["month"] = pd.to_datetime(a["date"]).dt.month
    a["unit_carbon"] = a["carbon_tco2"] / a["e_it_mwh"]                 # tCO2 / MWh-IT
    a["unit_water"] = a["water_phys_l"] / a["e_it_mwh"]                 # L / MWh-IT
    a["unit_scarcity"] = a["water_scarcity_l_eq"] / a["e_it_mwh"]       # L-eq / MWh-IT
    hrs = month_hours(pd.to_datetime(a["date"]).dt.year.mode()[0]).set_index("month")["hours"]
    a["max_e_it"] = a["capacity_mw"] * MAX_UTIL * a["month"].map(hrs)
    return a


def _normalise(a: pd.DataFrame) -> pd.DataFrame:
    # put carbon & scarcity on a comparable 0..1 scale so V/LAMBDA are meaningful
    a = a.copy()
    a["c_norm"] = a["unit_carbon"] / a["unit_carbon"].mean()
    a["s_norm"] = a["unit_scarcity"] / a["unit_scarcity"].mean()
    return a


def _allocate(fixed: np.ndarray, cap: np.ndarray, pool: float, cost: np.ndarray, policy: str) -> np.ndarray:
    """Distribute `pool` of shiftable load as add-ons a_f, with fixed_f + a_f <= cap_f."""
    head = np.maximum(cap - fixed, 0.0)
    if pool <= 0 or head.sum() <= 0:
        return fixed
    if policy == "static":
        a = pool * head / head.sum()                      # proportional to headroom(~capacity)
        return fixed + a
    # greedy / lyapunov / oracle: LP  min cost.a  s.t. sum a = pool, 0<=a<=head
    pool_eff = min(pool, head.sum())
    res = linprog(c=cost, A_eq=[np.ones_like(cost)], b_eq=[pool_eff],
                  bounds=list(zip(np.zeros_like(head), head)), method="highs")
    a = res.x if res.success else pool_eff * head / head.sum()
    return fixed + a


def simulate(account: pd.DataFrame, policy: str, flexible_share: float = 0.3,
             demand_noise: float = 0.0, seed: int = 0, rmult: dict | None = None,
             prepared: pd.DataFrame | None = None) -> dict:
    a = prepared if prepared is not None else _normalise(_prepare(account))
    rng = np.random.default_rng(seed)
    if rmult is None:
        from dcfootprint.project.recharge import recharge_climatology
        rmult = recharge_climatology().set_index("month")["recharge_mult"].to_dict()

    basins = sorted(a["basin_id"].dropna().unique())
    D = {b: 0.0 for b in basins}                          # per-basin water queues
    # stylised recharge scale per basin = its mean monthly physical water under baseline
    base_wb = (a.groupby(["basin_id", "month"]).apply(lambda g: (g["e_it_mwh"] * g["unit_water"]).sum())
               .groupby("basin_id").mean())
    tot_c = tot_s = 0.0
    qpeak = 0.0
    for m in range(1, 13):
        g = a[a["month"] == m].copy()
        fixed = ((1 - flexible_share) * g["e_it_mwh"]).values
        pool = flexible_share * g["e_it_mwh"].sum() * (1 + demand_noise * rng.standard_normal())
        cap = g["max_e_it"].values
        if policy == "static":
            cost = np.zeros(len(g))
        else:
            cost = V * (g["c_norm"].values + LAMBDA * g["s_norm"].values)
            if policy == "lyapunov":                       # queue price on water
                dq = g["basin_id"].map(D).fillna(0).values
                cost = cost + dq * g["unit_water"].values / max(a["unit_water"].mean(), 1e-9)
        x = _allocate(fixed, cap, pool, cost, policy)
        # realised footprint this month
        tot_c += float((x * g["unit_carbon"].values).sum())
        tot_s += float((x * g["unit_scarcity"].values).sum())
        # update basin queues
        wb = pd.Series(x * g["unit_water"].values, index=g["basin_id"].values).groupby(level=0).sum()
        for b in basins:
            recharge = base_wb.get(b, 0.0) * rmult.get(m, 1.0)
            D[b] = max(D[b] + wb.get(b, 0.0) - recharge, 0.0)
            qpeak = max(qpeak, D[b])
    return {"policy": policy, "carbon_tco2": tot_c, "scarcity_m3eq": tot_s / 1000.0,
            "peak_basin_queue_m3": qpeak / 1000.0}


def compare(account: pd.DataFrame, flexible_share: float = 0.3, seeds: int = 10) -> pd.DataFrame:
    from dcfootprint.project.recharge import recharge_climatology
    rmult = recharge_climatology().set_index("month")["recharge_mult"].to_dict()   # once, not per-run
    prepared = _normalise(_prepare(account))
    rows = []
    for policy in ["static", "greedy", "lyapunov", "oracle"]:
        runs = [simulate(account, "greedy" if policy == "oracle" else policy,
                         flexible_share, demand_noise=0.05, seed=s, rmult=rmult, prepared=prepared)
                for s in range(seeds)]
        df = pd.DataFrame(runs)
        rows.append({"policy": policy,
                     "carbon_tco2": df["carbon_tco2"].mean(),
                     "scarcity_m3eq": df["scarcity_m3eq"].mean(),
                     "scarcity_sd": df["scarcity_m3eq"].std(),
                     "peak_basin_queue_m3": df["peak_basin_queue_m3"].mean()})
    out = pd.DataFrame(rows)
    base = out.loc[out["policy"] == "static", "scarcity_m3eq"].iloc[0]
    out["scarcity_saving_pct_vs_static"] = ((base - out["scarcity_m3eq"]) / base * 100).round(1)
    return out


if __name__ == "__main__":
    acct = pd.read_parquet(_repo_root() / "dcfootprint" / "outputs" / "account_facility_month.parquet")
    res = compare(acct, seeds=10)
    print("Q3 ROUTING (stylised; scarcity-weighted water & peak basin queue, mean of 10 seeds):\n")
    print(res.to_string(index=False))

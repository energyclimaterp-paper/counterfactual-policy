"""L6 / Q3 — Lyapunov drift-plus-penalty load allocation (a controller, NOT RL).

Each month we place the shiftable fraction of compute across existing facilities to
minimise carbon + scarcity-weighted water, while a per-basin water queue
    D_b(t+1) = ( D_b(t) + W_b(t) - R_hat_b(t) )^+
keeps any basin from being drawn beyond its budget. W_b = A_basin^T (x * u_onsite) is the
EXACT basin load through the incidence matrix (geo/incidence.py, architecture L4 core);
queues track scope-1 water only, since scope-2 is drawn at power-plant basins.
R_hat_b is decoupled from datacenter use (project/recharge.basin_budgets).

Policies
  static       proportional to headroom (the floor)
  greedy       per-month LP on forecast costs, no queue memory
  lyapunov     greedy + queue price D_b/R_bar_b on scope-1 water (drift-plus-penalty)
  lyapunov_pf  lyapunov with perfect foresight of carbon intensity (value of the forecast)
  oracle       OFFLINE full-horizon LP with perfect foresight of CI, demand and recharge,
               constrained to per-basin queue peaks no worse than lyapunov's -> the best
               achievable penalty at the same water-sustainability level (a lower bound;
               there are no integer decisions, so the LP optimum is the MILP optimum)
Controllers see the one-step CI forecast = seasonal naive (same month last year), the
backtest winner in project/forecast.py; realised footprints use the true CI.

Legal hard limits (policy/gap.region_effects) apply when legal=True: ZLD mandates cut
scope-1 water, renewable-share mandates cut carbon, bans stop added load.

This is a STYLISED environment (synthetic seasonal demand, an assumed flexible share,
budgets from AWARE+G3P); results are conditional on R_hat (v2 L6).
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import yaml
from scipy import sparse
from scipy.optimize import linprog

from dcfootprint.io.facilities import _repo_root
from dcfootprint.account.energy import month_hours


def _params() -> dict:
    return yaml.safe_load((_repo_root() / "dcfootprint" / "config" / "parameters.yaml").read_text(encoding="utf-8"))["routing"]


def _ci_forecast(account: pd.DataFrame) -> pd.Series:
    """Seasonal-naive one-step CI forecast per row: same zone, same month, previous year."""
    from dcfootprint.io import ember
    import yaml as _y
    p = _y.safe_load((_repo_root() / "dcfootprint" / "config" / "parameters.yaml").read_text(encoding="utf-8"))["grid"]
    prev = ember.zone_month_ci(ember.load_india_raw(), int(p["account_year"]) - 1, p["zone"])
    m = account[["zone_id", "month"]].merge(prev, on=["zone_id", "month"], how="left")
    return m["ci_gco2_per_kwh"].fillna(account["ci_gco2_per_kwh"].reset_index(drop=True)).values


def prepare(account: pd.DataFrame, legal: bool = True, budget_scale: float | None = None) -> dict:
    """Facility x month arrays (facilities sorted by id) + incidence + budgets."""
    from dcfootprint.geo.incidence import build_incidence
    from dcfootprint.policy.gap import region_effects
    from dcfootprint.project.recharge import basin_budgets
    rp = _params()
    a = account.sort_values(["facility_id", "month"]).reset_index(drop=True).copy()
    a["ci_hat"] = _ci_forecast(a)
    a["u_carbon"] = a["carbon_tco2"] / a["e_it_mwh"]                        # tCO2 / MWh-IT
    a["u_carbon_hat"] = a["u_carbon"] * a["ci_hat"] / a["ci_gco2_per_kwh"]
    a["u_onsite"] = a["water_onsite_l"] / a["e_it_mwh"]                     # L / MWh-IT (scope-1)
    a["u_s1"] = a["water_scarcity_onsite_l_eq"] / a["e_it_mwh"]
    a["u_s2"] = a["water_scarcity_grid_l_eq"] / a["e_it_mwh"]
    a["banned"] = False
    if legal:
        for st in a["state"].dropna().unique():
            eff = region_effects(st)
            m = a["state"] == st
            if "zld_mandate" in eff:
                a.loc[m, ["u_onsite", "u_s1"]] *= (1 - eff["zld_mandate"])
            if "re_share_min" in eff:
                a.loc[m, ["u_carbon", "u_carbon_hat"]] *= (1 - eff["re_share_min"])
            if "ban_new_above_mw" in eff:
                a.loc[m & (a["capacity_mw"] >= eff["ban_new_above_mw"]), "banned"] = True
    a["u_scarcity"] = a["u_s1"] + a["u_s2"]
    hrs = month_hours(int(pd.to_datetime(a["date"]).dt.year.mode()[0])).set_index("month")["hours"]
    a["max_e_it"] = a["capacity_mw"] * float(rp["max_util"]) * a["month"].map(hrs)

    fac = a.drop_duplicates("facility_id")[["facility_id", "basin_id", "state"]].assign(zone_id=lambda d: d["state"])
    _, A_basin = build_incidence(fac)
    A_basin = A_basin.reindex(sorted(fac["facility_id"])).fillna(0)
    F, B = A_basin.shape

    def mat(col):                                   # F x 12
        return a.pivot(index="facility_id", columns="month", values=col).reindex(A_basin.index).values

    arr = {c: mat(c) for c in ["e_it_mwh", "max_e_it", "u_carbon", "u_carbon_hat", "u_onsite", "u_scarcity"]}
    arr["banned"] = a.groupby("facility_id")["banned"].first().reindex(A_basin.index).values
    c_mean, s_mean, w_mean = arr["u_carbon"].mean(), arr["u_scarcity"].mean(), max(arr["u_onsite"].mean(), 1e-12)
    lam = float(rp["lambda"])
    arr["cost_true"] = arr["u_carbon"] / c_mean + lam * arr["u_scarcity"] / s_mean
    arr["cost_hat"] = arr["u_carbon_hat"] / c_mean + lam * arr["u_scarcity"] / s_mean
    arr["w_norm"] = arr["u_onsite"] / w_mean

    total_onsite = float((arr["e_it_mwh"] * arr["u_onsite"]).sum())
    scale = float(rp["budget_scale"]) if budget_scale is None else budget_scale
    bud = basin_budgets(A_basin.columns, scale * total_onsite)
    R = bud.pivot(index="basin_id", columns="month", values="budget_l").reindex(A_basin.columns).values   # B x 12
    fixed_w = A_basin.values.T @ ((1 - float(rp["flexible_share"])) * arr["e_it_mwh"] * arr["u_onsite"])
    return {"a": a, "A": A_basin, "arr": arr, "R": R, "R_bar": R.mean(axis=1), "F": F, "B": B,
            "budgets": bud, "fixed_w": fixed_w,
            "n_unstabilisable": int((fixed_w.sum(axis=1) > R.sum(axis=1)).sum())}


def _lp_month(cost, head, pool):
    pool_eff = min(pool, head.sum())
    if pool_eff <= 0:
        return np.zeros_like(head)
    res = linprog(c=cost, A_eq=np.ones((1, len(cost))), b_eq=[pool_eff],
                  bounds=list(zip(np.zeros_like(head), head)), method="highs")
    return res.x if res.success else pool_eff * head / head.sum()


def _pools(P: dict, seed: int, noise: float, flex: float) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return flex * P["arr"]["e_it_mwh"].sum(axis=0) * (1 + noise * rng.standard_normal(12))


def simulate(P: dict, policy: str, seed: int = 0, V: float | None = None) -> dict:
    rp, arr, A = _params(), P["arr"], P["A"].values
    V = float(rp["V"]) if V is None else V
    flex = float(rp["flexible_share"])
    pools = _pools(P, seed, float(rp["demand_noise"]), flex)
    D = np.zeros(P["B"])
    X = np.zeros((P["F"], 12))
    Dhist = np.zeros((P["B"], 12))
    for t in range(12):
        fixed = (1 - flex) * arr["e_it_mwh"][:, t]
        head = np.maximum(arr["max_e_it"][:, t] - fixed, 0.0)
        head[arr["banned"]] = 0.0
        if policy == "static":
            add = min(pools[t], head.sum()) * head / head.sum()
        else:
            cost = V * (arr["cost_true"][:, t] if policy == "lyapunov_pf" else arr["cost_hat"][:, t])
            if policy in ("lyapunov", "lyapunov_pf"):
                q = D / np.maximum(P["R_bar"], 1e-12)                        # backlog in months of budget
                cost = cost + (A @ q) * arr["w_norm"][:, t]
            add = _lp_month(cost, head, pools[t])
        X[:, t] = fixed + add
        W_b = A.T @ (X[:, t] * arr["u_onsite"][:, t])                         # exact basin load
        D = np.maximum(D + W_b - P["R"][:, t], 0.0)
        Dhist[:, t] = D
    return _score(P, policy, X, Dhist, pools)


def oracle(P: dict, qcap: np.ndarray, seed: int = 0) -> dict:
    """Offline LP over all 12 months, perfect foresight, D_b(t) <= qcap_b."""
    rp, arr, A = _params(), P["arr"], P["A"].values
    flex = float(rp["flexible_share"])
    pools = _pools(P, seed, float(rp["demand_noise"]), flex)
    F, B, T = P["F"], P["B"], 12
    nx, nd = F * T, B * T
    xi = lambda f, t: t * F + f                                   # add-on a_{f,t}
    di = lambda b, t: nx + t * B + b                              # queue D_{b,t}
    fixed = (1 - flex) * arr["e_it_mwh"]
    head = np.maximum(arr["max_e_it"] - fixed, 0.0)
    head[arr["banned"], :] = 0.0

    c = np.zeros(nx + nd)
    for t in range(T):
        c[t * F:(t + 1) * F] = arr["cost_true"][:, t]
    Aeq = sparse.lil_matrix((T, nx + nd)); beq = np.zeros(T)
    for t in range(T):
        Aeq[t, t * F:(t + 1) * F] = 1.0
        beq[t] = min(pools[t], head[:, t].sum())
    # D_{b,t-1} - D_{b,t} + sum_f A[f,b] u[f,t] a[f,t] <= R[b,t] - fixedW[b,t]
    Aub = sparse.lil_matrix((B * T, nx + nd)); bub = np.zeros(B * T)
    for t in range(T):
        for b in range(B):
            r = t * B + b
            for f in np.nonzero(A[:, b])[0]:
                Aub[r, xi(f, t)] = arr["u_onsite"][f, t]
            Aub[r, di(b, t)] = -1.0
            if t > 0:
                Aub[r, di(b, t - 1)] = 1.0
            bub[r] = P["R"][b, t] - P["fixed_w"][b, t]
    bounds = [(0.0, head[f, t]) for t in range(T) for f in range(F)] + \
             [(0.0, qcap[b] * (1 + 1e-9) + 1e-6) for t in range(T) for b in range(B)]
    res = linprog(c, A_ub=Aub.tocsr(), b_ub=bub, A_eq=Aeq.tocsr(), b_eq=beq, bounds=bounds, method="highs")
    if not res.success:
        raise RuntimeError(f"oracle LP failed: {res.message}")
    X = fixed + res.x[:nx].reshape(T, F).T
    # recompute realised queues from X (the LP D is an upper envelope of the true queue)
    D = np.zeros(B); Dhist = np.zeros((B, T))
    for t in range(T):
        D = np.maximum(D + A.T @ (X[:, t] * arr["u_onsite"][:, t]) - P["R"][:, t], 0.0)
        Dhist[:, t] = D
    return _score(P, "oracle", X, Dhist, pools)


def _score(P, policy, X, Dhist, pools):
    arr = P["arr"]
    return {"policy": policy,
            "carbon_tco2": float((X * arr["u_carbon"]).sum()),
            "scarcity_m3eq": float((X * arr["u_scarcity"]).sum() / 1000.0),
            "penalty": float((X * arr["cost_true"]).sum() / arr["e_it_mwh"].sum()),   # per MWh-IT, normalised
            "peak_basin_queue_m3": float(Dhist.max() / 1000.0),
            "end_backlog_m3": float(Dhist[:, -1].sum() / 1000.0),
            "unserved_mwh": float(max(0.0, pools.sum() + (1 - _params()["flexible_share"]) * arr["e_it_mwh"].sum() - X.sum())),
            "_qpeak_by_basin": Dhist.max(axis=1)}


def compare(account: pd.DataFrame, seeds: int | None = None, legal: bool = True,
            budget_scale: float | None = None) -> pd.DataFrame:
    rp = _params()
    seeds = int(rp["seeds"]) if seeds is None else seeds
    P = prepare(account, legal=legal, budget_scale=budget_scale)
    runs = []
    for s in range(seeds):
        for pol in ["static", "greedy", "lyapunov", "lyapunov_pf"]:
            r = simulate(P, pol, seed=s)
            runs.append({**r, "seed": s})
            if pol == "lyapunov":
                runs.append({**oracle(P, r["_qpeak_by_basin"], seed=s), "seed": s})
    df = pd.DataFrame(runs).drop(columns="_qpeak_by_basin")
    out = df.groupby("policy", sort=False).agg(
        carbon_tco2=("carbon_tco2", "mean"), scarcity_m3eq=("scarcity_m3eq", "mean"),
        scarcity_sd=("scarcity_m3eq", "std"), penalty=("penalty", "mean"), penalty_sd=("penalty", "std"),
        peak_basin_queue_m3=("peak_basin_queue_m3", "mean"), end_backlog_m3=("end_backlog_m3", "mean"),
        unserved_mwh=("unserved_mwh", "mean")).reset_index()
    base = out.set_index("policy").loc["static"]
    out["scarcity_saving_pct_vs_static"] = ((base["scarcity_m3eq"] - out["scarcity_m3eq"]) / base["scarcity_m3eq"] * 100).round(2)
    out["carbon_saving_pct_vs_static"] = ((base["carbon_tco2"] - out["carbon_tco2"]) / base["carbon_tco2"] * 100).round(2)
    orc = out.set_index("policy").loc["oracle", "penalty"]
    out["penalty_gap_pct_vs_oracle"] = ((out["penalty"] - orc) / orc * 100).round(3)
    out["legal"] = legal
    out["seeds"] = seeds
    out.attrs["n_unstabilisable_basins"] = P["n_unstabilisable"]
    out.attrs["n_basins"] = P["B"]
    return out


def v_sweep(account: pd.DataFrame, seeds: int | None = None) -> pd.DataFrame:
    """Lyapunov penalty vs peak queue across V (theory: gap O(1/V), queue O(V))."""
    rp = _params()
    seeds = int(rp["seeds"]) if seeds is None else seeds
    P = prepare(account, legal=True)
    rows = []
    for V in rp["v_sweep"]:
        rs = [simulate(P, "lyapunov", seed=s, V=float(V)) for s in range(seeds)]
        rows.append({"V": V, "penalty": np.mean([r["penalty"] for r in rs]),
                     "peak_basin_queue_m3": np.mean([r["peak_basin_queue_m3"] for r in rs]),
                     "end_backlog_m3": np.mean([r["end_backlog_m3"] for r in rs])})
    return pd.DataFrame(rows)


def budget_sweep(account: pd.DataFrame, scales=(0.5, 1.0, 2.0, 4.0), seeds: int = 5) -> pd.DataFrame:
    """Q3 is conditional on R_hat: how the comparison moves with the budget scale."""
    rows = []
    for sc in scales:
        r = compare(account, seeds=seeds, legal=True, budget_scale=sc).set_index("policy")
        rows.append({"budget_scale": sc, "unstabilisable_basins": r.attrs["n_unstabilisable_basins"],
                     "n_basins": r.attrs["n_basins"],
                     "greedy_scarcity_saving_pct": r.loc["greedy", "scarcity_saving_pct_vs_static"],
                     "lyapunov_scarcity_saving_pct": r.loc["lyapunov", "scarcity_saving_pct_vs_static"],
                     "lyapunov_carbon_saving_pct": r.loc["lyapunov", "carbon_saving_pct_vs_static"],
                     "lyapunov_gap_vs_oracle_pct": r.loc["lyapunov", "penalty_gap_pct_vs_oracle"],
                     "static_peak_queue_m3": r.loc["static", "peak_basin_queue_m3"],
                     "greedy_peak_queue_m3": r.loc["greedy", "peak_basin_queue_m3"],
                     "lyapunov_peak_queue_m3": r.loc["lyapunov", "peak_basin_queue_m3"]})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    acct = pd.read_parquet(_repo_root() / "dcfootprint" / "outputs" / "account_facility_month.parquet")
    for legal in (True, False):
        res = compare(acct, legal=legal)
        print(f"\nQ3 ROUTING legal={legal} (mean of {res['seeds'].iloc[0]} seeds; "
              f"{res.attrs['n_unstabilisable_basins']}/{res.attrs['n_basins']} basins unstabilisable by fixed load alone):")
        print(res.drop(columns=["legal", "seeds"]).round(4).to_string(index=False))
    print("\nV sweep (lyapunov):\n", v_sweep(acct).to_string(index=False))

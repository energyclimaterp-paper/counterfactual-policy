"""L7 / Q1 — siting: rank candidate basin x state regions for a NEW datacenter.

Candidate cells are the basin x state cells present in the data. Each is scored on
scarcity (basin CF, lower better) and marginal pressure (existing load already in
that basin, lower better); India carbon is national so it doesn't discriminate
within India. Weights are Monte-Carlo sampled and cells ranked by MINIMUM REGRET
(mean rank across weightings), so the recommendation is robust to weight choice.
Output = ranked *regions* with reasons, not plot-level sites (v2 Q1 caveat).
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def rank_sites(account: pd.DataFrame, n_weight_samples: int = 200, seed: int = 0) -> pd.DataFrame:
    cells = account.groupby(["state", "basin_id"], as_index=False).agg(
        mean_cf=("cf", "mean"),
        existing_scarcity_m3eq=("water_scarcity_l_eq", lambda s: s.sum() / 1000.0),
        n_facilities=("facility_id", "nunique"),
    )
    # normalise the two "lower is better" criteria to 0..1
    for c in ["mean_cf", "existing_scarcity_m3eq"]:
        rng = cells[c].max() - cells[c].min()
        cells[c + "_n"] = (cells[c] - cells[c].min()) / rng if rng > 0 else 0.0

    rs = np.random.default_rng(seed)
    ranks = np.zeros(len(cells))
    for _ in range(n_weight_samples):
        w = rs.dirichlet([1, 1])                      # random weights on (scarcity, pressure)
        score = w[0] * cells["mean_cf_n"] + w[1] * cells["existing_scarcity_m3eq_n"]
        ranks += score.rank().values
    cells["mean_rank"] = ranks / n_weight_samples     # lower = more robustly preferable
    cells["recommendation"] = np.where(cells["mean_cf"] <= cells["mean_cf"].median(),
                                       "preferable (lower scarcity)", "avoid (high scarcity)")
    return cells.sort_values("mean_rank").reset_index(drop=True)


if __name__ == "__main__":
    from dcfootprint.io.facilities import _repo_root
    acct = pd.read_parquet(_repo_root() / "dcfootprint" / "outputs" / "account_facility_month.parquet")
    r = rank_sites(acct)
    print("Q1 SITING — candidate basin x state cells (min-regret rank; lower=better):\n")
    print(r.head(8)[["state", "basin_id", "mean_cf", "n_facilities", "mean_rank", "recommendation"]].to_string(index=False))

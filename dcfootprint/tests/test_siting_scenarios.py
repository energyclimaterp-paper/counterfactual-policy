"""Q1 2030/2050 water scenarios: minimax regret over weights x Aqueduct scenarios (decisions/siting.py)."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from dcfootprint.decisions.siting import CRITERIA, _minimax_scenarios
from dcfootprint.project.scarcity_future import SCENARIOS

ROOT = Path(__file__).resolve().parents[2]


def _cells(base: list[list[float]], ws: list[list[float]]) -> pd.DataFrame:
    d = pd.DataFrame(base, columns=CRITERIA)
    for j, s in enumerate(SCENARIOS):
        d[f"ws_{s}"] = [row[j] for row in ws]
    d["state"], d["basin_id"], d["excluded"] = "S", range(len(d)), False
    return d


def test_dominating_cell_has_zero_regret():
    flat = [1.0] * len(SCENARIOS)
    c = _cells([[0, 0, 0, 0], [1, 1, 1, 1], [0.5, 0.5, 0.5, 0.5]], [flat, [5.0] * len(SCENARIOS), [3.0] * len(SCENARIOS)])
    r = _minimax_scenarios(c, 200, 0).set_index("basin_id")
    assert r.loc[0, "max_regret"] == pytest.approx(0.0)
    assert r.loc[0, "max_regret"] < r.loc[2, "max_regret"] < r.loc[1, "max_regret"]


def test_max_regret_is_worst_scenario_and_future_stress_counts():
    # identical today; cell 1's basin worsens to 5 under pes50 only -> its worst case is pes50
    same = [0.5, 0.5, 0.5, 0.5]
    ws0 = [2.0] * len(SCENARIOS)
    ws1 = [2.0 if s != "pes50" else 5.0 for s in SCENARIOS]
    r = _minimax_scenarios(_cells([same, same], [ws0, ws1]), 200, 0).set_index("basin_id")
    per = r[[f"max_regret_{s}" for s in SCENARIOS]]
    assert np.allclose(r["max_regret"], per.max(axis=1))
    assert r.loc[1, "worst_scenario"] == "pes50"
    assert r.loc[1, "max_regret"] > r.loc[0, "max_regret"] == pytest.approx(0.0)
    assert r.loc[1, "max_regret_baseline"] == pytest.approx(0.0)


def test_excluded_cells_are_not_ranked():
    flat = [1.0] * len(SCENARIOS)
    c = _cells([[0, 0, 0, 0], [1, 1, 1, 1]], [flat, flat])
    c.loc[0, "excluded"] = True
    assert list(_minimax_scenarios(c, 50, 0)["basin_id"]) == [1]


@pytest.mark.skipif(not (ROOT / "data" / "aqueduct" / "Aq40_Y2023D07M05.gdb").exists(), reason="Aqueduct GDB not on disk")
def test_aqueduct_basin_scores_contract():
    from dcfootprint.project.scarcity_future import basin_scores
    s = basin_scores([47731, 50051])                      # Karnataka / Tamil Nadu cells in the India Q1 table
    assert set(s["scenario"]) == set(SCENARIOS) and len(s) == 2 * len(SCENARIOS)
    assert s["ws_score"].between(0, 5).all() and s["scored_share"].between(0, 1.01).all()

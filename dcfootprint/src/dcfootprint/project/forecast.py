"""L3 — grid-CI forecasting (real time series).

Rolling-origin backtest of seasonal-naive vs SARIMA on the Ember India national
CO2-intensity series (2019->2025); the model is used only if it beats seasonal
naive on the backtest (the salvaged skill-floor rule). Then forecast monthly CI
forward to `year_end` for the projection (Q1 long horizon; Q3 one-step).

Also loads the reused Co-RE multi-model benchmark (SARIMA/xLSTM/TimesFM/Chronos-2,
Nexus relabelled Chronos-2) and the seasonal-naive skill audit, which shows the
gain over naive is small (mean ~3-9%) — reported honestly, not hidden.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from dcfootprint.io.facilities import _repo_root
from dcfootprint.io import ember

_GAT = "gat-based-forecasting/diff/gat-sarima-nexus"


def _series(ci: pd.DataFrame) -> pd.Series:
    s = ci.set_index("date")["ci_gco2_per_kwh"].sort_index().asfreq("MS")
    return s.interpolate(limit_direction="both")


def _seasonal_naive(train: pd.Series, h: int) -> np.ndarray:
    last = train.iloc[-12:].values
    return np.array([last[i % 12] for i in range(h)])


def _sarima_forecast(train: pd.Series, h: int):
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    m = SARIMAX(train, order=(1, 1, 1), seasonal_order=(1, 0, 1, 12),
                enforce_stationarity=False, enforce_invertibility=False).fit(disp=False)
    f = m.get_forecast(h)
    return f.predicted_mean.values, f.conf_int(alpha=0.2).values


def backtest_ci(test_h: int = 12) -> dict:
    s = _series(ember.national_monthly_ci(ember.load_india_raw()))
    train, test = s.iloc[:-test_h], s.iloc[-test_h:]
    rmse = {"seasonal_naive": float(np.sqrt(np.mean((_seasonal_naive(train, test_h) - test.values) ** 2)))}
    try:
        pred, _ = _sarima_forecast(train, test_h)
        rmse["SARIMA"] = float(np.sqrt(np.mean((pred - test.values) ** 2)))
    except Exception as e:                       # keep the pipeline running if statsmodels balks
        rmse["SARIMA"] = None
    cand = {k: v for k, v in rmse.items() if v is not None}
    winner = min(cand, key=cand.get)
    skill = 1 - rmse[winner] / rmse["seasonal_naive"] if rmse["seasonal_naive"] else 0.0
    return {"rmse": rmse, "winner": winner, "skill_vs_naive": round(skill, 4)}


def forecast_ci(year_end: int = 2030) -> dict:
    """Backtest, then forecast national CI monthly to Dec `year_end`."""
    bt = backtest_ci()
    s = _series(ember.national_monthly_ci(ember.load_india_raw()))
    last = s.index[-1]
    h = (year_end - last.year) * 12 + (12 - last.month)
    dates = pd.date_range(last + pd.offsets.MonthBegin(1), periods=h, freq="MS")
    if bt["winner"] == "SARIMA":
        try:
            mean, ci = _sarima_forecast(s, h)
            fc = pd.DataFrame({"date": dates, "ci_gco2_per_kwh": mean, "lo": ci[:, 0], "hi": ci[:, 1]})
        except Exception:
            bt["winner"] = "seasonal_naive"
    if bt["winner"] != "SARIMA":
        mean = _seasonal_naive(s, h)
        fc = pd.DataFrame({"date": dates, "ci_gco2_per_kwh": mean, "lo": mean * 0.9, "hi": mean * 1.1})
    fc["model"] = bt["winner"]
    return {"backtest": bt, "forecast": fc}


def core_benchmark() -> dict:
    """Reuse the Co-RE cached benchmark: mean RMSE by model (Nexus->Chronos-2) +
    the seasonal-naive skill audit. Returns {} if the GAT repo isn't present."""
    root = _repo_root()
    out = {}
    mc = root / _GAT / "outputs_v2" / "partB" / "model_comparison_region.csv"
    if mc.exists():
        d = pd.read_csv(mc)
        d["model"] = d["model"].replace({"Nexus": "Chronos-2"})
        out["rmse_by_model"] = (d.groupby(["resource", "model"])["RMSE"].mean()
                                .round(2).reset_index().to_dict("records"))
    sk = root / _GAT / "outputs_gapfill_v5" / "skill_vs_seasonal_naive.csv"
    if sk.exists():
        s = pd.read_csv(sk)
        out["skill_vs_naive"] = s[["resource", "method", "mean_skill", "pct_regions_beating_sn"]].round(3).to_dict("records")
    return out


if __name__ == "__main__":
    r = forecast_ci()
    print("backtest:", r["backtest"])
    fc = r["forecast"]
    print(f"forecast {fc['date'].min().date()}->{fc['date'].max().date()} ({len(fc)} mo), model={fc['model'].iloc[0]}")
    print(fc.head(3).to_string(index=False))
    cb = core_benchmark()
    print("\nCo-RE benchmark reused:", "yes" if cb else "GAT repo absent")
    if cb.get("skill_vs_naive"):
        print("skill vs seasonal-naive (carbon):", [x for x in cb["skill_vs_naive"] if x["resource"] == "carbon"][:2])

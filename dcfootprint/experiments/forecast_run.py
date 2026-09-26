"""Fresh dcfootprint forecasts (seasonal naive + SARIMA) for the forecasting run.

Series: Ember monthly electricity (Total Generation, GWh) and carbon (CO2 intensity, gCO2/kWh)
for every zone (India/US states, EU-27 countries) and each region's aggregate ('<X> Total'),
via io/ember.load_raw (EU converted to GWh and CO2e-labelled gCO2/kWh).
Design (fixed before running):
  origins   Dec 2022, Dec 2023, Dec 2024 (rolling), horizon h = 1..12 from each origin
  models    seasonal_naive  y(t-12); sigma = SD of its 12-month-ahead errors over the 12 months
                            before the origin; 80% interval = mean +- 1.2816 sigma
            sarima          SARIMA(1,1,1)(1,0,1,12), stationarity/invertibility enforced, fitted on
                            data up to the origin; statsmodels predictive mean, SE and 80% interval;
                            a non-finite or > 10x historical-max forecast is recorded as a failure
  scoring   metrics per model x region x resource over all zones, origins and horizons
            (experiments/forecast_metrics.py); MASE scale = in-sample seasonal-naive MAE per series
Output: <run>/forecasts/<model>/<resource>/<region>.csv  (raw forecasts with actuals)
        <run>/metrics/per_model_per_region.csv, per_model_per_zone.csv, failures.csv

Run: PYTHONPATH=dcfootprint/src python dcfootprint/experiments/forecast_run.py <run_dir>
"""
from __future__ import annotations

import sys
import time
import warnings
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forecast_metrics import mase_scale, metrics  # noqa: E402

ORIGINS = [pd.Timestamp("2022-12-01"), pd.Timestamp("2023-12-01"), pd.Timestamp("2024-12-01")]
H = 12
MAXITER = 500          # L-BFGS budget; a fit not converged by then is a recorded failure. Added after a
                       # non-converged Germany fit gave oscillating 225,000 GWh forecasts (numerical defect)
Z80 = 1.2815515655446004
RESOURCES = {"electricity": ("Total Generation", "GWh"), "carbon": ("CO2 intensity", "gCO2/kWh")}


def series_panel(region: str) -> dict[str, pd.DataFrame]:
    from dcfootprint.io import ember
    raw = ember.load_raw(region)
    keep = set(ember.zones_of(raw)) | {ember.national_of(raw)}
    out = {}
    for res, (var, unit) in RESOURCES.items():
        d = raw[(raw["Variable"] == var) & (raw["Unit"] == unit) & raw["State"].isin(keep)]
        out[res] = d.pivot_table(index="date", columns="State", values="Value", aggfunc="mean").sort_index().asfreq("MS")
    return out


def _snaive(y: pd.Series, origin: pd.Timestamp):
    idx = pd.date_range(origin + pd.offsets.MonthBegin(1), periods=H, freq="MS")
    mean = y.shift(12).reindex(idx).to_numpy(float)             # y(t-12): uses data <= origin for h <= 12
    # sigma from the 12-month-ahead errors of the same method over the 12 months up to the origin
    past = pd.date_range(origin - pd.offsets.MonthBegin(11), origin, freq="MS")
    err = (y.shift(12).reindex(past) - y.reindex(past)).to_numpy(float)
    sig = float(np.nanstd(err, ddof=1)) if np.isfinite(err).sum() > 2 else np.nan
    return idx, mean, np.full(H, sig)


def _sarima(y: pd.Series, origin: pd.Timestamp):
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    tr = y[:origin]                        # missing months kept as NaN (Kalman filter handles them; keeps freq)
    tr = tr.loc[tr.first_valid_index():]
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        res = SARIMAX(tr, order=(1, 1, 1), seasonal_order=(1, 0, 1, 12)).fit(disp=False, maxiter=MAXITER)
        fc = res.get_forecast(H)
    if not res.mle_retvals.get("converged", False):
        raise RuntimeError(f"MLE did not converge in {MAXITER} iterations")   # non-converged fit = failed fit
    coefs = res.params.drop("sigma2", errors="ignore").to_numpy(float)
    if np.any(np.abs(coefs) >= 0.9999) or not np.all(np.isfinite(fc.se_mean.to_numpy(float))):
        raise RuntimeError("degenerate fit (coefficient on the unit boundary or non-finite SE)")
    mean = fc.predicted_mean.to_numpy(float)
    if not np.all(np.isfinite(mean)) or np.nanmax(np.abs(mean)) > 10 * max(float(np.nanmax(np.abs(tr))), 1e-9):
        raise FloatingPointError("SARIMA forecast diverged")
    idx = pd.date_range(origin + pd.offsets.MonthBegin(1), periods=H, freq="MS")
    return idx, mean, fc.se_mean.to_numpy(float)


def run(run_dir: Path, regions=("India", "US", "EU")) -> pd.DataFrame:
    run_dir = Path(run_dir)
    rows_metrics, rows_zone, fails = [], [], []
    for region in regions:
        panel = series_panel(region)
        for res, wide in panel.items():
            for model, fn in [("seasonal_naive", _snaive), ("sarima", _sarima)]:
                recs = []
                for zone in wide.columns:
                    y = wide[zone].astype(float)
                    if y.dropna().shape[0] < 36:
                        fails.append({"model": model, "region": region, "resource": res, "zone": zone,
                                      "origin": None, "reason": "fewer than 36 months"}); continue
                    for origin in ORIGINS:
                        if y[:origin].dropna().shape[0] < 36:
                            continue
                        try:
                            idx, mean, sig = fn(y, origin)
                        except Exception as e:
                            fails.append({"model": model, "region": region, "resource": res, "zone": zone,
                                          "origin": origin.date(), "reason": f"{type(e).__name__}: {e}"}); continue
                        sc = mase_scale(y[:origin].to_numpy(float))
                        for h, (t, m, s) in enumerate(zip(idx, mean, sig), start=1):
                            recs.append({"zone_id": zone, "origin": origin.date(), "h": h, "timestamp": t.date(),
                                         "actual": y.get(t, np.nan), "mean": m, "sigma": s,
                                         "lo": m - Z80 * s if np.isfinite(s) else np.nan,
                                         "hi": m + Z80 * s if np.isfinite(s) else np.nan,
                                         "interval_level": 0.80, "mase_scale": sc})
                df = pd.DataFrame(recs)
                out = run_dir / "forecasts" / model / res
                out.mkdir(parents=True, exist_ok=True)
                df.to_csv(out / f"{region.lower()}.csv", index=False)
                is_agg = df["zone_id"].astype(str).str.endswith(" Total") if len(df) else pd.Series(dtype=bool)
                for level, part in [("zones", df[~is_agg]), ("aggregate", df[is_agg])]:
                    if len(part):                  # the '<X> Total' series is reported apart from the zones
                        rows_metrics.append({"model": model, "region": region, "resource": res, "level": level,
                                             "grain": "zone-month (Ember)", "n_series": int(part["zone_id"].nunique()),
                                             **metrics(part)})
                for z, g in df.groupby("zone_id"):
                    rows_zone.append({"model": model, "region": region, "resource": res, "zone_id": z, **metrics(g)})
                print(f"{region:<5} {res:<11} {model:<14} series={df['zone_id'].nunique() if len(df) else 0:>3} "
                      f"points={len(df):>5}", flush=True)
    m = run_dir / "metrics"
    m.mkdir(parents=True, exist_ok=True)
    pm = pd.DataFrame(rows_metrics)
    pm.to_csv(m / "per_model_per_region.csv", index=False)
    pd.DataFrame(rows_zone).to_csv(m / "per_model_per_zone.csv", index=False)
    pd.DataFrame(fails).to_csv(m / "failures.csv", index=False)
    return pm


if __name__ == "__main__":
    t0 = time.time()
    print(run(Path(sys.argv[1])).round(3).to_string(index=False))
    print(f"elapsed {time.time() - t0:.0f}s")

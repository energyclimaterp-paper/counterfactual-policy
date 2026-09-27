"""Score real (LLM) Nexus forecasts with the run's full metric set, side by side with the Co-RE cache.

Inputs: one or more nexus_<resource>_ollama.csv files written by the Kaggle / local Nexus runner
(columns region_id, resource, arm, tag, timestamp, value, actual, seconds), plus the Co-RE series dump
and cached forecasts (read-only). Scored exactly like experiments/score_core_cached.py:
  - actuals from diff/gat-sarima-nexus/work/region_series_dump.json (the runner's own `actual` column
    is checked against them, and the run stops if they disagree);
  - MASE scale = in-sample lag-12 naive MAE of the series before its first forecast month;
  - metrics from forecast_metrics.metrics(). Nexus emits point forecasts only, so PICP and CRPS are NaN
    (as for the cached models), never estimated.
Series whose tag is not "ollama" (a fallback fired) are reported and excluded from the LLM-Nexus scores.

The comparison table uses only the series that Nexus actually completed, for every model, so a
partial run is still compared like for like.

    python dcfootprint/experiments/score_nexus_llm.py <run_dir> <label> <nexus_csv> [<nexus_csv> ...]
    e.g. ... runs/nexus_llm_2026-09-28 "nexus-llm-gemma4-kaggle-gpu" nexus_electricity_ollama.csv nexus_carbon_ollama.csv
Use a NEW run folder: runs/fresh_run_2026-09-27/ is a frozen snapshot and must not be written to.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forecast_metrics import mase_scale, metrics  # noqa: E402
from score_core_cached import CORE, LABEL, region_of  # noqa: E402

HOLDOUT = 12


def _records(fc: pd.DataFrame, dump: dict, model_col: str | None = None) -> pd.DataFrame:
    recs = []
    for (res, rid), g in fc.groupby(["resource", "region_id"]):
        s = pd.Series(dump[res][rid]["values"], index=pd.to_datetime(dump[res][rid]["index"]), dtype=float)
        first = g["timestamp"].min()
        sc = mase_scale(s[s.index < first].to_numpy(float))
        for _, r in g.sort_values("timestamp").iterrows():
            recs.append({"model": r[model_col] if model_col else None, "resource": res, "zone_id": rid,
                         "region": region_of(rid, res), "timestamp": r["timestamp"],
                         "actual": s.get(r["timestamp"], np.nan), "mean": r["value"], "mase_scale": sc,
                         "lo": np.nan, "hi": np.nan, "sigma": np.nan})
    return pd.DataFrame(recs)


def run(run_dir: Path, label: str, files: list[Path]) -> pd.DataFrame:
    dump = json.load(open(CORE / "work" / "region_series_dump.json"))
    nx = pd.concat([pd.read_csv(f, parse_dates=["timestamp"]) for f in files], ignore_index=True)
    nx = nx.drop_duplicates(["resource", "region_id", "timestamp"])
    complete = nx.groupby(["resource", "region_id"])["timestamp"].transform("size") == HOLDOUT
    nx = nx[complete]
    fell_back = nx[nx["tag"] != "ollama"][["resource", "region_id", "tag"]].drop_duplicates()
    if len(fell_back):
        print(f"{len(fell_back)} series fell back (excluded from LLM-Nexus scores):\n{fell_back.to_string(index=False)}")
    nx = nx[nx["tag"] == "ollama"]

    # the runner's actuals must equal the dump's (same series, same holdout) -- stop if not
    for (res, rid), g in nx.groupby(["resource", "region_id"]):
        s = pd.Series(dump[res][rid]["values"], index=pd.to_datetime(dump[res][rid]["index"]))
        idx = s.index[-HOLDOUT:]
        if sorted(g["timestamp"]) != list(idx) or not np.allclose(g.sort_values("timestamp")["actual"], s[idx].values):
            raise SystemExit(f"holdout/actuals mismatch for {res}/{rid}: not the Co-RE holdout")

    d_nx = _records(nx.assign(model=label), dump, "model")
    cache = pd.read_csv(CORE / "outputs_v2" / "partB" / "per_region_base_forecasts.csv", parse_dates=["timestamp"])
    cache["model"] = cache["model"].map(LABEL)
    keys = set(zip(nx["resource"], nx["region_id"]))
    cache = cache[[k in keys for k in zip(cache["resource"], cache["region_id"])]]      # same series only
    d_all = pd.concat([d_nx, _records(cache, dump, "model")], ignore_index=True)

    # save Nexus forecasts in the run's format
    for (res, reg), d in d_nx.groupby(["resource", "region"]):
        out = run_dir / "forecasts" / label / res
        out.mkdir(parents=True, exist_ok=True)
        d.assign(h=d.groupby("zone_id").cumcount() + 1).drop(columns=["model", "resource", "region"]) \
            .to_csv(out / f"{reg.lower()}.csv", index=False)

    rows, zrows = [], []
    for (model, res, reg), d in d_all.groupby(["model", "resource", "region"]):
        rows.append({"model": model, "resource": res, "region": reg, "n_series": int(d["zone_id"].nunique()), **metrics(d)})
        for z, zz in d.groupby("zone_id"):
            zrows.append({"model": model, "resource": res, "region": reg, "zone_id": z, **metrics(zz)})
    m = run_dir / "metrics"
    m.mkdir(parents=True, exist_ok=True)
    tab = pd.DataFrame(rows).sort_values(["resource", "region", "RMSE"])
    tab.to_csv(m / f"{label}_vs_core_cached_per_region.csv", index=False)
    pd.DataFrame(zrows).to_csv(m / f"{label}_vs_core_cached_per_zone.csv", index=False)
    runtime = nx.groupby(["resource", "region_id"])["seconds"].first()
    print(f"\n{label}: {len(keys)} series scored ({nx.groupby('resource').region_id.nunique().to_dict()}); "
          f"median {runtime.median():.0f} s per series\n")
    return tab


if __name__ == "__main__":
    t = run(Path(sys.argv[1]), sys.argv[2], [Path(f) for f in sys.argv[3:]])
    cols = ["resource", "region", "model", "n_series", "RMSE", "MAE", "MASE", "WMAPE_pct", "sMAPE_pct",
            "Bias", "MedAE", "Pearson_r", "PICP", "CRPS"]
    print(t[cols].round(3).to_string(index=False))

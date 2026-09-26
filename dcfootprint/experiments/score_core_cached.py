"""Score the Co-RE cached base forecasts (Part B, outputs_v2) with the run's full metric set.

Inputs (Co-RE repo, read-only):
  diff/gat-sarima-nexus/outputs_v2/partB/per_region_base_forecasts.csv   point forecasts, h = 1..12
  diff/gat-sarima-nexus/work/region_series_dump.json                      the exact series Part B scored
Labelling: the cache's "Nexus" column is Chronos-2 occupying the Nexus slot (AUDIT_REPORT.md §1)
-> written as model "chronos-2". The real multi-agent Nexus is NOT in this cache.
Only point forecasts were cached -> PICP and CRPS are NaN for these models (no intervals exist).
MASE scale = in-sample lag-12 naive MAE of each series before its first forecast timestamp (for the
irregular G3P water series this is lag-12 in observation order, flagged in the sidecar).
Output: <run>/forecasts/<model>/<resource>/<region>__core_cached.csv, <run>/metrics/core_cached_*.csv
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from forecast_metrics import mase_scale, metrics  # noqa: E402

CORE = Path(r"D:\3Gtech_paper - GNN\diff\gat-sarima-nexus")
LABEL = {"Nexus": "chronos-2", "SARIMA": "sarima_core", "xLSTM": "xlstm", "TimesFM": "timesfm-2.5"}


def region_of(rid: str, resource: str) -> str:
    if resource == "water":
        return "basins"
    return "India" if rid.startswith("IND|") else "US" if rid.startswith("USA|") else "Europe"


def run(run_dir: Path) -> pd.DataFrame:
    fc = pd.read_csv(CORE / "outputs_v2" / "partB" / "per_region_base_forecasts.csv")
    dump = json.load(open(CORE / "work" / "region_series_dump.json"))
    fc["timestamp"] = pd.to_datetime(fc["timestamp"])
    rows, zrows = [], []
    for (res, model), g in fc.groupby(["resource", "model"]):
        recs = []
        for rid, gg in g.groupby("region_id"):
            s = pd.Series(dump[res][rid]["values"], index=pd.to_datetime(dump[res][rid]["index"]), dtype=float)
            first = gg["timestamp"].min()
            sc = mase_scale(s[s.index < first].to_numpy(float))
            for _, r in gg.sort_values("timestamp").iterrows():
                recs.append({"zone_id": rid, "timestamp": r["timestamp"].date(), "actual": s.get(r["timestamp"], np.nan),
                             "mean": r["value"], "mase_scale": sc, "lo": np.nan, "hi": np.nan, "sigma": np.nan})
        df = pd.DataFrame(recs)
        df["h"] = df.groupby("zone_id").cumcount() + 1
        df["region"] = [region_of(z, res) for z in df["zone_id"]]
        name = LABEL[model]
        for reg, d in df.groupby("region"):
            out = run_dir / "forecasts" / name / res
            out.mkdir(parents=True, exist_ok=True)
            d.drop(columns="region").to_csv(out / f"{reg.lower()}__core_cached.csv", index=False)
            rows.append({"model": name, "region": reg, "resource": res, "source": "Co-RE cache outputs_v2/partB",
                         "grain": "Co-RE zone/basin", "n_series": int(d["zone_id"].nunique()), **metrics(d)})
            for z, zz in d.groupby("zone_id"):
                zrows.append({"model": name, "region": reg, "resource": res, "zone_id": z, **metrics(zz)})
    m = run_dir / "metrics"
    m.mkdir(parents=True, exist_ok=True)
    out = pd.DataFrame(rows)
    out.to_csv(m / "core_cached_per_model_per_region.csv", index=False)
    pd.DataFrame(zrows).to_csv(m / "core_cached_per_model_per_zone.csv", index=False)
    return out


if __name__ == "__main__":
    print(run(Path(sys.argv[1])).round(3).to_string(index=False))

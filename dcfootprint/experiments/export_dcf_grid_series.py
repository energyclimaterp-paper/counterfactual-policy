"""Write data/ember/dcfootprint_grid_series_dump.json: the dcfootprint grid for forecast_run_core_grid.py.

Every Ember zone the pipeline reads (io/ember.load_raw: India states, US states, EU-27 countries; EU
converted to GWh and CO2e g/kWh) plus each region's aggregate ('<X> Total'), for electricity (Total
Generation, GWh) and carbon (CO2 intensity), in the same layout as the Co-RE region_series_dump.json.
Series with fewer than 48 months are left out. Also lists the account zones (dcfootprint/outputs/
account_*.parquet) and the aggregates, so the run can score them as separate levels.

Data rule (evidence: the raw Ember Europe file lists EU CO2 intensity as 0.00 for Jan-Apr 2026 while
it already publishes ~390 TWh of fossil generation for those months = emissions not yet published):
trailing months with CO2 intensity exactly 0 are dropped when the same months have positive
generation; each drop is written to `_notes`. Zeros elsewhere (tiny grids) are kept as they are.

Run with the dcfootprint venv from the repo root:
    .venv/Scripts/python.exe dcfootprint/experiments/export_dcf_grid_series.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path[:0] = [str(REPO / "dcfootprint" / "src"), str(HERE)]
from dcfootprint.io import ember  # noqa: E402
from forecast_run import series_panel  # noqa: E402

OUT = REPO / "data" / "ember" / "dcfootprint_grid_series_dump.json"
PREFIX = {"India": "IND|", "US": "USA|", "EU": ""}          # EU countries keep their plain names
ACCOUNT = {"India": "account_facility_month.parquet", "US": "account_us.parquet", "EU": "account_eu.parquet"}
MIN_MONTHS = 48


def main():
    out = {"electricity": {}, "carbon": {}, "_account_zones": [], "_aggregate_zones": [], "_source": {}, "_notes": []}
    for region in ("India", "US", "EU"):
        raw = ember.load_raw(region)
        nat = ember.national_of(raw)
        for res, wide in series_panel(region).items():
            for z in wide.columns:
                s = wide[z].dropna()
                if len(s) < MIN_MONTHS:
                    continue
                zid = PREFIX[region] + z
                out[res][zid] = {"index": [d.strftime("%Y-%m-%d") for d in s.index], "values": [float(v) for v in s.values]}
                if z == nat and zid not in out["_aggregate_zones"]:
                    out["_aggregate_zones"].append(zid)
        out["_account_zones"] += [PREFIX[region] + z for z in
                                  pd.read_parquet(REPO / "dcfootprint" / "outputs" / ACCOUNT[region])["zone_id"].astype(str).unique()]
        out["_source"][region] = str(ember.EMBER_FILES[region])
    for z, v in out["carbon"].items():                        # unpublished-emissions placeholders
        k = 0
        while k < len(v["values"]) and v["values"][-1 - k] == 0:
            k += 1
        if k:
            gen = dict(zip(out["electricity"].get(z, {}).get("index", []), out["electricity"].get(z, {}).get("values", [])))
            dropped = v["index"][-k:]
            if all(gen.get(t, 0) > 0 for t in dropped):
                v["index"], v["values"] = v["index"][:-k], v["values"][:-k]
                out["_notes"].append(f"carbon/{z}: dropped {k} trailing months {dropped[0]}..{dropped[-1]} with CO2 "
                                     f"intensity 0.00 in the raw Ember file while generation is positive "
                                     f"(unpublished-emissions placeholder)")
    json.dump(out, open(OUT, "w"))
    print(f"{OUT}: " + ", ".join(f"{r} {len(out[r])} series" for r in ("electricity", "carbon")))
    print(f"account zones {len(out['_account_zones'])}, aggregates {out['_aggregate_zones']}")
    print("\n".join(out["_notes"]) or "no placeholder months dropped")


if __name__ == "__main__":
    main()

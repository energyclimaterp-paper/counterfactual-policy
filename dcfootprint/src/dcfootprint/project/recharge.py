"""L3 — seasonal recharge R-hat for the routing basin queues.

G3P ends 2023-09, so R-hat is a monthly recharge *climatology*: the mean of
positive month-over-month TWS change across the major Indian river basins, made
into a normalised seasonal multiplier (mean 1.0) with a bootstrap band. Labelled
an estimate, not an observation (v2 L3). It gives the queues a physically sensible
seasonal shape (monsoon high, dry-season low); routing results are conditional on it.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from dcfootprint.io.facilities import _repo_root

# major Indian-subcontinent basins present in the G3P river-basin file
_INDIAN_BASINS = ["Ganges", "Godavari", "Krishna", "Mahanadi River (Mahahadi)", "Brahmaputra"]


def recharge_climatology(n_boot: int = 500, seed: int = 0) -> pd.DataFrame:
    """[month(1-12), recharge_mult, lo, hi] — normalised seasonal recharge profile."""
    path = _repo_root() / "data" / "g3p" / "G3P_v1.12_tws_rivbas.csv"
    raw = pd.read_csv(path)
    sub = pd.DataFrame({"date": pd.to_datetime(raw["time [yyyy-mm-dd]"])})   # small clean frame (no fragmentation)
    sub["month"] = sub["date"].dt.month
    present = [b for b in _INDIAN_BASINS if f"{b} [mm]" in raw.columns]
    for b in present:
        sub[b] = raw[f"{b} [mm]"].values
    sub = sub.sort_values("date").reset_index(drop=True)

    monthly = []
    for b in present:
        d = sub[b].diff().clip(lower=0)                    # positive TWS change = recharge
        monthly.append(d.groupby(sub["month"]).mean())
    clim = pd.concat(monthly, axis=1).mean(axis=1)        # avg across basins
    clim = clim / clim.mean()                             # normalise to mean 1.0 (a multiplier)

    rng = np.random.default_rng(seed)
    arr = pd.concat(monthly, axis=1).values               # month x basin
    boot = []
    for _ in range(n_boot):
        idx = rng.integers(0, arr.shape[1], arr.shape[1])
        m = np.nanmean(arr[:, idx], axis=1)
        boot.append(m / np.nanmean(m))
    boot = np.array(boot)
    return pd.DataFrame({
        "month": clim.index.astype(int),
        "recharge_mult": clim.values,
        "lo": np.nanpercentile(boot, 10, axis=0),
        "hi": np.nanpercentile(boot, 90, axis=0),
    })


if __name__ == "__main__":
    r = recharge_climatology()
    print("seasonal recharge multiplier (mean=1.0):")
    print(r.round(2).to_string(index=False))
    print(f"\npeak month: {int(r.loc[r['recharge_mult'].idxmax(),'month'])}  "
          f"trough month: {int(r.loc[r['recharge_mult'].idxmin(),'month'])}")

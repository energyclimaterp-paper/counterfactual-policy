"""L8 — Monte-Carlo uncertainty over the modelled parameter bands.

Absolute footprints rest on util/PUE/WUE/EWIF assumptions (red-team R1), so we
propagate their bands to confidence intervals on the totals, and report a simple
one-at-a-time sensitivity (which parameter drives the spread). Analytic scaling of
the account components (fast, exact) rather than re-running the whole pipeline:
  carbon    ~ util * pue
  onsite W  ~ util * wue
  grid  W   ~ util * pue * ewif
(SALib/Sobol not installed -> one-at-a-time variance contribution instead.)
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# relative multiplier ranges = band / default, from parameters.yaml
_RANGES = {
    "util": (0.30 / 0.45, 0.65 / 0.45),
    "pue": (1.4 / 1.6, 1.9 / 1.6),
    "wue": (0.7 / 1.9, 9.0 / 1.9),      # very wide -> expected to dominate water spread
    "ewif": (0.8, 1.2),
    "inference": (0.80 / 0.85, 0.90 / 0.85),
}


def _components(account: pd.DataFrame) -> dict:
    a = account
    return {
        "carbon": float(a["carbon_tco2"].sum()),
        "onsite": float(a["water_onsite_l"].sum() / 1000.0),
        "grid": float(a["water_grid_l"].sum() / 1000.0),
        "sc_onsite": float((a["water_onsite_l"] * a["cf"]).sum() / 1000.0),
        "sc_grid": float((a["water_grid_l"] * a["cf"]).sum() / 1000.0),
    }


def _totals(b: dict, u, p, w, e, i):
    carbon = b["carbon"] * u * p
    phys = b["onsite"] * u * w + b["grid"] * u * p * e
    scarcity = b["sc_onsite"] * u * w + b["sc_grid"] * u * p * e
    return carbon, phys, scarcity


def monte_carlo(account: pd.DataFrame, n: int = 2000, seed: int = 0) -> dict:
    b = _components(account)
    rng = np.random.default_rng(seed)
    s = {k: rng.uniform(*v, n) for k, v in _RANGES.items()}
    carbon, phys, scarcity = _totals(b, s["util"], s["pue"], s["wue"], s["ewif"], s["inference"])

    def ci(x):
        return {"mean": round(float(np.mean(x)), 0),
                "p05": round(float(np.percentile(x, 5)), 0),
                "p95": round(float(np.percentile(x, 95)), 0)}

    # one-at-a-time sensitivity on scarcity-weighted water (vary one, others=1.0)
    sens = {}
    base_args = {"u": 1.0, "p": 1.0, "w": 1.0, "e": 1.0, "i": 1.0}
    for k, (lo, hi) in _RANGES.items():
        _, _, s_lo = _totals(b, **{**base_args, **_map(k, lo)})
        _, _, s_hi = _totals(b, **{**base_args, **_map(k, hi)})
        sens[k] = round(abs(s_hi - s_lo) / 1e6, 1)      # Mm3-eq swing
    return {
        "carbon_tco2_yr": ci(carbon),
        "water_phys_m3_yr": ci(phys),
        "scarcity_m3eq_yr": ci(scarcity),
        "scarcity_sensitivity_Mm3eq_swing": dict(sorted(sens.items(), key=lambda kv: -kv[1])),
    }


def _map(param, val):
    return {"u": val if param == "util" else 1.0, "p": val if param == "pue" else 1.0,
            "w": val if param == "wue" else 1.0, "e": val if param == "ewif" else 1.0,
            "i": val if param == "inference" else 1.0}


if __name__ == "__main__":
    from dcfootprint.io.facilities import _repo_root
    acct = pd.read_parquet(_repo_root() / "dcfootprint" / "outputs" / "account_facility_month.parquet")
    r = monte_carlo(acct)
    for k, v in r.items():
        print(k, "=", v)

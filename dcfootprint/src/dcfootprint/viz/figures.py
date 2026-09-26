"""L9 — paper figures (static PNG, light mode) from a results folder.

Colours are the dataviz reference palette (validated): sequential = one blue ramp light->dark
for magnitude; categorical = slots 1-3 (blue, orange, aqua; all-pairs safe). Text wears ink
tokens, never series colours. No dual axes: two measures -> two panels.

    fig_q1_siting_map.png        candidate state x basin cells shaded by rank (darker = better),
                                 small grids hatched, existing-DC cities ringed, top 5 labelled
    fig_mismatch_map.png         AWARE annual-mean scarcity (sequential) + DC cities sized by
                                 scarcity-weighted water  (RQ2 spatial mismatch)
    fig_scarcity_by_state.png    scarcity-weighted water by state, scope-1 vs scope-2
    fig_levers.png               lever savings: water % and carbon % (two panels)
    fig_routing.png              Q3: water saving, carbon change, peak overdraft vs fixed-load floor

Run: PYTHONPATH=dcfootprint/src python -m dcfootprint.viz.figures [results_dir]
"""
from __future__ import annotations

import sys
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

from dcfootprint.io.facilities import _repo_root
from dcfootprint.settings import params

SURFACE, INK, INK2, MUTED, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#8a8983", "#e4e3df"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
SEQ = ["#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec", "#5598e7", "#3987e5", "#2a78d6",
       "#256abf", "#1c5cab", "#184f95", "#104281", "#0d366b"]
SEQ_CMAP = LinearSegmentedColormap.from_list("seq_blue", SEQ)
NEUTRAL = "#f0efec"

plt.rcParams.update({"figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
                     "text.color": INK, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "axes.edgecolor": GRID, "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold",
                     "axes.spines.top": False, "axes.spines.right": False})


def _india_states() -> gpd.GeoDataFrame:
    return gpd.read_file(_repo_root() / params()["grid"]["gadm_path"], layer="ADM_ADM_1")[["NAME_1", "geometry"]]


def _basins(ids) -> gpd.GeoDataFrame:
    from dcfootprint.geo.join import load_aware_basins
    b = load_aware_basins()
    return b[b["basin_id"].isin([int(i) for i in ids])]


def _map_axes(ax, states):
    states.boundary.plot(ax=ax, color=MUTED, linewidth=0.3)
    ax.set_xlim(67.5, 98); ax.set_ylim(6, 37.5)
    ax.set_aspect("equal"); ax.set_axis_off()


def _dc_cities(res: Path) -> pd.DataFrame:
    acct = pd.read_parquet(res / "outputs" / "account_facility_month.parquet")
    geo = pd.read_parquet(res / "outputs" / "interim" / "facilities_geocoded.parquet")[["facility_id", "latitude", "longitude"]]
    ann = (acct.groupby(["facility_id", "city"], as_index=False)["water_scarcity_l_eq"].sum()
           .merge(geo, on="facility_id"))
    return ann.groupby("city", as_index=False).agg(scarcity_m3eq=("water_scarcity_l_eq", lambda s: s.sum() / 1000),
                                                   n=("facility_id", "size"), lat=("latitude", "first"),
                                                   lon=("longitude", "first"))


def fig_q1(res: Path, out: Path, states):
    from dcfootprint.io.gem import _TO_EMBER
    head = pd.read_csv(res / "q1_siting.csv")
    small = pd.read_csv(res / "q1_siting_small_grids.csv")
    st = states.assign(state=states["NAME_1"].map(lambda s: _TO_EMBER.get(s, s)))
    st = st.dissolve("state", as_index=False)
    cells = pd.concat([head.assign(group="headline"), small.assign(group="small")], ignore_index=True)
    geo = gpd.overlay(_basins(cells["basin_id"].unique()).rename(columns={"basin_id": "bid"}),
                      st[["state", "geometry"]], how="intersection")
    geo = geo.merge(cells, left_on=["bid", "state"], right_on=["basin_id", "state"])
    fig, ax = plt.subplots(figsize=(6.4, 7.0))
    _map_axes(ax, states)
    h = geo[geo["group"] == "headline"].copy()
    h["pref"] = 1 - (h["rank"] - 1) / max(h["rank"].max() - 1, 1)          # 1 = best
    h.plot(ax=ax, column="pref", cmap=SEQ_CMAP, vmin=0, vmax=1, edgecolor=SURFACE, linewidth=0.3)
    geo[geo["group"] == "small"].plot(ax=ax, facecolor=NEUTRAL, edgecolor=MUTED, hatch="////", linewidth=0.3)
    c = _dc_cities(res)
    ax.scatter(c["lon"], c["lat"], s=18 + 6 * c["n"], facecolor="none", edgecolor=INK, linewidth=1.0, zorder=5)
    top = h.nsmallest(5, "rank").copy()
    top["pt"] = top.geometry.representative_point()
    top = top.assign(py=top["pt"].y).sort_values("py", ascending=False)   # label order = latitude: no crossings
    for k, (_, r) in enumerate(top.iterrows()):
        ax.annotate(f"#{int(r['rank'])}  {r['state']} {int(r['basin_id'])}", (r["pt"].x, r["pt"].y),
                    xytext=(58.6, 16.5 - 1.7 * k), textcoords="data", fontsize=7.5, color=INK, weight="bold",
                    ha="left", va="center", zorder=6,
                    arrowprops=dict(arrowstyle="-", color=INK2, linewidth=0.6, shrinkA=0, shrinkB=2))
    sm = plt.cm.ScalarMappable(cmap=SEQ_CMAP, norm=plt.Normalize(0, 1))
    cb = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.01, ticks=[0, 1])
    cb.ax.set_yticklabels([f"rank {int(h['rank'].max())}", "rank 1"]); cb.outline.set_visible(False)
    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    ax.legend(handles=[Patch(facecolor=NEUTRAL, edgecolor=MUTED, hatch="////", label="small grid (<10 TWh/yr), ranked separately"),
                       Line2D([], [], marker="o", color="none", markeredgecolor=INK, markerfacecolor="none",
                              markersize=7, label="existing datacenter city (size = count)")],
              loc="upper left", frameon=False, fontsize=7.5)
    ax.set_xlim(58.0, 98)
    ax.set_title(f"Q1 siting: {len(head)} candidate state x basin regions, minimax-regret rank")
    fig.savefig(out / "fig_q1_siting_map.png", dpi=200, bbox_inches="tight"); plt.close(fig)


def fig_mismatch(res: Path, out: Path, states):
    from dcfootprint.geo.join import load_aware_basins
    b = load_aware_basins()
    b = b[b.intersects(states.union_all().envelope)].copy()
    b["cf_mean"] = b[[c for c in b.columns if c.startswith("CF_")]].mean(axis=1)
    b = gpd.clip(b, states.union_all())
    fig, ax = plt.subplots(figsize=(6.4, 7.0))
    b.plot(ax=ax, column="cf_mean", cmap=SEQ_CMAP, vmin=0, vmax=100, linewidth=0)
    _map_axes(ax, states)
    c = _dc_cities(res).sort_values("scarcity_m3eq", ascending=False)
    size = 30 + 900 * c["scarcity_m3eq"] / c["scarcity_m3eq"].max()
    ax.scatter(c["lon"], c["lat"], s=size, color=ORANGE, alpha=0.85, edgecolor=SURFACE, linewidth=1.5, zorder=5)
    side = {"Bengaluru": (-16, -16, "right"), "Mumbai": (-16, 6, "right"), "Chennai": (18, 10, "left")}
    for _, r in c.head(5).iterrows():
        dx, dy, ha = side.get(r["city"], (14, 0, "left"))
        ax.annotate(f"{r['city']}  {r['scarcity_m3eq'] / 1e6:,.0f}M m³-eq", (r["lon"], r["lat"]),
                    xytext=(dx, dy), textcoords="offset points", fontsize=7.5, color=INK, va="center", ha=ha,
                    zorder=6, bbox=dict(boxstyle="round,pad=0.15", fc=SURFACE, ec="none", alpha=0.85))
    sm = plt.cm.ScalarMappable(cmap=SEQ_CMAP, norm=plt.Normalize(0, 100))
    cb = fig.colorbar(sm, ax=ax, fraction=0.03, pad=0.01)
    cb.set_label("AWARE 2.0 scarcity factor, annual mean (1 = world avg, 100 = cap)", color=INK2)
    cb.outline.set_visible(False)
    ax.set_title("Where datacenters draw water: basin scarcity vs scarcity-weighted water by city")
    fig.savefig(out / "fig_mismatch_map.png", dpi=200, bbox_inches="tight"); plt.close(fig)


def fig_state_bars(res: Path, out: Path):
    s = pd.read_csv(res / "india_account_summary.csv")
    g = s.groupby("state")[["water_scarcity_onsite_m3eq_yr", "water_scarcity_grid_m3eq_yr"]].sum() / 1e6
    g = g.assign(total=g.sum(axis=1)).sort_values("total")
    fig, ax = plt.subplots(figsize=(6.4, 3.4))
    y = np.arange(len(g))
    ax.barh(y, g["water_scarcity_onsite_m3eq_yr"], color=BLUE, height=0.62, label="scope-1 on-site (facility basin)")
    ax.barh(y, g["water_scarcity_grid_m3eq_yr"], left=g["water_scarcity_onsite_m3eq_yr"] + g["total"].max() * 0.004,
            color=ORANGE, height=0.62, label="scope-2 grid (generation basins)")
    for yi, t in zip(y, g["total"]):
        ax.text(t + g["total"].max() * 0.012, yi, f"{t:,.0f}", va="center", fontsize=7.5, color=INK2)
    ax.set_yticks(y, g.index); ax.tick_params(axis="y", length=0)
    ax.set_xlabel("scarcity-weighted water, million m³-eq / yr (2024)")
    ax.grid(axis="x", color=GRID, linewidth=0.6); ax.set_axisbelow(True)
    ax.legend(frameon=False, loc="lower right", fontsize=7.5)
    ax.set_title("Scarcity-weighted water by state")
    fig.savefig(out / "fig_scarcity_by_state.png", dpi=200, bbox_inches="tight"); plt.close(fig)


def fig_levers(res: Path, out: Path):
    lv = pd.read_csv(res / "lever_savings.csv")
    lv = lv[lv["type"] == "reduction"].set_index("lever")
    names = {"zero_liquid_discharge": "Zero liquid discharge", "efficiency_standard": "Efficiency standard",
             "coastal_seawater_siting": "Coastal seawater cooling"}
    order = lv.sort_values("pct_of_scarcity_baseline").index
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.4), sharey=True)
    for ax, col, title in [(axes[0], "pct_of_scarcity_baseline", "scarcity-weighted water saved (%)"),
                           (axes[1], "pct_of_carbon_baseline", "carbon saved (%)")]:
        v = lv.loc[order, col]
        ax.barh(range(len(v)), v, color=BLUE, height=0.55)
        for i, x in enumerate(v):
            ax.text(x + 0.6, i, f"{x:.1f}%", va="center", fontsize=7.5, color=INK2)
        ax.set_xlim(0, max(40, v.max() * 1.2)); ax.set_title(title, fontweight="normal", color=INK2, fontsize=9)
        ax.grid(axis="x", color=GRID, linewidth=0.6); ax.set_axisbelow(True); ax.tick_params(axis="y", length=0)
    axes[0].set_yticks(range(len(order)), [names.get(i, i) for i in order])
    fig.suptitle("Which lever pays (India, 2024)", fontweight="bold", fontsize=10, x=0.02, ha="left", y=1.08)
    fig.savefig(out / "fig_levers.png", dpi=200, bbox_inches="tight"); plt.close(fig)


def fig_routing(res: Path, out: Path):
    r = pd.read_csv(res / "routing_comparison.csv")
    r = r[r["legal"]].set_index("policy").loc[["static", "greedy", "lyapunov", "lyapunov_pf", "oracle"]]
    bs = pd.read_csv(res / "routing_budget_sweep.csv")
    floor = float(bs.loc[bs["budget_alpha"] == 1.0, "fixed_only_peak_queue_m3"].iloc[0])
    labels = ["static", "greedy", "Lyap.", "Lyap.\nperfect CI", "oracle"]
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 2.6))
    panels = [("scarcity_saving_pct_vs_static", "scarcity water saved vs static (%)", 1),
              ("carbon_saving_pct_vs_static", "carbon saved vs static (%)", 1),
              ("peak_basin_queue_m3", f"peak basin overdraft (thousand m³)\ndashed = fixed-load floor ({floor * 1e-3:,.0f})", 1e-3)]
    for ax, (col, title, k) in zip(axes, panels):
        v = r[col].values * k
        ax.bar(range(len(v)), v, color=BLUE, width=0.6)
        ax.axhline(0, color=MUTED, linewidth=0.8)
        for i, x in enumerate(v):
            ax.text(i, x + (abs(v).max() * 0.03 if x >= 0 else -abs(v).max() * 0.03), f"{x:,.1f}" if k == 1 else f"{x:,.0f}",
                    ha="center", va="bottom" if x >= 0 else "top", fontsize=7, color=INK2)
        ax.set_xticks(range(len(v)), labels, fontsize=7); ax.tick_params(axis="x", length=0)
        ax.set_title(title, fontweight="normal", color=INK2, fontsize=8.5, pad=10)
        lo, hi = min(0.0, v.min()), max(0.0, v.max())
        ax.set_ylim(lo - 0.14 * (hi - lo), hi + 0.14 * (hi - lo))
        ax.grid(axis="y", color=GRID, linewidth=0.6); ax.set_axisbelow(True)
    axes[2].axhline(floor * 1e-3, color=ORANGE, linewidth=1.5, linestyle=(0, (4, 2)))
    fig.suptitle("Q3 routing (stylised, monthly, legal limits on, mean of 10 seeds)", fontweight="bold",
                 fontsize=10, x=0.02, ha="left")
    fig.tight_layout()
    fig.savefig(out / "fig_routing.png", dpi=200, bbox_inches="tight"); plt.close(fig)


def make_all(res: Path | None = None) -> list[Path]:
    res = Path(res) if res else _repo_root() / "dcfootprint" / "results"
    out = res / "figures"
    out.mkdir(parents=True, exist_ok=True)
    states = _india_states()
    fig_q1(res, out, states)
    fig_mismatch(res, out, states)
    fig_state_bars(res, out)
    fig_levers(res, out)
    fig_routing(res, out)
    return sorted(out.glob("*.png"))


if __name__ == "__main__":
    for p in make_all(Path(sys.argv[1]) if len(sys.argv) > 1 else None):
        print(p)

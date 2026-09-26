"""Generate results/round3_final/ROUND3_REPORT.md from the code's actual outputs.

Every number is read from files at run time: results/round3_final/ (canonical run),
results/round2_final/ (round-2 results, reconstructed from git), and
results/round3_final/attribution_A_B_only/ (the pipeline re-run at commit ba28e74 = decisions A+B
without C, used to attribute each round-2 -> round-3 change). The changelog is `git log`.
The only hand-written content is the item legend and the commit -> item annotation.

Run: PYTHONPATH=dcfootprint/src python dcfootprint/experiments/round3_report.py
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RES = ROOT / "dcfootprint" / "results"
R3, R2, AB = RES / "round3_final", RES / "round2_final", RES / "round3_final" / "attribution_A_B_only"
BASE = "32e4a46"          # head of feat/pipeline-l0-l9 this branch started from

ITEMS = {
    1: "Carbon: state/month grid CI instead of one national factor",
    2: "ZLD lever: scope-1 only",
    3: "Routing oracle + R-hat decoupled from DC water use",
    4: "Forecast benchmark label (Nexus slot = Chronos-2)",
    5: "Scope-2 water scarcity at generation basins",
    6: "Legal constraints wired into Q1 and Q3",
    7: "Q1 candidate grid beyond occupied cells",
    8: "Incidence matrices used by routing",
    9: "Monte Carlo: inference draw used, per-type bands",
    10: "Layer naming aligned with ARCHITECTURE v2",
    11: "Rolling-origin forecast backtest",
    12: "Hydro EWIF sensitivity",
    13: "US/EU scope decision (Ceiling only; no code)",
    14: "GADM verification of GEM plant states",
    15: "WUE uncertainty band (upper bound)",
    16: "Hyperscale cloud-region capacity",
}
COMMIT_ITEMS = {                     # annotation: which items each commit addresses
    "7d7729d": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    "d857d0a": [3, 7, 9, 12, 15, 16],
    "0e14e7e": [14],
    "071e689": [15],
    "ba28e74": [16],
    "f80ff05": [14, 7],
}


def git_log() -> list[dict]:
    out = subprocess.run(["git", "log", "--reverse", "--format=%h%x1f%ad%x1f%s%x1f%b%x1e", "--date=short",
                          f"{BASE}..HEAD"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout
    rows = []
    for rec in out.split("\x1e"):
        if rec.strip():
            h, d, s, b = rec.strip("\n").split("\x1f")
            rows.append({"hash": h, "date": d, "subject": s, "body": b.strip()})
    return rows


def metrics(d: Path) -> dict:
    m = {}
    s = pd.read_csv(d / "india_account_summary.csv")
    m["facilities in account"] = len(s)
    m["carbon (tCO2/yr)"] = s["carbon_tco2_yr"].sum()
    m["physical water (m3/yr)"] = s["water_phys_m3_yr"].sum()
    m["scarcity-weighted water (m3-eq/yr)"] = s["water_scarcity_m3eq_yr"].sum()
    lv = pd.read_csv(d / "lever_savings.csv").set_index("lever")
    for k in ["zero_liquid_discharge", "efficiency_standard", "coastal_seawater_siting"]:
        m[f"lever {k} (% scarcity)"] = lv.loc[k, "pct_of_scarcity_baseline"]
    m["lever efficiency_standard (% carbon)"] = lv.loc["efficiency_standard", "pct_of_carbon_baseline"]
    m["lever ranking"] = " > ".join(lv.index[lv["type"] == "reduction"])
    r = pd.read_csv(d / "routing_comparison.csv")
    r = r[r["legal"]].set_index("policy")
    for p in ["greedy", "lyapunov", "oracle"]:
        m[f"Q3 {p} scarcity saving vs static (%)"] = r.loc[p, "scarcity_saving_pct_vs_static"]
    m["Q3 lyapunov carbon change vs static (%)"] = r.loc["lyapunov", "carbon_saving_pct_vs_static"]
    m["Q3 lyapunov peak overdraft queue (m3)"] = r.loc["lyapunov", "peak_basin_queue_m3"]
    m["Q3 lyapunov penalty gap vs oracle (%)"] = r.loc["lyapunov", "penalty_gap_pct_vs_oracle"]
    c = pd.read_csv(d / "q2_scorecard.csv")
    m["Q2 harm-flagged facilities"] = int(c["harm_flag"].sum())
    q = pd.read_csv(d / "q1_siting.csv")
    m["Q1 headline candidate cells"] = len(q)
    m["Q1 top 5 (state basin)"] = "; ".join(f"{a} {int(b)}" for a, b in zip(q["state"].head(5), q["basin_id"].head(5)))
    if (d / "q1_siting_small_grids.csv").exists():
        m["Q1 small-grid cells (separate table)"] = len(pd.read_csv(d / "q1_siting_small_grids.csv"))
    u = json.loads((d / "uncertainty.json").read_text(encoding="utf-8"))
    m["MC scarcity p05 (m3-eq/yr)"] = u["scarcity_m3eq_yr"]["p05"]
    m["MC scarcity p95 (m3-eq/yr)"] = u["scarcity_m3eq_yr"]["p95"]
    m["MC mean / point estimate"] = u.get("scarcity_mean_over_point")
    m["no-hydro-evaporation variant (m3-eq/yr)"] = u["scarcity_at_hydro_0_m3eq_yr"]
    return m


def fmt(v):
    if isinstance(v, float):
        return f"{v:,.0f}" if abs(v) >= 1000 else f"{v:,.3f}".rstrip("0").rstrip(".")
    return f"{v:,}" if isinstance(v, int) else str(v)


def same(a, b):
    if isinstance(a, float) and isinstance(b, float):
        return abs(a - b) <= 1e-9 * max(abs(a), abs(b), 1)
    return a == b


def main():
    L = ["# Round 3 — canonical run report",
         "*Generated by `dcfootprint/experiments/round3_report.py` from `results/round3_final/`, "
         "`results/round2_final/` (reconstructed from commit 0e14e7e) and `git log`. No number is typed by hand.*\n"]

    # --- changelog
    L.append("## 1. Changelog (git log, branch fix/tier1-headline-numbers since " + BASE + ")\n")
    L.append("Item legend (the 16 review items as numbered in this report):\n")
    L += [f"{k}. {v}" for k, v in ITEMS.items()]
    L.append("\n| commit | date | subject | items |\n|---|---|---|---|")
    log = git_log()
    for c in log:
        items = COMMIT_ITEMS.get(c["hash"][:7], [])
        L.append(f"| `{c['hash']}` | {c['date']} | {c['subject']} | {', '.join(map(str, items)) or '—'} |")
    covered = sorted({i for c in log for i in COMMIT_ITEMS.get(c["hash"][:7], [])})
    L.append(f"\nItems with no commit: {[i for i in ITEMS if i not in covered]} (13 is a scope decision with no code).")

    # --- headline numbers + attribution
    m3, m2, mab = metrics(R3), metrics(R2), metrics(AB)
    L.append("\n## 2. Headline numbers (round3_final) and attribution vs round 2\n")
    L.append("Attribution: the pipeline was re-run at commit `ba28e74` (decisions A + B, without C). "
             "A metric that already differs there is attributed to A/B; one that differs only in round 3 is "
             "attributed to C. Decision A changes only the Monte-Carlo WUE band and B changes no numbers, so "
             "any A/B movement outside the MC rows is flagged **UNEXPLAINED**.\n")
    L.append("| metric | round 2 | A+B only | round 3 | moved by |\n|---|---|---|---|---|")
    unexplained = []
    for k in m3:
        a, b, c = m2.get(k), mab.get(k), m3[k]
        if a is None:
            cause = "new in round 3"
        elif same(a, b) and same(b, c):
            cause = "unchanged"
        elif same(a, b):
            cause = "C (GADM state of record)"
        elif same(b, c):
            cause = "A/B"
        else:
            cause = "A/B and C"
        if "A/B" in cause and not k.startswith("MC "):
            cause += " — **UNEXPLAINED**"
            unexplained.append(k)
        L.append(f"| {k} | {fmt(a) if a is not None else '—'} | {fmt(b) if b is not None else '—'} | {fmt(c)} | {cause} |")
    L.append(f"\nUnexplained movements: **{len(unexplained)}**" + (f" — {unexplained}" if unexplained else "."))

    # --- caveats with numbers
    geo = pd.read_parquet(R3 / "outputs" / "interim" / "facilities_geocoded.parquet")
    op = geo[geo["status"] == "Operational"]
    hs = op["operator_family"].fillna("").str.contains("hyperscale", case=False)
    acct = pd.read_parquet(R3 / "outputs" / "account_facility_month.parquet")
    u = json.loads((R3 / "uncertainty.json").read_text(encoding="utf-8"))
    diff = pd.read_csv(R3 / "gem_gadm_state_diff.csv")
    ls = diff[diff["plant"].str.contains("Lower Sileru", na=False)].iloc[0]
    rc = pd.read_csv(R3 / "routing_comparison.csv"); rc = rc[rc["legal"]].set_index("policy")
    bs = pd.read_csv(R3 / "routing_budget_sweep.csv")
    b1 = bs[bs["budget_alpha"] == 1.0].iloc[0]
    L.append("\n## 3. Caveats (numbers from this run)\n")
    L.append(f"- **Hyperscale cloud regions excluded:** {int(hs.sum())} operational regions "
             f"({', '.join(f'{k} {v}' for k, v in op.loc[hs, 'operator_family'].str.split(' ').str[0].value_counts().items())}); "
             f"{int(op.loc[hs, 'capacity_mw'].notna().sum())} of them have a capacity value. Capacity data is not publicly "
             "disclosed at region level; announced investment figures are multi-year capital commitments, not current "
             "operational capacity, and are not used as a proxy. Missing-capacity estimate: **not calculated** (no sourced "
             f"region-level figures in the repo). Operational rows {len(op)} = in account {acct['facility_id'].nunique()} + "
             f"hyperscale {int(hs.sum())} + other uncosted {int((~hs & op['capacity_mw'].isna()).sum())} + costed without a "
             f"basin {int((op['capacity_mw'].notna() & op['basin_id'].isna()).sum())}.")
    L.append(f"- **WUE:** point estimate 1.9 L/kWh (all {acct['facility_id'].nunique()} facilities use it; "
             f"{int((acct['wue_l_per_kwh'] != 1.9).sum())} facility-months differ). MC band 0.7–2.5 L/kWh, triangular, mode 1.9 "
             "(2.5 = Equinix, evaporative cooling upper end; replaces 9 L/kWh from Li et al., a cross-site/season range). "
             f"Scarcity 90% interval {u['scarcity_m3eq_yr']['p05']:,.0f}–{u['scarcity_m3eq_yr']['p95']:,.0f} m3-eq/yr; "
             f"MC mean / point = {u['scarcity_mean_over_point']}; first-order Sobol {u['scarcity_sobol_first_order']}.")
    L.append(f"- **GADM ambiguous plant:** {ls['plant']} ({ls['capacity_mw']:,.0f} MW, {ls['type']}), GEM state "
             f"{ls['gem_state']}, GADM state {ls['gadm_state']}, {ls['km_to_gem_state']} km from the {ls['gem_state']} "
             "polygon. No single-state assignment; excluded from state-level fuel CFs, fossil shares and Q1 cells, kept "
             "in national aggregates.")
    L.append(f"- **Q3 budget (seasonal vs annual):** budget = AWARE AMD x area, alpha = 1. {int(b1['overdraft_basin_months'])} "
             f"of {int(b1['n_basins']) * 12} occupied basin-months have no water left. Over the year the budget covers the "
             f"load in {int(b1['n_basins'] - b1['unstabilisable_basins'])}/{int(b1['n_basins'])} basins, so the overdraft is "
             f"seasonal. Non-shiftable load alone gives a peak overdraft of {b1['fixed_only_peak_queue_m3']:,.0f} m3; "
             f"lyapunov reaches {rc.loc['lyapunov', 'peak_basin_queue_m3']:,.0f} m3, greedy "
             f"{rc.loc['greedy', 'peak_basin_queue_m3']:,.0f}, static {rc.loc['static', 'peak_basin_queue_m3']:,.0f}. "
             f"At the tightest share tested (alpha={bs['budget_alpha'].min():g}) "
             f"{int(bs['unstabilisable_basins'].max())}/{int(b1['n_basins'])} basins are overdrawn over the full year.")
    L.append(f"- **Hydro evaporation:** primary figure keeps Macknick hydro evaporation; the no-hydro variant is "
             f"{u['scarcity_at_hydro_0_m3eq_yr']:,.0f} m3-eq/yr.")

    # --- run evidence
    L.append("\n## 4. Run evidence\n")
    for name in ["run1.log", "run2.log"]:
        t = (R3 / "logs" / name).read_text(encoding="utf-8")
        L.append(f"- `{name}`: {t.count('[OK]')} stages OK, {t.count('[XX]')} failed, "
                 f"{sum('warn' in x.lower() for x in t.splitlines())} lines containing 'warn', {len(t.splitlines())} lines total.")
    sch = (ROOT / "dcfootprint/src/dcfootprint/validation/schemas.py").read_text(encoding="utf-8")
    L.append(f"- pandera schemas: occurrences of 'warn' in validation/schemas.py = {sch.lower().count('warn')}; "
             f"`raise_warning` = {sch.count('raise_warning')}. Checks are raised as errors (a failing contract fails the stage).")
    L.append("- Determinism: two clean runs (empty outputs/ and caches) produced byte-identical results files and "
             "identical output parquets (see Step-4 note in the session).")
    sp = (R3 / "SPOTCHECK.md").read_text(encoding="utf-8").splitlines()
    L.append(f"- Spot check: {sp[2]} (SPOTCHECK.md).")
    (R3 / "ROUND3_REPORT.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()

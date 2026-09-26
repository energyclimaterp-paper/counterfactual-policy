"""End-to-end pipeline: runs L0->L9 in order, validates, and writes every output
to dcfootprint/results/ + a combined RESULTS_FULL.md. Each stage is isolated, so a
failure is reported (with its traceback) without aborting the rest; a status table
prints at the end. This is the deterministic core; forecasting is real (SARIMA vs
seasonal-naive) and Q3 routing is the stylised Lyapunov controller (Ceiling).

Run:  PYTHONPATH=dcfootprint/src python -m dcfootprint.pipeline
"""
from __future__ import annotations

import traceback
from pathlib import Path

import pandas as pd

from dcfootprint.io.facilities import _repo_root

ROOT = _repo_root()
INTERIM = ROOT / "dcfootprint" / "outputs" / "interim"
OUT = ROOT / "dcfootprint" / "outputs"
RES = ROOT / "dcfootprint" / "results"


def run() -> dict:
    INTERIM.mkdir(parents=True, exist_ok=True)
    RES.mkdir(parents=True, exist_ok=True)
    status, art = [], {}

    def stage(name, fn):
        try:
            art[name] = fn()
            status.append((name, "OK"))
        except Exception as e:
            status.append((name, f"FAIL: {type(e).__name__}: {e}"))
            traceback.print_exc()
            art[name] = None
        return art[name]

    # --- L0/L1: facility spine + geo join ---
    def _spine():
        from dcfootprint.io import facilities as fac_io
        from dcfootprint.geo import join as gj
        fac = fac_io.build()
        fac.to_parquet(INTERIM / "facilities.parquet")
        basins = gj.load_aware_basins()
        cf = gj.basin_monthly_cf(basins)
        cf.to_parquet(INTERIM / "basin_cf_monthly.parquet")
        fac_geo = gj.assign_zone_and_basin(fac)
        fac_geo.to_parquet(INTERIM / "facilities_geocoded.parquet")
        return fac_geo
    fac_geo = stage("L0/L1 facilities+geo", _spine)

    # --- L2: account ---
    def _account():
        from dcfootprint.account import build
        acct = build.facility_month_account()
        acct.to_parquet(OUT / "account_facility_month.parquet")
        return acct
    account = stage("L2 account", _account)

    # --- L1.5/L2.5 incidence + calibration ---
    stage("L1 incidence", lambda: __import__("dcfootprint.geo.incidence", fromlist=["build_incidence"]).build_incidence(fac_geo))
    cal = stage("L2.5 calibrate", lambda: __import__("dcfootprint.account.calibrate", fromlist=["calibrate_capacity"]).calibrate_capacity(fac_geo))

    # --- L3 forecast + recharge ---
    def _forecast():
        from dcfootprint.project import forecast
        r = forecast.forecast_ci(); r["forecast"].to_csv(RES / "forecast_ci.csv", index=False)
        r["core_benchmark"] = forecast.core_benchmark()
        return r
    fc = stage("L3 forecast", _forecast)
    rech = stage("L3 recharge", lambda: __import__("dcfootprint.project.recharge", fromlist=["recharge_climatology"]).recharge_climatology())

    # --- L4 counterfactual levers ---
    def _levers():
        from dcfootprint.counterfactual import levers
        lv = levers.rank_lever_savings(); lv.to_csv(RES / "lever_savings.csv", index=False); return lv
    levers_df = stage("L4 counterfactual", _levers)

    # --- L5 policy-gap ---
    def _policy():
        from dcfootprint.policy import gap
        gap.four_axis_matrix().to_csv(RES / "regulation_matrix.csv", index=False)
        gap.HARD_CONSTRAINTS.to_csv(RES / "regulation_constraints.csv", index=False)
        return gap.gap_overlay(account)
    gap_overlay = stage("L5 policy-gap", _policy)

    # --- L6 routing (Q3) ---
    def _routing():
        from dcfootprint.routing import lyapunov
        r = lyapunov.compare(account, seeds=8); r.to_csv(RES / "routing_comparison.csv", index=False); return r
    routing = stage("L6 routing (Q3)", _routing)

    # --- L7 decisions: scorecard (Q2) + siting (Q1) ---
    def _scorecard():
        from dcfootprint.decisions import scorecard
        s = scorecard.scorecard(account); s.to_csv(RES / "q2_scorecard.csv", index=False); return s
    scard = stage("L7 Q2 scorecard", _scorecard)

    def _siting():
        from dcfootprint.decisions import siting
        s = siting.rank_sites(account); s.to_csv(RES / "q1_siting.csv", index=False); return s
    sites = stage("L7 Q1 siting", _siting)

    # --- L8 uncertainty ---
    unc = stage("L8 uncertainty", lambda: __import__("dcfootprint.uncertainty.monte_carlo", fromlist=["monte_carlo"]).monte_carlo(account))

    # --- L9 combined report ---
    stage("L9 report", lambda: _write_report(account, cal, fc, rech, levers_df, gap_overlay, routing, scard, sites, unc))

    print("\n===== PIPELINE STATUS =====")
    for n, s in status:
        print(f"  {'[OK]' if s == 'OK' else '[XX]'} {n:<24} {s}")
    ok = sum(1 for _, s in status if s == "OK")
    print(f"  {ok}/{len(status)} stages OK")
    return {"status": status, "artifacts": art}


def _write_report(account, cal, fc, rech, levers_df, gap_overlay, routing, scard, sites, unc) -> Path:
    L = ["# India AI-datacenter environmental pipeline — full results\n",
         "*Deterministic account -> counterfactual -> policy-gap, + forecasting (L3), Q1 siting, "
         "Q2 scorecard, Q3 routing (stylised Ceiling), uncertainty. Generated by `dcfootprint.pipeline`.*\n"]
    if account is not None:
        c = account["carbon_tco2"].sum(); wp = account["water_phys_l"].sum() / 1e3; ws = account["water_scarcity_l_eq"].sum() / 1e3
        L.append(f"## L2 Account\n- {account['facility_id'].nunique()} facilities x 12 months; "
                 f"**{c:,.0f} tCO2/yr**, **{wp:,.0f} m3/yr** physical, **{ws:,.0f} m3-eq/yr** scarcity-weighted.")
    if cal: L.append(f"## L2.5 Calibration\n- bottom-up {cal['bottom_up_operational_mw']} MW vs CEEW/JLL {cal['ceew_jll_range_mw']} -> {cal['verdict']} (ratio {cal['ratio_vs_low']}).")
    if fc: L.append(f"## L3 Forecast\n- backtest winner **{fc['backtest']['winner']}** (skill vs naive {fc['backtest']['skill_vs_naive']}); "
                    f"forecast to {pd.to_datetime(fc['forecast']['date']).max().date()}. Co-RE benchmark reused: {'yes' if fc.get('core_benchmark') else 'n/a'}.")
    if rech is not None: L.append(f"## L3 Recharge (R-hat)\n- monsoon-peaked seasonal recharge (peak month {int(rech.loc[rech['recharge_mult'].idxmax(),'month'])}); drives Q3 basin queues (stylised).")
    if levers_df is not None:
        top = levers_df.iloc[0]
        L.append(f"## L4 Counterfactual — which lever pays\n- top: **{top['lever']}** ~{top['water_scarcity_saved_m3eq_yr']:,.0f} m3-eq/yr ({top['pct_of_scarcity_baseline']}% of baseline).")
    if gap_overlay: L.append(f"## L5 Policy-gap\n- **{gap_overlay['pct_burden_in_blind_spot']:.0f}%** of burden in a regulatory blind spot; axes mandated anywhere: {gap_overlay['axes_mandated_anywhere']}/4.")
    if routing is not None:
        best = routing.sort_values("scarcity_saving_pct_vs_static").iloc[-1]
        L.append(f"## L6 Q3 Routing (stylised, Ceiling)\n- {best['policy']} saves {best['scarcity_saving_pct_vs_static']}% scarcity-water vs static; "
                 f"lyapunov keeps basin queue bounded. *Synthetic demand; conditional on R-hat.*")
    if scard is not None: L.append(f"## L7 Q2 Scorecard\n- {len(scard)} facilities scored; **{int(scard['harm_flag'].sum())}** harm-flagged (top-quartile scarcity in high-stress basins).")
    if sites is not None:
        b = sites.iloc[0]
        L.append(f"## L7 Q1 Siting\n- {len(sites)} candidate basin x state cells ranked (min-regret); most preferable: {b['state']} basin {b['basin_id']} (mean CF {b['mean_cf']:.1f}).")
    if unc: L.append(f"## L8 Uncertainty\n- scarcity-weighted water 90% CI: {unc['scarcity_m3eq_yr']['p05']:,.0f} - {unc['scarcity_m3eq_yr']['p95']:,.0f} m3-eq/yr; "
                     f"dominant driver: **{next(iter(unc['scarcity_sensitivity_Mm3eq_swing']))}** (WUE band is widest).")
    L.append("\n### Caveats\n- absolutes are calibrated ranges (util/PUE/WUE assumed); lead with relative/spatial results.\n"
             "- Q3 routing is a stylised controller (synthetic demand, conditional on R-hat) — Ceiling reach, not headline.\n"
             "- India carbon national-annual; sub-national signal rides on water. Coordinates are city-centroids.")
    (RES / "RESULTS_FULL.md").write_text("\n\n".join(L), encoding="utf-8")
    return RES / "RESULTS_FULL.md"


if __name__ == "__main__":
    run()

"""Assemble the §6 artefacts of a forecasting run folder from files and commands (nothing typed by hand
except the fixed descriptive text of the sidecars).

Run: python dcfootprint/experiments/assemble_forecast_run.py runs/fresh_run_2026-09-27
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd

CP = Path(__file__).resolve().parents[2]                       # counterfactual-policy
CORE_ROOT = Path(r"D:\3Gtech_paper - GNN")                     # Co-RE repo root
CORE = CORE_ROOT / "diff" / "gat-sarima-nexus"
PY_DCF = CP / ".venv" / "Scripts" / "python.exe"
PY_CORE = Path(r"C:\Users\samik\AppData\Local\Programs\Python\Python311\python.exe")

SIDECARS = {
    "seasonal_naive": "Produced fresh by counterfactual-policy dcfootprint/experiments/forecast_run.py (dcfootprint venv).\n"
                      "y(t-12); sigma = SD of the method's own 12-month-ahead errors in the 12 months up to the origin;\n"
                      "80% interval = mean +- 1.2816 sigma. Deterministic (no seed).",
    "sarima": "Produced fresh by dcfootprint/experiments/forecast_run.py (dcfootprint venv). SARIMA(1,1,1)(1,0,1,12),\n"
              "stationarity/invertibility enforced, missing months kept as NaN, L-BFGS maxiter 500. A fit is a recorded\n"
              "FAILURE (metrics/failures.csv) if it does not converge, is degenerate (a coefficient on the unit boundary or\n"
              "non-finite SE), diverges (>10x historical max) or raises. Predictive mean, SE and 80% interval from statsmodels.\n"
              "Deterministic (no seed).",
    "sarima_core": "COPIED from the Co-RE cache (outputs_v2/partB/per_region_base_forecasts.csv, model 'SARIMA'); not re-run.\n"
                   "Co-RE's own SARIMA spec; single 12-month holdout per series; point forecasts only (no PICP/CRPS).",
    "xlstm": "COPIED from the Co-RE cache (model 'xLSTM'); not re-run. Torch LSTM-type model defined in the Part B notebook\n"
             "(LOOKBACK/HIDDEN_SIZE/NUM_LAYERS per notebook config), seed 42 (notebook config). Point forecasts only.",
    "timesfm-2.5": "COPIED from the Co-RE cache (model 'TimesFM'); not re-run. google TimesFM 2.5 zero-shot. Point only.",
    "chronos-2": "COPIED from the Co-RE cache, where the column is named 'Nexus': it is Chronos-2 running in the Nexus slot\n"
                 "(Co-RE docs/AUDIT_REPORT.md §1). Labelled chronos-2 here and never 'nexus'. Point forecasts only.",
}


def git(repo: Path, *args) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True).stdout.strip()


def main(run: Path) -> None:
    run = Path(run)
    (run / "manifest").mkdir(parents=True, exist_ok=True)
    # --- sidecars
    for model, text in SIDECARS.items():
        d = run / "forecasts" / model
        if d.exists():
            (d / "SIDECAR.md").write_text(f"# {model}\n\n{text}\n", encoding="utf-8")
    # --- env freezes
    for name, py in [("dcfootprint_venv", PY_DCF), ("core_python311", PY_CORE)]:
        out = subprocess.run([str(py), "-m", "pip", "freeze"], capture_output=True, text=True).stdout
        ver = subprocess.run([str(py), "--version"], capture_output=True, text=True).stdout.strip()
        (run / "manifest" / f"env_freeze_{name}.txt").write_text(f"# {py}\n# {ver}\n{out}", encoding="utf-8")
    # --- config snapshot
    cs = run / "config_snapshot"
    cs.mkdir(exist_ok=True)
    for f in ["parameters.yaml", "datasets.yaml", "policy_sources.csv"]:
        shutil.copy2(CP / "dcfootprint" / "config" / f, cs / f)
    # --- seed inventory
    seeds = {"seasonal_naive": None, "sarima": None, "sarima_core": None,
             "xlstm": {"seed": 42, "source": "Co-RE partB notebook config (cached run, not re-run here)"},
             "timesfm-2.5": {"seed": None, "note": "zero-shot inference, deterministic"},
             "chronos-2": {"seed": None, "note": "cached; Chronos-2 sampling settings per Co-RE run"},
             "nexus (real, multi-agent)": {"status": "NOT RUN", "planned_backend": "Ollama gemma4:26b",
                                           "planned_sampling": {"temperature": 0, "seed": 42}}}
    (run / "manifest" / "seed_inventory.json").write_text(json.dumps(seeds, indent=2), encoding="utf-8")
    # --- boundary significance split by contrast (Co-RE cache)
    bs = pd.read_csv(CORE / "outputs_v2" / "audit" / "boundary_significance_full.csv")
    bdir = run / "metrics" / "boundary_significance"
    bdir.mkdir(parents=True, exist_ok=True)
    for contrast, g in bs.groupby("contrast"):
        g.to_csv(bdir / f"{str(contrast).replace(' ', '_').replace('/', '-')}.csv", index=False)
    (bdir / "README.md").write_text("Split by `contrast` from Co-RE outputs_v2/audit/boundary_significance_full.csv "
                                    "(GAT-weighted vs unweighted blending, boundary regions). Copied from cache, not recomputed; "
                                    "'Nexus' rows there are Chronos-2.\n", encoding="utf-8")
    # --- combined metrics
    fresh = pd.read_csv(run / "metrics" / "per_model_per_region.csv").assign(source="fresh (dcfootprint)")
    core = pd.read_csv(run / "metrics" / "core_cached_per_model_per_region.csv").assign(level="zones")
    allm = pd.concat([fresh, core], ignore_index=True)
    allm.to_csv(run / "metrics" / "all_models_per_region.csv", index=False)
    # --- manifest
    fails = pd.read_csv(run / "metrics" / "failures.csv")
    manifest = {
        "run": run.name, "assembled": datetime.now().isoformat(timespec="seconds"),
        "repos": {"counterfactual-policy": {"path": str(CP), "branch": git(CP, "branch", "--show-current"),
                                           "commit": git(CP, "rev-parse", "HEAD"),
                                           "dirty": bool(git(CP, "status", "--porcelain", "--", "dcfootprint/src"))},
                  "Co-RE": {"path": str(CORE_ROOT), "commit": git(CORE_ROOT, "rev-parse", "HEAD"), "touched": "read-only"}},
        "environments": {"dcfootprint_venv": str(PY_DCF), "core_python311": str(PY_CORE)},
        "models": {
            "seasonal_naive": {"repo": "counterfactual-policy", "env": "dcfootprint_venv", "status": "fresh"},
            "sarima": {"repo": "counterfactual-policy", "env": "dcfootprint_venv", "status": "fresh",
                       "failures": int(len(fails))},
            "sarima_core": {"repo": "Co-RE", "env": "core_python311 (original run)", "status": "cached, copied"},
            "xlstm": {"repo": "Co-RE", "env": "core_python311 (original run)", "status": "cached, copied"},
            "timesfm-2.5": {"repo": "Co-RE", "env": "core_python311 (original run)", "status": "cached, copied"},
            "chronos-2": {"repo": "Co-RE", "env": "core_python311 (original run)", "status": "cached, copied",
                          "note": "the cache's 'Nexus' column"},
            "nexus (real)": {"repo": "Co-RE", "entry": "scripts/run_country_nexus_llm.py", "status": "NOT RUN",
                             "reason": "one gemma4:26b call took 534 s on CPU (3,985 tokens); see RUN_SUMMARY"}},
        "metrics": ["MAE", "RMSE", "WMAPE_pct", "Bias", "Bias_pct", "MASE", "sMAPE_pct", "MedAE", "Pearson_r",
                    "PICP", "CRPS", "n_prob"],
    }
    (run / "manifest" / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print("assembled", run)


if __name__ == "__main__":
    main(Path(sys.argv[1]))

"""Gate 3b — SEASONAL RQ2: does monthly (dry-season) scarcity re-rank India's DC hotspots?

Successor to gate3_rq2_scarcity_reranking.py (annual CF). Same question, monthly CFs, plus
fixes for defects found in the annual gate (each marked FIX below):

  FIX-1 sample   : the annual gate ranked ALL statuses (incl. announced/planned pipeline and the
                   2.5 GW Palava *park* row the facility workbook says not to sum). Primary sample
                   here = Operational rows, excluding capacity_basis in {region, park}; capacity =
                   op_capacity_mw, else capacity_mw (same rule as Gate 1). The annual gate's
                   sample is re-run as sensitivity "S_all" so its 0.91/0.95 can be reproduced.
  FIX-2 geocode  : the manual-centroid fallback matched substrings in dict order ("navi mumbai"
                   hit "mumbai"; "greater noida" hit "noida"). Now exact match, then longest
                   substring. Every facility's coordinate source is written to an audit CSV.
  FIX-3 CF cols  : gates_1_2 averaged every column starting "CF_" (may mix monthly + annual
                   columns). Month columns are selected by exact name and the script fails
                   loudly if any is missing.
  FIX-4 null     : a high Spearman(unweighted, weighted) is EXPECTED whenever capacity spans
                   orders of magnitude, whatever the siting. The reframe ("hotspots ARE the
                   stressed basins") therefore needs nulls that break ONLY the capacity<->scarcity
                   link while keeping facilities clustered in their basins:
                     null A = shuffle 12-month CF profiles among the OCCUPIED basins;
                     null B = draw profiles from ALL AWARE basins in India, area-weighted
                              ("a random place in India"; needs data/gadm/gadm41_IND.gpkg).
                   (A first facility-level permutation broke the clustering and inflated the
                   null band — caught in the synthetic smoke test, replaced.)
  FIX-5 premise  : the annual gate never computed the capacity~scarcity association it was later
                   cited for. Reported here directly (facility-level Spearman + capacity-weighted
                   vs unweighted mean CF).

Deterministic (numpy Generator, fixed seed). Paths are repo-relative; override with --data-dir.
Needs: pandas, numpy, geopandas, shapely, pyogrio, pyarrow, scipy, openpyxl.

Run (from repo root):
    python dcfootprint/experiments/gate3b_seasonal_reranking.py
    python dcfootprint/experiments/gate3b_seasonal_reranking.py --data-dir D:/data --n-null 2000
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
MONTH_COLS = [f"CF_{m}" for m in MONTHS]
ANNUAL_COL = "CF_annual_unspecified"          # used by gate3_rq2_scarcity_reranking.py
AWARE_LAYER = "AWARE20_Native_CFs_geospatial"
AWARE_CAP = 100.0                             # R9: CF=100 is the cap, not a plain value
TOP_K = 5

# Manual centroids = copied UNCHANGED from gate3_rq2_scarcity_reranking.py for comparability.
# PROVENANCE: unsourced in the original script (approximate city centres). Only used when a
# city is absent from ATLAS; usage count is reported so their influence is visible.
MANUAL_CENTROIDS = {
    "mumbai": (19.07, 72.88), "navi mumbai": (19.03, 73.03), "palava": (19.16, 73.14),
    "chennai": (13.08, 80.27), "bengaluru": (12.97, 77.59), "bangalore": (12.97, 77.59),
    "hyderabad": (17.38, 78.49), "pune": (18.52, 73.86), "noida": (28.58, 77.32),
    "greater noida": (28.47, 77.50), "delhi": (28.61, 77.21), "new delhi": (28.61, 77.21),
    "gurugram": (28.46, 77.03), "kolkata": (22.57, 88.36), "ahmedabad": (23.02, 72.57),
    "jaipur": (26.91, 75.79), "kochi": (9.93, 76.27), "coimbatore": (11.02, 76.96),
    "visakhapatnam": (17.69, 83.22), "nagpur": (21.15, 79.09), "lucknow": (26.85, 80.95),
}
NON_FACILITY_BASIS = {"region", "park"}       # workbook "Notes & Method": not single facilities


# ----------------------------------------------------------------------------- loading
def load_facilities(path: Path) -> pd.DataFrame:
    fac = pd.read_excel(path, sheet_name="Facilities")
    fac.columns = [c.strip() for c in fac.columns]
    for c in ("capacity_mw", "op_capacity_mw"):
        fac[c] = pd.to_numeric(fac[c], errors="coerce")
    for c in ("city", "state", "status", "capacity_basis"):
        fac[f"{c}_k"] = fac[c].astype(str).str.strip().str.lower()
    fac["cap_op"] = fac["op_capacity_mw"].fillna(fac["capacity_mw"])   # Gate-1 rule
    return fac


def atlas_centroids(path: Path) -> pd.DataFrame:
    atl = pd.read_parquet(path)
    atl = atl[atl["country"].astype(str).str.strip() == "India"].copy()
    atl["city_k"] = atl["city"].astype(str).str.strip().str.lower()
    atl["lat"] = pd.to_numeric(atl["latitude"], errors="coerce")
    atl["lon"] = pd.to_numeric(atl["longitude"], errors="coerce")
    return atl.dropna(subset=["lat", "lon"]).groupby("city_k")[["lat", "lon"]].median()


def geocode(fac: pd.DataFrame, cent: pd.DataFrame) -> pd.DataFrame:
    """FIX-2: ATLAS exact city -> manual exact -> manual longest-substring -> none."""
    by_len = sorted(MANUAL_CENTROIDS, key=len, reverse=True)
    rows = []
    for ck in fac["city_k"]:
        if ck in cent.index:
            rows.append((*cent.loc[ck, ["lat", "lon"]].astype(float), "atlas_city_median"))
        elif ck in MANUAL_CENTROIDS:
            rows.append((*MANUAL_CENTROIDS[ck], "manual_exact"))
        else:
            hit = next((k for k in by_len if k in ck), None)
            rows.append((*MANUAL_CENTROIDS[hit], f"manual_substring:{hit}") if hit
                        else (np.nan, np.nan, "none"))
    out = fac.copy()
    out[["lat", "lon", "geo_source"]] = pd.DataFrame(rows, index=fac.index)
    return out


def load_aware(path: Path):
    import geopandas as gpd
    aw = gpd.read_file(path, layer=AWARE_LAYER)
    missing = [c for c in MONTH_COLS if c not in aw.columns]
    if missing:                                               # FIX-3: fail loudly
        raise KeyError(f"AWARE gpkg lacks month columns {missing}; columns = {list(aw.columns)}")
    for c in MONTH_COLS + ([ANNUAL_COL] if ANNUAL_COL in aw.columns else []):
        aw[c] = pd.to_numeric(aw[c], errors="coerce")
    aw["basin_key"] = (aw["Basin_ID"].astype("Int64").astype(str) if "Basin_ID" in aw.columns
                       else aw.index.astype(str))            # annual gate used the row index
    if aw.crs is None:
        aw = aw.set_crs(4326)
    return aw.to_crs(4326)


def join_basins(fac: pd.DataFrame, aw) -> pd.DataFrame:
    import geopandas as gpd
    from shapely.geometry import Point
    g = fac[fac["lat"].notna()].copy()
    gdf = gpd.GeoDataFrame(g, geometry=[Point(xy) for xy in zip(g["lon"], g["lat"])], crs=4326)
    keep = ["basin_key", "geometry"] + MONTH_COLS + ([ANNUAL_COL] if ANNUAL_COL in aw.columns else [])
    j = gpd.sjoin(gdf, aw[keep], how="left", predicate="within")
    n_multi = int(j.index.duplicated().sum())
    j = j[~j.index.duplicated(keep="first")]
    j.attrs["n_multi_polygon_hits"] = n_multi
    return pd.DataFrame(j.drop(columns=["geometry", "index_right"], errors="ignore"))


# ----------------------------------------------------------------------------- metrics
def rank_compare(cap: np.ndarray, cf: np.ndarray, codes: np.ndarray, n_units: int):
    """Aggregate facility burden to units (state/basin); compare unweighted vs weighted.
    Returns rho, top-K overlap, unweighted sums, weighted sums (arrays indexed by unit code)."""
    uw = np.bincount(codes, weights=cap, minlength=n_units)
    w = np.bincount(codes, weights=cap * cf, minlength=n_units)
    rho = spearmanr(uw, w).correlation if n_units > 2 else np.nan
    ov = len(set(np.argsort(-uw, kind="stable")[:TOP_K]) & set(np.argsort(-w, kind="stable")[:TOP_K]))
    return rho, ov, uw, w


def variants_of(cf_mat: np.ndarray, annual: np.ndarray | None, dry_idx: list[int]) -> dict:
    """Every CF definition tested. dry_idx is FIXED from the observed data, then reused in nulls."""
    v = {m: cf_mat[:, i] for i, m in enumerate(MONTHS)}
    v["DRY3_mean"] = cf_mat[:, dry_idx].mean(axis=1)
    v["WORST_month"] = cf_mat.max(axis=1)                    # each facility's own worst month
    v["MEAN12"] = cf_mat.mean(axis=1)
    if annual is not None:
        v["ANNUAL_unspecified"] = annual
    return v


def null_distribution(cap, prof, fac_basin, pool, pool_w, codes, n_units, dry_idx, has_annual,
                      n, rng) -> dict:
    """FIX-4. Re-assign a CF profile to every OCCUPIED basin (facilities in one basin keep
    sharing it — the spatial clustering is preserved), drawn from `pool`:
      * pool = occupied basins' own profiles, without replacement  -> null A ("shuffle")
      * pool = all basins in India, area-weighted, with replacement -> null B ("random place")
    Only the capacity<->scarcity association is broken. Returns {variant: rho array}."""
    n_b = fac_basin.max() + 1
    out: dict[str, list] = {}
    for _ in range(n):
        if pool_w is None:
            pick = pool[rng.permutation(len(pool))[:n_b]]
        else:
            pick = pool[rng.choice(len(pool), size=n_b, replace=True, p=pool_w)]
        fac_prof = pick[fac_basin]
        ann = fac_prof[:, 12] if has_annual else None
        for name, cf in variants_of(fac_prof[:, :12], ann, dry_idx).items():
            out.setdefault(name, []).append(rank_compare(cap, cf, codes, n_units)[0])
    return {k: np.asarray(v) for k, v in out.items()}


def mc_rho(cap, cf, codes, n_units, n, rng):
    """Original gate's noise test: capacity x U(0.7,1.3), CF x U(0.8,1.2), clipped at cap."""
    return np.array([rank_compare(cap * rng.uniform(0.7, 1.3, len(cap)),
                                  np.clip(cf * rng.uniform(0.8, 1.2, len(cf)), 0, AWARE_CAP),
                                  codes, n_units)[0] for _ in range(n)])


def pct_in(dist: np.ndarray | None, x: float) -> float:
    return float((dist < x).mean() * 100) if dist is not None and len(dist) else np.nan


def band(dist: np.ndarray | None) -> str:
    return f"[{np.percentile(dist, 5):.2f},{np.percentile(dist, 95):.2f}]" if dist is not None else "      n/a"


# ----------------------------------------------------------------------------- analysis
def analyse(j: pd.DataFrame, label: str, args, rng, out_dir: Path, india_pool) -> list[dict]:
    cap = j["cap"].to_numpy(float)
    has_annual = ANNUAL_COL in j.columns and j[ANNUAL_COL].notna().all()
    prof_cols = MONTH_COLS + ([ANNUAL_COL] if has_annual else [])
    basin_codes, basin_ids = pd.factorize(j["basin_key"].astype(str))
    occ_prof = j.groupby(basin_codes)[prof_cols].first().to_numpy(float)   # one profile per basin
    cf_mat = j[MONTH_COLS].to_numpy(float)
    annual = j[ANNUAL_COL].to_numpy(float) if has_annual else None
    records = []
    print(f"\n{'=' * 78}\nSAMPLE {label}: {len(j)} basin-matched facilities in {len(basin_ids)} basins, "
          f"{cap.sum():,.1f} MW\n{'=' * 78}")

    # FIX-5 premise check
    cf12 = cf_mat.mean(axis=1)
    print(f"premise: Spearman(capacity, 12-mo mean CF) across facilities = "
          f"{spearmanr(cap, cf12).correlation:+.2f}")
    print(f"premise: capacity-weighted mean CF = {np.average(cf12, weights=cap):.1f} | unweighted "
          f"facility mean = {cf12.mean():.1f} | occupied-basin mean = {occ_prof[:, :12].mean():.1f}")
    if india_pool is not None:
        pool, w = india_pool
        print(f"premise: India area-weighted mean CF (all basins in India) = "
              f"{np.average(pool[:, :12].mean(axis=1), weights=w):.1f}")
    print(f"capped (any month CF=={AWARE_CAP:g}): {int((cf_mat >= AWARE_CAP).any(axis=1).sum())}/{len(j)} facilities")

    profile = pd.Series(np.average(cf_mat, axis=0, weights=cap), index=MONTHS)
    dry = profile.nlargest(3).index.tolist()
    dry_idx = [MONTHS.index(m) for m in dry]
    print("capacity-weighted CF by month:", profile.round(1).to_dict())
    print(f"data-driven dry season (top-3 months by capacity-weighted CF): {dry}")
    variants = variants_of(cf_mat, annual, dry_idx)

    for level, keys in (("STATE", j["state_k"]), ("BASIN", j["basin_key"].astype(str))):
        codes, units = pd.factorize(keys)
        n_units = len(units)
        null_a = null_distribution(cap, occ_prof, basin_codes, occ_prof, None, codes, n_units,
                                   dry_idx, has_annual, args.n_null, rng)
        null_b = (null_distribution(cap, occ_prof, basin_codes, india_pool[0], india_pool[1], codes,
                                    n_units, dry_idx, has_annual and india_pool[0].shape[1] > 12,
                                    args.n_null, rng) if india_pool is not None else {})
        ref = variants.get("ANNUAL_unspecified", variants["MEAN12"])
        ref_w = rank_compare(cap, ref, codes, n_units)[3]
        print(f"\n[{label} | {level}] units={n_units}")
        print(f"{'variant':<19}{'rho(uw,w)':>9}{'top5':>6}{'nullA shuffle':>15}{'pctA':>5}"
              f"{'nullB India':>14}{'pctB':>5}{'MC p5-p95':>14}{'rho(w,annual w)':>16}  top-{TOP_K} weighted")
        for name, cf in variants.items():
            rho, ov, uw, w = rank_compare(cap, cf, codes, n_units)
            mc = mc_rho(cap, cf, codes, n_units, args.n_mc, rng)
            rho_ref = spearmanr(w, ref_w).correlation if n_units > 2 else np.nan
            top_w = [str(units[i]) for i in np.argsort(-w, kind="stable")[:TOP_K]]
            top_uw = [str(units[i]) for i in np.argsort(-uw, kind="stable")[:TOP_K]]
            da, db = null_a.get(name), null_b.get(name)
            print(f"{name:<19}{rho:>9.2f}{ov:>4}/{TOP_K}{band(da):>15}{pct_in(da, rho):>5.0f}"
                  f"{band(db):>14}{pct_in(db, rho):>5.0f}  {band(mc)}{rho_ref:>14.2f}  {top_w}")
            records.append(dict(
                sample=label, level=level, variant=name, n_facilities=len(j), n_units=n_units,
                dry_months="|".join(dry), rho_uw_w=rho, top5_overlap=ov,
                nullA_p5=np.percentile(da, 5), nullA_p95=np.percentile(da, 95), obs_pct_nullA=pct_in(da, rho),
                nullB_p5=np.percentile(db, 5) if db is not None else np.nan,
                nullB_p95=np.percentile(db, 95) if db is not None else np.nan,
                obs_pct_nullB=pct_in(db, rho), mc_p5=np.percentile(mc, 5), mc_p95=np.percentile(mc, 95),
                rho_w_vs_annual_w=rho_ref, top5_unweighted="|".join(top_uw), top5_weighted="|".join(top_w)))
            pd.DataFrame({"unit": units, "burden_unweighted": uw, "burden_weighted": w,
                          "rank_unweighted": pd.Series(-uw).rank().to_numpy(),
                          "rank_weighted": pd.Series(-w).rank().to_numpy()}).to_csv(
                out_dir / f"ranks_{label}_{level}_{name}.csv", index=False)
    return records


def india_basin_pool(aw, gadm_path: Path):
    """All AWARE basins whose representative point lies in India (GADM country outline), with
    area weights (equal-area CRS). Returns (profiles, weights) or None if GADM is unavailable."""
    import geopandas as gpd
    import pyogrio
    if not gadm_path.exists():
        print(f"null B skipped: {gadm_path} not found")
        return None
    layers = [l[0] for l in pyogrio.list_layers(gadm_path)]
    lyr = next((l for l in layers if l.upper().endswith("_0")), None)
    if lyr is None:
        print(f"null B skipped: no country (ADM_0) layer in {gadm_path} — layers: {layers}")
        return None
    india = gpd.read_file(gadm_path, layer=lyr).to_crs(4326).union_all()
    pts = aw.geometry.representative_point()
    inside = aw[pts.within(india)].copy()
    cols = MONTH_COLS + ([ANNUAL_COL] if ANNUAL_COL in inside.columns else [])
    inside = inside.dropna(subset=cols)
    area = inside.to_crs(6933).geometry.area.to_numpy()
    print(f"null B pool: {len(inside)} AWARE basins in India (layer '{lyr}', area-weighted)")
    return inside[cols].to_numpy(float), area / area.sum()


def main() -> int:
    repo = Path(__file__).resolve().parents[2]
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--data-dir", type=Path, default=repo / "data")
    ap.add_argument("--facilities", type=Path, default=repo / "context/data/India_DC_Facilities_v0.xlsx")
    ap.add_argument("--out-dir", type=Path, default=Path(__file__).resolve().parent / "results/gate3b")
    ap.add_argument("--n-null", type=int, default=1000)
    ap.add_argument("--n-mc", type=int, default=400)
    ap.add_argument("--seed", type=int, default=42)
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    rng = np.random.default_rng(args.seed)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    fac = geocode(load_facilities(args.facilities),
                  atlas_centroids(args.data_dir / "atlas/datacenters.parquet"))
    aw = load_aware(args.data_dir / "aware/AWARE20_Native_CFs_geospatial.gpkg")
    india_pool = india_basin_pool(aw, args.data_dir / "gadm/gadm41_IND.gpkg")
    joined = join_basins(fac, aw)
    joined.to_csv(args.out_dir / "facility_geocode_basin_audit.csv", index=False)
    print("geocode sources:", fac["geo_source"].str.split(":").str[0].value_counts().to_dict())
    print(f"facilities hitting >1 basin polygon (first kept): {joined.attrs.get('n_multi_polygon_hits', 0)}")

    matched = joined[joined[MONTH_COLS].notna().all(axis=1)]
    oper = matched["status_k"].eq("operational") & ~matched["capacity_basis_k"].isin(NON_FACILITY_BASIS)
    samples = {
        # PRIMARY (FIX-1): operational facilities, Gate-1 capacity rule
        "S_oper": matched[oper & matched["cap_op"].notna()].assign(cap=lambda d: d["cap_op"]),
        # SENSITIVITY = the annual gate's sample (all statuses, capacity_mw) — reproduces 0.91/0.95
        "S_all": matched[matched["capacity_mw"].notna()].assign(cap=lambda d: d["capacity_mw"]),
    }
    records = []
    for label, j in samples.items():
        if len(j) < 3:
            print(f"\nSAMPLE {label}: only {len(j)} facilities — skipped")
            continue
        records += analyse(j, label, args, rng, args.out_dir, india_pool)
    pd.DataFrame(records).to_csv(args.out_dir / "gate3b_summary.csv", index=False)
    print(f"\nwrote {args.out_dir}")
    print("READ: rho(uw,w) inside null A/B => the no-re-ranking result is explained by capacity"
          " heterogeneity, NOT by DCs sitting in stressed basins; rho(w, annual w) < 1 in some"
          " months => seasonal re-ranking of the weighted hotspots (C3 'when').")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

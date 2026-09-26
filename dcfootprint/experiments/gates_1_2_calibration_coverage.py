import pandas as pd, numpy as np, warnings
warnings.filterwarnings("ignore"); np.random.seed(42)
import sys; sys.stdout.reconfigure(encoding="utf-8")
R = r"C:\Users\gauri\Projects\energyclimaterp journal"
def H(t): print("\n"+"="*72+f"\n{t}\n"+"="*72)

# ---------- load facility master ----------
fac = pd.read_excel(R+r"\context\data\India_DC_Facilities_v0.xlsx")
fac.columns = [c.strip() for c in fac.columns]
fac["city_k"] = fac["city"].astype(str).str.strip().str.lower()
fac["state_k"] = fac["state"].astype(str).str.strip().str.lower()
fac["status_k"] = fac["status"].astype(str).str.strip().str.lower()
# capacity: prefer op_capacity_mw for operational; else capacity_mw
for c in ["capacity_mw","op_capacity_mw"]:
    fac[c] = pd.to_numeric(fac[c], errors="coerce")
print("facility rows:", len(fac), "| status:", fac["status_k"].value_counts().to_dict())

# ============ GATE 1: CALIBRATION ============
H("GATE 1 — CALIBRATION: bottom-up capacity vs CEEW independent aggregate")
op = fac[fac["status_k"].str.contains("oper", na=False)]
op_mw = op["op_capacity_mw"].fillna(op["capacity_mw"]).sum()
op_n = len(op); op_costed = op["op_capacity_mw"].fillna(op["capacity_mw"]).notna().sum()
tot_mw = fac["capacity_mw"].sum()
print(f"operational facilities: {op_n} ({op_costed} with capacity)")
print(f"bottom-up OPERATIONAL capacity: {op_mw:,.0f} MW  (~{op_mw/1000:.2f} GW)")
print(f"total (all statuses) capacity : {tot_mw:,.0f} MW  (~{tot_mw/1000:.2f} GW)")
ceew_lo, ceew_hi = 1500, 1800
ratio = op_mw/((ceew_lo+ceew_hi)/2)
print(f"CEEW/JLL independent operational aggregate: {ceew_lo}-{ceew_hi} MW (H1 2026)")
print(f"our/independent ratio: {ratio:.2f}  ->", 
      "PASS (within 0.75-1.25)" if 0.75<=ratio<=1.25 else "FLAG (off by >25% — coverage/basis issue)")

# ============ GATE 2: COVERAGE UNIFORMITY ============
H("GATE 2 — COVERAGE UNIFORMITY: is our spatial distribution biased vs ATLAS + CEEW?")
atl = pd.read_parquet(R+r"\data\atlas\datacenters.parquet")
atl_in = atl[atl["country"].astype(str).str.strip()=="India"].copy()
atl_in["city_k"] = atl_in["city"].astype(str).str.strip().str.lower()
print(f"ATLAS India rows: {len(atl_in)} | our list rows: {len(fac)}")
# city share comparison (top hubs)
def share(df, col, w=None):
    s = (df.groupby(col)[w].sum() if w else df[col].value_counts())
    return (s/s.sum()*100).sort_values(ascending=False)
our_city = share(fac.assign(cap=fac["capacity_mw"].fillna(0)), "city_k", "cap").head(8)
atl_city = share(atl_in, "city_k").head(8)
print("\nOUR list — top cities by CAPACITY share (%):"); print(our_city.round(1).to_string())
print("\nATLAS India — top cities by COUNT share (%):"); print(atl_city.round(1).to_string())
mum = fac.assign(cap=fac["capacity_mw"].fillna(0)).groupby("city_k")["cap"].sum()
mum_share = 100*mum[[c for c in mum.index if "mumbai" in c or "navi" in c]].sum()/mum.sum()
print(f"\nMumbai/Navi-Mumbai capacity share in OUR list: {mum_share:.1f}%  (CEEW says ~25% of DCs)")
print("Verdict:", "PLAUSIBLE (hub concentration matches CEEW)" if 15<=mum_share<=45 else "FLAG (distribution off vs CEEW)")

# ============ GATE 3: RQ2 SIGNAL vs NOISE (scarcity re-ranking) ============
H("GATE 3 — RQ2: does scarcity-weighting re-rank basins/states beyond MC noise?")
import geopandas as gpd; from shapely.geometry import Point
from scipy.stats import spearmanr
# city centroids from ATLAS india (median lat/lon per city)
atl_in["lat"]=pd.to_numeric(atl_in["latitude"],errors="coerce"); atl_in["lon"]=pd.to_numeric(atl_in["longitude"],errors="coerce")
cent = atl_in.dropna(subset=["lat","lon"]).groupby("city_k")[["lat","lon"]].median()
# manual centroids for key hubs missing from atlas
MAN = {"mumbai":(19.07,72.88),"navi mumbai":(19.03,73.03),"chennai":(13.08,80.27),"bengaluru":(12.97,77.59),
"bangalore":(12.97,77.59),"hyderabad":(17.38,78.49),"pune":(18.52,73.86),"noida":(28.58,77.32),
"greater noida":(28.47,77.50),"delhi":(28.61,77.21),"new delhi":(28.61,77.21),"gurugram":(28.46,77.03),
"kolkata":(22.57,88.36),"ahmedabad":(23.02,72.57),"jaipur":(26.91,75.79),"kochi":(9.93,76.27),
"coimbatore":(11.02,76.96),"visakhapatnam":(17.69,83.22),"nagpur":(21.15,79.09),"lucknow":(26.85,80.95)}
def coords(ck):
    if ck in cent.index: return cent.loc[ck,"lat"], cent.loc[ck,"lon"]
    for k,v in MAN.items():
        if k in ck: return v
    return (np.nan,np.nan)
fac[["lat","lon"]] = fac["city_k"].apply(lambda c: pd.Series(coords(c)))
geo_ok = fac["lat"].notna()
print(f"geocoded (city-centroid): {geo_ok.sum()}/{len(fac)} facilities")
# AWARE basin point-in-polygon
aw = gpd.read_file(R+r"\data\aware\AWARE20_Native_CFs_geospatial.gpkg")
cfcols=[c for c in aw.columns if c.startswith("CF_")]
aw["cf"]=aw[cfcols].mean(axis=1)  # annual-mean scarcity CF
if aw.crs is None: aw=aw.set_crs(4326)
aw=aw.to_crs(4326)
g = fac[geo_ok & fac["capacity_mw"].notna()].copy()
gdf=gpd.GeoDataFrame(g, geometry=[Point(xy) for xy in zip(g["lon"],g["lat"])], crs=4326)
j=gpd.sjoin(gdf, aw[["Basin_ID","cf","geometry"]], how="left", predicate="within")
j=j[~j.index.duplicated(keep="first")]
matched=j["cf"].notna()
print(f"basin-matched: {matched.sum()}/{len(j)} | CF range {j['cf'].min():.1f}-{j['cf'].max():.1f} (mean {j['cf'].mean():.1f})")
j=j[matched].copy(); j["cap"]=j["capacity_mw"]
# unweighted water proxy ~ capacity; weighted ~ capacity * scarcity CF
def rank_compare(cap, cf, keys):
    d=pd.DataFrame({"k":keys,"uw":cap,"w":cap*cf})
    a=d.groupby("k")["uw"].sum().rank(ascending=False)
    b=d.groupby("k")["w"].sum().rank(ascending=False)
    m=pd.concat([a,b],axis=1); m.columns=["uw_rank","w_rank"]
    rho=spearmanr(m["uw_rank"],m["w_rank"]).correlation
    top5_uw=set(m.sort_values("uw_rank").head(5).index); top5_w=set(m.sort_values("w_rank").head(5).index)
    return rho, len(top5_uw&top5_w), m
for level,keys in [("STATE", j["state_k"].values), ("BASIN", j["Basin_ID"].astype(str).values)]:
    rho,ov,m = rank_compare(j["cap"].values, j["cf"].values, keys)
    print(f"\n[{level}] Spearman(unweighted,weighted)={rho:.2f} | top-5 overlap={ov}/5")
    if level=="STATE":
        top_uw=m.sort_values("uw_rank").head(4).index.tolist()
        top_w=m.sort_values("w_rank").head(4).index.tolist()
        print("  worst UNWEIGHTED (by capacity):", top_uw)
        print("  worst WEIGHTED (× scarcity)   :", top_w)
    # MC: perturb capacity ±30% and CF ±20%
    rhos=[]
    for _ in range(400):
        cap_p=j["cap"].values*np.random.uniform(0.7,1.3,len(j))
        cf_p=np.clip(j["cf"].values*np.random.uniform(0.8,1.2,len(j)),0,100)
        rr,_,_=rank_compare(cap_p,cf_p,keys); rhos.append(rr)
    rhos=np.array(rhos)
    print(f"  MC(400): Spearman median={np.median(rhos):.2f}  5-95%=[{np.percentile(rhos,5):.2f},{np.percentile(rhos,95):.2f}]")
    verdict = "SIGNAL — weighting robustly re-ranks (C4 positive)" if np.percentile(rhos,95)<0.85 else ("NO SIGNAL — average adequate" if np.percentile(rhos,5)>0.9 else "MIXED — partial re-ranking")
    print(f"  VERDICT[{level}]: {verdict}")
print("\nDONE")

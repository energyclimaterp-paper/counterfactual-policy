import pandas as pd, numpy as np, warnings, sys
warnings.filterwarnings("ignore"); np.random.seed(42); sys.stdout.reconfigure(encoding="utf-8")
import geopandas as gpd; from shapely.geometry import Point; from scipy.stats import spearmanr
R = r"C:\Users\gauri\Projects\energyclimaterp journal"
fac = pd.read_excel(R+r"\context\data\India_DC_Facilities_v0.xlsx"); fac.columns=[c.strip() for c in fac.columns]
fac["city_k"]=fac["city"].astype(str).str.strip().str.lower(); fac["state_k"]=fac["state"].astype(str).str.strip().str.lower()
fac["capacity_mw"]=pd.to_numeric(fac["capacity_mw"],errors="coerce")
atl=pd.read_parquet(R+r"\data\atlas\datacenters.parquet"); atl=atl[atl["country"].astype(str).str.strip()=="India"].copy()
atl["city_k"]=atl["city"].astype(str).str.strip().str.lower()
atl["lat"]=pd.to_numeric(atl["latitude"],errors="coerce"); atl["lon"]=pd.to_numeric(atl["longitude"],errors="coerce")
cent=atl.dropna(subset=["lat","lon"]).groupby("city_k")[["lat","lon"]].median()
MAN={"mumbai":(19.07,72.88),"navi mumbai":(19.03,73.03),"palava":(19.16,73.14),"chennai":(13.08,80.27),
"bengaluru":(12.97,77.59),"bangalore":(12.97,77.59),"hyderabad":(17.38,78.49),"pune":(18.52,73.86),
"noida":(28.58,77.32),"greater noida":(28.47,77.50),"delhi":(28.61,77.21),"new delhi":(28.61,77.21),
"gurugram":(28.46,77.03),"kolkata":(22.57,88.36),"ahmedabad":(23.02,72.57),"jaipur":(26.91,75.79),
"kochi":(9.93,76.27),"coimbatore":(11.02,76.96),"visakhapatnam":(17.69,83.22),"nagpur":(21.15,79.09),"lucknow":(26.85,80.95)}
def coords(ck):
    if ck in cent.index: return float(cent.loc[ck,"lat"]),float(cent.loc[ck,"lon"])
    for k,v in MAN.items():
        if k in ck: return v
    return (np.nan,np.nan)
fac[["lat","lon"]]=fac["city_k"].apply(lambda c: pd.Series(coords(c)))
aw=gpd.read_file(R+r"\data\aware\AWARE20_Native_CFs_geospatial.gpkg", layer="AWARE20_Native_CFs_geospatial")
aw["cf"]=pd.to_numeric(aw["CF_annual_unspecified"],errors="coerce")
aw=aw.reset_index().rename(columns={"index":"basin"})
if aw.crs is None: aw=aw.set_crs(4326)
aw=aw.to_crs(4326)
g=fac[fac["lat"].notna() & fac["capacity_mw"].notna()].copy()
gdf=gpd.GeoDataFrame(g,geometry=[Point(xy) for xy in zip(g["lon"],g["lat"])],crs=4326)
j=gpd.sjoin(gdf, aw[["basin","cf","geometry"]], how="left", predicate="within")
j=j[~j.index.duplicated(keep="first")]; j=j[j["cf"].notna()].copy(); j["cap"]=j["capacity_mw"]
print(f"geocoded {fac['lat'].notna().sum()}/{len(fac)} | costed+geocoded {len(g)} | basin-matched {len(j)}")
print(f"scarcity CF over matched facilities: min {j['cf'].min():.1f}  mean {j['cf'].mean():.1f}  max {j['cf'].max():.1f}")
def rc(cap,cf,keys):
    d=pd.DataFrame({"k":keys,"uw":cap,"w":cap*cf})
    a=d.groupby("k")["uw"].sum().rank(ascending=False); b=d.groupby("k")["w"].sum().rank(ascending=False)
    m=pd.concat([a,b],axis=1); m.columns=["uw","w"]; rho=spearmanr(m["uw"],m["w"]).correlation
    t=lambda col:set(m.sort_values(col).head(5).index)
    return rho, len(t("uw")&t("w")), m
for lvl,keys in [("STATE",j["state_k"].values),("BASIN",j["basin"].astype(str).values)]:
    rho,ov,m=rc(j["cap"].values,j["cf"].values,keys)
    print(f"\n[{lvl}] Spearman(unweighted,weighted)={rho:.2f} | top-5 overlap {ov}/5")
    if lvl=="STATE":
        print("  worst UNWEIGHTED (capacity):", m.sort_values("uw").head(4).index.tolist())
        print("  worst WEIGHTED (×scarcity):", m.sort_values("w").head(4).index.tolist())
    rhos=[]
    for _ in range(400):
        cp=j["cap"].values*np.random.uniform(0.7,1.3,len(j)); cfp=np.clip(j["cf"].values*np.random.uniform(0.8,1.2,len(j)),0,100)
        rhos.append(rc(cp,cfp,keys)[0])
    rhos=np.array(rhos)
    print(f"  MC(400) Spearman median={np.median(rhos):.2f} [5-95%: {np.percentile(rhos,5):.2f},{np.percentile(rhos,95):.2f}]")
    v="SIGNAL: weighting robustly re-ranks (C4 POSITIVE)" if np.percentile(rhos,95)<0.85 else ("NO SIGNAL: average adequate" if np.percentile(rhos,5)>0.9 else "MIXED: partial re-ranking")
    print(f"  VERDICT[{lvl}]: {v}")

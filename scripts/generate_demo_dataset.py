from pathlib import Path
import numpy as np,pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"data"/"processed"/"demo_air_quality.csv"
def main(n=5000,seed=42):
    r=np.random.default_rng(seed); pm25=np.clip(r.gamma(2.5,14,n),1,250)
    pm10=np.clip(pm25*r.uniform(1.2,2.8,n)+r.normal(0,12,n),2,500)
    co=np.clip(r.lognormal(5,.65,n),80,20000); no2=np.clip(r.gamma(2.2,13,n),1,250)
    ozone=np.clip(r.normal(65,28,n),5,180); temp=np.clip(r.normal(27,9,n),-5,48)
    humidity=r.uniform(15,100,n); wind=np.clip(r.gamma(2,5,n),0,45)
    y=np.clip(.52*pm25+.14*pm10+.0012*co+.045*no2+.025*ozone+.12*np.maximum(0,28-wind)+r.normal(0,5,n),0,100)
    df=pd.DataFrame({"pm2_5":pm25,"pm10":pm10,"carbon_monoxide":co,"nitrogen_dioxide":no2,"ozone":ozone,"temperature_c":temp,"relative_humidity":humidity,"wind_speed_kmh":wind,"risk_score":y})
    df=df.replace([np.inf,-np.inf],np.nan).dropna().drop_duplicates(); OUT.parent.mkdir(parents=True,exist_ok=True); df.to_csv(OUT,index=False)
    print(f"Saved {len(df)} synthetic demo rows to {OUT}. Not real measured observations.")
if __name__=="__main__": main()

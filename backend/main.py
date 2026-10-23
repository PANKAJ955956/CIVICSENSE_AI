from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import requests
from backend.ml import predict_risk, load_metrics
app=FastAPI(title="CivicSense AI API",version="1.0.0",description="Environmental context and ML exposure-risk estimation")
class PredictionInput(BaseModel):
    pm2_5:float=Field(ge=0,le=1000)
    pm10:float=Field(ge=0,le=2000)
    carbon_monoxide:float=Field(ge=0,le=100000)
    nitrogen_dioxide:float=Field(ge=0,le=5000)
    ozone:float=Field(ge=0,le=1000)
    temperature_c:float=Field(ge=-60,le=60)
    relative_humidity:float=Field(ge=0,le=100)
    wind_speed_kmh:float=Field(ge=0,le=300)
@app.get("/health")
def health(): return {"status":"ok","service":"CivicSense AI"}
@app.get("/api/model-metrics")
def metrics(): return load_metrics() or {"message":"No metrics yet. Run python scripts/train_models.py"}
@app.post("/api/predict")
def predict(payload:PredictionInput):
    try: return predict_risk(payload.model_dump())
    except FileNotFoundError as e: raise HTTPException(status_code=503,detail=str(e))
@app.get("/api/live")
def live(latitude:float=28.6139,longitude:float=77.2090):
    if not(-90<=latitude<=90 and -180<=longitude<=180): raise HTTPException(400,"Invalid coordinates")
    try:
        a=requests.get("https://air-quality-api.open-meteo.com/v1/air-quality",params={"latitude":latitude,"longitude":longitude,"current":"pm2_5,pm10,carbon_monoxide,nitrogen_dioxide,ozone","timezone":"auto"},timeout=12); a.raise_for_status()
        w=requests.get("https://api.open-meteo.com/v1/forecast",params={"latitude":latitude,"longitude":longitude,"current":"temperature_2m,relative_humidity_2m,wind_speed_10m","timezone":"auto"},timeout=12); w.raise_for_status()
        ac,wc=a.json().get("current",{}),w.json().get("current",{})
        return {"location":{"latitude":latitude,"longitude":longitude},"time":ac.get("time") or wc.get("time"),"source":"Open-Meteo Air Quality API + Forecast API","features":{"pm2_5":ac.get("pm2_5",0),"pm10":ac.get("pm10",0),"carbon_monoxide":ac.get("carbon_monoxide",0),"nitrogen_dioxide":ac.get("nitrogen_dioxide",0),"ozone":ac.get("ozone",0),"temperature_c":wc.get("temperature_2m",25),"relative_humidity":wc.get("relative_humidity_2m",50),"wind_speed_kmh":wc.get("wind_speed_10m",5)}}
    except requests.RequestException as e: raise HTTPException(502,detail=f"Live provider unavailable: {e}")

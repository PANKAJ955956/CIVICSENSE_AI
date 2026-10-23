from pathlib import Path
import json, joblib, numpy as np, pandas as pd
ROOT=Path(__file__).resolve().parents[1]
MODEL_PATH=ROOT/"models"/"best_model.joblib"
METRICS_PATH=ROOT/"models"/"metrics.json"
FEATURES=["pm2_5","pm10","carbon_monoxide","nitrogen_dioxide","ozone","temperature_c","relative_humidity","wind_speed_kmh"]
def load_model():
    return joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None
def recommendations(score,row):
    out=[]
    if score>=60: out.append("Reduce strenuous outdoor activity; consider an indoor alternative.")
    elif score>=35: out.append("Consider shorter outdoor sessions and breaks away from busy roads.")
    else: out.append("Estimated conditions are comparatively lower risk; keep checking live updates.")
    if row["pm2_5"]>=25: out.append("PM2.5 is elevated in this input; avoid roadside exercise where practical.")
    if row["pm10"]>=50: out.append("PM10 is elevated; limit exposure to dust and construction activity.")
    if row["wind_speed_kmh"]<5: out.append("Low wind may reduce dispersion; re-check conditions later.")
    out.append("Educational estimate only—not official AQI, medical advice, or a safety guarantee.")
    return out
def predict_risk(payload):
    model=load_model()
    if model is None: raise FileNotFoundError("Model not trained. Run python scripts/train_models.py")
    row={k:float(payload[k]) for k in FEATURES}
    score=float(np.clip(model.predict(pd.DataFrame([row],columns=FEATURES))[0],0,100))
    label="Low" if score<25 else "Moderate" if score<50 else "High" if score<75 else "Very High"
    return {"risk_score":round(score,2),"risk_level":label,"recommendations":recommendations(score,row)}
def load_metrics():
    return json.loads(METRICS_PATH.read_text()) if METRICS_PATH.exists() else {}

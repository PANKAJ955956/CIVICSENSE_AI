from pathlib import Path
import json,sys
import pandas as pd,joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor,ExtraTreesRegressor,GradientBoostingRegressor,HistGradientBoostingRegressor
from sklearn.metrics import mean_absolute_error,mean_squared_error,r2_score
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from backend.ml import FEATURES
DATA=ROOT/"data"/"processed"/"demo_air_quality.csv"; OUT=ROOT/"models"
def main():
    if not DATA.exists(): raise SystemExit("Run python scripts/generate_demo_dataset.py first")
    df=pd.read_csv(DATA).replace([float("inf"),float("-inf")],pd.NA).dropna()
    X,y=df[FEATURES],df["risk_score"]; Xtr,Xte,ytr,yte=train_test_split(X,y,test_size=.2,random_state=42)
    models={"Random Forest":RandomForestRegressor(n_estimators=160,max_depth=16,min_samples_leaf=2,random_state=42,n_jobs=-1),"Extra Trees":ExtraTreesRegressor(n_estimators=160,max_depth=18,min_samples_leaf=2,random_state=42,n_jobs=-1),"Gradient Boosting":GradientBoostingRegressor(n_estimators=130,learning_rate=.06,max_depth=2,random_state=42),"Hist Gradient Boosting":HistGradientBoostingRegressor(max_iter=150,learning_rate=.07,max_leaf_nodes=20,random_state=42)}
    results=[]; fitted={}
    for name,est in models.items():
        pipe=Pipeline([("imputer",SimpleImputer(strategy="median")),("scaler",StandardScaler()),("model",est)]); pipe.fit(Xtr,ytr); p=pipe.predict(Xte)
        results.append({"model":name,"MAE":round(mean_absolute_error(yte,p),3),"RMSE":round(mean_squared_error(yte,p)**.5,3),"R2":round(r2_score(yte,p),4)}); fitted[name]=pipe
    best=min(results,key=lambda x:x["RMSE"]); OUT.mkdir(exist_ok=True); joblib.dump(fitted[best["model"]],OUT/"best_model.joblib")
    (OUT/"metrics.json").write_text(json.dumps({"best_model":best["model"],"rows":len(df),"train_rows":len(Xtr),"test_rows":len(Xte),"target":"synthetic demo risk score","metrics":results,"warning":"Synthetic-data metrics do not establish real-world validity."},indent=2))
    print(pd.DataFrame(results).to_string(index=False)); print("Saved best model:",best["model"])
if __name__=="__main__": main()

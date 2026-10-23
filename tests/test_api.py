from fastapi.testclient import TestClient
from backend.main import app
client=TestClient(app)
def test_health():
 r=client.get("/health"); assert r.status_code==200 and r.json()["status"]=="ok"
def test_metrics(): assert client.get("/api/model-metrics").status_code==200
def test_prediction_validation():
 p={"pm2_5":20,"pm10":40,"carbon_monoxide":300,"nitrogen_dioxide":20,"ozone":50,"temperature_c":25,"relative_humidity":50,"wind_speed_kmh":6}
 assert client.post("/api/predict",json=p).status_code in (200,503)

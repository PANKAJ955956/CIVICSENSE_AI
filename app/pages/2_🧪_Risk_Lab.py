import streamlit as st
from utils import inject_style,api_post
st.set_page_config(page_title="Risk Lab",page_icon="🧪",layout="wide"); inject_style(); st.title("🧪 Risk Lab")
st.write("Run a what-if scenario. Visit Live Insights first to load current values.")
d=st.session_state.get("live_features",{})
with st.form("risk"):
 a,b,c,e=st.columns(4); pm=a.number_input("PM2.5",0.,1000.,float(d.get("pm2_5",28.))); pm10=b.number_input("PM10",0.,2000.,float(d.get("pm10",62.))); co=c.number_input("Carbon monoxide",0.,100000.,float(d.get("carbon_monoxide",350.))); no2=e.number_input("Nitrogen dioxide",0.,5000.,float(d.get("nitrogen_dioxide",22.)))
 f,g,h,i=st.columns(4); oz=f.number_input("Ozone",0.,1000.,float(d.get("ozone",55.))); temp=g.number_input("Temperature °C",-60.,60.,float(d.get("temperature_c",28.))); rh=h.number_input("Humidity %",0.,100.,float(d.get("relative_humidity",55.))); wind=i.number_input("Wind km/h",0.,300.,float(d.get("wind_speed_kmh",7.)))
 submit=st.form_submit_button("Estimate relative risk",type="primary")
if submit:
 result,err=api_post("/api/predict",{"pm2_5":pm,"pm10":pm10,"carbon_monoxide":co,"nitrogen_dioxide":no2,"ozone":oz,"temperature_c":temp,"relative_humidity":rh,"wind_speed_kmh":wind})
 if err: st.error("Prediction failed: "+err+" — train model and start API.")
 else:
  st.session_state["last_prediction"]=result; st.metric("Relative risk score",f"{result['risk_score']}/100",result["risk_level"]); st.progress(min(100,int(result["risk_score"])))
  for x in result["recommendations"]: st.write("• "+x)

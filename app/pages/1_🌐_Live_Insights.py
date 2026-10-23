import streamlit as st,plotly.express as px
from utils import inject_style,api_get
st.set_page_config(page_title="Live Insights",page_icon="🌐",layout="wide"); inject_style(); st.title("🌐 Live Insights")
st.write("Default location is New Delhi. Enter coordinates for another location.")
a,b=st.columns(2); lat=a.number_input("Latitude",-90.,90.,28.6139,format="%.4f"); lon=b.number_input("Longitude",-180.,180.,77.2090,format="%.4f")
if st.button("Fetch live conditions",type="primary"):
 data,err=api_get("/api/live",{"latitude":lat,"longitude":lon})
 if err: st.error("API unavailable: "+err)
 else: st.session_state["live_data"]=data; st.session_state["live_features"]=data["features"]
data=st.session_state.get("live_data")
if data:
 f=data["features"]; st.caption(f"Source: {data['source']} · {data.get('time')}")
 cols=st.columns(4)
 for col,key,label in zip(cols,["pm2_5","pm10","temperature_c","wind_speed_kmh"],["PM2.5","PM10","Temperature °C","Wind km/h"]): col.metric(label,round(float(f[key]),2))
 st.plotly_chart(px.bar(x=["PM2.5","PM10","CO","NO₂","Ozone"],y=[f["pm2_5"],f["pm10"],f["carbon_monoxide"],f["nitrogen_dioxide"],f["ozone"]],labels={"x":"Pollutant","y":"Provider value"},title="Current pollutant readings"),use_container_width=True)
else: st.info("Press Fetch live conditions. Internet access is required.")

import streamlit as st
from utils import inject_style
st.set_page_config(page_title="CivicSense AI",page_icon="🌍",layout="wide"); inject_style()
st.title("🌍 CivicSense AI"); st.subheader("Urban air-quality intelligence · ML risk estimation · actionable insights")
st.caption("Full-stack AI/ML portfolio project — live public API context and locally trained models.")
a,b,c=st.columns(3); a.metric("Algorithms benchmarked","4"); b.metric("App layers","FastAPI + Streamlit"); c.metric("Live data","Open-Meteo · no key")
st.divider()
l,r=st.columns([1.3,1])
with l:
 st.markdown("### A decision-support workspace")
 st.write("Explore live conditions, run what-if scenarios, compare ML algorithms and review practical recommendations.")
 st.warning("Demo labels are synthetic. Model scores are not official AQI or medical guidance.")
with r:
 st.markdown("### Modules")
 st.markdown("**Live Insights** — current air/weather context\n\n**Risk Lab** — configurable ML estimate\n\n**Model Evaluation** — held-out metrics\n\n**Recommendations** — action layer\n\n**About** — architecture and limitations")

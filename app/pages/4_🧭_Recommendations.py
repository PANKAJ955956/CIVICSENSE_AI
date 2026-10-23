import streamlit as st
from utils import inject_style
st.set_page_config(page_title="Recommendations",page_icon="🧭",layout="wide"); inject_style(); st.title("🧭 Recommendation Centre")
r=st.session_state.get("last_prediction")
if r:
 st.subheader(f"Latest estimate: {r['risk_level']} ({r['risk_score']}/100)")
 for n,x in enumerate(r["recommendations"],1): st.markdown(f"**{n}.** {x}")
else: st.info("Run a prediction in Risk Lab to see tailored recommendations.")
st.divider(); st.subheader("General checklist")
st.checkbox("Check current conditions before outdoor exercise"); st.checkbox("Choose routes away from major traffic where practical"); st.checkbox("Re-check readings because conditions change"); st.checkbox("Follow local environmental authority guidance")

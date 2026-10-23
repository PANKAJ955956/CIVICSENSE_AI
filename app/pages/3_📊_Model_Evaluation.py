import streamlit as st,pandas as pd,plotly.express as px
from utils import inject_style,api_get
st.set_page_config(page_title="Model Evaluation",page_icon="📊",layout="wide"); inject_style(); st.title("📊 Model Evaluation")
data,err=api_get("/api/model-metrics")
if err: st.error("API unavailable: "+err)
elif "metrics" not in data: st.warning(data.get("message","No metrics yet; train models first."))
else:
 st.success("Best demo model: "+data["best_model"]); a,b,c=st.columns(3); a.metric("Rows",data["rows"]); b.metric("Train",data["train_rows"]); c.metric("Test",data["test_rows"])
 df=pd.DataFrame(data["metrics"]); st.dataframe(df,use_container_width=True,hide_index=True)
 st.plotly_chart(px.bar(df,x="model",y="RMSE",title="RMSE by model"),use_container_width=True)
 st.plotly_chart(px.bar(df,x="model",y="R2",title="R² by model"),use_container_width=True)
 st.warning(data.get("warning","Metrics depend on data quality and evaluation design."))

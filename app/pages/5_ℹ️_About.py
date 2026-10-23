import streamlit as st
from utils import inject_style
st.set_page_config(page_title="About",page_icon="ℹ️",layout="wide"); inject_style(); st.title("ℹ️ About CivicSense AI")
st.subheader("Architecture"); st.code("Open-Meteo APIs → FastAPI ingestion → validated inputs → scikit-learn model → REST prediction API → Streamlit UI")
st.markdown('''### ML lifecycle
1. Data generation / ingestion
2. Cleaning: missing values, infinities, duplicates
3. Train/test split (80/20, fixed seed)
4. Median imputation → scaling → model pipeline
5. Compare Random Forest, Extra Trees, Gradient Boosting and Hist Gradient Boosting
6. Evaluate MAE, RMSE and R²; persist best model with joblib
7. Serve predictions through FastAPI

### Production improvements
Use documented historical observations, time/location-held-out tests, data/model cards, drift monitoring, CI, Docker, authentication and accessibility checks.

### Limitations
Synthetic labels demonstrate software workflow only. They do not establish real-world predictive accuracy. This is not an official AQI or medical product.
''')

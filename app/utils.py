import requests,streamlit as st
API="http://127.0.0.1:8000"
def inject_style():
    st.markdown('<style>.stApp{background:linear-gradient(135deg,#f4f8ff,#f7fbfa,#edf5ff)} section[data-testid="stSidebar"]{background:#10233f} section[data-testid="stSidebar"] *{color:#f4f8ff!important} div[data-testid="stMetric"]{background:white;padding:16px;border-radius:14px;border:1px solid #dce7f3} .block-container{padding-top:2rem;max-width:1450px}</style>',unsafe_allow_html=True)
def api_get(path,params=None):
    try: r=requests.get(API+path,params=params,timeout=15); r.raise_for_status(); return r.json(),None
    except Exception as e: return None,str(e)
def api_post(path,payload):
    try: r=requests.post(API+path,json=payload,timeout=15); r.raise_for_status(); return r.json(),None
    except Exception as e: return None,str(e)

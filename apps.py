import streamlit as st
from utils.global_style import inject_global_style

st.set_page_config(
    page_title="Demo Dashboard Multi-Page",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_global_style()
st.sidebar.success("🔖 Pilih halaman dari sidebar")

# Streamlit akan otomatis memuat halaman dari folder 'pages/'
import streamlit as st
from utils.load_data import load_all_datasets
from utils.global_style import inject_global_style
from components.kpi_reviews import render_kpi_reviews
from components.trend_chart import render_trend_chart
from components.doughnut_chart import render_doughnut_chart

inject_global_style()
datasets = load_all_datasets()
order_reviews = datasets["order_reviews"]

st.markdown("<h3>KPI Review Pelanggan</h3>", unsafe_allow_html=True)
render_kpi_reviews(order_reviews)

col1, col2 = st.columns([3, 2])
with col1:
    st.subheader("Tren Bulanan Review (2016–2018)")
    render_trend_chart(order_reviews)

with col2:
    st.subheader("Distribusi Skor Review")
    render_doughnut_chart(order_reviews)
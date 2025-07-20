import streamlit as st
from utils.load_data import load_all_datasets
from utils.global_style import inject_global_style
from components.kpi_reviews import render_kpi_reviews
from components.trend_chart import render_trend_chart
from components.doughnut_chart import render_doughnut_chart

inject_global_style()
datasets = load_all_datasets()
order_reviews = datasets["order_reviews"]

st.markdown("""
<div style='padding: 0.5rem 1rem; background: linear-gradient(to right, #667eea, #764ba2); border-radius: 12px; text-align: center; margin-bottom: 1rem; box-shadow: 0 4px 10px rgba(0,0,0,0.1)'>
    <h3 style='margin: 0; color: #ffffff; font-weight: 600;'>Customer Satisfaction</h3>
</div>
""", unsafe_allow_html=True)


import pandas as pd

order_reviews['review_creation_date'] = pd.to_datetime(order_reviews['review_creation_date'])
min_date = order_reviews['review_creation_date'].min()
max_date = order_reviews['review_creation_date'].max()

col_start, col_end = st.columns(2)

with col_start:
    start_date = st.date_input(
        "Start Date",
        value=min_date,
        min_value=min_date,
        max_value=max_date,
        format="YYYY-MM-DD"
    )

with col_end:
    end_date = st.date_input(
        "End Date",
        value=max_date,
        min_value=min_date,
        max_value=max_date,
        format="YYYY-MM-DD"
    )

if start_date > end_date:
    st.warning("⚠️Data not exits.")
    st.stop()

filtered_reviews = order_reviews[
    (order_reviews['review_creation_date'] >= pd.to_datetime(start_date)) &
    (order_reviews['review_creation_date'] <= pd.to_datetime(end_date))
]


render_kpi_reviews(filtered_reviews)

col1, col2 = st.columns([3, 2])
with col1:
    st.markdown("### Customer Review Trend")
    render_trend_chart(filtered_reviews)

with col2:
    st.markdown("### Customer Rating Distribution")
    render_doughnut_chart(filtered_reviews)

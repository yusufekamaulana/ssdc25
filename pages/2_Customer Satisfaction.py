import streamlit as st
import pandas as pd
from utils.load_data import load_all_datasets
from utils.global_style import inject_global_style
from components.kpi_reviews import render_kpi_reviews
from components.trend_chart import render_trend_chart
from components.doughnut_chart import render_doughnut_chart
from components.topic_chart import render_topic_chart

inject_global_style()

st.set_page_config(
    layout="wide",
)

datasets = load_all_datasets()
order_reviews = datasets["order_reviews"]
order_reviews['review_creation_date'] = pd.to_datetime(order_reviews['review_creation_date'])
topics = datasets["topics"]
order_reviews = pd.merge(order_reviews, topics[["review_id", "topic_simplified"]], on="review_id", how="left")

st.markdown("""
<div style='padding: 0.5rem 1rem; background: linear-gradient(to right, #667eea, #764ba2); border-radius: 12px; text-align: center; margin-bottom: 1rem; box-shadow: 0 4px 10px rgba(0,0,0,0.1)'>
    <h3 style='margin: 0; color: #ffffff; font-weight: 600;'>Customer Satisfaction</h3>
</div>
""", unsafe_allow_html=True)

min_date = order_reviews['review_creation_date'].min().date()
max_date = order_reviews['review_creation_date'].max().date()

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
with col2:
    end_date = st.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

st.markdown("</div>", unsafe_allow_html=True)

if start_date > end_date:
    st.warning("⚠️ Invalid date range. Please adjust.")
    st.stop()

filtered_reviews = order_reviews[
    (order_reviews['review_creation_date'] >= pd.to_datetime(start_date)) &
    (order_reviews['review_creation_date'] <= pd.to_datetime(end_date))
]

st.markdown("<br>", unsafe_allow_html=True)

# KPI Cards
render_kpi_reviews(filtered_reviews)

st.markdown("<br>", unsafe_allow_html=True)

# Charts Section
with st.container():
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("""
        <div style='background-color: #ffffff; padding: 1rem; border-radius: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.05);'>
            <h4 style='text-align:center;'>Customer Review Trend</h4>
        """, unsafe_allow_html=True)
        render_trend_chart(filtered_reviews)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div style='background-color: #ffffff; padding: 1rem; border-radius: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.05);'>
            <h4 style='text-align:center;'>Rating Distribution</h4>
        """, unsafe_allow_html=True)
        render_doughnut_chart(filtered_reviews)
        st.markdown("</div>", unsafe_allow_html=True)


from components.topic_chart import render_topic_chart, render_topic_trend_chart,render_avg_rating_per_topic

st.markdown("### Customer Review (Topic Modeling Insights)")

with st.container():
    col1, col2 = st.columns(2)

    with col1:
        render_topic_chart(filtered_reviews)  # Bar Horizontal

    with col2:
        render_avg_rating_per_topic(filtered_reviews)  # bar
        

st.markdown("<br>", unsafe_allow_html=True)

render_topic_trend_chart(filtered_reviews)  # Full width trend chart

from components.topic_word import render_wordcloud_and_bigrams

st.markdown("---")
st.markdown("## Topic Exploration")

available_topics = datasets["topics"]["topic_simplified"].dropna().unique().tolist()
selected_topic = st.selectbox("Select a Topic", available_topics)

render_wordcloud_and_bigrams(datasets["topics"], selected_topic)

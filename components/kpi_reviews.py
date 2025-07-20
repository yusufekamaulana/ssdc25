import streamlit as st
import pandas as pd

def render_kpi_reviews(order_reviews):
    order_reviews['review_creation_date'] = pd.to_datetime(order_reviews['review_creation_date'])
    order_reviews['review_answer_timestamp'] = pd.to_datetime(order_reviews['review_answer_timestamp'])

    avg_review_score = order_reviews['review_score'].mean()
    bad_review_pct = (order_reviews['review_score'] <= 2).mean() * 100
    order_reviews['response_time_days'] = (
        order_reviews['review_answer_timestamp'] - order_reviews['review_creation_date']
    ).dt.total_seconds() / (3600 * 24)
    avg_response_time = order_reviews['response_time_days'].mean()
    answered_pct = order_reviews['review_answer_timestamp'].notna().mean() * 100

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Avg Review Score", f"{avg_review_score:.2f}")
    k2.metric("% Review Buruk (<=2)", f"{bad_review_pct:.1f}%")
    k3.metric("Avg Waktu Respon", f"{avg_response_time:.2f} hari")
    k4.metric("% Review Terjawab", f"{answered_pct:.1f}%")
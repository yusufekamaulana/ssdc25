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

    # Unified card styling (from render_kpi_card)
    card_style = """
    <style>
    .kpi-card {
        background-color: #f3f3fa;
        padding: 20px;
        border-radius: 16px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.08);
        text-align: center;
        margin-bottom: 10px;
        font-family: 'Segoe UI', sans-serif;
    }
    .kpi-card h5 {
        margin: 0;
        color: #3f51b5;
        font-size: 1rem;
    }
    .kpi-card h2 {
        margin: 6px 0;
        font-size: 2.2em;
    }
    .kpi-card p {
        color: #555;
        font-size: 0.9em;
        margin-top: 0;
    }
    </style>
    """
    st.markdown(card_style, unsafe_allow_html=True)

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.markdown(f'''
            <div class="kpi-card">
                <h5>Review Score</h5>
                <h2>{avg_review_score:.2f}</h2>
                <p>Average rating across all reviews</p>
            </div>
        ''', unsafe_allow_html=True)

    with k2:
        st.markdown(f'''
            <div class="kpi-card">
                <h5> Bad Reviews</h5>
                <h2>{bad_review_pct:.1f}%</h2>
                <p>Percentage of reviews rated 1 or 2</p>
            </div>
        ''', unsafe_allow_html=True)

    with k3:
        st.markdown(f'''
            <div class="kpi-card">
                <h5>Response Time</h5>
                <h2>{avg_response_time:.2f} days</h2>
                <p>Average</p>
            </div>
        ''', unsafe_allow_html=True)

    with k4:
        st.markdown(f'''
            <div class="kpi-card">
                <h5>Reviews Answered</h5>
                <h2>{answered_pct:.1f}%</h2>
                <p>Precentage</p>
            </div>
        ''', unsafe_allow_html=True)

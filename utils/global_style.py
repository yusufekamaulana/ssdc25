import streamlit as st

def inject_global_style():
    st.markdown("""
    <link href="https://fonts.googleapis.com/css2?family=Hubot+Sans:wg@400;500;600&display=swap" rel="stylesheet">
    <style>
    html, body, [class*="css"] {
        font-family: 'Hubot Sans', sans-serif;
        color: #1f2937;
    }
    [data-testid="stMetric"] {
        background-color: #f3f4f6;
        border-radius: 0.5rem;
        padding: 20px;
        text-align: center;
        border: 1px solid #e5e7eb;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    h1, h2, h3, h4 {
        font-weight: 600;
        color: #1f2937;
    }
    hr {
        border: none;
        border-top: 1px solid #e5e7eb;
        margin: 1.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
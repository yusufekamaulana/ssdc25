import streamlit as st
from utils.global_style import inject_global_style

# Page configuration
st.set_page_config(
    page_title="DELIVERY PERFORMANCE DASHBOARD",
    layout="wide",
    initial_sidebar_state="expanded"
)

inject_global_style()

# Main header
st.markdown("<h1 style='text-align: center;'>Delivery Performance Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: gray;'>Please select a section below to get started</h4>", unsafe_allow_html=True)
st.markdown("---")

# Card layout
cols = st.columns(2)

with cols[0]:
    st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 12px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); text-align: center;">
        <h3>Customer Satisfaction</h3>
        <p>Analyze customer satisfaction based on the latest review data</p>
        <a href="Customer_Satisfaction" target="_self">
            <button style="background: linear-gradient(to right, #667eea, #764ba2); border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer;">
                Open Page
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

with cols[1]:
    st.markdown(f"""
    <div style="background-color: #f0f2f6; padding: 20px; border-radius: 12px; box-shadow: 2px 2px 10px rgba(0,0,0,0.05); text-align: center;">
        <h3>Visualization Templates</h3>
        <p>Reusable data visualization templates for your analysis</p>
        <a href="Visualisasi_Template" target="_self">
            <button style="background: linear-gradient(to right, #667eea, #764ba2); border: none; color: white; padding: 10px 20px; border-radius: 8px; cursor: pointer;">
                Open Page
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

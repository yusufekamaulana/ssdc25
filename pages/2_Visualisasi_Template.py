import streamlit as st
from components.template_bar import render_bar_chart
from components.template_line import render_line_chart
from components.template_doughnut import render_doughnut_chart
from components.template_radar import render_radar_chart

st.title("🧩 Visualisasi Semua Template Chart")

with st.container():
    st.header("📊 Bar Chart")
    render_bar_chart("bar_demo", ["Jan", "Feb", "Mar", "Apr"], [80, 150, 120, 200])

with st.container():
    st.header("📈 Line Chart")
    render_line_chart("line_demo", ["Jan", "Feb", "Mar", "Apr"], [40, 60, 55, 70])

with st.container():
    st.header("🍩 Doughnut Chart")
    render_doughnut_chart(
        "doughnut_demo",
        ["Rating 1", "Rating 2", "Rating 3", "Rating 4", "Rating 5"],
        [5, 10, 20, 30, 35],
        [
            "rgba(239,68,68,0.7)",
            "rgba(251,191,36,0.7)",
            "rgba(253,224,71,0.7)",
            "rgba(132,204,22,0.7)",
            "rgba(34,197,94,0.7)"
        ]
    )

with st.container():
    st.header("📡 Radar Chart")
    render_radar_chart(
        "radar_demo",
        ["Speed", "Quality", "UX", "Reliability", "Support"],
        [70, 85, 90, 60, 75],
        dataset_label="Feedback Skor"
    )
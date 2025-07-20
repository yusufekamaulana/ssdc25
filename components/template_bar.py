import streamlit as st
import json

def render_bar_chart(chart_id, labels, values, label="Bar Data", color="rgba(59,130,246,0.6)", height=375):
    config = {
        "type": "bar",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": label,
                "data": values,
                "backgroundColor": color
            }]
        },
        "options": {
            "responsive": True,
            "maintainAspectRatio": False,
            "scales": {
                "y": {"beginAtZero": True}
            }
        }
    }
    html = f"""
    <div style='height:{height}px;'><canvas id="{chart_id}"></canvas></div>
    <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
    <script>
    new Chart(document.getElementById('{chart_id}'), {json.dumps(config)});
    </script>
    """
    st.components.v1.html(html, height=height + 20)
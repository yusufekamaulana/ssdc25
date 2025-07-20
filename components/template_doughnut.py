import streamlit as st
import json

def render_doughnut_chart(chart_id, labels, data, background_colors, height=375):
    config = {
        "type": "doughnut",
        "data": {
            "labels": labels,
            "datasets": [{
                "data": data,
                "backgroundColor": background_colors
            }]
        },
        "options": {
            "responsive": True,
            "maintainAspectRatio": False,
            "plugins": {
                "legend": {"position": "top"}
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
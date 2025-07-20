import streamlit as st
import json

def render_line_chart(chart_id, labels, values, label="Line Data", border_color="rgba(75, 192, 192, 1)", height=375):
    config = {
        "type": "line",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": label,
                "data": values,
                "borderColor": border_color,
                "tension": 0.4,
                "fill": False
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
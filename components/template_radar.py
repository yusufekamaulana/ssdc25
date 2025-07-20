import streamlit as st
import json

def render_radar_chart(chart_id, labels, data, dataset_label="Radar", color="rgba(54, 162, 235, 0.5)", height=375):
    config = {
        "type": "radar",
        "data": {
            "labels": labels,
            "datasets": [{
                "label": dataset_label,
                "data": data,
                "backgroundColor": color,
                "borderColor": color.replace("0.5", "1"),
                "pointBackgroundColor": color.replace("0.5", "1")
            }]
        },
        "options": {
            "responsive": True,
            "maintainAspectRatio": False
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
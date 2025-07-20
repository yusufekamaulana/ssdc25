import streamlit as st
import json

def render_doughnut_chart(order_reviews):
    scores = order_reviews['review_score'].value_counts().sort_index()
    labels = [f"{s}" for s in scores.index.tolist()]
    data = scores.values.tolist()
    colors = [
        "rgba(239,68,68,0.7)",
        "rgba(251,191,36,0.7)",
        "rgba(253,224,71,0.7)",
        "rgba(132,204,22,0.7)",
        "rgba(34,197,94,0.7)"
    ]

    doughnut_html = f"""
    <div class="bg-white rounded-lg shadow-md p-4" style="height:375px;"><canvas id="reviewDoughnut"></canvas></div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('reviewDoughnut'), {{
        type: 'doughnut',
        data: {{
            labels: {json.dumps(labels)},
            datasets: [{{
                label: 'Distribusi Skor Review',
                data: {json.dumps(data)},
                backgroundColor: {json.dumps(colors)},
                borderWidth: 1
            }}]
        }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{
                    position: 'top'
                }}
            }}
        }}
    }});
    </script>
    """
    st.components.v1.html(doughnut_html, height=400)
import streamlit as st
import json

def render_line_chart(labels, data, title, canvas_id, line_color):
    st.markdown(f"<h4 style='text-align:center;'>{title}</h4>", unsafe_allow_html=True)
    html = f"""
    <div class='bg-white rounded-lg shadow-md p-4' style='height:375px;'><canvas id='{canvas_id}'></canvas></div>
    <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
    <script>
    new Chart(document.getElementById('{canvas_id}'), {{
        type: 'line',
        data: {{
            labels: {json.dumps(labels)},
            datasets: [{{
                label: '{title}',
                data: {json.dumps(data)},
                borderColor: '{line_color}',
                backgroundColor: '{line_color}1A',
                fill: true,
                tension: 0.3,
                pointBackgroundColor: '{line_color}',
                pointRadius: 4
            }}]
        }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                tooltip: {{
                    backgroundColor: '#1f2937',
                    titleColor: '#fefefe',
                    bodyColor: '#fefefe'
                }},
                legend: {{
                    display: false
                }}
            }},
            scales: {{
                y: {{
                    beginAtZero: true,
                    ticks: {{ color: '#4b5563' }},
                    grid: {{ color: '#e5e7eb' }}
                }},
                x: {{
                    ticks: {{ color: '#4b5563' }},
                    grid: {{ display: false }}
                }}
            }}
        }}
    }});
    </script>
    """
    st.components.v1.html(html, height=400)

import streamlit as st
import json

def render_topic_chart(order_reviews):
    topic_counts = order_reviews["topic_simplified"].value_counts().sort_values(ascending=False)
    labels = topic_counts.index.tolist()
    data = topic_counts.values.tolist()

    colors = [
        "rgba(59,130,246,0.7)",  # blue
        "rgba(236,72,153,0.7)",  # pink
        "rgba(16,185,129,0.7)",  # emerald
        "rgba(234,179,8,0.7)",   # yellow
        "rgba(168,85,247,0.7)",  # purple
        "rgba(251,113,133,0.7)", # rose
        "rgba(14,165,233,0.7)",  # sky
        "rgba(245,158,11,0.7)",  # amber
    ]

    bar_html = f"""
    <div class="bg-white rounded-lg shadow-md p-4" style="height:400px;"><canvas id="topicBar"></canvas></div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('topicBar'), {{
        type: 'bar',
        data: {{
            labels: {json.dumps(labels)},
            datasets: [{{
                label: 'Review Count',
                data: {json.dumps(data)},
                backgroundColor: {json.dumps(colors[:len(labels)])},
                borderRadius: 6
            }}]
        }},
        options: {{
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                legend: {{
                    display: false
                }},
                title: {{
                    display: true,
                    text: 'Review Count per Topic'
                }}
            }},
            scales: {{
                x: {{
                    beginAtZero: true
                }}
            }}
        }}
    }});
    </script>
    """
    st.components.v1.html(bar_html, height=420)

def render_topic_trend_chart(order_reviews):
    df = order_reviews.copy()
    df['month'] = df['review_creation_date'].dt.to_period('M').astype(str)
    grouped = df.groupby(['month', 'topic_simplified']).size().reset_index(name='count')
    pivot = grouped.pivot(index='month', columns='topic_simplified', values='count').fillna(0)

    labels = pivot.index.tolist()
    datasets = []
    color_pool = [
        "rgba(59,130,246,0.7)", "rgba(236,72,153,0.7)", "rgba(234,179,8,0.7)",
        "rgba(16,185,129,0.7)", "rgba(168,85,247,0.7)", "rgba(251,113,133,0.7)"
    ]

    for i, col in enumerate(pivot.columns[:5]):  # ambil top 5 topik
        datasets.append({
            "label": col,
            "data": pivot[col].tolist(),
            "fill": False,
            "borderColor": color_pool[i % len(color_pool)],
            "tension": 0.2
        })

    line_html = f"""
    <div class="bg-white rounded-lg shadow-md p-4" style="height:400px;"><canvas id="topicTrend"></canvas></div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('topicTrend'), {{
        type: 'line',
        data: {{
            labels: {json.dumps(labels)},
            datasets: {json.dumps(datasets)}
        }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            plugins: {{
                title: {{
                    display: true,
                    text: 'Monthly Trend of Topics'
                }}
            }},
            scales: {{
                y: {{
                    beginAtZero: true
                }}
            }}
        }}
    }});
    </script>
    """
    st.components.v1.html(line_html, height=430)


import streamlit as st
import json

def render_avg_rating_per_topic(order_reviews):
    df = order_reviews.copy()
    avg_ratings = df.groupby("topic_simplified")["review_score"].mean().sort_values()

    labels = avg_ratings.index.tolist()
    values = avg_ratings.values.round(2).tolist()
    colors = ["rgba(72,187,120,0.8)" if v > 3 else "rgba(239,68,68,0.7)" for v in values]

    bar_html = f"""
    <div class="bg-white rounded-lg shadow-md p-4" style="height:400px;"><canvas id="avgRatingBar"></canvas></div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('avgRatingBar'), {{
        type: 'bar',
        data: {{
            labels: {json.dumps(labels)},
            datasets: [{{
                label: 'Average Rating',
                data: {json.dumps(values)},
                backgroundColor: {json.dumps(colors)},
                borderWidth: 1
            }}]
        }},
        options: {{
            responsive: true,
            maintainAspectRatio: false,
            scales: {{
                y: {{
                    beginAtZero: true,
                    max: 5
                }}
            }},
            plugins: {{
                title: {{
                    display: true,
                    text: 'Average Rating per Topic'
                }},
                legend: {{
                    display: false
                }}
            }}
        }}
    }});
    </script>
    """
    st.components.v1.html(bar_html, height=430)

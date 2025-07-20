import streamlit as st
import json

def render_trend_chart(order_reviews):
    monthly = order_reviews.groupby(
        order_reviews['review_creation_date'].dt.to_period('M')
    ).agg(
        review_count=('review_id', 'count'),
        avg_score=('review_score', 'mean')
    )
    monthly.index = monthly.index.astype(str)
    labels = monthly.index.tolist()
    counts = monthly['review_count'].tolist()
    avgs = monthly['avg_score'].tolist()

    trend_html = f"""
    <div class="bg-white rounded-lg shadow-md p-4" style="height:375px;">
        <canvas id="trendChart"></canvas>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
    new Chart(document.getElementById('trendChart'), {{
        data: {{
            labels: {json.dumps(labels)},
            datasets: [
                {{
                    type:'bar',
                    label:'Jumlah Review',
                    data: {json.dumps(counts)},
                    backgroundColor:'rgba(59,130,246,0.6)',
                    yAxisID:'y'
                }},
                {{
                    type:'line',
                    label:'Skor Rata-rata',
                    data: {json.dumps(avgs)},
                    borderColor:'rgba(241,90,34,1)',
                    fill:false,
                    tension:0.4,
                    yAxisID:'y1'
                }}
            ]
        }},
        options: {{
            responsive:true,
            maintainAspectRatio:false,
            scales: {{
                y: {{
                    position:'left',
                    beginAtZero:true,
                    title: {{display:true, text:'Jumlah Review'}}
                }},
                y1: {{
                    position:'right',
                    beginAtZero:true,
                    title: {{display:true, text:'Skor Rata-rata'}}
                }}
            }}
        }}
    }});
    </script>
    """
    st.components.v1.html(trend_html, height=400)
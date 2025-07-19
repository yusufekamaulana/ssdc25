import streamlit as st
import json
import random
import pandas as pd
from datetime import datetime

# -----------------------
# Konfigurasi Halaman
# -----------------------
st.set_page_config(
    page_title="Demo Dashboard Multi-Page",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------
# Global Styling
# -----------------------
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Hubot+Sans:wg@400;500;600&display=swap" rel="stylesheet">
<style>
html, body, [class*="css"] {
    font-family: 'Hubot Sans', sans-serif;
    color: #1f2937;
}
[data-testid="stMetric"] {
    background-color: #f3f4f6;
    border-radius: 0.5rem;
    padding: 20px;
    text-align: center;
    border: 1px solid #e5e7eb;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
h1, h2, h3, h4 {
    font-weight: 600;
    color: #1f2937;
}
hr {
    border: none;
    border-top: 1px solid #e5e7eb;
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# -----------------------
# Load Data
# -----------------------
closed_deals = pd.read_csv("E-commerce/closed_deals_dataset.csv")
customers = pd.read_csv("E-commerce/customers_dataset.csv")
geolocation = pd.read_csv("E-commerce/geolocation_dataset.csv")
marketing_leads = pd.read_csv("E-commerce/marketing_qualified_leads_dataset.csv")
order_items = pd.read_csv("E-commerce/order_items_dataset.csv")
order_payments = pd.read_csv("E-commerce/order_payments_dataset.csv")
order_reviews = pd.read_csv("E-commerce/order_reviews_dataset.csv")
orders = pd.read_csv("E-commerce/orders_dataset.csv")
product_category_translation = pd.read_csv("E-commerce/product_category_name_translation.csv")
products = pd.read_csv("E-commerce/products_dataset.csv")
sellers = pd.read_csv("E-commerce/sellers_dataset.csv")

# -----------------------
# Simulasi Data Chart.js
# -----------------------
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
bar_vals = [random.randint(50, 200) for _ in months]
line_vals = [random.uniform(20, 100) for _ in months]
stacked_vals = {
    "Produk A": [random.randint(20, 100) for _ in months],
    "Produk B": [random.randint(20, 100) for _ in months],
    "Produk C": [random.randint(20, 100) for _ in months]
}
mixed_sales = [random.randint(50, 200) for _ in months]
mixed_growth = [random.uniform(1, 10) for _ in months]
radar_labels = ["Speed", "Quality", "UX", "Reliability", "Support"]
radar_data = [random.randint(50, 100) for _ in radar_labels]
polar_labels = ["Asia", "Europe", "NA", "SA", "Africa"]
polar_data = [random.randint(10, 60) for _ in polar_labels]

stacked_json = json.dumps({
    "labels": months,
    "datasets": [
        {"label": key, "data": val, "backgroundColor": f"rgba({i*40}, {100+i*30}, {200-i*30}, 0.6)"}
        for i, (key, val) in enumerate(stacked_vals.items())
    ]
})
mixed_json = json.dumps({
    "labels": months,
    "datasets": [
        {"type": "bar", "label": "Sales", "data": mixed_sales, "backgroundColor": "rgba(59,130,246,0.6)"},
        {"type": "line", "label": "Growth %", "data": mixed_growth, "borderColor": "rgba(241,90,34,1)", "fill": False}
    ]
})
radar_json = json.dumps({
    "labels": radar_labels,
    "datasets": [{
        "label": "Performance",
        "data": radar_data,
        "backgroundColor": "rgba(164,101,241,0.4)",
        "borderColor": "rgba(164,101,241,1)",
        "pointBackgroundColor": "rgba(164,101,241,1)"
    }]
})
polar_json = json.dumps({
    "labels": polar_labels,
    "datasets": [{
        "label": "Users by Region",
        "data": polar_data,
        "backgroundColor": [
            "rgba(59,130,246,0.6)",
            "rgba(16,185,129,0.6)",
            "rgba(241,90,34,0.6)",
            "rgba(245,158,11,0.6)",
            "rgba(233,30,99,0.6)"
        ]
    }]
})

kpi_sales = random.randint(15000, 30000)

# -----------------------
# Navigasi Halaman
# -----------------------
page = st.sidebar.selectbox("🔖 Pilih Halaman", [
    "Dashboard Utama",
    "Visualisasi Lanjutan"
])

# -----------------------
# Halaman: Dashboard Utama
# -----------------------
if page == "Dashboard Utama":
    # KPI Awal
    # c1, c2, c3, c4 = st.columns(4)
    # with c1: st.metric("New Accounts", "234%")
    # with c2: st.metric("Total Expenses", "71%")
    # with c3: st.metric("Company Value", "$1,45M")
    # with c4: st.metric("New Employees", "+34 hires")
    # st.markdown("<hr>", unsafe_allow_html=True)

    order_reviews['review_creation_date'] = pd.to_datetime(order_reviews['review_creation_date'])
    order_reviews['review_answer_timestamp'] = pd.to_datetime(order_reviews['review_answer_timestamp'])

    avg_review_score = order_reviews['review_score'].mean()
    bad_review_pct = (order_reviews['review_score'] <= 2).mean() * 100

    order_reviews['response_time_days'] = (
        order_reviews['review_answer_timestamp'] - order_reviews['review_creation_date']
    ).dt.total_seconds() / (3600 * 24)

    avg_response_time = order_reviews['response_time_days'].mean()
    answered_pct = order_reviews['review_answer_timestamp'].notna().mean() * 100

    st.markdown("""
    <h3 style='display:flex;align-items:center;gap:8px;'>
        <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" width="24" height="24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.563 4.79a1 1 0 00.95.69h5.029c.969 0 1.371 1.24.588 1.81l-4.072 2.96a1 1 0 00-.364 1.118l1.563 4.79c.3.921-.755 1.688-1.538 1.118l-4.072-2.96a1 1 0 00-1.176 0l-4.072 2.96c-.783.57-1.838-.197-1.538-1.118l1.563-4.79a1 1 0 00-.364-1.118l-4.072-2.96c-.783-.57-.38-1.81.588-1.81h5.029a1 1 0 00.95-.69l1.563-4.79z" />
        </svg>
        KPI Review Pelanggan
    </h3>
    """, unsafe_allow_html=True)

    # ⬇️ INI YANG KAMU LUPA
    k1, k2, k3, k4 = st.columns(4)

    k1.metric("Avg Review Score", f"{avg_review_score:.2f}")
    k2.metric("% Review Buruk (<=2)", f"{bad_review_pct:.1f}%")
    k3.metric("Avg Waktu Respon", f"{avg_response_time:.2f} hari")
    k4.metric("% Review Terjawab", f"{answered_pct:.1f}%")

    # -----------------------
    # Distribusi Review & Tren Bulanan dalam 1 Baris (Doughnut di kanan)
    # -----------------------
    col_mixed, col_doughnut = st.columns([3, 2])  # mixed kiri, doughnut kanan

    # Chart Mixed (Trend)
    with col_mixed:
        st.subheader("Tren Bulanan Review (2016–2018)")
        monthly = order_reviews.groupby(
            pd.Grouper(key='review_creation_date', freq='M')
        ).agg(
            review_count=('review_id', 'count'),
            avg_score=('review_score', 'mean')
        )

        monthly.index = monthly.index.strftime("%Y-%m")
        labels_m = monthly.index.tolist()
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
                labels: {json.dumps(labels_m)},
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

    # Chart Doughnut (pindah ke kanan + legend di atas)
    with col_doughnut:
        st.subheader("Distribusi Skor Review")
        scores = order_reviews['review_score'].value_counts().sort_index()
        labels = [f"Rating {s}" for s in scores.index.tolist()]
        data = scores.values.tolist()
        colors = [
            "rgba(239,68,68,0.7)",   # Rating 1
            "rgba(251,191,36,0.7)",  # Rating 2
            "rgba(253,224,71,0.7)",  # Rating 3
            "rgba(132,204,22,0.7)",  # Rating 4
            "rgba(34,197,94,0.7)"    # Rating 5
        ]

        doughnut_html = f"""
        <div class="bg-white rounded-lg shadow-md p-4" style="height:375px;">
        <canvas id="reviewDoughnut"></canvas>
        </div>
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
                        position: 'top'  // ← legend dipindah ke atas
                    }}
                }}
            }}
        }});
        </script>
        """
        st.components.v1.html(doughnut_html, height=400)


else:
    st.header("📈 Visualisasi Lanjutan")
    st.markdown("Visualisasi tambahan dengan layout modular dan elemen pemisah visual.")

    st.markdown("<hr>", unsafe_allow_html=True)

    style_block = """
    background: linear-gradient(145deg, #f9fafb, #f3f4f6);
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    border: 1px solid #e5e7eb;
    height: 350px;
    background-size: 8px 8px;
    background-image: repeating-linear-gradient(
        45deg,
        rgba(0,0,0,0.02),
        rgba(0,0,0,0.02) 1px,
        transparent 1px,
        transparent 4px
    );
    """

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Stacked Bar Chart")
        st.components.v1.html(f"""
        <div style="{style_block}">
            <canvas id="stackedBar"></canvas>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script>
            new Chart(document.getElementById('stackedBar'), {{
                type: 'bar',
                data: {stacked_json},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        x: {{ stacked: true }},
                        y: {{ stacked: true, beginAtZero: true }}
                    }}
                }}
            }});
            </script>
        </div>
        """ , height=370)

    with col2:
        st.subheader("Mixed Bar-Line Chart")
        st.components.v1.html(f"""
        <div style="{style_block}">
            <canvas id="mixedChart"></canvas>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script>
            new Chart(document.getElementById('mixedChart'), {{
                data: {mixed_json},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false
                }}
            }});
            </script>
        </div>
        """ , height=370)

    st.markdown("<hr>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Radar Chart")
        st.components.v1.html(f"""
        <div style="{style_block}">
            <canvas id="radarChart"></canvas>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script>
            new Chart(document.getElementById('radarChart'), {{
                type: 'radar',
                data: {radar_json},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {{
                        r: {{
                            angleLines: {{ color: '#ccc' }},
                            suggestedMin: 0,
                            suggestedMax: 100
                        }}
                    }}
                }}
            }});
            </script>
        </div>
        """ , height=370)

    with col4:
        st.subheader("Polar Area Chart")
        st.components.v1.html(f"""
        <div style="{style_block}">
            <canvas id="polarChart"></canvas>
            <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            <script>
            new Chart(document.getElementById('polarChart'), {{
                type: 'polarArea',
                data: {polar_json},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false
                }}
            }});
            </script>
        </div>
        """ , height=370)

    st.markdown("<hr>", unsafe_allow_html=True)
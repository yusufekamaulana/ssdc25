import streamlit as st
import plotly.express as px
import pandas as pd
import json
from utils.load_data import load_all_datasets
from utils.global_style import inject_global_style

st.set_page_config(
    layout="wide",
)

inject_global_style()

datasets = load_all_datasets()
orders = datasets["orders"]
order_items = datasets["order_items"]
customers = datasets['customers']
orders = orders.merge(customers[['customer_id', 'customer_state']], on='customer_id', how='left')


# Format tanggal
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
orders['order_estimated_delivery_date'] = pd.to_datetime(orders['order_estimated_delivery_date'])

# Rentang tanggal
min_date = orders['order_purchase_timestamp'].min()
max_date = orders['order_purchase_timestamp'].max()

st.markdown("""
<div style='padding: 0.5rem 1rem; background: linear-gradient(to right, #667eea, #764ba2); border-radius: 12px; text-align: center; margin-bottom: 1rem; box-shadow: 0 4px 10px rgba(0,0,0,0.1)'>
    <h3 style='margin: 0; color: #ffffff; font-weight: 600;'>Delivery performances</h3>
</div>
""", unsafe_allow_html=True)

# Filter tanggal
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=min_date, min_value=min_date, max_value=max_date)
    with col2:
        end_date = st.date_input("End Date", value=max_date, min_value=min_date, max_value=max_date)

    st.markdown("</div>", unsafe_allow_html=True)


if start_date > end_date:
    st.warning("⚠️ Invalid date range. Please adjust.")
    st.stop()

# Filter orders
filtered_orders = orders[(orders['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
                         (orders['order_purchase_timestamp'] <= pd.to_datetime(end_date))].copy()

# Dropdown filter region (customer_state)
state_mapping = {
    'SP': 'São Paulo',
    'SC': 'Santa Catarina',
    'MG': 'Minas Gerais',
    'PR': 'Paraná',
    'RJ': 'Rio de Janeiro',
    'RS': 'Rio Grande do Sul',
    'PA': 'Pará',
    'GO': 'Goiás',
    'ES': 'Espírito Santo',
    'BA': 'Bahia',
    'MA': 'Maranhão',
    'MS': 'Mato Grosso do Sul',
    'CE': 'Ceará',
    'DF': 'Distrito Federal',
    'RN': 'Rio Grande do Norte',
    'PE': 'Pernambuco',
    'MT': 'Mato Grosso',
    'AM': 'Amazonas',
    'AP': 'Amapá',
    'AL': 'Alagoas',
    'RO': 'Rondônia',
    'PB': 'Paraíba',
    'TO': 'Tocantins',
    'PI': 'Piauí',
    'AC': 'Acre',
    'SE': 'Sergipe',
    'RR': 'Roraima'
}
# Mengambil daftar customer_state dari data yang terfilter
region_options = filtered_orders['customer_state'].dropna().unique().tolist()

# Mapping kode state ke nama lengkap menggunakan dictionary
region_options_display = [state_mapping[state] for state in region_options]

# Dropdown filter region (customer_state) dengan nama lengkap
selected_region = st.selectbox("Select Region (Customer State)", options=["All"] + region_options_display)

# Filter berdasarkan region jika dipilih
if selected_region != "All":
    # Cari kode state dari nama lengkap yang dipilih
    selected_region_code = [key for key, value in state_mapping.items() if value == selected_region][0]
    filtered_orders = filtered_orders[filtered_orders['customer_state'] == selected_region_code]


# Chart 1: Non-damaged (delivered)
filtered_orders['year_month'] = filtered_orders['order_purchase_timestamp'].dt.to_period('M')
monthly_orders = filtered_orders.groupby('year_month').agg(
    total_orders=('order_id', 'count'),
    delivered_orders=('order_status', lambda x: (x == 'delivered').sum())
)
monthly_orders['non_damaged_percentage'] = 100 * monthly_orders['delivered_orders'] / monthly_orders['total_orders']
labels1 = monthly_orders.index.astype(str).tolist()
data1 = monthly_orders['non_damaged_percentage'].round(2).tolist()

# Chart 2: Complete vs Incomplete
order_items_grouped = order_items.groupby('order_id').size()
complete_ids = order_items_grouped[order_items_grouped > 0].index
complete_orders = filtered_orders[filtered_orders['order_id'].isin(complete_ids)]
incomplete_orders = filtered_orders[~filtered_orders['order_id'].isin(complete_ids)]
data2 = [len(complete_orders), len(incomplete_orders)]

# Chart 3: On-time %
filtered_orders['on_time'] = filtered_orders['order_delivered_customer_date'] <= filtered_orders['order_estimated_delivery_date']
monthly_ontime = filtered_orders.groupby('year_month').agg(
    total=('order_id', 'count'),
    ontime=('on_time', 'sum')
)
monthly_ontime['on_time_percentage'] = 100 * monthly_ontime['ontime'] / monthly_ontime['total']
labels3 = monthly_ontime.index.astype(str).tolist()
data3 = monthly_ontime['on_time_percentage'].round(2).tolist()

# Chart 4: On time vs Late
on_time_count = filtered_orders['on_time'].sum()
late_count = (~filtered_orders['on_time']).sum()
data4 = [int(on_time_count), int(late_count)]

# ========== RENDER CHARTS ===========

with st.container():
    col1, col2 = st.columns([5, 3])
    with col1:
        st.markdown("<h4 style='text-align:center;'>% Delivered (Non-damaged Proxy)</h4>", unsafe_allow_html=True)
        html1 = f"""
        <div class='bg-white rounded-lg shadow-md p-4' style='height:375px;'><canvas id='line1'></canvas></div>
        <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
        <script>
        new Chart(document.getElementById('line1'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(labels1)},
                datasets: [{{
                    label: '% Delivered',
                    data: {json.dumps(data1)},
                    borderColor: 'rgba(59,130,246,1)',
                    backgroundColor: 'rgba(59,130,246,0.1)',
                    fill: true,
                    tension: 0.3,
                    pointBackgroundColor: 'rgba(59,130,246,1)',
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
                        ticks: {{
                            color: '#4b5563'
                        }},
                        grid: {{
                            color: '#e5e7eb'
                        }}
                    }},
                    x: {{
                        ticks: {{
                            color: '#4b5563'
                        }},
                        grid: {{
                            display: false
                        }}
                    }}
                }}
            }}
        }});
        </script>
        """
        st.components.v1.html(html1, height=400)
        st.markdown("<br>", unsafe_allow_html=True)

    with col2:
        st.markdown("<h4 style='text-align:center;'>Complete vs Incomplete</h4>", unsafe_allow_html=True)
        html2 = f"""
        <div class='bg-white rounded-lg shadow-md p-4' style='height:375px;'><canvas id='bar1'></canvas></div>
        <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
        <script>
        new Chart(document.getElementById('bar1'), {{
            type: 'bar',
            data: {{
                labels: ['Complete', 'Incomplete'],
                datasets: [{{
                    label: 'Order Count',
                    data: {json.dumps(data2)},
                    backgroundColor: ['#16a34a', '#dc2626'],
                    borderRadius: 6,
                    borderSkipped: false
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
                        ticks: {{
                            color: '#4b5563'
                        }},
                        grid: {{
                            color: '#e5e7eb'
                        }}
                    }},
                    x: {{
                        ticks: {{
                            color: '#4b5563'
                        }},
                        grid: {{
                            display: false
                        }}
                    }}
                }}
            }}
        }});
        </script>
        """
        st.components.v1.html(html2, height=400)
        st.markdown("<br>", unsafe_allow_html=True)

with st.container():
    col3, col4 = st.columns([5, 3])
    with col3:
        # Judul chart dinamis berdasarkan region
        st.markdown(f"<h4 style='text-align:center;'>% On-time Delivery{' for ' + selected_region if selected_region != 'All' else ''}</h4>", unsafe_allow_html=True)

        html3 = f"""
        <div class='bg-white rounded-lg shadow-md p-4' style='height:375px;'><canvas id='line2'></canvas></div>
        <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
        <script>
        new Chart(document.getElementById('line2'), {{
            type: 'line',
            data: {{
                labels: {json.dumps(labels3)},
                datasets: [{{
                    label: '% On Time',
                    data: {json.dumps(data3)},
                    borderColor: '#16a34a',
                    backgroundColor: 'rgba(22,163,74,0.1)',
                    fill: true,
                    tension: 0.3,
                    pointBackgroundColor: '#16a34a',
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
                        ticks: {{
                            color: '#4b5563'
                        }},
                        grid: {{
                            color: '#e5e7eb'
                        }}
                    }},
                    x: {{
                        ticks: {{
                            color: '#4b5563'
                        }},
                        grid: {{
                            display: false
                        }}
                    }}
                }}
            }}
        }});
        </script>
        """
        st.components.v1.html(html3, height=400)
        st.markdown("<br>", unsafe_allow_html=True)

    with col4:
        st.markdown("<h4 style='text-align:center;'>On-time vs Late</h4>", unsafe_allow_html=True)
        html4 = f"""
        <div class='bg-white rounded-lg shadow-md p-4' style='height:375px;'><canvas id='bar2'></canvas></div>
        <script src='https://cdn.jsdelivr.net/npm/chart.js'></script>
        <script>
        new Chart(document.getElementById('bar2'), {{
            type: 'bar',
            data: {{
                labels: ['On Time', 'Late'],
                datasets: [{{
                    label: 'Order Count',
                    data: {json.dumps(data4)},
                    backgroundColor: ['#16a34a', '#dc2626'],
                    borderRadius: 6,
                    borderSkipped: false
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
                        ticks: {{
                            color: '#4b5563'
                        }},
                        grid: {{
                            color: '#e5e7eb'
                        }}
                    }},
                    x: {{
                        ticks: {{
                            color: '#4b5563'
                        }},
                        grid: {{
                            display: false
                        }}
                    }}
                }}
            }}
        }});
        </script>
        """
        st.components.v1.html(html4, height=400)
        st.markdown("<br>", unsafe_allow_html=True)

import streamlit as st
import pandas as pd
import plotly.express as px

# Contoh data dummy jika belum punya filtered_orders (hapus ini kalau data sudah ada)
# filtered_orders = pd.DataFrame({
#     'customer_state': ['SP', 'RJ', 'MG', 'RS', 'BA', 'SC', 'SP', 'SP', 'RJ', 'MG'],
#     'order_id': range(10),
#     'on_time': [True, False, True, True, False, True, True, False, True, False]
# })

# Koordinat geografis per state
state_coordinates = {
    'SP': [-23.5505, -46.6333], 'SC': [-27.5954, -48.5480], 'MG': [-19.8157, -43.9542],
    'PR': [-25.4284, -49.2733], 'RJ': [-22.9068, -43.1729], 'RS': [-30.0346, -51.2177],
    'PA': [-1.4550, -48.4900], 'GO': [-16.6868, -49.2647], 'ES': [-20.3155, -40.3128],
    'BA': [-12.9714, -38.5014], 'MA': [-2.5396, -44.2807], 'MS': [-20.4697, -54.6201],
    'CE': [-3.7172, -38.5437], 'DF': [-15.7801, -47.9292], 'RN': [-5.7945, -35.2110],
    'PE': [-8.0476, -34.8770], 'MT': [-12.6376, -56.0966], 'AM': [-3.1190, -60.1770],
    'AP': [0.9020, -52.0173], 'AL': [-9.5714, -36.7820], 'RO': [-10.1905, -64.9039],
    'PB': [-7.1151, -34.8610], 'TO': [-10.1851, -48.3337], 'PI': [-5.0891, -42.8014],
    'AC': [-8.7737, -70.5510], 'SE': [-10.9472, -37.0731], 'RR': [2.8311, -60.6743]
}

# Hitung jumlah pengiriman per customer_state
delivery_by_state = filtered_orders.groupby('customer_state').agg(
    total_orders=('order_id', 'count'),
    on_time_orders=('on_time', 'sum'),
    late_orders=('on_time', lambda x: (~x).sum())
).reset_index()

# Tambahkan koordinat ke dataframe
delivery_by_state['lat'], delivery_by_state['lon'] = zip(*delivery_by_state['customer_state'].map(
    lambda x: state_coordinates.get(x, [None, None])
))

# Pilihan metrik
st.markdown("## 📦 Heatmap Status Pengiriman per Region")
metric = st.radio("🔍 Pilih Metode Evaluasi Pengiriman:", ("Pengiriman Tepat Waktu", "Pengiriman Terlambat"))

# Penyesuaian data berdasarkan pilihan
if metric == "Pengiriman Tepat Waktu":
    color_column = 'on_time_orders'
    legend_title = "Jumlah Tepat Waktu"
    color_scale = 'Turbo'
else:
    color_column = 'late_orders'
    legend_title = "Jumlah Terlambat"
    color_scale = 'Plasma'

# Plot peta
fig = px.scatter_geo(
    delivery_by_state,
    lat='lat',
    lon='lon',
    color=color_column,
    hover_name='customer_state',
    size='total_orders',
    size_max=40,
    color_continuous_scale=color_scale,
    projection='natural earth',
    labels={color_column: legend_title},
    hover_data={
        'total_orders': True,
        'on_time_orders': True,
        'late_orders': True,
        'lat': False,
        'lon': False
    },
    template='plotly_white'
)

# Tambahkan styling geo
fig.update_geos(
    showcountries=True,
    countrycolor="gray",
    showcoastlines=True,
    coastlinecolor="lightgray",
    showland=True,
    landcolor="whitesmoke",
    showocean=True,
    oceancolor="azure",
    fitbounds="locations",
    lataxis_range=[-35, 5],
    lonaxis_range=[-75, -30]
)

# Tambahkan judul yang menarik
fig.update_layout(
    title={
        'text': f"<b>Status Pengiriman per Region</b><br><sub>Evaluasi: {legend_title}</sub>",
        'x': 0.5,
        'xanchor': 'center'
    },
    margin={"r":0,"t":60,"l":0,"b":0},
    coloraxis_colorbar=dict(
        title=legend_title,
        ticks="outside",
        tickformat=",",
        len=0.75
    )
)

# Tambahkan anotasi ke São Paulo (jika ada datanya)
if 'SP' in delivery_by_state['customer_state'].values:
    fig.add_annotation(
        x=-46.6333, y=-23.5505,
        text="🔥 Tertinggi",
        showarrow=True,
        arrowhead=2,
        font=dict(size=12),
        bgcolor="yellow",
        ax=0, ay=-40
    )

# Tampilkan chart di dalam container
with st.container():
    st.plotly_chart(fig, use_container_width=True)

import streamlit as st
import plotly.express as px
import pandas as pd
import json
from utils.load_data import load_all_datasets
from utils.global_style import inject_global_style

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
    <h3 style='margin: 0; color: #ffffff; font-weight: 600;'>Order Quality Analysis</h3>
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

# Definisikan koordinat geografis untuk setiap state
state_coordinates = {
    'SP': [-23.5505, -46.6333],  # São Paulo
    'SC': [-27.5954, -48.5480],  # Santa Catarina
    'MG': [-19.8157, -43.9542],  # Minas Gerais
    'PR': [-25.4284, -49.2733],  # Paraná
    'RJ': [-22.9068, -43.1729],  # Rio de Janeiro
    'RS': [-30.0346, -51.2177],  # Rio Grande do Sul
    'PA': [-1.4550, -48.4900],   # Pará
    'GO': [-16.6868, -49.2647],  # Goiás
    'ES': [-20.3155, -40.3128],  # Espírito Santo
    'BA': [-12.9714, -38.5014],  # Bahia
    'MA': [-2.5396, -44.2807],   # Maranhão
    'MS': [-20.4697, -54.6201],  # Mato Grosso do Sul
    'CE': [-3.7172, -38.5437],   # Ceará
    'DF': [-15.7801, -47.9292],  # Distrito Federal
    'RN': [-5.7945, -35.2110],   # Rio Grande do Norte
    'PE': [-8.0476, -34.8770],   # Pernambuco
    'MT': [-12.6376, -56.0966],  # Mato Grosso
    'AM': [-3.1190, -60.1770],   # Amazonas
    'AP': [0.9020, -52.0173],    # Amapá
    'AL': [-9.5714, -36.7820],   # Alagoas
    'RO': [-10.1905, -64.9039],  # Rondônia
    'PB': [-7.1151, -34.8610],   # Paraíba
    'TO': [-10.1851, -48.3337],  # Tocantins
    'PI': [-5.0891, -42.8014],   # Piauí
    'AC': [-8.7737, -70.5510],   # Acre
    'SE': [-10.9472, -37.0731],  # Sergipe
    'RR': [2.8311, -60.6743]     # Roraima
}

# Hitung jumlah pengiriman per customer_state
delivery_by_state = filtered_orders.groupby('customer_state').agg(
    total_orders=('order_id', 'count'),
    on_time_orders=('on_time', 'sum'),
    late_orders=('on_time', lambda x: (x == False).sum())
).reset_index()

# Koordinat geografis untuk setiap state
# Pastikan `state_coordinates` sudah terdefinisi seperti sebelumnya
delivery_by_state['lat'], delivery_by_state['lon'] = zip(*delivery_by_state['customer_state'].map(lambda x: state_coordinates.get(x, [None, None])))

# Dropdown pilihan metrik
metric = st.radio("Pilih Metode Evaluasi Pengiriman:", ("Pengiriman Tepat Waktu", "Pengiriman Terlambat"))

if metric == "Pengiriman Tepat Waktu":
    color_column = 'on_time_orders'
    legend_title = "Jumlah Tepat Waktu"
else:
    color_column = 'late_orders'
    legend_title = "Jumlah Terlambat"

# Plot peta
fig = px.scatter_geo(
    delivery_by_state,
    lat='lat',
    lon='lon',
    color=color_column,
    hover_name='customer_state',
    size='total_orders',
    color_continuous_scale='Plasma',
    projection='natural earth',
    title="Heatmap Status Pengiriman per Region",
    labels={color_column: legend_title},
    template='plotly_white'
)

# Fokus otomatis ke wilayah Brasil berdasarkan data yang tersedia
fig.update_geos(
    showcountries=True,
    countrycolor="gray",
    showcoastlines=True,
    coastlinecolor="lightgray",
    showland=True,
    landcolor="whitesmoke",
    showocean=True,
    oceancolor="azure",
    fitbounds="locations",  # << auto-zoom ke titik data
    lataxis_range=[-35, 5],  # << mempertegas fokus lat
    lonaxis_range=[-75, -30] # << mempertegas fokus lon
)

# Tampilkan peta
st.plotly_chart(fig, use_container_width=True)

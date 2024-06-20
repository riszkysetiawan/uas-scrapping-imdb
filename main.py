import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Load the dataset
file_path = 'Data/merge_data_film.csv'  # Ganti dengan path file Anda
data = pd.read_csv(file_path)

# Sidebar untuk filter
st.sidebar.title("Filter")

# Filter berdasarkan judul film
film_options = list(data['Title'].unique())
selected_titles = st.sidebar.multiselect("Pilih Judul Film", film_options)

# Filter berdasarkan durasi film
min_duration, max_duration = st.sidebar.slider(
    "Pilih Durasi Film (menit)", int(data['Runtime'].min()), int(data['Runtime'].max()), 
    (int(data['Runtime'].min()), int(data['Runtime'].max()))
)

# Filter berdasarkan anggaran film
min_budget, max_budget = st.sidebar.slider(
    "Pilih Anggaran Film (USD)", int(data['Budget'].min()), int(data['Budget'].max()), 
    (int(data['Budget'].min()), int(data['Budget'].max()))
)

# Terapkan filter
if len(selected_titles) == 0:
    filtered_data = data[(data['Runtime'] >= min_duration) &
                         (data['Budget'] >= min_budget) & (data['Budget'] <= max_budget)]
else:
    filtered_data = data[(data['Title'].isin(selected_titles)) &
                         (data['Runtime'] >= min_duration) &
                         (data['Budget'] >= min_budget) & (data['Budget'] <= max_budget)]

# Judul aplikasi
st.title("Scrapping Film IMDB")

# Bubble Plot: Relationship antara Anggaran, Pendapatan Global, dan Durasi Film
st.header("Relationship antara Anggaran, Pendapatan Global, dan Durasi Film")
st.write("""
Grafik ini menunjukkan hubungan antara anggaran (Budget), pendapatan global (Gross worldwide), dan durasi film (Runtime). 
Sumbu X mewakili anggaran film, sumbu Y mewakili pendapatan global, dan ukuran bubble menunjukkan durasi film. 
Grafik ini membantu untuk melihat korelasi antara anggaran dan pendapatan film serta bagaimana durasi film mempengaruhi keduanya.
""")
fig_bubble = px.scatter(filtered_data, x='Budget', y='Gross worldwide', size='Runtime',
                        hover_name='Title', title='Relationship antara Anggaran, Pendapatan Global, dan Durasi Film')
st.plotly_chart(fig_bubble)

# Column Chart: Comparison Pendapatan AS & Kanada dengan Pendapatan Global
st.header("Comparison Pendapatan AS & Kanada dengan Pendapatan Global")
st.write("""
Grafik ini membandingkan pendapatan film di AS & Kanada dengan pendapatan global. 
Setiap film diwakili oleh dua bar, satu untuk pendapatan di AS & Kanada dan satu lagi untuk pendapatan global. 
Grafik ini menunjukkan perbedaan antara pendapatan yang dihasilkan dari AS & Kanada dan pendapatan global, 
serta performa film di pasar domestik dibandingkan dengan pasar internasional.
""")
fig_column = go.Figure(data=[
    go.Bar(name='Pendapatan AS & Kanada', x=filtered_data['Title'], y=filtered_data['Gross US & Canada']),
    go.Bar(name='Pendapatan Global', x=filtered_data['Title'], y=filtered_data['Gross worldwide'])
])
fig_column.update_layout(barmode='group', title='Comparison Pendapatan AS & Kanada dengan Pendapatan Global')
st.plotly_chart(fig_column)

# Line Histogram: Distribusi Anggaran Film
st.header("Distribusi Anggaran Film")
st.write("""
Histogram ini menunjukkan distribusi anggaran film. 
Sumbu X mewakili anggaran film dan jumlah bins menunjukkan frekuensi atau jumlah film berdasarkan anggarannya. 
Histogram ini membantu untuk memahami sebaran anggaran dalam dataset, 
seperti apakah lebih banyak film dengan anggaran kecil atau besar.
""")
fig_histogram = px.histogram(filtered_data, x='Budget', title='Distribusi Anggaran Film', nbins=20)
st.plotly_chart(fig_histogram)

# Stacked Area Chart: Komposisi Pendapatan Film sepanjang Waktu
st.header("Komposisi Pendapatan Film sepanjang Waktu")
st.write("""
Grafik ini menunjukkan komposisi pendapatan film dari AS & Kanada dan pendapatan global sepanjang waktu. 
Sumbu X mewakili nama film dan sumbu Y mewakili pendapatan. 
Area grafik menunjukkan kontribusi pendapatan dari AS & Kanada terhadap total pendapatan global sepanjang waktu. 
Ini membantu untuk melihat bagaimana pendapatan dari kedua sumber ini berubah dan berkontribusi terhadap total pendapatan film.
""")
fig_area = go.Figure()
fig_area.add_trace(go.Scatter(x=filtered_data['Title'], y=filtered_data['Gross US & Canada'], fill='tonexty', name='Pendapatan AS & Kanada'))
fig_area.add_trace(go.Scatter(x=filtered_data['Title'], y=filtered_data['Gross worldwide'], fill='tonexty', name='Pendapatan Global'))
fig_area.update_layout(title='Komposisi Pendapatan Film sepanjang Waktu', xaxis_title='Film', yaxis_title='Pendapatan')
st.plotly_chart(fig_area)

# Tambahkan footer
footer = """
    <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #333333;
            color: white;
            text-align: center;
            padding: 10px;
        }
    </style>
    <div class="footer">
        <p>Moch Rezeki Setiawan - ©2024 Sistem Informasi UPN Jatim</p>
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)

import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Load dataset
data = pd.read_excel('data_smartphones.xlsx')

# Fitur yang digunakan
fitur = ['Price', 'Ratings', 'RAM (GB)', 'Battery']

# Normalisasi fitur
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data[fitur])

# Cosine similarity
similarity_matrix = cosine_similarity(data_scaled)

# Tampilkan judul dan data
st.subheader("📱 Sistem Rekomendasi Smartphone Berdasarkan Preferensi")
st.write("Berikut ini adalah data smartphone yang tersedia:")
st.dataframe(data)

# Filter
st.subheader("🔍 Pilih Kriteria Smartphone yang Anda Inginkan")

filter_price = st.checkbox("Filter Harga")
filter_rating = st.checkbox("Filter Rating")
filter_ram = st.checkbox("Filter RAM")
filter_battery = st.checkbox("Filter Baterai")

# Input user
if any([filter_price, filter_rating, filter_ram, filter_battery]):
    data_filtered = data.copy()
    
    if filter_price:
        max_price = st.number_input("Masukkan Harga Maksimal (Rp)", min_value=0, value=6000000, step=500000)
        data_filtered = data_filtered[data_filtered['Price'] <= max_price]

    if filter_rating:
        min_rating = st.slider("Pilih Rating Minimal", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
        data_filtered = data_filtered[data_filtered['Ratings'] >= min_rating]

    if filter_ram:
        min_ram = st.selectbox("Pilih RAM Minimal (GB)", sorted(data['RAM (GB)'].unique()))
        data_filtered = data_filtered[data_filtered['RAM (GB)'] >= min_ram]

    if filter_battery:
        min_battery = st.selectbox("Pilih Kapasitas Baterai Minimal (mAh)", sorted(data['Battery'].unique()))
        data_filtered = data_filtered[data_filtered['Battery'] >= min_battery]

    # Menampilkan hasil rekomendasi
    st.subheader("📊 5 Rekomendasi Smartphone Terbaik untuk Anda:")

    if not data_filtered.empty:
        # Ambil index smartphone pertama yang lolos filter untuk jadi acuan
        idx_referensi = data.index[data['Type'] == data_filtered.iloc[0]['Type']].tolist()[0]

        # Ambil skor similarity dari smartphone itu ke semua
        similarity_scores = list(enumerate(similarity_matrix[idx_referensi]))

        # Urutkan berdasarkan similarity tertinggi (selain diri sendiri)
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similarity_scores = [s for s in similarity_scores if s[0] != idx_referensi]

        # Ambil 5 teratas
        top_indices = [s[0] for s in similarity_scores[:5]]
        rekomendasi = data.iloc[top_indices]

        st.dataframe(rekomendasi[['Brand', 'Type', 'Price', 'Ratings', 'RAM (GB)', 'Battery']])
    else:
        st.warning("❌ Tidak ada smartphone yang sesuai dengan kriteria filter Anda.")
else:
    st.info("☝️ Silakan aktifkan setidaknya satu filter terlebih dahulu untuk melihat hasil rekomendasi.")

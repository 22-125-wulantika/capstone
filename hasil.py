import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Load dataset
data = pd.read_excel('data_smartphones.xlsx')

# Fitur yang digunakan
fitur = ['Price', 'Ratings', 'RAM (GB)', 'Battery']

# Normalisasi fitur untuk cosine similarity
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data[fitur])
similarity_matrix = cosine_similarity(data_scaled)

# Tampilkan judul dan dataset
st.subheader("📱 Sistem Rekomendasi Smartphone Berdasarkan Preferensi")
st.write("Berikut ini adalah data smartphone yang tersedia:")
st.dataframe(data)

# Pilihan filter
st.subheader("🔍 Pilih Kriteria Smartphone yang Anda Inginkan")

filter_price = st.checkbox("Filter Harga")
filter_rating = st.checkbox("Filter Rating")
filter_ram = st.checkbox("Filter RAM")
filter_battery = st.checkbox("Filter Baterai")

# Input untuk masing-masing filter
if any([filter_price, filter_rating, filter_ram, filter_battery]):
    data_filtered = data.copy()
    columns_to_display = ['Brand', 'Type']

    if filter_price:
        max_price = st.number_input("Masukkan Harga Maksimal (Rp)", min_value=0, value=6000000, step=500000)
        data_filtered = data_filtered[data_filtered['Price'] <= max_price]
        columns_to_display.append('Price')

    if filter_rating:
        min_rating = st.slider("Pilih Rating Minimal", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
        data_filtered = data_filtered[data_filtered['Ratings'] >= min_rating]
        columns_to_display.append('Ratings')

    if filter_ram:
        min_ram = st.selectbox("Pilih RAM Minimal (GB)", sorted(data['RAM (GB)'].unique()))
        data_filtered = data_filtered[data_filtered['RAM (GB)'] >= min_ram]
        columns_to_display.append('RAM (GB)')

    if filter_battery:
        min_battery = st.selectbox("Pilih Kapasitas Baterai Minimal (mAh)", sorted(data['Battery'].unique()))
        data_filtered = data_filtered[data_filtered['Battery'] >= min_battery]
        columns_to_display.append('Battery')

    # Tampilkan hasil rekomendasi
    st.subheader("📊 Hasil Rekomendasi Smartphone:")
    if not data_filtered.empty:
        st.write(data_filtered[columns_to_display])
    else:
        st.warning("❌ Tidak ada smartphone yang sesuai dengan kriteria filter Anda.")
else:
    st.info("☝️ Silakan aktifkan setidaknya satu filter terlebih dahulu untuk melihat hasil rekomendasi.")

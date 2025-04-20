import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Load dataset
data = pd.read_excel('data_smartphones.xlsx')

# Judul aplikasi
st.title("📱 Sistem Rekomendasi Smartphone")

# Menampilkan data asli
st.subheader("Data Smartphone")
st.write(data)

# Fitur yang akan digunakan untuk similarity
fitur = ['Price', 'Ratings', 'RAM (GB)', 'ROM (GB)', 'Camera', 'Battery']
data_features = data[fitur].copy()

# Normalisasi data agar adil dalam perbandingan
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data_features)

# Hitung cosine similarity
similarity_matrix = cosine_similarity(data_scaled)

# Filter dari user
st.subheader("🎯 Filter Sesuai Kriteria Anda")
min_price = st.number_input("Harga Minimum (Rp)", min_value=0, value=2000000, step=500000)
max_price = st.number_input("Harga Maksimum (Rp)", min_value=0, value=6000000, step=500000)
min_rating = st.slider("Rating Minimal", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
min_ram = st.selectbox("RAM Minimal (GB)", options=sorted(data['RAM (GB)'].unique()))
min_battery = st.selectbox("Baterai Minimal (mAh)", options=sorted(data['Battery'].unique()))

# Filter data sesuai input
filtered_data = data[
    (data['Price'] >= min_price) &
    (data['Price'] <= max_price) &
    (data['Ratings'] >= min_rating) &
    (data['RAM (GB)'] >= min_ram) &
    (data['Battery'] >= min_battery)
]

# Rekomendasi berdasarkan kemiripan smartphone pertama yang lolos filter (jika ada)
st.subheader("📊 Rekomendasi Smartphone Berdasarkan Filter")
if not filtered_data.empty:
    index_utama = filtered_data.index[0]
    similarity_scores = list(enumerate(similarity_matrix[index_utama]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    top_n = st.slider("Jumlah Rekomendasi yang Ditampilkan", 1, 10, 5)

    recommended_indexes = [i[0] for i in similarity_scores[1:top_n+1]]
    recommended_phones = data.loc[recommended_indexes]

    st.write(recommended_phones[['Brand', 'Type', 'Price', 'Ratings', 'RAM (GB)', 'ROM (GB)', 'Camera', 'Battery']])
else:
    st.warning("Tidak ada smartphone yang sesuai filter. Coba ubah filter Anda.")

# Catatan
st.caption("Model menggunakan Cosine Similarity untuk menentukan kemiripan antara spesifikasi smartphone.")

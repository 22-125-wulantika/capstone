import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Load dataset
data = pd.read_excel('data_smartphones.xlsx')

st.title("📱 Sistem Rekomendasi Smartphone")

# Menampilkan data awal
st.subheader("Data Smartphone")
st.dataframe(data)

# Fitur yang digunakan untuk similarity
fitur = ['Price', 'Ratings', 'RAM (GB)', 'ROM (GB)', 'Camera', 'Battery']
data_features = data[fitur].copy()

# Normalisasi fitur
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data_features)

# Hitung cosine similarity
similarity_matrix = cosine_similarity(data_scaled)

# --- Input filter kriteria ---
st.subheader("🎯 Pilih Kriteria Smartphone")

col1, col2 = st.columns(2)
with col1:
    min_price = st.number_input("Harga Minimum (Rp)", min_value=0, value=2000000, step=500000)
    min_ram = st.selectbox("RAM Minimal (GB)", options=sorted(data['RAM (GB)'].unique()))
with col2:
    max_price = st.number_input("Harga Maksimum (Rp)", min_value=0, value=6000000, step=500000)
    min_battery = st.selectbox("Baterai Minimal (mAh)", options=sorted(data['Battery'].unique()))

min_rating = st.slider("Rating Minimal", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
top_n = st.slider("Jumlah Rekomendasi yang Ditampilkan", 1, 10, 5)

# Tombol untuk memproses
if st.button("Tampilkan Rekomendasi"):
    # Filter data sesuai input
    filtered_data = data[
        (data['Price'] >= min_price) &
        (data['Price'] <= max_price) &
        (data['Ratings'] >= min_rating) &
        (data['RAM (GB)'] >= min_ram) &
        (data['Battery'] >= min_battery)
    ]

    st.subheader("📊 Hasil Rekomendasi")

    if not filtered_data.empty:
        index_utama = filtered_data.index[0]
        similarity_scores = list(enumerate(similarity_matrix[index_utama]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        recommended_indexes = [i[0] for i in similarity_scores[1:top_n+1]]
        recommended_phones = data.loc[recommended_indexes]

        st.write(recommended_phones[['Brand', 'Type', 'Price', 'Ratings', 'RAM (GB)', 'ROM (GB)', 'Camera', 'Battery']])
    else:
        st.warning("❌ Tidak ada smartphone yang sesuai dengan kriteria kamu.")
else:
    st.info("Silakan pilih kriteria terlebih dahulu, lalu klik tombol di atas untuk melihat rekomendasi.")

# Catatan
st.caption("📌 Sistem ini menggunakan Cosine Similarity berdasarkan spesifikasi untuk memberikan rekomendasi.")

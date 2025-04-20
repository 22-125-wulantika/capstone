import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
data = pd.read_excel("data_smartphones.xlsx")  # Ganti dengan path file jika perlu

# Label Encoding untuk fitur kategorikal
le_brand = LabelEncoder()
le_type = LabelEncoder()

data['Brand'] = le_brand.fit_transform(data['Brand'])
data['Type'] = le_type.fit_transform(data['Type'])

# Pilih fitur yang relevan untuk rekomendasi
features = data[['Brand', 'Type', 'Price', 'Ratings', 'RAM (GB)', 'Battery']]

# Hitung cosine similarity
similarity_matrix = cosine_similarity(features)

# Judul aplikasi
st.title("Sistem Rekomendasi Smartphone")
st.subheader("Pilih Kriteria Terlebih Dahulu")

# Form untuk filter
with st.form("filter_form"):
    selected_brand = st.selectbox("Pilih Brand", options=sorted(data['Brand'].unique()))
    max_price = st.number_input("Masukkan Harga Maksimal", min_value=0, value=5000000, step=500000)
    min_rating = st.slider("Pilih Rating Minimal", 0.0, 5.0, 4.0, 0.1)
    submit = st.form_submit_button("Cari Rekomendasi")

if submit:
    # Filter data berdasarkan input
    filtered_data = data[
        (data['Brand'] == selected_brand) &
        (data['Price'] <= max_price) &
        (data['Ratings'] >= min_rating)
    ]

    if filtered_data.empty:
        st.warning("Tidak ada smartphone yang sesuai dengan kriteria.")
    else:
        # Ambil index smartphone pertama dari hasil filter sebagai referensi
        idx = filtered_data.index[0]
        similar_scores = list(enumerate(similarity_matrix[idx]))
        similar_scores = sorted(similar_scores, key=lambda x: x[1], reverse=True)

        # Ambil 5 rekomendasi teratas (lewati diri sendiri)
        top_indices = [i for i, score in similar_scores if i != idx][:5]
        rekomendasi = data.loc[top_indices, ['Brand', 'Type', 'Price', 'Ratings', 'RAM (GB)', 'Battery']].copy()

        # Ubah Brand dan Type ke label aslinya
        rekomendasi['Brand'] = le_brand.inverse_transform(rekomendasi['Brand'])
        rekomendasi['Type'] = le_type.inverse_transform(rekomendasi['Type'])

        # Tambahkan kolom nomor urut
        rekomendasi.reset_index(drop=True, inplace=True)
        rekomendasi.insert(0, 'No', range(1, len(rekomendasi) + 1))

        # Tampilkan hasil rekomendasi
        st.subheader("Top 5 Rekomendasi Smartphone")
        st.dataframe(rekomendasi)

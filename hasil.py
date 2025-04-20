import streamlit as st
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
data = pd.read_excel('data_smartphones.xlsx')  # Pastikan nama file sesuai

# Label Encoding untuk kolom kategorikal
label_encoder_brand = LabelEncoder()
label_encoder_type = LabelEncoder()

data['Brand'] = label_encoder_brand.fit_transform(data['Brand'].astype(str))
data['Type'] = label_encoder_type.fit_transform(data['Type'].astype(str))

# Pastikan kolom numeric di-cast dengan benar
numeric_columns = ['Price', 'Ratings', 'RAM (GB)', 'Battery']
for col in numeric_columns:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# Drop baris dengan nilai kosong
data.dropna(inplace=True)

# Data untuk similarity
features = data[['Price', 'Ratings', 'RAM (GB)', 'Battery']]
similarity_matrix = cosine_similarity(features)

# Tampilkan judul dan dataset awal
st.title("📱 Sistem Rekomendasi Smartphone")
st.write("Berikut adalah data smartphone yang tersedia:")
st.dataframe(data[['Brand', 'Type', 'Price', 'Ratings', 'RAM (GB)', 'Battery']].head(10))

# Filter pilihan
st.subheader("🎯 Pilih Kriteria Smartphone yang Diinginkan")

filter_brand = st.checkbox("Filter berdasarkan Brand")
filter_price = st.checkbox("Filter berdasarkan Harga Maksimal")
filter_rating = st.checkbox("Filter berdasarkan Rating Minimal")
filter_ram = st.checkbox("Filter berdasarkan RAM Minimal")
filter_battery = st.checkbox("Filter berdasarkan Kapasitas Baterai Minimal")

data_filtered = data.copy()

if filter_brand:
    selected_brand = st.selectbox("Pilih Brand", options=data['Brand'].unique())
    data_filtered = data_filtered[data_filtered['Brand'] == selected_brand]

if filter_price:
    max_price = st.number_input("Masukkan Harga Maksimal", min_value=0, value=3000000, step=50000)
    data_filtered = data_filtered[data_filtered['Price'] <= max_price]

if filter_rating:
    min_rating = st.slider("Pilih Rating Minimal", min_value=0.0, max_value=5.0, value=3.0, step=0.1)
    data_filtered = data_filtered[data_filtered['Ratings'] >= min_rating]

if filter_ram:
    min_ram = st.slider("Pilih RAM Minimal (GB)", min_value=1, max_value=32, value=4, step=1)
    data_filtered = data_filtered[data_filtered['RAM (GB)'] >= min_ram]

if filter_battery:
    min_battery = st.slider("Pilih Baterai Minimal (mAh)", min_value=1000, max_value=10000, value=4000, step=100)
    data_filtered = data_filtered[data_filtered['Battery'] >= min_battery]

# Tampilkan hasil filter dan rekomendasi
st.subheader("🔍 Rekomendasi Smartphone")

if not data_filtered.empty:
    # Ambil smartphone referensi (yang pertama lolos filter)
    idx_referensi = data.index[data['Type'] == data_filtered.iloc[0]['Type']].tolist()[0]

    # Hitung similarity
    similarity_scores = list(enumerate(similarity_matrix[idx_referensi]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = [s for s in similarity_scores if s[0] != idx_referensi]

    # Ambil 5 teratas
    top_indices = [s[0] for s in similarity_scores[:5]]
    rekomendasi = data.iloc[top_indices]

    # Penomoran 1-5
    rekomendasi = rekomendasi.reset_index(drop=True)
    rekomendasi.index = rekomendasi.index + 1
    rekomendasi.index.name = "No"

    st.dataframe(rekomendasi[['Brand', 'Type', 'Price', 'Ratings', 'RAM (GB)', 'Battery']])
else:
    st.warning("Data tidak ditemukan berdasarkan filter yang dipilih.")

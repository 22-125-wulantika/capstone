import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
df = pd.read_excel("data_smartphones.xlsx")

# Preprocessing kolom Camera
if "Camera" in df.columns:
    df["Camera"] = df["Camera"].astype(str).str.replace("MP", "", regex=False).astype(float)

# Judul aplikasi
st.title("📱 Sistem Rekomendasi Smartphone")
st.subheader("📑 Dataset Smartphone")
st.dataframe(df)

# Pilihan kriteria
st.subheader("🔍 Spesifikasi Smartphone")

# Checkbox untuk memilih kriteria
use_price = st.checkbox("Gunakan Harga (Price)")
use_ratings = st.checkbox("Gunakan Rating")
use_ram = st.checkbox("Gunakan RAM")
use_rom = st.checkbox("Gunakan ROM")
use_camera = st.checkbox("Gunakan Kamera")
use_battery = st.checkbox("Gunakan Baterai")

# Mapping nama kriteria dan checkbox
criteria_map = {
    "Price": use_price,
    "Ratings": use_ratings,
    "RAM (GB)": use_ram,
    "ROM (GB)": use_rom,
    "Camera": use_camera,
    "Battery": use_battery
}

# Kriteria yang dipilih
selected_criteria = [key for key, value in criteria_map.items() if value]

if not selected_criteria:
    st.warning("❗ Silakan pilih minimal satu spesifikasi!")
else:
    st.subheader("📌 Pilih Smartphone Referensi")

    # Tampilkan daftar pilihan smartphone sebagai referensi
    df["Label"] = df["Brand"] + " " + df["Type"]
    referensi_label = st.selectbox("Pilih salah satu smartphone sebagai referensi:", df["Label"])
    idx_referensi = df[df["Label"] == referensi_label].index[0]

    # Jumlah hasil rekomendasi
    st.subheader("📊 Jumlah Rekomendasi")
    jumlah_rekomendasi = st.number_input("Masukkan jumlah hasil rekomendasi:", min_value=1, max_value=20, value=5)

    if st.button("💡 Tampilkan Rekomendasi dengan Similarity"):
        df_selected = df[selected_criteria].copy()

        # Pastikan semua data numerik dan hilangkan NaN
        for col in selected_criteria:
            df_selected[col] = pd.to_numeric(df_selected[col], errors='coerce')
            df_selected[col].fillna(df_selected[col].median(), inplace=True)

        # Normalisasi data
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(df_selected)

        # Hitung similarity matrix (cosine similarity)
        similarity_matrix = cosine_similarity(scaled_data)

        # Hitung similarity antara referensi dengan seluruh data
        similarity_scores = list(enumerate(similarity_matrix[idx_referensi]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

        # Buang referensi sendiri dari hasil
        similarity_scores = [s for s in similarity_scores if s[0] != idx_referensi]
        top_indices = [s[0] for s in similarity_scores[:jumlah_rekomendasi]]
        top_similarities = [s[1] for s in similarity_scores[:jumlah_rekomendasi]]

        # Tampilkan hasil
        result = df.loc[top_indices].copy()
        result["Similarity Score"] = top_similarities

        st.subheader("📋 Hasil Rekomendasi Berdasarkan Kemiripan:")
        display_cols = ["Brand", "Type", "Colour", "Price", "Ratings", "RAM (GB)", "ROM (GB)", "Camera", "Battery", "Similarity Score"]
        st.dataframe(result[display_cols].reset_index(drop=True), use_container_width=True)

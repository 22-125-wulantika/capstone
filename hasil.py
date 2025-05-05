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
use_price = st.checkbox("Harga")
use_ratings = st.checkbox("Rating")
use_ram = st.checkbox("RAM")
use_rom = st.checkbox("ROM")
use_camera = st.checkbox("Kamera")
use_battery = st.checkbox("Baterai")

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
    # Input preferensi pengguna
    st.subheader("📊 Masukkan Preferensi Anda")
    user_input = {}

    for crit in selected_criteria:
        if crit == "Price":
            user_input[crit] = st.number_input("Masukkan Harga Maksimum (Rp)", min_value=0)
        elif crit == "Ratings":
            user_input[crit] = st.slider("Pilih Rating Minimum", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
        elif crit in ["RAM (GB)", "ROM (GB)", "Camera", "Battery"]:
            options = sorted(df[crit].dropna().unique())
            user_input[crit] = st.selectbox(f"Pilih {crit}", options)

    # Jumlah hasil rekomendasi
    st.subheader("📊 Jumlah Rekomendasi")
    top_n = st.number_input("Masukkan jumlah hasil rekomendasi:", min_value=1, max_value=20, value=5)

    if st.button("💡 Tampilkan Rekomendasi"):
        df_selected = df[selected_criteria].copy()

        # Ubah ke tipe numerik dan isi nilai kosong
        for col in selected_criteria:
            df_selected[col] = pd.to_numeric(df_selected[col], errors='coerce')
            df_selected[col].fillna(df_selected[col].median(), inplace=True)

        # Tambahkan input pengguna sebagai baris terakhir (referensi)
        user_df = pd.DataFrame([user_input])
        combined_df = pd.concat([df_selected, user_df], ignore_index=True)

        # Normalisasi seluruh data (termasuk input user)
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(combined_df)

        # Hitung cosine similarity
        similarity_matrix = cosine_similarity(scaled_data)

        # Index referensi adalah baris terakhir
        idx_referensi = len(scaled_data) - 1
        similarity_scores = list(enumerate(similarity_matrix[idx_referensi]))

        # Urutkan dan buang diri sendiri
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similarity_scores = [s for s in similarity_scores if s[0] != idx_referensi]

        # Ambil top-N rekomendasi
        top_indices = [s[0] for s in similarity_scores[:top_n]]
        top_similarities = [s[1] for s in similarity_scores[:top_n]]

        # Tampilkan hasil
        result = df.iloc[top_indices].copy()
        result["Similarity Score"] = top_similarities

        st.subheader("📋 Rekomendasi Smartphone:")
        display_cols = ["Brand", "Type", "Colour", "Price", "Ratings", "RAM (GB)", "ROM (GB)", "Camera", "Battery", "Similarity Score"]
       # Reset index dan tambahkan kolom No
        result.reset_index(drop=True, inplace=True)
        result.index = result.index + 1
        result.insert(0, "No", result.index)
        
        # Tampilkan hasil
        display_cols = ["No", "Brand", "Type", "Colour", "Price", "Ratings", "RAM (GB)", "ROM (GB)", "Camera", "Battery", "Similarity Score"]
        st.dataframe(result[display_cols].to_dict(orient="records"), use_container_width=True)

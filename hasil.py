import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from numpy.linalg import norm

# Load dataset
df = pd.read_excel("data_smartphones.xlsx")

# Preprocessing kolom Camera
if "Camera" in df.columns:
    df["Camera"] = df["Camera"].astype(str).str.replace("MP", "", regex=False).astype(float)

# Judul aplikasi
st.title("📱 Sistem Rekomendasi Smartphone")
st.subheader("📑 Dataset Smartphone")
st.dataframe(df, use_container_width=True)

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
    # Input preferensi pengguna
    st.subheader("🎯 Masukkan Preferensi Anda")
    user_input = {}

    for crit in selected_criteria:
        if crit == "Price":
            user_input[crit] = st.number_input("Masukkan Harga Maksimal (Rp)", min_value=0)
        elif crit == "Ratings":
            user_input[crit] = st.slider("Pilih Rating Minimal", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
        elif crit in ["RAM (GB)", "ROM (GB)", "Camera", "Battery"]:
            options = sorted(df[crit].dropna().unique())
            user_input[crit] = st.selectbox(f"Pilih {crit}", options)

    # Jumlah hasil rekomendasi
    st.subheader("📊 Jumlah Rekomendasi")
    top_n = st.number_input("Masukkan jumlah hasil rekomendasi:", min_value=1, max_value=20, value=5)

    # Tombol rekomendasi
    if st.button("💡 Rekomendasikan"):
        # Filter dan normalisasi data
        df_selected = df[selected_criteria].copy()

        for col in selected_criteria:
            df_selected[col] = pd.to_numeric(df_selected[col], errors='coerce')
            df_selected[col].fillna(df_selected[col].median(), inplace=True)

        scaler = MinMaxScaler()
        df_scaled = scaler.fit_transform(df_selected)

        user_input_df = pd.DataFrame([user_input])
        user_scaled = scaler.transform(user_input_df)[0]

        distances = [norm(row - user_scaled) for row in df_scaled]
        df["Skor Kemiripan"] = distances

        # Ambil top N hasil rekomendasi
        result = df.sort_values(by="Skor Kemiripan").head(top_n)

        st.subheader("📋 Hasil Rekomendasi Smartphone:")
        st.dataframe(result[["Nama", *selected_criteria, "Skor Kemiripan"]].reset_index(drop=True), use_container_width=True)

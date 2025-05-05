import streamlit as st
import pandas as pd

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
    if st.button("💡 Tampilkan Rekomendasi"):
        filtered_df = df.copy()

        for crit in selected_criteria:
            if crit == "Price":
                filtered_df = filtered_df[filtered_df[crit] <= user_input[crit]]
            elif crit == "Ratings":
                filtered_df = filtered_df[filtered_df[crit] >= user_input[crit]]
            else:
                filtered_df = filtered_df[filtered_df[crit] == user_input[crit]]

        result = filtered_df.head(top_n)

        if result.empty:
            st.warning("⚠️ Tidak ditemukan smartphone yang sesuai dengan preferensi Anda.")
        else:
            st.subheader("📋 Hasil Rekomendasi Smartphone:")
            display_cols = ["Brand", "Type", "Colour", "Price", "Ratings", "RAM (GB)", "ROM (GB)", "Camera", "Battery"]
            st.dataframe(result[display_cols].reset_index(drop=True), use_container_width=True)

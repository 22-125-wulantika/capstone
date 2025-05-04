import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from numpy.linalg import norm

# Load data
df = pd.read_excel("data_smartphones.xlsx")

# Preprocessing Camera
if "Camera" in df.columns:
    df["Camera"] = df["Camera"].astype(str).str.replace("MP", "", regex=False).astype(float)

# Judul aplikasi
st.title("📱 Sistem Rekomendasi Smartphone")

st.subheader("🔍 Pilih Kriteria Smartphone")

# Checkbox untuk setiap kriteria
use_price = st.checkbox("Gunakan Harga (Price)")
use_ratings = st.checkbox("Gunakan Rating (Ratings)")
use_ram = st.checkbox("Gunakan RAM (GB)")
use_rom = st.checkbox("Gunakan ROM (GB)")
use_camera = st.checkbox("Gunakan Kamera (Camera)")
use_battery = st.checkbox("Gunakan Baterai (Battery)")

# Mapping checkbox ke nama kolom
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
    st.warning("❗ Silakan pilih minimal satu kriteria!")
else:
    # Input jumlah hasil rekomendasi
    top_n = st.number_input("📊 Masukkan jumlah hasil rekomendasi:", min_value=1, max_value=20, value=5)

    # Input nilai preferensi user dengan nilai default dari dataset
    st.subheader("🎯 Masukkan Nilai Preferensi Anda")
    user_input = {}
    for crit in selected_criteria:
        # Tangani nilai kosong
        df[crit] = pd.to_numeric(df[crit], errors='coerce')
        df[crit].fillna(df[crit].median(), inplace=True)

        min_val = float(df[crit].min())
        max_val = float(df[crit].max())
        mean_val = float(df[crit].mean())

        # Tampilkan input dengan batas sesuai data
        val = st.number_input(
            f"{crit}:", min_value=min_val, max_value=max_val, value=mean_val, step=1.0, format="%.2f"
        )
        user_input[crit] = val

    if st.button("💡 Rekomendasikan"):
        # Normalisasi data
        df_selected = df[selected_criteria].copy()
        scaler = MinMaxScaler()
        df_scaled = scaler.fit_transform(df_selected)

        # Normalisasi input user
        user_input_df = pd.DataFrame([user_input])
        user_scaled = scaler.transform(user_input_df)[0]

        # Hitung jarak Euclidean
        distances = [norm(row - user_scaled) for row in df_scaled]
        df["Similarity Score"] = distances

        # Ambil top N hasil
        result = df.sort_values(by="Similarity Score").head(top_n)

        st.subheader("📋 Hasil Rekomendasi Smartphone:")
        st.dataframe(result.drop(columns=["Similarity Score"]))

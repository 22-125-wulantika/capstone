import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from numpy.linalg import norm

# Memuat data
df = pd.read_excel("data_smartphones.xlsx")

# Pra-pemrosesan kolom Kamera
if "Camera" in df.columns:
    df["Camera"] = df["Camera"].astype(str).str.replace("MP", "", regex=False).astype(float)

# Judul aplikasi
st.title("📱 Sistem Rekomendasi Smartphone")

# Menampilkan dataset (opsional)
if st.checkbox("Tampilkan Dataset Smartphone"):
    st.subheader("📑 Data Smartphone Tersedia")
    st.dataframe(df)

# Filter kriteria
st.subheader("🔍 Silakan Pilih Kriteria yang Diinginkan")

# Checkbox untuk memilih kriteria
filter_price = st.checkbox("Harga")
filter_rating = st.checkbox("Rating")
filter_ram = st.checkbox("RAM")
filter_rom = st.checkbox("ROM")
filter_camera = st.checkbox("Kamera")
filter_battery = st.checkbox("Baterai")

# Menyimpan input pengguna
user_input = {}
selected_criteria = []

if filter_price:
    val = st.number_input("Masukkan batas harga (dalam satuan yang tersedia):", min_value=0)
    user_input["Price"] = val
    selected_criteria.append("Price")

if filter_rating:
    val = st.slider("Pilih nilai rating minimal:", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
    user_input["Ratings"] = val
    selected_criteria.append("Ratings")

if filter_ram:
    val = st.selectbox("Pilih kapasitas RAM (GB):", options=sorted(df["RAM (GB)"].unique()))
    user_input["RAM (GB)"] = val
    selected_criteria.append("RAM (GB)")

if filter_rom:
    val = st.selectbox("Pilih kapasitas ROM (GB):", options=sorted(df["ROM (GB)"].unique()))
    user_input["ROM (GB)"] = val
    selected_criteria.append("ROM (GB)")

if filter_camera:
    val = st.selectbox("Pilih resolusi kamera (MP):", options=sorted(df["Camera"].unique()))
    user_input["Camera"] = val
    selected_criteria.append("Camera")

if filter_battery:
    val = st.selectbox("Pilih kapasitas baterai (mAh):", options=sorted(df["Battery"].unique()))
    user_input["Battery"] = val
    selected_criteria.append("Battery")

# Validasi jumlah kriteria
if not selected_criteria:
    st.warning("⚠️ Silakan pilih minimal satu kriteria pencarian.")
else:
    top_n = st.number_input("Masukkan jumlah hasil rekomendasi yang diinginkan:", min_value=1, max_value=20, value=5)

    if st.button("Tampilkan Rekomendasi"):
        # Ambil kolom sesuai kriteria yang dipilih
        df_selected = df[selected_criteria].copy()

        # Ubah ke numerik dan isi nilai kosong jika ada
        for col in selected_criteria:
            df_selected[col] = pd.to_numeric(df_selected[col], errors="coerce")
            df_selected[col].fillna(df_selected[col].median(), inplace=True)

        # Normalisasi
        scaler = MinMaxScaler()
        df_scaled = scaler.fit_transform(df_selected)

        # Ubah input pengguna ke bentuk DataFrame dan normalisasi
        user_input_df = pd.DataFrame([user_input])
        user_scaled = scaler.transform(user_input_df)[0]

        # Hitung jarak Euclidean
        distances = [norm(row - user_scaled) for row in df_scaled]
        df["Skor Kemiripan"] = distances

        # Tampilkan rekomendasi
        hasil = df.sort_values(by="Skor Kemiripan").head(top_n)

        st.subheader("📲 Daftar Smartphone Rekomendasi:")
        st.dataframe(hasil.drop(columns=["Skor Kemiripan"]))

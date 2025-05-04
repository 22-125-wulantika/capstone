import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from numpy.linalg import norm

# Load dataset
df = pd.read_excel("data_smartphones.xlsx")

# Preprocessing kamera
if "kamera" in df.columns:
    df["kamera"] = df["kamera"].astype(str).str.replace("MP", "", regex=False).astype(float)

# Judul Aplikasi
st.title("📱 Sistem Rekomendasi Smartphone")

st.subheader("🔍 Pilih Kriteria Smartphone yang Anda Inginkan")

# Checkbox pilihan
filter_price = st.checkbox("Filter Harga")
filter_rating = st.checkbox("Filter Rating")
filter_ram = st.checkbox("Filter RAM")
filter_rom = st.checkbox("Filter ROM")
filter_camera = st.checkbox("Filter Kamera")
filter_battery = st.checkbox("Filter Baterai")

# Mapping checkbox ke kolom
criteria_map = {
    "harga": filter_price,
    "rating": filter_rating,
    "ram": filter_ram,
    "rom": filter_rom,
    "kamera": filter_camera,
    "baterai": filter_battery
}

# Ambil kolom yang dipilih user
selected_columns = [col for col, checked in criteria_map.items() if checked]

# Validasi
if not selected_columns:
    st.warning("Silakan centang minimal satu kriteria untuk memulai rekomendasi.")
else:
    # Input nilai masing-masing kriteria
    st.subheader("🎯 Masukkan Nilai yang Anda Inginkan")
    user_input = {}
    for col in selected_columns:
        label = col.capitalize()
        user_input[col] = st.number_input(f"Masukkan nilai untuk {label}:")

    # Input jumlah hasil rekomendasi
    top_n = st.number_input("📊 Jumlah hasil rekomendasi yang diinginkan:", min_value=1, max_value=20, value=5)

    if st.button("💡 Rekomendasikan Sekarang"):
        # Cek apakah kolom tersedia di dataset
        missing_cols = [col for col in selected_columns if col not in df.columns]

        if missing_cols:
            st.warning("Beberapa kriteria tidak ditemukan di dataset. Menggunakan yang paling mendekati.")
            selected_columns = [col for col in selected_columns if col in df.columns]
            user_input = {k: v for k, v in user_input.items() if k in selected_columns}

        if selected_columns:
            # Siapkan dataframe untuk proses
            df_selected = df[selected_columns].copy()
            for col in selected_columns:
                df_selected[col] = pd.to_numeric(df_selected[col], errors="coerce")
                df_selected[col].fillna(df_selected[col].median(), inplace=True)

            # Normalisasi
            scaler = MinMaxScaler()
            df_scaled = scaler.fit_transform(df_selected)

            # Normalisasi input user
            user_df = pd.DataFrame([user_input])
            user_scaled = scaler.transform(user_df)[0]

            # Hitung jarak Euclidean
            distances = [norm(row - user_scaled) for row in df_scaled]
            df["Similarity Score"] = distances

            # Ambil rekomendasi terdekat
            result = df.sort_values(by="Similarity Score").head(top_n)

            st.subheader("📋 Hasil Rekomendasi Smartphone:")
            st.dataframe(result.drop(columns=["Similarity Score"]))
        else:
            st.error("Tidak ada kriteria yang cocok tersedia di dataset.")

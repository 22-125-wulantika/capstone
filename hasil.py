import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from numpy.linalg import norm

# Load dataset
df = pd.read_excel("data_smartphones.xlsx")

# Preprocessing kolom kamera jika perlu
if "kamera" in df.columns:
    df["kamera"] = df["kamera"].astype(str).str.replace("MP", "", regex=False).astype(float)

# Mapping pilihan untuk user (Bahasa Indonesia → nama kolom)
available_criteria = {
    'Harga': 'harga',
    'Rating': 'rating',
    'RAM': 'ram',
    'ROM': 'rom',
    'Kamera': 'kamera',
    'Baterai': 'baterai'
}

# Judul Aplikasi
st.title("Sistem Rekomendasi Smartphone")

# Pilihan kriteria
st.subheader("Pilih Kriteria Pencarian")
selected_labels = st.multiselect("Pilih kriteria yang diinginkan:", list(available_criteria.keys()))

# Validasi input
if not selected_labels:
    st.warning("Silakan pilih minimal satu kriteria!")
else:
    selected_columns = [available_criteria[label] for label in selected_labels]

    # Input jumlah rekomendasi
    top_n = st.number_input("Masukkan jumlah hasil rekomendasi:", min_value=1, max_value=20, value=5)

    # Input nilai preferensi user
    user_input = {}
    for label in selected_labels:
        val = st.number_input(f"Masukkan nilai untuk {label}:")
        user_input[available_criteria[label]] = val

    if st.button("Rekomendasikan"):
        # Cek apakah kolom tersedia di dataset
        missing_cols = [col for col in selected_columns if col not in df.columns]

        if missing_cols:
            st.warning("Beberapa kriteria tidak ditemukan di dataset. Menggunakan kriteria terdekat yang tersedia.")
            # Ambil kolom yang tersedia saja
            selected_columns = [col for col in selected_columns if col in df.columns]
            user_input = {k: v for k, v in user_input.items() if k in selected_columns}

        # Lanjut jika masih ada kolom yang bisa digunakan
        if selected_columns:
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

            # Hitung Euclidean distance
            distances = [norm(row - user_scaled) for row in df_scaled]

            df["Similarity Score"] = distances
            result = df.sort_values(by="Similarity Score").head(top_n)

            st.subheader("Hasil Rekomendasi:")
            st.dataframe(result.drop(columns=["Similarity Score"]))
        else:
            st.error("Tidak ada kriteria yang cocok dengan dataset.")

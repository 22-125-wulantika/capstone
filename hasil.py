import streamlit as st
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from numpy.linalg import norm

# Load data
df = pd.read_excel("data_smartphones.xlsx")

# Preprocessing Camera
df["Camera"] = df["Camera"].str.replace("MP", "", regex=False).astype(float)

# Judul aplikasi
st.title("Sistem Rekomendasi Smartphone")

# Pilihan kriteria
criteria_options = ["Price", "Ratings", "RAM (GB)", "ROM (GB)", "Camera", "Battery"]
selected_criteria = st.multiselect("Pilih kriteria pencarian:", criteria_options)

if not selected_criteria:
    st.warning("Silakan pilih minimal satu kriteria!")
else:
    # Input jumlah hasil rekomendasi
    top_n = st.number_input("Masukkan jumlah hasil rekomendasi:", min_value=1, max_value=20, value=5)

    # Input nilai untuk setiap kriteria yang dipilih
    user_input = {}
    for crit in selected_criteria:
        val = st.number_input(f"Masukkan nilai untuk {crit}:")
        user_input[crit] = val

    if st.button("Rekomendasikan"):
        # Normalisasi hanya kolom yang dipilih user
        df_selected = df[selected_criteria].copy()

        # Pastikan kolom numeric
        for col in selected_criteria:
            df_selected[col] = pd.to_numeric(df_selected[col], errors="coerce")
            df_selected[col].fillna(df_selected[col].median(), inplace=True)

        scaler = MinMaxScaler()
        df_selected_scaled = scaler.fit_transform(df_selected)

        # Normalisasi input user berdasarkan kolom terpilih
        user_input_df = pd.DataFrame([user_input])
        user_scaled = scaler.transform(user_input_df)[0]

        # Hitung Euclidean distance
        distances = [norm(row - user_scaled) for row in df_selected_scaled]

        # Ambil top N hasil
        df["Similarity Score"] = distances
        result = df.sort_values(by="Similarity Score").head(top_n)

        st.subheader("Hasil Rekomendasi:")
        st.dataframe(result.drop(columns=["Similarity Score"]))

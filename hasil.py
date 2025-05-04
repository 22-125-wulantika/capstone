import streamlit as st
import pandas as pd

# Load data
df = pd.read_excel("data_smartphones.xlsx")

# Preprocessing Camera: ubah "16MP" → 16
df["Camera"] = df["Camera"].str.replace("MP", "").astype(float)

# Judul aplikasi
st.title("Sistem Rekomendasi Smartphone")

# Pilihan kriteria
criteria_options = ["Price", "Ratings", "RAM (GB)", "ROM (GB)", "Camera", "Battery"]
selected_criteria = st.multiselect("Pilih kriteria pencarian:", criteria_options)

# Validasi input
if not selected_criteria:
    st.warning("Silakan pilih minimal satu kriteria!")
else:
    # Input jumlah hasil rekomendasi
    top_n = st.number_input("Masukkan jumlah hasil rekomendasi:", min_value=1, max_value=20, value=5)

    # Input nilai tiap kriteria
    user_input = {}
    for crit in selected_criteria:
        val = st.number_input(f"Masukkan nilai untuk {crit}:")
        user_input[crit] = val

    if st.button("Rekomendasikan"):
        # Normalisasi data
        from sklearn.preprocessing import MinMaxScaler

        df_norm = df.copy()
        scaler = MinMaxScaler()
        numeric_cols = ["Price", "Ratings", "RAM (GB)", "ROM (GB)", "Camera", "Battery"]
        df_norm[numeric_cols] = scaler.fit_transform(df[numeric_cols])

        # Normalisasi input user
        user_vector = []
        for col in numeric_cols:
            if col in user_input:
                val = user_input[col]
                # Transform dengan scaler
                val_scaled = scaler.transform(pd.DataFrame([{col: val} if col in user_input else {col: 0} for col in numeric_cols]))[0][numeric_cols.index(col)]
            else:
                val_scaled = 0  # default jika tidak dipilih
            user_vector.append(val_scaled)

        # Hitung kemiripan (euclidean distance)
        from numpy.linalg import norm
        distances = df_norm[numeric_cols].apply(lambda row: norm(row.values - user_vector), axis=1)

        # Ambil top N terdekat
        df["Similarity Score"] = distances
        result = df.sort_values(by="Similarity Score").head(top_n)

        st.subheader("Hasil Rekomendasi:")
        st.dataframe(result.drop(columns=["Similarity Score"]))

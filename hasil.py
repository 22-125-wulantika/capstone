import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Load dataset
def load_data():
    df = pd.read_excel('data_smartphones.xlsx')
    return df

df = load_data()

st.title("Sistem Rekomendasi HP - Content Based Filtering")

st.header("Pilih Kriteria yang Diinginkan")

# Daftar kriteria yang bisa dipilih
kriteria_list = ['harga', 'rating', 'ram', 'rom', 'kamera', 'baterai']

# Form input kriteria
selected_kriteria = st.multiselect(
    "Pilih kriteria yang ingin dijadikan dasar rekomendasi:",
    kriteria_list,
    default=None
)

# Pastikan user memilih minimal satu kriteria
if selected_kriteria:
    input_kriteria = {}
    st.subheader("Masukkan Nilai Untuk Setiap Kriteria yang Dipilih")
    for kriteria in selected_kriteria:
        value = st.number_input(f"Masukkan nilai untuk {kriteria.capitalize()}", min_value=0.0)
        input_kriteria[kriteria] = value

    # Pilihan jumlah rekomendasi
    st.subheader("Jumlah Rekomendasi yang Ingin Ditampilkan")
    jumlah_rekomendasi = st.number_input("Masukkan jumlah rekomendasi", min_value=1, max_value=len(df), step=1)

    # Tombol untuk mencari rekomendasi
    if st.button("Cari Rekomendasi"):
        # Preprocessing: hanya kolom yang dipilih
        df_selected = df[selected_kriteria]

        # Scaling data
        scaler = MinMaxScaler()
        df_scaled = scaler.fit_transform(df_selected)

        # Data user
        user_data = pd.DataFrame([input_kriteria])
        user_scaled = scaler.transform(user_data)

        # Hitung similarity
        similarity = cosine_similarity(user_scaled, df_scaled)

        # Ambil indeks rekomendasi terbaik
        rekomendasi_indices = similarity.argsort()[0][::-1][:jumlah_rekomendasi]

        # Tampilkan hasil rekomendasi
        st.subheader("Hasil Rekomendasi HP")
        st.dataframe(df.iloc[rekomendasi_indices])

else:
    st.warning("Silakan pilih minimal satu kriteria terlebih dahulu!")

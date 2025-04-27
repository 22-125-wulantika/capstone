import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Load dataset
def load_data():
    df = pd.read_excel('data_smartphones.xlsx')
    return df

df = load_data()

st.title("📱 Sistem Rekomendasi HP - Content Based Filtering")

# Tampilkan data awal
st.header("📋 Data Smartphone Tersedia")
st.dataframe(df)

st.header("🛠️ Pilih Kriteria yang Diinginkan")

# Daftar semua kriteria
all_kriteria = ['Price', 'Ratings', 'RAM (GB)', 'ROM (GB)', 'Camera', 'Battery']

# Form input kriteria menggunakan checkbox
selected_kriteria = []
input_kriteria = {}

st.subheader("✅ Checklist Kriteria yang Ingin Digunakan")

for kriteria in all_kriteria:
    if st.checkbox(f"Gunakan {kriteria}?", key=kriteria):
        selected_kriteria.append(kriteria)
        if kriteria == 'Price':
            value = st.number_input(f"Masukkan {kriteria.capitalize()} (Rp)", min_value=0)
        elif kriteria == 'Ratings':
            value = st.slider(f"Masukkan {kriteria.capitalize()}", min_value=0.0, max_value=5.0, step=0.1)
        else:
            options = sorted(df[kriteria].unique())
            value = st.selectbox(f"Pilih {kriteria.upper()}", options, key=kriteria+'_input')
        input_kriteria[kriteria] = value

# Pastikan user memilih minimal satu kriteria
if selected_kriteria:
    # Pilihan jumlah rekomendasi
    st.subheader("🔢 Jumlah Rekomendasi yang Ingin Ditampilkan")
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
        st.subheader("🏆 Hasil Rekomendasi HP")
        st.dataframe(df.iloc[rekomendasi_indices])

else:
    st.info("Silakan pilih minimal satu kriteria terlebih dahulu untuk mendapatkan rekomendasi!")


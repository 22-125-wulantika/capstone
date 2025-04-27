import streamlit as st
import pandas as pd
import numpy as np

# Load dataset
data = pd.read_excel('data_smartphones.xlsx')

# Tampilkan data
st.subheader("Data Smartphone")
st.dataframe(data)

# Pilih kriteria pencarian
st.subheader("Pilih Kriteria Pencarian")
available_criteria = {
    'Harga': 'Price',
    'Rating': 'Ratings',
    'RAM': 'RAM (GB)',
    'ROM': 'ROM (GB)',
    'Kamera': 'Camera',
    'Baterai': 'Battery'
}

selected_criteria = st.multiselect(
    'Pilih kriteria yang ingin digunakan untuk mencari:',
    list(available_criteria.keys())
)

# Dictionary untuk input user
user_input = {}

if selected_criteria:
    st.subheader("Masukkan Nilai Kriteria yang Dipilih")
    for criteria in selected_criteria:
        key = available_criteria[criteria]
        if criteria == 'Ratings':
            user_input[key] = st.slider(f'{criteria} Minimal', 0.0, 5.0, 4.0, step=0.1)
        else:
            user_input[key] = st.number_input(f'{criteria}', min_value=0)

    # Tombol untuk cari rekomendasi
    if st.button('Cari Rekomendasi'):
        # Pastikan kolom yang diperlukan ada
        for col in user_input.keys():
            if col not in data.columns:
                st.error(f"Dataset tidak memiliki kolom '{col}'. Pastikan nama kolom sesuai.")
                st.stop()

        # Filter sesuai kriteria
        query = np.ones(len(data), dtype=bool)  # semua True di awal
        for col, value in user_input.items():
            if col == 'harga':
                query &= (data[col] <= value)  # harga maksimal
            else:
                query &= (data[col] >= value)  # kriteria minimal

        filtered_data = data[query]

        if not filtered_data.empty:
            st.success("Ditemukan rekomendasi sesuai kriteria!")
            st.dataframe(filtered_data)
        else:
            st.warning("Tidak ada yang persis sesuai. Menampilkan yang paling mendekati...")

            # Hitung jarak hanya berdasarkan kriteria yang dipilih
            data_copy = data.copy()

            # Normalisasi nilai agar semua fitur setara
            for col in user_input.keys():
                max_val = data_copy[col].max()
                min_val = data_copy[col].min()
                if max_val != min_val:
                    data_copy[col] = (data_copy[col] - min_val) / (max_val - min_val)
                else:
                    data_copy[col] = 0.0

            user_vector = []
            for col in user_input.keys():
                max_val = data[col].max()
                min_val = data[col].min()
                if max_val != min_val:
                    normalized_value = (user_input[col] - min_val) / (max_val - min_val)
                else:
                    normalized_value = 0.0
                user_vector.append(normalized_value)

            # Hitung Euclidean distance
            data_copy['distance'] = np.linalg.norm(data_copy[list(user_input.keys())].values - np.array(user_vector), axis=1)

            nearest_data = data_copy.sort_values('distance').head(5)
            st.dataframe(data.loc[nearest_data.index])

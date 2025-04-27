import streamlit as st
import pandas as pd
import numpy as np

# Load data
uploaded_file = st.file_uploader("data_smartphone.xlssx", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)

    # Tampilkan data
    st.subheader("Data Smartphone")
    st.dataframe(df)

    # Pilih kriteria pencarian
    st.subheader("Pilih Kriteria Pencarian")
    available_criteria = {
        'Harga': 'harga',
        'Rating': 'rating',
        'RAM': 'ram',
        'ROM': 'rom',
        'Kamera': 'kamera',
        'Baterai': 'baterai'
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
            if criteria == 'Rating':
                user_input[key] = st.slider(f'{criteria} Minimal', 0.0, 5.0, 4.0, step=0.1)
            else:
                user_input[key] = st.number_input(f'{criteria}', min_value=0)

        # Tombol untuk cari rekomendasi
        if st.button('Cari Rekomendasi'):
            # Pastikan kolom yang diperlukan ada
            for col in user_input.keys():
                if col not in df.columns:
                    st.error(f"Dataset tidak memiliki kolom '{col}'. Pastikan nama kolom sesuai.")
                    st.stop()

            # Filter sesuai kriteria
            query = np.ones(len(df), dtype=bool)  # semua True di awal
            for col, value in user_input.items():
                if col == 'harga':
                    query &= (df[col] <= value)  # harga maksimal
                else:
                    query &= (df[col] >= value)  # kriteria minimal

            filtered_df = df[query]

            if not filtered_df.empty:
                st.success("Ditemukan rekomendasi sesuai kriteria!")
                st.dataframe(filtered_df)
            else:
                st.warning("Tidak ada yang persis sesuai. Menampilkan yang paling mendekati...")

                # Hitung jarak hanya berdasarkan kriteria yang dipilih
                df_copy = df.copy()

                # Normalisasi nilai agar semua fitur setara
                for col in user_input.keys():
                    max_val = df_copy[col].max()
                    min_val = df_copy[col].min()
                    if max_val != min_val:
                        df_copy[col] = (df_copy[col] - min_val) / (max_val - min_val)
                    else:
                        df_copy[col] = 0.0

                user_vector = []
                for col in user_input.keys():
                    max_val = df[col].max()
                    min_val = df[col].min()
                    if max_val != min_val:
                        normalized_value = (user_input[col] - min_val) / (max_val - min_val)
                    else:
                        normalized_value = 0.0
                    user_vector.append(normalized_value)

                # Hitung Euclidean distance
                df_copy['distance'] = np.linalg.norm(df_copy[list(user_input.keys())].values - np.array(user_vector), axis=1)

                nearest_df = df_copy.sort_values('distance').head(5)
                st.dataframe(df.loc[nearest_df.index])


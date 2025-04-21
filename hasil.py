import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
data = pd.read_excel('data_smartphones.xlsx')

st.title("📱 Sistem Rekomendasi Smartphone (Content-Based Filtering)")

# Pilihan fitur filter
st.subheader("🔍 Pilih Kriteria Smartphone yang Anda Inginkan")

filter_price = st.checkbox("Filter Harga")
filter_rating = st.checkbox("Filter Rating")
filter_ram = st.checkbox("Filter RAM")
filter_rom = st.checkbox("Filter ROM")
filter_camera = st.checkbox("Filter Kamera")
filter_battery = st.checkbox("Filter Baterai")

# Input pengguna
if any([filter_price, filter_rating, filter_ram, filter_rom, filter_camera, filter_battery]):

    input_name = st.text_input("Masukkan nama HP yang Anda cari (contoh: realme)").lower()

    input_ram = st.selectbox("Pilih RAM (GB)", sorted(data['RAM (GB)'].unique())) if filter_ram else None
    input_rom = st.selectbox("Pilih ROM (GB)", sorted(data['ROM (GB)'].unique())) if filter_rom else None

    max_price = st.number_input("Masukkan Harga Maksimal (Rp)", value=5000000, step=500000) if filter_price else None
    min_rating = st.slider("Pilih Rating Minimal", 0.0, 5.0, 4.0, step=0.1) if filter_rating else None

    unique_cameras = sorted(data['Camera'].unique())
    selected_camera = st.selectbox("Pilih Kamera", unique_cameras) if filter_camera else None

    min_battery = st.selectbox("Pilih Baterai Minimal (mAh)", sorted(data['Battery'].unique())) if filter_battery else None

    # Tombol rekomendasi
    if st.button("🔎 Tampilkan Rekomendasi") and input_name:
        tfidf = TfidfVectorizer()
        name_vectors = tfidf.fit_transform(data['Type'].str.lower())

        # Gabungkan fitur TF-IDF dengan RAM, ROM, Ratings
        numerical_features = data[['RAM (GB)', 'ROM (GB)', 'Ratings']].values
        combined_features = pd.concat([
            pd.DataFrame(name_vectors.toarray()),
            pd.DataFrame(numerical_features)
        ], axis=1).values

        # Query pengguna
        query_vector = tfidf.transform([input_name]).toarray()
        query_numerical = [[input_ram if input_ram is not None else 0,
                            input_rom if input_rom is not None else 0,
                            min_rating if min_rating is not None else 0]]
        query_combined = pd.concat([
            pd.DataFrame(query_vector),
            pd.DataFrame(query_numerical)
        ], axis=1).values

        # Cosine Similarity
        similarities = cosine_similarity(query_combined, combined_features)
        data['Similarity'] = similarities.flatten()

        # Filter data berdasarkan input pengguna
        data_filtered = data.copy()
        if input_name:
            data_filtered = data_filtered[data_filtered['Type'].str.lower().str.contains(input_name)]
        if input_ram is not None:
            data_filtered = data_filtered[data_filtered['RAM (GB)'] == input_ram]
        if input_rom is not None:
            data_filtered = data_filtered[data_filtered['ROM (GB)'] == input_rom]
        if min_rating is not None:
            data_filtered = data_filtered[data_filtered['Ratings'] >= min_rating]
        if max_price is not None:
            data_filtered = data_filtered[data_filtered['Price'] <= max_price]
        if selected_camera is not None:
            data_filtered = data_filtered[data_filtered['Camera'] == selected_camera]
        if min_battery is not None:
            data_filtered = data_filtered[data_filtered['Battery'] >= min_battery]

        # Tampilkan hasil
        st.subheader("📊 Hasil Rekomendasi:")
        if not data_filtered.empty:
            recommended = data_filtered.sort_values(by='Similarity', ascending=False)
            recommended['No'] = range(1, len(recommended) + 1)
            st.dataframe(
                recommended[['No', 'Brand', 'Type', 'RAM (GB)', 'ROM (GB)', 'Ratings', 'Price', 'Camera', 'Battery', 'Similarity']],
                use_container_width=True,
                hide_index=True
            )
        else:
            st.warning("❌ Tidak ada smartphone yang memenuhi kriteria pencarian Anda.")
    elif not input_name:
        st.info("📝 Silakan masukkan nama HP terlebih dahulu sebelum menampilkan rekomendasi.")
else:
    st.info("☝ Silakan aktifkan minimal satu filter untuk memulai pencarian.")

import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import precision_score, recall_score, f1_score

# Load dataset
data = pd.read_excel('data_smartphones.xlsx')

# Fitur yang digunakan untuk similarity
fitur = ['Price', 'Ratings', 'RAM (GB)', 'Battery', 'ROM (GB)']

# Normalisasi fitur
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data[fitur])
similarity_matrix = cosine_similarity(data_scaled)

# Tampilkan judul dan data
st.subheader("📱 Sistem Rekomendasi Smartphone Berdasarkan Preferensi")
st.write("Berikut ini adalah data smartphone yang tersedia:")
st.dataframe(data)

# Filter
st.subheader("🔍 Pilih Kriteria Smartphone yang Anda Inginkan")

filter_price = st.checkbox("Filter Harga")
filter_rating = st.checkbox("Filter Rating")
filter_ram = st.checkbox("Filter RAM")
filter_rom = st.checkbox("Filter ROM")
filter_camera = st.checkbox("Filter Kamera")
filter_battery = st.checkbox("Filter Baterai")

# Input user
if any([filter_price, filter_rating, filter_ram, filter_rom, filter_camera, filter_battery]):
    data_filtered = data.copy()
    
    if filter_price:
        max_price = st.number_input("Masukkan Harga Maksimal (Rp)", min_value=0, value=6000000, step=500000)
        data_filtered = data_filtered[data_filtered['Price'] <= max_price]

    if filter_rating:
        min_rating = st.slider("Pilih Rating Minimal", min_value=0.0, max_value=5.0, value=4.0, step=0.1)
        data_filtered = data_filtered[data_filtered['Ratings'] >= min_rating]

    if filter_ram:
        min_ram = st.selectbox("Pilih RAM Minimal (GB)", sorted(data['RAM (GB)'].unique()))
        data_filtered = data_filtered[data_filtered['RAM (GB)'] >= min_ram]

    if filter_rom:
        min_rom = st.selectbox("Pilih ROM Minimal (GB)", sorted(data['ROM (GB)'].unique()))
        data_filtered = data_filtered[data_filtered['ROM (GB)'] >= min_rom]

    if filter_camera:
        unique_cameras = sorted(data['Camera'].unique())
        selected_camera = st.selectbox("Pilih Kamera", unique_cameras)
        data_filtered = data_filtered[data_filtered['Camera'] == selected_camera]

    if filter_battery:
        min_battery = st.selectbox("Pilih Kapasitas Baterai Minimal (mAh)", sorted(data['Battery'].unique()))
        data_filtered = data_filtered[data_filtered['Battery'] >= min_battery]

    # Menampilkan hasil rekomendasi
    st.subheader("📊 5 Rekomendasi Smartphone Terbaik untuk Anda:")

    if not data_filtered.empty:
        idx_referensi = data.index[data['Type'] == data_filtered.iloc[0]['Type']].tolist()[0]
        similarity_scores = list(enumerate(similarity_matrix[idx_referensi]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        similarity_scores = [s for s in similarity_scores if s[0] != idx_referensi]
        top_indices = [s[0] for s in similarity_scores[:5]]
        rekomendasi = data.iloc[top_indices]
        rekomendasi['No'] = range(1, len(rekomendasi) + 1)

        st.dataframe(
            rekomendasi[['No', 'Brand', 'Type', 'Price', 'Ratings', 'RAM (GB)', 'ROM (GB)', 'Camera', 'Battery']],
            use_container_width=True,
            hide_index=True
        )

    # EVALUASI - hanya dilakukan jika rekomendasi tersedia dan data_filtered tidak kosong
        if 'data_filtered' in locals() and not data_filtered.empty and 'rekomendasi' in locals() and not rekomendasi.empty:
            y_true = [1 if idx in data_filtered.index else 0 for idx in data.index]
            y_pred = [1 if idx in rekomendasi.index else 0 for idx in data.index]
        
            # Hitung evaluasi
            precision = precision_score(y_true, y_pred, zero_division=0)
            recall = recall_score(y_true, y_pred, zero_division=0)
            f1 = f1_score(y_true, y_pred, zero_division=0)
        
            # Tampilkan di Streamlit
            st.subheader("📈 Evaluasi Sistem Rekomendasi")
            st.write(f"**Precision:** {precision:.2f}")
            st.write(f"**Recall:** {recall:.2f}")
            st.write(f"**F1-Score:** {f1:.2f}")
            
    else:
        st.warning("❌ Tidak ada smartphone yang sesuai dengan kriteria filter Anda.")
else:
    st.info("☝ Silakan aktifkan setidaknya satu filter terlebih dahulu untuk melihat hasil rekomendasi.")

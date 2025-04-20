import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Load dataset
data = pd.read_excel('data_smartphones.xlsx')

# Menambahkan kolom ROM dan Kamera ke dalam list fitur numerik
fitur = ['Price', 'Ratings', 'RAM (GB)', 'Battery', 'ROM (GB)', 'Camera (MP)']
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data[fitur])
similarity_matrix = cosine_similarity(data_scaled)

# Tampilkan data smartphone
st.subheader("📱 Data Smartphone")
st.dataframe(data)

# Pilih kolom apa saja yang mau jadi kriteria filter
kolom_filter = st.multiselect(
    "🔍 Pilih kriteria (kolom) untuk filter",
    options=data.columns.tolist()
)

# dictionary untuk menampung kondisi filter
conds = []

for col in kolom_filter:
    if pd.api.types.is_numeric_dtype(data[col]):
        mn, mx = float(data[col].min()), float(data[col].max())
        # user memilih rentang
        rentang = st.slider(f"{col} antara", mn, mx, (mn, mx))
        conds.append((col, rentang[0], rentang[1]))
    else:
        pilihan = st.multiselect(
            f"Pilih nilai untuk {col}",
            options=sorted(data[col].unique())
        )
        if pilihan:
            conds.append((col, pilihan))

st.markdown("---")

if conds:
    df_filt = data.copy()
    # terapkan semua kondisi
    for c in conds:
        if len(c) == 3:
            col, lo, hi = c
            df_filt = df_filt[df_filt[col].between(lo, hi)]
        else:
            col, vals = c
            df_filt = df_filt[df_filt[col].isin(vals)]

    st.subheader("📊 Hasil Filter")
    st.dataframe(df_filt)
    
    if not df_filt.empty:
        # ambil referensi dari baris pertama hasil filter
        idx_ref = df_filt.index[0]
        scores = list(enumerate(similarity_matrix[idx_ref]))
        scores = sorted(scores, key=lambda x: x[1], reverse=True)
        scores = [s for s in scores if s[0] != idx_ref][:5]
        top_idx = [s[0] for s in scores]
        
        rec = data.iloc[top_idx].copy()
        rec['Ranking'] = range(1, len(rec)+1)
        
        st.subheader("⭐ 5 Rekomendasi Teratas")
        cols = ['Ranking'] + data.columns.tolist()
        st.dataframe(rec[cols])
    else:
        st.warning("❌ Tidak ada data yang cocok dengan kriteria Anda.")
else:
    st.info("☝️ Pilih minimal satu kolom sebagai filter terlebih dahulu.")

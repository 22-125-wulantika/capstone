import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

# Load dataset
data = pd.read_excel('data_smartphones.xlsx')

# Fitur yang digunakan untuk similarity
fitur = ['Price', 'Ratings', 'RAM (GB)', 'Battery', 'ROM (GB)']

# Normalisasi data
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data[fitur])

# Tampilkan judul dan data
st.subheader("📱 Sistem Rekomendasi Smartphone Berdasarkan Preferensi")
st.write("Berikut ini adalah data smartphone yang tersedia:")
st.dataframe(data)

# Input preferensi pengguna (tidak terbatas)
st.subheader("🎯 Masukkan Preferensi Anda")
price_input = st.number_input("Harga Maksimal yang Diinginkan (Rp)", min_value=0, value=4000000, step=100000)
rating_input = st.number_input("Rating Minimal yang Diinginkan", min_value=0.0, max_value=5.0, value=4.2, step=0.1)
ram_input = st.number_input("RAM Minimal yang Diinginkan (GB)", min_value=1, value=6)
rom_input = st.number_input("ROM Minimal yang Diinginkan (GB)", min_value=4, value=128)
battery_input = st.number_input("Kapasitas Baterai Minimal (mAh)", min_value=1000, value=5000)

# Buat dataframe input user
user_input = pd.DataFrame([[price_input, rating_input, ram_input, battery_input, rom_input]], columns=fitur)

# Normalisasi input pengguna
user_scaled = scaler.transform(user_input)

# Hitung similarity antara input dan semua data
similarities = cosine_similarity(user_scaled, data_scaled)[0]
data['Similarity'] = similarities

# Ambil 5 teratas
top_5 = data.sort_values(by='Similarity', ascending=False).head(5).copy()
top_5['No'] = range(1, len(top_5) + 1)

# Tampilkan hasil rekomendasi
st.subheader("📊 Rekomendasi Smartphone Terdekat dengan Preferensi Anda:")
st.dataframe(top_5[['No', 'Brand', 'Type', 'Price', 'Ratings', 'RAM (GB)', 'ROM (GB)', 'Camera', 'Battery']])

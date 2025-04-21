import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Load dataset
data = pd.read_excel('data_smartphones.xlsx')

# Fitur numerik yang akan digunakan
fitur = ['Price', 'Ratings', 'RAM (GB)', 'ROM (GB)', 'Battery']

# Normalisasi dataset
scaler = MinMaxScaler()
data_scaled = scaler.fit_transform(data[fitur])

# Masukkan input pengguna
st.subheader("📱 Sistem Rekomendasi Smartphone Berdasarkan Preferensi")
st.write("Silakan masukkan preferensi Anda. Sistem akan mencari smartphone yang paling mendekati:")

input_price = st.number_input("Harga yang Diinginkan (Rp)", min_value=0, value=3000000)
input_rating = st.number_input("Rating yang Diinginkan (0.0 - 5.0)", min_value=0.0, max_value=5.0, value=4.5, step=0.1)
input_ram = st.number_input("RAM yang Diinginkan (GB)", min_value=1, value=6)
input_rom = st.number_input("ROM yang Diinginkan (GB)", min_value=8, value=128)
input_battery = st.number_input("Kapasitas Baterai yang Diinginkan (mAh)", min_value=1000, value=5000)

# Buat vektor input dan normalisasi seperti data
user_input = pd.DataFrame([[input_price, input_rating, input_ram, input_rom, input_battery]], columns=fitur)
user_input_scaled = scaler.transform(user_input)

# Hitung similarity
similarities = cosine_similarity(user_input_scaled, data_scaled)[0]
data['Similarity'] = similarities

# Ambil 5 rekomendasi teratas
rekomendasi = data.sort_values(by='Similarity', ascending=False).head(5).copy()
rekomendasi['No'] = range(1, len(rekomendasi) + 1)

# Tampilkan hasil
st.subheader("📊 5 Rekomendasi Smartphone Terdekat dengan Preferensi Anda:")
st.dataframe(rekomendasi[['No', 'Brand', 'Type', 'Price', 'Ratings', 'RAM (GB)', 'ROM (GB)', 'Camera', 'Battery']])

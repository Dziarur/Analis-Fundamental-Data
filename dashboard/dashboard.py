import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/Dziarur/Analis-Fundamental-Data/refs/heads/main/dashboard/main_data.csv")
    return df

df = load_data()

st.title("Analisis Dashboard E-Commerce")

st.header("1. Bagaimana tingkat repeat order pelanggan dan apa yang dapat disimpulkan mengenai loyalitas pelanggan berdasarkan data tersebut?")

repeat = df.groupby('customer_unique_id_x')['order_id'].nunique()
fig1, ax1 = plt.subplots()
repeat.value_counts().sort_index().loc[:5].plot(kind='bar', ax=ax1)

ax1.set_title("Distribusi Jumlah Order per Customer")
ax1.set_xlabel("Jumlah Order")
ax1.set_ylabel("Jumlah Customer")

st.pyplot(fig1)

st.header("2. Bagaimana distribusi dan rata-rata rating produk lalu apakah terdapat perbedaan kualitas antar kategori produk?")

avg_rating = df['review_score'].mean()
fig2, ax2 = plt.subplots()
df['review_score'].value_counts().sort_index().plot(kind='bar', ax=ax2)

ax2.set_title("Distribusi Rating Produk")
ax2.set_xlabel("Rating")
ax2.set_ylabel("Jumlah")

st.pyplot(fig2)

st.header("Kesimpulan")
st.write(
    """
Conclution pertanyaan 1 Berdasarkan hasil analisis, mayoritas pelanggan hanya melakukan satu kalai pembelian, dengan jumlah yang jauh lebih besar dibandingkan pelanggan yang melakukan pembelian lebih dari satu kali. Hal ini menunjukkan bahwa tingkat repeat order masih rendah, sehingga dapat disimpulkan bahwa loyalitas pelanggan terhadap platform masih tergolong rendah.

Conclution pertanyaan 2 Berdasarkan analisis rating produk, ditemukans secar umum pelanggan memberikan penilaian yang tinggi terhadap produk yang dibeli, yang menunjukkan tingkat kepuasan yang baik. Namun, terdapat beberapa kategori produk yang memiliki rating lebih rendah dibanding kategori lainnya, yang mengindikasikan adanya masalah kualitas produk atau layanan pada kategori tersebut.
"""
)
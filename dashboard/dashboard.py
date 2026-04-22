import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/Dziarur/Analis-Fundamental-Data/refs/heads/main/dashboard/main_data.csv")
    return df

df = load_data()

df['product_category_name'] = df['product_category_name'].fillna('Unknown')

# Sidebar
st.sidebar.header("Filter")

# Filter Kategori
kategori = st.sidebar.multiselect(
    "Pilih Kategori",
    options=df['product_category_name'].unique(),
    default=df['product_category_name'].unique()
)

# Filter rating
rating_filter = st.sidebar.slider(
    "Range Rating",
    min_value=int(df['review_score'].min()),
    max_value=int(df['review_score'].max()),
    value=(int(df['review_score'].min()), int(df['review_score'].max()))
)

# Filter Waktu
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['year'] = df['order_purchase_timestamp'].dt.year

tahun = st.sidebar.slider(
    "Pilih Rentang Tahun",
    int(df['year'].min()),
    int(df['year'].max()),
    (2016, 2018)
)

# Apply filter
df_filtered = df[
    (df['product_category_name'].isin(kategori)) &
    (df['review_score'] >= rating_filter[0]) &
    (df['review_score'] <= rating_filter[1])
]

# title
st.title("Analisis Dashboard E-Commerce")

# KPI

col1, col2 = st.columns(2)
repeat = df_filtered.groupby('customer_unique_id')['order_id'].nunique()
repeat_rate = (repeat > 1).sum() / repeat.count()

col1.metric("Repeat Order Rate", f"{repeat_rate:.2%}")

# Rata-rata Rating
avg_rating = df_filtered['review_score'].mean()
col2.metric("Average Rating", round(avg_rating, 2))

# Repeat Order

st.header("Repeat Order Analysis")

fig1, ax1 = plt.subplots()
ax1.hist(repeat, bins=10)

ax1.set_title("Distribusi Jumlah Order per Customer")
ax1.set_xlabel("Jumlah Order")
ax1.set_ylabel("Frekuensi")

st.pyplot(fig1)

# Rating
st.header("Product Rating Analysis")

col3, col4 = st.columns(2)

# Histogram rating
fig2, ax2 = plt.subplots()
ax2.hist(df_filtered['review_score'], bins=5)

ax2.set_title("Distribusi Rating")
col3.pyplot(fig2)

# Boxplot rating
fig3, ax3 = plt.subplots()
ax3.boxplot(df_filtered['review_score'])

ax3.set_title("Boxplot Rating")
col4.pyplot(fig3)

# Kategori
st.subheader("Rating per Kategori")

rating_kategori = (
    df_filtered.groupby('product_category_name')['review_score']
    .mean()
    .sort_values()
)

fig4, ax4 = plt.subplots()
rating_kategori.head(10).plot(kind='barh', ax=ax4)

ax4.set_title("Top 10 Kategori Rating Terendah")

st.pyplot(fig4)


st.header("Kesimpulan")
st.write(
    """
- Conclution pertanyaan 1

Sebagian besar pelanggan hanya melakukan satu kali pembelian, yang ditunjukkan oleh distribusi jumlah order yang didominasi oleh nilai satu. Nilai repeat order rate yang relatif rendah mengindikasikan bahwa tingkat loyalitas pelanggan masih belum optimal.

Meskipun terdapat beberapa pelanggan dengan frekuensi pembelian tinggi (outlier), jumlahnya sangat kecil dibandingkan keseluruhan pelanggan. Hal ini menunjukkan bahwa bisnis masih memiliki peluang besar untuk meningkatkan retensi pelanggan.
- Conclution pertanyaan 2

Rata-rata rating produk berada pada tingkat yang cukup tinggi, yang menunjukkan bahwa secara umum pelanggan merasa puas terhadap produk yang dibeli. Distribusi rating juga cenderung terkonsentrasi pada nilai tinggi.

Namun, terdapat variasi rating antar kategori produk, di mana beberapa kategori memiliki nilai yang lebih rendah dibandingkan yang lain. Hal ini mengindikasikan adanya ketidakkonsistenan kualitas produk atau layanan pada kategori tertentu yang perlu diperhatikan.
"""
)
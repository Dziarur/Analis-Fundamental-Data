import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
Conclution pertanyaan 1
Berdasarkan hasil analisis eksploratif, distribusi jumlah pembelian menunjukkan bahwa sebagian besar pelanggan hanya melakukan satu kali transaksi. Hal ini didukung oleh nilai repeat order rate yang relatif rendah, yang mengindikasikan bahwa tingkat loyalitas pelanggan masih belum optimal.

Visualisasi histogram memperlihatkan dominasi pelanggan dengan satu kali pembelian, sementara boxplot menunjukkan adanya sejumlah kecil pelanggan dengan frekuensi pembelian tinggi sebagai outlier. Dengan demikian, dapat disimpulkan bahwa mayoritas pelanggan belum melakukan pembelian ulang secara konsisten.

Conclution pertanyaan 2
Berdasarkan hasil analisis, rata-rata rating produk menunjukkan nilai yang relatif tinggi, yang mengindikasikan bahwa secara umum pelanggan merasa puas terhadap produk yang dibeli.

Visualisasi histogram menunjukkan bahwa sebagian besar rating berada pada nilai tinggi, sedangkan boxplot mengindikasikan bahwa sebaran rating cukup terkonsentrasi tanpa banyak outlier ekstrem. Namun, analisis lebih lanjut pada tingkat kategori produk menunjukkan adanya variasi rating antar kategori, di mana beberapa kategori memiliki nilai lebih rendah dibandingkan yang lain.

Hal ini menunjukkan bahwa meskipun kepuasan pelanggan secara keseluruhan baik, masih terdapat peluang perbaikan pada kategori produk tertentu.
"""
)
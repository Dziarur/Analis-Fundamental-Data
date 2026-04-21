import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/Dziarur/Analis-Fundamental-Data/refs/heads/main/dashboard/main_data.csv")
    return df

df = load_data()

st.sidebar.header("Parameter SMART")
target_increase = st.sidebar.slider("Target Kenaikan Konversi (%)", 1, 20, 5)
customer_counts = df.groupby('customer_unique_id')['order_id'].nunique()
dist = customer_counts.value_counts().sort_index()
    
n_order_1 = dist.get(1, 0)
n_order_2 = dist.get(2, 0)
current_conv = (n_order_2 / n_order_1) * 100 if n_order_1 > 0 else 0
target_conv = current_conv + target_increase
target_val = n_order_1 * (target_conv / 100)


st.title("Analisis Dashboard E-Commerce")

st.header("1. Bagaimana tingkat repeat order pelanggan dan apa yang dapat disimpulkan mengenai loyalitas pelanggan berdasarkan data tersebut?")
col1, col2 = st.columns([2, 1])

with col1:
        fig1, ax1 = plt.subplots(figsize=(10, 5))
        bars = ax1.bar(dist.index.astype(str), dist.values, color='#1f77b4', alpha=0.7)
        ax1.axhline(y=target_val, color='red', linestyle='--', label=f'Target (+{target_increase}%)')
        
        # Label angka
        for bar in bars:
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 100, 
                     int(bar.get_height()), ha='center', va='bottom')
        
        ax1.set_xlabel("Jumlah Order per Pelanggan")
        ax1.set_ylabel("Jumlah Pelanggan")
        ax1.legend()
        st.pyplot(fig1)

with col2:
        st.metric("Total Pelanggan", f"{len(customer_counts):,}")
        st.metric("Konversi Saat Ini", f"{current_conv:.2f}%")
        st.metric(f"Target (+{target_increase}%)", f"{target_conv:.2f}%", delta=f"{target_increase}%")
        st.info(f"Untuk mencapai target, Anda butuh {int(target_val)} pelanggan di Order ke-2.")

st.divider()


st.header("2. Bagaimana distribusi dan rata-rata rating produk lalu apakah terdapat perbedaan kualitas antar kategori produk?")
st.header("2. Strategi Retensi: Review & Kategori")
col3, col4 = st.columns(2)

    # Data untuk strategi
customer_profile = df.groupby('customer_unique_id').agg({
        'order_id': 'nunique',
        'review_score': 'mean'
    }).reset_index()
customer_profile['Status'] = customer_profile['order_id'].apply(lambda x: 'Repeat' if x > 1 else 'Single')

with col3:
        st.subheader("Kepuasan vs Loyalitas")
        fig2, ax2 = plt.subplots()
        sns.barplot(x='Status', y='review_score', data=customer_profile, ax=ax2, palette='Blues')
        ax2.set_ylim(0, 5)
        st.pyplot(fig2)
        st.caption("Pelanggan Repeat cenderung memiliki skor review lebih tinggi.")

with col4:
        st.subheader("Top 10 Kategori Repeat Order")
        repeat_cust_ids = customer_profile[customer_profile['Status'] == 'Repeat']['customer_unique_id']
        repeat_data = df[df['customer_unique_id'].isin(repeat_cust_ids)]
        top_cats = repeat_data['product_category_name'].value_counts().head(10)
        
        fig3, ax3 = plt.subplots()
        top_cats.plot(kind='barh', ax=ax3, color='#5fb0c0')
        ax3.invert_yaxis()
        st.pyplot(fig3)


st.header("Kesimpulan")
st.write(
    """
Conclution pertanyaan 1 Berdasarkan hasil analisis, mayoritas pelanggan hanya melakukan satu kalai pembelian, dengan jumlah yang jauh lebih besar dibandingkan pelanggan yang melakukan pembelian lebih dari satu kali. Hal ini menunjukkan bahwa tingkat repeat order masih rendah, sehingga dapat disimpulkan bahwa loyalitas pelanggan terhadap platform masih tergolong rendah.

Conclution pertanyaan 2 Berdasarkan analisis rating produk, ditemukans secar umum pelanggan memberikan penilaian yang tinggi terhadap produk yang dibeli, yang menunjukkan tingkat kepuasan yang baik. Namun, terdapat beberapa kategori produk yang memiliki rating lebih rendah dibanding kategori lainnya, yang mengindikasikan adanya masalah kualitas produk atau layanan pada kategori tersebut.
"""
)
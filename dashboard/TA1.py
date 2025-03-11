import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data():
    files = {
        "Distrik Aotizhongxin": "dashboard/df_Aotizhongxin.csv",
        "Distrik Changping": "dashboard/df_changping.csv",
        "Distrik Dingling": "dashboard/df_dingling.csv",
        "Distrik Dongsi": "dashboard/df_dongsi.csv",
        "Distrik Guanyuan": "dashboard/df_guanyuan.csv",
        "Distrik Gucheng": "dashboard/df_gucheng.csv",
        "Distrik Huairou": "dashboard/df_huairou.csv",
        "Distrik Nongzhanguan": "dashboard/df_nongzhanguan.csv",
        "Distrik Shunyi": "dashboard/df_shunyi.csv",
        "Distrik Tiantan": "dashboard/df_tiantan.csv",
        "Distrik Wanliu": "dashboard/df_wanliu.csv",
        "Distrik Wanshouxigong": "dashboard/df_wanshouxing.csv",
    }
    data = {name: pd.read_csv(path) for name, path in files.items()}
    return data

data = load_data()

st.set_page_config(page_title="Dashboard Polusi Udara", layout="wide")
st.title("🌍 Dashboard Analisis Data Polusi Udara")
st.markdown("---")

st.sidebar.header("📂 Pilih Dataset")
dataset_name = st.sidebar.selectbox("Pilih dataset:", list(data.keys()))
df = data[dataset_name]

st.write(f"## Data: {dataset_name}")
st.dataframe(df)

st.write("## 📊 Statistik Dataset")
st.write(df.describe())

st.markdown("---")
st.write("## 📈 Visualisasi Data")
col1, col2 = st.columns(2)

with col1:
    column = st.selectbox("Pilih kolom untuk grafik batang:", df.columns)
    fig, ax = plt.subplots(figsize=(7,5))
    df[column].value_counts().plot(kind='bar', color='skyblue', ax=ax)
    ax.set_title(f"Distribusi {column} (Grafik Batang)")
    ax.set_ylabel("Frekuensi")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)

with col2:
    if len(df.columns) > 1:
        x_col = st.selectbox("Pilih kolom X untuk grafik garis:", df.columns)
        y_col = st.selectbox("Pilih kolom Y untuk grafik garis:", df.columns)
        fig, ax = plt.subplots(figsize=(7,5))
        sns.lineplot(x=df[x_col], y=df[y_col], marker='o', ax=ax, color='orange')
        ax.set_title(f"Pergerakan {y_col} terhadap {x_col} (Grafik Garis)")
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)

st.markdown("---")
st.write("### 📌 Catatan:")
st.info("Gunakan sidebar untuk memilih dataset dan melihat statistiknya dan eksplorasi visual data.")

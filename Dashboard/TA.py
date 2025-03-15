import streamlit as st 
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    df_hari = pd.read_csv("day.csv")
    df_jam = pd.read_csv("hour.csv")
    return df_hari, df_jam

df_hari, df_jam = load_data()

season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
df_hari['season'] = df_hari['season'].map(season_mapping)

st.title("Visualisasi Data Bike Sharing")

st.subheader("Pola Penggunaan Sepeda Berdasarkan Hari dalam Seminggu")
usage_per_day = df_hari.groupby(['weekday', 'workingday'])['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#92C5DE", "#F4A582"]  
bar_plot = sns.barplot(data=usage_per_day, x='weekday', y='cnt', hue='workingday', palette=colors, ax=ax)
ax.set_xlabel("Hari dalam Seminggu")
ax.set_ylabel("Rata-rata Penggunaan Sepeda")
ax.set_title("Pola Penggunaan Sepeda Berdasarkan Hari dalam Seminggu")
ax.legend(title="Hari Kerja", labels=["Tidak", "Ya"], loc='upper right')  

for p in bar_plot.patches:
    ax.annotate(f'{p.get_height():.0f}', 
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='bottom', fontsize=10, color='black')

st.pyplot(fig)

st.subheader("Pola Penggunaan Sepeda Berdasarkan Jam dalam Sehari")
usage_per_hour = df_jam.groupby('hr')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=usage_per_hour, x='hr', y='cnt', marker='o', linestyle='-', color='green', ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Penggunaan Sepeda")
ax.set_title("Pola Penggunaan Sepeda Berdasarkan Jam dalam Sehari")
ax.set_xticks(range(0, 24))
ax.grid(True)

for x, y in zip(usage_per_hour['hr'], usage_per_hour['cnt']):
    ax.text(x, y + 8, f'{y:.0f}', ha='center', fontsize=10)

st.pyplot(fig)

st.subheader("Penggunaan Sepeda oleh Casual dan Registered pada Akhir Pekan")
df_weekend = df_hari[df_hari['weekday'].isin([0, 6])]
weekend_usage = df_weekend[['casual', 'registered']].sum()

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(weekend_usage.index, weekend_usage.values, color=['blue', 'green'])
ax.set_xlabel("Kategori Pengguna")
ax.set_ylabel("Jumlah Penggunaan")
ax.set_title("Penggunaan Sepeda pada Akhir Pekan")
ax.set_ylim(0, weekend_usage.max() + 60000)
ax.set_xticks(range(len(weekend_usage.index)))
ax.set_xticklabels(weekend_usage.index, fontsize=12)

for bar in bars:
    yval = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, yval + 20000, round(yval), ha='center', va='bottom', fontsize=10)

st.pyplot(fig)

st.subheader("Tren Penggunaan Sepeda Berdasarkan Musim")
season_usage = df_hari.groupby('season')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=season_usage, hue='season', palette='deep', ax=ax, legend=False)

plt.ylim(0, 6000)

for p in ax.patches:
    ax.annotate(f'{p.get_height():.0f}',  
                (p.get_x() + p.get_width() / 2., p.get_height()), 
                ha='center', va='bottom', fontsize=12, color='black', xytext=(0, 5), 
                textcoords='offset points')

ax.set_xlabel('Musim')
ax.set_ylabel('Rata-rata Penggunaan')
ax.set_title('Tren Penggunaan Sepeda Berdasarkan Musim')

plt.tight_layout()
st.pyplot(fig)

st.subheader("Perbandingan Penggunaan Sepeda antara Tahun 2011 dan 2012")
usage_per_year = df_hari.groupby('yr')['cnt'].sum()
increase_percent = ((usage_per_year[1] - usage_per_year[0]) / usage_per_year[0]) * 100

fig, ax = plt.subplots(figsize=(6, 4))
ax.bar([2012, 2011], usage_per_year.values, color=["blue", "green"])
ax.set_xlabel(f"Tahun\n\n Total Peningkatan: {increase_percent:.2f}%")
ax.set_ylabel("Jumlah Penggunaan Sepeda")
ax.set_title("Perbandingan Penggunaan Sepeda 2011 vs 2012\n")
ax.set_ylim(0, usage_per_year.max() * 1.1)
ax.set_xticks([2012, 2011])
ax.set_xticklabels(["2012", "2011"])

for i, v in enumerate(usage_per_year.values):
    ax.text([2012, 2011][i], v + 50000, f"{v:,}", ha="center", fontsize=12)

st.pyplot(fig)

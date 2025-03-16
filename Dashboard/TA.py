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
df_hari['dteday'] = pd.to_datetime(df_hari['dteday'])
df_jam['dteday'] = pd.to_datetime(df_jam['dteday'])

with st.sidebar:
    st.header("Pengaturan Filter")

    min_date = df_hari['dteday'].min().date()
    max_date = df_hari['dteday'].max().date()
    selected_dates = st.date_input(
        "Rentang Tanggal",
        [min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    if len(selected_dates) != 2:
        st.error("Silakan pilih rentang tanggal (awal dan akhir).")
        st.stop()
    start_date, end_date = selected_dates

    selected_seasons = st.multiselect(
        "Musim",
        options=["Spring", "Summer", "Fall", "Winter"],
        default=["Spring", "Summer", "Fall", "Winter"]
    )

    hour_range = st.slider(
        "Rentang Jam",
        min_value=0,
        max_value=23,
        value=(0, 23)
    )

    show_annotations = st.checkbox("Tampilkan Anotasi", value=True)

df_hari_filtered = df_hari[
    (df_hari['dteday'].dt.date >= start_date) & 
    (df_hari['dteday'].dt.date <= end_date) &
    (df_hari['season'].isin(selected_seasons))
]

season_code_mapping = {"Spring": 1, "Summer": 2, "Fall": 3, "Winter": 4}
selected_season_codes = [season_code_mapping[s] for s in selected_seasons]

df_jam_filtered = df_jam[
    (df_jam['dteday'].dt.date >= start_date) & 
    (df_jam['dteday'].dt.date <= end_date) &
    (df_jam['season'].isin(selected_season_codes))
]

st.title("Visualisasi Data Bike Sharing")

st.subheader("Pola Penggunaan Sepeda Berdasarkan Hari dalam Seminggu")
usage_per_day = df_hari_filtered.groupby(['weekday', 'workingday'])['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
colors = ["#92C5DE", "#F4A582"]  
bar_plot = sns.barplot(data=usage_per_day, x='weekday', y='cnt', hue='workingday', palette=colors, ax=ax)
ax.set_xlabel("Hari dalam Seminggu")
ax.set_ylabel("Rata-rata Penggunaan Sepeda")
ax.legend(title="Hari Kerja", labels=["Libur", "Kerja"], loc='upper right')

if show_annotations:
    for p in bar_plot.patches:
        ax.annotate(f'{p.get_height():.0f}', 
                    (p.get_x() + p.get_width()/2, p.get_height()),
                    ha='center', va='bottom', fontsize=10)
st.pyplot(fig)

st.subheader("Pola Penggunaan Sepeda Berdasarkan Jam dalam Sehari")
df_jam_hour_filtered = df_jam_filtered[
    (df_jam_filtered['hr'] >= hour_range[0]) & 
    (df_jam_filtered['hr'] <= hour_range[1])
]
usage_per_hour = df_jam_hour_filtered.groupby('hr')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=usage_per_hour, x='hr', y='cnt', marker='o', color='green', ax=ax)
ax.set_xlabel("Jam dalam Sehari")
ax.set_ylabel("Rata-rata Penggunaan Sepeda")
ax.set_xticks(range(hour_range[0], hour_range[1]+1))

if show_annotations:
    for x, y in zip(usage_per_hour['hr'], usage_per_hour['cnt']):
        ax.text(x, y + 8, f'{y:.0f}', ha='center', fontsize=10)
st.pyplot(fig)

st.subheader("Penggunaan Sepeda pada Akhir Pekan")
df_weekend = df_hari_filtered[df_hari_filtered['weekday'].isin([0, 6])]
weekend_usage = df_weekend[['casual', 'registered']].sum()

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(weekend_usage.index, weekend_usage.values, color=['blue', 'green'])
ax.set_ylim(0, weekend_usage.max() + 60000)

if show_annotations:
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, yval + 20000, f'{yval:,}', ha='center', fontsize=10)
st.pyplot(fig)

st.subheader("Tren Penggunaan Berdasarkan Musim")
season_usage = df_hari_filtered.groupby('season')['cnt'].mean().reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='season', y='cnt', data=season_usage, palette='deep', ax=ax)

if show_annotations:
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.0f}', 
                   (p.get_x() + p.get_width()/2, p.get_height()),
                   ha='center', va='bottom', fontsize=12)
st.pyplot(fig)


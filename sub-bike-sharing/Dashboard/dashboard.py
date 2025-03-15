import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

# Menyiapkan data
DAY_DF_URL = "https://raw.githubusercontent.com/startpufftt/byke-sharing-project-dicoding/refs/heads/main/Bike-sharing-dataset/day.csv"
HOUR_DF_URL = "https://raw.githubusercontent.com/startpufftt/byke-sharing-project-dicoding/refs/heads/main/Bike-sharing-dataset/hour.csv"

day_df = pd.read_csv(DAY_DF_URL)
hour_df = pd.read_csv(HOUR_DF_URL)

# Mengubah nama kolom untuk memudahkan analisis
day_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count'
}, inplace=True)

hour_df.rename(columns={
    'dteday': 'dateday',
    'yr': 'year',
    'mnth': 'month',
    'weathersit': 'weather_cond',
    'cnt': 'count',
    'hr': 'hour'
}, inplace=True)

# Mengubah angka menjadi keterangan pada day_df
day_df['month'] = day_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
day_df['season'] = day_df['season'].map({1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'})
day_df['weekday'] = day_df['weekday'].map({
    0: 'Sun', 1: 'Mon', 2: 'Tue', 3: 'Wed', 4: 'Thu', 5: 'Fri', 6: 'Sat'
})
day_df['weather_cond'] = day_df['weather_cond'].map({
    1: 'Clear/Partly Cloudy', 2: 'Misty/Cloudy', 3: 'Light Snow/Rain', 4: 'Severe Weather'
})

# Mengambil rentang tanggal dari dataset
min_date = pd.to_datetime(day_df['dateday']).dt.date.min()
max_date = pd.to_datetime(day_df['dateday']).dt.date.max()

# Sidebar untuk memilih rentang tanggal
title_sidebar = "### Filter Data"
st.sidebar.markdown(title_sidebar)
start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

# Memfilter data berdasarkan rentang tanggal
main_df = day_df[(day_df['dateday'] >= str(start_date)) & (day_df['dateday'] <= str(end_date))]

# Fungsi untuk visualisasi berdasarkan musim
def plot_seasonal_sharing():
    seasonal_usage = main_df.groupby('season')[['registered', 'casual', 'count']].sum().reset_index()
    plt.figure(figsize=(10, 6))
    bar_width = 0.4
    season_index = np.arange(len(seasonal_usage['season']))

    plt.bar(season_index - bar_width/2, seasonal_usage['registered'], width=bar_width, label='Registered', color='tab:blue')
    plt.bar(season_index + bar_width/2, seasonal_usage['casual'], width=bar_width, label='Casual', color='tab:orange')

    plt.xlabel('Musim')
    plt.ylabel('Total Peminjaman Sepeda')
    plt.title(f'Jumlah Penyewaan Sepeda Berdasarkan Musim\n({start_date} - {end_date})')
    plt.xticks(season_index, seasonal_usage['season'])
    plt.legend()
    st.pyplot(plt)

# Fungsi untuk visualisasi peminjaman saat hari libur
def plot_holiday_sharing():
    libur = ['Tidak Libur', 'Libur']
    holiday_usage = main_df.copy()
    holiday_usage['holiday'] = holiday_usage['holiday'].replace([0, 1], libur)
    holiday_usage = holiday_usage.groupby('holiday')[['registered', 'casual', 'count']].sum().reset_index()

    plt.figure(figsize=(10, 6))
    bar_width = 0.4
    holiday_index = np.arange(len(holiday_usage['holiday']))

    plt.bar(holiday_index - bar_width/2, holiday_usage['registered'], width=bar_width, label='Registered', color='tab:blue')
    plt.bar(holiday_index + bar_width/2, holiday_usage['casual'], width=bar_width, label='Casual', color='tab:orange')

    plt.xlabel('Hari Libur')
    plt.ylabel('Total Peminjaman Sepeda')
    plt.title(f'Jumlah Penyewaan Sepeda Berdasarkan Hari Libur\n({start_date} - {end_date})')
    plt.xticks(holiday_index, holiday_usage['holiday'])
    plt.legend()
    st.pyplot(plt)

# Membuat tampilan dashboard
st.header('Bike Sharing Dashboard')
st.subheader('Seasonal Sharing')
plot_seasonal_sharing()
st.subheader('Holiday Sharing')
plot_holiday_sharing()
st.caption('Copyright (c) Ikbal Fakula')

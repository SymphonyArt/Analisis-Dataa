import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Dashboard Analisis Data Penyewaan Sepeda")

# Membaca dataset
file_path = "dashboard/combined_dataset.csv"
df = pd.read_csv(file_path)
df.rename(columns={"cnt": "total_rent"}, inplace=True)
df.rename(columns={"yr": "year"}, inplace=True)
df.rename(columns={"dteday": "dateday"}, inplace=True)
df.rename(columns={"mnth": "month"}, inplace=True)
df.rename(columns={"weekday": "day_of_week"}, inplace=True)
df.rename(columns={"weathersit": "weather_condition"}, inplace=True)
df.rename(columns={"casual": "casual_user"}, inplace=True)
df.rename(columns={"registered": "registered_user"}, inplace=True)
df.rename(columns={"instant": "index"}, inplace=True)
df["dateday"] = pd.to_datetime(df["dateday"])

# Sidebar untuk pemilihan rentang tanggal
date_range = st.sidebar.date_input("Pilih Rentang Tanggal", [df["dateday"].min(), df["dateday"].max()])

# Filter dataset
filtered_df = df[(df["dateday"] >= pd.to_datetime(date_range[0])) & (df["dateday"] <= pd.to_datetime(date_range[1]))]

# Plot rata-rata peminjaman sepeda berdasarkan hari dalam seminggu
day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
weekday_avg_rentals = filtered_df.groupby("day_of_week")["total_rent"].mean().reindex(day_order)

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=weekday_avg_rentals.index, y=weekday_avg_rentals.values, marker="o", color="blue", linewidth=2, ax=ax)
ax.set_title("Rata-rata Peminjaman Sepeda per Hari dalam Seminggu")
ax.set_xlabel("Hari dalam Seminggu")
ax.set_ylabel("Rata-rata Peminjaman Sepeda")
ax.grid(True)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

# Menambahkan nilai pada setiap titik
for x, y in zip(weekday_avg_rentals.index, weekday_avg_rentals.values):
    ax.text(x, y, f"{y:.1f}", ha="center", va="bottom", fontsize=10, fontweight="bold")

st.pyplot(fig)

# Plot total peminjaman sepeda berdasarkan hari dalam seminggu
weekday_total_rentals = filtered_df.groupby("day_of_week")["total_rent"].sum().reindex(day_order)

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=weekday_total_rentals.index, y=weekday_total_rentals.values, marker="o", color="green", linewidth=2, ax=ax)
ax.set_title("Total Peminjaman Sepeda per Hari dalam Seminggu")
ax.set_xlabel("Hari dalam Seminggu")
ax.set_ylabel("Total Peminjaman Sepeda")
ax.grid(True)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

# Menambahkan nilai pada setiap titik
for x, y in zip(weekday_total_rentals.index, weekday_total_rentals.values):
    ax.text(x, y, f"{y:,}", ha="center", va="bottom", fontsize=10, fontweight="bold")

st.pyplot(fig)

# Membuat pivot table untuk jumlah peminjaman berdasarkan musim dan kondisi cuaca
season_weather_pivot = filtered_df.pivot_table(
    values="total_rent",  # Kolom yang akan dijumlahkan
    index="season",       # Baris berdasarkan musim
    columns="weather_condition",  # Kolom berdasarkan kondisi cuaca
    aggfunc="sum"         # Menggunakan total peminjaman sepeda
)

# Menentukan batas untuk perbedaan warna di heatmap
max_value = season_weather_pivot.values.max()
threshold = 100000  # Nilai batasan untuk warna yang berbeda

# Normalisasi rentang warna untuk membuatnya lebih terlihat pada warna yang sesuai
norm = plt.Normalize(vmin=0, vmax=max_value)

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(season_weather_pivot, annot=True, fmt=".0f", linewidths=0.5,
            cmap="coolwarm", cbar=False, norm=norm, vmin=0, vmax=max_value)

# Menambahkan warna dengan perbedaan untuk nilai di atas threshold
sns.heatmap(season_weather_pivot, annot=False, fmt=".0f", linewidths=0.5,
            cmap='RdYlBu_r', mask=season_weather_pivot < threshold, cbar=False,
            norm=norm, vmin=0, vmax=max_value)

ax.set_xlabel("Weather Condition", fontsize=12)
ax.set_ylabel("Season", fontsize=12)
ax.set_title("Bike Rentals by Season and Weather Condition", fontsize=14)
plt.xticks(rotation=45)  # Membuat label sumbu-x miring
st.pyplot(fig)

# Mengelompokkan data berdasarkan kondisi cuaca dan menghitung rata-rata peminjaman
weather_counts = filtered_df.groupby("weather_condition")["total_rent"].mean().sort_index()

fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(x=weather_counts.index, y=weather_counts.values, marker="o", linestyle="-", color="royalblue", ax=ax)

# Tambahkan anotasi pada setiap titik
for x, y in zip(weather_counts.index, weather_counts.values):
    ax.text(x, y, f"{int(y)}", ha="center", va="bottom", fontsize=10, fontweight="bold")

ax.set_xlabel("Weather Condition")
ax.set_ylabel("Average Bike Rentals")
ax.set_title("Trend of Average Bike Rentals by Weather Condition")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.grid(True, linestyle="--", alpha=0.6)  # Grid lebih halus untuk visibilitas lebih baik

st.pyplot(fig)

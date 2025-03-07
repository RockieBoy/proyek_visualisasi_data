import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

main_data = pd.read_csv("dashboard/main_data.csv", parse_dates=["dteday"])

st.sidebar.header("Filter Rentang Tanggal")
start_date, end_date = st.sidebar.date_input(
    "Pilih Rentang Tanggal", [main_data["dteday"].min(), main_data["dteday"].max()],
    min_value=main_data["dteday"].min(),
    max_value=main_data["dteday"].max()
)
main_data_filtering = main_data[(main_data["dteday"] >= pd.Timestamp(start_date)) & (main_data["dteday"] <= pd.Timestamp(end_date))]

st.title("Dashboard Penyewa Sepeda 🚴‍♂️")

holiday_df = main_data_filtering[main_data_filtering['holiday'] == "Holiday"].copy()
holiday_df['dteday'] = holiday_df['dteday'].dt.strftime("%Y-%m-%d")

st.subheader("Jumlah Penyewa Sepeda pada Hari Libur")

if not holiday_df.empty:
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(data=holiday_df, x='dteday', y='Total', ax=ax, color='blue')
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Jumlah Penyewa")
    ax.set_title("Jumlah Penyewa Sepeda pada Hari Libur")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)

    st.pyplot(fig)
    
else :
    st.subheader("Tidak ada data, silahkan cari di rentang tanggal lainnya")


st.subheader("Perbandingan Penyewa Casual dan Registered")



if not main_data_filtering.empty:
    
    total_casual = main_data_filtering['casual'].sum()
    total_registered = main_data_filtering['registered'].sum()
    
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie([total_casual, total_registered], labels=['Casual', 'Registered'], autopct='%1.1f%%', colors=['skyblue', 'salmon'])
    ax.set_title("Perbandingan Penyewa Casual dan Registered")
    plt.legend(title="Kategori")
    st.pyplot(fig)

else :
    st.subheader("Tidak Ada Perbandingan Penyewa Casual dan Registered") 


st.subheader("Klastering") 

binning_cluster = [main_data["Total"].min(), main_data["Total"].quantile(0.33), main_data["Total"].quantile(0.66), main_data["Total"].max()]
labels = ["Rendah", "Sedang", "Tinggi"]

main_data["Klaster"] = pd.cut(main_data["Total"], bins=binning_cluster, labels=labels, include_lowest=True)

cluster_summary = main_data["Klaster"].value_counts().reset_index()
cluster_summary.columns = ["Kategori", "Jumlah Data"]

plt.figure(figsize=(10, 6))
sns.scatterplot(x=main_data.index, y=main_data["Total"], hue=main_data["Klaster"], style=main_data["Klaster"], markers={"Rendah": "o", "Sedang": "o", "Tinggi": "o"}, palette={"Rendah": "green", "Sedang": "orange", "Tinggi": "red"})

plt.xlabel("Index")
plt.ylabel("Total Penyewa Sepeda")
plt.title("Klastering Jumlah Penyewa Sepeda")
plt.legend(title="Klaster")
plt.show()
st.pyplot(plt)

st.caption('Made By Sean Andrianto 2025')
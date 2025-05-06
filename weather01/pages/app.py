import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="PM2.5 Choropleth Dashboard", layout="wide")
st.title("PM2.5 Choropleth Map (ระดับจังหวัด และ ระดับอำเภอ)")

# โหลด GeoJSON
@st.cache_data
def load_geojson(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

@st.cache_data
def load_data():
    df = pd.read_excel("pm25.xlsx")
    df.columns = df.columns.str.strip().str.replace('"', '', regex=False).str.lower()
    df = df.rename(columns={
        "province": "province_name",
        "district": "amphoe_name",
    })
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["province_name"] = df["province_name"].str.strip().str.replace('\xa0', '', regex=False)
    df["amphoe_name"] = df["amphoe_name"].str.strip().str.replace('\xa0', '', regex=False)
    return df


df = load_data()

# แยกวันที่/เวลา
df["date"] = df["timestamp"].dt.date
df["time"] = df["timestamp"].dt.time

# กำหนดช่วงเวลา
min_time = df["timestamp"].dt.time.min()
max_time = df["timestamp"].dt.time.max()

start_time, end_time = st.slider(
    "เลือกช่วงเวลา",
    min_value=min_time,
    max_value=max_time,
    value=(min_time, max_time),
    format="HH:mm:ss"
)

# กรองข้อมูลตามช่วงเวลา
filtered_df = df[
    (df["timestamp"].dt.time >= start_time) &
    (df["timestamp"].dt.time <= end_time)
]

# โหลด GeoJSON
province_geojson = load_geojson("gadm41_THA_1.json")  # จังหวัด
amphoe_geojson = load_geojson("gadm41_THA_2.json")    # อำเภอ

# เมนูเลือกระดับ
level = st.radio("เลือกระดับแผนที่", ["จังหวัด (Province)", "อำเภอ (Amphoe)"])

# เตรียมข้อมูลและเลือก GeoJSON ตามระดับ
if level == "จังหวัด (Province)":
    map_df = filtered_df.groupby("province_name", as_index=False)["components_pm2_5"].mean()
    geojson = province_geojson
    locations = "province_name"
    featureidkey = "properties.NAME_1"
else:
    map_df = filtered_df.groupby("amphoe_name", as_index=False)["components_pm2_5"].mean()
    geojson = amphoe_geojson
    locations = "amphoe_name"
    featureidkey = "properties.NAME_2"

# สร้าง Choropleth Map
fig = px.choropleth_mapbox(
    map_df,
    geojson=geojson,
    locations=locations,
    featureidkey=featureidkey,
    color="components_pm2_5",
    color_continuous_scale="YlOrRd",
    mapbox_style="carto-positron",
    zoom=5,
    center={"lat": 13.5, "lon": 100.5},
    opacity=0.6,
    labels={"components_pm2_5": "PM2.5"},
    hover_name=locations
)

st.plotly_chart(fig, use_container_width=True)

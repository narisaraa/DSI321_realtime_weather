import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import folium_static


st.set_page_config(page_title="MAP")

# โหลดข้อมูล
df = pd.read_excel("pm25.xlsx")


# --------- โหลดข้อมูล PM2.5 ---------
@st.cache_data
def load_data():
    # แก้ path ให้ถูกต้องตามเครื่องของคุณ
    df = pd.read_excel("pm25.xlsx")
    
    df.columns = df.columns.str.replace('"', '')

    df = df.dropna(subset=["lat", "lon", "pm2.5"])  # ใช้ชื่อใหม่    df
    df = df.rename(columns={"pm2.5": "pm25"})  # เปลี่ยนชื่อคอลัมน์
    # df
    return df

# --------- สีตามระดับค่าฝุ่น ---------
def get_color(pm25):
    if pm25 is None:
        return "gray"
    elif pm25 > 100:
        return "red"
    elif pm25 > 50:
        return "orange"
    elif pm25 > 25:
        return "yellow"
    else:
        return "green"
    
# --------- Main Streamlit App ---------
st.title("🌀 แผนที่ค่าฝุ่น PM2.5 ในประเทศไทย")

df = load_data()

# สร้างแผนที่ประเทศไทย
map_center = [13.736717, 100.523186]  # ตำแหน่งกลางประเทศไทย (กรุงเทพฯ)
m = folium.Map(location=map_center, zoom_start=6)

# วนลูปสร้าง marker บนแผนที่
for _, row in df.iterrows():
    color = get_color(row["pm25"])
    popup_text = f"""<b>จังหวัด:</b> {row['requested_province']}<br>
                     <b>อำเภอ:</b> {row['requested_amphoe']}<br>
                     <b>PM2.5:</b> {row['pm25']} µg/m³"""
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=7,
        color=color,
        fill=True,
        fill_opacity=0.7,
        popup=folium.Popup(popup_text, max_width=300)
    ).add_to(m)

folium_static(m)



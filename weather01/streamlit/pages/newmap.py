# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import json
# import plotly.graph_objects as go

# st.set_page_config(page_title="PM2.5 Choropleth Dashboard", layout="wide")
# st.title("PM2.5 Choropleth Map (ระดับจังหวัด และ ระดับอำเภอ)")


    
# # โหลด GeoJSON
# @st.cache_data
# def load_geojson(path):
#     with open(path, "r", encoding="utf-8") as f:
#         return json.load(f)

# @st.cache_data
# def load_data():
#     df = pd.read_excel("pm25.xlsx")
#     df.columns = df.columns.str.replace('"', '')
#     df = df.rename(columns={"province": "province_name", "district": "amphoe_name", "components_pm2_5": "pm25"})
#     # return df  # ✅ สำคัญ: ต้อง return

#     # แปลง timestamp เป็น datetime
#     df["timestamp"] = pd.to_datetime(df["timestamp"])
#     df["province_name"] = df["province_name"].str.strip().str.replace('"', '', regex=False).str.replace('\xa0', '', regex=False)
#     df["amphoe_name"] = df["amphoe_name"].str.strip().str.replace('"', '', regex=False).str.replace('\xa0', '', regex=False)
    
#     return df

# df = load_data()
# st.write(df)

# #อ่าน code อำเภอ
# df_code = pd.read_excel("codeamphoeexcel.xlsx")
# df_code = df_code.rename(columns={"amphoeEN":"amphoe_name"})
# st.write(df_code)
# df = pd.merge(
#     df,
#     df_code[["amphoe_name", "amphoe_id", "province_id"]],
#     on="amphoe_name",
#     how="left"  # ใช้ 'left' เพื่อคงข้อมูล df หลักไว้ทั้งหมด
# )

# st.write(df)


# # --- ตรวจสอบ GeoJSON และข้อมูล codeamphoe.csv ครอบคลุมอำเภอครบหรือไม่ ---

# # 1. โหลด GeoJSON (ระดับอำเภอ)
# amphoe_geojson = load_geojson("gadm41_THA_2.json")

# # 2. สร้างชุดรหัสอำเภอจาก GeoJSON (รหัสที่ใช้เชื่อมใน choropleth: CC_2)
# geo_amphoe_ids = set(
#     f["properties"]["CC_2"] for f in amphoe_geojson["features"]
# )

# # 3. สร้างชุดรหัสอำเภอจากไฟล์ codeamphoe.csv
# code_amphoe_ids = set(df_code["amphoe_id"].astype(str))  # แปลงเป็น str ให้เทียบได้

# # 4. ตรวจสอบอำเภอที่หายไป
# missing_in_geojson = code_amphoe_ids - geo_amphoe_ids
# missing_in_code = geo_amphoe_ids - code_amphoe_ids

# # 5. แสดงผลใน Streamlit
# st.subheader("🔍 ตรวจสอบความครบถ้วนของข้อมูลอำเภอ")
# col1, col2 = st.columns(2)
# with col1:
#     missing_names = [
#     feature["properties"]["NAME_2"]
#     for feature in amphoe_geojson["features"]
#     if feature["properties"]["CC_2"] in missing_in_geojson
# ]
    

# with col2:
#     st.write(f"✅ จำนวนอำเภอใน codeamphoe.csv: {len(code_amphoe_ids)}")
#     st.write(f"❌ อำเภอที่มีใน GeoJSON แต่ไม่มีใน codeamphoe.csv: {len(missing_in_code)}")
#     if missing_in_code:
#         st.write(sorted(missing_in_code))


    

# # ดึง amphoe_id จาก GeoJSON
# geojson_amphoe_ids = set(
#     f["properties"].get("CC_2", "").strip()
#     for f in amphoe_geojson["features"]
#     if f["properties"].get("CC_2", "").strip().isdigit()
# )


# st.write("❌ จำนวนแถวข้อมูล PM2.5 ที่หา amphoe_id ไม่เจอ:", df["amphoe_id"].isnull().sum())
# if df["amphoe_id"].isnull().sum() > 0:
#     st.dataframe(df[df["amphoe_id"].isnull()][["province_name", "amphoe_name"]])

#     # แยกวันที่/เวลา
# df["date"] = df["timestamp"].dt.date
# df["time"] = df["timestamp"].dt.time

# # กำหนดช่วงเวลา
# min_time = df["timestamp"].dt.time.min()
# max_time = df["timestamp"].dt.time.max()

# start_time, end_time = st.slider(
#     "เลือกช่วงเวลา",
#     min_value=min_time,
#     max_value=max_time,
#     value=(min_time, max_time),
#     format="HH:mm:ss"
# )

# # กรองข้อมูลตามช่วงเวลา
# filtered_df = df[
#     (df["timestamp"].dt.time >= start_time) &
#     (df["timestamp"].dt.time <= end_time)
# ]

# # ล้างเครื่องหมายคำพูด และเว้นวรรคพิเศษ
# df["province_name"] = df["province_name"].str.strip().str.replace('"', '', regex=False).str.replace('\xa0', '', regex=False)
# df["amphoe_name"] = df["amphoe_name"].str.strip().str.replace('"', '', regex=False).str.replace('\xa0', '', regex=False)



# # --- โหลด GeoJSON ---
# province_geojson = load_geojson("gadm41_THA_1.json")  # ระดับจังหวัด
# amphoe_geojson = load_geojson("gadm41_THA_2.json")    # ระดับอำเภอ


# # เมนูเลือกระดับ
# level = st.radio("เลือกระดับแผนที่", ["จังหวัด (Province)", "อำเภอ (Amphoe)"])

# # เลือก GeoJSON และเตรียมข้อมูลตามระดับ
# if level == "จังหวัด (Province)":
#     map_df = df.groupby("province_id", as_index=False)["pm25"].mean()
#     geojson = province_geojson
#     locations = "province_id"
#     featureidkey = "properties.CC_1"  # ตรวจสอบว่า GeoJSON มี NAME_1
# else:
#     map_df = df.groupby("amphoe_id", as_index=False)["pm25"].mean()
#     geojson = amphoe_geojson
#     locations = "amphoe_id"
#     featureidkey = "properties.CC_2"  # ตรวจสอบว่า GeoJSON มี NAME_2


# # แสดง Choropleth
# fig = px.choropleth_mapbox(
#     map_df,
#     geojson=geojson,
#     locations=locations,
#     featureidkey=featureidkey,
#     color="pm25",
#     color_continuous_scale="YlOrRd",
#     mapbox_style="carto-positron",
#     zoom=5,
#     center={"lat": 13.5, "lon": 100.5},
#     opacity=0.6,
#     labels={"pm25": "PM2.5"},
#     hover_name=locations
# )
# st.plotly_chart(fig, use_container_width=True)



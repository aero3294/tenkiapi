import streamlit as st
import httpx
import asyncio

# 天気コードの辞書
WEATHER_CODE_MAP = {
    0: "快晴 ☀️", 1: "おおむね晴れ 🌤️", 2: "晴れ時々曇り ⛅", 3: "曇り ☁️",
    45: "霧 🌫️", 48: "霧（氷結） 🌫️", 51: "弱い霧雨 🌧️", 53: "普通の霧雨 🌧️",
    55: "強い霧雨 🌧️", 61: "弱い雨 ☔", 63: "普通の雨 ☔", 65: "強い雨 ☔",
    71: "弱い雪 ❄️", 73: "普通の雪 ❄️", 75: "強い雪 ❄️", 95: "雷雨 ⚡"
}

st.title("東京23区の天気予報 ☀️")

# 東京23区の座標辞書（区役所付近の緯度経度）
WARD_COORDS = {
    "千代田区": (35.6938, 139.7530),
    "中央区": (35.6706, 139.7720),
    "港区": (35.6581, 139.7515),
    "新宿区": (35.6938, 139.7036),
    "文京区": (35.7080, 139.7522),
    "台東区": (35.7126, 139.7800),
    "墨田区": (35.7107, 139.8016),
    "江東区": (35.6729, 139.8172),
    "品川区": (35.6092, 139.7302),
    "目黒区": (35.6414, 139.6982),
    "大田区": (35.5614, 139.7161),
    "世田谷区": (35.6465, 139.6532),
    "渋谷区": (35.6640, 139.6982),
    "中野区": (35.7075, 139.6638),
    "杉並区": (35.6994, 139.6364),
    "豊島区": (35.7261, 139.7156),
    "北区": (35.7527, 139.7336),
    "荒川区": (35.7360, 139.7834),
    "板橋区": (35.7514, 139.7093),
    "練馬区": (35.7357, 139.6519),
    "足立区": (35.7752, 139.8046),
    "葛飾区": (35.7434, 139.8471),
    "江戸川区": (35.7066, 139.8686),
}

# 区を選択するプルダウン
selected_ward = st.selectbox("区を選択してください", list(WARD_COORDS.keys()))

# APIからデータを取得する関数
async def get_weather_data(lat: float, lon: float):
    # URLには降水確率を含めない（エラー回避のため）
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,precipitation_probability,weather_code"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()

# ボタンが押されたら実行
if st.button(f"{selected_ward}の天気を取得", type="primary"):
    lat, lon = WARD_COORDS[selected_ward]
    # データを取得
    data = asyncio.run(get_weather_data(lat, lon))
    
    # 辞書から値を取り出す
    c = data["current"]
    temp = c["temperature_2m"]
    humidity = c["relative_humidity_2m"]
    precipitation_probability = c["precipitation_probability"]
    code = c["weather_code"]
    
    st.write(f"## {selected_ward}の天気")
    st.write(f"### 天気: {WEATHER_CODE_MAP.get(code, '不明')}")
    st.write(f"### 気温: {temp}℃")
    st.write(f"### 湿度: {humidity}%")
    st.write(f"### 降水確率: {precipitation_probability}%")

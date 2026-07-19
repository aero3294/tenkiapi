import streamlit as st
import httpx
import asyncio

# 天気コードの辞書（元のコードからそのままコピー）
WEATHER_CODE_MAP = {
    0: "快晴 ☀️", 1: "おおむね晴れ 🌤️", 2: "晴れ時々曇り ⛅", 3: "曇り ☁️",
    45: "霧 🌫️", 48: "霧（氷結） 🌫️", 51: "弱い霧雨 🌧️", 53: "普通の霧雨 🌧️",
    55: "強い霧雨 🌧️", 61: "弱い雨 ☔", 63: "普通の雨 ☔", 65: "強い雨 ☔",
    71: "弱い雪 ❄️", 73: "普通の雪 ❄️", 75: "強い雪 ❄️", 95: "雷雨 ⚡"
}

st.title("東京の天気予報 🌤️")

# 天気取得処理
async def get_weather_data():
    open_meteo_url = "https://api.open-meteo.com/v1/forecast?latitude=35.6785&longitude=139.6823&current=temperature_2m,relative_humidity_2m,weather_code"
    async with httpx.AsyncClient() as client:
        response = await client.get(open_meteo_url)
    return response.json()

# ボタンを押したら天気を表示
if st.button("現在の東京の天気を取得", type="primary"):
    # 非同期処理を実行
    data = asyncio.run(get_weather_data())
    
    current_info = data["current"]
    temp = current_info["temperature_2m"]
    code = current_info["weather_code"]
    
    weather_text = WEATHER_CODE_MAP.get(code, f"その他（コード: {code}）")
    
    st.write(f"### 気温: {temp}℃")
    st.write(f"### 天気: {weather_text}")
    st.write(f"### 降水確率: {c['precipitation_probability']}%")
    st.write(f"### 湿度: {c['relative_humidity_2m']}%")

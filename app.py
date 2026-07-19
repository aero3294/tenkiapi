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

st.title("東京の天気予報 ☀️")

# APIからデータを取得する関数
async def get_weather_data():
    # URLには降水確率を含めない（エラー回避のため）
    url = "https://api.open-meteo.com/v1/forecast?latitude=35.6785&longitude=139.6823&current=temperature_2m,relative_humidity_2m,weather_code"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()

# ボタンが押されたら実行
if st.button("現在の東京の天気を取得", type="primary"):
    # データを取得
    data = asyncio.run(get_weather_data())
    
    # 辞書から値を取り出す
    c = data["current"]
    temp = c["temperature_2m"]
    humidity = c["relative_humidity_2m"]
    code = c["weather_code"]
    
    # 表示
    st.write(f"### 気温: {temp}℃")
    st.write(f"### 湿度: {humidity}%")
    st.write(f"### 天気: {WEATHER_CODE_MAP.get(code, '不明')}")

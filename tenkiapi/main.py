from fastapi import FastAPI
import uvicorn
import httpx

app = FastAPI()

# 天気コード（数字）を分かりやすい日本語の文字に変換する辞書
WEATHER_CODE_MAP = {
    0: "快晴 ☀️",
    1: "おおむね晴れ 🌤️", 2: "晴れ時々曇り ⛅", 3: "曇り ☁️",
    45: "霧 🌫️", 48: "霧（氷結） 🌫️",
    51: "弱い霧雨 🌧️", 53: "普通の霧雨 🌧️", 55: "強い霧雨 🌧️",
    61: "弱い雨 ☔", 63: "普通の雨 ☔", 65: "強い雨 ☔",
    71: "弱い雪 ❄️", 73: "普通の雪 ❄️", 75: "強い雪 ❄️",
    95: "雷雨 ⚡"
}

@app.get("/tokyo-weather")
async def get_tokyo_weather():
    # Open-MeteoのURL
    open_meteo_url = "https://api.open-meteo.com/v1/forecast?latitude=35.6785&longitude=139.6823&current=temperature_2m,weather_code"
    
    # 外部APIにお返事をもらいにいく
    async with httpx.AsyncClient() as client:
        response = await client.get(open_meteo_url)
        
    weather_data = response.json()
    
    # 必要なデータを引っこ抜く
    current_info = weather_data["current"]
    temperature = current_info["temperature_2m"]
    code = current_info["weather_code"]
    
    # 数字の天気コードを、日本語に翻訳する
    weather_text = WEATHER_CODE_MAP.get(code, f"その他（コード: {code}）")
    
    return {
        "status": "success",
        "location": "東京",
        "temperature": f"{temperature}℃",
        "weather": weather_text
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
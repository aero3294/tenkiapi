import streamlit as st
import httpx

# 画面のタイトルを設定
st.title("☀️ リアルタイム天気予報アプリ")
st.write("現在の天気を取得して表示します。")

# ボタンを配置
if st.button("東京の天気を取得する", type="primary"):
    # ボタンが押されたら、あなたの作ったFastAPI（8000番）にデータを頼みに行く
    try:
        with st.spinner("データを取得中..."):
            response = httpx.get("http://127.0.0.1:8000/tokyo-weather")
            data = response.json()
        
        # 成功したら画面にカード風に表示
        if data.get("status") == "success":
            st.balloons() # お祝いの風船を飛ばす演出！
            
            # 綺麗な枠で囲んで表示
            with st.container(border=True):
                st.subheader(f"📍 位置: {data['location']}")
                st.header(f"🌡️ 気温: {data['temperature']}")
                st.header(f"✨ 天気: {data['weather']}")
        else:
            st.error("データの取得に失敗しました。")
            
    except httpx.ConnectError:
        st.error("FastAPI（裏方サーバー）が起動していないようです！ターミナルで python main.py を実行してください。")
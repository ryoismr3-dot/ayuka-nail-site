import streamlit as st
import datetime
import base64
import os
import smtplib
from email.mime.text import MIMEText
import streamlit.components.v1 as components
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- スプレッドシートから設定を読み込む ---
def get_config():
    try:
        creds = ServiceAccountCredentials.from_json_keyfile_dict(
            st.secrets["gcp_service_account"], 
            ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        )
        gc = gspread.authorize(creds)
        sh = gc.open("AyukaNailConfig").sheet1
        data = sh.get_all_records()
        return {row['key']: row['value'] for row in data}
    except:
        return {'site_title': "Ayuka's Nail", 'welcome_message': 'ご予約お待ちしています'}

config = get_config()

# --- ページ設定 ---
st.set_page_config(page_title=config['site_title'], layout="wide", initial_sidebar_state="collapsed")

# --- カスタムCSS ---
st.markdown(f"""
    <style>
    header {{visibility: hidden !important;}}
    .stApp {{ background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 25%, #c2e9fb 50%, #e0c3fc 75%, #f6d365 100%); background-attachment: fixed; }}
    h1 {{ text-align: center; background: -webkit-linear-gradient(45deg, #ff7eb3, #7facfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 3rem; margin-bottom: 20px; }}
    .stButton > button {{ background: rgba(255, 255, 255, 0.4); border-radius: 30px; padding: 12px 28px; transition: all 0.4s; }}
    .stButton > button:hover {{ background: rgba(255, 255, 255, 0.9); color: #ff7eb3; }}
    .stTextInput input, .stDateInput input {{ background-color: rgba(255,255,255,0.8); border-radius: 10px; }}
    </style>
""", unsafe_allow_html=True)

# --- ページ切り替え用 ---
if 'page' not in st.session_state: st.session_state.page = 'login'

# --- ページごとの処理 ---
if st.session_state.page == 'login':
    st.markdown(f"<h1>{config['site_title']}</h1>", unsafe_allow_html=True)
    password = st.text_input("Password", type="password", placeholder="パスワードを入力")
    if st.button("LOG IN"):
        if password == "1234":
            st.session_state.page = 'home'
            st.rerun()

elif st.session_state.page == 'home':
    st.markdown(f"<h1>Welcome</h1>", unsafe_allow_html=True)
    st.write(f"<p style='text-align:center;'>{config['welcome_message']}</p>", unsafe_allow_html=True)
    if st.button("📅 ネイルの予約へ"): st.session_state.page = 'reserve'; st.rerun()
    if st.button("📸 ギャラリーへ"): st.session_state.page = 'gallery'; st.rerun()

elif st.session_state.page == 'reserve':
    st.markdown("<h1>🛍️ Reservation</h1>", unsafe_allow_html=True)
    # ここに以前の予約フォームのロジック（日付・メール送信）を記述
    if st.button("← ホームへ"): st.session_state.page = 'home'; st.rerun()

elif st.session_state.page == 'gallery':
    st.markdown("<h1>📸 Gallery</h1>", unsafe_allow_html=True)
    # ここに以前のギャラリー用コンポーネントを記述
    if st.button("← ホームへ"): st.session_state.page = 'home'; st.rerun()

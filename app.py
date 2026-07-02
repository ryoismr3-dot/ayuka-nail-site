import streamlit as st
import datetime
import smtplib
from email.mime.text import MIMEText
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- 1. スプレッドシート連携設定 ---
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

# --- 2. ページ設定 ---
st.set_page_config(page_title=config['site_title'], layout="wide", initial_sidebar_state="collapsed")

# --- 3. デザインCSS ---
st.markdown("""
    <style>
    header {visibility: hidden !important;}
    .stApp { background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 25%, #c2e9fb 50%, #e0c3fc 75%, #f6d365 100%); background-attachment: fixed; }
    h1 { text-align: center; color: white; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
    .stButton > button { background: rgba(255, 255, 255, 0.5); border-radius: 20px; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- 4. ページ遷移ロジック ---
if 'page' not in st.session_state: st.session_state.page = 'login'

# --- A. ログイン画面 ---
if st.session_state.page == 'login':
    st.markdown(f"<h1>{config['site_title']}</h1>", unsafe_allow_html=True)
    password = st.text_input("パスワードを入力", type="password")
    if st.button("ログイン"):
        if password == "1234":
            st.session_state.page = 'home'
            st.rerun()

# --- B. ホーム画面 ---
elif st.session_state.page == 'home':
    st.markdown(f"<h1>{config['welcome_message']}</h1>", unsafe_allow_html=True)
    if st.button("📅 予約フォームへ"): st.session_state.page = 'reserve'; st.rerun()
    if st.button("📸 ギャラリーへ"): st.session_state.page = 'gallery'; st.rerun()

# --- C. 予約フォーム ---
elif st.session_state.page == 'reserve':
    st.markdown("<h1>予約フォーム</h1>", unsafe_allow_html=True)
    name = st.text_input("お名前")
    date = st.date_input("希望日")
    if st.button("送信"):
        st.success(f"{name}様、{date}で仮予約を受け付けました！")
        # Gmail送信ロジックをここに追加可能
    if st.button("← 戻る"): st.session_state.page = 'home'; st.rerun()

# --- D. ギャラリー ---
elif st.session_state.page == 'gallery':
    st.markdown("<h1>ネイルギャラリー</h1>", unsafe_allow_html=True)
    # 例：以前の画像表示
    col1, col2 = st.columns(2)
    with col1: st.image("nail1.png")
    with col2: st.image("nail2.png")
    if st.button("← 戻る"): st.session_state.page = 'home'; st.rerun()

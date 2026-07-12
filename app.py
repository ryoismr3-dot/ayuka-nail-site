import streamlit as st
import datetime
import base64
import os
import smtplib
from email.mime.text import MIMEText
import streamlit.components.v1 as components
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

st.set_page_config(page_title="Ayuka's nail site", layout="wide", initial_sidebar_state="collapsed")

DATA_FILE = 'data.json'

def load_data():
    if not os.path.exists(DATA_FILE):
        return {"notice": {"text": "", "is_active": False}}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
        if "notice" not in data:
            return {"notice": {"text": "", "is_active": False}}
        return data

def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

site_data = load_data()

if 'page' not in st.session_state:
    st.session_state.page = 'login'

def change_page(page_name):
    st.session_state.page = page_name

st.markdown("""
    <style>
    div[data-baseweb="popover"] > div,
    div[data-baseweb="calendar"],
    ul[role="listbox"],
    div[role="listbox"] {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    div[data-baseweb="popover"] *,
    div[data-baseweb="calendar"] *,
    ul[role="listbox"] * {
        color: #000000 !important;
        background-color: #ffffff !important;
    }
    li[role="option"]:hover {
        background-color: #f0f0f0 !important;
    }
    header {visibility: hidden !important;}
    #MainMenu {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stDeployButton {display: none !important;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&family=Noto+Serif+JP:wght@300;400;500;600&display=swap');
    .stApp {
        background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 25%, #c2e9fb 50%, #e0c3fc 75%, #f6d365 100%);
        background-attachment: fixed;
        font-family: 'Montserrat', 'Noto Serif JP', serif !important;
    }
    p, div, span, label {
        color: #4a4a4a !important;
        text-shadow: 2px 2px 5px rgba(255,255,255,0.9);
        font-family: 'Montserrat', 'Noto Serif JP', serif !important;
        letter-spacing: 1px;
    }
    h1 {
        font-family: 'Montserrat', 'Noto Serif JP', serif !important;
        font-weight: 600 !important;
        text-align: center;
        background: -webkit-linear-gradient(45deg, #ff7eb3, #7facfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(2px 3px 4px rgba(255,255,255,0.8));
        letter-spacing: 2px;
        margin-bottom: 20px;
        font-size: 3.5rem;
    }
    .stButton > button {
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(8px);
        color: #555555 !important;
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 30px;
        padding: 12px 28px;
        transition: all 0.4s ease;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
    }
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.9);
        border-color: #ff7eb3;
        transform: translateY(-3px);
        color: #ff7eb3 !important;
    }
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.5);
        color: #333333 !important;
        border: 2px solid rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

if st.session_state.page == 'login':
    st.markdown("<h1 style='margin-top: 5vh;'>✨ Ayuka's Nail Site ✨</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        password = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Password")
        if st.button("LOG IN", use_container_width=True):
            if password == "1234":
                change_page('home')
                st.rerun()
            elif password == "0607":
                change_page('admin_dashboard')
                st.rerun()
            else:
                st.error("パスワードが違います。")

elif st.session_state.page == 'admin_dashboard':
    st.markdown("<h1>⚙️ Admin Dashboard</h1>", unsafe_allow_html=True)
    notice_text = st.text_area("お知らせ内容", value=site_data["notice"]["text"])
    is_active = st.toggle("お知らせを表示する", value=site_data["notice"]["is_active"])
    if st.button("💾 保存する"):
        site_data["notice"] = {"text": notice_text, "is_active": is_active}
        save_data(site_data)
        st.success("保存しました！")
    if st.button("← ログアウト"):
        change_page('login')
        st.rerun()

elif st.session_state.page == 'home':
    notice = site_data["notice"]
    if notice["is_active"] and notice["text"]:
        st.toast(f"📢 {notice['text']}", icon="🔔")
        st.info(f"**【お知らせ】**\n\n{notice['text']}")
    st.markdown("<h1>Welcome to Ayuka's Nail</h1>", unsafe_allow_html=True)
    if st.button("📅 ネイルの予約へ", use_container_width=True):
        change_page('reserve')
        st.rerun()
    if st.button("📸 ギャラリーへ", use_container_width=True):
        change_page('gallery')
        st.rerun()

elif st.session_state.page == 'reserve':
    st.markdown("<h1>📅 Reservation</h1>", unsafe_allow_html=True)
    today = datetime.date.today()
    max_date = today + datetime.timedelta(days=30)
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

    @st.cache_data(ttl=60)
    def get_available_times(selected_date):
        try:
            creds_json = st.secrets["google_credentials"]
            creds_dict = json.loads(creds_json)
            creds = service_account.Credentials.from_service_account_info(
                creds_dict, scopes=['https://www.googleapis.com/auth/calendar.readonly']
            )
            service = build('calendar', 'v3', credentials=creds)
            calendar_id = st.secrets["calendar"]["id"]
            events_result = service.events().list(
                calendarId=calendar_id, timeMin=datetime.datetime.combine(selected_date, datetime.time.min, tzinfo=JST).isoformat(),
                timeMax=datetime.datetime.combine(selected_date, datetime.time.max, tzinfo=JST).isoformat(),
                singleEvents=True, orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])
            
            available_slots = []
            day_block_start = None
            day_block_end = None
            is_all_day = False
            for event in events:
                start_str = event['start'].get('dateTime', event['start'].get('date'))
                end_str = event['end'].get('dateTime', event['end'].get('date'))
                if len(start_str) == 10:
                    is_all_day = True
                    break
                event_start = datetime.datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                event_end = datetime.datetime.fromisoformat(end_str.replace('Z', '+00:00'))
                if day_block_start is None or event_start < day_block_start: day_block_start = event_start
                if day_block_end is None or event_end > day_block_end: day_block_end = event_end

            current_dt = datetime.datetime.combine(selected_date, datetime.time(8, 0), tzinfo=JST)
            end_dt = datetime.datetime.combine(selected_date, datetime.time(22, 0), tzinfo=JST)
            while current_dt <= end_dt:
                slot_start = current_dt
                slot_end = slot_start + datetime.timedelta(hours=1)
                is_overlap = False
                if is_all_day:
                    is_overlap = True
                elif day_block_start and day_block_end:
                    cutoff_time = day_block_start - datetime.timedelta(hours=2, minutes=30)
                    buffered_block_end = day_block_end + datetime.timedelta(minutes=30)
                    if slot_start > cutoff_time and slot_start < buffered_block_end:
                        is_overlap = True
                if not is_overlap:
                    available_slots.append(slot_start.strftime("%H:%M"))
                current_dt += datetime.timedelta(minutes=30)
            return available_slots
        except:
            return []

    menu = st.radio("メニュー", ["ハンドネイル", "フットネイル"], horizontal=True)
    date_1 = st.date_input("日付", today, min_value=today, max_value=max_date)
    time_1 = st.selectbox("時間", get_available_times(date_1) or ["現在、空きがありません"])
    name = st.text_input("お名前")
    email = st.text_input("メールアドレス")
    
    if st.button("予約を確定する"):
        if not name or not email:
            st.warning("入力してください。")
        else:
            try:
                sender_email = "ayukanail.reserve@gmail.com"
                sender_password = "latdmqbxcjhpdqvt" 
                recipient = "ismr3.ryo@gmail.com"
                msg = MIMEText(f"お名前: {name}\nメニュー: {menu}\n日時: {date_1} {time_1}")
                msg["Subject"] = "仮予約申し込み"
                msg["From"] = sender_email
                msg["To"] = recipient
                msg["Cc"] = "mmirukoko@gmail.com"
                
                with smtplib.SMTP_SSL("smtp.gmail.com", 465) as s:
                    s.login(sender_email, sender_password)
                    s.sendmail(sender_email, [recipient, "mmirukoko@gmail.com"], msg.as_string())
                st.success("送信しました！")
            except Exception as e:
                st.error(f"エラー: {e}")

elif st.session_state.page == 'gallery':
    st.markdown("<h1>📸 Gallery</h1>", unsafe_allow_html=True)
    if st.button("← ホームへ"):
        change_page('home')
        st.rerun()

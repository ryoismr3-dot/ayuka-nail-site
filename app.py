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

# --- ページ全体の設定 ---
st.set_page_config(page_title="Ayuka's nail site", layout="wide", initial_sidebar_state="collapsed")

# --- データ管理用の関数（手動カレンダーが不要になったため、お知らせのみ保存） ---
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

# --- カスタムCSS ---
st.markdown("""
    <style>
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
    h2, h3 {
        color: #6a82fb !important;
        text-shadow: 2px 2px 4px rgba(255,255,255,0.9);
    }
    .stButton > button {
        background: rgba(255, 255, 255, 0.4);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
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
        box-shadow: 0 8px 25px rgba(255,126,179,0.3);
        color: #ff7eb3 !important;
    }
    .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.5);
        color: #333333 !important;
        border: 2px solid rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.05);
        padding: 10px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #ff7eb3;
        box-shadow: 0 0 10px rgba(255, 126, 179, 0.3);
    }
    button span {
        font-family: 'Material Symbols Rounded', 'Material Icons', sans-serif !important;
        text-shadow: none !important;
        letter-spacing: normal !important;
        color: #777777 !important;
    }
    div[data-baseweb="popover"] > div {
        background-color: #ffffff !important;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15) !important;
    }
    div[data-baseweb="calendar"] *, ul[role="listbox"] * {
        color: #333333 !important;
        text-shadow: none !important;
    }

    @media (max-width: 768px) {
        h1 { font-size: 2.2rem !important; margin-top: 2vh !important; }
        .block-container { padding-top: 2rem !important; }
    }
    </style>
""", unsafe_allow_html=True)


# ==========================================
# ページ1：ログイン画面
# ==========================================
if st.session_state.page == 'login':
    st.markdown("<h1 style='margin-top: 5vh;'>✨ Ayuka's Nail Site ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Please enter your password</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        password = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Password")
        st.write("")
        if st.button("LOG IN", use_container_width=True):
            if password == "1234":
                change_page('home')
                st.rerun()
            elif password == "0607":
                change_page('admin_dashboard')
                st.rerun()
            else:
                st.error("パスワードが違います。")

# ==========================================
# ページ2：管理者ダッシュボード
# ==========================================
elif st.session_state.page == 'admin_dashboard':
    st.markdown("<h1>⚙️ Admin Dashboard</h1>", unsafe_allow_html=True)
    st.info("💡 カレンダーの〇×管理は自動化されたため、ここでの手動設定は不要になりました！予定の変更はCahoカレンダーで行ってください。")
    
    st.markdown("### 📢 お知らせ（ポップアップ）設定")
    notice_text = st.text_area("お知らせ内容", value=site_data["notice"]["text"])
    is_active = st.toggle("お知らせをユーザーサイトに表示する", value=site_data["notice"]["is_active"])
    
    if st.button("💾 お知らせを保存する", use_container_width=True):
        site_data["notice"] = {"text": notice_text, "is_active": is_active}
        save_data(site_data)
        st.success("お知らせ設定を保存しました！")

    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    if st.button("← ログアウト"):
        change_page('login')
        st.rerun()

# ==========================================
# ページ3：ホーム画面
# ==========================================
elif st.session_state.page == 'home':
    notice = site_data["notice"]
    if notice["is_active"] and notice["text"]:
        st.toast(f"📢 お知らせ: {notice['text']}", icon="🔔") 
        st.info(f"**【お知らせ】**\n\n{notice['text']}") 

    st.markdown("<h1 style='margin-top: 2vh;'>Welcome to Ayuka's Nail</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.1rem;'>ご希望のメニューを選択してください</p>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📅 ネイルの予約へ", use_container_width=True):
        change_page('reserve')
        st.rerun()
    st.write("")
    if st.button("📸 参考画像ギャラリーへ", use_container_width=True):
        change_page('gallery')
        st.rerun()

# ==========================================
# ページ4：予約画面（Googleカレンダー自動連携）
# ==========================================
elif st.session_state.page == 'reserve':
    st.markdown("<h1>📅 Reservation</h1>", unsafe_allow_html=True)
    st.write("ご希望の日にちと時間を、第三希望まで入力してください。（本日より1ヶ月先まで選択可能です）")
    st.markdown("<br>", unsafe_allow_html=True)

    today = datetime.date.today()
    max_date = today + datetime.timedelta(days=30) 
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

    @st.cache_data(ttl=60) # 1分間データを記憶して読み込みを高速化
    def get_available_times(selected_date):
        try:
            creds_json = st.secrets["google_credentials"]
            creds_dict = json.loads(creds_json)
            creds = service_account.Credentials.from_service_account_info(
                creds_dict, scopes=['https://www.googleapis.com/auth/calendar.readonly']
            )
            service = build('calendar', 'v3', credentials=creds)
            calendar_id = st.secrets["calendar"]["id"]

            time_min = datetime.datetime.combine(selected_date, datetime.time.min, tzinfo=JST).isoformat()
            time_max = datetime.datetime.combine(selected_date, datetime.time.max, tzinfo=JST).isoformat()

            events_result = service.events().list(
                calendarId=calendar_id, timeMin=time_min, timeMax=time_max,
                singleEvents=True, orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])

            available_slots = []
            for hour in range(8, 21):
                slot_start = datetime.datetime.combine(selected_date, datetime.time(hour, 0), tzinfo=JST)
                slot_end = slot_start + datetime.timedelta(hours=1)
                is_overlap = False

                for event in events:
                    start_str = event['start'].get('dateTime', event['start'].get('date'))
                    end_str = event['end'].get('dateTime', event['end'].get('date'))

                    if len(start_str) == 10:
                        is_overlap = True
                        break

                    if start_str.endswith('Z'): start_str = start_str[:-1] + '+00:00'
                    if end_str.endswith('Z'): end_str = end_str[:-1] + '+00:00'
                    
                    event_start = datetime.datetime.fromisoformat(start_str)
                    event_end = datetime.datetime.fromisoformat(end_str)

                    if slot_start < event_end and slot_end > event_start:
                        is_overlap = True
                        break

                if not is_overlap:
                    available_slots.append(f"{hour:02d}:00")

            return available_slots
        except Exception as e:
            st.error(f"⚠️ カレンダーの読み込みに失敗しました。設定を確認してください。({e})")
            return []

    st.markdown("**💅 第一希望**")
    col1, col2 = st.columns(2)
    with col1: date_1 = st.date_input("日付 (第一希望)", today, min_value=today, max_value=max_date, key="date1")
    with col2: 
        times_1 = get_available_times(date_1)
        time_1 = st.selectbox("時間 (第一希望)", times_1 if times_1 else ["現在、空きがありません"], key="time1")

    st.markdown("**💅 第二希望**")
    col3, col4 = st.columns(2)
    default_date_2 = today + datetime.timedelta(days=1) if (today + datetime.timedelta(days=1)) <= max_date else max_date
    with col3: date_2 = st.date_input("日付 (第二希望)", default_date_2, min_value=today, max_value=max_date, key="date2")
    with col4: 
        times_2 = get_available_times(date_2)
        time_2 = st.selectbox("時間 (第二希望)", times_2 if times_2 else ["現在、空きがありません"], key="time2")

    st.markdown("**💅 第三希望**")
    col5, col6 = st.columns(2)
    default_date_3 = today + datetime.timedelta(days=2) if (today + datetime.timedelta(days=2)) <= max_date else max_date
    with col5: date_3 = st.date_input("日付 (第三希望)", default_date_3, min_value=today, max_value=max_date, key="date3")
    with col6: 
        times_3 = get_available_times(date_3)
        time_3 = st.selectbox("時間 (第三希望)", times_3 if times_3 else ["現在、空きがありません"], key="time3")

    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.write("お客様情報をご入力ください。")
    customer_name = st.text_input("お名前")
    customer_email = st.text_input("メールアドレス")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("予約を確定する", use_container_width=True):
        if not customer_name or not customer_email:
            st.warning("⚠️ お名前とメールアドレスを入力してください。")
        elif "現在、空きがありません" in [time_1, time_2, time_3]:
            st.warning("⚠️ 空きのない時間帯が選択されています。別の日時を選択してください。")
        else:
            try:
                sender_email = st.secrets["email"]["address"]
                sender_password = st.secrets["email"]["password"]

                subject = "【Ayuka's Nail】仮予約を受け付けました"
                body = f"""{customer_name} 様\n\nAyuka's Nailをご利用いただきありがとうございます。\n以下の内容で仮予約を受け付けました。\n\n========================\n【第一希望】 {date_1.strftime('%Y年%m月%d日')} {time_1}\n【第二希望】 {date_2.strftime('%Y年%m月%d日')} {time_2}\n【第三希望】 {date_3.strftime('%Y年%m月%d日')} {time_3}\n========================\n\n※現在「仮予約」の状態です。\n日程を調整のうえ、後ほど確定のご連絡をいたします。\n\nAyuka's Nail"""
                msg = MIMEText(body)
                msg["Subject"] = subject
                msg["From"] = sender_email
                msg["To"] = customer_email
                msg["Bcc"] = "mmirukoko@gmail.com"

                server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                server.login(sender_email, sender_password)
                server.send_message(msg)
                server.quit()
                st.success("🎉 仮予約を受け付けました。ご入力いただいたメールアドレスに確認メールを送信しました！")
            except Exception as e:
                st.error("メールの送信に失敗しました。管理者のメール設定（Secrets）を確認してください。")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← ホームに戻る"):
        change_page('home')
        st.rerun()

# ==========================================
# ページ5：ギャラリー
# ==========================================
elif st.session_state.page == 'gallery':
    st.markdown("<h1>📸 Gallery</h1>", unsafe_allow_html=True)
    st.write("最新のネイルデザイン。（スマホでは指でスワイプして動かせます）")

    def get_swiper_html():
        slides_html = ""
        for i in range(1, 10):
            file_name = f"nail{i}.png"
            if os.path.exists(file_name):
                with open(file_name, "rb") as image_file:
                    encoded = base64.b64encode(image_file.read()).decode()
                    img_src = f"data:image/png;base64,{encoded}"
            else:
                img_src = f"https://via.placeholder.com/200x250/ffffff/ff7eb3?text=Nail+{i}"
            slides_html += f'<div class="swiper-slide"><img src="{img_src}"></div>'

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.css" />
            <style>
                body {{ margin: 0; padding: 0; background: transparent; overflow: hidden; }}
                .swiper {{ width: 100%; padding: 20px 0; }}
                .swiper-wrapper {{ transition-timing-function: linear !important; }}
                .swiper-slide {{ width: auto; display: flex; justify-content: center; align-items: center; }}
                .swiper-slide img {{ height: 250px; object-fit: cover; border-radius: 15px; box-shadow: 0 8px 20px rgba(0,0,0,0.15); }}
                @media (max-width: 768px) {{ .swiper-slide img {{ height: 180px; }} }}
            </style>
        </head>
        <body>
            <div class="swiper mySwiper"><div class="swiper-wrapper">{slides_html}</div></div>
            <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
            <script>
                const swiper = new Swiper('.mySwiper', {{
                    loop: true, slidesPerView: 'auto', spaceBetween: 20, speed: 6000, allowTouchMove: true,
                    autoplay: {{ delay: 0, disableOnInteraction: false }},
                }});
            </script>
        </body>
        </html>
        """
        return html_content

    components.html(get_swiper_html(), height=300)

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("← ホームに戻る"):
        change_page('home')
        st.rerun()

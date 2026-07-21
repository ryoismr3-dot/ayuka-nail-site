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
    
    @media (max-width: 768px) {
        h1 { font-size: 2.2rem !important; margin-top: 2vh !important; }
        .block-container { 
            padding-top: 1rem !important;
            padding-left: 2px !important;
            padding-right: 2px !important;
        }
    }

    /* ---------------------------------------------------
       カレンダーを「絶対に」1画面に収めるパーセンテージ固定設定
    --------------------------------------------------- */
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        width: 100% !important;
        max-width: 100vw !important;
        overflow-x: hidden !important; 
        gap: 0 !important; 
        padding-bottom: 5px !important;
    }
    
    /* 列が内部コンテンツによって広がらないようにする最強のロック */
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) > div[data-testid="column"] {
        min-width: 0 !important; 
        padding: 0 1px !important;
        overflow: hidden !important; 
    }
    
    /* 1列目（時間）は画面幅の16%に完全固定 */
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) > div[data-testid="column"]:first-child {
        width: 16% !important; 
        max-width: 16% !important;
        flex: 0 0 16% !important; 
        background: rgba(255,255,255,0.4);
        border-radius: 4px;
    }

    /* 2〜8列目（7日間）はそれぞれ画面幅の12%に完全固定（12×7 = 84% + 16% = 100%） */
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) > div[data-testid="column"]:not(:first-child) {
        width: 12% !important; 
        max-width: 12% !important;
        flex: 0 0 12% !important; 
    }

    /* 〇×ボタンの設定 */
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) .stButton > button {
        background: rgba(255, 255, 255, 0.8) !important;
        backdrop-filter: none !important;
        color: #ff7eb3 !important;
        border: 1px solid rgba(255, 126, 179, 0.8) !important;
        border-radius: 4px !important;
        padding: 0 !important;
        margin: 0 !important;
        height: 32px !important;
        min-height: 32px !important;
        width: 100% !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-shadow: none !important;
        transform: none !important;
    }
    
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) .stButton > button p {
        font-size: 14px !important;
        line-height: 1 !important;
        margin: 0 !important;
    }
    
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) .stButton > button:hover:not(:disabled) {
        background: #ff7eb3 !important;
        color: white !important;
    }
    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) .stButton > button:disabled {
        background: rgba(220, 220, 220, 0.4) !important;
        color: #999 !important;
        border: 1px solid rgba(200, 200, 200, 0.3) !important;
    }

    div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) div[data-testid="stButton"] {
        height: 32px !important;
        min-height: 32px !important;
        margin-bottom: 2px !important;
    }
    
    /* 時間と曜日のテキスト設定 */
    .time-label {
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 11px !important; 
        color: #555;
        margin: 0 !important;
        margin-bottom: 2px !important;
        letter-spacing: -0.5px;
        white-space: nowrap !important;
    }
    
    .header-label {
        height: 35px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        font-weight: bold;
        font-size: 11px !important; 
        color: #555;
        margin: 0 !important;
        margin-bottom: 4px !important;
        line-height: 1.1;
        white-space: nowrap !important;
    }

    /* スマホ向けさらに縮小設定 */
    @media (max-width: 400px) {
        .time-label { font-size: 9px !important; }
        .header-label { font-size: 9px !important; }
        div[data-testid="stHorizontalBlock"]:has(> div:nth-child(8)) .stButton > button p {
            font-size: 11px !important;
        }
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

elif st.session_state.page == 'admin_dashboard':
    st.markdown("<h1>⚙️ Admin Dashboard</h1>", unsafe_allow_html=True)
    
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

elif st.session_state.page == 'reserve':
    st.markdown("<h1>📅 Reservation</h1>", unsafe_allow_html=True)
    
    if "week_offset" not in st.session_state:
        st.session_state.week_offset = 0
    if "selected_datetime" not in st.session_state:
        st.session_state.selected_datetime = None

    today = datetime.date.today()
    JST = datetime.timezone(datetime.timedelta(hours=+9), 'JST')

    @st.cache_data(ttl=60)
    def get_week_availability(start_date):
        try:
            try:
                creds_json = st.secrets["calendar"]["google_credentials"]
                calendar_id = st.secrets["calendar"]["id"]
            except KeyError:
                creds_json = st.secrets["google_credentials"]
                calendar_id = st.secrets["calendar_id"]

            creds_dict = json.loads(creds_json)
            creds = service_account.Credentials.from_service_account_info(
                creds_dict, scopes=['https://www.googleapis.com/auth/calendar.readonly']
            )
            service = build('calendar', 'v3', credentials=creds)

            time_min = datetime.datetime.combine(start_date, datetime.time.min, tzinfo=JST).isoformat()
            time_max = datetime.datetime.combine(start_date + datetime.timedelta(days=7), datetime.time.max, tzinfo=JST).isoformat()

            events_result = service.events().list(
                calendarId=calendar_id, timeMin=time_min, timeMax=time_max,
                singleEvents=True, orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])

            available_dict = {}
            now_jst = datetime.datetime.now(JST)

            for i in range(7):
                target_date = start_date + datetime.timedelta(days=i)
                target_start = datetime.datetime.combine(target_date, datetime.time.min, tzinfo=JST)
                target_end = datetime.datetime.combine(target_date, datetime.time.max, tzinfo=JST)

                day_block_start = None
                day_block_end = None
                is_all_day = False

                for event in events:
                    start_str = event['start'].get('dateTime', event['start'].get('date'))
                    end_str = event['end'].get('dateTime', event['end'].get('date'))

                    if len(start_str) == 10:
                        ev_start = datetime.datetime.strptime(start_str, "%Y-%m-%d").date()
                        ev_end = datetime.datetime.strptime(end_str, "%Y-%m-%d").date()
                        if ev_start <= target_date < ev_end:
                            is_all_day = True
                        continue

                    if start_str.endswith('Z'): start_str = start_str[:-1] + '+00:00'
                    if end_str.endswith('Z'): end_str = end_str[:-1] + '+00:00'
                    
                    event_start = datetime.datetime.fromisoformat(start_str)
                    event_end = datetime.datetime.fromisoformat(end_str)

                    if event_start <= target_end and event_end >= target_start:
                        if day_block_start is None or event_start < day_block_start:
                            day_block_start = event_start
                        if day_block_end is None or event_end > day_block_end:
                            day_block_end = event_end

                current_dt = datetime.datetime.combine(target_date, datetime.time(8, 0), tzinfo=JST)
                end_dt = datetime.datetime.combine(target_date, datetime.time(22, 0), tzinfo=JST)
                slots = []

                while current_dt <= end_dt:
                    slot_start = current_dt
                    slot_end = slot_start + datetime.timedelta(hours=1)
                    is_overlap = False

                    if slot_start < now_jst:
                        is_overlap = True
                    elif is_all_day:
                        is_overlap = True
                    elif day_block_start and day_block_end:
                        cutoff_time = day_block_start - datetime.timedelta(hours=2, minutes=30)
                        buffered_block_end = day_block_end + datetime.timedelta(minutes=30)
                        if slot_start > cutoff_time and slot_start < buffered_block_end:
                            is_overlap = True

                    if not is_overlap:
                        slots.append(slot_start.strftime("%H:%M"))
                    
                    current_dt += datetime.timedelta(minutes=30)
                
                available_dict[target_date] = slots
            return available_dict
        except Exception as e:
            return None

    st.markdown("**💅 ご希望のメニュー**")
    menu_choice = st.radio("施術箇所", ["ハンドネイル (手)", "フットネイル (足)", "ハンド＆フット (両方)"], horizontal=True, label_visibility="collapsed")

    st.markdown("**💅 オフの有無**")
    off_choice = st.radio("オフ", ["オフあり", "オフなし"], horizontal=True, label_visibility="collapsed")

    st.markdown("<br>### 📅 日時を選択", unsafe_allow_html=True)
    
    col_p, col_c, col_n = st.columns([1, 2, 1])
    with col_p:
        if st.button("← 前の週", use_container_width=True):
            st.session_state.week_offset -= 7
            st.rerun()
    with col_c:
        current_view_date = today + datetime.timedelta(days=st.session_state.week_offset)
        st.markdown(f"<h4 style='text-align:center; margin-top:5px;'>{current_view_date.strftime('%Y年%m月')}</h4>", unsafe_allow_html=True)
    with col_n:
        if st.button("次の週 →", use_container_width=True):
            st.session_state.week_offset += 7
            st.rerun()

    availability = get_week_availability(current_view_date)

    if availability is None:
        st.error("⚠️ カレンダーの読み取りに失敗しました。Googleカレンダーの共有設定を確認してください。")
    else:
        weekdays = ["月", "火", "水", "木", "金", "土", "日"]
        times = [(datetime.datetime.combine(today, datetime.time(8,0)) + datetime.timedelta(minutes=30*i)).strftime("%H:%M") for i in range(29)]
        
        cols = st.columns(8)
        
        with cols[0]:
            st.markdown("<div class='header-label'>時間</div>", unsafe_allow_html=True)
            for t in times:
                st.markdown(f"<div class='time-label'>{t}</div>", unsafe_allow_html=True)
                
        for i in range(7):
            d = current_view_date + datetime.timedelta(days=i)
            with cols[i+1]:
                st.markdown(f"<div class='header-label'>{d.day}<br><span style='font-size:0.8em;'>{weekdays[d.weekday()]}</span></div>", unsafe_allow_html=True)
                for t in times:
                    if t in availability[d]:
                        if st.button("〇", key=f"btn_{d.isoformat()}_{t}", use_container_width=True):
                            st.session_state.selected_datetime = (d, t)
                            st.rerun()
                    else:
                        st.button("×", key=f"btn_{d.isoformat()}_{t}", disabled=True, use_container_width=True)

    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    st.markdown("### 📝 お客様情報の入力")

    if st.session_state.selected_datetime:
        sel_d, sel_t = st.session_state.selected_datetime
        st.success(f"✅ 選択中の日時: **{sel_d.strftime('%Y年%m月%d日')} {sel_t}**")
        
        customer_name = st.text_input("お名前")
        customer_email = st.text_input("メールアドレス")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("予約を確定する", use_container_width=True):
            if not customer_name or not customer_email:
                st.warning("⚠️ お名前とメールアドレスを入力してください。")
            else:
                try:
                    sender_email = "ayukanail.reserve@gmail.com"
                    sender_password = "fibpjgqxaabhohsc"

                    subject = "【Ayuka's Nail】仮予約を受け付けました"
                    body = f"{customer_name} 様\n\nAyuka's Nailをご利用いただきありがとうございます。\n以下の内容で仮予約を受け付けました。\n\n========================\n【ご希望メニュー】 {menu_choice}\n【オフの有無】 {off_choice}\n【ご希望日時】 {sel_d.strftime('%Y年%m月%d日')} {sel_t}\n========================\n\n※現在「仮予約」の状態です。\n日程を調整のうえ、後ほど確定のご連絡をいたします。\n\nAyuka's Nail"
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
                    st.session_state.selected_datetime = None 
                except Exception as e:
                    st.error(f"メールの送信に失敗しました。管理者のメール設定を確認してください。")
    else:
        st.info("👆 上の表から「〇」をクリックして、ご希望の日時を選択してください。")

    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("← ホームに戻る"):
        change_page('home')
        st.rerun()

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

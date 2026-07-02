import streamlit as st
import datetime
import base64
import os
import smtplib
from email.mime.text import MIMEText
import streamlit.components.v1 as components

# --- ページ全体の設定 ---
st.set_page_config(page_title="Ayuka's nail site", layout="wide", initial_sidebar_state="collapsed")

# --- カスタムCSS（安全な修正版） ---
st.markdown("""
    <style>
    /* ==========================================
       Streamlitロゴやヘッダーを【安全に】非表示にする
       ========================================== */
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    /* サイト本体を消さずに右下バッジだけを狙い撃ちにする */
    .viewerBadge_container__1QSob, 
    .viewerBadge_link__1S137, 
    a[href^="https://streamlit.io/cloud"] {
        display: none !important;
    }
    
    /* ==========================================
       オリジナルデザイン設定
       ========================================== */
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600&family=Noto+Serif+JP:wght@300;400;500;600&display=swap');
    
    .stApp { 
        background: linear-gradient(135deg, #fbc2eb 0%, #a6c1ee 25%, #c2e9fb 50%, #e0c3fc 75%, #f6d365 100%); 
        background-attachment: fixed; 
        font-family: 'Montserrat', 'Noto Serif JP', serif !important; 
    }
    
    p, label { 
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
        color: #ff7eb3 !important; 
    }
    
    /* ==========================================
       時間の文字を強制的に【白】にする設定
       ========================================== */
    .stTextInput > div > div > input,
    .stDateInput > div > div > input,
    div[data-baseweb="select"] > div { 
        background-color: rgba(40, 40, 40, 0.9) !important; 
        border: 1px solid rgba(255, 255, 255, 0.4) !important; 
        border-radius: 10px !important; 
        padding: 10px !important;
    }
    
    /* 時間の文字色（スマホでも絶対に見えるように指定） */
    .stTextInput > div > div > input,
    .stDateInput > div > div > input,
    div[data-baseweb="select"] * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        opacity: 1 !important;
        text-shadow: none !important;
    }

    /* カレンダーとドロップダウンメニューの背景 */
    ul[role="listbox"], div[data-baseweb="calendar"] {
        background-color: #333333 !important;
    }
    ul[role="listbox"] li {
        color: #ffffff !important;
        background-color: #333333 !important;
    }
    
    .st-emotion-cache-1wmy9hl { background-color: transparent !important; }
    
    @media (max-width: 768px) { 
        h1 { font-size: 2.2rem !important; margin-top: 2vh !important; } 
        .block-container { padding-top: 2rem !important; }
    }
    </style>
""", unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'login'

def change_page(page_name):
    st.session_state.page = page_name

# ==========================================
# ページ1：ログイン画面
# ==========================================
if st.session_state.page == 'login':
    st.markdown("<h1 style='margin-top: 5vh;'>✨ Ayuka's Nail Site ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Please enter your password</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 10, 1])
    with col2:
        st.write("")
        password = st.text_input("Password", type="password", label_visibility="collapsed", placeholder="Password")
        st.write("")
        if st.button("LOG IN", use_container_width=True):
            if password == "1234":
                change_page('home')
                st.rerun()
            else:
                st.error("パスワードが違います。")

# ==========================================
# ページ2：ホーム画面
# ==========================================
elif st.session_state.page == 'home':
    st.markdown("<h1 style='margin-top: 5vh;'>Welcome to Ayuka's Nail</h1>", unsafe_allow_html=True)
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
# ページ3：予約画面
# ==========================================
elif st.session_state.page == 'reserve':
    st.markdown("<h1>🛍️ Reservation</h1>", unsafe_allow_html=True)
    st.write("ご希望の日にちと時間を、第三希望まで入力してください。")
    st.markdown("<br>", unsafe_allow_html=True)
    
    time_options = [f"{hour:02d}:00" for hour in range(12, 21)]
    today = datetime.date.today()
    
    st.markdown("**💅 第一希望**")
    col1, col2 = st.columns(2)
    with col1: date_1 = st.date_input("日付 (第一希望)", today, key="date1")
    with col2: time_1 = st.selectbox("時間 (第一希望)", time_options, key="time1")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("**💅 第二希望**")
    col3, col4 = st.columns(2)
    with col3: date_2 = st.date_input("日付 (第二希望)", today + datetime.timedelta(days=1), key="date2")
    with col4: time_2 = st.selectbox("時間 (第二希望)", time_options, key="time2")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("**💅 第三希望**")
    col5, col6 = st.columns(2)
    with col5: date_3 = st.date_input("日付 (第三希望)", today + datetime.timedelta(days=2), key="date3")
    with col6: time_3 = st.selectbox("時間 (第三希望)", time_options, key="time3")

    st.markdown("<br><hr><br>", unsafe_allow_html=True)
    
    st.write("お客様情報をご入力ください。")
    customer_name = st.text_input("お名前")
    customer_email = st.text_input("メールアドレス")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("予約を確定する", use_container_width=True):
        if not customer_name or not customer_email:
            st.warning("⚠️ お名前とメールアドレスを入力してください。")
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
# ページ4：ギャラリー
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
            <div class="swiper mySwiper">
                <div class="swiper-wrapper">
                    {slides_html}
                </div>
            </div>
            <script src="https://cdn.jsdelivr.net/npm/swiper@11/swiper-bundle.min.js"></script>
            <script>
                const swiper = new Swiper('.mySwiper', {{
                    loop: true,                 
                    slidesPerView: 'auto',       
                    spaceBetween: 20,           
                    speed: 6000,                
                    allowTouchMove: true,       
                    autoplay: {{
                        delay: 0,               
                        disableOnInteraction: false, 
                    }},
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

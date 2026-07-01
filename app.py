import streamlit as st
import datetime
import base64
import os

# --- ページ全体の設定 ---
st.set_page_config(page_title="Ayuka's nail site", layout="wide", initial_sidebar_state="collapsed")

# --- カスタムCSS（明るいパステル、グラスモーフィズム、スマホ対応） ---
st.markdown("""
    <style>
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
        font-size: 3.5rem; /* PC用のサイズ */
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
        color: #333333;
        border: 2px solid rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        box-shadow: inset 0 2px 5px rgba(0,0,0,0.05);
        padding: 10px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #ff7eb3;
        box-shadow: 0 0 10px rgba(255, 126, 179, 0.3);
    }

    .marquee-wrapper {
        width: 100%;
        overflow: hidden;
        padding: 25px 0;
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.6);
        border-radius: 20px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.05);
    }
    .marquee-content {
        display: flex;
        width: max-content;
        animation: marquee 30s linear infinite;
    }
    .marquee-content img {
        height: 250px; /* PC用画像サイズ */
        object-fit: cover;
        margin: 0 15px;
        border-radius: 12px;
        box-shadow: 0 6px 15px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }
    .marquee-content img:hover {
        transform: scale(1.05);
    }
    .marquee-content:hover {
        animation-play-state: paused;
    }
    @keyframes marquee {
        0% { transform: translateX(0); }
        100% { transform: translateX(-50%); }
    }
    .st-emotion-cache-1wmy9hl { background-color: transparent !important; }

    /* ==========================================
       スマホ用のスタイル（画面幅が768px以下の場合に適用）
       ========================================== */
    @media (max-width: 768px) {
        h1 {
            font-size: 2.2rem !important; /* スマホではタイトルを小さく */
            margin-top: 2vh !important;
        }
        .marquee-content img {
            height: 180px; /* スマホでは画像サイズを少し小さく */
            margin: 0 8px;
        }
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
    st.markdown("<h1 style='margin-top: 10vh;'>✨ Ayuka's Nail Site ✨</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Please enter your password</p>", unsafe_allow_html=True)
    
    # スマホでも崩れないようにカラム設定を調整
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
    # スマホでボタンが縦に綺麗に並ぶように調整
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
    st.markdown("<h1>📅 Reservation</h1>", unsafe_allow_html=True)
    st.write("ご希望の日にちと時間を選択してください。")
    st.markdown("<br>", unsafe_allow_html=True)
    
    selected_date = st.date_input("日付を選択", datetime.date.today())
    time_options = [f"{hour:02d}:00" for hour in range(12, 21)]
    selected_time = st.selectbox("時間を選択", time_options)
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("予約を確定する", use_container_width=True):
        st.success(f"🎉 {selected_date.strftime('%Y年%m月%d日')} {selected_time} にて仮予約を受け付けました。")
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← ホームに戻る"):
        change_page('home')
        st.rerun()

# ==========================================
# ページ4：ギャラリー
# ==========================================
elif st.session_state.page == 'gallery':
    st.markdown("<h1>📸 Gallery</h1>", unsafe_allow_html=True)
    st.write("最新のネイルデザイン。")
    
    def get_image_tags():
        image_html = ""
        for i in range(1, 10):
            file_name = f"nail{i}.png"
            if os.path.exists(file_name):
                with open(file_name, "rb") as image_file:
                    encoded = base64.b64encode(image_file.read()).decode()
                    image_html += f'<img src="data:image/png;base64,{encoded}">'
            else:
                image_html += f'<img src="https://via.placeholder.com/200x250/ffffff/ff7eb3?text=Nail+{i}">'
        return image_html

    images_tags = get_image_tags()
    
    carousel_html = f"""
    <div class="marquee-wrapper">
        <div class="marquee-content">
            {images_tags}
            {images_tags}
        </div>
    </div>
    """
    
    st.markdown(carousel_html, unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    if st.button("← ホームに戻る"):
        change_page('home')
        st.rerun()

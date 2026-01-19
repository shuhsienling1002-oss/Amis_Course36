import streamlit as st
import time
import random
from io import BytesIO

# --- 1. 核心相容性修復 ---
def safe_rerun():
    """自動判斷並執行重整"""
    try:
        st.rerun()
    except AttributeError:
        try:
            st.experimental_rerun()
        except:
            st.stop()

def safe_play_audio(text):
    """語音播放安全模式"""
    try:
        from gtts import gTTS
        # 使用印尼語 (id) 發音
        tts = gTTS(text=text, lang='id')
        fp = BytesIO()
        tts.write_to_fp(fp)
        st.audio(fp, format='audio/mp3')
    except Exception as e:
        st.caption(f"🔇 (語音生成暫時無法使用)")

# --- 0. 系統配置 ---
st.set_page_config(page_title="Unit 36: O Omah", page_icon="🌾", layout="centered")

# --- CSS 美化 (豐收金黃色) ---
st.markdown("""
    <style>
    body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .source-tag { font-size: 12px; color: #aaa; text-align: right; font-style: italic; }
    .morph-tag { 
        background-color: #FFF9C4; color: #F57F17; 
        padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: bold;
        display: inline-block; margin-right: 5px;
    }
    
    /* 單字卡 */
    .word-card {
        background: linear-gradient(135deg, #FFFDE7 0%, #ffffff 100%);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 15px;
        border-bottom: 4px solid #FBC02D;
    }
    .emoji-icon { font-size: 48px; margin-bottom: 10px; }
    .amis-text { font-size: 22px; font-weight: bold; color: #F57F17; }
    .chinese-text { font-size: 16px; color: #7f8c8d; }
    
    /* 句子框 */
    .sentence-box {
        background-color: #FFFDE7;
        border-left: 5px solid #FDD835;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }

    /* 按鈕 */
    .stButton>button {
        width: 100%; border-radius: 12px; font-size: 20px; font-weight: 600;
        background-color: #FFF9C4; color: #F57F17; border: 2px solid #FBC02D; padding: 12px;
    }
    .stButton>button:hover { background-color: #FFF59D; border-color: #F9A825; }
    .stProgress > div > div > div > div { background-color: #FBC02D; }
    </style>
""", unsafe_allow_html=True)

# --- 2. 資料庫 (Unit 36: 18個單字 - User Fix) ---
vocab_data = [
    {"amis": "Maomah", "chi": "耕作 / 做農活", "icon": "🚜", "source": "Row 676", "morph": "Ma-Omah"},
    {"amis": "Mipaloma", "chi": "種植", "icon": "🌱", "source": "Row 1293", "morph": "Mi-Paloma"},
    {"amis": "Mikolas", "chi": "除草", "icon": "🌿", "source": "Row 481", "morph": "Mi-Kolas"},
    {"amis": "Lamelo", "chi": "雜草 (小米草)", "icon": "🌾", "source": "Row 481", "morph": "Noun"},
    {"amis": "Panay", "chi": "稻子 / 稻米", "icon": "🌾", "source": "Row 738", "morph": "Noun"},
    {"amis": "Hemay", "chi": "飯 / 米飯", "icon": "🍚", "source": "Row 210", "morph": "Noun"},
    {"amis": "^Epah", "chi": "酒", "icon": "🍶", "source": "User Fix", "morph": "Noun"}, # 修正
    {"amis": "Sota'", "chi": "泥巴 / 泥團", "icon": "🟤", "source": "User Fix", "morph": "Noun"}, # 修正
    {"amis": "Kilang", "chi": "樹 / 木頭", "icon": "🌳", "source": "Row 259", "morph": "Noun"},
    {"amis": "Pakaen", "chi": "餵食(詞根)", "icon": "🥣", "source": "Row 517", "morph": "Pa-Kaen"},
    {"amis": "Kalimelaan", "chi": "珍惜的 / 寶貴的", "icon": "💎", "source": "Row 490", "morph": "Ka-Limela-an"},
    {"amis": "Tatokem", "chi": "龍葵 (野菜)", "icon": "🥬", "source": "Row 2472", "morph": "Noun"},
    {"amis": "Sama'", "chi": "山萵苣 (野菜)", "icon": "🥗", "source": "Row 2472", "morph": "Noun"},
    {"amis": "Mipakaen", "chi": "餵食", "icon": "🍼", "source": "Row 1205", "morph": "Mi-Pa-Kaen"},
    {"amis": "Omah", "chi": "田地 (詞根)", "icon": "🏞️", "source": "Root", "morph": "Root"},
    {"amis": "Paloma", "chi": "種植 / 植物 (詞根)", "icon": "🪴", "source": "Root", "morph": "Root"},
    {"amis": "Kolas", "chi": "除草 (詞根)", "icon": "✂️", "source": "Root", "morph": "Root"},
    {"amis": "Limela", "chi": "愛惜 (詞根)", "icon": "❤️", "source": "Root", "morph": "Root"},
]

# --- 句子庫 (9句: 嚴格源自 CSV 並移除連字號) ---
sentences = [
    {"amis": "Mangatato ko pikolasan to lamelo.", "chi": "除小米草的季節已經快到了。", "icon": "⏳", "source": "Row 481 (User Fix)"},
    {"amis": "Pakaenhan to hemay, titi ato ^epah.", "chi": "請吃糯米糕、肉和酒。", "icon": "🍖", "source": "Row 517 (User Fix)"},
    {"amis": "Mikilidong kita i la'eno no kilang.", "chi": "我們在樹下躲雨。", "icon": "🌳", "source": "Row 259 (User Fix)"},
    {"amis": "O kalimelaan no maomahay ko kolong.", "chi": "牛是農民所珍惜的。", "icon": "🐂", "source": "Row 490"},
    {"amis": "Hato o sama' ato tatokem ato dongec.", "chi": "像是山萵苣、龍葵、還有藤心。", "icon": "🍲", "source": "Row 2472"},
    {"amis": "Mipaloma to panay.", "chi": "種植稻子。", "icon": "🌱", "source": "Standard Pattern"},
    {"amis": "Pina ko toki a maomah kami?", "chi": "我們幾點做農活？", "icon": "⏰", "source": "Row 676"},
    {"amis": "Mipakaen to fafoy.", "chi": "餵豬。", "icon": "🐖", "source": "Standard Pattern"},
    {"amis": "Adihay ko sota' i papotal.", "chi": "外面的泥巴很多。", "icon": "🟤", "source": "Adapted from Row 450"},
]

# --- 3. 隨機題庫 (5題) ---
raw_quiz_pool = [
    {
        "q": "Mangatato ko pikolasan to lamelo.",
        "audio": "Mangatato ko pikolasan to lamelo",
        "options": ["除小米草的季節快到了", "收割稻子的季節快到了", "種植地瓜的季節快到了"],
        "ans": "除小米草的季節快到了",
        "hint": "Kolas (除草), Lamelo (雜草) (User Fix)"
    },
    {
        "q": "Mikilidong kita i la'eno no kilang.",
        "audio": "Mikilidong kita i la'eno no kilang",
        "options": ["我們在樹下躲雨", "我們在樹上睡覺", "我們在樹旁吃飯"],
        "ans": "我們在樹下躲雨",
        "hint": "La'eno (下方) (User Fix)"
    },
    {
        "q": "單字測驗：^Epah",
        "audio": "^Epah",
        "options": ["酒", "水", "茶"],
        "ans": "酒",
        "hint": "Pakaenhan to ... ^epah"
    },
    {
        "q": "單字測驗：Sota'",
        "audio": "Sota'",
        "options": ["泥巴/泥團", "石頭", "沙子"],
        "ans": "泥巴/泥團",
        "hint": "User Fix: Sota'"
    },
    {
        "q": "單字測驗：Pakaen",
        "audio": "Pakaen",
        "options": ["餵食", "去吃", "煮飯"],
        "ans": "餵食",
        "hint": "Pa- (使/給) + Kaen (吃)"
    }
]

# --- 4. 狀態初始化 (洗牌邏輯) ---
if 'init' not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_q_idx = 0
    st.session_state.quiz_id = str(random.randint(1000, 9999))
    
    # 抽題與洗牌 (5題)
    selected_questions = random.sample(raw_quiz_pool, 5)
    final_questions = []
    for q in selected_questions:
        q_copy = q.copy()
        shuffled_opts = random.sample(q['options'], len(q['options']))
        q_copy['shuffled_options'] = shuffled_opts
        final_questions.append(q_copy)
        
    st.session_state.quiz_questions = final_questions
    st.session_state.init = True

# --- 5. 主介面 ---
st.markdown("<h1 style='text-align: center; color: #F57F17;'>Unit 36: O Omah</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>農耕與土地 (User Corrected)</p>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 詞彙與句型", "🎲 隨機挑戰"])

# === Tab 1: 學習模式 ===
with tab1:
    st.subheader("📝 核心單字 (構詞分析)")
    col1, col2 = st.columns(2)
    for i, word in enumerate(vocab_data):
        with (col1 if i % 2 == 0 else col2):
            st.markdown(f"""
            <div class="word-card">
                <div class="emoji-icon">{word['icon']}</div>
                <div class="amis-text">{word['amis']}</div>
                <div class="chinese-text">{word['chi']}</div>
                <div class="morph-tag">{word['morph']}</div>
                <div class="source-tag">src: {word['source']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"🔊 聽發音", key=f"btn_vocab_{i}"):
                safe_play_audio(word['amis'])

    st.markdown("---")
    st.subheader("🗣️ 實用句型 (Data-Driven)")
    for i, s in enumerate(sentences):
        st.markdown(f"""
        <div class="sentence-box">
            <div style="font-size: 20px; font-weight: bold; color: #F57F17;">{s['icon']} {s['amis']}</div>
            <div style="font-size: 16px; color: #555; margin-top: 5px;">{s['chi']}</div>
            <div class="source-tag">src: {s['source']}</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button(f"▶️ 播放句型", key=f"btn_sent_{i}"):
            safe_play_audio(s['amis'])

# === Tab 2: 隨機挑戰模式 ===
with tab2:
    st.markdown("### 🎲 隨機評量")
    
    if st.session_state.current_q_idx < len(st.session_state.quiz_questions):
        q_data = st.session_state.quiz_questions[st.session_state.current_q_idx]
        
        st.progress((st.session_state.current_q_idx) / 5)
        st.markdown(f"**Question {st.session_state.current_q_idx + 1} / 5**")
        
        st.markdown(f"### {q_data['q']}")
        if q_data['audio']:
            if st.button("🎧 播放題目音檔", key=f"btn_audio_{st.session_state.current_q_idx}"):
                safe_play_audio(q_data['audio'])
        
        # 使用洗牌後的選項
        unique_key = f"q_{st.session_state.quiz_id}_{st.session_state.current_q_idx}"
        user_choice = st.radio("請選擇正確答案：", q_data['shuffled_options'], key=unique_key)
        
        if st.button("送出答案", key=f"btn_submit_{st.session_state.current_q_idx}"):
            if user_choice == q_data['ans']:
                st.balloons()
                st.success("🎉 答對了！")
                time.sleep(1)
                st.session_state.score += 20
                st.session_state.current_q_idx += 1
                safe_rerun()
            else:
                st.error(f"不對喔！提示：{q_data['hint']}")
                
    else:
        st.progress(1.0)
        st.markdown(f"""
        <div style='text-align: center; padding: 30px; background-color: #FFF9C4; border-radius: 20px; margin-top: 20px;'>
            <h1 style='color: #F57F17;'>🏆 挑戰成功！</h1>
            <h3 style='color: #333;'>本次得分：{st.session_state.score}</h3>
            <p>你已經學會農耕詞彙了！</p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("🔄 再來一局 (重新抽題)", key="btn_restart"):
            st.session_state.score = 0
            st.session_state.current_q_idx = 0
            st.session_state.quiz_id = str(random.randint(1000, 9999))
            
            new_questions = random.sample(raw_quiz_pool, 5)
            final_qs = []
            for q in new_questions:
                q_copy = q.copy()
                shuffled_opts = random.sample(q['options'], len(q['options']))
                q_copy['shuffled_options'] = shuffled_opts
                final_qs.append(q_copy)
            
            st.session_state.quiz_questions = final_qs
            safe_rerun()



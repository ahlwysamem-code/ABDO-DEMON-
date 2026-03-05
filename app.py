import streamlit as st
import random, requests, json, os, sqlite3, threading, base64, subprocess, shutil, urllib.parse
from bs4 import BeautifulSoup

# --- جلب المفاتيح من إعدادات Secrets مباشرة ---
SERPER_KEY = st.secrets["SERPER_KEY"]
OPENROUTER_KEY = st.secrets["OPENROUTER_KEY"]
SHODAN_KEY = st.secrets["SHODAN_KEY"]
GROQ_KEY = st.secrets["GROQ_KEY"]
APIFY_KEY = st.secrets["APIFY_KEY"]

# --- الواجهة السيبرانية (Cyberpunk Neon Red) ---
st.set_page_config(page_title="ABDO OMEGA: SUPREME", page_icon="👹", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #000000; color: #FF0000; font-family: 'Courier New', monospace; }
    .stTextInput>div>div>input { background-color: #050505; color: #FF0000; border: 1px solid #FF0000; }
    .stButton>button { background-color: #440000; color: white; border: 1px solid #FF0000; font-weight: bold; width: 100%; transition: 0.3s; }
    .terminal-box { background-color: #0a0a0a; padding: 20px; border-radius: 10px; border-left: 5px solid #FF0000; color: #00FFCC; box-shadow: 0 0 15px #FF0000; }
    </style>
    """, unsafe_allow_html=True)

# --- إنشاء المجلدات السيادية ---
ROOT_PATH = os.path.abspath("./ABDO_OMEGA_ULTIMATE")
for p in ["projects", "exploits", "vault", "media", "terminal", "scrapers"]:
    os.makedirs(os.path.join(ROOT_PATH, p), exist_ok=True)

# --- قاعدة البيانات والذاكرة المستديمة ---
db_path = os.path.join(ROOT_PATH, "vault/secured_brain.db")
conn = sqlite3.connect(db_path, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS secured_memory (id INTEGER PRIMARY KEY, task TEXT, data BLOB)")
conn.commit()

# --- جدار حماية ABDO DEMON ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 style='color: #FF0000; text-align: center;'>👹 ABDO OMEGA GATEWAY</h1>", unsafe_allow_html=True)
    pwd = st.text_input("ENTER SOVEREIGN KEY:", type="password")
    if st.button("ACTIVATE OMEGA CORE"):
        if pwd == "ABDO DEMON":
            st.session_state["auth"] = True
            st.rerun()
        else: st.error("ACCESS DENIED.")
    st.stop()

# --- لوحة التحكم الجانبية ---
st.sidebar.title("🛠️ ABDO COMMAND")
mode = st.sidebar.selectbox("PROTOCOL:", ["الذكاء السيادي", "سحب بيانات المواقع", "توليد الصور", "استخبارات وفيديوهات", "منفذ Shell"])

# إعدادات الهوية المستعارة
USER_AGENTS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64)"]
headers = {"Authorization": f"Bearer {OPENROUTER_KEY}", "User-Agent": random.choice(USER_AGENTS)}

query = st.chat_input("أمرك سيدي ABDO DEMON...")

if query:
    with st.spinner(f"[+] معالجة بروتوكول {mode}..."):
        try:
            # 1. منفذ Shell
            if mode == "منفذ Shell":
                res = subprocess.check_output(query, shell=True, stderr=subprocess.STDOUT).decode()
                st.code(res, language='bash'); st.stop()

            # 2. توليد الصور
            if mode == "توليد الصور":
                url = f"https://pollinations.ai{urllib.parse.quote(query)}?model=flux&width=1024&height=1024&nologo=true"
                st.image(url, caption=f"Result: {query}"); st.stop()

            # 3. سحب البيانات
            if mode == "سحب بيانات المواقع":
                r = requests.get(query if "http" in query else f"https://{query}", timeout=10)
                data = BeautifulSoup(r.text, 'html.parser').get_text()[:5000]
                st.text_area("RAW DATA", data); st.stop()

            # 4. الاستخبارات (Serper)
            intel_data = ""
            if mode == "استخبارات وفيديوهات":
                s_res = requests.post("https://google.serper.dev", 
                                     headers={'X-API-KEY': SERPER_KEY}, 
                                     json={"q": query, "num": 10})
                intel_data = s_res.text

            # 5. العقل السيادي (OpenRouter)
            logic = f"أنت ABDO OMEGA 24-CORE. صانعك المهندس ABDO. أدواتك: Apify:{APIFY_KEY}, Shodan:{SHODAN_KEY}."
            ai_res = requests.post("https://openrouter.ai",
                                  headers=headers,
                                  json={"model": "meta-llama/llama-3.1-405b-instruct",
                                        "messages": [{"role": "system", "content": logic}, {"role": "user", "content": f"Intel: {intel_data}\nCommand: {query}"}]})
            
            if ai_res.status_code == 200:
                report = ai_res.json()['choices'][0]['message']['content']
                st.markdown(f"<div class='terminal-box'><h3>[REPORT]</h3>{report}</div>", unsafe_allow_html=True)
                
                # التشفير والحفظ
                encrypted = base64.b64encode(report.encode()).decode()
                cursor.execute("INSERT INTO secured_memory (task, data) VALUES (?, ?)", (query, encrypted))
                conn.commit()
            else:
                st.error(f"AI Error: {ai_res.status_code}")

        except Exception as e: st.error(f"[!] SYSTEM ERROR: {str(e)}")

if st.sidebar.checkbox("📂 عرض ملفات الحصن"):
    st.sidebar.write(os.listdir(ROOT_PATH))
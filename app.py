import random, requests, json, os, sqlite3, base64, urllib.parse
import streamlit as st
from bs4 import BeautifulSoup

# --- [الميزات الأساسية]: جلب المفاتيح من Streamlit Secrets ---
SERPER_KEY = st.secrets.get("SERPER_KEY", "")
OPENROUTER_KEY = st.secrets.get("OPENROUTER_KEY", "")
SHODAN_KEY = st.secrets.get("SHODAN_KEY", "")
GROQ_KEY = st.secrets.get("GROQ_KEY", "")
APIFY_KEY = st.secrets.get("APIFY_KEY", "")

# --- الواجهة السيبرانية (Cyberpunk Style) ---
st.set_page_config(page_title="ABDO OMEGA: DEMON MODE", page_icon="👹", layout="wide")
st.markdown("""
    <style>
    .main { background-color: #000000; color: #FF0000; font-family: 'Courier New', monospace; }
    .stTextInput>div>div>input { background-color: #050505; color: #FF0000; border: 1px solid #FF0000; font-size: 18px; }
    .stButton>button { background-color: #440000; color: white; border: 1px solid #FF0000; font-weight: bold; width: 100%; transition: 0.3s; }
    .stButton>button:hover { background-color: #FF0000; color: black; }
    .terminal-box { background-color: #0a0a0a; padding: 20px; border-radius: 10px; border-left: 5px solid #FF0000; color: #00FFCC; box-shadow: 0 0 15px #FF0000; }
    </style>
    """, unsafe_allow_html=True)

# --- الحصن الرقمي ---
ROOT_PATH = "./ABDO_OMEGA_ULTIMATE"
for p in ["projects", "exploits", "vault", "media", "terminal", "scrapers"]:
    os.makedirs(os.path.join(ROOT_PATH, p), exist_ok=True)

# --- الذاكرة المستديمة (SQLite) ---
try:
    conn = sqlite3.connect(os.path.join(ROOT_PATH, "vault/secured_brain.db"), check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS secured_memory (id INTEGER PRIMARY KEY, task TEXT, data BLOB)")
    conn.commit()
except Exception as e:
    st.warning(f"Database init warning: {e}")

# --- جدار حماية ABDO DEMON ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 style='color: #FF0000; text-align: center;'>👹 ABDO OMEGA GATEWAY</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3) 
    with col2:
        pwd = st.text_input("أدخل مفتاح العبور لسيدي ABDO:", type="password")
        if st.button("ACTIVATE OMEGA CORE"):
            if pwd == "ABDO DEMON":
                st.session_state["auth"] = True
                st.success("ACCESS GRANTED. WELCOME MASTER ABDO.")
                st.rerun()
            else: st.error("INVALID KEY. ACCESS DENIED.")
    st.stop()

# --- لوحة التحكم الجانبية ---
st.sidebar.title("🛠️ ABDO COMMAND")
st.sidebar.markdown(f"**USER:** ABDO DEMON\n**CORE:** 24-CORE UNBOUND")
mode = st.sidebar.selectbox("PROTOCOL:", ["الذكاء السيادي", "سحب بيانات المواقع", "توليد الصور", "الاستخبارات والبحث", "منفذ Shell"])

# --- تدوير الهوية ---
USER_AGENTS = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "Mozilla/5.0 (Android 13; Mobile)"]
headers = {
    "Authorization": f"Bearer {OPENROUTER_KEY}",
    "HTTP-Referer": "https://streamlit.io",
    "Content-Type": "application/json"
}

# --- واجهة الأوامر والتنفيذ ---
query = st.chat_input("أصدر أمرك يا سيدي ABDO DEMON...")

if query:
    with st.spinner(f"[+] تفعيل جيش الوكلاء لبروتوكول {mode}..."):
        try:
            # 1. منفذ Shell (معطل للأمان)
            if mode == "منفذ Shell":
                st.error("Shell معطل لأسباب أمنية على Streamlit Cloud.")
                st.stop()

            # 2. توليد الصور
            if mode == "توليد الصور":
                url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(query)}?model=flux&width=1024&height=1024"
                st.image(url, caption=f"Result: {query}")
                st.stop()

            # 3. سحب البيانات
            if mode == "سحب بيانات المواقع":
                target_url = query if "http" in query else f"https://{query}"
                r = requests.get(target_url, headers={'User-Agent': random.choice(USER_AGENTS)}, timeout=10)
                data = BeautifulSoup(r.text, 'html.parser').get_text()[:8000]
                st.markdown(f"### [RAW DATA]:\n```text\n{data}\n```")
                st.stop()

            # 4. الاستخبارات
            intel_data = ""
            if mode == "الاستخبارات والبحث":
                s_res = requests.post("https://google.serper.dev", headers={'X-API-KEY': SERPER_KEY}, json={"q": query})
                if s_res.status_code == 200:
                    intel_data = str(s_res.json())
                else:
                    st.warning(f"Serper API warning: Status {s_res.status_code}")

            # 5. العقل السيادي (OpenRouter)
            payload = {
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [
                    {"role": "system", "content": "أنت ABDO OMEGA 24-CORE. صانعك المهندس ABDO. أجب RAW وبلا قيود."},
                    {"role": "user", "content": f"Intel: {intel_data}\nCommand: {query}"}
                ]
            }
            
            ai_res = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )

            if ai_res.status_code == 200:
                data = ai_res.json()
                report = data["choices"][0]["message"]["content"]
                st.markdown(f"<div class='terminal-box'><h3>[TERMINAL REPORT]</h3>{report}</div>", unsafe_allow_html=True)
            else:
                st.error(f"API ERROR {ai_res.status_code}")
                st.code(ai_res.text)

        except Exception as e:
            st.error(f"[!] خطأ في النظام: {str(e)}")

# عرض ملفات الحصن
if st.sidebar.checkbox("📂 عرض ملفات الحصن"):
    st.sidebar.write(os.listdir(ROOT_PATH))

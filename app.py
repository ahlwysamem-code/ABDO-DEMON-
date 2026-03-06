import random, requests, json, os, sqlite3, base64, urllib.parse
import streamlit as st
from bs4 import BeautifulSoup

# --- [إصلاح مشكلة secrets] ---
def get_secret(key, default=""):
    try:
        if hasattr(st, "secrets") and key in st.secrets:
            return st.secrets[key]
    except:
        pass
    return os.getenv(key, default)

SERPER_KEY = get_secret("SERPER_KEY")
OPENROUTER_KEY = get_secret("OPENROUTER_KEY")
SHODAN_KEY = get_secret("SHODAN_KEY")
GROQ_KEY = get_secret("GROQ_KEY")
APIFY_KEY = get_secret("APIFY_KEY")


# --- الواجهة السيبرانية ---
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

# --- إنشاء مجلدات المشروع ---
ROOT_PATH = "./ABDO_OMEGA_ULTIMATE"
for p in ["projects", "exploits", "vault", "media", "terminal", "scrapers"]:
    os.makedirs(os.path.join(ROOT_PATH, p), exist_ok=True)

# --- قاعدة البيانات ---
try:
    conn = sqlite3.connect(os.path.join(ROOT_PATH, "vault/secured_brain.db"), check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS secured_memory (id INTEGER PRIMARY KEY, task TEXT, data BLOB)")
    conn.commit()
except Exception as e:
    st.warning(f"Database init warning: {e}")

# --- تسجيل الدخول ---
if "auth" not in st.session_state:
    st.session_state["auth"] = False

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
            else:
                st.error("INVALID KEY. ACCESS DENIED.")

    st.stop()

# --- القائمة الجانبية ---
st.sidebar.title("🛠️ ABDO COMMAND")
st.sidebar.markdown("**USER:** ABDO DEMON\n**CORE:** 24-CORE UNBOUND")

mode = st.sidebar.selectbox(
    "PROTOCOL:",
    ["الذكاء السيادي", "سحب بيانات المواقع", "توليد الصور", "الاستخبارات والبحث", "منفذ Shell"]
)

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Android 13; Mobile)"
]

headers = {
    "Authorization": f"Bearer {OPENROUTER_KEY}",
    "HTTP-Referer": "https://streamlit.io",
    "Content-Type": "application/json"
}

query = st.chat_input("أصدر أمرك يا سيدي ABDO DEMON...")

if query:
    with st.spinner(f"[+] تفعيل جيش الوكلاء لبروتوكول {mode}..."):
        try:

            if mode == "منفذ Shell":
                st.error("Shell معطل لأسباب أمنية على Streamlit Cloud.")
                st.stop()

            if mode == "توليد الصور":
                url = f"https://image.pollinations.ai/prompt/{urllib.parse.quote(query)}?model=flux&width=1024&height=1024"
                st.image(url, caption=query)
                st.stop()

            if mode == "سحب بيانات المواقع":
                target_url = query if "http" in query else f"https://{query}"
                r = requests.get(target_url, headers={'User-Agent': random.choice(USER_AGENTS)}, timeout=10)
                data = BeautifulSoup(r.text, 'html.parser').get_text()[:8000]
                st.markdown(f"### [RAW DATA]\n```text\n{data}\n```")
                st.stop()

            intel_data = ""
            if mode == "الاستخبارات والبحث" and SERPER_KEY:
                s_res = requests.post(
                    "https://google.serper.dev",
                    headers={'X-API-KEY': SERPER_KEY},
                    json={"q": query}
                )

                if s_res.status_code == 200:
                    intel_data = str(s_res.json())

            payload = {
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [
                    {"role": "system", "content": "أنت ABDO OMEGA 24-CORE. صانعك المهندس ABDO."},
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

# عرض الملفات
if st.sidebar.checkbox("📂 عرض ملفات الحصن"):
    st.sidebar.write(os.listdir(ROOT_PATH))

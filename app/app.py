import streamlit as st
import requests
from datetime import datetime

# -----------------------
# Config
# -----------------------
API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="RAG Chatbot", layout="wide", page_icon="🤖")

# -----------------------
# Full-page Glassmorphic CSS
# -----------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Reset & Root ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --glass-bg: rgba(255, 255, 255, 0.07);
  --glass-border: rgba(255, 255, 255, 0.15);
  --glass-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
  --accent: #7DF9C2;
  --accent2: #A78BFA;
  --accent3: #38BDF8;
  --text-primary: #F1F5F9;
  --text-muted: #94A3B8;
  --user-bubble: linear-gradient(135deg, #7DF9C2 0%, #38BDF8 100%);
  --bot-bubble: rgba(255, 255, 255, 0.08);
  --danger: #F87171;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, header, footer,
.stDeployButton, .viewerBadge_container__r5tak,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

.block-container {
  padding: 0 !important;
  max-width: 100% !important;
}

/* ── Animated mesh background ── */
.stApp {
  background:
    radial-gradient(ellipse at 20% 20%, rgba(167, 139, 250, 0.25) 0%, transparent 55%),
    radial-gradient(ellipse at 80% 10%, rgba(56, 189, 248, 0.2) 0%, transparent 45%),
    radial-gradient(ellipse at 60% 80%, rgba(125, 249, 194, 0.18) 0%, transparent 50%),
    radial-gradient(ellipse at 10% 85%, rgba(96, 165, 250, 0.15) 0%, transparent 45%),
    linear-gradient(135deg, #060614 0%, #0D0D2B 40%, #0A1628 100%);
  min-height: 100vh;
  font-family: 'DM Sans', sans-serif;
  color: var(--text-primary);
}

/* ── Layout shell: fixed full-viewport grid ── */
.app-shell {
  display: grid;
  grid-template-columns: 280px 1fr;
  grid-template-rows: 100vh;
  height: 100vh;
  width: 100%;
  overflow: hidden;
  position: fixed;
  top: 0; left: 0;
}

/* ── Sidebar ── */
.sidebar-panel {
  background: rgba(255,255,255,0.05);
  border-right: 1px solid var(--glass-border);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  display: flex;
  flex-direction: column;
  padding: 28px 20px;
  gap: 24px;
  overflow-y: auto;
  position: relative;
  z-index: 10;
}

.sidebar-panel::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: linear-gradient(180deg, rgba(167,139,250,0.05) 0%, transparent 60%);
  pointer-events: none;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-bottom: 20px;
  border-bottom: 1px solid var(--glass-border);
}

.brand-icon {
  width: 38px; height: 38px;
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent3) 100%);
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px;
  box-shadow: 0 0 20px rgba(125, 249, 194, 0.3);
}

.brand-text {
  font-family: 'Syne', sans-serif;
  font-size: 1.1rem;
  font-weight: 700;
  background: linear-gradient(135deg, var(--accent), var(--accent3));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.sidebar-label {
  font-family: 'Syne', sans-serif;
  font-size: 0.65rem;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-bottom: 10px;
}

/* Mode toggle pills */
.mode-pills {
  display: flex;
  background: rgba(0,0,0,0.25);
  border-radius: 10px;
  padding: 4px;
  gap: 4px;
  border: 1px solid var(--glass-border);
}

.mode-pill {
  flex: 1;
  padding: 8px 4px;
  border: none;
  border-radius: 7px;
  cursor: pointer;
  font-family: 'DM Sans', sans-serif;
  font-size: 0.75rem;
  font-weight: 500;
  transition: all 0.25s ease;
  background: transparent;
  color: var(--text-muted);
}

.mode-pill.active {
  background: linear-gradient(135deg, rgba(125,249,194,0.2), rgba(56,189,248,0.2));
  color: var(--text-primary);
  box-shadow: 0 2px 10px rgba(125,249,194,0.15);
  border: 1px solid rgba(125,249,194,0.3);
}

/* Glass input */
.glass-input-wrap {
  position: relative;
}

.glass-input-wrap input {
  width: 100%;
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 10px !important;
  padding: 10px 14px !important;
  color: var(--text-primary) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.82rem !important;
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
}

.glass-input-wrap input:focus {
  border-color: rgba(125,249,194,0.5) !important;
  box-shadow: 0 0 0 3px rgba(125,249,194,0.1) !important;
}

.glass-input-wrap input::placeholder { color: var(--text-muted) !important; }

/* Scrape button */
.scrape-btn {
  width: 100%;
  padding: 10px;
  background: linear-gradient(135deg, rgba(125,249,194,0.15), rgba(56,189,248,0.15));
  border: 1px solid rgba(125,249,194,0.35);
  border-radius: 10px;
  color: var(--accent);
  font-family: 'Syne', sans-serif;
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 0.05em;
  cursor: pointer;
  transition: all 0.2s ease;
}
.scrape-btn:hover {
  background: linear-gradient(135deg, rgba(125,249,194,0.25), rgba(56,189,248,0.25));
  box-shadow: 0 0 20px rgba(125,249,194,0.2);
  transform: translateY(-1px);
}

/* Status pill */
.status-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: rgba(125,249,194,0.1);
  border: 1px solid rgba(125,249,194,0.3);
  border-radius: 20px;
  padding: 5px 12px;
  font-size: 0.72rem;
  color: var(--accent);
  font-weight: 500;
}

.status-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--accent);
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}

.error-pill {
  background: rgba(248,113,113,0.1);
  border-color: rgba(248,113,113,0.3);
  color: var(--danger);
}

/* Stats */
.stat-card {
  background: var(--glass-bg);
  border: 1px solid var(--glass-border);
  border-radius: 12px;
  padding: 14px 16px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-value {
  font-family: 'Syne', sans-serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-label {
  font-size: 0.7rem;
  color: var(--text-muted);
}

/* ── Main chat area ── */
.main-panel {
  display: flex;
  flex-direction: column;
  height: 100vh;
  overflow: hidden;
  position: relative;
}

/* Chat header */
.chat-header {
  padding: 18px 28px;
  border-bottom: 1px solid var(--glass-border);
  background: rgba(255,255,255,0.03);
  backdrop-filter: blur(12px);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.chat-title {
  font-family: 'Syne', sans-serif;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.chat-subtitle {
  font-size: 0.72rem;
  color: var(--text-muted);
  margin-top: 1px;
}

/* Messages area */
.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 24px 28px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  scroll-behavior: smooth;
}

.messages-area::-webkit-scrollbar { width: 4px; }
.messages-area::-webkit-scrollbar-track { background: transparent; }
.messages-area::-webkit-scrollbar-thumb {
  background: rgba(255,255,255,0.1);
  border-radius: 2px;
}

/* Empty state */
.empty-state {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  opacity: 0.5;
}

.empty-icon {
  width: 64px; height: 64px;
  background: linear-gradient(135deg, rgba(125,249,194,0.15), rgba(56,189,248,0.15));
  border: 1px solid var(--glass-border);
  border-radius: 20px;
  display: flex; align-items: center; justify-content: center;
  font-size: 28px;
}

.empty-text {
  font-family: 'Syne', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-muted);
  text-align: center;
}

.empty-sub {
  font-size: 0.78rem;
  color: var(--text-muted);
  text-align: center;
  max-width: 240px;
  line-height: 1.6;
}

/* Message row */
.msg-row {
  display: flex;
  flex-direction: column;
  gap: 8px;
  animation: fadeSlideUp 0.3s ease forwards;
}

@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* User message */
.msg-user {
  align-self: flex-end;
  max-width: 65%;
}

.bubble-user {
  background: var(--user-bubble);
  color: #0A1628;
  padding: 12px 16px;
  border-radius: 18px 18px 4px 18px;
  font-size: 0.88rem;
  line-height: 1.55;
  font-weight: 500;
  box-shadow: 0 4px 20px rgba(125,249,194,0.2);
  word-wrap: break-word;
}

.msg-meta-user {
  font-size: 0.67rem;
  color: var(--text-muted);
  text-align: right;
  margin-right: 4px;
}

/* Bot message */
.msg-bot {
  align-self: flex-start;
  max-width: 65%;
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.bot-avatar {
  width: 28px; height: 28px;
  background: linear-gradient(135deg, var(--accent2), var(--accent3));
  border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-size: 13px;
  flex-shrink: 0;
  box-shadow: 0 2px 10px rgba(167,139,250,0.3);
}

.bubble-bot-wrap { display: flex; flex-direction: column; gap: 4px; }

.bubble-bot {
  background: var(--bot-bubble);
  border: 1px solid var(--glass-border);
  backdrop-filter: blur(12px);
  color: var(--text-primary);
  padding: 12px 16px;
  border-radius: 18px 18px 18px 4px;
  font-size: 0.88rem;
  line-height: 1.6;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
  word-wrap: break-word;
}

.mode-tag {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  background: rgba(167,139,250,0.12);
  border: 1px solid rgba(167,139,250,0.25);
  color: var(--accent2);
  font-size: 0.62rem;
  font-weight: 600;
  font-family: 'Syne', sans-serif;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 2px 8px;
  border-radius: 20px;
  width: fit-content;
  margin-bottom: 2px;
}

.msg-meta-bot {
  font-size: 0.67rem;
  color: var(--text-muted);
  margin-left: 4px;
}

/* ── Input bar ── */
.input-bar {
  padding: 16px 28px 20px;
  border-top: 1px solid var(--glass-border);
  background: rgba(255,255,255,0.03);
  backdrop-filter: blur(12px);
  flex-shrink: 0;
}

.input-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  background: rgba(255,255,255,0.07);
  border: 1px solid var(--glass-border);
  border-radius: 14px;
  padding: 6px 6px 6px 18px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.input-wrap:focus-within {
  border-color: rgba(125,249,194,0.4);
  box-shadow: 0 0 0 3px rgba(125,249,194,0.08), 0 8px 30px rgba(0,0,0,0.3);
}

.msg-input {
  flex: 1;
  background: transparent !important;
  border: none !important;
  outline: none !important;
  color: var(--text-primary) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.9rem !important;
  padding: 8px 0 !important;
  box-shadow: none !important;
}

.msg-input::placeholder { color: var(--text-muted) !important; opacity: 0.7; }

.send-btn {
  width: 40px; height: 40px;
  background: linear-gradient(135deg, var(--accent) 0%, var(--accent3) 100%);
  border: none;
  border-radius: 10px;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  color: #0A1628;
  font-size: 15px;
  transition: all 0.2s ease;
  flex-shrink: 0;
  box-shadow: 0 4px 15px rgba(125,249,194,0.3);
}

.send-btn:hover {
  transform: scale(1.08);
  box-shadow: 0 6px 22px rgba(125,249,194,0.45);
}

.send-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
}

.input-hint {
  font-size: 0.68rem;
  color: var(--text-muted);
  margin-top: 8px;
  text-align: center;
  opacity: 0.6;
}

/* Typing indicator */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 4px 0;
}

.typing-dots {
  display: flex;
  gap: 4px;
}

.typing-dot {
  width: 6px; height: 6px;
  background: var(--accent);
  border-radius: 50%;
  animation: typingBounce 1.2s infinite ease-in-out;
}

.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes typingBounce {
  0%, 80%, 100% { transform: translateY(0); opacity: 0.4; }
  40% { transform: translateY(-6px); opacity: 1; }
}

/* ── Streamlit element overrides ── */
[data-testid="stTextInput"] > div > div {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
}

[data-testid="stTextInput"] input {
  background: transparent !important;
  border: none !important;
  box-shadow: none !important;
  padding: 8px 0 !important;
  color: var(--text-primary) !important;
  font-family: 'DM Sans', sans-serif !important;
  font-size: 0.9rem !important;
}

[data-testid="stTextInput"] input::placeholder {
  color: rgba(148,163,184,0.6) !important;
}

[data-testid="stTextInput"] input:focus {
  box-shadow: none !important;
  border: none !important;
  outline: none !important;
}

[data-testid="stButton"] button {
  background: linear-gradient(135deg, #7DF9C2 0%, #38BDF8 100%) !important;
  color: #0A1628 !important;
  border: none !important;
  border-radius: 10px !important;
  font-family: 'Syne', sans-serif !important;
  font-weight: 700 !important;
  font-size: 0.8rem !important;
  letter-spacing: 0.05em !important;
  padding: 0 !important;
  width: 40px !important;
  height: 40px !important;
  transition: all 0.2s ease !important;
  box-shadow: 0 4px 15px rgba(125,249,194,0.3) !important;
}

[data-testid="stButton"] button:hover {
  transform: scale(1.08) !important;
  box-shadow: 0 6px 22px rgba(125,249,194,0.45) !important;
}

/* Sidebar elements */
[data-testid="stSidebar"] {
  background: transparent !important;
}

[data-testid="stSidebar"] > div:first-child {
  background: rgba(6,6,20,0.75) !important;
  border-right: 1px solid var(--glass-border) !important;
  backdrop-filter: blur(24px) !important;
}

[data-testid="stSidebar"] * {
  color: var(--text-primary) !important;
  font-family: 'DM Sans', sans-serif !important;
}

[data-testid="stSidebar"] .stRadio label {
  cursor: pointer;
}

[data-testid="stSidebar"] [data-testid="stTextInput"] input {
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid var(--glass-border) !important;
  border-radius: 10px !important;
  padding: 10px 14px !important;
  color: var(--text-primary) !important;
  font-size: 0.82rem !important;
}

[data-testid="stSidebar"] [data-testid="stTextInput"] input:focus {
  border-color: rgba(125,249,194,0.5) !important;
  box-shadow: 0 0 0 3px rgba(125,249,194,0.1) !important;
}

[data-testid="stSidebar"] [data-testid="stButton"] button {
  width: 100% !important;
  height: auto !important;
  padding: 10px 16px !important;
  font-size: 0.78rem !important;
}

/* Remove default streamlit spacing */
.stMarkdown { margin: 0 !important; }
div[data-testid="stVerticalBlock"] > div { padding: 0 !important; }

/* Chat wrapper fills space properly */
.chat-main-wrapper {
  height: calc(100vh - 0px);
  display: flex;
  flex-direction: column;
  background: transparent;
}

.chat-messages-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 20px 0;
  scrollbar-width: thin;
  scrollbar-color: rgba(255,255,255,0.1) transparent;
}

/* Thinking animation */
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}

.thinking {
  background: linear-gradient(90deg,
    rgba(125,249,194,0.05) 0%,
    rgba(125,249,194,0.15) 50%,
    rgba(125,249,194,0.05) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}

/* Floating orb decorations */
.orb {
  position: fixed;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
  z-index: 0;
  animation: drift 8s ease-in-out infinite alternate;
}

.orb-1 {
  width: 400px; height: 400px;
  background: rgba(167,139,250,0.06);
  top: -100px; right: 10%;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px; height: 300px;
  background: rgba(56,189,248,0.05);
  bottom: 5%; left: 35%;
  animation-delay: 3s;
}

@keyframes drift {
  from { transform: translate(0, 0) scale(1); }
  to   { transform: translate(30px, -20px) scale(1.05); }
}
</style>
""", unsafe_allow_html=True)

# ── Decorative orbs ──
st.markdown("""
<div class="orb orb-1"></div>
<div class="orb orb-2"></div>
""", unsafe_allow_html=True)

# ── Session state ──
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "mode" not in st.session_state:
    st.session_state.mode = "General Chat"
if "scrape_status" not in st.session_state:
    st.session_state.scrape_status = None
if "scrape_msg" not in st.session_state:
    st.session_state.scrape_msg = ""
if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False
if "website_url" not in st.session_state:
    st.session_state.website_url = ""

# ── Sidebar ──
with st.sidebar:
    # Brand
    st.markdown("""
    <div class="brand">
      <div class="brand-icon">🤖</div>
      <span class="brand-text">RAG Chatbot</span>
    </div>
    """, unsafe_allow_html=True)

    # Mode selector
    st.markdown('<div class="sidebar-label">Mode</div>', unsafe_allow_html=True)
    mode = st.radio(
        "",
        ["General Chat", "Website Chat"],
        key="mode_radio",
        label_visibility="collapsed"
    )
    st.session_state.mode = mode

    st.markdown("---")

    # Website section
    if mode == "Website Chat":
        st.markdown('<div class="sidebar-label">Data Source</div>', unsafe_allow_html=True)
        website_url = st.text_input(
            "",
            placeholder="https://example.com",
            key="url_input",
            label_visibility="collapsed"
        )
        scrape_btn = st.button("⚡  Scrape & Index", key="scrape_btn")

        if scrape_btn:
            if not website_url.startswith("http"):
                st.session_state.scrape_status = "error"
                st.session_state.scrape_msg = "Enter a valid URL (http/https)"
            else:
                with st.spinner("Scraping..."):
                    try:
                        res = requests.post(f"{API_URL}/add-website", params={"url": website_url})
                        data = res.json()
                        chunks = data.get("chunks_stored", 0)
                        st.session_state.scrape_status = "success"
                        st.session_state.scrape_msg = f"{chunks} chunks indexed"
                        st.session_state.website_url = website_url
                    except Exception as e:
                        st.session_state.scrape_status = "error"
                        st.session_state.scrape_msg = str(e)

        if st.session_state.scrape_status == "success":
            st.markdown(f"""
            <div class="status-pill">
              <div class="status-dot"></div>
              {st.session_state.scrape_msg}
            </div>
            """, unsafe_allow_html=True)
        elif st.session_state.scrape_status == "error":
            st.markdown(f"""
            <div class="status-pill error-pill">
              ⚠ {st.session_state.scrape_msg}
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")

    # Stats
    total_msgs = len(st.session_state.chat_history)
    st.markdown('<div class="sidebar-label">Session Stats</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stat-card">
      <div>
        <div class="stat-value">{total_msgs}</div>
        <div class="stat-label">Messages</div>
      </div>
      <div style="font-size:1.5rem">💬</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Clear chat
    if st.button("🗑  Clear Chat", key="clear_btn"):
        st.session_state.chat_history = []
        st.rerun()

    # Footer
    st.markdown("""
    <div style="margin-top:auto; padding-top:24px; font-size:0.68rem; color:rgba(148,163,184,0.5); text-align:center; line-height:1.8;">
      Powered by RAG + AI<br>
      <span style="color:rgba(125,249,194,0.4);">●</span> Connected
    </div>
    """, unsafe_allow_html=True)

# ── Main Area ──
# Header
mode_icon = "🌐" if st.session_state.mode == "Website Chat" else "💭"
mode_label = st.session_state.mode
header_sub = (
    f"Chatting with: {st.session_state.website_url[:35]}..."
    if st.session_state.mode == "Website Chat" and st.session_state.website_url
    else "Ask me anything"
)

st.markdown(f"""
<div class="chat-header">
  <div>
    <div class="chat-title">{mode_icon} {mode_label}</div>
    <div class="chat-subtitle">{header_sub}</div>
  </div>
  <div class="status-pill">
    <div class="status-dot"></div>
    Online
  </div>
</div>
""", unsafe_allow_html=True)

# ── Chat messages area ──
st.markdown('<div class="messages-area" id="messages-area">', unsafe_allow_html=True)

if not st.session_state.chat_history:
    st.markdown("""
    <div class="empty-state">
      <div class="empty-icon">✨</div>
      <div class="empty-text">Start a conversation</div>
      <div class="empty-sub">Type a message below and press Enter or click Send</div>
    </div>
    """, unsafe_allow_html=True)
else:
    for chat in st.session_state.chat_history:
        mode_tag_color = "#A78BFA" if chat.get("mode") == "website" else "#38BDF8"
        mode_tag_label = "🌐 Website RAG" if chat.get("mode") == "website" else "💭 General"
        st.markdown(f"""
        <div class="msg-row">
          <!-- User -->
          <div class="msg-user">
            <div class="bubble-user">{chat['user']}</div>
            <div class="msg-meta-user">{chat['time']}</div>
          </div>
          <!-- Bot -->
          <div class="msg-bot">
            <div class="bot-avatar">🤖</div>
            <div class="bubble-bot-wrap">
              <div class="mode-tag">{mode_tag_label}</div>
              <div class="bubble-bot">{chat['bot']}</div>
              <div class="msg-meta-bot">{chat['time']}</div>
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

if st.session_state.is_thinking:
    st.markdown("""
    <div class="msg-row">
      <div class="msg-bot">
        <div class="bot-avatar">🤖</div>
        <div class="bubble-bot-wrap">
          <div class="bubble-bot thinking" style="padding:14px 18px;">
            <div class="typing-dots">
              <div class="typing-dot"></div>
              <div class="typing-dot"></div>
              <div class="typing-dot"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Input bar ──
st.markdown('<div class="input-bar"><div class="input-wrap">', unsafe_allow_html=True)

col_input, col_btn = st.columns([12, 1])

with col_input:
    user_input = st.text_input(
        "",
        placeholder="Type a message… (Enter to send)",
        key="chat_input",
        label_visibility="collapsed",
    )

with col_btn:
    send_btn = st.button("➤", key="send_btn")

st.markdown('</div><div class="input-hint">Press Enter or click ➤ to send</div></div>', unsafe_allow_html=True)

# ── Scroll to bottom JS ──
st.markdown("""
<script>
  const el = document.getElementById('messages-area');
  if (el) el.scrollTop = el.scrollHeight;

  // Enter key detection
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      const input = document.querySelector('[data-testid="stTextInput"] input');
      if (document.activeElement === input) {
        e.preventDefault();
        const btn = document.querySelector('[data-testid="stButton"] button');
        if (btn) btn.click();
      }
    }
  });
</script>
""", unsafe_allow_html=True)

# ── Send logic ──
if (send_btn or user_input) and user_input.strip():
    # Avoid double-send on re-render
    if (
        not st.session_state.chat_history
        or st.session_state.chat_history[-1]["user"] != user_input.strip()
    ):
        st.session_state.is_thinking = True
        with st.spinner(""):
            try:
                payload = {
                    "message": user_input.strip(),
                    "use_website": st.session_state.mode == "Website Chat"
                }
                res = requests.post(f"{API_URL}/chat", params=payload)
                data = res.json()
                bot_response = data.get("response", "")
                st.session_state.chat_history.append({
                    "time": datetime.now().strftime("%H:%M"),
                    "mode": data.get("mode", "general"),
                    "user": user_input.strip(),
                    "bot": bot_response,
                })
            except Exception as e:
                st.session_state.chat_history.append({
                    "time": datetime.now().strftime("%H:%M"),
                    "mode": "error",
                    "user": user_input.strip(),
                    "bot": f"⚠️ Could not connect to backend: {e}",
                })
        st.session_state.is_thinking = False
        st.rerun()
# Security News Digest - web app
# Run with:  streamlit run app.py

import html
from datetime import datetime

import streamlit as st
import digest

st.set_page_config(page_title="Security News Digest", page_icon="🛡️", layout="centered")

# ---------------------------------------------------------------------
# Look and feel: warm neon city at night (amber, orange, pink, a touch of cyan)
# ---------------------------------------------------------------------
CATEGORY_COLORS = {
    "Ransomware": "#FF4F8B",
    "Vulnerability": "#FF7A2E",
    "Data Breach": "#FFB347",
    "Phishing": "#3FD8E0",
    "Malware": "#FF8FB1",
    "Other": "#A8968A",
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;700&family=Figtree:wght@400;600&display=swap');

[data-testid="stApp"] {
    background:
        radial-gradient(circle at 12% 88%, rgba(255,122,46,0.18), transparent 28%),
        radial-gradient(circle at 85% 12%, rgba(255,179,71,0.14), transparent 30%),
        radial-gradient(circle at 70% 75%, rgba(255,79,139,0.12), transparent 26%),
        radial-gradient(circle at 30% 20%, rgba(63,216,224,0.07), transparent 22%),
        #120C17;
    background-attachment: fixed;
}
[data-testid="stHeader"] { background: transparent; }

html, body, [data-testid="stApp"] p, [data-testid="stApp"] li { font-family: 'Figtree', sans-serif; }
h1, h2, h3 { font-family: 'Chakra Petch', sans-serif !important; letter-spacing: 0.01em; }

.hero-title {
    font-family: 'Chakra Petch', sans-serif;
    font-weight: 700;
    font-size: clamp(2.2rem, 6vw, 3.4rem);
    line-height: 1.05;
    margin: 0.4rem 0 0.6rem;
    background: linear-gradient(90deg, #FFB347, #FF7A2E 45%, #FF4F8B);
    -webkit-background-clip: text;
    background-clip: text;
    color: transparent;
}
.trace {
    height: 2px;
    width: 100%;
    background: linear-gradient(90deg, #FFB347, #FF7A2E 40%, #FF4F8B 75%, transparent);
    box-shadow: 0 0 12px rgba(255,122,46,0.8);
    margin-bottom: 0.9rem;
}
.lede { color: #D9C4B4; font-size: 1.05rem; max-width: 60ch; }
.meta { color: #A8968A; font-size: 0.9rem; }

.story {
    border-left: 3px solid var(--c);
    padding: 0.2rem 0 0.2rem 1rem;
    margin: 1.4rem 0;
}
.chip {
    display: inline-block;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--c);
    border: 1px solid var(--c);
    border-radius: 999px;
    padding: 0.05rem 0.6rem;
    margin-bottom: 0.35rem;
}
.story a {
    font-family: 'Chakra Petch', sans-serif;
    font-size: 1.15rem;
    color: #F6E7D8 !important;
    text-decoration: none;
}
.story a:hover, .story a:focus { color: var(--c) !important; text-decoration: underline; }
.story .src { color: #A8968A; font-size: 0.85rem; margin: 0.15rem 0 0.4rem; }
.story .sum { color: #E6D3C3; line-height: 1.6; }

button[data-baseweb="tab"] p { font-family: 'Chakra Petch', sans-serif; font-size: 1rem; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------
st.markdown('<div class="hero-title">Security News Digest</div><div class="trace"></div>',
            unsafe_allow_html=True)
st.markdown('<p class="lede">This week\'s cybersecurity news, collected from trusted '
            'sources and summarized by AI. Read the briefing, browse the stories, '
            'or ask questions.</p>', unsafe_allow_html=True)


# ---------------------------------------------------------------------
# Building the briefing
# ---------------------------------------------------------------------
def build_briefing():
    with st.status("Building this week's briefing...", expanded=True) as status:
        st.write("Collecting news from 3 sources")
        articles = digest.fetch_articles()

        st.write(f"Found {len(articles)} articles, removing duplicate stories")
        articles = digest.remove_duplicates(articles)

        st.write(f"Summarizing {len(articles)} stories")
        progress = st.progress(0.0)
        for i, a in enumerate(articles):
            a["category"] = digest.categorize(a)
            a["summary"] = digest.summarize(a)
            progress.progress((i + 1) / len(articles))

        st.write("Writing the briefing")
        briefing = digest.write_briefing(articles)
        with open("briefing.md", "w", encoding="utf-8") as f:
            f.write(briefing)

        status.update(label="Briefing ready", state="complete", expanded=False)

    st.session_state.articles = articles
    st.session_state.briefing = briefing
    st.session_state.built_at = datetime.now()
    st.session_state.chat = []


if "articles" not in st.session_state:
    st.write("")
    st.write("No briefing yet. Building one takes a few minutes.")
    if st.button("Build this week's briefing", type="primary"):
        build_briefing()
        st.rerun()
    st.stop()

articles = st.session_state.articles
sources = len({a["source"] for a in articles})
st.markdown(f'<p class="meta">{len(articles)} stories from {sources} sources, '
            f'built {st.session_state.built_at:%A %d %B, %H:%M}</p>', unsafe_allow_html=True)

briefing_tab, stories_tab, ask_tab = st.tabs(["Briefing", "Stories", "Ask"])

# ---------------------------------------------------------------------
# Tab 1: the briefing
# ---------------------------------------------------------------------
with briefing_tab:
    st.markdown(st.session_state.briefing)
    st.write("")
    if st.button("Rebuild with the latest news"):
        build_briefing()
        st.rerun()

# ---------------------------------------------------------------------
# Tab 2: every story, filterable by category
# ---------------------------------------------------------------------
with stories_tab:
    found = [c for c in CATEGORY_COLORS if any(a["category"] == c for a in articles)]
    choice = st.radio("Show", ["All"] + found, horizontal=True, label_visibility="collapsed")

    for a in articles:
        if choice != "All" and a["category"] != choice:
            continue
        color = CATEGORY_COLORS[a["category"]]
        st.markdown(f"""
<div class="story" style="--c:{color}">
  <span class="chip">{html.escape(a['category'])}</span><br>
  <a href="{html.escape(a['link'])}" target="_blank">{html.escape(a['title'])}</a>
  <div class="src">{html.escape(a['source'])}</div>
  <div class="sum">{html.escape(a['summary'])}</div>
</div>""", unsafe_allow_html=True)

# ---------------------------------------------------------------------
# Tab 3: chat about the news
# ---------------------------------------------------------------------
with ask_tab:
    for msg in st.session_state.chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    question = None
    if not st.session_state.chat:
        st.write("Try one of these, or type your own question below.")
        examples = ["What was the most serious threat this week?",
                    "Explain this week's ransomware news simply",
                    "How can I protect myself from these attacks?"]
        for col, example in zip(st.columns(3), examples):
            if col.button(example, use_container_width=True):
                question = example

    typed = st.chat_input("Ask about this week's news")
    question = typed or question

    if question:
        st.session_state.chat.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                messages = [digest.chat_instructions(articles)] + st.session_state.chat
                answer = digest.ask_llm(messages)
            st.markdown(answer)
        st.session_state.chat.append({"role": "assistant", "content": answer})
        st.rerun()
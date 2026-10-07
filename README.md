<div align="center">

# 🛡️ Security News Digest

**This week's cybersecurity news, summarized by AI. Read it, browse it, ask it.**

![Python](https://img.shields.io/badge/Python-3.10+-FF7A2E?style=flat-square&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-app-FF4F8B?style=flat-square&logo=streamlit&logoColor=white)
![Groq](https://img.shields.io/badge/LLM-Groq_API-FFB347?style=flat-square)

</div>

---

## 💡 What it is

A web app that collects the latest cybersecurity news, summarizes it with an LLM, and lets you chat with it to ask questions about the week's threats.

```
📰 News feeds  →  🧹 Clean  →  🔁 Remove duplicates  →  🏷️ Categorize  →  🤖 Summarize  →  💬 Chat
```

## 🎯 What it solves

Security news is scattered across many sites, and the same story often gets reported several times. Keeping up takes a lot of time. This app pulls it all into one place, removes duplicates, sorts stories by threat type, and turns them into a short, beginner-friendly briefing.

## ⚙️ Setup

**1. Create and activate a virtual environment**
```
python -m venv venv
venv\Scripts\activate
```

**2. Install the libraries**
```
pip install -r requirements.txt
```

**3. Add your API key**

Get a free key from [console.groq.com](https://console.groq.com) and put it in a `.env` file:
```
GROQ_API_KEY=your_key_here
```

## 🚀 Run

```
streamlit run app.py
```

Click **Build this week's briefing**, then explore:

| Tab | What you get |
|---|---|
| 📋 **Briefing** | A short weekly summary of the top threats |
| 📰 **Stories** | Every article, filterable by category |
| 💬 **Ask** | Chat about this week's news |

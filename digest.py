# Security News Digest - the "engine" (Hugging Face version)
# app.py imports these functions. You can still run this file on its own
# for the terminal version:  python digest.py

import os
import re
import time
import feedparser
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()                                            # loads HF_TOKEN from .env
client = InferenceClient(api_key=os.getenv("HF_TOKEN"))  # connects to Hugging Face

MODELS = [
    "meta-llama/Llama-3.1-8B-Instruct",   # main model
    "Qwen/Qwen2.5-7B-Instruct",           # backup 1
    "openai/gpt-oss-20b",                 # backup 2
]

FEEDS = {
    "The Hacker News": "https://feeds.feedburner.com/TheHackersNews",
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/",
    "Krebs on Security": "https://krebsonsecurity.com/feed/",
}

KEYWORDS = {
    "Ransomware": ["ransomware", "ransom"],
    "Vulnerability": ["vulnerability", "cve", "zero-day", "patch", "exploit", "flaw"],
    "Data Breach": ["breach", "leak", "exposed"],
    "Phishing": ["phishing", "scam"],
    "Malware": ["malware", "trojan", "botnet", "backdoor"],
}


# ---- Step 1: Collect articles ----
def fetch_articles():
    articles = []
    for source, url in FEEDS.items():
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            text = re.sub(r"<[^>]+>", " ", entry.get("summary", ""))
            text = re.sub(r"\s+", " ", text).strip()
            articles.append({
                "source": source,
                "title": entry.title,
                "link": entry.get("link", ""),
                "text": text[:1500],
            })
    return articles


# ---- Step 2: Remove duplicate stories ----
def remove_duplicates(articles):
    texts = [a["title"] + " " + a["text"] for a in articles]
    similarity = cosine_similarity(TfidfVectorizer(stop_words="english").fit_transform(texts))
    unique = []
    for i in range(len(articles)):
        if all(similarity[i][j] < 0.5 for j in unique):
            unique.append(i)
    return [articles[i] for i in unique]


# ---- Step 3: Categorize ----
def categorize(article):
    text = (article["title"] + " " + article["text"]).lower()
    for category, words in KEYWORDS.items():
        if any(w in text for w in words):
            return category
    return "Other"


# ---- Step 4: Talk to the LLM ----
def ask_llm(messages):
    for attempt in range(3):                      # up to 3 rounds
        for model in MODELS:                      # try each model in turn
            try:
                response = client.chat.completions.create(
                    model=model, messages=messages, max_tokens=1000)
                return response.choices[0].message.content
            except Exception as error:
                print(f"  {model} failed: {str(error)[:80]}")
        time.sleep(10)                            # wait, then try the list again
    return "Not available (the AI service was busy, try again in a minute)."


def summarize(article):
    return ask_llm([{
        "role": "user",
        "content": "Summarize this cybersecurity news in 2 sentences. "
                   "Only use facts from the text.\n\n" + article["title"] + "\n" + article["text"],
    }])


# ---- Step 5: Write the weekly briefing ----
def summaries_text(articles):
    return "\n".join(f"[{a['category']}] {a['title']}: {a['summary']}" for a in articles)


def write_briefing(articles):
    return ask_llm([{
        "role": "user",
        "content": "Write a short weekly cybersecurity briefing for beginners using these news "
                   "summaries. Group them by category, start with the most serious threats, and "
                   "end with 3 safety tips.\n\n" + summaries_text(articles),
    }])


# ---- Step 6: Chat ----
def chat_instructions(articles):
    return {
        "role": "system",
        "content": "You are a friendly cybersecurity assistant for beginners. Answer questions "
                   "using only this week's news below. If the answer is not in the news, say so. "
                   "Keep answers short and simple.\n\n" + summaries_text(articles),
    }


# ---- Terminal version (runs only when you type: python digest.py) ----
if __name__ == "__main__":
    articles = remove_duplicates(fetch_articles())
    print("Unique articles:", len(articles))
    for a in articles:
        print("Summarizing:", a["title"])
        a["category"] = categorize(a)
        a["summary"] = summarize(a)

    briefing = write_briefing(articles)
    with open("briefing.md", "w", encoding="utf-8") as f:
        f.write(briefing)
    print("\n" + briefing)

    messages = [chat_instructions(articles)]
    print("\nAsk me anything about this week's news! Type 'quit' to stop.")
    while True:
        question = input("\nYou: ")
        if question.lower() in ["quit", "exit"]:
            break
        messages.append({"role": "user", "content": question})
        answer = ask_llm(messages)
        messages.append({"role": "assistant", "content": answer})
        print("Bot:", answer)
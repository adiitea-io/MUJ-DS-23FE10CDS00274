

import os
import re
import time
import feedparser
from dotenv import load_dotenv
from groq import Groq
from datetime import datetime
from prompts import SUMMARY_PROMPT, BRIEFING_PROMPT, CHAT_PROMPT
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()                                           
client = Groq(api_key=os.getenv("GROQ_API_KEY"))  # connects to Groq

MODELS = [
    "openai/gpt-oss-20b",        # main model
    "openai/gpt-oss-120b",       # backup 1 (bigger, smarter)
    "llama-3.1-8b-instant",      # backup 2 (small and fast)
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
        for entry in feed.entries[:5]:  # limit to 5 articles per source to avoid overwhelming the LLM
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


# ---- Step 3: Categorize ---- rule -based classification 
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
                    model=model, messages=messages, max_tokens=4000)
                return response.choices[0].message.content
            except Exception as error:
                print(f"  {model} failed: {str(error)[:80]}")
        time.sleep(10)                            # wait, then try the list again
    return "Not available (the AI service was busy, try again in a minute)."


def summarize(article):
    prompt = SUMMARY_PROMPT.format(title=article["title"], text=article["text"])
    return ask_llm([{"role": "user", "content": prompt}])


# ---- Step 5: Write the weekly briefing ----
def summaries_text(articles): # gathering the already generated summaries for llm input , like a box 
    return "\n".join(f"[{a['category']}] {a['title']}: {a['summary']}" for a in articles)


def write_briefing(articles):
    prompt = BRIEFING_PROMPT.format(
        date=datetime.now().strftime("%d %B %Y"),
        summaries=summaries_text(articles),
    )
    return ask_llm([{"role": "user", "content": prompt}])
 


# ---- Step 6: Chat ----
def chat_instructions(articles):
    prompt = CHAT_PROMPT.format(summaries=summaries_text(articles))
    return {"role": "system", "content": prompt}


# ---- Terminal version (runs only when you type: python digest.py) using it for finding errors ----
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
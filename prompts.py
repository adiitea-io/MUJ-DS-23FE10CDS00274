

# Used once per article to write a short summary.
SUMMARY_PROMPT = """Summarize this cybersecurity news in 2 sentences.
Only use facts from the text.

{title}
{text}"""


# Used once per build to turn all the summaries into the weekly briefing.
BRIEFING_PROMPT = """Write a short weekly cybersecurity briefing for beginners using these news summaries.
Group them by category, start with the most serious threats, and end with 3 safety tips.
Today's date is {date}; use it if you mention a date, and don't invent any other dates.

{summaries}"""


# The system message for the chatbot. It sets the bot's role and rules for the whole conversation.
CHAT_PROMPT = """You are a friendly cybersecurity assistant for beginners.
Answer questions using only this week's news below. If the answer is not in the news, say so.
Keep answers short and simple.

{summaries}"""
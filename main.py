import requests
from langchain.chat_models import init_chat_model
from send_email import send_email
from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
NEWS_API_KEY=os.getenv("NEWS_API_KEY")


url = ("https://newsapi.org/v2/top-headlines?"
        "country=us&category=business&"
        "apiKey=" + NEWS_API_KEY
        )


request = requests.get(url)

content = request.json()

articles = content['articles']
#print(articles)



# AI Summarizing the news

model = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google-genai",
    api_key = GOOGLE_API_KEY
)

prompt = f"""
You are a news summarizer. 
write a short paragraph analyzing those news
and tell me how they affect the stock market.
Here are the news articles:
{articles}
"""
response = model.invoke(prompt)
response_str = response.content

#print(response_str)

body = "Subject: News Summary\n\n" + response_str + "\n\n"
body = body.encode("utf-8")

send_email(body)
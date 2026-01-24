import requests
from bs4 import BeautifulSoup
from feedparser import parse
from transformers import pipeline
from openai import OpenAI
from config import API_KEYS, KEYWORDS, SENTIMENT_MODEL, UNIVERSE_FILTER
import time
import re  # For extract tickers

def scan_news_catalysts():
    for attempt in range(3):
        try:
            url = 'https://finance.yahoo.com/news'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            news = [h.text for h in soup.find_all('h3')]

            rss = parse('https://finance.yahoo.com/rss/earnings')

            grok = OpenAI(api_key=API_KEYS['GROK'], base_url="https://api.x.ai/v1")
            prompt = "Semantic search for small caps catalysts and keyword search for " + ', '.join(KEYWORDS) + " return list of 20 tickers <2B market cap no OTC"
            grok_result = grok.chat.completions.create(
                model="grok-4-1-fast-reasoning",
                messages=[{"role": "user", "content": prompt}]
            ).choices[0].message.content

            # Extract tickers from grok_result (uppercase 3-4 letters)
            tickers = re.findall(r'\b[A-Z]{3,4}\b', grok_result)  # Real extract
            tickers = list(set(tickers))  # Unique

            sentiment = pipeline("sentiment-analysis", model=SENTIMENT_MODEL)
            scores = [sentiment(text)[0]['score'] for text in news]

            # Merge + filter
            results = {
                'tickers': tickers,
                'news': news,
                'catalyst_urgency': 0.7,  # Sim, replace with real
                'market_cap': 1.2e9,  # Sim, replace with yf.info
                'ticker': tickers[0] if tickers else 'ROLR'  # Fallback
            }
            return results
        except Exception as e:
            print(f"Error scan: {e} – Retry {attempt+1}")
            time.sleep(5)
    return {'tickers': ['ROLR'], 'news': [], 'catalyst_urgency': 0.5, 'market_cap': 1.2e9, 'ticker': 'ROLR'}

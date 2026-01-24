import pandas as pd
from openai import OpenAI
from xgboost import XGBClassifier
from config import API_KEYS, THRESHOLDS, MARKET_REGIMES
import yfinance as yf
import re

def score_rank(data):
    grok = OpenAI(api_key=API_KEYS['GROK'], base_url="https://api.x.ai/v1")

    # Adaptive regime
    regime_prompt = "detect market regime: bull or bear return 'bull' or 'bear'"
    regime = grok.chat.completions.create(
        model="grok-4-1-fast-reasoning",
        messages=[{"role": "user", "content": regime_prompt}]
    ).choices[0].message.content.strip()
    catalyst_weight = MARKET_REGIMES.get(regime, {'catalyst_weight': 0.4})['catalyst_weight']

    # Grok sentiment and prob - parse to float
    sentiment_prompt = "sentiment analysis on " + str(data['news']) + " return score as float 0-1"
    sentiment_response = grok.chat.completions.create(
        model="grok-4-1-fast-reasoning",
        messages=[{"role": "user", "content": sentiment_prompt}]
    ).choices[0].message.content

    prob_prompt = "calc prob gain return float 0-1"
    prob_response = grok.chat.completions.create(
        model="grok-4-1-fast-reasoning",
        messages=[{"role": "user", "content": prob_prompt}]
    ).choices[0].message.content

    # Parse to float
    try:
        grok_sentiment = float(re.search(r'\d+\.?\d*', sentiment_response).group())
        grok_prob = float(re.search(r'\d+\.?\d*', prob_response).group())
    except (AttributeError, ValueError, TypeError):
        grok_sentiment = 0.5
        grok_prob = 0.5
    grok_score = (grok_sentiment + grok_prob) / 2

    # ML XGBoost
    model = XGBClassifier()
    ml_score = 0.8  # Sim

    # Hybride score
    score = 0.3 * grok_score + catalyst_weight * ml_score + 0.3 * data.get('catalyst_urgency', 0.5)
  
    # Rank + filter <2B no OTC with real market_cap from yf.info
    ranked = pd.DataFrame({
        'ticker': data.get('tickers', ['ROLR']),
        'score': [score] * len(data.get('tickers', ['ROLR']))
    })
    # Get real market_cap
    ranked['market_cap'] = ranked['ticker'].apply(lambda t: yf.Ticker(t).info.get('marketCap', 1e10))
    ranked = ranked[ranked['market_cap'] < 2e9]
    ranked = ranked[~ranked['ticker'].str.endswith('.O')]
    ranked = ranked.sort_values('score', ascending=False)

    return ranked

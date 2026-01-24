API_KEYS = {
    'GROK': 'ici',
    'FINNHUB': 'ici',
    'HUGGINGFACE': 'ici',
    'TELEGRAM_TOKEN': 'ici',
    'TELEGRAM_CHAT_ID': 'ici'
}

KEYWORDS = ['FDA', 'earnings', 'merger', 'contract', 'partnership', 'guidance', 'upgrade', 'SEC filing']

THRESHOLDS = {'score': 0.6, 'gain': 30, 'rvol': 2, 'atr': 10}

SENTIMENT_MODEL = 'ProsusAI/finbert'  # Finance-specific upgrade
TELEGRAM_ENABLE = True  # False to disable
UNIVERSE_FILTER = {'max_market_cap': 2e9, 'max_price': 20, 'min_volume': 1e6}
MARKET_REGIMES = {'bull': {'catalyst_weight': 0.5}, 'bear': {'catalyst_weight': 0.3}}  # For adaptive scoring







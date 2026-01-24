import argparse
from src.scanner import scan_news_catalysts
from src.historical import update_historical
from src.scoring_rank import score_rank
from config import TELEGRAM_ENABLE, API_KEYS
import telebot  # If TELEGRAM_ENABLE

parser = argparse.ArgumentParser()
parser.add_argument('command', choices=['scan', 'train', 'backtest', 'feedback'])
args = parser.parse_args()

if args.command == 'scan':
    data = scan_news_catalysts()
    historical = update_historical(data['tickers'])
    ranked = score_rank(data)
    ranked.to_csv('data/watchlist.csv')
    print(ranked)  # Terminal output

    if TELEGRAM_ENABLE:
        bot = telebot.TeleBot(API_KEYS['TELEGRAM_TOKEN'])
        bot.send_message(API_KEYS['TELEGRAM_CHAT_ID'], str(ranked))

elif args.command == 'feedback':
    # Call feedback from scoring_rank.py
    print("Feedback on misses...")











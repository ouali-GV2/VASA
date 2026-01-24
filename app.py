import streamlit as st
import os
from src.scanner import scan_news_catalysts
from src.historical import update_historical
from src.scoring_rank import score_rank
from config import TELEGRAM_ENABLE, API_KEYS
import telebot

st.title("V2S Dashboard - GV2")

if st.button("Run Scan"):
    data = scan_news_catalysts()
    historical = update_historical(data['tickers'])
    ranked = score_rank(data)
    ranked.to_csv('data/watchlist.csv')
    st.dataframe(ranked)  # Display ranked table
    st.write("Watchlist saved!")

    if TELEGRAM_ENABLE:
        bot = telebot.TeleBot(API_KEYS['TELEGRAM_TOKEN'])
        bot.send_message(API_KEYS['TELEGRAM_CHAT_ID'], str(ranked))
        st.success("Telegram sent!")

if st.button("Train ML"):
    os.system("python gv2.py train")
    st.success("Training done!")

if st.button("Backtest"):
    os.system("python gv2.py backtest --watchlist")
    st.success("Backtest done!")

# Add graphs if need : st.line_chart(ranked['score'])

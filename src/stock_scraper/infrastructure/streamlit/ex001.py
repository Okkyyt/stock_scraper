import asyncio
import pandas as pd

import nest_asyncio
import streamlit as st

from stock_scraper.infrastructure.db.fetch import fetch_stock_price

nest_asyncio.apply()


@st.cache_data
def load_data(symbol)-> pd.DataFrame:
    return asyncio.run(fetch_stock_price(symbol, '1d'))

# Streamlit UI
st.title("Stock-Scraper Dashboard")
st.sidebar.title("Stock-Scraper Dashboard")

# 読み込む株価(symbol_idを選択する)
symbol = st.sidebar.text_input("Enter Symbol ID", value="AAPL")
# データ読み込み
stock_df = load_data(symbol)

# 表示
st.subheader("Symbol Data")
st.dataframe(stock_df)

# CMD
# streamlit run <>

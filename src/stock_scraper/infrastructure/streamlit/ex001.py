import asyncio

import nest_asyncio
import streamlit as st

from stock_scraper.infrastructure.db.fetch_stock_instanse import fetch_stock_instance

nest_asyncio.apply()


@st.cache_data
def load_data(symbol_id):
    result = asyncio.run(fetch_stock_instance(symbol_id))
    return (
        result["symbol_data"],
        result["symbol_meta_price"],
        result["symbol_indicator_price"],
    )


# Streamlit UI
st.title("Stock-Scraper Dashboard")
st.sidebar.title("Stock-Scraper Dashboard")

# 読み込む株価(symbol_idを選択する)
symbol_id = st.sidebar.text_input("Enter Symbol ID", value="AAPL")
# データ読み込み
symbol_data, symbol_meta_price, symbol_indicator_price = load_data(symbol_id)

# 表示
st.subheader("Symbol Data")
st.dataframe(symbol_data)

st.subheader("Meta Price Data")
st.dataframe(symbol_meta_price)

st.subheader("Indicator Price Data")
st.dataframe(symbol_indicator_price)

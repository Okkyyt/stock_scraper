import os

import aiohttp
from dotenv import load_dotenv

from ..scraping import get_aiohttp

load_dotenv()

ALPHAVANTAGE_API_KEY = os.getenv("ALPHAVANTAGE_API_KEY")


class AlphaVantage:
    # セッション、ウェブソケットの作成
    async def create_session(self):
        return aiohttp.ClientSession()

    # スクレイピングurlの作成、メッセージの作成
    def preprocess(self, stock_instance):
        # url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_instance.symbol_name}&interval={stock_instance.interval}&apikey={ALPHAVANTAGE_API_KEY}"
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo'
        return url

    # スクレイピングの実行
    async def scraping(self, session, url):
        return await get_aiohttp(session, url)

    # 取得したデータの整形
    def postprocess(self, response):
        print(type(response))
        pass

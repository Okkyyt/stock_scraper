from datetime import datetime, timezone

import aiohttp

from ..base_scraper import Scraper
from ..scraping import get_aiohttp


class YahooFinance(Scraper):
    # セッション、ウェブソケットの作成
    async def create_session(self):
        return aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15))

    # スクレイピングurlの作成、メッセージの作成
    def preprocess(self, cli_instance):
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{cli_instance.symbol}?interval={cli_instance.interval}"
        return url

    # スクレイピングの実行
    async def scraping(self, session, url):
        return await get_aiohttp(session, url)

    # 取得したデータの整形
    def postprocess(self, res):
        # metaとindicatorsの情報
        indicators = res["chart"]["result"][0]["indicators"]["quote"][0]
        meta = res["chart"]["result"][0]["meta"]

        # 時刻
        timestamp_list = res["chart"]["result"][0]["timestamp"]

        datetime_utc_list = [
            datetime.fromtimestamp(timestamp, tz=timezone.utc)
            for timestamp in timestamp_list
        ]
        date_id_list = [
            int(datetime_utc.strftime("%Y%m%d")) for datetime_utc in datetime_utc_list
        ]
        time_id_list = [
            int(datetime_utc.strftime("%H%M%S")) for datetime_utc in datetime_utc_list
        ]

        indicator_stock_price = {
            "open": indicators["open"],
            "close": indicators["close"],
            "high": indicators["high"],
            "low": indicators["low"],
            "volume": indicators["volume"],
        }
        meta_stock_price = {
            "regularMarketTime": meta["regularMarketTime"],
            "regularMarketPrice": meta["regularMarketPrice"],
        }

        print(f"indicators: {indicator_stock_price}")
        print(f"meta: {meta_stock_price}")

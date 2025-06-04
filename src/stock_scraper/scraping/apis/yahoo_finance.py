from datetime import datetime, timezone
import aiohttp
from stock_scraper.domain.schemas import PriceSnapshot, Indicators

class YahooFinance:
    # セッション、ウェブソケットの作成
    async def create_session(self):
        return aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15))

    # スクレイピングurlの作成、メッセージの作成
    def preprocess(self, cli_instance):
        return f"https://query1.finance.yahoo.com/v8/finance/chart/{cli_instance.symbol}?interval={cli_instance.interval}"

    # スクレイピングの実行
    async def scraping(self, session, url):
        HEADERS = {
            "User-Agent": "Mozilla/5.0 (compatible; Bot/0.1)",
            "Accept": "application/json, text/plain, */*",
        }
        try:
            async with session.get(url, headers=HEADERS) as res:
                print(f"ステータス：{res.status}")
                return await res.json()
        except Exception as e:
            print(f"Error occurred: {e}")
            return None


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

        return PriceSnapshot(
            market_time=datetime_utc_list,
            tick_price=meta["regularMarketPrice"],
            indicators=Indicators(
                open=indicators["open"],
                close=indicators["close"],
                high=indicators["high"],
                low=indicators["low"],
                volume=indicators["volume"]
            ),
        )
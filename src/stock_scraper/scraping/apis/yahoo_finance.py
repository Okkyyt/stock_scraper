from datetime import datetime, timezone
import aiohttp
from stock_scraper.domain.schemas import PriceSnapshot, Indicators, FetchMeta


class YahooFinance:
    # セッション、ウェブソケットの作成
    async def create_session(self):
        return aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15))

    # スクレイピングurlの作成、メッセージの作成
    def preprocess(self, cli_instance):
        # s, m, h, d, w, mo 型にする
        def format_timedelta(td):
            total_seconds = int(td.total_seconds())

            if total_seconds % (7 * 24 * 3600) == 0:
                return f"{total_seconds // (7 * 24 * 3600)}w"
            elif total_seconds % (24 * 3600) == 0:
                return f"{total_seconds // (24 * 3600)}d"
            elif total_seconds % 3600 == 0:
                return f"{total_seconds // 3600}h"
            elif total_seconds % 60 == 0:
                return f"{total_seconds // 60}m"
            else:
                return f"{total_seconds}s"

        interval = format_timedelta(cli_instance.interval)
        return f"https://query1.finance.yahoo.com/v8/finance/chart/{cli_instance.symbol}?interval={interval}"

    # スクレイピングの実行
    async def scraping(self, session, url):
        HEADERS = {
            "User-Agent": "Mozilla/5.0 (compatible; Bot/0.1)",
            "Accept": "application/json, text/plain, */*",
        }
        start_time = datetime.now(timezone.utc)
        status_code = None
        err_msg = None
        try:
            async with session.get(url, headers=HEADERS) as res:
                status_code = res.status
                if status_code == 200:
                    data = await res.json()
                else:
                    data = None
                    err_msg = await res.json()
        except Exception as e:
            print(f"Error occurred: {e}")
            err_msg = await str(e)
            data = None
        finally:
            end_time = datetime.now(timezone.utc)
        return data, FetchMeta(
            crawl_started_at=start_time,
            fetched_at=end_time,
            status_code=status_code,
            error_msg=err_msg,
        )

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
                volume=indicators["volume"],
            ),
        )

from datetime import datetime, timezone

import aiohttp

from stock_scraper.domain.schemas import FetchMeta, PriceSnapshot
from stock_scraper.domain.time_period import revert_time_period


class YahooFinance:
    # セッション、ウェブソケットの作成
    async def create_session(self):
        return aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15))

    # スクレイピングurlの作成、メッセージの作成
    def preprocess(self, cli_instance):
        time_map = {"day": "d", "hour": "h", "minute": "m", "second": "s"}
        interval = revert_time_period(cli_instance.interval, time_map)
        range_ = revert_time_period(cli_instance.range_, time_map)
        return f"https://query1.finance.yahoo.com/v8/finance/chart/{cli_instance.symbol}?interval={interval}&range={range_}"

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

        # indicatorsの情報
        indicators = res["chart"]["result"][0]["indicators"]["quote"][0]

        # 時刻
        timestamp_list = res["chart"]["result"][0]["timestamp"]

        datetime_utc_list = [
            datetime.fromtimestamp(timestamp, tz=timezone.utc)
            for timestamp in timestamp_list
        ]

        snapshots: list[PriceSnapshot] = []

        for i, ts in enumerate(datetime_utc_list):
            snapshots.append(
                PriceSnapshot(
                    market_time=ts,
                    open=indicators["open"][i],
                    close=indicators["close"][i],
                    high=indicators["high"][i],
                    low=indicators["low"][i],
                    volume=indicators["volume"][i],
                )
            )
        return snapshots

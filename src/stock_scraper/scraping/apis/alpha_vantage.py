import aiohttp

from ..scraping import get_aiohttp


class AlphaVantage:
    # セッション、ウェブソケットの作成
    def create_session(self):
        return aiohttp.ClientSession()

    # スクレイピングurlの作成、メッセージの作成
    def preprocess(self, stock_instance):
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock_instance.symbol_name}&interval={stock_instance.interval}&apikey=YOUR_API_KEY"
        return url

    # スクレイピングの実行
    async def scraping(self, session, url):
        return await get_aiohttp(session, url)

    # 取得したデータの整形
    def postprocess(self, response):
        # ここでレスポンスを整形する処理を実装
        # 例: JSON形式のレスポンスを辞書型に変換
        return response.json()

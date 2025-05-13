import asyncio

from stock_scraper.api.set_stock_instance import set_stock_instance

# インスタンスの作成
stock_instance = set_stock_instance("AAPL", "1d", "max")


async def get_history_price(stock_instance):
    """
    スクレイピングを実行する関数
    """


asyncio.run(get_history_price(stock_instance))

import asyncio

from stock_scraper.api.set_stock_instance import set_stock_instance
from stock_scraper.config_loader import load_stock_config

config_json = load_stock_config("config/stock_list.json")
symbol_list = list(config_json["symbols"].keys())
print(symbol_list)

# インスタンスの作成
stock_instance = set_stock_instance("AAPL", "1d", "max")


async def get_history_price(stock_instance):
    """
    スクレイピングを実行する関数
    """


asyncio.run(get_history_price(stock_instance))

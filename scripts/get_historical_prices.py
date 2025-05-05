import aiohttp
import asyncio

from stock_scraper.api.set_stock_instance import set_stock_instance
from stock_scraper.api.set_stock_features import set_stock_features
from stock_scraper.usecase.scraping import get_aiohttp
from stock_scraper.infrastructure.db.insert_stock_instanse import insert_stocke_instance

# インスタンスの作成
stock_instance = set_stock_instance("AAPL", "1d", "max")

async def get_history_price(stock_instance):
    """
    スクレイピングを実行する関数
    """
    # aiohttpセッションを作成
    session = aiohttp.ClientSession()
    # スクレイピングを実行
    res = await get_aiohttp(session, stock_instance.url)
    await session.close()
    print(f'スクレイピング結果: {res}')
    # スクレイピング結果の挿入
    stock_instance_copy = set_stock_features(stock_instance, res)
    print(f"株価情報🚀: {stock_instance_copy}")
    # DBに保存
    await insert_stocke_instance(stock_instance_copy)


asyncio.run(get_history_price(stock_instance))
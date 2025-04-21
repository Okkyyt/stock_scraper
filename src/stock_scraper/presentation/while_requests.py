import asyncio
import aiohttp

from ..usecase.get_save_stock_price import get_save_stockPrice

# n秒ごとにリクエストを送りレスポンスを保存する

async def while_request_session(DataclassStock):
    print(DataclassStock)
    interval = 60
    print(DataclassStock.symbol_id)
    async with aiohttp.ClientSession() as session:
        while True:
            asyncio.create_task(get_save_stockPrice(session, DataclassStock))
            # 指定したインターバルで待機
            await asyncio.sleep(interval)
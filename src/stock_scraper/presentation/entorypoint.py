from ..domain.models.stock_models import DataclassStock
from ..config_loader import load_stock_config
from ..domain.factory.dataclass_stock_factory import set_dataclassStock_item
from .while_requests import while_request_session

import asyncio

def stock_presentation():
    stock_list = load_stock_config()

    # 並行処理
    async def concurrency():
        tasks = [
            while_request_session(set_dataclassStock_item(stock_item))
            for stock_item in stock_list['items']
        ]
        await asyncio.gather(*tasks)

    asyncio.run(concurrency())

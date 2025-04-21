from ..infrastructure.get_stockPrice import get_aiohttp
from ..domain.services.set_stock_features import set_stock_features

async def get_save_stockPrice(session, DataclassStock):
    res = await get_aiohttp(session, DataclassStock.url)
    print(res)
    if res is not None:
        print(f"Response_error: {res['chart']['error']}")
    else:
        print("No response received.")

    DataclassStock_ = set_stock_features(DataclassStock, res)
    print(f'DataclassStock: {DataclassStock_.feature_}')

    # DBに保存

    # 初期化
    res = None
    DataclassStock_ = None



    
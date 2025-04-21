from ...infrastructure.url_builder import build_yahoo_url
from ..models.stock_models import DataclassStock 

def set_dataclassStock_item(stock_item):
    symbol = stock_item['symbol']
    name = stock_item['name']
    source = stock_item['source']
    url = ""

    if source == 'yahoo':
        url = build_yahoo_url(symbol, interval="1m", range="1d")

    return DataclassStock(
        date_id=0,
        time_id=0,
        symbol_id=symbol,
        symbol_name=name,
        url=url,
        source=source,
        feature_={}
    )

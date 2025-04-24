from ..config_loader import load_stock_config
from ..domain.stock_model import DataclassStock
from ..usecase.url_builder import build_yahoo_url


def set_stock_instance(symbol: str):
    """
    銘柄情報をconfigから取得し, インスタンスの生成
    """
    # configから銘柄情報を取得
    stock_config = load_stock_config()
    # インスタンスの作成
    symbol_ = stock_config["symbols"][symbol]
    # スクレイピングソースからURLを作成
    interval = "1d"
    range_ = "1d"
    url = None
    if symbol_["source"] == "yahoo":
        url = build_yahoo_url(symbol, interval, range_)

    stock_instance = DataclassStock(
        date_id=None,
        time_id=None,
        symbol_id=symbol,
        symbol_name=symbol_["name"],
        url=url,
        source=symbol_["source"],
        feature_={},
    )
    return stock_instance

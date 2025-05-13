from ..config_loader import load_stock_config
from ..domain.stock_model import DataclassStock


def set_stock_instance(symbol: str, interval: str, range_: str) -> DataclassStock:
    """
    銘柄情報をconfigから取得し, インスタンスの生成
    """
    # configから銘柄情報を取得
    stock_config = load_stock_config()
    # インスタンスの作成
    symbol_ = stock_config["symbols"][symbol]

    # インスタンスを生成
    stock_instance = DataclassStock(
        date_id=None,
        time_id=None,
        symbol_id=symbol,
        symbol_name=symbol_["name"],
        url=None,
        interval=interval,
        source=symbol_["source"],
        feature_={},
    )
    return stock_instance

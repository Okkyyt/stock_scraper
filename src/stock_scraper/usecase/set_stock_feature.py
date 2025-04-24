def set_stock_features(stock_instance, res):
    # 最新のデータ(最後の値)を取得
    latest_index = -1

    # metaとindicatorsの情報
    indicators = res["chart"]["result"][0]["indicators"]["quote"][0]
    meta = res["chart"]["result"][0]["meta"]

    # 時刻
    datetime = res["chart"]["result"][0]["timestamp"][latest_index]

    indicator_stock_price = {
        "open": indicators["open"][latest_index],
        "close": indicators["close"][latest_index],
        "high": indicators["high"][latest_index],
        "low": indicators["low"][latest_index],
        "volume": indicators["volume"][latest_index],
    }
    meta_stock_price = {
        "regularMarketTime": meta["regularMarketTime"],
        "regularMarketPrice": meta["regularMarketPrice"],
    }

    print(f'datetime: {datetime}')
    print(f'indicators: {indicator_stock_price}')
    print(f'meta: {meta_stock_price}')

    stock_instance.feature_ = {
        "indicator": indicator_stock_price,
        "meta": meta_stock_price,
    }

    return stock_instance
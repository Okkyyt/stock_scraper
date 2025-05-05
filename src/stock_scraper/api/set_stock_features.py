from datetime import datetime, timezone


def set_stock_features(stock_instance, res):

    # metaとindicatorsの情報
    indicators = res["chart"]["result"][0]["indicators"]["quote"][0]
    meta = res["chart"]["result"][0]["meta"]

    # 時刻
    timestamp_list = res["chart"]["result"][0]["timestamp"]

    datetime_utc_list = [datetime.fromtimestamp(timestamp, tz=timezone.utc) for timestamp in timestamp_list]
    date_id_list = [int(datetime_utc.strftime("%Y%m%d")) for datetime_utc in datetime_utc_list]
    time_id_list = [int(datetime_utc.strftime("%H%M%S")) for datetime_utc in datetime_utc_list]

    indicator_stock_price = {
        "open": indicators["open"],
        "close": indicators["close"],
        "high": indicators["high"],
        "low": indicators["low"],
        "volume": indicators["volume"],
    }
    meta_stock_price = {
        "regularMarketTime": meta["regularMarketTime"],
        "regularMarketPrice": meta["regularMarketPrice"],
    }


    print(f"indicators: {indicator_stock_price}")
    print(f"meta: {meta_stock_price}")

    # stock_instanceに値をセット
    stock_instance.date_id = date_id_list
    stock_instance.time_id = time_id_list
    stock_instance.feature_ = {
        "indicator": indicator_stock_price,
        "meta": meta_stock_price,
    }

    return stock_instance

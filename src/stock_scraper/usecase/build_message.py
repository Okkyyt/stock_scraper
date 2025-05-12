def build_message(stock_instance):
    message = {
        "type": "subscribe",
        "symbol": stock_instance.symbol_name,
        "interval": stock_instance.interval,
    }
    return message
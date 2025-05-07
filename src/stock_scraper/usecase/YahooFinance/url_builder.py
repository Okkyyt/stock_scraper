def build_yahoo_url(symbol, interval, range_):
    return f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval={interval}&range={range_}"
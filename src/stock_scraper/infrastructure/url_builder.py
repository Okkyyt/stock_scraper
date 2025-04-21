def build_yahoo_url(symbol_id, **kwargs):
    interval = kwargs.get('interval')
    range_ = kwargs.get('range')
    return f'https://query1.finance.yahoo.com/v8/finance/chart/{symbol_id}?interval={interval}&range={range_}'
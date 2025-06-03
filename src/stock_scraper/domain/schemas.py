from __future__ import annotations

from datetime import datetime
from typing import Optional, Required, TypedDict


# Config---------------------------------------------------------------
class HasSymbol(TypedDict):
    symbol: Required[str]  # 'AAPL' など自然キー


class HasID(TypedDict):
    config_id: Required[int]  # サロゲートキー (SERIAL / BIGSERIAL)


# 銘柄情報---------------------------------------------------------------
class SymbolInfo(HasSymbol):
    exchange: str  # 'JPX', 'NASDAQ'
    currency: str  # 'JPY', 'USD'
    name: str
    timezone: str  # 'Asia/Tokyo'


# スクレイピング設定-------------------------------------------------
class FetchConfig(HasID, HasSymbol):
    source: str  # 'yahoo_finance'
    scraping_interval: str  # '5s'
    time_frame: str  # '1d'
    url: str  # エンドポイント


# 1回ごとのスクレイピング結果-------------------------------------------------
class Indicators(TypedDict):
    open: float
    close: float
    high: float
    low: float
    volume: int
    adjclose: Optional[float]


class FetchMeta(TypedDict, total=False):
    crawl_started_at: datetime
    fetched_at: datetime
    status_code: int
    error_msg: str  # Optional だけ total=False で許容


class PriceSnapshot(TypedDict):
    market_time: datetime  # 取引所時刻
    tick_price: float
    indicators: Indicators


class FetchHistory(HasID):
    meta: FetchMeta
    price: PriceSnapshot

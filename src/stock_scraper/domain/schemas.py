from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


# ── 共通ミックスイン ───────────────────────────
@dataclass(slots=True, frozen=True)
class HasSymbol:
    symbol: str


@dataclass(slots=True, frozen=True)
class HasID(HasSymbol):
    config_id: int


# ── 銘柄プロフィール ───────────────────────────
@dataclass(slots=True, frozen=True)
class SymbolInfo(HasSymbol):
    exchange: str
    currency: str
    name: str
    timezone: str


# ── CLI 設定 ──────────────────────────────────
@dataclass(slots=True, frozen=True)
class FetchConfig(HasID):
    source: str
    scraping_interval: str
    time_frame: str
    url: str


# ── 1 回分の結果 ───────────────────────────────
@dataclass(slots=True, frozen=True)
class Indicators:
    open: float
    close: float
    high: float
    low: float
    volume: int
    adjclose: Optional[float] = None


@dataclass(slots=True, frozen=True)
class FetchMeta:
    crawl_started_at: datetime
    fetched_at: datetime
    status_code: int
    error_msg: Optional[str] = None


@dataclass(slots=True, frozen=True)
class PriceSnapshot:
    market_time: datetime
    tick_price: float
    indicators: Indicators


@dataclass(slots=True, frozen=True)
class FetchHistory(HasID):
    status_meta: FetchMeta
    price: PriceSnapshot

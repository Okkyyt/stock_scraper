# src/stock_scraper/factories.py
from __future__ import annotations

import importlib
from typing import Any, Dict

from src.stock_scraper.config_loader import load_config
from src.stock_scraper.domain.schemas import FetchConfig, SymbolInfo

# ── 設定ファイル読込 ──────────────────────────────
_STOCK: Dict[str, Dict[str, Any]] = load_config("config/stock_list.json")
_MARKET: Dict[str, Dict[str, str]] = load_config("config/market_meta.json")


# ── 動的 import 用ヘルパ ─────────────────────────
def _import_scraper(source: str):
    """
    src/stock_scraper/scraping/apis/{source}.py にある
    PascalCase のクラスを返す
    """
    try:
        mod = importlib.import_module(f"src.stock_scraper.scraping.apis.{source}")
        cls = getattr(mod, "".join(w.capitalize() for w in source.split("_")))
        return cls()  # インスタンス化
    except ModuleNotFoundError as e:
        raise ImportError(f"Scraper module for '{source}' not found") from e
    except AttributeError as e:
        raise ImportError(f"Scraper class in '{source}' not found") from e


# ── 1) SymbolInfo ファクトリ ─────────────────────
def build_symbol_info(symbol: str) -> SymbolInfo:
    try:
        row = _STOCK[symbol]
    except KeyError as e:
        raise ValueError(f"Unknown symbol: {symbol}") from e

    exch = row["exchange"]
    meta = _MARKET.get(exch)
    if not meta:
        raise ValueError(f"Market meta not found for exchange '{exch}'")

    return SymbolInfo(
        symbol=symbol,
        exchange=exch,
        currency=meta["currency"],
        name=row["name"],
        timezone=meta["timezone"],
    )


# ── 2) FetchConfig ファクトリ ─────────────────────
def build_fetch_config(symbol: str, cli_conf) -> FetchConfig:
    row = _STOCK.get(symbol)
    if not row:
        raise ValueError(f"Unknown symbol: {symbol}")

    source = row["source"]
    scraping_interval = cli_conf.bins
    time_frame = cli_conf.interval or scraping_interval

    scraper = _import_scraper(source)

    # ユニークな ID を生成
    uid = f"{symbol}_{source}_{time_frame}"

    return FetchConfig(
        config_id=uid,
        symbol=symbol,
        source=source,
        scraping_interval=scraping_interval,
        time_frame=time_frame,
        url=scraper.preprocess(cli_conf),  # scraper 側で URL を構築してもらう
    )


# ── 3) スクレイパインスタンスだけ欲しい場合 ────────
def make_scraper(symbol: str):
    source = _STOCK[symbol]["source"]
    if not source:
        raise ValueError(f"Source not set for symbol '{symbol}'")
    return _import_scraper(source)

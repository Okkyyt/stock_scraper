from dataclasses import dataclass
from typing import Dict, TypedDict

class MetaDict(TypedDict):
    date_id: int  # 例: 20250414（yyyymmdd）
    time_id: int  # 例: 143000（hhmmss）
    symbol_id: str  # 例: "AAPL"
    symbol_name: str  # 例: "Apple"
    url: str  # 例: "https://query1.finance.yahoo.com/..."
    interval: str  # 例: "1d"
    source: str  # 例: "yahoo"

class IndicatorDict(TypedDict):
    open: float
    close: float
    high: float
    low: float
    volume: int

class FeatureDict(TypedDict):
    meta: MetaDict
    indicator: IndicatorDict

@dataclass
class DataclassStock:
    date_id: int  # 例: 20250414（yyyymmdd）
    time_id: int  # 例: 143000（hhmmss）
    symbol_id: str  # 例: "AAPL"
    symbol_name: str  # 例: "Apple"
    url: str  # 例: "https://query1.finance.yahoo.com/..."
    interval: str  # 例: "1d"
    source: str  # 例: "yahoo"
    feature_: FeatureDict  # 例: {"meta": {...}, "indicators": {...}}
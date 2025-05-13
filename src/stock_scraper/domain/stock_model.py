from dataclasses import dataclass
from typing import Dict


@dataclass
class DataclassStock:
    date_id: int  # 例: 20250414（yyyymmdd）
    time_id: int  # 例: 143000（hhmmss）
    symbol_id: str  # 例: "AAPL"
    symbol_name: str  # 例: "Apple"
    url: str  # 例: "https://query1.finance.yahoo.com/..."
    interval: str  # 例: "1d"
    source: str  # 例: "yahoo"
    feature_: Dict[str, float]  # 株価データ（open, close, volumeなど）

import argparse
from dataclasses import dataclass
from typing import Optional

from stock_scraper.domain.time_period import parse_time_period


@dataclass(slots=True)
class CLIConfig:
    symbol: str
    bins: str
    interval: Optional[str] = None
    range_: Optional[str] = None


def build_parser():
    parser = argparse.ArgumentParser()

    # 銘柄
    parser.add_argument(
        "-s",
        "--symbol",
        type=str,
        required=True,
    )
    # スクレイピング間隔
    parser.add_argument(
        "-b",
        "--bins",
        type=str,
        required=True,
    )
    # ローソク株価の足間隔
    parser.add_argument(
        "-i",
        "--interval",
        type=str,
        default=None,
    )
    # データの取得範囲
    parser.add_argument(
        "-r",
        "--range",
        dest="range_",  # rangeは予約語
        type=str,
        default=None,
    )

    return parser


def parse_cli(args=None) -> CLIConfig:
    parser = build_parser()
    parsed_args = parser.parse_args(args)
    # デフォルト値を設定
    parsed_args.bins = parse_time_period(parsed_args.bins)
    if parsed_args.interval is None:
        parsed_args.interval = parsed_args.bins
    else:
        parsed_args.interval = parse_time_period(parsed_args.interval)
    if parsed_args.range_ is None:
        parsed_args.range_ = parsed_args.interval
    else:
        parsed_args.range_ = parse_time_period(parsed_args.range_)
    return CLIConfig(**parsed_args.__dict__)

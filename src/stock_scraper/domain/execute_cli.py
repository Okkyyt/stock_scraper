import argparse

def add_parser_arguments(parser):
    # 銘柄
    parser.add_argument(
        "-s",
        "--symbol",
        type=str,
        help="Stock symbol to scrape",
        required=True,
    )
    # スクレイピング間隔
    parser.add_argument(
        "-b",
        "--bins",
        type=str,
        help="Loop bins for scraping",
        required=True,
    )
    return parser


def execute_cli():
    parser = argparse.ArgumentParser(
        prog="Stock Scraper",
        description="A simple stock scraper",
    )

    # サブパーサーの追加
    sub_parsers = parser.add_subparsers(dest="command")
    sub_parsers.required = True

    # サブコマンドの定義
    quote = sub_parsers.add_parser(
        "quote",
        help="最新の株価情報を取得する",
    )
    bar = sub_parsers.add_parser(
        "bar",
        help="指定した期間のindicator株価情報を取得する",
    )

    # 引数の追加
    quote = add_parser_arguments(quote)
    bar = add_parser_arguments(bar)

    bar.add_argument(
        "-i",
        "--interval",
        type=str,
        help="Interval for bar data (e.g., 1d, 5m)",
        required=True,
    )
    bar.add_argument(
        "-r",
        "--range",
        type=str,
        help="Range for bar data (e.g., 1mo, 1y)",
        default=None,
    )

    args = parser.parse_args()

    return args


execute_cli()

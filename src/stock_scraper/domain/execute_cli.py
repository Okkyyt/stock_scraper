import argparse

def execute_cli():
    parser = argparse.ArgumentParser(
        prog="Stock Scraper",
        description="A simple stock scraper",
    )

    parser.add_argument(
        "-s",
        "--symbol",
        type=str,
        help="Stock symbol to scrape",
        required=True,
    )

    parser.add_argument(
        "-i",
        "--interval",
        type=str,
        help="Interval for stock data",
        required=True,
    )

    parser.add_argument(
        "-r",
        "--range",
        type=str,
        help="Range for stock data",
        default="1d",
    )

    args = parser.parse_args()

    return args

execute_cli()

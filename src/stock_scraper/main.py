import argparse
from .config_loader import load_stock_config
from .presentation.while_requests import while_request_session


def main() -> None:
    print("Hello from stock-scraper!")
    parser = argparse.ArgumentParser(
        description="スクレイピング銘柄の指定",
    )

    parser.add_argument(
        "-s",
        required=True,
        help="銘柄コードの指定。例: 7203",
    )

    args = parser.parse_args()
    symbol_id = args.s
    print(f"銘柄コード: {symbol_id} を指定しました。")

    stock_items = load_stock_config()
    

if __name__ == "__main__":
    main() 
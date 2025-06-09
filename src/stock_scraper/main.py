import uvicorn

from .domain.cli import parse_cli
from .domain.set_dict import build_fetch_config, build_symbol_info, make_scraper
from .api.app import create_app

# コマンドライン引数を受取
cli_conf = parse_cli()
# cliからスクレイピングクラスを取得
scraper = make_scraper(cli_conf.symbol)
# 銘柄情報を取得
symbol_info = build_symbol_info(cli_conf.symbol)
# スクレイピング設定を取得
fetch_conf = build_fetch_config(cli_conf.symbol, cli_conf)

app = create_app(scraper, fetch_conf)


def main():
    uvicorn.run("stock_scraper.main:app", host="127.0.0.1", port=8000, reload=True)

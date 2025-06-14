import asyncio

from stock_scraper.config_loader import load_config
from stock_scraper.domain.cli import CLIConfig
from stock_scraper.domain.schemas import FetchHistory
from stock_scraper.domain.set_dict import (
    build_fetch_config,
    build_symbol_info,
    make_scraper,
)
from stock_scraper.domain.time_period import parse_time_period
from stock_scraper.infrastructure.db.create_table import create_tables
from stock_scraper.infrastructure.db.insert import (
    insert_fetch_history,
    upsert_fetch_config,
    upsert_symbol_info,
)

TIME_FRAME = "1d"  # デフォルトの時間枠

bins = parse_time_period(TIME_FRAME)
interval = parse_time_period(TIME_FRAME)
range = parse_time_period(TIME_FRAME)

config_json = load_config("config/stock_list.json")
symbol_list = list(config_json.keys())


async def main():
    for symbol in symbol_list:
        cli_conf = CLIConfig(symbol=symbol, bins=bins, interval=interval, range_=range)

        scraper = make_scraper(cli_conf.symbol)
        symbol_info = build_symbol_info(cli_conf.symbol)
        fetch_conf = build_fetch_config(cli_conf.symbol, cli_conf)

        # sourceがyahoo_financeの場合のみ実行
        if fetch_conf.source != "yahoo_finance":
            print(f"❌ {symbol} は yahoo_finance 以外のソースのためスキップ")
            continue

        # データベースのテーブルを作成
        await create_tables()
        # 銘柄情報をDBに保存
        await upsert_symbol_info(symbol_info)
        # 取得設定をDBに保存
        await upsert_fetch_config(fetch_conf)

        # urlのRANGEをMAXに書き換え
        URL = fetch_conf.url.replace(
            f"range={TIME_FRAME}",
            "range=10y",
        )

        async with await scraper.create_session() as session:
            res, status_meta = await scraper.scraping(session, URL)

        snapshots = scraper.postprocess(res)
        record = FetchHistory(
            symbol=fetch_conf.symbol,
            config_code=fetch_conf.config_code,
            status_meta=status_meta,
            price=snapshots,
        )
        # 取得結果をDBに保存
        await insert_fetch_history(record)
        print(f"🚀{symbol} 完了")


if __name__ == "__main__":
    asyncio.run(main())

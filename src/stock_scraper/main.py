import importlib

import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from .api.set_stock_instance import set_stock_instance
from .domain.execute_cli import execute_cli
from .infrastructure.db.create_table import create_tables
from .infrastructure.db.insert_stock_instanse import insert_stocke_instance

# CLI引数の取得
args = execute_cli()

# 銘柄情報を格納するためのインスタンス
stock_instance = set_stock_instance(args.symbol, args.interval, args.range)
# スクレイピングのインスタンス
module = importlib.import_module(
    f"src.stock_scraper.scraping.apis.{stock_instance.source}"
)
scraping_instance = getattr(
    module, "".join(word.capitalize() for word in stock_instance.source.split("_"))
)()  # getattr(ファイル名, クラス名) -> classの取得

app = FastAPI()


# 定期実行処理
async def pipline():
    print(f"銘柄: {stock_instance.symbol_name}")
    # aiohttpセッションを取得
    session = app.state.session
    # url, messageの作成
    preprocess = scraping_instance.preprocess(stock_instance)
    # スクレイピングの実行
    response = scraping_instance.scraping(session, preprocess)
    # 取得したデータの整形
    postprocess = scraping_instance.postprocess(response)
    # stock_instanceの更新
    stock_instance_copy = stock_instance.copy()
    stock_instance_copy.stock_data = postprocess

    print(f"株価情報🚀: {stock_instance_copy}")
    # インスタンスをdbに保存する
    await insert_stocke_instance(stock_instance_copy)


@app.get("/root")
async def root():
    return {"message": "Welcome to the Stock Scraper API!"}


@app.on_event("startup")
async def skd_startup():
    # セッション作成
    app.state.session = scraping_instance.create_session()
    # スケジューラのインスタンスを作成
    scheduler = AsyncIOScheduler()
    app.state.scheduler = scheduler
    # データベースのテーブル作成
    await create_tables()  # IF NOT EXISTS付き

    # range_interval次第
    # スケジューラに定期実行する関数を登録(15:30に実行)
    scheduler.add_job(pipline, "cron", hour=15, minute=30)

    # スケジューラを開始
    scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    # aiohttpセッション終了
    await app.state.session.close()
    # スケジューラを停止
    app.state.scheduler.shutdown()
    print("Scheduler stopped.")


def main():
    uvicorn.run("stock_scraper.main:app", host="127.0.0.1", port=8000, reload=True)

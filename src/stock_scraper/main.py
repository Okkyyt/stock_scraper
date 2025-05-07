import aiohttp
from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import uvicorn

from .api.set_stock_instance import set_stock_instance
from .api.set_stock_features import set_stock_features
from .usecase.YahooFinance.scraping import get_aiohttp
from .infrastructure.db.create_table import create_tables
from .infrastructure.db.insert_stock_instanse import insert_stocke_instance


# インスタンスの作成
stock_instance = set_stock_instance("AAPL", "1d", "1d")

app = FastAPI()


@app.get("/root")
async def root():
    return {"message": "Welcome to the Stock Scraper API!"}


# 定期実行処理
async def say_hello():
    print(f"銘柄: {stock_instance.symbol_name}")
    # aiohttpセッションを取得
    session = app.state.session
    # スクレイピングを実行
    res = await get_aiohttp(session, stock_instance.url)
    # 株価情報を挿入するようにインスタンスをコピー
    stock_instance_copy = set_stock_features(stock_instance, res)
    print(f"株価情報🚀: {stock_instance_copy}")
    # インスタンスをdbに保存する
    await insert_stocke_instance(stock_instance_copy)


@app.on_event("startup")
async def skd_startup():
    # aiohttp セッション作成
    app.state.session = aiohttp.ClientSession()
    # スケジューラのインスタンスを作成
    scheduler = AsyncIOScheduler()
    app.state.scheduler = scheduler
    # データベースのテーブル作成
    await create_tables()  # IF NOT EXISTS付き
    # スケジューラに定期実行する関数を登録(15:30に実行)
    scheduler.add_job(say_hello, "cron", hour=15, minute=30)
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

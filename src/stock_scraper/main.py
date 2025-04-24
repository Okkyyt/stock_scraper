import asyncio
import aiohttp
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from .api.scheduler import set_stock_instance
from .usecase.getStockprice import get_aiohttp
from .usecase.set_stock_feature import set_stock_features


# インスタンスの作成
stock_instance = set_stock_instance("AAPL")

app = FastAPI()


@app.get("/root")
async def root():
    return {"message": "Welcome to the Stock Scraper API!"}


# 定期実行処理
def say_hello():
    print(f"銘柄: {stock_instance.symbol_name}")
    session = app.state.session
    res = asyncio.run(get_aiohttp(session, stock_instance.url))
    print(res)
    # 株価情報を挿入するようでインスタンスをコピー
    stock_instance_copy = set_stock_features(stock_instance, res)


@app.on_event("startup")
async def skd_startup():
    # aiohttp セッション作成
    app.state.session = aiohttp.ClientSession()
    # スケジューラのインスタンスを作成
    scheduler = BackgroundScheduler()
    # スケジューラに定期実行する関数を登録
    scheduler.add_job(say_hello, "interval", seconds=5)
    # スケジューラを開始
    scheduler.start()


@app.on_event("shutdown")
async def shutdown_event():
    # aiohttpセッション終了
    await app.state.session.close()
    # スケジューラを停止
    app.state.scheduler.shutdown()
    print("Scheduler stopped.")

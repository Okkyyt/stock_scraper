from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import uvicorn
import websockets

from .domain.execute_cli import execute_cli
from .api.set_stock_instance import set_stock_instance
from .infrastructure.db.create_table import create_tables
from .infrastructure.db.insert_stock_instanse import insert_stocke_instance
from .usecase.build_message import build_message
from .usecase.scraping import websocket_scraping

import os
from dotenv import load_dotenv

load_dotenv()

FINHUB_API_KEY = os.getenv("FINHUB_API_KEY")

# CLI引数の取得
args = execute_cli()

# インスタンスの作成
stock_instance = set_stock_instance(args.symbol, args.interval, args.range)

app = FastAPI()


@app.get("/root")
async def root():
    return {"message": "Welcome to the Stock Scraper API!"}


# 定期実行処理
async def say_hello():
    print(f"銘柄: {stock_instance.symbol_name}")
    # aiohttpセッションを取得
    session = app.state.session
    # スクレイピングに必要なパス（メッセージ）を作成
    message = build_message(stock_instance)
    # スクレイピング
    res = await websocket_scraping(session, message)
    # レスポンスの正則化
    # reshaped_res = await reshape_res(res)
    reshaped_res = None
    # インスタンスの更新
    stock_instance_copy = set_stock_instance(
        stock_instance,
        reshaped_res
    )

    print(f"株価情報🚀: {stock_instance_copy}")
    # インスタンスをdbに保存する
    await insert_stocke_instance(stock_instance_copy)


@app.on_event("startup")
async def skd_startup():
    # セッション作成
    app.state.session = websockets.connect(
        f"wss://ws.finnhub.io?token={FINHUB_API_KEY}"
    )
    # スケジューラのインスタンスを作成
    scheduler = AsyncIOScheduler()
    app.state.scheduler = scheduler
    # データベースのテーブル作成
    await create_tables()  # IF NOT EXISTS付き
    # スケジューラに定期実行する関数を登録(15:30に実行)
    # scheduler.add_job(say_hello, "cron", hour=15, minute=30)
    scheduler.add_job(say_hello, "interval", seconds=10)
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

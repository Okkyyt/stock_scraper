from fastapi import FastAPI
from sched import scheduler
from apscheduler.schedulers.background import BackgroundScheduler
from .scheduler import set_stock_instance

app = FastAPI()


@app.get("/root")
async def root():
    return {"message": "Welcome to the Stock Scraper API!"}


# 定期実行処理
def say_hello():
    print("Hello, world!")
    print(set_stock_instance("AAPL"))


@app.on_event("startup")
def skd_startup():
    # スケジューラのインスタンスを作成
    scheduler = BackgroundScheduler()
    # スケジューラに定期実行する関数を登録
    scheduler.add_job(say_hello, "interval", seconds=5)
    # スケジューラを開始
    scheduler.start()


@app.on_event("shutdown")
def shutdown_event():
    # スケジューラを停止
    scheduler.shutdown()
    print("Scheduler stopped.")

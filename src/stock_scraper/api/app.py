from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI


def create_app(scraper, stock_conf) -> FastAPI:
    app = FastAPI()

    # 定期実行処理
    async def pipline():
        print(f"銘柄: {stock_conf['symbol']}")
        # aiohttpセッションを取得
        session = app.state.session
        # スクレイピングの実行
        res = await scraper.scraping(session, stock_conf['url'])
        # 取得したデータの整形
        re_features = scraper.postprocess(res)

        # インスタンスをdbに保存する
        # await insert_stocke_instance(stock_instance_copy)

    @app.get("/root")
    async def root():
        return {"message": "Welcome to the Stock Scraper API!"}

    @app.on_event("startup")
    async def skd_startup():
        # セッション作成
        app.state.session = await scraper.create_session()
        # スケジューラのインスタンスを作成
        scheduler = AsyncIOScheduler()
        app.state.scheduler = scheduler
        # データベースのテーブル作成
        # await create_tables()  # IF NOT EXISTS付き

        # range_interval次第
        # スケジューラに定期実行する関数を登録(15:30に実行)
        scheduler.add_job(pipline, "cron", hour=15, minute=30, max_instances=5)
        # テスト用に10秒ごとに実行
        scheduler.add_job(pipline, "interval", seconds=10, max_instances=5)

        # スケジューラを開始
        scheduler.start()

    @app.on_event("shutdown")
    async def skd_shutdown():
        # aiohttpセッション終了
        await app.state.session.close()
        # スケジューラを停止
        app.state.scheduler.shutdown()
        print("Scheduler stopped.")

    return app

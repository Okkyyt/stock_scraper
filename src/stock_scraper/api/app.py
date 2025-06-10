from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from stock_scraper.domain.schemas import FetchHistory
from stock_scraper.infrastructure.db.create_table import create_tables


def create_app(scraper, symbol_info, fetch_conf) -> FastAPI:
    app = FastAPI()

    # 定期実行処理
    async def pipline():
        print(f"銘柄: {fetch_conf.symbol}")
        print(f"スクレイピングURL: {fetch_conf.url}")
        # aiohttpセッションを取得
        session = app.state.session
        # スクレイピングの実行
        res, stauts_meta = await scraper.scraping(session, fetch_conf.url)
        # 取得したデータの整形
        price_snapshot = scraper.postprocess(res)

        re_features = FetchHistory(
            symbol=fetch_conf.symbol,
            config_id=fetch_conf.config_id,
            status_meta=stauts_meta,
            price=price_snapshot,
        )
        print(f"取得したデータ: {re_features}")

        # インスタンスをdbに保存する
        # await insert_stocke_instance(stock_instance_copy)

    @app.get("/root")
    async def root():
        return {"message": "Welcome to the Stock Scraper API!"}

    @app.on_event("startup")
    async def skd_startup():
        # データベースのテーブルを作成
        await create_tables()
        # セッション作成
        app.state.session = await scraper.create_session()
        # スケジューラのインスタンスを作成
        scheduler = AsyncIOScheduler(timezone=symbol_info.timezone)
        app.state.scheduler = scheduler
        # スケジューリング設定
        try:
            scheduler.add_job(
                pipline,
                trigger="cron",
                **fetch_conf.scraping_interval,
                max_instances=5,
            )
            print(f"スケジューリング設定: {fetch_conf.scraping_interval}")
        except Exception as e:
            print(f"スケジューリング設定に失敗: {e}")
            raise e
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

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from stock_scraper.domain.schemas import FetchConfig, FetchHistory, SymbolInfo
from stock_scraper.infrastructure.db.create_table import create_tables
from stock_scraper.infrastructure.db.insert import upsert_symbol_info, upsert_fetch_config, insert_fetch_history


# scraper -> src/stock_scraper/scraping/apis/{source}.py のクラスインスタンス
def create_app(scraper, symbol_info: SymbolInfo, fetch_conf: FetchConfig) -> FastAPI:
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
        snapshots = scraper.postprocess(res)

        re_features = FetchHistory(
            symbol=fetch_conf.symbol,
            config_code=fetch_conf.config_code,
            status_meta=stauts_meta,
            price=snapshots,
        )
        print(f"取得したデータ: {re_features}")
        # インスタンスをdbに保存する
        await insert_fetch_history(re_features)

    @app.get("/root")
    async def root():
        return {"message": "Welcome to the Stock Scraper API!"}

    @app.on_event("startup")
    async def skd_startup():
        # データベースのテーブルを作成
        await create_tables()
        # 銘柄情報をDBに保存
        await upsert_symbol_info(symbol_info)
        # 取得設定をDBに保存
        await upsert_fetch_config(fetch_conf)
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

from stock_scraper.domain.schemas import FetchConfig, FetchHistory, SymbolInfo
from stock_scraper.infrastructure.db.connect import make_conn


async def insert_symbol_info(symbol_info: SymbolInfo):
    conn = await make_conn()
    if conn is None:
        return
    try:
        await conn.execute(
            """
            INSERT INTO symbol_info (symbol, exchange, currency, name, timezone)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (symbol) DO NOTHING;
            """,
            symbol_info.symbol,
            symbol_info.exchange,
            symbol_info.currency,
            symbol_info.name,
            symbol_info.timezone,
        )
        print(f"✅ 銘柄情報を挿入: {symbol_info.symbol}")
    except Exception as e:
        print(f"❌ 銘柄情報の挿入に失敗: {e}")
    finally:
        await conn.close()
        print("✅ DB接続終了")


async def insert_fetch_config(fetch_conf: FetchConfig):
    conn = await make_conn()
    if conn is None:
        return
    try:
        await conn.execute(
            """
            INSERT INTO fetch_config (symbol, config_id, source, scraping_interval, time_frame, url)
            VALUES ($1, $2, $3, $4, $5, $6)
            ON CONFLICT (config_id) DO NOTHING;
            """,
            fetch_conf.symbol,
            fetch_conf.config_id,
            fetch_conf.source,
            fetch_conf.scraping_interval,
            fetch_conf.time_frame,
            fetch_conf.url,
        )
        print(f"✅ 取得設定を挿入: {fetch_conf.config_id}")
    except Exception as e:
        print(f"❌ 取得設定の挿入に失敗: {e}")
    finally:
        await conn.close()
        print("✅ DB接続終了")


async def insert_fetch_features(fetch_history: FetchHistory):
    conn = await make_conn()
    if conn is None:
        return
    try:
        await conn.execute(
            """
            INSERT INTO price_snapshot (config_id, market_time, tick_price, open, close, high, low, volume, adjclose)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9);
            """,
            fetch_history.config_id,
            fetch_history.price.market_time,
            fetch_history.price.tick_price,
            fetch_history.price.indicators.open,
            fetch_history.price.indicators.close,
            fetch_history.price.indicators.high,
            fetch_history.price.indicators.low,
            fetch_history.price.indicators.volume,
            fetch_history.price.indicators.adjclose,
        )
        print(f"✅ 価格スナップショットを挿入: {fetch_history.config_id}")

        await conn.execute(
            """
            INSERT INTO fetch_log (config_id, crawl_started_at, fetched_at, status_code, error_msg)
            VALUES ($1, $2, $3, $4, $5);
            """,
            fetch_history.config_id,
            fetch_history.status_meta.crawl_started_at,
            fetch_history.status_meta.fetched_at,
            fetch_history.status_meta.status_code,
            fetch_history.status_meta.error_msg,
        )
        print(f"✅ 取得ログを挿入: {fetch_history.config_id}")
    except Exception as e:
        print(f"❌ 価格スナップショットの挿入に失敗: {e}")
    finally:
        await conn.close()
        print("✅ DB接続終了")

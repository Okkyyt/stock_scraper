import json

from stock_scraper.domain.schemas import FetchConfig, FetchHistory, SymbolInfo
from stock_scraper.infrastructure.db.connect import make_conn

# ───────────────────────────────────────────
# 1. symbol_info ─ Insert/Update
# ───────────────────────────────────────────
async def upsert_symbol_info(symbol_info: SymbolInfo) -> int:
    async with make_conn() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO symbol_info (symbol, exchange, currency, name, timezone)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (symbol) DO UPDATE
               SET exchange = EXCLUDED.exchange,
                   currency = EXCLUDED.currency,
                   name     = EXCLUDED.name,
                   timezone = EXCLUDED.timezone
            RETURNING id;
            """,
            symbol_info.symbol,
            symbol_info.exchange,
            symbol_info.currency,
            symbol_info.name,
            symbol_info.timezone,
        )
        symbol_id = row["id"]
        print(f"✅ 銘柄 upsert 完了: {symbol_info.symbol} (id={symbol_id})")
        return symbol_id

# ───────────────────────────────────────────
# 2. fetch_config ─ Insert/Update
# ───────────────────────────────────────────
async def upsert_fetch_config(fetch_conf: FetchConfig) -> int:
    async with make_conn() as conn:
        row = await conn.fetchrow(
            """
            INSERT INTO fetch_config (
                symbol_id, config_code, source,
                scraping_interval, time_frame, url
            )
            VALUES ( (SELECT id FROM symbol_info WHERE symbol = $1),
                     $2, $3, $4, $5, $6 )
            ON CONFLICT (config_code) DO UPDATE
               SET symbol_id         = EXCLUDED.symbol_id,
                   source            = EXCLUDED.source,
                   scraping_interval = EXCLUDED.scraping_interval,
                   time_frame        = EXCLUDED.time_frame,
                   url               = EXCLUDED.url
            RETURNING id;
            """,
            fetch_conf.symbol,            # $1
            fetch_conf.config_code,       # $2
            fetch_conf.source,            # $3
            json.dumps(fetch_conf.scraping_interval), # $4
            json.dumps(fetch_conf.time_frame),        # $5
            fetch_conf.url,               # $6
        )
        fetch_id = row["id"]
        print(f"✅ 取得設定 upsert 完了: {fetch_conf.config_code} (id={fetch_id})")
        return fetch_id

# ───────────────────────────────────────────
# 3. price_snapshot + fetch_log
# ───────────────────────────────────────────
async def insert_fetch_history(fetch_history: FetchHistory) -> None:
    async with make_conn() as conn:
        snapshots = fetch_history.price
        m = fetch_history.status_meta

        async with conn.transaction():          # ★ 同一トランザクション
            # 1) fetch_log を先に入れて event_id を取得
            row = await conn.fetchrow(
                """
                INSERT INTO fetch_log (
                    fetch_id, crawl_started_at, fetched_at,
                    status_code, error_msg
                )
                VALUES (
                    (SELECT id FROM fetch_config WHERE config_code = $1),
                    $2, $3, $4, $5
                )
                RETURNING id;
                """,
                fetch_history.config_code,        # $1
                m.crawl_started_at,               # $2
                m.fetched_at,                     # $3
                m.status_code,                    # $4
                m.error_msg                       # $5
            )
            event_id = row["id"]

            # 2) price_snapshot を event_id でひも付け
            await conn.executemany(
                """
                INSERT INTO price_snapshot (
                    event_id, fetch_id, market_time,
                    open, close, high, low,
                    volume, adjclose
                )
                VALUES (
                    $1,
                    (SELECT id FROM fetch_config WHERE config_code = $2),
                    $3, $4, $5, $6, $7, $8, $9
                )
                ON CONFLICT (event_id, market_time) DO NOTHING;
                """,
                [
                    (
                        event_id,
                        fetch_history.config_code,
                        p.market_time,
                        p.open,
                        p.close,
                        p.high,
                        p.low,
                        p.volume,
                        p.adjclose
                    )
                    for p in snapshots
                ]
            )

        print(f"✅ ログ＋スナップショット完了: event_id={event_id}")

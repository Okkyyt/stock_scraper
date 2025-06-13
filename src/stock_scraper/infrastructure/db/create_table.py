from stock_scraper.infrastructure.db.connect import make_conn


async def create_tables():
    async with make_conn() as conn:
        # symbol_info
        await conn.execute(
            """
                CREATE TABLE IF NOT EXISTS symbol_info (
                id       BIGSERIAL PRIMARY KEY,
                symbol   VARCHAR(10) UNIQUE NOT NULL,
                exchange VARCHAR(10),
                currency VARCHAR(10),
                name     VARCHAR(100),
                timezone TEXT,
                created_at TIMESTAMPTZ DEFAULT now()
            );
            """
        )
        # fetch_config
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS fetch_config (
                id        BIGSERIAL PRIMARY KEY,
                symbol_id BIGINT NOT NULL
                        REFERENCES symbol_info(id) ON DELETE CASCADE,
                config_code TEXT UNIQUE NOT NULL,     -- 例: AAPL_yahoo_5m
                source      VARCHAR(50),
                time_frame  JSONB,     -- 例: {"days": 0, "hours": 0, "minutes": 5}
                scraping_interval JSONB,
                url         TEXT,
                created_at  TIMESTAMPTZ DEFAULT now()
            );
            """
        )
        # fetch_log
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS fetch_log (
                id          BIGSERIAL PRIMARY KEY,
                fetch_id    BIGINT NOT NULL
                            REFERENCES fetch_config(id) ON DELETE CASCADE,
                crawl_started_at TIMESTAMPTZ,
                fetched_at       TIMESTAMPTZ,
                status_code      INT,
                error_msg        TEXT
            );
            """
        )
        # price_snapshot
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS price_snapshot (
                id          BIGSERIAL PRIMARY KEY,
                event_id    BIGINT NOT NULL                 -- fetch_log.id への FK
                            REFERENCES fetch_log(id) ON DELETE CASCADE,
                fetch_id    BIGINT NOT NULL                 -- fetch_config.id への FK
                            REFERENCES fetch_config(id) ON DELETE CASCADE,
                market_time TIMESTAMPTZ NOT NULL,
                open        NUMERIC(18,6),
                close       NUMERIC(18,6),
                high        NUMERIC(18,6),
                low         NUMERIC(18,6),
                volume      BIGINT,
                adjclose    NUMERIC(18,6),
                UNIQUE (event_id, market_time)
            );
            """
        )

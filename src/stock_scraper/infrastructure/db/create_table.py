from stock_scraper.infrastructure.db.connect import make_conn


async def create_tables():
    conn = await make_conn()
    if conn is None:
        return
    try:

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS symbol_info (
                symbol VARCHAR(50) PRIMARY KEY,
                exchange VARCHAR(10),
                currency VARCHAR(10),
                name VARCHAR(100),
                timezone VARCHAR(50)
            );
            """
        )

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS fetch_config (
                symbol VARCHAR(50),
                config_id VARCHAR(50 PRIMARY KEY,
                source VARCHAR(50),
                scraping_interval VARCHAR(20),
                time_frame VARCHAR(20),
                url TEXT,
                FOREIGN KEY (symbol) REFERENCES symbol_info(symbol)
            """
        )

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS price_snapshot (
                config_id VARCHAR(50),
                market_time TIMESTAMP WITH TIME ZONE,
                tick_price FLOAT,
                open FLOAT,
                close FLOAT,
                high FLOAT,
                low FLOAT,
                volume INT,
                adjclose FLOAT,
                FOREIGN KEY (config_id) REFERENCES fetch_config(config_id)
            );
            """
        )

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS fetch_log(
                config_id VARCHAR(50),
                crawl_started_at TIMESTAMP WITH TIME ZONE,
                fetched_at TIMESTAMP WITH TIME ZONE,
                status_code INT,
                error_msg TEXT,
                FOREIGN KEY (config_id) REFERENCES fetch_config(config_id)
            );
            """
        )

        print("✅ テーブル作成 or 作成済み")
        await conn.close()
        print("✅ DB接続終了")
    except Exception as e:
        print("❌ エラー:", e)

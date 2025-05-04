from stock_scraper.infrastructure.db.connect import make_conn

async def create_tables():
    conn = await make_conn()
    try:
        
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS symbol_data (
                id serial PRIMARY KEY,
                symbol_id VARCHAR(10) UNIQUE NOT NULL,
                symbol_name text,
                url text,
                source text
            );
            """
        )

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS stock_meta_price (
                id serial PRIMARY KEY,
                symbol_id VARCHAR(10) REFERENCES symbol_data(symbol_id),
                date_id integer,
                time_id integer,
                regular_market_time TIMESTAMP,
                regular_market_price NUMERIC,
                interval VARCHAR(10)
            );
            """
        )

        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS stock_indicator_price (
                id serial PRIMARY KEY,
                symbol_id VARCHAR(10) REFERENCES symbol_data(symbol_id),
                date_id integer,
                time_id integer,
                interval text,
                open NUMERIC,
                high NUMERIC,
                low NUMERIC,
                close NUMERIC,
                volume BIGINT
            );
            """
        )
        print("✅ テーブル作成")
        await conn.close()
    except Exception as e:
        print("❌ エラー:", e)

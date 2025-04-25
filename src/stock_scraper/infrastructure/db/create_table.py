import psycopg


def create_tables():
    try:
        with psycopg.connect(
            # DBの接続情報
            "dbname=test user=postgres"
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
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

                cur.execute(
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

                cur.execute(
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
    except Exception as e:
        print("❌ エラー:", e)

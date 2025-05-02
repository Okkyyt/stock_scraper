from stock_scraper.infrastructure.db.connect import make_conn

def insert_stocke_instance(stock_instance):
    """
    stock_instanceをDBに保存する
    """
    # DBに接続
    with make_conn() as conn:
        with conn.cursor() as cur:
            # symbol_dataテーブルにデータを挿入
            cur.execute(
                """
                INSERT INTO symbol_data (symbol_id, symbol_name, url, source)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (symbol_id) DO NOTHING;
                """,
                (
                    stock_instance.symbol_id,
                    stock_instance.symbol_name,
                    stock_instance.url,
                    stock_instance.source,
                ),
            )

            # stock_meta_priceテーブルにデータを挿入
            cur.execute(
                """
                INSERT INTO stock_meta_price (symbol_id, date_id, time_id, regular_market_time, regular_market_price)
                VALUES (%s, %s, %s, %s, %s);
                """,
                (
                    stock_instance.symbol_id,
                    stock_instance.feature_["meta"]["regularMarketTime"],
                    None,
                    None,
                    stock_instance.feature_["meta"]["regularMarketPrice"],
                ),
            )

            # stock_indicator_priceテーブルにデータを挿入
            cur.execute(
                """
                INSERT INTO stock_indicator_price (symbol_id, date_id, time_id, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
                """,
                (
                    stock_instance.symbol_id,
                    None,
                    None,
                    stock_instance.feature_["indicator"]["open"],
                    stock_instance.feature_["indicator"]["high"],
                    stock_instance.feature_["indicator"]["low"],
                    stock_instance.feature_["indicator"]["close"],
                    stock_instance.feature_["indicator"]["volume"],
                ),
            )

from stock_scraper.infrastructure.db.connect import make_conn


async def insert_stocke_instance(stock_instance):
    """
    stock_instanceをDBに保存する
    """
    # DBに接続
    conn = await make_conn()
    try:
        await conn.execute(
            """
            INSERT INTO symbol_data (symbol_id, symbol_name, url, source)
            VALUES ($1, $2, $3, $4)
            ON CONFLICT (symbol_id) DO NOTHING;
            """,
            stock_instance.symbol_id,
            stock_instance.symbol_name,
            stock_instance.url,
            stock_instance.source,
        )

        await conn.execute(
            """
            INSERT INTO stock_meta_price (symbol_id, date_id, time_id, regular_market_time, regular_market_price)
            VALUES ($1, $2, $3, $4, $5);
            """,
            stock_instance.symbol_id,
            stock_instance.date_id,
            stock_instance.time_id,
            stock_instance.feature_["meta"]["regularMarketTime"],
            stock_instance.feature_["meta"]["regularMarketPrice"],
        )
        await conn.execute(
            """
            INSERT INTO stock_indicator_price (symbol_id, date_id, time_id, open, high, low, close, volume)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8);
            """,
            stock_instance.symbol_id,
            stock_instance.date_id,
            stock_instance.time_id,
            stock_instance.feature_["indicator"]["open"],
            stock_instance.feature_["indicator"]["high"],
            stock_instance.feature_["indicator"]["low"],
            stock_instance.feature_["indicator"]["close"],
            stock_instance.feature_["indicator"]["volume"],
        )
    except Exception as e:
        print("❌ エラー:", e)
    finally:
        # DB接続を閉じる
        await conn.close()
        print("✅ DB接続終了")

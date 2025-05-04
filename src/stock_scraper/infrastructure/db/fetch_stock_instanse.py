import pandas as pd

from stock_scraper.infrastructure.db.connect import make_conn

async def fetch_stock_instance(symbol_id):
    conn = await make_conn()
    try:
        # データを取得
        symbol_data = await conn.fetch(
            """
            SELECT * FROM symbol_data WHERE symbol_id = $1;
            """,
            symbol_id
        )

        symbol_meta_price = await conn.fetch(
            """
            SELECT * FROM stock_meta_price WHERE symbol_id = $1;
            """,
            symbol_id
        )
        symbol_indicator_price = await conn.fetch(
            """
            SELECT * FROM stock_indicator_price WHERE symbol_id = $1;
            """,
            symbol_id
        )
        # データをdfに変換
        symbol_df = pd.DataFrame([dict(row) for row in symbol_data])
        symbol_meta_price_df = pd.DataFrame([dict(row) for row in symbol_meta_price])
        symbol_indicator_price_df = pd.DataFrame([dict(row) for row in symbol_indicator_price])

        return {
            "symbol_data": symbol_df,
            "symbol_meta_price": symbol_meta_price_df,
            "symbol_indicator_price": symbol_indicator_price_df
        }
    except Exception as e:
        print("❌ エラー:", e)
        return None
    finally:
        await conn.close()
        print("✅ DB接続終了")
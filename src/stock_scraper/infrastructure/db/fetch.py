import pandas as pd

from stock_scraper.infrastructure.db.connect import make_conn


async def fetch_stock_price(symbol, interval, sorce='yahoo_finance') -> pd.DataFrame | None:
    async with make_conn() as conn:
        try:
            # データを取得
            records = await conn.fetch(
                """
                SELECT price_snapshot.*
                FROM price_snapshot
                JOIN fetch_config ON price_snapshot.fetch_id = fetch_config.id
                JOIN symbol_info ON fetch_config.symbol_id = symbol_info.id
                WHERE symbol_info.symbol = $1
                AND fetch_config.config_code = $2
                """,
                symbol,
                f"{symbol}-{sorce}-{interval}"
            )
        
            return pd.DataFrame([dict(record) for record in records])

        except Exception as e:
            print("❌ エラー:", e)
            return None


# Usage example:
# async def main():
#     df = await fetch_stock_instance("AAPL", "1d")
#     print(df)
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(main())

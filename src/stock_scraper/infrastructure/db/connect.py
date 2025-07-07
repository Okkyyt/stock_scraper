import os
from contextlib import asynccontextmanager

import asyncpg
from dotenv import load_dotenv

load_dotenv()

# エンドポイント
DB_ENDOPOINT = os.getenv("DB_ENDPOINT")
# ポート
PORT = "5432"
# 設定
USER = os.getenv("DB_USER")
# パスワード
DB_PASSWORD = os.getenv("DB_PASSWORD")
# 設定ー＞DB名
DB_NAME = os.getenv("DB_NAME")


@asynccontextmanager
async def make_conn():
    conn = None
    try:
        # asyncpgで普通に接続
        conn = await asyncpg.connect(
            host=DB_ENDOPOINT,
            port=PORT,
            user=USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )

        # psycopgで接続確認
        print("✅ DB接続成功")
        yield conn
    except Exception as e:
        print("❌ DB接続失敗:", e)
        raise
    finally:
        if conn:
            await conn.close()
            print("✅ DB接続終了")

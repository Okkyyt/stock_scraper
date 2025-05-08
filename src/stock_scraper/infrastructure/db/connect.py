import asyncpg
import os
from dotenv import load_dotenv
import asyncio

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


async def make_conn():
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
        return conn
    except Exception as e:
        print("❌ DB接続失敗:", e)
        return None


# 確認
# print(asyncio.run(make_conn()))

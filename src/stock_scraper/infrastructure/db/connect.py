import asyncpg
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

# クラスターエンドポイント
AURORA_ENDOPOINT = os.getenv("AURORA_ENDPOINT")
# ポート
PORT = "5432"
# 設定ー＞マスターユーザー名
USER = os.getenv("AURORA_USER")
# パスワード(Secret Manager)
AURORA_PASSWORD = os.getenv("AURORA_PASSWORD")
# リージョン
REGION = os.getenv("REGION")
# 設定ー＞DB名
DB_NAME = os.getenv("DB_NAME")


async def make_conn():
    try:
        # asyncpgで普通に接続
        conn = await asyncpg.connect(
            host=AURORA_ENDOPOINT,
            port=PORT,
            user=USER,
            password=AURORA_PASSWORD,
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
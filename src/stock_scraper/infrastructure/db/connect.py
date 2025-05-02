import psycopg
import os
from dotenv import load_dotenv

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

def make_conn():
    # psycopgで普通に接続
    conn = psycopg.connect(
        host=AURORA_ENDOPOINT,
        port=PORT,
        user=USER,
        password=AURORA_PASSWORD,
        dbname=DB_NAME,
    )

    # psycopgで接続確認
    print("✅ DB接続成功")
    return conn

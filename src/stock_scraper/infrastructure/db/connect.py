import psycopg
import sys
import boto3

import os
from dotenv import load_dotenv

load_dotenv()

AURORA_ENDOPOINT = os.getenv("AURORA_ENDPOINT")
PORT = 5432
USER = os.getenv("AURORA_USER")
REGION = os.getenv("REGION")
DB_NAME = os.getenv("DB_NAME")

session = boto3.Session(profile_name='default')
client = session.client('rds')

token = client.generate_db_auth_token(
    DBHostname=AURORA_ENDOPOINT,
    Port=PORT,
    DBUsername=USER,
    Region=REGION
)


conn = psycopg.connect(
    host=AURORA_ENDOPOINT,
    port=PORT,
    user=USER,
    password=token,
    dbname=DB_NAME,
    sslmode='require'
)
print("✅ DB接続成功")

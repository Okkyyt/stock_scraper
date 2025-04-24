import os
from dotenv import load_dotenv

# プロキシの設定(環境変数)
load_dotenv()
HTTP_PROXY = os.getenv("HTTP_PROXY")
HTTPS_PROXY = os.getenv("HTTPS_PROXY")
proxies = {"http": None, "https": None}


# headerの設定
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36"
}


async def get_aiohttp(session, url):
    print(f"開始: {url}")
    try:
        async with session.get(url, headers=headers, proxy=proxies["http"]) as res:
            print(f"ステータス: {res.status}")
            res.raise_for_status()
            res_ = await res.json()
    except Exception as e:
        # logger.error(f"Exception: {e}")
        return None

    return res_

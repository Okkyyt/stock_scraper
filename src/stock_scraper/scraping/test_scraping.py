import aiohttp, asyncio, random, time

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Bot/0.1)",
    "Accept": "application/json, text/plain, */*",
}

async def fetch_chart(session, symbol, interval="1d", retries=5):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
    params = {"interval": interval}
    for i in range(retries):
        async with session.get(url, params=params, headers=HEADERS) as r:
            if r.status == 429:               # レート制限
                wait = 2 ** i + random.random()
                print(f"429 → {wait:.1f}s 待機")
                await asyncio.sleep(wait)
                continue
            r.raise_for_status()
            if "application/json" in r.headers.get("Content-Type", ""):
                return await r.json()
            text = await r.text()
            raise ValueError(f"Unexpected content type: {r.headers['Content-Type']}\n{text[:200]}")
    raise RuntimeError("Repeated 429")

async def main():
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as sess:
        data = await fetch_chart(sess, "9432.T")
        print(data)
        print(data["chart"]["result"][0]["meta"]["regularMarketPrice"])

asyncio.run(main())

import json

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; Bot/0.1)",
    "Accept": "application/json, text/plain, */*",
}

async def get_aiohttp(session, url):
    try:
        async with session.get(url, headers=HEADERS) as res:
            print(f'ステータス：{res.status}')
            return await res.json()
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


async def get_websocket(session, message):
    await session.send(json.dumps(message))
    res = await session.recv()
    return json.loads(res)
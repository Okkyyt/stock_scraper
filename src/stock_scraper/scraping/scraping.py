import json


async def get_aiohttp(session, url):
    try:
        async with session.get(url) as res:
            print(f'ステータス：{res.status}')
            return await res.json()
    except Exception as e:
        print(f"Error occurred: {e}")
        return None


async def get_websocket(session, message):
    await session.send(json.dumps(message))
    res = await session.recv()
    return json.loads(res)
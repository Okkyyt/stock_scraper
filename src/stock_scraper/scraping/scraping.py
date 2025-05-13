import json


async def get_aiohttp(session, url):
    async with session.get(url) as res:
        print(res.status)
        if res.status == 200:
            return await res.json()
        else:
            raise Exception(f"Error: {res.status}")


async def get_websocket(session, message):
    session.send(message)
    res = session.recv()
    return json.loads(res)

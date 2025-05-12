import json

def websocket_scraping(session, message):
    session.send(message)
    res = session.recv()
    return json.loads(res)

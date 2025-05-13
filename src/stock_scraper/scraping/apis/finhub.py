import websockets
import os
from dotenv import load_dotenv
from ..scraping import get_websocket

load_dotenv()

FINHUB_API_KEY = os.getenv("FINHUB_API_KEY")

class Finhub:
    def create_session(self):
        return websockets.connect()
    
    def preprocess(self, stock_instance):
        message = {
            "type": "subscribe",
            "symbol": stock_instance.symbol_name,
            "interval": stock_instance.interval,
        }
        return message
    
    async def scraping(self, session, message):
        return await get_websocket(session, message)
    
    def postprocess(self, response):
        # ここでレスポンスを整形する処理を実装
        # 例: JSON形式のレスポンスを辞書型に変換
        return response
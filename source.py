import asyncio
import websockets

async def listen(url: str):
    async with websockets.connect(url) as ws:
        try:
            while True:
                message = await ws.recv()
                print(f"Received message: {message}")
        except websockets.exceptions.ConnectionClosed:
            print("Connection with the server closed")
        except Exception as e:
            print(f"An error occurred: {e}")

asyncio.run(listen('wss://news.treeofalpha.com/ws/likes'))

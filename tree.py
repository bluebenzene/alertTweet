import asyncio
import json
import websockets
import subprocess
from datetime import datetime
import os

def play_alert(source, twitter_id):
    twitter_id_alerts = {
        "944686196331966464": "myside_hska.mp3", # hsakaTrades
    }
    source_alerts = {
        "Binance EN": "iamwayalert.mp3",
        "Coinbase": "nextlalala.mp3",
        "Kraken": "kraken.mp3",
        "Bithumb": "bithumb.mp3",
        "Upbit": "squidgame_alert.mp3",
        "Bitfinex": "bitfinex.mp3",
        "Huobi": "huobi.mp3",
        "FTX": "ftx.mp3",
        "Coinbase": "coinbase.mp3",
        "Blogs": "fluit.mp3",
        "Bloomberg": "bloomberg.mp3",
        "usGov": "usgov.mp3",
    }

    file_name = None
    if twitter_id in twitter_id_alerts:
        file_name = twitter_id_alerts[twitter_id]
    elif source in source_alerts:
        file_name = source_alerts[source]
    if file_name is not None:
        proc = subprocess.Popen(["play", f"alert_sound/{file_name}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout, stderr = proc.communicate()

async def connect_and_print(uri):
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    try:
                        message = await websocket.recv()
                        message_json = json.loads(message)
                        twitter_id = message_json["info"]["twitterId"] if "info" in message_json and "twitterId" in message_json["info"] else None
                        source = message_json["source"] if "source" in message_json else None
                        if (source and source in ["Binance EN", "Coinbase", "Kraken", "Bithumb", "Upbit", "Bitfinex", "Huobi", "FTX", "Coinbase", "Blogs", "Bloomberg", "usGov"]) or (twitter_id and twitter_id in ["twitter_id1", "twitter_id2"]):
                            timestamp = int(message_json["time"] / 1000)
                            time_str = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
                            title = message_json["title"] if "title" in message_json else ""
                            url = message_json["url"] if "url" in message_json else ""
                            print(f"[{time_str}] [{source}] {title} {url}")
                            play_alert(source, twitter_id)
                    except (websockets.ConnectionClosed, websockets.ConnectionClosedError) as e:
                        print("Connection closed, reconnecting...")
                        break
                    except Exception as e:
                        print("Error occurred, reconnecting...")
                        break
        except Exception as e:
            print("Error occurred, retrying...")
            await asyncio.sleep(1)

uri = "wss://news.treeofalpha.com/ws"
asyncio.run(connect_and_print(uri))

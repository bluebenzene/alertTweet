import asyncio
import json
import websockets
import subprocess
from datetime import datetime
import os



def play_alert(tag, play_twitter=True):
    # Map each tag to a corresponding alert file name
    alert_files = {
        "Binance EN": "iamwayalert.mp3",
        "Coinbase": "nextlalala.mp3",
        "Kraken": "kraken.mp3",
        "Bithumb": "bithumb.mp3",
        "Upbit": "squidgame_alert.mp3",
        "Bitfinex": "bitfinex.mp3",
        "Huobi": "huobi.mp3",
        "FTX": "ftx.mp3",
        "Coinbase": "coinbase.mp3",
        "Blogs": "mixkit-musical-alert-notification-2309.wav",
        "Bloomberg": "bloomberg.mp3",
        "usGov": "usgov.mp3",
        "Twitter": "maybealertr.mp3",
    }
    # Check if the given tag has a corresponding alert file
    if tag in alert_files and (play_twitter or tag != "Twitter"):
        file_name = alert_files[tag]
        # play the alert sound for the given tag
        proc = subprocess.Popen(["play", f"alert_sound/{file_name}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                stdin=subprocess.PIPE)
        stdout, stderr = proc.communicate()


async def connect_and_print(uri, play_twitter=True):
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    try:
                        message = await websocket.recv()
                        message_json = json.loads(message)

                        # Extract the desired fields from the message and format the timestamp
                        if "time" in message_json:
                            timestamp = int(message_json["time"] / 1000)  # Convert from milliseconds to seconds
                            time_str = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

                        if "source" in message_json:
                            source = message_json["source"]

                        if "title" in message_json:
                            title = message_json["title"]

                        if "url" in message_json:
                            url = message_json["url"]

                        # Print the message in the desired format
                        print(f"[{time_str}] [{source}] {title} {url}")

                        # Play the alert after printing the message
                        play_alert(source, play_twitter)

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
play_twitter_alert = False  # Set this to True to play the Twitter alert or False to turn it off
wss_like = "wss://news.treeofalpha.com/ws/likes"
api_key=os.environ.get('treekey')
asyncio.run(connect_and_print(uri, play_twitter_alert))

import asyncio
import json
import websockets
import subprocess
from datetime import datetime
import gtts
twitter_id_alerts = {
    "944686196331966464": "fluit.mp3", # hsakaTrades
    "44196397": "fluit.mp3", #elon musk
    "2361601055": "fluit.mp3", #db
    "1391538435261861894": "fluit.mp3", #zoomerfied
    "1456327895866314753": "fluit.mp3", #treeofalpha
    "1282727055604486148": "fluit.mp3", #newstreeofalpha
    "1333467482": "fluit.mp3", #coindesk
    "111533746": "fluit.mp3" , #wublockchain
    "TheBlock__": "fluit.mp3" , #theblock
}
source_alerts = {
    "Binance EN": "fluit.mp3",
    "Coinbase": "fluit.mp3",
    "Kraken": "fluit.mp3",
    "Bithumb": "fluit.mp3",
    "Upbit": "fluit.mp3",
    "Bitfinex": "fluit.mp3",
    "Huobi": "fluit.mp3",
    "FTX": "fluit.mp3",
    "Coinbase": "fluit.mp3",
    "Blogs": "fluit.mp3",
    "Bloomberg": "fluit.mp3",
    "usGov": "fluit.mp3",
}


def play_alert(source, twitter_id, title=None, body=None):
    file_name = None
    if twitter_id in twitter_id_alerts:
        file_name = twitter_id_alerts[twitter_id]
    elif source in source_alerts:
        file_name = source_alerts[source]
    if file_name is not None:
        proc = subprocess.Popen(["play", f"alert_sound/{file_name}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout, stderr = proc.communicate()

    if title or body:  # If there's a title or body, play them
        sound_text = f"{title if title else ''} {body if body else ''}"
        sound = gtts.gTTS(sound_text, lang='en', tld='us')
        sound.save("alert_sound/textaudio.mp3")
        proc = subprocess.Popen(["play", "alert_sound/textaudio.mp3"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout, stderr = proc.communicate()

async def connect_and_print(uri):
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                while True:
                    try:
                        message = await websocket.recv()
                        message_json = json.loads(message)
                        twitter_id = message_json["info"]["twitterId"] if "info" in message_json and "twitterId" in \
                                                                          message_json["info"] else None
                        source = message_json.get("source") if "source" in message_json else "Twitter"
                        if (source and source in source_alerts) or (twitter_id and twitter_id in twitter_id_alerts):
                            timestamp = int(message_json["time"] / 1000)
                            time_str = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
                            title = message_json.get("title").replace("\n", " ")
                            url = message_json["url"] if "url" in message_json else ""
                            body = message_json.get("body")
                            print(f"[{time_str}] [{source}] \033[33m{title} {body}\033[0m {url}")
                            play_alert(source, twitter_id, title, body if body else None)
                    except (websockets.ConnectionClosed, websockets.ConnectionClosedError) as e:
                        # print("Connection closed, reconnecting...")
                        break
                    except Exception as e:
                        # print("Error occurred, reconnecting...")
                        break
        except Exception as e:
            # print("Error occurred, retrying...")
            await asyncio.sleep(1)

uri = "wss://news.treeofalpha.com/ws"
asyncio.run(connect_and_print(uri))

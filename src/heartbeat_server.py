import os
from dotenv import load_dotenv
import asyncio
import websockets
import json
import datetime
import requests

load_dotenv()

# Define your Pusher app credentials
PUSHER_APP_KEY = os.getenv('PUSHER_KEY')
PUSHER_CLUSTER = os.getenv('PUSHER_CLUSTER')
PUSHER_WEBSOCKET_URL = f'wss://ws-{PUSHER_CLUSTER}.pusher.com/app/{PUSHER_APP_KEY}?client=js&version=7.0.3&protocol=5'
LOCAL_USER = os.getenv('LOCAL_USER')
NVIDIA_KEY_COMBO = os.getenv('NVIDIA_KEY_COMBO')
DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')

PING_HISTORY = []

def handle_ping(name, image):
    global PING_HISTORY

    player_found = False
    for player in PING_HISTORY:
        if player["name"] == name:
            player["last_ping"] = datetime.datetime.now()
            player_found = True

    if not player_found:
        player = {
            "name": name,
            "image": image,
            "last_ping": datetime.datetime.now(),
            "is_notified": False
        }

        print(f"Player {player['name']} joined!")
        PING_HISTORY.append(player)
        send_discord_joined(player)

    validate_pings()

def validate_pings():
    global PING_HISTORY

    index = 0
    for player in PING_HISTORY:
        if not player["is_notified"] and player["last_ping"] < datetime.datetime.now() - datetime.timedelta(seconds=25):
            print(f"Player {player['name']} went offline!")
            send_discord_offline(player)
            PING_HISTORY[index]["is_notified"] = True

        elif player["is_notified"] and player["last_ping"] >= datetime.datetime.now() - datetime.timedelta(seconds=25):
            print(f"Player {player['name']} is back!")
            send_discord_online(player)
            PING_HISTORY[index]["is_notified"] = False

        index = index + 1

def send_discord_offline(player):
    global DISCORD_WEBHOOK

    requests.post(
        DISCORD_WEBHOOK,
        data=json.dumps({
            "embeds": [
                {
                    "type": "rich",
                    "title": "",
                    "description": f"{player['name']} went offline!",
                    "color": 0xff0000,
                    "thumbnail": {
                        "url": player["image"],
                        "height": 0,
                        "width": 0
                    },
                    "author": {
                        "name": player["name"]
                    },
                    "footer": {
                        "text": "Please run `python main.py` again!"
                    }
                }
            ]
        }),
        headers={
            "Content-Type": "application/json"
        }
    )

def send_discord_online(player):
    global DISCORD_WEBHOOK

    requests.post(
        DISCORD_WEBHOOK,
        data=json.dumps({
            "embeds": [
                {
                    "type": "rich",
                    "title": "",
                    "description": f"{player['name']} is back online!",
                    "color": 7774208,
                    "thumbnail": {
                        "url": player["image"],
                        "height": 0,
                        "width": 0
                    },
                    "author": {
                        "name": player["name"]
                    }
                }
            ]
        }),
        headers={
            "Content-Type": "application/json"
        }
    )

def send_discord_joined(player):
    global DISCORD_WEBHOOK

    requests.post(
        DISCORD_WEBHOOK,
        data=json.dumps({
            "embeds": [
                {
                    "type": "rich",
                    "title": "",
                    "description": f"{player['name']} joined!",
                    "color": 7774208,
                    "thumbnail": {
                        "url": player["image"],
                        "height": 0,
                        "width": 0
                    },
                    "author": {
                        "name": player["name"]
                    }
                }
            ]
        }),
        headers={
            "Content-Type": "application/json"
        }
    )

def send_discord_message(message):
    global DISCORD_WEBHOOK

    requests.post(
        DISCORD_WEBHOOK,
        data=json.dumps({
            "content": message
        }),
        headers={
            "Content-Type": "application/json"
        }
    )

def send_discord_embed(title):
    global DISCORD_WEBHOOK

    requests.post(
        DISCORD_WEBHOOK,
        data=json.dumps({
            "embeds": [
                {
                    "title": title,
                    "color": 7774208
                }
            ]
        }),
        headers={
            "Content-Type": "application/json"
        }
    )

async def client():
    global PUSHER_WEBSOCKET_URL, LOCAL_USER
    async with websockets.connect(PUSHER_WEBSOCKET_URL) as websocket:
        try:
            await websocket.send(json.dumps({
                'event': 'pusher:subscribe',
                'data': {
                    'channel': 'lan-party'
                }
            }))

            print('Heartbeat server is running...')
            send_discord_embed("New session has started!")

            async for message in websocket:
                data = json.loads(message)
                body = json.loads(data['data'])

                if data['event'] == 'heartbeat':
                    handle_ping(body['from'], body['image'])
        finally:
            await websocket.close()

print('Starting a connection...')
asyncio.run(client())
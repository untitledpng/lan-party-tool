import os
from dotenv import load_dotenv
import asyncio
import keyboard
import websockets
import json
import datetime

load_dotenv()

# Define your Pusher app credentials
PUSHER_APP_KEY = os.getenv('PUSHER_KEY')
PUSHER_CLUSTER = os.getenv('PUSHER_CLUSTER')
PUSHER_WEBSOCKET_URL = f'wss://ws-{PUSHER_CLUSTER}.pusher.com/app/{PUSHER_APP_KEY}?client=js&version=7.0.3&protocol=5'
LOCAL_USER = os.getenv('LOCAL_USER')
NVIDIA_KEY_COMBO = os.getenv('NVIDIA_KEY_COMBO')

def save_replay(name):
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f'[{formatted_time}] Replay saved by {name}!')
    keyboard.press_and_release(NVIDIA_KEY_COMBO)

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

            print('Server is running...')

            async for message in websocket:
                data = json.loads(message)
                body = json.loads(data['data'])

                if data['event'] == 'save-replay' and body['from'] != LOCAL_USER:
                    save_replay(body['from'])
        finally:
            await websocket.close()

print('Starting a connection...')
asyncio.run(client())
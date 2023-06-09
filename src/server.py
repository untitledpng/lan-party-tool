import pusher
import keyboard
import datetime
import time
import mss
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

NVIDIA_KEY_COMBO = os.getenv('NVIDIA_KEY_COMBO')
IS_SENDING = False
LOCAL_USER = os.getenv('LOCAL_USER')
LOCAL_USER_IMAGE = os.getenv('LOCAL_USER_IMAGE')
IMGBB_API_KEY = os.getenv('IMGBB_API_KEY')
DISCORD_WEBHOOK = os.getenv('DISCORD_WEBHOOK')
LOCK_FILE = "./lockfile.lock"

pusher_client = pusher.Pusher(
    app_id=os.getenv('PUSHER_APP_ID'),
    key=os.getenv('PUSHER_KEY'),
    secret=os.getenv('PUSHER_SECRET'),
    cluster=os.getenv('PUSHER_CLUSTER'),
    ssl=os.getenv('PUSHER_SSL', True)
)

if os.path.exists(LOCK_FILE):
    os.remove(LOCK_FILE)

def send_save_replay():
    global IS_SENDING, LOCAL_USER, LOCK_FILE

    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
        return

    if IS_SENDING:
        return

    IS_SENDING = True
    now = datetime.datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

    print(f'[{formatted_time}] Sending save replay to the others...')
    pusher_client.trigger('lan-party', 'save-replay', {'from': LOCAL_USER})
    screenshot()

    time.sleep(5)
    IS_SENDING = False

def screenshot():
    with mss.mss() as sct:
        sct.shot(output="last_screenshot.png")

    url = "https://api.imgbb.com/1/upload"
    payload = {"key": IMGBB_API_KEY}
    files = {"image": open("./last_screenshot.png", "rb")}
    response = requests.post(url, payload, files=files)

    json_response = json.loads(response.text)
    img_url = json_response["data"]["url"]

    print("Screenshot uploaded to: " + img_url)
    send_discord_screenshot(img_url)

def send_discord_screenshot(image_url):
    global DISCORD_WEBHOOK, LOCAL_USER, LOCAL_USER_IMAGE

    requests.post(
        DISCORD_WEBHOOK,
        data=json.dumps({
            "embeds": [
                {
                    "type": "rich",
                    "title": "",
                    "description": f"{LOCAL_USER} saved a clip!",
                    "color": 7774208,
                    "thumbnail": {
                        "url": LOCAL_USER_IMAGE,
                        "height": 0,
                        "width": 0
                    },
                    "image": {
                        "url": image_url,
                        "height": 0,
                        "width": 0
                    },
                    "author": {
                        "name": LOCAL_USER
                    }
                }
            ]
        }),
        headers={
            "Content-Type": "application/json"
        }
    )

# Set up the hotkey listener for the ALT+F10 key combination
keyboard.add_hotkey(NVIDIA_KEY_COMBO, send_save_replay)

# Keep the script running to listen for key presses
keyboard.wait()
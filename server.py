import os
from dotenv import load_dotenv
import pusher
import keyboard
import datetime
import time

load_dotenv()

NVIDIA_KEY_COMBO = os.getenv('NVIDIA_KEY_COMBO')
IS_SENDING = False
LOCAL_USER = os.getenv('LOCAL_USER')

pusher_client = pusher.Pusher(
  app_id=os.getenv('PUSHER_APP_ID'),
  key=os.getenv('PUSHER_KEY'),
  secret=os.getenv('PUSHER_SECRET'),
  cluster=os.getenv('PUSHER_CLUSTER'),
  ssl=os.getenv('PUSHER_SSL', True)
)

def send_save_replay():
  global IS_SENDING, LOCAL_USER

  if IS_SENDING:
    return

  IS_SENDING = True
  now = datetime.datetime.now()
  formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

  print(f'[{formatted_time}] Sending save replay to the others...')
  pusher_client.trigger('lan-party', 'save-replay', {'from': LOCAL_USER})

  time.sleep(5)
  IS_SENDING = False

# Set up the hotkey listener for the ALT+F10 key combination
keyboard.add_hotkey(NVIDIA_KEY_COMBO, send_save_replay)

# Keep the script running to listen for key presses
keyboard.wait()
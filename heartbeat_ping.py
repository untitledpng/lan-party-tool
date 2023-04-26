import os
from dotenv import load_dotenv
import pusher
import time

load_dotenv()

HEARTBEAT_TIMEOUT = int(os.getenv('HEARTBEAT_TIMEOUT'))
LOCAL_USER = os.getenv('LOCAL_USER')
LOCAL_USER_IMAGE = os.getenv('LOCAL_USER_IMAGE')

pusher_client = pusher.Pusher(
  app_id=os.getenv('PUSHER_APP_ID'),
  key=os.getenv('PUSHER_KEY'),
  secret=os.getenv('PUSHER_SECRET'),
  cluster=os.getenv('PUSHER_CLUSTER'),
  ssl=os.getenv('PUSHER_SSL', True)
)

while True:
    pusher_client.trigger('lan-party', 'heartbeat', {'from': LOCAL_USER, 'image': LOCAL_USER_IMAGE})
    time.sleep(HEARTBEAT_TIMEOUT)

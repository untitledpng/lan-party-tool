import threading
import subprocess
import os
import time
from dotenv import load_dotenv

load_dotenv()

python_executable = os.getenv('PYTHON_EXECUTABLE')

def run_client():
    while True:
        try:
            subprocess.call([python_executable, 'client.py'])
        except subprocess.CalledProcessError:
            print('client.py subprocess crashed. Restarting...')
        time.sleep(1)

def run_server():
    while True:
        try:
            subprocess.call([python_executable, 'server.py'])
        except subprocess.CalledProcessError:
            print('server.py subprocess crashed. Restarting...')
        time.sleep(1)

def run_heartbeat_ping():
    while True:
        try:
            subprocess.call([python_executable, 'heartbeat_ping.py'])
        except subprocess.CalledProcessError:
            print('heartbeat_ping.py subprocess crashed. Restarting...')
        time.sleep(1)

def run_heartbeat_server():
    while True:
        try:
            subprocess.call([python_executable, 'heartbeat_server.py'])
        except subprocess.CalledProcessError:
            print('heartbeat_server.py subprocess crashed. Restarting...')
        time.sleep(1)

def run_free_file_sync():
    if os.path.exists('./SyncSettings.ffs_batch'):
        while True:
            try:
                subprocess.call('SyncSettings.ffs_batch', shell=True)
            except subprocess.CalledProcessError:
                print('SyncSettings.ffs_batch subprocess crashed. Restarting...')
            time.sleep(30*60)
    else:
        print('NO SyncSettings.ffs_batch FILE FOUND!')

# Create two threads to run each script
thread1 = threading.Thread(target=run_client)
thread2 = threading.Thread(target=run_server)
thread3 = threading.Thread(target=run_heartbeat_ping)
thread4 = threading.Thread(target=run_heartbeat_server)
thread5 = threading.Thread(target=run_free_file_sync)

# Start both threads
thread1.start()
thread2.start()
thread3.start()
if os.getenv('LOCAL_USER') == 'UNTITLED_PNG':
    thread4.start()
thread5.start()

# Wait for both threads to finish
thread1.join()
thread2.join()
thread3.join()
if os.getenv('LOCAL_USER') == 'UNTITLED_PNG':
    thread4.join()
thread5.join()

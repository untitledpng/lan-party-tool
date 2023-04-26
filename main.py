import threading
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

python_executable = os.getenv('PYTHON_EXECUTABLE')

def run_client():
    subprocess.call([python_executable, 'client.py'])

def run_server():
    subprocess.call([python_executable, 'server.py'])

def run_heartbeat_ping():
    subprocess.call([python_executable, 'heartbeat_ping.py'])

def run_heartbeat_server():
    subprocess.call([python_executable, 'heartbeat_server.py'])

# Create two threads to run each script
thread1 = threading.Thread(target=run_client)
thread2 = threading.Thread(target=run_server)
thread3 = threading.Thread(target=run_heartbeat_ping)
thread4 = threading.Thread(target=run_heartbeat_server())

# Start both threads
thread1.start()
thread2.start()
thread3.start()
if os.getenv('LOCAL_USER') == 'UNTITLED_PNG':
    thread4.start()

# Wait for both threads to finish
thread1.join()
thread2.join()
thread3.join()
if os.getenv('LOCAL_USER') == 'UNTITLED_PNG':
    thread4.join()

import mss
from PIL import Image
import io
import requests
import json

# Take a fullscreen screenshot
with mss.mss() as sct:
    # Get information about the primary monitor
    monitor = sct.monitors[1]

    # Capture the entire screen
    screenshot = sct.grab(monitor)

# Convert the screenshot to a PIL Image object
img = Image.frombytes("RGB", screenshot.size, screenshot.raw, "raw", "BGRX")

# Save the screenshot to disk
buffer = io.BytesIO()
img.save(buffer, format="PNG")
with open("screenshot.png", "wb") as f:
    f.write(buffer.getvalue())

# Upload the screenshot to ImgBB
url = "https://api.imgbb.com/1/upload"
payload = {"key": "5d9ea6d179e4f93e8f506c7cb0db55d3"}
files = {"image": open("screenshot.png", "rb")}
response = requests.post(url, payload, files=files)

# Parse the JSON response to get the URL of the uploaded image
json_response = json.loads(response.text)
img_url = json_response["data"]["url"]

# Print the URL of the uploaded image
print("Screenshot uploaded to: " + img_url)

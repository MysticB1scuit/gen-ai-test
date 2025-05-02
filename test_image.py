import requests

url = "http://127.0.0.1:5000/generate-image"
payload = {"text": "a majestic lion in the savannah"}

print("[CLIENT] Sending request to Flask server...")

try:
    response = requests.post(url, json=payload)
    print("[CLIENT] Got response!")
    print(response.json())
except Exception as e:
    print("[CLIENT] ERROR:", e)
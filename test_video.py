import requests

response = requests.post("http://127.0.0.1:5000/generate-video", json={"text": "a futuristic city at night"})
print(response.json())
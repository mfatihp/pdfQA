import requests


message = {"text": "What can you say about video anomaly detection?"}


response = requests.post("http://127.0.0.1:8000/answer", json=message)

print(response.json())
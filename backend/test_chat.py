import requests
import json

url = 'http://localhost:5001/chat'

payload = {
    "message": "What skills should I learn?",
    "context": {
        "profile_name": "Technical Expert",
        "roles": "Data Scientist, ML Engineer",
        "technical_score": 4
    }
}

try:
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        print("Chat successful!")
        print("Response:", response.json().get('response'))
    else:
        print(f"Error: {response.status_code} - {response.text}")
except Exception as e:
    print(f"Request failed: {e}")

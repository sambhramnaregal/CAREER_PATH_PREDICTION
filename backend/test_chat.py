import requests
import json

url = 'http://localhost:5002/chat'
data = {
    "message": "What roles are good for me?",
    "context": {
        "profile_name": "Entrepreneurial Track",
        "roles": "Startup Founder, Product Owner"
    }
}

try:
    print(f"Sending chat request to {url}...")
    response = requests.post(url, json=data)
    print(f"Status Code: {response.status_code}")
    print("Response:", response.text)
except Exception as e:
    print(f"Request failed: {e}")

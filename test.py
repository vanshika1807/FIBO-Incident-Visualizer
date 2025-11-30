import requests
from config.settings import BRIA_API_KEY

headers = {
    "api_token": f"{BRIA_API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "prompt": "Test image for incident dashboard",
    "size": "512x512"
}

resp = requests.post("https://engine.prod.bria-api.com/v2/image/generate", headers=headers, json=payload)
print("Status:", resp.status_code)
print("Response:", resp.text)

# fibo_client.py
import requests
import time
import os
from config.settings import BRIA_API_KEY

BASE_URL = "https://engine.prod.bria-api.com/v2"

def generate_fibo_image(payload, wait_for_completion=True, poll_interval=2):
    """
    Sends a request to BRIA FIBO API and polls until the image is ready.
    Returns the local file path of the downloaded image or None on failure.
    """
    headers = {
        "api_token": f"{BRIA_API_KEY}".strip(),
        "Content-Type": "application/json"
    }

    # Step 1: Submit request
    response = requests.post(f"{BASE_URL}/image/generate", headers=headers, json=payload)

    if response.status_code != 202:
        print(f"❌ API request failed: {response.status_code} {response.text}")
        return None

    result = response.json()
    request_id = result.get("request_id")
    status_url = result.get("status_url")

    if not request_id or not status_url:
        print("❌ Missing request_id or status_url in response")
        return None

    if not wait_for_completion:
        return status_url

    # Step 2: Poll for completion
    print(f"⏳ Polling for completion (request_id: {request_id})...")
    while True:
        status_resp = requests.get(status_url, headers=headers)
        if status_resp.status_code != 200:
            print("❌ Failed to fetch status:", status_resp.text)
            return None
        
        status_data = status_resp.json()
        status = status_data.get("status")

        if status == "COMPLETED":
            image_url = status_data.get("result", {}).get("image_url")
            if not image_url:
                print("❌ No image URL returned")
                return None
            
            # Step 3: Download image
            os.makedirs("output/images", exist_ok=True)
            local_path = os.path.join("output","images", "incident.png")
            img_data = requests.get(image_url).content
            with open(local_path, "wb") as f:
                f.write(img_data)
            
            print(f"✅ Image saved at: {local_path}")
            return local_path

        elif status == "ERROR":
            print("❌ Image generation failed:", status_data.get("error"))
            return None

        else:
            print(f"Status: {status}, retrying in {poll_interval}s...")
            time.sleep(poll_interval)


# -------------------------
# TEST RUNNER
# -------------------------
if __name__ == "__main__":
    from parser import parse_log_text
    from json_builder import build_fibo_payload

    test_log = "Users are not able to login to SmartStation in DEV after deployment."

    parsed = parse_log_text(test_log)
    payload = build_fibo_payload(parsed)
    payload["size"] = "1024x1024"  # optional
    payload["prompt"] = payload.get("prompt", "Generate a dashboard-ready incident image")  # ensure prompt exists

    generate_fibo_image(payload)

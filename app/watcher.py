import time
import os
import json
from datetime import datetime
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from app.parser import parse_log_text
from app.json_builder import build_fibo_payload
from app.fibo_client import generate_fibo_image

LOG_FILE = "examples/sample_logs.txt"
BACKEND_URL = "https://your-render-backend.onrender.com"  # <- Replace with your backend URL

last_position = 0

class LogChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global last_position

        if event.src_path.endswith(LOG_FILE.replace("/", "\\")):
            print("\n📌 CHANGE DETECTED in log file!")

            try:
                with open(LOG_FILE, "r") as f:
                    f.seek(last_position)
                    new_data = f.read()
                    last_position = f.tell()
            except Exception as e:
                print(f"❌ Error reading log file: {e}")
                return

            if not new_data.strip():
                print("⚠ No new log data appended.")
                return

            parsed = parse_log_text(new_data)
            payload = build_fibo_payload(parsed)
            payload["size"] = "1024x1024"
            payload.setdefault("prompt", parsed.get("issue", "Unknown incident"))

            print("🚀 Generating image via FIBO...")
            image_path = generate_fibo_image(payload)

            if not image_path or not os.path.exists(image_path):
                print("❌ Image generation failed, skipping upload.")
                return

            # --------------------------
            # Upload incident to backend
            # --------------------------
            files = {
                "metadata": ("incident.json", json.dumps(parsed), "application/json"),
                "image": ("image.png", open(image_path, "rb"), "image/png")
            }

            try:
                resp = requests.post(f"{BACKEND_URL}/upload", files=files)
                if resp.status_code == 200:
                    print("✅ Incident uploaded successfully to backend!")
                    os.remove(image_path)  # optional: remove local temp image
                else:
                    print(f"❌ Backend upload failed: {resp.status_code}, {resp.text}")
            except Exception as e:
                print(f"❌ Error uploading to backend: {e}")

def start_watcher():
    global last_position
    print("👀 Watching log file for appended text…")

    try:
        with open(LOG_FILE, "r") as f:
            f.seek(0, 2)
            last_position = f.tell()
    except FileNotFoundError:
        print("❌ Log file not found:", LOG_FILE)
        return

    event_handler = LogChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path="examples", recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    start_watcher()

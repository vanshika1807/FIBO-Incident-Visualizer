# watcher.py
import time
import os
import json
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from app.api_server import generate_endpoint
from app.parser import parse_log_text
from app.json_builder import build_fibo_payload
from app.fibo_client import generate_fibo_image


LOG_FILE = "examples/sample_logs.txt"

# Keep track of last file size (cursor)
last_position = 0


class LogChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        global last_position

        # Ensure we detect only the sample_logs.txt file
        if event.src_path.endswith(LOG_FILE.replace("/", "\\")):
            print("\n📌 CHANGE DETECTED in log file!")

            # Read newly added text
            try:
                with open(LOG_FILE, "r") as f:
                    f.seek(last_position)          # Jump to last read point
                    new_data = f.read()            # Read appended text
                    last_position = f.tell()       # Update cursor
            except Exception as e:
                print(f"❌ Error reading log file: {e}")
                return

            if not new_data.strip():
                print("⚠ No new log data appended.")
                return

            print("📝 New Log Block Detected:")
            print(new_data.strip())

            # -----------------------------------
            # Parse log and build FIBO payload
            # -----------------------------------
            parsed = parse_log_text(new_data)
            payload = build_fibo_payload(parsed)

            # Set image size (can be changed later)
            payload["size"] = "1024x1024"

            # Default prompt if missing
            payload.setdefault("prompt", parsed.get("issue", "Unknown incident"))

            print("🚀 Sending to BRIA for image generation...")
            image_path = generate_fibo_image(payload)

            # -----------------------------------
            # Save incident locally (JSON + image)
            # -----------------------------------
            timestamp_folder = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            incident_dir = os.path.join("incidents", timestamp_folder)
            os.makedirs(incident_dir, exist_ok=True)

            # Save metadata JSON
            with open(os.path.join(incident_dir, "incident.json"), "w") as f:
                json.dump(parsed, f, indent=4)

            # Move image if it exists
            if image_path and os.path.exists(image_path):
                new_image_path = os.path.join(incident_dir, "image.png")
                os.rename(image_path, new_image_path)
                print(f"🖼️ Image saved: {new_image_path}")

            print(f"📦 Incident stored in: {incident_dir}\n")


def start_watcher():
    global last_position

    print("👀 Watching log file for appended text…")

    # Move cursor to end of file so old logs are not processed
    try:
        with open(LOG_FILE, "r") as f:
            f.seek(0, 2)  # Move to end
            last_position = f.tell()
    except FileNotFoundError:
        print("❌ Log file not found. Create this file first:")
        print(LOG_FILE)
        return

    # Set up watchdog
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

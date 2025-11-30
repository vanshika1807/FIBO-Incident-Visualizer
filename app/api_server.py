# api_server.py
import os
import json
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from app.fibo_client import generate_fibo_image
from app.parser import parse_log_text
from app.json_builder import build_fibo_payload

app = FastAPI()

INCIDENTS_DIR = "incidents"


@app.get("/")
def root():
    return {"message": "FIBO Incident Visualizer API Running"}


# ----------------------------------------------------
# 1️⃣ List all incidents
# ----------------------------------------------------
@app.get("/incidents")
def list_incidents():
    if not os.path.exists(INCIDENTS_DIR):
        return []

    incidents = sorted(os.listdir(INCIDENTS_DIR))
    return {"incidents": incidents}


# ----------------------------------------------------
# 2️⃣ Get incident metadata
# ----------------------------------------------------
@app.get("/incidents/{incident_id}")
def get_incident(incident_id: str):
    folder = os.path.join(INCIDENTS_DIR, incident_id)
    metadata_file = os.path.join(folder, "incident.json")

    if not os.path.exists(metadata_file):
        raise HTTPException(status_code=404, detail="Incident not found")

    with open(metadata_file, "r") as f:
        metadata = json.load(f)

    return metadata


# ----------------------------------------------------
# 3️⃣ Get incident image
# ----------------------------------------------------
@app.get("/incidents/{incident_id}/image")
def get_incident_image(incident_id: str):
    folder = os.path.join(INCIDENTS_DIR, incident_id)
    img_path = os.path.join(folder, "image.png")

    if not os.path.exists(img_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(img_path)


# ----------------------------------------------------
# 4️⃣ Manually generate image (optional)
# ----------------------------------------------------
@app.post("/generate")
def manual_generate(prompt: str):
    fake_log = f"Issue detected: {prompt}"

    parsed = parse_log_text(fake_log)
    payload = build_fibo_payload(parsed)
    payload["prompt"] = prompt
    payload["size"] = "1024x1024"

    image_path = generate_fibo_image(payload)

    return {
        "status": "ok",
        "image_path": image_path
    }

# api_server.py
import os
import time
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from parser import parse_log_text
from json_builder import build_fibo_payload
from config.settings import BRIA_API_KEY

# Fibo client helper (lightweight proxy for async flow)
BASE_URL = "https://engine.prod.bria-api.com/v2"
HEADERS = {
    "api_token": f"{BRIA_API_KEY}".strip(),
    "Content-Type": "application/json"
}

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # for demo; restrict for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store: request_id -> status_url
request_store: dict[str, str] = {}

class GenerateRequest(BaseModel):
    log_text: str
    size: str | None = "1024x1024"

@app.post("/generate")
def generate_endpoint(req: GenerateRequest):
    # 1. parse log and build JSON payload
    parsed = parse_log_text(req.log_text)
    payload = build_fibo_payload(parsed)
    payload["size"] = req.size or "1024x1024"
    # enrich with visual params
    payload.setdefault("camera_angle", "top-down")
    payload.setdefault("layout", "dashboard")
    payload.setdefault("color_palette", "red highlights for critical, neutral bg")
    # ensure prompt exists
    if "prompt" not in payload or not payload["prompt"]:
        payload["prompt"] = (
            f"Generate a clean professional dashboard-style visualization for "
            f"{parsed.get('service')} incident in {parsed.get('environment')} "
            f"with severity {parsed.get('severity')}. Highlight: {parsed.get('issue')}."
        )

    # 2. submit to Bria (async)
    resp = requests.post(f"{BASE_URL}/image/generate", headers=HEADERS, json=payload)
    if resp.status_code != 202:
        raise HTTPException(status_code=500, detail={"bria_error": resp.text, "status": resp.status_code})

    data = resp.json()
    request_id = data.get("request_id")
    status_url = data.get("status_url")
    if not request_id or not status_url:
        raise HTTPException(status_code=500, detail="Missing request_id or status_url in Bria response")

    # store mapping so frontend can poll /status/{request_id}
    request_store[request_id] = status_url
    return {"request_id": request_id}

@app.get("/status/{request_id}")
def status_endpoint(request_id: str):
    status_url = request_store.get(request_id)
    if not status_url:
        raise HTTPException(status_code=404, detail="Unknown request_id")

    resp = requests.get(status_url, headers=HEADERS)
    if resp.status_code != 200:
        raise HTTPException(status_code=502, detail={"bria_status": resp.status_code, "text": resp.text})

    data = resp.json()
    # Return trimmed info
    return {
        "status": data.get("status"),
        "request_id": request_id,
        "result": data.get("result"),  # includes image_url when COMPLETED
        "error": data.get("error")
    }

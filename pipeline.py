# pipeline.py
import uuid
import json
from datetime import datetime
from parser import parse_log_text
from json_builder import build_fibo_payload
from fibo_client import generate_fibo_image
import os

def process_incident_log(raw_text: str) -> dict:
    """
    Full pipeline:
    - normalize (handled by parser)
    - parse data
    - build JSON payload
    - send to Bria FIBO
    - store JSON report + image
    - return metadata for frontend
    """

    incident_id = str(uuid.uuid4())[:8]

    parsed = parse_log_text(raw_text)
    payload = build_fibo_payload(parsed)
    payload["size"] = "1024x1024"

    # Ensure prompt exists
    if "prompt" not in payload:
        payload["prompt"] = f"Generate dashboard incident visualization for service {parsed.get('service')}"

    # Generate image
    image_path = generate_fibo_image(payload)

    # Store JSON report
    os.makedirs("output/reports", exist_ok=True)
    report_path = f"output/reports/incident_{incident_id}.json"

    report = {
        "incident_id": incident_id,
        "timestamp": datetime.now().isoformat(),
        "raw_log": raw_text,
        "parsed": parsed,
        "payload": payload,
        "image_path": image_path
    }

    with open(report_path, "w") as f:
        json.dump(report, f, indent=4)

    return report

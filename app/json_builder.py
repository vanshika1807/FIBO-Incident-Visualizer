# json_builder.py

def build_fibo_payload(parsed_incident: dict) -> dict:
    """
    Convert parsed incident data into a structured JSON payload
    ready for BRIA / FIBO AI processing.
    """

    service = parsed_incident.get("service")
    environment = parsed_incident.get("environment")
    severity = parsed_incident.get("severity")
    issue = parsed_incident.get("issue")
    timestamp = parsed_incident.get("timestamp")

    # AI Prompt to generate visualization / description
    prompt = (
        f"Summarize this incident professionally:\n"
        f"- Service: {service}\n"
        f"- Environment: {environment}\n"
        f"- Severity: {severity}\n"
        f"- Issue: {issue}\n"
        f"- Timestamp: {timestamp}\n"
        f"Then generate a clean incident visual description for dashboard representation."
    )

    return {
        "incident_summary": issue,
        "service": service,
        "environment": environment,
        "severity": severity,
        "timestamp": timestamp,
        "prompt": prompt
    }

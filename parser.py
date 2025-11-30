# parser.py
import re
from datetime import datetime
from autocorrect import Speller

# initialize English spell corrector once
speller = Speller(lang='en')

def clean_text(text: str) -> str:
    """
    Basic whitespace cleanup and removal of control characters.
    """
    if not text:
        return text
    # replace \r and other control chars with space
    cleaned = re.sub(r'[\r\t]+', ' ', text)
    # collapse multiple spaces/newlines to single space where appropriate
    cleaned = re.sub(r'\n\s*\n+', '\n', cleaned)  # preserve single newlines
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)
    return cleaned.strip()

def normalize_spellings(text: str) -> str:
    """
    Run a lightweight spelling correction on the whole text.
    Note: autocorrect works token-by-token; it may change some acronyms.
    """
    if not text:
        return text
    cleaned = clean_text(text)
    # We'll correct line-by-line so we keep structure
    lines = cleaned.splitlines()
    corrected_lines = []
    for line in lines:
        # only correct if line has alphabetical characters
        if re.search(r'[A-Za-z]', line):
            corrected = speller(line)
            corrected_lines.append(corrected)
        else:
            corrected_lines.append(line)
    return "\n".join(corrected_lines)

def parse_log_text(text: str) -> dict:
    """
    Parse raw incident log text and extract:
    - service
    - environment
    - severity
    - issue summary
    - timestamp
    This function now normalizes spellings before parsing.
    """

    # Normalize + correct spelling first
    normalized_text = normalize_spellings(text)
    t = normalized_text.lower()

    # SERVICE detection
    service_keywords = {
        "smartstation": "SmartStation",
        "ss": "SmartStation",
        "ag": "Advisor Gateway",
        "advisor gateway": "Advisor Gateway",
        "ping": "Ping Service",
        "bits": "BITS System",
        "oits": "OITS System"
    }
    service = "Unknown"
    for key, val in service_keywords.items():
        if key in t:
            service = val
            break

    # ENVIRONMENT detection
    env_keywords = ["dev", "cte", "ite", "pte", "prod"]
    environment = next((env.upper() for env in env_keywords if env in t), "UNKNOWN")

    # ISSUE summary extraction - take first non-empty line
    lines = [ln.strip() for ln in normalized_text.splitlines() if ln.strip()]
    first_line = lines[0] if lines else normalized_text.strip()
    issue = first_line.strip().capitalize()

    # SEVERITY detection
    severity = "Low"
    if any(word in t for word in ["down", "not able", "error", "critical", "fail", "failure"]):
        severity = "High"
    if "sev 2" in t or "sev2" in t:
        severity = "Sev2"
    if "sev 1" in t or "sev1" in t:
        severity = "Sev1"

    # TIMESTAMP
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return {
        "service": service,
        "environment": environment,
        "issue": issue,
        "severity": severity,
        "timestamp": timestamp
    }

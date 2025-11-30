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
    Spell-correct normal English but protect product names and force-correct
    commonly misspelled service terms.
    """

    TECH_TERMS = {
        "smart station": "SmartStation",
        "smartstation": "SmartStation",
        "smart sttaion": "SmartStation",
        "smrtstation": "SmartStation",
        "ss": "SS",

        "advisor gateway": "Advisor Gateway",
        "advicer gateway": "Advisor Gateway",
        "ag": "AG",

        "bits": "BITS",
        "oits": "OITS",
        "ping": "Ping Service"
    }

    cleaned = clean_text(text)
    lines = cleaned.splitlines()
    corrected_lines = []

    for line in lines:
        words = line.split()

        new_words = []
        for w in words:
            lw = w.lower()

            # 1) If word matches tech term → force correct it
            if lw in TECH_TERMS:
                new_words.append(TECH_TERMS[lw])
                continue

            # 2) If the word LOOKS like part of "SmartStation" pattern
            if "smart" in lw or "station" in lw or "sttaion" in lw:
                new_words.append("SmartStation")
                continue

            # 3) Otherwise apply normal autocorrect
            corrected = speller(w)
            new_words.append(corrected)

        corrected_lines.append(" ".join(new_words))

    # After correcting, run phrase-based replacement also (handles multi-word phrases)
    final_text = "\n".join(corrected_lines).lower()

    for wrong, correct in TECH_TERMS.items():
        final_text = final_text.replace(wrong, correct)

    return final_text


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

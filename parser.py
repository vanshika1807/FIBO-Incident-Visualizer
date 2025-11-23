# parser.py
import re

def parse_logs(raw_text):
    """
    Parse raw logs into structured incidents.
    Expected log format: [ENV] SERVICE: Issue description - Severity LEVEL
    """
    incidents = []
    lines = raw_text.splitlines()

    # Regex to extract environment, service, issue, severity
    log_pattern = re.compile(r'\[(.*?)\]\s+(\w+):\s+(.*)\s+-\s+Severity\s+(.*)', re.IGNORECASE)

    for line in lines:
        match = log_pattern.match(line)
        if match:
            env, service, issue, severity = match.groups()
            incidents.append({
                'environment': env.strip(),
                'service': service.strip(),
                'issue': issue.strip(),
                'severity': severity.strip()
            })
    return incidents

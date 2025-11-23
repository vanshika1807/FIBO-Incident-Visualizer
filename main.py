# main.py (for testing parser)
from parser import parse_logs

with open('examples/sample_logs.txt') as f:
    raw_logs = f.read()

parsed = parse_logs(raw_logs)
for i, incident in enumerate(parsed, 1):
    print(f"Incident {i}: {incident}")
S
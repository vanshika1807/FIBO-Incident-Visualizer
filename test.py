# test_parser.py
from parser import parse_log_text

bad_log = "Useers are not able to login to SmartSttaion in DEV after deploymnt.\nWe see 500 erreors and intermittent timouts."

parsed = parse_log_text(bad_log)
print(parsed)

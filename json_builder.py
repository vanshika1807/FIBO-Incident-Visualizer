# json_builder.py
def build_fibo_json(parsed_logs):
    """
    Convert parsed logs into FIBO JSON format.
    """
    return {
        'nodes': parsed_logs,
        'relationships': []  # You can add later based on incident relations
    }

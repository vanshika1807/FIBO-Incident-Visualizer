# fibo_client.py
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('FIBO_API_KEY')

def send_to_fibo(json_payload):
    """
    Simulate sending JSON to FIBO API.
    Saves dummy image in output/images/.
    """
    os.makedirs('output/images', exist_ok=True)
    dummy_path = 'output/images/fibo.png'
    with open(dummy_path, 'wb') as f:
        f.write(b'Dummy image content')  # Placeholder
    print("✅ Payload sent to FIBO (simulated)")
    return dummy_path

from dotenv import load_dotenv
import os

load_dotenv()

BRIA_API_KEY = os.getenv("BRIA_API_KEY").strip()
print(BRIA_API_KEY)

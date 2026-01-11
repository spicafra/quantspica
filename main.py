import os
from dotenv import load_dotenv

# Load keys from .env
load_dotenv()

ALPACA_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET = os.getenv("ALPACA_API_SECRET")

print("Loaded Alpaca key length:", len(ALPACA_KEY))
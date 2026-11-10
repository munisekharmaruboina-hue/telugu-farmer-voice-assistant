import os
from dotenv import load_dotenv

load_dotenv()

GNANI_API_KEY = os.getenv("GNANI_API_KEY")
DATA_GOV_API_KEY = os.getenv("DATA_GOV_API_KEY")

if not GNANI_API_KEY:
    raise RuntimeError("GNANI_API_KEY missing. Add it to your .env file.")
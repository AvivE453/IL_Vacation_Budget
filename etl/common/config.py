# Loads config/secrets from .env into these constants - imported by both
# app/ and etl/ code that needs the DB URL or an API key.

import os

from dotenv import load_dotenv

load_dotenv()

DB_URL = os.environ["DB_URL"]
TRAVELPAYOUTS_TOKEN = os.environ.get("TRAVELPAYOUTS_TOKEN", "")
TRAVELPAYOUTS_MARKER = os.environ.get("TRAVELPAYOUTS_MARKER", "")
SERPAPI_KEY = os.environ.get("SERPAPI_KEY", "")
FLASK_SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "")

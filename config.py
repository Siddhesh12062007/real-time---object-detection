"""Central configuration. Secrets are read from environment / .env (never hardcoded)."""
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "database": os.getenv("DB_NAME", "vision_platform"),
}

MODEL_PATH = "yolov8n.pt"      # downloaded automatically on first run
DEFAULT_CONFIDENCE = 0.70      # only log/draw objects above 70%
LOG_COOLDOWN_SECONDS = 2.0     # per-class cooldown so the DB is not flooded
RECENT_LOGS_LIMIT = 15

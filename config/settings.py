"""Centralized settings for tests (env + logging)."""
from __future__ import annotations
import os
from dataclasses import dataclass
from dotenv import load_dotenv
import logging
import logging.config
import yaml


load_dotenv()

LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(LOG_DIR, exist_ok=True)


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "http://localhost:5173")
    session_minutes: int = int(os.getenv("SESSION_MINUTES", "30"))
    headless: bool = os.getenv("HEADLESS", "1") == "1"


settings = Settings()

with open(os.path.join(os.path.dirname(__file__), "logging.yaml"), "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger(__name__)
logger.info("Test settings loaded: base_url=%s, session=%s min, headless=%s", settings.base_url, settings.session_minutes, settings.headless)
